"""Apply Layer 4 redteam verdicts to keyword-ideas.csv."""
import csv
from pathlib import Path

ROOT = Path(r"C:\Users\ndong\Downloads\blog-agent-2\content-pipeline\0-keywords")
IDEAS = ROOT / "keyword-ideas.csv"

# Verdicts derived in redteam-notes.md
# Format: keyword -> (verdict, delta, summary)
VERDICTS = {
    "spicy ai": ("DROP", 0, "Branded query for SpicyChat masquerading as informational; vanity-rank trap"),
    "nsfw ai photo maker": ("KEEP", 0, "Genuine tool-opportunity; route to /generate"),
    "nsfw ai image generator no login": ("KEEP", 0, "Tool keyword; competitive bar is no-login UX"),
    "nsfw ai generator no login": ("KEEP", 0, "Variant of no-login tool kw; consolidate"),
    "nsfw ai generator image": ("KEEP", 0, "Tool-opportunity for /generate"),
    "ai chat girlfriend": ("KEEP", 0, "Core funnel keyword for Companion Creator"),
    "ai girlfriend experience": ("REVISE_PRIORITY", 0.5, "AIO-resistant opinion-driven top-of-funnel keyword"),
    "ai nsfw generator free": ("KEEP", 0, "Tool-opportunity; free-tier framing"),
    "ai girlfriend chat": ("KEEP", 0, "Core listicle keyword, beatable"),
    "ai girlfriend love simulator": ("REVISE_PRIORITY", -0.8, "Adjacent: love-sim seekers, not chat seekers"),
    "ai girlfriend chat bot": ("KEEP", 0, "Variant of ai girlfriend chat"),
    "ai chat bot girlfriend": ("KEEP", 0, "Lowest-difficulty top-30 candidate"),
    "ai girlfriend text": ("REVISE_PRIORITY", -0.5, "Narrow texting variant; lower priority"),
    "nsfw ai pic generator": ("KEEP", 0, "Tool-opportunity; consolidate cluster"),
    "nsfw ai companion": ("KEEP", 0, "Highest brand-categorical match; must-write"),
    "free ai art generator nsfw": ("KEEP", 0, "Tool-opportunity; route to /generate"),
    "ai chat nsfw free": ("KEEP", 0, "KD 16 — high-priority displacement target"),
    "ai chat nsfw": ("KEEP", 0, "Core listicle keyword"),
    "ai nsfw chat": ("KEEP", 0, "Word-order variant of ai chat nsfw"),
    "ai nsfw chat bot": ("KEEP", 0, "KD 18 soft-difficulty variant"),
    "ai roleplay porn": ("REVISE_PRIORITY", -1.0, "Audience mismatch: porn-directory seekers"),
    "nsfw ai chat porn": ("REVISE_PRIORITY", -0.5, "Mixed-audience query; borderline"),
    "ai girlfriend simulator": ("REVISE_PRIORITY", -0.8, "Same audience mismatch as love simulator"),
    "virtual ai girlfriend": ("KEEP", 0, "Solid category synonym"),
    "ai chatbot girlfriend": ("KEEP", 0, "AIO-RISKY but salvageable with comparative depth"),
    "image generator ai nsfw": ("KEEP", 0, "Tool-opportunity"),
    "ai girlfriend image generator": ("KEEP", 0, "Highest combined product_fit; flagship tool"),
    "ai girlfriend game": ("REVISE_PRIORITY", -0.8, "Game-vs-chat mismatch"),
    "ai girlfriend games": ("REVISE_PRIORITY", -0.8, "Plural variant of #28"),
    "fake ai girlfriend": ("REVISE_PRIORITY", -1.0, "Awareness-stage keyword with negative framing"),
}

with IDEAS.open("r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

applied = 0
for r in rows:
    kw = r["keyword"]
    if kw in VERDICTS:
        v, delta, summary = VERDICTS[kw]
        r["redteam_verdict"] = v
        r["redteam_priority_delta"] = str(delta)
        r["redteam_critique_summary"] = summary
        applied += 1
    else:
        # Untouched rows
        if not r.get("redteam_verdict"):
            r["redteam_verdict"] = ""
            r["redteam_priority_delta"] = ""
            r["redteam_critique_summary"] = ""

# Write back
fieldnames = list(rows[0].keys())
with IDEAS.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)

# Summary
keep = sum(1 for v in VERDICTS.values() if v[0] == "KEEP")
drop = sum(1 for v in VERDICTS.values() if v[0] == "DROP")
revise = sum(1 for v in VERDICTS.values() if v[0] == "REVISE_PRIORITY")
revise_neg = sum(1 for v in VERDICTS.values() if v[0] == "REVISE_PRIORITY" and v[1] < 0)
revise_pos = sum(1 for v in VERDICTS.values() if v[0] == "REVISE_PRIORITY" and v[1] > 0)
sum_neg = sum(v[1] for v in VERDICTS.values() if v[0] == "REVISE_PRIORITY" and v[1] < 0)
sum_pos = sum(v[1] for v in VERDICTS.values() if v[0] == "REVISE_PRIORITY" and v[1] > 0)

print(f"Applied {applied} redteam verdicts")
print(f"  KEEP: {keep}")
print(f"  DROP: {drop}")
print(f"  REVISE_PRIORITY+: {revise_pos} (sum delta: +{sum_pos:.1f})")
print(f"  REVISE_PRIORITY-: {revise_neg} (sum delta: {sum_neg:.1f})")

# Top DROPs
print("\nDROPs:")
for kw, (v, d, s) in VERDICTS.items():
    if v == "DROP":
        print(f"  - {kw} — {s}")

# Top REVISE-
print("\nTop 3 REVISE-:")
neg_list = sorted([(kw, v, d, s) for kw, (v, d, s) in VERDICTS.items() if v == "REVISE_PRIORITY" and d < 0], key=lambda x: x[2])
for kw, v, d, s in neg_list[:3]:
    print(f"  - {kw} — {s} (delta: {d:.1f})")
