# PLE-2726 — EO classification of remaining Semrush content/internal-link rows

Observed date: 2026-06-18 · Source: PLE-2724 browser-only Semrush pass (campaign 29377366), live HTTP checks (browser UA), performance-ledger.csv
Method: classification/judgment only. **No Semrush API units, MCP report/data endpoints, DataForSEO, or paid report calls used** (hard rule honored).

## TL;DR

All four EO-owned rows resolve to **explicit exceptions or normal post-publish monitoring**. None require content remediation that would move organic traffic, and **no EO-driven Semrush rerun is warranted**. From the content/search side, accepting **Site Health 98% as the exception ceiling is the correct call** — the remaining rows are Semrush cosmetic/heuristic warnings (text-to-HTML ratio, on-page keyword-density "optimization", a navigational archive page, an external bot-block), not Google ranking problems. Errors are 0, Crawlability 100%, Markup 100%.

## Row-by-row

### 1. Low text-to-HTML ratio — 57 pages (Warning) → EXCEPTION (accept all)
- **query/page:** mixed surface — `/`, `/affiliate`, `/age-verification`, `/blog`, blog articles + app/auth pages.
- **baseline:** Semrush Warning, 57 pages, 2026-06-18 browser pass (PLE-2724).
- **gap/diagnosis:** Text-to-HTML ratio is **not a Google ranking factor** (Google has stated this repeatedly). The warning fires on JS-rendered sites — pleasur.ai is Next.js, so hydration markup, auto-emitted JSON-LD (FAQPage/BlogPosting/BreadcrumbList), and component scaffolding inflate HTML weight relative to visible text. The blog articles in this set already pass the engine's benchmark-relative quality gate (≥85, competitor-matched word counts) — they are **not thin**. App/auth surfaces (`/chat`, `/create`, `/explore`, `/generate/image`) are intentionally interactive, not text pages.
- **recommendation:** Accept as a known false-positive class. No content remediation. (A DOM/markup trim is a CTO code concern and is not worth a ticket for a non-ranking cosmetic warning.)
- **impact tier:** Low (no ranking impact). **Owner:** EO (accepted exception).

### 2a. Content not optimized — `/blog/pleasur-ai-vs-dondi-ai` (Notice) → EXCEPTION (monitor, timing false-positive)
- **baseline:** indexed=no, clicks/impr 0 (brand-new), ledger row `new`, observed 2026-06-18.
- **gap/diagnosis:** Page was **published 2026-06-18 (PLE-2689) — the same day as the Semrush crawl** — at quality **89/100** (benchmark-relative PASS), clean citations, adult-boundary compliant, 46 internal links, strong title. Semrush's on-page optimizer flags fresh pages before signals settle and scores on keyword-density heuristics the editorial gate intentionally rejects. Live = HTTP 200, indexable (no `noindex`).
- **recommendation:** No action beyond the post-publish monitoring already in the ledger (recheck on indexing). Expect the flag to clear on natural recrawl as the page indexes and accrues internal/external signals.
- **impact tier:** Low. **Owner:** EO (monitor).

### 2b. Content not optimized — `/legal/affiliate-terms` (Notice) → EXCEPTION (not EO content; owner CEO/legal)
- **baseline:** Semrush Notice, live HTTP 200, **indexable** (no `noindex`), observed 2026-06-18.
- **gap/diagnosis:** Legal terms are intentional boilerplate. We do **not** want legal terms competing in organic search; SEO "optimization" of legal copy is out of scope and undesirable.
- **recommendation:** Accept as exception. **Optional low-impact improvement (CTO, only if Leo wants a cleaner crawl surface):** add `noindex` to `/legal/*` utility pages — saves crawl budget and removes them from Semrush content warnings. Not creating a ticket unless requested; it does not move organic traffic.
- **impact tier:** Low. **Owner:** CEO/legal (copy) / CTO (optional noindex). Not EO content work.

### 3. Only one incoming internal link — `/blog/archive` (Notice) → ACCEPT (low-impact)
- **baseline:** Semrush Notice (1 inbound internal link), live HTTP 200, title "All Articles — Archive", links OUT to 55 articles, observed 2026-06-18.
- **gap/diagnosis:** `/blog/archive` is a navigational hub that distributes link equity outward to articles; it receives only 1 inbound link. One inbound link is acceptable for a non-money navigational/pagination page — boosting it does not move organic traffic, and internal-link effort is better spent on orphaned *articles* (e.g. the openmind-ai inbound-link fix, PLE-2642), not the archive index.
- **recommendation:** Accept. Optional cheap fix if a CTO template slot exists: link `/blog/archive` from the `/blog` index nav/footer. Not creating a ticket.
- **impact tier:** Low. **Owner:** EO (accepted exception).

### 4. External page/resource returns 403 — 1 link (Notice) → EXCEPTION pending identification (folded into Link-Integrity routine)
- **baseline:** Semrush Notice (1 external 403). The specific destination URL was **not captured** in the PLE-2724 browser evidence, observed 2026-06-18.
- **gap/diagnosis:** External 403s almost always mean the destination server blocks automated crawlers (Cloudflare/WAF) while serving human visitors normally — i.e. the outbound link works fine for users and is not "broken." Source unavailability note: exact URL absent from browser evidence; no paid Semrush call permitted to pull it.
- **recommendation:** Identify + confirm in this week's **Tuesday Link-Integrity routine** (scan our own published outbound links, re-test with a browser UA — no Semrush units). If a genuine dead link → replace/remove via update pipeline; if bot-block → accept. No CTO ticket; no rerun needed.
- **impact tier:** Low. **Owner:** EO (routine).

## Rerun decision

**No EO-driven Semrush rerun needed.** No EO-owned row has a content change pending that would alter the dashboard. The dondi page will re-evaluate naturally as it indexes; the 403 is handled in routine; the rest are accepted exceptions. EO supports accepting 98% as the documented exception ceiling.

## Implementation tasks created

None. No EO row warrants a CTO/content implementation ticket. Two optional, low-impact CTO improvements are offered above (noindex `/legal/*`; archive nav link) — to be created only on Leo's request.
