# Infographic recipe — LOCKED 2026-06-28 (ndong-approved)

**Style: `hand-drawn-edu`** — hand-drawn *illustration* + **clean brand-sans** *text*.
Chosen over corporate-memphis / bold-graphic / isometric / craft-handmade. The imperfect
hand-drawn look is intentional; the text must stay clean (matches the blog).

## Two-step pipeline
1. **Generate** — `node infographic_engine.js --content c.json --out raw.png`
   Builds the hand-drawn-edu prompt from content and renders via Nano Banana
   (Replicate `google/nano-banana`, ~$0.10). `REPLICATE_API_KEY` is **mandatory — no fallback**
   (loud-fail if missing, per the no-silent-fallback mandate).
2. **Logo** — `python composite_logo.py --in raw.png --out final.png`
   Stamps the **real** Pleasur.ai logo (charcoal "Pleasur." + blue ".ai") bottom-right,
   deterministically. **Never let AI draw the logo.** Auto-downloads + caches the asset.

## Content schema (`c.json`)
```json
{ "title": "...", "subtitle": "...", "takeaway": "...", "aspect": "4:5 portrait",
  "items": [ {"icon":"camera","number":"500","label":"AI images","sublabel":"10 coins each","color":"blue"} ] }
```

## Rules
- **Illustration** hand-drawn; **TEXT** clean sans (Geist / IBM Plex — the blog fonts). Nano-Banana
  *approximates* the font; for pixel-exact Geist add a deterministic text layer (future).
- Macaron palette (blue #A8D8EA / mint #B5E5CF / lavender #D5C6E0 / peach #FFD5C2) + coral #E8655A
  numbers on warm cream #F5F0E8. Restrained doodles (no clutter).
- **Logo:** real asset only, via `composite_logo.py`. Blue ".ai" preserved; white half → charcoal on light canvas.
- **Layout varies per piece** — this 3-card breakdown is one layout; comparison / funnel / timeline
  come from different content (same style).
