# Research Adversarial — what-do-ai-companion-coins-actually-cost

Stage: research-adversarial (Phase 3, PLEAA-418). Run date: 2026-06-16.
Reviewer: skeptical research lead (Task sub-agent) armed with the SERP benchmark
and the PLE-2330 / PLE-2347 hard rails from the 0-context file.

## Findings

**1. [HIGH] Candy.ai per-action token estimates cite third-party reviewers, not Candy's live page.** The contrast claim "reviewers *estimate* ~2–4 tokens/image and ~3 tokens/call-min" carries `source: https://skywork.ai/blog/candy-ai-review-2025/`. Candy's subscription price ($13.99/$8.99/$3.99) and 100 tokens/mo trace to `candy.ai/subscriptions` (fetched 2026-06-16) — fine. But the per-action token rates and the $9.99–$299.99 top-up range trace only to reviewers. Defensible *because* the angle is literally "Candy publishes no per-action spec," but the writer must label these reviewer-estimated, never as Candy fact. Load-bearing for the comparison table.

**2. [LOW] Token-pack range citation is thin.** "$9.99 to $299.99 ... `source: skywork.ai candy review + freerdps (2026)`" — "freerdps" appears with no URL anywhere in the dossier. One of two sources for a load-bearing range is an un-URL'd shorthand.

**3. [MEDIUM] Surprising findings — mixed.**
- "Market leader publishes no per-action spec" — **actually-surprising**; genuine information-gain hinge.
- "Phantom $19/mo still circulates in live reviews" — **actually-surprising** as reader service + compliance-safe drift warning.
- "Candy annual drops to $3.99/mo but only 100 tokens" — **dressed-up-table-stakes**; "cheap headline, expensive add-ons" is the oldest freemium critique. True and useful, but not surprising in this niche.

**4. [LOW] Strongest competitor angle captured AND beaten.** Strongest is skywork.ai (#2, `https://skywork.ai/blog/candy-ai-review-2025/`): BLUF + token-economics section + scenario table + FAQ. Dossier names the beat: skywork "can't give the reader certainty" — every number hedged "confirm in-app." The plan to beat it (published exact numbers + math) is real, not just acknowledged.

**5. [PASS] Data consistency — 3 spot-checks pass.** `pleasurai_coins_per_month.standard: 5000` = prose "5,000"; `candy_ai_included_tokens_per_month: 100` = prose "100 tokens/month"; `what_1500_coins_buys.call_minutes_max: 30` = prose "30 call-minutes". One unused JSON key (`starter_effective_cost_per_image_usd_annual: 0.035`) never surfaces in prose — minor, not a problem.

**6. [PASS — compliance] First-party fact trace.** Every Pleasur.AI tier ($12.99/$27.99/$49.99 mo; $5.20/$11.20/$20.00 annual; 1,500/5,000/10,000 coins; image 10 / voice 10 / call 50/min; text unlimited) carries `source: https://pleasur.ai/pricing (fetched 2026-06-16)` — a live fetch FROM THIS RUN, not just brand-config. Matches the hard-rail block EXACTLY. No $19 tier (explicitly debunked). No "unlimited media." PLE-2330 standard met.

**7. [PASS — hard rail] No absence-of-metering framing.** Differentiator stated as "transparency of metering — published allowances + published per-action costs," with explicit guard against "no metering / no tokens / flat rate / unlimited everything." Clean.

**8. [PASS — hard rail] No internal-stack leak in reader-facing prose.** Semrush appears only as a data-source note in internal sections (sanctioned). No Strapi/Doppler/etc. in recommended copy.

**9. [MEDIUM] Brand-ownable material is strong, not generic.** Surfaces a defensible moat: Pleasur's *published* per-action coin math against a SERP that can only estimate. Exactly what the brand can OWN.

## What works

The first-party fact lock is exemplary: live-fetched this run, exactly matches canonical pricing, and surfaces-then-discards the stale "$19/mo" figures with the prior failure mode named explicitly. This is how the trace is supposed to look.

## Verdict: **PASS**
