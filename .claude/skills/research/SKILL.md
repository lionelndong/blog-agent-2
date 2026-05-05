---
name: research
description: Gather keyword metrics, related terms, questions, SERP analysis, top-page summaries, and Topic Research idea-cluster context for a target keyword. Triggered when the user runs /research <keyword> or as the first content stage of /blog-pipeline.
allowed-tools: Read, Write, WebFetch, mcp__semrush__*, Bash
---

# Research Skill

Produce a research dossier that the `outline` skill can turn into a structured outline. The dossier consolidates Semrush MCP data (Keyword Magic Tool, Topic Research, SERP, Domain Organic Pages), SERP intelligence, and competitor content gaps into a single file the next stage will read.

> Read [`references/semrush-mcp-cheatsheet.md`](./references/semrush-mcp-cheatsheet.md) before constructing tool calls — it pins the actual tool names and parameter shapes. Tool-name discrepancies trace back to [`../keyword-research-pipeline/references/semrush-mcp-tool-inventory.md`](../keyword-research-pipeline/references/semrush-mcp-tool-inventory.md) (the live inventory).

## Input

A target keyword as a string. Example: `keyword cannibalization`.

If invoked with no argument, read the most recent context file in `content-pipeline/0-context/` and prompt the user for the keyword.

## Process

1. **Slugify the keyword.** Run `python scripts/slugify.py "<keyword>"` and store the slug.
2. **Read brand context.** Read `brand-config.md` for audience, products, voice — research framing should consider what this brand can credibly own.
3. **Pull keyword metrics via Semrush MCP.** Use the playbook in `references/semrush-mcp-cheatsheet.md`:
   - Keyword Overview (volume, KD%, CPC, **`intents` array**, trend, parent cluster) via `mcp__semrush__keyword-overview`
   - Related keywords (broad + phrase + related; aim for 50+ candidates, filter to ~10–15 sharing the same Keyword Strategy Builder cluster — fall back to `first_keyword_group` if KSB cluster unavailable)
   - Questions report — merge `mcp__semrush__keyword-magic-questions` results with Topic Research's questions tab; group into 3–5 themes
   - SERP results / SERP overview for top 10 via `mcp__semrush__serp-results` (or `mcp__semrush__serp-overview`)
   - **Topic Research idea-cluster tree** via `mcp__semrush__topic-research` — root keyword = primary; pull headlines + questions + related searches per top cluster (this is the audience-question landscape the Ahrefs pipeline didn't have)
4. **Analyze the SERP.** Classify dominant intent and content type (guide/listicle/comparison/etc.). Note brand presence. The Semrush per-keyword `intents` array is the primary intent signal — only fall back to URL-pattern heuristics if `intents` is empty or mixed.
5. **Read the top-ranking pages.** WebFetch each of the top 5 URLs. For each, extract: title, H2 list, key arguments, evidence used, what's missing. Be systematic, not summarizing — name the actual structures.
6. **Run deep web research via OpenRouter (Perplexity).** This is the voice-of-customer + community-signals pass that fills gaps WebFetch can't reach (Reddit, Cloudflare-blocked sites, forums, review sites). Call:

   ```bash
   doppler run -- python .claude/skills/research/scripts/openrouter_research.py \
     --keyword "<keyword>" --slug "<slug>"
   ```

   The script defaults to `perplexity/sonar-reasoning-pro` and falls back to `openai/o4-mini` if Perplexity errors. Output lands at `content-pipeline/1-research/{slug}-deep.md`.

   **If `OPENROUTER_API_KEY_BLOG_AGENT` isn't set** (Doppler not configured yet), skip this step and note in the dossier that deep research wasn't available. Don't fail the pipeline.

7. **Identify content gaps.** Cross-reference: Semrush top-page coverage + Topic Research's idea-cluster headlines + WebFetch findings + Perplexity deep research:
   - Topics covered by all → must include
   - Topics covered by some → differentiate with depth
   - Topics covered by none but in Topic Research's questions tab / Semrush questions filter / Perplexity's "voice of customer" → angle to own
   - Direct user quotes from Perplexity → ammunition for the article
8. **Recommend an angle.** A one-sentence thesis for the article that wins against the current SERP. Explain why this angle wins.
9. **Write the dossier.** Save to `content-pipeline/1-research/{slug}.md` using the structure in `../../templates/research-template.md`. Replace template placeholders with real content; do not leave any `{{VAR}}` markers. Add a section called **"Deep web research findings"** that summarizes (not duplicates) the most actionable signals from `{slug}-deep.md` — the deep file stays available for the drafting stage to reference directly.

10. **Emit chartable data.** If the dossier surfaces any numeric breakdown that downstream stages might chart (search-volume clusters, format share, traffic distribution, top-page rankings), also write `content-pipeline/1-research/{slug}-data.json` containing the structured numbers. This is the data file `/generate-visuals` resolves when a chart placeholder uses `data=research.<key>`. Schema:

    ```json
    {
      "cluster_volumes": {"Image / generator": 860000, "Video": 38000, "Chat": 33000, "Apps / sites": 11400},
      "format_share": {"image": 0.85, "video": 0.05, "chat": 0.06, "apps": 0.04},
      "traffic_top_pages": {"page-1-domain.com": 125000, "page-2-domain.com": 95000, "page-3-domain.com": 47000},
      "_meta": {
        "source": "Aggregated from research dossier; cluster volumes from Semrush Keyword Magic Tool + Topic Research",
        "generated_at": "2026-05-03"
      }
    }
    ```

    Each top-level key maps to either a `{label: number}` dict or a `[[label, number], ...]` list of pairs — both are acceptable inputs to `render_chart.py`. Use snake_case keys; the outline / draft skills reference them as `data=research.cluster_volumes` etc. Include a `_meta.source` field so the editor can audit where the numbers came from. Don't fabricate — if a breakdown only has 2 data points, emit 2; if you don't have chartable data, omit the JSON entirely (the chart placeholder will fall back to manual-capture with a clear hint).

## Output

`content-pipeline/1-research/{slug}.md`

The file should be 800–1500 words. Dense, scannable, no fluff. The `outline` skill will read this end-to-end.

## Quality checklist

Before saving, verify:

- [ ] Primary keyword has volume, KD%, intents array, KSB cluster id (or first_keyword_group fallback)
- [ ] At least 8 related keywords sharing the same KSB cluster (or first_keyword_group), with their volumes
- [ ] At least 10 questions grouped into 3+ themes
- [ ] Top 5 SERP results summarized — each has H2 list + key arguments + what's missing
- [ ] Content gaps explicitly listed (must-include / differentiate / own)
- [ ] One-sentence recommended angle with justification
- [ ] No raw JSON dumped; everything is synthesized prose or tidy bullets
- [ ] Brand context is reflected — angle considers what THIS brand can credibly say
- [ ] Deep web research findings section present (or explicit note that OpenRouter wasn't configured)
- [ ] At least 3 verbatim user quotes from Perplexity included (when deep research ran)

## When to re-run

If the SERP has shifted significantly (new competitor ranking, Ahrefs metrics changed) or the recommended angle no longer holds. The `outline` skill depends entirely on this file's quality — re-running here is cheaper than reworking later stages.
