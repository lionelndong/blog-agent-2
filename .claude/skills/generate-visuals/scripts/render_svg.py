"""Render an SVG blueprint to a crisp PNG via the headless browser (infographic step 2).
Usage: python render_svg.py --svg blueprint.svg --out blueprint.png [--width 1080] [--height 1320] [--scale 2]
"""
import argparse
import pathlib

try:
    from patchright.sync_api import sync_playwright
except ImportError:
    from playwright.sync_api import sync_playwright


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--svg", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1320)
    ap.add_argument("--scale", type=int, default=2)
    a = ap.parse_args()

    svg = pathlib.Path(a.svg).read_text(encoding="utf-8")
    html = '<!doctype html><html><body style="margin:0;padding:0">' + svg + "</body></html>"
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        pg = b.new_page(viewport={"width": a.width, "height": a.height}, device_scale_factor=a.scale)
        pg.set_content(html)
        pg.wait_for_timeout(500)
        pg.screenshot(path=a.out, clip={"x": 0, "y": 0, "width": a.width, "height": a.height})
        b.close()
    print("rendered", a.out)


if __name__ == "__main__":
    main()
