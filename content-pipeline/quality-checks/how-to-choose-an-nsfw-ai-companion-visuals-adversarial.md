# Visuals Adversarial — how-to-choose-an-nsfw-ai-companion

Stage 9b re-run (re-verification after density fix). Skeptical art-director read of
visual placement against `templates/editorial-principles-visuals.md`.

## Computed baseline (verified on disk + in draft)

- **Body prose:** ~3,130 words → band **>3k** → density **floor 10, target 12**.
- **Visual count:** **9 image refs** (draft lines 21, 52, 64, 76, 90, 106, 122, 136, 156)
  + **2 GFM tables** (header-separator rows at lines 32, 149) = **11 info-bearing visuals**.
  - Counted from the draft's `![` image refs, NOT from manifest.json (the dispatcher's
    manifest lists only the most-recent batch; all 9 referenced PNGs exist on disk,
    113KB–1.3MB, no blank/truncated failures).
- **Type diversity:** concept-illustration/diagram ×5, screenshot ×2, chart ×1,
  external ×1, table ×2 = **5 distinct types** (≥3 required). PASS.
- **`manual-capture.md`:** "No manual visuals required" — clean fallthrough.

**11 ≥ floor 10 → density floor MET.** One below the soft target of 12. Not CRITICAL.
The prior FAIL (under-density) is resolved: 4 new SFW concept-illustration diagrams were
added at Criteria 1, 4, 7, 8 (memory real-vs-forget split, content-range spectrum,
real-gate vs checkbox-theater, use-case→platform match) — each carries information not
in the prose. Topic is 18+ but every visual is SFW; topic not flagged.

## Findings

**1. [LOW] Density at floor, not target.** 11 vs 12. A twelfth could be justified (e.g. a
small token-burn `chart` in Criterion 5) but every present visual earns its place, which
the principle values over a round number. Do not pad.

**2. [MEDIUM] Emergent second table not in the annotated outline.** Criterion 8 was specced
`{type: none}` in the outline. The draft added BOTH a 3-platform comparison table
(lines 148–152) AND the use-case-match diagram (image-4). The table is genuinely
info-bearing (only place the method is shown *applied* across named platforms with sourced
cost cells), so it earns placement — but C8 went from 0 planned visuals to 2. Flag so the
outline/draft divergence is a conscious call, not drift. Not harmful.

**3. [LOW] image-4 and the C8 table are adjacent and partially overlap.** Different axes
(table = named platforms + cost; diagram = device/discretion → platform-type), so not a
MECE violation — but two visuals in one ~200-word section is dense. image-4 is the weakest
visual (re-renders the prose list as glyphs); keep, but first to cut if preview feels crowded.

**4. [LOW] Two outline-cut diagrams reappeared — and now earn it.** The outline killed a
memory-test flow (C1) and an adult-range decision tree (C4) as table-column duplicates. The
draft's replacements are different artifacts: image-1-split-panel contrasts real-memory vs
no-memory *behavior*; image-2 is a content-range *spectrum* with the prohibited line marked.
Both carry new information. Net improvement, not regression.

**5. [LOW] Crop — screenshots are un-clipped full captures.** screenshot-2 (Creator, 1.3MB)
and screenshot-3 (Image Gen, 879KB) appear full-viewport; the outline names specific panels,
so a tighter selector-clip would serve the reader better on a future pass. Not blocking — they
show the right surface. external (228KB) and chart (114KB) are appropriately sized.

## Visuals that genuinely earn their place

- **chart-4 (Criterion 5, advertised-vs-real cost):** the article's primary information-gain
  made visible — the 3–4× bait-price gap in one glance, wired to exact sourced figures.
  Highest-value visual in the piece.
- **image-3 (Criterion 7, real-gate vs checkbox-theater):** carries the contrarian thesis
  (age-gate = green flag) as a labeled, MECE-clean comparison a reader absorbs faster than prose.
- **image-1-side-by-side (category boundary):** explains the mainstream-vs-companion
  distinction — the section's whole job — faster than the next paragraph.

## Six-question pushback

1. **Density** — MET at floor (11 ≥ 10), 1 below soft target. Not CRITICAL.
2. **Type diversity** — 5 types, ≥3 satisfied.
3. **Decorative/duplicate** — none actively decorative; image-4 weakest but distinct-axis.
4. **Wrong type** — none. UI→screenshot, concept→image, data→chart, cited artifact→external.
5. **Crop** — only screenshots un-clipped (Finding 5); no captured/external asset mis-cropped.
6. **Manual fallthrough** — clean; nothing wrongly requested.

## Summary

- **CRITICAL: 0** | HIGH: 0 | MEDIUM: 1 | LOW: 4
- Visual count: **11** (9 image assets + 2 GFM tables) vs floor 10 / target 12 — floor MET.
- Type diversity: 5 distinct types (≥3 required).
- **Strip:** none required. **Add:** none required (floor met; optional 12th is discretionary).
- Prior under-density FAIL is resolved; no actively-harmful visual.

## Verdict: **PASS**
