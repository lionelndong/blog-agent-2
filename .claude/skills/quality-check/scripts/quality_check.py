#!/usr/bin/env python3
"""Completeness FLOORS for a draft — binary and un-gameable (2026-06-25 Ryan-faithful rebuild).

Replaces the old 0-100 mechanical score. A numeric score invites gaming: a model can
sprinkle numbers, add links, and split H2 headers to clear "85" without making the article
any better — exactly the failure behind drafts that scored 85 PASS while the adversarial
read named five real weaknesses. Ryan Law's method uses human editorial judgment, not a
rubric. We approximate that judgment with two un-gameable halves:

  * FLOORS (this script): objective completeness prerequisites that can ONLY be met by
    actually doing the work — hitting the SERP-benchmarked depth, covering every consensus
    topic the winners cover, citing every claim, and leaking no internal tooling into the
    prose. Each is a hard pass/fail. There is no score to optimize toward.

  * PANEL (the SKILL): a panel of skeptical reviewers answers the only question that
    matters — "reader sees this and the live #1 side by side, which do they keep?" That
    judgment, not a number, is what decides publish.

This script emits FLOORS_OK or FLOORS_FAIL plus non-gating OBSERVATIONS (claim density,
link count, paragraph rhythm, crutch words) for the panel and editor to weigh. Nothing here
can be satisfied by padding.

Usage:
    python .claude/skills/quality-check/scripts/quality_check.py <slug> [--stage cited]

Exit codes:
    0   all floors pass (FLOORS_OK)
    1   one or more floors failed (FLOORS_FAIL)
    2   no draft found
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

# A draft below this fraction of the SERP-median word count is thin and cannot auto-publish.
# (The #1 historical failure mode was 1,100-word drafts against 2,500-word SERP winners.)
DEPTH_FLOOR = 0.80

# Internal tooling / research jargon that must NEVER appear in reader-facing prose.
# Catches leaks like a raw "Semrush 40,500-volume aside" sitting in a published draft.
INTERNAL_LEAK_TERMS = [
    "semrush", "dataforseo", "data for seo", "ahrefs", "contentshake", "content shake",
    "strapi", "doppler", "posthog", "openrouter", "open router", "replicate", "firecrawl",
    "paperclip", "supabase", "trafficstars", "beat spec", "beat-spec", "must-cover topic",
]

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
    text = re.sub(r"\[GAIN\]", "", text)
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
    """Distinctive words/bigrams repeated enough to read as a tic (OBSERVATION only)."""
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
                    help="cited = post-verify-claims (naked [link] is a hard floor there)")
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
    body_lower = body.lower()
    draft_lower = " ".join(words(raw))
    title = (re.search(r"^#\s+(.+)$", raw, re.MULTILINE) or [None, args.slug])[1]
    h2s = re.findall(r"^##\s+(.+)$", raw, re.MULTILINE)
    h3s = re.findall(r"^###\s+(.+)$", raw, re.MULTILINE)
    headers = " ".join(h2s + h3s)
    brand = (re.search(r"\*\*Name:\*\*\s*(.+)", read(BRAND_CONFIG)) or [None, ""])[1]
    topic_terms = {w for w in words(f"{title} {args.slug} {headers} {brand}") if w not in STOPWORDS}

    # floors: list of (name, passed, detail). observations: list of str.
    floors: list[tuple[str, bool, str]] = []
    observations: list[str] = []

    # --- FLOOR: a SERP benchmark must exist (no benchmark -> cannot verify competitiveness) ---
    if not spec:
        floors.append((
            "beat_spec", False,
            "No BEAT SPEC in the dossier — cannot verify the draft beats the SERP. Re-run /research.",
        ))

    # --- FLOOR: depth vs the SERP median ---
    if spec.get("target_words"):
        ratio = body_words / spec["target_words"]
        floors.append((
            "depth", ratio >= DEPTH_FLOOR,
            f"{body_words} words vs SERP median {spec['target_words']} "
            f"(ratio {ratio:.2f}; floor {DEPTH_FLOOR:.2f})"
            + ("" if ratio >= DEPTH_FLOOR else " — THIN against the SERP"),
        ))
    elif spec:
        floors.append((
            "depth", body_words >= 1500,
            f"{body_words} words; beat spec has no parseable target word count",
        ))

    # --- FLOOR: item count (listicles must carry the items the SERP demands) ---
    if spec.get("item_count"):
        sections = len(h2s) + len(h3s)
        floors.append((
            "item_count", sections >= spec["item_count"],
            f"{sections} H2+H3 sections vs beat-spec {spec['item_count']} items",
        ))

    # --- FLOOR: comparison table when the SERP has one ---
    if spec.get("table_required"):
        has_table = bool(re.search(r"^\|.+\|\s*$", raw, re.MULTILINE))
        floors.append((
            "table", has_table,
            "comparison table present" if has_table
            else "beat spec requires a comparison table; none found in the draft",
        ))

    # --- FLOOR: consensus coverage (EVERY must-cover topic, not a ratio) ---
    must = spec.get("must_cover", [])
    if must:
        missing = [t for t in must if not topic_covered(t, draft_lower)]
        floors.append((
            "consensus_coverage", not missing,
            "all must-cover topics present" if not missing else f"MISSING: {', '.join(missing)}",
        ))

    # --- FLOOR: citations resolved (cited stage only) ---
    naked_links = len(re.findall(r"\[link\]", raw))
    real_links = len(re.findall(r"\[[^\]]+\]\(https?://", raw))
    if args.stage == "cited":
        floors.append((
            "citations", naked_links == 0,
            "no naked [link] placeholders" if naked_links == 0
            else f"{naked_links} naked [link] placeholders remain post-citation",
        ))

    # --- FLOOR: no internal tooling leaked into reader-facing prose ---
    leaks = []
    for term in INTERNAL_LEAK_TERMS:
        n = len(re.findall(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", body_lower))
        if n:
            leaks.append(f'"{term}"x{n}')
    floors.append((
        "no_internal_leak", not leaks,
        "no internal tooling in prose" if not leaks else f"LEAK in prose: {', '.join(leaks)}",
    ))

    # --- FLOOR: no brand-forbidden phrases ---
    forbidden = load_forbidden_phrases()
    fhits = [(p, len(re.findall(re.escape(p), raw, re.IGNORECASE))) for p in forbidden]
    fhits = [(p, n) for p, n in fhits if n]
    floors.append((
        "forbidden_phrases", not fhits,
        "no forbidden phrases" if not fhits else "; ".join(f'"{p}"x{n}' for p, n in fhits),
    ))

    # --- OBSERVATIONS (non-gating — the panel and editor weigh these, the gate does not) ---
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", body) if s.strip()]
    numeric = [s for s in sentences if re.search(r"\d", s)]
    claim_density = len(numeric) / max(len(sentences), 1)
    observations.append(
        f"Claim density {claim_density:.2f} ({len(numeric)}/{len(sentences)} numeric sentences); "
        f"{real_links} real hyperlinks; {naked_links} naked [link]."
    )
    observations.append(f"Structure: {len(h2s)} H2 + {len(h3s)} H3 sections.")
    observations.append("Information gain: [GAIN] marker " + ("present." if "[GAIN]" in raw else "ABSENT — the panel must confirm a genuine information gain."))
    crutches = crutch_phrases(body, topic_terms)
    for p, n in crutches:
        observations.append(f'Repetition: "{p}" x{n}' + ("  <-- reads as a crutch" if n >= 4 else ""))
    bluf_fails = []
    for sec in re.split(r"^##\s+", raw, flags=re.MULTILINE)[1:]:
        first_para = next((p for p in sec.splitlines()[1:] if p.strip() and not p.startswith(("#", "|", "[", "!"))), "")
        if any(re.match(rx, first_para.strip().lower()) for rx in BLUF_BAD_OPENERS):
            bluf_fails.append(sec.splitlines()[0][:50])
    for s in bluf_fails:
        observations.append(f"BLUF fail (throat-clearing opener): {s}")
    paras = split_paragraphs(body)
    lens = [len(words(p)) for p in paras if words(p)]
    if len(lens) >= 8:
        cv = statistics.pstdev(lens) / max(statistics.mean(lens), 1)
        observations.append(
            f"Paragraph rhythm: mean {statistics.mean(lens):.0f}w, CV {cv:.2f}"
            + ("  <-- uniform; vary rhythm" if cv < 0.35 else "")
        )

    floors_ok = all(passed for _, passed, _ in floors)
    result = "FLOORS_OK" if floors_ok else "FLOORS_FAIL"
    failed = [name for name, passed, _ in floors if not passed]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{args.slug}-metrics.md"
    lines = [
        f"# Completeness floors — {args.slug} ({args.stage} stage)",
        "",
        f"**{result}**" + ("" if floors_ok else f" — failed: {', '.join(failed)}"),
        "",
        "Floors are hard prerequisites (you can only satisfy them by doing the work). They do",
        "NOT decide publish on their own — the /quality-check panel decides whether the article",
        "beats the live #1. A draft that clears every floor can still FAIL the panel.",
        "",
        "| Floor | Result | Detail |",
        "|---|---|---|",
    ]
    for name, passed, detail in floors:
        lines.append(f"| {name} | {'PASS' if passed else 'FAIL'} | {detail} |")
    lines += ["", "## Observations (non-gating — for the panel / editor)", ""]
    lines += [f"- {o}" for o in observations]
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0 if floors_ok else 1


if __name__ == "__main__":
    sys.exit(main())
