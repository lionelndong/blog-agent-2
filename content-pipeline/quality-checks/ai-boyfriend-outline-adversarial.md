# Outline Adversarial — ai-boyfriend

Skeptical-expert read of `3-outlines/ai-boyfriend.md` for MECE coverage, BLUF discipline, problem→agitate→solution arc, SERP differentiation, and whether visuals earn their place.

## Verdict: **PASS**

Seven H2s, MECE, every opener carries a BLUF, and the arc moves what-is → features → comparison → build → privacy → health → close. It covers everything the top-5 SERP covers (definition, app comparison, pricing, free tiers, how-to) AND adds the two things none of them cover (privacy crisis, health/dependency with the China context). Structure is publishable. Findings are guidance for draft, not blockers.

## Findings

### CRITICAL
None.

### HIGH
- **H1 — Single visual is an `action-shot` requiring live Chrome capture.** In an unattended run with no browser MCP, this routes to manual and HALTS the visuals gate. The comparison section already specifies a table; the strongest information-carrying visual here is a rendered comparison **table-card** (matplotlib), which is generatable headless. Recommendation: demote the action-shot to `none` (the walkthrough is well-served by prose steps) and promote the comparison table to a typed `[VISUAL:type=table-card]` so the article ships with at least one real, legible asset. This respects "visuals earn their place" — the comparison table genuinely carries information; a creator screenshot is decorative product-marketing.

### MEDIUM
- **M1 — Boyfriend audience specificity.** The outline mirrors the ai-girlfriend structure but must write for the boyfriend reader (women 25–40 as lead adopters, the "texts you first" / emotional-attunement angle). Draft should not read as find-replace of a girlfriend article.
- **M2 — Cross-link parity.** Brief requires cross-linking to the gender-parallel ai-girlfriend content ("prefer an AI girlfriend? see …"). Outline notes the ai-girlfriend-simulator link; confirm it lands in both the "what is" section and the conclusion.

### LOW
- **L1 — Conclusion risks restating.** Close on one sharp new thought, not a recap (also flagged by quality-check on the v1 draft).

## What works
The privacy H2 is a true differentiator and is correctly sequenced after the build step (you've made something worth protecting → here's the risk). The problem→agitate→solution arc is intact across the whole piece, not just the intro.
