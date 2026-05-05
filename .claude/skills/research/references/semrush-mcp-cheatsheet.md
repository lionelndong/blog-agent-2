# Semrush MCP Cheat Sheet

Maps each research task to the Semrush MCP tools you should call. Tool names follow the `mcp__semrush__*` namespace once the Power 1 MCP server connects. **Run the discovery prompt first** to enumerate the actual tool names the server exposes — they're persisted to `../../keyword-research-pipeline/references/semrush-mcp-tool-inventory.md` and that file is the source of truth. The names below are the convention this repository uses; treat them as placeholders until verified.

> **Always read [`../../keyword-research-pipeline/references/semrush-metric-translation.md`](../../keyword-research-pipeline/references/semrush-metric-translation.md) before applying any threshold.** Semrush's KD%, AS, and intent-label scales differ from Ahrefs' KD, DR, and intent heuristics. Transplanting Ahrefs thresholds without translation will silently degrade Layer 2's BID gate.

## Research checklist — what to pull for every keyword

For the primary keyword, call (in order):

| Step | Tool | What you're getting |
|---|---|---|
| 1 | `mcp__semrush__keyword-overview` (Keyword Magic Tool overview) | volume, KD%, CPC, **`intents` array** (informational/navigational/commercial/transactional), trend, competitive density, SERP-features list |
| 2 | `mcp__semrush__keyword-magic-broad` + `mcp__semrush__keyword-magic-phrase` + `mcp__semrush__keyword-magic-related` | matching terms (broad/phrase/exact), related terms, semantic neighbors — get 50+, you'll filter to ~10–15 sharing the **Keyword Strategy Builder cluster** (preferred) or `keyword_overview.first_keyword_group` (fallback) |
| 3 | `mcp__semrush__keyword-magic-questions` | question-form variants for the parent keyword — group into 3–5 themes, drop spammy ones |
| 4 | `mcp__semrush__topic-research` (root keyword = primary) | idea-cluster tree, headlines per cluster, questions per cluster, related searches per cluster |
| 5 | `mcp__semrush__serp-results` (or `mcp__semrush__serp-overview`) | top 10 ranking URLs with AS/Page-AS/word-count/backlink-count/traffic for each, plus the `serp_features` array (look for `ai_overview`, `featured_snippet`, `people_also_ask`) |
| 6 | `mcp__semrush__domain-organic-pages` per top-result domain | URL traffic + top organic keywords for that URL — used to estimate `traffic_potential` (= traffic of #1 page in `domain_organic_pages`) |
| 7 | `WebFetch` each top URL | full page text — extract H2 list, dominant arguments, evidence used, opinion gaps. Semrush MCP returns metadata only. |

For step 7, WebFetch is fine — Semrush MCP doesn't generally return full page text. The MCP gives you metadata; WebFetch gives you content.

## Topic Research playbook

`mcp__semrush__topic-research` returns a tree of *idea clusters* rooted at the seed term. Each cluster has:

- **Headlines** — actual blog headlines other publishers used in this cluster (strong signal of "what gets written")
- **Questions** — what real searchers are asking inside this cluster
- **Related searches** — Google's related-searches block as a list
- **Volume / difficulty** — aggregated cluster-level metrics (use as cluster sort)

Use Topic Research to:

1. **Pre-feed Layer 1a (seed-modifier-prompt)** with the top 5 cluster names per brand category. The seed agent grounds its output in real Semrush clusters rather than just brand-config alone.
2. **Cluster-match related keywords** — when filtering Keyword Magic broad/phrase results, prefer keywords whose `cluster_id` matches the primary keyword's `cluster_id`. Replaces Ahrefs' "share-parent-topic" filter.
3. **Find audience-question landscape** — Topic Research's questions tab is denser than Keyword Magic's questions filter; merge both for full coverage.
4. **Detect content-gap angles** — if a cluster's headlines include a recurring sub-topic NOT covered by the SERP top-5, that's a "covered by no one but the topic graph already knows about it" angle to own.

## .Trends quick-reference

`mcp__semrush__trends-overview` (root URL = brand domain or category-level URL) surfaces:

- **Search-volume momentum** — which queries are trending up vs. down in the brand's category
- **Competitor traffic shifts** — domains gaining/losing share in the category
- **Audience overlap** — which competitor audiences also visit which sites

The redteam agent (Layer 4) reads `trends.md` to ground its (b) "AIO trajectory" critique — a keyword's volume momentum is signal for whether it's worth writing about today vs. next quarter.

## Keyword Strategy Builder (cluster matching)

Semrush's Keyword Strategy Builder (KSB) auto-clusters a keyword pool into topical groups. The `cluster_id` on each keyword is the **replacement for Ahrefs' `parent_topic`**. Use it whenever the legacy method would have called `share_parent_topic`:

- **Same `cluster_id`** → keywords can be ranked together with one article
- **Different `cluster_id`** → separate articles even if the seeds look similar
- **No `cluster_id` returned** → fall back to `keyword_overview.first_keyword_group` (lower-precision but always present)

The prioritization layer also reads `cluster_id` to compute `cluster_authority_gap` (the brand has zero cluster authority but the cluster is low-difficulty → +0.5 boost; the keyword is the entry point to claiming that cluster).

## Domain Overview vs. Domain-vs-Domain (Keyword Gap)

For competitive analysis, use the right tool for the question:

- **`mcp__semrush__domain-overview`** — single-domain snapshot: AS, organic traffic, paid traffic, top keywords, top pages
- **`mcp__semrush__keyword-gap`** — head-to-head against up to 4 competitors. Returns 5 modes:
  - `common` — keywords everyone ranks for (saturated SERPs)
  - `missing` — competitors rank, brand doesn't (the classic "content gap")
  - `weak` — brand ranks 11+, competitors top-10 (small-effort win)
  - `unique` — only one competitor ranks (single point of failure to displace)
  - `strong` — brand top-3, competitors don't (already won; signal not opportunity)

Layer 1b uses all 5 modes and tags each row with `gap_mode`. Layer 5 prioritization applies mode-specific boosts/penalties (see `semrush-metric-translation.md`).

- **`mcp__semrush__organic-competitors`** — auto-discover top-3 competitors when brand-config doesn't list any. Used by Layer 1b's competitor-discovery fallback.

## Keyword filtering rules

When you get back hundreds of related keywords, keep only ones that:

- Share the **same `cluster_id`** as the primary keyword (KSB) — or, if `cluster_id` is unavailable, share `first_keyword_group` (Keyword Magic fallback)
- Match the **same dominant intent** in the `intents` array (informational/commercial/etc.)
- Have ≥ 10 monthly volume (or no volume but match a strong question theme)
- Aren't pure brand terms for competitors (unless deliberately targeting comparison content)

Group remaining keywords into the article's H2 sections — each H2 should "own" 5–15 keyword variants.

## SERP intent classification

Semrush returns the per-keyword `intents` array directly from `keyword-overview` — **use it as the primary signal**, not URL-pattern derivation. The `intents` array contains zero or more of: `informational`, `navigational`, `commercial`, `transactional`. For the BID-Intent test:

- `informational` ∪ `commercial` → PASS (publish-as-blog territory)
- `transactional` → FAIL `serp_is_transactional` (e-commerce-shaped SERP)
- `navigational` → FAIL `serp_is_navigational` (single-brand SERP — usually not worth targeting)
- Empty / mixed-without-clear-dominant → fall back to URL-pattern heuristic on the SERP top-10 (legacy code stays, demoted to tie-breaker)

`tool-led` is **not** a Semrush intent label. The URL/title heuristic for tool detection (paths like `/tools/`, `/calculator/`, `/generator/`; titles like "free X tool") still runs as a separate gate. Tool-led keywords keep their routing to `tool-opportunities.csv` (not the writing queue).

## Content gap signals

When summarizing top-ranking pages, flag:

- **Topics covered by ALL** → must include in your article
- **Topics covered by SOME** → differentiation opportunity (include with depth others lack)
- **Topics covered by NONE but in Topic Research's questions / Keyword Magic's questions / PAA** → high-value angle to own
- **Topics that are clearly outdated** → opportunity for a fresher take
- **Stats/research older than 3 years** → opportunity to cite newer data

## Output

The `research` skill writes to `content-pipeline/1-research/{slug}.md` using the structure in `templates/research-template.md`. Don't dump raw JSON — synthesize into prose the next stage can act on. Also emit `{slug}-data.json` with chartable numbers (cluster volumes, format share, traffic distribution) so `/generate-visuals` can resolve `data=research.<key>` placeholders downstream.

## When MCP isn't enough

Semrush MCP doesn't currently provide:

- Full text of competing articles → use **WebFetch**
- Real-time citation sources for stats → use **WebFetch + WebSearch** in the `verify-claims` step
- Live AIO body capture for keywords Semrush hasn't crawled recently → AI Toolkit AI Response is first-line; WebFetch on `https://www.google.com/search?q=...` is the last-resort fallback
- Screenshot URLs of internal Semrush reports → handled separately by `generate-screenshot`

If a specific MCP tool isn't responding, fall back to WebFetch on the equivalent Semrush report URL where read-only data is available, or surface the failure to the orchestrator. **Never silently swap to Ahrefs** — Ahrefs is retired; an Ahrefs call from a migrated skill is a bug, not a fallback.

## Auth + quota

- Auth env var: `SEMRUSH_API_KEY_BLOG_AGENT` (Doppler-loaded, mirrors `OPENROUTER_API_KEY_BLOG_AGENT`)
- ContentShake may use a separate sub-key: `SEMRUSH_API_KEY_CONTENTSHAKE` — only if the Power 1 MCP gates ContentShake under a different scope
- Rate-limit response: HTTP 429 from any tool → persist progress, exit code 75, the orchestrator handles retry on the next cron cycle (matches the prior Ahrefs convention)
