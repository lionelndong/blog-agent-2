"""Layer 3 AIO cannibalization vetting.

Heuristic-driven for autonomous mode (Brand Radar AI is gated; no per-keyword AIO fetcher).
- AIO presence: from existing serp_features column ("ai_overview" present)
- Score: rubric-driven keyword-shape heuristic
- Verdict: per SKILL rules (intent + score interaction)
"""
import csv
from pathlib import Path

ROOT = Path(r"C:\Users\ndong\Downloads\blog-agent-2\content-pipeline\0-keywords")
IDEAS = ROOT / "keyword-ideas.csv"

DEFINITIONAL_TOKENS = ["what is", "what does", "what are", "definition", "meaning"]
HOWTO_TOKENS = ["how to", "how do", "steps to"]
COMMERCIAL_INV_TOKENS = ["best ", "vs ", "review", "alternative", "top "]


def detect_aio(serp_features: str) -> bool:
    sf = (serp_features or "").lower()
    return "ai_overview" in sf


def score_aio_completeness(kw: str, intent: str) -> tuple[int, str, str]:
    """Returns (score 0-10, click_intent, reasoning).

    Heuristic per rubric: definitional/how-to → high cannibalization;
    commercial-investigation → low; tool-led → exempt.
    """
    kl = kw.lower()
    # Tool-led: exempt — score is irrelevant
    if intent == "tool-led":
        return 0, "yes-deep", "Tool-led intent — users need to use a generator, not read text. AIO can't substitute."

    # Definitional "what is X" — most cannibalized class
    if any(t in kl for t in DEFINITIONAL_TOKENS):
        return 9, "no", "Definitional query — AIOs typically deliver definition + 2 examples + implication, satisfying the searcher with no click incentive."

    # How-to procedural: AIOs answer steps directly
    if any(t in kl for t in HOWTO_TOKENS):
        return 8, "yes-shallow", "How-to query — AIOs typically lay out steps; only deep dive material (specifics, walkthroughs) earns a click."

    # Commercial investigation: AIO underperforms (users want options)
    if any(t in kl for t in COMMERCIAL_INV_TOKENS) or intent == "commercial-investigation":
        return 4, "yes-deep", "Comparison/listicle intent — readers want options + opinion the AIO can't summarize. AIO underperforms here."

    # Generic informational niche: usually moderate AIO
    return 5, "yes-deep", "Niche/informational query — AIO gives a partial answer; readers click for depth, examples, or platform-specific guidance."


def verdict(score: int, intent: str, source: str, has_aio: bool) -> tuple[str, str]:
    """Apply rubric+SKILL exemptions."""
    if not has_aio:
        return "PASS", "no_aio_present"
    # Tool-led exemption
    if intent == "tool-led":
        return "PASS", "tool_led_immune"
    # AIO-gap source exemption (we don't have any of these in this run)
    if source == "aio_gap":
        return "PASS", "aio_gap_target"
    # Commercial-investigation: PASS regardless of score (per SKILL line 81)
    if intent == "commercial-investigation":
        return "PASS", "commercial_investigation_immune"
    # Score-based for informational
    if score >= 8 and intent == "informational":
        return "FAIL_CANNIBALIZED", "high_aio_completeness_informational"
    if score >= 5:
        return "RISKY", "moderate_aio_completeness"
    return "PASS", "weak_aio"


# ---- Run ----
with IDEAS.open("r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

# Process only BID-PASS
pass_count = 0
exempt_count = 0
no_aio_count = 0
risky_count = 0
fail_count = 0
score_buckets = {"0-4": 0, "5-7": 0, "8-10": 0}

for r in rows:
    if r["bid_verdict"] != "PASS":
        # Layer 3 doesn't run on FAILs
        r["has_aio"] = ""
        r["aio_completeness_score"] = ""
        r["aio_click_intent"] = ""
        r["aio_verdict"] = "SKIPPED_BID_FAIL"
        r["aio_reasoning"] = ""
        continue

    has_aio = detect_aio(r.get("serp_features", ""))
    if not has_aio:
        r["has_aio"] = "false"
        r["aio_completeness_score"] = ""
        r["aio_click_intent"] = ""
        r["aio_verdict"] = "PASS"
        r["aio_reasoning"] = "No AIO present in SERP features."
        no_aio_count += 1
        pass_count += 1
        continue

    score, click_intent, reasoning = score_aio_completeness(r["keyword"], r["serp_intent"])
    v, v_reason = verdict(score, r["serp_intent"], r["source"], has_aio)

    r["has_aio"] = "true"
    r["aio_completeness_score"] = str(score)
    r["aio_click_intent"] = click_intent
    r["aio_verdict"] = v
    r["aio_reasoning"] = f"{reasoning} [{v_reason}]"

    if score <= 4:
        score_buckets["0-4"] += 1
    elif score <= 7:
        score_buckets["5-7"] += 1
    else:
        score_buckets["8-10"] += 1

    if v == "PASS":
        if v_reason in ("tool_led_immune", "commercial_investigation_immune", "aio_gap_target"):
            exempt_count += 1
        else:
            pass_count += 1
    elif v == "RISKY":
        risky_count += 1
    elif v == "FAIL_CANNIBALIZED":
        fail_count += 1


# Write back
fieldnames = list(rows[0].keys())
with IDEAS.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)

bid_pass = sum(1 for r in rows if r["bid_verdict"] == "PASS")
print(f"AIO check on {bid_pass} BID-PASS candidates:")
print(f"  No AIO present:                       {no_aio_count}")
print(f"  AIO present, exempt:                  {exempt_count}")
print(f"  Score buckets: 0-4={score_buckets['0-4']}, 5-7={score_buckets['5-7']}, 8-10={score_buckets['8-10']}")
print(f"  PASS (incl. exempt):                  {pass_count + exempt_count}")
print(f"  RISKY:                                {risky_count}")
print(f"  FAIL_CANNIBALIZED:                    {fail_count}")

# Top cannibalized rejections
fails = [r for r in rows if r["aio_verdict"] == "FAIL_CANNIBALIZED"]
fails.sort(key=lambda r: -int(r["traffic_potential"]))
print("\nTop 3 cannibalized rejections:")
for r in fails[:3]:
    print(f"  {r['keyword']:<45} score={r['aio_completeness_score']} TP={int(r['traffic_potential'])} reason={r['aio_reasoning'][:80]}")

# Top risky survivors
risky = [r for r in rows if r["aio_verdict"] == "RISKY"]
risky.sort(key=lambda r: -int(r["traffic_potential"]))
print("\nTop 3 risky survivors:")
for r in risky[:3]:
    print(f"  {r['keyword']:<45} score={r['aio_completeness_score']} TP={int(r['traffic_potential'])} reason={r['aio_reasoning'][:80]}")

with (ROOT / "cache" / "aio-calibration.log").open("a", encoding="utf-8") as f:
    f.write(f"2026-05-04 AIO run: {bid_pass} bid-pass scored, "
            f"distribution 0-4={score_buckets['0-4']} 5-7={score_buckets['5-7']} 8-10={score_buckets['8-10']}, "
            f"verdicts PASS={pass_count+exempt_count} RISKY={risky_count} FAIL={fail_count}\n")
