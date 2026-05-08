# Visuals Adversarial Review — ai-boyfriend (Pass 2)

**Reviewer:** Art Director (adversarial re-check after pass-1 remediations)
**Date:** 2026-05-07
**Article word count:** ~2,400 words (body only, excluding editor-notes section)
**Density band:** 2,000–3,000 words → target 10, acceptable floor 8
**Captured visuals (status=captured):** 10 (indices 1,2,3,4,6,7,8,10,11,12)
**Stripped:** 2 (indices 5 and 9)
**Distinct types (captured):** 4 — `chart`, `image`, `external`, `action-shot`

---

## Pass-1 HIGH Findings — Resolution Check

**HIGH #1 — Index 5 (pricing bar chart after comparison table, MECE violation)**
RESOLVED. Manifest status is `stripped`, reason `visuals_adversarial_HIGH_mece_violation`. Visual does not appear in the draft. The comparison table now stands alone in that section. No redundancy.

**HIGH #2 — Index 8 (Cybernews external, local HTML render)**
RESOLVED WITH ACKNOWLEDGED LIMITATION. Manifest `result.method: local_html_render`. The Cybernews headline, byline, and excerpt were extracted from the live page via Chrome JavaScript (cybernews.com blocks patchright DNS) and rendered as styled local HTML. Content accuracy is verified against the live page. The rendering method is a site-WAF constraint, not a fabrication — the underlying data is real and sourced. This limitation was surfaced in pass 1 and is accepted as the best attainable capture for this URL.

---

## Additional Strip Since Pass 1

**Index 9 (external-9 — Mozilla h1 clip), MEDIUM MECE violation**
Correctly stripped. Both index 9 and index 10 covered the same Mozilla audit data in the same section. Bar chart (index 10) retained; h1 clip stripped. No new MECE violation introduced — the privacy section now has one visual per distinct claim.

---

## Remaining Issues

**LOW — Index 8 rendering method (carried from pass 1)**
Local HTML re-render rather than live browser screenshot. Content verified accurate from live page. Site WAF prevents direct capture. Acknowledged constraint, not blocking.

No other issues identified. All 10 captured visuals appear in the draft at appropriate placements. No `[VISUAL:...]` placeholder tags remain in the draft. No section longer than ~600 words is visual-free. Type diversity is adequate (4 types). Density is 10, above the floor of 8 for this word-count band.

---

## Verdict: PASS
