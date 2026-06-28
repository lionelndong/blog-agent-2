# Research Adversarial — pleasur-ai-vs-dondi-ai

Stage: 1b (research-adversarial) · Date: 2026-06-18 · Slug: pleasur-ai-vs-dondi-ai

Skeptical pushback on `content-pipeline/1-research/pleasur-ai-vs-dondi-ai.md` before
it feeds `/outline`. This run carries a GATE-ENFORCED claim-discipline brief
(`0-context/pleasur-ai-vs-dondi-ai.md`); the adversarial read checks the dossier
against those binding rules and flags any violation as CRITICAL.

## Findings

**1. [LOW] Citations — load-bearing claims are well-sourced.** Every Pleasur.ai
price, coin allowance, and per-action cost carries
`source: https://pleasur.ai/pricing (fetched 2026-06-18)`. Every Dondi figure
carries a named source or "Dondi's own homepage." Honest "0 / no data" volume
admissions cite Semrush reports. No uncited load-bearing numeric claim found. Soft
spot: context-neighbor volumes (line 27, "uncensored ai 22,200… nsfw ai reddit
5,400") cite `phrase_related` collectively but are decorative, not load-bearing.
Not a violation.

**2. [HIGH] Surprising findings are real but two of three collapse into one.**
The information-gain levers (lines 104–105, 134): (a) the uncensored-vs-billing
precision split, (b) a cited pricing-math walkthrough, (c) reviewers misquote
Pleasur's own pricing. (a) and (c) are genuinely surprising and citation-valuable.
(b) "do a pricing table with real numbers" is table-stakes for any comparison page,
dressed up as a gap. Net: two distinct surprises, not three.

**3. [LOW] Strongest competitor angle captured with a beat plan.** straight.com's
#1 Dondi ranking (https://straight.com, line 81) is not buried — lines 117–119 make
*conceding* it the trust mechanism that earns the citation. Correct GEO move,
captured as a how-to-beat, not a passive acknowledgement.

**4. [LOW] Data consistency — JSON matches prose; one benign orphan.** Spot-checks:
`pleasur_ai_monthly_price_usd` (12.99/27.99/49.99) = line 63 ✓;
`pleasur_ai_coin_cost_per_action` (image 10, voice 10, call 50/min) = line 64 ✓;
`dondi_ai_monthly_price_usd_range` (13–20, start 10) = lines 81–82 ✓. The
`pleasur_ai_starter_coin_budget_examples` key (150 images OR 150 voice OR 30
call-min) is JSON-only with no prose mirror yet — but it is exactly the worked-math
input the beat spec demands, correctly flagged "illustrative max." Acceptable.

**5. [LOW] Brand fit is strong, not a generic survey.** Thesis is Pleasur.ai-ownable:
"we are the source of truth for our own prices" (line 105) — a first-party angle no
affiliate can replicate. genfindr 7.6/10 used only as attributed (lines 85, 128). No
generic-survey drift.

**6. [LOW] First-party fact trace (PLE-2330) — PASSES cleanly.** Every Pleasur.ai
price/tier/coin/metering claim traces to `pleasur.ai/pricing (fetched 2026-06-18)`
recorded this run (lines 62–66, JSON `_meta`), with an explicit drift-check against
brand-config (line 67). Dondi claims correctly split: homepage → `dondi.ai (fetched
2026-06-18)`; review pricing → labeled "ATTRIBUTED INTEL, not first-party-verified
this run." No own-product claim leans on brief/memory alone. CRITICAL trigger NOT met.

**Gate-enforced claim-discipline checks (A–F):**
- **A [PASS]** — No flat-rate/unlimited/no-meter framing of Pleasur.ai. Line 65
  pre-empts its own "without limits" tag: "Do not read Pleasur.ai's own 'without
  limits' tag as an unlimited-media claim." Recommended angle (line 117): "not
  'cheaper' and not 'unlimited too'."
- **B [PASS]** — No two-way video claim; line 131 states "**NO two-way video**."
- **C [PASS]** — The two Dondi claims (uncensored = community-contested per
  r/Chatbots 1tj3w3s; unlimited-billing = NOT contested) kept strictly separate at
  every appearance (lines 73–74, 104, 128, 134). Never conflated.
- **D [PASS]** — Every Dondi fact attributed to a named source; "unlimited
  everything" labeled "Dondi's OWN copy" (line 71) / "Dondi's own homepage marketing
  claim" (line 127).
- **E [PASS]** — genfindr 7.6/10 appears only as an attributed genfindr rating; no
  invented numbers.
- **F [PASS]** — Beat spec (lines 121–137) is answer-first BLUF + cited comparison
  table + worked pricing-math + FAQ, targeting the GEO query set (line 135). Citable
  comparison page, correctly specified.

**7. [HIGH, not CRITICAL] Un-refetchable sources + 0-citation deep research is an
acceptable *carried* state at this stage.** straight.com 404'd, scribehow timed out,
Reddit is Firecrawl-blocked (line 59), deep research returned 0 citations (line 109).
For a page whose value proposition is *being citable*, shipping brief-attributed-only
competitor facts would be CRITICAL. But the dossier does not ship them — it labels
each "brief-attributed intel, NOT independently re-verified this run" and hands
URL-resolution to `verify-claims` (lines 59, 80–85). Honest, correct disposition at
research stage. It becomes CRITICAL only if `verify-claims` cannot resolve the exact
straight.com / scribehow / indiehackers / Reddit URLs before publish — the dossier
correctly makes that the gate, not this stage. Flagged HIGH so the run issue tracks
it as a hard pre-publish blocker.

## What works

The dossier refuses to invent demand: it records "0 / no data" volume honestly
(lines 12–17) and reframes success as AI-assistant citation share rather than
fabricating a ranking story. That intellectual honesty *is* the product here — a GEO
page that lies about its own volume would never earn the trust it's chasing.

## Verdict: **PASS**
