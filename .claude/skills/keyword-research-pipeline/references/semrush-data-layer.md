# Keyword pipeline data layer — real Semrush MCP calls per layer (2026-06-12)

**This file supersedes every `mcp__semrush__<kebab-name>` and every DataForSEO reference inside the layer SKILL.md files.** Those tool names (`keyword-overview`, `keyword-magic-*`, `serp-results`, `serp-overview`, `topic-research`, `trends-overview`, `organic-competitors`, `keyword-gap`, `ai-toolkit-*`, `domain-overview`) never existed on the live server; DataForSEO is retired. The server has exactly 13 tools and one call pattern:

```
get_report_schema(toolkit, report)  →  execute_report(toolkit, report, params)
```

Full inventory + schemas: [`semrush-mcp-tool-inventory.md`](./semrush-mcp-tool-inventory.md). Task→report quick map: [`../../research/references/semrush-mcp-cheatsheet.md`](../../research/references/semrush-mcp-cheatsheet.md). Always `database: "us"` unless told otherwise; `display_limit` ≤ 50 (≤100 only in Layer 1b expansion).

## Layer 0 — `/topic-discovery`

| Old fictional call | Real call |
|---|---|
| `topic-research` (idea-cluster tree) | `keyword_research/phrase_related` on each of the brand's 3–5 category seeds (limit 30) — cluster by shared head terms; plus `keyword_research/phrase_questions` (limit 20/seed) |
| `trends-overview` (market momentum) | run `trends_research` discovery once; if a traffic-overview report is available on this plan, pull it for own domain + top-2 competitors; otherwise skip momentum and note it |
| own-domain footprint | `organic_research/domain_organic_unique` (limit 30) on the brand domain |

## Layer 1b — `/content-gap-analysis`

| Old | Real |
|---|---|
| `organic-competitors` | `organic_research/domain_organic_organic` `{domain: <brand>, display_limit: 15}` → competitor domains by keyword overlap; cache to `cache/competitors.json` |
| `keyword-gap` (multi-mode) | `organic_research/domain_domains` `{domains: "*|or|<brand>|*|or|<competitor>"}` pairwise per competitor (limit 50–100). Derive `gap_mode` from position columns: competitor ≤20 & brand absent → `missing`; both ranked, brand worse → `weak`; brand better → `strong`; both similar → `common` |
| `keyword-magic-broad/phrase/related` seed expansion | `keyword_research/phrase_fullsearch` (contains-seed variants) + `keyword_research/phrase_related` (semantic neighbors), limit 50 each, modifiers applied as post-filter in code |
| `keyword-overview` per-row enrichment | `keyword_research/phrase_these` `{phrase: "kw1;kw2;…"}` batched 50/call; add `phrase_kdi` for difficulty on survivors only (50 u/line — don't KD the whole pool) |
| per-row `intents` array | attempt `export_columns: ["Ph","Nq","Cp","Co","Nr","In"]` on `phrase_these`; if the API rejects `In`, leave intent blank — Layer 2 infers it from SERP shape |

## Layer 1c — `/keyword-aio-gap`

**SKIPPED — provider capability.** This MCP server exposes no AI-visibility toolkit (no `ai-toolkit-*`). Log the skip in the run summary. Revisit if Semrush ships AI-toolkit reports on MCP.

## Layer 1d — `/keyword-question-mining`

| Old | Real |
|---|---|
| `keyword-magic-questions` | `keyword_research/phrase_questions` per surviving seed (limit 30–40) |
| PAA strings from `serp-results` | **dropped** — `phrase_organic` returns ranking URLs, not PAA boxes. `phrase_questions` carries the question load. (Optional future: Firecrawl search for PAA harvesting.) `question_subtype` is always `km_question` for now |

## Layer 2 — `/keyword-vet-bid`

| Old | Real |
|---|---|
| `keyword-overview` | `phrase_these` (volume, CPC, competition) — batched |
| difficulty | `phrase_kdi` (batchable with `;`) |
| `serp-overview` / `serp-results` (SERP shape) | `keyword_research/phrase_organic` `{phrase, display_limit: 10}` → who ranks, what URL patterns (listicle/forum/product) |
| `domain-overview` (authority of rankers) | `overview_research/domain_ranks` per distinct top domain (dedupe first — many keywords share rankers) |
| Intent | `In` column if accepted (see Layer 1b); else classify from the SERP's URL/title patterns and say so in the log |

## Layer 3 — `/keyword-vet-aio`

| Old | Real |
|---|---|
| `serp-overview` `ai_overview` flag | `phrase_these` with `export_columns: ["Ph","Nq","Fk"]` — `Fk` lists SERP features; AIO presence = features list contains the AI-overview marker. If the API rejects `Fk`, set `aio_presence: unknown`, PASS the keyword, and log the blind spot — never guess |
| `ai-toolkit-response` (AIO completeness rating) | **dropped** (no such tool). The vet is presence-only now: present + informational head term → apply the cannibalization penalty in scoring; absent → clean |

## Layers 1a / 4 / 5 — `/seed-modifier-prompt`, `/keyword-redteam`, `/keyword-prioritization`

No external data calls — unchanged. Prioritization consumes whatever columns upstream layers produced; treat missing `aio_*` columns as neutral (no boost, no penalty).

## Budget

Full pipeline run ≈ 15–30k API units (~$1–2). The expensive lines: `domain_domains` (80 u/line) and `phrase_kdi` (50 u/line) — gate both behind survivor lists, never run them on the raw pool.
