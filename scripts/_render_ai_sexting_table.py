#!/usr/bin/env python3
"""Render the feature-pricing-privacy matrix table as a PNG."""
import json
import matplotlib.pyplot as plt
from matplotlib.table import Table
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]
data_path = Path("content-pipeline/1-research/ai-sexting-app-data.json")
out_path = Path("content-pipeline/images/ai-sexting-app/table-1-feature-pricing-matrix.png")

with data_path.open() as f:
    data = json.load(f)

features = data["feature_matrix"]
pricing = data["pricing_comparison"]

apps = ["Candy.AI", "OurDream.AI", "Nastia AI", "Pleasur.AI"]
columns = ["App", "Chat", "Image", "Voice", "Video", "Custom Character", "Price (USD/mo)", "Privacy posture"]

privacy_posture = {
    "Candy.AI": "Mozilla PNI: flagged",
    "OurDream.AI": "Mozilla PNI: flagged",
    "Nastia AI": "Says no data sale; deletion allowed",
    "Pleasur.AI": "Says no data sale; deletion allowed",
}

def yn(v):
    return "Yes" if v else "No"

def price_str(app):
    p = pricing[app]
    if isinstance(p, (int, float)):
        return f"${p:.2f}"
    if p == "gated":
        return "Gated (trial required)"
    if p == "free-tier-only-public":
        return "Free tier published; paid USD not public"
    return str(p)

rows = []
for app in apps:
    fm = features[app]
    rows.append([
        app,
        yn(fm["chat"]),
        yn(fm["image"]),
        yn(fm["voice"]),
        yn(fm["video"]),
        yn(fm["custom_character"]),
        price_str(app),
        privacy_posture[app],
    ])

# Build figure
fig, ax = plt.subplots(figsize=(13, 3.4), dpi=180)
ax.axis("off")
ax.set_title(
    "AI sexting apps — feature, pricing, and privacy matrix",
    fontsize=13, fontweight="bold", loc="left", pad=14,
)

n_rows = len(rows) + 1
n_cols = len(columns)

# Column widths (relative)
col_widths = [0.10, 0.06, 0.06, 0.06, 0.06, 0.12, 0.20, 0.34]
assert abs(sum(col_widths) - 1.0) < 0.01

tbl = Table(ax, bbox=[0, 0, 1, 1])

row_h = 1.0 / n_rows
# Header
x = 0.0
for j, (col, w) in enumerate(zip(columns, col_widths)):
    cell = tbl.add_cell(0, j, w, row_h, text=col, loc="center", facecolor="#1f2a44")
    cell.get_text().set_color("white")
    cell.get_text().set_fontweight("bold")
    cell.get_text().set_fontsize(10)
    cell.set_edgecolor("white")

# Data rows
for i, row in enumerate(rows, start=1):
    bg = "#f4f6fb" if i % 2 == 1 else "#ffffff"
    for j, (val, w) in enumerate(zip(row, col_widths)):
        cell = tbl.add_cell(i, j, w, row_h, text=val, loc="center", facecolor=bg)
        cell.get_text().set_fontsize(9)
        cell.set_edgecolor("#d6dbe5")
        # Bold the app name column
        if j == 0:
            cell.get_text().set_fontweight("bold")
        # Color Yes/No
        if j in (1, 2, 3, 4, 5):
            if val == "Yes":
                cell.get_text().set_color("#1d7a4d")
            elif val == "No":
                cell.get_text().set_color("#b3261e")

# Set column positions manually (Table uses cells we added, but need to update x)
# matplotlib Table doesn't auto-layout columns by width across the bbox unless we use add_cell with bbox.
# Override: we'll set cell positions explicitly.
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
    0.01, -0.02,
    "Sources: live-fetched pricing 2026-05-13 (candy.ai, ourdream.ai/pricing, nastia.ai, pleasur.ai/upgrade); "
    "Mozilla *Privacy Not Included* romantic-AI audit, Feb 2024.",
    fontsize=7.5, color="#444",
)

out_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(out_path, bbox_inches="tight", dpi=180, facecolor="white")
print(f"wrote {out_path}")
