# Research adversarial — janitorai-alternatives-2026

Skeptical read of `content-pipeline/1-research/janitorai-alternatives-2026.md` before it feeds the outline.

## Findings

1. **[HIGH] The deep-research appendix is knowledge-cutoff-limited and the dossier leans on live search instead — good, but say so louder.** The `-deep.md` file self-declares "knowledge runs to October 2024." The dossier correctly notes this and sources the news hook from current search (roborhythms.com, JanitorAI help center). This is handled, but the outline must NOT pull any "2026 development" from the deep file — only the macro/regulatory backdrop is safe.

2. **[CRITICAL — RESOLVED IN DOSSIER] Every attributed numeric stat in Neo's brief failed verification.** The dossier explicitly logs: mariavibe.com 82%/33% (page exists, claim absent → DROP), genfindr 7.6/10 (review exists, number unconfirmable → DROP), scribehow quote (unconfirmable → DROP), topai.tools wait-time figure (403/not stated → SOFTEN to "users report delays"). This is the single biggest risk in the brief and the dossier handles it correctly: net rule "NO unsourced numeric comparative claim about a named competitor." Downstream stages MUST honor this. Flagged CRITICAL because if the draft re-introduces any of these numbers, the article is non-compliant.

3. **[MEDIUM] "Surprising findings" are mostly table-stakes for this niche.** The news hook (verification rollout) is real but already the #1 topic on the SERP — not surprising to the audience. The genuinely non-obvious insight, well-captured: the entire SERP leans on a "no ID required" framing that we are banned from using, which means the open competitive lane is honesty + pricing transparency, not evasion. That IS the differentiating angle and it is surfaced.

4. **[HIGH] Strongest competitor angle is correctly identified.** roborhythms.com ("10 Janitor AI Alternatives That Still Work Without ID") is the strongest SERP piece: current pricing table, category grouping, FAQ. The dossier captures both how to match it (at-a-glance table, FAQ, accurate pricing) and how to beat it (drop the verification-evasion framing it relies on; be the fair/transparent voice). Beat-strategy is present, not just acknowledgement.

5. **[LOW] Data consistency check.** `-data.json` keys spot-checked against prose: `competitor_monthly_price_usd` (CrushOn 5.99, SpicyChat 9.99, Pleasur Starter 12.99, Nomi 16.99, Pleasur Standard 27.99) all match the prose pricing section and pleasur.ai/pricing. `keyword_cluster_volume` (chub 110k, hammer 49.5k, janitor ai reddit 12.1k, xoul 8.1k, janitor ai alternatives 1900) match the long-tail section. No memory-retention numbers in JSON — correct, since those were dropped. Consistent.

6. **[MEDIUM] Brand fit.** Dossier surfaces ownable material: exact Pleasur.ai pricing (Starter/Standard/Ultimate, yearly discounts, 7-day money-back), the "responsible/not predatory 18+" stance, memory+NSFW combo. Honest enough to rank Nomi above us on emotional depth per the brief. Adequate — the brand can own the "transparent + fair" position credibly.

## One thing that works

The attributed-stat verification table is exactly what verify-claims needs: each third-party claim has a fetch result and an explicit DROP/SOFTEN ruling. This prevents the most likely failure mode — publishing an unsourced comparative number about a named competitor.

## Verdict: **PASS**
