"""Stamp the real Pleasur.ai logo onto an infographic (LOCKED recipe 2026-06-28).
The logo is composited deterministically — NEVER redrawn by AI. Robust to the site's
white-on-black variant: keys out the background, recolors the white half to charcoal for
light canvases, and preserves the blue ".ai".

Usage: python composite_logo.py --in raw.png --out final.png
       [--logo /path/logo.png] [--width-frac 0.21] [--margin-frac 0.05] [--dark]
If --logo is omitted it downloads https://pleasur.ai/images/pleasurai-logo.png (cached at /tmp).
--dark keeps the original white wordmark (use only on a dark canvas).
"""
import argparse, io, statistics, urllib.request, pathlib
from PIL import Image

LOGO_URL = 'https://pleasur.ai/images/pleasurai-logo.png'
CACHE = '/tmp/pleasurai-logo-src.png'


def load_logo(path):
    if path:
        return Image.open(path).convert('RGBA')
    if pathlib.Path(CACHE).exists():
        return Image.open(CACHE).convert('RGBA')
    req = urllib.request.Request(LOGO_URL, headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req, timeout=30).read()  # loud-fail if unreachable (no fallback)
    pathlib.Path(CACHE).write_bytes(data)
    return Image.open(io.BytesIO(data)).convert('RGBA')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='inp', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--logo', default=None)
    ap.add_argument('--width-frac', type=float, default=0.21)
    ap.add_argument('--margin-frac', type=float, default=0.05)
    ap.add_argument('--dark', action='store_true', help='keep white wordmark (dark canvas)')
    a = ap.parse_args()

    logo = load_logo(a.logo)
    px = logo.load(); W, H = logo.size
    corner = px[0, 0]
    if corner[3] > 250:  # opaque bg -> key it out
        bg = corner[:3]
        logo.putdata([(r, g, b, 0) if (abs(r-bg[0]) < 28 and abs(g-bg[1]) < 28 and abs(b-bg[2]) < 28)
                      else (r, g, b, 255) for (r, g, b, al) in logo.getdata()])
    px = logo.load()
    lums = [0.299*px[x, y][0]+0.587*px[x, y][1]+0.114*px[x, y][2]
            for y in range(H) for x in range(W) if px[x, y][3] > 120]
    avg = statistics.mean(lums) if lums else 0
    if avg > 150 and not a.dark:  # white variant on a light canvas -> charcoal, keep blue
        logo.putdata([(45, 45, 45, al) if (al > 40 and r > 150 and g > 150 and b > 150) else (r, g, b, al)
                      for (r, g, b, al) in logo.getdata()])

    info = Image.open(a.inp).convert('RGBA'); IW, IH = info.size
    tw = max(1, int(IW * a.width_frac)); sc = tw / logo.size[0]
    logo = logo.resize((tw, max(1, int(logo.size[1]*sc))), Image.LANCZOS)
    m = int(IW * a.margin_frac)
    pos = (IW - logo.size[0] - m, IH - logo.size[1] - m)
    info.alpha_composite(logo, pos)
    info.convert('RGB').save(a.out)
    print('SAVED', a.out, info.size, '| logo', logo.size, '| avg_lum', round(avg, 1))


if __name__ == '__main__':
    main()
