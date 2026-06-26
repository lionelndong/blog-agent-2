#!/usr/bin/env python3
"""Format a cited draft for Strapi publishing.

Produces three files under content-pipeline/8-publish/{slug}/:
  - article.md       (clean markdown body, no H1, no shortcodes, with :::tip / :::note callouts)
  - article.json     (Strapi-shaped payload for API publish or admin paste)
  - README.md        (human-readable summary + what to do next)

Usage:
    python .claude/skills/format-for-publish/scripts/format_for_strapi.py <slug>

To enable direct Strapi API publish later:
  - Set STRAPI_BASE_URL and STRAPI_API_TOKEN env vars (e.g. via `doppler run --`)
  - Pass --publish flag
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DRAFT_DIR = ROOT / "content-pipeline" / "6-drafts-cited"
OUT_DIR = ROOT / "content-pipeline" / "8-publish"
IMAGES_DIR = ROOT / "content-pipeline" / "images"
QC_DIR = ROOT / "content-pipeline" / "quality-checks"
AUDIT_DIR = ROOT / "content-pipeline" / "audit"
OVERRIDE_LOG = AUDIT_DIR / "publish-overrides.log"
DOCS_DIR = ROOT / "docs"
BUNDLE_VIEWER = ROOT / "scripts" / "bundle_viewer.py"
INDEX_HTML = DOCS_DIR / "index.html"

IMAGE_REF_RE = re.compile(r"!\[([^\]]*)\]\((images/[^)]+\.(?:png|jpg|jpeg|webp|gif))\)")
QC_VERDICT_RE = re.compile(r"\b(PASS|BORDERLINE|FAIL)\b", re.IGNORECASE)

# ── PLE-2646: QA / research-scaffolding scrub at the publish boundary ──────────
# Background: the live /blog/ai-sexting-app page (and, on sweep, five other
# published articles) rendered internal pipeline metadata in the body — citation-
# density tallies, "Anchor URLs resolution status", `_Visual asset: … Target
# section: …_` manifest captions, an `<a id="editor-note-serp">` editor note,
# raw keyword-research dumps ("keyword baseline", "33,100 searches at $3.08 CPC"),
# and self-referential production vocabulary ("our source review", "before
# publication", "the approved draft language is narrow"). `strip_editor_notes`
# only caught a literal `## Editor notes` heading, so every other shape leaked.
#
# Two-tier defense, mirroring the existing [VISUAL:…] gate:
#   1. AUTO_STRIP_* — structural scaffolding that is NEVER legitimate reader copy
#      and is safe to delete in place (HTML comments, manifest caption lines).
#   2. PIPELINE_LEAK_PATTERNS — high-precision inline production vocabulary that
#      a machine should not silently rewrite. If any survives to publish, HALT
#      and make a human/agent fix the prose (same posture as the visuals gate).
# Patterns are deliberately high-precision: none of them appears in clean,
# reader-facing prose in this niche, so the gate does not false-positive on real
# articles. Add new markers here when a new leak class is found in the wild.

# Whole-line `_Visual asset: … Target section: …._` manifest captions emitted by
# the visuals manifest — pure pipeline metadata, safe to delete in place.
VISUAL_ASSET_CAPTION_RE = re.compile(r"(?m)^[ \t]*_Visual asset:[^\n]*_[ \t]*$\n?")
# HTML comments (`<!-- … -->`). The pipeline uses these for QA annotations
# (`<!-- VOICE-FLAGGED -->`, `<!-- CITATION DENSITY -->`); they are never meant
# for the published rich-text block.
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)

# Inline production vocabulary that must NEVER reach a published block. Each
# entry is (compiled_regex, human_label). Kept high-precision on purpose.
PIPELINE_LEAK_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"_Visual asset:", re.IGNORECASE), "visual-asset manifest caption"),
    (re.compile(r"Target section:", re.IGNORECASE), "visual-asset manifest caption"),
    (re.compile(r"Anchor URLs? resolution status", re.IGNORECASE), "anchor-resolution QA note"),
    (re.compile(r"research revision pass", re.IGNORECASE), "research-stage QA note"),
    (re.compile(r"CITATION DENSITY", re.IGNORECASE), "citation-density QA note"),
    (re.compile(r"VOICE-FLAGGED", re.IGNORECASE), "voice-flag QA note"),
    (re.compile(r"Must-cite claims? identified", re.IGNORECASE), "citation-density QA note"),
    (re.compile(r"BEAT SPEC", re.IGNORECASE), "research beat-spec marker"),
    (re.compile(r"keyword baseline", re.IGNORECASE), "raw keyword-research dump"),
    (re.compile(r"research dossier", re.IGNORECASE), "internal pipeline reference"),
    (re.compile(r"(?:research|SERP) artifact captured", re.IGNORECASE), "internal research-artifact reference"),
    (re.compile(r"sampled SERPs?\b", re.IGNORECASE), "internal SERP-methodology reference"),
    (re.compile(r"SERP-observed", re.IGNORECASE), "internal SERP-methodology reference"),
    (re.compile(r"\b(?:our |the |current )?source review\b", re.IGNORECASE), "internal source-review reference"),
    (re.compile(r"\bbefore publication\b", re.IGNORECASE), "editorial-process instruction"),
    (re.compile(r"approved (?:draft language|wording|factual placement)", re.IGNORECASE), "editorial-process instruction"),
    (re.compile(r"this packet (?:does not|provides)", re.IGNORECASE), "research-packet reference"),
    (re.compile(r"editor[- ]note[- ]serp", re.IGNORECASE), "editor-note anchor"),
    (re.compile(r"\$[0-9.]+ ?CPC\b", re.IGNORECASE), "raw keyword-research CPC metric"),
    (re.compile(r"content-pipeline/", re.IGNORECASE), "internal pipeline file path"),
    (re.compile(r"\bPLEAA-\d", re.IGNORECASE), "internal ticket reference"),
    (re.compile(r"\bPLE-\d", re.IGNORECASE), "internal ticket reference"),
]

# PLEAA-524: editorial category taxonomy. Strapi is the source of truth for the
# `name` strings — keep this list aligned with /api/categories. The publisher
# pipeline routes a cited draft to a category via three signals (in order):
#
#   1. An explicit `category:` line in the cited draft's frontmatter or
#      `## Editor notes` block. Wins outright when present.
#   2. A slug-pattern heuristic — `*-review*` → Reviews, `*-guide*` → Guides,
#      keyword markers like `uncensored`/`no-filter`/`nsfw`/`dirty` → Uncensored.
#   3. Default: AI Companions (the brand-categorical bucket).
#
# Out of scope here (PLEAA-524): tag taxonomy, multi-category posts, or the
# auto-creation of new categories on Strapi when an unknown name is referenced —
# the resolver in this file silently omits `category` for unknown names rather
# than POSTing a new category. Operators add categories in the Strapi admin and
# the next publish picks them up via the existing /api/categories cache.
CATEGORY_DEFAULT = "AI Companions"
CATEGORY_KNOWN = {"AI Companions", "Reviews", "Guides", "Uncensored"}

# Regex catching `category: <name>` either in YAML-style frontmatter at the top
# of the draft or inside an `## Editor notes` block. Multi-word names are fine
# (the value is everything up to end-of-line, then trimmed).
CATEGORY_FRONTMATTER_RE = re.compile(
    r"^\s*category\s*:\s*(.+?)\s*$",
    re.MULTILINE | re.IGNORECASE,
)

# ── Multi-author byline → Strapi Author relation ───────────────────────────────
# /draft stamps the chosen persona into the first line of the cited draft as an
# HTML comment:  <!-- byline: Sloane Avery | persona: sloane-avery -->
# We parse the `persona` slug, strip the comment from the published body, and map
# the slug → the live Strapi Author `documentId` below. The map is the source of
# truth shared with examples/authors.md — keep the two in lockstep. Unknown or
# missing slugs leave the author relation unset (no crash); the editor can attach
# an author manually in admin.
PERSONA_AUTHORS: dict[str, str] = {
    "sloane-avery": "wfmxn1rf6wav1dn9t5bd7hsi",
    "theo-hart": "bhofw86kms6ihklbhy72b0vh",
    "mateo-reyes": "u42i38c5i95mfj47nenzx25u",
}

# Matches the byline stamp anywhere it appears (it's authored as the first line,
# but we tolerate leading whitespace/blank lines). Captures the persona slug.
# Note: HTML_COMMENT_RE in scrub_pipeline_scaffolding would also remove this
# comment, so byline extraction MUST run on the raw draft before that scrub.
BYLINE_COMMENT_RE = re.compile(
    r"<!--\s*byline:\s*(?P<byline>[^|]+?)\s*\|\s*persona:\s*(?P<persona>[a-z0-9-]+)\s*-->",
    re.IGNORECASE,
)

# Leftover deferred-visual placeholders. Visuals are DEFERRED in the current
# pipeline (the visuals stage leaves placeholders, generates nothing, and does
# NOT gate), so format-for-publish no longer hard-fails on these. Instead we
# convert each to an HTML comment so the marker is retained in source but stays
# invisible on the live site. Covers both the current [VISUAL:...] vocabulary and
# the legacy [SCREENSHOT:...] form.
VISUAL_PLACEHOLDER_RE = re.compile(r"\[(?:VISUAL|SCREENSHOT):[^\]]*\]")

# ── Ahrefs component library: verbatim pass-through contract ───────────────────
# /draft emits the full authored component set from examples/ahrefs-components.md.
# These fences (and the inline {lead}/==mark== tokens below) are NOT rendered to
# HTML here and are NOT normalized — they pass through to the published article.md
# body BYTE-FOR-BYTE so the blog-page renderer (a separate CTO task; see the
# "Render contract" in examples/ahrefs-components.md) can style them. This list is
# documentation, kept in lockstep with that spec — preservation is *passive*
# (nothing in this file transforms a `:::fence`, a `{lead}` wrapper, or a `==mark==`
# span). transform_callouts() only NORMALIZES the `**Label:**` shorthands into a
# subset of these fences; it must never touch an already-authored fence or token.
# scrub_pipeline_scaffolding() (HTML comments + `_Visual asset:_` captions) and
# assert_no_pipeline_leak() (high-precision internal vocab) match none of these,
# so every component + inline token survives untouched.
PRESERVED_AUTHORED_FENCES = (
    # 14 BUILT (render today — component-mockup.html)
    "byline", "nutshell", "methodology", "key-takeaways", "sidenote", "tip",
    "note", "stat", "stat-group", "table", "expert", "pullquote",
    "further-reading", "cta",
    # New authored fences (renderer TODO; preserved verbatim all the same)
    "warning", "important", "definition", "primer", "proscons", "feature-matrix",
    "decision-table", "preferred-order", "verdict", "badge", "stat-list", "tweet",
    "video", "faq", "jumplinks", "figure", "diagram", "entry",
)
# Inline treatments preserved as raw tokens (page renderer turns these into
# cmp-lead / <mark>; inline `code` is plain markdown and also left as-is):
#   {lead}…{/lead}   — editorial lead-paragraph wrapper
#   ==marked text==  — highlight span
# No regex in this file consumes them; they are listed here only to document the
# guarantee for maintainers.
PRESERVED_INLINE_TOKENS = ("{lead}…{/lead}", "==mark==", "`code`")


def _slug_to_category_heuristic(slug: str) -> str:
    """Pick a category for a slug when no explicit override is present.

    Lower-cased slug matched in priority order: review → Reviews,
    uncensored / no-filter / nsfw / dirty → Uncensored, guide → Guides,
    everything else → AI Companions. Heuristic is deliberately conservative;
    operators override via `category:` in the draft when this gets it wrong.
    """
    s = slug.lower()
    if "review" in s:
        return "Reviews"
    if any(tok in s for tok in ("uncensored", "no-filter", "nofilter", "nsfw", "dirty")):
        return "Uncensored"
    if "guide" in s or s.startswith("how-to-"):
        return "Guides"
    return CATEGORY_DEFAULT


def resolve_category_name(slug: str, raw_md: str) -> str:
    """Return the human-readable category name to send to Strapi for `slug`.

    Reads an explicit `category: <name>` declaration anywhere in the raw cited
    draft (frontmatter or editor-notes section) before falling back to the
    slug-pattern heuristic. The result MUST be one of CATEGORY_KNOWN — anything
    else is logged and replaced with the heuristic so a typo can't silently
    publish under an unknown bucket. Strapi-side resolution still validates by
    fetching /api/categories; an unknown name is dropped from the payload.
    """
    m = CATEGORY_FRONTMATTER_RE.search(raw_md)
    if m:
        candidate = m.group(1).strip()
        canonical = next(
            (k for k in CATEGORY_KNOWN if k.casefold() == candidate.casefold()),
            None,
        )
        if canonical:
            return canonical
        sys.stderr.write(
            f"warning: cited draft requested unknown category {candidate!r}; "
            f"falling back to slug heuristic. Known: {sorted(CATEGORY_KNOWN)}\n"
        )
    return _slug_to_category_heuristic(slug)


def _git_run(args: list[str], *, timeout: int = 15) -> tuple[int, str, str]:
    """Run a git subcommand inside ROOT. Never raises; returns (rc, stdout, stderr)."""
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except Exception as exc:  # FileNotFoundError, TimeoutExpired, etc.
        return -1, "", f"{type(exc).__name__}: {exc}"


def verify_publish_artifact(slug: str) -> tuple[bool, str]:
    """PLEAA-581 Layer 1: hard gate before any HTTP write to Strapi.

    Verifies the publish artifact for ``slug``:

      1. ``content-pipeline/8-publish/{slug}/article.json`` exists locally, AND
      2. The same path is present in ``origin/main`` HEAD — i.e.
         ``git ls-tree -r origin/main -- <path>`` returns a non-empty line.

    Returns ``(allow_publish, reason)``. Caller hard-exits on a False unless
    the operator passed ``--human-approved "<reason>"``. See PLEAA-577 for the
    audit + root cause; gate spec lives on PLEAA-581.
    """
    rel_path = f"content-pipeline/8-publish/{slug}/article.json"
    local = ROOT / rel_path
    if not local.exists():
        return False, (
            f"publish gate REJECT — local artifact missing: {rel_path}\n"
            f"  fix: run /blog-pipeline through stage 8 (format-for-publish without --publish)\n"
            f"       before retrying with --publish.\n"
            f"  see: https://lionelndong.github.io/blog-agent-2/ (/blog-pipeline)\n"
            f"  override (last resort): --human-approved \"<reason>\""
        )
    rc, stdout, stderr = _git_run(["ls-tree", "-r", "origin/main", "--", rel_path])
    if rc != 0:
        return False, (
            f"publish gate REJECT — git ls-tree origin/main failed (rc={rc}): "
            f"{stderr.strip()[:200]}.\n"
            f"  fix: run `git fetch origin main` and re-try.\n"
            f"  override (last resort): --human-approved \"<reason>\""
        )
    if not stdout.strip():
        return False, (
            f"publish gate REJECT — artifact NOT in origin/main HEAD: {rel_path}\n"
            f"  fix: commit + push the publish package on main, then re-run --publish.\n"
            f"  see: https://lionelndong.github.io/blog-agent-2/ (/blog-pipeline)\n"
            f"  override (last resort): --human-approved \"<reason>\""
        )
    return True, f"publish gate OK — artifact present in origin/main ({rel_path})"


def _git_user_email() -> str:
    rc, stdout, _ = _git_run(["config", "user.email"], timeout=10)
    if rc == 0 and stdout.strip():
        return stdout.strip()
    return os.environ.get("USER", "unknown") + "@local"


def _git_head_sha() -> str:
    rc, stdout, _ = _git_run(["rev-parse", "HEAD"], timeout=10)
    return stdout.strip() if rc == 0 else "unknown"


def _git_current_branch() -> str:
    rc, stdout, _ = _git_run(["rev-parse", "--abbrev-ref", "HEAD"], timeout=10)
    return stdout.strip() if rc == 0 else "unknown"


def log_publish_override(slug: str, reason: str) -> Path:
    """Append one tab-separated line to ``content-pipeline/audit/publish-overrides.log``.

    Schema: ``timestamp\\tslug\\treason\\tuser.email\\tbranch\\tHEAD-sha``.

    Tabs and newlines inside ``reason`` are flattened to spaces so the log
    stays line-oriented. The directory is created lazily — first override on a
    fresh checkout creates ``content-pipeline/audit/`` as a side-effect.
    """
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    safe_reason = re.sub(r"[\t\r\n]+", " ", reason or "").strip() or "(no reason given)"
    line = "\t".join([
        datetime.now(timezone.utc).isoformat(),
        slug,
        safe_reason,
        _git_user_email(),
        _git_current_branch(),
        _git_head_sha(),
    ]) + "\n"
    with OVERRIDE_LOG.open("a", encoding="utf-8") as f:
        f.write(line)
    return OVERRIDE_LOG


def write_manifest(out_dir: Path, slug: str, title: str) -> Path:
    """PLEAA-581 Layer 2 hook: write ``content-pipeline/8-publish/{slug}/manifest.json``.

    The ``sync-publish-approvals.yml`` GitHub Action scans
    ``content-pipeline/8-publish/*/manifest.json`` on every push to ``main`` and
    upserts one row per slug into the Supabase ``blog_publish_approvals``
    registry. The edge function ``sync-blog-posts`` then refuses any Strapi
    ``entry.publish`` webhook whose ``documentId`` has no approval row.

    Minimum required field: ``slug``. ``title`` and ``pipeline_run_id`` are
    convenience fields for human triage. ``approved_by`` is intentionally a
    placeholder here (``"pending-ci"``) — the action overwrites it with
    ``github-actions[bot]`` at merge time, which is the moment the artifact
    actually becomes "approved" (committed to ``main`` by a reviewed PR).
    """
    pipeline_run_id = (
        os.environ.get("BLOG_AGENT_PIPELINE_RUN_ID")
        or os.environ.get("GITHUB_RUN_ID")
        or os.environ.get("PAPERCLIP_RUN_ID")
        or ""
    )
    manifest = {
        "slug": slug,
        "title": title,
        "pipeline_run_id": pipeline_run_id,
        "approved_by": "pending-ci",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    path = out_dir / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def quality_precondition(slug: str) -> tuple[bool, str]:
    """Read content-pipeline/quality-checks/{slug}.md verdict line.

    Returns (allow_publish, reason). Refuses publish if verdict is FAIL or file missing.
    """
    path = QC_DIR / f"{slug}.md"
    if not path.exists():
        return False, f"quality-check report missing: {path}"
    text = path.read_text(encoding="utf-8")
    head = "\n".join(text.splitlines()[:30])
    m = QC_VERDICT_RE.search(head)
    if m is None:
        return False, f"no verdict line found in {path}"
    verdict = m.group(1).upper()
    if verdict == "FAIL":
        return False, f"quality verdict is FAIL — refusing auto-publish"
    return True, f"verdict={verdict}"


def read_draft(slug: str) -> str:
    path = DRAFT_DIR / f"{slug}.md"
    if not path.exists():
        sys.exit(f"error: cited draft not found at {path}")
    return path.read_text(encoding="utf-8")


def strip_editor_notes(md: str) -> str:
    """Drop the '## Editor notes' section and everything after it."""
    m = re.search(r"^---\s*\n+##\s+Editor notes", md, re.MULTILINE)
    if m:
        return md[:m.start()].rstrip() + "\n"
    m = re.search(r"^##\s+Editor notes", md, re.MULTILINE)
    if m:
        return md[:m.start()].rstrip() + "\n"
    return md


def extract_byline_persona(raw_md: str) -> str | None:
    """Parse the persona slug from the draft's byline stamp, if present.

    /draft writes `<!-- byline: <Name> | persona: <slug> -->` as the first line.
    Returns the lower-cased persona slug, or None when no byline comment exists.
    MUST be called on the RAW draft — `scrub_pipeline_scaffolding` strips all HTML
    comments (including this one), so byline extraction has to happen first.
    """
    m = BYLINE_COMMENT_RE.search(raw_md)
    if not m:
        return None
    return m.group("persona").strip().lower()


def strip_byline_comment(md: str) -> str:
    """Remove the byline stamp comment from the body and tidy the blank line.

    Defensive: `scrub_pipeline_scaffolding` already deletes every HTML comment,
    so by publish time the byline is usually gone anyway. We strip it explicitly
    here too so the function is correct even if called before/without the scrub.
    """
    md = BYLINE_COMMENT_RE.sub("", md)
    # Drop a leading blank line the removed first-line comment may leave behind.
    return md.lstrip("\n")


def resolve_author_document_id(persona_slug: str | None) -> str | None:
    """Map a persona slug → Strapi Author documentId, or None if unknown/missing."""
    if not persona_slug:
        return None
    doc_id = PERSONA_AUTHORS.get(persona_slug)
    if doc_id is None:
        sys.stderr.write(
            f"warning: byline persona {persona_slug!r} not in PERSONA_AUTHORS "
            f"{sorted(PERSONA_AUTHORS)}; leaving author relation unset\n"
        )
    return doc_id


def defer_visual_placeholders(md: str) -> str:
    """Convert leftover `[VISUAL:...]` / `[SCREENSHOT:...]` placeholders to HTML comments.

    Visuals are DEFERRED: the visuals stage intentionally leaves placeholders and
    generates nothing, so a raw placeholder reaching publish is expected, not an
    error. We retain each one as `<!-- VISUAL-TODO: ...original... -->` — a marker
    that survives in the source (so the visuals agent can find it later) but is
    invisible on the live site. Returns the body with every placeholder rewritten.

    NB: This must run BEFORE `scrub_pipeline_scaffolding` (which deletes all HTML
    comments) is applied to the *body* — otherwise the VISUAL-TODO markers would be
    scrubbed away. In `main()` the scrub runs on the raw draft for QA-note removal,
    and this conversion runs afterward on the body, so the markers persist to the
    published article.md.
    """
    return VISUAL_PLACEHOLDER_RE.sub(
        lambda m: f"<!-- VISUAL-TODO: {m.group(0)} -->", md
    )


def scrub_pipeline_scaffolding(md: str) -> str:
    """PLE-2646: auto-remove structural QA scaffolding that is never reader copy.

    Deletes HTML comments (``<!-- … -->`` — the pipeline's QA annotations) and
    whole-line ``_Visual asset: … Target section: …_`` manifest captions in
    place, then collapses the blank-line runs the deletions leave behind. This
    is the SAFE tier: these shapes carry zero reader value, so removing them
    cannot damage an article. Inline production vocabulary is handled separately
    by :func:`assert_no_pipeline_leak`, which HALTS rather than guessing a
    rewrite.
    """
    md = HTML_COMMENT_RE.sub("", md)
    md = VISUAL_ASSET_CAPTION_RE.sub("", md)
    # Collapse 3+ newlines (left by removed standalone lines) down to a blank line.
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md


def assert_no_pipeline_leak(md: str, slug: str) -> None:
    """PLE-2646 hard gate: refuse to ship inline QA/research scaffolding.

    Scans the publish-ready body for high-precision production vocabulary that
    must never reach a ``shared.rich-text`` block (see ``PIPELINE_LEAK_PATTERNS``).
    On any hit, exits non-zero with the matched marker + a context snippet —
    same posture as the leftover-``[VISUAL:…]`` gate. The fix is editorial (clean
    the prose in the cited draft), not mechanical, so we stop rather than mangle.
    """
    hits: list[tuple[str, str]] = []
    for pattern, label in PIPELINE_LEAK_PATTERNS:
        m = pattern.search(md)
        if m:
            start = max(0, m.start() - 60)
            end = min(len(md), m.end() + 60)
            snippet = re.sub(r"\s+", " ", md[start:end]).strip()
            hits.append((label, snippet))
    if hits:
        lines = "\n".join(f"  - {label}: …{snippet}…" for label, snippet in hits)
        sys.exit(
            f"error: refusing to write publish package for {slug!r} — "
            f"{len(hits)} QA/research-scaffolding leak(s) in the body:\n{lines}\n"
            f"  These are internal pipeline notes (citation tallies, keyword-research\n"
            f"  dumps, '_Visual asset:' captions, editor notes, source-review/\n"
            f"  'before publication' vocabulary, ticket refs, content-pipeline/ paths)\n"
            f"  and must not reach readers. Fix: edit the cited draft\n"
            f"  (content-pipeline/6-drafts-cited/{slug}.md) to remove the leaked text,\n"
            f"  then re-run /format-for-publish. See PLE-2646."
        )


def extract_title(md: str) -> tuple[str, str]:
    m = re.search(r"^#\s+(.+?)\s*$", md, re.MULTILINE)
    if not m:
        return "Untitled", md
    title = m.group(1).strip()
    body = (md[:m.start()] + md[m.end():]).lstrip("\n")
    return title, body


def transform_callouts(md: str) -> str:
    """Normalize `**Label:**` callout shorthands into `:::fence` blocks.

    Two shapes are handled:

    1. **Single-paragraph callouts** (Tip / Pro tip / Note / Sidenote / Editor) —
       the label leads one paragraph; capture runs to the next blank line. These
       are the original mappings and are UNCHANGED (Pro tip→tip, Tip→tip,
       Sidenote→note, Note→note, Editor→editor) so existing drafts keep
       converting byte-for-byte.

    2. **Block-shaped callouts** (Methodology / In a nutshell / Key takeaways) —
       the Ahrefs house-standard components whose body is often a *bulleted list*
       (`:::methodology`, `:::key-takeaways`) or a short multi-sentence answer
       (`:::nutshell`). A blank-line-terminated capture would truncate a bullet
       list whose items sit on their own lines, so these use a block capture that
       keeps the label's paragraph AND an immediately-adjacent bullet list
       (bullets separated from the label by a single newline, no blank line).

    The fence names are the exact catalog names from examples/ahrefs-components.md
    (`:::nutshell`, `:::key-takeaways`, `:::methodology`). Authors are encouraged
    to write the explicit `:::fence` directly (it passes through untouched — see
    the "fence pass-through" contract); these shorthands are the convenience path.

    Pass-through guarantee (PRESERVED_AUTHORED_FENCES / PRESERVED_INLINE_TOKENS):
    this function ONLY normalizes the `**Label:**` shorthands into their subset of
    fences. It never rewrites an already-authored `:::fence` (BUILT or the newer
    `:::warning` / `:::definition` / `:::proscons` / `:::feature-matrix` /
    `:::decision-table` / `:::preferred-order` / `:::stat-list` / `:::faq` /
    `:::jumplinks` / `:::entry` / `:::figure` / … set), nor the inline `{lead}…{/lead}`
    wrapper or `==mark==` spans. The shorthand patterns are anchored to literal
    `**Label:**` text, and the final "move a glued opener to its own line" rule
    targets only `:::name` openers (which is desirable for EVERY fence name) — so
    new fences and inline tokens reach the published body byte-for-byte.
    """
    # Shape 1: single-paragraph callouts (UNCHANGED — original behavior).
    paragraph_patterns = [
        (r"\*\*Pro tip:\*\*\s*(.+?)(?=\n\n|\Z)", "tip"),
        (r"\*\*Tip:\*\*\s*(.+?)(?=\n\n|\Z)", "tip"),
        (r"\*\*Sidenote:\*\*\s*(.+?)(?=\n\n|\Z)", "note"),
        (r"\*\*Note:\*\*\s*(.+?)(?=\n\n|\Z)", "note"),
        (r"\*\*Editor:\*\*\s*(.+?)(?=\n\n|\Z)", "editor"),
    ]
    for pattern, kind in paragraph_patterns:
        md = re.sub(
            pattern,
            lambda m, k=kind: f":::{k}\n{m.group(1).strip()}\n:::",
            md,
            flags=re.DOTALL,
        )

    # Shape 2: block-shaped callouts. The capture grabs the rest of the label
    # line plus any contiguous following lines up to (but not including) the
    # next blank line that is NOT immediately followed by a list item — i.e. a
    # bullet list directly under the label is kept whole. `[ \t]*` lets the
    # block include indented continuations; the lookahead stops at a true
    # paragraph break (blank line followed by a non-bullet) or end-of-string.
    block_patterns = [
        (r"\*\*In a nutshell:\*\*[ \t]*(.+?)(?=\n\n(?![ \t]*[-*+] )|\Z)", "nutshell"),
        (r"\*\*Key takeaways:\*\*[ \t]*(.+?)(?=\n\n(?![ \t]*[-*+] )|\Z)", "key-takeaways"),
        (r"\*\*Methodology:\*\*[ \t]*(.+?)(?=\n\n(?![ \t]*[-*+] )|\Z)", "methodology"),
    ]
    for pattern, kind in block_patterns:
        md = re.sub(
            pattern,
            lambda m, k=kind: f":::{k}\n{m.group(1).strip()}\n:::",
            md,
            flags=re.DOTALL,
        )

    # A shorthand authored mid-paragraph (`Some prose. **Tip:** …`) leaves the
    # converted opener glued to the preceding text on the same line
    # (`Some prose. :::tip`). A fence opener must begin its own block, so move
    # any opener that is preceded by non-whitespace onto a fresh line with a
    # blank line before it. Targets ONLY named openers (`:::name…`) — the bare
    # closing `:::` and already-line-leading openers are untouched. Idempotent.
    md = re.sub(r"(?m)(\S)[ \t]+(:::[A-Za-z])", r"\1\n\n\2", md)
    return md


def first_sentences(text: str, max_chars: int = 160) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r"(?<=[.!?])\s+", text)
    out = ""
    for s in sentences:
        candidate = (out + " " + s).strip() if out else s
        if len(candidate) > max_chars:
            return out if out else s[:max_chars].rstrip() + "..."
        out = candidate
    return out


def extract_excerpt(body_md: str) -> str:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body_md) if p.strip()]
    intro = ""
    for p in paragraphs:
        if (p.startswith("#") or p.startswith(":::") or p.startswith("|")
                or p.startswith("```") or p.startswith("![") or p.startswith("!")):
            # skip headings, callouts, tables, code, and image-only lines
            # (an image's alt text must never become the meta description)
            continue
        intro = p
        break
    intro = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", intro)
    intro = re.sub(r"\*\*(.+?)\*\*", r"\1", intro)
    intro = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", intro)
    return first_sentences(intro, max_chars=160)


def truncate_meta_title(title: str, limit: int = 60) -> str:
    if len(title) <= limit:
        return title
    cut = title[:limit]
    last_space = cut.rfind(" ")
    return (cut[:last_space] if last_space > 0 else cut).rstrip() + "..."


def truncate_description(text: str, limit: int = 80) -> str:
    """Strapi v5 `description` is capped at 80 chars. Truncate at the last word
    boundary before `limit`, dropping trailing punctuation/quotes so we never end
    on a half-word or a dangling clause-opener like "include," or "with:". Falls
    back to a hard cut when there's no whitespace in the input.
    """
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    last_space = cut.rfind(" ")
    out = cut[:last_space] if last_space > 0 else cut
    # Strip trailing connector punctuation that signals a sentence in progress.
    return out.rstrip(" ,;:.-—–").rstrip()


def extract_tags(body_md: str, max_tags: int = 5) -> list[str]:
    h2s = re.findall(r"^##\s+(.+?)\s*$", body_md, re.MULTILINE)
    tags = []
    for h in h2s[:max_tags]:
        h = re.sub(r"^[\d\.\)\s]+", "", h)
        slug = re.sub(r"[^\w\s-]", "", h).strip().lower()
        slug = re.sub(r"\s+", "-", slug)
        if slug and slug not in tags:
            tags.append(slug)
    return tags[:max_tags]


def compute_read_time(body_md: str, *, wpm: int = 220) -> int:
    """Conservative read-time estimate in whole minutes. Floors at 1.

    Default 220 wpm matches the typical "tech blog reader" benchmark used by
    Medium / Substack — high enough to not feel padded, low enough that a
    skimmer can still trust the number on a quick read.
    """
    words = len(re.findall(r"\b\w+\b", body_md or ""))
    if words <= 0:
        return 1
    return max(1, round(words / wpm))


# Module-level cache for category-name → documentId. Strapi categories are
# small (<50 rows) and rarely change; pulling them once per process avoids
# re-hitting /api/categories for every article in a batch run.
_CATEGORY_DOCUMENT_ID_CACHE: dict[str, str] | None = None


def _load_category_index(base_url: str, token: str) -> dict[str, str]:
    """Fetch /api/categories once and return a {lowercased_name: documentId} map.

    Caches a successful result for the rest of the process lifetime. A transient
    fetch failure (network hiccup, expired token, Strapi restart) is NOT cached —
    we return an empty dict to the caller so it omits `category` for that one
    payload, but the next call retries the fetch. PLEAA-457 (Greptile P1): the
    earlier shape cached the empty dict on failure too, which permanently
    disabled category resolution for the rest of a batch run and silently
    published every later article without a category — exactly the silent-
    failure pattern this PR was written to close.
    """
    global _CATEGORY_DOCUMENT_ID_CACHE
    if _CATEGORY_DOCUMENT_ID_CACHE is not None:
        return _CATEGORY_DOCUMENT_ID_CACHE

    import urllib.request

    endpoint = f"{base_url.rstrip('/')}/api/categories?pagination[limit]=100"
    req = urllib.request.Request(
        endpoint,
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        items = data.get("data") if isinstance(data, dict) else None
        index: dict[str, str] = {}
        if isinstance(items, list):
            for entry in items:
                if not isinstance(entry, dict):
                    continue
                name = entry.get("name") or (entry.get("attributes") or {}).get("name")
                doc_id = entry.get("documentId") or (entry.get("attributes") or {}).get("documentId")
                if isinstance(name, str) and isinstance(doc_id, str):
                    index[name.strip().lower()] = doc_id
        _CATEGORY_DOCUMENT_ID_CACHE = index
        return index
    except Exception as exc:
        sys.stderr.write(f"warning: category index fetch failed: {exc}\n")
        # Intentionally do NOT write the cache here — let the next call retry.
        return {}


def resolve_category_document_id(name: str) -> str | None:
    """Resolve a human-readable category name to a Strapi v5 documentId.

    Requires STRAPI_BASE_URL + STRAPI_API_TOKEN (silently returns None if absent
    so dry-runs that just write the JSON package don't fail).
    """
    base_url = os.environ.get("STRAPI_BASE_URL")
    token = os.environ.get("STRAPI_API_TOKEN")
    if not base_url or not token or not name:
        return None
    index = _load_category_index(base_url, token)
    return index.get(name.strip().lower())


def extract_cover_image_url(body_md: str, base_url: str | None) -> str | None:
    """Pick a cover image URL from the body. We prefer the first image whose ref
    we can resolve to an absolute URL — i.e. either already absolute, or under
    `images/` once `base_url` is known so we can rewrite to `<base>/uploads/<file>`.

    Returns None when no image is referenced or no rewrite target is available
    (caller should then omit `cover_image_url` from the payload).
    """
    # Absolute URL in the markdown wins outright. We accept any http(s) URL
    # inside an image-markdown link rather than gating on a known file extension —
    # CDN-hosted images (Cloudinary, imgix, Strapi /uploads/, signed URLs) commonly
    # omit extensions and the previous extension-gated regex silently dropped them
    # (PLEAA-457 Greptile P3).
    abs_match = re.search(r"!\[[^\]]*\]\((https?://[^)\s]+)\)", body_md)
    if abs_match:
        return abs_match.group(1)
    # Otherwise fall back to the first uploaded local image, if we have a base.
    if not base_url:
        return None
    rel_match = IMAGE_REF_RE.search(body_md)
    if not rel_match:
        return None
    filename = Path(rel_match.group(2)).name
    return f"{base_url.rstrip('/')}/uploads/{filename}"


def resolve_cover_file_id(body_md: str, media_map: dict[str, dict] | None) -> int | None:
    """Return the Strapi upload id for the article's hero image, or None.

    PLEAA-570 (2026-05-11): on auto-publish, ``article.cover`` was being left
    null because the payload only carried images inside dynamic-zone
    ``shared.media`` blocks. The public blog page kept rendering because
    Next.js resolves the hero from a slug-derived CDN URL convention, but
    every other consumer of ``cover`` (RSS, OG tags, social cards, admin
    preview) saw nothing. We pick the same asset ``extract_cover_image_url``
    would surface — the first uploaded image referenced in the body — and
    attach it as the article's cover relation in :func:`build_payload`.

    Selection mirrors :func:`build_blocks`: the body has already been
    rewritten by :func:`rewrite_image_refs` by the time we get here, so
    image refs are absolute Strapi URLs. Index ``media_map`` by URL and walk
    every absolute image ref in body order, returning the first one we
    uploaded ourselves. PLEAA-570 Greptile P2 (2026-05-11): scanning every
    ref (not just the first) means an article whose first ref is an
    external CDN image still picks up a later uploaded image as the cover,
    instead of silently leaving the relation null. Returns None when no
    body image matches ``media_map`` (dry-run, unconfigured Strapi, or
    article with only inline external URLs) — caller should then omit
    ``cover`` from the payload.
    """
    if not media_map:
        return None
    by_url: dict[str, int] = {}
    for entry in media_map.values():
        url = entry.get("url")
        fid = entry.get("id")
        if url and isinstance(fid, int):
            by_url[url] = fid
    if not by_url:
        return None
    for abs_match in re.finditer(r"!\[[^\]]*\]\((https?://[^)\s]+)\)", body_md):
        fid = by_url.get(abs_match.group(1))
        if isinstance(fid, int):
            return fid
    return None


def build_blocks(body_md: str, media_map: dict[str, dict] | None = None) -> list[dict]:
    """Split body markdown into alternating ``shared.rich-text`` and ``shared.media`` blocks.

    The renderer Neo runs (Pleasur.ai blog frontend) only displays media that
    lives inside its own ``shared.media`` block — images embedded inside a
    single rich-text block aren't rendered as ``<img>`` (PLEAA-528 2026-05-08).
    To make every uploaded image actually appear on the published page, we
    walk the body and emit a fresh block whenever an image ref sits on a line
    by itself:

      - whole-line ``![alt](https://media.strapiapp.com/foo.png)`` and the
        URL is one we just uploaded → emit ``shared.media`` with the file id
        and drop the markdown line
      - everything else → accumulate into the current ``shared.rich-text``

    When ``media_map`` is empty or no whole-line image refs match it, this
    function returns a single rich-text block containing the full body —
    same behaviour as the pre-PLEAA-528 emitter, so dry-runs and unconfigured
    Strapi targets keep working unchanged.

    The ``media_map`` is the same one ``upload_to_strapi_media`` returns:
    ``{filename: {"id": <int>, "url": <absolute_url>}}``. We index it by the
    absolute Strapi URL because ``rewrite_image_refs`` has already replaced
    local paths with the absolute Strapi Cloud media URLs by the time we get
    here.
    """
    if not media_map:
        return [{"__component": "shared.rich-text", "body": body_md.strip() + "\n"}]

    # Index by absolute URL (the form rewrite_image_refs leaves in the body).
    by_url: dict[str, int] = {}
    for entry in media_map.values():
        url = entry.get("url")
        fid = entry.get("id")
        if url and isinstance(fid, int):
            by_url[url] = fid

    if not by_url:
        return [{"__component": "shared.rich-text", "body": body_md.strip() + "\n"}]

    # Match a line that is *only* a markdown image — possibly with surrounding
    # whitespace. Avoid matching images embedded inside a paragraph.
    whole_line_image = re.compile(r"^\s*!\[[^\]]*\]\(([^)]+)\)\s*$")

    blocks: list[dict] = []
    buf: list[str] = []

    def flush_text() -> None:
        text = "\n".join(buf).strip()
        buf.clear()
        if text:
            blocks.append({"__component": "shared.rich-text", "body": text + "\n"})

    for line in body_md.splitlines():
        m = whole_line_image.match(line)
        if not m:
            buf.append(line)
            continue
        file_id = by_url.get(m.group(1))
        if file_id is None:
            # Image we didn't upload (e.g. inline cover URL) — leave inline.
            buf.append(line)
            continue
        flush_text()
        # PLEAA-567 (2026-05-11): Strapi v5 silently drops a component-scoped
        # media relation when ``file`` is sent as a bare integer — the row is
        # created but ``file`` populates as null on the next read, so the
        # frontend has nothing to <img>. The fix is to send the relation as
        # ``{"id": <fileId>}`` (the object form Strapi's connect resolver
        # accepts on PUT and POST alike). Verified live by PUTting
        # is-having-an-ai-girlfriend-cheating (documentId
        # ur4ey6i9cuewnfpa9ygx2egb) — all 7 media blocks went from file:null
        # to fully populated after the shape switch.
        blocks.append({"__component": "shared.media", "file": {"id": file_id}})

    flush_text()

    # Defensive fallback: if for some reason every line was an image-only line
    # (or all matched nothing), don't emit an empty block list — Strapi will 400.
    if not blocks:
        return [{"__component": "shared.rich-text", "body": body_md.strip() + "\n"}]

    return blocks


def build_payload(
    slug: str,
    title: str,
    body_md: str,
    *,
    published_at: str | None = None,
    category_name: str = "AI Companions",
    author_name: str = "Pleasur.AI Team",  # noqa: ARG001 — kept for backwards compat with callers; not in v5 schema
    cover_image_url: str | None = None,    # noqa: ARG001 — same as above
    media_map: dict[str, dict] | None = None,
    cover_file_id: int | None = None,
    author_document_id: str | None = None,
) -> dict:
    """Build a Strapi v5 article payload.

    v5 schema (verified end-to-end on 2026-05-07 by live POST/GET/DELETE
    against production Strapi — see ``scripts/_smoke_integrations.py::strapi_v5_shape``):

      - title:        string
      - slug:         string (unique)
      - description:  short summary, hard-capped at 80 chars
      - blocks[]:     component array — at minimum one shared.rich-text with
                      the full markdown body in `body`
      - category:     documentId STRING (not array, not numeric id). Resolved
                      by name from Strapi when STRAPI_BASE_URL + STRAPI_API_TOKEN
                      are set; omitted otherwise so the package still serialises
                      in dry-runs.
      - publishedAt:  ISO timestamp to publish live, null for draft.

    Strict-mode rejection list (PLEAA-457, 2026-05-07): the live Strapi
    rejects unknown keys with HTTP 400 ``Invalid key <name>``. Fields that
    looked plausible but are NOT in the schema and would fail every POST:
    ``author_name``, ``read_time``, ``readTime``, ``cover_image_url``,
    ``coverImage``, ``tags``, ``excerpt``, ``content``. ``author`` and
    ``cover`` exist as relations to the Author / Media content-types.
    ``cover`` (Media) takes a numeric upload id; ``author`` (Author) takes the
    Strapi v5 documentId STRING — see ``author_document_id`` below.

    Cover relation (PLEAA-570, 2026-05-11): when ``cover_file_id`` is set,
    the article-level ``cover`` relation is included in the payload so
    consumers that read ``article.cover`` directly (RSS feed, social cards,
    OG tags, admin preview UI) resolve the same hero image the public page
    renders. Before PLEAA-570, auto-published articles left ``cover`` null
    and the public page only worked because Next.js synthesized the hero
    URL from a slug-derived CDN convention. ``cover`` is emitted as a bare
    integer (Strapi v5 single-media field), matching the upload response's
    ``id`` from :func:`upload_to_strapi_media`.

    Author relation (multi-author byline, 2026-06): when ``author_document_id``
    is set, the article-level ``author`` relation is included so the byline
    resolves on the public page / RSS / OG. The value comes from the draft's
    byline stamp (``<!-- byline: … | persona: <slug> -->``) mapped through
    ``PERSONA_AUTHORS``. Emitted as the documentId STRING (Strapi v5 accepts the
    string form for a relation); the ``{"connect": [<documentId>]}`` object form
    is the documented fallback if a Strapi build rejects the string. Omitted when
    no byline was found, so untagged drafts still publish (attach in admin).

    SEO metadata (DOD#4, resolved 2026-05-07): the Article content-type
    does NOT expose a ``seo`` field, ``seo`` component, or separate
    ``/api/seos`` collection (verified — populate=seo and /api/seos both
    return 400/404). ``title`` + ``description`` ARE the SEO surface: the
    frontend renders ``<title>`` from ``title`` and ``<meta name="description">``
    from ``description`` (hence the 80-char cap matching Google's mobile
    snippet ceiling). If a richer SEO model is ever needed, add a ``seo``
    component to the Article type in Strapi admin first; do not pre-emit it.

    The ``author_name`` and ``cover_image_url`` parameters are kept on the
    function signature for backwards compatibility with existing callers
    (notably ``main()`` and any orchestrator override) but are intentionally
    NOT emitted into the payload. ``compute_read_time`` is similarly retained
    for callers that want to surface a read-time number in the publish
    package's README, but the value never crosses the wire to Strapi.
    """
    description_source = extract_excerpt(body_md) or title
    description = truncate_description(description_source, limit=80)

    # PLEAA-528 (2026-05-08): when images were uploaded to Strapi, split the
    # body into alternating shared.rich-text + shared.media blocks so the
    # frontend actually renders each image. Falls back to single-block when
    # no media_map (dry-run, unconfigured Strapi, or article with no images).
    blocks = build_blocks(body_md, media_map)

    payload: dict = {
        "data": {
            "title": title,
            "slug": slug,
            "description": description,
            "blocks": blocks,
            "publishedAt": published_at,
        }
    }

    category_document_id = resolve_category_document_id(category_name)
    if category_document_id:
        payload["data"]["category"] = category_document_id

    # PLEAA-570 (2026-05-11): attach the article-level cover relation so
    # admin preview / RSS / OG tags / social cards resolve the hero from the
    # canonical ``article.cover`` field instead of relying on the brittle
    # slug-derived URL convention the public page falls back to. Emit only
    # when we have a real upload id — Strapi v5 rejects unknown relations
    # silently (would store null) but accepts a bare integer for single
    # media fields.
    if isinstance(cover_file_id, int) and cover_file_id > 0:
        payload["data"]["cover"] = cover_file_id

    # Multi-author byline (2026-06): attach the Strapi `author` relation derived
    # from the draft's byline stamp (persona slug → documentId via PERSONA_AUTHORS).
    # Strapi v5 accepts the documentId STRING for a relation field. If the string
    # form is ever rejected, use the connect form instead:
    #     payload["data"]["author"] = {"connect": [author_document_id]}
    # Omitted entirely when no byline was found, so untagged drafts still publish
    # (author left unset; attach manually in admin).
    if author_document_id:
        payload["data"]["author"] = author_document_id

    return payload


RENDER_TABLE_CARD = (
    ROOT / ".claude" / "skills" / "generate-visuals" / "scripts" / "render_table_card.py"
)
GFM_TABLE_RE = re.compile(
    r"(?m)^\|.*\|[ \t]*\n\|[ \t:|-]+\|[ \t]*\n(?:\|.*\|[ \t]*\n?)+"
)


def _split_gfm_row(line: str) -> list[str]:
    """Split a GFM table row into trimmed cell strings."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


# Opener / closer for an authored `:::fence … :::` block. Used to find the
# character spans of every fence so the GFM→table-card workaround can skip any
# table that lives INSIDE a fence (see _fence_spans / convert_gfm_tables).
_FENCE_OPEN_RE = re.compile(r"(?m)^[ \t]*:::[A-Za-z][\w-]*\b.*$")
_FENCE_CLOSE_RE = re.compile(r"(?m)^[ \t]*:::[ \t]*$")


def _fence_spans(md: str) -> list[tuple[int, int]]:
    """Return (start, end) char spans of every top-level `:::fence … :::` block.

    Walks the text line-anchored: a named opener (`:::name…`) starts a block, the
    next bare `:::` closes it. `:::stat-group` nests bare-named `:::stat` openers,
    so we depth-count — a block ends only when depth returns to zero. Tables that
    fall inside any returned span must NOT be converted to table-cards, because
    the renderer parses the GFM table *inside* `:::table` / `:::feature-matrix` /
    `:::decision-table` itself (Render contract, examples/ahrefs-components.md).
    """
    # Collect every fence-ish line (opener or closer) with its position, in order.
    events: list[tuple[int, int, bool]] = []  # (start, end, is_opener)
    for m in _FENCE_OPEN_RE.finditer(md):
        events.append((m.start(), m.end(), True))
    for m in _FENCE_CLOSE_RE.finditer(md):
        # A bare `:::` also matches _FENCE_OPEN_RE? No — opener requires a letter
        # after `:::`, so closers and openers are disjoint. Safe to merge.
        events.append((m.start(), m.end(), False))
    events.sort(key=lambda e: e[0])

    spans: list[tuple[int, int]] = []
    depth = 0
    block_start = 0
    for start, end, is_opener in events:
        if is_opener:
            if depth == 0:
                block_start = start
            depth += 1
        else:  # closer
            if depth > 0:
                depth -= 1
                if depth == 0:
                    spans.append((block_start, end))
    return spans


def convert_gfm_tables(body_md: str, slug: str) -> str:
    """PLEAA-567 publish-boundary workaround: the public Next.js renderer can't
    render GFM tables, so replace each markdown table with (a) a brand table-card
    PNG via render_table_card.py and (b) a crawlable bulleted text fallback (one
    bullet per row, bold first-column label). When the renderer ships GFM support,
    delete this step — nothing upstream changes (the draft keeps real tables).

    Fence-aware (component library): a GFM table that lives INSIDE a `:::fence`
    block is left untouched. The table-bearing fences `:::table`,
    `:::feature-matrix`, and `:::decision-table` carry a real GFM table that the
    blog-page renderer parses itself (mapping `yes`/`no`/`partial` → ✓/✕/–,
    applying caption/source/winner-row), per the Render contract in
    examples/ahrefs-components.md. Converting that inner table to a PNG here would
    break the fence's verbatim-preservation contract and pre-empt the renderer, so
    we skip any table whose span falls within a fence. Only bare body tables (not
    wrapped in a fence) get the table-card workaround.
    """
    if not GFM_TABLE_RE.search(body_md):
        return body_md
    if not RENDER_TABLE_CARD.exists():
        sys.stderr.write(
            f"warning: render_table_card.py not found at {RENDER_TABLE_CARD}; "
            "leaving GFM tables inline (public renderer can't display them)\n"
        )
        return body_md

    fence_spans = _fence_spans(body_md)

    def _inside_fence(start: int, end: int) -> bool:
        return any(fs <= start and end <= fe for fs, fe in fence_spans)

    img_dir = IMAGES_DIR / slug
    img_dir.mkdir(parents=True, exist_ok=True)
    counter = {"n": 0}

    def _replace(m: re.Match) -> str:
        block = m.group(0)
        # Skip tables inside a `:::fence` — the renderer handles those (see docstring).
        if _inside_fence(m.start(), m.end()):
            return block
        lines = [ln for ln in block.splitlines() if ln.strip().startswith("|")]
        if len(lines) < 3:
            return block  # not a real table (header + separator + >=1 row)
        cols = _split_gfm_row(lines[0])
        rows = [_split_gfm_row(ln) for ln in lines[2:] if ln.strip()]
        ncol = len(cols)
        rows = [r + [""] * (ncol - len(r)) if len(r) < ncol else r[:ncol] for r in rows]

        counter["n"] += 1
        out_png = img_dir / f"table-pub-{counter['n']}.png"
        spec = {
            "title": "",
            "columns": cols,
            "rows": rows,
            "col_weights": [1.0] * ncol,
        }
        spec_path = img_dir / f".table-pub-{counter['n']}-spec.json"
        spec_path.write_text(json.dumps(spec), encoding="utf-8")
        try:
            subprocess.run(
                [sys.executable, str(RENDER_TABLE_CARD),
                 "--spec", str(spec_path), "--out", str(out_png)],
                check=True, capture_output=True, text=True,
            )
        except (subprocess.CalledProcessError, OSError) as e:
            sys.stderr.write(f"warning: table-card render failed ({e}); leaving table inline\n")
            return block
        finally:
            spec_path.unlink(missing_ok=True)

        alt = (cols[0] if cols else "comparison") + " table"
        rel = f"images/{slug}/{out_png.name}"
        bullets = []
        for r in rows:
            label = r[0]
            rest = " — ".join(c for c in r[1:] if c)
            bullets.append(f"- **{label}** — {rest}" if rest else f"- **{label}**")
        return f"![{alt}]({rel})\n\n" + "\n".join(bullets) + "\n"

    return GFM_TABLE_RE.sub(_replace, body_md)


def find_image_refs(md: str) -> list[tuple[str, str]]:
    """Return list of (alt, relative-path-from-content-pipeline)."""
    return [(m.group(1), m.group(2)) for m in IMAGE_REF_RE.finditer(md)]


def copy_images_to_publish(out_dir: Path, refs: list[tuple[str, str]]) -> list[Path]:
    """Copy referenced images into <out_dir>/media/, return the absolute paths."""
    if not refs:
        return []
    media_dir = out_dir / "media"
    media_dir.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for _, rel in refs:
        src = ROOT / "content-pipeline" / rel
        if not src.exists():
            sys.stderr.write(f"warning: missing image {src}\n")
            continue
        dest = media_dir / src.name
        try:
            dest.write_bytes(src.read_bytes())
            copied.append(dest)
        except OSError as exc:
            sys.stderr.write(f"warning: copy failed {src}: {exc}\n")
    return copied


def upload_to_strapi_media(image_paths: list[Path], base_url: str, token: str) -> dict[str, dict]:
    """POST each image to /api/upload, return mapping of filename -> {id, url}.

    Strapi Cloud rewrites uploaded asset URLs to a separate media subdomain
    (e.g. ``media.strapiapp.com/<file>_<hash>.png``) instead of serving them
    from ``{base_url}/uploads/<filename>``. We must trust the ``url`` field
    that Strapi returns from /api/upload — synthesizing /uploads/ paths
    produces 404s on Strapi Cloud (PLEAA-499 followup, 2026-05-08).
    """
    if not image_paths:
        return {}
    try:
        import urllib.request
        import uuid
        import mimetypes
    except ImportError as exc:
        sys.stderr.write(f"warning: stdlib missing for media upload ({exc}); skipping\n")
        return {}

    endpoint = f"{base_url.rstrip('/')}/api/upload"
    base = base_url.rstrip("/")
    out: dict[str, dict] = {}
    for path in image_paths:
        boundary = uuid.uuid4().hex
        mime = mimetypes.guess_type(path.name)[0] or "image/png"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="files"; filename="{path.name}"\r\n'
            f"Content-Type: {mime}\r\n\r\n"
        ).encode("utf-8")
        body += path.read_bytes() + f"\r\n--{boundary}--\r\n".encode("utf-8")
        req = urllib.request.Request(
            endpoint,
            data=body,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, list) and data:
                first = data[0]
                if isinstance(first, dict) and "id" in first:
                    rel_url = first.get("url") or ""
                    # Strapi Cloud returns absolute URLs (https://...media.strapiapp.com/...);
                    # self-hosted returns paths like "/uploads/<file>". Make absolute either way.
                    if rel_url.startswith("//"):
                        full_url = f"https:{rel_url}"
                    elif rel_url.startswith("http"):
                        full_url = rel_url
                    elif rel_url:
                        full_url = f"{base}{rel_url if rel_url.startswith('/') else '/' + rel_url}"
                    else:
                        # Fallback to legacy /uploads/<name> guess; will likely 404 on Strapi Cloud.
                        full_url = f"{base}/uploads/{path.name}"
                    out[path.name] = {"id": int(first["id"]), "url": full_url}
        except Exception as exc:
            sys.stderr.write(f"warning: upload failed for {path.name}: {exc}\n")
    return out


def rewrite_image_refs(md: str, base_url: str | None, media_map: dict[str, dict] | None = None) -> str:
    """Rewrite local image refs to absolute Strapi-served URLs.

    Prefers the ``url`` returned by ``/api/upload`` (correct for Strapi Cloud's
    separate media subdomain). Falls back to ``{base}/uploads/<filename>`` only
    when no upload entry exists for that filename. Without a base URL, leaves
    refs alone so the editor can drag from the publish package's ``media/``.
    """
    if not base_url:
        return md
    base = base_url.rstrip("/")
    media_map = media_map or {}

    def _rewrite(match: "re.Match[str]") -> str:
        alt = match.group(1)
        rel = match.group(2)
        filename = Path(rel).name
        entry = media_map.get(filename)
        if entry and entry.get("url"):
            return f"![{alt}]({entry['url']})"
        return f"![{alt}]({base}/uploads/{filename})"

    return IMAGE_REF_RE.sub(_rewrite, md)


def write_outputs(slug: str, body_md: str, payload: dict) -> Path:
    out_dir = OUT_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "article.md").write_text(body_md.strip() + "\n", encoding="utf-8")
    (out_dir / "article.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    data = payload["data"]
    # PLEAA-567: blocks may start with a `shared.media` (when the draft opens
    # with an uploaded image), which has no `body`. Pull stats from the first
    # `shared.rich-text` block instead of indexing position 0 blindly.
    first_rt = next(
        (b for b in data.get("blocks", []) if b.get("__component") == "shared.rich-text"),
        None,
    )
    body_text = first_rt.get("body", "") if first_rt else ""
    word_count = len(re.findall(r"\b\w+\b", body_text))
    category_value = data.get("category") or "(unresolved — set STRAPI_BASE_URL + STRAPI_API_TOKEN)"
    author_value = data.get("author") or "(none — no byline stamp in draft; attach manually if desired)"
    read_time_min = compute_read_time(body_text)
    readme = f"""# Publish package — {data['title']}

Generated by /format-for-publish. Strapi v5 schema (PLEAA-457). Two ways to use this:

## Option A — paste into Strapi admin (no API needed)
1. Open Strapi admin → Content Manager → create a new Article
2. Title: {data['title']}
3. Slug: {data['slug']}
4. Description (≤80 chars): {data['description']}
5. Blocks: paste the contents of `article.md` into a `shared.rich-text` block
6. Category (documentId): {category_value}
7. Author (documentId): {author_value} — derived from the draft byline stamp via PERSONA_AUTHORS. Cover relation auto-attached on `--auto-publish` to the first uploaded image (PLEAA-570)
8. Save as draft, review, then publish

## Option B — direct API publish (when Doppler creds are wired)
```bash
doppler run -- python .claude/skills/format-for-publish/scripts/format_for_strapi.py {slug} --publish
```
Requires STRAPI_BASE_URL and STRAPI_API_TOKEN env vars.

## Files
- `article.md` — clean markdown body (paste in Strapi rich-text block)
- `article.json` — Strapi v5 payload (for API publish)
- `README.md` — this file

## Stats
- Word count: {word_count}
- Description length: {len(data['description'])} chars (cap 80)
- Read time: ~{read_time_min} min (computed at 220 wpm; informational only — not in payload)
- Blocks: {len(data.get('blocks', []))}
"""
    (out_dir / "README.md").write_text(readme, encoding="utf-8")
    return out_dir


def find_existing_article_id(base_url: str, token: str, slug: str) -> str | None:
    """Look up the Strapi v5 article documentId for a slug.

    Strapi v5 routes entity URLs by documentId (string), not numeric id, so
    we return that here. Returns None if not found.
    """
    import urllib.parse
    import urllib.request

    endpoint = f"{base_url.rstrip('/')}/api/articles?filters[slug][$eq]={urllib.parse.quote(slug)}"
    req = urllib.request.Request(
        endpoint,
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        items = data.get("data") if isinstance(data, dict) else None
        if isinstance(items, list) and items:
            entry = items[0]
            if isinstance(entry, dict):
                # v5 places documentId at the top level; some Strapi configs
                # still mirror it under attributes.
                doc_id = entry.get("documentId") or (entry.get("attributes") or {}).get("documentId")
                if isinstance(doc_id, str) and doc_id:
                    return doc_id
    except Exception as exc:
        sys.stderr.write(f"warning: lookup of slug {slug!r} failed: {exc}\n")
    return None


def publish_to_strapi(payload: dict, *, update: bool = False) -> None:
    """Push payload to Strapi.

    POST to /api/articles by default. If `update=True`, looks up the existing
    article by slug and PUTs /api/articles/{documentId} instead. Strapi v5
    uses PUT for updates with full-replacement semantics — fields not present
    in the payload are wiped on the server. Callers that want to preserve
    admin-edited fields (e.g. a manually attached cover image) must include
    those fields in the update payload, or POST a brand-new article instead.
    PLEAA-457 (Greptile P2): the original docstring + PR description called
    this "PATCH" which is a v4 idiom and misleads anyone reading the code.

    Update-path safety guard (PLEAA-457 Greptile P1, round 2): on the PUT path,
    if ``payload.data.category`` is missing we abort instead of sending the
    request. Strapi's PUT semantics would otherwise WIPE the article's existing
    category server-side, which is exactly the silent destructive-failure class
    this PR was opened to close. The most common cause is a transient
    ``/api/categories`` fetch failure inside ``_load_category_index``; the
    cache stays ``None`` so the next run retries cleanly, but only if we don't
    let this PUT through. POSTs are still allowed without ``category`` (a
    brand-new article without a category is recoverable in admin; an existing
    one having its category wiped is not).
    """
    base_url = os.environ.get("STRAPI_BASE_URL")
    token = os.environ.get("STRAPI_API_TOKEN")
    if not base_url or not token:
        sys.exit("error: STRAPI_BASE_URL and STRAPI_API_TOKEN env vars required for --publish")
    try:
        import urllib.request
    except ImportError:
        sys.exit("error: stdlib urllib unavailable (impossible on stdlib Python)")

    method = "POST"
    endpoint = f"{base_url.rstrip('/')}/api/articles"
    if update:
        slug = payload.get("data", {}).get("slug")
        if not slug:
            sys.exit("error: --update requires payload to have data.slug")
        existing_doc_id = find_existing_article_id(base_url, token, slug)
        if existing_doc_id is None:
            sys.stderr.write(f"warning: --update set but slug {slug!r} not found in Strapi; falling back to POST\n")
        else:
            # Refuse to PUT when category resolution failed — see docstring.
            if not (payload.get("data") or {}).get("category"):
                sys.exit(
                    "error: --update with missing data.category — refusing to PUT.\n"
                    "  Strapi v5 PUT is full-replacement; sending this would wipe the\n"
                    "  existing article's category server-side. Most likely cause: a\n"
                    "  transient /api/categories fetch failure in _load_category_index.\n"
                    "  Re-run when Strapi is reachable; the category cache resets per\n"
                    "  process so the next run will retry cleanly."
                )
            method = "PUT"
            endpoint = f"{base_url.rstrip('/')}/api/articles/{existing_doc_id}"

    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"{'updated' if method == 'PUT' else 'published'} — {resp.status} {resp.reason}")
            print(resp.read().decode("utf-8"))
    except Exception as e:
        sys.exit(f"error: Strapi {method} failed: {e}")


def _supabase_url_from_env() -> str | None:
    return (
        os.environ.get("SUPABASE_URL")
        or os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
        or os.environ.get("PUBLIC_SUPABASE_URL")
    )


def _supabase_service_key_from_env() -> str | None:
    return (
        os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        or os.environ.get("SUPABASE_SERVICE_KEY")
        or os.environ.get("SUPABASE_SERVICE_ROLE")
    )


def _strapi_webhook_secret_from_env() -> str | None:
    return os.environ.get("STRAPI_WEBHOOK_SECRET")


def assert_blog_post_mirrored(slug: str, *, max_attempts: int = 30, sleep_seconds: float = 10.0) -> None:
    """Fail the publish run unless the public-site mirror contains the slug.

    Strapi can return 2xx while the public site still 404s: the Next.js blog
    reads Supabase ``blog_posts``, and ``sync-blog-posts`` refuses a publish
    unless ``blog_publish_approvals`` has a row for the slug/documentId. After a
    direct API publish, keep triggering the existing sync function and polling
    the public mirror row long enough for the approval workflow to finish.
    """
    supabase_url = (_supabase_url_from_env() or "").rstrip("/")
    service_key = _supabase_service_key_from_env() or ""
    if not supabase_url or not service_key:
        sys.exit(
            "error: post-publish mirror assertion requires SUPABASE_URL "
            "(or NEXT_PUBLIC_SUPABASE_URL) and SUPABASE_SERVICE_ROLE_KEY"
        )

    import urllib.error
    import urllib.parse
    import urllib.request

    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
    }
    sync_headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {_strapi_webhook_secret_from_env() or service_key}",
    }

    sync_endpoint = f"{supabase_url}/functions/v1/sync-blog-posts"
    # The Supabase edge function explicitly supports GET as its manual full-sync trigger.
    sync_req = urllib.request.Request(sync_endpoint, headers=sync_headers, method="GET")
    query = urllib.parse.urlencode(
        {
            "slug": f"eq.{slug}",
            "select": "slug,status,title,published_at",
            "limit": "1",
        }
    )
    endpoint = f"{supabase_url}/rest/v1/blog_posts?{query}"
    req = urllib.request.Request(endpoint, headers={**headers, "Accept": "application/json"}, method="GET")
    last_seen = "no row"
    for attempt in range(1, max_attempts + 1):
        try:
            with urllib.request.urlopen(sync_req, timeout=60) as resp:
                sync_body = resp.read().decode("utf-8", errors="replace")[:500]
                print(f"sync-blog-posts — {resp.status} {resp.reason}: {sync_body}")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:500]
            sys.exit(f"error: sync-blog-posts failed HTTP {exc.code}: {body}")
        except Exception as exc:
            sys.exit(f"error: sync-blog-posts failed: {type(exc).__name__}: {exc}")

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                rows = json.loads(resp.read().decode("utf-8"))
        except Exception as exc:
            last_seen = f"{type(exc).__name__}: {exc}"
        else:
            row = rows[0] if isinstance(rows, list) and rows else None
            if isinstance(row, dict):
                status = row.get("status")
                last_seen = json.dumps(row, ensure_ascii=False)
                if status == "published":
                    print(f"public mirror OK — blog_posts slug={slug!r} status=published")
                    return
        if attempt < max_attempts:
            time.sleep(sleep_seconds)
    sys.exit(
        f"error: public mirror missing or not published for slug={slug!r} "
        f"after {max_attempts} attempt(s); last_seen={last_seen}"
    )


# ---------- GitHub-Pages whiteboard staging (PLEAA-448) ----------
# After format-for-publish writes the Strapi package, also bake a static
# `docs/run-<slug>.html` viewer and append the slug to the fallback runs
# array in `docs/index.html` so the run shows up at
# https://lionelndong.github.io/blog-agent-2/ as soon as the operator pushes
# `main`. The GitHub-API enumeration path in index.html is rate-limited and
# unreliable, so the static fallback is the source of truth.
#
# This step is best-effort: a failure here must NOT fail the publish run —
# the publish package is the primary deliverable and the operator can
# always run `python scripts/bundle_viewer.py <slug>` manually.

# The fallback runs array is a JS literal on a single line in docs/index.html.
# We match it loosely so we tolerate whitespace/newline drift but require the
# array to be the one inside the `catch` block (the only `return [...]` of
# string-literals followed by `;` in the file).
_FALLBACK_RUNS_RE = re.compile(
    r'(return\s*\[)([^\]]*?)(\]\s*;)',
)


def _update_index_fallback(slug: str) -> tuple[bool, str]:
    """Idempotently append slug to the fallback runs array in docs/index.html.

    Returns (changed, message). Never raises.
    """
    if not INDEX_HTML.exists():
        return False, f"docs/index.html not found at {INDEX_HTML}"
    try:
        html = INDEX_HTML.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"read error: {e}"

    match = _FALLBACK_RUNS_RE.search(html)
    if not match:
        return False, "fallback runs array not found in docs/index.html"

    body = match.group(2)
    # Existing slugs are quoted strings; cheap parse via regex.
    existing = re.findall(r'"([^"]+)"', body)
    if slug in existing:
        return False, f"slug already in fallback runs ({len(existing)} entries)"

    new_list = existing + [slug]
    rendered = ", ".join(f'"{s}"' for s in new_list)
    new_body = match.group(1) + rendered + match.group(3)
    new_html = html[: match.start()] + new_body + html[match.end():]
    try:
        INDEX_HTML.write_text(new_html, encoding="utf-8")
    except Exception as e:
        return False, f"write error: {e}"
    return True, f"appended to fallback runs ({len(new_list)} entries)"


def _bundle_run_viewer(slug: str) -> tuple[bool, str]:
    """Run scripts/bundle_viewer.py to write docs/run-<slug>.html. Never raises."""
    if not BUNDLE_VIEWER.exists():
        return False, f"bundle_viewer.py not found at {BUNDLE_VIEWER}"
    try:
        proc = subprocess.run(
            [sys.executable, str(BUNDLE_VIEWER), slug],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
    except Exception as e:
        return False, f"subprocess failed: {e}"
    if proc.returncode != 0:
        return False, f"bundle_viewer exit {proc.returncode}: {proc.stderr.strip()[:200]}"
    out_path = DOCS_DIR / f"run-{slug}.html"
    if not out_path.exists():
        return False, f"bundle_viewer ran but {out_path} missing"
    return True, f"wrote {out_path.relative_to(ROOT)} ({out_path.stat().st_size:,} bytes)"


def stage_whiteboard(slug: str) -> None:
    """Stage the GitHub-Pages whiteboard artifacts for `slug`.

    Idempotent: re-running for the same slug overwrites the bundle and
    leaves the index untouched if the slug is already in the fallback list.
    Best-effort: failures print a warning but never raise.
    """
    print(f"\n--- whiteboard staging for {slug} ---")
    bundled, bmsg = _bundle_run_viewer(slug)
    print(f"  bundle: {'ok' if bundled else 'skipped'} — {bmsg}")

    if not bundled:
        print(
            "  hint: run `python scripts/bundle_viewer.py "
            f"{slug}` manually to regenerate the static viewer."
        )
        return

    indexed, imsg = _update_index_fallback(slug)
    print(f"  index:  {'updated' if indexed else 'unchanged'} — {imsg}")

    # Best-effort `git add` so the operator just has to commit + push.
    paths_to_stage = [DOCS_DIR / f"run-{slug}.html"]
    if indexed:
        paths_to_stage.append(INDEX_HTML)
    try:
        rels = [str(p.relative_to(ROOT)) for p in paths_to_stage]
        proc = subprocess.run(
            ["git", "add", "--", *rels],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=20,
        )
        if proc.returncode == 0:
            print(f"  staged: {', '.join(rels)}")
            print(
                "  hint: commit + push `main` to surface this run on "
                "https://lionelndong.github.io/blog-agent-2/"
            )
        else:
            # Non-fatal: maybe not a git repo, or git missing. Just tell the
            # operator the file paths so they can stage manually.
            print(
                "  staged: git add skipped — "
                f"{proc.stderr.strip()[:120] or 'non-zero exit'}"
            )
            print(f"  files: {', '.join(rels)}")
    except Exception as e:
        rels = [str(p.relative_to(ROOT)) for p in paths_to_stage]
        print(f"  staged: git add unavailable ({e}); files: {', '.join(rels)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    parser.add_argument("--publish", action="store_true", help="Direct API publish (requires STRAPI_BASE_URL + STRAPI_API_TOKEN)")
    parser.add_argument("--auto-publish", action="store_true", help="Set publishedAt = now (live publish, not draft). Implies --publish. Requires quality-check verdict != FAIL.")
    parser.add_argument("--update", action="store_true", help="PUT the existing Strapi article by slug instead of POST (full-replacement semantics — fields absent from the payload get wiped). For /update-pipeline runs.")
    parser.add_argument(
        "--human-approved",
        default=None,
        metavar="REASON",
        help=(
            "PLEAA-581 escape hatch: bypass the artifact-in-origin/main gate "
            "with a written rationale (required, non-empty). Appends an audit "
            "line to content-pipeline/audit/publish-overrides.log. Use only "
            "when a manual unpublish/reseed or hotfix needs to run before the "
            "publish package has been committed to main."
        ),
    )
    args = parser.parse_args()

    auto_publish = args.auto_publish or os.environ.get("BLOG_AGENT_AUTO_PUBLISH") == "1"
    publish_via_api = args.publish or auto_publish  # auto-publish implies --publish

    # PLEAA-581 Layer 1: hard gate before any HTTP write to Strapi (upload OR
    # publish). The check is artifact-side: the slug's publish package must be
    # committed to origin/main. A --human-approved override is the only escape
    # hatch and logs a tab-separated audit line. Local-only runs (no --publish /
    # no --auto-publish) still write the package to disk and bypass the gate —
    # that's the explicit "generate, review, commit, then publish" workflow.
    human_override_reason: str | None = None
    if publish_via_api:
        if args.human_approved is not None:
            reason = (args.human_approved or "").strip()
            if not reason:
                sys.exit(
                    "error: --human-approved requires a non-empty reason string. "
                    "Quote the reason: --human-approved \"manual unpublish reseed\""
                )
            log_path = log_publish_override(args.slug, reason)
            human_override_reason = reason
            sys.stderr.write(
                f"publish gate OVERRIDDEN — reason={reason!r}; "
                f"audit appended to {log_path.relative_to(ROOT) if log_path.is_relative_to(ROOT) else log_path}\n"
            )
        else:
            allow, reason_msg = verify_publish_artifact(args.slug)
            if not allow:
                sys.exit(f"error: {reason_msg}")
            else:
                print(reason_msg)

    if auto_publish:
        allow, reason = quality_precondition(args.slug)
        if not allow:
            sys.exit(f"error: auto-publish refused — {reason}")
        else:
            print(f"quality-check precondition passed ({reason})")

    raw = read_draft(args.slug)
    # Multi-author byline: parse the persona slug from the byline stamp on the RAW
    # draft, before scrub_pipeline_scaffolding strips all HTML comments (the byline
    # is one). Maps slug → Strapi Author documentId; None when no byline present.
    byline_persona = extract_byline_persona(raw)
    author_document_id = resolve_author_document_id(byline_persona)
    if author_document_id:
        print(f"byline persona: {byline_persona} → author documentId {author_document_id}")
    elif byline_persona:
        print(f"byline persona: {byline_persona} (no documentId mapping; author unset)")
    else:
        print("no byline comment found; author relation left unset")
    no_notes = strip_editor_notes(raw)
    # PLE-2646: auto-remove structural QA scaffolding (HTML comments, manifest
    # captions) before anything else looks at the body. This also removes the
    # byline stamp comment (already captured above).
    no_notes = scrub_pipeline_scaffolding(no_notes)
    title, body = extract_title(no_notes)
    body = transform_callouts(body)
    # PLEAA-567 publish-boundary workaround: convert GFM tables to table-cards +
    # bulleted fallback so the public renderer (no GFM support yet) shows them.
    body = convert_gfm_tables(body, args.slug)

    # Deferred-visual handling (2026-06): visuals are DEFERRED — the visuals stage
    # leaves typed placeholders, generates nothing, and does NOT gate. So a raw
    # [VISUAL:...] / [SCREENSHOT:...] reaching this point is EXPECTED, not an error.
    # We no longer hard-fail (the old PLEAA-392 gate); instead we convert each
    # leftover placeholder into an HTML comment `<!-- VISUAL-TODO: ...original... -->`
    # so the marker is retained in the published source for the future visuals agent
    # but stays invisible on the live site. This runs AFTER scrub_pipeline_scaffolding
    # (which removed QA comments from the body), so these VISUAL-TODO comments are
    # intentionally preserved through to article.md.
    deferred_visuals = VISUAL_PLACEHOLDER_RE.findall(body)
    body = defer_visual_placeholders(body)
    if deferred_visuals:
        print(
            f"deferred {len(deferred_visuals)} [VISUAL:...]/[SCREENSHOT:...] "
            f"placeholder(s) → retained as <!-- VISUAL-TODO: ... --> (visuals deferred)"
        )

    # PLE-2646 hard gate: never ship inline QA/research scaffolding to readers.
    # Runs after auto-strip + callout/table transforms so it judges the exact
    # text that would land in the published block.
    assert_no_pipeline_leak(body, args.slug)

    # Always copy referenced images into the publish folder so the editor can paste manually
    image_refs = find_image_refs(body)
    out_dir = OUT_DIR / args.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    copied_images = copy_images_to_publish(out_dir, image_refs)

    base_url = os.environ.get("STRAPI_BASE_URL")
    token = os.environ.get("STRAPI_API_TOKEN")

    media_map: dict[str, dict] = {}
    if publish_via_api and base_url and token and copied_images:
        media_map = upload_to_strapi_media(copied_images, base_url, token)
        if media_map:
            print(f"uploaded {len(media_map)} images to Strapi media library")
    body = rewrite_image_refs(body, base_url if (base_url and media_map) else None, media_map)

    published_at = datetime.now(timezone.utc).isoformat() if auto_publish else None
    cover_image_url = extract_cover_image_url(body, base_url)
    # PLEAA-570: pick the upload id of the hero image so build_payload can
    # set the top-level ``cover`` relation. Mirrors extract_cover_image_url's
    # selection (first absolute image ref) so the cover stays in sync with
    # what the body shows.
    cover_file_id = resolve_cover_file_id(body, media_map)
    if cover_file_id is not None:
        print(f"cover relation resolved: upload id {cover_file_id}")
    # PLEAA-524: resolve category from the raw cited draft (frontmatter wins,
    # slug-heuristic fallback). `raw` carries the editor-notes block intact —
    # we resolve before strip_editor_notes() above already ran (`raw` is
    # untouched), but downstream `body` is already cleaned, so reach for `raw`.
    category_name = resolve_category_name(args.slug, raw)
    print(f"category resolved: {category_name}")
    payload = build_payload(
        args.slug,
        title,
        body,
        published_at=published_at,
        category_name=category_name,
        cover_image_url=cover_image_url,
        media_map=media_map,
        cover_file_id=cover_file_id,
        author_document_id=author_document_id,
    )
    out_dir = write_outputs(args.slug, body, payload)
    manifest_path = write_manifest(out_dir, args.slug, title)
    print(f"wrote {out_dir}/article.md")
    print(f"wrote {out_dir}/article.json")
    print(f"wrote {out_dir}/README.md")
    print(f"wrote {manifest_path.relative_to(ROOT) if manifest_path.is_relative_to(ROOT) else manifest_path}")
    if copied_images:
        print(f"copied {len(copied_images)} image(s) to {out_dir / 'media'}")

    if publish_via_api:
        publish_to_strapi(payload, update=args.update)
        assert_blog_post_mirrored(args.slug)

    # PLEAA-448: bake the static GitHub-Pages viewer + index entry so the run
    # surfaces at https://lionelndong.github.io/blog-agent-2/ as soon as the
    # operator pushes `main`. Best-effort — never blocks publish.
    if os.environ.get("BLOG_AGENT_SKIP_WHITEBOARD") != "1":
        stage_whiteboard(args.slug)


if __name__ == "__main__":
    main()
