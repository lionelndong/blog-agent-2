# Visuals adversarial review — ai-porn (second pass)

**Date:** 2026-05-07
**Reviewer:** Art director / adversarial pass (revision re-run)
**Prior verdict:** FAIL — density 7/10, 1 CRITICAL, 3 HIGH

---

## Counts

| Metric | Value |
|---|---|
| Article word count (prose only, excl. editor notes) | ~2,680 words |
| Density target band | 8–13 (target 10) for 2,000–3,000 word article |
| Floor (minimum acceptable) | 8 |
| Captured/rendered visuals | **10** |
| Manifest status=captured | 2 (screenshot-1, external-4-cnbc-city) |
| Pre-rendered image tags in draft (not in manifest) | 8 |
| Distinct types | **4** (`image`, `external`, `screenshot`, `chart`) |
| Type diversity target | ≥ 3 — Met |

**Rendered visual inventory:**

| File | Type | Section |
|---|---|---|
| external-1-cnbc-dutch-court-threatens-100.png | external | Intro |
| image-2-split-diagram-labeled-the-ai-p.png | image (concept-illustration) | §Definition |
| image-3-three-layer-architecture-diagr.png | image (diagram) | §How it's made |
| chart-1-ai-porn.png | chart | §How it's made |
| external-4-ccdh-research-report-grok-gene.png | external | §Ethical |
| screenshot-5-pleasur-ai-terms-of-service-pr.png | screenshot | §Ethical |
| screenshot-1-pleasur-ai-companion-creator-t.png | screenshot | §Walkthrough |
| external-4-cnbc-city-of-baltimore-sues-xa.png | external | §Legal |
| image-9-two-zone-diagram-titled-ai-con.png | image (concept-illustration) | §Legal |
| image-11-side-by-side-comparison-titled.png | image (diagram) | §Where it's going |

**Not counted:** Manifest indexes 2 and 3 (action-shot, status=manual — unfired placeholders, no `![...]` tag in draft).

---

## Findings

**[HIGH] F1 — Two action-shots still pending editor capture**

Manifest indexes 2 and 3 (Companion Creator personality step; in-chat selfie generation) remain status=manual. They are the highest-intent visuals in the article — the walkthrough section is the one place readers see the product in use. The rendered visual count (10) meets the density target without them, so this is not a CRITICAL density failure. But the walkthrough (§5) currently shows only the templates-grid screenshot and two `[VISUAL:]` prose placeholders with no image delivered. If those placeholders render as broken tags in production, the section degrades. Must be captured via `/capture-visuals ai-porn` before publish, or the placeholders removed from the draft prose.

**[MEDIUM] F2 — §Ethical screenshot (screenshot-5) missing selector**

The prior review flagged index 5 as a viewport-only capture lacking a CSS selector, meaning the prohibited-content section may not be visible. This file now appears as a `![...]` tag in the draft. The manifest entry is not present for screenshot-5 (it was pre-rendered separately), so its capture quality is unverifiable from the manifest. Editor should confirm the prohibited-content paragraph is legible before publish. If not, add `selector=` targeting the relevant heading and re-run.

**[LOW] F3 — §Where it's going diagram deviates from outline intent**

The outline marked §Where it's going as `{type: none}`, warning against speculative future-timeline graphics. The delivered image-11 is a concrete stack-comparison (Available Now vs. Arriving Next layer diagram), not a vague timeline — it earns its place on the merits. Noting for record; no action required unless editor disagrees on the distinction.

**[LOW] F4 — Intro external (external-1) remains marginal**

The CNBC Dutch court headline in the intro adds proof-of-citation value but the hyperlink already carries that. The visual is not harmful and the density count does not depend on it. No action required; keep if the editor prefers visible provenance in the intro, cut if trimming to exactly 9 is preferable.

---

## What improved since the prior run

- Chart (chart-1) added in §How it's made — closes the data-visualization gap and adds a fourth distinct type.
- Legal zone diagram (image-9) added in §Legal — replaces the failed WaPo external with a durable, earned concept-illustration.
- Baltimore CNBC external (external-4-cnbc-city) captured successfully in the manifest — the §Legal section now has a functioning external anchor instead of a broken placeholder.
- Stack comparison diagram (image-11) added in §Where it's going — concrete layer comparison, not the abstract timeline the outline warned against.
- Net density moved from 7 to 10, crossing both the floor (8) and the target (10).

---

**Verdict: PASS — density 10/10 (at target), distinct types 4/4 (≥3), no CRITICAL findings.**
