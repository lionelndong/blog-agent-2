# Visuals adversarial: build-a-girlfriend-body

**Run date:** 2026-05-08
**Slug:** build-a-girlfriend-body
**Word count:** 3,069 words (>3k band)
**Density target:** 12 (acceptable range 10–15)
**Captured (status=captured):** 7 — orig-1 (chart), orig-4 (chart), index-1 (image), index-2 (image), index-4 (image), index-5 (image), index-8 (image)
**Non-captured:** 5 — 2 mockup\_in\_place (action-shot), 2 manual (action-shot), 1 failed (external)
**Distinct types (captured only):** 2 — chart, image
**Distinct types (all non-none):** 4 — chart, image, action-shot, external

---

## Findings

**CRITICAL — C-1 — Density: 5 below target, three sections with zero captured visuals**

7 captured visuals vs. 12 target for a >3k-word article. Gap = 5. Three sections are effectively blank to the reader right now:

- **Age presentation, outfit, and the final preview** (340 words): one action-shot in manual-capture.md, nothing captured. The archetype-to-preview decision cycle is the section's concrete takeaway — a flow diagram earns a place here.
- **Walking the build: art style through body type** (520 words, >400-word rule applies): art-style action-shot pending as HTML comment; ethnicity is mockup only; body-types image-4 is the one captured entry. A 520-word section deserves a second captured visual.
- **Conclusion** (130 words): currently prose-only. Editorial principles permit one visual here; a compact 7-step reference card adds recall value without padding.

Suggested additions — all `image` sub=concept-illustration (fastest to capture, highest type-diversity lift):

1. **H2 Age presentation**: "Final preview trust-check flow" — a four-node decision loop: final preview → archetype reads right? → yes → proceed / no → fix archetype words → re-run
2. **H2 Walking the build**: "Realistic vs Anime output comparison" — two-panel diagram naming the visual differences (photorealistic skin / natural proportions / photography palette vs cel-shaded outlines / stylized proportions / saturated palette)
3. **H2 Seven decisions**: "Archetype anchor diagram" — three rows showing example archetypes ("athletic surfer", "soft librarian", "club promoter") each mapped to the decisions they drive (ethnicity, hair, outfit), illustrating why the 2–3 word anchor matters before anything else is picked
4. **H2 Conclusion**: "7-step decision reference card" — condensed horizontal pipeline of all seven decisions, labels only, as a final one-glance recall visual

Four additions bring captured to 11. At 11 captured, density is 1 below target → HIGH, not CRITICAL → PASS threshold met.

**HIGH — H-1 — Type diversity: 2 distinct types among captured visuals**

Captured-only types: chart and image. Target is ≥3. The pending action-shots (2 mockup\_in\_place, 2 manual) will add action-shot as a third type when they materialize via /capture-visuals; the failed external adds a fourth if retried. This resolves without the revision loop — it is a function of capture timing, not of missing placeholders. Flagged HIGH because the captured-article-as-shipped still looks narrow if action-shots are not captured before publish.

**MEDIUM — M-1 — Pew Research external (index-7) remains failed**

The `bounding_box_failed` reason indicates Playwright was blocked by Cloudflare. The entry is in manual-capture.md with the Claude-in-Chrome retry hint. Run `/capture-visuals build-a-girlfriend-body` and walk through this entry. If both paths fail, the HTML comment in the draft should be converted to a concept-illustration for the regulatory backdrop — the current chart-4 + image-8 pairing in that section is already strong; the Pew pullquote is supplemental, not load-bearing.

**LOW — L-1 — Walking the build has one HTML comment instead of a concept-illustration**

The art-style action-shot is correctly routed to manual-capture.md. The gap it leaves (no captured visual for the first wizard step) is partially covered by image-4 (body types), but the art-style decision is described in prose only. The Realistic vs Anime comparison diagram recommended in C-1 fills this gap without waiting on action-shot capture timing.

---

## What earns its place

**image-5 (Preset Card Compatibility Matrix):** the most useful single visual in the article. All 16 body-type × size-card pairings in one grid — green for clean renders, red for card-fights. No reader should burn forty regenerations to discover Slim+Large conflicts. This is what the SERP is missing and what the article is for.

**image-1 (7-step decision flow diagram in intro):** delivers the entire thesis in one glance before a single prose paragraph. A reader who sees only this image and the headline understands the article's value proposition. Properly placed after the intro's BLUF, not before it.

---

## Verdict: FAIL

Captured visual count (7) is 5 below the target of 12 for a >3k-word article. CRITICAL finding C-1 is open. Revision budget: 1 pass remaining.

**Revision action:** Add 4 `image` sub=`concept-illustration` placeholders at the H2s named in C-1. Run `/generate-visuals` for those 4 entries only. Expected post-revision captured count: 11 (1 below target → HIGH, not CRITICAL → PASS threshold met).

---

## Post-revision re-check (2026-05-08)

**Added 4 concept-illustrations:**
1. `image-1-archetype-anchor-diagram-title.png` (778KB) — H2 "The seven decisions": archetype anchor diagram, three example rows mapping 2–3-word archetype to downstream decisions
2. `image-2-two-panel-comparison-diagram-l.png` (798KB) — H2 "Walking the build": Realistic vs Anime two-panel comparison
3. `image-3-flow-diagram-titled-final-prev.png` (645KB) — H2 "Age presentation": final preview trust-check decision loop
4. `image-4-compact-horizontal-reference-c.png` (590KB) — H2 "Conclusion": 7-step reference card

**Post-revision captured count:** 11 (7 original + 4 new)
**Density:** 1 below target (HIGH, not CRITICAL)
**Type diversity (captured):** 2 types (chart, image) — HIGH from original run, unchanged by revision; resolves when action-shots are captured via /capture-visuals
**Open CRITICALs:** 0
**Open HIGHs:** H-1 (type diversity, resolves on action-shot capture)

## Verdict: PASS
