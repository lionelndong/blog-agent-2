# Article cover / hero image — RECIPE (LOCKED 2026-06-28)

The **featured image** at the top of every blog post (and the card thumbnail + the OG/Twitter
share image — the site reuses one `coverImage` for all three). Fourth visual type, after
annotation, infographic, and chart. **Quality is #1** — covers must read Ahrefs-grade, never
"vibe-coded". Two routes; **route A (deterministic) is the default for consistency.**

## Dimensions — 1600×900 (16:9)

The blog uses **16:9** for the cover everywhere:
- article hero renders in an `aspect-video` box, `object-cover`, `priority` (blog-article-page.tsx)
- cards are `aspect-ratio: 16/9` (globals.css)
- the post's `og:image` + `twitter:image` both reuse `coverImage` (blog `[slug]/page.tsx`)

So the canonical asset is **1600×900** (exact 2× of the 800px content column → crisp, zero crop on
hero + cards, valid Twitter `summary_large_image`). The engine renders at 2× supersample and
LANCZOS-downscales for sharp text. Keep the title + logo inside a **centred safe-zone** so an
OG-side crop to ~1.91:1 (1600×838) never clips. `--width/--height` are configurable if a separate
1200×630 OG variant is ever wanted.

## Brand system (matches render_chart_web.py / CHART-THEME.md)

- **Palette** `#2E90FA` blue · `#8B5CF6` purple · `#22B276` mint · `#F5A623` amber · `#E8655A` coral
- **Title font = Plus Jakarta Sans 800** — the LIVE blog hero H1 font (`src/config/fonts/blog-display.ts`,
  "bold geometric sans, Ahrefs-style"). The cover title sits directly above the article H1, so it
  matches it. (This is a deliberate refinement over IBM Plex for the title.)
- **Eyebrow = IBM Plex Sans 700** (uppercase, letter-spaced, with a rule + dot). **Body/byline = Geist.**
  All three load via Google Fonts `@import` (the container reaches Google Fonts at render time).
- **Logo = the REAL wordmark**, composited deterministically, NEVER AI-drawn. Bundled
  `pleasurai-logo.png` (charcoal "Pleasur." + blue ".ai") is used on light covers; on dark covers the
  engine recolours the charcoal half to white at render time and keeps the blue ".ai".

## Route A — designed HTML cover via patchright (DEFAULT)

`render_cover.py` builds a designed HTML hero from a content JSON and screenshots it headless —
**no AI, pixel-exact text, fully reproducible, free, fast.** One design language, three themes
(a built-in style sampler), driven by a content object.

**Themes** (`--theme`): `gradient` (rich brand mesh, dark — bold/premium, default) · `light`
(airy editorial canvas — the most Ahrefs-like) · `spotlight` (near-black + a single accent glow —
moody, for emotional/concept topics).

**Motif** — a *designed* "app-tile" composition (NOT clip-art): a rounded squircle with a brand
gradient + the chosen icon, glossy highlight, reflection, concentric halo rings, two orbiting
feature chips, and sparkle accents. Reads as "a premium AI-companion app" — on-theme for the niche.

**Icon vocabulary** (`--icon`, Lucide stroke paths, MIT): `heart chat sparkles phone shield image
users star robot infinity`. **Auto-picked from the title** if omitted (memory→sparkles,
companion→heart, chat/sext→chat, call→phone, safety→shield, image→image, …).

**Content JSON**
```json
{ "title": "Best AI Girlfriend Apps", "eyebrow": "COMPARISON · 2026",
  "subtitle": "optional one-liner", "theme": "light",
  "accent": "blue|purple|mint|coral|amber" | "#RRGGBB",
  "icon": "heart", "author": "By Theo Hart" }
```
Only `title` is required. Title font-size auto-scales to length (no overflow).

**Run**
```bash
python render_cover.py --content cover.json --out cover.png
# or flags:
python render_cover.py --title "Are AI Girlfriends Safe?" --eyebrow "PRIVACY & SAFETY" \
       --theme spotlight --accent blue --icon shield --out cover.png
```

## Route B — AI illustration background, GATED + rare (REUSES `concept_illustration_engine.js`)

For the rare cover where an illustration genuinely beats a designed card. **No second AI engine** —
the cover's optional AI background reuses the existing gated AI lane (`concept_illustration_engine.js`
+ `concept_palette_check.py`; see `CONCEPT-ILLUSTRATION-RECIPE.md`, prompt taxonomy informed by the
`baoyu-cover-image` skill). **Hybrid by design so AI never touches text** (text is the #1 AI tell):
AI makes a *text-free* background; the deterministic layer adds the exact title + real logo.

1. **Generate** a text-free brand illustration at 16:9:
   `node concept_illustration_engine.js --content c.json --style luminous-dark --aspect 16:9 --out raw.png`
   (`luminous-dark` suits dark covers; `editorial-vector` suits light covers. `REPLICATE_API_KEY`
   mandatory, loud-fail. The metaphor is the whole craft — write it richly; ask for generous empty
   space on the left for the title.)
2. **Palette first-filter:** `python concept_palette_check.py --in raw.png` (`ok` / `WARN`).
3. **Composite** title + logo over it:
   `python render_cover.py --bg-image raw.png --title "…" --eyebrow "…" --accent purple --author "…" --out final.png`
   A legibility **scrim** darkens the left for the title and the **real logo** sits bottom-left —
   together they also cover any stray corner artifact. The motif is suppressed (the illustration is
   the visual).
4. **Hard vision gate** (VISUAL-CRITIQUE-LOOP.md → "Cover" + "Concept illustration"): cut on sight if
   it reads "AI", has artifacts / garbled text / a baked logo, a face, or is off-brand/generic. If
   unsure → fall back to route A.

> Proven 2026-06-28: `luminous-dark` "memory-constellation" (concept "How AI companions remember you")
> → palette `ok` → composited cleanly. Honest gate: **borderline** (the tiny memory tokens read a touch
> busy) — usable, but **route A stays the distinctive, consistent default**. (An earlier ad-hoc
> cover-only AI prompt even baked a literal "LOGO" placeholder — exactly why text + logo are always
> deterministic and the gate is mandatory.)

## Critique loop

Every cover passes `VISUAL-CRITIQUE-LOOP.md`: render → deterministic check (file exists, exact
1600×900) → **vision critique vs the Cover checklist** → fix → re-render, max 3, else flag a human
(never publish a bad cover). The v1→v2 iteration that produced the locked motif (halo rings +
confident orbiting chips + reflection, vs the first faint floating chips) is the loop in action.

## Running in the container

The HOST lacks patchright; render in the **container** (headless — no `DISPLAY` needed for our own
HTML). `render_cover.py` + `pleasurai-logo.png` must sit together (both bundled in `scripts/`).
```bash
C=paperclip-whwi-paperclip-1
docker exec $C bash -lc "cd <REPO>/.claude/skills/generate-visuals/scripts && \
  python3 render_cover.py --content cover.json --out /tmp/cover.png"
```

## Open follow-ups (not blocking this engine)
- Wire `type=cover` into the `generate_visuals.py` dispatcher (same pending step as the premium
  infographic/chart engines — they're all standalone until the unified dispatcher rewire +
  `BLOG_AGENT_VISUALS=on`).
- `format-for-publish`: upload the cover to Strapi media and set the Article `coverImage` field.
- Optional: a deterministic-text "illustrated" variant gallery; a 1200×630 OG-specific export.
