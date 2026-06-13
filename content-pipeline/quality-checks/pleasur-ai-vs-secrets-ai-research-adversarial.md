# Research-Adversarial Critique: `pleasur-ai-vs-secrets-ai`

Stage 1b adversarial read of the research dossier before it feeds the outline.
Re-judged 2026-06-13 (one revision pass spent, budget 1/1 — now exhausted).

## HARD stat-rule sweep: CLEAN

Grepped all five inputs for `82 / 6x / recall / retention / no-filter / anything goes / guarantee / volume / AI Overview`. Every hit is a guardrail, not a violation:
- "82% retention" appears **only** as a ban (dossier line 8; context lines 24 & 58). Never asserted as ours.
- "6x recall" appears **only** labeled "their marketing claim" / "Secrets AI's self-described tier feature, not an independently benchmarked figure" (dossier line 100; beat-spec lines 141/147). No fabricated counter-number anywhere.
- Search volume / AIO recorded as `unknown` where the data provider returned nothing (dossier lines 18-19, 24; JSON `pleasur_ai_vs_secrets_ai_head: null`). No guessing.
- No reader-facing vendor naming, no-filter absolutism, or safety guarantee in prose; "no-safety-guarantees" appears as posture instruction only.

No CRITICAL stat violations.

## Findings

**1. [CRITICAL → RESOLVED via revision — Unverifieds not all marked] Time Travel, 100+-Moments trait persistence, and group chat were asserted as facts and over-attributed.**
- `grep` confirms NONE of Time Travel / group chat / Moments System / "100+" appear in `-deep.md`. They trace solely to the companionguide affiliate review + the context brief. Yet the dossier attributed Time Travel to "companionguide / deep research" (over-claimed corroboration), and Time Travel carried no unverified tag at all (line 102) — unlike "100+ Moments (their claim)" which at least had a partial tag.
- The brief explicitly required these be "clearly marked so verify-claims/draft handle them — not silently asserted." They were not.
- **Revision applied (framing only, no new data call):** every one of these now carries an explicit **UNVERIFIED / single-affiliate-source / not corroborated by deep research** tag in section 3 (Partial topics), section 4 (Secrets feature surface), and a guard in BEAT SPEC must-cover item 5 instructing the draft to frame them as "Secrets AI describes…" not as fact, with verify-claims to confirm.

**2. [HIGH — Citations] genfindr 7.6/10 trust anchor has no resolvable URL.** It is the page's one allowed shared comparison metric and trust anchor, but traced only to "per brief" (circular). Not invented — the brand's own live memory + Replika pages already cite genfindr 7.6/10 for Secrets AI — so this is a URL-resolution task, not a fabrication risk. **Revision applied:** line 103 now flags it as a verify-claims MUST-resolve before the trust section ships. Companionguide pricing / "3,600–16,600 Moments" bundles still lack inline URLs (drafting-time resolution).

**3. [HIGH — Data consistency] Three conflicting pleasur.ai price stories.** JSON is internally clean (`secrets_ai_premium_monthly 19.99`, `genfindr 7.6`, `secrets_ai 2400` all match prose). But deep.md reports pleasur.ai at $9.99 / $12.99 / $5.20 / $27.99 / $11.20 across five reviewers; 2-reference reuses a Starter $5.20 / Standard $11.20 / Ultimate $20.00 read; the dossier anchors to authoritative $19/mo. The dossier already flags this openly (line 107) and instructs not to cite reviewer pricing. Acceptable as a flagged drafting-time reconciliation — no silent assertion.

**4. [MEDIUM — Surprising findings] Two of three "surprises" are dressed-up table-stakes.** "Direct head-to-head coverage almost entirely absent" = `actually-surprising`, the real one and the basis of the angle. "Trust/legitimacy is the dominant anxiety" and "Secrets AI has moved multimodal" = `dressed-up-table-stakes`; the genuinely novel sub-finding (scanners mis-label pleasur.ai as "gambling"; pleasures.ai scores 16/100) is buried as support. Not foundation-poisoning.

**5. [MEDIUM — Strongest competitor angle] Captured and beaten, not just acknowledged.** Strongest SERP angle is companionguide.ai's depth + authority (~9,480 words, 9.6/10, 14 images, FAQ + PAA). Dossier names its weakness (single-product affiliate review, no pleasur.ai depth) and beats it with the unoccupied exact-match head-to-head + honest price concession. The exact-match pleasur.ai-vs-Secrets-AI page being unoccupied is the defensible information gain.

**6. [LOW — Brand fit] Strong ownable material, not a generic survey.** 2-reference surfaces real Pleasur.AI hooks: persistent-persona/shared-history module, payment-transparency module, AI Companion Creator (`/create`) and Image Generation (`/generate`) as live counters to the Moments System, the genfindr like-for-like, and the required `/blog/ai-companion-best-memory` internal link. Product pillars map onto the beat-spec axes.

## What works

The beat spec is genuinely competitive, not compliance-theater: a real unoccupied exact-match SERP slot, a defensible 2,000-word target *below* the bloated incumbents, a six-axis table with a no-invented-cell rule, and one true information gain (the only honest head-to-head + crypto-payment-friction axis). Word count, table shape (6 axes), FAQ count (3 brief-mandated), and consensus-topic coverage all check out against the live SERP benchmark.

## Verdict: **PASS**

Initial read was FAIL on Finding 1 (named unverifieds — Time Travel, 100+-Moments persistence, group chat — silently asserted / over-attributed to deep research that does not mention them). One revision pass (budget now 1/1, exhausted) applied framing-only fixes: all three are now tagged UNVERIFIED with single-source provenance and a draft-framing guard; the genfindr trust anchor is flagged for verify-claims URL resolution. Stat rules clean, strongest competitor angle beaten not just acknowledged, beat spec defensible against the SERP. Remaining HIGH/MEDIUM items (genfindr/companionguide URLs, pleasur.ai price reconciliation) are explicitly flagged drafting-time tasks for verify-claims/draft, not silent assertions. Dossier + beat spec are sound to feed the outline.
