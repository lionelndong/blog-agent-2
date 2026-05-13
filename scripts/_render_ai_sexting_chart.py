#!/usr/bin/env python3
"""Render the Mozilla PNI 2024 chart with proper labels and source attribution.

The dispatcher's auto-chart mashed percentages with a 'millions' value
on the same y-axis. We want a clean bar chart of the 5 Mozilla percentages
only, with the Muah AI breach called out separately in the caption.
"""
import json
from pathlib import Path
import matplotlib.pyplot as plt

data_path = Path("content-pipeline/1-research/ai-sexting-app-data.json")
out_path = Path("content-pipeline/images/ai-sexting-app/chart-3-mozilla-pni-2024.png")

with data_path.open() as f:
    data = json.load(f)

signals = data["privacy_signals"]

# Pull only the % rows (Mozilla PNI), keep the Muah AI breach for caption only.
metrics = [
    ("May share or sell\nyour data", signals["Mozilla PNI 2024 - chatbots that may share or sell data (%)"]),
    ("Failed minimum\nsecurity standards", signals["Mozilla PNI 2024 - failed minimum security standards (%)"]),
    ("No published\nvulnerability process", signals["Mozilla PNI 2024 - have not published vulnerability process (%)"]),
    ("No clear\nencryption info", signals["Mozilla PNI 2024 - lack clear encryption info (%)"]),
    ("Allow users\nto delete data", signals["Mozilla PNI 2024 - allow users to delete personal data (%)"]),
]

labels = [m[0] for m in metrics]
values = [m[1] for m in metrics]

# Color: red for "bad" stats (high = bad), green for the deletion stat
colors = ["#b3261e", "#b3261e", "#b3261e", "#b3261e", "#1d7a4d"]

fig, ax = plt.subplots(figsize=(11, 5.4), dpi=180)
bars = ax.bar(labels, values, color=colors, edgecolor="white", linewidth=1.2)

ax.set_ylim(0, 100)
ax.set_ylabel("% of romantic AI chatbots audited", fontsize=10)
ax.set_title(
    "Mozilla *Privacy Not Included* 2024 — romantic AI chatbots audit",
    fontsize=13, fontweight="bold", loc="left", pad=14,
)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="x", labelsize=9.5)
ax.tick_params(axis="y", labelsize=9)
ax.yaxis.grid(True, linestyle="--", alpha=0.35)
ax.set_axisbelow(True)

# Annotate values on bars
for bar, v in zip(bars, values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1.5,
        f"{v}%",
        ha="center", va="bottom",
        fontsize=11, fontweight="bold",
        color=bar.get_facecolor(),
    )

caption = (
    "Source: Mozilla Foundation, *Privacy Not Included* — \"Romantic AI Chatbots Don't Have Your Privacy at "
    "Heart,\" Feb 14, 2024 (n=11 apps audited). Standalone reference point: Muah.AI breach Sept 2024 exposed "
    "1.9M accounts (Have I Been Pwned)."
)
fig.text(0.01, -0.01, caption, fontsize=8, color="#444", wrap=True)

plt.tight_layout()
plt.savefig(out_path, bbox_inches="tight", dpi=180, facecolor="white")
print(f"wrote {out_path}")
