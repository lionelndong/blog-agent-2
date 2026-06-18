## Verdict: **PASS**

# Visuals Adversarial — ai-companion-pricing-guide-2026 (re-run after prior FAIL)

Re-run of stage 9b after the surgical visuals revision pass. Prior FAIL was (a) density below floor and (b) a decorative Candy AI external screenshot. Both are remediated.

## Computed baseline

- **Word count (cited draft):** ~4,944 → >3,000-word band → density target **10** (acceptable band 10–15).
- **Captured non-`none` visuals** (manifest `status=captured`): **9** — image ×4 (idx 1,4,5,9), chart ×4 (idx 2,6,8,10), screenshot ×1 (idx 7). The Candy AI `external` (idx 3) is correctly `status=stripped` and not counted.
- **Inline 16-row master comparison table** = +1 visual.
- **Total landed = 10** → meets the density target.
- **Distinct types:** image, chart, screenshot, table = **4** (≥3 required). PASS.
- **Naked `[VISUAL:...]` placeholders remaining:** 0.

## Findings

**1. [LOW] Density sits at the floor (10) of the 10–15 band.** Ten visuals across ~4,944 words clears the >3k target but is the bottom edge. Every substantive H2 carries a visual; the `none` sections (FAQ, How-to-Pay-the-Least checklist, Conclusion) are defensible (Q&A / argumentative / recap). Not a FAIL trigger — target met, not missed by 2+. (Note: annotated-outline self-checks still say "7 visuals / ~3,200 words" — stale vs. the real article; cosmetic.)

**2. [GOOD — compliance verified] pleasur.ai is framed as coin-metered everywhere.** Checked every label, alt, and table row:
- Model-distribution chart (idx 8) folds pleasur.ai into **Metered** (Flat 7 / Metered 3 / Freemium 5 / Free 1) — NOT Flat/Freemium.
- Image-1 (idx 1) and image-4 (idx 4) use a **generic "$9.99"** metered example; neither labels pleasur.ai as the flat side. Image-4's draining gauge (image −10 / voice −10 / call −50/min) describes the metered model generically.
- Master-table pleasur.ai row + screenshot alt + FAQ all scope "unlimited" to **text only**; media is coin-priced.
- No chart/diagram/screenshot frames pleasur.ai as flat / no-metering / unlimited. **No compliance issue.**

**3. [GOOD] Every charted figure is sourced.** Entry prices (idx 2), model distribution 7/3/5/1 (idx 8), annual savings Replika 71 / Candy 54 / pleasur.ai Starter 60 / Chai 20 (idx 10), hidden-cost ranges (idx 6) all trace to the research data JSON with aicompanionguides.com (Mar 2026) + pleasur.ai/pricing attribution. **No unsourced charted figure.**

**4. [GOOD — earns its place] Screenshot `screenshot-1-pleasur-ai-s-three-coin-tiers.png` (idx 7).** Strongest add of the re-run: first-party proof the coin tiers are *published* (the transparency thesis), where prose only asserts. Quality sane (2880×1800, stddev 0.18, auth_used), placed at the pleasur.ai breakdown.

**5. [GOOD — earns its place] Model-distribution chart (idx 8) + worked-calculation infographic (idx 5).** The chart turns "most charge flat, a handful meter, the rest are freemium" into a glanceable proportion; image-5 renders the headline arithmetic (5,000 ÷ 10 = 500 images, text = 0 coins) as a skim-able formula band carrying the information-gain section visually. Neither is decorative.

**6. [LOW] Decorative-risk audit — image-1 and image-4 lean conceptual but clear the bar.** Both are labeled flat-vector concept diagrams (not mood/lifestyle stock), each anchoring the flat-vs-metered distinction the whole piece is built on. They pass the "remove it — does the reader lose concrete information?" test. No strip recommended; no entry is purely decorative.

**7. [GOOD — remediation confirmed] Candy AI external stripped cleanly.** idx 3 = `status=stripped` (decorative duplication of the master-table Candy row), placeholder removed from the draft, master table still carries Candy's pricing. `manual-capture.md` says "no manual visuals required" — no manual fallthrough. No naked placeholder remains.

**Wrong-type / crop:** No wrong types (chart for distributions/prices, table for the 16-way comparison, screenshot for first-party UI, image for concept diagrams). Crop N/A for generated assets; the one screenshot is framed to the three-tier pricing grid (`target=pricing`).

## Summary

- **CRITICAL count:** 0
- **Density floor (10):** met (10 landed visuals)
- **Type diversity (≥3):** met (4 types: image, chart, screenshot, table)
- **Naked `[VISUAL]` placeholders:** 0
- **Compliance (pleasur.ai metered, charts sourced):** 0 issues
- **Strip/add recommendations:** none open

## Verdict: **PASS**
