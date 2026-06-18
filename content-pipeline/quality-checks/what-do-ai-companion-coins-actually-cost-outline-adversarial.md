# Outline Adversarial — what-do-ai-companion-coins-actually-cost (Pass 1)

## Verdict: **PASS**

Pass 1 of 2 (revision budget BLOG_AGENT_OUTLINE_REVISION_BUDGET=1).

## Findings

### CRITICAL

- None. Compliance rails respected: every pricing/coin figure matches the canonical block exactly ($12.99/1,500, $27.99/5,000, $49.99/10,000; image 10, voice 10, call 50/min, text unlimited) — BLUF L15/L46, Table 1 L73-75, FAQ L157-159. "Text unlimited" is consistently scoped to text-only and explicitly contrasted against metered media (L48-49, L77, L115); it never bleeds into "unlimited everything." The transparency-of-metering frame is the spine, not absence-of-metering (L21, L99, L103). The phantom "$19/mo" is named as a debunk target (L88, L194), not asserted.

### HIGH

- [Info-gain ledger L193 / H2 #2 / Tables] Information-gain (b) — the "100 tokens vs 1,500 coins" allowance translation specced at research L134 / BEAT SPEC L169 — is never realized as a discrete artifact. The ledger maps it onto Table 1 (pleasur.ai-only) + Table 2 (per-action rates), but neither does the side-by-side "what a competitor's 100-token allowance buys vs a 1,500-coin allowance" translation. As specced, gain (b) is a relabel of gain (a), not a second gain. Add the allowance-translation row/section explicitly or the GEO differentiator thins from three gains to two. Fix before drafting.

### MEDIUM

- [H2 #3 L81-90 vs H2 #4 L95-101] Seam risk: #3's "annual hero is a bait number" (L88) and #4's "opaque metering hides cost" (L99-101) are the same buyer's-eye point applied to two mechanisms. Defensibly distinct (billing cadence vs per-action disclosure) but a careless draft will repeat the "you misread the sticker" beat twice. Hold #3 to billing cadence, #4 to per-action disclosure.
- [H2 #6 L140; H2 #3 L85] BLUF discipline slips. H2 #6 opens "Before any coin math matters, most readers want to know it's safe to pay — so here's the short version…" — throat-clear; the answer (card needed, cancel anytime, discreet billing) lands after the clause. H2 #3 BLUF is also hedged. Both pass; fix at draft.
- [H2 #3 chart L91] Weakest-earning visual. The grouped-bar monthly-vs-annual chart plots six numbers already in Table 1's Monthly/Annual columns — step 5 (MECE) warns against a chart AND table showing the same data. Keep only if the draft makes the annual-savings delta the single takeaway.

### LOW

- [FAQ Q1 L157] "~$12.99/mo entry to ~$49.99/mo top tier" — the tildes imply approximation on exact, published first-party figures the rest of the outline states as hard numbers. Drop the tildes; softening weakens citation-readiness.
- [H2 #2 L63] The worked "mixed-use" example (80 images + 14 call-minutes ≈ 1,500 coins) is prose-only and is the most skimmable arithmetic on the page — strongest candidate for one more visual to hit the 8-target midpoint (currently 6). Not required.
- [Differentiation] H2 #3's "annual hero is a bait number" matches SERP/brand How-to-Choose Criterion 5 rather than beating it. Offset by the angle competitors miss: published per-action arithmetic in H2 #2 + Table 2 (research L133 confirms no page-1 result has this). Net differentiation is genuine.

## What Works

- [Coverage map L180-189 + info-gain ledger L191-194] Every consensus topic from research traces to a section, and all GEO answer-first requirements are present and verifiable: 40-60 word BLUF (L46), 6-Q FAQ (L150), both required tables (L69, L108), stat-every-~150-words density. A structurally complete answer-first spine that will be competitive with the SERP top-5, not merely matching it.

## Recommendation

- Verdict is PASS: advance to stage 4 (/product-mentions). Address HIGH finding #2 (give information-gain (b) a real allowance-translation artifact) during /product-mentions or /draft — it is the difference between three information gains and two.
