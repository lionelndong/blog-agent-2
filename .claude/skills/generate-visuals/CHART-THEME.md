# Charts — engine + skill (LOCKED 2026-06-28)

Charts render via **`render_chart_web.py`** (ApexCharts headless in the browser) with the
Pleasur.AI **brand theme** baked in (palette, IBM Plex, gradient fills, rounded bars, donut
center-total, clean card). `apexcharts.min.js` v3.49.1 is bundled next to the engine — **no
runtime CDN dependency**. The official **`apexcharts` skill** (`.claude/skills/apexcharts/`)
supplies correct configs for all 16 chart types.

## 1. Presets — the common cases
```
python render_chart_web.py --type bar|bar_h|area|line|donut \
  --title "..." [--subtitle "..."] --data '<json>' --out chart.png
```
`--data`: `{"Label":value,...}` or `[["Label",value],...]` or `path:KEY` into a JSON file.

## 2. Any of the 16 types — use the `apexcharts` skill
For scatter / heatmap / radar / treemap / candlestick / boxPlot / bubble / polarArea / rangeBar / rangeArea:
1. Use the **`apexcharts` skill** to build a correct ApexCharts options object (it has the
   data-format table + critical rules — the #1 source of chart mistakes).
2. Save the options as **JSON** (data + structure only — no function values; the theme adds formatters).
3. `python render_chart_web.py --config options.json --title "..." --out chart.png`

The renderer **deep-merges the brand theme UNDER your config** (your config wins on any key it
sets), applies value formatters, and wraps it in the brand card. Colors default to the brand palette.

## Rules
- Brand palette: `#2E90FA #8B5CF6 #22B276 #F5A623 #E8655A`. Font: IBM Plex Sans. Light card, Pleasur.AI mark.
- Always run through **VISUAL-CRITIQUE-LOOP.md**: numbers match the source data, labels legible, on-brand, nothing clipped.
- Supersedes the old matplotlib `render_chart.py` (kept only as a no-browser fallback).
