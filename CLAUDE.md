# Blog Engine — Project Instructions for Claude Code

This is a content engineering pipeline that turns a keyword into a publish-ready blog article. It implements Ryan Law's content-engineering method ([article](https://ahrefs.com/blog/how-i-do-content-engineering-with-claude-code/), Ahrefs podcast 2026) on the **Ahrefs MCP** as the source of SEO, keyword, SERP, and competitive data.

**2026-06-24 provider ruling (supersedes the 2026-06-12 Semrush ruling):** the **Ahrefs MCP** (`mcp__ahrefs__*`) is the primary data provider — Keyword Magic-equivalent overview, matching/related terms, SERP overview, and Site Explorer all return data via the MCP server (`https://api.ahrefs.com/mcp/mcp`, `Bearer ${AHREFS_MCP_KEY}`). Semrush, DataForSEO, and ContentShake are **retired** from the main path; do not call any of them in any skill. Firecrawl handles full-page extraction of ranking content; Perplexity (OpenRouter) handles deep web research.

## Operating context: this engine runs inside Paperclip (read this first if you are the EO agent)

This repo is operated by the **EO agent** of the Pleasur.AI company on the Paperclip platform — not by a human at a terminal. That changes four things:

1. **Secrets & launch.** All credentials flow through Doppler with the company key:
   `DOPPLER_TOKEN="$DOPPLER_KEY" doppler run --project pleasurai --config dev -- <cmd>`.
   Launching via `scripts/run_pipeline.sh` loads the **Ahrefs MCP** from `.mcp.json`. In a plain
   heartbeat session (no repo MCP loaded), call the **Ahrefs REST API** instead — same data, same
   endpoints (e.g. `curl -H "Authorization: Bearer $AHREFS_API_KEY" "https://api.ahrefs.com/v3/keywords-explorer/overview?country=us&keywords=..."`).
   Both paths are sanctioned and share the same 400,000-units/month workspace pool; the cheatsheet's
   task→tool table applies to either.
2. **Coordination.** One Paperclip issue per article run (never per stage). Every touch leaves a
   comment: status, what changed, next action. Stage state lives on disk in `content-pipeline/`
   and the board watches it on the whiteboard (http://100.73.44.58:8770/). Report each article's
   BEAT-SPEC numbers + final scorecard on the run issue.
3. **Publishing reality (two-layer).** `format-for-publish` pushes to Strapi, but the public site
   reads Supabase `blog_posts`, mirrored by a buggy poller (PLE-1334), AND the mirror only holds
   `status='published'` when an approval-registry row exists (PLEAA-581) — which is created by
   **committing `content-pipeline/8-publish/<slug>/manifest.json` to this repo's `main`**. So the
   durable publish step is: publish to Strapi → commit the publish package to main → verify the
   public URL. A manual Supabase status flip is an emergency unblock only, not durable.
4. **Autonomy.** Fully autonomous within the gates (`BLOG_AGENT_AUTONOMOUS=1 UNATTENDED=1
   BLOG_AGENT_AUTO_PUBLISH=1`): when gates pass, publish — no human review. Escalate only
   legal/privacy/brand-risk copy or hard tool failures. The agent-level operating docs
   (AGENTS.md / PIPELINE.md / TOOLS.md in the agent's Paperclip instructions bundle) cover cadence
   and escalation; **this repo is canonical for pipeline mechanics** — on contradiction, the repo
   wins and the contradiction gets reported on the run issue.

## How this project works

The pipeline is decomposed into small, single-purpose **skills** under `.claude/skills/`. Each skill produces a file in a numbered subdirectory under `content-pipeline/`. You can run skills individually or chain them via the master orchestrator skills (`/blog-pipeline`, `/update-pipeline`).

**The single most important rule:** every skill saves its output to disk before finishing. The user reviews stage outputs and re-runs failed stages — never re-run the whole pipeline because of one bad stage.

## Quality bar — beat the SERP, not the checklist

Past failure mode (diagnosed 2026-06-12, board review): articles scored 88–95 on the internal rubric while being objectively thin — 1,100 words against SERPs whose winners run 2,500+, 4 items where the SERP demands 7–10, no comparison table where every ranking page has one, one rhetorical tic repeated eight times. The rubric measured *compliance* (forbidden phrases, paragraph lengths) instead of *competitiveness*. That is over.

The new quality contract, enforced end-to-end:

1. **`/research` produces a quantified SERP benchmark and a "beat spec"** — median word count of the top 3, section counts, item counts for listicles, table/visual usage, consensus topics, gaps. The beat spec states what this article must do to deserve the click: format parity or better, every consensus topic covered, at least one genuine information gain.
2. **`/outline` is bound by the beat spec.** Section count and per-section word targets come from the SERP, not from a fixed cap. If the SERP demands a 9-app listicle with a comparison table, the outline has 9+ apps and a comparison table.
3. **`/draft` is judged on depth and specificity, not surface metrics.** Voice comes from `examples/` (read them every run), not from numeric paragraph/em-dash quotas.
4. **`/quality-check` scores against the benchmark.** The leading question is: *"a reader opens this and the #1 result side by side — which do they keep?"* PASS requires ≥ 85 overall AND no dimension below 60% of its weight.

If a draft sounds generic or AI-flavored, the pipeline has failed — regardless of what any score says.

## Editorial principles

- **BLUF** — Bottom Line Up Front. Every section opens with the most important sentence.
- **MECE** — Mutually Exclusive, Collectively Exhaustive. Sections don't overlap; together they cover the topic completely.
- **Problem → Agitate → Solution** for intros.
- **Inverted pyramid** — most important info first, supporting detail after.
- **Show with examples** — concrete examples beat abstract claims every time. Specifics (names, numbers, steps, screenshots) are the unit of quality.
- **Product-led** — when relevant, demonstrate concepts using the brand's tools (designed-in at outline stage by `/product-mentions`, never bolted on during drafting).
- **Cite everything** — every numerical claim has a hyperlinked source. No made-up stats. Ever.
- **Visuals earn their place** — see `templates/editorial-principles-visuals.md`. A visual is justified when removing it would cost the reader concrete information.
- **Information gain** — every article contains at least one thing the top 10 don't have: an original comparison, first-hand product walkthrough, fresh data, a genuinely better explanation. "Same topics, nicer words" is not an article.

## The pipeline

### Keyword research (top of funnel — fills `keyword-queue.csv`)
0. `/topic-discovery` — Ahrefs-backed seed/category discovery (Layer 0; idempotent)
1. `/seed-modifier-prompt` — generate seeds + modifiers, grounded in Layer 0's topic graph
2. `/content-gap-analysis` — Ahrefs `site-explorer-organic-competitors` (competitor discovery) + `site-explorer-organic-keywords` (keyword gap) + `keywords-explorer-matching-terms`/`keywords-explorer-related-terms` expansion
3. `/keyword-aio-gap` — SKIPPED by default (logged no-op). Ahrefs Brand Radar (`brand-radar-ai-responses`, `brand-radar-cited-pages`) now exposes the AI-citation data to enable it, so un-skipping Layer 1c is a deliberate methodology change you can make — not on by default.
4. `/keyword-question-mining` — Ahrefs `keywords-explorer-matching-terms` (`match_mode:"terms"`, question-word filter) + SERP People-Also-Ask mining
5. `/keyword-vet-bid` — BID method (Business / Intent / Difficulty); `keywords-explorer-overview` `difficulty` + intent + `serp-overview` SERP shape
6. `/keyword-vet-aio` — AI-Overview cannibalization check via `serp-overview`'s `serp_features` where available
7. `/keyword-redteam` — adversarial sub-agent challenges survivors
8. `/keyword-prioritization` — emit `keyword-queue.csv` (top 50 ranked)
9. `/keyword-research-pipeline` — run all of the above end-to-end

### Creation (keyword → publish-ready article)
1. `/research` — Ahrefs metrics + SERP benchmark + Firecrawl top-page extraction + deep research (Perplexity) → dossier **with beat spec**
2. `/brand-reference` — find existing articles on your blog covering this topic
3. `/outline` — H2/H3 structure with BLUFs, bound by the beat spec
4. `/product-mentions` — annotate where to mention which products
5. `/draft` — expand to full prose, anchored in `examples/`
6. `/quality-check` — benchmark-relative scorecard + adversarial read; gates the pipeline
7. `/verify-claims` — find sources for every stat, add hyperlinks
8. `/optimize-content` — benchmark-relative scoring + voice-preserving rewrites (against the dossier's beat spec and `examples/`; no external optimizer)
9. `/generate-visuals` — produce real assets per typed `[VISUAL:...]` placeholder
10. `/preview` — render HTML preview
11. `/format-for-publish` — package as clean markdown + Strapi JSON payload (markdown tables → rendered table-cards until the site renderer supports GFM)
12. `/blog-pipeline <keyword> [--context "..."]` — run the whole chain

### Update (existing article → refreshed)
1. `/extract-content <url>` — pull article content + metadata
2. `/update-guidance` — set update priorities
3. `/update-claims` — find outdated stats, propose replacements
4. `/update-product-mentions` — find missed product features
5. `/update-topic-gaps` — find missing sections vs current SERP
6. `/update-draft` — consolidate audits into refreshed article
7. `/update-preview` — side-by-side diff HTML
8. `/update-pipeline <url> [--context "..."]` — run the whole update chain

### Self-improvement
- `/skill-eval <stage> <keyword>` — run a stage with and without its skill file, compare outputs, propose skill edits (Ryan Law principle #3). Run after any board complaint about a stage, and monthly per stage.

## Folder conventions

- `content-pipeline/{N-stage}/{slug}.md` — output of stage N for a given slug
- `content-pipeline/0-context/{slug}.md` — captured `--context` input for that slug
- `content-pipeline/0-keywords/keyword-queue.csv` — vetted keyword queue
- `content-pipeline/images/{slug}/` — generated/captured visuals
- `content-pipeline/updates/{N-stage}/{slug}.md` — update pipeline outputs

Use `python scripts/slugify.py "your keyword phrase"` for slugs, `python scripts/pipeline_status.py <slug>` for stage status, `python scripts/whiteboard.py` for the web dashboard.

## Ahrefs MCP — how to actually call it

Configured in `.mcp.json` as a single HTTP MCP at `https://api.ahrefs.com/mcp/mcp` with header `Authorization: Bearer ${AHREFS_MCP_KEY}` (env-expanded; load via `doppler run -- claude`). **No OAuth, no token refresh, no session juggling.** `scripts/run_pipeline.sh` is just a Doppler wrapper now.

The server exposes ~130 tools (`mcp__ahrefs__*`) — keyword (`keywords-explorer-overview`, `keywords-explorer-matching-terms`, `keywords-explorer-related-terms`, `serp-overview`), Site Explorer (`site-explorer-organic-keywords`, `site-explorer-top-pages`, `site-explorer-organic-competitors`, `site-explorer-domain-rating`, `site-explorer-metrics`), Brand Radar / AI-citation (`brand-radar-ai-responses`, `brand-radar-cited-pages`), Site Audit, and Search Console — plus the self-documenting `doc` tool. The workflow is always:

```
doc {tool:"<tool-name>"} (returns exact input/output schema) → call the tool with verified params
```

- **Source of truth for tool names + params:** the live `doc` tool. Call `doc {tool:"keywords-explorer-overview"}` for any tool you haven't used this run; never guess tool names.
- **Task → tool mapping:** `.claude/skills/research/references/ahrefs-mcp-cheatsheet.md`. Every skill that touches Ahrefs reads the cheatsheet first.
- **Param rules that bite:** params are comma-separated **strings**, not JSON arrays (`keywords:"ai girlfriend app"`, not `["ai girlfriend app"]`); `select` and `country` (UPPERCASE ISO, `"US"`) are required on most endpoints.
- **API units are real money.** ~50 units base + per-row. Keep `limit` tight on expensive reports; check budget any time with `subscription-info-limits-and-usage`. The weekly data-spend guardrail in `PIPELINE.md` covers Ahrefs units.

## Firecrawl (top-page extraction)

`/research` and `/update-topic-gaps` extract full content of ranking pages via the Firecrawl API (`FIRECRAWL_API_KEY` via Doppler). One POST to `https://api.firecrawl.dev/v1/scrape` with `{"url": ..., "formats": ["markdown"]}` per page. Prefer it over WebFetch for SERP competitors — it defeats most bot walls and returns clean markdown. WebFetch remains the fallback if Firecrawl errors or the budget is tight.

## Content optimization

The `/optimize-content` skill scores the draft against the dossier's beat spec and the `examples/` voice anchors, then applies voice-preserving rewrites — no external content optimizer (ContentShake is retired with Semrush). Voice drift > 8 pts on `/quality-check` triggers a rollback.

## OpenRouter (deep research)

- **Env var:** `OPENROUTER_API_KEY_BLOG_AGENT` (Doppler)
- **Default model:** `perplexity/sonar-reasoning-pro`; fallback `openai/o4-mini`
- **Runner:** `.claude/skills/research/scripts/openrouter_research.py`
- **Output:** `content-pipeline/1-research/{slug}-deep.md`

If the env var isn't set, `/research` skips deep research and notes this in the dossier — pipeline still runs.

## Style guide

When writing or editing prose, **read the `examples/` tree first** — `examples/README.md` explains what each subfolder anchors (voice vs structure vs niche depth). The voice in `examples/voice/` is the source of truth; `voice-guide.md` is guardrails, not the spec. Articles the board grades 9+/10 get promoted into `examples/voice/` — the anchor set is meant to improve over time.
