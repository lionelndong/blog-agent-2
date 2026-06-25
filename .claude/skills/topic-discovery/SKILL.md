---
name: topic-discovery
description: Layer 0 of the keyword research pipeline. Builds a topic-graph snapshot for the brand's category before any seed work, approximated from Ahrefs keywords-explorer-related-terms + keywords-explorer-matching-terms on the category seeds plus the brand's own ranking footprint (site-explorer-organic-keywords). Idempotent on brand-config hash; never blocks the pipeline; cheap.
allowed-tools: Read, Write, Bash, mcp__ahrefs__*
---

# Topic Discovery Skill (Layer 0)

> **DATA LAYER (2026-06-24).** This layer runs on the **Ahrefs MCP** (`mcp__ahrefs__*`); Semrush and DataForSEO are retired. Map every data call to the tools pinned in [`../research/references/ahrefs-mcp-cheatsheet.md`](../research/references/ahrefs-mcp-cheatsheet.md) — read it first. Two param rules bite: params are comma-separated **strings**, not JSON arrays (`keywords:"ai companion"`, not `["ai companion"]`), and `select` + `country` are required on most endpoints. For any tool you haven't used this run, call `doc {tool:"keywords-explorer-related-terms"}` first to get its exact schema; never invent tool names. The logic below (filters, thresholds, output schema) remains binding; only the data calls changed.

Take `brand-config.md` and produce two artefacts that downstream layers consume as enrichment:

1. **`content-pipeline/0-keywords/topic-graph.json`** — an idea-cluster tree rooted at the brand's category, approximated from Ahrefs `keywords-explorer-related-terms` ("also talk about") + `keywords-explorer-matching-terms` on the category seeds, with each surviving keyword's `parent_topic` (from `keywords-explorer-overview`) used as the cluster key. Layer 1a (`/seed-modifier-prompt`) reads the top 5 cluster names so the seed agent grounds its output in Ahrefs's actual parent-topic graph rather than brand-config alone. Layer 5 (`/keyword-prioritization`) reads cluster-level metrics to compute the `cluster_authority_gap` boost.
2. **`content-pipeline/0-keywords/trends.md`** — a short markdown summary of category-level momentum and competitor footprint, derived from the brand's `site-explorer-organic-competitors` set plus per-keyword `volume_monthly_history` (from `keywords-explorer-overview`) on the top category clusters. Layer 4 (`/keyword-redteam`) reads this to ground its "is this keyword trending up or down today?" critique.

This layer is **enrichment, not a gate.** If Ahrefs returns nothing useful, downstream layers fall through to brand-config-only behavior. Layer 0 must never block the pipeline.

## Input

`/topic-discovery [--regen]`

Reads:
- `brand-config.md` — brand category positioning, brand domain
- `content-pipeline/0-keywords/topic-graph.json` — previous output (for change detection)

`--regen` forces a fresh run even if the brand-config hash hasn't changed.

## Process

1. **Compute brand-config hash.** SHA-256 of `brand-config.md` content. Compare against `topic-graph.json`'s `brand_snapshot` field if it exists. If unchanged AND `--regen` not passed, exit cleanly with a one-line message saying "topic graph is current, skipping" — Layer 0 stays idempotent (mirrors the pattern in `seed-modifier-prompt/SKILL.md` step 1).

2. **Read brand-config.** Extract:
   - **Brand category root** — the noun-phrase that defines the brand's category for SEO purposes. Derived from `brand-config.md`'s "Category positioning" line. If the line is verbose, condense to 1–3 words (e.g. for Pleasur.AI: "ai adult companions" → root seed `ai companion`). When in doubt, prefer the broader of two candidates — the related-terms expansion returns a richer tree from broader roots.
   - **Brand domain** — used as the Site Explorer target. Strip protocol and trailing slash.

3. **Build the cluster tree from Ahrefs Keywords Explorer.** There is no single "Topic Research" endpoint on Ahrefs; approximate the idea-cluster tree from two calls on the brand category root:
   - `keywords-explorer-related-terms` (`select:"keyword,volume,difficulty,parent_topic,intents"`, `country:"US"`, `view_for:"also_talk_about"`, `limit` ~100) — the "also talk about" surface is the closest analogue to a topical-cluster expansion.
   - `keywords-explorer-matching-terms` (`match_mode:"terms"`, `select:"keyword,volume,difficulty,parent_topic,intents"`, `country:"US"`, `limit` ~100) — breadth of phrasings that share the root's terms.
   Concatenate, dedupe on keyword, then **group rows by `parent_topic`** — Ahrefs's `parent_topic` is the cluster key (it's the keyword Ahrefs considers the topical parent). Each cluster's aggregated `volume` is the sum of member volumes; its `difficulty` is the member median. Cache the raw responses under `content-pipeline/0-keywords/cache/topic-research-raw.json` so re-runs without `--regen` don't refetch when only writing the structured tree.

4. **Pull category momentum + competitor footprint.** Two calls:
   - `keywords-explorer-overview` (`select:"keyword,volume,volume_monthly_history,parent_topic"`, `country:"US"`) on the top ~10 cluster-parent keywords from step 3 → `volume_monthly_history` gives the volume momentum (rising vs. falling) per cluster without a dedicated trends API.
   - `site-explorer-organic-competitors` for the brand domain → the domains that overlap the brand's organic footprint, with their overlap/traffic figures (the competitor-shift signal).
   Cache the raw responses under `content-pipeline/0-keywords/cache/trends-raw.json`.

5. **Assemble `topic-graph.json`** as a structured tree:
   ```json
   {
     "root_seed": "ai companion",
     "brand_domain": "pleasur.ai",
     "clusters": [
       {
         "id": "parent-topic-from-ahrefs",
         "name": "ai girlfriend",
         "volume": 246000,
         "difficulty": 64,
         "headlines": ["...", "..."],
         "questions": ["what is an ai girlfriend?", "..."],
         "related_searches": ["...", "..."]
       }
     ],
     "generated_at": "ISO8601 UTC",
     "brand_snapshot": "sha256-hex-of-brand-config-md",
     "_meta": {
       "source": "Ahrefs Keywords Explorer (related-terms + matching-terms, grouped by parent_topic) + Site Explorer organic-competitors",
       "cheatsheet_ref": ".claude/skills/research/references/ahrefs-mcp-cheatsheet.md"
     }
   }
   ```
   `id`/`name` come from the `parent_topic` cluster key; `questions` are the question-form members (keywords starting with what/how/is/are/can/does/why/which/who/where) within the cluster; `headlines` / `related_searches` are the highest-volume non-question members. Sort clusters by `volume` descending. Cap headlines / questions / related_searches at 10 entries each per cluster — Layer 1a only consumes the top 5 clusters anyway, but downstream tooling stays bounded.

6. **Assemble `trends.md`** as readable markdown for the redteam agent:
   ```markdown
   # Category trends — {brand_domain} ({YYYY-MM-DD})

   ## Trending up (volume momentum +)
   - keyword (vol_now → vol_3mo_ago, change %)

   ## Trending down (volume momentum −)
   - keyword (vol_now → vol_3mo_ago, change %)

   ## Competitor footprint (organic overlap)
   - competitor.com — shares X overlapping keywords / Y est. organic traffic

   _Source: Ahrefs Keywords Explorer (volume_monthly_history) + Site Explorer organic-competitors, generated {ISO timestamp}_
   ```
   Trend direction comes from comparing the most-recent `volume_monthly_history` point to the point ~3 months prior. Keep it tight — under 60 lines. The redteam agent reads this as ambient context, not a primary input.

7. **Write both files** atomically (write to `.tmp` then move). Print a one-line summary: cluster count, top 3 cluster names with volumes, trending-up count, trending-down count, top 3 competitors by organic overlap.

## Output

- `content-pipeline/0-keywords/topic-graph.json` — structured idea-cluster tree
- `content-pipeline/0-keywords/trends.md` — markdown trends summary
- `content-pipeline/0-keywords/cache/topic-research-raw.json` — raw MCP response (gitignored)
- `content-pipeline/0-keywords/cache/trends-raw.json` — raw MCP response (gitignored)

## Idempotency

Same contract as `seed-modifier-prompt`: re-runs without `--regen` exit cleanly when the brand-config SHA-256 hasn't changed. ~4 MCP calls per actual run; zero on the no-op path. Safe for the orchestrator to call on every keyword-research-pipeline invocation without worrying about cost.

## Failure handling

**Layer 0 never blocks the pipeline.** It's enrichment, not a gate. Specific failure modes:

- **`keywords-explorer-related-terms` / `keywords-explorer-matching-terms` return empty** (root seed too narrow / not indexed): write a stub `topic-graph.json` with `clusters: []`, `_meta.degraded: true`, and the root_seed used. Append a one-line entry to `content-pipeline/0-keywords/cache/topic-discovery-failed.log` with the timestamp and reason. Exit code 0. Layer 1a reads the empty `clusters` array and falls through to brand-config-only seed generation (current behavior preserved).
- **Keywords Explorer errors** (auth, network, server): write the same stub graph with `_meta.degraded: true` and `_meta.error: "<reason>"`. Log to `cache/topic-discovery-failed.log`. Exit 0.
- **`site-explorer-organic-competitors` / momentum calls return empty / error**: write a `trends.md` containing only the heading and a single line `_Source: Ahrefs — no momentum/competitor data returned for {brand_domain} ({YYYY-MM-DD})_`. Log to `cache/topic-discovery-failed.log`. Exit 0. The redteam agent reads the absence as "no trend signal available" and reasons without it.
- **Both surfaces error with the same auth code (401)**: Ahrefs MCP isn't connected or the key is rejected. Surface a clear one-line error to stderr ("Ahrefs MCP unauthenticated — check `AHREFS_MCP_KEY`") and exit 0 anyway. The orchestrator continues.
- **Rate-limit / units-exhausted (429)**: persist whatever responses we did get; if neither surface succeeded, write the stub artefacts and log the quota event. Exit 0 (do **not** propagate exit 75 — Layer 0 is non-blocking). The orchestrator will pick up the cached stubs on the next run.

The discipline here is the user's call-out: "the pipeline never blocks on Layer 0 because it's enrichment, not a gate."

## Quality checklist

- [ ] `topic-graph.json` exists and parses as JSON
- [ ] `brand_snapshot` matches current `brand-config.md` SHA-256
- [ ] `clusters` array is sorted by volume descending (or empty + `_meta.degraded: true`)
- [ ] Each non-degraded cluster has at least: id, name, volume, headlines, questions
- [ ] `trends.md` exists and has a section heading even if empty
- [ ] Failure paths log to `cache/topic-discovery-failed.log` rather than crashing
- [ ] ~4 MCP calls maximum per actual run; zero on no-op
- [ ] Cache files are under `content-pipeline/0-keywords/cache/` (gitignored)

## Why this exists

Ryan Law's method surfaces individual keywords but not the **cluster topology** of a category, nor the **time-axis momentum** signal that tells you whether a topic is rising or fading. Ahrefs supplies a usable proxy for both:

- The cluster topology — approximated from `related-terms`/`matching-terms` grouped by `parent_topic` — lets Layer 1a generate seeds that match how the brand's category actually clusters in Google's view (rather than a brand-config-trained generative guess).
- The momentum signal — `volume_monthly_history` per cluster parent — lets Layer 4's redteam reject keywords that look attractive but are on a 12-month decline, an opportunity-cost critique a static keyword list couldn't make.

Adding Layer 0 doesn't disturb the existing chain — Layers 1–5 still run if Layer 0 produces nothing. It's pure enrichment, gated on a cheap idempotency check.

## When the brand-config has no clear category

(Edge case: a personal blog or generic agency site without a sharp category positioning.) The root seed will be too broad and the related-terms expansion returns a shallow tree. The skill still runs — it writes whatever it gets, and downstream layers behave as if Layer 0 returned an empty tree. No special-casing required; the failure-handling path covers it.

## Invocation from the master orchestrator

`/keyword-research-pipeline` calls this skill **first**, before Layer 1a. Because of the brand-config hash check, the master can call it on every run without worrying about waste. On a typical run with stable brand-config, Layer 0 is a < 1-second no-op.

## References

- `.claude/skills/research/references/ahrefs-mcp-cheatsheet.md` — task→tool mapping for Keywords Explorer + Site Explorer, param rules, verified `select` columns
- `.claude/skills/keyword-research-pipeline/references/bid-method.md` — `parent_topic` is the cluster key downstream layers read from `topic-graph.json`; reference for the metric semantics Layer 5 applies
