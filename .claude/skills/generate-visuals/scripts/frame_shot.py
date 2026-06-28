#!/usr/bin/env python3
"""Wrap a raw product screenshot in an on-brand frame + polish (LOCKED aesthetic 2026-06-28).

This is the polish layer for PRODUCT ACTION-SHOTS. It takes a raw retina capture (from
capture_screenshot.py / action_shot.py) and renders it onto the Pleasur.AI brand canvas with a
soft device/browser frame, big-soft drop shadow, optional caption, and the real composited logo —
matching `render_chart_web.py` (light #F7F8FA canvas, white rounded card, Geist + IBM Plex,
Pleasur.ai mark). A dark app screenshot floating on the light canvas reads as premium SaaS UI.

Framing is rendered as an HTML/CSS document screenshotted headless with patchright (same trick the
chart engine uses) — CSS gives soft shadows + rounded masking that PIL can't match. No network is
required except optional Google-Fonts (graceful fallback to system fonts).

Usage:
  python frame_shot.py --in raw.png --out final.png [--frame plain|browser|device]
     [--caption "A chat with Aria on Pleasur.AI"] [--url-bar "pleasur.ai/chat"]
     [--accent "#2E90FA"] [--max-width 1180] [--no-logo] [--bg "#F7F8FA"]

`frame`:
  plain   — rounded corners + soft shadow on the brand canvas (the versatile hero treatment).
  browser — a clean macOS-style browser chrome (3 dots + URL pill) above the shot (desktop pages).
  device  — a soft phone bezel around a portrait shot (chat / call — mobile-first aspirational).
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_LOGO = SCRIPT_DIR / "pleasurai-logo.png"

# Brand tokens — kept in lockstep with render_chart_web.py
BG = "#F7F8FA"
FONT = "'Geist', system-ui, -apple-system, 'Segoe UI', sans-serif"          # blog body font
TITLE_FONT = "'IBM Plex Sans', 'Geist', system-ui, sans-serif"              # blog heading font
ACCENT = "#2E90FA"
CAPTION_COLOR = "#6B7280"

FONTS_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Geist:wght@400;500;600&family=IBM+Plex+Sans:wght@600&display=swap');"
)


def _data_uri(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def _img_dims(path: Path) -> tuple[int, int]:
    from PIL import Image
    with Image.open(path) as im:
        return im.size


def _logo_html(logo_path: Path | None) -> str:
    if logo_path and logo_path.exists():
        try:
            return '<img class="logo" src="%s" alt="Pleasur.ai">' % _data_uri(logo_path)
        except Exception:
            pass
    # Text fallback keeps the wordmark on-brand even if the asset is missing
    return '<span class="logo-txt">Pleasur<span style="color:%s">.ai</span></span>' % ACCENT


def _shot_block(frame: str, shot_uri: str, url_bar: str, accent: str) -> str:
    """The framed screenshot itself (no caption/logo)."""
    if frame == "browser":
        pill = url_bar or "pleasur.ai"
        return (
            '<div class="shot browser">'
            '<div class="bar">'
            '<span class="dots"><i style="background:#FF5F57"></i>'
            '<i style="background:#FEBC2E"></i><i style="background:#28C840"></i></span>'
            '<div class="pill"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" '
            'style="margin-right:6px;vertical-align:-1px"><path d="M6 10V8a6 6 0 1112 0v2" '
            'stroke="#9AA2AE" stroke-width="2" stroke-linecap="round"/><rect x="4" y="10" '
            'width="16" height="10" rx="2.5" fill="#C8CED8"/></svg>' + pill + "</div>"
            '<span class="dots ghost"><i></i><i></i><i></i></span>'
            "</div>"
            '<img class="screen" src="' + shot_uri + '" alt="Pleasur.AI screen">'
            "</div>"
        )
    if frame == "device":
        return (
            '<div class="shot device">'
            '<div class="notch"></div>'
            '<img class="screen" src="' + shot_uri + '" alt="Pleasur.AI screen">'
            "</div>"
        )
    # plain
    return (
        '<div class="shot plain">'
        '<img class="screen" src="' + shot_uri + '" alt="Pleasur.AI screen">'
        "</div>"
    )


def build_html(
    shot_uri: str,
    *,
    frame: str,
    caption: str,
    url_bar: str,
    accent: str,
    bg: str,
    max_width: int,
    logo_html: str,
    portrait: bool,
) -> str:
    pad = 84 if not portrait else 64
    device_radius = 46
    # CSS uses a token-replace template so we never fight Python %/format brace escaping.
    css = """
*{box-sizing:border-box;margin:0;padding:0}
__FONTS__
body{font-family:__FONT__;background:__BG__}
#wrap{display:inline-block;background:__BG__;padding:__PAD__px}
#stage{width:__MAXW__px;display:flex;flex-direction:column;align-items:center}

/* plain */
.shot.plain{width:100%;border-radius:18px;overflow:hidden;
  box-shadow:0 2px 4px rgba(20,30,50,.04), 0 34px 80px -12px rgba(20,30,50,.30);
  outline:1px solid rgba(20,30,50,.06);outline-offset:-1px;background:#0b0b0d}
.shot.plain .screen{display:block;width:100%}

/* browser */
.shot.browser{width:100%;border-radius:16px;overflow:hidden;
  box-shadow:0 2px 4px rgba(20,30,50,.04), 0 34px 80px -12px rgba(20,30,50,.30);
  outline:1px solid rgba(20,30,50,.07);outline-offset:-1px;background:#fff}
.shot.browser .bar{display:flex;align-items:center;gap:14px;height:46px;padding:0 18px;
  background:#F4F6F9;border-bottom:1px solid #E7EBF1}
.shot.browser .dots{display:inline-flex;gap:8px;align-items:center;flex:0 0 auto;width:54px}
.shot.browser .dots i{width:12px;height:12px;border-radius:50%;display:inline-block}
.shot.browser .dots.ghost{visibility:hidden}
.shot.browser .pill{flex:1;max-width:560px;margin:0 auto;height:28px;line-height:28px;
  background:#fff;border:1px solid #E7EBF1;border-radius:8px;text-align:center;
  font-size:13px;color:#7A828F;font-weight:500;overflow:hidden;white-space:nowrap}
.shot.browser .screen{display:block;width:100%}

/* device (phone) */
.shot.device{position:relative;width:100%;border-radius:__DEVR__px;overflow:hidden;
  background:#000;padding:11px;
  box-shadow:0 2px 4px rgba(20,30,50,.05), 0 40px 90px -14px rgba(20,30,50,.38);
  outline:1px solid rgba(20,30,50,.10);outline-offset:-1px}
.shot.device .screen{display:block;width:100%;border-radius:__DEVRIN__px}
.shot.device .notch{position:absolute;top:11px;left:50%;transform:translateX(-50%);
  width:34%;max-width:170px;height:24px;background:#000;border-radius:0 0 16px 16px;z-index:2}

.cap{margin-top:26px;text-align:center;font-size:16px;line-height:1.5;color:__CAPCOL__;
  font-weight:450;max-width:88%}
.foot{margin-top:17px;display:flex;align-items:center;justify-content:center;opacity:.9}
.logo{height:18px;display:block}
.logo-txt{font-family:__TITLEFONT__;font-weight:600;font-size:14px;color:#2D2D2D}
"""
    css = (
        css.replace("__FONTS__", FONTS_IMPORT)
        .replace("__FONT__", FONT)
        .replace("__TITLEFONT__", TITLE_FONT)
        .replace("__BG__", bg)
        .replace("__PAD__", str(pad))
        .replace("__MAXW__", str(max_width))
        .replace("__DEVRIN__", str(device_radius - 8))
        .replace("__DEVR__", str(device_radius))
        .replace("__CAPCOL__", CAPTION_COLOR)
    )

    shot = _shot_block(frame, shot_uri, url_bar, accent)
    cap_html = ('<div class="cap">%s</div>' % caption) if caption else ""
    foot_html = ('<div class="foot">%s</div>' % logo_html) if logo_html else ""

    return (
        '<!doctype html><html><head><meta charset="utf-8"><style>'
        + css
        + "</style></head><body><div id=\"wrap\"><div id=\"stage\">"
        + shot
        + cap_html
        + foot_html
        + "</div></div></body></html>"
    )


def frame(
    in_path: Path,
    out_path: Path,
    *,
    frame: str = "plain",
    caption: str = "",
    url_bar: str = "",
    accent: str = ACCENT,
    bg: str = BG,
    max_width: int = 1180,
    logo: bool = True,
    logo_path: Path | None = None,
) -> dict:
    if not in_path.exists():
        return {"status": "failed", "reason": "input_missing", "in": str(in_path)}
    try:
        w, h = _img_dims(in_path)
    except Exception as exc:
        return {"status": "failed", "reason": "input_unreadable", "error": str(exc)}
    portrait = h > w
    shot_uri = _data_uri(in_path)
    logo_html = _logo_html(logo_path or DEFAULT_LOGO) if logo else ""
    # Phones look right narrower; landscape app shots want the full width.
    if frame == "device" and max_width > 480:
        max_width = 430
    html = build_html(
        shot_uri,
        frame=frame,
        caption=caption,
        url_bar=url_bar,
        accent=accent,
        bg=bg,
        max_width=max_width,
        logo_html=logo_html,
        portrait=portrait,
    )

    try:
        from patchright.sync_api import sync_playwright
    except ImportError:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            return {"status": "failed", "reason": "no_browser_engine",
                    "hint": "pip install patchright && patchright install chromium"}

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--no-sandbox"])
        pg = b.new_context(viewport={"width": 1600, "height": 1200},
                           device_scale_factor=2).new_page()
        pg.set_content(html, wait_until="networkidle")
        try:
            pg.wait_for_timeout(600)  # let fonts settle
        except Exception:
            pass
        pg.locator("#wrap").screenshot(path=str(out_path))
        b.close()

    try:
        fw, fh = _img_dims(out_path)
    except Exception:
        fw = fh = 0
    return {
        "status": "framed",
        "path": str(out_path),
        "frame": frame,
        "src_dims": [w, h],
        "out_dims": [fw, fh],
        "portrait": portrait,
        "caption": caption or None,
        "logo": bool(logo),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Frame a product screenshot on the Pleasur.AI brand canvas.")
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--frame", default="plain", choices=["plain", "browser", "device"])
    ap.add_argument("--caption", default="")
    ap.add_argument("--url-bar", dest="url_bar", default="")
    ap.add_argument("--accent", default=ACCENT)
    ap.add_argument("--bg", default=BG)
    ap.add_argument("--max-width", dest="max_width", type=int, default=1180)
    ap.add_argument("--no-logo", dest="logo", action="store_false")
    ap.add_argument("--logo", dest="logo_path", default=None, help="override logo asset path")
    a = ap.parse_args()
    res = frame(
        Path(a.inp).resolve(),
        Path(a.out).resolve(),
        frame=a.frame,
        caption=a.caption,
        url_bar=a.url_bar,
        accent=a.accent,
        bg=a.bg,
        max_width=a.max_width,
        logo=a.logo,
        logo_path=Path(a.logo_path).resolve() if a.logo_path else None,
    )
    json.dump(res, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if res.get("status") == "framed" else 1


if __name__ == "__main__":
    sys.exit(main())
