# Visuals Adversarial — how-to-make-an-ai-girlfriend

## Inputs

- Cited draft: `content-pipeline/6-drafts-cited/how-to-make-an-ai-girlfriend.md` (~2,400 words of article prose; 3,459 raw including editor notes)
- Annotated outline: `content-pipeline/4-outlines-annotated/how-to-make-an-ai-girlfriend.md`
- Manifest: `content-pipeline/images/how-to-make-an-ai-girlfriend/manifest.json`
- Manual-capture: `content-pipeline/images/how-to-make-an-ai-girlfriend/manual-capture.md`

## Measurements

- **Article word count:** ~2,400 (article prose, excluding editor notes block).
- **Density target band:** 2,000–3,000 words → **target 10, acceptable 8–13**.
- **Captured (`status=captured`) visuals:** **3** (image-1, image-2, external-4).
- **Distinct captured types:** **2** — `image`, `external`. Below the ≥3 diversity bar.
- **Outline planned vs. captured:** outline planned 6 (2 image + 2 table + 1 action-shot + 1 external). The DIY-vs-off-the-shelf comparison table is now an inline bulleted list (not a markdown table); the off-the-shelf comparison table is also rendered as a bulleted list, not a `| col |` block; the action-shot was deferred; the original outlined external (Stanford abstract) was swapped for Vice on Replika.

The article ships at **3/10** — five below target, and **two below the acceptable-range floor of 8**. By the rule (FAIL if density 2+ below target), this is automatic FAIL.

## Visuals that earn their place (the good)

- **image-1, intro decision diagram.** Anchors the article's load-bearing thesis (two paths, pick one) before the prose names them. Labels (`Rent A100 GPU ($0.72/hr)`, `Fine-tune Llama-3-8B with LoRA`, etc.) match the prose. Earns its place.
- **external-4, Vice on Replika 2023 ERP rollback.** Pairs with the "week-three failure / personality drift" beat and gives the reader a real artifact behind the claim. The crop is wide-but-shallow (2880×462) — readable, padded, sourced. Earns its place.

## Findings

### CRITICAL-1 — Density: 3/10. Article ships 5 below target, 2 below the acceptable floor.

The article currently has three captured visuals across ~2,400 words and six H2s. Long stretches of unbroken prose live in:

- **H2 "First decide which 'make' you mean"** (~340 words) — visual: none. The outline asked for a 6-row decision table; the draft rendered it as a bulleted list. **Add a real markdown `table` (Question / DIY path / Off-the-shelf path).** Type diversity win and matches the skim job the outline scoped.
- **H2 "The off-the-shelf path"** (~520 words, the article's longest section) — visual: none captured. The action-shot was deferred (acceptable per orchestrator note) but the section still ends with the cross-app pricing comparison rendered as bullets. **Add a real markdown `table` for the 5-app pricing comparison** (App / Body customization / Voice / In-chat image gen / Monthly price). Sourcing already lives inline; this is a re-render of existing content into the typed `table` form the outline asked for.
- **H2 "What 'good' actually feels like — and what breaks"** (~360 words) — has external-4 (Vice). Good. But the section also quotes the Stanford Replika numbers (90% / 43% / 3%) as standalone evidence with no visual. **Add `external` clipping `section.abstract` on the PMC article (Cerit et al.)** — the outline planned exactly this and it got dropped. The Vice external belongs where it is; this is additive, not a swap.
- **H2 "Choosing your path"** (~280 words) — visual: none. Argumentative-rhetorical, can default to `none` per the rule, but a tight `image` (sub=concept-illustration) showing the "DIY reader vs off-the-shelf reader" decision crystallization would earn its place and add type diversity without preaching. **Optional add.**

Minimum to clear FAIL: add the two `table`s + the Stanford `external`. That brings the article to 3 captured + 2 inline tables + 1 new external = **6 visuals across 4 distinct types** (`image`, `external`, `table`, plus the existing two `image`s). 6 sits inside the 6–11 acceptable range floor; 4 types clears the ≥3 diversity bar.

### CRITICAL-2 — Type diversity: 2 distinct captured types. Below ≥3 bar.

Resolved by CRITICAL-1's adds (tables + a second external = 4 types).

### HIGH-1 — `image-2` four-layer architecture diagram likely shipped with truncated prompt.

The `attrs.prompt` field in the manifest reads only `Four-layer architecture diagram for a DIY AI girlfriend build. Stack from bottom to top: "Compute layer — rented A100 GPU"`. The full intent (per `raw`) was four named layers — Compute / Model / Memory / Interface — with the Memory layer carrying a "the part every guide skips" accent badge that mirrors the prose. The truncation happened at the first `;` in the placeholder string (the prompt contained semicolons inside the layer labels, which collided with the `key=value;key=value` placeholder grammar). The captured PNG is likely either one-layer or hallucinated three remaining layers.

**Action:** re-run `/generate-visuals` for `index=2` with the prompt escaped (replace inner `;` with `,` or `|` so the parser doesn't split). Don't strip the entry — the diagram earns its place; it just needs to actually carry the four labels the prose references.

### HIGH-2 — Off-the-shelf walkthrough has no UI evidence (action-shot deferred).

Per the orchestrator note this is accepted — the manual-capture deferral is fine and the section can survive on the prose walkthrough plus the proposed pricing table. Confirming: **do not chase the Chrome MCP capture back**. The off-the-shelf path is the SERP's clearest existing pattern (every product page on rows 2/5/7/13/14/15 shows a similar wizard); the reader is not denied specific concrete information by its absence.

### LOW-1 — `manual-capture.md` still lists the deferred action-shot entry.

The entry at line 5 (`action-shot: Companion Creator personality and backstory step`) was already stripped from the cited draft and removed from manifest.json. The orphan in `manual-capture.md` is a stale breadcrumb that risks the editor chasing it on the next pass. **Action:** delete that entry from `manual-capture.md` (or annotate `status=deferred`) during the revision.

## Visuals to strip

None. All three captured visuals earn their place.

## Visuals to add (revision targets)

1. **H2 "First decide which 'make' you mean"** — `table` (DIY-vs-off-the-shelf decision table, 6 rows). Inline markdown; no asset file.
2. **H2 "The off-the-shelf path"** — `table` (5-app comparison, 4 feature columns + monthly price). Inline markdown; no asset file. Sources already cited in current prose.
3. **H2 "What 'good' actually feels like — and what breaks"** — `external` (PMC Cerit et al. abstract). Placeholder: `[VISUAL:type=external;sub=news-quote;url=https://pmc.ncbi.nlm.nih.gov/articles/PMC10955814/;selector=section.abstract;crop=padded;what=Stanford Replika user study abstract — 90% any loneliness, 43% severely lonely, 3% suicidal-ideation halt]`. Auto-capturable.
4. **`image-2` re-generate** — escape the inner semicolons in the prompt so the four-layer diagram actually renders four layers.

## Verdict: **FAIL**

CRITICAL count: **2** (density, type diversity — both resolved by the same revision set). HIGH: 2. LOW: 1. Strip: 0. Add: 3 visuals + 1 re-generate.
