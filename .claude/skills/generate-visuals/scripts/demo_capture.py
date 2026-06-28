#!/usr/bin/env python3
"""Capture a SEQUENCE of frames of a scripted page interaction.

The animated-demo engine's capture stage. Drives a real (headed, under DISPLAY=:99)
patchright browser through a *scene* — a list of beats, each beat being some actions
(click / type / hover / scroll) followed by either a held keyframe or a burst of
motion frames — and returns ordered frame segments that demo_polish.py turns into a
loopable GIF / MP4 / WebP.

It reuses the proven stealth + Cloudflare-wait + age-gate + auth machinery from
capture_screenshot.py (the public capture engine) so it clears pleasur.ai's
Cloudflare and 18+ gate exactly the same way.

This module is a library (imported by animate_demo.py); it has no CLI of its own.
"""
from __future__ import annotations

import io
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

SCRIPT_DIR = Path(__file__).resolve().parent

# --- Reuse the public capture engine's constants/helpers (DRY). ---------------
# capture_screenshot.py lives next to us; fall back to local copies if its
# module-level ROOT computation ever fails to import in an odd layout.
try:
    sys.path.insert(0, str(SCRIPT_DIR))
    from capture_screenshot import (  # type: ignore
        STEALTH_INIT_JS,
        KNOWN_MODAL_DISMISS_TEXTS,
        CF_TITLE_HINTS,
        DEFAULT_USER_AGENT,
        _resolve_auth_state,
    )
except Exception:  # pragma: no cover - defensive fallback
    STEALTH_INIT_JS = (
        "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"
    )
    KNOWN_MODAL_DISMISS_TEXTS = (
        "i am 18 years of age or older",
        "i am 18 or older",
        "yes, i am 18",
        "enter site",
        "i agree",
        "accept all",
        "got it",
        "continue to site",
    )
    CF_TITLE_HINTS = ("just a moment", "attention required", "checking your browser")
    DEFAULT_USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    )

    def _resolve_auth_state() -> str | None:  # type: ignore
        enc = os.environ.get("PLEASUR_AUTH_STATE_B64")
        return None if not enc else None

DEVICE_SCALE_FACTOR = 2


@dataclass
class Segment:
    """One frame in the output timeline.

    `img` is an RGBA PIL frame of the clip region. `dur_ms` is how long it shows.
    `xfade_ms` > 0 means: crossfade into this frame from the previous segment's
    frame over that many ms (used for discrete UI state changes like a toggle).
    """

    img: Any  # PIL.Image.Image
    dur_ms: int
    xfade_ms: int = 0


@dataclass
class CaptureResult:
    segments: list[Segment] = field(default_factory=list)
    beats: list[dict[str, Any]] = field(default_factory=list)  # per-beat report
    ok: bool = True
    auth_used: bool = False
    final_url: str = ""
    clip: dict[str, int] | None = None
    error: str | None = None


# ---------------------------------------------------------------------------
# Browser bring-up (mirrors capture_screenshot.capture's launch ladder)
# ---------------------------------------------------------------------------

def _import_playwright():
    try:
        from patchright.sync_api import sync_playwright  # type: ignore

        return sync_playwright, True
    except ImportError:
        from playwright.sync_api import sync_playwright  # type: ignore

        return sync_playwright, False


def _dismiss_age_gate(page) -> str | None:
    """Click through pleasur.ai's 18+ / cookie modal. Returns the matched text."""
    page.wait_for_timeout(1_500)
    for text in KNOWN_MODAL_DISMISS_TEXTS:
        for sel in ("button", "[role='button']", "a"):
            try:
                loc = page.locator(sel, has_text=re.compile(re.escape(text), re.I))
                if not loc.count():
                    continue
                first = loc.first
                first.wait_for(state="visible", timeout=1_500)
                first.click(timeout=2_500, force=True)
                page.wait_for_timeout(900)
                sys.stderr.write(f"info: dismissed modal via text='{text}'\n")
                return text
            except Exception:
                continue
    return None


def _wait_out_cloudflare(page) -> None:
    try:
        title = (page.title() or "").lower()
    except Exception:
        return
    if not any(h in title for h in CF_TITLE_HINTS):
        return
    for _ in range(20):
        page.wait_for_timeout(2_000)
        try:
            title = (page.title() or "").lower()
        except Exception:
            title = ""
        if not any(h in title for h in CF_TITLE_HINTS):
            return


def _resolve_clip(page, clip: dict[str, Any] | None) -> dict[str, int]:
    """Resolve the fixed CSS-px box every frame is clipped to.

    A constant box across all frames is what makes the content (and only the
    content) appear to animate. Computed once after the page settles.
    """
    vp = page.viewport_size or {"width": 1280, "height": 860}
    if not clip:
        return {"x": 0, "y": 0, "width": vp["width"], "height": vp["height"]}
    if "crop" in clip:
        x, y, w, h = clip["crop"]
        return {"x": int(x), "y": int(y), "width": int(w), "height": int(h)}
    if "selector" in clip:
        loc = page.locator(clip["selector"]).first
        try:
            loc.scroll_into_view_if_needed(timeout=4_000)
        except Exception:
            pass
        box = loc.bounding_box()
        if box:
            pad = int(clip.get("pad", 0))
            return {
                "x": max(0, int(box["x"]) - pad),
                "y": max(0, int(box["y"]) - pad),
                "width": int(box["width"]) + pad * 2,
                "height": int(box["height"]) + pad * 2,
            }
    return {"x": 0, "y": 0, "width": vp["width"], "height": vp["height"]}


def _shoot(page, clip: dict[str, int]):
    from PIL import Image

    raw = page.screenshot(clip=clip, animations="disabled")
    return Image.open(io.BytesIO(raw)).convert("RGBA")


# ---------------------------------------------------------------------------
# Action runner
# ---------------------------------------------------------------------------

def _run_action(page, act: dict[str, Any], timeout: int = 8_000) -> None:
    do = act.get("do")
    if do == "wait":
        page.wait_for_timeout(int(act.get("ms", 500)))
    elif do == "click":
        loc = page.locator(act["selector"]).first
        try:
            loc.scroll_into_view_if_needed(timeout=4_000)
        except Exception:
            pass
        loc.click(timeout=int(act.get("timeout", timeout)), force=bool(act.get("force", True)))
    elif do == "hover":
        page.locator(act["selector"]).first.hover(timeout=timeout)
    elif do == "fill":
        page.locator(act["selector"]).first.fill(act.get("text", ""), timeout=timeout)
    elif do == "type":
        loc = page.locator(act["selector"]).first
        try:
            loc.click(timeout=timeout)
        except Exception:
            pass
        loc.type(act.get("text", ""), delay=int(act.get("delay", 55)))
    elif do == "press":
        page.locator(act.get("selector", "body")).first.press(act.get("key", "Enter"))
    elif do == "scroll":
        if act.get("selector"):
            page.locator(act["selector"]).first.scroll_into_view_if_needed()
        else:
            page.evaluate("(y) => window.scrollTo({top: y, behavior: 'auto'})", int(act.get("y", 0)))
    elif do == "wheel":
        # Real wheel event scrolls whatever is under the cursor — robust to apps
        # (like pleasur.ai) that scroll an inner container, not window.
        page.mouse.wheel(0, int(act.get("dy", 42)))
    elif do == "mouse_move":
        page.mouse.move(int(act.get("x", 640)), int(act.get("y", 420)))
    elif do == "eval":
        page.evaluate(act["js"])
    else:
        raise ValueError(f"unknown action: {do!r}")


def _run_actions(page, actions: list[dict[str, Any]], strict: bool) -> list[dict[str, Any]]:
    report = []
    for act in actions or []:
        entry = {"do": act.get("do"), "selector": act.get("selector"), "ok": True}
        try:
            _run_action(page, act)
        except Exception as exc:
            entry["ok"] = False
            entry["error"] = str(exc)[:200]
            report.append(entry)
            if strict and act.get("required", True):
                raise RuntimeError(
                    f"required action failed: {act.get('do')} {act.get('selector')}: {exc}"
                )
        else:
            report.append(entry)
    return report


# ---------------------------------------------------------------------------
# Scene player
# ---------------------------------------------------------------------------

def play(scene: dict[str, Any], *, headed: bool = True, use_auth: bool = False,
         strict: bool = False, max_frames: int = 300) -> CaptureResult:
    """Play a scene and return its frame segments + a per-beat report."""
    sync_playwright, using_patchright = _import_playwright()
    res = CaptureResult()

    vp = scene.get("viewport", {"width": 1280, "height": 900})
    settle_ms = int(scene.get("settle_ms", 1_200))
    default_fps = int(scene.get("fps", 12))

    auth_state = _resolve_auth_state() if use_auth else None
    res.auth_used = bool(auth_state)

    with sync_playwright() as p:
        ctx_kwargs: dict[str, Any] = {
            "viewport": vp,
            "device_scale_factor": DEVICE_SCALE_FACTOR,
            "locale": "en-US",
            "timezone_id": "America/New_York",
        }
        if not using_patchright:
            ctx_kwargs["user_agent"] = DEFAULT_USER_AGENT
        if auth_state:
            ctx_kwargs["storage_state"] = auth_state

        browser = p.chromium.launch(headless=not headed) if using_patchright \
            else p.chromium.launch(headless=not headed, args=["--no-sandbox"])
        context = browser.new_context(**ctx_kwargs)
        if not using_patchright:
            try:
                context.add_init_script(STEALTH_INIT_JS)
            except Exception:
                pass

        page = context.new_page()
        try:
            page.goto(scene["url"], wait_until="domcontentloaded", timeout=45_000)
            page.wait_for_load_state("load", timeout=15_000)
            page.wait_for_timeout(1_500)
            _wait_out_cloudflare(page)
            if scene.get("dismiss_age_gate", True):
                _dismiss_age_gate(page)
            page.wait_for_timeout(settle_ms)
            res.final_url = page.url

            clip = _resolve_clip(page, scene.get("clip"))
            res.clip = clip

            for bi, beat in enumerate(scene.get("beats", [])):
                breport: dict[str, Any] = {"index": bi, "label": beat.get("label", "")}
                try:
                    breport["actions"] = _run_actions(page, beat.get("actions", []), strict)
                except RuntimeError as exc:
                    res.ok = False
                    res.error = str(exc)
                    breport["fatal"] = str(exc)
                    res.beats.append(breport)
                    break

                if "motion" in beat:
                    m = beat["motion"]
                    frames = int(m.get("frames", 24))
                    interval = int(m.get("interval_ms", 1000 // default_fps))
                    each = m.get("each", [])
                    n = 0
                    for _ in range(frames):
                        if each:
                            try:
                                _run_actions(page, each, strict=False)
                            except Exception:
                                pass
                        res.segments.append(_seg_or_stop(page, clip, interval, res, max_frames))
                        if res.segments and res.segments[-1] is None:
                            res.segments.pop()
                            break
                        n += 1
                        page.wait_for_timeout(interval)
                    breport["motion_frames"] = n
                else:
                    shoot = beat.get("shoot", {"hold_ms": 1_200})
                    img = _shoot(page, clip)
                    res.segments.append(
                        Segment(img=img, dur_ms=int(shoot.get("hold_ms", 1_200)),
                                xfade_ms=int(shoot.get("transition_ms", 0)
                                             if shoot.get("transition") == "crossfade" else 0))
                    )
                    breport["keyframe"] = True

                res.beats.append(breport)
                if len(res.segments) >= max_frames:
                    res.beats.append({"warning": f"hit max_frames={max_frames}; truncated"})
                    break
        except Exception as exc:
            res.ok = False
            res.error = f"{type(exc).__name__}: {exc}"
        finally:
            try:
                browser.close()
            except Exception:
                pass

    if not res.segments and res.ok:
        res.ok = False
        res.error = res.error or "no frames captured"
    return res


def _seg_or_stop(page, clip, interval, res: CaptureResult, max_frames: int):
    if len(res.segments) >= max_frames:
        return None
    return Segment(img=_shoot(page, clip), dur_ms=interval, xfade_ms=0)
