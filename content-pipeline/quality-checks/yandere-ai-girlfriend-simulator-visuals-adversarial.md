# Visuals Adversarial Review — yandere-ai-girlfriend-simulator

_Reviewed 2026-05-07 against manifest.json (8 captured, indices 0–7) and cited draft (~1,550 words)_

## Metrics

- **Word count:** ~1,550 words → bracket: 1,200–2,000
- **Density target:** 8 | Acceptable: 6–11
- **Captured visuals (manifest):** 8 — all status=captured
- **Distinct types:** 4 — `external` (×3), `chart` (×2), `image` (×2), `screenshot` (×1)

---

## Findings

**[HIGH] Index 0 and Index 3 share the `external-1-*` filename prefix.**  
Index 0 (itch.io, legacy) resolves to `external-1-external-visual.png`. Index 3 (Steam) resolves to `external-1-ai2u-on-steam-very-positive-re.png`. Both carry the `external-1` prefix. If the pipeline re-runs and re-sequences by manifest index, index 3 (the fourth visual, index 3) should be `external-3-*`. With index 0 flagged `legacy: true` and captured in a prior run, a re-run risks clobbering or confusing the two. The naming convention must be index-stable; index 0 should produce `external-0-*`.

**[MEDIUM] Index 0 uses a broken legacy relative path in the draft.**  
The itch.io external is embedded in the draft as `../images/yandere-ai-girlfriend-simulator/external-1-external-visual.png` — one directory level up from every other image reference, which use `images/yandere-ai-girlfriend-simulator/...`. The manifest flags it `legacy: true`. This path will break on Strapi upload or static-site resolution. It must be normalized to the same relative root as the other seven visuals before publishing.

**[MEDIUM] Index 5 (screenshot, Pleasur.AI) is the wrong type — should be `action-shot`.**  
The `what` caption is "personality field where you write the yandere archetype directly." The prose argues that you type in the yandere archetype as free text. A static headless capture of `pleasur.ai/create` on first load shows an empty form — the personality field will contain no text. Per the decision rule: "Could a developer paste a single URL into a fresh browser and see this state immediately?" — No; the populated state only exists after the user types. This should be `action-shot` with a goal that navigates to `/create` and types example personality text, so the visual actually shows what the caption claims. As captured, the screenshot likely demonstrates an empty form, making the caption inaccurate.

**[MEDIUM] Index 6 (chart — player engagement) mixes incommensurable metrics on one axis.**  
The chart plots itch.io ratings (286), itch.io comments (970), and Steam reviews (1,468) as if they are the same unit. Comments and ratings are different signals; the chart title ("Player engagement: itch.io vs Steam review volume") implies a like-for-like comparison that doesn't exist. The prose already states these numbers explicitly. Either restrict to a single metric type across both platforms or add per-bar unit labels. As-is the chart carries a mild misinformation risk for a skimming reader.

**[LOW] Index 6 (chart — player engagement) is misplaced by section.**  
This chart lives in the AI2U section, which is correct for the Steam review figure, but it also plots itch.io metrics from the prior section. A reader who has already passed the itch.io section will see itch.io numbers again without warning. Move the chart to sit immediately after the AI2U review claim, or split into section-local figures.

**[LOW] Index 2 (keyword chart) placement is after the how-to list, not after the search-volume claim.**  
The chart earns its place — it is concrete evidence for the "TikTok phenomenon / search volume" claim. However it appears after the numbered get-started list, three paragraphs after the claim it supports. Move it to immediately follow "Search volume for the phrase now exceeds what the active player base alone would generate."

**[LOW] Psychology section cites a PMC source that could carry an `external` visual.**  
The section quotes a specific academic article (pmc.ncbi.nlm.nih.gov) on attachment anxiety. A `sub=news-quote` external clipping the relevant abstract or finding would add concrete evidential weight alongside the concept diagram. Not a blocker; the section density is fine without it.

---

## Visuals earning their place

**Index 1 (yandere archetype concept diagram):** The etymology diagram — "yanderu" + "deredere" merging into dual output branches — explains the word-compound and its dual nature faster than prose can. It directly follows the BLUF, supports rather than replaces it, and the prompt is specific and label-explicit. Unconditional earner.

**Index 7 (real relationship vs. yandere fantasy side-by-side diagram):** The article's central analytical claim is that the yandere fantasy maps a real emotional need (total devotion, no abandonment) onto an obviously dystopian structure. The two-column diagram with matching sub-items and a shared label at the bottom makes this parallel structure scannable in one glance. Removing it would require three sentences of prose to replace. Strong earner.

---

## Verdict

## Verdict: PASS

Density is 8 (on target for 1,550 words). Type diversity is 4 (exceeds minimum of 3). No CRITICAL findings. Three issues require remediation before publish: normalize the legacy path on index 0 (MEDIUM), confirm the Pleasur.AI screenshot actually shows a populated personality field or re-capture as `action-shot` (MEDIUM), and fix the mixed-metric chart (MEDIUM). The filename prefix collision (HIGH) must be resolved to prevent a re-run from corrupting the asset set.
