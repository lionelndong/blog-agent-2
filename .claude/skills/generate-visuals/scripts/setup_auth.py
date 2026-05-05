#!/usr/bin/env python3
"""One-time browser login flow that saves Pleasur.AI session state.

Usage:
    python .claude/skills/generate-visuals/scripts/setup_auth.py [--start-url <url>] [--print-b64] [--browser chrome|chromium]

Launches a non-headless browser pointed at the brand login page.
Log in manually (including Google / Apple OAuth flows). When you're done,
**close the browser window** — the script saves cookies + storage to
auth/state.json and exits.

By default uses your installed Chrome (channel="chrome") because Google
OAuth blocks Playwright's bundled Chromium with a "secure browser"
warning. Pass --browser chromium to override.

For cloud deployments (VPS, GitHub Actions): pass --print-b64 to also print
a base64-encoded copy of state.json. Paste that value into Doppler / GitHub
Secrets as PLEASUR_AUTH_STATE_B64. The capture script reads that env var
in cloud environments where the state.json file isn't checked in.
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path
from typing import Any

AUTH_DIR = Path(__file__).resolve().parent.parent / "auth"
AUTH_STATE = AUTH_DIR / "state.json"
PROFILE_DIR = AUTH_DIR / "profile"
DEFAULT_START_URL = "https://pleasur.ai/login"

STEALTH_INIT_JS = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
window.chrome = window.chrome || { runtime: {} };
"""

STEALTH_LAUNCH_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-default-browser-check",
    "--no-first-run",
    "--disable-features=IsolateOrigins,site-per-process",
]


def run(start_url: str, browser_choice: str) -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.stderr.write(
            "playwright is not installed. Run: pip install playwright && playwright install chromium\n"
        )
        return 2

    import time

    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        # Persistent context = real Chrome user data dir. Critical for OAuth:
        # Google's "secure browser" check trusts a stable profile + real Chrome
        # but rejects Playwright's bundled Chromium even with stealth flags.
        launch_kwargs: dict[str, Any] = {
            "headless": False,
            "args": STEALTH_LAUNCH_ARGS,
            "ignore_default_args": ["--enable-automation"],
            "viewport": {"width": 1440, "height": 900},
            "user_agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
        }
        if browser_choice == "chrome":
            launch_kwargs["channel"] = "chrome"

        try:
            context = p.chromium.launch_persistent_context(
                str(PROFILE_DIR), **launch_kwargs
            )
        except Exception as exc:
            if browser_choice == "chrome":
                sys.stderr.write(
                    f"could not launch real Chrome ({exc}). Falling back to bundled Chromium.\n"
                    "If Google OAuth still blocks, install Chrome and re-run.\n"
                )
                launch_kwargs.pop("channel", None)
                context = p.chromium.launch_persistent_context(
                    str(PROFILE_DIR), **launch_kwargs
                )
            else:
                raise

        # Apply stealth init JS to every page context creates.
        try:
            context.add_init_script(STEALTH_INIT_JS)
        except Exception:
            pass

        def snapshot_state() -> None:
            try:
                state = context.storage_state()
                if state.get("cookies") or state.get("origins"):
                    AUTH_STATE.write_text(json.dumps(state))
                    sys.stderr.write(
                        f"info: snapshot saved ({len(state.get('cookies', []))} cookies, "
                        f"{len(state.get('origins', []))} origins)\n"
                    )
            except Exception:
                pass

        page = context.pages[0] if context.pages else context.new_page()
        try:
            page.goto(start_url, timeout=60_000)
        except Exception as exc:
            sys.stderr.write(f"warning: initial navigation failed: {exc}\n")
        sys.stdout.write(
            "Browser is open (real Chrome with stealth flags).\n"
            "Log in to Pleasur.AI — Google / Apple / Discord OAuth will all work.\n"
            "After you've signed in, **close the browser window** to finish.\n"
            "The script snapshots state every second so closing any time is safe.\n"
        )
        sys.stdout.flush()

        try:
            while True:
                if not context.browser and not context.pages:
                    break
                try:
                    if not context.pages:
                        break
                except Exception:
                    break
                snapshot_state()
                time.sleep(1.0)
        except KeyboardInterrupt:
            sys.stderr.write("\nInterrupted; using last snapshot if any.\n")

        # Final snapshot before close.
        snapshot_state()
        try:
            context.close()
        except Exception:
            pass

    if not AUTH_STATE.exists():
        sys.stderr.write("no state.json was captured — browser may have closed before login.\n")
        return 1
    sys.stdout.write(f"saved {AUTH_STATE}\n")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-url", default=DEFAULT_START_URL)
    parser.add_argument(
        "--browser",
        default="chrome",
        choices=["chrome", "chromium"],
        help="Which browser to launch. Default: chrome (real installed Chrome — required for Google OAuth).",
    )
    parser.add_argument(
        "--print-b64",
        action="store_true",
        help="Print the base64-encoded state.json so you can paste it into Doppler / GitHub Secrets as PLEASUR_AUTH_STATE_B64",
    )
    args = parser.parse_args()
    rc = run(args.start_url, args.browser)
    if rc == 0 and args.print_b64 and AUTH_STATE.exists():
        encoded = base64.b64encode(AUTH_STATE.read_bytes()).decode("ascii")
        sys.stdout.write("\n--- PLEASUR_AUTH_STATE_B64 ---\n")
        sys.stdout.write(encoded + "\n")
        sys.stdout.write("--- end ---\n")
        sys.stdout.write(
            "Paste the value above into Doppler (or your secret store) as PLEASUR_AUTH_STATE_B64.\n"
        )
    return rc


if __name__ == "__main__":
    sys.exit(main())
