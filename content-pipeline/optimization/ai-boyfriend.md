# optimize-content — skipped (API integration mismatch)

- **Slug:** ai-boyfriend
- **Run date (UTC):** 2026-05-05
- **Verdict:** `SKIPPED` — auth chain works; the script's API contract does not.

## What worked end-to-end

| Layer | Status | Evidence |
|---|---|---|
| Doppler CLI auth | OK | `doppler me` returns service-token actor `claude-code-local` (workplace `Leo`, project `pleasurai`, config `dev`) |
| Secret presence | OK | `doppler secrets --only-names` lists `SEMRUSH_API_KEY`, `SEMRUSH_API_KEY_BLOG_AGENT`, `SEMRUSH_API_KEY_CONTENTSHAKE`, `SEMRUSH_MCP_URL` |
| Script env injection | OK | `doppler run -- python contentshake_optimize.py` reaches the Python process with the key in env (script logs `endpoint=/articles/analyze`, indicating it loaded the key and constructed the request) |
| Network reach to Semrush | OK | Real HTTP response from `api.semrush.com` (not 401/403/network error) |

## What did NOT work

- **Endpoint or payload contract mismatch.** Semrush returned `HTTP 400 Bad Request: query type not found` to the script's POST against `https://api.semrush.com/contentshake/v1/articles/analyze`. The error wording matches Semrush's classic Reports API style (which dispatches on a top-level `type` parameter), suggesting the script's `/articles/analyze` REST shape isn't what the live ContentShake API expects.
- The script's own [contentshake_optimize.py:108-113](.claude/skills/optimize-content/scripts/contentshake_optimize.py) docstring on `build_payload()` flagged this risk: *"Field names follow the documented Semrush convention; if the live endpoint expects different keys, change them in this one place — the rest of the script is endpoint-agnostic."* This stage hit that scenario.

## Run metadata

- SEO score before / after: n/a (no successful API call)
- Quality score before / after: n/a
- Voice-drift delta: n/a (no edits applied to draft)
- Iterations used: 0 / 5
- Budget consumed: 0 calls (the rejected request did not count against monthly quota)
- Budget remaining: 100 / 100 (`BLOG_AGENT_CONTENTSHAKE_MONTHLY_CAP` default)
- Baseline snapshot at `content-pipeline/optimization/ai-boyfriend-iter-0.md`: created
- Baseline quality at `content-pipeline/optimization/ai-boyfriend-baseline-quality.md`: created (copied from `quality-checks/ai-boyfriend-metrics.md`)
- The cited draft at `content-pipeline/6-drafts-cited/ai-boyfriend.md` is **unchanged** — the next pipeline stage (`/generate-visuals`) can proceed against it.

## To unblock optimization for future runs

This is a script-integration task, not a stage-8 task. One of the three:

1. **Validate `/articles/analyze` against Semrush's published ContentShake API docs.** Update `DEFAULT_API_BASE` and `build_payload()` keys at [contentshake_optimize.py:55-57, 107-124](.claude/skills/optimize-content/scripts/contentshake_optimize.py). Re-run; if successful, this report file will be overwritten with a real verdict.
2. **Probe with a `type` parameter.** "query type not found" specifically suggests the API expects something like `type=audit` or `type=score` in the body or query string. A 5-minute probe with `curl` against the live API (using the working DOPPLER_TOKEN-loaded key) would confirm which value works.
3. **Switch to MCP transport.** The Semrush MCP at `https://mcp.semrush.com/v1/mcp` may expose `mcp__semrush__contentshake-optimize` / `mcp__semrush__contentshake-score` tools. Per `keyword-research-pipeline/references/semrush-mcp-tool-inventory.md`, this tool's existence was tagged "_verify_" — confirmation requires running an MCP tool-discovery prompt. If they exist, the skill could route through the MCP and bypass the REST contract entirely.

## Pipeline impact

- This stage failed soft per `SKILL.md` Phase B step 8 ("save stderr, exit 0 with stub, don't crash the pipeline").
- The next stage (`/generate-visuals`) is unblocked and can run against the un-optimized cited draft.
- Re-run `/optimize-content ai-boyfriend` after fixing the API integration; stage state files (`-iter-0.md`, `-baseline-quality.md`) are already in place so it can resume from baseline without re-baselining (per `SKILL.md`: "no re-baselining needed unless the user passes `--regen`").

See `content-pipeline/optimization/ai-boyfriend-errors.log` for the raw error context.
