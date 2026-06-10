# Quality Check — janitorai-alternatives-2026

## Verdict: **PASS**

**Combined score: 95 / 100** (auto-metrics 77/80 + adversarial 18/20). Clears the ≥85 PUBLISH BAR.

No CRITICAL items. No banned verification-evasion phrases. No internal-stack terms. No forbidden phrases. The two remaining auto-metric points recover automatically once /verify-claims resolves the `[link]` markers (must-cite linkage rises from 60% to ~100%).

## Metrics summary

- **Forbidden phrases:** none (20/20).
- **Voice metrics:** all 7 dimensions in baseline range, including em-dash density 5.7/1k (target band) and second-person 28.6/1k (>25 floor). (25/25.)
- **BLUF:** 7/7 section openers pass the heuristic (100%). (20/20.)
- **Claim density:** must-cite linkage 60% at draft stage (3/5) — the unlinked items are bare `[link]` placeholders for /verify-claims to resolve. (12/15 → 15/15 after citation.)
- **Word count:** ~1,150 words; matches the scannable Reddit-native target.

## Compliance check (hard bans)

- No "no ID / no verification / no government ID" phrasing anywhere. PASS.
- No ID-required column in the comparison list. PASS.
- 18+ framing present; no "no filter / anything goes" absolutism; no safety guarantees. PASS.
- Unverifiable stats dropped (mariavibe 82%/33%, genfindr 7.6/10, scribehow quote); memory claim kept qualitative. PASS.
- Visuals are SFW conceptual/data only; no real-person likeness. PASS.
- No internal-stack terms in prose. PASS.

## Adversarial critique (summary)

Full read at `quality-checks/{slug}-adversarial.md`. Five points raised, severity-graded below:

- [MEDIUM, resolves downstream] Memory differentiator asserted, not shown — relies on a `[link]` placeholder. /verify-claims must attach a real, defensible source or keep it strictly qualitative.
- [LOW, editorial bet] Only four apps vs ten-app SERP listicles. Deliberate "fewer, honest" positioning — accepted, not a defect.
- [MEDIUM, resolves downstream] Pricing numbers carry bare `[link]`s; the transparency angle is itself unsourced until /verify-claims attaches pricing-page sources.
- [FIXED] Duplicate "an app asking your age is doing its job" framing — second instance reworded.
- [LOW] At-a-glance bullets are attribute-dense but still scan.

## Punch list (ordered by severity)

1. [HIGH — for /verify-claims] Resolve all `[link]` markers: the verification rollout (roborhythms.com / JanitorAI help center), the regulation dates, each competitor price, Pleasur.ai pricing (pleasur.ai/pricing). The memory-praise `[link]` must resolve to a real source OR the sentence stays qualitative with the link removed — never an unsourced numeric/comparative claim about a named competitor.
2. [LOW] Optional: consider naming one more app (Chub/Joyland) in a single line if breadth concerns surface post-publish. Not blocking.

## Recommendation

Proceed to /verify-claims. The draft is structurally sound, fully compliant with the hard bans, and above the publish bar. Citation work is the only must-do before publish.
