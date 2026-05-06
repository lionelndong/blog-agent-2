# optimize-content — skipped (API integration mismatch)

- **Slug:** what-is-an-ai-girlfriend
- **Run date (UTC):** 2026-05-05
- **Verdict:** `SKIPPED` — auth chain works; the script's API contract does not.

## What worked end-to-end

| Layer | Status | Evidence |
|---|---|---|
| Doppler CLI auth | OK | `doppler run --` injects env into the Python process |
| Secret presence | OK | Both `SEMRUSH_API_KEY_BLOG_AGENT` and `SEMRUSH_API_KEY_CONTENTSHAKE` present in env |
| Script env injection | OK | Script logged `endpoint=/articles/analyze` and constructed an authenticated request |
| Network reach to Semrush | OK | Real HTTP 400 response from `api.semrush.com` (not 401/403/network error) |

## What did NOT work

- **Endpoint or payload contract mismatch.** Semrush returned `HTTP 400 Bad Request: query type not found` to the script's POST against `https://api.semrush.com/contentshake/v1/articles/analyze`. The error wording matches Semrush's classic Reports API dispatch style (top-level `type` parameter), so the live ContentShake API does not appear to accept the script's `/articles/analyze` REST shape.
- This is the **same failure mode** previously hit on the sibling slug `ai-boyfriend` (see `content-pipeline/optimization/ai-boyfriend.md` for the deeper write-up). Not a per-article issue — a script-integration issue.
- The script's own `build_payload()` docstring already flagged this risk: *"Field names follow the documented Semrush convention; if the live endpoint expects different keys, change them in this one place."*

## Run metadata

- SEO score before / after: n/a (no successful API call)
- Quality score before / after: n/a (no successful API call)
- Voice-drift delta: n/a (no edits applied to draft)
- Iterations used: 0 / 5
- Budget consumed: 0 calls (rejected request did not count against monthly quota)
- Budget remaining: 100 / 100 (`BLOG_AGENT_CONTENTSHAKE_MONTHLY_CAP` default)
- Baseline draft snapshot: `content-pipeline/optimization/what-is-an-ai-girlfriend-iter-0.md` (created)
- Baseline quality: `content-pipeline/optimization/what-is-an-ai-girlfriend-baseline-quality.md` (copied from `quality-checks/what-is-an-ai-girlfriend-metrics.md`)
- Cited draft at `content-pipeline/6-drafts-cited/what-is-an-ai-girlfriend.md`: **unchanged** — next stage (`/generate-visuals`) can proceed against it.

## To unblock optimization for future runs

Same fix-list as the `ai-boyfriend` stub — pick one:

1. Validate `/articles/analyze` against Semrush's published ContentShake API docs and update `DEFAULT_API_BASE` / `build_payload()` keys in `.claude/skills/optimize-content/scripts/contentshake_optimize.py`.
2. Probe with a `type` parameter — "query type not found" specifically suggests the API expects something like `type=audit` in the body or query string.
3. Switch to MCP transport via the Semrush MCP at `https://mcp.semrush.com/v1/mcp` if it exposes a `contentshake-*` tool family.

## Pipeline impact

- Stage failed soft per `SKILL.md` Phase B step 8 (save stderr, write stub, exit 0).
- Next stage (`/generate-visuals`) is unblocked.
- Re-run `/optimize-content what-is-an-ai-girlfriend` after fixing the integration. Existing stage state files let it resume from baseline without re-baselining.

See `content-pipeline/optimization/what-is-an-ai-girlfriend-errors.log` for the raw error context.
