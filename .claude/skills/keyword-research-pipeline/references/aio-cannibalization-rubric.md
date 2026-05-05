# AIO Cannibalization Scoring Rubric

> Used by `/keyword-vet-aio` (Layer 3) when an adversarial Sonnet sub-agent rates how completely a Google AI Overview answers a query. The rubric is the source of truth for the 0-10 score.
>
> AIO bodies are sourced from **Semrush AI Toolkit's AI Response endpoint** (primary), then Semrush SERP Features (fallback), then `WebFetch` against Google Search (last resort). The scoring rubric below is data-source-agnostic — the reader-perspective question is the same regardless of where the AIO text came from.

## The question the rubric answers

For a given keyword, given the AI Overview body Google currently shows, **how likely is the searcher to still click a regular result?** That likelihood, inverted, is the cannibalization risk.

## The 0-10 scale

### 9-10 — Fully answers, zero click incentive

The AIO contains everything a typical reader of this query would need: the definition + key examples + the implication / recommendation. No major facets are missing. A reader satisfied by the AIO would not click any result.

**Examples:**
- `what is keyword cannibalization` → AIO defines it, gives 2-3 examples, explains the impact. Reader needs nothing more. **Score: 9-10**
- `how to delete instagram account` → AIO walks through the steps. Reader follows them in-app. **Score: 9-10**

**Action:** `aio_verdict=FAIL_CANNIBALIZED`. Don't write a blog post for this query — Google answered it.

### 7-8 — Mostly answers, click only for one specific thing

The AIO covers the main answer but skips a specific dimension a serious reader cares about (depth, examples in a specific context, an opinion, recent news). A reader might click ONE result for that one missing piece, but won't read deep.

**Examples:**
- `how to write a blog post` → AIO gives steps. Misses voice/tone advice. Reader might click for voice tips but skim. **Score: 7-8**
- `what is rss` → AIO defines it. Reader might click to find a specific RSS reader recommendation. **Score: 7-8**

**Action:** Borderline. If `serp_intent=informational` and the missing piece can be supplied by the AIO over time → reject. If the missing piece is *opinionated* (where AIs are weak) → keep as `RISKY`. The redteam (Layer 4) re-checks.

In practice: **score 8 + informational intent = `FAIL_CANNIBALIZED`**.

### 5-6 — Partial answer, multiple clicks needed

The AIO gives a generic answer but skips multiple key dimensions. A reader gets a starting point but needs to read further to actually accomplish their goal.

**Examples:**
- `best espresso machine under $500` → AIO might list 3 machines generically. Reader clicks for specs, photos, opinions, current pricing. **Score: 5-6**
- `python list comprehension examples` → AIO shows one canonical example. Reader needs more variations and edge cases. **Score: 5-6**

**Action:** `aio_verdict=RISKY`. Stays in queue with the flag. The writer differentiates against the AIO (depth + opinion + visual examples + walkthroughs).

### 3-4 — Shallow / wrong, mostly ignorable

The AIO gives a stale, generic, or partially incorrect answer. A reader who notices the issues clicks past it to the regular results.

**Examples:**
- A query about a recent product where the AIO references the old version
- A query where the AIO conflates two related concepts

**Action:** `aio_verdict=PASS`. Classic SERP traffic intact.

### 0-2 — Useless or off-target

The AIO either fails to render meaningfully, gives irrelevant content, or hedges so heavily it provides no value.

**Action:** `aio_verdict=PASS`. The AIO is no threat.

## Decision factors the rubric rewards

When scoring, weight these:

1. **Specific examples present** — if the AIO contains 2+ concrete examples (not generic "for instance"), it's pulling click incentive away from result pages that would otherwise show examples.
2. **Recommendation/advice present** — readers often click *for the recommendation*. If the AIO gives one (even hedged), click incentive drops.
3. **Visual elements** — the AIO sometimes shows images, lists, or tables. These are click-killers because regular results compete on the same dimensions.
4. **Sources cited inline** — a citation-rich AIO suggests Google has high confidence; readers treat it as authoritative and don't click.
5. **Length** — short AIOs (1-2 sentences) rarely satisfy; long AIOs (200+ words) usually do.

## Decision factors the rubric penalizes

When scoring, deduct for these:

1. **Hedging language** — "may", "might", "depends on" — readers click past hedges to find specific answers.
2. **Generic-feeling content** — content that reads like a stitched-together summary without point of view.
3. **Missing the asker's actual question** — many AIOs answer the broad topic, not the specific intent (e.g. asks "best X for Y use case", AIO answers "best X" generally).
4. **Stale information** — AIOs are crawled less frequently than the regular index; if the topic moves fast, the AIO may be 6+ months behind.
5. **No examples** — abstract definitions without concrete instances.

## Special cases

### Tool / generator / calculator queries

These queries route to `tool-opportunities.csv` regardless of AIO. The AIO doesn't kill them because users need a *tool*, not text. Score doesn't matter — the keyword is not a blog post candidate.

Per the keyword-research transcript: "when someone searches for a tool, they need to actually use something. AI can't replace that yet."

### Brand / commercial-investigation queries

`best X for Y`, `X vs Y`, `is X worth it`, `[brand name] review` — AIOs underperform here because users explicitly want comparison or opinion. Score whatever the rubric says, but `aio_verdict=PASS` regardless of score (per `keyword-vet-aio` exemption rules).

### AIO-gap-source queries

Layer 1c added these because competitors are cited in AI search but the brand isn't. Score them, but `aio_verdict=PASS` because the goal is *to be cited*, not to capture click traffic.

### Definitional / "what is X" queries

These are the most cannibalized class. AIOs typically score 9-10. The pipeline should reject most of these unless there's a compelling angle (the brand has a unique definitional take, the query is hyper-specific, etc.). The redteam (Layer 4) re-questions any "what is X" survivor.

## Calibration examples (canonical)

Run these on first calibration; if the rubric's verdicts don't match the expected scores within ±1, the prompt needs strengthening.

| Keyword | Expected score | Expected verdict |
|---|---|---|
| what is keyword cannibalization | 9 | FAIL_CANNIBALIZED |
| how to fix keyword cannibalization | 6-7 | RISKY |
| best keyword research tool 2026 | 4-5 | PASS (commercial-investigation exemption) |
| keyword cannibalization examples | 5 | RISKY |
| semrush keyword cannibalization checker | 2 | PASS (tool-led routing) |
| seo audit checklist | 7 | RISKY |
| how to write a meta description | 8 | FAIL_CANNIBALIZED if informational |
| meta description vs meta title | 5 | RISKY (commercial-investigation, exempted to PASS) |

## When the AIO can't be fetched

Score `null`, verdict `UNKNOWN`. Treated as `RISKY` for queue purposes — the keyword stays in the queue but flagged. The redteam (Layer 4) re-questions it explicitly.

## When the rubric and the agent disagree

The rubric is the source of truth. If the agent argues for a different score, it must do so by citing a specific rubric criterion the rubric missed. Otherwise the rubric verdict stands.

## Updates to this rubric

The AIO landscape changes. Re-read this rubric quarterly and update the canonical calibration examples. The SKILL's `Calibration` section logs drift; if drift is significant, this file is the place to encode the change.
