#!/usr/bin/env python3
"""Render the AI-companion regulatory-history timeline for is-candy-ai-safe.

Designed editorial timeline (NOT a generic bar chart) built only from the
sourced regulatory events already in the cited draft. NO third-party logos,
NO website capture, NO real-person likeness, NO invented events. Every node
maps 1:1 to a citation in content-pipeline/6-drafts-cited/is-candy-ai-safe.md.

Sourced events (and ONLY these):
  - Feb 2023  Italy's regulator banned the app          (TechCrunch / IAPP)
  - Jan 2025  US FTC complaint filed (unresolved)       (Tech Justice Law / TIME)
  - 2025      Operator fined EUR 5M                      (TechCrunch / IAPP)

Usage:
    python3 _render_regulatory_timeline.py --out <abs path>
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Neutral, brand-restrained editorial palette (no saturated alarm-red dominance).
PAPER = "#F7F6F2"
INK = "#23272E"
SLATE = "#6B7280"
HAIRLINE = "#C7CDD6"
ACCENT = "#9333EA"   # restrained violet accent for event markers
MUTED = "#9AA3AF"

# (x-position, top-label date, two-line description, source attribution)
EVENTS = [
    (0.0, "Feb 2023",
     "Italy's data regulator\nbanned the app",
     "TechCrunch / IAPP"),
    (1.0, "Jan 2025",
     "US FTC complaint filed\n(unresolved as of early 2026)",
     "Tech Justice Law / TIME"),
    (2.0, "2025",
     "Operator fined €5M over\nage-checks & data handling",
     "TechCrunch / IAPP"),
]


def render(out_path: Path) -> int:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyBboxPatch
    except ImportError as exc:
        sys.stderr.write(f"matplotlib unavailable: {exc}\n")
        return 1

    width_px, height_px, dpi = 1600, 760, 160
    fig, ax = plt.subplots(figsize=(width_px / dpi, height_px / dpi), dpi=dpi)
    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(PAPER)

    ax.set_xlim(-0.6, 2.6)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # Title + subtitle.
    ax.text(-0.55, 9.4, "A documented regulatory trail",
            fontsize=20, fontweight="bold", color=INK, ha="left", va="center")
    ax.text(-0.55, 8.5,
            "Public regulatory actions on record for one compared AI-companion platform",
            fontsize=11, color=SLATE, ha="left", va="center")

    # Timeline spine.
    spine_y = 5.0
    ax.plot([0.0, 2.0], [spine_y, spine_y], color=HAIRLINE, linewidth=3,
            solid_capstyle="round", zorder=1)

    for x, date, desc, source in EVENTS:
        # marker node
        ax.scatter([x], [spine_y], s=260, color=ACCENT, zorder=3,
                   edgecolors=PAPER, linewidths=2.5)
        ax.scatter([x], [spine_y], s=70, color=PAPER, zorder=4)

        # date label above
        ax.text(x, spine_y + 1.15, date, fontsize=14, fontweight="bold",
                color=INK, ha="center", va="bottom")

        # description card below
        ax.text(x, spine_y - 1.0, desc, fontsize=11.5, color=INK,
                ha="center", va="top", linespacing=1.35)

        # source attribution at the very bottom
        ax.text(x, spine_y - 2.9, source, fontsize=8.5, color=MUTED,
                ha="center", va="top", style="italic")

    # Footer note — keeps the graphic honest / non-absolutist.
    ax.text(-0.55, 0.5,
            "Sourced events only. Replika remains a working service; figures reflect "
            "cited public reporting, not legal advice.",
            fontsize=8.5, color=MUTED, ha="left", va="center")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=dpi, bbox_inches="tight", facecolor=PAPER)
    plt.close(fig)
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    args = p.parse_args()
    return render(Path(args.out))


if __name__ == "__main__":
    sys.exit(main())
