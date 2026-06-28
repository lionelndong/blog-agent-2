# optimize-content — SKIPPED

slug: best-uncensored-ai-chatbot-free
date: 2026-06-18
verdict: SKIPPED

## Reason

ContentShake API returned HTTP 400 "query type not found" on the `/articles/analyze` endpoint.
This is a persistent API outage — same error on 6 consecutive runs across different slugs since 2026-06-15
(see `content-pipeline/optimization/api-budget.md` for history).

No API budget slots were consumed (calls remain at 0/100 for 2026-06).

## Baseline quality at time of skip

- Stage: cited draft (post-verify-claims)
- Mechanical score: 100/100
- Final quality check: PASS — 87/100 (judgment 68/100)
- Word count: 5,557 (vs 4,850 target)
- Adversarial verdict: keep this draft over current #1 (rankz.co)

## Action

- Pipeline continues to /generate-visuals without ContentShake optimization.
- Re-run `/optimize-content best-uncensored-ai-chatbot-free` once ContentShake API is restored.
- Recommend: CTO to investigate whether Semrush ContentShake `/articles/analyze` endpoint requires
  account provisioning or a different API key scope. All 6 runs have failed identically since 2026-06-15.

## No score deltas to report

SEO score before: n/a (ContentShake not reached)
SEO score after: n/a
Quality score before: n/a
Quality score after: n/a
Voice drift: 0 (no edits made)
Iterations: 0
Budget consumed: 0 / 100
