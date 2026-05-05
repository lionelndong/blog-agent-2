# Blog Agent — Powered by Semrush

A Claude Code content-engineering pipeline that turns a keyword into a publish-ready blog article. Adapts Ryan Law's content-engineering method to **Semrush's Power 1 MCP** as the single source of SEO + AI-search data — Keyword Magic Tool, Topic Research, .Trends, Keyword Strategy Builder, Organic Competitors, multi-mode Keyword Gap, AI Toolkit (AIO / ChatGPT / Gemini / Perplexity / Copilot citations), and ContentShake AI for content optimization, all under one MCP.

## Quick start

1. Open this directory in Claude Code.
2. Approve the Semrush MCP OAuth flow on first use (requires a Semrush plan that exposes the Power 1 MCP).
3. Set `SEMRUSH_API_KEY_BLOG_AGENT` via Doppler — `doppler secrets set SEMRUSH_API_KEY_BLOG_AGENT=...` — then run Claude Code as `doppler run -- claude`.
4. Edit `brand-config.md` — fill in your brand name, products, target audience, and voice keywords.
5. Run a smoke test:

   ```
   /blog-pipeline keyword cannibalization --context "Beginner audience, lean on visuals"
   ```

6. Watch the pipeline produce stage outputs in `content-pipeline/`. The HTML preview is at `content-pipeline/7-preview/keyword-cannibalization.html`. When you're ready to publish, run `/format-for-publish keyword-cannibalization` to produce a Strapi-ready package at `content-pipeline/8-publish/keyword-cannibalization/` (markdown body, Strapi JSON payload, paste-or-publish README).

## Dependencies

- **Python 3.9+** for the slugify, pipeline-status, preview, diff, Strapi-format, OpenRouter research, ContentShake-optimize, and quality-check scripts
- **Semrush plan with Power 1 MCP access** — covers Keyword Magic, Topic Research, .Trends, Keyword Strategy Builder, AI Toolkit, ContentShake AI
- **OpenRouter account** (recommended) — powers the deep web research stage via Perplexity (env var `OPENROUTER_API_KEY_BLOG_AGENT`)
- **Doppler CLI** (recommended) — injects `SEMRUSH_API_KEY_BLOG_AGENT`, `OPENROUTER_API_KEY_BLOG_AGENT`, and (later) Strapi creds. Run Claude Code via `doppler run -- claude`

## Whiteboard UI

A local dashboard for inspecting, editing, and re-running pipeline stages — inspired by the UI Ryan Law demoed in his original write-up.

```bash
python scripts/whiteboard.py
# then open http://localhost:8765
```

Features:
- Sidebar shows every pipeline stage with status (done / pending) per slug
- Preview tab renders markdown / HTML for each stage's output
- Edit tab lets you fix outputs in-place and save back to disk (next stage picks up the change)
- Skill tab shows the SKILL.md governing that stage
- Re-run button copies the slash command to your clipboard so you can paste into Claude Code

Standard library only (no Flask). Run on a different port with `--port 9000`.

## How it works

See [CLAUDE.md](./CLAUDE.md) for the full pipeline description and editorial principles.

For unattended operation on a VPS (always-on Chrome + the Claude-in-Chrome extension, cron-fired pipeline runs, recovery procedures), see [docs/vps-deploy.md](./docs/vps-deploy.md).

The pipeline is intentionally decomposed into ~20 small skills. You can:
- **Run the whole chain** with `/blog-pipeline <keyword>` or `/update-pipeline <url>`
- **Run individual skills** like `/research <keyword>` or `/draft <slug>` to redo a single stage
- **Inspect every stage** under `content-pipeline/{N-stage}/{slug}.md`

This is the killer feature: when one stage produces bad output, you fix that stage's prompt or output, then continue from the next stage — no need to regenerate the whole article.

## Customizing voice

The system applies Ryan Law's editorial style (BLUF, MECE, problem-agitate-solution, inverted pyramid, product-led) to whatever brand you configure. To change the voice:

1. Replace files in `examples/` with your own reference articles
2. Edit `.claude/skills/draft/references/voice-guide.md`
3. Update `brand-config.md` voice keywords and forbidden phrases

The `examples/` directory ships with 5 reference articles for voice anchoring — replace with whatever matches your house style.

## Pipeline stages

| Skill | Output |
|---|---|
| `/topic-discovery` | `content-pipeline/0-keywords/topic-graph.json` + `trends.md` (Semrush Topic Research + .Trends; runs once per brand-config change) |
| `/research` | `content-pipeline/1-research/{slug}.md` (+ `{slug}-deep.md` from Perplexity, `{slug}-data.json` chartable numbers) |
| `/brand-reference` | `content-pipeline/2-reference/{slug}.md` |
| `/outline` | `content-pipeline/3-outlines/{slug}.md` |
| `/product-mentions` | `content-pipeline/4-outlines-annotated/{slug}.md` |
| `/draft` | `content-pipeline/5-drafts/{slug}.md` |
| `/quality-check` | `content-pipeline/quality-checks/{slug}.md` (gates pipeline if FAIL) |
| `/verify-claims` | `content-pipeline/6-drafts-cited/{slug}.md` |
| `/optimize-content` | `content-pipeline/optimization/{slug}.md` (Semrush ContentShake AI; no Chrome required) |
| `/generate-visuals` | `content-pipeline/images/{slug}/manifest.json` |
| `/preview` | `content-pipeline/7-preview/{slug}.html` |
| `/format-for-publish` | `content-pipeline/8-publish/{slug}/` (article.md + article.json + README.md, ready for Strapi paste or API publish) |

Update pipeline outputs land under `content-pipeline/updates/`.

Keyword-research outputs (the upstream of `auto-blog-loop`) land under `content-pipeline/0-keywords/` — `seeds.json`, `topic-graph.json`, `trends.md`, `keyword-ideas.csv`, `keyword-queue.csv`, `tool-opportunities.csv`, `redteam-notes.md`.

## Credit

Methodology: [Ryan Law — How I Do Content Engineering with Claude Code](https://ahrefs.com/blog/how-i-do-content-engineering-with-claude-code/) (originally Ahrefs-tooled; this fork is Semrush-tooled with the same editorial method).
