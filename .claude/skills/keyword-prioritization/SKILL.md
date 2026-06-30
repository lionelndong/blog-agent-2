---
name: keyword-prioritization
description: Layer 5 of the keyword research pipeline. Scores and ranks keywords that survived BID + AIO vetting with a 4-factor model (product_fit-dominant + traffic + brand_fit + winnability-vs-our-DR), times a free-seeker penalty. Routes tool-led keywords aside and drops gap_mode=strong (track-only). Emits keyword-queue.csv (the vetted queue auto-blog-loop reads) and tool-opportunities.csv.
allowed-tools: Read, Write, Edit, Bash
---

# Keyword Prioritization Skill

Take the unscored CSV from `/content-gap-analysis` and add a priority score to each keyword. The score balances traffic opportunity (volume × TP × inverse KD) with brand fit (relevance to audience) and product fit (likelihood of natural product mention).

## Input

`/keyword-prioritization` (no args; reads the latest CSV)

Reads:
- `content-pipeline/0-keywords/keyword-ideas.csv` (input CSV, must exist)
- `brand-config.md` (audience, products — for fit scoring)

## Process

1. **Read the CSV.** Validate it has the expected columns (keyword, volume, kd, traffic_potential, parent_topic, intent).
2. **Read brand-config.md.** Extract product names, top use cases, audience persona, audience pain points.
3. **For each keyword, score it on three dimensions (0–10 each):**

   **Traffic Score** (0–10): based on `traffic_potential` and `kd`
   - High TP + Low KD = 10
   - High TP + High KD = 5
   - Low TP + Low KD = 4
   - Low TP + High KD = 1
   - Use a simple formula: `min(10, log10(traffic_potential + 1) * 2) - (kd / 20)`, clamp to [0, 10]

   **Brand Fit** (0–10): how well does this keyword serve the brand's audience?
   - 10 = directly addresses a known audience pain point
   - 7 = relevant topic the audience cares about, not a stated pain point
   - 4 = adjacent topic the audience might find useful
   - 0 = wrong audience entirely (cut these later)

   **Product Fit** (0–10): how naturally can the brand's products be mentioned?
   - 10 = the article is essentially impossible to write well without mentioning a brand product
   - 7 = product strongly helps demonstrate the topic
   - 4 = product can be mentioned in passing
   - 0 = no relevant product (Ryan Law's "Business Potential 0" — usually not worth writing)

   **Free-seeker check** (the conversion guardrail — see `bid-method.md` B#4): the *conversion signal is `product_fit`*, which is HIGH for genuinely useful informational, product-adjacent posts (the Ahrefs model) — do NOT add a salesy "best/review" boost. Instead flag `free_seeker` when the keyword wants the thing for free ("free", "no-filter", "uncensored", "unfiltered", "unlimited", "without paying/account") — those readers don't pay even when the product fits (the 0-paid leak). Reuse the `free_seeker` / `business_value` columns if BID already set them.

   **Winnability** (0–10): can WE realistically rank this given our **live** domain authority? (Course Lesson 3.4–3.5 — "cherry-pick the most traffic with the LEAST backlinks.") A great article on a keyword we can't rank for is publish-and-pray. Read **`cache/brand-dr.json`** — `domain_rating` (our DR) + **`max_targetable_kd`** (the hardest KD we can realistically rank for at this DR; refreshed by `scripts/refresh_brand_authority.py`, so it **MOVES as DR grows — never hardcode it**). Then, from `kd` + `weak_link_count` (set by `keyword-vet-bid`'s D-test):
   - `kd ≤ domain_rating` → **10** (at/below our authority — trivially winnable).
   - `domain_rating < kd ≤ max_targetable_kd` → **8 → 5** (winnable with effort; scale linearly across the band).
   - `max_targetable_kd < kd ≤ max_targetable_kd + 15` → **3** (a reach — needs links we don't have yet).
   - `kd > max_targetable_kd + 15` → **1** and set a `above_ceiling` flag (don't target yet; revisit when DR rises).
   - **Weak-link override:** if `weak_link_count ≥ 3`, bump up one tier (a beatable SERP with displaceable pages is winnable even at higher KD).
   At DR 21 / `max_targetable_kd` 30 this scores KD-7 → 10, KD-30 → ~5, KD-45 → 3, KD-59 → 1 — rankable wins rise, out-of-reach terms sink. **As DR climbs, `max_targetable_kd` rises and the whole band shifts up automatically** (STRATEGY.md §2) — the strategy is never frozen.

4. **Compute priority_score.** Put **product fit above traffic** (the Ahrefs model) AND **only rank what we can actually rank for** (the backlink-reality of Lesson 3), then penalize free-seekers: **`priority_score = (0.2·traffic + 0.2·brand_fit + 0.4·product_fit + 0.2·winnability) × free_seeker_penalty`**, range 0–10, where `free_seeker_penalty = 0.4` if `free_seeker` is set, else `1.0`. `product_fit` stays the dominant weight (the buying undercurrent); **`winnability` is co-weighted with traffic and brand_fit** so a high-product-fit keyword we *can't rank for yet* (KD far above our DR) loses to an easier, rankable one. No reward for salesy "best/review" phrasing — comparison posts win only on genuine `product_fit`. The result: easy, winnable, product-adjacent wins rise; out-of-reach big terms and free-seekers sink.
5. **Add a `notes` column** with a one-line justification per keyword (why brand_fit / product_fit got that score, named product if applicable).
6. **Sort the CSV by priority_score descending.**
7. **Add a `rank` column** (1, 2, 3, ...) reflecting the new sort order.
8. **Overwrite the CSV** at `content-pipeline/0-keywords/keyword-ideas.csv` — build the full table in memory and `Write` it whole in one shot (never `Edit` individual cells; a format/linter hook can race a partial write — PLE-3063 item 4). The same atomic rule applies to `keyword-queue.csv` and `tool-opportunities.csv` below.
9. **Tell the user:**
   - Top 10 keywords with rank, keyword, priority_score, and notes
   - Suggest running `/blog-pipeline "<top keyword>" --context "..."` for the chosen keyword

## Output

Updated `content-pipeline/0-keywords/keyword-ideas.csv` with:
- `priority_score` column (0–10)
- `brand_fit` column (0–10)
- `product_fit` column (0–10)
- `winnability` column (0–10) + the `kd` / `weak_link_count` it was derived from
- `business_value` (0–3) + `free_seeker` flag
- `notes` column (justification)
- `rank` column (sorted ranking)

## Quality checklist

- [ ] Every keyword has all five new columns populated (incl. `winnability`)
- [ ] `winnability` actually varies with KD vs our live ceiling — terms with `kd > max_targetable_kd` are NOT scoring 8+ (if they are, `brand-dr.json` wasn't read / is stale, or the D-test didn't set `weak_link_count`)
- [ ] Top 5 keywords visibly differ in product_fit (the scoring is doing real work, not flat-rating everything)
- [ ] At least one keyword scored 8+ on product_fit (otherwise either nothing fits the brand, or scoring is too conservative)
- [ ] CSV opens correctly in Excel (notes column with commas is properly quoted)

## Scoring discipline

Don't inflate. If a keyword genuinely doesn't fit the brand, score it low — don't try to find a stretch reason. The goal is to surface the keywords most worth writing, not to rationalize every keyword.

When in doubt:
- Brand fit < 4 → probably skip
- Product fit < 3 → probably skip (Ryan Law's content-engineering rule of thumb: ~77% of high-quality SEO blog posts score 2–3 on Business Potential; 0s rarely worth writing)
- Either dimension = 0 → cut from the active list (mark notes as "skip")

## Autonomous behavior (Layer 5 of /keyword-research-pipeline)

When `BLOG_AGENT_AUTONOMOUS=1` (or invoked from `/keyword-research-pipeline`):

### Filter input pool (only score vetted survivors)

Score ONLY rows where:
- `bid_verdict == PASS`
- `aio_verdict ∈ {PASS, RISKY}` (UNKNOWN is treated as RISKY)

Failed candidates stay in `keyword-ideas.csv` (transparency, future re-vet) but never reach `keyword-queue.csv`.

### Routing on top of the scoring

The `priority_score` is the re-weighted formula (`(0.2 traffic + 0.2 brand_fit + 0.4 product_fit + 0.2 winnability) × free_seeker_penalty` — product fit dominant, winnability co-weighted so we only queue what we can rank for, see step 4) — no other boosts. Column-driven routing rules apply:

1. **`serp_intent=tool-led` → ROUTE TO `tool-opportunities.csv`**, not the writing queue. The writing pipeline never sees these.
2. **`gap_mode=strong` → route to `content-pipeline/0-keywords/cache/strong-positions.csv`** — already won; do NOT include in `keyword-queue.csv` regardless of priority_score. (`gap_mode=missing` is the write pool; it scores on the formula with no modifier.)
3. **`free_seeker` set → keep in the queue but DEPRIORITIZED** (the ×0.4 penalty already sinks them) and tag `top-of-funnel / low-business-value` in `notes`. A free-seeker keyword must never outrank a useful product-adjacent one on raw traffic alone — if it does after scoring, the penalty wasn't applied.

### Tie-breaker on equal priority_score

When two keywords have the same `priority_score`, the row with the higher `traffic_potential` wins.

### Two output files

1. **`content-pipeline/0-keywords/keyword-queue.csv`** — top 50 ranked keywords meeting all gates AND `serp_intent != tool-led`. This is what `auto_keyword_selector.py` reads. Columns include: keyword, slug (computed via `scripts/slugify.py`), priority_score, source, serp_intent, gap_mode, bid_verdict, aio_verdict.

2. **`content-pipeline/0-keywords/tool-opportunities.csv`** — keywords with `serp_intent=tool-led` that survived BID. These are *not* blog candidates; they're tool-build opportunities for offline triage. Columns include: keyword, volume, kd, traffic_potential.

### Auto-slugify keywords

For each row entering `keyword-queue.csv`, compute the slug via `python scripts/slugify.py "<keyword>"` and persist it as the `slug` column. This makes `auto_keyword_selector.py`'s "is this slug already in 8-publish/" check trivial.

### Skip the user-facing suggestion line

In autonomous mode, do not print "Suggest running /blog-pipeline `<top keyword>`". Instead, emit a one-line summary: `queue size N, top keyword "<...>" (priority X.X, source <...>), N tool-opportunities written separately.`

## When the brand has no products

If `brand-config.md` lists no products (it's a personal blog, agency, etc.), product_fit becomes irrelevant. Set product_fit weight to 0 and re-weight: `(0.3 traffic + 0.4 brand_fit + 0.3 winnability) × free_seeker_penalty` — winnability stays in (the DR ceiling applies regardless of products). Note this in the output summary.
