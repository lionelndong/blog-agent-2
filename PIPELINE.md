# PIPELINE.md — Continuous publishing cadence (self-sustaining)

This file is the **operating cadence** for the blog-engine. It answers two questions so the
engine self-sustains without a per-cycle CEO/board ping (PLE-1344):

1. **How many articles per week, and when?**
2. **How are the next targets chosen?**

It is board-independent and fully autonomous (board ruling 2026-06-09; PLE-1329 Addendum 2). The
deterministic gates in this repo ARE the review. When they pass, the article publishes — same run,
no approval gate, no human in the loop. The board reads the whiteboard + audit log after the fact.

> Companion docs: `CLAUDE.md` (editorial constitution / quality bar), the EO agent's
> `instructions/PIPELINE.md` (publish-gate detail + measurement), `brand-config.md` (products,
> voice, forbidden phrases, internal-stack forbidden-terms list).

---

## 1. Cadence — 5 articles/week (Mon/Tue/Wed/Fri/Sat; board 2026-06-10)

The drumbeat is the Paperclip routine **"SEO Publishing Pipeline"**
(`0adb85a8-a76a-44bc-afd9-865f7a075ce7`), assigned to EO:

- **Schedule trigger:** `0 9 * * 1,2,3,5,6` America/New_York (Mon/Tue/Wed/Fri/Sat 09:00 ET;
  trigger `32e5612c` — the old Mon/Wed/Fri 09:30 trigger `b3e07eed` is disabled).
- Each scheduled fire creates one execution issue assigned to EO. EO advances the engine by
  ~1 article that run via the auto-blog-loop semantics.

**Target throughput: 5 articles/week is the CAP** — the only exception is a board-flagged
product/feature announcement (may ship same-day as a 6th). That is the sustainable rate at the
quality bar (≥2 drafts/article, the floors + reviewer-panel gate, real visuals).

If a scheduled run is missed (downtime), the catch-up policy is `skip_missed` — we do not
double-publish to catch up; we resume the next scheduled slot. Cadence is a floor, not a debt.

**Weekly decay pass:** one run per week should use `--update-mode` (refresh the oldest/most-decayed
published article) instead of writing new — see auto-blog-loop SKILL "Update mode" and the
decay-watch in the EO measurement stage. Falling impressions 2 weeks running → queue for update.

---

## 2. How the next target is chosen

Deterministic selector first, EO judgment override second.

### 2a. Deterministic pick
```
python scripts/auto_keyword_selector.py            # top 1
python scripts/auto_keyword_selector.py --top 5    # inspect the shortlist
```
Reads `content-pipeline/0-keywords/keyword-queue.csv` (the vetted queue from
`/keyword-research-pipeline`, layers 0–5: topic discovery → gap → BID → AIO-cannibalization →
redteam → prioritization). Emits the highest `priority_score` keyword whose slug is **not** already
published (`content-pipeline/8-publish/<slug>/`) and **not** quarantined
(`content-pipeline/9-needs-review/<slug>.md`).

- **Exit 0** → JSON target. Proceed.
- **Exit 2** → queue empty → run `/keyword-research-pipeline` to refill, then re-select. Do not run
  keyword research twice in a row; if still empty, log "no work" and stop the loop.

### 2b. EO override — cannibalization + topical-authority (REQUIRED)
The selector is blind to cannibalization. Before committing a cycle's targets, apply judgment:

- **One canonical page per intent cluster.** The queue routinely surfaces near-duplicates
  (e.g. `ai sexting` / `sexting ai`, both 33.1k vol, same intent). Pick **one**; skip the twin.
- **Diversify across distinct clusters per cycle.** Don't ship three slugs from the same head
  cluster in one week — spread across clusters to build topical breadth (e.g. dirty-talk / sexting /
  boyfriend rather than three girlfriend variants).
- **Differentiate vs. existing live pages.** If a target overlaps a published slug, define a
  distinct search intent (concept/how-to vs. app roundup) and cross-link rather than compete. Check
  the live inventory first (Strapi API; the `auto_keyword_selector` only knows local publish dirs).
- The queue's `redteam_critique_summary` flags "manual adversarial review still required" — this
  override IS that review.

Record the override reasoning in the run issue comment when you deviate from the selector's raw
top-N, so the choice is auditable.

---

## 3. Per-run procedure (what each cadence fire does)

Run `/blog-pipeline "<keyword>"` in autonomous mode for the chosen slug. Env:
```
BLOG_AGENT_AUTONOMOUS=1 UNATTENDED=1 BLOG_AGENT_AUTO_PUBLISH=1 BLOG_AGENT_REVISION_BUDGET=2
```
Stages (each dispatched as a fresh agent; `scripts/pipeline_gate.py` between them):
research → brand-reference → outline → product-mentions → draft → quality-check →
verify-claims → generate-visuals → preview → format-for-publish →
`auto_publish_check.py`. (The standalone adversarial stages AND /optimize-content are retired —
the skeptical read now lives inside /quality-check's 3-reviewer panel.)

### Non-negotiable publish gates
1. **/quality-check PASS** — no score, on purpose. PASS requires BOTH the completeness floors
   (depth ≥ 80% of the SERP median, every consensus topic covered, citations resolved, no internal
   tooling in the prose) AND the 3-reviewer skeptical panel (≥ 2 of 3 keep ours over the live #1;
   none keeps the competitor). Min 2 full drafts: v1 → brutal self-critique → full rewrite v2.
   Still FAIL after the revision budget (2) → **quarantine** to `9-needs-review/`.
2. **Claims verified** — no naked `[link]` placeholders.
3. **Internal-stack scrub (HARD)** — reader-facing prose must never name internal tools/vendors/data
   sources (DataForSEO, Strapi, Doppler, PostHog, OpenRouter, Replicate, Firecrawl, Paperclip,
   Semrush, Ahrefs, …; full list in `brand-config.md`). grep `article.md` before publish; any hit = fix.
4. **Visuals** — **DEFERRED** (its own future project; off by default, `BLOG_AGENT_VISUALS=off`).
   /generate-visuals is a no-op: it leaves the typed `[VISUAL:...]` placeholders in the draft as
   markers, generates no assets, and the visuals gate does **not** block on them. Re-enable with
   `BLOG_AGENT_VISUALS=on` for the screenshots-via-Playwright + matplotlib-table-cards behavior
   (lean by design — Ryan does images by hand; no AI image generation). Preview just carries the
   placeholders through.
5. **Adult-content compliance** — 18+ framing, no "no filter/anything goes" absolutism, no safety
   guarantees, no real-person likenesses. Legal/privacy copy escalates to board, never auto-publish.

A stage failing its gate **twice** → quarantine to `9-needs-review/` and move to the next keyword.
Never publish broken prose; never spin on one article.

### Publish + verify
`format-for-publish --auto-publish` (publishedAt = now) → `auto_publish_check.py {slug}`
(HTTP 200 + correct H1 at `https://pleasur.ai/blog/<slug>`). On mismatch, quarantine.

**Known public-404 root cause + workaround (Strapi→Supabase mirror, PLE-1334).** The public
Next.js blog route does NOT read Strapi directly — it reads Supabase `public.blog_posts` filtered
`status='published'`. An external poller mirrors live Strapi articles into that table on a ~10-min
cadence, but it is buggy (PLE-1334): it leaves the mirrored row at `status='draft'` (so the page
404s) and sometimes does not create the row at all. So a fresh `--auto-publish` reliably 404s for
~10+ min. This is NOT a content failure — do not quarantine for it. Fix it yourself (same safe
data-propagation the CTO used in PLE-1333; data-only, never touch site code/schema):
- Supabase MCP, project `qbzfgpsbcfdtmqpugndm`. If the mirror row exists:
  `update public.blog_posts set status='published', updated_at=now() where document_id='<docId>' and slug='<slug>' and status='draft' returning id,slug,status;`
- If the row is missing, mirror it from Strapi: fetch the live article with media populated
  (`populate[blocks][on][shared.media][populate][file]=true` — plain `populate=*` does NOT populate
  nested media `file` objects in this instance), then upsert id/document_id/slug/title/description/
  `content`=the Strapi `blocks` array verbatim/category/cover_image_url/read_time/published_at/
  `status='published'` (`on conflict (id) do update`). The public route picks it up within seconds.
- The systemic fix is **CTO-owned (PLE-1334, in_review)** — leave evidence there; do not re-fix the
  poller yourself. Until it lands, the manual flip above is a standing step of every cadence run.

Either way **keep producing other articles** — one infra blocker never halts the cadence.

### Log
Append to `content-pipeline/audit/auto-blog-log.csv`
(`slug,keyword,started_at,ended_at,verdict,score,action,error_reason,source,…,strapi_url`).
Report a one-line status per article on the run issue. The whiteboard
(http://100.73.44.58:8770/) renders `content-pipeline/` live for the board.

---

## 4. Escalation boundaries

- **Website-codebase defects** (Next.js routes, webhook/revalidation, sitemap code, CWV) → CTO child
  issue. The pleasur.ai site lives outside this VPS; EO does not edit it.
- **Legal / privacy / brand-risk copy** → board escalation before publish.
- Everything else in the content pipeline (keyword → research → draft → quality → visuals → publish →
  measurement) is EO-owned and autonomous.

## 5. Spend guardrail
Ahrefs API units (400,000/month workspace pool, shared with the REST `AHREFS_API_KEY`), Firecrawl
scrapes, and image-generation calls are metered real money. Stay ≤ **$20/week** combined incremental
spend without board approval. Ahrefs reports cost ~50 units base + per-row, so keep `limit` tight on
every report and check the remaining pool any time with `subscription-info-limits-and-usage` before a
big pull. Log notable spend in the run ledger; report monthly to the CFO (PLE-333).

## 6. Self-improvement cadence (2026-06-12)
- **Example promotion:** when the board grades a published article 9+/10, promote its final
  markdown into `examples/voice/` and rotate out the weakest anchor (see `examples/README.md`).
- **Skill evals:** run `/skill-eval` on one core stage per week (rotate research → outline →
  draft → quality-check), and immediately after any board complaint that names a stage. Proposed
  skill diffs are applied only after operator/EO review.
