#!/usr/bin/env python3
"""Render a brand-styled comparison / checklist 'table card' as a legible PNG.

Generative image models mangle in-image text, so any [VISUAL] that is fundamentally a
table or checklist is rendered here instead: crisp real text, brand palette, rounded
card framing. Free (no API spend), answer-engine friendly, accessible.

Usage:
    python render_table_card.py --spec /path/to/spec.json --out /path/to/out.png
"""
from __future__ import annotations
import argparse, json, textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Brand palette (working system — see images/<slug>/prompts.md)
PLUM = "#1B1430"
AUBERGINE = "#2E1A3D"
ROSE = "#E26D9C"
MAGENTA = "#C14A6E"
BLUSH = "#F5D6E0"
CREAM = "#F7F2EC"
GOLD = "#E0A458"
INK = "#1A1A1A"
SLATE = "#4A4458"


def _wrap(text: str, width: int) -> str:
    return "\n".join(textwrap.wrap(text, width=width)) if text else ""


def render(spec: dict, out: Path) -> None:
    title = spec.get("title", "")
    subtitle = spec.get("subtitle", "")
    cols = spec["columns"]
    rows = spec["rows"]  # list of lists, len == len(cols)
    ncol = len(cols)

    # Column width weights (first column a touch narrower for "label" tables)
    weights = spec.get("col_weights") or [1.0] * ncol
    wsum = sum(weights)
    fracs = [w / wsum for w in weights]

    # Layout metrics (figure coords 0..1)
    fig_w = spec.get("fig_w", 16.0)
    # estimate wrapped lines per cell to size row heights
    wrap_chars = spec.get("wrap_chars") or [max(14, int(60 * f)) for f in fracs]
    row_lines = []
    for r in rows:
        maxlines = 1
        for j, cell in enumerate(r):
            wrapped = _wrap(str(cell), wrap_chars[j])
            maxlines = max(maxlines, wrapped.count("\n") + 1)
        row_lines.append(maxlines)
    header_lines = max((_wrap(c, wrap_chars[j]).count("\n") + 1) for j, c in enumerate(cols))

    line_h = 0.32  # inches per text line
    pad = 0.22
    row_heights = [max(0.62, lines * line_h + pad) for lines in row_lines]
    header_h = max(0.7, header_lines * line_h + pad)
    title_h = 1.05 if title else 0.0
    margin = 0.45
    fig_h = title_h + header_h + sum(row_heights) + 2 * margin

    fig = plt.figure(figsize=(fig_w, fig_h), dpi=130)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor(CREAM)

    # outer rounded card
    ax.add_patch(FancyBboxPatch((0.012, 0.012), 0.976, 0.976,
                 boxstyle="round,pad=0,rounding_size=0.02",
                 linewidth=1.4, edgecolor=BLUSH, facecolor="white",
                 mutation_aspect=fig_h / fig_w, zorder=0))

    x0, x1 = margin / fig_w, 1 - margin / fig_w
    table_w = x1 - x0
    # column x edges
    xedges = [x0]
    for f in fracs:
        xedges.append(xedges[-1] + f * table_w)

    y = 1 - margin / fig_h
    # Title
    if title:
        ax.text(x0, y, title, fontsize=24, fontweight="bold", color=AUBERGINE,
                va="top", ha="left")
        if subtitle:
            ax.text(x0, y - 0.40 / fig_h, subtitle, fontsize=13,
                    color=SLATE, va="top", ha="left")
        # small rose accent rule under the title
        ax.plot([x0, x0 + 0.07], [y - (title_h - 0.18) / fig_h, y - (title_h - 0.18) / fig_h],
                color=ROSE, linewidth=3, solid_capstyle="round", zorder=2)
        y -= title_h / fig_h

    # Header band
    hh = header_h / fig_h
    header_bottom = y - hh
    ax.add_patch(FancyBboxPatch((x0, y - hh), table_w, hh,
                 boxstyle="round,pad=0,rounding_size=0.012",
                 linewidth=0, facecolor=AUBERGINE, mutation_aspect=fig_h / fig_w, zorder=1))
    for j, c in enumerate(cols):
        cx = xedges[j] + 0.012
        ax.text(cx, y - hh / 2, _wrap(c, wrap_chars[j]), fontsize=13.5, fontweight="bold",
                color=CREAM, va="center", ha="left", zorder=2)
    y -= hh

    # Rows
    for i, r in enumerate(rows):
        rh = row_heights[i] / fig_h
        face = CREAM if i % 2 == 0 else "#FBEFF4"  # cream / very light blush stripe
        ax.add_patch(plt.Rectangle((x0, y - rh), table_w, rh, facecolor=face,
                     edgecolor="none", zorder=1))
        for j, cell in enumerate(r):
            cx = xedges[j] + 0.012
            cell_s = str(cell)
            # First column = label (bold ink); accent markers for ✅⚠️🚫
            if j == 0:
                color, weight, size = INK, "bold", 12.8
            else:
                color, weight, size = SLATE, "normal", 12.0
            ax.text(cx, y - rh / 2, _wrap(cell_s, wrap_chars[j]), fontsize=size,
                    fontweight=weight, color=color, va="center", ha="left", zorder=2)
        # thin row rule
        ax.plot([x0, x1], [y - rh, y - rh], color="#EADFE6", linewidth=0.8, zorder=1)
        y -= rh

    # vertical column dividers (rows only — not across the header band)
    for xe in xedges[1:-1]:
        ax.plot([xe, xe], [y, header_bottom], color="#EADFE6",
                linewidth=0.8, zorder=1)

    fig.savefig(out, facecolor=CREAM, bbox_inches=None)
    plt.close(fig)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    spec = json.loads(Path(args.spec).read_text())
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    render(spec, out)
    print(json.dumps({"status": "captured", "path": str(out), "renderer": "table-card"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
