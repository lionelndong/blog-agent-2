#!/usr/bin/env python3
"""Parse a quality-check verdict file and emit a deterministic exit code.

Reads `content-pipeline/quality-checks/<slug>.md` and looks for the verdict line
written by /quality-check ("PASS", "BORDERLINE", "FAIL") plus any CRITICAL flags
in the punch list. Used by the autonomous blog loop's revision retry logic.

Exit codes:
    0   PASS (>=75)
    1   BORDERLINE without CRITICAL items in punch list
    2   BORDERLINE with CRITICAL items in punch list (revision needed)
    3   FAIL (<60) (revision needed)
    4   Verdict unparseable / file missing

Usage:
    python scripts/auto_quality_gate.py <slug>
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QC_DIR = ROOT / "content-pipeline" / "quality-checks"

VERDICT_RE = re.compile(r"\b(PASS|BORDERLINE|FAIL)\b", re.IGNORECASE)
SCORE_RE = re.compile(r"(?:score|verdict)[^0-9]*?(\d{1,3})", re.IGNORECASE)
CRITICAL_RE = re.compile(r"\bCRITICAL\b", re.IGNORECASE)


def first_verdict(text: str) -> str | None:
    head = "\n".join(text.splitlines()[:30])
    m = VERDICT_RE.search(head)
    return m.group(1).upper() if m else None


def has_critical(text: str) -> bool:
    return bool(CRITICAL_RE.search(text))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    args = parser.parse_args()

    path = QC_DIR / f"{args.slug}.md"
    if not path.exists():
        print(f"error: {path} not found", file=sys.stderr)
        sys.exit(4)

    text = path.read_text(encoding="utf-8")
    verdict = first_verdict(text)
    if verdict is None:
        print(f"error: no verdict found in {path}", file=sys.stderr)
        sys.exit(4)

    critical = has_critical(text)
    print(f"{verdict}{' (CRITICAL)' if critical and verdict != 'FAIL' else ''}")

    if verdict == "PASS":
        sys.exit(0)
    if verdict == "BORDERLINE":
        sys.exit(2 if critical else 1)
    sys.exit(3)


if __name__ == "__main__":
    main()
