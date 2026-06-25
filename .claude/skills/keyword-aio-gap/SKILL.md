---
name: keyword-aio-gap
description: Layer 1c of the keyword research pipeline — SKIPPED by default. Ahrefs MCP *does* ship a Brand Radar AI-citation toolkit (so unlike the Semrush/DataForSEO era this is now technically sourceable), but un-skipping 1c is a deliberate methodology change to make separately. Retained as a logged no-op pass-through; never fabricate aio_gap rows. The spec below is the Brand-Radar implementation to switch on when 1c is enabled.
allowed-tools: Read, Write, Bash, mcp__ahrefs__*
---

# Keyword AI-Overview Gap Skill (Ahrefs Brand Radar)

> **DATA LAYER (2026-06-24).** This layer runs on the **Ahrefs MCP** (`mcp__ahrefs__*`); Semrush and DataForSEO are retired. Map every data call to the tools pinned in [`../research/references/ahrefs-mcp-cheatsheet.md`](../research/references/ahrefs-mcp-cheatsheet.md) — read it first, especially the "Bonus capabilities" section (Brand Radar). Params are comma-separated **strings** (not arrays); `select` + `country` are required; call `doc {tool:"brand-radar-ai-responses"}` for any tool you haven't used this run. The logic below (filters, thresholds, output schema) remains binding; only the data calls changed.

> **SKIPPED BY DEFAULT (2026-06-24 orchestrator ruling).** Keep Layer 1c a **logged no-op** for now. This is a *methodology* decision, not a data-availability one: Ahrefs Brand Radar (`brand-radar-ai-responses`, `brand-radar-cited-pages`, `brand-radar-sov-overview`, `site-explorer-ai-responses-count`) genuinely exposes multi-engine AI-citation data — so the gap *is* sourceable now, unlike the Semrush/DataForSEO era where this layer was skipped for lack of any panel. Un-skipping 1c is a deliberate pipeline change to make on its own. Until then: **do not register prompts, do not pull mentions, do not append `aio_gap` rows, and never fabricate `aio_sov_competitor_top`.** Write a one-line "Layer 1c skipped (methodology hold)" note to `cache/aio-gap-summary.md` and return. The full spec below is what to switch on when the layer is enabled.

Find prompts where competitors appear in AI search (Google AI Overview, ChatGPT, Gemini, Perplexity, Copilot) but the brand doesn't. These are "AI-search citation gaps" — queries where the goal isn't traditional ranking, it's getting cited by the AI when someone asks about the topic.

This is the fifth piece of Ryan Law's keyword-research strategy: instead of asking "what keywords should I rank for?", ask "what queries do I want my brand associated with in AI search?" Then work backwards.

## The model: Ahrefs Brand Radar (prompt-centric)

Ahrefs Brand Radar tracks a configurable set of *prompts* (questions / comparisons / "best X" queries) against a panel of AI engines. For each prompt, it reports which brands / domains / URLs each engine cited and the share-of-voice per domain. The signal is multi-engine, prompt-level, and SoV-bearing.

> **Read [`../research/references/ahrefs-mcp-cheatsheet.md`](../research/references/ahrefs-mcp-cheatsheet.md)** ("Bonus capabilities — GEO / AI-citation tracking") for the Brand Radar tool surface before applying any threshold. The cheatsheet is the source of truth for which Brand Radar tools the connected MCP exposes.

## Input

`/keyword-aio-gap`

Reads:
- `brand-config.md` — brand domain + brand name
- `content-pipeline/0-keywords/cache/competitors.json` — produced by `/content-gap-analysis` Layer 1b. Falls back to `site-explorer-organic-competitors` (top-3 by organic intersection) when missing.
- `content-pipeline/0-keywords/keyword-ideas.csv` — current candidate pool. Each surviving candidate seeds 1–3 prompt phrasings.

Optional:
- `--competitors competitor1.com,competitor2.com` — override auto-discovered competitors
- `--max-prompts 200` — cap on prompts registered per run (default 200; respects Brand Radar quota/units)
- `--engines aio,chatgpt,gemini,perplexity,copilot` — restrict the engine panel (default: all that the plan exposes)
- `--regen` — bust the prompt-panel hash cache and re-register from scratch

## Process

### Step 1 — Resolve brand + competitors

1. Read brand domain + name from `brand-config.md`.
2. Load competitors:
   - First: `cache/competitors.json` (Layer 1b output).
   - Else: `--competitors` override.
   - Else: call `site-explorer-organic-competitors` with the brand domain; take top 3 by organic-intersection score.
3. Persist the resolved set to `cache/aio-gap-competitors.json` so the rest of the run is deterministic.

### Step 2 — Generate the prompt panel from the candidate pool

Read `content-pipeline/0-keywords/keyword-ideas.csv`. For each candidate keyword (skip `source=question_mining` rows already covered by Layer 1d), generate **1–3 prompt phrasings**:

| Phrasing | Pattern | When to emit |
|---|---|---|
| Informational | `what is {keyword}?` / `how does {keyword} work?` | Always (1 prompt per candidate) |
| Comparison | `{keyword} vs {competitor-product}` / `best {keyword} alternatives` | Emit only if `gap_mode=missing` or `gap_mode=weak` |
| "Best for X" | `best {keyword} for {audience-persona-from-brand-config}` | Emit only if the candidate has `intents` containing `commercial` |

**Cap**: `--max-prompts` (default 200) per run. If the candidate pool would generate more, prioritize by current `priority_score` (or `volume` if Layer 5 hasn't run yet).

Persist the generated panel to `cache/aio-prompt-panel.json` with `{prompts: [{id, text, source_keyword, source_phrasing}], generated_at, hash}`. The `hash` is `sha256(sorted-prompt-texts)` — used for idempotency in Step 3.

### Step 3 — Register the prompt panel (idempotent, hash-keyed)

Register the panel with Brand Radar (the project/portfolio that tracks AI prompts). Two paths:

- **First run, or hash changed since last run:** create/update the Brand Radar prompt set with the full panel; persist the returned `panel_id` (Brand Radar project/list id) to `cache/aio-panel-registry.json`.
- **Hash unchanged AND `--regen` not passed:** reuse the existing `panel_id`. Skip re-registration. Log "panel reused (hash match)" to the run summary.

Idempotency matters because Brand Radar tracking is metered against the shared Ahrefs units pool. Re-registering an unchanged panel wastes units.

### Step 4 — Pull mentions per engine

Call `brand-radar-ai-responses` for the registered prompt set, filtered to `--engines` (default: full panel); use `brand-radar-cited-pages` to resolve the cited URLs and `brand-radar-sov-overview` for per-domain share-of-voice. The response shape we expect (verify against the cheatsheet / `doc`):

```json
{
  "results": [
    {
      "prompt_id": "...",
      "prompt_text": "...",
      "engine": "aio" | "chatgpt" | "gemini" | "perplexity" | "copilot",
      "responded": true,
      "mentions": [
        {"domain": "candy.ai", "url": "https://candy.ai/...", "rank": 1, "share_of_voice": 0.42},
        ...
      ]
    }
  ]
}
```

Cache the response at `cache/aio-brand-radar-mentions-{panel_id}.json`. TTL **7 days** (Brand Radar data refreshes frequently on Ahrefs's side, but we don't need daily granularity for content planning).

### Step 5 — Compute the gap

For each `prompt_id`, group mentions by domain. A prompt qualifies as a **gap** if:

- At least one competitor domain appears in `mentions` for at least one engine, AND
- The brand domain does NOT appear in `mentions` for ANY engine

For each gap prompt, derive the row payload:

| Field | Computation |
|---|---|
| `keyword` | `prompts[i].source_keyword` (the original candidate the prompt was generated from) |
| `aio_prompt_text` | `prompts[i].text` (the prompt phrasing — useful for the writer, doesn't go in the CSV but lands in the summary) |
| `aio_engines` | comma-list of engines that cited a competitor for this prompt (e.g. `aio,chatgpt,perplexity`) — multi-engine citation = stronger signal |
| `competitor_aio_mention` | comma-list of competitor domains cited |
| `competitor_cited_url` | the most-prominent (highest `rank` / lowest number) competitor URL across the engine panel |
| `aio_sov_competitor_top` | top competitor's share-of-voice for this prompt (max of competitor SoVs across engines) — `priority_score` tie-breaker in Layer 5 |
| `source` | `aio_gap` (or `both` if a prior layer already added the row — see Step 6) |

### Step 6 — Enrich + append to keyword-ideas.csv

For each gap row, call `keywords-explorer-overview` to add `volume`, `difficulty` (KD), `traffic_potential`, `parent_topic`, `intents`. Skip rows with `volume < 20` (signal too thin).

Append to `content-pipeline/0-keywords/keyword-ideas.csv`. Column contract for `aio_gap` source rows:

```
keyword, volume, kd, traffic_potential, parent_topic, intents,
source, competitor_aio_mention, aio_engines, competitor_cited_url,
aio_sov_competitor_top, gap_mode, question_subtype,
priority_score, brand_fit, product_fit, notes, rank
```

The `aio_engines`, `competitor_cited_url`, and `aio_sov_competitor_top` columns are **new** vs the classic-gap rows. The first run after enabling 1c will widen the CSV — that's expected.

If a row already exists for the same `keyword` (e.g. content-gap-analysis surfaced it as `gap_mode=missing`), **merge in place**: set `source=both`, append competitors to `competitor_aio_mention`, write `aio_engines` / `aio_sov_competitor_top` / `competitor_cited_url` as new columns. Don't duplicate the row.

If `keyword-ideas.csv` doesn't exist yet, create it with the standard header (above) — Layer 5 prioritization tolerates absent columns by treating them as default.

### Step 7 — Print the run summary

```
Layer 1c — Brand Radar AI-citation gap analysis
  Brand domain: pleasur.ai
  Competitors: candy.ai, ourdream.ai, createporn.com
  Prompt panel: 187 prompts (hash 1f3a..., cache HIT — reused panel_id 8721)
  Engines queried: aio, chatgpt, gemini, perplexity, copilot
  Prompts with competitor citations: 84
  Prompts with brand AND competitor citations: 12
  Gap prompts (competitor cited, brand not): 72

Top 5 gap prompts by aio_sov_competitor_top:
  1. "best ai girlfriend app 2026"             SoV 0.61   engines: aio,chatgpt,perplexity   competitor: candy.ai
  2. "candy.ai vs ourdream comparison"          SoV 0.55   engines: chatgpt,gemini           competitor: candy.ai
  3. "ai companion app with voice chat"         SoV 0.48   engines: aio,perplexity           competitor: ourdream.ai
  ...
```

Save the summary to `cache/aio-gap-summary.md` for the orchestrator + auto-blog-loop's redteam read.

## Output

- Rows appended to `content-pipeline/0-keywords/keyword-ideas.csv` with `source=aio_gap` (or `both`)
- `cache/aio-prompt-panel.json` — the generated prompt panel + hash
- `cache/aio-panel-registry.json` — `{hash: panel_id}` mapping for idempotency
- `cache/aio-brand-radar-mentions-{panel_id}.json` — raw API response (TTL 7 days)
- `cache/aio-gap-competitors.json` — resolved competitor list for this run
- `cache/aio-gap-summary.md` — human-readable run summary

## Quota handling — 429 → exit 75

Brand Radar is metered against the shared Ahrefs units pool. If `brand-radar-ai-responses` or the prompt-set registration returns HTTP 429:

1. Persist whatever progress was made (panel registration succeeded? mentions fetch partial?) to the cache files above.
2. Append a quota event to `cache/aio-brand-radar-quota.log`.
3. **Exit code 75** — same convention `auto-blog-loop` and the keyword-research-pipeline orchestrator already understand. The orchestrator retries on the next cron cycle; units windows reset on Ahrefs's side.

Don't fall back to Semrush AI Toolkit or DataForSEO — both are retired. Don't fall back to WebFetch — manual scraping won't reproduce Brand Radar's panel methodology.

## Quality checklist

- [ ] At least 1 competitor's mentions were successfully fetched (otherwise Brand Radar may be unauthenticated / the brand isn't tracked — surface clearly)
- [ ] Each gap row has a non-empty `aio_engines` and `aio_sov_competitor_top`
- [ ] No duplicate rows by keyword (existing rows get merged with `source=both`, not duplicated)
- [ ] Cache files are under `content-pipeline/0-keywords/cache/` (gitignored)
- [ ] Summary lists top 5 gap prompts with the citing competitors and engine breakdown
- [ ] Prompt panel hash matches the `cache/aio-panel-registry.json` entry (idempotency working)
- [ ] CSV header includes the three new columns (`aio_engines`, `competitor_cited_url`, `aio_sov_competitor_top`) when this skill writes for the first time

## Why this exists

AI search is increasingly where queries get answered. If competitors are getting cited in Google AI Overview / ChatGPT for "best electric bike under $2000" and the brand isn't, ranking #1 in classic SERP doesn't fix that — the user may never click through. The fix is to **become the source AI cites**. That requires: (a) finding which prompts the AI cites competitors for; (b) writing content that earns those citations.

Layer 5 (`/keyword-prioritization`) gives `aio_gap` keywords a `+1.5` priority boost. The `aio_sov_competitor_top` column adds a tie-breaker — when two keywords tie on `priority_score`, the one with higher competitor SoV-to-displace ranks higher (more headroom to claim).

## When the brand has zero AI-search presence

That's normal for newer brands or brands that haven't optimized for AI search. The skill (when enabled) still runs — every competitor-cited prompt is a gap. The summary calls this out so the orchestrator can prioritize content that earns the brand's first AI citations.

## When competitors aren't in AI search either

If neither brand nor competitors get AI citations for any of the registered prompts, the gap set is empty. That's still useful information. Write a stub row to `cache/aio-gap-summary.md` documenting which prompts were checked and the absence of citations. Layer 5 will see no `aio_gap` source and skip the boost.

## When the prompt panel hashes mismatch

If `cache/aio-panel-registry.json` has a `panel_id` for a hash you don't recognize, the candidate pool changed (Layer 1a/1b/1d ran since the last AIO sweep). Generate a fresh panel; register it; persist the new `(hash, panel_id)` entry. The old `panel_id` stays in the registry for audit but isn't reused.

## When Brand Radar returns multi-engine mentions but no `share_of_voice` field

Some Ahrefs plans expose mentions but not domain SoV. In that case, fall back to **citation count rank** as the SoV proxy:

```
sov_proxy = 1 / rank if rank else 0
aio_sov_competitor_top = max(sov_proxy across engines)
```

Note this in the summary so the editor knows the SoV column is approximate, not raw SoV.

## Caching policy

- **Mentions cache (`aio-brand-radar-mentions-{panel_id}.json`):** 7-day TTL. The orchestrator's weekly keyword-research cadence lines up with the cache TTL — re-fetches happen automatically without manual invalidation.
- **Panel registry (`aio-panel-registry.json`):** persistent. Hashes don't expire; `panel_id`s only get retired when Ahrefs deletes them upstream.
- **Quota log (`aio-brand-radar-quota.log`):** persistent. The auto-blog-loop reads it to throttle subsequent runs after a 429.
- **`--regen`** invalidates the panel registry for the current hash and forces re-registration. Use sparingly — wastes units.
