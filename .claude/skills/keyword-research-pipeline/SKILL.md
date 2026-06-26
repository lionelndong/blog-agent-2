---
name: keyword-research-pipeline
description: Master orchestrator for the keyword research pipeline. Chains topic-discovery → seed/modifier ideation → competitor gap analysis (with question mining folded in) → BID method → AIO cannibalization check → final ranked queue. Same anti-context-bloat pattern as /blog-pipeline (every layer is an Agent dispatch, never a Skill fork).
allowed-tools: Read, Write, Bash, Agent, Glob
---

# Keyword Research Pipeline (Master Orchestrator)

## Provider ruling — Ahrefs MCP only

**Ahrefs MCP is the single data layer.** Semrush and DataForSEO are retired — no layer calls
`mcp__semrush__*` or DataForSEO, and any sub-agent that reaches for them is a migration-leftover
bug, not a fallback. Every layer's data calls map to the Ahrefs MCP tools pinned in
[`../research/references/ahrefs-mcp-cheatsheet.md`](../research/references/ahrefs-mcp-cheatsheet.md) —
read it before dispatching any layer. Two param rules bite: params are comma-separated **strings**,
not JSON arrays (`keywords:"ai girlfriend app"`, not `["ai girlfriend app"]`), and `select` +
`country` are required on most endpoints. For any tool a layer hasn't used this run, call the `doc`
tool first (e.g. `doc {tool:"keywords-explorer-overview"}`) to get its exact schema; never invent
tool names. Metric thresholds go through [`references/bid-method.md`](./references/bid-method.md)
(Ahrefs edition) — stale Semrush/DataForSEO thresholds will silently mis-fire on Ahrefs data.

Take a brand and produce a *vetted* keyword queue (`keyword-queue.csv`) ready for the autonomous
blog loop. Lean layered chain **0 → 1a → 1b → 2 → 3 → 5**, each rejecting candidates with reasons
logged, each dispatched as a fresh Agent. This is the upstream of `auto-blog-loop`; the blog loop
reads the queue this orchestrator emits — never the raw `keyword-ideas.csv`.

## Invocation

```
/keyword-research-pipeline [--regen]
```

`--regen` forces fresh runs of idempotent layers (topic-discovery re-runs even if brand-config hash
unchanged, seed-modifier-prompt re-runs, BID/AIO refetch cached SERP data).

## Why agent dispatch, not skill fork

Same constraint as `/blog-pipeline`: the Skill tool forks with the parent's context and hits
`Prompt is too long` after any compaction. The Agent tool starts each layer with a clean window.
Every layer MUST be an Agent dispatch.

## Process

1. **Resolve project root** and set `{ROOT}`.

2. **Layer 0 — `/topic-discovery`** (Agent dispatch). Build a topic-graph + market-trends snapshot
   for the brand's category before any seed work. Brief:

   ```
   You are running Layer 0 of the keyword research pipeline at {ROOT}.

   Your job: produce content-pipeline/0-keywords/topic-graph.json plus content-pipeline/0-keywords/trends.md per .claude/skills/topic-discovery/SKILL.md. Read the SKILL.md first.

   Read brand-config.md. Pull keywords-explorer-related-terms + keywords-explorer-matching-terms (mcp__ahrefs__*) for the brand's category-level seeds to approximate topic clusters, and site-explorer-organic-keywords on the brand domain for its ranking footprint / trending vs. declining queries. Ahrefs param rules: comma-separated string params, `select` + `country` required, `doc` the tool first if unused this run. Synthesize the top 5 KSB clusters per category and the trending vs. declining queries. Save the JSON + markdown atomically.

   Idempotent: if topic-graph.json exists and the brand-config hash is unchanged AND --regen was not passed, exit without re-generating. Never block the pipeline — if Ahrefs calls error, log to cache/topic-discovery-failed.log and exit cleanly with topic-graph.json containing only the brand-config seeds.

   Return: top 5 cluster names, count of trending-up / trending-down queries, idempotency status. Under 250 words.
   ```

   On failure: log and continue. Layer 0 is enrichment, not a gate.

3. **Layer 1a — `/seed-modifier-prompt`** (Agent dispatch). Brief:

   ```
   You are running Layer 1a of the keyword research pipeline at {ROOT}.

   Your job: produce content-pipeline/0-keywords/seeds.json per .claude/skills/seed-modifier-prompt/SKILL.md. Read the SKILL.md first.

   Read brand-config.md AND content-pipeline/0-keywords/topic-graph.json (from Layer 0). Pre-feed the top 5 KSB clusters into the seed-generation prompt so seeds anchor in real Ahrefs-sourced topic clusters. Generate 10 seeds + 10+ modifiers (with at least 3 AI-resistant: calculator/checker/generator/tool/template/examples). No word overlap between seeds and modifiers.

   Idempotent: if seeds.json exists and brand-config hash unchanged, exit without re-generating unless --regen passed.

   Return: seeds count, modifiers count, tool-modifier count, first 3 seeds, regenerated-or-skipped. Under 200 words.
   ```

   On failure: stop. Layer 1a is the cheapest layer; failure means something is structurally wrong.

4. **Layer 1b — `/content-gap-analysis`** (Agent dispatch; question mining folded in). Brief:

   ```
   You are running Layer 1b at {ROOT}.

   Your job: produce content-pipeline/0-keywords/keyword-ideas.csv per .claude/skills/content-gap-analysis/SKILL.md. Read the SKILL.md first.

   Auto-discover competitors via mcp__ahrefs__site-explorer-organic-competitors if brand-config doesn't list any; cache to cache/competitors.json. Read seeds.json from Layer 1a — for each seed, expand via mcp__ahrefs__keywords-explorer-matching-terms (`match_mode:"phrase"` or `"terms"`) plus keywords-explorer-related-terms / search-suggestions where breadth is thin; filter to the modifiers. **Question mining (folded in): also retain question-form terms (what/how/is/are/can/does/why/which/who/where/should) surfaced by matching-terms(`terms`), and read serp-overview `serp_features` for People-Also-Ask entries; tag those rows source=question.** Pull intents + metrics via mcp__ahrefs__keywords-explorer-overview per row (`select:"keyword,volume,difficulty,cpc,parent_topic,traffic_potential,intents"`, `country:"US"`). Comma-separated string params, NOT arrays.

   Content gap = a competitor's ranking keywords (mcp__ahrefs__site-explorer-organic-keywords on each competitor URL; consensus across 3+ top pages) MINUS the brand's. Derive gap_mode yourself: competitor ranks and brand does not → `missing`; both rank but brand outside top 10 → `weak`; brand-only → `strong` (route to cache/strong-positions.csv, NOT the writing pool); approximate `unique`/`common` from how many competitors share the term. Tag every row with `gap_mode` and `source`. Merge + dedupe on keyword.

   Apply the difficulty (KD) collection ceiling ≤ 70 (Ahrefs `difficulty`) as default — see references/bid-method.md; do not let a sub-agent invent its own threshold.

   Return: total candidates, breakdown by source (competitor_gap / seed_modifier / question / both), breakdown by gap_mode, strong-positions count, top 5 by traffic_potential. Under 300 words.
   ```

   On failure: stop. Layer 1b failures usually mean an Ahrefs auth issue (401 / bad `AHREFS_MCP_KEY`) or units exhaustion on the 400k/mo pool.

5. **Layer 2 — `/keyword-vet-bid`** (Agent dispatch). Brief:

   ```
   You are running Layer 2 at {ROOT}.

   Your job: enrich content-pipeline/0-keywords/keyword-ideas.csv with BID verdicts per .claude/skills/keyword-vet-bid/SKILL.md. Read the SKILL.md first.

   Resolve brand DR via mcp__ahrefs__site-explorer-domain-rating, cache to cache/brand-dr.json (7-day TTL). Delete any leftover cache/brand-as.json — its Semrush Authority-Score payload is incompatible with Ahrefs DR.

   For each row: compute brand_fit + product_fit; classify intent — PRIMARY signal is the Ahrefs `intents` flags from mcp__ahrefs__keywords-explorer-overview (informational/commercial = PASS; transactional/navigational = FAIL); fall back to URL-pattern heuristic on mcp__ahrefs__serp-overview only when `intents` is empty/mixed. Pull per-URL DR for the SERP top-10 via mcp__ahrefs__serp-overview (`select` includes DR) or batch-analysis. Apply the BID gate (Ahrefs DR-native — dr_top10_median ≤ brand_DR + 15; weak_link_count of pages with DR < brand_DR + 5; difficulty (KD) ≤ 70 baseline). All Ahrefs params comma-separated strings with `select`+`country`.

   Persist columns: brand_fit, product_fit, serp_intent, dr_top10_median, weak_link_count, bid_verdict, bid_reason.

   Calibration check: if all rows pass OR all fail, log to cache/bid-calibration.log and adjust thresholds per the SKILL's "Calibration" section.

   Return: total vetted, B/I/D pass rates, share of intent decisions via `intents` flags vs URL fallback, PASS count, top 5 PASS by traffic_potential, top 5 FAIL with reasons. Under 350 words.
   ```

   On failure: stop. BID failures usually mean Ahrefs units exhaustion or auth issues.

6. **Layer 3 — `/keyword-vet-aio`** (Agent dispatch). Brief:

   ```
   You are running Layer 3 at {ROOT}.

   Your job: enrich BID-PASS rows in keyword-ideas.csv with AIO cannibalization verdicts per .claude/skills/keyword-vet-aio/SKILL.md and the rubric at .claude/skills/keyword-research-pipeline/references/aio-cannibalization-rubric.md. Read both first.

   For each BID-PASS row: detect AIO presence via mcp__ahrefs__serp-overview — read its `serp_features` and look for the `ai_overview` key. Apply exemptions (tool-led, commercial-investigation). For non-exempt AIO-present rows fetch the AIO body: serp-overview's serp_features summary → WebFetch on https://www.google.com/search?q=…  Spawn the adversarial Sonnet sub-agent with the 0-10 completeness brief; persist has_aio, aio_completeness_score, aio_click_intent, aio_verdict, aio_reasoning, aio_body_source. Ahrefs params comma-separated strings, `select`+`country` required.

   Cache AIO bodies under cache/aio-fetch/ with _meta.source; refresh weekly. Pre-migration cache files (Semrush ai-toolkit / old brand_radar_*) are stale — re-fetch.

   Calibration check: if every score is 8+ OR every score is 4-, the scorer is mis-calibrated — log and re-run with strengthened brief.

   Return: total checked, breakdown (no AIO / exempt / PASS / RISKY / FAIL_CANNIBALIZED / UNKNOWN), body-source mix, top 3 cannibalized rejections, top 3 risky survivors. Under 400 words.
   ```

   On rate-limit (exit 75): persist progress, surface to orchestrator. Layer 3 is the most quota-heavy layer.

7. **Layer 5 — `/keyword-prioritization`** (Agent dispatch). Brief:

   ```
   You are running Layer 5 at {ROOT}.

   Your job: emit content-pipeline/0-keywords/keyword-queue.csv per .claude/skills/keyword-prioritization/SKILL.md. Read the SKILL.md first.

   Filter pool: only rows where bid_verdict=PASS AND aio_verdict ∈ {PASS, RISKY}.

   Apply the existing 0.4/0.3/0.3 scoring weights. Apply boosts:
     +0.5 if gap_mode=weak
     +0.7 if gap_mode=unique
     -0.3 if gap_mode=common
     +0.5 if cluster_authority_gap=true (KSB cluster the brand has zero authority in but is low-difficulty)
     +1.0 if serp_intent=tool-led (but ROUTE those to tool-opportunities.csv, not the writing queue)
   Tie-breaker on equal priority_score: higher traffic_potential wins.

   Re-rank, write top-50 to keyword-queue.csv. Tool-opportunity rows go to tool-opportunities.csv. gap_mode=strong rows are already in cache/strong-positions.csv and ignored here.

   Return: queue size, top 10 with rank/keyword/priority_score/source/intent/gap_mode/verdicts, tool-opportunities count. Under 350 words.
   ```

8. **Verify each layer's output file exists** before advancing. Layer 0: topic-graph.json + trends.md (or topic-discovery-failed.log). Layer 1a: seeds.json. Layer 1b: keyword-ideas.csv (+ cache/strong-positions.csv when applicable). Layer 2/3: required columns present. Layer 5: keyword-queue.csv.

9. **Reporting.** When complete, output:

   ```
   ✓ Keyword research pipeline complete

   Layers:
     ✓ 0 topic-discovery  → topic-graph.json (12 clusters, 8 trending-up) / trends.md
     ✓ 1a seed-modifier   → seeds.json (10 seeds, 12 modifiers, 4 tool-modifiers)
     ✓ 1b content-gap     → keyword-ideas.csv (124 candidates: 78 missing, 22 weak, 14 unique, 10 common; 24 question-tagged; 6 strong → cache)
     ✓ 2 keyword-vet-bid  → 203 vetted, 91 PASS / 112 FAIL  (intents signal: 78%, URL-fallback: 22%)
     ✓ 3 keyword-vet-aio  → 91 checked, 71 PASS / 14 RISKY / 4 FAIL_CANNIBALIZED
     ✓ 5 prioritization   → keyword-queue.csv (top 50 ranked) + tool-opportunities.csv (12 entries)

   Queue ready for /auto-blog-loop.
   ```

## Failure handling

**Bad keyword research is worse than an empty queue.** Layer failures stop the chain rather than
auto-retrying:

- Layer 0 fails → continue (enrichment, not a gate).
- Layer 1a fails → stop (brand-config hash issue or agent malfunction).
- Layer 1b fails → stop (likely Ahrefs auth / units exhaustion).
- Layer 2 fails → stop (mechanical filter is required).
- Layer 3 rate-limit (exit 75) → persist progress, exit 75; auto-blog-loop retries next cron.
- Layer 3 fails (other) → stop (AIO check is required).
- Layer 5 fails → stop (queue emission is the whole point).

The orchestrator never auto-retries — it logs the failure to
`content-pipeline/0-keywords/cache/pipeline-failures.log` and exits.

## When `/auto-blog-loop` invokes this orchestrator

The blog loop calls this when `keyword-queue.csv` is empty (selector exit 2). On failure the
previous queue (if any) stays in place; if no previous queue, the blog loop exits "no work."

## Calibration cadence

The mechanical layers (BID, AIO) need calibration on first run after the Ahrefs migration AND after
major brand-config changes. Calibration logs in `cache/`: `bid-calibration.log`,
`aio-calibration.log`. Always recalibrate against `references/bid-method.md` (Ahrefs edition).

## Cost per run

Approximate, for a 200-candidate pool, on the Ahrefs 400k-units/month pool (≈50 base units + per-row;
keep `limit` tight): Layer 0 ~3-5 calls (idempotent — most runs skip); Layer 1a ~1K LLM tokens;
Layer 1b ~10-15 calls (competitors + per-competitor organic-keywords + matching/related + question
retention); Layer 2 ~200 overview + serp-overview + batch-analysis; Layer 3 ~100 serp-overview +
~50-70 AIO-body fetches + ~50 Sonnet sub-agents; Layer 5 ~1 Agent call. Total: a few-thousand Ahrefs
units + ~$0.50 LLM tokens per run; weekly cadence stays comfortably inside the pool.
