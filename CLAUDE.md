# Blog Engine — Project Instructions for Claude Code

This is a content engineering pipeline that turns a keyword into a publish-ready blog article. It implements Ryan Law's content-engineering method ([article](https://ahrefs.com/blog/how-i-do-content-engineering-with-claude-code/), Ahrefs podcast 2026) on **Semrush MCP** as the source of SEO, keyword, SERP, and competitive data.

**2026-06-12 provider ruling (supersedes 2026-06-10):** Semrush MCP is the primary data provider — the paid plan now has full MCP data access (verified live: `phrase_this`, `phrase_related`, `phrase_organic`, `domain_organic_organic`, `domain_domains` all return data with plain `Apikey` auth, no OAuth). DataForSEO is **retired** from the main path; its scripts live on only as an archived fallback (`scripts/_archive/`). Do not call DataForSEO in any skill. Firecrawl handles full-page extraction of ranking content; Perplexity (OpenRouter) handles deep web research.

## Operating context: this engine runs inside Paperclip (read this first if you are the EO agent)

This repo is operated by the **EO agent** of the Pleasur.AI company on the Paperclip platform — not by a human at a terminal. That changes four things:

1. **Secrets & launch.** All credentials flow through Doppler with the company key:
   `DOPPLER_TOKEN="$DOPPLER_KEY" doppler run --project pleasurai --config dev -- <cmd>`.
   Launching via `scripts/run_pipeline.sh` loads the Semrush **MCP** from `.mcp.json`. In a plain
   heartbeat session (no repo MCP loaded), call the **classic Semrush API** instead — same report
   names, same CSV: `curl "https://api.semrush.com/?type=phrase_this&key=$SEMRUSH_API_KEY&phrase=...&database=us"`.
   Both paths are sanctioned; the cheatsheet's task→report table applies to either.
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
0. `/topic-discovery` — Semrush-backed seed/category discovery (Layer 0; idempotent)
1. `/seed-modifier-prompt` — generate seeds + modifiers, grounded in Layer 0's topic graph
2. `/content-gap-analysis` — Semrush `domain_organic_organic` (competitor discovery) + `domain_domains` (keyword gap) + `phrase_fullsearch`/`phrase_related` expansion
3. `/keyword-aio-gap` — SKIPPED: this MCP server exposes no AI-visibility toolkit. Revisit if Semrush ships one.
4. `/keyword-question-mining` — Semrush `phrase_questions` + SERP People-Also-Ask mining
5. `/keyword-vet-bid` — BID method (Business / Intent / Difficulty); `phrase_kdi` + intent + `phrase_organic` SERP shape
6. `/keyword-vet-aio` — AI-Overview cannibalization check via `Fk` (SERP features) column where available
7. `/keyword-redteam` — adversarial sub-agent challenges survivors
8. `/keyword-prioritization` — emit `keyword-queue.csv` (top 50 ranked)
9. `/keyword-research-pipeline` — run all of the above end-to-end

### Creation (keyword → publish-ready article)
1. `/research` — Semrush metrics + SERP benchmark + Firecrawl top-page extraction + deep research (Perplexity) → dossier **with beat spec**
2. `/brand-reference` — find existing articles on your blog covering this topic
3. `/outline` — H2/H3 structure with BLUFs, bound by the beat spec
4. `/product-mentions` — annotate where to mention which products
5. `/draft` — expand to full prose, anchored in `examples/`
6. `/quality-check` — benchmark-relative scorecard + adversarial read; gates the pipeline
7. `/verify-claims` — find sources for every stat, add hyperlinks
8. `/optimize-content` — Semrush ContentShake AI scores + voice-preserving rewrites
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

## Semrush MCP — how to actually call it

Configured in `.mcp.json` as a single HTTP MCP at `https://mcp.semrush.com/v1/mcp` with header `Authorization: Apikey ${SEMRUSH_API_KEY}` (env-expanded; load via `doppler run -- claude`). **No OAuth, no token refresh, no session juggling.** `scripts/run_pipeline.sh` is just a Doppler wrapper now.

The server exposes **13 tools**: 11 toolkit-discovery tools (`keyword_research`, `organic_research`, `url_research`, `overview_research`, `backlink_research`, `trends_research`, `tracking_research`, `siteaudit_research`, `subdomain_research`, `subfolder_research`, `projects_research`) plus `get_report_schema` and `execute_report`. The workflow is always:

```
discovery tool (lists reports) → get_report_schema(toolkit, report) → execute_report(toolkit, report, params)
```

- **Source of truth for tool/report names:** `.claude/skills/keyword-research-pipeline/references/semrush-mcp-tool-inventory.md` (generated live 2026-06-12 — regenerate with `python scripts/semrush_inventory.py` if Semrush changes the server).
- **Task → report mapping:** `.claude/skills/research/references/semrush-mcp-cheatsheet.md`. Every skill that touches Semrush reads the cheatsheet first; never guess tool or report names — the pre-2026-06-12 skills hallucinated names like `mcp__semrush__keyword-overview` and silently broke.
- **Metric translation gotchas:** Semrush AS ≠ Ahrefs DR; Semrush KD% is materially stricter than Ahrefs KD. See `.claude/skills/keyword-research-pipeline/references/semrush-metric-translation.md` before applying thresholds.
- **API units are real money.** Costs per report line are listed in the inventory (10–100 units/line). Use `display_limit` 30–50. The weekly data-spend guardrail in `PIPELINE.md` covers Semrush units.

## Firecrawl (top-page extraction)

`/research` and `/update-topic-gaps` extract full content of ranking pages via the Firecrawl API (`FIRECRAWL_API_KEY` via Doppler). One POST to `https://api.firecrawl.dev/v1/scrape` with `{"url": ..., "formats": ["markdown"]}` per page. Prefer it over WebFetch for SERP competitors — it defeats most bot walls and returns clean markdown. WebFetch remains the fallback if Firecrawl errors or the budget is tight.

## ContentShake AI (content optimization)

The `/optimize-content` skill calls Semrush ContentShake AI via API. Monthly API-call budget via `BLOG_AGENT_CONTENTSHAKE_MONTHLY_CAP` (default 100). Voice drift > 8 pts on `/quality-check` triggers a rollback.

## OpenRouter (deep research)

- **Env var:** `OPENROUTER_API_KEY_BLOG_AGENT` (Doppler)
- **Default model:** `perplexity/sonar-reasoning-pro`; fallback `openai/o4-mini`
- **Runner:** `.claude/skills/research/scripts/openrouter_research.py`
- **Output:** `content-pipeline/1-research/{slug}-deep.md`

If the env var isn't set, `/research` skips deep research and notes this in the dossier — pipeline still runs.

## Style guide

When writing or editing prose, **read the `examples/` tree first** — `examples/README.md` explains what each subfolder anchors (voice vs structure vs niche depth). The voice in `examples/voice/` is the source of truth; `voice-guide.md` is guardrails, not the spec. Articles the board grades 9+/10 get promoted into `examples/voice/` — the anchor set is meant to improve over time.
