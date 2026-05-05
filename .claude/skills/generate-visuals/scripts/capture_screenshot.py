#!/usr/bin/env python3
"""Capture a screenshot of a brand-owned UI URL using Playwright.

Supports element-clipped captures (via CSS selector), manual rect crops,
post-capture quality heuristics, and optional Claude-vision validation.

Standalone usage:
    python capture_screenshot.py --url <url> --out <path>
        [--selector "css selector"]
        [--crop X,Y,W,H]
        [--annotate "css selector to highlight"]
        [--validate]   # opt-in vision check via Claude API

Env vars:
    PLEASUR_AUTH_STATE_B64 — base64-encoded state.json (cloud-friendly).
                             Falls back to .claude/skills/generate-visuals/auth/state.json on disk.
    ANTHROPIC_API_KEY      — required only when --validate is set.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
DEFAULT_AUTH_STATE = Path(__file__).resolve().parent.parent / "auth" / "state.json"

VIEWPORT = {"width": 1440, "height": 900}
DEVICE_SCALE_FACTOR = 2

LOGIN_URL_HINTS = ("/login", "/signin", "/sign-in", "/auth")
MIN_FILE_BYTES = 5_000
MIN_COLOR_VARIANCE = 0.02  # below this = mostly blank/uniform capture

# Cloudflare bot-wall fingerprints (page title + body markers)
CF_TITLE_HINTS = ("just a moment", "attention required", "checking your browser")
CF_BODY_HINTS = (
    "performing security verification",
    "checking if the site connection is secure",
    "ddos protection by cloudflare",
    "verify you are human",
    "ray id:",
)

# Realistic user agent — Playwright's default flags us as automation
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

# Buttons that dismiss common blocking modals (age gates, cookie banners, etc).
# Matched as case-insensitive substrings of the button's visible text.
KNOWN_MODAL_DISMISS_TEXTS = (
    "i am 18 years of age or older",
    "i am 18 or older",
    "yes, i am 18",
    "enter site",
    "i agree",
    "accept all",
    "accept cookies",
    "got it",
    "continue to site",
)


# Stealth init script: remove the obvious Playwright/automation fingerprints
STEALTH_INIT_JS = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
window.chrome = window.chrome || { runtime: {} };
const originalQuery = window.navigator.permissions && window.navigator.permissions.query;
if (originalQuery) {
    window.navigator.permissions.query = (p) => (
        p.name === 'notifications'
            ? Promise.resolve({ state: Notification.permission })
            : originalQuery(p)
    );
}
"""


# ---------------------------------------------------------------------------
# Auth state resolution: env var (cloud) > on-disk file (local)
# ---------------------------------------------------------------------------

def _decode_b64_forgiving(value: str) -> bytes | None:
    """Decode base64 even when padding / whitespace / Supabase prefixes got mixed in."""
    # Strip whitespace, newlines, quotes
    cleaned = "".join(value.split()).strip("'\"")
    # Strip Supabase's "base64-" marker if someone pasted a cookie value verbatim
    if cleaned.startswith("base64-"):
        cleaned = cleaned[len("base64-"):]
    # Repair missing padding
    pad = (-len(cleaned)) % 4
    cleaned_padded = cleaned + ("=" * pad)
    for decoder in (base64.b64decode, base64.urlsafe_b64decode):
        try:
            return decoder(cleaned_padded)
        except Exception:
            continue
    return None


def _is_playwright_state(blob: bytes) -> bool:
    """Playwright state.json has top-level keys 'cookies' and 'origins'."""
    try:
        import json as _json
        data = _json.loads(blob)
    except Exception:
        return False
    return isinstance(data, dict) and ("cookies" in data or "origins" in data)


def _resolve_auth_state() -> str | None:
    """Return a path to a usable state.json, or None if no auth available.

    Priority:
      1. PLEASUR_AUTH_STATE_B64 env var (decoded to a tempfile)
      2. on-disk auth/state.json
    """
    encoded = os.environ.get("PLEASUR_AUTH_STATE_B64")
    if encoded:
        decoded = _decode_b64_forgiving(encoded)
        if decoded and _is_playwright_state(decoded):
            tmp = tempfile.NamedTemporaryFile(
                prefix="pleasur_auth_", suffix=".json", delete=False
            )
            tmp.write(decoded)
            tmp.close()
            return tmp.name
        sys.stderr.write(
            "warning: PLEASUR_AUTH_STATE_B64 is not a valid Playwright state.json. "
            "It must contain top-level 'cookies' and 'origins' keys (the format produced by "
            "Playwright's context.storage_state()).\n"
            "Common mistake: pasting a Supabase session object from browser localStorage "
            "instead of running setup_auth.py.\n"
            "Fix: run\n"
            "  python .claude/skills/generate-visuals/scripts/setup_auth.py --print-b64\n"
            "and replace the Doppler secret with the value it prints.\n"
        )
    if DEFAULT_AUTH_STATE.exists():
        return str(DEFAULT_AUTH_STATE)
    return None


# ---------------------------------------------------------------------------
# Quality heuristics on the captured PNG
# ---------------------------------------------------------------------------

def _check_quality(
    image_path: Path,
    final_url: str,
    expected_url: str,
    used_selector: bool = False,
) -> dict[str, Any]:
    """Return a quality report. status: 'ok' | 'suspect' | 'failed'.

    When `used_selector` is True, dimension thresholds are relaxed (the user
    explicitly clipped to a small region; their selector is the source of truth
    for what counts as "right size").
    """
    if not image_path.exists():
        return {"status": "failed", "reason": "image_missing"}

    size = image_path.stat().st_size
    if size < MIN_FILE_BYTES:
        return {"status": "failed", "reason": "image_too_small", "bytes": size}

    # Redirect to login = auth broken
    final_lower = final_url.lower()
    if any(hint in final_lower for hint in LOGIN_URL_HINTS) and not any(
        hint in expected_url.lower() for hint in LOGIN_URL_HINTS
    ):
        return {
            "status": "failed",
            "reason": "redirected_to_login",
            "final_url": final_url,
            "expected_url": expected_url,
        }

    # Color variance — catch mostly-blank captures
    try:
        from PIL import Image, ImageStat
        with Image.open(image_path) as img:
            width, height = img.size
            min_height = 30 if used_selector else 100
            min_width = 100 if used_selector else 200
            if height < min_height or width < min_width:
                return {
                    "status": "failed",
                    "reason": "image_dimensions_too_small",
                    "width": width,
                    "height": height,
                    "min_required": {"width": min_width, "height": min_height},
                }
            stat = ImageStat.Stat(img.convert("RGB"))
            mean_stddev = sum(stat.stddev) / (len(stat.stddev) * 255.0)
            if mean_stddev < MIN_COLOR_VARIANCE:
                return {
                    "status": "suspect",
                    "reason": "low_color_variance",
                    "stddev_normalized": round(mean_stddev, 4),
                    "hint": "Capture may be a blank page, login wall, or render failure",
                }
            return {
                "status": "ok",
                "width": width,
                "height": height,
                "stddev_normalized": round(mean_stddev, 4),
                "bytes": size,
            }
    except ImportError:
        # Pillow unavailable — best-effort: only check file size
        return {"status": "ok", "bytes": size, "note": "pillow_unavailable_skipped_variance_check"}
    except Exception as exc:
        return {"status": "suspect", "reason": "quality_check_error", "error": str(exc)}


# ---------------------------------------------------------------------------
# Vision validation (opt-in, costs money)
# ---------------------------------------------------------------------------

def _validate_with_vision(image_path: Path, expected_what: str) -> dict[str, Any]:
    """Ask Claude whether this image shows what the placeholder said it would.

    Returns {ok: bool, verdict: str, reason: str}. Cheap (~$0.003/check on Haiku).
    Requires ANTHROPIC_API_KEY in env.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {"ok": True, "verdict": "skipped", "reason": "no_anthropic_api_key"}
    try:
        import anthropic
    except ImportError:
        return {"ok": True, "verdict": "skipped", "reason": "anthropic_sdk_not_installed"}

    image_b64 = base64.b64encode(image_path.read_bytes()).decode("ascii")
    client = anthropic.Anthropic(api_key=api_key)
    prompt = (
        f"This screenshot is supposed to show: \"{expected_what}\".\n\n"
        "Check whether the image clearly shows that subject. Reply in one line as "
        "JSON like: {\"ok\": true, \"verdict\": \"matches\", \"reason\": \"...\"} or "
        "{\"ok\": false, \"verdict\": \"login_wall\"|\"wrong_content\"|\"low_quality\"|\"empty\", "
        "\"reason\": \"...\"}.\n\nNo other text. Just the JSON line."
    )
    try:
        resp = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {"type": "base64", "media_type": "image/png", "data": image_b64},
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
        text = "".join(b.text for b in resp.content if hasattr(b, "text")).strip()
        # Be forgiving about extra text
        first_brace = text.find("{")
        last_brace = text.rfind("}")
        if first_brace == -1 or last_brace == -1:
            return {"ok": True, "verdict": "unparseable", "reason": text[:200]}
        try:
            parsed = json.loads(text[first_brace : last_brace + 1])
        except json.JSONDecodeError:
            return {"ok": True, "verdict": "unparseable", "reason": text[:200]}
        return {
            "ok": bool(parsed.get("ok", True)),
            "verdict": parsed.get("verdict", "unknown"),
            "reason": parsed.get("reason", ""),
        }
    except Exception as exc:
        return {"ok": True, "verdict": "error", "reason": str(exc)[:200]}


# ---------------------------------------------------------------------------
# Capture
# ---------------------------------------------------------------------------

def _parse_crop(spec: str | None) -> dict[str, int] | None:
    if not spec:
        return None
    parts = spec.split(",")
    if len(parts) != 4:
        return None
    try:
        x, y, w, h = (int(p.strip()) for p in parts)
    except ValueError:
        return None
    if w <= 0 or h <= 0:
        return None
    return {"x": x, "y": y, "width": w, "height": h}


def capture(
    url: str,
    out_path: Path,
    selector: str | None = None,
    crop: dict[str, int] | None = None,
    annotate_selector: str | None = None,
    validate: bool = False,
    expected_what: str | None = None,
    headed: bool = False,
) -> dict[str, Any]:
    """Capture a screenshot. Returns a result dict for the manifest."""
    # Prefer patchright over playwright. Patchright is a drop-in fork that
    # patches CDP detection to bypass Cloudflare/DataDome/PerimeterX bot
    # protection. Patchright requires MINIMAL launch options — no channel,
    # no custom args, no ignore_default_args. It handles those internally
    # to avoid leaving fingerprints.
    using_patchright = False
    try:
        from patchright.sync_api import sync_playwright  # type: ignore[import-not-found]
        using_patchright = True
    except ImportError:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            return {
                "status": "failed",
                "reason": "playwright_not_installed",
                "hint": "pip install patchright && patchright install chromium",
            }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    auth_state = _resolve_auth_state()
    # Profile dir from setup_auth — has the EXACT browser fingerprint that
    # earned the cf_clearance cookie, so CF doesn't re-challenge.
    profile_dir = ROOT / ".claude" / "skills" / "generate-visuals" / "auth" / "profile"
    use_persistent_profile = profile_dir.is_dir() and any(profile_dir.iterdir())
    # Optional residential proxy for sites with extreme bot protection
    # (CF Pro / Akamai / DataDome). Format: http://user:pass@host:port
    proxy_url = os.environ.get("SCREENSHOT_PROXY")
    proxy_config: dict[str, str] | None = None
    if proxy_url:
        from urllib.parse import urlparse
        parsed = urlparse(proxy_url)
        proxy_config = {"server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}"}
        if parsed.username:
            proxy_config["username"] = parsed.username
        if parsed.password:
            proxy_config["password"] = parsed.password

    with sync_playwright() as p:
        # Patchright wants minimal launch options — no channel, no args,
        # no custom UA — it handles automation hiding internally. Vanilla
        # playwright needs the manual stealth flags + real Chrome channel.
        if using_patchright:
            common_args: list[str] = []
            context_kwargs: dict[str, Any] = {
                "viewport": VIEWPORT,
                "device_scale_factor": DEVICE_SCALE_FACTOR,
                "locale": "en-US",
                "timezone_id": "America/New_York",
            }
        else:
            common_args = [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-features=IsolateOrigins,site-per-process",
            ]
            context_kwargs = {
                "viewport": VIEWPORT,
                "device_scale_factor": DEVICE_SCALE_FACTOR,
                "user_agent": DEFAULT_USER_AGENT,
                "locale": "en-US",
                "timezone_id": "America/New_York",
            }

        if proxy_config:
            context_kwargs["proxy"] = proxy_config

        browser = None
        if use_persistent_profile:
            # Persistent context = same profile that issued cf_clearance.
            # Best chance of getting past Cloudflare on protected pages.
            try:
                if using_patchright:
                    context = p.chromium.launch_persistent_context(
                        str(profile_dir),
                        headless=not headed,
                        **context_kwargs,
                    )
                else:
                    context = p.chromium.launch_persistent_context(
                        str(profile_dir),
                        channel="chrome",
                        headless=not headed,
                        args=common_args,
                        ignore_default_args=["--enable-automation"],
                        **context_kwargs,
                    )
            except Exception as exc:
                sys.stderr.write(f"info: persistent profile launch failed ({exc}); falling back\n")
                use_persistent_profile = False

        if not use_persistent_profile:
            if using_patchright:
                browser = p.chromium.launch(headless=not headed)
            else:
                launch_kwargs: dict[str, Any] = {
                    "headless": not headed,
                    "args": common_args,
                }
                try:
                    browser = p.chromium.launch(channel="chrome", **launch_kwargs)
                except Exception:
                    sys.stderr.write(
                        "info: real Chrome unavailable, falling back to bundled Chromium\n"
                    )
                    browser = p.chromium.launch(**launch_kwargs)
            if auth_state:
                context_kwargs["storage_state"] = auth_state
            context = browser.new_context(**context_kwargs)

        # When patchright is in use, skip playwright-stealth — patchright
        # has deeper stealth built in, and layering them causes conflicts.
        # When vanilla playwright is in use, apply playwright-stealth.
        try:
            if using_patchright:
                raise ImportError  # short-circuit to skip apply
            from playwright_stealth import Stealth
            Stealth().apply_stealth_sync(context)
        except ImportError:
            if not using_patchright:
                sys.stderr.write(
                    "info: playwright-stealth not installed; using minimal stealth. "
                    "pip install playwright-stealth for Cloudflare-protected pages.\n"
                )
                context.add_init_script(STEALTH_INIT_JS)

        def _cleanup() -> None:
            try:
                if browser is not None:
                    _cleanup()
                else:
                    context.close()
            except Exception:
                pass
        page = context.new_page()
        try:
            # SPAs with realtime / analytics keep network busy — networkidle
            # never fires. domcontentloaded + a settle wait is more reliable.
            page.goto(url, wait_until="domcontentloaded", timeout=45_000)
            page.wait_for_load_state("load", timeout=15_000)
            page.wait_for_timeout(2_000)
        except Exception as exc:
            _cleanup()
            return {"status": "failed", "reason": "navigation_failed", "error": str(exc), "url": url}

        # If we landed on a Cloudflare challenge, give it up to ~12s to resolve.
        page_title = ""
        try:
            page_title = (page.title() or "").lower()
        except Exception:
            pass
        if any(hint in page_title for hint in CF_TITLE_HINTS):
            # CF Turnstile Pro can take 15-30s. Wait up to 40s, polling.
            for _ in range(20):
                page.wait_for_timeout(2_000)
                try:
                    page_title = (page.title() or "").lower()
                except Exception:
                    pass
                if not any(hint in page_title for hint in CF_TITLE_HINTS):
                    break
            if any(hint in page_title for hint in CF_TITLE_HINTS):
                # Still stuck — capture for diagnostics but flag it
                try:
                    page.screenshot(path=str(out_path), full_page=False)
                except Exception:
                    pass
                _cleanup()
                return {
                    "status": "failed",
                    "reason": "cloudflare_challenge_unresolved",
                    "page_title": page_title,
                    "url": url,
                    "final_url": page.url,
                    "auth_used": auth_state is not None,
                    "hint": "Cloudflare detected automation. Either refresh the auth state (cookies prove you're a returning user, which CF treats more leniently) or use a residential-IP proxy / non-headless mode for this domain.",
                }

        # Dismiss known blocking modals (age gate, cookie banner, etc.)
        # The brand owns this site — clicking through their own legal modal is fine.
        # Modals often render after DOMContentLoaded as a separate animation; give them time.
        page.wait_for_timeout(1_500)
        modal_dismissed = False
        for text in KNOWN_MODAL_DISMISS_TEXTS:
            try:
                # Plain substring match (case-insensitive) — Playwright's regex
                # variants of these matchers can be picky about whole-word boundaries,
                # so the simple 2-arg form is more reliable.
                # We try several candidate locators in order.
                candidates = [
                    page.locator(
                        "button",
                        has_text=re.compile(re.escape(text), re.I),
                    ),
                    page.locator(
                        "[role='button']",
                        has_text=re.compile(re.escape(text), re.I),
                    ),
                    page.locator(
                        "a",
                        has_text=re.compile(re.escape(text), re.I),
                    ),
                ]
                for locator in candidates:
                    try:
                        cnt = locator.count()
                    except Exception:
                        continue
                    if cnt == 0:
                        continue
                    first = locator.first
                    try:
                        first.wait_for(state="visible", timeout=2_000)
                    except Exception:
                        continue
                    try:
                        first.scroll_into_view_if_needed(timeout=1_500)
                    except Exception:
                        pass
                    try:
                        first.click(timeout=3_000, force=True)
                        page.wait_for_timeout(1_000)
                        modal_dismissed = True
                        sys.stderr.write(f"info: dismissed modal via text='{text}'\n")
                        break
                    except Exception as click_exc:
                        sys.stderr.write(f"info: matched '{text}' but click failed: {click_exc}\n")
                        continue
                if modal_dismissed:
                    break
            except Exception:
                continue
        if modal_dismissed:
            try:
                page.wait_for_load_state("networkidle", timeout=5_000)
            except Exception:
                pass

        final_url = page.url

        # Optional annotation: highlight an element before capture
        if annotate_selector:
            try:
                page.evaluate(
                    """sel => {
                        const el = document.querySelector(sel);
                        if (el) {
                            el.style.outline = '4px solid #ef4444';
                            el.style.outlineOffset = '2px';
                            el.scrollIntoView({block: 'center'});
                        }
                    }""",
                    annotate_selector,
                )
                page.wait_for_timeout(300)  # let scroll/repaint settle
            except Exception:
                pass

        # Capture: prefer element-clipped > manual crop > viewport
        try:
            if selector:
                locator = page.locator(selector).first
                try:
                    locator.scroll_into_view_if_needed(timeout=5_000)
                except Exception:
                    pass
                locator.screenshot(path=str(out_path))
            elif crop:
                # Capture full viewport then crop with Pillow
                tmp_full = out_path.with_suffix(".full.png")
                page.screenshot(path=str(tmp_full), full_page=False)
                try:
                    from PIL import Image
                    with Image.open(tmp_full) as img:
                        # Account for device scale factor in crop coords
                        sf = DEVICE_SCALE_FACTOR
                        box = (
                            crop["x"] * sf,
                            crop["y"] * sf,
                            (crop["x"] + crop["width"]) * sf,
                            (crop["y"] + crop["height"]) * sf,
                        )
                        img.crop(box).save(out_path, format="PNG")
                    tmp_full.unlink(missing_ok=True)
                except Exception as exc:
                    _cleanup()
                    return {"status": "failed", "reason": "crop_failed", "error": str(exc)}
            else:
                page.screenshot(path=str(out_path), full_page=False)
        except Exception as exc:
            _cleanup()
            return {"status": "failed", "reason": "screenshot_failed", "error": str(exc)}

        _cleanup()

    # Heuristic quality checks (relaxed when caller specified an explicit selector)
    quality = _check_quality(
        out_path,
        final_url=final_url,
        expected_url=url,
        used_selector=bool(selector),
    )
    if quality["status"] == "failed":
        return {
            "status": "failed",
            "reason": quality["reason"],
            "quality": quality,
            "url": url,
            "final_url": final_url,
            "auth_used": auth_state is not None,
        }

    try:
        rel_path = str(out_path.relative_to(ROOT))
    except ValueError:
        rel_path = str(out_path)
    result: dict[str, Any] = {
        "status": "captured",
        "path": rel_path,
        "url": url,
        "final_url": final_url,
        "auth_used": auth_state is not None,
        "quality": quality,
    }
    if quality["status"] == "suspect":
        result["needs_review"] = True

    # Optional vision validation (costs money; only run if explicitly asked)
    if validate and expected_what:
        verdict = _validate_with_vision(out_path, expected_what)
        result["vision"] = verdict
        if not verdict.get("ok", True):
            result["needs_review"] = True
            result["status"] = "captured_suspect"

    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--selector", default=None, help="CSS selector to clip the capture to")
    parser.add_argument("--crop", default=None, help="Manual crop X,Y,W,H (CSS px, pre-scale)")
    parser.add_argument("--annotate", default=None, help="CSS selector to highlight before capture")
    parser.add_argument("--validate", action="store_true", help="Run Claude vision check (costs money)")
    parser.add_argument("--what", default=None, help="Expected subject — used by --validate")
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run with a visible browser window. Required for sites with aggressive Cloudflare bot detection (e.g. Pleasur /generate). On VPS, run under xvfb-run.",
    )
    args = parser.parse_args()

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = ROOT / out_path

    result = capture(
        args.url,
        out_path,
        selector=args.selector,
        crop=_parse_crop(args.crop),
        annotate_selector=args.annotate,
        validate=args.validate,
        expected_what=args.what,
        headed=args.headed,
    )
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if result.get("status", "").startswith("captured") else 1


if __name__ == "__main__":
    sys.exit(main())
