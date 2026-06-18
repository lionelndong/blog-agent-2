# optimize-content — skipped (verdict: SKIPPED)

- **Slug:** what-do-ai-companion-coins-actually-cost
- **Keyword:** what do ai companion coins actually cost
- **Date:** 2026-06-16
- **Reason:** Semrush ContentShake AI endpoint returned **HTTP 400 "query type not found"** — the
  endpoint is down, not a quota or key issue. Both `SEMRUSH_API_KEY_CONTENTSHAKE` and
  `SEMRUSH_API_KEY_BLOG_AGENT` are set; the API itself is rejecting the request type.
- **Recurrence:** Same failure logged 2026-06-15 for `how-to-choose-an-nsfw-ai-companion` and
  `openmind-ai-vs-pleasurai`. The ContentShake endpoint has been unavailable since at least then.

## Scores

No scores obtained — the initial `--action optimize` call failed before any analysis ran.
SEO before/after: n/a. Quality (ContentShake) before/after: n/a. Voice drift: n/a (0 iterations,
no edits made). The draft is unchanged.

## Budget

- Budget consumed this run: **0 slots** (HTTP 400 returned before the request was accepted; no
  slot charged — consistent with the two prior failed runs).
- Budget after: **0/100** for 2026-06.

## Action

- Pipeline **continues** without the ContentShake optimization step (Phase B step 8 — soft-fail
  on transient/endpoint error, exit 0).
- Re-run `/optimize-content what-do-ai-companion-coins-actually-cost` once the endpoint is
  restored. The cited draft is preserved at `content-pipeline/6-drafts-cited/` and the iter-0
  baseline snapshot is at `content-pipeline/optimization/what-do-ai-companion-coins-actually-cost-iter-0.md`.
- Raw stderr saved to `content-pipeline/optimization/what-do-ai-companion-coins-actually-cost-errors.log`.
- No compliance rails were touched — zero edits applied; pleasur.ai pricing, both tables, and all
  four [VISUAL] placeholders in the draft remain exactly as drafted.
