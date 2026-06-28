# Cards — stat / quote / callout engine (LOCKED 2026-06-28)

The **fourth** visual type (after annotation, infographic, chart). Renders via
**`render_card_web.py`** — HTML headless in the browser (patchright), the `#wrap` element
screenshotted at 2×. Same **brand card standard** as `render_chart_web.py`: white card
(`#fff`, border `#EDF0F4`, radius 20, soft shadow) on `#F7F8FA`, **IBM Plex Sans** title +
**Geist** body (Google Fonts `@import`), the **real Pleasur.ai logo** (`pleasurai-logo.png`,
bundled next to the engine) bottom-right. No CDN at render except the font `@import`.

Use a card when the "visual" is really a **number, a sentence, or a tip** — text an image
model would mangle and a screenshot can't show. Crisp real text, answer-engine friendly,
accessible, free (no API spend).

## Usage
```
python render_card_web.py --spec card.json --out card.png
python render_card_web.py --json '<inline JSON>' --out card.png
```
`kind` in the spec selects the sub-type: `stat` | `quote` | `callout`. Optional `--logo`,
`--scale` (default 2). Every spec field is plain data — never a function — so it round-trips
safely from a manifest.

---

## 1. STAT — big number(s) + label
1–3 stats per card (auto-sizes: 1 → 76px, 2 → 54px, 3 → 44px). Each stat: a `value` (string,
formatted as you want — `"5,000"`, `"2.5×"`, `"<2s"`, `"92%"`), optional `unit`, `label`,
`icon`, a delta-trend pill, and a `sub` line.
```json
{
  "kind": "stat",
  "eyebrow": "Premium plan at a glance",
  "accent": "#2E90FA",
  "stats": [
    {"value": "5,000", "unit": "coins/mo", "label": "Included every month",
     "icon": "coins", "delta": "+25%", "trend": "up", "sub": "vs. Starter"},
    {"value": "2.5×", "label": "Longer average session", "icon": "heart",
     "delta": "+150%", "trend": "up"},
    {"value": "<2s", "label": "Median reply time", "icon": "zap", "sub": "p50 across chats"}
  ],
  "footnote": "Source / context (optional)"
}
```
- `trend`: `up` → green ▲, `down` → red ▼, `flat` → grey –. Override the colour with
  `tone`: `positive` | `negative` | `neutral` (e.g. churn `down` is *positive*).
- `valueColor` (per stat) tints the number; default is ink `#1E2430` (keep numbers dark and
  let the accents carry colour — more editorial).
- `width` optional (defaults 540 / 760 / 940 by stat count).

## 2. QUOTE — pull-quote + attribution
```json
{
  "kind": "quote",
  "style": "bar",
  "accent": "#2E90FA",
  "quote": "The full pull-quote sentence.",
  "attribution": {"name": "Jordan M.", "role": "Premium subscriber · 6 months",
                  "avatar": "JM", "avatarColor": "#8B5CF6"}
}
```
- **`style`** (default `bar`):
  - `bar` — editorial pull-quote with a brand left accent rule; the cleanest "blog quote" (Ahrefs-like). Avatar optional.
  - `mark` — oversized typographic quote glyph in the accent; reads instantly as a testimonial.
  - `review` — a 5-star `rating` row + an optional `attribution.source` chip ("App Store", "Trustpilot"). Best for real reviews / social proof.
  - `highlight` — wraps `highlight` (a substring of the quote) in a soft brand highlighter; emphasizes the key line.
- Quote text auto-sizes by length. `attribution` / `avatar` / `source` are optional — no avatar → just name/role. `avatarColor` defaults to `accent`.
- Use full names + a specific role, and keep it to one strong sentence (testimonial best practice).

## 3. CALLOUT — key-takeaway / tip / warning box
Accent rail + icon chip + label + text, with a faint accent wash.
```json
{
  "kind": "callout",
  "variant": "takeaway",
  "heading": "Lead with a question, not a pitch.",
  "text": "Body of the callout.",
  "footnote": "optional"
}
```
`variant` sets the default accent + icon + label (all overridable with `accent` / `icon` / `label`):

| variant | accent | icon | label |
|---|---|---|---|
| `takeaway` | `#2E90FA` blue | key | Key takeaway |
| `tip` | `#22B276` green | lightbulb | Tip |
| `success` | `#22B276` green | check-circle | Why it works |
| `warning` | `#F5A623` amber | alert-triangle | Warning |
| `info` | `#0891B2` cyan | info | Good to know |
| `note` | `#534AB7` indigo | pin | Note |

`heading` is optional (bold lead line); `text` is required.

---

## Icons (inline Lucide-style, themed to the accent)
`coins zap heart users trending-up trending-down clock star message-circle rocket gift percent
flame shield sparkles target key lightbulb alert-triangle info check-circle pin bar-chart calendar`
— unknown name → no icon (graceful). Add more by dropping a path into `ICONS` in the engine.

## Rules
- Brand palette only: `#2E90FA #8B5CF6 #22B276 #F5A623 #E8655A #0891B2 #534AB7`. Numbers stay
  ink `#1E2430`; colour lives in the eyebrow / icon chip / delta pill / rail.
- Fonts: IBM Plex Sans (title/number) + Geist (body). Real logo bottom-right. Card on `#F7F8FA`.
- Always run **VISUAL-CRITIQUE-LOOP.md** (Card checklist): every word spelled right and fully
  inside the frame, numbers match the source, deltas point the right way, on-brand, nothing clipped.
- Keep stat copy honest — if a number isn't a verified metric, mark it illustrative in the `footnote`.
