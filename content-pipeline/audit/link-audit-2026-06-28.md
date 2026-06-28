# Link Integrity Audit — 2026-06-28 (PLE-2919)

**Owner:** EO agent. **Scope:** weekly sweep per PIPELINE.md Operating Week (Link Integrity).
**Data sources:** pleasur.ai/sitemap.xml (62 URLs), Strapi inventory (`/api/articles`, 41 published),
live crawl of all 40 blog pages (258 unique testable links), GSC Search Analytics page-level
(sc-domain:pleasur.ai, service account, 90-day window 2026-03-30→2026-06-27), deletion-log.csv,
performance-ledger.csv, lost-equity-redirect-map-2026-06-16.csv. Observed 2026-06-28.

**Method note (vs prior failed run 1b14aa89):** the previous CMO sweep hung on slow links and
overflowed context. This run used a bounded crawler — 12s hard per-request timeout, 12-worker
pool, browser UA, all detail written to disk — completing in ~10s with zero hangs.

## Headline counts

| Metric | Count |
|---|---|
| Sitemap URLs crawled | 62 (all HTTP 200) |
| Blog pages crawled | 40 |
| Unique links tested (internal + outbound) | 258 (60 internal, 198 outbound) |
| Broken links found (real 4xx/5xx) | 9 unique dead targets / 14 occurrences |
| Broken links FIXED in Strapi (live-verified) | 14 occurrences across 8 articles |
| Ever-published URLs tested (backlink protection) | 250 |
| Working 301 redirects (prior CTO work, confirmed) | 63 |
| Lost-equity 404s still receiving GSC impressions (90d) | 107 (≈84k impr/90d) |
| New 301 redirects requested (on-topic, impr≥50) | 70 (68,336 impr/90d) — CTO child issue |
| Live articles unpublished by mirror-flip this run | 0 (all 8 PUTs stayed `published`) |

## Part 1 — Sitemap / canonical pages

All **62** sitemap URLs (home, 40 blog articles, /blog, /blog/archive, /affiliate, /pricing,
/explore, /subscription, /chat, 13 /legal/*) returned **HTTP 200**. No sitemap ghosts, no orphans.

## Part 2 — Broken links inside live content (FIXED)

Tested 258 unique URLs. 24 returned 403/406/429 — re-confirmed as CDN bot-blocks (resolve for real
browsers: ftc.gov, reddit, time.com, etc.), left as-is. 9 genuinely-dead targets fixed directly in
Strapi via field-preserving round-trip PUT (blocks round-tripped incl. media `file` ids; category/
cover/publishedAt preserved → no content or image loss; `sync-blog-posts` re-triggered; Supabase
mirror status re-verified `published` after each write; live HTTP 200 + dead-link-absence verified):

| # | Article | Dead target | Status | Fix | Occ. |
|---|---|---|---|---|---|
| 1 | ai-companion-vs-chatgpt-companionship | `https://pleasur.ai/privacy` (INTERNAL) | 404 | **Repointed → /legal/privacy-policy** (200) | 1 |
| 2 | what-breaks-immersion-ai-roleplay | `en.wikipedia.org/wiki/Transportation_theory_(psychology)` | 404 (markdown paren-break) | **URL-encoded → `%28psychology%29`** (200) | 1 |
| 3 | best-uncensored-ai-chatbot-free | scribehow Kindroid_AI_Review | 404 | De-linked (anchor kept) | 1 |
| 4 | best-uncensored-ai-chatbot-free | scribehow Dreamgf_AI_Review | 404 | De-linked | 1 |
| 5 | how-to-choose-an-nsfw-ai-companion | scribehow Digital_Girlfriend_AI_Review | 404 | De-linked | 2 |
| 6 | pleasur-ai-vs-dondi-ai | scribehow Dondi_AI_Honest_Review | 404 | De-linked | 4 |
| 7 | best-ai-girlfriend-app | `candy.ai/privacy` | 404 | De-linked | 1 |
| 8 | best-replika-alternative-2026 | scribehow How_Much_Does_Candy_AI_Cost | 404 | De-linked | 2 |
| 9 | joi-ai-alternative-2026 | scribehow Candy_AI_Voice_and_Video | 410 Gone | De-linked | 1 |

**Fix rationale:** the internal `/privacy` and the malformed Wikipedia link had valid live targets,
so they were repointed/encoded (E-E-A-T: preserve the citation). The 6 dead scribehow pages are the
brand's own retired how-to pages (404/410) and `candy.ai/privacy` is a moved competitor page — for
these, de-linking (URL removed, anchor text + attribution preserved, no fabricated replacement) is
the correct action. Method matches the 2026-06-16 sweep.

## Part 3 — Backlink protection (lost equity)

Built the ever-published URL set (250 URLs) from deletion-log.csv + performance-ledger.csv +
lost-equity-redirect-map-2026-06-16.csv, and tested each live:

- **63** redirect correctly to a live page (HTTP 200 after 301) — the 2026-06-16 CTO redirect work
  shipped and is holding.
- **39** still resolve 200 directly.
- **148** return 404/410 with no redirect.

Of those 148, **107 still received GSC impressions in the last 90 days** = live lost-equity. The
top decile is substantial — e.g. `/blog/ai-chat-free-unlimited-2026` (7,517 impr), `/blog/joi-ai-review-2026`
(5,290 impr, 40 clicks), `/blog/nomi-ai-review-2026` (5,007 impr), `/blog/replika-review-2026`
(3,256 impr, 14 clicks). These were deliberately deleted (deletion-log DELETE verdicts) but still
rank and bleed traffic to a 404.

**Decision (keyword-cannibalization + relevance lens):** NOT a blanket redirect. 10 off-topic
AI-tool 404s (ai-video-generator, poe-ai-review, ai-image-generator, gpt-4-guide, etc. — 16,295
impr but ~0 clicks, outside the companion niche) are **left to 404** — redirecting them to companion
content would be low-relevance soft-404s that pass no equity and risk a doorway pattern. The
remaining negligible-equity 404s (impr<50) are also left to 404 naturally.

**Action:** **70 on-topic equity URLs (impr≥50)** mapped to the best-matching live article →
`lost-equity-redirect-map-2026-06-28.csv` (68,336 impr/90d recoverable). Filed as CTO child issue
for 301 implementation in the Next.js frontend redirect config (redirects = website code, out of EO
scope). Same-day per PIPELINE.md backlink-protection clause.

## Deliverable schema

- **query/page:** 250 ever-published URLs + 258 live content links + 62 sitemap URLs.
- **baseline:** 9 dead in-content targets; 107 deleted-but-still-impressed 404s (84k impr/90d); 63 working redirects.
- **source:** live crawl + GSC service-account page-level (90d) + Strapi `/api/articles` + deletion/ledger CSVs.
- **observed:** 2026-06-28.
- **gap:** dead in-content links (UX/E-E-A-T) + un-redirected equity-bearing 404s (lost organic traffic).
- **recommendation:** 14 in-content links fixed live (done); 70 301s requested (CTO).
- **impact:** High (68k impr/90d recoverable via redirects); Medium (in-content link trust).
- **owner:** EO (in-content fixes, done) + CTO (301 redirect deploy).

## Next sweep (2026-07-05)

1. Verify the 70 new 301s shipped and resolve 200.
2. Re-check `helixngc7293.itch.io/yandere-ai-girlfriend-simulator` (was 500, possibly transient).
3. Re-run backlink protection — confirm the 107 lost-equity 404s drop as redirects propagate.
