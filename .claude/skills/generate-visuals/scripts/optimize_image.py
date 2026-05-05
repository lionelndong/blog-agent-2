#!/usr/bin/env python3
"""Lossless PNG optimization via Pillow.

Usage:
    python optimize_image.py <path>...

Re-encodes each PNG with maximum compression and stripped metadata.
Skips files that don't exist or aren't PNGs. Returns 0 even if some
files couldn't be optimized; this is a best-effort polish step.
"""
from __future__ import annotations

import sys
from pathlib import Path


def optimize(path: Path) -> tuple[bool, int, int]:
    if not path.exists() or path.suffix.lower() != ".png":
        return False, 0, 0
    try:
        from PIL import Image
    except ImportError:
        sys.stderr.write("Pillow not installed; skipping optimization.\n")
        return False, 0, 0

    before = path.stat().st_size
    try:
        with Image.open(path) as img:
            img.load()
            img.save(path, format="PNG", optimize=True, compress_level=9)
    except Exception as exc:  # treat as best-effort
        sys.stderr.write(f"optimize failed for {path}: {exc}\n")
        return False, before, before
    after = path.stat().st_size
    return True, before, after


def main() -> int:
    if len(sys.argv) < 2:
        sys.stderr.write("usage: optimize_image.py <path>...\n")
        return 2
    total_before = 0
    total_after = 0
    for arg in sys.argv[1:]:
        ok, before, after = optimize(Path(arg))
        if ok:
            total_before += before
            total_after += after
    if total_before:
        saved = total_before - total_after
        pct = 100 * saved / total_before if total_before else 0
        sys.stdout.write(f"optimized: {total_before} -> {total_after} bytes ({pct:.1f}% saved)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
