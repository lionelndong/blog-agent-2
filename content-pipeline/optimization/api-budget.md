# ContentShake AI — monthly API call budget

month: 2026-05
calls: 0

Each `--action optimize` or `--action score` call increments `calls`. Cap is read from
`BLOG_AGENT_CONTENTSHAKE_MONTHLY_CAP` env (default 100). At 80% the skill warns and asks
for confirmation per call; at 100% it refuses further calls and writes a stub report.
The month line auto-rolls over on the first call of a new calendar month (UTC).

## Per-slug log

| date (UTC) | slug | action | iteration | seo_before | seo_after | quality_before | quality_after | budget_after |
|---|---|---|---|---|---|---|---|---|
