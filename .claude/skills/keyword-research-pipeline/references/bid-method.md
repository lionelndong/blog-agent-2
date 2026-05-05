# BID Method — Distilled Reference (Semrush edition)

> Source: Ryan Law's keyword-research method, adapted to Semrush's data surface. Codified here as the operational checklist `/keyword-vet-bid` applies. Read this when the BID gate's behavior is unclear or thresholds need tuning. Recalibration math lives in [`semrush-metric-translation.md`](./semrush-metric-translation.md) — read that first if you're touching any threshold.

The BID method is the second-to-last layer of defense before a keyword reaches the writing pipeline. It's mechanical (heuristics + Semrush metrics, no judgment), cheap, and deterministic. Layer 4 (redteam) handles the judgment-heavy challenges.

## B — Business potential

> "Ask yourself: if I rank number one for this keyword, does it actually help my business achieve its goals?"

The keyword's value isn't its volume — it's the share of that volume that converts to brand outcome (revenue / users / mentions / authority). Two heuristics:

1. **brand_fit ≥ 4** — the keyword's topic must be relevant to the brand's audience, not adjacent or off-topic.
   - 10: addresses a specific stated pain point in `brand-config.md`
   - 7: relevant topic the audience cares about
   - 4: adjacent — audience might find it useful (floor)
   - 0-3: wrong audience entirely → reject

2. **product_fit ≥ 3** — the article should be writable in a way that demonstrates a brand product naturally.
   - 10: impossible to write well without mentioning a brand product
   - 7: product strongly helps demonstrate the topic
   - 3: product can be mentioned in passing (floor)
   - 0-2: no relevant product → reject (Ryan Law: 77% of his Ahrefs blog posts scored 2-3 here; 0s rarely worth writing)

   Exception: if `brand-config.md` lists no live products, set the product_fit weight to zero and skip this gate.

3. **Vanity-rank check**: the "what is espresso" example. Volume + low difficulty + irrelevant intent = traffic that doesn't move the needle. The redteam (Layer 4) is the judgment-based version of this; the mechanical version is brand_fit ≥ 4.

## I — Intent (Semrush classifier primary, SERP-grounded fallback)

> "No matter what you do, if you can't match the intent of the searcher, you will never rank. To check intent, just Google the keyword and look at what's actually ranking."

Semrush returns a per-keyword `intents` array directly from `mcp__semrush__keyword-overview`. Use it as the primary signal — higher quality than re-deriving from URL patterns.

### Primary signal — Semrush `intents` array

| Intent value | Action |
|---|---|
| `informational` (alone or with `commercial`) | **Accept** (we publish blog posts; informational is publish-as-blog territory) |
| `commercial` (alone or with `informational`) | **Accept** (blog posts compete on "best/vs/review" SERPs) |
| `transactional` (dominant) | **Reject** reason `serp_is_transactional` |
| `navigational` (only intent) | **Reject** reason `serp_is_navigational` (single-brand SERP — usually not worth targeting) |
| empty / mixed-without-clear-dominant | fall through to SERP-grounded fallback |

### Fallback signal — SERP-grounded URL/title heuristic

When the `intents` array is empty, equally split, or disagrees with brand fit, classify the SERP top-10 by URL pattern + title heuristics. Same code as the legacy Ahrefs pipeline used; demoted to tie-breaker.

| Class | URL/title signals | Action |
|---|---|---|
| `informational` | `/blog/`, `/learn/`, `/how-to/`; how/what/why/guide titles | **Accept** |
| `commercial-investigation` | `/best/`, `/vs/`, `/review/`; "best X for Y", "X vs Y" | **Accept** |
| `transactional` | `/products/`, `/shop/`, `/pricing/`; e-commerce platforms; price in snippet | **Reject** |
| `tool-led` | `/tools/`, `/calculator/`, `/generator/`; "free X tool" titles | **Route to tool-opportunities** (not blog queue) |
| `hybrid` | mixed top 10 (e.g. 4 blog + 4 product + 2 tool) | **Accept** if blog or commercial-investigation is plurality |

### Tool-led detection (independent gate, not in Semrush `intents`)

`tool-led` is **not** a Semrush intent label. Run the URL/title heuristic separately as a routing gate:
- Tool keywords are AI-Overview-immune (per the keyword-research method)
- But a *blog post* on a tool keyword loses to the *tools* that rank — the brand needs the tool, not a blog about the tool
- Layer 5 routes these to `tool-opportunities.csv` for offline triage

## D — Difficulty (KD% + AS + weak-link check)

> "There's no way a single number can capture the true difficulty of ranking in an algorithm Google has spent billions perfecting. That's why you need to dig deeper into a page's metrics."

KD% alone is a one-number summary; the method's argument is to also check the link graph of the actual top-10 pages. Three signals:

1. **`kd_percent`** — Semrush Keyword Difficulty % (0-100). Captured but not the gate.
2. **`as_top10_median`** — median Authority Score of the top 10 ranking pages. A real proxy for "how authoritative are the pages I'd need to outrank."
3. **`weak_link_count`** — count of top-10 results with `AS < (brand_AS + 4)`. These are pages the brand could realistically displace.

Gate (recalibrated for Semrush — see [`semrush-metric-translation.md`](./semrush-metric-translation.md)):
- **Accept** if `as_top10_median ≤ brand_AS + 12` (within striking distance)
- **Accept** if `weak_link_count ≥ 2` (at least two displaceable pages — a foothold strategy)
- **Reject** otherwise → reason `as_gap_too_wide`

> **Reminder**: the legacy Ahrefs gate was `dr_top10_median ≤ brand_DR + 15`. Don't transplant that threshold — Semrush AS tends ~5-10 points lower for the same site, so we tighten the gap by 3pts to `+12` for equivalent gate strictness.

## Calibration

If the gate's behavior drifts (everything passes or everything fails), the threshold is wrong. Tune in this order:

1. **Everything passes** — gates too lenient. Raise floors:
   - brand_fit ≥ 5 (was 4)
   - product_fit ≥ 4 (was 3)
   - AS-gap to `brand_AS + 8` (was +12)
   - KD% ≤ 60 (was 70)

2. **Nothing passes** — gates too tight OR pool is genuinely poor.
   - Look at the top FAIL reasons:
     - `as_gap_too_wide` dominant → brand AS may be too low for current ambition. Relax to `brand_AS + 20` once and re-run.
     - `serp_is_transactional` dominant → Layer 1's seed/modifier mix is producing commerce-leaning candidates. Adjust modifiers (drop "buy", "shop" — keep "best", "vs", "review").
     - `brand_fit < 4` dominant → seeds are too generic. Tighten Layer 1a's prompt to require seeds tied to specific audience pain points.

Calibration logs go to `content-pipeline/0-keywords/cache/bid-calibration.log` so threshold drift over time is visible.

## What BID can't see

Mechanical filters miss judgment. Examples:

- **SERP intent is hybrid in a tricky way.** Top 10 has 4 blogs and 4 products; the intent classifier (Semrush `intents` or URL fallback) picks "commercial+informational" but user behavior is overwhelmingly transactional. Layer 4's redteam catches this with question (a) — "why might the SERP-intent classification be wrong?"
- **AS-gap is wide but the top pages are stale.** A 5-year-old listicle with high AS is beatable by a fresh, deeper article even if the metrics suggest otherwise. Layer 4's redteam catches this with question (c) — "is the difficulty assessment hiding a weak-link advantage?"
- **Brand_fit is high but the article won't produce revenue.** Vanity-rank trap. Layer 4 question (d) — "is the business potential overstated — does writing this actually produce revenue / users / brand mentions?"

BID is necessary but not sufficient. Layer 4 is where judgment kicks in.

## Reading list

- [`semrush-metric-translation.md`](./semrush-metric-translation.md) — recalibration math (DR→AS, KD→KD%, threshold deltas, "do not transplant" rules)
- [`../../research/references/semrush-mcp-cheatsheet.md`](../../research/references/semrush-mcp-cheatsheet.md) — tool-by-tool playbook for the data this method consumes
- [`semrush-mcp-tool-inventory.md`](./semrush-mcp-tool-inventory.md) — actual tool names exposed by the connected Semrush MCP
- `keyword-prioritization/SKILL.md` — the existing 0-10 scoring framework BID re-uses for B
- `quality-check/SKILL.md` — the adversarial sub-agent pattern Layer 4 mirrors
