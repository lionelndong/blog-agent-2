# Semrush MCP Cheat Sheet — REAL tool calls (verified live 2026-06-12)

Maps each research task to actual Semrush MCP calls. The server exposes exactly **13 tools**; there is no `mcp__semrush__keyword-overview`, no `keyword-magic-*`, no `topic-research`, no `serp-results`, no AI-toolkit tool — those names were hallucinated by earlier versions of this repo and break silently. The full live inventory (every toolkit's reports + schemas + per-line API-unit costs) is [`../../keyword-research-pipeline/references/semrush-mcp-tool-inventory.md`](../../keyword-research-pipeline/references/semrush-mcp-tool-inventory.md).

**The only call pattern that exists:**

1. Discovery (optional once you know the report): `mcp__semrush__keyword_research`, `mcp__semrush__organic_research`, `mcp__semrush__url_research`, `mcp__semrush__overview_research`, `mcp__semrush__trends_research`, … (no arguments) — each lists its reports.
2. `mcp__semrush__get_report_schema` `{toolkit, report}` — REQUIRED before the first `execute_report` of a report you haven't called this session.
3. `mcp__semrush__execute_report` `{toolkit, report, params}` — returns CSV-ish text (`;`-separated).

Defaults: `database: "us"`. Keep `display_limit` 30–50 (units are billed per line). Responses are semicolon-separated with a header row.

> **Always read [`../../keyword-research-pipeline/references/semrush-metric-translation.md`](../../keyword-research-pipeline/references/semrush-metric-translation.md) before applying any threshold.** Semrush KD% is materially stricter than Ahrefs KD; AS ≠ DR.

## Task → report mapping

| Research task | toolkit / report | params (beyond `database`) | Cost |
|---|---|---|---|
| Keyword metrics (volume, CPC, competition) | `keyword_research` / `phrase_this` | `phrase` | 10 u/line |
| Batch metrics for many keywords | `keyword_research` / `phrase_these` | `phrase: "kw1;kw2;kw3"` (semicolons, NOT array) | 10 u/line |
| Keyword difficulty | `keyword_research` / `phrase_kdi` | `phrase` (batchable with `;`) | 50 u/line |
| All variations containing the seed | `keyword_research` / `phrase_fullsearch` | `phrase`, `display_limit` | 20 u/line |
| Semantically related / topic neighbors | `keyword_research` / `phrase_related` | `phrase`, `display_limit` | 40 u/line |
| Question keywords | `keyword_research` / `phrase_questions` | `phrase`, `display_limit` | 40 u/line |
| **SERP top organic results for a keyword** | `keyword_research` / `phrase_organic` | `phrase`, `display_limit` (10–20) | 10 u/line |
| Keyword metrics across countries | `keyword_research` / `phrase_all` | `phrase` | 10 u/line |
| Domain's organic keywords (incl. our own blog) | `organic_research` / `domain_organic` | `domain`, `display_limit`, optional `display_filter` | 10 u/line |
| Domain's top traffic pages | `organic_research` / `domain_organic_unique` | `domain`, `display_limit` | 10 u/line |
| **Find organic competitors of a domain** | `organic_research` / `domain_organic_organic` | `domain`, `display_limit` | 40 u/line |
| **Keyword gap between 2–5 domains** | `organic_research` / `domain_domains` | `domains: "*|or|domain1|*|or|domain2"` | 80 u/line |
| Keywords a specific URL ranks for | `url_research` / `url_organic` | `url`, `display_limit` | 10 u/line |
| Domain authority + traffic snapshot | `overview_research` / `domain_ranks` | `domain` | 10 u/line |
| Real traffic / sources / audience (.Trends) | `trends_research` / (run discovery for report list) | varies | 100+ u |

**SERP features / intent columns:** keyword reports accept `export_columns`. Try adding `"Fk"` (SERP features) and `"In"` (intent) to `export_columns` on `phrase_fullsearch` / `phrase_related` / `phrase_these`; if the API rejects the column, drop it and record `aio_presence: unknown` rather than guessing. Default columns when omitted: `Ph, Nq, Cp, Co, Nr`.

## Research checklist — what to pull for every keyword

For the primary keyword, in order:

| Step | Call | What you're getting |
|---|---|---|
| 1 | `phrase_this` (+ `phrase_kdi`) | volume, CPC, competition, results count; KD% |
| 2 | `phrase_fullsearch` + `phrase_related` (limit 40–50 each) | the variation pool — filter to 10–15 same-intent keywords by volume |
| 3 | `phrase_questions` (limit 30–40) | question variants — group into 3–5 themes, drop spam |
| 4 | `phrase_organic` (limit 10–20) | **the SERP**: ranking domains + URLs + positions |
| 5 | Firecrawl each top-5–8 URL (`https://api.firecrawl.dev/v1/scrape`, `formats:["markdown"]`, `FIRECRAWL_API_KEY` via Doppler) | full page content → word count, H2 list, items count, tables, evidence, gaps. WebFetch is the fallback. |
| 6 | `url_organic` per top-3 URL (limit 10) | what else those pages rank for → secondary keywords to fold in |
| 7 | `domain_ranks` per top-3 domain | authority snapshot → is this SERP beatable? |

Steps 5–7 feed the **SERP benchmark + beat spec** (see `/research` SKILL.md §4) — they are not optional garnish; they're where the article's depth targets come from.

## Topic-research approximation

This MCP has no Topic Research tool. Approximate the idea-cluster tree with: `phrase_related` (relevance-sorted neighbors) + `phrase_questions` themes + the H2s harvested from top-ranking pages (step 5). That triangulation gives you the audience-question landscape the old skill expected from `topic-research`.

## Known-good worked example (verified 2026-06-12)

```
execute_report(toolkit="keyword_research", report="phrase_this",
               params={phrase: "ai girlfriend", database: "us"})
→ Keyword;Search Volume;CPC;Competition;Number of Results
  ai girlfriend;74000;0.75;0.02;133

execute_report(toolkit="keyword_research", report="phrase_related",
               params={phrase: "ai girlfriend", database: "us", display_limit: 5})
→ candy ai;…;90500;…  / nomi;…;22200;…  (semicolon CSV, includes Trends column)
```

## Budget discipline

API units are real spend. A full research run ≈ 10 + 50 + 800 + 1600 + 1200 + 200 + 60 + 30 ≈ **~4,000 units (~$0.20 at standard pricing)** — fine. A careless `display_limit: 1000` on `phrase_related` alone is 40,000 units. Cap exploratory pulls at 50 lines; only the keyword-research pipeline's Layer 1b may go to 100.
