# Visuals Adversarial — ai-girlfriend-experience (post-PLEAA-500 second pass)

Second adversarial pass after the prior FAIL. The §5 paraphrased
gpt-image-2 checklist (prior CRITICAL) was stripped and replaced with an
inline 5×4 markdown `table`. A new §3 `screenshot` of `pleasur.ai/generate`
was added. Verifying the prior CRITICAL is resolved and the additions hold.

## Computed inputs

- **Word count (cited draft, prose only — alt-text excluded):** ~2,600 words.
  `wc -w` reports 3,400 because alt-text inside `![alt](path)` is dense.
  Per the brief, prose-words density-band controls.
- **Density band:** 2,000–3,000 words → **target 10, acceptable range 8–13.**
- **Captured visuals:** 11 (10 PNG assets + 1 inline `table` per manifest
  index 11; indices 100–103 are stripped legacy entries).
- **Distinct types:** 5 — `image` (6), `screenshot` (2), `external` (1),
  `chart` (1), `table` (1).
- **Type diversity target (≥3):** met, with comfortable margin.
- **Density vs target:** 11 / 10 — at target, +1.
- **manual-capture.md:** "No manual visuals required." — clean.

## Prior CRITICAL verification

The prior CRITICAL was that gpt-image-2 paraphrased the §5 five-test
checklist into generic chatbot-eval categories (Clarity / Completeness /
Accuracy / Reasoning / Fit & Tone) — actively misleading readers. The
revision strips that asset (manifest index 102, `status=stripped`) and
substitutes an inline markdown `table` (manifest index 11) at draft lines
136–142. The table preserves the actual test names verbatim:
**Fictional-dog callback**, **Contradiction test**, **"I'm here for you"
count**, **Privacy-policy 2-minute read**, **Modality-stitch test** — same
names the prose uses below it, with a "what you do / what a pass looks like"
column pair. `table` is the canonical type for an N×M comparison
(visual-types.md decision step 3); no asset file is expected. **Prior
CRITICAL resolved.**

## Six-question framework

### 1. Density vs target

11 captured / 10 target → **+1, comfortably inside 8–13 band.** The intro
and conclusion each carry one image (legitimate per editorial rules).
§1 carries the stacked-components definition diagram. §2, §3, §4 each
carry two visuals (a primary + a supporting artifact). §5 now carries
the inline `table`. No section is starved.

### 2. Type diversity

**Five distinct types** — well above the ≥3 bar. The mix is
`image` (6) + `screenshot` (2) + `external` (1) + `chart` (1) + `table` (1).
The image lean is lighter than the prior pass (was 7 of 10, now 6 of 11)
and the new `screenshot` + `table` shift texture toward the ahrefs
reference.

### 3. Decorative visuals

The conclusion lifeline-graph (`image-6-a-simple-recap-illustration-sh.png`)
remains borderline — it restates the three-act arc with one new beat
(the Week-3 fork). MEDIUM rather than CRITICAL because the prose's "either
keeps up with you or repeats itself" is *itself* the fork, so the visual
is not load-bearing. Everything else earns placement: the §1 stacked-
components diagram has a "NOT THIS" contrast column doing definitional
work, the §3 memory side-by-side legibly distinguishes summarize-vs-
truncate, the §4 chart anchors the 28M→20M cliff.

### 4. Wrong type

No wrong-type findings. The §5 conversion from `image` to `table` is
correct: the section is genuinely a 5×N comparison and the table is the
canonical fit. The §3 `pleasur.ai/generate` capture is a real static-URL
product surface → `screenshot` is the right call.

### 5. Crop / framing

The new §3 `screenshot-1-pleasur-ai-in-chat-image-gener.png` lands on
the empty/blank state of `pleasur.ai/generate` — the prompt input,
20-coins meter, and four style chips (Portrait photo / Fantasy art /
Anime style / Cinematic) are visible, but **no chat thread and no recent
generations are visible**, despite the alt-text claiming "request form and
recent generations visible inside the chat surface." Minor mismatch with
the prose ("inside the chat thread" — the captured page is the standalone
generator, not the in-thread surface). HIGH below.

The Mozilla `external` is well-clipped (h1 padded), the §2 Companion
Creator screenshot lands on the Personality step, the chart's framing is
generous and readable. No other framing failures.

### 6. Manual fallthrough

`manual-capture.md` reads "No manual visuals required." — clean.

## Findings

### HIGH — §3 image-gen screenshot mismatches the alt-text and the prose claim

The new `screenshot-1-pleasur-ai-in-chat-image-gener.png` shows
`pleasur.ai/generate` in its empty default state — prompt box, style
chips, 20-coins meter, "Login / Join Free" in the corner. The alt-text
promises "request form and recent generations visible *inside the chat
surface*." Two problems: (a) no recent generations are visible (the
gallery / history is empty); (b) the §3 prose explicitly contrasts
"in-chat image generation" against competitors that "route image gen
through a separate page" — but the captured surface *is* the separate
page (`/generate`), not an in-chat thread. Either re-capture inside an
authenticated chat (an `action-shot` with a sent image-request and the
returned image visible) or rewrite the alt-text + caption to honestly
describe what's shown ("Pleasur.AI image-generation entry surface with
style presets"). Not strip-worthy as a real product capture, but the
alt/prose alignment is wrong.

### MEDIUM — Conclusion recap image still borderline decorative

`image-6-a-simple-recap-illustration-sh.png` (lifeline-graph forking at
Week 3) restates the three-act arc the prose has already summarized in
the paragraph above. Only new beat is the explicit fork at Week 3,
which the prose covers verbatim ("either keeps up with you or repeats
itself in six predictable ways"). Density floor doesn't demand it;
cleanest cut takes the article to 10 captured (still at target). Keep
if editor prefers the recap visual; it's not actively misleading.

### MEDIUM — §1 carries two images on a section the outline marked `Visual: none`

The outline self-check still claims §1 is `none` (foundational
definition argues with prose). The cited draft now carries the intro
three-act timeline *and* the §1 stacked-components diagram inside that
section. The stacked-components diagram earns its place — the "NOT THIS"
contrast column makes the MECE argument visually — but the outline
should be reconciled to reflect the upgrade rather than carrying a stale
self-check.

### LOW — Chart still has only 2 data points

`chart-3-character-ai-monthly-active-us.png` carries the 28M→20M cliff
on two markers. Reads as a slope, not a trend. A pre-peak third point
(if the dossier supports it) or an explicit "-28%" annotation would
upgrade this from "passes the bar" to "carries the section's hardest
evidence with confidence." Not strip-worthy; same finding as the prior
pass.

## What earns its place

- **§5 inline `table`** — correct type (5×4 comparison), preserves the
  actual test names (fictional-dog, contradiction, "I'm here for you"
  count, privacy-policy read, modality-stitch), and resolves the prior
  CRITICAL cleanly. Adds skim-able structure exactly where the section
  hands the reader a checklist.
- **§4 Character.AI MAU chart** — clean 2-point line, takeaway in the
  title, sourced (Business of Apps + Sacra), supports the BLUF.
- **§2 Companion Creator screenshot** — real product surface (Personality
  step, 2880×1800 patchright), matches the §2 walkthrough.
- **§3 Mozilla `external`** — clipped to the h1, supports the privacy-
  floor claim with a real third-party artifact.
- **§3 memory-architecture side-by-side image** — makes summarize-vs-
  truncate legible at a glance.
- **§1 stacked-components diagram** — definitional work the prose takes
  a paragraph to do, NOT THIS column does the MECE move.

## Verdict: **PASS**

Zero CRITICAL. Density at target (+1). Type diversity strong (5 types).
Prior CRITICAL resolved cleanly via the inline `table`. The HIGH on the
§3 screenshot/alt mismatch should be fixed before publish but is not a
ship-blocker (the asset is real, only the alt-text/prose alignment is
off). Two MEDIUMs are housekeeping.
