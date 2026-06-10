# Visuals adversarial — ai-sexting

Skeptical art-director review of visual placement for `ai-sexting`, against
`templates/editorial-principles-visuals.md` and `templates/visual-types.md`.

## Computed inputs

- **Cited-draft body word count:** ~2,213 words (excludes trailing Editor notes).
- **Density band** (2,000–3,000 words): target 10, acceptable range **8–13**.
- **Captured visuals in manifest (`status=captured`):** **8**.
- **Distinct types:** **3** — `image` (2), `chart` (3), `table`/table-card (3). Meets the ≥3 diversity bar.

So the article sits at the **floor of the acceptable band** (8) with full type diversity. Not thin, not padded.

## The 9-step "earns its place" pass — every visual

1. **Hero — `image` lifestyle (image-1).** Photoreal night-table still-life, no people, SFW. Earns the SERP/social click and sets the calm/private/adult mood the prose promises. Carries tone the prose can't. **Keep.**
2. **Search-trend chart — `chart` (chart-1 trend).** Real six-month US search-interest data, placed right after the "tens of thousands of searches a month" claim. Proves the demand claim with a number. **Keep.**
3. **Intent-cluster chart — `chart` (intent).** Real data showing the "what is it" head term dwarfs the commercial and is-it-cheating clusters. Justifies the entire informational angle and the cannibalization routing. Distinct information from #2 (composition, not trend). **Keep.**
4. **How-it-works flow diagram — `image` concept-illustration (image-2).** The single highest-value visual: makes the message → persona+memory → model → reply loop spatial, with a feedback arrow. All five labels render correctly, zero gibberish. Explains a concept faster than the paragraph beneath it. **Keep.**
5. **SERP page-type chart — `chart` (serp).** Real top-10 page-type mix (7 product pages, 2 roundups, 1 forum). Proves the thesis "the pages that rank are conversion funnels and app lists." Distinct from #2/#3 (what ranks, not how much/what intent). **Keep.**
6. **Comparison card — `table`-card (comparison).** Five dimensions, app vs general chatbot, legible brand-styled card (real text, no model gibberish). Scannable; carries the side-by-side the BLUF sets up. **Keep** — note: prose still introduces it, so it supports rather than repeats.
7. **Privacy checklist card — `table`-card (privacy).** Four checks with the "why it matters" column — adds the *reason* the bullet list above states tersely. Anchors the most actionable section. **Keep.**
8. **Getting-started steps card — `table`-card (steps).** Four-step setup at the top of the how-to section (after the BLUF). Skim-able spine for the section. **Keep.**

### Decorative check (strip candidates)
None. Every visual either proves a claim with sourced data (charts), explains a concept (flow diagram), structures a comparison/checklist (cards), or carries tone the explainer needs (hero). No lifestyle "happy user," no logo shot, no abstract "AI brain glow."

### Wrong-type / crop check
- The three data charts are correctly `chart` (real numbers, trend + two distributions) — not forced into prose or tables.
- The comparison, checklist, and steps are correctly `table`-cards (legible real text) rather than generative `image` (which would mangle the in-card copy) — the right call per the visual-types guidance.
- No full-page screenshots with buried detail. The one available product screenshot (`/create`) was **removed**, not shipped: the public page renders explicit preview imagery, which fails the SFW / ad-network rule and the adult-compliance constraint. Removing it (rather than chasing an auth'd interior state unattended) is correct; its informational job is covered by the steps card + the concept diagram + the prose.

### Under-density check
At 8 captured visuals the article is at the band floor, not below it. Diversity is satisfied (3 types). No H2 is left as a wall of prose: intro (hero), "what it is" (2 charts), "how it works" (flow diagram), "apps vs chatbots" (SERP chart + comparison card), "private & safe" (privacy card), "how to start" (steps card). The only sections without a dedicated visual are the short "is it cheating" ethics section (argumentative-rhetorical — correctly `none` per the rule) and the brief conclusion.

### Real-money note
Two generative (Replicate) images only — hero + flow diagram. The remaining six visuals are free (matplotlib charts and table-cards). This honors the run's frugality constraint while still hitting the density floor and type-diversity bar. Adding more generative concept-illustrations would raise spend without raising information density.

## Two visuals that genuinely earn their place

- The **how-it-works flow diagram** — it is the article's conceptual spine made visible, and the labels rendered perfectly.
- The **SERP page-type chart** — it turns the intro's rhetorical complaint ("every result wants to sign you up") into a verifiable bar chart from real data.

## Verdict: **PASS**

Density at band floor (8/8–13), three distinct types, zero decorative entries, every visual carries information the prose can't, all SFW and compliance-clean. No CRITICAL or HIGH findings.
