# optimize-content — SKIPPED (ContentShake API down)

- **Verdict:** SKIPPED (transient tool failure — not a key/quota/budget block).
- **Reason:** ContentShake API returned `HTTP 400 Bad Request: query type not found`
  on BOTH endpoints (`/articles/analyze` and `/articles/score`),
  base `https://api.semrush.com/contentshake/v1`. This is a server-side
  endpoint error, not an auth issue — both `SEMRUSH_API_KEY_CONTENTSHAKE`
  and `SEMRUSH_API_KEY_BLOG_AGENT` are present in env.
- **Same failure today:** the identical error was logged for slug
  `how-to-choose-an-nsfw-ai-companion` in `api-budget.md` (2026-06-15) — the
  ContentShake endpoint is currently unavailable under this path.
- **Budget:** 0 slots consumed (the API rejected the request before any work;
  budget remains 0/100 for 2026-06).
- **Scores:** none captured (no successful API response). No baseline drift to
  measure — no edits were applied.
- **Draft:** left UNMODIFIED at
  `content-pipeline/6-drafts-cited/openmind-ai-vs-pleasurai.md`. No guardrail
  surface was touched, so no guardrail violation could be introduced.
- **Pipeline:** continues. Re-run `/optimize-content openmind-ai-vs-pleasurai`
  once the ContentShake endpoint is restored. If it stays down, treat this stage
  as a no-op — `/quality-check` remains the gate that protects publish quality.

See `openmind-ai-vs-pleasurai-errors.log` for the raw error detail.
