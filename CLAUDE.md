# Blog Agent — Project Instructions for Claude Code

This is a content engineering pipeline that turns a keyword into a publish-ready blog article. It adapts Ryan Law's content-engineering method (originally described [here](https://ahrefs.com/blog/how-i-do-content-engineering-with-claude-code/)) to **Semrush's Power 1 MCP** as the single source of SEO + AI-search data. The Ryan Law method (BID, AIO cannibalization, redteam, prioritization) is preserved verbatim — only the data source changes, and the keyword research pipeline is enhanced with Semrush capabilities Ahrefs lacked (Topic Research, .Trends, Keyword Strategy Builder, AI Toolkit, ContentShake AI).

## How this project works

The pipeline is decomposed into small, single-purpose **skills** under `.claude/skills/`. Each skill produces a file in a numbered subdirectory under `content-pipeline/`. You can run skills individually or chain them via the master orchestrator skills (`/blog-pipeline`, `/update-pipeline`).

**The single most important rule:** every skill saves its output to disk before finishing. The user reviews stage outputs and re-runs failed stages — never re-run the whole pipeline because of one bad stage.

## Quality bar

Articles must read like they were written by an experienced human editor — the same editorial bar Ryan Law's Ahrefs-era method targets. The user said this multiple times: **content quality is the #1 priority**. If a draft sounds generic or AI-flavored, the pipeline has failed.

Every drafting/editing skill must:
1. Read `brand-config.md` to ground voice, products, and audience
2. Read 2–3 articles from `examples/` to anchor tone (do this every run; don't trust distilled rules alone)
3. Apply the editorial principles in `.claude/skills/draft/references/voice-guide.md`
4. Avoid the forbidden phrases listed in `brand-config.md`

## Editorial principles

- **BLUF** — Bottom Line Up Front. Every section opens with the most important sentence.
- **MECE** — Mutually Exclusive, Collectively Exhaustive. Sections don't overlap; together they cover the topic completely.
- **Problem → Agitate → Solution** for intros.
- **Inverted pyramid** — most important info first, supporting detail after.
- **Show with examples** — concrete examples beat abstract claims every time.
- **Product-led** — when relevant, demonstrate concepts using the brand's tools (designed-in at outline stage by `/product-mentions`, never bolted on during drafting).
- **Cite everything** — every numerical claim has a hyperlinked source. No made-up stats. Ever.
- **Visuals earn their place** — see `templates/editorial-principles-visuals.md`. The same principles above govern visual decisions: a visual is justified only when removing it would cost the reader specific, concrete information. The default for every section's `Visual:` field is `none`. Most sections do not need a visual. AI-written content's most common failure mode is sprinkling decorative visuals everywhere — don't.

## The pipeline

### Keyword research (top of funnel — fills `keyword-queue.csv`)
0. `/topic-discovery` — Semrush Topic Research + .Trends category-level idea graph & trending topics (Layer 0; idempotent)
1. `/seed-modifier-prompt` — generate seeds + modifiers, grounded in Layer 0's topic graph
2. `/content-gap-analysis` — Semrush Organic Competitors + multi-mode Keyword Gap (common/missing/weak/strong/unique)
3. `/keyword-aio-gap` — Semrush AI Toolkit (multi-engine: AIO, ChatGPT, Gemini, Perplexity, Copilot)
4. `/keyword-question-mining` — Keyword Magic "Questions" filter + PAA mining (Layer 1d)
5. `/keyword-vet-bid` — BID method (Business / Intent / Difficulty); Semrush AS + KD% + intent classifier
6. `/keyword-vet-aio` — AIO cannibalization check via AI Toolkit AI Response
7. `/keyword-redteam` — adversarial sub-agent challenges survivors
8. `/keyword-prioritization` — emit `keyword-queue.csv` (top 50 ranked)
9. `/keyword-research-pipeline` — run all of the above end-to-end

### Creation (keyword → publish-ready article)
1. `/research` — Semrush Keyword Magic Tool + Topic Research + SERP analysis + top-page summaries + **deep web research via Perplexity (OpenRouter)**
4. `/brand-reference` — find existing articles on your blog covering this topic
5. `/outline` — H2/H3 structure with BLUFs
6. `/product-mentions` — annotate where to mention which products
7. `/draft` — expand to full prose
8. `/quality-check` — score voice match, BLUF compliance, forbidden phrases, claim density + adversarial read; gates the pipeline if verdict is FAIL
9. `/verify-claims` — find sources for every stat, add hyperlinks
10. `/optimize-content` — Semrush ContentShake AI scores + iterative voice-preserving rewrites (no Chrome required)
11. `/generate-visuals` — produce real assets per typed `[VISUAL:...]` placeholder (Playwright screenshots, Replicate-generated SFW images via GPT-image-2 / Nano Banana, matplotlib charts) and flag video / external / adult-content for manual capture
12. `/preview` — render HTML preview
13. `/format-for-publish` — package as clean markdown + Strapi JSON payload (with optional direct API publish via Doppler)
14. `/blog-pipeline <keyword> [--context "..."]` — run the whole chain

### Update (existing article → refreshed)
1. `/extract-content <url>` — pull article content + metadata
2. `/update-guidance` — set update priorities
3. `/update-claims` — find outdated stats, propose replacements
4. `/update-product-mentions` — find missed product features
5. `/update-topic-gaps` — find missing sections vs current SERP
6. `/update-draft` — consolidate audits into refreshed article
7. `/update-preview` — side-by-side diff HTML
8. `/update-pipeline <url> [--context "..."]` — run the whole update chain

## Folder conventions

- `content-pipeline/{N-stage}/{slug}.md` — output of stage N for a given slug
- `content-pipeline/0-context/{slug}.md` — captured `--context` input for that slug
- `content-pipeline/0-keywords/keyword-ideas.csv` — keyword research output
- `content-pipeline/images/{slug}/screenshot-urls.md` — screenshot placeholder URLs
- `content-pipeline/updates/{N-stage}/{slug}.md` — update pipeline outputs

Use `python scripts/slugify.py "your keyword phrase"` to get a consistent slug. Use `python scripts/pipeline_status.py <slug>` to see which stages have run from the CLI, or `python scripts/whiteboard.py` to launch the local web dashboard for visual pipeline management (preview / edit / re-run).

## Semrush MCP (Power 1)

The Semrush "Power 1" MCP server is configured in `.mcp.json` (single HTTP MCP at `https://mcp.semrush.com/v1/mcp` — verify the exact URL the user is provisioned with on first run). It powers everything: keyword research (Keyword Magic, Topic Research, .Trends, Keyword Strategy Builder), SERP analysis, Organic Competitors, multi-mode Keyword Gap, the AI Toolkit (AIO / ChatGPT / Gemini / Perplexity / Copilot citations + share-of-voice), and ContentShake AI for content optimization.

First use triggers an OAuth consent flow — approve it once.

**Auth env var:** `SEMRUSH_API_KEY_BLOG_AGENT` — load via Doppler (`doppler run -- claude`). Mirrors the OpenRouter convention. If Semrush gates ContentShake under a sub-key, the optimize-content skill picks up `SEMRUSH_API_KEY_CONTENTSHAKE` separately.

**Tool-name discovery (one-shot, after first connection):** run a discovery prompt to enumerate the actual `mcp__semrush__*` tool names the server exposes, and persist them to `.claude/skills/keyword-research-pipeline/references/semrush-mcp-tool-inventory.md`. Every skill references that file as the source of truth on tool naming. Without it, skill briefs may guess wrong on naming.

**Ahrefs retirement:** Ahrefs is no longer in `.mcp.json`. Archived references (cheatsheet, products catalog) live under `.claude/skills/**/references/_archive/` for rollback. To revert, `git revert` the migration commit and redo the Ahrefs OAuth.

**Metric translation gotchas:** Semrush AS ≠ Ahrefs DR; Semrush KD% is materially stricter than Ahrefs KD; "parent topic" maps to Keyword Strategy Builder cluster id. See `.claude/skills/keyword-research-pipeline/references/semrush-metric-translation.md` — every BID/AIO/prioritization skill links there before applying thresholds.

## ContentShake AI (content optimization)

The `/optimize-content` skill calls Semrush ContentShake AI directly via API — no Chrome MCP, no TipTap injection, no port-8766 CORS server. The skill enforces a monthly API-call budget via `BLOG_AGENT_CONTENTSHAKE_MONTHLY_CAP` (default 100). Voice drift > 8 pts on `/quality-check` triggers a rollback, mirroring the prior safety net.

## OpenRouter (deep research)

The `/research` skill calls OpenRouter to fetch what WebFetch can't reach (Reddit, Cloudflare-blocked sites, forums). Configuration:

- **Env var:** `OPENROUTER_API_KEY_BLOG_AGENT` — load via Doppler (`doppler run -- claude`)
- **Default model:** `perplexity/sonar-reasoning-pro` (web-grounded, citation-heavy)
- **Fallback model:** `openai/o4-mini` (used only if Perplexity errors)
- **Where it runs:** `.claude/skills/research/scripts/openrouter_research.py`
- **Output:** `content-pipeline/1-research/{slug}-deep.md` alongside the main dossier

If the env var isn't set, `/research` skips deep research and notes this in the dossier — pipeline still runs.

## Style guide

When writing or editing prose, **read 2–3 example articles from `examples/` first**. The voice in those files is the source of truth. The rules in `voice-guide.md` are guardrails, not the spec.
