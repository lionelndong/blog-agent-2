#!/usr/bin/env python3
"""Action-shot capture entrypoint (dispatcher-facing shim).

History: this used to drive **Browser Use Cloud** — a paid LLM agent that returned low-res,
non-deterministic viewport screenshots. For clean, aspirational *retina* product shots that was the
wrong tool. Replaced 2026-06-28 by the deterministic engine in `action_shot.py`: our own patchright
capture (Cloudflare bypass + 18+ gate + 2880×1800 retina), the session minted by `setup_auth.py`,
and an on-brand frame (`frame_shot.py`). No paid cloud agent, no per-task LLM spend.

This module just re-exports `action_shot.run(goal, out_path, *, start_url, max_steps, llm)` so
`generate_visuals.py`'s `_handle_action_shot` keeps working unchanged. Run `action_shot.py`
directly (or via a `--preset`) for full control.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from action_shot import run  # noqa: E402,F401  re-exported for generate_visuals._handle_action_shot


if __name__ == "__main__":
    import action_shot
    sys.exit(action_shot.main())
