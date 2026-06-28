# Quality Check — pleasur-ai-vs-dondi-ai (draft stage, re-run 2026-06-18)

## Verdict: **PASS**

**Final score: 89/100** (0.6 × mechanical 90 + 0.4 × judgment 88).
No CRITICAL findings remain. No mechanical dimension below 60% of weight. The adversarial read keeps THIS draft over the current #1, and is negative only on the sanctioned vendor-self-comparison axis plus draft-stage citation placeholders (resolved downstream by /verify-claims) — not on a fixable structural axis.

Re-run context: this replaces the prior verdict file, which used the unparseable heading `## VERDICT: BORDERLINE` and halted the gate. This run uses the required `## Verdict: **PASS**` format.

---

## Metrics summary

| Dimension | Score | Weight | Floor (60%) | Status |
|---|---|---|---|---|
| Depth vs benchmark | 15.0 | 25 | 15.0 | ok |
| Consensus coverage | 20.0 | 20 | 12.0 | ok |
| Evidence | 15.0 | 15 | 9.0 | ok |
| AI tells | 25.0 | 25 | 15.0 | ok |
| Structure | 15.0 | 15 | 9.0 | ok |
| **Mechanical total** | **90/100** | | | **PASS** |

- **Word count: 2,303.** Beat-spec nominal band 1,600–2,000; +20% ceiling 2,400 → **within ceiling.** The over-run is concentrated in the pricing-collision section (worked two-scenario example + named break-even), which is the page's primary information-gain payload and the dossier's mandated precision-split. The length is justified by depth, not padding.
- The metrics script's "NO BEAT SPEC found" flag is a false negative — the dossier does carry a binding BEAT SPEC (heading at line 121); the script's grep simply didn't match the heading format. Not a legacy-dossier problem.
- 39 `[link]`/`(URL)` placeholders unresolved — **expected at draft stage**; /verify-claims must resolve AND figure-verify every one (especially the Dondi intel, which the dossier notes is unverified-at-source).

### Claim-discipline gate re-verification (all CLEAR)
- Pleasur.ai **never** framed flat-rate/unlimited/no-meter/no-fees/cheaper-absolute. "cheaper" appears 3×, each explicitly usage-dependent ("neither is cheaper in the abstract"; "the right choice isn't which is cheaper"). CLEAR.
- No two-way video claim for Pleasur.ai — explicitly "voice notes + phone calls + generated clips; no two-way video." CLEAR.
- Uncensored (moderation) vs unlimited-billing claims kept in separate sections; line 38 and line 50 each explicitly forbid the conflation. CLEAR.
- Every Dondi fact attributed in-prose (straight.com / scribehow / indiehackers / Dondi homepage); "unlimited everything" labeled Dondi's own homepage marketing. CLEAR.
- genfindr 7.6/10 used only as an attributed genfindr rating. CLEAR.
- No "no-filter/anything-goes" absolutism for either platform; no safety/privacy guarantee; internal-stack vendor scrub clean. CLEAR.

### Revised pricing-math section (lines 46–60) — targeted re-verify
- **(a) Billing-only:** the section's moderation recap (line 50) is explicitly billing-anchored and is the dossier-required precision split ("question the moderation, take the flat-rate model at face value"). No moderation bleed into the cost math. PASS.
- **(b) Not flat-out "cheaper":** usage-dependent throughout; hands the win to Dondi above the break-even ("you'd be better off… on Dondi's flat rate"; "above it, the heavy-media user should take the flat fee"). PASS.
- **(c) Math internally consistent:** light month 900 coins < 1,500 → stays at $12.99 base; heavy month 150 coins/day crosses 1,500 "inside the second week" (day 10) — both correct.
- **(d) Dondi figures attributed:** scribehow $13–$20 (April 2026), straight.com ~$10 starting — all named in prose (hrefs pending verify-claims).
- **Tic reduction confirmed:** the prior over-repeated "calculable/knowable upfront" crutch is gone — "calculable" 0×, "knowable upfront" 1×; supporting phrasing ("model your spend," "before you subscribe," "published per-action") spread 5× each across a 2,300-word piece, no single phrase weaponized.

---

## Adversarial critique (full file: `…-adversarial.md`)

Side-by-side call: **keeps THIS draft** over the affiliate-listicle #1, because the SERP sells Dondi as "~$10, fully uncensored, #1" and never separates moderation from billing or shows what a metered month actually costs — this draft does both, concedes Dondi's real strengths (including that Dondi is cheaper for heavy-media), and works a named-crossover cost example.

Five weakest points (severity-ranked): (1) all citations are still empty placeholders and the Dondi column is unverified-at-source intel — downstream-fixable but load-bearing; (2) no vendor-bias disclosure under repeated "fair/honest" framing; (3) thin on first-hand Pleasur.ai substance beyond pricing (companion/image/UX); (4) genfindr 7.6/10 leaned on repeatedly; (5) the break-even's "~150 actions ≈ 1,500 coins" silently assumes images+voice at 10 coins and excludes 50-coin/min calls — and calls are Standard+, so they can't apply to the Starter scenario the example is built on. What genuinely works: the dollar-for-dollar usage-dependent framing with a named crossover that hands the win to Dondi above the line — keep verbatim.

None of the adversarial negatives sit on a fixable structural axis that would flip the keep decision; the empty-citation and bias-disclosure items are downstream/editorial, not depth or coverage failures.

---

## Punch list (severity-ordered)

1. **[HIGH — downstream]** /verify-claims must resolve AND independently confirm every Dondi figure (#1 / top-3 / $13–$20 / ~$10 / homepage quotes) and the genfindr 7.6/10, with live URLs. The dossier flags straight.com 404 / scribehow timeout / Reddit blocked at research time — if a figure can't be sourced, hedge or cut it. The trust thesis depends entirely on this.
2. **[MEDIUM — draft]** Bound the break-even's scope in one clause: state it assumes images + voice notes (10 coins each) on **Starter**, and note phone calls (50 coins/min) require Standard+ — so they don't dangle in a Starter-built example. Cheap precision fix; prevents a math-scope nit.
3. **[MEDIUM — draft]** Trim genfindr 7.6/10 repetition (~9×) and the "model your spend before you subscribe" restatement (~5–7×) by 2–3 instances each; vary phrasing. Add a one-line honest vendor-bias acknowledgment to defuse the repeated "fair/honest" framing.
4. **[LOW — optional]** Consider one concrete first-hand Pleasur.ai detail (companion/image/UX) if a later pass has room — would broaden the page beyond the accountant's view without bloating it. Not gate-blocking.

---

## Recommendation

**Proceed to /verify-claims.** This is a depth- and discipline-PASS; the dominant remaining risk (empty citations) is exactly what the next stage owns, and the punch-list items 2–3 are light prose touches that can ride a verify-claims/optimize pass rather than a full re-draft. Do NOT route back to /outline or /research — coverage, structure, and claim-discipline are all sound. Hard requirement on /verify-claims: any Dondi figure that cannot be sourced live gets hedged or cut, not shipped on brief-intel alone.
