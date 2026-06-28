"""Annotation engine — capture a web page and draw PIXEL-EXACT (DOM-bbox) annotations.

Captures headed (patchright stealth, passes Cloudflare) under DISPLAY=:99, optionally
dismisses an age-gate/modal, reads each target element's real bounding box from the DOM,
and draws annotations that pop on dark or light UIs.

Per-target "kind":
  "box"       (default) bright rounded box + glow + numbered label with arrow
  "highlight"           semi-transparent colored fill over the element (+ optional label)
  "zoom"                magnified loupe of the element in a corner + connector line

Usage:
  DISPLAY=:99 python annotate_screenshot.py --url URL --out out.png \
    --targets '[{"selector":"text=5,000","kind":"zoom","corner":"br","note":"5,000 coins"},
                {"selector":"text=Yearly","kind":"highlight","note":"save 60%"}]' \
    [--dismiss "I am 18 years of age or older"] [--color blue] [--shot-only]
Target fields: selector (req), kind?, note?, color?, corner? (zoom: br|bl|tr|tl).
"""
import argparse
import json
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

try:
    from patchright.sync_api import sync_playwright
except ImportError:
    from playwright.sync_api import sync_playwright

COLORS = {
    "blue": (46, 144, 250, 255),
    "purple": (83, 74, 183, 255),
    "red": (229, 57, 53, 255),
    "orange": (245, 124, 0, 255),
    "green": (34, 178, 118, 255),
}


def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def num_label(d, cx, anchor_top_y, text, C, sz=30):
    """Numbered pill above the element with a connector + arrow pointing down to it."""
    f = font(sz)
    tb = d.textbbox((0, 0), text, font=f)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    ly = max(anchor_top_y - 84, 60)
    d.rounded_rectangle([cx - tw // 2 - 24, ly - th // 2 - 15, cx + tw // 2 + 24, ly + th // 2 + 15], radius=18, fill=C)
    d.text((cx, ly), text, fill=(255, 255, 255, 255), font=f, anchor="mm")
    d.line([cx, ly + th // 2 + 15, cx, anchor_top_y - 2], fill=C, width=6)
    ah = 16
    d.polygon([(cx - ah, anchor_top_y - ah - 2), (cx + ah, anchor_top_y - ah - 2), (cx, anchor_top_y + 4)], fill=C)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--targets", default="[]", help='JSON list of {selector, kind?, note?, color?, corner?}')
    ap.add_argument("--dismiss", default=None, help="exact text of a modal button to click")
    ap.add_argument("--color", default="blue")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--shot-only", action="store_true")
    ap.add_argument("--strict", action="store_true", help="exit non-zero if any target not found")
    a = ap.parse_args()

    targets = json.loads(a.targets)
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
    drawn = 0
    zooms = []
    for i, (t, bb) in enumerate(boxes, 1):
        if not bb:
            continue
        C = COLORS.get(t.get("color"), COLORS.get(a.color, COLORS["blue"]))
        GLOW = (C[0], C[1], C[2], 80)
        kind = t.get("kind", "box")
        pad = t.get("pad", 28 if kind == "zoom" else 12)
        x0 = (bb["x"] - pad) * DSF
        y0 = (bb["y"] - pad) * DSF
        x1 = (bb["x"] + bb["width"] + pad) * DSF
        y1 = (bb["y"] + bb["height"] + pad) * DSF
        note = t.get("note") or ""
        lbl = (str(i) + "   " + note) if note else str(i)
        if kind == "highlight":
            d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=(C[0], C[1], C[2], 66), outline=C, width=5)
            num_label(d, (x0 + x1) // 2, y0, lbl, C)
        elif kind == "zoom":
            d.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=(C[0], C[1], C[2], 40), outline=C, width=6)
            zooms.append((i, t, C, (int(max(0, x0)), int(max(0, y0)), int(x1), int(y1))))
        else:  # box
            d.rounded_rectangle([x0 - 6, y0 - 6, x1 + 6, y1 + 6], radius=22, outline=GLOW, width=18)
            d.rounded_rectangle([x0, y0, x1, y1], radius=16, outline=C, width=8)
            num_label(d, (x0 + x1) // 2, y0, lbl, C)
        drawn += 1

    base = Image.alpha_composite(img, ov)
    IW, IH = base.size
    d2 = ImageDraw.Draw(base)
    for (i, t, C, (sx0, sy0, sx1, sy1)) in zooms:
        sx1 = min(IW, sx1); sy1 = min(IH, sy1)
        crop = img.crop((sx0, sy0, sx1, sy1))
        cw, ch = crop.size
        if cw < 6 or ch < 6:
            continue
        factor = min(2.8, max(1.6, (IW * 0.40) / cw))
        iw, ih = int(cw * factor), int(ch * factor)
        if ih > IH * 0.45:
            f2 = (IH * 0.45) / ih
            iw, ih = int(iw * f2), int(ih * f2)
        ins = crop.resize((iw, ih), Image.LANCZOS)
        corner = t.get("corner", "br")
        m = int(IW * 0.03)
        ix0, iy0 = (IW - iw - m if corner in ("br", "tr") else m), (IH - ih - m if corner in ("br", "bl") else m)
        ix1, iy1 = ix0 + iw, iy0 + ih
        scx, scy = (sx0 + sx1) // 2, (sy0 + sy1) // 2
        d2.line([scx, scy, (ix0 + ix1) // 2, (iy0 + iy1) // 2], fill=(C[0], C[1], C[2], 170), width=5)
        sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([ix0 + 7, iy0 + 9, ix1 + 7, iy1 + 9], radius=16, fill=(0, 0, 0, 95))
        base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
        base.paste(ins, (ix0, iy0))
        d2.rounded_rectangle([ix0, iy0, ix1, iy1], radius=16, outline=C, width=8)
        d2.ellipse([ix0 - 4, iy0 - 4, ix0 + 50, iy0 + 50], fill=C)
        d2.text((ix0 + 23, iy0 + 23), str(i), fill=(255, 255, 255, 255), font=font(34), anchor="mm")

    # --- deterministic critique report (step 2 of the loop) ---
    report = []
    for i, (t, bb) in enumerate(boxes, 1):
        if not bb:
            report.append({"idx": i, "selector": t.get("selector"), "kind": t.get("kind", "box"), "found": False})
            continue
        k = t.get("kind", "box")
        pd = t.get("pad", 28 if k == "zoom" else 12)
        ex0 = (bb["x"] - pd) * DSF; ey0 = (bb["y"] - pd) * DSF
        ex1 = (bb["x"] + bb["width"] + pd) * DSF; ey1 = (bb["y"] + bb["height"] + pd) * DSF
        report.append({"idx": i, "selector": t.get("selector"), "kind": k, "found": True,
                       "edge_clipped": bool(ex0 < 0 or ey0 < 0 or ex1 > IW or ey1 > IH)})
    with open(a.out.rsplit(".", 1)[0] + "_report.json", "w") as fh:
        json.dump(report, fh, indent=2)
    print("REPORT", json.dumps(report))
    missing = [r["selector"] for r in report if not r["found"]]

    base.convert("RGB").save(a.out, quality=95)
    print("DREW", drawn, "annotations (", len(zooms), "zoom) ->", a.out)
    if a.strict and missing:
        print("STRICT-FAIL: targets not found ->", missing)
        sys.exit(2)


if __name__ == "__main__":
    main()
