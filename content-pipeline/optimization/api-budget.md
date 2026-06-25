# ContentShake AI — monthly API call budget

month: 2026-06
calls: 0

Each `--action optimize` or `--action score` call increments `calls`. Cap is read from
`BLOG_AGENT_CONTENTSHAKE_MONTHLY_CAP` env (default 100). At 80% the skill warns and asks
for confirmation per call; at 100% it refuses further calls and writes a stub report.
The month line auto-rolls over on the first call of a new calendar month (UTC).

## Per-slug log

| date (UTC) | slug | action | iteration | seo_before | seo_after | quality_before | quality_after | budget_after |
|---|---|---|---|---|---|---|---|---|
| 2026-06-15 | how-to-choose-an-nsfw-ai-companion | optimize+score | — | — | — | — | — | 0 (HTTP 400 endpoint down; no slot consumed) |
| 2026-06-15 | openmind-ai-vs-pleasurai | optimize+score | — | — | — | — | — | 0 (HTTP 400 "query type not found"; endpoint still down; no slot consumed) |
| 2026-06-16 | what-do-ai-companion-coins-actually-cost | optimize | — | — | — | — | — | 0 (HTTP 400 "query type not found"; endpoint still down; no slot consumed) |
| 2026-06-16 | ai-companion-pricing-guide-2026 | optimize | — | — | — | — | — | 0 (HTTP 400 "query type not found"; endpoint still down 4th run; no slot consumed) |
| 2026-06-18 | character-ai-no-filter-2026 | optimize | — | — | — | — | — | 0 (HTTP 400 "query type not found"; endpoint still down 5th run; no slot consumed) |
| 2026-06-18 | best-uncensored-ai-chatbot-free | optimize | — | — | — | — | — | 0 (HTTP 400 "query type not found"; endpoint still down 6th run; no slot consumed) |
| 2026-06-19 | spicychat-alternative-2026 | optimize | — | — | — | — | — | 0 (HTTP 400 "query type not found"; endpoint still down 7th run; no slot consumed) |
| 2026-06-22 | joi-ai-alternative-2026 | optimize | — | — | — | — | — | 0 (HTTP 400 "query type not found"; endpoint still down 8th run; no slot consumed) |
| 2026-06-24 | ai-companion-vs-chatgpt-companionship | optimize | — | — | — | — | — | 0 (HTTP 400 "query type not found"; endpoint still down 9th run; no slot consumed) |
