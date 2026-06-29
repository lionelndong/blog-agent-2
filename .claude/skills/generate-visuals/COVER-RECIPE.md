# Article cover / hero image — RECIPE (LOCKED 2026-06-28)

The **featured image** at the top of every blog post (also the card thumbnail + the post
`og:image`/`twitter:image` — the site reuses one `coverImage`). **Quality is #1.**

## Dimensions — 1600×900 (16:9)

Verified from the frontend: the article hero renders in an `aspect-video` box (`object-cover`,
`priority`); cards are `aspect-ratio: 16/9` (globals.css); the post `og:image`+`twitter:image` reuse
`coverImage`; the site-wide OG default is 1200×630. **Canonical asset = 1600×900** (2× the 800px
content column → crisp on hero + cards, valid Twitter `summary_large_image`). Keep key content inside
a centred safe-zone so an OG-side crop to ~1.91:1 never clips.

## The cover style (operator-chosen): Ahrefs-style flat-vector illustration

ndong's call, reviewing Ahrefs' real blog heroes (e.g. `ahrefs.com/blog/facebook-marketing-groups/`):
the cover is a **playful, characterful FLAT-VECTOR scene illustration** in the Ahrefs blog house-style
— bold uniform navy outlines, flat colour fills, friendly cartoon objects/scenes depicting the topic,
on a **bold brand-blue** background (`#2E90FA`; `white` variant available).

- **No fixed mascot** — scene/object-based (like Ahrefs' plug/laptop covers); the locked house-style +
  bold-blue bg + brand palette + logo chip are what make them one family ("same template, not the same").
- **No title text on the image** — the page H1 carries the title. (Verified in a page mock: the bold-blue
  cover sits cleanly next to the title in both above- and beside-the-title layouts — the blue is
  contained and doesn't clash with the dark title on the white page.)
- **No logo on the cover** (operator's call) — the cover is the clean illustration; branding comes from
  the page chrome + `og:title`. (`logo_stamp.py` can still stamp a white logo chip if ever wanted elsewhere.)
- **SFW** — covers are public + indexed, so topics are shown via friendly phones / hearts / chat
  bubbles / shields / sparkles / simple cartoon people. No nudity/suggestive/contact, ever.

This is **AI-generated** (Nano Banana / Replicate) — a deliberate operator override of the
"deterministic-default" rule **for covers**, because the characterful illustration beats a designed
card. It MUST pass the **hard SFW + no-slop vision gate** (VISUAL-CRITIQUE-LOOP.md → "Cover"). The
deterministic line-art engine (`render_cover.py`) stays as a free fallback.

### Pipeline (primary)
1. **Generate** — `node cover_hero_engine.js --content c.json --out raw.png`  (or `--title "…" --bg blue`)
   Locked Ahrefs house-style + a per-topic **`scene`** (the creative variable; derived from the title
   if absent) → Nano Banana, 16:9. `REPLICATE_API_KEY` mandatory (loud-fail). `c.json`:
   `{ "title", "scene"?, "bg"? ("blue"|"white") }`.
2. **Finalize (resize)** — `python logo_stamp.py --no-logo --in raw.png --out cover.png`
   Resizes to **1600×900**. **No logo on covers** (operator's call) — branding comes from the page + og:title.
3. **Hard vision gate** — look at the PNG vs the Cover checklist: **cut** if it reads "AI"/slop, is
   off-brand, **NOT SFW**, garbled, or has any stray text/wrong logo. Max 3 re-rolls (refine the
   `scene` wording), else fall back to route-line-art. A bad cover never ships.

### The craft (what makes or breaks it)
- The **`scene` is the only creative variable — and it's the whole game.** Write it richly, literally,
  cheerfully, SFW. Describe WHAT objects/characters do; the finish (flat vector, bold blue, outlines)
  is locked in the engine — don't put finish words in the scene.
- Bold-blue is the default (verified not to clash with the adjacent title); `--bg white` is the lighter
  variant for rhythm in the feed.

## Fallback — deterministic line-art (`render_cover.py`)

Free, no-AI, reproducible. An editorial **line-motif** system: 4 themes (`light` default / `dark`
Linear / `aurora` / `bold` Sam-Marsh) × 6 auto-picked motif layouts (cluster/orbit/thread/wave/radial/
grid) × 5 accents, with the title composited on. Use when AI is unavailable/undesired, for a quick
draft, or if the gate cuts the illustration 3×. `python render_cover.py --title "…" --eyebrow "…" --out c.png`.

## Critique loop
Every cover passes `VISUAL-CRITIQUE-LOOP.md` (render → deterministic check: exists, 1600×900 → **vision
critique vs the Cover + Concept-illustration checklists** → fix → re-render, max 3, else flag a human).

## Running in the container
The HOST lacks node/patchright; run in the **container** (`paperclip-whwi-paperclip-1`). The engine +
`logo_stamp.py` + `pleasurai-logo.png` live together in `scripts/`. Replicate key via Doppler
(`REPLICATE_API_KEY`); inject with `docker exec -e REPLICATE_API_KEY=…`.

## Open follow-ups (not blocking)
- Wire `type=cover` into `generate_visuals.py` (generate → stamp → gate) + `BLOG_AGENT_VISUALS=on`.
- `format-for-publish`: upload the cover to Strapi media and set the Article `coverImage`.
