#!/usr/bin/env python3
"""Run a Browser Use Cloud task to capture an action-driven screenshot.

Unlike capture_screenshot.py (which navigates one URL and clicks one optional
selector), this script gives an LLM agent a natural-language goal and lets it
drive a real browser through whatever multi-step flow the goal requires:
log in, click into a conversation, fill a form, scroll past an age gate, etc.

Usage:
    python run_action_shot.py --goal "..." --out <path> [--url <start_url>]
                              [--max-steps N] [--llm gpt-4o]

Env vars:
    BROWSER_USE_API_KEY   — required, from cloud.browser-use.com
    BROWSER_USE_LLM       — optional override (default: gpt-4o)
    BROWSER_USE_MAX_STEPS — optional override (default: 25)

Output: a PNG written to --out, plus the same JSON envelope capture_screenshot.py
emits so the dispatcher treats it uniformly.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path
from typing import Any


def _download(url: str, dest: Path) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=30) as resp:
        data = resp.read()
    dest.write_bytes(data)
    return len(data)


def run(goal: str, out_path: Path, *, start_url: str | None, max_steps: int, llm: str) -> dict[str, Any]:
    api_key = os.environ.get("BROWSER_USE_API_KEY")
    if not api_key:
        return {
            "status": "manual",
            "reason": "browser_use_api_key_missing",
            "hint": "Set BROWSER_USE_API_KEY in Doppler (project: pleasurai, config: dev).",
        }

    try:
        from browser_use_sdk import BrowserUse
    except ImportError:
        return {
            "status": "manual",
            "reason": "browser_use_sdk_not_installed",
            "hint": "pip install browser-use-sdk",
        }

    client = BrowserUse(api_key=api_key)
    try:
        result = client.run(
            task=goal,
            start_url=start_url,
            llm=llm,
            max_steps=max_steps,
            highlight_elements=False,
            vision=True,
        )
    except Exception as exc:
        return {"status": "failed", "reason": "browser_use_run_error", "error": str(exc)}

    status = str(getattr(result, "status", "")).lower()
    is_success = bool(getattr(result, "is_success", False))
    steps = list(getattr(result, "steps", []) or [])
    cost = getattr(result, "cost", None)
    output_text = getattr(result, "output", None)

    # Pick the last step that has a screenshot. Fall back to any with one.
    screenshot_url: str | None = None
    for step in reversed(steps):
        url = getattr(step, "screenshot_url", None)
        if url:
            screenshot_url = url
            break

    if not screenshot_url:
        return {
            "status": "failed",
            "reason": "no_screenshot_in_steps",
            "task_status": status,
            "is_success": is_success,
            "agent_output": str(output_text)[:500] if output_text else None,
        }

    try:
        bytes_written = _download(screenshot_url, out_path)
    except Exception as exc:
        return {
            "status": "failed",
            "reason": "screenshot_download_failed",
            "error": str(exc),
            "screenshot_url": screenshot_url,
        }

    if bytes_written < 5_000:
        return {
            "status": "failed",
            "reason": "downloaded_screenshot_too_small",
            "bytes": bytes_written,
            "screenshot_url": screenshot_url,
        }

    return {
        "status": "captured",
        "path": str(out_path),
        "screenshot_url": screenshot_url,
        "agent_status": status,
        "agent_success": is_success,
        "agent_output": str(output_text)[:500] if output_text else None,
        "agent_steps": len(steps),
        "agent_cost_usd": str(cost.root) if cost is not None and hasattr(cost, "root") else (str(cost) if cost is not None else None),
        "agent_llm": llm,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--goal", required=True, help="Natural-language description of what to capture")
    parser.add_argument("--out", required=True, help="Output PNG path")
    parser.add_argument("--url", default=None, help="Optional starting URL")
    parser.add_argument("--max-steps", type=int, default=int(os.environ.get("BROWSER_USE_MAX_STEPS", "25")))
    parser.add_argument("--llm", default=os.environ.get("BROWSER_USE_LLM", "claude-sonnet-4-6"))
    args = parser.parse_args()

    out_path = Path(args.out).resolve()
    result = run(
        args.goal,
        out_path,
        start_url=args.url,
        max_steps=args.max_steps,
        llm=args.llm,
    )
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if result.get("status") == "captured" else 1


if __name__ == "__main__":
    sys.exit(main())
