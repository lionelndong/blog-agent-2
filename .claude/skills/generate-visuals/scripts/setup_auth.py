#!/usr/bin/env python3
"""Mint + verify the Pleasur.AI showcase session for logged-in action-shots (rebuilt 2026-06-28).

Logged-in product shots (a chat with a persona, a call screen, the image gallery) need a real
Pleasur.AI session. This script logs in ONCE and persists the session to
`.claude/skills/generate-visuals/auth/state.json` (Playwright storage_state — cookies + Supabase
localStorage). `capture_screenshot.py` / `action_shot.py` then replay it. Nothing here is committed
(auth/.gitignore excludes it); for cloud use, `--print-b64` emits PLEASUR_AUTH_STATE_B64 for Doppler.

Works in the VPS container: prefers **patchright** (the engine that already beats Cloudflare here) —
no real-Chrome / Google-OAuth-Chromium requirement. Three ways to get a session:

  1) INTERACTIVE (any auth method — password / OTP / Google / Apple), recommended on the VPS:
       python setup_auth.py --interactive --headed
     Then open noVNC (http://100.73.44.58:6080/vnc.html, pw in CLAUDE.md), log into pleasur.ai in
     the visible browser, and CLOSE the window. The session is snapshotted every second.

  2) CREDENTIALS (hands-off, only if the showcase account is plain email+password):
       python setup_auth.py --email show@pleasur.ai --password '...' [--login-url ...]

  3) VERIFY an existing/just-minted session (no login):
       python setup_auth.py --verify

Always finish with a verify. SFW showcase account only.
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
import time
from pathlib import Path
from typing import Any

AUTH_DIR = Path(__file__).resolve().parent.parent / "auth"
AUTH_STATE = AUTH_DIR / "state.json"
GITIGNORE = AUTH_DIR / ".gitignore"

DEFAULT_LOGIN_URL = "https://pleasur.ai/login"
DEFAULT_VERIFY_URL = "https://pleasur.ai/profile"
LOGIN_URL_HINTS = ("/login", "/signin", "/sign-in", "/auth")
LOGGED_OUT_TEXTS = ("join free", "sign up free", "log in", "login", "sign in")

STEALTH_INIT_JS = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
window.chrome = window.chrome || { runtime: {} };
"""


def _playwright():
    """Prefer patchright (beats Cloudflare in this container); fall back to vanilla playwright."""
    try:
        from patchright.sync_api import sync_playwright
        return sync_playwright, True
    except ImportError:
        try:
            from playwright.sync_api import sync_playwright
            return sync_playwright, False
        except ImportError:
            sys.stderr.write("Neither patchright nor playwright is installed.\n")
            return None, False


def _ensure_auth_dir() -> None:
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    # The session is a secret — never let it be committed.
    if not GITIGNORE.exists():
        GITIGNORE.write_text("# Session secrets — never commit.\n*\n!.gitignore\n", encoding="utf-8")


def _new_context(p, using_patchright: bool, headed: bool, storage_state: str | None):
    ctx_kwargs: dict[str, Any] = {
        "viewport": {"width": 1440, "height": 900},
        "locale": "en-US",
        "timezone_id": "America/New_York",
    }
    if storage_state:
        ctx_kwargs["storage_state"] = storage_state
    if using_patchright:
        browser = p.chromium.launch(headless=not headed)
    else:
        ctx_kwargs["user_agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        try:
            browser = p.chromium.launch(channel="chrome", headless=not headed,
                                        args=["--disable-blink-features=AutomationControlled"])
        except Exception:
            browser = p.chromium.launch(headless=not headed)
    context = browser.new_context(**ctx_kwargs)
    if not using_patchright:
        context.add_init_script(STEALTH_INIT_JS)
    return browser, context


def _snapshot(context) -> int:
    try:
        state = context.storage_state()
    except Exception:
        return 0
    if state.get("cookies") or state.get("origins"):
        AUTH_STATE.write_text(json.dumps(state), encoding="utf-8")
        return len(state.get("cookies", []))
    return 0


def _dismiss_age_gate(page) -> bool:
    """Dismiss the 18+ age gate / common blocking modals before touching the form."""
    import re
    try:
        page.get_by_text("I am 18 years of age or older", exact=True).click(timeout=3000)
        page.wait_for_timeout(1000)
        return True
    except Exception:
        pass
    for t in ("I am 18 or older", "Yes, I am 18", "Enter site", "I Agree", "Accept all", "Continue to site"):
        try:
            loc = page.locator("button", has_text=re.compile(re.escape(t), re.I))
            if loc.count() == 0:
                continue
            loc.first.click(timeout=2500, force=True)
            page.wait_for_timeout(800)
            return True
        except Exception:
            continue
    return False


def _auth_signals(page) -> dict[str, Any]:
    """Heuristic: logged-OUT pages show Login/Join-Free CTAs; logged-IN do not."""
    final_url = page.url
    redirected = any(h in final_url.lower() for h in LOGIN_URL_HINTS)
    try:
        login_ctas = page.evaluate(
            """(texts)=>{const els=[...document.querySelectorAll('a,button,[role=button]')];
                return els.filter(e=>{const t=(e.textContent||'').trim().toLowerCase();
                  return texts.some(x=>t===x);}).length;}""",
            list(LOGGED_OUT_TEXTS),
        )
    except Exception:
        login_ctas = -1
    logged_in = (not redirected) and login_ctas == 0
    return {"final_url": final_url, "redirected_to_login": redirected,
            "login_ctas_found": login_ctas, "logged_in": logged_in}


def verify(verify_url: str, headed: bool) -> int:
    if not AUTH_STATE.exists():
        sys.stderr.write("no auth/state.json to verify — run a login mode first.\n")
        return 2
    sp, using = _playwright()
    if sp is None:
        return 2
    with sp() as p:
        browser, context = _new_context(p, using, headed, str(AUTH_STATE))
        page = context.new_page()
        try:
            page.goto(verify_url, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_load_state("load", timeout=15000)
            page.wait_for_timeout(2500)
        except Exception as exc:
            sys.stderr.write(f"verify navigation failed: {exc}\n")
            browser.close()
            return 2
        _dismiss_age_gate(page)
        signals = _auth_signals(page)
        browser.close()
    state = json.loads(AUTH_STATE.read_text())
    out = {"verify_url": verify_url, "cookies": len(state.get("cookies", [])),
           "origins": len(state.get("origins", [])), **signals}
    json.dump(out, sys.stdout, indent=2)
    sys.stdout.write("\n")
    if signals["logged_in"]:
        sys.stdout.write("SESSION OK — logged in. Action-shots can capture authed pages.\n")
        return 0
    sys.stdout.write("SESSION INVALID — looks logged out. Re-run a login mode.\n")
    return 1


def login_credentials(email: str, password: str, login_url: str, headed: bool,
                      sel_email: str | None, sel_pw: str | None, sel_submit: str | None) -> int:
    sp, using = _playwright()
    if sp is None:
        return 2
    _ensure_auth_dir()
    with sp() as p:
        browser, context = _new_context(p, using, headed, None)
        page = context.new_page()
        try:
            page.goto(login_url, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_load_state("load", timeout=15000)
            page.wait_for_timeout(2500)
        except Exception as exc:
            sys.stderr.write(f"login navigation failed: {exc}\n")
            browser.close()
            return 2

        if _dismiss_age_gate(page):
            sys.stderr.write("info: dismissed age gate\n")
        email_sel = sel_email or "input[type=email], input[name=email], input[autocomplete=username]"
        pw_sel = sel_pw or "input[type=password], input[name=password]"
        try:
            page.locator(email_sel).first.fill(email, timeout=8000)
            page.locator(pw_sel).first.fill(password, timeout=8000)
        except Exception as exc:
            browser.close()
            sys.stderr.write(
                f"could not find email/password fields ({exc}).\n"
                "The login may be OTP/magic-link/OAuth — use --interactive via noVNC instead, "
                "or pass --email-selector/--password-selector/--submit-selector.\n"
            )
            return 1
        try:
            if sel_submit:
                page.locator(sel_submit).first.click(timeout=6000)
            else:
                import re
                page.get_by_role("button", name=re.compile(r"log\s*in|sign\s*in|continue", re.I)).first.click(timeout=6000)
        except Exception:
            page.locator(pw_sel).first.press("Enter")
        # wait to leave the login page
        for _ in range(20):
            page.wait_for_timeout(1000)
            if not any(h in page.url.lower() for h in LOGIN_URL_HINTS):
                break
        page.wait_for_timeout(1500)
        n = _snapshot(context)
        signals = _auth_signals(page)
        browser.close()
    if not AUTH_STATE.exists() or not signals["logged_in"]:
        sys.stderr.write(f"login did not produce a valid session (signals={signals}).\n")
        return 1
    sys.stdout.write(f"saved {AUTH_STATE} ({n} cookies). logged_in={signals['logged_in']}\n")
    return 0


def login_interactive(start_url: str, headed: bool) -> int:
    sp, using = _playwright()
    if sp is None:
        return 2
    _ensure_auth_dir()
    with sp() as p:
        browser, context = _new_context(p, using, headed, None)
        page = context.pages[0] if context.pages else context.new_page()
        try:
            page.goto(start_url, timeout=60000)
        except Exception as exc:
            sys.stderr.write(f"warning: initial navigation failed: {exc}\n")
        sys.stdout.write(
            "Browser is open under DISPLAY=:99.\n"
            "Open noVNC (http://100.73.44.58:6080/vnc.html), log into pleasur.ai (any method —\n"
            "password / OTP / Google / Apple), then CLOSE the browser window to finish.\n"
            "The session is snapshotted every second, so closing any time is safe.\n"
        )
        sys.stdout.flush()
        try:
            while True:
                if not context.pages:
                    break
                _snapshot(context)
                time.sleep(1.0)
        except KeyboardInterrupt:
            sys.stderr.write("\ninterrupted; using last snapshot if any.\n")
        _snapshot(context)
        try:
            context.close()
        except Exception:
            pass
        try:
            browser.close()
        except Exception:
            pass
    if not AUTH_STATE.exists():
        sys.stderr.write("no state.json captured — the window may have closed before login.\n")
        return 1
    sys.stdout.write(f"saved {AUTH_STATE}\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Mint + verify the Pleasur.AI showcase session.")
    ap.add_argument("--interactive", action="store_true", help="manual login via a visible browser (noVNC)")
    ap.add_argument("--email", default=None)
    ap.add_argument("--password", default=None)
    ap.add_argument("--login-url", default=DEFAULT_LOGIN_URL)
    ap.add_argument("--email-selector", dest="sel_email", default=None)
    ap.add_argument("--password-selector", dest="sel_pw", default=None)
    ap.add_argument("--submit-selector", dest="sel_submit", default=None)
    ap.add_argument("--verify", action="store_true", help="verify an existing session (no login)")
    ap.add_argument("--verify-url", default=DEFAULT_VERIFY_URL)
    ap.add_argument("--start-url", default="https://pleasur.ai/login", help="interactive start URL")
    ap.add_argument("--headed", action="store_true", help="visible browser (needed for interactive + Cloudflare)")
    ap.add_argument("--headless", action="store_true", help="force headless (credentials/verify only)")
    ap.add_argument("--print-b64", action="store_true", help="print PLEASUR_AUTH_STATE_B64 for Doppler")
    args = ap.parse_args()

    headed = True if args.headed else (False if args.headless else not args.verify)

    if args.verify and not (args.interactive or args.email):
        return verify(args.verify_url, headed=headed if args.headed or args.headless else True)

    if args.email and args.password:
        rc = login_credentials(args.email, args.password, args.login_url, headed,
                               args.sel_email, args.sel_pw, args.sel_submit)
    elif args.interactive:
        rc = login_interactive(args.start_url, headed=True)
    else:
        ap.error("choose a mode: --interactive | --email/--password | --verify")
        return 2

    if rc == 0 and args.print_b64 and AUTH_STATE.exists():
        encoded = base64.b64encode(AUTH_STATE.read_bytes()).decode("ascii")
        sys.stdout.write("\n--- PLEASUR_AUTH_STATE_B64 ---\n" + encoded + "\n--- end ---\n")
        sys.stdout.write("Paste into Doppler (pleasurai/dev) as PLEASUR_AUTH_STATE_B64.\n")

    if rc == 0 and args.verify:
        sys.stdout.write("\n--- verifying ---\n")
        return verify(args.verify_url, headed=False)
    return rc


if __name__ == "__main__":
    sys.exit(main())
