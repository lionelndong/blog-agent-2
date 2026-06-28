"""Deterministic brand-palette check for concept illustrations (gate first-filter, 2026-06-28).

A cheap, machine signal to support the HARD VISION GATE (see VISUAL-CRITIQUE-LOOP.md). It does
NOT decide on its own — the agent's vision pass is decisive — but it catches obvious palette
drift (e.g. the model rendering a "cyan/teal" hero instead of brand blue→violet) before a human
even looks. Classifies every non-neutral pixel by HUE into brand bins and reports coverage +
an off-brand-color percentage.

Brand palette: blue #2E90FA, violet #8B5CF6, mint #22B276, coral #FF6B5C (on a light/cool bg).

Usage: python concept_palette_check.py --in img.png [--json]
Verdict (advisory): WARN if off_pct > 12 (notable non-brand color) or brand_pct < 12 (washed out).
"""
import argparse, colorsys, json
from PIL import Image

# Brand hue windows (degrees). The blue->violet continuum is one band (gradients live here).
BANDS = {
    "blue_violet": [(198, 282)],   # #2E90FA hue~211 .. #8B5CF6 hue~258 (+ gradient blend + margins)
    "mint":        [(138, 168)],   # #22B276 hue~154
    "coral":       [(0, 18), (348, 360)],  # #FF6B5C hue~6 (warm red-orange)
}
OFF_LABEL = {  # for human-readable reporting of common off-brand hues
    "cyan_teal": [(168, 198)], "green_yellow": [(60, 138)], "pink_magenta": [(282, 348)],
    "orange_yellow": [(18, 60)],
}


def _band(hue, table):
    for name, wins in table.items():
        for lo, hi in wins:
            if lo <= hue <= hi:
                return name
    return None


def analyze(path, sample_w=160):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    if w > sample_w:
        im = im.resize((sample_w, max(1, round(h * sample_w / w))), Image.BILINEAR)
    px = im.load(); W, H = im.size
    total = W * H
    neutral = brand = off = 0
    by_brand = {k: 0 for k in BANDS}
    by_off = {k: 0 for k in OFF_LABEL}
    for y in range(H):
        for x in range(W):
            r, g, b = px[x, y]
            hh, ss, vv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            hue = hh * 360
            if ss < 0.14 or vv < 0.10:   # washed-out / near-white / near-black -> background
                neutral += 1
                continue
            bb = _band(hue, BANDS)
            if bb:
                brand += 1; by_brand[bb] += 1
            else:
                off += 1
                ob = _band(hue, OFF_LABEL)
                if ob:
                    by_off[ob] += 1
    pct = lambda n: round(100 * n / total, 1)
    chroma = brand + off  # non-neutral pixels
    off_of_chroma = round(100 * off / chroma, 1) if chroma else 0.0
    # Tuned against real data (2026-06-28): editorial concept art is mostly negative space, so a
    # high neutral % is GOOD and brand % is naturally small. Real palette drift shows up as a
    # MEANINGFUL ABSOLUTE off-color area (rejected v1 cyan = 3.7% abs / 25% of-colored) — not as
    # the <1.5% anti-alias noise that legit clean v2 renders carry. Gate on absolute off AND its
    # share of colored pixels; only flag "washed out" if there is essentially no brand color.
    warn = (pct(off) >= 2.0 and off_of_chroma >= 15.0) or (pct(brand) < 3.0)
    return {
        "image": path, "size": [w, h],
        "neutral_pct": pct(neutral), "brand_pct": pct(brand), "off_pct": pct(off),
        "off_pct_of_colored": off_of_chroma,
        "brand_breakdown": {k: pct(v) for k, v in by_brand.items()},
        "off_breakdown": {k: pct(v) for k, v in by_off.items() if v},
        "verdict": "WARN" if warn else "ok",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    res = analyze(a.inp)
    if a.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"{res['verdict']:>4}  brand={res['brand_pct']}%  off={res['off_pct']}% "
              f"(off-of-colored={res['off_pct_of_colored']}%)  neutral={res['neutral_pct']}%  "
              f"| {res['brand_breakdown']}"
              + (f"  OFF:{res['off_breakdown']}" if res['off_breakdown'] else ""))


if __name__ == "__main__":
    main()
