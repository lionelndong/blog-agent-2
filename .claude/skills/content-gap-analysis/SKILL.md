---
name: content-gap-analysis
description: Layer 1b of the keyword research pipeline. Finds keyword opportunities by comparing the brand's blog against competitors AND by expanding seeds + modifiers via the Ahrefs MCP (keywords-explorer-matching-terms / related-terms). Auto-discovers competitors via site-explorer-organic-competitors when none are provided, derives the keyword gap from competitors' organic keywords minus ours, tags every row with `gap_mode`, and outputs a candidate-keyword CSV ready for downstream BID/AIO vetting.
allowed-tools: Read, Write, Bash, mcp__ahrefs__*
---

# Content Gap Analysis Skill

> **DATA LAYER RULING (2026-06-24 — supersedes the 2026-06-12 Semrush note).** Ahrefs MCP (`mcp__ahrefs__*`) is the data layer; Semrush AND DataForSEO are retired. Before making any data call, read [`../research/references/ahrefs-mcp-cheatsheet.md`](../research/references/ahrefs-mcp-cheatsheet.md) — it maps each task to the real Ahrefs MCP tools and pins the param rules. Two that bite: params are comma-separated **strings**, not JSON arrays (`keywords:"ai girlfriend app"`, not `["ai girlfriend app"]`), and `select` + `country` are required on most endpoints. For any tool you haven't used this run, call `doc {tool:"..."}` first to get its exact schema; never invent tool names. The logic below (filters, thresholds, output schema, the five `gap_mode` tags) remains binding; only the data calls changed.

Use Ahrefs Site Explorer (competitor organic keywords) plus Keywords Explorer (matching/related terms) to surface keywords competitors rank for that the brand doesn't, plus seed-modifier expansion of the brand's own keyword universe. The output feeds `/keyword-prioritization`, which then feeds `/blog-pipeline` for the chosen keywords.

> **Threshold reminder.** All KD thresholds in this skill are Ahrefs Keyword Difficulty (KD 0–100), recalibrated per `.claude/skills/keyword-research-pipeline/references/bid-method.md` (Ahrefs edition — the recalibration math lives inline there). Read the BID doc before tuning any number here.

## Input

`/content-gap-analysis <competitor-domain> [<competitor-domain> ...] [--our-domain <domain>]`

Examples:
- `/content-gap-analysis competitor1.com competitor2.com`
- `/content-gap-analysis competitor1.com --our-domain mybrand.com`

If `--our-domain` isn't provided, read it from `brand-config.md`.

## Process

1. **Parse input.** Extract competitor domains (CLI args or auto-discover) and read the brand domain from `brand-config.md`.

2. **Resolve competitors.** In order of preference:
   - CLI args (e.g. `/content-gap-analysis competitor1.com competitor2.com`)
   - `brand-config.md` competitor list
   - **Autonomous fallback**: call `mcp__ahrefs__site-explorer-organic-competitors` for the brand domain, take top 3 by organic-keyword intersection
   - Cache the resolved competitors to `content-pipeline/0-keywords/cache/competitors.json` so Layer 1c (`/keyword-aio-gap`) reuses the same set without re-querying

3. **Read brand context.** Audience, products — used downstream to filter the gap list to relevant intent (Layer 2's BID).

4. **Derive the multi-mode Keyword Gap from Ahrefs Site Explorer.** Ahrefs has no single five-mode "Keyword Gap" tool, so build the gap by pulling each domain's organic-keyword footprint and comparing positions. Layer 1b still produces **all five** `gap_mode` tags — the taxonomy is unchanged; only the data source is. For the brand domain AND each competitor domain, call `mcp__ahrefs__site-explorer-organic-keywords` with:
   - `target` = the domain (one call per domain)
   - `country` = "US" (uppercase ISO; or read from `brand-config.md` if specified)
   - `select` = `"keyword,volume,difficulty,traffic_potential,best_position,intents"` (call `doc {tool:"site-explorer-organic-keywords"}` to confirm the exact column names before the first call)
   - `where` (filter expression) = volume ≥ 20 AND difficulty ≤ 70 (Ahrefs KD)
   - `order_by` = `"traffic_potential:desc"`, `limit` = 1000
   - Drop branded terms for competitors (filter out rows whose keyword contains a competitor brand string).

   ### Phase 4b — multi-mode Keyword Gap (computed from the position sets)

   Join the per-domain keyword sets on `keyword` and assign each row a `gap_mode` from the brand's vs the competitors' best positions:

   | `gap_mode` | Position rule (brand vs competitors) | What to do with it |
   |---|---|---|
   | `missing` | Competitors rank (any top-100), brand has no position (the classic content gap) | Default candidates — feed straight into the merged pool |
   | `weak` | Brand ranks 11+, ≥1 competitor in top-10 | Small-effort wins — feed into the pool, prioritization will boost |
   | `unique` | Only one competitor ranks (single point of failure to displace) | High-leverage — feed into the pool, prioritization will boost |
   | `common` | Brand and ≥2 competitors all rank (saturated SERPs) | Feed into the pool with a penalty applied at Layer 5 — keep for completeness, deprioritize |
   | `strong` | Brand ranks top-3, no competitor does (already won) | **Do NOT feed into the writing queue.** Route to `content-pipeline/0-keywords/cache/strong-positions.csv` for tracking only |

   Assignment order (first match wins): `missing` → `weak` → `unique` → `common`. Skip `strong` for the writing pool; write its rows to `cache/strong-positions.csv` with the same column shape so downstream tooling can read them. Cap each mode at 200 rows sorted by traffic_potential descending. (`best_position` is the column the position comparison reads; if `doc` names it differently — e.g. `position` — use that.)

5. **Pull the gap keyword list.** Aim for ~400–800 raw rows across the four pool-eligible modes (missing/weak/unique/common). Tag each with `source=competitor_gap` and the corresponding `gap_mode`.

6. **Auto-relax filters if pool is small.** If fewer than 50 candidates come back at the default filters, automatically re-run once with relaxed thresholds: volume ≥ 5, KD ≤ 80 (Ahrefs). Log the relaxation. If still under 50, continue with what we have — Layer 1c (AIO gap) and Layer 1a-driven seed expansion will widen the pool.

7. **Seed-modifier expansion (Layer 1a integration).** If `content-pipeline/0-keywords/seeds.json` exists:
   - For each seed, call `mcp__ahrefs__keywords-explorer-matching-terms` with `keywords` = the seed, `match_mode:"phrase"`, and `country:"US"` to pull the phrase-match variation pool; filter to keep rows whose keyword contains any of the modifier strings. Use `mcp__ahrefs__keywords-explorer-related-terms` ("also rank for" / "also talk about") for breadth where phrase-match is thin, and `mcp__ahrefs__keywords-explorer-matching-terms` with `match_mode:"terms"` when a modifier is a multi-word phrase that needs broader term expansion.
   - Set `select` to include `keyword,volume,difficulty,traffic_potential,parent_topic,intents` so each result already carries volume, KD, traffic_potential, parent topic (use as the cluster anchor), and the `intents` array. Only call `mcp__ahrefs__keywords-explorer-overview` for a result that came back without an intent label.
   - Tag each row with `source=seed_modifier` and `gap_mode=seed_modifier` (sentinel value — not one of the five gap modes).
   - Cap per-seed expansion at 100 results to keep the merged pool manageable.

8. **Merge and dedupe.** Combine competitor-gap rows with seed-modifier rows. Keep one row per unique keyword:
   - If a keyword appears in both a competitor-gap mode and seed-modifier expansion, set `source=both` and retain BOTH `gap_mode` (from the competitor-gap row) and `competitor_top_position` from the gap row, plus the seed_modifier metadata.
   - If a keyword appears in multiple competitor-gap modes (e.g. it shows up in both `missing` and `weak` because two different competitors are scored differently), keep the row with the higher-priority `gap_mode`. Priority order: `unique` > `weak` > `missing` > `common`.
   - Otherwise keep the source-specific row as-is.

9. **Add columns the downstream layers need:**
   - `keyword` (from Ahrefs)
   - `volume` (monthly searches)
   - `kd_percent` (Ahrefs Keyword Difficulty, 0–100 — column header kept as `kd_percent` for downstream-tooling compatibility)
   - `traffic_potential` (Ahrefs traffic potential of the keyword's parent topic, from `mcp__ahrefs__keywords-explorer-overview` / the `site-explorer-organic-keywords` `traffic_potential` column)
   - `competitor_top_position` (the best position any competitor holds; null for seed_modifier-only rows)
   - `cluster_id` (Ahrefs parent-topic id when available; otherwise empty — Layer 5 uses this for `cluster_authority_gap` boost)
   - `first_keyword_group` (Ahrefs `parent_topic` string; fallback when `cluster_id` is empty)
   - `intents` (array — Ahrefs per-keyword intent classification: informational / navigational / commercial / transactional. Layer 2 uses this as the primary BID-Intent signal)
   - `source` (competitor_gap / seed_modifier / both / aio_gap — Layer 1c will append aio_gap rows)
   - `gap_mode` (missing / weak / unique / common / seed_modifier — populated for every row; `strong`-mode rows go to `cache/strong-positions.csv`, not this CSV)
   - Empty columns for `priority_score`, `brand_fit`, `product_fit`, `notes`, plus the BID/AIO/redteam columns Layers 2-4 will fill

10. **Save as CSV** to `content-pipeline/0-keywords/keyword-ideas.csv`. Use UTF-8, headers in row 1.

11. **Print a one-line summary** (autonomous mode) or suggest running `/keyword-prioritization` next (interactive mode). The summary breaks out row counts per `gap_mode` so the orchestrator can see whether the pool leans `missing` vs `weak` vs `unique`.

## Output

`content-pipeline/0-keywords/keyword-ideas.csv`

A CSV with one row per gap keyword, every row tagged with a `gap_mode`, plus the columns listed above.

`content-pipeline/0-keywords/cache/strong-positions.csv` (parallel — `gap_mode=strong` rows; tracking only, not the writing queue).

## Quality checklist

- [ ] CSV has at least 50 rows (the gap is real)
- [ ] Every row has a `gap_mode` populated (no nulls)
- [ ] No competitor branded terms in the list (e.g. competitor product names)
- [ ] All keywords have volume ≥ 20 (or ≥ 5 if auto-relaxed)
- [ ] All keywords have `kd_percent ≤ 70` (Ahrefs KD; or ≤ 80 if auto-relaxed)
- [ ] `cluster_id` or `first_keyword_group` (Ahrefs parent topic) populated (used by prioritization for cluster_authority_gap)
- [ ] `intents` array populated for ≥ 90% of rows (Layer 2 needs it as the primary BID-Intent signal)
- [ ] File is valid UTF-8 CSV (opens in Excel / Sheets without garbage)
- [ ] `cache/strong-positions.csv` exists when `gap_mode=strong` rows were returned

## When the gap is small

If fewer than 20 results come back, either:
- The brand and competitors are too similar in coverage (good problem) — try different competitors
- The filters were too tight — relax volume to ≥ 5 and KD to ≤ 80 (Ahrefs)
- Ahrefs returned a partial result — re-run

## Autonomous behavior

When invoked from `/keyword-research-pipeline` (or with `BLOG_AGENT_AUTONOMOUS=1` set):

- **Auto-discover competitors** via `mcp__ahrefs__site-explorer-organic-competitors` if neither CLI args nor `brand-config.md` provide any. Take top 3 by organic-keyword intersection. Cache to `cache/competitors.json` so Layer 1c reuses the same set.
- **Run all five gap modes** and tag rows with `gap_mode`. Route `strong` to `cache/strong-positions.csv`; the rest go to the writing pool.
- **Auto-relax filters** if pool is < 50 (volume ≥ 5, KD ≤ 80; once only).
- **Auto-merge seed-modifier expansion** if `seeds.json` exists.
- **No human prompt** — never ask "which competitors?" or "is this enough?"; the orchestrator can't answer.

## When competitors can't be auto-discovered

If `mcp__ahrefs__site-explorer-organic-competitors` returns empty (very rare — usually means the brand domain isn't indexed by Ahrefs, or it's brand-new):

- Log to `cache/competitor-discovery-failed.log`
- Fall through to seed-modifier expansion alone (which doesn't need competitors). Every row will have `source=seed_modifier` and `gap_mode=seed_modifier`.
- Downstream layers handle the empty `competitor_top_position` column gracefully

## Interactive mode (legacy / dev-only)

If neither CLI args nor brand-config nor auto-discovery yields competitors AND `BLOG_AGENT_AUTONOMOUS` is not set, fall back to asking the user. This branch only fires when a human is at the keyboard.

## Tool naming

Tool names are the real Ahrefs MCP tools pinned in `.claude/skills/research/references/ahrefs-mcp-cheatsheet.md`. Call `doc {tool:"..."}` for any tool you haven't used this run to confirm its exact `select` columns / filters before calling it; never invent tool names. **No `mcp__semrush__*` or DataForSEO calls** — both are retired; a Semrush or DataForSEO call from this skill is a migration-leftover bug, not a fallback.
