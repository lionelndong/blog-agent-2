# Diagrams — process flows / decision trees / flow charts (LOCKED 2026-06-28)

The **4th blog visual type** (alongside annotation, infographic, chart). For "how it works"
process flows, step sequences, and simple decision trees: **clean + structured + on-brand**,
deliberately DISTINCT from the hand-drawn infographic (crisp geometric cards, smooth connectors,
exact blog fonts).

Renders via **`render_diagram_web.py`** — **dagre.js** (the layout engine that powers Mermaid)
computes node coordinates + edge routing; we render the *look* ourselves: absolutely-positioned
HTML node cards (rounded cards, numbered badges, decision diamonds, terminal pills) over an SVG
edge layer (smooth rounded connectors + crisp triangle arrowheads + branch pills). Wrapped in the
**brand card** (same standard as `render_chart_web.py`): white card on `#F7F8FA`, IBM Plex Sans
title + Geist body (Google Fonts @import), the **real Pleasur.ai logo** in the footer, rendered
headless via patchright @2x and screenshotted tight. **`dagre.min.js` is bundled next to the
engine — no runtime CDN dependency.**

## When to use which type
| Type | Use for | Default direction |
|---|---|---|
| **linear** | a "how it works" / step-by-step process (steps + connecting arrows) | LR (horizontal) |
| **tree** | a decision tree / "which option fits you" (branching questions → outcomes) | TB (top-down) |
| **flow** | any flow chart with branches **and merges**, terminals, decisions | TB |
| **cycle** | a repeating loop — "how X works" as a feedback cycle (icons-in-pastel-circles) | (ring) |

## 1. Linear process (preset)
```
python render_diagram_web.py --type linear \
  --title "How Pleasur.AI works" --subtitle "From sign-up to a companion who knows you." \
  --data '[{"label":"Create your companion","desc":"Choose her look, voice, and personality."},
           {"label":"Start chatting","desc":"Message anytime — she remembers everything."}]' \
  --out diagram.png
```
`--data` = a list of strings, or a list of `{label, desc?, color?}`. Steps auto-number and cycle the
brand palette (blue → purple → green → amber); cards equalize to a uniform row. Use `--direction TB`
for a vertical checklist.

## 2. Decision tree (preset)
```
python render_diagram_web.py --type tree --title "Which experience fits you?" \
  --data '{"label":"What matters most?","children":[
            {"edge":"Conversation","label":"Want her voice?","children":[
               {"edge":"Yes","label":"Voice & Calls","desc":"Live voice + video."},
               {"edge":"No","label":"Text Chat","desc":"Unlimited messaging."}]}]}' \
  --out tree.png
```
Nested `{label, desc?, color?, edge?, tone?, children?}`. A node **with** children renders as a
**decision diamond**; a **leaf** renders as an **outcome card**.
- `edge` = the branch answer, shown as a **pill** on the connector.
- `tone` colours the **branch** only: `yes`→green, `no`→coral, `caution`→amber. Outcome-card colour
  is its OWN identity (`color`, else palette-cycled) — so a "No" branch never makes its outcome look
  bad. For a **preference** tree (options, not good/bad), **omit `tone`** → neutral connectors.

## 3. Flow chart (full spec — branches + merges)
```
python render_diagram_web.py --config spec.json --title "..." --out flow.png   # or: --type flow --data '<json>'
```
```json
{"direction":"TB",
 "nodes":[
   {"id":"a","shape":"start","label":"You send a message"},
   {"id":"b","shape":"process","label":"She reads the moment","desc":"Pulls history + memory."},
   {"id":"c","shape":"decision","label":"Safe & in character?"},
   {"id":"d","shape":"process","label":"Craft her reply","color":"#22B276"},
   {"id":"e","shape":"process","label":"Soften & redirect","color":"#F5A623"},
   {"id":"f","shape":"end","label":"She replies in seconds"}],
 "edges":[
   {"from":"a","to":"b"},{"from":"b","to":"c"},
   {"from":"c","to":"d","label":"Yes","tone":"yes"},{"from":"c","to":"e","label":"No","tone":"no"},
   {"from":"d","to":"f"},{"from":"e","to":"f"}]}
```
- **node** = `{id, label, shape, desc?, num?, color?}` — `shape`: `step | process | decision | start | end | outcome`.
  `process` defaults to brand blue so explicit green/amber stay *meaningful*; `step` cycles the palette.
- **edge** = `{from, to, label?, tone?, color?}` — `tone` colours the connector + pill. Two edges into
  one node = a merge; dagre routes and rounds it automatically.

## 4. Cycle (preset) — icons-in-pastel-circles loop
```
python render_diagram_web.py --type cycle --title "How your AI remembers you" \
  --subtitle "Every chat makes her understand you a little better." \
  --data '[{"label":"You chat","icon":"chat"},{"label":"It notes what matters","icon":"star"},
           {"label":"Saves to memory","icon":"chip"},{"label":"Recalls it later","icon":"sparkle"}]' \
  --out cycle.png
```
`--data` = a list of `{label, icon?, color?}`. Nodes sit on a ring with clockwise grey arrows; each is a
soft pastel circle (palette-cycled, or explicit `color`) holding a crisp line **icon**, with the label
beneath. Use it for a **loop** (the process feeds back on itself); use `linear` for a one-way sequence.
Keep it to **3–6 steps**. Icons (name → glyph): `chat message star note sparkle recall chip memory brain
shield privacy lock key heart user person database bell clock time search find bolt lightning bulb idea
check done eye phone call image gallery gear settings` — unknown name → a neutral dot. Add more as inline
SVG paths in the `ICONS` map in `render_diagram_web.py`.

## Theme (matches the brand card standard)
- Palette `#2E90FA #8B5CF6 #22B276 #F5A623 #E8655A`; connectors neutral `#B7BFCC`; yes=green, no=coral, caution=amber.
- Shapes: numbered step cards, colour-accent process cards, rounded decision diamonds, terminal pills, tinted outcome cards.
- Fonts: IBM Plex Sans (titles/labels) + Geist (body) — the live blog fonts.

## Rules
- Keep it **simple** — short node labels (diamonds hold ~3 short words per line), ≤ ~6 linear steps,
  shallow trees. This engine is for *clean process/decision visuals*, not dense graphs.
- Always run **VISUAL-CRITIQUE-LOOP.md**: every label fully inside its node (no clipping), arrows
  connect the right nodes, colours on-brand AND meaningful (not random), nothing overlaps, real logo present.
