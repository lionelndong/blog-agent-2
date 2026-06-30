# Blog Engine STRATEGY — the Ahrefs "Blogging for Business" method, encoded

> **This is the canonical strategy for the Pleasur.AI blog engine.** Every keyword, article, author choice, and routine must trace to a rule here. It is the distilled, operational form of Tim Soulo's full 10-lesson "Blogging for Business" course (full transcript lives in the cockpit: `plans/ahrefs-course-full-transcript.txt`). If anything elsewhere contradicts this file or the repo `CLAUDE.md`, those two win — surface the contradiction, don't improvise.
>
> **The point of this file:** we publish on a *strategy*, never publish-and-pray. Volume without a system is what failed before (≈4 articles/week, one-off keywords, no clusters, 0 paid customers). This is the system.

---

## North star
Blog-attributed **paying subscriptions** — *not traffic*. Traffic is a leading indicator only. The blog is a **customer-acquisition channel**.

## What "winning" looks like (the success spec)
- **Per article:** ranks page 1 for its **parent topic + keyword family**, brings **passive, non-fading** traffic that *compounds*, and has **business value ≥ 2** so it converts.
- **Per cluster:** a ranked **keystone** + a supporting ring, internally linked, expanding as our DR grows.
- **Overall:** % of articles compounding ↑, **customers-per-article** ↑, DR ↑.
- The opposite of winning — and what we refuse to call growth — is the **"spike of hope → flatline of nope"**: a promotion bump that fades to nothing. If our effort doesn't *add up over time*, we're doing it wrong.

---

## THE STRATEGY — 6 decisions (the navigation system)

### 1. Money clusters — never one-off keywords
We do **not** pick keywords individually. We build a few deliberate **money clusters**: business-value PARENT topics where our product is the natural answer (BV 2-3). Each cluster =
- one **keystone article** on the **parent/top keyword** — the highest-volume query the SERP winners actually rank for (one strong page ranks for ~1,000 related keywords, so the parent topic is the unit, not the single keyword);
- a ring of **supporting articles** (sub-topics, long-tail, intent variants);
- **internal links** funneling link-juice to the keystone and to money/product pages.

Build the **winnable members first** (low KD relative to our DR — see #2); expand the cluster's ambition as DR grows. Our starting clusters map to our products (AI companions, NSFW image generation, adult chat/sexting/roleplay, voice & calls, tools/comparisons). The vetted keyword queue is **cluster-organized**, with each row tagged `cluster` + `keystone|supporting`.

**The cluster list is a *living* config, never a fixed list** (`content-pipeline/0-keywords/clusters.md`). Adding a cluster is one edit — no code change — and `cluster-planner` actively **proposes new clusters** when it finds high-business-value demand, or a newly-shipped product, that no cluster covers yet. So as Pleasur.AI grows (e.g. new interactive/real-time features), the blog strategy expands with it and never stays stuck. *(Enforced by `cluster-planner`, Layer 6 of the keyword research pipeline.)*

### 2. Winnability that MOVES with our DR
Difficulty is judged **relative to our own domain**, and our domain changes. Our DR is a **live value** (read from `content-pipeline/0-keywords/cache/brand-dr.json`, refreshed on a cadence together with our "Best by links" referring-domain ceiling) — **never a hardcoded number.** The winnability tiers recompute from live DR, and the *ambition ladders up automatically*:
- low DR → target **KD ≤ ~ (DR + a small margin)** easy wins + small clusters, **cherry-picking the most traffic for the least backlinks**;
- as DR climbs (via linkable assets + links) → unlock higher-KD cluster members + bigger parent topics.

The course's own rule, verbatim in spirit: *don't go after "big" keywords until you've grown a big enough audience and accumulated enough resources to compete.* KD is non-linear (KD 10 ≈ 10 referring domains, KD 70 ≈ 202, KD 90 ≈ 756) and is only a **proxy** — always sanity-check the live top-10 SERP (weak-link count), never trust KD blindly. *(Enforced by `keyword-vet-bid` D-test + `keyword-prioritization` winnability + the weekly DR/RD-ceiling refresh.)*

### 3. Cadence — publish *less*, strategically (the answer to "how often?")
The course **busts the "publish more often" myth.** Ahrefs went from 2-3 articles/**week** (flatline) to 2-3/**month** (growth), and spends **~half its time updating/relaunching** old content, not making new.

- **Cadence is an *output* of the strategy, not a quota.** Publish only what clears every gate (clustered + winnable + unique + BV ≥ 2 + intent-matched). **Never publish to hit a number.**
- **Build-out phase (now):** a gated ~2-4 new articles/week is fine *if* each passes the gates — we're populating the first clusters.
- **Mature phase:** taper new volume; shift toward **update/relaunch** (the Ahrefs steady state).
- **Reserve ~50% of the calendar for AUDIT & RELAUNCH** of existing pieces (see the audit routine).

### 4. Authorship — the right craft for each content type (already built; keep it)
We publish under 3 AI author personas (`examples/authors.md`), each modeled on a great writer's **craft** (never their topic): **Sloane Avery** (Analyst — opinion / data-benchmark / trends), **Theo Hart** (Guide — how-to / comparison / checklist; the fallback), **Mateo Reyes** (Tester — experiment / explainer / hands-on). The pipeline **already selects the persona by the article's content TYPE**, so each type gets the right craft and a consistent, credible voice (this *is* the course's authority-via-consistent-craft).
- **"Who posts this?" = the article's content type**, decided by the existing select-by-type rule (`draft` stamps the byline, `format-for-publish` maps it to the Strapi author) — **not** the cluster. A money cluster naturally spans types → spans authors (a how-to keystone by Theo, a data study by Sloane, an experiment by Mateo).
- **Hard rule — craft, not content (already enforced in `authors.md`):** personas imitate the *moves*, write in OUR voice, and produce **original content only** — never reuse anyone's words, examples, structure, or subject. Every piece still passes the uniqueness gate (#5).
- **Subject-matter authority** comes not from author-cluster-ownership but from being **product-led** (we demonstrate our own tools first-hand) + our **own data** (#5 and the data-study assets).

### 5. Uniqueness — never repeat what's already been said
**Never clone page 1.** Researching everything published and squeezing it into one article just makes a clone, and a clone doesn't deserve more attention than the original. Every article must add **≥ 1 information-gain element**: our **own data**, **first-hand testing**, a **sharper angle**, or a **180° challenge** to consensus (with real arguments). This is a **publish-blocking gate** — nothing ships without a named unique element. It also enforces #4's craft-not-clone. *(Enforced by the uniqueness/info-gain gate in the quality stage.)*

### 6. The spine — compound + business value + intent (always on)
Every article must simultaneously be:
- **Business value ≥ 2** — a reader of this plausibly becomes a paying customer (search *intent*, not search *volume*, is the business signal; the HubSpot "how-to-make-a-GIF" trap — huge traffic, zero product fit — is the anti-example).
- **Intent-matched** — match the SERP's dominant intent *exactly*; the wrong shape never ranks. Check the live SERP before committing.
- **Built to compound** — designed to earn passive, non-fading search traffic, not a promotion spike.

### Two rules that govern promotion (apply once we reach the off-page phase)
- **110/110:** go all-out on **both** the content **and** its promotion, and don't stop promoting until it ranks.
- **Promotion = building backlinks**, not chasing short-term traffic. 94.3% of new pages never reach page 1 in a year — almost always for lack of links. (Off-page is sequenced *after* the blogs prove out and traffic is rising.)

---

## The 16 things we NEVER do (anti-patterns)
1. Optimize for **traffic** instead of **paying customers**.
2. Chase the **spike of hope** / treat **viral** as a strategy.
3. Set a **"publish N/week" quota**.
4. Write about things **no one searches for**.
5. Judge a topic by a **single keyword's volume** (use full traffic potential of the top page).
6. Trust **KD blindly** (review the live top-10 SERP).
7. **Chase keywords above our DR/backlink ceiling.**
8. Write **high-traffic, zero-business-value** content (the GIF trap).
9. **Mismatch searcher intent** to grab a higher-volume keyword.
10. **Keyword-stuff** or over-engineer on-page SEO.
11. **Clone page 1** — unique angle/data/authority, or don't publish.
12. **Abandon old content** or settle for any position below #1.
13. Make promotion about **short-term traffic** instead of backlinks.
14. **Quit promotion early** or refuse to spend on it.
15. **Spam communities / mass-blast outreach / push for links / nag** with follow-ups.
16. Go after **"big" keywords before we have the audience + resources** to compete.

---

## Lesson quick-reference (the whole course, so nothing is dropped)
| # | Lesson | DO | DON'T | Winning = |
|---|--------|----|----|-----------|
| 1 | Compound effect | Blog = customer-acquisition; passive non-fading traffic that adds up | Chase traffic/spikes | Traffic doesn't fade; it compounds |
| 2 | Viral vs SEO | Favor SEO; keystone articles; build audience | Publish-quota; rely on viral | Publish less, grow more |
| 3 | Traffic potential + difficulty | Full traffic potential; parent keyword; RD ceiling; most-traffic/least-backlinks | Single-kw volume; KD-blind; above ceiling | Winnable, real-potential queue |
| 4 | 4 idea sources + business value | Communities/tools/competitors/Content-Explorer; BV 0-3 | The GIF trap | BV ≥ 2, winnable topics |
| 5 | On-page + intent + audit | Match intent; light on-page; squeeze max traffic; update/merge/delete | Wrong keyword; stuffing; abandon old | Intent-matched, wide kw family, fresh catalog |
| 6 | Great content | Quality + ≥5 headlines; unique; authority (journalist) | Clone page 1; "secret" tactics | Readers would email it to a friend |
| 7 | Linkable assets | Linkbait (Emotion/Utility/Numbers/Stories) → DR; internal juice | Expect natural links while small | Data assets pull links; DR climbs |
| 8 | Promotion + big guys | Promotion = backlinks; 110/110; relaunch; pay to promote | Short-term focus; quit early; chase big kw early | Reaches page 1 and stays |
| 9 | Link building | Comments; replicate competitor links; guest (Splinter/Perspective) | Spam; high-DR-only; generic guest | Steady manual RDs |
| 10 | Outreach | A tool; reach linkers/mentioners; them-focused excuse; ≤1 follow-up | Mass-blast; no excuse; pushy; nag | Opened/clicked/replied; links accrue |

---

## How the strategy maps to the pipeline (which step enforces what)
- **#1 clusters** → `cluster-planner` (organizes the queue) + internal-linking in `format-for-publish`.
- **#2 winnability/DR** → `keyword-vet-bid` (D-test) + `keyword-prioritization` (winnability) + weekly DR/RD-ceiling refresh.
- **#3 cadence** → the Publish routine is **gate-driven, not quota-driven**; the Audit & Relaunch routine takes ~half the calendar.
- **#4 authorship** → existing **select-by-content-type** persona rule (`draft` byline → `format-for-publish` Strapi author); no change needed.
- **#5 uniqueness** → blocking info-gain gate in `quality-check`.
- **#6 spine** → BID-B (business value), intent check in `research`/SERP step, compound framing throughout.
- **Off-page (later)** → linkable-asset generator + competitor-mining + outreach, run by the off-page sub-agent once blogs are proven.
