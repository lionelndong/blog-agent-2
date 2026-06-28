# Quality Check — joi-ai-alternative-2026 (re-run after surgical revision)

## Verdict: **PASS**

- **Final score: 95 / 100** (0.6 × mechanical 100 + 0.4 × judgment 88 = 95.2)
- **Mechanical: 100/100** — no dimension below 60% floor; no CRITICAL.
- **Adversarial: KEEPS OURS** (flipped from the prior BORDERLINE, which kept scribehow).
- **CRITICAL findings: none.**
- **Constraint-violation re-audit (6 classes): all clean — no regression introduced by the revision.**
- **Recommendation: PROCEED to `/verify-claims`.** The single most important downstream action is resolving the 18 `[link]` placeholders — they are expected at draft stage but are the article's entire evidence spine (esp. the load-bearing genfindr 7.6/10 citation).

This is a re-run of stage 6 after a surgical revision addressed the prior BORDERLINE's 3 punch-list items: (1) concrete attributed specifics added to all 5 competitor sections; (2) comparison table price + message-cap columns populated with attributed varying values; (3) privacy section rebuilt as a real multi-app comparison. The revision flipped the side-by-side read and introduced no constraint regressions.

---

## Mechanical metrics summary

| Dimension | Score | Weight | Floor (60%) |
|---|---|---|---|
| depth_vs_benchmark | 25.0 | 25 | ok |
| consensus_coverage | 20.0 | 20 | ok |
| evidence | 15.0 | 15 | ok |
| ai_tells | 25.0 | 25 | ok |
| structure | 15.0 | 15 | ok |

- **Word count: 3,640 (script) / ~3,830 prose vs 2,800 target — ratio 1.30.** Over beat spec by ~30–37%. See length judgment below.
- Claim density 0.26 (44/172 numeric sentences); 16 hyperlinks live + 18 `[link]` placeholders (OK at draft; verify-claims must resolve).
- Repetition flags (crutch words, all soft): "current" ×22, "verify" ×21, "companion" ×17, "adult" ×17, "rather" ×17. The "current"/"verify" pair is a real verbal tic driven by the per-section "verify current" hedge — see punch list #2.
- Paragraph rhythm: mean 48w, CV 0.48 (healthy variance, no uniform-rhythm AI tell).

## Length judgment (the ~37% overage)

**Justified in principle, trimmable in execution.** The article is beating a 3,700-word first-hand leader, so length parity is competitive, not padding-by-default — the depth target legitimately tracks the SERP, not the 2,800 floor. But ~400–500 words are genuine restatement: the cap-and-Neurons pains are explained three times (intro line 3, "Why people are leaving" lines 13–17, table preamble line 31), and the per-section "verify current" hedge repeats ~12× when one standing disclaimer under the table (already present, line 43) would carry it. Trim is a polish recommendation, **not** a gate failure — the depth is genuine and the overage does not sink the side-by-side.

## Voice + judgment read (judgment: 88/100)

Read against `examples/voice/pleasur-privacy-data-guide.md` (the closest niche+structure anchor). The draft sits squarely in brand voice: BLUF section openers, concrete attributed specifics, table-driven comparison, and the signature honesty register ("a document you can open and read, not a badge" mirrors the anchor's "read the policy yourself"). Would survive a serious byline — it does not read as AI. Information gain is real and on-spec: the privacy-as-buying-axis comparison and the inclusion of a memory-first/no-cap pick (absent from every ranking page) are both genuinely not on page 1. Product mentions are demonstrated, not bolted on — the #3 placement with a stated reason ("it earns the spot on the two Joi pains, not by sitting at the top of an affiliate list") is the article's credibility moat. Points off for: 6 of 7 competitor cards are secondhand reviewer paraphrase vs scribehow's first-hand-on-all-seven texture, and the restatement noted above.

## Adversarial critique (full read in `joi-ai-alternative-2026-adversarial.md`)

**Verdict: KEEP OURS.** "Side by side, this draft wins for the specific reader it targets — the frustrated Joi user — because it does three things scribehow doesn't: it opens honest about the cap being reviewer-reported (not a fabricated spec), it includes a genuine privacy-as-buying-axis comparison, and it has a real migration section, while still matching scribehow's table + per-app depth and 7-app roster."

- **The revision flipped the read.** The added competitor specifics (Candy's Live Action clips, OurDream's "past ~100 messages," LoveScape's interactive-story mode, Kindroid's memory journal, CrushOn's per-character model choice) killed the home-team depth asymmetry that drove the prior BORDERLINE. The populated table (varying attributed prices $5.90–$27.99, differentiated memory cells) and the privacy comparison are the real flippers.
- **Depth-parity gap closed; first-hand gap not.** We test one app (Pleasur, §3), reviewer-paraphrase the other six. Acceptable trade for an honest brand piece, but not a match for scribehow's hands-on-all-seven provenance.
- **Padding callouts:** cap/Neurons restated 3×; "verify current" repeated to a tic; the LoveScape trade-off graf is generic. (The OurDream "flat-rate" trade-off graf is good substance, not padding.)
- **One thing that genuinely works:** the honest billing paragraph (§3, line 87) + the explicit #3 placement justification — the credibility no affiliate listicle can buy.

## Constraint-violation re-audit (6 classes — all CLEAN, no regression)

1. **Joi facts reviewer-attributed, not Joi-published** — PASS. Every cap/Neurons/price claim is framed "hands-on reviewers report" / "according to third-party reviews" / "Joi's own site doesn't publish" (lines 15, 17, 19, 189). No "Joi states/charges" assertions.
2. **No quarantined Pleasur.ai pricing** — PASS. Zero instances of $9.99/$19.99/$19-mo/"no metering"/"no credit meter" applied to Pleasur.ai. Pleasur's own pricing is canonical throughout: $12.99/$27.99/$49.99, $5.20/mo annual (lines 37, 87). The new competitor cells use ~$9.99 for **LoveScape/Kindroid** (lines 38–39) and ~$9.99 for **Character AI c.ai+** (line 41) — legitimate, as instructed; Pleasur's own row stays canonical.
3. **"Unlimited" never applied to Pleasur.ai** — PASS. Both "unlimited" hits explicitly negate it: line 71 warns against assuming a competitor bundle "means unlimited"; line 87 states Pleasur media "is coin-metered on every tier — it is not unlimited."
4. **Memory attributed to genfindr 7.6/10** — PASS. Lines 37, 85, 192 all attribute, with explicit "we're attributing that, not claiming a bare 'best memory' superlative" (line 85).
5. **No "no filter" absolutism; 18+ throughout** — PASS. Line 143 actively disclaims it: "We're not calling any app here 'no filter' or 'anything goes'." 18+/adult framing appears 16×, including the closing safety caveat (lines 165, 204).
6. **No internal-stack vendor names; no Pleasur shoehorned into competitor sections** — PASS. Zero internal-tool/vendor names (Firecrawl/Perplexity/Replicate/Strapi/Supabase/Semrush/etc.). Pleasur.ai appears only in answer-first triads (intro/conclusion/FAQ, as a co-equal pick), its own §3, the table row, and the privacy axis (as the verifiable data point) — never inside a competitor's section.

## Punch list (top 3 by severity)

1. **[HIGH — owned by /verify-claims, not a gate blocker] Resolve all 18 `[link]` placeholders.** The evidence spine is currently unfilled, including the load-bearing genfindr 7.6/10 citation and the attributed competitor prices. Expected at draft stage; must be live before publish.
2. **[MEDIUM — polish] Trim ~400–500 words of restatement.** Cap/Neurons explained 3× (lines 3, 13–17, 31); consolidate the per-section "verify current" hedge (~12 instances) into the single standing disclaimer under the table (line 43). Brings it toward the 2,800 target without losing depth and kills the "verify/current" crutch-word flag.
3. **[MEDIUM — information gain completeness] Extend the privacy axis from 4 apps to the full 7.** The privacy comparison (lines 159–163) covers Candy, OurDream, Character AI + Pleasur but omits LoveScape, Kindroid, CrushOn — the beat spec sells privacy as *the* differentiating axis, so a 4-of-7 axis slightly undercuts the "real comparison axis" claim. Optional given the section already clears the bar, but it would harden the headline information gain.

## Recommendation

**PROCEED to `/verify-claims`.** Score 95, no CRITICAL, no mechanical floor breach, adversarial keeps ours, all six constraint classes clean. Punch-list items 2 and 3 are polish/optional and do not gate; item 1 is verify-claims' job. Length overage is justified by competitiveness and should be lightly trimmed, not failed.
