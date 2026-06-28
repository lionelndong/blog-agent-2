# PLE-2727 — EO remediation of Semrush content/link blockers (for PLE-2725)

Run date: 2026-06-18 (EO, agent e5c46c5a)
Method note: remediation made via the sanctioned content path (Strapi article edit + live-page verification + outbound-link integrity sweep). No DataForSEO, no paid Semrush API units, no Semrush API report calls, no Semrush MCP report/data endpoints were used. The Semrush dashboard *recheck screenshot* is a browser-recrawl follow-up (see Remaining).

Schema per row: query/page -> baseline -> source -> observed date -> gap -> recommendation -> impact tier -> owner.

---

## Row 1 — "2 pages require content optimization"

### 1a. /blog/pleasur-ai-vs-dondi-ai — EO lane — ASSESSED, no defect
- baseline: 3,078 words, 7 H2 sections, dedicated "Frequently asked questions" H2, at-a-glance comparison + worked pricing example; published 2026-06-18. The blog template auto-emits FAQPage + BlogPosting + BreadcrumbList JSON-LD, so AEO schema is already covered.
- source: Strapi article body (live), pulled 2026-06-18; Semrush AI Search notice (PLE-2725 browser evidence).
- gap: none material. Semrush's "content not optimized" here is a soft AI-Search/ContentShake heuristic, not a structural defect. The article has strong depth and answer-first structure. Only soft lever available: add H3 sub-headers under the comparison/pricing H2s to improve scannability and AI passage extraction (currently 0 H3).
- recommendation: keep as-is for now (it meets our depth + AEO bar). Fold a light H3-subheading pass into the next scheduled refresh of this slug; not worth a same-day republish for a soft notice.
- impact tier: Low. owner: EO.

### 1b. /legal/affiliate-terms — NOT EO lane — EXCEPTION for Leo
- baseline: legal affiliate-terms page flagged "content not optimized".
- gap: it is legal copy; EO cannot alter legal/affiliate terms.
- recommendation: EXCEPTION — retain as legal page; any rewrite is a Leo/legal decision. Recommend no SEO-driven change (legal clarity > keyword optimization on a /legal/ page).
- impact tier: Low (legal utility page, not a ranking target). owner: Leo/legal.

---

## Row 2 — "1 page has only one incoming internal link": /blog/archive
- baseline: /blog/archive is a template/system pagination page, NOT one of our 32 content articles. No article body links to it; its single incoming link comes from the blog-index template.
- source: full Strapi article inventory (32 articles), 2026-06-18 — zero contain a link to /blog/archive.
- gap: a utility archive/pagination surface with one internal link. Forcing article-body links to a bare archive page would be unnatural internal-link noise (cannibalization + crawl-budget lenses argue against it).
- recommendation: do NOT inject archive links into article bodies. Resolve at the template level — EO recommends CTO **noindex /blog/archive** (it is a thin, duplicate-of-index pagination surface; noindexing it removes the notice and saves crawl budget). Alternative: add it to the blog-section footer nav. Either is a Next.js template change.
- impact tier: Low (lowest-severity AI Search notice; utility page). owner: CTO (template) on EO recommendation; or accept.

---

## Row 3 — "1 link to external page returns a 403 HTTP status code"
- baseline/source: I crawled all 32 articles, harvested 217 unique outbound links, and tested every one with a real-browser User-Agent (curl, 2026-06-18). Result: 24 return 403, 2 return 406, 1 returns 000 (dead). Full table below.
- finding: **all 403/406 are bot-walls, not broken links.** Header inspection confirms: journals.sagepub.com returns `cf-mitigated: challenge` / `server: cloudflare`; reddit.com `server: snooserv`; trustpilot.com `server: CloudFront`. These destinations are LIVE for human readers and return 403/406 only to automated crawlers (Semrush's site-audit bot and curl alike). They are authoritative citations: peer-reviewed journals (SAGE, JAMA, Elsevier), Reddit communities, Trustpilot, Time, Newsweek, NordVPN, OpenAI/Character.AI help centers.
- gap vs recommendation: removing these would DAMAGE E-E-A-T and answer-engine citation-readiness (citing authoritative sources is exactly what Google and AI engines reward) for ZERO ranking benefit — Google renders outbound links normally; a crawler-403 on an *outbound* link is a cosmetic Semrush notice (lowest severity), not a ranking signal.
- recommendation: **EXCEPTION — intentionally retain.** These are live, authoritative citations that bot-wall automated crawlers. Document for Leo; no content change.
- impact tier: Low (cosmetic crawler notice). owner: EO (decision) / Leo (acknowledge exception).

### 3b. Bonus link-integrity fix (genuinely dead link — FIXED)
While sweeping, I found one **genuinely dead** outbound link (HTTP 000, DNS does not resolve even at the root domain): `https://aitipsters.com/candy-ai-pricing-2/`, used twice in `/blog/how-to-make-an-ai-girlfriend` as the citation for Candy.ai pricing ($12.99/mo monthly, $5.99/mo annual). This is a separate real Link-Integrity defect (not the Semrush 403 row — that one is a bot-wall).
- FIX: replaced both occurrences with a live (HTTP 200), already-trusted-in-corpus source — `https://aicompanionguides.com/blog/candy-ai-review-2026/` — which states verbatim "Premium ($12.99/mo) Annual ($5.99/mo)" with tokens sold separately, exactly matching our claim. No claim changed; only the dead citation was swapped.
- Verification (2026-06-18): Strapi PUT 200, all 7 blocks + 3 images (file ids 477/478/479) + cover + category preserved; live public page https://pleasur.ai/blog/how-to-make-an-ai-girlfriend returns 200 with `aitipsters`=0 occurrences and the new aicompanionguides link present. End-to-end remediated (Strapi + live site).

---

## Row 4 — "Low text-HTML ratio (57 pages)"
- baseline: the live /blog article HTML is ~260 KB for a ~2,700-word article — i.e. heavy framework scaffolding (Next.js hydration payload, preload tags, inline styles) relative to visible text.
- source: live fetch of https://pleasur.ai/blog/how-to-make-an-ai-girlfriend, 2026-06-18.
- gap: this is a **framework artifact**, not a content-thinness problem. EO-lane blog pages already meet/exceed word-count bars (the pipeline enforces benchmark-relative word counts; flagged blog articles are 2,000-3,000+ words). The ratio lever is HTML payload reduction (code-splitting, deferring non-critical markup) — a site-template / Core Web Vitals concern, not content.
- recommendation: EO-lane content pages need no change (they are word-rich). HTML-overhead reduction is a CTO/CWV optimization, low priority (it is a notice). Genuinely thin product/auth pages in the 57 (root `/`, `/age-verification`, `/login`, `/register`, `/subscription`, `/chat`, `/create`, `/explore`, `/generate/image`, `/legal`) are NOT EO surfaces — adding crawlable copy there is a Leo/founder product decision.
- impact tier: Low. owner: EO content pages = no action; product/auth pages = Leo; HTML-weight = CTO/CWV.

---

## Outbound-link audit table (217 tested, 27 non-OK)

(Full table in the issue comment / regenerable from the sweep. Status legend: 403/406 = bot-wall, live for humans; 000 = dead.)

See PLE-2727 comment for the full 27-row table.

---

## Summary of dispositions
- FIXED (this run): dead aitipsters citation in /blog/how-to-make-an-ai-girlfriend -> live source; verified on Strapi + live site.
- EXCEPTION (Leo to acknowledge): external 403/406 bot-walled authoritative citations (retain — E-E-A-T); /legal/affiliate-terms content (legal copy).
- ASSESSED, no defect: /blog/pleasur-ai-vs-dondi-ai (healthy; optional light H3 pass on next refresh).
- ROUTED to CTO (recommendation): /blog/archive noindex (or footer link); blog-page low text-HTML = CWV/template, low priority.
- Leo/founder: low-word-count + low text-HTML on product/auth/legal surfaces (root, age-verification, login, etc.).

## Remaining
- Semrush dashboard *recheck screenshot*: requires a browser Semrush recrawl (Semrush crawled 64/1,000 pages; recrawl is async). The aitipsters fix is live now and will clear on the next recrawl. The browser Semrush session lives on PLE-2725 (CTO) — recheck folds into that recrawl. EO has no paid-API path to force this and will not use one (per acceptance).
