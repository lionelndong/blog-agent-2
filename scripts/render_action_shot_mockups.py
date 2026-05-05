#!/usr/bin/env python3
"""Generate clean mockup PNGs of the Pleasur.AI Companion Creator steps based
on the navigation agent's verified UI observations. These fill the [VISUAL]
action-shot slots in the preview when the real captures live on a different
filesystem. Real PNGs overwrite these once sync_captures_from_vps.sh runs.

Usage:
    python scripts/render_action_shot_mockups.py
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("error: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SLUG = "build-a-girlfriend-body"
OUT_DIR = ROOT / "content-pipeline" / "images" / SLUG

W, H = 1440, 900
BG = (10, 10, 14)
PANEL = (22, 22, 28)
CARD = (38, 40, 48)
CARD_HOVER = (52, 56, 70)
TEXT = (238, 240, 245)
TEXT_DIM = (160, 162, 170)
ACCENT = (147, 119, 240)
ACCENT_DIM = (90, 72, 160)

WIZARD_STEPS = ["Style", "Identity", "Body", "Outfit", "Voice", "Backstory"]


def _font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _rounded_rect(draw: ImageDraw.ImageDraw, xy, radius=12, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle((x0, y0, x1, y1), radius=radius, fill=fill, outline=outline, width=width)


def _draw_chrome(draw: ImageDraw.ImageDraw, current_step: int) -> None:
    f_logo = _font(22, bold=True)
    f_step = _font(14)
    f_step_active = _font(14, bold=True)

    draw.rectangle((0, 0, W, 64), fill=PANEL)
    draw.text((40, 22), "Pleasur.AI · Companion Creator", fill=TEXT, font=f_logo)

    # Wizard progress bar
    x = 40
    y = 96
    for i, step in enumerate(WIZARD_STEPS):
        active = i == current_step
        completed = i < current_step
        radius = 14
        if completed:
            color = ACCENT_DIM
        elif active:
            color = ACCENT
        else:
            color = CARD
        draw.ellipse((x, y, x + 28, y + 28), fill=color)
        text_color = TEXT if (active or completed) else TEXT_DIM
        font = f_step_active if active else f_step
        draw.text((x + 36, y + 6), step, fill=text_color, font=font)
        bbox = draw.textbbox((x + 36, y + 6), step, font=font)
        x = bbox[2] + 28
        if i < len(WIZARD_STEPS) - 1:
            draw.line((x, y + 14, x + 16, y + 14), fill=CARD, width=2)
            x += 24


def _card(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    w: int,
    h: int,
    label: str,
    sublabel: str = "",
    selected: bool = False,
) -> None:
    fill = CARD_HOVER if selected else CARD
    outline = ACCENT if selected else None
    width = 2 if selected else 0
    _rounded_rect(draw, (x, y, x + w, y + h), radius=14, fill=fill, outline=outline, width=width)
    f_label = _font(18, bold=True)
    f_sub = _font(12)
    # vertical center the label block
    text_h = 22 + (16 if sublabel else 0)
    ty = y + (h - text_h) // 2
    draw.text((x + 16, ty), label, fill=TEXT, font=f_label)
    if sublabel:
        draw.text((x + 16, ty + 24), sublabel, fill=TEXT_DIM, font=f_sub)


def _section_label(draw: ImageDraw.ImageDraw, x: int, y: int, text: str) -> None:
    f = _font(14, bold=True)
    draw.text((x, y), text.upper(), fill=TEXT_DIM, font=f)


def _watermark(draw: ImageDraw.ImageDraw, text: str) -> None:
    f = _font(11)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    pad = 8
    x0, y0 = W - tw - pad * 2 - 24, H - 32
    x1, y1 = x0 + tw + pad * 2, y0 + 22
    _rounded_rect(draw, (x0, y0, x1, y1), radius=8, fill=(36, 28, 60))
    draw.text((x0 + pad, y0 + 4), text, fill=(200, 188, 240), font=f)


def render_ethnicity_step(out: Path) -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    _draw_chrome(draw, current_step=1)

    f_h = _font(28, bold=True)
    f_sub = _font(15)
    draw.text((40, 160), "Choose her ethnicity", fill=TEXT, font=f_h)
    draw.text(
        (40, 196),
        "Pick the preset that matches your archetype, not the one that catches your eye.",
        fill=TEXT_DIM,
        font=f_sub,
    )

    # Five ethnicity cards
    presets = ["Caucasian", "Asian", "Latina", "Black / Afro", "Arab"]
    card_w, card_h, gap = 240, 220, 16
    total = len(presets) * card_w + (len(presets) - 1) * gap
    start_x = (W - total) // 2
    y = 250
    for i, name in enumerate(presets):
        x = start_x + i * (card_w + gap)
        _card(draw, x, y, card_w, card_h, name, sublabel="preset", selected=(i == 0))

    _section_label(draw, 40, 510, "Skin tone")
    swatch_colors = [(245, 220, 198), (228, 192, 154), (205, 158, 110), (160, 105, 70), (110, 65, 38), (70, 38, 22)]
    sx = 40
    for c in swatch_colors:
        draw.ellipse((sx, 540, sx + 44, 584), fill=c, outline=ACCENT_DIM if c == swatch_colors[1] else None, width=2)
        sx += 56

    _section_label(draw, 40, 620, "Age presentation")
    age_cards = ["early 20s", "mid 20s", "late 20s", "30s"]
    ax = 40
    for i, age in enumerate(age_cards):
        _card(draw, ax, 650, 180, 80, age, sublabel="adult range", selected=(i == 1))
        ax += 196

    # Continue button
    _rounded_rect(draw, (W - 200, H - 96, W - 40, H - 56), radius=20, fill=ACCENT)
    f_btn = _font(15, bold=True)
    draw.text((W - 168, H - 88), "Continue  →", fill=TEXT, font=f_btn)

    _watermark(draw, "MOCKUP · real screenshot pending VPS sync")
    img.save(out, "PNG", optimize=True)


def render_body_step(out: Path) -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    _draw_chrome(draw, current_step=2)

    f_h = _font(28, bold=True)
    f_sub = _font(15)
    draw.text((40, 160), "Body, breast, and butt", fill=TEXT, font=f_h)
    draw.text(
        (40, 196),
        "Pleasur uses preset cards here, not sliders. Match the size card to your body-type card.",
        fill=TEXT_DIM,
        font=f_sub,
    )

    _section_label(draw, 40, 240, "Body type")
    body_types = ["Slim", "Athletic", "Voluptuous", "Curvy"]
    card_w, card_h, gap = 304, 140, 16
    total = len(body_types) * card_w + (len(body_types) - 1) * gap
    start_x = (W - total) // 2
    y = 270
    for i, name in enumerate(body_types):
        x = start_x + i * (card_w + gap)
        _card(draw, x, y, card_w, card_h, name, sublabel="preset", selected=(i == 1))

    _section_label(draw, 40, 440, "Breast size")
    sizes = ["Small", "Medium", "Large", "Athletic"]
    card_w2, card_h2, gap2 = 240, 96, 16
    total2 = len(sizes) * card_w2 + (len(sizes) - 1) * gap2
    start_x2 = (W - total2) // 2
    y2 = 470
    for i, name in enumerate(sizes):
        x = start_x2 + i * (card_w2 + gap2)
        _card(draw, x, y2, card_w2, card_h2, name, selected=(i == 1))

    _section_label(draw, 40, 590, "Butt size")
    butt_sizes = ["Small", "Medium", "Large", "Athletic"]
    y3 = 620
    for i, name in enumerate(butt_sizes):
        x = start_x2 + i * (card_w2 + gap2)
        _card(draw, x, y3, card_w2, card_h2, name, selected=(i == 2))

    # Continue button
    _rounded_rect(draw, (W - 200, H - 96, W - 40, H - 56), radius=20, fill=ACCENT)
    f_btn = _font(15, bold=True)
    draw.text((W - 168, H - 88), "Continue  →", fill=TEXT, font=f_btn)

    _watermark(draw, "MOCKUP · real screenshot pending VPS sync")
    img.save(out, "PNG", optimize=True)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out1 = OUT_DIR / "action-2-companion-creator-ethnicity.png"
    out2 = OUT_DIR / "action-3-companion-creator-body.png"
    render_ethnicity_step(out1)
    render_body_step(out2)
    print(f"wrote {out1.relative_to(ROOT)} ({out1.stat().st_size:,} bytes)")
    print(f"wrote {out2.relative_to(ROOT)} ({out2.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
