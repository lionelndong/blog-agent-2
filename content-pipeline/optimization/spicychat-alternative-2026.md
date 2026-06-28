# optimize-content — skipped (ContentShake endpoint down)

- **Slug:** spicychat-alternative-2026
- **Keyword:** spicychat alternative
- **Date (UTC):** 2026-06-19
- **Verdict:** SKIPPED (transient API failure — not a missing key, not a budget cap)

## Reason

The ContentShake AI optimize endpoint (`POST .../articles/analyze`) returned
**HTTP 400 "query type not found"** — the identical failure recorded for
`how-to-choose-an-nsfw-ai-companion` and `openmind-ai-vs-pleasurai` (2026-06-15),
`what-do-ai-companion-coins-actually-cost` and `ai-companion-pricing-guide-2026`
(2026-06-16), and `character-ai-no-filter-2026` and `best-uncensored-ai-chatbot-free`
(2026-06-18). This is the known persistent ContentShake `/analyze` outage (see MEMORY:
"ContentShake /analyze outage"). The request never reached a 200, so no analysis,
scores, or recommendations were returned. Per skill + run instructions, this is
EXPECTED infra and is not chased.

See `spicychat-alternative-2026-errors.log` for the raw stderr.

## Preflight results (all green — the block is the endpoint, not config)

- API key: **present** (`SEMRUSH_API_KEY_CONTENTSHAKE` set via Doppler). Missing-key skip path does NOT apply.
- Budget: **0 / 100** for 2026-06 — nowhere near cap. No slot consumed (a 400 before any 200 is not a billable call).
- Baseline draft snapshotted to `spicychat-alternative-2026-iter-0.md`.

## Scores

- SEO score before / after: **n/a** (endpoint returned no scores)
- Quality score before / after: **n/a**
- Voice-drift delta: **0** (no edits were made; the canonical draft is untouched)

## Pipeline impact

None. The cited draft at `content-pipeline/6-drafts-cited/spicychat-alternative-2026.md`
is unchanged — all citations, `[VISUAL:...]` placeholders, and brand-voice prose preserved
exactly as drafted/quality-checked. The pipeline continues to the next stage. Re-run
`/optimize-content spicychat-alternative-2026` once the ContentShake endpoint is restored.
