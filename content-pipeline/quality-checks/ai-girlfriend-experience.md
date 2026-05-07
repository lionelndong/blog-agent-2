# Quality check — ai-girlfriend-experience

## Verdict: **PASS**

**Combined score: 85 / 100** (auto 75/80 + adversarial 10/20)

The draft clears the PASS threshold (>=75). No CRITICAL constraint violations: the coming-soon Voice Replies and Phone Call features are referenced only as a category-level direction in Act 3 ("In-chat voice replies and a tap-to-call button are the current direction across the category"), not as a Pleasur.AI walkthrough — consistent with the pre-flight reconciliation note in the annotated outline. Live products only (AI Companion Creator at /create; AI Image Generation at /generate) are walked through.

## Metrics summary

- **Forbidden phrases:** 0 found.
- **Voice metrics:** all 7 dimensions within 1.5x SD of the examples baseline.
  - Avg sentence words 14.3 (baseline 15.9). Median 12 (baseline 15).
  - Avg paragraph words 32.8 (baseline 24.3) — slightly long but in range.
  - Second-person 27.7/1k (baseline 41.2) — lighter "you" density than baseline. In range, but worth noting.
  - Em-dash 7.1/1k (baseline 5.9) — slight over-index.
- **BLUF compliance:** 6/6 H2 openers pass (100%). Above the 80% bar.
- **Claim density:** 14 must-cite claims, 9 linked (64.3%). 5 unlinked must-cite items cost 5 pts. Voice-flagged statements: 16 (visibility only).
- **Word count:** 2,240 (target 2,400–2,800; under by ~160–560 words).

## Adversarial critique (full text in `ai-girlfriend-experience-adversarial.md`)

The skeptical reviewer flagged five specific weaknesses:

1. **Three-act arc is a thesis, not a proven finding.** The 8M C.AI MAU drop doesn't time-stamp the churn to week three — the piece treats it as evidence for a narrative shape it imposed.
2. **Six phrases are asserted, not shown.** Section promises "the section nobody else writes" then declines to quote a real chat exchange.
3. **Five-tests section reads like a Lifehacker sidebar bolted onto an essay.** Voice/structure seam between the moody acts and the prescriptive tests.
4. **Privacy paragraph in Act 2 is a sourced data dump.** Five statistics in a row break the experiential register.
5. **Pleasur.AI mentions hedge so hard they undersell.** Repeated "one example of" hedging reads as defensive; only the test-5 worked example actually demonstrates anything.

One thing that works: the opening hook (8M-user defection stat → contrarian framing → thesis) is clean and earns the next 2,000 words.

## Punch list (ordered by severity)

### CRITICAL
- None. Coming-soon products are not walked through; live products only; brand-config compliant.

### HIGH
- **Add 4 missing must-cite citations** (file: `content-pipeline/5-drafts/ai-girlfriend-experience.md`). Five must-cite claims are unlinked; pushing to >=80% would lift the auto score and is exactly the work `/verify-claims` is built to do — flag for that stage. Specifically the SERP composition claim (line 25), the 6,700-word ranking-exercise claim (line 27), the "vendor blog content fails primary verification" claim (line 27), and the Reddit fragment attribution (line 85).
- **Quote one verbatim chat exchange in Act 3** (lines 89–103). The section's own promise ("nobody else writes this") is undercut by listing patterns abstractly. Even one paraphrased-and-labeled exchange would close the gap the adversarial called out. Substantive — not just polish.
- **Smooth the Lifehacker seam in "How to tell — fast"** (lines 120–138). The prescriptive numbered list works, but the lead-in and the test descriptions could carry more of the experiential voice from earlier acts. Rewrite the test rubrics in second-person scenario form rather than imperative form.

### MEDIUM
- **Tighten the privacy paragraph in Act 2** (lines 75–81). Five statistics in a row break the register. Keep Mozilla's 90% and Muah.AI 1.9M; demote the 73% / 54% / Genesia detail to a parenthetical or move to the "privacy policy read" test in the next section, which is the natural home.
- **Re-anchor the "week-three cliff" claim** (line 106). The 8M C.AI MAU drop doesn't timestamp the churn to week three. Either soften the claim ("a real cliff *somewhere* in the experience curve") or add a second source that actually timestamps it. Currently overclaims.
- **Decide on Pleasur.AI hedging posture.** Either reduce the "one example of" repetitions (lines 39, 51, 69, 134) or commit to one strong demonstration and let the others fall away. Current cadence flags as defensive.

### LOW
- **Word count is under target** (2,240 vs 2,400–2,800). Adding the verbatim chat exchange in Act 3 plus the citation work would close most of the gap.
- **Em-dash density slightly over baseline** (7.1 vs 5.9 / 1k). Sweep for filler em-dashes; keep meaningful asides.
- **Visual placeholders** look correctly typed and section-anchored — no action.

## Recommendation

**Proceed to `/verify-claims`** with the HIGH-severity citation gap as the top thing to fix in that stage. The verbatim-chat-exchange and the Lifehacker-seam smoothing should be queued for `/edit` or returned to `/draft` for a targeted revision pass; both are substantive enough that the editor or a revision Agent should take a swing rather than letting `/verify-claims` paper over them with citations.

If running autonomously: the orchestrator should treat this as PASS and continue, with a note in the revision-budget log that HIGH items 2 and 3 were left for the editor pass rather than burning a draft revision on them.

Override the verdict by re-running the next stage manually if a human editor disagrees.
