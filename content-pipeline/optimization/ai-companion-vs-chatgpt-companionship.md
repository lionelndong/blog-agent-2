# optimize-content — skipped (ContentShake /analyze outage)

- **Verdict:** SKIPPED (infra soft-skip, not a failure)
- **Slug:** ai-companion-vs-chatgpt-companionship
- **Keyword:** ai companion vs chatgpt companionship
- **Date (UTC):** 2026-06-24

## Reason

ContentShake AI `/articles/analyze` endpoint returned **HTTP 400 "query type not found"** — the same persistent outage affecting every slug since 2026-06-15. This is the 9th consecutive run hitting the identical 400. The Semrush API key IS present (the request reached the server and got a 400, not an auth error); the endpoint itself is down server-side.

Per the optimize-content skill's fail-soft convention and the known-infra note, this is an **expected soft-skip**, not a bug to chase.

## Budget

- API slot consumed: **0** (a 400 from the endpoint does not consume a ContentShake call slot).
- Budget remaining: **100/100** (month 2026-06).

## Scores

- SEO before/after: n/a (endpoint down — no score returned)
- Quality before/after: n/a
- Voice-drift delta: 0 (no content was rewritten; draft untouched)

## Pipeline impact

None. The cited draft at `content-pipeline/6-drafts-cited/ai-companion-vs-chatgpt-companionship.md` is unchanged and passes downstream as-is. No fact-lock surface was touched (pricing, audio-only voice, title, H2/FAQ structure, hook all preserved by virtue of zero edits).

Re-run `/optimize-content ai-companion-vs-chatgpt-companionship` once the ContentShake `/analyze` endpoint is restored.
