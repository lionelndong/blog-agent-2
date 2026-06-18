# Research Adversarial Review: character-ai-no-filter-2026 (revision check)

Stage 1b adversarial pushback on the REVISED research dossier before it feeds `/outline`.
This is a one-revision-budget gate re-run. The prior verdict was FAIL (1 CRITICAL:
unverified competitor pricing in the comparison table; 2 HIGH: own-product live-fetch
wording, mislabeled median word count). Headline check: are those three resolved, and
does any NEW critical exist? Inputs reviewed:
`1-research/character-ai-no-filter-2026.md`, `-deep.md`, `-data.json`,
`0-context/character-ai-no-filter-2026.md`, `brand-config.md`.

## Prior findings — resolved?

**(a) Competitor prices first-party-traced OR flagged "unconfirmed — reviewer-sourced"
and barred from the draft as fact — RESOLVED (Y).**
The "Competitor first-party facts" section traces every price to a live vendor URL
fetched 2026-06-18 and flags the unverifiable ones: Candy AI "**Price: UNCONFIRMED —
reviewer-sourced** (`candy.ai/pricing` returned HTTP 404 this run … do not state a
Candy price as fact)"; Joyland "UNCONFIRMED — reviewer-sourced (`joyland.ai/pricing`
redirects to the homepage)"; Janitor "**Price: UNCONFIRMED**." The BEAT SPEC
"Price-cell rule" bars these from the table as hard numbers. CrushOn
($0/$4.90/$7.90 → `crushon.ai/pricing`) and DreamGen ($7.83/$19.35/$48.30 →
`v2.dreamgen.com/pricing`) are confirmed with URLs. `-data.json` `price_status`
fields agree. The false third-party figures ($19/mo, $15/$30, unlimited/lifetime)
remain quarantined in a DATA-INTEGRITY FLAG.

**(b) Own-product (pleasur.ai) pricing states live-fetched values explicitly —
RESOLVED (Y).**
"First-party fact lock" section: "**Re-fetched live this run** — `source:
https://pleasur.ai/pricing (live WebFetch 2026-06-18)`," with explicit Starter
$12.99 / Standard $27.99 / Ultimate $49.99, coin allowances, and per-action metering
(image 10, voice 10, calls 50/min). Matches `-data.json`.

**(c) Word-count median is now a true top-3 median (2,718), not the #9 page —
RESOLVED (Y).**
SERP benchmark: "True median word count (top-3 qualifying blog articles) **2,718** —
median of TheKnowledgeAcademy 4,105 / DreamGen 2,718 / AISeesoft 2,293 … The middle
value is DreamGen's 2,718 — a genuine three-page median." Arithmetic checks out;
`-data.json` `median_word_count_top3: 2718` matches.

## Findings

**1. [HIGH] The genuinely ownable angle (compliance/privacy of "unrestricted" platforms)
is named but not stocked.**
"Coverage gaps deep research flagged: compliance/age-verification reality …
data-retention/privacy of intimate chats; none of the ranking blogs engage these." The
dossier flags this wedge but supplies zero sourced substrate ("No regulatory/legal
primary sources surfaced"). The writer is told to win on a topic with no research
backing. Not draft-blocking, but it weakens the stated "information gain."

**2. [MEDIUM] Surprising findings are mostly dressed-up table-stakes.**
- "Community frustration with the filter is the dominant signal" → `dressed-up-table-stakes` (it's the keyword's premise).
- "The honest answer … is no" → `dressed-up-table-stakes` in-niche.
- "Market repositioning around memory / emotional continuity / multi-modal media" → `actually-surprising` and the only one mapping to a brand-ownable angle. Only 1 of 3 is a genuine insight.

**3. [MEDIUM] Data consistency: prose ↔ JSON clean.**
Spot-check: `competition: 0.08`, `target_item_count: 6`, `pages_with_comparison_table: 0`
all match prose. `related_keyword_volumes` (10 keys) vs prose long-tails (15) — no
contradiction. No JSON number contradicts prose; no prose number absent from JSON.

**4. [LOW] One keyword line lacks an inline source tag.**
"$0.32 / 0.08 (low paid competition …)" carries no inline Semrush ref, though the
`_meta` source in JSON covers it. Volume 1,600 (`Semrush phrase_this`) and KD 42
(`Semrush phrase_kdi`) are tagged.

**5. [LOW] Own-product freshness assertion is strongest available but unprovable on-page.**
"Live values match the 2026-06-15 canonical block to the dollar" is the desired no-drift
outcome; nothing on-page proves the WebFetch returned tier values vs echoing the block,
but a live WebFetch source IS recorded this run, clearing the PLE-2330 bar. Watch-only,
not critical.

**6. [LOW] Brand-ownable material is present and specific.**
Coin-metering math ("5,000 coins/mo buys ~500 images … or ~100 minutes of calls"),
setup-friction axis (Janitor BYO-API-key vs zero-setup), persistent memory +
in-platform image gen. Pillars 1 (Companion Creator) and 2 (Image Gen) used; voice/calls
correctly held as coming-soon. Not a generic survey.

## What works

The price-trace discipline is now exemplary: every competitor price is either URL-traced
this run or explicitly flagged "UNCONFIRMED — reviewer-sourced" with a draft-level bar,
and the false third-party figures are quarantined in a DATA-INTEGRITY FLAG. This is
exactly the PLE-2330 fix the prior FAIL demanded.

## CRITICAL count: 0

The prior CRITICAL (unverified competitor pricing) is resolved and no NEW critical
exists. Both prior HIGH items (own-product live-fetch wording, mislabeled median) are
resolved. Remaining items are MEDIUM/LOW and do not block drafting. Applying the fair
one-revision bar.

## Verdict: **PASS**
