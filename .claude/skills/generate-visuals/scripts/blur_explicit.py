#!/usr/bin/env python3
"""Selectively blur ONLY the explicit regions of a captured product shot — keep the character
visible and on-brand, make the result SFW. (2026-06-28, for the blog action-shot SFW pass.)

ndong's directive: don't blur the whole character — blur only the explicit part. The blur is a
strong gaussian under a FEATHERED rounded mask, so it reads as a soft focus, not a hard censor box.

Two modes (combinable):
  --auto                       NudeNet detects explicit regions and blurs each. Explicit classes only
                               (genitalia / exposed breast / buttocks / anus) — faces, clothing,
                               and non-explicit skin are left untouched.
  --boxes '[[x,y,w,h],...]'    Manual regions, FRACTIONS of width/height (0..1) by default, or --px
                               for pixels. Use this for precise, vision-specified curation.

Emits a JSON report (what was blurred). Pair with the VISUAL-CRITIQUE-LOOP SFW gate: after blurring,
the agent verifies NOTHING explicit survives before the shot is framed/used.
"""
import argparse
import json
import sys
from pathlib import Path
from PIL import Image, ImageFilter, ImageDraw

# NudeNet classes that are actually explicit (the "_EXPOSED" set). Covered/clothed variants and
# FACE/FEET are intentionally NOT blurred — we keep the character recognizable.
EXPLICIT_CLASSES = {
    "FEMALE_GENITALIA_EXPOSED",
    "MALE_GENITALIA_EXPOSED",
    "FEMALE_BREAST_EXPOSED",
    "BUTTOCKS_EXPOSED",
    "ANUS_EXPOSED",
}


def _blur_region(img: Image.Image, box_px, strength: float, feather: float) -> None:
    x, y, w, h = box_px
    x, y, w, h = int(x), int(y), int(w), int(h)
    x2, y2 = min(img.width, x + w), min(img.height, y + h)
    x, y = max(0, x), max(0, y)
    if x2 <= x or y2 <= y:
        return
    pad = int(max(w, h) * 0.22)
    rx, ry = max(0, x - pad), max(0, y - pad)
    rx2, ry2 = min(img.width, x2 + pad), min(img.height, y2 + pad)
    region = img.crop((rx, ry, rx2, ry2))
    rad = max(10, int(min(region.size) * strength))
    blurred = region.filter(ImageFilter.GaussianBlur(rad))
    # feathered rounded mask over the actual box (in region-local coords)
    mask = Image.new("L", region.size, 0)
    d = ImageDraw.Draw(mask)
    bx0, by0, bx1, by1 = x - rx, y - ry, x2 - rx, y2 - ry
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=int(min(w, h) * 0.32), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather))
    img.paste(blurred, (rx, ry), mask)


def detect_auto(path: Path, min_score: float):
    from nudenet import NudeDetector  # lazy; only needed for --auto
    det = NudeDetector()
    out = []
    for r in det.detect(str(path)):
        if r.get("class") in EXPLICIT_CLASSES and float(r.get("score", 0)) >= min_score:
            out.append((r["box"], r["class"], float(r["score"])))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--auto", action="store_true", help="auto-detect explicit regions (NudeNet)")
    ap.add_argument("--boxes", default=None, help="JSON [[x,y,w,h],...] (fractions 0..1, or px with --px)")
    ap.add_argument("--px", action="store_true", help="treat --boxes as pixels, not fractions")
    ap.add_argument("--strength", type=float, default=0.20, help="blur radius as a fraction of region size")
    ap.add_argument("--feather", type=float, default=16, help="mask edge feather (px)")
    ap.add_argument("--min-score", type=float, default=0.35, help="min NudeNet confidence (--auto)")
    a = ap.parse_args()

    img = Image.open(a.inp).convert("RGB")
    W, H = img.size
    report = []

    if a.auto:
        try:
            for box, cls, score in detect_auto(Path(a.inp), a.min_score):
                _blur_region(img, box, a.strength, a.feather)
                report.append({"mode": "auto", "class": cls, "score": round(score, 2), "box": box})
        except Exception as exc:
            sys.stderr.write(f"auto-detect failed ({exc}); use --boxes for vision-specified regions.\n")
            print(json.dumps({"status": "failed", "reason": "nudenet_unavailable", "error": str(exc)}))
            return 1

    if a.boxes:
        for b in json.loads(a.boxes):
            box_px = b if a.px else [b[0] * W, b[1] * H, b[2] * W, b[3] * H]
            _blur_region(img, box_px, a.strength, a.feather)
            report.append({"mode": "px" if a.px else "frac", "box": b})

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    img.save(a.out, quality=95)
    print(json.dumps({"status": "blurred", "out": a.out, "regions": len(report), "detail": report}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
