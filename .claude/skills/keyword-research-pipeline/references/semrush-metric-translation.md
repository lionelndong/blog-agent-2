# Semrush Metric Translation (the "be careful" gotcha doc)

> **Read this before touching any threshold in Layer 2 (BID) or Layer 5 (prioritization).** Ryan Law's method was tuned against Ahrefs' metric formulas. Semrush returns superficially-similar numbers that are scaled and computed differently. Transplanting Ahrefs thresholds without translation will silently degrade the gates — too lenient (everything passes) or too strict (everything fails).

Single source of truth for: Ahrefs ↔ Semrush metric mapping, threshold deltas, calibration math, and the "do not transplant" warning. Every BID / AIO / prioritization skill links here.

## The translation table

| Ahrefs concept | Semrush equivalent | What it means | Scale / range | Recalibration note |
|---|---|---|---|---|
| Domain Rating (DR) | Authority Score (AS) | Site-level authority | 0-100 | AS folds organic-traffic + backlink-quality + spam signals; DR is backlink-only. AS tends ~5-10 points lower for the same site. |
| URL Rating (UR) | Page Authority Score (Page AS) | Page-level authority | 0-100 | Roughly comparable; same recalibration logic as DR→AS. |
| Keyword Difficulty (KD) | Keyword Difficulty % (KD%) | Per-keyword competition score | 0-100 (KD); 0-100% (KD%) | **Semrush KD% is materially stricter than Ahrefs KD.** A keyword Ahrefs scores KD=60 will frequently be Semrush KD%=72-78. |
| Traffic Potential (TP) | Estimated Traffic / Top-Page Traffic | Expected organic traffic per article | absolute monthly clicks | Semrush has `traffic` per keyword (sum) and per page; not the exact "TP = traffic of #1-ranking page" Ahrefs concept. **Derive `traffic_potential` = traffic of #1 ranking page in `domain_organic_pages` for the keyword's #1 URL.** |
| Parent topic | KSB cluster id (preferred) / `first_keyword_group` (fallback) | Topical cluster | string id | **No 1:1 mapping.** Use Keyword Strategy Builder cluster id when available; fall back to `keyword_overview.first_keyword_group`. |
| SERP feature `ai-overview` | SERP feature `ai_overview` | AIO presence flag in SERP | boolean | Both expose the AIO flag. Naming differs by underscore/hyphen — pin the Semrush literal `ai_overview` in code, not the Ahrefs literal. |
| Brand Radar mentions (keyword-centric) | AI Toolkit AI Mentions (prompt-centric) | AI-search citation tracking | per-prompt, per-engine | **Different model entirely.** AI Toolkit tracks user-defined *prompts* against a panel of AI engines (AIO / ChatGPT / Gemini / Perplexity / Copilot). Brand Radar was per-keyword. The Layer 1c / Layer 3 skills are rewritten to the prompt-centric model. |
| Ahrefs intent label (heuristic) | Semrush intent classifier (`intents` array) | Per-keyword intent | array of: informational / navigational / commercial / transactional | Semrush's classifier is higher-quality and per-keyword. **Use it as the primary BID-Intent signal**; URL-pattern derivation is the fallback / tie-breaker. |
| Content Helper score | ContentShake AI score | Content optimization score | 0-100 (Helper) → 0-10 SEO + 0-10 Quality (ContentShake) | **Different scales.** "Score ≥ 90 win" target maps to "ContentShake SEO ≥ 8 AND Quality ≥ 8". Verify against published articles before locking. |
| Ahrefs Lite 50-doc/month cap | ContentShake API quota | Optimize-content rate-limit | API calls/month, plan-dependent | Replace doc-count budget with API-call budget. Cap pinned to `BLOG_AGENT_CONTENTSHAKE_MONTHLY_CAP` env (default 100). Same warn-80%/refuse-100% pattern. |

## Threshold deltas (BID Layer 2)

Apply these in `keyword-vet-bid/SKILL.md`. The derivation logic is unchanged — only the magic numbers move.

### BID-D (Difficulty) thresholds — DR → AS substitution

| Threshold | Ahrefs (legacy) | Semrush (current) | Justification |
|---|---|---|---|
| Default "within striking distance" | `dr_top10_median ≤ brand_DR + 15` | `as_top10_median ≤ brand_AS + 12` | AS is ~5-10pts lower for similar sites; tighten the gap by 3pts to keep gate equivalent strictness. |
| Calibration tighten (everything passes) | `≤ brand_DR + 10` | `≤ brand_AS + 8` | Same -2pt delta. |
| Calibration relax (nothing passes) | `≤ brand_DR + 25` | `≤ brand_AS + 20` | Same -5pt delta — relaxed gate stays a real signal. |
| Weak-link rule | top-10 page with `DR < (brand_DR + 5)` | top-10 page with `AS < (brand_AS + 4)` | One-pt tighten on weak-link to compensate for AS scaling. |

### BID-D KD threshold — KD → KD% substitution

| Threshold | Ahrefs KD | Semrush KD% | Justification |
|---|---|---|---|
| Default Layer 1b filter | `KD ≤ 60` | `KD% ≤ 70` | Empirically a 60→72-78 shift on the same query. Set 70 as median-correction default. |
| Auto-relaxed retry | `KD ≤ 80` | `KD% ≤ 85` | Same `+10pt-ish` band. |
| Tightening for niche brands | `KD ≤ 40` | `KD% ≤ 50` | Inherit the `+10pt` rule of thumb. |

### BID-I — Semrush intent classifier as primary signal

The legacy code derived intent from URL-patterns + title heuristics on the SERP top-10. The new approach:

1. **Primary**: read `intents` array from `mcp__semrush__keyword-overview`.
   - `informational` ∈ intents OR `commercial` ∈ intents (and not `transactional`/`navigational`-only) → `intent_match = PASS`
   - `transactional` is the dominant intent → `intent_match = FAIL`, reason `serp_is_transactional`
   - `navigational` is the only intent → `intent_match = FAIL`, reason `serp_is_navigational`
2. **Fallback** (when `intents` is empty / mixed-without-clear-dominant / disagrees with brand fit): the existing URL-pattern heuristic — same code, demoted to tie-breaker.
3. **Independent gate** (not in `intents`): tool-led detection from URL/title heuristic (paths like `/tools/`, `/calculator/`, `/generator/`; titles like "free X tool"). Tool-led keywords route to `tool-opportunities.csv`, not the writing queue.

`tool-led` is **not** a Semrush intent label. Don't try to derive it from `intents`.

## Threshold deltas (prioritization Layer 5)

Layer 5's existing weighted formula stays:

```
priority_score = 0.4 * traffic_score + 0.3 * brand_fit + 0.3 * product_fit
```

Three new column-driven boosts/penalties layer on top. Apply them in this order before clamping to ±2.0 redteam delta:

| Signal | Source | Boost / Penalty | Justification |
|---|---|---|---|
| `gap_mode = missing` | content-gap (Layer 1b) | +0.0 (default) | Classic "competitors rank, we don't" — already the default behavior. |
| `gap_mode = weak` | content-gap (Layer 1b) | +0.5 | Brand already ranks 11-20+; competitors top-10. Small effort to close. |
| `gap_mode = unique` | content-gap (Layer 1b) | +0.7 | Single competitor ranking; SERP shallow; one displacement away. |
| `gap_mode = strong` | content-gap (Layer 1b) | route to `cache/strong-positions.csv` (NOT writing queue) | Already won; signal not opportunity. |
| `gap_mode = common` | content-gap (Layer 1b) | -0.3 | Saturated SERPs are harder to differentiate on. |
| `source = aio_gap` | keyword-aio-gap (Layer 1c) | +1.5 | Existing boost preserved. AI-citation gap is doubly valuable. |
| `aio_sov_competitor_top` (top competitor's SoV ≥ 0.4) | keyword-aio-gap (Layer 1c) | tie-breaker on equal `priority_score` | Higher SoV-to-displace prefers higher rank. |
| `cluster_authority_gap = true` | derived from KSB cluster + brand domain | +0.5 | Brand has zero authority in cluster; cluster is low-difficulty. Keyword is the entry point to claiming the cluster. |
| `serp_intent = tool-led` | keyword-vet-bid (Layer 2) | +1.0, but ROUTED to tool-opportunities.csv | Existing routing preserved. The boost is recorded for triage; writing pipeline never sees these. |
| `redteam_priority_delta` | keyword-redteam (Layer 4) | applied after all of the above; capped ±2.0 by Layer 4 | Adversarial judgment is the final corrector. |

## Calibration discipline

The mechanical layers (BID, prioritization) need calibration on first run after migration AND after major brand-config changes. Calibration logs:

- `content-pipeline/0-keywords/cache/bid-calibration.log` — threshold drift, pass-rate trends
- `content-pipeline/0-keywords/cache/aio-calibration.log` — AIO score distribution, rubber-stamp detection

**The trip-wires** (the orchestrator should fire these, not me-the-skill):

- All rows pass BID → thresholds too loose. First-line tighten: raise `brand_fit` floor to 5, raise `product_fit` floor to 4, narrow KD% to ≤60, narrow AS gap to `brand_AS + 8`.
- Zero rows pass BID → thresholds too tight, OR Layer 1 produced a poor pool. Look at top FAIL reasons. If `dr_gap_too_wide` (now `as_gap_too_wide`) dominates, brand AS may be too low for current ambition — relax the gap to `brand_AS + 20` once and re-run. If `serp_is_transactional` dominates, Layer 1's seed/modifier mix is wrong — go back and adjust modifiers.
- All AIO scores ≥ 8 → scoring is rubber-stamping. Re-run with the contrarian addendum from `keyword-vet-aio/SKILL.md`.
- Zero AIO scores ≥ 5 → scoring is hallucinating. Spot-check 3 known-cannibalized queries against Semrush AI Toolkit's AI Response payload manually.

## "Do not transplant" warning (the user's call-out)

Three rules exist solely to defend against the migration foot-gun:

1. **Never copy an Ahrefs threshold into a Semrush skill without checking this doc first.** Look up the row in the table above; apply the recalibration delta. If the Ahrefs threshold is missing from this doc, **flag it and stop** rather than guessing.
2. **`mcp__ahrefs__*` is a bug, not a fallback.** Ahrefs is retired. If a skill calls a `mcp__ahrefs__*` tool, that's a leftover from migration and must be removed. Don't paper over Semrush quota errors by reaching back to Ahrefs — it's not configured anymore.
3. **Cache files from the Ahrefs era are footguns.** They have Ahrefs-shaped payloads. Migration explicitly wipes:
   - `content-pipeline/0-keywords/cache/aio-fetch/*` (Brand Radar payloads)
   - `content-pipeline/0-keywords/cache/competitors.json`
   - `content-pipeline/0-keywords/cache/competitor-keywords-raw.json`
   - `content-pipeline/0-keywords/cache/brand-dr.json` (regenerated as `brand-as.json`)
   - `content-pipeline/0-keywords/cache/aio-gap-*.json`
   - Any `cache/aio-fetch/*.json` written before the migration date
   The skills regenerate these on first run. If you see one of these files lingering with old data, delete it; don't trust its contents.

## Where this doc gets read from

- `keyword-vet-bid/SKILL.md` — BID thresholds (linked in the SKILL's process section)
- `keyword-vet-aio/SKILL.md` — AIO score interpretation
- `keyword-aio-gap/SKILL.md` — AI Toolkit prompt-centric model (the "different model entirely" note)
- `keyword-prioritization/SKILL.md` — boost/penalty weights (linked in the SKILL's autonomous-behavior section)
- `keyword-research-pipeline/references/bid-method.md` — the BID-method reference doc lifts the recalibration tables verbatim
- `optimize-content/SKILL.md` — ContentShake score interpretation

When updating this doc, propagate the change to those linked skills if the threshold logic moves; otherwise the linked skills will silently use stale thresholds.
