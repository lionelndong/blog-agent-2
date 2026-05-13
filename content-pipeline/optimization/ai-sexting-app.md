# optimize-content — ai-sexting-app

## Verdict: SKIPPED

ContentShake API not available — proceeding to visuals without optimization pass.

## Reason

ContentShake API returned `HTTP 400 Bad Request: query type not found` for keyword `ai sexting app` (endpoint `/articles/analyze`, draft 19971 chars). This is a hard API rejection of the query — likely because the adult/NSFW category trips ContentShake's content classifier, mirroring the same failure mode observed on prior NSFW slugs (`ai-boyfriend`, `what-is-an-ai-girlfriend`) which also bailed at iteration 1.

The script exited 1 (not 75 / quota), so the budget counter was not incremented. Per `optimize-content/SKILL.md` Phase B step 8, a non-75 error writes a stub report and exits 0 so the pipeline continues.

## Scores

- SEO before / after: N/A
- Quality before / after: N/A
- Voice drift delta: N/A
- Iterations used: 0 (call 1 failed before any score returned)

## Budget

- Consumed: 0 / 100 (HTTP 400 did not count against quota)
- Remaining: 100

## Artifacts

- `content-pipeline/optimization/ai-sexting-app-iter-0.md` — baseline snapshot of `6-drafts-cited/ai-sexting-app.md`
- `content-pipeline/optimization/ai-sexting-app-raw-iter-1.json` — empty (no JSON returned by failed call)
- `content-pipeline/optimization/ai-sexting-app-errors.log` — full stderr from the failed call

## Next step

Pipeline continues to `/generate-visuals`. Re-running `/optimize-content ai-sexting-app` will hit the same 400 unless ContentShake either (a) widens its acceptable-keyword list or (b) the keyword is rephrased to a non-NSFW variant for the score call. Neither is in scope for this run.
