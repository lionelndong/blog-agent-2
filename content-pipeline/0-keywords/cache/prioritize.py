"""Layer 5 prioritization: filter, score, boost, slugify, write queues."""
import csv
import math
import subprocess
from pathlib import Path

ROOT = Path(r"C:\Users\ndong\Downloads\blog-agent-2\content-pipeline\0-keywords")
IDEAS = ROOT / "keyword-ideas.csv"
QUEUE = ROOT / "keyword-queue.csv"
TOOLS = ROOT / "tool-opportunities.csv"
SCRIPTS = Path(r"C:\Users\ndong\Downloads\blog-agent-2\scripts")


def traffic_score(tp: int, kd: int) -> float:
    raw = min(10.0, math.log10(tp + 1) * 2) - (kd / 20)
    return max(0.0, min(10.0, raw))


def slug_for(kw: str) -> str:
    try:
        out = subprocess.run(
            ["python", str(SCRIPTS / "slugify.py"), kw],
            capture_output=True, text=True, check=True
        )
        return out.stdout.strip()
    except Exception:
        return kw.lower().replace(" ", "-").replace("/", "-")


# ---- Read input ----
with IDEAS.open("r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

# ---- Filter ----
def survives(r) -> bool:
    if r["bid_verdict"] != "PASS":
        return False
    if r["aio_verdict"] not in ("PASS", "RISKY", "UNKNOWN"):
        return False
    rv = r.get("redteam_verdict", "")
    # Untouched (no redteam) is allowed — it just means it wasn't in top-30
    if rv in ("DROP",):
        return False
    return True


survivors = [r for r in rows if survives(r)]

# ---- Score & boost ----
for r in survivors:
    tp = int(r["traffic_potential"])
    kd = int(r["kd"])
    bf = int(r["brand_fit"])
    pf = int(r["product_fit"])

    base = 0.4 * traffic_score(tp, kd) + 0.3 * bf + 0.3 * pf

    boost = 0.0
    if r["source"] == "aio_gap":
        boost += 1.5
    if r["serp_intent"] == "tool-led":
        boost += 1.0  # recorded for triage; tool-led routes elsewhere

    delta = 0.0
    if r.get("redteam_priority_delta"):
        try:
            delta = float(r["redteam_priority_delta"])
        except ValueError:
            delta = 0.0
        # cap ±2.0
        delta = max(-2.0, min(2.0, delta))

    final = base + boost + delta
    r["priority_score"] = f"{final:.2f}"
    r["notes"] = (
        f"base={base:.2f} (T={traffic_score(tp,kd):.2f},BF={bf},PF={pf}) "
        f"boost={boost:.1f} delta={delta:+.1f}"
    )


# ---- Sort & rank ----
survivors.sort(key=lambda r: -float(r["priority_score"]))


# ---- Split queues ----
writing_queue = [r for r in survivors if r["serp_intent"] != "tool-led"][:50]
tool_queue = [r for r in survivors if r["serp_intent"] == "tool-led"]

# Slugify writing queue (work on copies so we don't mutate the original rows)
queue_with_extras = []
for i, r in enumerate(writing_queue, 1):
    rc = dict(r)
    rc["rank"] = i
    rc["slug"] = slug_for(r["keyword"])
    queue_with_extras.append(rc)


# ---- Write keyword-queue.csv ----
queue_fields = [
    "rank", "keyword", "slug", "priority_score",
    "volume", "kd", "traffic_potential",
    "source", "serp_intent",
    "bid_verdict", "aio_verdict", "redteam_verdict",
    "brand_fit", "product_fit",
    "competitor_top_position", "competitor_domains",
    "parent_topic", "intent",
    "redteam_priority_delta", "redteam_critique_summary",
    "notes",
]
with QUEUE.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=queue_fields)
    w.writeheader()
    for r in queue_with_extras:
        w.writerow({k: r.get(k, "") for k in queue_fields})


# ---- Write tool-opportunities.csv ----
tool_fields = [
    "keyword", "volume", "kd", "traffic_potential",
    "priority_score", "source",
    "bid_verdict", "redteam_verdict",
    "redteam_critique_summary", "notes",
]
with TOOLS.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=tool_fields)
    w.writeheader()
    for r in tool_queue:
        w.writerow({k: r.get(k, "") for k in tool_fields})


# ---- Update keyword-ideas.csv with priority_score for all rows ----
all_fields = list(rows[0].keys())
with IDEAS.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=all_fields)
    w.writeheader()
    w.writerows(rows)


# ---- Summary ----
aio_gap_boosted = sum(1 for r in writing_queue if r["source"] == "aio_gap")
print(f"Queue size: {len(writing_queue)} (top 50 ranked)")
print(f"Tool-opportunities count: {len(tool_queue)}")
print(f"AIO-gap-boosted: {aio_gap_boosted}")
print(f"\nTop 10 in keyword-queue.csv:")
for r in queue_with_extras[:10]:
    print(
        f"  #{r['rank']:>2} {r['priority_score']:>5} {r['keyword']:<40} "
        f"src={r['source']:<14} intent={r['serp_intent']:<25} "
        f"bid={r['bid_verdict']:<4} aio={r['aio_verdict']:<6} rt={r['redteam_verdict'] or 'untouched'}"
    )

print(f"\nTop 5 tool-opportunities:")
for r in tool_queue[:5]:
    print(f"  {r['priority_score']:>5} {r['keyword']:<40} V={r['volume']:>6} KD={r['kd']:>2}")
