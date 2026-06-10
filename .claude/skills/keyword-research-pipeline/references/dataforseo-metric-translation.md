# DataForSEO Metric Translation (the "be careful" gotcha doc)

> **Read this before touching any threshold in Layer 2 (BID), Layer 3 (AIO), or Layer 5 (prioritization).** The pipeline was originally tuned against Ahrefs-style metrics, then partially rewritten for Semrush. DataForSEO returns similar-looking keyword, SERP, and domain fields, but they are not the same scoring systems. Transplanting Ahrefs or Semrush thresholds without translation will silently degrade the gates: too lenient, too strict, or built on the wrong signal.

Single source of truth for: DataForSEO endpoint mapping, metric semantics, threshold deltas, skipped capabilities, and the "do not transplant" warning. Every BID / AIO / prioritization skill should link here before applying numeric gates.

Primary docs:
- Keyword Overview: https://docs.dataforseo.com/v3/dataforseo_labs-google-keyword_overview-live/
- Keyword Suggestions: https://docs.dataforseo.com/v3/dataforseo_labs-google-keyword_suggestions-live/
- Keyword Ideas: https://docs.dataforseo.com/v3/dataforseo_labs-google-keyword_ideas-live/
- Competitors Domain: https://docs.dataforseo.com/v3/dataforseo_labs-google-competitors_domain-live/
- Domain Intersection: https://docs.dataforseo.com/v3/dataforseo_labs-google-domain_intersection-live/
- Google Organic SERP Advanced: https://docs.dataforseo.com/v3/serp-se-type-live-advanced/

## The translation table

| Pipeline need | DataForSEO source | What it means | Scale / range | Recalibration note |
|---|---|---|---|---|
| Keyword volume | Labs `google/keyword_overview/live` (`keyword_info.search_volume`) | Provider-estimated monthly Google demand for a keyword in the selected location/language | absolute monthly searches | Use US `location_code=2840`, `language_code=en` for Pleasur.ai unless a brief says otherwise. Do not mix Google Ads `search_volume/live` rows into the vetted queue unless Labs overview is unavailable and clearly labeled fallback. |
| Keyword Difficulty | Labs `google/keyword_overview/live` (`keyword_properties.keyword_difficulty` or `keyword_difficulty`) | DataForSEO estimate of top-10 ranking difficulty | 0-100 | Treat like a distinct DataForSEO KD, not Semrush KD%. Start with the Semrush-era `<=70` collection ceiling only as a migration guardrail, then calibrate pass rates from the first run. |
| Search intent | Labs `google/keyword_overview/live` (`search_intent_info`) | Per-keyword intent classification/probability | informational / navigational / commercial / transactional, with probabilities when returned | Primary BID-I signal. Fall back to SERP URL/title shape only when `search_intent_info` is missing or ambiguous. |
| Keyword expansion | Labs `google/keyword_suggestions/live`; supplement with `google/keyword_ideas/live` | Suggestions contain the seed phrase; ideas are category/relevance expansion | keyword rows with keyword_info/search_intent_info | Use suggestions for seed+modifier coverage, ideas for broader category discovery. Dedupe before overview enrichment. |
| Question mining | Labs `google/keyword_suggestions/live` client-filtered to question words; SERP Advanced `people_also_ask` / question item types | Question-shaped search demand and PAA strings | keyword rows plus SERP feature items | DataForSEO does not expose a Semrush Keyword Magic "Questions" mode. Filter suggestions by who/what/when/where/why/how/can/does/is/are/best/free, then enrich with PAA from SERP. |
| Competitor discovery | Labs `google/competitors_domain/live` | Domains with ranking overlap against Pleasur.ai | domain rows with intersections and organic metrics | Use to choose 1-3 competitors. Cache the chosen competitor set for the run. |
| Competitor gap | Labs `google/domain_intersection/live` | Keywords where a competitor and Pleasur.ai intersect, or where competitor ranks and Pleasur.ai does not (`intersections=false`) | keyword rows with rank/search metrics | DataForSEO has no Semrush five-mode Keyword Gap labels. Map `intersections=false` rows to `gap_mode=missing`; map rank gap rows from intersections to `weak` when Pleasur.ai is outside top 10 and competitor is top 10. Do not invent `unique/common/strong` unless the data supports it. |
| SERP top-10 | SERP API `serp/google/organic/live/advanced` | Live Google results and SERP feature items | ordered SERP item list | Use organic items for top-10 shape, tool-led detection, PAA extraction, and AIO presence. Live SERP costs per task; batch only the candidates needed for gates. |
| Per-URL/domain strength | SERP Advanced item rank metadata plus Labs rank/domain endpoints when needed (`ranked_keywords`, `domain_rank_overview`, `bulk_traffic_estimation`) | Ranking/traffic context for URLs/domains | provider-specific counts/traffic estimates | DataForSEO does not provide Semrush Authority Score. Do not keep `as_top10_median` or `dr_top10_median` as if sourced. For the first DataForSEO run, use KD + weak SERP-shape signals; add a dedicated authority calibration later only after validating the field. |
| AI Overview presence/body | SERP Advanced `ai_overview` item and references | Whether Google returned an AI Overview and the body/references DataForSEO exposes | item type `ai_overview`, related references | `ai_overview` is the literal item type. If no item is returned, record `has_aio=false` for that observed SERP. If body is absent, keep `aio_body_source=serp_ai_overview_item` and score only from available text/reference coverage. |
| Multi-engine AI citation gap | None | Semrush AI Toolkit-style ChatGPT/Gemini/Perplexity/Copilot citation share | not available | **SKIPPED.** DataForSEO does not replace multi-engine LLM citation tracking. Do not fake `aio_gap` rows or `aio_sov_competitor_top`. |
| ContentShake scoring | None verified | External SEO/quality score from Semrush ContentShake | not available | Treat `/draft-score` and `/optimize-content` external scoring as optional soft-fail. Keep deterministic quality checks, judgment rewrite, voice-drift rollback, and claim verification. |

## Threshold deltas (BID Layer 2)

The BID logic remains: Business potential, Intent, Difficulty. Only the metrics feeding it change.

### BID-D (Difficulty) thresholds

| Threshold | Semrush-era value | DataForSEO migration value | Justification |
|---|---|---|---|
| Collection ceiling | `KD% <= 70` | `keyword_difficulty <= 70` as a temporary migration ceiling | Same nominal scale, different formula. Keep only until the first two DataForSEO runs produce pass-rate logs. |
| Tighten if everything passes | `KD% <= 60`, AS gap `brand_AS + 8` | `keyword_difficulty <= 55`, require at least two weak SERP-shape links | DataForSEO KD can be sparse for long-tail terms; tighten both KD and observed SERP weakness. |
| Relax if nothing passes | `KD% <= 85`, AS gap `brand_AS + 20` | `keyword_difficulty <= 85`, but only for high brand/product fit rows | Do not relax low-fit candidates into the queue just because demand exists. |
| Weak-link rule | AS < `brand_AS + 4` | count top-10 results with forum/UGC/thin-tool/result-list pages OR low-quality exact-match pages | No validated Authority Score equivalent. Use SERP shape as a temporary weak-link signal, label it `weak_link_count_source=serp_shape`. |

### BID-I -- DataForSEO search intent as primary signal

1. **Primary:** read `search_intent_info` from Keyword Overview.
   - informational or commercial dominant -> PASS
   - transactional dominant -> FAIL, reason `serp_is_transactional`
   - navigational dominant -> FAIL, reason `serp_is_navigational`
2. **Fallback:** classify the SERP top-10 from SERP Advanced organic URLs/titles when `search_intent_info` is missing.
3. **Independent route:** detect tool-led SERPs from `/tools/`, `/generator/`, `/calculator/`, or "free X tool" in top results. Route to `tool-opportunities.csv`; do not send tool-led rows into the article queue.

## Threshold deltas (AIO Layer 3)

| Signal | DataForSEO source | Gate behavior |
|---|---|---|
| No `ai_overview` item in SERP Advanced | SERP `items[].type` | `has_aio=false`, `aio_verdict=PASS` |
| `ai_overview` item present but thin/no useful body | SERP item only | `has_aio=true`, `aio_verdict=RISKY`, because click risk is unknown |
| `ai_overview` item present with direct-answer body that fully satisfies the query | SERP item body/text fields when returned | `aio_verdict=FAIL_CANNIBALIZED` unless query is commercial-investigation or tool-led |
| DataForSEO error/rate limit | API status or task status | `aio_verdict=UNKNOWN`, do not publish queue rows as PASS unless the run ledger records the failure and retry posture |

## Threshold deltas (prioritization Layer 5)

Layer 5's base weighted formula stays:

```text
priority_score = 0.4 * traffic_score + 0.3 * brand_fit + 0.3 * product_fit
```

Apply DataForSEO-safe boosts only from observed columns:

| Signal | Source | Boost / penalty | Justification |
|---|---|---|---|
| `gap_mode=missing` | domain_intersection with `intersections=false` | +0.4 | A competitor ranks and Pleasur.ai does not. |
| `gap_mode=weak` | domain_intersection with both domains ranked and Pleasur.ai outside top 10 | +0.5 | Small-effort displacement opportunity. |
| `gap_mode=seed_modifier` | keyword_suggestions / keyword_ideas | +0.0 | Default pool expansion. |
| `gap_mode=question_mining` | suggestion question filter / PAA | +0.3 | Better fit for snippets and answer-engine citation readiness. |
| `source=aio_gap` | unavailable | **do not apply** | Multi-engine AI citation tracking is skipped. |
| `aio_sov_competitor_top` | unavailable | **do not apply** | No DataForSEO equivalent. |
| `serp_intent=tool-led` | SERP shape | route to `tool-opportunities.csv` | Tool-led keywords should become product/tool work, not blog articles. |
| `redteam_priority_delta` | Layer 4 | apply after all boosts, capped +/-2.0 | Judgment remains the final corrector. |

## Calibration discipline

Write calibration logs under `content-pipeline/0-keywords/cache/`:

- `dataforseo-smoke-results.json` -- endpoint status, task count, cost, and observed fields
- `dataforseo-run-summary.md` -- run-level source/cost/queue summary
- `bid-calibration.log` -- pass-rate drift and first-line threshold changes
- `aio-calibration.log` -- AIO detection/scoring distribution

Trip-wires:

1. All rows pass BID -> thresholds too loose. Tighten KD to <=55 and require stronger business/product fit.
2. Zero rows pass BID -> candidate pool or threshold issue. If low-fit dominates, adjust seeds. If difficulty dominates, relax KD once to <=85 only for `brand_fit>=8` and `product_fit>=7`.
3. All AIO rows PASS because no `ai_overview` was detected -> spot-check at least five high-volume queries in SERP Advanced before trusting the distribution.
4. Queue has fewer than 50 rows -> rerun expansion before publishing routine consumes the queue.

## "Do not transplant" warning

1. **Never copy Ahrefs DR/UR or Semrush AS thresholds into a DataForSEO gate.** DataForSEO has different rank/domain metrics and no verified Authority Score replacement in the current pipeline.
2. **`mcp__semrush__*` and `mcp__ahrefs__*` are migration bugs here, not fallbacks.** If a skill reaches for either provider during keyword research, update the skill or run the DataForSEO script instead.
3. **Do not fake skipped capabilities.** `keyword-aio-gap` is skipped because DataForSEO has no multi-engine AI citation panel. ContentShake scoring is optional because no DataForSEO equivalent exists.
4. **Old cache files are footguns.** Treat `brand-dr.json`, `brand-as.json`, Semrush tool inventories, and pre-DataForSEO `dr_*`/`as_*` columns as stale unless the run ledger says they were regenerated from DataForSEO.

## Where this doc gets read from

- `keyword-research-pipeline/SKILL.md` -- orchestrator mapping and skip policy
- `content-gap-analysis/SKILL.md` -- DataForSEO expansion/gap endpoints
- `keyword-question-mining/SKILL.md` -- suggestions question filter + SERP PAA
- `keyword-vet-bid/SKILL.md` -- BID-D and BID-I thresholds
- `keyword-vet-aio/SKILL.md` -- SERP Advanced `ai_overview`
- `keyword-aio-gap/SKILL.md` -- skipped multi-engine gap
- `keyword-prioritization/SKILL.md` -- DataForSEO-safe boosts
- `draft-score/SKILL.md` and `optimize-content/SKILL.md` -- optional external scoring soft-fail
