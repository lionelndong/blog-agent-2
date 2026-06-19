# Research Adversarial — spicychat-alternative-2026 (re-run after revision)

**Stage:** 1b research-adversarial (re-run)
**Slug:** spicychat-alternative-2026
**Date:** 2026-06-19
**Prior pass:** 2 CRITICAL + 1 HIGH (competitor first-party pricing unverified; SpicyChat tiers unsourced; prose/JSON drift + banned $19/unlimited stat). This re-run judges whether those are resolved.

Inputs read: `1-research/spicychat-alternative-2026.md`, `…-deep.md`, `…-data.json`, `0-context/spicychat-alternative-2026.md`, `brand-config.md`.

---

## Prior CRITICALs — resolution check

- **Prior CRITICAL #1 (competitor first-party pricing unverified): RESOLVED.** Candy AI ($13.99/mo, candy.ai/subscriptions, fetched 2026-06-19) and CrushOn ($0/$4.9/$7.9/$25, crushon.ai/pricing, fetched 2026-06-19) are now live first-party. Muah AI and Kindroid prices are honestly tagged `[UNVERIFIED — first-party page unreachable]` because their pricing is login/captcha/Chargebee-gated, with features still first-party-confirmed from their home/docs pages this run. Per calibration, honest [UNVERIFIED] disclosure is acceptable, not a fabrication. The BEAT SPEC price-cell rule (line 184) instructs verify-claims to pin or mark, never invent.
- **Prior CRITICAL #2 (SpicyChat tiers unsourced; banned $19/unlimited): RESOLVED.** SpicyChat tiers ($0/$4.95/$13.95/$23.95) are pinned to one dated named review (`aigirlfriendscout 2026-06-19`) because spicychat.ai/pricing is login-gated — acceptable per calibration. The banned "$19/mo unlimited / no credit meter" and "82% retention" claims are caught and quarantined (deep.md line 169; guardrail line 200); live page wins.
- **Prior HIGH (prose/JSON reconciliation): SUBSTANTIALLY RESOLVED.** Prices reconcile across prose and JSON. One minor table-cell ambiguity remains (CrushOn free $0 vs entry-paid $4.9) — non-blocking, flagged below.

No own-product or competitor price/feature claim is presented as verified without a live first-party source recorded this run. No comparison-table-critical value is fabricated.

---

## Findings

### CRITICAL

**1. "Information gain ≥1 (we hit 3)" is over-counted — only 1 is a genuine reader surprise.** BEAT SPEC line 192. Rated:
- (1) "only side-by-side table featuring Pleasur.ai + the exact 5-app roster" — `dressed-up-table-stakes`. Being on your own table is publication mechanics, not a reader insight.
- (2) "context window vs persistent memory" tied to SpicyChat's 4K/8K/16K tiers — `actually-surprising`. The real wedge; keep it.
- (3) privacy/"is it safe?" section — `dressed-up-table-stakes` as framed. Lines 161/192 promise it is "sourced to pleasur.ai's live privacy policy" but no privacy-policy facts are actually fetched in this dossier — a promise, not material.

*Severity note (NOT a fail-trigger this run):* This is a depth/inflation concern, NOT a sourcing or fabrication defect. It does not present an unverified claim as verified and does not fabricate a table value, so per this run's calibration it does not block. Recorded CRITICAL-by-rubric to force the writer to (a) downgrade the "we hit 3" claim to "1 strong + 1 unique-table" and (b) fetch real privacy-policy facts before drafting gain #3.

### HIGH

**2. Strongest competitor angle identified but under-exploited.** theborderlessmind.com (#5) is correctly named as "the most credible structure on the SERP" with a "How I tested" methodology + dedicated "Memory and context" section (line 95). The BEAT SPEC never directs the writer to produce a comparable first-hand testing methodology, so our page risks reading as "brand ranks itself #1" — the exact self-serving flaw it criticizes in weavai/kalon.

**3. Voice roadmap conflict.** Deep research says Pleasur.ai voice is "in beta, full rollout Q3 2026" (mariavibe.com, third-party); brand-config says voice replies/calls are "coming this week." Guardrails (lines 170, 199) handle this, but the writer must not publish "Q3 2026" as our roadmap.

### MEDIUM

**4. Semrush volume/KD absent.** Lines 8–9 flag `[SEMRUSH UNAVAILABLE — 0 units]`; "Beatability: HIGH" (line 194) is reasoned from SERP shape, not data. Defensible disclosure; flag for re-pull but acceptable to proceed.

**5. CrushOn table-cell ambiguity.** Prose gives entry price as "$4.9/mo (Standard)" while the real headline is the $0 free tier. Reconcile which number lands in the Price cell vs the Free-tier cell so the comparison table isn't internally contradictory.

---

## What works

The PLE-2330 first-party trace is exemplary. Pleasur.ai / Candy / CrushOn prices carry live first-party URLs fetched this run; SpicyChat is pinned to one dated named review because its page is gated; Muah/Kindroid prices are honestly tagged `[UNVERIFIED]` with feature cells still first-party-confirmed; the banned $19/unlimited and 82%-retention pillars are caught and quarantined. No price is fabricated. This is exactly the disclosure discipline the revision was asked to deliver.

---

## Verdict: **PASS**
