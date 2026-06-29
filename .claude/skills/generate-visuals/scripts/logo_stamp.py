#!/usr/bin/env python3
"""Stamp the REAL Pleasur.ai logo onto a cover as a small white rounded chip (always legible on any
background — solves the blue-".ai"-on-blue problem). The logo itself is never AI-drawn.

Usage: python logo_stamp.py --in raw.png --out final.png [--logo pleasurai-logo.png] [--frac 0.17] [--margin 0.045]
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

SCRIPT_DIR = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--logo", default=str(SCRIPT_DIR / "pleasurai-logo.png"))  # charcoal "Pleasur." + blue ".ai"
    ap.add_argument("--frac", type=float, default=0.16, help="chip width as a fraction of image width")
    ap.add_argument("--margin", type=float, default=0.045)
    ap.add_argument("--width", type=int, default=1600, help="resize illustration to the cover spec first")
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--no-logo", dest="no_logo", action="store_true",
                    help="just resize to spec, no logo chip (covers ship logo-free per operator)")
    a = ap.parse_args()

    img = Image.open(a.inp).convert("RGBA")
    if a.width and a.height and img.size != (a.width, a.height):
        img = img.resize((a.width, a.height), Image.LANCZOS)  # flat vector art upscales cleanly
    if a.no_logo:
        img.convert("RGB").save(a.out)
        print("SAVED", a.out, img.size, "| no logo")
        return
    IW, IH = img.size
    logo = Image.open(a.logo).convert("RGBA")
    lw = int(IW * a.frac)
    logo = logo.resize((lw, max(1, int(logo.size[1] * lw / logo.size[0]))), Image.LANCZOS)

    padx, pady = int(lw * 0.16), int(lw * 0.11)
    cw, ch = logo.size[0] + 2 * padx, logo.size[1] + 2 * pady
    rad = int(ch * 0.34)

    # soft shadow
    shadow = Image.new("RGBA", (cw + 40, ch + 40), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([20, 24, 20 + cw, 24 + ch], radius=rad, fill=(15, 25, 45, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(9))

    # white chip
    chip = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    cd = ImageDraw.Draw(chip)
    cd.rounded_rectangle([0, 0, cw - 1, ch - 1], radius=rad, fill=(255, 255, 255, 244))
    chip.alpha_composite(logo, (padx, pady))

    m = int(IW * a.margin)
    pos = (IW - cw - m, IH - ch - m)
    img.alpha_composite(shadow, (pos[0] - 20, pos[1] - 24))
    img.alpha_composite(chip, pos)
    img.convert("RGB").save(a.out)
    print("SAVED", a.out, img.size, "| chip", (cw, ch))


if __name__ == "__main__":
    main()
