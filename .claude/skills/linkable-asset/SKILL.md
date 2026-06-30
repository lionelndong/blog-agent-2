---
name: linkable-asset
description: Phase P4 / Lesson 7. Turn our OWN aggregate PostHog + Stripe data into a brand-safe, link-worthy DATA STUDY (the linkbait dimensions — Emotion / Utility / Numbers / Stories) that earns referring domains and raises Domain Rating, then routes that authority DOWN to our money clusters via internal links. Aggregate-only (NEVER PII), and APPROVAL-GATED: drafts only — the operator approves before anything publishes.
allowed-tools: Read, Write, Edit, Bash
---

# Linkable-Asset Skill — data studies that pull links (Lesson 7)

We are a small, young domain (DR 21). Lesson 7 of the course is blunt: **don't expect natural
links while you're small — you have to build linkable assets.** The single best asset a product
company owns is **its own data**. Almost nobody links to a product page; lots of people link to
*"X% of users do Y"* statistics, charts, and trend reports. So this skill converts our aggregate
PostHog + Stripe numbers into a **DATA STUDY** that journalists, bloggers, and roundup writers cite —
each citation a referring domain — and then **points that new authority at our money clusters** so
the link-juice does real work. See `STRATEGY.md` Lesson 7 + the off-page note (§"How the strategy
maps to the pipeline").

> **What "winning" looks like:** the study earns referring domains we didn't have to ask for, our
> **Domain Rating climbs**, and because the study **internally links down** to keystone + money/product
> pages, that DR lifts the whole cluster's rankings — `max_targetable_kd` rises and harder keywords
> unlock (`STRATEGY.md` §2). A data study that gets links but links to *nothing of ours* is a near-miss:
> the authority leaks instead of compounding. **Links earned + DR up + juice routed to clusters = win.**

This is **NOT** a normal blog article. It skips the keyword-cluster pipeline (it's an *asset*, not a
cluster member) but it MUST still clear the uniqueness gate (`STRATEGY.md` §5 — our data IS the
information-gain element) and carry our brand. It runs only in **Phase P4 / off-page**, after the
core blogs are proven and traffic is rising.

---

## Two HARD RULES (read before anything else)

### RULE 1 — AGGREGATE ONLY. NEVER PII. (non-negotiable)

Every number in the study is a **count, rate, average, or trend over a population** — never a fact
about an identifiable person. This is what makes our data brand-safe and publishable at all: a
mainstream site can cite *"43% of AI-companion users chat daily"* and never touch a real customer.

We are an **adult brand** — leaking even one user's behavior is both a privacy breach and a
reputational landmine. There is no "small exception." If a metric could be tied back to one person,
it does not ship.

**SAFE (aggregate — publish these):**
- `"68% of users who create a companion send a message within the first hour."`
- `"Average companion conversation runs 14 messages."`
- `"NSFW image generations grew 3.2× quarter-over-quarter."`
- `"Voice replies are used by 1 in 4 active companions."`
- `"Weekend sign-ups run 22% higher than weekday."`

**UNSAFE (PII / re-identifiable — NEVER, no matter how 'interesting'):**
- ❌ Any email, username, display name, user id, `distinct_id`, Stripe `cus_…`/`sub_…`/charge id, IP, or device id.
- ❌ Any **single-person** row, quote, transcript snippet, or "one user did X" anecdote.
- ❌ **Small-cohort** stats that re-identify: a bucket of < **100 people** (k-anonymity floor), or
  "100% / 0% of [tiny segment]", or a combination of filters (city + plan + day) that narrows to a
  handful. Suppress or widen the bucket instead.
- ❌ **Free-text** properties (message bodies, prompts, support replies) — even "aggregated," text
  leaks. Only count/bucket structured fields; never surface the words.
- ❌ Geographic precision finer than country, or any timestamp precise enough to single someone out.

**How this skill enforces it:**
- The scaffold (`scripts/data_study_draft.py`) only ever runs **`count()` / `avg()` / ratio**
  HogQL — it never `SELECT`s a person field, and it applies a **minimum-cohort floor** (default
  `MIN_COHORT = 100`): any metric whose denominator is below the floor is **dropped and listed as
  suppressed**, not published.
- Stripe figures used in the study are **aggregate totals/rates already computed** (e.g. "paid
  conversion rate", "MRR growth %") — pulled from the scorecard / finance aggregates, never raw
  customer rows. **Mask anything that smells like an id** (`cus_…`, emails) on sight; if you can't
  aggregate it, you can't use it. (Mirrors the cockpit PII-redaction doctrine.)
- The reviewer (you / the operator) does a final **PII sweep** before approval — see the checklist.

### RULE 2 — APPROVAL-GATED. DRAFT → OPERATOR APPROVES → PUBLISH. NEVER AUTO.

This skill **produces a draft and stops.** It never publishes, never pushes to Strapi, never calls
`/format-for-publish --auto-publish`, never opens outreach. A data study makes a public, quotable
claim about our company under our brand — that is a board-level statement, so a human signs off.

The flow is exactly:

```
1. /linkable-asset            → pulls SAFE aggregates, writes a DRAFT study + a data appendix.
   (scaffold: scripts/data_study_draft.py)
2. OPERATOR REVIEW            → reads the draft, runs the PII sweep, sanity-checks every number
                                against source, confirms the internal-link routing. APPROVES or edits.
3. (only after approval)     → the normal publish path runs as a DRAFT in Strapi for a final human
                                read (/format-for-publish WITHOUT --auto-publish), then the operator
                                clicks Publish. Promotion/outreach is a SEPARATE approved step.
```

If you are running autonomously, you **stop at step 1** and surface the draft path + a one-line
"ready for operator approval" — you do **not** advance to step 2 or 3 yourself.

---

## The linkbait dimensions (Lesson 7 — what makes an asset link-worthy), mapped to Contagious STEPPS

Pick the angle that our data can actually support. A study is strongest when it hits **two or more**.
Lesson 7 names four linkbait dimensions; each maps onto a **Contagious / STEPPS** principle
(`/contagious-why-things-catch-on`, Jonah Berger) — and STEPPS is the engineering manual for *why*
each one earns a share/link. **The data study is our strongest linkbait, so engineer it explicitly
for shareability:**

| Dimension (Lesson 7) | STEPPS principle | What it is | Our data study version |
|---|---|---|---|
| **Numbers** | **Social currency** | A concrete, quotable statistic people repeat — and sharing an exclusive number makes the sharer look in-the-know | "The state of AI companions 2026: N data points from M conversations" — the headline stat IS the link. Our **exclusive** data is pure social currency: only we have it, so citing us signals insider knowledge. |
| **Utility** | **Practical value** | "News you can use" — a benchmark/reference others measure themselves against | "AI companion engagement benchmarks" — what 'normal' usage looks like, so writers cite us as the yardstick. Most brand-safe, most-cited shape. |
| **Emotion** | **Emotion** (high-arousal) | A surprising / counter-intuitive finding — arousal (surprise, awe), not mere positivity, drives sharing | a trend that defies the assumption (e.g. "voice adoption outpaced text faster than anyone expected") — with the real number behind it. Lead with the *gap* between expectation and reality. |
| **Stories** | **Stories** (Trojan Horse) | A narrative the data tells over time, with our brand **integral** to the telling | "How AI-companion behavior shifted across 2026" — a trend line, not a snapshot; build it so the story can't be told without naming Pleasur.AI as the source (valuable virality, not a "fool in the pool"). |

**Engineer the share, don't hope for it (STEPPS moves to apply on top of the dimension):**
- **Inner remarkability + Social currency** — find the one genuinely *surprising* number in the data
  and make it the headline; the more remarkable, the more it gets repeated. An exclusive stat only we
  hold is the strongest social currency a product company has.
- **Practical value** — frame the study as a **benchmark/yardstick** readers and writers can act on
  and measure against; package it scannable (`:::stat` / `:::stat-group`) so the useful bit is
  effortless to lift and cite.
- **Brand-integral story** — if the angle is a trend, make Pleasur.AI inseparable from the finding so
  every citation carries the brand (valuable virality).

**Numbers + Utility (Social currency + Practical value)** is our bread-and-butter: a *benchmark report*
("here's what typical engagement looks like") is the most-cited, most brand-safe shape — it's useful,
it's quotable, and it positions Pleasur.AI as the category's data authority without a single PII risk.

---

## Internal-link routing — the juice MUST flow DOWN to our clusters (Lesson 7)

A linkable asset that earns links but keeps the authority to itself is wasted. The entire point is to
**funnel the new DR down to the pages that make money.** Every study MUST link to:

1. **The relevant cluster keystone(s)** — read `content-pipeline/0-keywords/cluster-map.md` for the
   live keystone slug per cluster. A companions data study links down to the `companions` keystone;
   an image-gen study to the `image-gen` keystone; etc. (clusters: `companions`, `image-gen`,
   `chat-roleplay`, `voice-calls`, `tools-compare` — see `clusters.md`).
2. **The money / product page** the cluster showcases (the product the data is *about* — link the
   feature page so a reader who came for the stat can convert).
3. **2–4 supporting articles** in the same cluster that deepen a finding (descriptive anchors, not
   "click here").

Anchors are **descriptive and natural** (`our AI companion creator`, `NSFW image generation`), never
keyword-stuffed. This is the same internal-linking discipline `format-for-publish` applies — the study
is just an unusually high-authority source page, so its outbound internal links matter more than most.

> Mechanism: external sites link to the **study** (it's safe + quotable) → the study passes that
> authority **internally** to the keystone + money pages → those pages climb. That's how a brand that
> can't get links *to its product* still grows the product's rankings.

---

## Input

`/linkable-asset [cluster-id]` (optional cluster focus; defaults to the highest-data cluster).
Reads:
- `content-pipeline/scorecard/snapshots/<latest>.json` — already-aggregated per-article + conversion
  data (a safe, PII-free source the scorecard produced).
- `content-pipeline/scorecard/latest.md` — aggregate conversion/compounding context.
- `content-pipeline/0-keywords/cluster-map.md` — live keystone slug per cluster (for the routing).
- `content-pipeline/0-keywords/cache/brand-dr.json` — our live DR (the asset's *reason for existing*:
  raise this; frame the study's ambition around it).
- `examples/authors.md` — the byline (a data study is **Sloane Avery**, the Analyst / data-benchmark
  persona — `persona: sloane-avery`).
- live aggregates via the scaffold (PostHog `count()`/`avg()` only; Stripe aggregates only).

## Process

1. **Pick the angle + cluster.** Choose a linkbait dimension (above) our data genuinely supports;
   pick the cluster the study is *about* (so routing has a home). Prefer **Numbers + Utility**
   (a benchmark) unless a real, surprising trend justifies Emotion/Stories.
2. **Pull SAFE aggregates only.** Run the scaffold:
   ```bash
   doppler run -- python scripts/data_study_draft.py [cluster-id]
   ```
   It emits a draft outline + a **data appendix** of aggregate metrics (counts/rates/trends),
   with every below-floor cohort **suppressed and listed**. It does **not** publish anything.
3. **PII sweep (RULE 1).** Read every number. Confirm each is population-level, each cohort ≥ the
   floor, no field, anecdote, or free-text could identify a person. Drop or widen anything borderline.
   If in doubt, cut it — a thinner study that's unimpeachable beats a richer one that leaks.
4. **Write the study around the data.** Lead with the headline stat (the thing people will quote).
   Structure: hook → top-line findings (the quotable numbers, in `:::stat` / `:::stat-group`) →
   trend(s) → what it means → **methodology disclosure** (`:::methodology`: source = our own
   product analytics, sample size, date range, definitions, the aggregation + privacy note "no
   individual user data; all figures are aggregate counts/rates over ≥N users"). Byline Sloane Avery.
5. **Route the juice (Lesson 7).** Add the internal links DOWN to the keystone(s) + money/product
   page + 2–4 supporting articles (descriptive anchors). This is a required section, not optional.
6. **Uniqueness check (`STRATEGY.md` §5).** Our data is the information-gain element — confirm the
   study says something the SERP doesn't already have (it does, by construction: it's *our* numbers).
7. **STOP — hand to the operator (RULE 2).** Save the draft + appendix; surface the path and
   "ready for operator approval." Do **not** publish, push, or promote.

## Output

`content-pipeline/linkable-assets/<study-slug>/`
- `draft.md` — the data-study draft (byline comment + H1 + `:::stat`/`:::methodology` + the
  internal-link routing section). A DRAFT — not a publish package.
- `data-appendix.md` — the aggregate metrics the draft is built on (every figure population-level;
  suppressed cohorts listed) + the methodology/privacy note, for the operator's sanity-check.
- `APPROVAL.md` — the gate record: the PII-sweep checklist (unticked), the routing targets, and the
  explicit "operator must approve before publish" line. Publishing before this is signed is a process
  violation.

## DO / DON'T

**DO**
- Lead with **one quotable number** — the headline stat is the link magnet.
- Aggregate everything; state the **sample size + date range + definitions** openly (credibility = links).
- Frame it as a **benchmark / reference** others measure against (Utility) — the most-cited shape.
- **Link DOWN** to the keystone + money page + supporting ring (route the juice — Lesson 7).
- Keep it **on-brand** (Sloane Avery byline; Pleasur.AI named as the source of the data).
- **Stop at draft** and let the operator approve.

**DON'T**
- ❌ Surface ANY individual user/customer datum, id, email, free-text, or small-cohort (< floor) stat.
- ❌ Auto-publish, push to Strapi live, or kick off outreach — ever. Drafts only; operator gate.
- ❌ Treat it like a keyword article (it's an asset) — but DON'T skip uniqueness or the brand.
- ❌ Earn links to a page that **links to nothing of ours** (authority leak — route it down).
- ❌ Inflate, cherry-pick, or round dishonestly — a debunked stat is a reputational + SEO loss
  (`STRATEGY.md` anti-patterns: don't chase the spike; don't ship what you can't stand behind).
- ❌ Expect this to work before the core blogs are proven (Lesson 7 is sequenced into Phase P4).

## Quality checklist

- [ ] **Every** figure is aggregate (count/rate/avg/trend over a population) — zero individual data.
- [ ] **No PII** anywhere: no email/username/user-id/`distinct_id`/Stripe-id/IP/device, no free-text,
      no single-person anecdote, nothing finer than country / coarse date.
- [ ] **Every cohort ≥ the minimum floor** (default 100); below-floor metrics suppressed + listed, not shipped.
- [ ] Headline carries a **quotable Numbers/Utility stat**; ≥ 2 linkbait dimensions hit.
- [ ] **Engineered for shareability via STEPPS (`/contagious-why-things-catch-on`): the surprising/exclusive number is the headline (Social currency + inner remarkability), the study reads as a citable benchmark/yardstick (Practical value), and — if a trend — the brand is integral to the story. Name which STEPPS principle(s) the study is built to hit.**
- [ ] `:::methodology` discloses source (our product analytics), sample size, date range, definitions,
      and the explicit **aggregate-only / no-PII** note.
- [ ] **Internal-link routing present:** links DOWN to the cluster keystone(s) + money/product page
      + 2–4 supporting articles, descriptive anchors (Lesson 7 juice flow).
- [ ] Byline is **Sloane Avery** (`persona: sloane-avery`) — the data-benchmark persona.
- [ ] Passes uniqueness (`STRATEGY.md` §5) — our data is the information-gain element.
- [ ] Output is a **DRAFT + appendix + APPROVAL.md** — nothing was published, pushed, or promoted.
- [ ] `APPROVAL.md` states the operator must approve before any publish (RULE 2).

## Discipline

- **Aggregate or it doesn't ship.** When a number can't be made population-level without
  re-identifying someone, it's cut. The credibility of the whole asset depends on us never being the
  brand that leaked its users (`STRATEGY.md` — we refuse reputational losses dressed up as growth).
- **The operator is the publish gate, by design.** This skill's job ends at a reviewed-ready draft.
  Auto-publishing a claim about our company is exactly the kind of high-blast-radius action that
  stops for a human (it mirrors the cockpit's guardrail doctrine).
- **An asset that doesn't route juice is a miss.** The reason we build it is DR → clusters. If the
  draft doesn't link down to money/keystone pages, it isn't done (Lesson 7).
- **Phase-gated.** Linkable assets belong to the off-page phase (P4), after the blogs prove out — not
  a thing we do while the core clusters are still being seeded (`STRATEGY.md` Lesson 8 / off-page note).
