# optimize-content — skipped

- Slug: why-does-my-ai-companion-forget
- Keyword: "why does my ai companion forget"
- Date: 2026-06-25
- Verdict: SKIPPED
- Reason: Ahrefs MCP unreachable (no `mcp__ahrefs__*` tools loaded in this environment; ToolSearch for keywords-explorer-related-terms / matching-terms / site-explorer-organic-keywords returned no matching deferred tools). Stage 1 also reported the Ahrefs MCP server not connected, so this is a persistent environment condition, not a transient error.
- Action: launch via `doppler run -- claude` so the Ahrefs MCP loads from `.mcp.json` (requires `AHREFS_MCP_KEY`), then re-run `/optimize-content why-does-my-ai-companion-forget`.
- Term coverage: not measured (no recommended-term pool / competitor-coverage data could be pulled).
- Voice-drift delta: n/a (no edits made; draft untouched).
- Iterations used: 0.
- Pipeline: continues without the term-coverage optimization. The cited draft at `content-pipeline/6-drafts-cited/why-does-my-ai-companion-forget.md` was left unmodified — all hyperlinks, internal links, [VISUAL] placeholders, and [GAIN] marker preserved. `/quality-check` remains the publish gate, so a skipped optimize-content does not ship unreviewed prose.

This is an allowed skip condition per `.claude/skills/optimize-content/SKILL.md` ("Ahrefs MCP unavailable — fail soft, pipeline continues"). Voice integrity beats forced term-stuffing; no prose was degraded to add terms against a missing data layer.
