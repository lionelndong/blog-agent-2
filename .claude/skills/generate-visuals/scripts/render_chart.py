#!/usr/bin/env python3
"""Render a chart PNG via matplotlib.

Reads a chart spec (data + style + title) and writes a 1200x720 PNG with
brand-neutral palette and labelled axes.

Standalone usage:
    python render_chart.py --title "Monthly searches" --style bar \\
        --out content-pipeline/images/<slug>/chart-1.png \\
        --data '{"Pleasur.AI": 235000, "Candy.ai": 410000, "RomanticAI": 88000}'

The --data argument can be:
  - inline JSON object (key->numeric)
  - inline JSON list of [label, value] pairs
  - path:KEY where path resolves to a JSON file relative to project root and
    KEY drills into nested keys (e.g. content-pipeline/1-research/<slug>.json:search_volumes)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]

DEFAULT_WIDTH_PX = 1200
DEFAULT_HEIGHT_PX = 720
DEFAULT_DPI = 120
PALETTE = ["#1a73e8", "#d97706", "#16a34a", "#9333ea", "#dc2626", "#0891b2", "#db2777", "#65a30d"]


def _resolve_data(spec: str) -> dict[str, float] | list[tuple[str, float]] | None:
    """Decode inline JSON, or path:KEY pointing into a JSON file."""
    spec = spec.strip()
    if spec.startswith("{") or spec.startswith("["):
        try:
            return json.loads(spec)
        except json.JSONDecodeError:
            return None
    # path:key.nested
    if ":" in spec:
        path_part, _, key_path = spec.partition(":")
        path = ROOT / path_part
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        for k in key_path.split("."):
            if k and isinstance(data, dict):
                data = data.get(k)
            else:
                return None
        return data
    return None


def _coerce_pairs(data: Any) -> list[tuple[str, float]]:
    if isinstance(data, dict):
        return [(str(k), float(v)) for k, v in data.items() if _is_numeric(v)]
    if isinstance(data, list):
        out: list[tuple[str, float]] = []
        for item in data:
            if isinstance(item, list) and len(item) == 2 and _is_numeric(item[1]):
                out.append((str(item[0]), float(item[1])))
        return out
    return []


def _is_numeric(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    return isinstance(value, (int, float))


def render(
    title: str,
    style: str,
    data_spec: str,
    out_path: Path,
    x_label: str | None = None,
    y_label: str | None = None,
) -> dict[str, Any]:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return {
            "status": "failed",
            "reason": "matplotlib_not_installed",
            "hint": "pip install matplotlib",
        }

    data = _resolve_data(data_spec)
    if data is None:
        return {"status": "failed", "reason": "invalid_data_spec", "spec": data_spec}

    pairs = _coerce_pairs(data)
    if not pairs:
        return {"status": "failed", "reason": "no_numeric_data"}

    labels = [p[0] for p in pairs]
    values = [p[1] for p in pairs]
    style_lower = style.lower()

    fig_w = DEFAULT_WIDTH_PX / DEFAULT_DPI
    fig_h = DEFAULT_HEIGHT_PX / DEFAULT_DPI
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=DEFAULT_DPI)

    if style_lower == "pie":
        ax.pie(values, labels=labels, colors=PALETTE[: len(values)], autopct="%1.0f%%", startangle=90)
        ax.axis("equal")
    elif style_lower == "line":
        ax.plot(labels, values, color=PALETTE[0], linewidth=2, marker="o")
        if y_label:
            ax.set_ylabel(y_label)
        if x_label:
            ax.set_xlabel(x_label)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
    else:  # bar (default)
        ax.bar(labels, values, color=PALETTE[: len(values)])
        if y_label:
            ax.set_ylabel(y_label)
        if x_label:
            ax.set_xlabel(x_label)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        for tick in ax.get_xticklabels():
            tick.set_rotation(20)
            tick.set_horizontalalignment("right")

    ax.set_title(title, fontsize=14, pad=14)
    fig.tight_layout()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fig.savefig(out_path, dpi=DEFAULT_DPI, bbox_inches="tight")
    except OSError as exc:
        plt.close(fig)
        return {"status": "failed", "reason": "write_failed", "error": str(exc)}
    plt.close(fig)

    return {
        "status": "captured",
        "path": str(out_path.relative_to(ROOT)),
        "style": style_lower,
        "data_points": len(pairs),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--style", default="bar", choices=["bar", "line", "pie"])
    parser.add_argument("--data", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--x-label", default=None)
    parser.add_argument("--y-label", default=None)
    args = parser.parse_args()

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = ROOT / out_path

    result = render(args.title, args.style, args.data, out_path, args.x_label, args.y_label)
    json.dump(result, sys.stdout)
    sys.stdout.write("\n")
    return 0 if result.get("status") == "captured" else 1


if __name__ == "__main__":
    sys.exit(main())
