# optimize-content — skipped (ContentShake endpoint down)

- **Slug:** ai-companion-pricing-guide-2026
- **Keyword:** ai companion pricing guide 2026
- **Date (UTC):** 2026-06-16
- **Verdict:** SKIPPED (transient API failure — not a missing key, not a budget cap)

## Reason

The ContentShake AI optimize endpoint (`POST https://api.semrush.com/contentshake/v1/articles/analyze`)
returned **HTTP 400 "query type not found"** — the same failure recorded for
`how-to-choose-an-nsfw-ai-companion`, `openmind-ai-vs-pleasurai`, and
`what-do-ai-companion-coins-actually-cost` on 2026-06-15/06-16. The endpoint is
still down (or has moved / been deprecated under this base host); the request never
reached a 200, so no analysis, scores, or recommendations were returned.

See `ai-companion-pricing-guide-2026-errors.log` for the raw stderr.

## Preflight results (all green — the block is the endpoint, not config)

- API key: **present** (`SEMRUSH_API_KEY_CONTENTSHAKE` set via Doppler). Missing-key skip path does NOT apply.
- Budget: **0 / 100** for 2026-06 — nowhere near cap. No slot consumed (a 400 before any 200 is not a billable call).
- Baseline draft snapshotted to `ai-companion-pricing-guide-2026-iter-0.md`.

## Scores

- SEO score before / after: **n/a** (endpoint returned no scores)
- Quality score before / after: **n/a**
- Voice-drift delta: **0** (no edits were made; the canonical draft is untouched)

## Iterations / budget

- Iterations used: **0** (initial optimize call failed before the loop)
- Budget consumed this run: **0** (no successful 200; no slot charged)
- Budget remaining: **100 / 100**

## Recommendations applied / skipped

- None — no recommendation payload was returned to evaluate.

## Pipeline impact

The canonical cited draft at `content-pipeline/6-drafts-cited/ai-companion-pricing-guide-2026.md`
is **unchanged**. The pipeline continues to the next stage (`/verify-claims` /
`/generate-visuals` / `/format-for-publish` as applicable) without the ContentShake
optimization pass. Compliance guardrails were never at risk — no rewrites were proposed.

## Recommended follow-up

The ContentShake `/articles/analyze` (and `/articles/score`) endpoints have now failed
on four consecutive slugs with HTTP 400 "query type not found." This looks like a
provider-side endpoint change, not a transient blip. Recommend the board/engine owner:
1. Re-verify the ContentShake API base/path against current Semrush docs
   (`SEMRUSH_CONTENTSHAKE_API_BASE` / `ENDPOINT_OPTIMIZE` in `contentshake_optimize.py`).
2. Confirm the ContentShake sub-key still has API scope.
3. Until fixed, `/optimize-content` will keep soft-skipping; pipeline output quality is
   unaffected (the stage is additive, not gating).
