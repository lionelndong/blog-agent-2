#!/usr/bin/env python3
"""Pick the next unwritten keyword from the vetted queue for the autonomous blog loop.

Reads `content-pipeline/0-keywords/keyword-queue.csv` (produced by /keyword-research-pipeline)
and emits one JSON object on stdout for the top-ranked keyword whose slug isn't already in
`content-pipeline/8-publish/<slug>/` or quarantined in `content-pipeline/9-needs-review/<slug>.md`.

Exit codes:
    0   Selected a keyword (JSON on stdout).
    2   Queue empty / missing — orchestrator should run /keyword-research-pipeline.
    1   Other failure (CSV malformed, etc.) — error on stderr.

Usage:
    python scripts/auto_keyword_selector.py
    python scripts/auto_keyword_selector.py --top 3        # emit top-3 as JSON array
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "content-pipeline" / "0-keywords" / "keyword-queue.csv"
PUBLISHED_DIR = ROOT / "content-pipeline" / "8-publish"
QUARANTINE_DIR = ROOT / "content-pipeline" / "9-needs-review"


def published_slugs() -> set[str]:
    if not PUBLISHED_DIR.exists():
        return set()
    return {p.name for p in PUBLISHED_DIR.iterdir() if p.is_dir()}


def quarantined_slugs() -> set[str]:
    if not QUARANTINE_DIR.exists():
        return set()
    return {p.stem for p in QUARANTINE_DIR.glob("*.md")}


def candidate_rows() -> list[dict[str, str]]:
    if not QUEUE.exists():
        sys.exit(2)
    with QUEUE.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader if r.get("keyword")]
    if not rows:
        sys.exit(2)
    return rows


def parse_score(row: dict[str, str]) -> float:
    try:
        return float(row.get("priority_score", "") or 0)
    except ValueError:
        return 0.0


def select(rows: list[dict[str, str]], top: int) -> list[dict[str, str]]:
    excluded = published_slugs() | quarantined_slugs()
    available = [r for r in rows if r.get("slug") and r["slug"] not in excluded]
    available.sort(key=parse_score, reverse=True)
    return available[:top]


def to_payload(row: dict[str, str]) -> dict[str, object]:
    keys = (
        "keyword",
        "slug",
        "priority_score",
        "source",
        "serp_intent",
        "bid_verdict",
        "aio_verdict",
        "redteam_verdict",
        "redteam_critique_summary",
    )
    payload: dict[str, object] = {}
    for k in keys:
        v = row.get(k, "")
        if k == "priority_score":
            try:
                payload[k] = float(v) if v else None
            except ValueError:
                payload[k] = None
        else:
            payload[k] = v or None
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top", type=int, default=1, help="Emit top-N as JSON array (default 1)")
    args = parser.parse_args()

    rows = candidate_rows()
    picked = select(rows, args.top)
    if not picked:
        sys.exit(2)

    if args.top == 1:
        print(json.dumps(to_payload(picked[0]), ensure_ascii=False))
    else:
        print(json.dumps([to_payload(r) for r in picked], ensure_ascii=False))


if __name__ == "__main__":
    main()
