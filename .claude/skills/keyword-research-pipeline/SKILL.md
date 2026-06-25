---
name: keyword-research-pipeline
description: Master orchestrator for the keyword research pipeline. Chains topic-discovery → seed/modifier ideation → competitor + AI-search gap analysis → question mining → BID method → AIO cannibalization check → adversarial redteam → final ranked queue. Same anti-context-bloat pattern as /blog-pipeline (every layer is an Agent dispatch, never a Skill fork).
allowed-tools: Read, Write, Bash, Agent, Glob
---

# Keyword Research Pipeline (Master Orchestrator)

## Provider ruling (2026-06-24 — supersedes the 2026-06-12 Semrush note and the 2026-06-10 DataForSEO note)

**Ahrefs MCP is the data layer.** Both Semrush and DataForSEO are retired:
`scripts/dataforseo_keyword_pipeline.py` is archived and must not run, and no layer calls
`mcp__semrush__*` any more.

Every layer's real data calls map to the **Ahrefs MCP tools** pinned in
[`../research/references/ahrefs-mcp-cheatsheet.md`](../research/references/ahrefs-mcp-cheatsheet.md) — read it
before dispatching any layer. Two param rules bite: params are comma-separated **strings**, not
JSON arrays (`keywords:"ai girlfriend app"`, not `["ai girlfriend app"]`), and `select` + `country`
are required on most endpoints. For any tool a layer hasn't used this run, call the `doc` tool first
(e.g. `doc {tool:"keywords-explorer-overview"}`) to get its exact schema; never invent tool names.
Metric thresholds still go through [`references/bid-method.md`](./references/bid-method.md) — the
recalibration math now lives inline there (the old `*-metric-translation.md` doc is retired).

Layer 1c (`keyword-aio-gap`) stays **SKIPPED by default** for now — this is a methodology decision,
not a data-availability one. NOTE: unlike Semrush/DataForSEO, Ahrefs MCP *does* ship a Brand Radar
AI-citation toolkit (`brand-radar-ai-responses`, `brand-radar-cited-pages`, `brand-radar-sov-overview`,
`site-explorer-ai-responses-count`), so the multi-engine citation gap is now technically sourceable.
Un-skipping 1c is a deliberate pipeline change to make separately — until then keep it a logged
no-op and do **not** fabricate `aio_gap` rows or `aio_sov_competitor_top`. Layer 3's AIO check stays
presence-only via `serp-overview`'s `serp_features` (the `ai_overview` key). Keep the deterministic
quality, judgment rewrite, and voice-drift rollback gates.

Take a brand and produce a *vetted* keyword queue (`keyword-queue.csv`) ready for the autonomous blog loop. Layered chain (0 → 1a → 1b → 1c → 1d → 2 → 3 → 4 → 5), each rejecting candidates with reasons logged, each dispatched as a fresh Agent.

This is the upstream of `auto-blog-loop`. The blog loop reads the queue this orchestrator emits — never the raw `keyword-ideas.csv`.

> **Threshold reminder.** Every layer in this chain is recalibrated against the thresholds in `.claude/skills/keyword-research-pipeline/references/bid-method.md` (Ahrefs edition). If a brief tells a layer to apply a numeric threshold, the underlying skill's gate should already match the BID doc — do not let an Agent invent its own threshold from training data. **`mcp__semrush__*` and DataForSEO are retired for keyword research; `mcp__ahrefs__*` is the only sanctioned provider**; if any sub-agent reaches for Semrush or DataForSEO, that's a migration leftover bug, not a fallback.

## Invocation

```
/keyword-research-pipeline [--regen] [--max-redteam 30]
```

`--regen` forces fresh runs of idempotent layers (topic-discovery re-runs even if brand-config hash unchanged, seed-modifier-prompt re-runs, redteam re-evaluates already-judged rows, BID/AIO refetch cached SERP data).

`--max-redteam` overrides the Layer 4 batch size (default 30).

## Why agent dispatch, not skill fork

Same constraint as `/blog-pipeline` (line 22-24 of `blog-pipeline/SKILL.md`): the Skill tool forks with the parent's context. After any compaction or accumulated history, that fork hits `Prompt is too long`. The Agent tool starts each layer with a clean window. This is non-negotiable — every layer MUST be an Agent dispatch.

## Process

1. **Resolve project root** (`C:\Users\ndong\Downloads\blog-agent-2` or wherever the host runs). Set `{ROOT}`.

2. **Layer 0 — `/topic-discovery`** (Agent dispatch). Build a topic-graph + market-trends snapshot for the brand's category before any seed work happens. Self-contained brief:

   ```
   You are running Layer 0 of the keyword research pipeline at {ROOT}.

   Your job: produce content-pipeline/0-keywords/topic-graph.json plus content-pipeline/0-keywords/trends.md per .claude/skills/topic-discovery/SKILL.md. Read the SKILL.md first.

   Read brand-config.md. Pull keywords-explorer-related-terms + keywords-explorer-matching-terms (mcp__ahrefs__*) for the brand's category-level seeds to approximate topic clusters, and site-explorer-organic-keywords on the brand domain for its ranking footprint / trending vs. declining queries (cross-check with gsc-performance-history when available). Remember the Ahrefs param rules: comma-separated string params, `select` + `country` required, `doc` the tool first if unused this run. Synthesize the top 5 KSB clusters per category and the trending vs. declining queries. Save the JSON + markdown atomically.

   Idempotent: if topic-graph.json exists and the brand-config hash is unchanged AND --regen was not passed, exit without re-generating. Never block the pipeline — if the Ahrefs calls error, log to cache/topic-discovery-failed.log and exit cleanly with topic-graph.json containing only the brand-config seeds.

   Return: top 5 cluster names, count of trending-up / trending-down queries, idempotency status (regenerated vs. skipped). Under 250 words.
   ```

   On failure: log and continue. Layer 0 is enrichment, not a gate — Layer 1a will still run with brand-config seeds alone if topic-graph.json is empty.

3. **Layer 1a — `/seed-modifier-prompt`** (Agent dispatch). Self-contained brief:

   ```
   You are running Layer 1a of the keyword research pipeline at {ROOT}.

   Your job: produce content-pipeline/0-keywords/seeds.json per .claude/skills/seed-modifier-prompt/SKILL.md. Read the SKILL.md first.

   Read brand-config.md AND content-pipeline/0-keywords/topic-graph.json (from Layer 0). Pre-feed the top 5 KSB clusters from topic-graph.json into the seed-generation prompt so seeds anchor in real Ahrefs-sourced topic clusters, not just brand-config alone. Generate 10 seeds + 10+ modifiers (with at least 3 AI-resistant: calculator/checker/generator/tool/template/examples). No word overlap between seeds and modifiers.

   Idempotent: if seeds.json exists and brand-config hash unchanged, exit without re-generating. Force re-gen only if --regen passed.

   Return: seeds count, modifiers count, tool-modifier count, first 3 seeds, whether re-generated or skipped. Under 200 words.
   ```

   On failure: stop the pipeline. Layer 1a is the cheapest layer; if it fails, something is structurally wrong.

4. **Layer 1b — `/content-gap-analysis`** (Agent dispatch). Brief:

   ```
   You are running Layer 1b at {ROOT}.

   Your job: produce content-pipeline/0-keywords/keyword-ideas.csv per .claude/skills/content-gap-analysis/SKILL.md. Read the SKILL.md first.

   Auto-discover competitors via mcp__ahrefs__site-explorer-organic-competitors if brand-config doesn't list any; cache to cache/competitors.json so Layer 1c reuses the same set. Read seeds.json from Layer 1a — for each seed, expand via mcp__ahrefs__keywords-explorer-matching-terms (`match_mode:"phrase"` or `"terms"`) plus keywords-explorer-related-terms / keywords-explorer-search-suggestions where breadth is thin; filter to the modifiers. Pull the intents flags + metrics via mcp__ahrefs__keywords-explorer-overview for each row (`select:"keyword,volume,difficulty,cpc,parent_topic,traffic_potential,intents"`, `country:"US"`). Remember: comma-separated string params, NOT arrays.

   Content gap = a competitor's ranking keywords (mcp__ahrefs__site-explorer-organic-keywords on each competitor URL; consensus across 3+ top pages) MINUS the brand's. Ahrefs has no Semrush five-mode Keyword Gap labels — derive gap_mode yourself: a keyword a competitor ranks for and the brand does not → `missing`; both rank but the brand sits outside the top 10 → `weak`; brand-only ranking → `strong` (route those to cache/strong-positions.csv, NOT the writing pool); approximate `unique`/`common` from how many competitors share the term. Tag every row with `gap_mode`. Merge competitor-gap + seed-modifier sources, dedupe on keyword. Add `source` and `gap_mode` columns.

   Apply the difficulty (KD) collection ceiling ≤ 70 (Ahrefs `difficulty` column) as the default — see references/bid-method.md for the recalibration math; do not let a sub-agent invent its own threshold.

   Return: total candidates, breakdown by source (competitor_gap / seed_modifier / both), breakdown by gap_mode (missing / weak / unique / common), strong-positions count, top 5 candidates by traffic_potential. Under 300 words.
   ```

   On failure: stop. Layer 1b failures usually mean an Ahrefs auth issue (401 / bad `AHREFS_MCP_KEY`) or units exhaustion on the 400k/mo pool.

5. **Layer 1c — `/keyword-aio-gap`** (Agent dispatch). Brief:

   ```
   You are running Layer 1c at {ROOT}.

   Your job: append AI-search gap candidates to content-pipeline/0-keywords/keyword-ideas.csv per .claude/skills/keyword-aio-gap/SKILL.md. Read the SKILL.md first.

   DEFAULT: this layer is a logged no-op (see the Provider ruling). Only run the data path below if 1c has been explicitly un-skipped for this run. When run: use the Ahrefs Brand Radar AI-citation toolkit (mcp__ahrefs__brand-radar-ai-responses, brand-radar-cited-pages, brand-radar-sov-overview, site-explorer-ai-responses-count) across the engines Ahrefs reports (e.g. ChatGPT, Perplexity, Google AI Overviews). For each brand + competitor, find prompts/queries where a competitor is cited and the brand isn't. Compute the gap. Enrich with mcp__ahrefs__keywords-explorer-overview metrics (string params, `select`+`country` required). Append rows with source=aio_gap (or merge to existing rows as source=both). Add aio_engines and aio_sov_competitor_top columns for Layer 5 prioritization. Never fabricate rows when the toolkit returns nothing.

   If Brand Radar returns 429, exit code 75 — orchestrator retries on next cron cycle. Don't crash.

   Return: brand mentions, total competitor mentions across the engine panel, gap-prompt count, top 5 gap keywords with their dominant engine. Under 300 words.
   ```

   On Layer 1c rate-limit: don't fail the pipeline — Layer 1b already produced a candidate pool, downstream layers can vet it. Note the 1c skip in the run summary.

6. **Layer 1d — `/keyword-question-mining`** (Agent dispatch). Brief:

   ```
   You are running Layer 1d at {ROOT}.

   Your job: append question-shaped keyword candidates to content-pipeline/0-keywords/keyword-ideas.csv per .claude/skills/keyword-question-mining/SKILL.md. Read the SKILL.md first.

   There is NO dedicated "questions" tool on Ahrefs. For every primary seed in seeds.json, call mcp__ahrefs__keywords-explorer-matching-terms with `match_mode:"terms"` and client-filter to keywords starting with what/how/is/are/can/does/do/why/which/who/where/will/should. Then call mcp__ahrefs__serp-overview per top seed and read its `serp_features` for People-Also-Ask entries the matching-terms pass missed. Cap the merged pool at 100 rows per pipeline run; dedupe against existing keyword-ideas.csv. Tag every appended row with source=question_mining and a question_subtype field (`paa` / `km_question` / `both`). Pull intents + metrics via mcp__ahrefs__keywords-explorer-overview for each new row (string params, `select`+`country` required).

   On 429: persist progress, exit 75. The orchestrator handles retry.

   Return: km_questions count, paa-only count, deduped-against-existing count, top 5 questions by volume, subtype breakdown. Under 250 words.
   ```

   On failure (other than 429): continue. Layer 1d is enrichment; missing question-mining rows don't break the queue.

7. **Layer 2 — `/keyword-vet-bid`** (Agent dispatch). Brief:

   ```
   You are running Layer 2 at {ROOT}.

   Your job: enrich content-pipeline/0-keywords/keyword-ideas.csv with BID verdicts per .claude/skills/keyword-vet-bid/SKILL.md. Read the SKILL.md first.

   Resolve brand DR via mcp__ahrefs__site-explorer-domain-rating, cache to cache/brand-dr.json (7-day TTL). Delete any leftover cache/brand-as.json — its Semrush Authority-Score payload is incompatible.

   For each row: compute brand_fit + product_fit; classify intent — PRIMARY signal is the Ahrefs `intents` flags from mcp__ahrefs__keywords-explorer-overview (informational/commercial = PASS; transactional/navigational = FAIL); fall back to URL-pattern heuristic on mcp__ahrefs__serp-overview only when `intents` is empty/mixed. Pull per-URL Domain Rating for the SERP top-10 via mcp__ahrefs__serp-overview (`select` includes DR) or batch-analysis over the top-10 URLs. Apply the BID gate (Ahrefs DR-native — dr_top10_median ≤ brand_DR + 15; weak_link_count of pages with DR < brand_DR + 5; difficulty (KD) ≤ 70 baseline). All Ahrefs params are comma-separated strings with `select`+`country`.

   Persist columns: brand_fit, product_fit, serp_intent, dr_top10_median, weak_link_count, bid_verdict, bid_reason.

   Calibration check: if all rows pass OR all fail, log to cache/bid-calibration.log and adjust thresholds per the SKILL's "Calibration" section.

   Return: total vetted, B/I/D pass rates, share of intent decisions made via `intents` flags vs URL fallback, overall PASS count, top 5 PASS by traffic_potential, top 5 FAIL with reasons. Under 350 words.
   ```

   On failure: stop. BID failures usually mean Ahrefs units exhaustion or auth issues — not recoverable mid-run.

8. **Layer 3 — `/keyword-vet-aio`** (Agent dispatch). Brief:

   ```
   You are running Layer 3 at {ROOT}.

   Your job: enrich BID-PASS rows in keyword-ideas.csv with AIO cannibalization verdicts per .claude/skills/keyword-vet-aio/SKILL.md. Read the SKILL.md and the rubric at .claude/skills/keyword-research-pipeline/references/aio-cannibalization-rubric.md first.

   For each BID-PASS row: detect AIO presence via mcp__ahrefs__serp-overview — read its `serp_features` and look for the `ai_overview` key (underscore). Apply exemptions (tool-led, commercial-investigation, aio_gap source). For non-exempt AIO-present rows fetch the AIO body in this order: mcp__ahrefs__brand-radar-ai-responses (when 1c's Brand Radar path is enabled) → serp-overview's serp_features summary → WebFetch on https://www.google.com/search?q=…  Spawn the adversarial Sonnet sub-agent with the 0-10 completeness brief; persist has_aio, aio_completeness_score, aio_click_intent, aio_verdict, aio_reasoning, aio_body_source. Ahrefs params are comma-separated strings, `select`+`country` required.

   Cache AIO bodies under cache/aio-fetch/ with _meta.source. Refresh weekly. Pre-migration cache files (Semrush ai-toolkit / old brand_radar_*) are stale — re-fetch.

   Calibration check: if every score is 8+ OR every score is 4-, the scorer is mis-calibrated — log and re-run with strengthened brief per the SKILL's "Calibration" section.

   Return: total checked, breakdown (no AIO / exempt / PASS / RISKY / FAIL_CANNIBALIZED / UNKNOWN), body-source mix (brand_radar / serp_features / webfetch), top 3 cannibalized rejections, top 3 risky survivors. Under 400 words.
   ```

   On rate-limit (exit 75): persist progress, surface to orchestrator. Layer 3 is the most quota-heavy layer (one serp-overview + one AIO-body fetch per non-exempt BID-PASS row).

9. **Layer 4 — `/keyword-redteam`** (Agent dispatch — judgment-heavy, stays on parent model). Brief:

   ```
   You are running Layer 4 at {ROOT}.

   Your job: redteam top-{max_redteam} survivors per .claude/skills/keyword-redteam/SKILL.md. Read the SKILL.md first.

   Filter to bid_verdict=PASS AND aio_verdict ∈ {PASS, RISKY, UNKNOWN} AND no existing redteam_verdict (idempotent). Take top 30 by current priority_score. Spawn the skeptical-SEO sub-agent with the (a)-(d) challenge brief. The agent reasons over Ahrefs metrics (intents flags, DR gap, difficulty (KD), parent_topic / cluster id, Brand Radar SoV when available).

   Apply discipline check: if KEEP rate > 80% with weak per-candidate critique (avg < 60 words), re-run with the contrarian addendum from the SKILL.

   Persist redteam_verdict, redteam_priority_delta, redteam_critique_summary to keyword-ideas.csv. Save full critique to redteam-notes.md.

   Return: KEEP/DROP/REVISE counts, sum of priority deltas, top 3 DROPs with one-line reasons, top 3 REVISE-down with reasons. Under 400 words.
   ```

   On failure: stop. Don't ship a queue without the redteam check.

10. **Layer 5 — `/keyword-prioritization`** (Agent dispatch). Brief:

    ```
    You are running Layer 5 at {ROOT}.

    Your job: emit content-pipeline/0-keywords/keyword-queue.csv per the updated .claude/skills/keyword-prioritization/SKILL.md. Read the SKILL.md first.

    Filter pool: only rows where bid_verdict=PASS AND aio_verdict ∈ {PASS, RISKY} AND redteam_verdict ∈ {KEEP, REVISE_PRIORITY}.

    Apply the existing 0.4/0.3/0.3 scoring weights. Apply boosts:
      +1.5 if source=aio_gap
      +0.5 if gap_mode=weak
      +0.7 if gap_mode=unique
      -0.3 if gap_mode=common
      +0.5 if cluster_authority_gap=true (KSB cluster the brand has zero authority in but is low-difficulty)
      +1.0 if serp_intent=tool-led (but ROUTE those to tool-opportunities.csv, not the writing queue)
    Tie-breaker on equal priority_score: row with higher aio_sov_competitor_top wins.

    Apply redteam_priority_delta (capped ±2.0).

    Re-rank, write top-50 to keyword-queue.csv. Tool-opportunity rows go to tool-opportunities.csv (not the writing queue). gap_mode=strong rows are already in cache/strong-positions.csv and are ignored here.

    Return: queue size, top 10 with rank/keyword/priority_score/source/intent/gap_mode/verdicts, tool-opportunities count. Under 350 words.
    ```

11. **Verify each layer's output file exists** before advancing. Layer 0: topic-graph.json + trends.md (or topic-discovery-failed.log). Layer 1a: seeds.json. Layer 1b/1c/1d: keyword-ideas.csv with relevant `source` rows; cache/strong-positions.csv when applicable. Layer 2/3: required columns present. Layer 4: redteam-notes.md exists, keyword-ideas.csv has redteam columns. Layer 5: keyword-queue.csv exists.

12. **Reporting.** When complete, output:

    ```
    ✓ Keyword research pipeline complete

    Layers:
      ✓ 0 topic-discovery     → topic-graph.json (12 clusters, 8 trending-up) / trends.md
      ✓ 1a seed-modifier      → seeds.json (10 seeds, 12 modifiers, 4 tool-modifiers)
      ✓ 1b content-gap        → keyword-ideas.csv (124 candidates: 78 missing, 22 weak, 14 unique, 10 common; 6 strong → cache)
      ✓ 1c keyword-aio-gap    → +37 rows from aio_gap (engines: AIO=18 ChatGPT=11 Perplexity=8) (or SKIPPED: rate-limit)
      ✓ 1d question-mining    → +42 rows (28 km_questions, 19 paa, dedup-overlap=5)
      ✓ 2 keyword-vet-bid     → 203 vetted, 91 PASS / 112 FAIL  (intents-array signal: 78%, URL-fallback: 22%)
      ✓ 3 keyword-vet-aio     → 91 checked, 71 PASS / 14 RISKY / 4 FAIL_CANNIBALIZED  (body source: ai_toolkit=58 serp=7 webfetch=2)
      ✓ 4 keyword-redteam     → 30 redteamed, 22 KEEP / 5 DROP / 3 REVISE
      ✓ 5 prioritization      → keyword-queue.csv (top 50 ranked, 8 aio_gap-boosted, 4 cluster-authority-boosted)
                               → tool-opportunities.csv (12 entries)

    Queue ready for /auto-blog-loop.
    ```

## Failure handling

Per the plan, **bad keyword research is worse than empty queue**. Layer failures stop the chain rather than auto-retrying. Specifically:

- Layer 0 fails → continue. Topic-discovery is enrichment, not a gate.
- Layer 1a fails → stop. Brand-config hash issue or agent malfunction.
- Layer 1b fails → stop. Likely Ahrefs auth issue (401 / bad `AHREFS_MCP_KEY`) or units exhaustion.
- Layer 1c fails (rate-limit) → continue without 1c rows; log skip.
- Layer 1c fails (other) → continue with a warning; 1b alone is a viable candidate pool.
- Layer 1d fails (rate-limit, exit 75) → persist progress; orchestrator retries on next cron.
- Layer 1d fails (other) → continue. Question mining is enrichment.
- Layer 2 fails → stop. The mechanical filter is required (Ahrefs units exhaustion or auth issue).
- Layer 3 rate-limit (exit 75) → persist progress, exit cleanly with code 75. The auto-blog-loop reads this and retries on the next cron cycle.
- Layer 3 fails (other) → stop. AIO check is required.
- Layer 4 fails → stop. Redteam is required.
- Layer 5 fails → stop. Queue emission is the whole point.

The orchestrator never auto-retries — bad keyword research compounds. It logs the failure to `content-pipeline/0-keywords/cache/pipeline-failures.log` and exits.

## When `/auto-blog-loop` invokes this orchestrator

The blog loop calls this when `keyword-queue.csv` is empty (selector exit 2). The keyword-research-pipeline runs to completion (or fails cleanly), then control returns to the blog loop. If it fails:
- The previous `keyword-queue.csv` (if any) stays in place — blog loop falls back to the stale queue.
- If no previous queue, blog loop exits cleanly with a "no work" log entry.

## Calibration cadence

The mechanical layers (BID, AIO) need calibration on first run after the Ahrefs migration AND after major brand-config changes. Calibration logs are in `cache/`:
- `cache/bid-calibration.log` — threshold drift, pass-rate trends
- `cache/aio-calibration.log` — score distribution, rubber-stamp detection

The runbook (`.claude/skills/auto-blog-loop/references/runbook.md`) has a section on reading these logs and tuning thresholds. **Always recalibrate against `references/bid-method.md` (Ahrefs edition) — stale Semrush/DataForSEO thresholds will silently mis-fire on Ahrefs data.**

## Cost per run

Approximate, for a 200-candidate pool, on the Ahrefs 400k-units/month workspace pool (≈50 base units + per-row; keep `limit` tight):

- Layer 0: ~3-5 Ahrefs MCP calls (related-terms / matching-terms + site-explorer-organic-keywords); idempotent — most runs skip
- Layer 1a: ~1K LLM tokens (one Agent call)
- Layer 1b: ~10-15 Ahrefs MCP calls (site-explorer-organic-competitors + per-competitor organic-keywords + ~6 matching/related expansions per seed)
- Layer 1c: SKIPPED by default (no calls). If un-skipped: ~10-30 Brand Radar calls across the engine panel
- Layer 1d: ~10-20 matching-terms(`terms`) + serp-overview PAA-extraction calls
- Layer 2: ~200 keywords-explorer-overview + 200 serp-overview + batch-analysis calls (batched for the per-domain DR lookups)
- Layer 3: ~100 serp-overview + ~50-70 AIO-body fetches + ~50 Sonnet sub-agent invocations
- Layer 4: ~1 Opus call (30K-50K tokens)
- Layer 5: ~1 Agent call

Total: a few-thousand Ahrefs units per run + ~$0.50 in LLM tokens. Weekly cadence stays comfortably inside the 400k/mo pool. The blog loop's article cost is much higher; keyword research is cheap insurance. Layer 0 + Layer 1d add a small fixed unit cost on top of the core chain — worth it for the upstream uplift.
