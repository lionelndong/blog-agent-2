# optimize-content — skipped (ContentShake /analyze outage)

- **Slug:** joi-ai-alternative-2026
- **Keyword:** joi ai alternative / joi ai alternatives 2026
- **Verdict:** SKIPPED
- **Run date (UTC):** 2026-06-22

## Reason

ContentShake AI `/articles/analyze` returned **HTTP 400 Bad Request: "query type not found"** — the same persistent endpoint outage tracked since 2026-06-15 (this is the 8th consecutive slug to hit it). Expected infra, not a bug to chase (see MEMORY: ContentShake /analyze outage). The cited draft (31,854 chars) was submitted unchanged; the API rejected the request before any scoring occurred.

## Action

- No edits made to `content-pipeline/6-drafts-cited/joi-ai-alternative-2026.md` — draft preserved as-is, including all `[VISUAL]` placeholders and internal links.
- No API slot consumed (the call failed at the endpoint; no scoring returned).
- Budget unchanged: 0/100 for 2026-06.

## Scores

| metric | before | after |
|---|---|---|
| SEO score | n/a (endpoint down) | n/a |
| Quality score | n/a (endpoint down) | n/a |
| Voice drift | n/a (no edits) | 0 pts |

## Pipeline

Continues without the ContentShake optimization step. Re-run `/optimize-content joi-ai-alternative-2026` once the ContentShake `/analyze` endpoint recovers. Note: Semrush API units were also exhausted earlier this run (`ERROR 132`), so even a recovered endpoint may need a units top-up.
