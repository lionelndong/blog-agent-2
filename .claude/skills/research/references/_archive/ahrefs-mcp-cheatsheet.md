# Ahrefs MCP Cheat Sheet

Maps each research task to the Ahrefs MCP tools you should call. The exact tool names follow the `mcp__ahrefs__*` namespace once the MCP server connects (run any Ahrefs tool once to discover the full list — the MCP server self-documents its schema).

## Research checklist — what to pull for every keyword

For the primary keyword, call (in order):

| Step | Tool category | What you're getting |
|---|---|---|
| 1 | **Keywords overview** | volume, KD, CPC, parent topic, global volume, intent label |
| 2 | **Keyword ideas / related** | matching terms (phrase + terms match), related terms (also rank for, also talk about) — get 50+, you'll filter to ~10 |
| 3 | **Questions report** | questions report for the parent topic — group into 3–5 themes, drop spammy ones |
| 4 | **SERP overview** | top 10 ranking URLs with DR/UR/word-count/backlinks/traffic for each |
| 5 | **Top-page analysis** (per top result) | URL traffic + top organic keywords for that URL (use to estimate traffic potential) |
| 6 | **WebFetch each top URL** | extract their H2 list, dominant arguments, evidence used, opinion gaps |

For step 6, WebFetch is fine — Ahrefs MCP doesn't generally return full page text. The MCP gives you metadata; WebFetch gives you content.

## Keyword filtering rules

When you get back hundreds of related keywords, keep only ones that:

- Share the **same parent topic** as the primary keyword (these can rank with one article)
- Match the **same dominant intent** (informational/commercial/etc.)
- Have ≥ 10 monthly volume (or no volume but match a strong question theme)
- Aren't pure brand terms for competitors (unless deliberately targeting comparison content)

Group remaining keywords into the article's H2 sections — each H2 should "own" 5–15 keyword variants.

## SERP intent classification

After pulling the SERP, classify the dominant intent based on the result mix:

- **Informational** — guides, definitions, blog posts dominate top 10
- **Commercial investigation** — comparisons, "best X" listicles dominate
- **Transactional** — product/category pages, pricing pages dominate
- **Navigational** — single-brand pages dominate (skip these — usually not worth targeting)
- **Mixed** — note the split (e.g. "5 informational, 3 commercial, 2 transactional") and pick the side your brand fits

Match your article's content type to dominant intent. If SERP is mostly listicles and you write a definitive guide, you're swimming against the current.

## Content gap signals

When summarizing top-ranking pages, flag:

- **Topics covered by ALL** → must include in your article
- **Topics covered by SOME** → differentiation opportunity (include with depth others lack)
- **Topics covered by NONE but in questions report** → high-value angle to own
- **Topics that are clearly outdated** → opportunity for a fresher take
- **Stats/research older than 3 years** → opportunity to cite newer data

## Output

The `research` skill writes to `content-pipeline/1-research/{slug}.md` using the structure in `templates/research-template.md`. Don't dump raw JSON — synthesize into prose the next stage can act on.

## When MCP isn't enough

Ahrefs MCP doesn't currently provide:

- Full text of competing articles → use **WebFetch**
- Real-time citation sources for stats → use **WebFetch + WebSearch** in the `verify-claims` step
- Screenshot URLs of internal Ahrefs reports → handled separately by `generate-screenshot`

If a specific MCP tool isn't responding, fall back to WebFetch on the equivalent Ahrefs report URL (many work with read-only public data).
