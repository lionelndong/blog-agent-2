#!/usr/bin/env python3
"""Automated quality metrics for a draft — benchmark-relative (2026-06-12 rebuild).

The old version scored compliance (paragraph lengths, em-dash quotas) and let
objectively thin articles score 95. This version scores *competitiveness*
against the research dossier's BEAT SPEC, plus the mechanical AI-tell signals
that don't lie.

Computes:
  - Beat-spec compliance: draft word count vs target, item count, table presence
  - Consensus-topic coverage: every must-cover topic from the dossier present
  - Evidence: numeric-claim density, citation ratio, naked [link] count
  - AI tells: forbidden phrases, BLUF failures, crutch repetition, rhythm uniformity
  - A 0-100 mechanical score with per-dimension subscores (the SKILL combines
    this with the adversarial read for the final verdict)

Usage:
    python .claude/skills/quality-check/scripts/quality_check.py <slug> [--stage cited]
"""
from __future__ import annotations

import argparse
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DRAFT_DIR = ROOT / "content-pipeline" / "5-drafts"
CITED_DIR = ROOT / "content-pipeline" / "6-drafts-cited"
RESEARCH_DIR = ROOT / "content-pipeline" / "1-research"
BRAND_CONFIG = ROOT / "brand-config.md"
OUT_DIR = ROOT / "content-pipeline" / "quality-checks"

BLUF_BAD_OPENERS = [
    r"^in this section", r"^now that we", r"^now let", r"^before we",
    r"^let'?s look", r"^let'?s explore", r"^let'?s dive", r"^let'?s talk",
    r"^let me", r"^to begin", r"^first of all", r"^firstly", r"^moreover",
    r"^furthermore", r"^additionally", r"^as we mentioned", r"^as discussed",
    r"^when it comes to", r"^it'?s important to (note|understand|remember)",
    r"^one of the (most |key )?(things|aspects|factors)",
]

# Known stylistic crutch words — repetition of these reads as a tic regardless of topic.
CRUTCH_LEXICON = {
    "honest", "honestly", "plainly", "genuinely", "truly", "actually", "simply",
    "essentially", "basically", "clear", "clearly", "straightforward", "frankly",
    "seamless", "robust", "powerful", "comprehensive", "ultimately", "crucial",
    "elevate", "unlock", "supercharge", "delve", "landscape", "journey",
}

STOPWORDS = set(
    """the a an and or but if then else for to of in on at by with from as is are was were be been
    being have has had do does did will would can could should may might must not no nor this that
    these those it its they them their there here you your yours we our ours i me my he she his her
    what which who whom how when where why all any both each few more most other some such only own
    same so than too very just also even still about into over under again once during before after
    between out off above below up down s t don re ll ve d m o won isn aren doesn didn hasn haven
    wasn weren wouldn couldn shouldn mightn mustn needn""".split()
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def words(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z'-]*", text.lower())


def strip_markup(text: str) -> str:
    text = re.sub(r"\[VISUAL:[^\]]*\]", "", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`[^`]*`", "", text)
    return text


def split_paragraphs(text: str) -> list[str]:
    out = []
    for chunk in re.split(r"\n\s*\n", text):
        chunk = chunk.strip()
        if not chunk or chunk.startswith("#") or chunk.startswith("|"):
            continue
        if re.match(r"^[-*]\s", chunk):  # list block counts as one unit
            out.append(chunk)
            continue
        out.append(chunk)
    return out


def load_forbidden_phrases() -> list[str]:
    text = read(BRAND_CONFIG)
    m = re.search(r"## Forbidden phrases.*?(?=^##\s|\Z)", text, re.MULTILINE | re.DOTALL)
    if not m:
        return []
    return re.findall(r'\s*-\s*"([^"]+)"', m.group(0))


def parse_beat_spec(dossier: str) -> dict:
    """Parse the BEAT SPEC block. Returns {} if absent (legacy dossier)."""
    m = re.search(r"## BEAT SPEC.*?(?=^##\s|\Z)", dossier, re.MULTILINE | re.DOTALL)
    if not m:
        return {}
    block = m.group(0)
    spec: dict = {}
    wc = re.search(r"[Tt]arget word count:?\s*\*{0,2}\s*([\d,]{3,6})", block)
    if wc:
        spec["target_words"] = int(wc.group(1).replace(",", ""))
    items = re.search(r"item count:?\s*\*{0,2}(\d{1,2})", block, re.IGNORECASE)
    if items:
        spec["item_count"] = int(items.group(1))
    table = re.search(r"[Cc]omparison table:?\s*\*{0,2}(required|yes)", block)
    spec["table_required"] = bool(table)
    # Capture only the Must-cover sub-list; stop at the next bolded sibling bullet
    # (e.g. "- **Differentiation topics:**") so it doesn't swallow later sections.
    topics_m = re.search(
        r"Must-cover topics[^\n]*\n(.*?)(?=\n\s*[-*]\s+\*\*|\Z)",
        block, re.DOTALL,
    )
    if topics_m:
        items = re.findall(r"^\s*(?:[-*]|\d+\.)\s+(.+)$", topics_m.group(1), re.MULTILINE)
        spec["must_cover"] = [
            re.sub(r"\s*\(.*?\)\s*$", "", re.sub(r"^\*+|\*+$", "", t).strip())
            for t in items
        ]
    return spec


def topic_covered(topic: str, draft_lower: str) -> bool:
    """A consensus topic counts as covered if most of its content words appear in the draft."""
    content_words = [w for w in words(topic) if w not in STOPWORDS and len(w) > 3]
    if not content_words:
        return True
    hits = sum(1 for w in content_words if w in draft_lower)
    return hits / len(content_words) >= 0.6


def crutch_phrases(text: str, topic_terms: set[str]) -> list[tuple[str, int]]:
    """Distinctive words/bigrams repeated enough to read as a tic."""
    toks = words(text)
    flagged: list[tuple[str, int]] = []
    uni = Counter(t for t in toks if t not in STOPWORDS and len(t) >= 5 and t not in topic_terms)
    n_words = max(len(toks), 1)
    for term, count in uni.most_common(40):
        if count >= 5 and count / n_words >= 4 / 1500:
            flagged.append((term, count))
    bigrams = Counter(
        f"{a} {b}" for a, b in zip(toks, toks[1:])
        if a not in STOPWORDS and b not in STOPWORDS and a not in topic_terms and b not in topic_terms
    )
    for phrase, count in bigrams.most_common(40):
        if count >= 3:
            flagged.append((phrase, count))
    return flagged[:10]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--stage", choices=["draft", "cited"], default="draft",
                    help="cited = post-verify-claims (naked [link] is a hard fail there)")
    args = ap.parse_args()

    draft_path = (CITED_DIR if args.stage == "cited" else DRAFT_DIR) / f"{args.slug}.md"
    raw = read(draft_path)
    if not raw:
        print(f"ERROR: no draft at {draft_path}", file=sys.stderr)
        return 2

    dossier = read(RESEARCH_DIR / f"{args.slug}.md")
    spec = parse_beat_spec(dossier)
    body = strip_markup(raw)
    body_words = len(words(body))
    title = (re.search(r"^#\s+(.+)$", raw, re.MULTILINE) or [None, args.slug])[1]
    # Topic terms repeat legitimately: title, slug, every H2/H3 header (app names,
    # comparison axes), and the brand name. Only NON-topical repetition is a crutch.
    headers = " ".join(re.findall(r"^#{2,3}\s+(.+)$", raw, re.MULTILINE))
    brand = (re.search(r"\*\*Name:\*\*\s*(.+)", read(BRAND_CONFIG)) or [None, ""])[1]
    topic_terms = {
        w for w in words(f"{title} {args.slug} {headers} {brand}") if w not in STOPWORDS
    }

    findings: list[str] = []
    scores: dict[str, tuple[float, float]] = {}  # dim -> (earned, weight)

    # --- Depth vs beat spec (25) ---
    if spec.get("target_words"):
        ratio = body_words / spec["target_words"]
        depth = max(0.0, min(1.0, (ratio - 0.5) / 0.35)) if ratio < 0.85 else (1.0 if ratio <= 1.35 else 0.85)
        findings.append(f"Word count: {body_words} vs target {spec['target_words']} (ratio {ratio:.2f})")
        if ratio < 0.7:
            findings.append("CRITICAL: draft is <70% of the beat-spec word target — thin against the SERP.")
    else:
        depth = 0.6 if body_words >= 1500 else 0.3
        findings.append(f"Word count: {body_words}; NO BEAT SPEC found in dossier (legacy?) — re-run /research.")
    h2s = re.findall(r"^##\s+(.+)$", raw, re.MULTILINE)
    if spec.get("item_count"):
        h3s = re.findall(r"^###\s+(.+)$", raw, re.MULTILINE)
        sections = len(h2s) + len(h3s)
        if sections < spec["item_count"]:
            depth = min(depth, 0.5)
            findings.append(
                f"CRITICAL: beat spec demands ~{spec['item_count']} items; draft has {sections} H2+H3 sections."
            )
    if spec.get("table_required") and not re.search(r"^\|.+\|\s*$", raw, re.MULTILINE):
        depth = min(depth, 0.6)
        findings.append("CRITICAL: beat spec requires a comparison table; none found in draft.")
    scores["depth_vs_benchmark"] = (depth * 25, 25)

    # --- Consensus coverage (20) ---
    draft_lower = " ".join(words(raw))
    must = spec.get("must_cover", [])
    if must:
        missing = [t for t in must if not topic_covered(t, draft_lower)]
        cov = 1 - len(missing) / len(must)
        for t in missing:
            findings.append(f"MISSING consensus topic: {t}")
        scores["consensus_coverage"] = (cov * 20, 20)
    else:
        scores["consensus_coverage"] = (10, 20)
        findings.append("No must-cover topics parsed from dossier — coverage unscored (10/20 neutral).")

    # --- Evidence (15) ---
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", body) if s.strip()]
    numeric = [s for s in sentences if re.search(r"\d", s)]
    naked_links = len(re.findall(r"\[link\]", raw))
    real_links = len(re.findall(r"\[[^\]]+\]\(https?://", raw))
    claim_density = len(numeric) / max(len(sentences), 1)
    ev = min(1.0, claim_density / 0.18) * 0.6 + min(1.0, real_links / 8) * 0.4
    if args.stage == "cited" and naked_links:
        ev = 0.0
        findings.append(f"CRITICAL: {naked_links} naked [link] placeholders remain post-citation.")
    elif naked_links:
        findings.append(f"{naked_links} [link] placeholders (OK at draft stage; verify-claims must resolve).")
    findings.append(f"Claim density {claim_density:.2f} ({len(numeric)}/{len(sentences)} sentences numeric); {real_links} hyperlinks.")
    scores["evidence"] = (ev * 15, 15)

    # --- AI tells (25) ---
    tell_penalty = 0.0
    forbidden = load_forbidden_phrases()
    hits = [(p, len(re.findall(re.escape(p), raw, re.IGNORECASE))) for p in forbidden]
    hits = [(p, n) for p, n in hits if n]
    for p, n in hits:
        findings.append(f"FORBIDDEN phrase x{n}: \"{p}\"")
    if hits:
        tell_penalty += 0.5
    crutches = crutch_phrases(body, topic_terms)
    bad_crutches = [(p, n) for p, n in crutches if n >= 4]
    for p, n in crutches:
        findings.append(f"Repetition: \"{p}\" x{n}" + ("  <-- crutch, rewrite" if n >= 4 else ""))
    # Only stylistic repetition is penalized; topical nouns repeating is normal
    # (the findings still list them for the editor's judgment).
    stylistic = [
        (p, n) for p, n in bad_crutches
        if " " in p or p in CRUTCH_LEXICON or p.endswith("ly")
    ]
    tell_penalty += min(0.3, 0.1 * len(stylistic))
    bluf_fails = []
    for sec in re.split(r"^##\s+", raw, flags=re.MULTILINE)[1:]:
        first_para = next((p for p in sec.splitlines()[1:] if p.strip() and not p.startswith(("#", "|", "[", "!"))), "")
        opener = first_para.strip().lower()
        if any(re.match(rx, opener) for rx in BLUF_BAD_OPENERS):
            bluf_fails.append(sec.splitlines()[0][:50])
    for s in bluf_fails:
        findings.append(f"BLUF fail (throat-clearing opener): {s}")
    tell_penalty += min(0.2, 0.05 * len(bluf_fails))
    paras = split_paragraphs(body)
    lens = [len(words(p)) for p in paras if words(p)]
    if len(lens) >= 8:
        cv = statistics.pstdev(lens) / max(statistics.mean(lens), 1)
        findings.append(f"Paragraph rhythm: mean {statistics.mean(lens):.0f}w, CV {cv:.2f}" + ("  <-- uniform, vary rhythm" if cv < 0.35 else ""))
        if cv < 0.35:
            tell_penalty += 0.1
    scores["ai_tells"] = (max(0.0, 1 - tell_penalty) * 25, 25)

    # --- Structure (15) ---
    has_intro = bool(paras) and bool(h2s)
    h2_ok = len(h2s) >= 4
    structure = (0.5 if has_intro else 0) + (0.5 if h2_ok else 0)
    if not h2_ok:
        findings.append(f"Only {len(h2s)} H2 sections — structure too flat.")
    scores["structure"] = (structure * 15, 15)

    earned = sum(e for e, _ in scores.values())
    total = sum(w for _, w in scores.values())
    score = round(earned / total * 100)
    criticals = [f for f in findings if f.startswith(("CRITICAL", "MISSING", "FORBIDDEN"))]
    dim_floor_fail = [d for d, (e, w) in scores.items() if e / w < 0.6]
    verdict = "PASS" if score >= 85 and not criticals and not dim_floor_fail else (
        "BORDERLINE" if score >= 70 else "FAIL")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{args.slug}-metrics.md"
    lines = [
        f"# Mechanical quality metrics — {args.slug} ({args.stage} stage)",
        "",
        f"**Mechanical score: {score}/100 — {verdict}**",
        "(Final verdict = this + adversarial read + voice judgment, per SKILL.md.)",
        "",
        "| Dimension | Score | Weight | Floor (60%) |",
        "|---|---|---|---|",
    ]
    for dim, (e, w) in scores.items():
        flag = "FAIL" if e / w < 0.6 else "ok"
        lines.append(f"| {dim} | {e:.1f} | {w} | {flag} |")
    lines += ["", "## Findings", ""] + [f"- {f}" for f in findings]
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
