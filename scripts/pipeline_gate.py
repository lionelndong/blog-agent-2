#!/usr/bin/env python3
"""Hard-fail gate for the blog pipeline.

The orchestrator must call this between every stage transition. Exit code 0
means the named stage's outputs are complete and consistent. Non-zero means
HALT: a clear failure summary is printed to stderr and the orchestrator must
NOT advance to the next stage.

Why: the pipeline used to mark stages "done" because the script exited 0,
even when the actual deliverable was missing or contained placeholder text.
Neo (PLEAA-392 2026-05-06): "we cannot skip steps. If something is missing
we stop and fix it before moving on."

Usage:
    python scripts/pipeline_gate.py <stage-key> <slug>

Stage keys mirror the pipeline stages:
    research              — 1-research/{slug}.md exists and is non-trivial
    research-adversarial  — quality-checks/{slug}-research-adversarial.md
                            verdict PASS, OR FAIL with revision budget
                            remaining (orchestrator must re-run /research)
    reference             — 2-reference/{slug}.md exists
    outline               — 3-outlines/{slug}.md exists
    outline-adversarial   — quality-checks/{slug}-outline-adversarial.md
                            verdict PASS, OR FAIL with budget remaining
    annotated             — 4-outlines-annotated/{slug}.md exists
    draft                 — 5-drafts/{slug}.md exists and has H2 sections
    cited                 — 6-drafts-cited/{slug}.md exists
    visuals               — images/{slug}/manifest.json exists, no `manual` or
                            `failed` entries remain, AND the cited draft
                            contains no naked `[VISUAL:...]` placeholders
    visuals-adversarial   — quality-checks/{slug}-visuals-adversarial.md
                            verdict PASS, OR FAIL with budget remaining
    quality               — quality-checks/{slug}.md exists with verdict PASS
                            or BORDERLINE-no-CRITICAL
    preview               — 7-preview/{slug}.html exists
    publish         — 8-publish/{slug}/{article.md, article.json, README.md}
                      all exist, no naked [VISUAL:...] in article.md
    deliverable     — for an issue-driven run: verify a comment with the
                      slug + verdict was posted to PAPERCLIP_TASK_ID

Exit codes:
    0   — gate passed
    1   — gate failed (output incomplete; halt and fix)
    64  — usage error
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CP = REPO_ROOT / "content-pipeline"

VISUAL_PLACEHOLDER_RE = re.compile(r"\[VISUAL:[^\]]+\]|\[SCREENSHOT:[^\]]+\]")


def fail(reason: str, *details: str) -> int:
    print(f"GATE FAIL: {reason}", file=sys.stderr)
    for d in details:
        print(f"  · {d}", file=sys.stderr)
    return 1


def ok(stage: str, slug: str, *details: str) -> int:
    print(f"GATE PASS: {stage} for {slug}")
    for d in details:
        print(f"  · {d}")
    return 0


def must_exist(path: Path, min_bytes: int = 1) -> str | None:
    if not path.exists():
        return f"missing: {path.relative_to(REPO_ROOT)}"
    if path.stat().st_size < min_bytes:
        return f"too small ({path.stat().st_size}B < {min_bytes}B): {path.relative_to(REPO_ROOT)}"
    return None


# ------------------- per-stage checks -------------------


def check_research(slug: str) -> int:
    primary = CP / f"1-research/{slug}.md"
    err = must_exist(primary, min_bytes=500)
    if err:
        return fail("research stage didn't produce a substantive dossier", err)
    return ok("research", slug, f"{primary.stat().st_size:,}B at {primary.relative_to(REPO_ROOT)}")


def check_reference(slug: str) -> int:
    p = CP / f"2-reference/{slug}.md"
    err = must_exist(p)
    if err:
        return fail("reference snapshot missing", err)
    return ok("reference", slug)


def check_outline(slug: str) -> int:
    p = CP / f"3-outlines/{slug}.md"
    err = must_exist(p, min_bytes=200)
    if err:
        return fail("outline missing or too short", err)
    return ok("outline", slug)


def check_annotated(slug: str) -> int:
    p = CP / f"4-outlines-annotated/{slug}.md"
    err = must_exist(p, min_bytes=200)
    if err:
        return fail("annotated outline missing", err)
    return ok("annotated", slug)


def check_draft(slug: str) -> int:
    p = CP / f"5-drafts/{slug}.md"
    err = must_exist(p, min_bytes=1000)
    if err:
        return fail("draft missing or too short (<1KB)", err)
    body = p.read_text(encoding="utf-8")
    h2_count = sum(1 for line in body.splitlines() if line.startswith("## "))
    if h2_count < 3:
        return fail("draft has fewer than 3 H2 sections", f"got {h2_count} H2s in {p.relative_to(REPO_ROOT)}")
    return ok("draft", slug, f"{len(body.split())} words, {h2_count} H2 sections")


def check_cited(slug: str) -> int:
    p = CP / f"6-drafts-cited/{slug}.md"
    err = must_exist(p, min_bytes=1000)
    if err:
        return fail("cited draft missing", err)
    return ok("cited", slug)


def check_visuals(slug: str) -> int:
    """Hard-fail if visuals stage didn't fully resolve.

    Neo's rule (PLEAA-392 2026-05-06): every visual placeholder must produce
    a real asset on disk OR be explicitly captured. `manual` and `failed`
    entries in the manifest, OR naked [VISUAL:...] tags in the cited draft,
    are HALT conditions — the pipeline cannot advance to preview/publish.
    """
    manifest_path = CP / f"images/{slug}/manifest.json"
    err = must_exist(manifest_path)
    if err:
        return fail("visuals stage didn't produce a manifest", err)
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as e:
        return fail("visuals manifest is not valid JSON", str(e))
    visuals = manifest.get("visuals", [])
    bad = [v for v in visuals if v.get("status") in ("manual", "failed")]
    if bad:
        details = [f"#{v.get('index')} {v.get('type')} → {v.get('status')}: {v.get('result',{}).get('reason','no reason')}" for v in bad]
        return fail(f"{len(bad)}/{len(visuals)} visuals unresolved (manual or failed)", *details,
                    "fix by running /capture-visuals or extending the SKILL to handle the type")

    # Also verify the cited draft has no naked [VISUAL:...] placeholders left.
    draft = CP / f"6-drafts-cited/{slug}.md"
    if draft.exists():
        text = draft.read_text(encoding="utf-8")
        leftovers = VISUAL_PLACEHOLDER_RE.findall(text)
        if leftovers:
            preview = leftovers[0][:120] + ("…" if len(leftovers[0]) > 120 else "")
            return fail(f"{len(leftovers)} naked [VISUAL:...] / [SCREENSHOT:...] placeholders still in cited draft",
                        f"first: {preview}", "the visuals stage must rewrite these into ![alt](path) markdown")
    return ok("visuals", slug, f"{len(visuals)} visual(s), all resolved")


def _check_adversarial(slug: str, stage_key: str, file_suffix: str, label: str) -> int:
    """Shared check for an adversarial verdict file.

    Phase 3 of PLEAA-392 (PLEAA-418): each adversarial pass writes a verdict
    file with a `## Verdict: **PASS|FAIL**` line. The gate fails when:
      - the verdict file is missing, OR
      - the verdict is FAIL AND the revision budget for this stage is
        exhausted (per `scripts/adversarial_runlog.py`).

    A FAIL with budget remaining is NOT a gate fail — the orchestrator is
    expected to re-dispatch the producing stage and re-run the adversarial
    skill. The gate only halts the pipeline once the budget is gone.
    """
    p = CP / f"quality-checks/{slug}-{file_suffix}.md"
    err = must_exist(p)
    if err:
        return fail(f"{label} adversarial verdict missing", err,
                    f"orchestrator must run /{label}-adversarial after the producing stage")
    text = p.read_text(encoding="utf-8")
    m = re.search(r"##\s*Verdict:\s*\*\*(PASS|FAIL)\*\*", text, re.I)
    if not m:
        return fail(f"{label} adversarial has no parseable verdict line",
                    f"expected '## Verdict: **PASS**' or '## Verdict: **FAIL**' in {p.relative_to(REPO_ROOT)}")
    verdict = m.group(1).upper()
    if verdict == "PASS":
        return ok(f"{label}-adversarial", slug, "verdict=PASS")

    # FAIL: only halt if the per-stage revision budget is exhausted.
    # Guard the entire runlog interaction (import + used + budget_for) so an
    # unknown stage_key or any other runlog failure surfaces as a clean GATE
    # FAIL instead of a Python traceback. _check_adversarial is a shared
    # helper; today's callers pass valid keys but a future caller mistyping a
    # key shouldn't crash the gate.
    try:
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        import adversarial_runlog  # type: ignore
        used = adversarial_runlog.used(slug, stage_key)
        budget = adversarial_runlog.budget_for(stage_key)
    except Exception as e:
        return fail(f"{label} adversarial FAIL and runlog module unavailable", str(e))
    if used < budget:
        return ok(f"{label}-adversarial", slug,
                  f"verdict=FAIL but budget remains ({used}/{budget}) — orchestrator must revise + re-run")
    return fail(f"{label} adversarial verdict is FAIL and revision budget is exhausted ({used}/{budget})",
                f"see {p.relative_to(REPO_ROOT)}",
                f"write 9-needs-review/{slug}.md and STOP — never advance with unresolved CRITICAL adversarial findings")


def check_outline_adversarial(slug: str) -> int:
    return _check_adversarial(slug, "outline", "outline-adversarial", "outline")


def check_research_adversarial(slug: str) -> int:
    return _check_adversarial(slug, "research", "research-adversarial", "research")


def check_visuals_adversarial(slug: str) -> int:
    return _check_adversarial(slug, "visuals", "visuals-adversarial", "visuals")


def check_quality(slug: str) -> int:
    p = CP / f"quality-checks/{slug}.md"
    err = must_exist(p)
    if err:
        return fail("quality-check verdict missing", err)
    text = p.read_text(encoding="utf-8")
    m = re.search(r"Verdict:\s*\*\*(PASS|FAIL|BORDERLINE)\*\*", text, re.I)
    if not m:
        return fail("quality-check has no parseable verdict line", f"expected '## Verdict: **PASS|FAIL|BORDERLINE**' in {p.relative_to(REPO_ROOT)}")
    verdict = m.group(1).upper()
    has_critical = "CRITICAL" in text and re.search(r"###\s*CRITICAL[^\n]*\n([^#]+)", text, re.I)
    critical_body = (has_critical.group(1) if has_critical else "").strip()
    has_real_critical = bool(critical_body and not re.match(r"^[—-]+\s*none\s*$", critical_body, re.I))
    if verdict == "FAIL":
        return fail("quality verdict is FAIL — pipeline halts here", f"see {p.relative_to(REPO_ROOT)} for the punch list")
    if verdict == "BORDERLINE" and has_real_critical:
        return fail("quality verdict is BORDERLINE with CRITICAL items — pipeline halts here",
                    f"resolve CRITICALs in {p.relative_to(REPO_ROOT)}")
    return ok("quality", slug, f"verdict={verdict}, no blocking CRITICALs")


def check_preview(slug: str) -> int:
    p = CP / f"7-preview/{slug}.html"
    err = must_exist(p, min_bytes=500)
    if err:
        return fail("preview HTML missing", err)
    return ok("preview", slug)


def check_publish(slug: str) -> int:
    pub_dir = CP / f"8-publish/{slug}"
    for required in ("article.md", "article.json", "README.md"):
        err = must_exist(pub_dir / required)
        if err:
            return fail(f"publish package missing {required}", err)
    article_md = (pub_dir / "article.md").read_text(encoding="utf-8")
    leftovers = VISUAL_PLACEHOLDER_RE.findall(article_md)
    if leftovers:
        preview = leftovers[0][:120] + ("…" if len(leftovers[0]) > 120 else "")
        return fail(f"{len(leftovers)} naked [VISUAL:...] placeholder(s) in article.md", f"first: {preview}",
                    "format-for-publish must strip or substitute these — never ship raw template syntax")
    try:
        json.loads((pub_dir / "article.json").read_text(encoding="utf-8"))
    except Exception as e:
        return fail("article.json is not valid JSON", str(e))
    return ok("publish", slug)


def check_deliverable(slug: str) -> int:
    """Verify a deliverable comment was posted to the triggering Paperclip issue.

    Postcondition for an issue-driven run. Reads PAPERCLIP_TASK_ID and
    PAPERCLIP_API_URL/PAPERCLIP_API_KEY; if any are missing, treats the run
    as non-issue-driven and passes. When all present, polls the comment
    thread for one mentioning the slug + verdict.
    """
    task_id = os.environ.get("PAPERCLIP_TASK_ID")
    api_url = os.environ.get("PAPERCLIP_API_URL")
    api_key = os.environ.get("PAPERCLIP_API_KEY")
    if not (task_id and api_url and api_key):
        return ok("deliverable", slug, "non-issue-driven run (no PAPERCLIP_TASK_ID); skipped")
    try:
        import urllib.request
        req = urllib.request.Request(
            f"{api_url}/api/issues/{task_id}/comments?order=desc&limit=20",
            headers={"Authorization": f"Bearer {api_key}"},
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
    except Exception as e:
        return fail("deliverable check could not reach Paperclip API", str(e))
    comments = data if isinstance(data, list) else data.get("items") or data.get("comments") or []
    for c in comments:
        body = c.get("body", "") or ""
        if slug in body and any(k in body.lower() for k in ("verdict", "pass", "fail", "borderline")):
            return ok("deliverable", slug, f"found comment {c.get('id')} mentioning slug + verdict")
    return fail("no Paperclip comment posted with slug + verdict",
                f"orchestrator must POST a deliverable summary to issue {task_id} after stage 8")


CHECKS = {
    "research": check_research,
    "research-adversarial": check_research_adversarial,
    "reference": check_reference,
    "outline": check_outline,
    "outline-adversarial": check_outline_adversarial,
    "annotated": check_annotated,
    "draft": check_draft,
    "cited": check_cited,
    "visuals": check_visuals,
    "visuals-adversarial": check_visuals_adversarial,
    "quality": check_quality,
    "preview": check_preview,
    "publish": check_publish,
    "deliverable": check_deliverable,
}


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 64
    stage, slug = sys.argv[1], sys.argv[2]
    if stage not in CHECKS:
        print(f"unknown stage '{stage}'. valid: {', '.join(CHECKS)}", file=sys.stderr)
        return 64
    return CHECKS[stage](slug)


if __name__ == "__main__":
    sys.exit(main())
