#!/usr/bin/env python3
"""Per-slug, per-stage revision-budget tracking for adversarial pushback loops.

Phase 3 of PLEAA-392 (PLEAA-418, 2026-05-06): every production stage gets an
adversarial sub-agent that pushes back on its own output before the orchestrator
advances. Failures the adversarial agent identifies trigger a revision pass
within a per-stage budget. After the budget is exhausted, halt and write to
9-needs-review.

The orchestrator owns dispatch; this module just keeps the bookkeeping. Budgets
live at `.runs/{slug}-budgets.json` so they survive across orchestrator
sub-agents and so `pipeline_gate.py` can read them.

Per-stage env-var defaults (each is the *number of revision passes allowed*,
NOT counting the original generation):

    BLOG_AGENT_OUTLINE_REVISION_BUDGET     default 1   (PLEAA-418 spec)
    BLOG_AGENT_RESEARCH_REVISION_BUDGET    default 1
    BLOG_AGENT_VISUALS_REVISION_BUDGET     default 1
    BLOG_AGENT_REVISION_BUDGET             default 2   (existing prose loop)

CLI:
    python scripts/adversarial_runlog.py status <slug>
    python scripts/adversarial_runlog.py used <slug> <stage>
    python scripts/adversarial_runlog.py budget <stage>
    python scripts/adversarial_runlog.py increment <slug> <stage>
    python scripts/adversarial_runlog.py can-revise <slug> <stage>
        # exit 0 if a revision pass is still within budget, 1 if exhausted

Stage keys:
    outline | research | visuals | quality
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNS_DIR = REPO_ROOT / ".runs"

# Stage -> env var name -> default budget. Default 1 for the new Phase-3 loops
# matches PLEAA-418's "One revision pass on FAIL" spec; the older prose loop
# stays at 2 to preserve existing BLOG_AGENT_REVISION_BUDGET behaviour.
STAGE_BUDGETS = {
    "outline": ("BLOG_AGENT_OUTLINE_REVISION_BUDGET", 1),
    "research": ("BLOG_AGENT_RESEARCH_REVISION_BUDGET", 1),
    "visuals": ("BLOG_AGENT_VISUALS_REVISION_BUDGET", 1),
    "quality": ("BLOG_AGENT_REVISION_BUDGET", 2),
}


def budget_for(stage: str) -> int:
    if stage not in STAGE_BUDGETS:
        raise ValueError(f"unknown stage '{stage}'. valid: {', '.join(STAGE_BUDGETS)}")
    env_name, default = STAGE_BUDGETS[stage]
    raw = os.environ.get(env_name)
    if raw is None or raw == "":
        return default
    try:
        return max(0, int(raw))
    except ValueError:
        return default


def _path(slug: str) -> Path:
    return RUNS_DIR / f"{slug}-budgets.json"


def _load(slug: str) -> dict:
    p = _path(slug)
    if not p.exists():
        return {"slug": slug, "stages": {}}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {"slug": slug, "stages": {}}


def _save(slug: str, data: dict) -> None:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    _path(slug).write_text(json.dumps(data, indent=2), encoding="utf-8")


def used(slug: str, stage: str) -> int:
    # Validate the stage so an unknown key surfaces at the earliest call site
    # — keeps used()/budget_for()/increment() consistent (all three raise
    # ValueError for unknown stages) and avoids the silent `used=0` followed
    # by an exception on the next line trap when callers chain the two.
    if stage not in STAGE_BUDGETS:
        raise ValueError(f"unknown stage '{stage}'. valid: {', '.join(STAGE_BUDGETS)}")
    data = _load(slug)
    return int(data.get("stages", {}).get(stage, {}).get("revisions_used", 0))


def increment(slug: str, stage: str) -> int:
    if stage not in STAGE_BUDGETS:
        raise ValueError(f"unknown stage '{stage}'")
    data = _load(slug)
    stages = data.setdefault("stages", {})
    entry = stages.setdefault(stage, {"revisions_used": 0})
    entry["revisions_used"] = int(entry.get("revisions_used", 0)) + 1
    _save(slug, data)
    return entry["revisions_used"]


def can_revise(slug: str, stage: str) -> bool:
    return used(slug, stage) < budget_for(stage)


def status(slug: str) -> dict:
    data = _load(slug)
    out = {"slug": slug, "stages": {}}
    for stage in STAGE_BUDGETS:
        u = used(slug, stage)
        b = budget_for(stage)
        out["stages"][stage] = {
            "revisions_used": u,
            "budget": b,
            "exhausted": u >= b,
        }
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 64
    cmd = argv[1]
    if cmd == "status":
        if len(argv) != 3:
            print("usage: status <slug>", file=sys.stderr)
            return 64
        print(json.dumps(status(argv[2]), indent=2))
        return 0
    # Wrap the stage-aware subcommands so an unknown-stage `ValueError` surfaces
    # as a usage error (exit 64) rather than Python's default unformatted-traceback
    # exit 1 — which the orchestrator interprets as "budget exhausted — HALT" for
    # `can-revise`, silently halting the pipeline on a typo'd stage key.
    if cmd == "used":
        if len(argv) != 4:
            print("usage: used <slug> <stage>", file=sys.stderr)
            return 64
        try:
            print(used(argv[2], argv[3]))
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 64
        return 0
    if cmd == "budget":
        if len(argv) != 3:
            print("usage: budget <stage>", file=sys.stderr)
            return 64
        try:
            print(budget_for(argv[2]))
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 64
        return 0
    if cmd == "increment":
        if len(argv) != 4:
            print("usage: increment <slug> <stage>", file=sys.stderr)
            return 64
        try:
            n = increment(argv[2], argv[3])
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 64
        print(n)
        return 0
    if cmd == "can-revise":
        if len(argv) != 4:
            print("usage: can-revise <slug> <stage>", file=sys.stderr)
            return 64
        try:
            return 0 if can_revise(argv[2], argv[3]) else 1
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 64
    print(f"unknown subcommand: {cmd}", file=sys.stderr)
    return 64


if __name__ == "__main__":
    sys.exit(main(sys.argv))
