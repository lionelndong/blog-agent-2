# Link Integrity Audit — 2026-06-16 (PLE-2580)

**Owner:** EO agent. **Scope:** weekly sweep per PIPELINE.md Operating Week (Tue Link Integrity).
**Data sources:** pleasur.ai/sitemap.xml (52 URLs), Strapi inventory (30 articles), live-page crawl of
all 30 blog pages (2,235 hrefs → 423 unique testable URLs), GSC Search Analytics (page-level,
sc-domain:pleasur.ai, service account), deletion-log.csv, performance-ledger.csv. Observed 2026-06-16.

## Headline counts

| Metric | Count |
|---|---|
| URLs crawled (sitemap) | 52 (all HTTP 200) |
| Blog pages crawled | 30 |
| Unique links tested (internal + outbound) | 423 |
| Broken links found | 9 unique dead targets / 21 occurrences |
| Broken links FIXED in Strapi (live-verified) | 21 occurrences across 7 articles |
| Lost-backlink-equity 404s (ever-published, still ranking) | 62 URLs (6,833 impr/30d) |
| 301 redirects requested (CTO child issue) | 62 |
| Live articles accidentally unpublished + restored this run | 2 (mirror-flip, restored) |

## Part 1 — Sitemap / canonical pages

All **52** sitemap URLs (home, 30 blog articles, /blog, /blog/archive, /explore, /pricing, 13 /legal/*,
auth/app pages) returned **HTTP 200**. Strapi inventory (30 articles, all published) matches the sitemap
exactly — no orphans, no sitemap ghosts. One live page, `/blog/how-to-choose-an-nsfw-ai-companion`, is
**absent from performance-ledger.csv** (tracking gap, not an equity loss — added to ledger backlog).

## Part 2 — Broken links inside live content (FIXED)

Tested 423 unique URLs. Most 403/406 responses are CDN bot-blocks (re-verified live with a browser
UA: ftc.gov, cybernews, time.com, sagepub, jamanetwork, reddit, trustpilot, replika/character help,
nordvpn, businessofapps, hbs.edu, elsevier, medium, androidheadlines, datingadvice, aitipsters all
resolve for real users — **left as-is**). Genuinely-dead targets, all fixed directly in Strapi
(field-preserving round-trip PUT; media/images preserved; live-verified after ISR revalidation):

| # | Article | Dead target | Status | Fix |
|---|---|---|---|---|
| 1 | how-to-make-an-ai-girlfriend | `/blog/build-a-girlfriend-body` (internal, ×2) | 404 (never existed) | **Repointed → /create** (live customization flow) |
| 2 | how-to-make-an-ai-girlfriend | vice.com/.../n7ezkm/replika-ai-erotic-roleplay (×2) | 404 | De-linked (kept attribution text) |
| 3 | ai-girlfriend-experience | wired.com/story/ai-girlfriend-week/ | 404 | De-linked |
| 4 | ai-boyfriend | scribehow Candy_AI_Voice_Calls | 401 | De-linked |
| 5 | how-to-choose-an-nsfw-ai-companion | scribehow Privee_AI_Review (×2) | 401 | De-linked |
| 6 | best-replika-alternative-2026 | scribehow Candy_AI_Free_vs_Premium (×5) | 410 Gone | De-linked |
| 7 | muah-ai-review | scribehow Candy_AI_Pricing_1_Mistake + Ourdream_AI_Pricing | 410 Gone | De-linked |
| 8 | is-candy-ai-safe | scribehow Is_CandyAI_Safe (×6) | 410 Gone | De-linked |

**Fix method:** dead outbound links converted `[anchor](deadurl)` → `anchor` (broken link removed, prose
+ attribution preserved, no fabricated replacement source). The 6 dead scribehow pages were the brand's
own retired how-to pages — de-linking is the correct action; live sibling scribehow links (4×, HTTP 200)
were left intact. The internal `build-a-girlfriend-body` walkthrough was never published, so its links
were repointed to the live `/create` page (preserves internal-link equity to a conversion page).

**Flag (not fixed):** `helixngc7293.itch.io/yandere-ai-girlfriend-simulator` (linked from
yandere-ai-girlfriend-simulator) returns **500** under both curl and browser UA — third-party server
error, may be transient. Re-check next sweep; if persistent, de-link.

**Incident + recovery (documented, PLE-1334/PLEAA-581/PLE-249):** the Strapi PUTs triggered the known
buggy Supabase mirror poller, which flipped **2 of 7** articles (`ai-boyfriend`, `is-candy-ai-safe`) to
`status='draft'` (→ public 404). Detected via post-edit live verification + Supabase query. Restored both
to `status='published'` (mirror content already carried the fixes). All 7 confirmed live HTTP 200 with
dead links gone and images intact. **Root cause is the mirror race, not the edits** — see CTO note below.

## Part 3 — Backlink protection (lost-equity 404s → 301 redirects requested)

A forensic content cleanup on **2026-05-03** (deletion-log.csv) deleted **189** legacy auto-generated
articles. Cross-referencing the deleted slugs against GSC page-level Search Analytics for the **last 30
days (post-deletion)** shows **62 of those URLs are still earning organic impressions while returning
404** — **6,833 impressions/30 days bleeding into dead pages** = lost ranking + backlink equity. Three
others already 308-redirect (ai-chat-porn, ourdream-ai-review-2026, replika-alternative-nsfw); three were
re-created as live quality articles (ai-boyfriend, character-ai-alternative, yandere-ai-girlfriend-simulator).

Highest-equity 404s (full 62-row map in `lost-equity-redirect-map-2026-06-16.csv`):

| impr/30d | dead URL | 301 target |
|---|---|---|
| 1,512 | /blog/character-ai-free-guide-2026 | /blog/character-ai-alternative |
| 833 | /blog/best-nsfw-ai-2026 | /blog/best-uncensored-ai-chatbot-free |
| 415 | /blog/free-ai-chat-bot-guide-2026 | /blog/ai-chatbot-app-guide-2026 |
| 375 | /blog/spicy-ai-chat-review-2026 | /blog/dirty-ai-guide-2026 |
| 286 | /blog/top-ai-chatbots-2026 | /blog/ai-chatbot-app-guide-2026 |
| 254 | /blog/character-ai-alternative-2026 | /blog/character-ai-alternative |
| … | (57 more) | … |

All 62 map to a topically-relevant live article (0 fallbacks to /blog). **301 redirects are frontend
(Next.js) work → filed as a CTO child issue** (out of EO scope per boundaries). Restoring the equity is
time-sensitive: Google de-indexes 404s over weeks, so each week without redirects loses recoverable equity.

## Schema (research-deliverable contract)

- **query/page:** 62 ever-published /blog/* URLs now 404 + 9 dead links in 7 live articles
- **baseline metric:** 6,833 GSC impressions/30d to 404s; 21 dead-link occurrences in live content
- **source:** GSC Search Analytics (service account), live-crawl HTTP tests, Strapi/Supabase inventory, deletion-log.csv
- **observed date:** 2026-06-16
- **gap:** dead inbound 404s leak ranking equity; dead outbound/internal links hurt UX + E-E-A-T + crawl
- **recommendation:** (a) DONE — 21 links fixed in Strapi, live-verified; (b) CTO — implement 62 301s
- **impact tier:** High (6,833 impr/mo recoverable + crawl-budget/E-E-A-T hygiene)
- **owner:** EO (content fixes — done) + CTO (301 redirects — child issue)

## Next actions
1. CTO child issue: implement 62 301 redirects from the map CSV (same-day per PIPELINE.md).
2. Next sweep: re-check itch.io 500; verify the 62 redirects landed; confirm no new mirror flips.
3. Add `how-to-choose-an-nsfw-ai-companion` to performance-ledger.csv (tracking gap).
4. Standing risk: every Strapi content edit can trip the mirror flip — verify live + Supabase status after each.
