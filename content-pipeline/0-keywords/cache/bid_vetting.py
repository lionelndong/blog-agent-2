"""Layer 2 BID vetting for keyword-ideas.csv.

Heuristic-driven for autonomous mode (no per-keyword SERP overview fetches).
Uses available Layer 1 columns: volume, kd, traffic_potential, intent, source,
serp_features. SERP intent inferred from keyword shape + Ahrefs serp_features.
"""
import csv
import re
from pathlib import Path

ROOT = Path(r"C:\Users\ndong\Downloads\blog-agent-2\content-pipeline\0-keywords")
IDEAS = ROOT / "keyword-ideas.csv"
BRAND_DR = 21
DR_GAP_LIMIT = BRAND_DR + 30  # KD-as-proxy ceiling: 51 (calibrated for autonomous mode w/o per-kw DR pulls)

# ---- Brand fit heuristics (Pleasur.AI: AI adult companion app) ----
# Pain points from brand-config: mainstream chatbots restricted, repetitive companions,
# voice/video low-quality, privacy, free-tier limits, fragmented UX, hard to find quality characters.
HIGH_FIT_TERMS = [
    # core pain-point matches
    "ai girlfriend", "ai boyfriend", "ai companion", "ai roleplay", "ai sext", "sexting",
    "sex chat", "ai chat", "nsfw chat", "nsfw ai", "ai porn", "uncensored ai",
    "virtual girlfriend", "ai gf", "ai bf", "ai chatbot", "no filter", "uncensored",
    "ai dirty", "dirty talk", "horny ai", "ai romantic", "romantic ai",
    "ai character", "character ai", "sexting bot", "ai sexchat", "ai sext chat",
    "no sign up", "free ai girlfriend", "best ai girlfriend", "best ai boyfriend",
    "ai girl chat", "girl ai chat", "ai chat girl", "ai chat boyfriend",
    "create ai", "create your own", "ai girlfriend creator", "ai girlfriend generator",
    "spicy ai", "naughty ai", "nasty ai", "dream ai", "ai girls", "ai girl",
    "horny", "nude ai", "naked ai", "ai chat sex",
    "ai sexting", "sext ai", "sex bot", "ai sex bot", "ai sex roleplay",
    "ai girlfriend simulator", "girlfriend simulator", "ai girlfriend chat",
    "best ai girlfriend app", "ai girlfriend apps", "ai gf chat",
    "porn ai", "ai porn chat", "ai porn girlfriend",
]

# Image generation use case (Pleasur AI Image Generation product)
IMAGE_GEN_TERMS = [
    "ai image", "image generator ai", "nsfw image", "ai picture",
    "nsfw ai generator", "ai nsfw generator", "uncensored ai image",
    "ai art generator nsfw", "nsfw ai image", "ai pic generator",
    "ai photo maker", "ai porn generator", "porn ai generator",
    "girlfriend image generator", "ai girlfriend image",
    "nsfw maker", "nsfw ai creator",
]

# Lower fit (adjacent / brand-name-driven / wrong vertical)
LOW_FIT_TERMS = [
    "candy ai", "candy a", "candya", "candiai", "candy ai videos", "candy ai images",  # competitor brand variants
    "nastia", "ourdream", "nofiltergpt",  # competitor brand variants
    "replika", "muah ai", "grok ai", "polybuzz", "spicychat", "crushon", "joyland", "perchance",
    "girlfriend movie", "companion movie",  # film references
    "ai companion robot",  # physical robot vertical
    "vector robot", "vector 2.0",
    "ai bbw porn", "ai cumshot", "ai generated cum", "ai furry", "ai trans girlfriend", "ai gay porn",
    # niche fetish-specific (still some product fit but lower brand_fit)
]

REJECT_TERMS = [
    # Brand-named misspellings / competitors with very low product_fit (we'd be writing a competitor brand article)
    "candiai", "candya", "candy a",
    # Real-life movie or unrelated meanings that polluted the SERP via parent_topic
    "ai girlfriend movie",
    # Misspellings that aren't worth indexing
    "ai girlfrind", "ai girfriend", "ai girfriend", "ai girfried", "ai girlfried", "ai girlf", "nsfw ai chst", "nsfw ai caht", "nsfw ai chat.", "ai chat.",
]

# ---- SERP intent heuristics (signals from keyword + serp_features) ----
TOOL_LED_TOKENS = ["generator", "creator", "maker"]
COMMERCIAL_TOKENS = ["best ", "vs ", "review", "alternative", " app", " apps"]
HOWTO_TOKENS = ["how to", "guide", "what is", "what does"]


def classify_brand_fit(kw: str) -> int:
    kl = kw.lower().strip()
    # rejects first
    for r in REJECT_TERMS:
        if kl == r or (r in kl and len(kl) <= len(r) + 3):
            return 1
    # competitor brand variants → very low brand_fit
    for low in LOW_FIT_TERMS:
        if low in kl:
            return 3
    # high-fit core niche terms
    for hi in HIGH_FIT_TERMS:
        if hi in kl:
            return 9
    for ig in IMAGE_GEN_TERMS:
        if ig in kl:
            return 8
    # contains "ai" + relevant adult/companion modifier somewhere
    if "ai" in kl and any(t in kl for t in ["girlfriend", "boyfriend", "companion", "chat", "sex", "nsfw", "porn", "horny", "nude", "naked", "dirty", "sext", "spicy", "naughty", "roleplay"]):
        return 7
    # generic ai term, weak fit
    if "ai" in kl:
        return 5
    return 4


def classify_product_fit(kw: str) -> int:
    """Pleasur.AI products: Companion Creator (chat) + Image Generation."""
    kl = kw.lower()
    # Companion Creator demos
    creator_signals = [
        "ai girlfriend", "ai boyfriend", "create", "make", "ai companion",
        "ai roleplay", "character ai", "ai chat", "sexting", "sex chat",
        "girlfriend creator", "girlfriend generator", "girlfriend maker",
        "build your", "design your", "ai girlfriend app", "ai gf chat",
        "ai chatbot girlfriend", "ai girl chat", "virtual girlfriend",
        "uncensored chat", "no filter", "spicy ai", "horny ai",
        "ai sex bot", "ai sex chat", "nsfw chat", "nude ai chat",
        "dirty ai", "dirty talk ai", "talk dirty", "naughty ai", "nasty ai",
        "romantic ai", "ai girlfriends",
    ]
    # Image Generation demos
    image_signals = [
        "image generator", "ai nsfw generator", "nsfw ai gen",
        "ai porn", "porn ai", "ai photo", "ai picture", "ai pic generator",
        "uncensored ai generator", "ai art generator", "image ai",
        "nsfw ai photo", "nsfw maker", "nsfw ai creator", "ai cumshot generator",
        "furry porn ai", "ai furry porn",
    ]
    if any(s in kl for s in creator_signals) and any(s in kl for s in image_signals):
        return 9  # both products fit
    if any(s in kl for s in creator_signals):
        return 8
    if any(s in kl for s in image_signals):
        return 7
    if "ai" in kl and any(t in kl for t in ["girl", "boy", "companion", "chat"]):
        return 6
    return 4


def classify_serp_intent(kw: str, serp_features: str) -> str:
    kl = kw.lower()
    sf = serp_features.lower() if serp_features else ""
    # tool-led: keyword shape strongly indicates a tool
    if any(tok in kl for tok in TOOL_LED_TOKENS):
        # but exclude "best X generator" which is comparison, not tool
        if any(tok in kl for tok in ["best ", "vs "]):
            return "commercial-investigation"
        return "tool-led"
    # commercial-investigation: best/vs/review/alternative/app
    if any(tok in kl for tok in COMMERCIAL_TOKENS):
        return "commercial-investigation"
    # how-to / what-is informational
    if any(tok in kl for tok in HOWTO_TOKENS):
        return "informational"
    # SERP-feature signal: if SERP shows "discussion" + "question" → informational
    if "question" in sf or "discussion" in sf:
        return "informational"
    # ai_overview presence → informational (people-also-ask style)
    if "ai_overview" in sf:
        return "informational"
    # Default informational for niche terms
    return "informational"


def difficulty_pass(kd_str: str) -> tuple[bool, str]:
    try:
        kd = int(kd_str)
    except (TypeError, ValueError):
        return False, "kd_missing"
    if kd <= DR_GAP_LIMIT:
        return True, ""
    return False, "dr_gap_too_wide"


def vet(row: dict) -> dict:
    kw = row["keyword"]
    bf = classify_brand_fit(kw)
    pf = classify_product_fit(kw)
    intent = classify_serp_intent(kw, row.get("serp_features", ""))
    diff_ok, diff_reason = difficulty_pass(row["kd"])

    # Estimate dr_top10_median + weak_link_count from KD as proxy:
    # KD is correlated with DR-gate; we use kd directly for the autonomous BID gate
    dr_top10_median = row["kd"]  # proxy
    weak_link_count = 2 if int(row["kd"] or 0) <= BRAND_DR + 5 else (1 if int(row["kd"] or 0) <= BRAND_DR + 15 else 0)

    # B test
    b_pass = bf >= 4 and pf >= 3
    if not b_pass:
        return {
            **row,
            "brand_fit": bf,
            "product_fit": pf,
            "serp_intent": intent,
            "dr_top10_median": dr_top10_median,
            "weak_link_count": weak_link_count,
            "bid_verdict": "FAIL",
            "bid_reason": "low_brand_fit" if bf < 4 else "low_product_fit",
        }

    # I test
    if intent == "transactional":
        return {
            **row,
            "brand_fit": bf,
            "product_fit": pf,
            "serp_intent": intent,
            "dr_top10_median": dr_top10_median,
            "weak_link_count": weak_link_count,
            "bid_verdict": "FAIL",
            "bid_reason": "serp_is_transactional",
        }
    # tool-led: keep PASS but mark serp_intent=tool-led so Layer 5 routes to tool-opportunities
    # (Per SKILL: tool-led keywords are AI-Overview-immune and routable, not rejected outright)

    # D test
    if not diff_ok:
        return {
            **row,
            "brand_fit": bf,
            "product_fit": pf,
            "serp_intent": intent,
            "dr_top10_median": dr_top10_median,
            "weak_link_count": weak_link_count,
            "bid_verdict": "FAIL",
            "bid_reason": diff_reason,
        }

    return {
        **row,
        "brand_fit": bf,
        "product_fit": pf,
        "serp_intent": intent,
        "dr_top10_median": dr_top10_median,
        "weak_link_count": weak_link_count,
        "bid_verdict": "PASS",
        "bid_reason": "",
    }


# ---- Run ----
with IDEAS.open("r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

vetted = [vet(r) for r in rows]

# Counts
b_pass = sum(1 for r in vetted if int(r["brand_fit"]) >= 4 and int(r["product_fit"]) >= 3)
b_fail = len(vetted) - b_pass
i_tool = sum(1 for r in vetted if r["serp_intent"] == "tool-led")
i_pass = sum(1 for r in vetted if r["serp_intent"] in ("informational", "commercial-investigation", "hybrid", "tool-led"))
d_pass = sum(1 for r in vetted if int(r["dr_top10_median"]) <= DR_GAP_LIMIT)
overall_pass = sum(1 for r in vetted if r["bid_verdict"] == "PASS")

# Write back
fieldnames = list(vetted[0].keys())
with IDEAS.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(vetted)

print(f"Vetted {len(vetted)} candidates")
print(f"  B (business potential): {b_pass} PASS, {b_fail} FAIL")
print(f"  I (intent): {i_pass} accept-eligible (tool-led: {i_tool})")
print(f"  D (difficulty proxy KD<={DR_GAP_LIMIT}): {d_pass} PASS, {len(vetted)-d_pass} FAIL")
print(f"  Overall: {overall_pass} PASS, {len(vetted)-overall_pass} FAIL")

# Top 5 PASS by traffic_potential
pass_rows = sorted([r for r in vetted if r["bid_verdict"] == "PASS"],
                   key=lambda r: -int(r["traffic_potential"]))
print("\nTop 5 PASS by traffic_potential:")
for r in pass_rows[:5]:
    print(f"  {r['keyword']:<40} TP={int(r['traffic_potential']):>7} KD={r['kd']:>2} V={r['volume']:>6} intent={r['serp_intent']} BF={r['brand_fit']} PF={r['product_fit']}")

# Top 5 FAIL with reasons
fail_rows = sorted([r for r in vetted if r["bid_verdict"] == "FAIL"],
                   key=lambda r: -int(r["traffic_potential"]))
print("\nTop 5 FAIL with reasons:")
for r in fail_rows[:5]:
    print(f"  {r['keyword']:<40} reason={r['bid_reason']}")

# Calibration log
with (ROOT / "cache" / "bid-calibration.log").open("a", encoding="utf-8") as f:
    f.write(f"2026-05-04 BID run: {len(vetted)} vetted, {overall_pass} PASS ({100*overall_pass//len(vetted)}%), brand_DR={BRAND_DR}, dr_gap_limit={DR_GAP_LIMIT}\n")
