"""Annotation engine — capture a web page and draw PIXEL-EXACT (DOM-bbox) annotations.

Captures headed (patchright stealth, passes Cloudflare) under DISPLAY=:99, optionally
dismisses an age-gate/modal, reads each target element's real bounding box from the DOM,
and draws a bright box + arrow + numbered label that pops on dark or light UIs.

Usage:
  DISPLAY=:99 python annotate_screenshot.py --url URL --out out.png \
    --targets '[{"selector":"text=Yearly","note":"Yearly saves 60%"}]' \
    [--dismiss "I am 18 years of age or older"] [--color blue] [--shot-only]
"""
import argparse
import json
from PIL import Image, ImageDraw, ImageFont

try:
    from patchright.sync_api import sync_playwright
except ImportError:
    from playwright.sync_api import sync_playwright

COLORS = {
    "blue": (46, 144, 250, 255),
    "purple": (83, 74, 183, 255),
    "red": (229, 57, 53, 255),
    "orange": (245, 124, 0, 255),
}


def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--targets", default="[]", help='JSON list of {selector, note?}')
    ap.add_argument("--dismiss", default=None, help="exact text of a modal button to click")
    ap.add_argument("--color", default="blue")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--shot-only", action="store_true")
    a = ap.parse_args()

    targets = json.loads(a.targets)
    C = COLORS.get(a.color, COLORS["blue"])
    GLOW = (C[0], C[1], C[2], 80)
    DSF = a.scale
    raw = a.out.rsplit(".", 1)[0] + "_raw.png"

    boxes = []
    with sync_playwright() as p:
        br = p.chromium.launch(headless=False, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
        ctx = br.new_context(viewport={"width": a.width, "height": a.height}, device_scale_factor=DSF)
        pg = ctx.new_page()
        pg.goto(a.url, wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(3500)
        if a.dismiss:
            try:
                pg.get_by_text(a.dismiss, exact=True).first.click(timeout=12000, force=True)
                pg.wait_for_timeout(2500)
            except Exception as e:
                print("dismiss failed:", str(e)[:100])
        pg.wait_for_timeout(1500)
        pg.screenshot(path=raw)
        for t in targets:
            try:
                bb = pg.locator(t["selector"]).first.bounding_box(timeout=4000)
                boxes.append((t, bb))
            except Exception as e:
                boxes.append((t, None))
                print("target not found:", t.get("selector"), str(e)[:60])
        br.close()

    img = Image.open(raw).convert("RGBA")
    if a.shot_only or not targets:
        img.convert("RGB").save(a.out, quality=95)
        print("captured ->", a.out, img.size)
        return

    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    pad, drawn = 12, 0
    for i, (t, bb) in enumerate(boxes, 1):
        if not bb:
            continue
        x0 = (bb["x"] - pad) * DSF
        y0 = (bb["y"] - pad) * DSF
        x1 = (bb["x"] + bb["width"] + pad) * DSF
        y1 = (bb["y"] + bb["height"] + pad) * DSF
        d.rounded_rectangle([x0 - 6, y0 - 6, x1 + 6, y1 + 6], radius=22, outline=GLOW, width=18)
        d.rounded_rectangle([x0, y0, x1, y1], radius=16, outline=C, width=8)
        note = t.get("note") or ""
        txt = (str(i) + "   " + note) if note else str(i)
        f = font(30)
        tb = d.textbbox((0, 0), txt, font=f)
        tw, th = tb[2] - tb[0], tb[3] - tb[1]
        lx = (x0 + x1) // 2
        ly = max(y0 - 84, 60)
        d.rounded_rectangle([lx - tw // 2 - 24, ly - th // 2 - 15, lx + tw // 2 + 24, ly + th // 2 + 15], radius=18, fill=C)
        d.text((lx, ly), txt, fill=(255, 255, 255, 255), font=f, anchor="mm")
        d.line([lx, ly + th // 2 + 15, lx, y0 - 2], fill=C, width=6)
        ah = 16
        d.polygon([(lx - ah, y0 - ah - 2), (lx + ah, y0 - ah - 2), (lx, y0 + 4)], fill=C)
        drawn += 1
    Image.alpha_composite(img, ov).convert("RGB").save(a.out, quality=95)
    print("DREW", drawn, "annotations ->", a.out)


if __name__ == "__main__":
    main()
