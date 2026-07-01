"""Annotation engine — SVG-overlay annotations rendered by the BROWSER (crisp, vector).

Arrow = "C / bold": a thick single-arc bezier with a clean triangular head, placed DIAGONALLY
(label offset to the side) so it sweeps in as one clean arc — no vertical hook. Boxes, circles,
highlights too. Default colour = brand BLUE. Emits a JSON report incl. pairwise OVERLAP detection;
--strict hard-fails on overlap / missing target (forces a redo).

Per-target "kind": box (default) | circle | highlight
Usage:
  DISPLAY=:99 python annotate_screenshot.py --url URL --out out.png \
    --targets '[{"selector":"text=Tools","kind":"box","note":"open Tools"}]' \
    [--dismiss "I am 18 years of age or older"] [--color blue] [--strict] [--shot-only]
"""
import argparse
import json
import sys
import math
from PIL import ImageFont, Image, ImageDraw

try:
    from patchright.sync_api import sync_playwright
except ImportError:
    from playwright.sync_api import sync_playwright

COLORS = {"blue": "#2E90FA", "purple": "#8B5CF6", "indigo": "#534AB7",
          "red": "#E53935", "orange": "#F57C00", "green": "#22B276"}

INJECT = r"""(args) => {
  const old=document.getElementById('__annot__'); if(old) old.remove();
  const wrap=document.createElement('div'); wrap.id='__annot__';
  wrap.setAttribute('style','position:fixed;left:0;top:0;width:'+args.W+'px;height:'+args.H
    +'px;z-index:2147483647;pointer-events:none');
  wrap.innerHTML='<svg xmlns="http://www.w3.org/2000/svg" width="'+args.W+'" height="'+args.H
    +'" viewBox="0 0 '+args.W+' '+args.H+'">'+args.svg+'</svg>';
  document.body.appendChild(wrap);
}"""


def measure(sz):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)
    except Exception:
        return ImageFont.load_default()


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _ctrl(sx, sy, ex, ey, bend):
    dx, dy = ex - sx, ey - sy
    L = math.hypot(dx, dy) or 1
    return (sx + ex) / 2 - dy / L * bend * L, (sy + ey) / 2 + dx / L * bend * L


def _tan(sx, sy, cx, cy, ex, ey, t):
    u = 1 - t
    dx, dy = 2 * u * (cx - sx) + 2 * t * (ex - cx), 2 * u * (cy - sy) + 2 * t * (ey - cy)
    L = math.hypot(dx, dy) or 1
    return dx / L, dy / L


def arrow_bold(sx, sy, ex, ey, color, w=7, bend=0.24, hd=22):
    """C/bold arrow: thick single-arc bezier (shortened before the tip) + filled triangle head."""
    cx, cy = _ctrl(sx, sy, ex, ey, bend)
    tx, ty = _tan(sx, sy, cx, cy, ex, ey, 1.0)
    bx, by = ex - tx * hd * 0.7, ey - ty * hd * 0.7
    nx, ny = -ty, tx
    h1x, h1y = ex - tx * hd + nx * hd * 0.58, ey - ty * hd + ny * hd * 0.58
    h2x, h2y = ex - tx * hd - nx * hd * 0.58, ey - ty * hd - ny * hd * 0.58
    return ('<path d="M %.1f %.1f Q %.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"/>'
            '<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f Z" fill="%s"/>'
            % (sx, sy, cx, cy, bx, by, color, w, ex, ey, h1x, h1y, h2x, h2y, color))


# SFW pass — blur explicit img/video >= min px (keep logos/icons/labels sharp) so
# an annotated competitor/adult surface stays publishable on our SFW blog.
BLUR_IMAGES_JS = """
(min) => {
  let n = 0;
  document.querySelectorAll('img, video').forEach(el => {
    const r = el.getBoundingClientRect();
    const s = ((el.currentSrc||el.src||'') + ' ' + (el.alt||'')).toLowerCase();
    if (r.width >= min && r.height >= min && !/logo|icon|wordmark/.test(s)) {
      const px = Math.max(26, Math.round(Math.min(r.width, r.height) / 5));
      el.style.setProperty('filter', 'blur(' + px + 'px)', 'important');
      el.style.setProperty('clip-path', 'inset(0)', 'important');
      n++;
    }
  });
  return n;
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--targets", default="[]")
    ap.add_argument("--dismiss", default=None)
    ap.add_argument("--color", default="blue")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--shot-only", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--blur-images", dest="blur_images", type=int, default=64,
                    help="Blur img/video >= N px before capture (SFW). Default 64 (our niche is 18+).")
    ap.add_argument("--no-blur", dest="no_blur", action="store_true",
                    help="Disable the SFW blur (for a genuinely SFW surface).")
    a = ap.parse_args()
    blur_images = None if a.no_blur else a.blur_images

    targets = json.loads(a.targets)
    base_col = COLORS.get(a.color, COLORS["blue"])
    W, H = a.width, a.height
    FS = 16
    f = measure(FS)

    with sync_playwright() as p:
        br = p.chromium.launch(headless=False, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
        ctx = br.new_context(viewport={"width": W, "height": H}, device_scale_factor=a.scale)
        pg = ctx.new_page()
        pg.goto(a.url, wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(3500)
        if a.dismiss:
            try:
                pg.get_by_text(a.dismiss, exact=True).first.click(timeout=12000, force=True)
                pg.wait_for_timeout(2500)
            except Exception as e:
                print("dismiss failed:", str(e)[:100])
        pg.wait_for_timeout(1200)
        # SFW pass before measuring/drawing: blur explicit media so the annotated
        # shot is publishable (logos/labels stay sharp; the callout sits on top).
        if blur_images:
            try:
                nb = pg.evaluate(BLUR_IMAGES_JS, blur_images)
                pg.wait_for_timeout(250)
                print(f"SFW blur -> {nb} media element(s) >= {blur_images}px")
            except Exception as e:
                print("blur failed:", str(e)[:80])
        boxes = []
        for t in targets:
            try:
                bb = pg.locator(t["selector"]).first.bounding_box(timeout=4000)
            except Exception as e:
                bb = None
                print("target not found:", t.get("selector"), str(e)[:60])
            boxes.append((t, bb))
        if a.shot_only or not targets:
            pg.screenshot(path=a.out)
            br.close()
            print("captured ->", a.out)
            return

        clean = a.out.rsplit(".", 1)[0] + "_clean.png"
        pg.screenshot(path=clean)
        svg = []
        rects = {}
        zooms = []
        for i, (t, bb) in enumerate(boxes, 1):
            if not bb:
                continue
            C = COLORS.get(t.get("color"), base_col)
            kind = t.get("kind", "box")
            pad = t.get("pad", 6)
            x, y = bb["x"] - pad, bb["y"] - pad
            w, h = bb["width"] + 2 * pad, bb["height"] + 2 * pad
            cxb = x + w / 2
            if kind == "circle":
                svg.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="%s" stroke-width="3.5"/>'
                           % (cxb, y + h / 2, w / 2 + 5, h / 2 + 5, C))
                shape = (x - 5, y - 5, x + w + 5, y + h + 5)
            elif kind == "highlight":
                svg.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" fill="%s" fill-opacity="0.18" stroke="%s" stroke-width="2.5"/>'
                           % (x, y, w, h, C, C))
                shape = (x, y, x + w, y + h)
            elif kind == "zoom":
                svg.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" fill="%s" fill-opacity="0.14" stroke="%s" stroke-width="3"/>'
                           % (x, y, w, h, C, C))
                corner = t.get("corner", "br")
                factor = min(2.8, max(1.7, (W * 0.30) / w))
                iw, ih = w * factor, h * factor
                if ih > H * 0.40:
                    scf = H * 0.40 / ih
                    iw, ih = iw * scf, ih * scf
                mg = W * 0.025
                ix0 = (W - iw - mg) if corner in ("br", "tr") else mg
                iy0 = (H - ih - mg) if corner in ("br", "bl") else mg
                ix1, iy1 = ix0 + iw, iy0 + ih
                scx, scy = x + w / 2, y + h / 2
                if ix0 > scx:
                    ax2, ay2 = ix0 - 10, iy0 + ih / 2
                elif ix1 < scx:
                    ax2, ay2 = ix1 + 10, iy0 + ih / 2
                elif iy0 > scy:
                    ax2, ay2 = ix0 + iw / 2, iy0 - 10
                else:
                    ax2, ay2 = ix0 + iw / 2, iy1 + 10
                svg.append(arrow_bold(scx, scy, ax2, ay2, C, bend=0.16))
                zooms.append((i, (x, y, w, h), (ix0, iy0, ix1, iy1), C))
                rects[i] = [(x, y, x + w, y + h), (ix0, iy0, ix1, iy1)]
                continue
            else:
                svg.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="9" fill="none" stroke="%s" stroke-width="3.5"/>'
                           % (x, y, w, h, C))
                shape = (x, y, x + w, y + h)
            # label pill + diagonal arrow
            note = (t.get("note") or "").strip()
            text = (str(i) + "  " + note) if note else str(i)
            pw, ph = f.getlength(text) + 30, 30
            ox, oy = 120, 122
            left = (x - 40 - pw) >= 6 and t.get("side") != "R"
            ex = cxb + (-6 if left else 6)
            ey = y - 3
            pcx = (cxb - ox) if left else (cxb + ox)
            pcx = min(max(pcx, 6 + pw / 2), W - 6 - pw / 2)
            pcy = max(6 + ph / 2, y - oy)
            prect = (pcx - pw / 2, pcy - ph / 2, pcx + pw / 2, pcy + ph / 2)
            sx = pcx + (pw * 0.16 if left else -pw * 0.16)
            sy = pcy + ph / 2
            svg.append(arrow_bold(sx, sy, ex, ey, C, bend=(0.24 if left else -0.24)))
            svg.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="15" fill="%s"/>'
                       % (prect[0], prect[1], pw, ph, C))
            svg.append('<text x="%.1f" y="%.1f" fill="#fff" font-family="Inter,Segoe UI,Arial,sans-serif" font-weight="700" font-size="%d" text-anchor="middle" dominant-baseline="central">%s</text>'
                       % (pcx, pcy + 1, FS, esc(text)))
            rects[i] = [shape, prect]

        pg.evaluate(INJECT, {"svg": "".join(svg), "W": W, "H": H})
        pg.wait_for_timeout(450)
        pg.screenshot(path=a.out)
        br.close()

    if zooms:
        ann = Image.open(a.out).convert("RGB")
        cln = Image.open(clean).convert("RGB")
        dd = ImageDraw.Draw(ann)
        D = a.scale
        try:
            bf = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
        except Exception:
            bf = ImageFont.load_default()
        for (idx, (zx, zy, zw, zh), (ix0, iy0, ix1, iy1), Cz) in zooms:
            crop = cln.crop((int(zx * D), int(zy * D), int((zx + zw) * D), int((zy + zh) * D)))
            tw, th = max(1, int((ix1 - ix0) * D)), max(1, int((iy1 - iy0) * D))
            ann.paste(crop.resize((tw, th), Image.LANCZOS), (int(ix0 * D), int(iy0 * D)))
            rgb = hexrgb(Cz)
            dd.rounded_rectangle([ix0 * D, iy0 * D, ix1 * D, iy1 * D], radius=16, outline=rgb, width=4 * D)
            bx, by = int(ix0 * D), int(iy0 * D)
            dd.ellipse([bx - 6, by - 6, bx + 48, by + 48], fill=rgb)
            dd.text((bx + 21, by + 21), str(idx), fill=(255, 255, 255), font=bf, anchor="mm")
        ann.save(a.out, quality=95)

    def ov(p, q):
        return not (p[2] <= q[0] or q[2] <= p[0] or p[3] <= q[1] or q[3] <= p[1])
    idxs = sorted(rects)
    overlaps = [[idxs[i], idxs[j]] for i in range(len(idxs)) for j in range(i + 1, len(idxs))
                if any(ov(ra, rb) for ra in rects[idxs[i]] for rb in rects[idxs[j]])]
    report = []
    for i, (t, bb) in enumerate(boxes, 1):
        if not bb:
            report.append({"idx": i, "selector": t.get("selector"), "found": False})
            continue
        r = rects[i][0]
        report.append({"idx": i, "selector": t.get("selector"), "kind": t.get("kind", "box"),
                       "found": True, "edge_clipped": bool(r[0] < 0 or r[1] < 0 or r[2] > W or r[3] > H)})
    summary = {"targets": report, "overlaps": overlaps, "missing": [r["selector"] for r in report if not r["found"]]}
    with open(a.out.rsplit(".", 1)[0] + "_report.json", "w") as fh:
        json.dump(summary, fh, indent=2)
    print("REPORT", json.dumps(summary))
    print("DREW ->", a.out)
    if a.strict and (summary["missing"] or overlaps):
        print("STRICT-FAIL: missing", summary["missing"], "overlaps", overlaps)
        sys.exit(2)


if __name__ == "__main__":
    main()
