# Semrush MCP Tool Inventory

> **Source of truth** for actual `mcp__semrush__*` tool names exposed by the Power 1 MCP server. Every skill in this repository references this file when constructing tool calls — if a name here is wrong, every dependent skill is wrong.

## How to populate / refresh this inventory

After connecting `.mcp.json`'s `semrush` entry for the first time (or after Semrush adds new tools), run a discovery prompt:

```bash
doppler run -- claude -p "List every mcp__semrush__* tool the connected MCP server exposes. For each tool, return: (1) the exact tool name, (2) its description, (3) the parameter schema as JSON. Output as a markdown table. Persist nothing else; I will paste the table into the inventory file."
```

Paste the resulting table into the **Live inventory** section below. Commit. The skills will pick up the new tool names on next run.

## Conventions

- Names follow `mcp__semrush__<kebab-case-task>` convention (mirrors how `mcp__ahrefs__keywords-explorer-overview` was structured).
- The `semrush-mcp-cheatsheet.md` and the SKILL.md files in this repository use placeholder names (e.g. `mcp__semrush__keyword-overview`) until this inventory is populated. **Treat the placeholders as suggestions only**; the names below override them once verified.

## Live inventory (verified)

> **Status: PENDING DISCOVERY.** Populate after first connection. Until then, the placeholder names in the cheatsheet apply.

| Tool name | Purpose | Parameters | Used by |
|---|---|---|---|
| _populate after running the discovery prompt above_ | | | |

## Placeholder → likely-real mapping (best-effort, pre-discovery)

The following placeholders appear in skill briefs and cheatsheets. After discovery, fill in the **Verified name** column (or strike through and rewrite if Semrush's actual name is different):

| Placeholder used in skills | Verified name (post-discovery) | Skills that reference |
|---|---|---|
| `mcp__semrush__keyword-overview` | _verify_ | research, keyword-vet-bid, keyword-aio-gap, content-gap-analysis, keyword-question-mining |
| `mcp__semrush__keyword-magic-broad` | _verify_ | research, content-gap-analysis |
| `mcp__semrush__keyword-magic-phrase` | _verify_ | research, content-gap-analysis |
| `mcp__semrush__keyword-magic-related` | _verify_ | research, content-gap-analysis |
| `mcp__semrush__keyword-magic-questions` | _verify_ | research, keyword-question-mining |
| `mcp__semrush__keyword-magic-exact` | _verify_ | content-gap-analysis |
| `mcp__semrush__topic-research` | _verify_ | topic-discovery, research, update-topic-gaps |
| `mcp__semrush__trends-overview` | _verify_ | topic-discovery |
| `mcp__semrush__keyword-strategy-builder` | _verify_ | research (cluster matching), prioritization (cluster_authority_gap) |
| `mcp__semrush__serp-results` | _verify_ | research, keyword-vet-bid, keyword-vet-aio, update-topic-gaps, keyword-question-mining |
| `mcp__semrush__serp-overview` | _verify_ | keyword-vet-bid, keyword-vet-aio |
| `mcp__semrush__domain-overview` | _verify_ | keyword-vet-bid (brand AS), auto-blog-loop runbook (sanity check) |
| `mcp__semrush__domain-organic-pages` | _verify_ | research (TP derivation) |
| `mcp__semrush__organic-competitors` | _verify_ | content-gap-analysis (auto-discovery) |
| `mcp__semrush__keyword-gap` | _verify_ | content-gap-analysis (5-mode multi) |
| `mcp__semrush__ai-toolkit-prompts` | _verify_ | keyword-aio-gap (prompts management) |
| `mcp__semrush__ai-toolkit-mentions` | _verify_ | keyword-aio-gap, keyword-vet-aio |
| `mcp__semrush__ai-toolkit-response` | _verify_ | keyword-vet-aio (AIO body fetch) |
| `mcp__semrush__contentshake-optimize` | _verify (may live behind ContentShake API, not MCP)_ | optimize-content |
| `mcp__semrush__contentshake-score` | _verify_ | draft-score (optional self-check) |

## Pivots if the discovery surfaces different naming

- **If Semrush groups tools under fewer endpoints** (e.g. one `mcp__semrush__keyword-magic` tool with a `mode` parameter instead of separate `-broad`/`-phrase`/`-related`): update the cheatsheet step-table and the SKILL.md references in one pass. Same logic; one tool name; pass mode as parameter.
- **If Semrush exposes tools under a different namespace** (e.g. `mcp__semrush_seo__*` and `mcp__semrush_ai__*` separately): split the inventory table by namespace, and update each SKILL.md's `allowed-tools` frontmatter to enumerate both namespaces.
- **If a tool we expect doesn't exist** (e.g. ContentShake is API-only, not MCP): document in the Skills-affected column. Phase 6's `optimize-content` rewrite already plans for this fallback — `contentshake_optimize.py` calls the API directly via Doppler-loaded key; the MCP tool is the preferred surface but the script is the safety net.

## Auth notes

- Single env var: `SEMRUSH_API_KEY_BLOG_AGENT` (Doppler-loaded). Mirrors `OPENROUTER_API_KEY_BLOG_AGENT`.
- If Semrush gates ContentShake under a separate sub-key, the optimize-content skill picks up `SEMRUSH_API_KEY_CONTENTSHAKE` independently.
- OAuth consent: one-shot on first MCP connection. Subsequent runs reuse the consent. If consent expires, Semrush returns a 401 — the orchestrator surfaces this as a Layer-2 fail and the user re-consents via `claude` CLI.
