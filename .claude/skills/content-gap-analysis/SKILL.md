---
name: content-gap-analysis
description: Layer 1b of the keyword research pipeline. Finds keyword opportunities by comparing the brand's blog against competitors AND by expanding seeds + modifiers via the Ahrefs MCP (keywords-explorer-matching-terms / related-terms). Auto-discovers competitors via site-explorer-organic-competitors when none are provided, derives the keyword gap from competitors' organic keywords minus ours, tags every row with `gap_mode` (`missing` = the write pool, `strong` = track-only), and outputs a candidate-keyword CSV ready for downstream BID/AIO vetting.
allowed-tools: Read, Write, Bash, mcp__ahrefs__*
---

# Content Gap Analysis Skill

> **Data layer: Ahrefs MCP** (`mcp__ahrefs__*`). Read [`../research/references/ahrefs-mcp-cheatsheet.md`](../research/references/ahrefs-mcp-cheatsheet.md) first — string params not JSON arrays (`keywords:"ai girlfriend app"`, not `["ai girlfriend app"]`), `select`+`country` required, `doc {tool:"..."}` any unfamiliar tool. The logic below (filters, thresholds, schema, the two `gap_mode` tags) is binding.

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
   - **`brand-config.md` `## Competitors (PINNED ...)` list** — the source of truth. Use the domains under **"Use these"**; these are vetted subscription companion/girlfriend peers. **When this section exists, use it and DO NOT auto-discover** (auto-discovery is the skewed path that pinned the queue to free-seeker uncensored/smut long-tail — that's exactly what the pinned list exists to prevent). Doctrine #2.
   - **Autonomous fallback (only when no pinned list exists)**: call `mcp__ahrefs__site-explorer-organic-competitors` for the brand domain, take the top organic-keyword-intersection domains, **then filter through the exclude rules below** and keep the top 3 survivors.
   - **Free-seeker / off-category exclude (ALWAYS apply, even to CLI args and the pinned list as a sanity check).** Drop any candidate domain that is:
     - on the brand-config **"NEVER pin / always exclude"** list (e.g. `uncensored.com`, `venice.ai`, `janitorai.com`, `theresanaiforthat.com`, `miniapps.ai`, `ninjachat.ai`, …), OR
     - a directory / aggregator / off-topic giant (AI tool directories, review sites, app stores), OR
     - free-seeker-dominated: spot-check its top ranking keywords (`site-explorer-organic-keywords`, `limit:20`, `order_by:"traffic:desc"`); if ≥ ~40% contain free-seeker modifiers (`free`, `no filter`, `uncensored`, `unfiltered`, `unlimited`, `nsfw generator`), drop it — its gap is full of traffic that won't pay (Doctrine #2).
     Log every dropped domain + reason to `cache/competitors.json`'s `excluded_generic` array.
   - **Cache the resolved competitors atomically** to `content-pipeline/0-keywords/cache/competitors.json` so later layers reuse the same set: build the full JSON in memory and **`Write` the whole file in one shot** (never `Edit` it incrementally — a linter/format hook can race a partial write and corrupt it; see PLE-3063 item 4). Stamp `resolved_at`, `source` (`brand_config_pinned` | `auto_discovered`), `selected_domains`, and `excluded_generic`.

3. **Read brand context.** Audience, products — used downstream to filter the gap list to relevant intent (Layer 2's BID).

4. **Derive the Keyword Gap from Ahrefs Site Explorer.** Ahrefs has no single "Keyword Gap" tool, so build the gap by pulling each domain's organic-keyword footprint and comparing positions. For the brand domain AND each competitor domain, call `mcp__ahrefs__site-explorer-organic-keywords` with:
   - `target` = the domain (one call per domain)
   - `country` = "US" (uppercase ISO; or read from `brand-config.md` if specified)
   - `select` = `"keyword,volume,difficulty,traffic_potential,best_position,intents"` (call `doc {tool:"site-explorer-organic-keywords"}` to confirm the exact column names before the first call)
   - `where` (filter expression) = volume ≥ 20 AND difficulty ≤ 70 (Ahrefs KD)
   - `order_by` = `"traffic_potential:desc"`, `limit` = 1000
   - Drop branded terms for competitors (filter out rows whose keyword contains a competitor brand string).

   ### Phase 4b — Keyword Gap (computed from the position sets)

   Join the per-domain keyword sets on `keyword` and assign each row a `gap_mode` from the brand's vs the competitors' best positions:

   | `gap_mode` | Position rule (brand vs competitors) | What to do with it |
   |---|---|---|
   | `missing` | Competitors rank (any top-100), brand has no position (the classic content gap) | **The write pool** — feed straight into the merged pool |
   | `strong` | Brand ranks top-3, no competitor does (already won) | **Track-only. Do NOT feed into the writing queue.** Route to `content-pipeline/0-keywords/cache/strong-positions.csv` |

   `missing` is the write pool; `strong` is track-only. Rows where both the brand and competitors already rank are not actionable content gaps — drop them. Write `strong` rows to `cache/strong-positions.csv` with the same column shape so downstream tooling can read them. Cap the `missing` pool at 200 rows sorted by traffic_potential descending. (`best_position` is the column the position comparison reads; if `doc` names it differently — e.g. `position` — use that.)

5. **Pull the gap keyword list.** Aim for ~400–800 raw `missing` rows. Tag each with `source=competitor_gap` and `gap_mode=missing`.

6. **Auto-relax filters if pool is small.** If fewer than 50 candidates come back at the default filters, automatically re-run once with relaxed thresholds: volume ≥ 5, KD ≤ 80 (Ahrefs). Log the relaxation. If still under 50, continue with what we have — Layer 1a-driven seed expansion will widen the pool.

7. **Seed-modifier expansion (Layer 1a integration).** If `content-pipeline/0-keywords/seeds.json` exists:
   - For each seed, call `mcp__ahrefs__keywords-explorer-matching-terms` with `keywords` = the seed, `match_mode:"phrase"`, and `country:"US"` to pull the phrase-match variation pool. Use `mcp__ahrefs__keywords-explorer-related-terms` ("also rank for" / "also talk about") for breadth where phrase-match is thin, and `mcp__ahrefs__keywords-explorer-matching-terms` with `match_mode:"terms"` when a modifier is a multi-word phrase that needs broader term expansion.
   - **Retention (do NOT over-drop — PLE-3063 item 3).** Keep a row if it meets the base bar (`volume ≥ 20`, `kd ≤ 70`, same/adjacent parent_topic, not branded). **Modifier presence is a BONUS, NOT a requirement** — the old rule "keep only rows whose keyword contains a modifier string" discarded ~80% of the legitimate seed expansion (last run: only 15 of 68 final rows came from seed_modifier). The matching-terms / related-terms pool for a relevant seed is *itself* the value; modifier-bearing combos (`best <seed>`, `<seed> vs`, `<seed> app`) are a high-priority subset to surface first, not a gate that drops everything else. Tag whether a row is modifier-bearing in `notes` (e.g. `mod=best`) so prioritization can weight it, but retain non-modifier same-parent variations too.
   - Set `select` to include `keyword,volume,difficulty,traffic_potential,parent_topic,intents` so each result already carries volume, KD, traffic_potential, parent topic (use as the cluster anchor), and the `intents` array. Only call `mcp__ahrefs__keywords-explorer-overview` for a result that came back without an intent label.
   - Tag each row with `source=seed_modifier` and `gap_mode=seed_modifier` (sentinel value — not the competitor-gap `missing`/`strong` modes).
   - Cap per-seed expansion at 100 results (sorted by `traffic_potential desc`) to keep the merged pool manageable. **Aim for seed_modifier to contribute a meaningful share of the final pool** (it is the only ideation channel independent of competitor coverage); if it contributes < ~25% of final rows, the retention filter is still too tight — relax to `volume ≥ 5` and re-pull once, and log it.

8. **Merge and dedupe.** Combine competitor-gap rows with seed-modifier rows. Keep one row per unique keyword:
   - If a keyword appears in both the competitor-gap `missing` mode and seed-modifier expansion, set `source=both` and retain `gap_mode=missing` (from the competitor-gap row) and `competitor_top_position` from the gap row, plus the seed_modifier metadata.
   - Otherwise keep the source-specific row as-is.

9. **Add columns the downstream layers need:**
   - `keyword` (from Ahrefs)
   - `volume` (monthly searches)
   - `kd_percent` (Ahrefs Keyword Difficulty, 0–100 — column header kept as `kd_percent` for downstream-tooling compatibility)
   - `traffic_potential` (Ahrefs traffic potential of the keyword's parent topic, from `mcp__ahrefs__keywords-explorer-overview` / the `site-explorer-organic-keywords` `traffic_potential` column)
   - `competitor_top_position` (the best position any competitor holds; null for seed_modifier-only rows)
   - `cluster_id` (Ahrefs parent-topic id when available; otherwise empty — cluster anchor)
   - `first_keyword_group` (Ahrefs `parent_topic` string; fallback when `cluster_id` is empty)
   - `intents` (array — Ahrefs per-keyword intent classification: informational / navigational / commercial / transactional. Layer 2 uses this as the primary BID-Intent signal)
   - `source` (competitor_gap / seed_modifier / both)
   - `gap_mode` (missing / seed_modifier — populated for every row; `strong`-mode rows go to `cache/strong-positions.csv`, not this CSV)
   - Empty columns for `priority_score`, `brand_fit`, `product_fit`, `notes`, plus the BID/AIO columns Layers 2-3 will fill

10. **Save as CSV** to `content-pipeline/0-keywords/keyword-ideas.csv`. Use UTF-8, headers in row 1.

11. **Print a one-line summary** (autonomous mode) or suggest running `/keyword-prioritization` next (interactive mode). **Report the ACTUAL written row count — count the rows in the CSV you just wrote, never the 200 cap (PLE-3063 item 3: last run claimed "200" when only 68 rows were written).** Break out the actual counts per `source`/`gap_mode`:
    ```
    Wrote N rows to keyword-ideas.csv (actual, = `wc -l` minus header):
      competitor_gap (missing):  X
      seed_modifier:             Y   (Y/N = Z% — flag if < 25%)
      both:                      W
      → strong (track-only, separate file): S rows to cache/strong-positions.csv
    Competitors used: <domains>  (source: brand_config_pinned | auto_discovered)
    ```
    If the missing pool was capped, say "capped at 200 from <raw> raw" — but the headline count is always the actual rows written.

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
- [ ] `cluster_id` or `first_keyword_group` (Ahrefs parent topic) populated (cluster anchor)
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

- **Prefer the `brand-config.md` `## Competitors (PINNED ...)` list** — when it exists, use it and skip auto-discovery entirely (it's the fix for the free-seeker skew; Doctrine #2). Only **auto-discover** via `mcp__ahrefs__site-explorer-organic-competitors` when no pinned list exists; then apply the free-seeker / directory exclude filter (step 2) and take the top 3 survivors. Cache atomically (single `Write`, never `Edit`) to `cache/competitors.json` so later layers reuse the same set.
- **Tag rows with `gap_mode`** (`missing` / `strong`). Route `strong` to `cache/strong-positions.csv`; `missing` goes to the writing pool.
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

Tool names are the real Ahrefs MCP tools pinned in `.claude/skills/research/references/ahrefs-mcp-cheatsheet.md`. Call `doc {tool:"..."}` for any tool you haven't used this run to confirm its exact `select` columns / filters; never invent tool names.
