# Comparison / pricing / feature-grid table-cards — engine (LOCKED 2026-06-28)

`render_table_card.py` renders premium, ON-BRAND **table cards** for any `[VISUAL]` that is
fundamentally tabular. Rendered as HTML headless via **patchright** and screenshotted — the
exact same brand card as `render_chart_web.py`: white card (`#fff`, border `#EDF0F4`, radius 20,
soft shadow) on a `#F7F8FA` canvas, **IBM Plex Sans** title + **Geist** body (Google Fonts
`@import`), brand palette `#2E90FA #8B5CF6 #22B276 #F5A623 #E8655A`, and the **real Pleasur.ai
logo** bottom-right (bundled `scripts/pleasurai-logo.png` — charcoal "Pleasur." + blue ".ai",
never AI-drawn). Crisp real text — **never** a generative image model (they mangle in-image
text). Free, accessible, answer-engine friendly. Requires the container (patchright + chromium).

## Four modes (`spec.type`)
1. **comparison** — us-vs-competitor. `rows` = features, `columns` = products; `✓/✗/partial` or
   text cells; the OUR column is highlighted as a brand-blue "winner" card column.
2. **pricing** — plan/pricing matrix. `columns` = plans (`name/price/period/tagline`), feature
   rows, the popular plan highlighted, optional CTA-button row.
3. **grid** — a grid of feature cards (icon + title + desc).
4. **table** — a generic GFM table (`columns` = plain strings, `rows` = lists). The path
   `format-for-publish` uses for the PLEAA-567 GFM→PNG workaround. `yes/no/partial` → chips,
   inline markdown stripped. **Auto-detected** when `type` is absent and `columns` are strings.

## Usage
```bash
python render_table_card.py --spec spec.json --out out.png      # spec from a file
python render_table_card.py --data '<inline json>' --out out.png
# --logo defaults to the bundled scripts/pleasurai-logo.png
```

## Cell tokens (comparison / pricing / generic)
`check|yes|true|✓` → green ✓ · `cross|no|false|x|✗` → grey ✗ · `partial|limited|~` → amber half
· empty → blank · anything else → literal text. A cell can also be an object:
`{"icon":"check|cross|partial","text":"…","note":"…"}`.

## Spec schemas (compact)
```jsonc
// comparison
{"type":"comparison","title":"…","subtitle":"…","featureHeader":"Feature",
 "columns":[{"name":"Pleasur.AI","sub":"iOS · Android","highlight":true,"badge":"Best overall"},
            {"name":"Candy.ai"},{"name":"Replika"}],
 "rows":[{"feature":"Uncensored chat","note":"NSFW","cells":["check","check","cross"]},
         {"feature":"Starting price","cells":["$5.99/mo","$12.99/mo","$19.99/mo"]}]}

// pricing  (one column highlight:true = the popular plan; optional "cta")
{"type":"pricing","title":"…","columns":[
  {"name":"Free","price":"$0","tagline":"…"},
  {"name":"Premium","price":"$12.99","period":"/mo","tagline":"…","highlight":true,"badge":"Most popular"},
  {"name":"Ultimate","price":"$29.99","period":"/mo"}],
 "rows":[{"feature":"Daily messages","cells":["30 / day","Unlimited","Unlimited"]},
         {"feature":"AI voice calls","cells":["cross","check","check"]}],
 "cta":"Choose plan"}

// grid  (icons: chat heart image mic phone lock shield bolt sparkle infinity star palette
//        globe user video bell coin memory gift clock check; unknown → sparkle)
{"type":"grid","title":"…","columns":3,
 "items":[{"icon":"chat","title":"Uncensored chat","desc":"…","color":"#2E90FA"}]}
```

## Rules
- Always run through **VISUAL-CRITIQUE-LOOP.md** (render → check → fix → re-render): values match
  the source, labels legible, on-brand, nothing clipped.
- One highlighted column max (`"highlight": true`); add a `"badge"` for the ribbon.
- Pure deterministic text — the most accurate, accessible, answer-engine-friendly form for tables.
