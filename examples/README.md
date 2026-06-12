# Examples — the anchor set (restructured 2026-06-12)

Reference articles the pipeline reads before outlining and drafting. LLMs infer quality from real text far more reliably than from rules — this is the core insight of [Ryan Law's process](https://ahrefs.com/blog/how-i-do-content-engineering-with-claude-code/). But an anchor only works if it anchors the *right thing*. The old setup used five Ahrefs B2B-SEO articles as the *voice* anchor for a consumer adult-AI blog — the model got conflicting signals and fell back to generic AI prose. Each subfolder now anchors exactly one thing:

## `voice/` — how we sound (THE voice spec)

The brand's own best published work. `/draft` and `/quality-check` read 2 of these every run. Also read `_voice-notes.md` — it lists what to keep and what to avoid from these specific pieces (they are good anchors, not perfect ones).

**Promotion rule:** when the board grades a published article 9+/10, its final markdown gets added here (and the weakest existing anchor rotated out). The anchor set is supposed to get better over time. Never let it exceed ~5 files.

## `niche/` — what winning consumer content looks like (depth + structure, NOT voice)

Best-in-class consumer comparison/listicle content. Currently: Zapier's "best AI chatbot" roundup (~6,800 words — note the per-item depth: hands-on detail, screenshots, pricing specifics, a real comparison table, honest cons). Read for *how much substance a winning listicle carries*, never for voice (different brand, different audience).

## `structure/` — explainer/guide mechanics (NOT voice)

Ahrefs articles kept for their structural craft: BLUF section openers, MECE coverage, evidence placement, product-led demonstrations. Read when writing definitive guides and explainers.

## How the pipeline uses these

- `/outline` — 1 structure or niche example closest to the content type
- `/draft` — 2 from `voice/` (full read, every run) + 1 from `structure/` or `niche/` per content type
- `/quality-check` — 1–2 from `voice/` as the judgment baseline

## Customizing

Replace files freely — the pipeline favors examples over rules. If output should change, change the anchors.
