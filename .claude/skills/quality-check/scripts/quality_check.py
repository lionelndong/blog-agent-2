#!/usr/bin/env python3
"""Automated quality metrics for a draft.

Computes:
  - Forbidden phrase scan (against brand-config.md list)
  - Voice metrics vs examples/ baseline (sentence length, paragraph length, second-person, em-dash)
  - BLUF heuristic per section (does the opener carry information?)
  - Claim density (sentences with numbers/percentages/comparisons)

Usage:
    python .claude/skills/quality-check/scripts/quality_check.py <slug>
"""
from __future__ import annotations

import argparse
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DRAFT_DIR = ROOT / "content-pipeline" / "5-drafts"
BRAND_CONFIG = ROOT / "brand-config.md"
EXAMPLES_DIR = ROOT / "examples"
OUT_DIR = ROOT / "content-pipeline" / "quality-checks"

# Heuristic openers that fail the BLUF test — sentence starters that throat-clear instead of carry.
BLUF_BAD_OPENERS = [
    r"^in this section",
    r"^now that we",
    r"^now let",
    r"^before we",
    r"^let'?s look",
    r"^let'?s explore",
    r"^let'?s dive",
    r"^let'?s talk",
    r"^let me",
    r"^to begin",
    r"^first of all",
    r"^firstly",
    r"^moreover",
    r"^furthermore",
    r"^additionally",
    r"^as we mentioned",
    r"^as discussed",
    r"^when it comes to",
    r"^it'?s important to (note|understand|remember)",
    r"^one of the (most |key )?(things|aspects|factors)",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_forbidden_phrases() -> list[str]:
    text = read(BRAND_CONFIG)
    if not text:
        return []
    m = re.search(r"## Forbidden phrases.*?(?=^##\s|\Z)", text, re.MULTILINE | re.DOTALL)
    if not m:
        return []
    block = m.group(0)
    phrases = []
    for line in block.split("\n"):
        m2 = re.match(r'\s*-\s*"([^"]+)"', line)
        if m2:
            phrases.append(m2.group(1))
    return phrases


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def split_paragraphs(text: str) -> list[str]:
    paragraphs = []
    for chunk in re.split(r"\n\s*\n", text):
        chunk = chunk.strip()
        if not chunk:
            continue
        if chunk.startswith("#") or chunk.startswith("|") or chunk.startswith("```") or chunk.startswith(":::"):
            continue
        if chunk.startswith("- ") or chunk.startswith("* ") or chunk.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
            continue
        paragraphs.append(chunk)
    return paragraphs


def words(text: str) -> list[str]:
    return re.findall(r"\b[\w']+\b", text)


def voice_metrics(text: str) -> dict:
    sentences = split_sentences(text)
    paragraphs = split_paragraphs(text)
    if not sentences:
        return {}

    sentence_word_counts = [len(words(s)) for s in sentences]
    paragraph_word_counts = [len(words(p)) for p in paragraphs] if paragraphs else [0]

    total_words = sum(sentence_word_counts) or 1
    second_person_hits = len(re.findall(r"\b(you|your|yours|you'?re|you'?ve|you'?ll|you'?d)\b", text, re.IGNORECASE))
    em_dash_count = text.count("—")

    return {
        "sentences": len(sentences),
        "paragraphs": len(paragraphs),
        "avg_sentence_words": round(statistics.mean(sentence_word_counts), 1),
        "median_sentence_words": round(statistics.median(sentence_word_counts), 1),
        "stdev_sentence_words": round(statistics.pstdev(sentence_word_counts), 1) if len(sentence_word_counts) > 1 else 0,
        "avg_paragraph_words": round(statistics.mean(paragraph_word_counts), 1),
        "median_paragraph_words": round(statistics.median(paragraph_word_counts), 1),
        "second_person_per_1k": round(second_person_hits * 1000 / total_words, 1),
        "em_dash_per_1k": round(em_dash_count * 1000 / total_words, 1),
        "total_words": total_words,
    }


def baseline_metrics() -> dict:
    examples = list(EXAMPLES_DIR.glob("ahrefs-*.md"))
    if not examples:
        return {}
    combined = "\n\n".join(read(p) for p in examples)
    return voice_metrics(combined)


def metric_in_range(value: float, baseline: float, tolerance: float = 0.5) -> bool:
    if baseline == 0:
        return True
    lo = baseline * (1 - tolerance)
    hi = baseline * (1 + tolerance)
    return lo <= value <= hi


def forbidden_scan(text: str, forbidden: list[str]) -> list[tuple[str, int]]:
    text_lower = text.lower()
    hits = []
    for phrase in forbidden:
        count = text_lower.count(phrase.lower())
        if count > 0:
            hits.append((phrase, count))
    return hits


def section_openers(text: str) -> list[tuple[str, str]]:
    """Return [(section_heading, first_real_sentence), ...]."""
    sections = re.split(r"^(##+\s+.+)$", text, flags=re.MULTILINE)
    out = []
    for i in range(1, len(sections), 2):
        heading = sections[i].strip()
        body = sections[i + 1] if i + 1 < len(sections) else ""
        for para in body.split("\n\n"):
            p = para.strip()
            if not p or p.startswith("#") or p.startswith("|") or p.startswith("```") or p.startswith(":::"):
                continue
            if p.startswith("- ") or p.startswith("* "):
                continue
            sentences = split_sentences(p)
            if sentences:
                out.append((heading, sentences[0]))
                break
    return out


def bluf_fail(opener: str) -> bool:
    o = opener.strip().lower()
    return any(re.search(pat, o) for pat in BLUF_BAD_OPENERS)


# Must-cite: assertions that genuinely need a source under "cite everything".
# Numbers, percentages, named studies, year-anchored facts, "according to X".
MUST_CITE_PATTERNS: list[tuple[str, re.RegexFlag | int]] = [
    # Percentages, multiples (3x), explicit decimals
    (r"\b\d+(\.\d+)?\s*(%|percent|x\b)", 0),
    # 4+ digit numbers or comma-grouped (1,000)
    (r"\b(\d{1,3}(,\d{3})+|\d{4,})\b", 0),
    # Bounded comparators with numbers ("more than 50", "up to 1000")
    (r"\b(more than|less than|over|under|up to|at least|at most|fewer than|as many as|nearly|roughly|approximately|about|around)\s+\d", re.IGNORECASE),
    # Number-as-words ("hundreds of thousands of X", "millions of users", "six figures")
    (r"\b(hundreds|thousands|millions|billions|tens of (thousands|millions|billions))\s+of\s+\w+", re.IGNORECASE),
    (r"\b(six|seven|eight|nine|ten)\s+figures?\b", re.IGNORECASE),
    # Year references — factual time-anchoring claims
    (r"\b(in|since|by|after|before)\s+(19|20)\d{2}\b", re.IGNORECASE),
    # Named studies / research / reports
    (r"\b(study|studies|research|report|survey|paper|data|analysis) (shows?|finds?|found|says?|said|reveals?|revealed|suggests?|estimates?)\b", re.IGNORECASE),
    (r"\baccording to\b", re.IGNORECASE),
]

# Voice-flagged: rhetorical patterns that may or may not need a link — editor decides per case.
# These are the kinds of sentences over-citing damages: opinionated population claims, superlatives,
# brand-comparison voice. Tracked for visibility, NOT used to gate the verify-claims pass.
VOICE_FLAGGED_PATTERNS: list[tuple[str, re.RegexFlag | int]] = [
    # Quantifier-adjective claims about a population ("most platforms", "almost every user")
    (r"\b(most|many|few|almost (every|all|no)|the majority of|the minority of|nearly all|nearly every)\s+\w+", re.IGNORECASE),
    # Absolute statements ("every platform", "no platform", "all users")
    (r"\b(every|all|no|none of the|each of the)\s+\w+\s+(is|are|was|were|has|have|does|do|gets?|requires?|needs?|claims?|delivers?|fails?|wins?|hedges?|breaks?)\b", re.IGNORECASE),
    # Comparative superlatives ("the best X", "the only X", "the largest X")
    (r"\bthe (best|worst|only|first|last|largest|smallest|biggest|fastest|slowest|leading|dominant)\s+\w+", re.IGNORECASE),
]

# Capitalised product/brand names without an inline link → comparator voice; falls under voice-flagged.
COMPETITOR_LIKE_PATTERN = re.compile(
    r"\b("
    r"ChatGPT|Claude|GPT-?\d?|Replika|Character\.?AI|Candy\.?AI|Ourdream\.?AI|"
    r"Crushon\.?AI|Magi1\.?AI|Pleasur\.?AI|Anthropic|OpenAI|Google|Meta|Microsoft"
    r")\b"
)

LINK_PATTERN = re.compile(r"\[[^\]]+\]\([^)]+\)")


def _is_linked(s: str) -> bool:
    return bool(LINK_PATTERN.search(s)) or "[link]" in s


def _matches_any(s: str, patterns: list[tuple[str, re.RegexFlag | int]]) -> bool:
    return any(re.search(p, s, f) for p, f in patterns)


def claim_density(text: str) -> dict:
    """Two-tier classification: must-cite (gated) vs voice-flagged (visibility only)."""
    must_cite: list[str] = []
    voice_flagged: list[str] = []
    seen: set[str] = set()
    for s in split_sentences(text):
        if not s or s.startswith(("#", "|", "- ", "* ", "```", ":::")):
            continue
        if s in seen:
            continue
        if _matches_any(s, MUST_CITE_PATTERNS):
            must_cite.append(s)
            seen.add(s)
            continue
        if _matches_any(s, VOICE_FLAGGED_PATTERNS):
            voice_flagged.append(s)
            seen.add(s)
            continue
        if COMPETITOR_LIKE_PATTERN.search(s) and not LINK_PATTERN.search(s):
            voice_flagged.append(s)
            seen.add(s)

    must_linked = sum(1 for s in must_cite if _is_linked(s))
    voice_linked = sum(1 for s in voice_flagged if _is_linked(s))
    must_pct = round(100 * must_linked / len(must_cite), 1) if must_cite else 100.0
    voice_pct = round(100 * voice_linked / len(voice_flagged), 1) if voice_flagged else 100.0

    total = len(must_cite) + len(voice_flagged)
    total_linked = must_linked + voice_linked
    aggregate_pct = round(100 * total_linked / total, 1) if total else 100.0

    return {
        "must_cite_claims": len(must_cite),
        "must_linked_claims": must_linked,
        "must_linkable_pct": must_pct,
        "must_cite_examples": must_cite[:5],
        "voice_flagged_claims": len(voice_flagged),
        "voice_linked_claims": voice_linked,
        "voice_linkable_pct": voice_pct,
        "voice_flagged_examples": voice_flagged[:5],
        # Backwards-compatible aggregate fields (legacy callers — score no longer uses these)
        "factual_claims": total,
        "linked_claims": total_linked,
        "linkable_pct": aggregate_pct,
        "examples": (must_cite + voice_flagged)[:5],
    }


def compute_score(forbidden_hits, voice_compare, bluf_pct, claim_data, total_words) -> tuple[int, list[str]]:
    notes = []
    score = 0

    # Forbidden phrases (20 pts)
    if not forbidden_hits:
        score += 20
    else:
        score += max(0, 20 - len(forbidden_hits) * 5)
        notes.append(f"-{min(len(forbidden_hits) * 5, 20)} pts: {len(forbidden_hits)} forbidden phrase(s) found")

    # Voice metrics within baseline (25 pts)
    in_range = sum(1 for ok in voice_compare.values() if ok)
    total_dims = len(voice_compare) or 1
    voice_score = round(25 * in_range / total_dims)
    score += voice_score
    if voice_score < 25:
        notes.append(f"-{25 - voice_score} pts: voice metrics out of baseline range on {total_dims - in_range} dimension(s)")

    # BLUF (20 pts)
    bluf_score = round(20 * (bluf_pct / 100))
    score += bluf_score
    if bluf_score < 16:
        notes.append(f"-{20 - bluf_score} pts: only {bluf_pct}% of section openers pass BLUF heuristic")

    # Citation density (15 pts) — gated on MUST-CITE only (numbers, studies, year-anchored facts).
    # Voice-flagged sentences (rhetorical "most platforms" etc.) are tracked for visibility but
    # do NOT affect the score — over-citing rhetorical voice damages Ryan's conversational tone.
    must_cite = claim_data["must_cite_claims"]
    if must_cite == 0:
        if total_words > 800:
            # Long article with zero must-cite claims is unusual but not a score penalty —
            # it likely means the piece is opinion/voice-led rather than data-led.
            notes.append("note: 0 must-cite claims in a long article — voice/opinion-led piece, score not penalized")
        score += 15
    else:
        link_pct = claim_data["must_linkable_pct"]
        link_score = round(15 * (link_pct / 100))
        score += link_score
        if link_score < 12:
            notes.append(f"-{15 - link_score} pts: only {link_pct}% of MUST-CITE claims linked ({claim_data['must_linked_claims']}/{must_cite})")

    # Reserve 20 pts for adversarial verdict (filled by SKILL.md after sub-agent runs)
    # Score will be partial here; final score combined in skill report
    return score, notes


def render_report(slug: str, metrics: dict, baseline: dict, forbidden_hits, voice_compare, openers, claim_data, partial_score, notes):
    lines = [f"# Automated quality metrics — {slug}\n"]

    lines.append(f"**Partial score (auto-only):** {partial_score} / 80")
    lines.append("(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)\n")

    if notes:
        lines.append("## Score breakdown")
        for n in notes:
            lines.append(f"- {n}")
        lines.append("")

    lines.append("## Forbidden phrases")
    if forbidden_hits:
        for phrase, count in forbidden_hits:
            lines.append(f"- `\"{phrase}\"` — {count} occurrence(s)")
    else:
        lines.append("None found.")
    lines.append("")

    lines.append("## Voice metrics vs baseline (examples/)")
    lines.append("")
    lines.append("| Metric | Draft | Baseline | In range |")
    lines.append("|---|---|---|---|")
    for key, draft_val in metrics.items():
        if key in {"sentences", "paragraphs", "total_words"}:
            continue
        base_val = baseline.get(key, 0)
        ok = voice_compare.get(key, True)
        mark = "[x]" if ok else "[ ]"
        lines.append(f"| {key} | {draft_val} | {base_val} | {mark} |")
    lines.append("")
    lines.append(f"Draft total words: {metrics.get('total_words', 0)}")
    lines.append(f"Baseline corpus: {len(list(EXAMPLES_DIR.glob('ahrefs-*.md')))} files")
    lines.append("")

    lines.append("## BLUF heuristic (section openers)")
    bluf_pass = [(h, o) for h, o in openers if not bluf_fail(o)]
    bluf_fail_list = [(h, o) for h, o in openers if bluf_fail(o)]
    pct = round(100 * len(bluf_pass) / len(openers), 1) if openers else 100.0
    lines.append(f"- Sections checked: {len(openers)}")
    lines.append(f"- Pass: {len(bluf_pass)} ({pct}%)")
    lines.append(f"- Fail: {len(bluf_fail_list)}")
    if bluf_fail_list:
        lines.append("")
        lines.append("**Failures:**")
        for h, o in bluf_fail_list:
            short = (o[:120] + "...") if len(o) > 120 else o
            lines.append(f"- `{h}` opens with: \"{short}\"")
    lines.append("")

    lines.append("## Claim density")
    lines.append("")
    lines.append("**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:")
    lines.append(f"- Count: {claim_data['must_cite_claims']}")
    lines.append(f"- Linked: {claim_data['must_linked_claims']} ({claim_data['must_linkable_pct']}%)")
    if claim_data["must_cite_examples"]:
        lines.append("")
        lines.append("Sample must-cite claims:")
        for s in claim_data["must_cite_examples"]:
            short = (s[:200] + "...") if len(s) > 200 else s
            lines.append(f"- {short}")
    lines.append("")
    lines.append("**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:")
    lines.append(f"- Count: {claim_data['voice_flagged_claims']}")
    lines.append(f"- Linked: {claim_data['voice_linked_claims']} ({claim_data['voice_linkable_pct']}%)")
    if claim_data["voice_flagged_examples"]:
        lines.append("")
        lines.append("Sample voice-flagged statements (editor decides — over-citing damages voice):")
        for s in claim_data["voice_flagged_examples"]:
            short = (s[:200] + "...") if len(s) > 200 else s
            lines.append(f"- {short}")
    lines.append("")

    lines.append("## Notes for the adversarial reader (next step)")
    lines.append("Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    parser.add_argument("--path", default=None, help="Override path to read draft from (defaults to content-pipeline/5-drafts/<slug>.md)")
    args = parser.parse_args()

    draft_path = Path(args.path) if args.path else (DRAFT_DIR / f"{args.slug}.md")
    if not draft_path.exists():
        sys.exit(f"error: draft not found at {draft_path}")
    draft = read(draft_path)
    # Strip "## Editor notes" tail (cited drafts have these) — they shouldn't count toward voice metrics
    draft = re.split(r"^---\s*\n+##\s+Editor notes", draft, maxsplit=1, flags=re.MULTILINE)[0].rstrip() + "\n"

    forbidden = load_forbidden_phrases()
    forbidden_hits = forbidden_scan(draft, forbidden)

    metrics = voice_metrics(draft)
    base = baseline_metrics()

    voice_compare = {}
    for key in ("avg_sentence_words", "median_sentence_words", "avg_paragraph_words", "median_paragraph_words", "second_person_per_1k", "em_dash_per_1k"):
        voice_compare[key] = metric_in_range(metrics.get(key, 0), base.get(key, 0))

    openers = section_openers(draft)
    bluf_pct = round(100 * sum(1 for h, o in openers if not bluf_fail(o)) / len(openers), 1) if openers else 100.0
    claims = claim_density(draft)

    partial_score, notes = compute_score(forbidden_hits, voice_compare, bluf_pct, claims, metrics.get("total_words", 0))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{args.slug}-metrics.md"
    out_path.write_text(render_report(args.slug, metrics, base, forbidden_hits, voice_compare, openers, claims, partial_score, notes), encoding="utf-8")
    print(str(out_path))
    print(f"partial_score: {partial_score}/80")


if __name__ == "__main__":
    main()
