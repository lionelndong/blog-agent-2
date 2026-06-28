#!/usr/bin/env python3
"""Polish stage for the animated-demo engine (pure PIL, no browser).

Two jobs:
  1. Synthesize crossfade tweens between discrete keyframes (so a UI toggle
     dissolves instead of cutting).
  2. Wrap the captured content in a soft, on-brand "browser window" frame —
     same palette / radius / shadow / real-logo family as the chart card in
     render_chart_web.py — so the demo reads as part of the Pleasur.ai visual
     system rather than a raw screen grab.

The frame chrome is built ONCE per render (a static "stage" with a hole); each
animated frame is pasted into the hole. That keeps the chrome perfectly steady.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SCRIPT_DIR = Path(__file__).resolve().parent
LOGO_PATH = SCRIPT_DIR / "pleasurai-logo.png"

# Brand tokens — kept in sync with render_chart_web.py's card.
CANVAS = (247, 248, 250, 255)        # #F7F8FA
CARD = (255, 255, 255, 255)          # #FFFFFF
BORDER = (237, 240, 244, 255)        # #EDF0F4
BAR_BG = (252, 253, 254, 255)        # near-white top bar
PILL_BG = (241, 243, 245, 255)       # #F1F3F5 url pill
URL_TEXT = (122, 130, 143, 255)      # #7A828F
DOTS = ((255, 95, 87), (254, 188, 46), (40, 200, 64))  # soft traffic lights


def _font(size: int):
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/Library/Fonts/Arial.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


# ---------------------------------------------------------------------------
# Crossfade
# ---------------------------------------------------------------------------

def crossfade(a: Image.Image, b: Image.Image, n: int) -> list[Image.Image]:
    """n intermediate frames blending a -> b (exclusive of both endpoints)."""
    if n <= 0:
        return []
    if a.size != b.size:
        b = b.resize(a.size, Image.LANCZOS)
    a = a.convert("RGBA")
    b = b.convert("RGBA")
    out = []
    for i in range(1, n + 1):
        alpha = i / (n + 1)
        out.append(Image.blend(a, b, alpha))
    return out


# ---------------------------------------------------------------------------
# Rounded-corner helpers
# ---------------------------------------------------------------------------

def _rounded_mask(w: int, h: int, r: int) -> Image.Image:
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    return m


def _fade_bottom(img: Image.Image, px: int, color: tuple[int, int, int]) -> Image.Image:
    """Fade the bottom `px` rows into `color` (the page's own bg).

    The captured region rarely ends on a natural boundary (a UI list runs past
    the clip), and the two states of a toggle have different heights — so any
    fixed crop cuts a row mid-line. Fading the bottom into the product's own
    dark background makes the overflow read as intentional, like the screenshots
    in Linear / Vercel docs.
    """
    if px <= 1:
        return img.convert("RGBA")
    img = img.convert("RGBA")
    w, h = img.size
    grad = Image.linear_gradient("L").resize((w, px))  # 0 (top) -> 255 (bottom)
    overlay = Image.new("RGBA", (w, px), color + (0,))
    overlay.putalpha(grad)
    img.alpha_composite(overlay, (0, h - px))
    return img


def _round_bottom_only(img: Image.Image, r: int) -> Image.Image:
    """Apply an alpha mask that rounds only the bottom two corners."""
    w, h = img.size
    mask = _rounded_mask(w, h, r)
    d = ImageDraw.Draw(mask)
    d.rectangle([0, 0, w, r], fill=255)  # square off the top edge
    img = img.convert("RGBA")
    img.putalpha(mask)
    return img


# ---------------------------------------------------------------------------
# Browser frame
# ---------------------------------------------------------------------------

def _load_logo(target_w: int) -> Image.Image | None:
    try:
        logo = Image.open(LOGO_PATH).convert("RGBA")
    except Exception:
        return None
    # Bundled asset is already the light-canvas variant (charcoal + blue);
    # key out an opaque background if present so it sits cleanly on #F7F8FA.
    px = logo.getpixel((0, 0))
    if len(px) == 4 and px[3] > 250:
        bg = px[:3]
        logo.putdata([
            (r, g, b, 0) if (abs(r - bg[0]) < 28 and abs(g - bg[1]) < 28 and abs(b - bg[2]) < 28)
            else (r, g, b, a)
            for (r, g, b, a) in logo.getdata()
        ])
    scale = target_w / logo.width
    return logo.resize((target_w, max(1, int(logo.height * scale))), Image.LANCZOS)


def build_stage(content_w: int, content_h: int, url_text: str,
                caption: str = "") -> tuple[Image.Image, tuple[int, int], int]:
    """Build the static chrome. Returns (stage_rgba, content_xy, content_radius)."""
    pad = 60
    bar_h = 54
    radius = 22
    foot = 64 if (caption or True) else 36

    win_w, win_h = content_w, bar_h + content_h
    cw = win_w + pad * 2
    ch = win_h + pad * 2 + foot
    stage = Image.new("RGBA", (cw, ch), CANVAS)

    win_xy = (pad, pad)
    # Drop shadow: blurred dark rounded rect behind the window.
    shadow = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        [win_xy[0], win_xy[1] + 10, win_xy[0] + win_w, win_xy[1] + win_h + 10],
        radius=radius, fill=(20, 30, 50, 46),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    stage.alpha_composite(shadow)

    # White window card + 1px border.
    card = Image.new("RGBA", (win_w, win_h), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([0, 0, win_w - 1, win_h - 1], radius=radius, fill=CARD,
                         outline=BORDER, width=1)
    stage.alpha_composite(card, win_xy)

    # Top bar: separator + traffic lights + url pill.
    d = ImageDraw.Draw(stage)
    bx, by = win_xy
    d.line([(bx + 1, by + bar_h), (bx + win_w - 2, by + bar_h)], fill=BORDER, width=1)
    cy = by + bar_h // 2
    dot_r = 6
    for i, col in enumerate(DOTS):
        cx = bx + 24 + i * 22
        d.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=col + (255,))

    pill_l = bx + 110
    pill_r = bx + win_w - 24
    pill_h = 30
    d.rounded_rectangle([pill_l, cy - pill_h // 2, pill_r, cy + pill_h // 2],
                        radius=pill_h // 2, fill=PILL_BG)
    f = _font(15)
    # tiny lock glyph
    lock_x = pill_l + 16
    d.rounded_rectangle([lock_x, cy - 5, lock_x + 9, cy + 4], radius=2, fill=URL_TEXT)
    d.rectangle([lock_x + 2, cy - 8, lock_x + 7, cy - 4], outline=URL_TEXT, width=2)
    d.text((lock_x + 18, cy), url_text, font=f, fill=URL_TEXT, anchor="lm")

    # Footer: caption (left) + real logo (right).
    foot_cy = win_xy[1] + win_h + foot // 2 + 4
    if caption:
        d.text((pad + 4, foot_cy), caption, font=_font(16), fill=(122, 130, 143, 255), anchor="lm")
    logo = _load_logo(118)
    if logo is not None:
        stage.alpha_composite(logo, (cw - pad - logo.width, foot_cy - logo.height // 2))
    else:
        d.text((cw - pad, foot_cy), "Pleasur.ai", font=_font(18), fill=(45, 45, 45, 255), anchor="rm")

    content_xy = (pad, pad + bar_h)
    return stage, content_xy, radius


def compose_frames(frames: list[Image.Image], url_text: str, caption: str = "",
                   inner_w: int = 980, fade_bottom_px: int = 48) -> list[Image.Image]:
    """Wrap every frame in the same browser stage. Returns composited RGB frames."""
    if not frames:
        return []
    # Normalize content to a common inner width.
    base = frames[0].convert("RGBA")
    scale = inner_w / base.width
    content_w = inner_w
    content_h = max(1, int(base.height * scale))

    # Sample the page's own bottom-bg colour so the fade is seamless.
    bg = base.resize((content_w, content_h), Image.LANCZOS).getpixel((6, content_h - 4))[:3]

    stage, (cx, cy), radius = build_stage(content_w, content_h, url_text, caption)
    out = []
    for fr in frames:
        c = fr.convert("RGBA").resize((content_w, content_h), Image.LANCZOS)
        c = _fade_bottom(c, fade_bottom_px, bg)
        c = _round_bottom_only(c, radius)
        frame = stage.copy()
        frame.alpha_composite(c, (cx, cy))
        out.append(frame.convert("RGB"))
    return out


# ---------------------------------------------------------------------------
# Sizing
# ---------------------------------------------------------------------------

def fit(frames: list[Image.Image], max_w: int) -> list[Image.Image]:
    """Downscale to max_w (if wider) and force even dimensions (mp4/yuv420p)."""
    if not frames:
        return frames
    w, h = frames[0].size
    tw = min(max_w, w)
    th = int(h * (tw / w))
    tw -= tw % 2
    th -= th % 2
    if (tw, th) == (w, h):
        return [f.convert("RGB") for f in frames]
    return [f.convert("RGB").resize((tw, th), Image.LANCZOS) for f in frames]
