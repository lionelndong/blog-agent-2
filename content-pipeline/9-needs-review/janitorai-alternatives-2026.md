# Needs review — janitorai-alternatives-2026

- Status: **PUBLISHED to Strapi CMS; public-render verification FAILED (auto_publish_check exit 1).**
- Quarantined at: 2026-06-10T20:46:52Z

## What succeeded
- Full pipeline ran clean through every gate (research → preview); all `pipeline_gate.py` exits 0.
- /quality-check verdict PASS, combined score 95/100 (above the >=85 publish bar).
- HARD STOP compliance grep CLEAN on cited draft + article.json + article.md + manifest.json: zero verification-evasion phrases, zero safety-guarantee/absolutism, zero internal-stack terms, zero dropped/unconfirmed stats, zero unresolved [VISUAL:] placeholders.
- 3 SFW visuals generated and uploaded to Strapi media (cover relation resolved).
- Strapi publish: PUT `/api/articles/lmjvwf4t9e74s2ewlu4m7icn` returned **200 OK**, `publishedAt=2026-06-10T20:46:46.927Z`. The article IS live in the CMS — returned by the default (published-only) `/api/articles?filters[slug][$eq]=janitorai-alternatives-2026` query.
  - A prior partial attempt (publishedAt 20:39:45, pre-this-run) had already created the slug, so this run correctly used `--update` (PUT) to avoid a duplicate-slug 400.

## Why quarantined
- `scripts/auto_publish_check.py` builds its probe URL from `STRAPI_BASE_URL` = `https://elegant-cactus-c693703b28.strapiapp.com` and got **404** at `/blog/janitorai-alternatives-2026`.
- Two compounding causes:
  1. **Checker host misconfig:** that strapiapp.com host 404s for EVERY article (verified: `/blog/crushon-ai-review-2026` also 404s there). The real public reader site is `https://pleasur.ai/blog/<slug>`, where existing articles return 200. The checker should use `BLOG_PUBLIC_BASE_URL=https://pleasur.ai`, which is unset here.
  2. **Frontend propagation delay:** even at the correct host `https://pleasur.ai/blog/janitorai-alternatives-2026` the page returns 404 after ~6 min of polling. pleasur.ai is statically generated; new slugs surface only on the next site rebuild. There is no `sync-publish-approvals.yml` workflow in this repo checkout and no on-demand ISR reachable from here, so the rebuild trigger is infra outside this pipeline.

## Action for editor / ops (no content fix needed)
1. Set `BLOG_PUBLIC_BASE_URL=https://pleasur.ai` (or fix the checker default) so it probes the real reader host.
2. Trigger / wait for the pleasur.ai frontend rebuild (the mechanism that surfaces other published Strapi articles), then re-run:
   `BLOG_PUBLIC_BASE_URL=https://pleasur.ai doppler run -- python scripts/auto_publish_check.py janitorai-alternatives-2026`
   Expect HTTP 200 + H1 "Best JanitorAI Alternatives in 2026", then move this file out of 9-needs-review/.
3. The article passed all quality/compliance gates and is live in the CMS. This is a publish-infra verification gap, not a content defect.

## URLs
- CMS record (live): Strapi documentId `lmjvwf4t9e74s2ewlu4m7icn`.
- Expected public reader URL once frontend rebuilds: https://pleasur.ai/blog/janitorai-alternatives-2026
