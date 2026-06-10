#!/usr/bin/env python3
"""Render the AI boyfriend app comparison matrix as a legible PNG table-card.

Deterministic matplotlib render (no generative model -> no gibberish-text risk).
Data is the single source of truth: content-pipeline/1-research/ai-boyfriend-data.json
under the `app_comparison` key. Legible labels, brand-neutral palette, color-coded
support cells. Satisfies the D5 visual mandate (text-table -> legible table-card).
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.table import Table

ROOT = Path("/paperclip/instances/default/projects/d11fb003-42e2-4b84-8d88-e1242ad09a70/58966819-f893-4728-ad83-5956700fd1c6/_default/blog-engine")
data_path = ROOT / "content-pipeline/1-research/ai-boyfriend-data.json"
out_path = ROOT / "content-pipeline/images/ai-boyfriend/table-1-ai-boyfriend-apps-compared.png"
out_path.parent.mkdir(parents=True, exist_ok=True)

with data_path.open() as f:
    data = json.load(f)

comp = data["app_comparison"]
columns = comp["columns"]
rows = comp["rows"]

n_rows = len(rows) + 1
n_cols = len(columns)

# Relative column widths (sum to 1.0): App + 7 attribute columns
col_widths = [0.135, 0.135, 0.135, 0.095, 0.150, 0.105, 0.105, 0.140]
assert abs(sum(col_widths) - 1.0) < 0.01, sum(col_widths)

fig, ax = plt.subplots(figsize=(14, 3.6), dpi=180)
ax.axis("off")
ax.set_title(
    "AI Boyfriend Apps Compared (2026)",
    fontsize=14, fontweight="bold", loc="left", pad=16, color="#1f2a44",
)

tbl = Table(ax, bbox=[0, 0, 1, 1])
row_h = 1.0 / n_rows

# Header row
for j, col in enumerate(columns):
    cell = tbl.add_cell(0, j, col_widths[j], row_h, text=col, loc="center",
                        facecolor="#1f2a44")
    cell.get_text().set_color("white")
    cell.get_text().set_fontweight("bold")
    cell.get_text().set_fontsize(9.5)
    cell.set_edgecolor("white")

# Cells whose value signals strong/weak support get color cues.
POSITIVE = {"yes", "yes, full", "best: weeks-long", "deep", "deep (full)",
            "deep personality", "good + key-memory", "generous", "free to start"}
NEGATIVE = {"no", "pro only", "limited", "moderate", "rolling out", "within-session"}

def cue_color(val: str):
    v = val.strip().lower()
    if v in POSITIVE:
        return "#1d7a4d"
    if v in NEGATIVE:
        return "#9a6a00"
    return "#222222"

for i, row in enumerate(rows, start=1):
    bg = "#f4f6fb" if i % 2 == 1 else "#ffffff"
    for j, val in enumerate(row):
        cell = tbl.add_cell(i, j, col_widths[j], row_h, text=val, loc="center",
                            facecolor=bg)
        cell.get_text().set_fontsize(8.6)
        cell.set_edgecolor("#d6dbe5")
        if j == 0:
            cell.get_text().set_fontweight("bold")
            cell.get_text().set_color("#1f2a44")
        else:
            cell.get_text().set_color(cue_color(val))

# Explicit column layout (matplotlib Table doesn't auto-flow widths across the bbox)
x_positions = [0.0]
for w in col_widths[:-1]:
    x_positions.append(x_positions[-1] + w)
for (r, c), cell in tbl.get_celld().items():
    cell.set_x(x_positions[c])
    cell.set_width(col_widths[c])
    cell.set_y(1.0 - (r + 1) * row_h)
    cell.set_height(row_h)
    cell.set_linewidth(0.6)

ax.add_table(tbl)

fig.text(
    0.01, -0.04,
    "Pricing changes frequently — check current tiers before committing. "
    "Feature data compiled from public 2026 reviews and platform pages.",
    fontsize=7.5, color="#555",
)

fig.savefig(out_path, bbox_inches="tight", facecolor="white", dpi=180)
plt.close(fig)
print(f"wrote {out_path}")
