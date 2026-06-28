# Research Adversarial — joi-ai-alternative-2026 (re-run)

Stage: research-adversarial (Phase 3 / PLEAA-418). Re-evaluation after the dossier
was revised to address 2 prior CRITICAL findings:
(1) circular affiliate corroboration of the Joi 115-char cap / Neurons-billing facts;
(2) zero keyword metrics this run not caveated on the beat spec.

Inputs reviewed: `1-research/joi-ai-alternative-2026.md` (revised),
`1-research/joi-ai-alternative-2026-deep.md`,
`1-research/joi-ai-alternative-2026-data.json`,
`0-context/joi-ai-alternative-2026.md`, `brand-config.md`.

## Verdict: **PASS**

## Resolution of prior CRITICALs

- **Prior CRITICAL (1) — circular affiliate corroboration. RESOLVED.**
  The new "⚠️ SOURCING CAVEAT" block (lines 82–91) is genuinely toothed. It (a)
  names the circularity explicitly ("two mutually-citing affiliate-review pages...
  inside ONE monetized affiliate ecosystem... treat the 'two sources' as
  effectively one"); (b) supplies SAFE phrasing that hedges ("Hands-on reviewers
  report a roughly 115-character limit... a cap Joi's own site doesn't publish, so
  verify it"); (c) supplies FORBIDDEN phrasing that bans assertion ("Joi AI caps
  messages at 115 characters" / "Joi charges 1,000 Neurons per companion"). The
  draft literally cannot state the cap or Neuron prices as Joi-published facts.

- **Prior CRITICAL (2) — uncaveated zero keyword metrics. RESOLVED (downgraded LOW).**
  The new "METRIC PROVENANCE" block (lines 160–165) marks metrics
  `[UNVERIFIED — Semrush units exhausted... ERROR 132]`, states volume/KD/CPC
  "were NOT pulled and must not be asserted," sources format targets from live
  competitor extraction, and reframes "Beatability: High" as a SERP-shape
  judgment, not a KD call. Per calibration, Semrush units exhausted is a known
  infra limit, not a dossier defect — honestly caveated, out-of-scope to fix
  without a unit top-up. **Not CRITICAL.**

## Remaining findings

- **HIGH — First-party fact trace (PLE-2330): live-fetch proof is self-asserted.**
  Every Pleasur.ai pricing/tier/coin/metering claim (12.99/27.99/49.99;
  1,500/5,000/10,000 coins; 10/10/50-coin actions; "no unlimited tier") carries
  `verified live https://pleasur.ai/pricing, fetched 2026-06-22` (lines 42, 65, 77)
  and reconciles against brand-config. The FACT-LOCK quarantine of the wrong
  $9.99/$19.99/"unlimited"/"no metering" figures (lines 54–75) is strong and
  neutralizes the poisoned `-deep.md`. Competitor prices are correctly NOT
  asserted first-party (hedged "verify current"). Not CRITICAL — live fetch
  asserted with date — but flagged HIGH because the proof is the dossier's own
  "matches brand-config exactly" assertion; no independent fetch artifact
  distinguishes "fetched and matched" from "copied brand-config and labeled it."

- **MEDIUM — Joi pain-point integers stored unflagged in data.json.**
  Prose (line 91) caveats "Do not present any of these as Joi-official," but
  `joi_ai_pain_points_attributed` in data.json stores `115`, `20`, `10`, `15` as
  bare integers; the only caveat is the top-level `_meta.note`. A downstream stage
  reading the key directly gets naked numbers.

- **MEDIUM — Surprise #2 ("Pleasur.ai absent from every list") is table-stakes.**
  Lines 132/172 frame our own absence as the information gain. Absence is the
  premise of every alternatives article, not an insight. Surprise #1
  (privacy/data-handling axis) and #3 ("how to actually switch off Joi") are
  genuine SERP gaps and hold. 2 of 3 surprises hold.

- **MEDIUM — Strongest competitor angle captured but BEAT-plan thin on voice.**
  Strongest top-5 angle is scribehow.com ("7 Best Joi AI Alternatives 2026") —
  first-hand "I tested across multiple sessions" voice + 7-col comparison table
  (lines 101/112). Dossier acknowledges it, says "match or beat it" (line 111),
  specs a table (line 169), but the only concrete BEAT lever is the privacy
  column; it defers the first-hand-credibility gap to post-publish outreach
  (line 174). Acknowledged > beaten on the voice dimension.

- **LOW — Data consistency (clean).** `pleasur_ai_pricing_live_usd_monthly`
  (12.99/27.99/49.99), `serp_benchmark.top3_median_words: 2500`,
  `beat_spec_target_words: 2800`, annual-equiv (5.20/11.20/20.00) all match prose.
  No mismatches. `market_context_attributed_scribehow` (337/128) correctly tagged.

## What works

The "⚠️ SOURCING CAVEAT" block (lines 82–91) is the model fix — a named-mechanism
diagnosis of the circular-affiliate problem paired with concrete SAFE-vs-FORBIDDEN
draft phrasing. A real, enforceable guardrail, not a label. Combined with the
honest METRIC PROVENANCE caveat and the strengthened FACT-LOCK quarantine, both
prior CRITICALs are genuinely resolved.
