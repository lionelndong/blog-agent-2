# Ahrefs MCP Cheat Sheet

Maps each content-pipeline research task to the **real** Ahrefs MCP tools (`mcp__ahrefs__*`).
Replaces the Semrush data layer. Verified live 2026-06-24 (Standard plan, 400k units/mo).

> **Always call the `doc` tool first** for any tool you haven't used this run:
> `doc {tool:"keywords-explorer-overview"}` → returns that tool's exact input/output schema
> (valid `select` columns, filters, defaults). The server self-documents; don't guess params.

---

## Connection
- Server `ahrefs`, endpoint `https://api.ahrefs.com/mcp/mcp`, auth `Bearer ${AHREFS_MCP_KEY}`.
- 130 tools. Shares one **400k units/month** workspace pool with the REST `AHREFS_API_KEY`
  (use the raw REST API for bulk/scripted pulls; use the MCP for in-pipeline agent calls).

## Param rules (these bite — get them wrong and you get empty results, billed)
1. **Params are comma-separated STRINGS, not JSON arrays.** ✅ `keywords:"ai girlfriend app"`,
   `select:"keyword,volume,difficulty"`  ❌ `keywords:["ai girlfriend app"]` (gets stringified to
   the literal `["ai girlfriend app"]`, returns 0 rows, still costs ~50 units).
2. **`select` and `country` are REQUIRED** on most endpoints. `country` is an UPPERCASE ISO code
   (`"US"`). `select` lists the columns you want (see verified columns below).
3. `limit` (default 1000), `order_by` like `"volume:desc"`, `where` = filter expression.
4. **Units cost** ≈ 50 base + per-row. Keep `limit` tight on expensive reports. Check budget any
   time with `subscription-info-limits-and-usage`. Stay ≤ $-equivalent budget in PIPELINE.md.
5. Results return as JSON text in the tool `content`. `render-data-table` / `render-time-series-chart`
   / `render-scorecard` exist for display widgets if needed.

---

## Research workflow (Ryan-Law method, mapped to tools)

### 1. Keyword metrics — `keywords-explorer-overview`
`{keywords:"<kw>", country:"US", select:"keyword,volume,difficulty,cpc,parent_topic,parent_volume,traffic_potential,global_volume,intents,serp_features"}`
→ volume, KD, CPC, **parent topic** (write to the parent, not the long-tail), traffic potential,
intent flags. This anchors the beat spec.

### 2. Related / long-tail ideas
- `keywords-explorer-related-terms` — "also rank for" / "also talk about".
- `keywords-explorer-matching-terms` — `match_mode:"phrase"` or `"terms"`.
- `keywords-explorer-search-suggestions` — autocomplete-style.
Pull 50+, then keep only same **parent topic** + same dominant **intent**; group into H2 sections
(each H2 owns 5–15 variants).

### 3. Questions → FAQ source  ⚠️ there is NO dedicated "questions" tool
Build the FAQ from two sources, then **group into 3–5 themes, drop spam, cap ~5 crisp Q&As**:
- `keywords-explorer-matching-terms` `{match_mode:"terms"}` → filter keywords that start with
  `what|how|is|are|can|does|do|why|which|who|where|will|should`.
- `serp-overview` → read `serp_features` for **People Also Ask** entries.
**This is the FAQ fix.** No 12-question dumps, no near-duplicates, no competitor-stuffing.
Each answer ≤ 2–3 sentences, ≤ 1 link.

### 4. SERP + intent — `serp-overview`
`{keyword:"<kw>", country:"US", select:"url,title,position,..."}` (keyword REQUIRED) → top 10 URLs,
positions, DR/UR/word-count where available. Classify dominant intent (informational / commercial /
transactional / mix) and the modal format + item count for the benchmark table.

### 5. Competitor / content gap
- `site-explorer-organic-keywords` — a competitor URL's ranking keywords.
- `site-explorer-top-pages` — their best pages.
- `site-explorer-organic-competitors` — who else ranks for our space.
- `batch-analysis` — DR / traffic / metrics for many URLs at once.
Content gap = competitors' ranking keywords (consensus across 3+ top pages) **minus** ours.

### 6. Authority check
`site-explorer-domain-rating`, `site-explorer-backlinks-stats`, `site-explorer-metrics` →
is this SERP beatable; what secondary keywords winners also rank for.

### 7. Page content
`WebFetch` each top URL. The MCP returns **metadata**, not full page text — WebFetch gives the
H2 list, dominant arguments, evidence used, and opinion gaps for the beat spec.

---

## Bonus capabilities the Semrush layer never had

- **GEO / AI-citation tracking** — `brand-radar-ai-responses`, `brand-radar-cited-pages`,
  `brand-radar-sov-overview`, `site-explorer-ai-responses-count`. Measures how often AI engines
  (ChatGPT, Perplexity, …) actually cite pleasur.ai. This is the GEO goal, finally measurable.
- **Technical SEO audit** — `site-audit-projects`, `site-audit-issues`, `site-audit-page-content`,
  `site-audit-page-explorer`. Replaces the (blocked) Semrush Site Audit.
- **Search Console** — `gsc-keywords`, `gsc-performance-history`, `gsc-performance-by-position`,
  `gsc-pages`. Real clicks/impressions/positions → fuel for the weekly decay-watch + self-analysis.

## Verified keyword `select` columns (keywords-explorer-overview)
`serp_last_update, cpc, volume_mobile_pct, first_seen, volume_desktop_pct, volume_monthly,
parent_topic, global_volume, keyword, searches_pct_clicks_organic_and_paid, clicks, parent_volume,
cps, volume, serp_features, traffic_potential, difficulty, searches_pct_clicks_organic_only,
searches_pct_clicks_paid_only, intents, volume_monthly_history`

## Worked example (verified)
`keywords-explorer-overview {keywords:"ai girlfriend app", country:"US", select:"keyword,volume,difficulty,cpc,parent_topic,traffic_potential,intents"}`
→ `volume 3300, difficulty 69, cpc $90, parent_topic "free ai girlfriend", traffic_potential 86000,
intents {informational, commercial}`.
