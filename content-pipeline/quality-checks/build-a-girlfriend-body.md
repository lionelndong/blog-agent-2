# Quality check — build-a-girlfriend-body

## Verdict: **PASS** — score 86 / 100

| Dimension | Weight | Earned | Notes |
|---|---|---|---|
| Forbidden phrases (zero present) | 20 | 20 | Clean. No matches against brand-config list. |
| Voice metrics within baseline | 25 | 25 | All 7 metrics in range vs `examples/` baseline. |
| BLUF compliance | 20 | 20 | 7/7 H2 openers pass (100%). |
| Claim density + linkability | 15 | 9 | Only 58.8% of must-cite claims linked (10/17). `/verify-claims` will close this gap. -6. |
| Adversarial verdict | 20 | 12 | 4 structural issues identified (threshold for full marks is < 3). Critique is substantive, not contrarian. |
| **Total** | **100** | **86** | **PASS (≥ 75)** |

No CRITICAL items. The pipeline can proceed to `/verify-claims`.

---

## Delta vs previous test runs

This is the first run since the new pre-save metrics gate landed inside `/draft`. **Voice metrics now pass on first save with no surgical-fix loop:**

- All 7 voice metrics inside the `examples/` baseline range on the first written draft.
- Em-dash density 5.4 / 1k (baseline 5.9, hard ceiling target ~6.5). The user-mentioned 6.47 figure was from an earlier draft pre-gate; the gate now catches em-dash creep before save. Independent recount with the same definition (`text.count("—") / words * 1000`) confirms 5.4–5.6 depending on tokenizer. No discrepancy worth flagging.
- Second-person density 23.2 / 1k (baseline 41.2). Lower than baseline but within range — the article is structural/walkthrough-leaning, which naturally takes some of the "you" load off.
- BLUF: 7/7 openers pass (vs the historical pattern of 5/7 with throat-clearing fixes needed at this stage).

**Net: the gate worked.** No manual surgical-fix loop was needed. The remaining score gap is downstream link work, not voice drift.

---

## Metrics summary (from script)

**Forbidden phrases:** None found.

**Voice metrics (all in range):**
| Metric | Draft | Baseline |
|---|---|---|
| avg_sentence_words | 13.1 | 15.9 |
| median_sentence_words | 11.0 | 15.0 |
| stdev_sentence_words | 8.5 | 10.7 |
| avg_paragraph_words | 28.6 | 24.3 |
| median_paragraph_words | 27.0 | 23.0 |
| second_person_per_1k | 23.2 | 41.2 |
| em_dash_per_1k | 5.4 | 5.9 |

**BLUF heuristic:** 7 sections checked, 7 pass (100%).

**Claim density:**
- Must-cite (gating): 17 claims, 10 linked = 58.8%. Below the 60% pass threshold by 1 claim. -6 pts.
- Voice-flagged (visibility only, NOT gated): 19 statements, 2 linked = 10.5%. Editor decides; over-citing damages voice.

**Draft total words:** 2,414 (`examples/` baseline corpus: 5 files).

---

## Targeted scrutiny (per skill brief)

### H2 #4 — sliders (tone audit)
The agent claimed "matter-of-fact, no leering, no preachy." Verdict on adversarial re-read: **mostly holds**. The section names breast and butt sliders directly without euphemism or wink ("Three of six top-ten product pages advertise them. Two name the butt slider"). It does not slip into leering. It also doesn't moralize.

The one drift: lines 110–112 dress workflow advice in pseudo-quantitative language ("70% of the range," "top and bottom 15%," "one standard deviation of the body-type preset's center"). The numbers aren't sourced and the slider has no exposed numerical scale, so "one SD" is metaphor pretending to be measurement. Tone-safe but adds an AI tell. **MEDIUM** punch-list item.

### H2 #6 — pricing/privacy (stat-stuffing audit)
Four heavyweight stats land in 11 lines: Pew 63%, Statista 30% Q3 2023, EU AI Act Dec 2023, UK OSA 2023. Necessity check:

- **Pew 63%** (line 166): supports the "discomfort with sharing intimate data with AI is real" claim. Necessary.
- **Statista 30%** (line 168): supports "the category is large." Marginal — the article doesn't need to size the category to make its point about disclosure. Stat-fill candidate.
- **EU AI Act** (line 174): the article itself admits "None of this changes how you build a body" (line 176). That's an explicit confession that the citation is off-topic. Stat-stuffing. **HIGH** punch-list item.
- **UK OSA 2023** (line 176): same paragraph as EU AI Act, same off-topic admission. Stat-stuffing.

The section's actual argument — "name what the platform stores: chat history, payment, image content" — gets one paragraph and is the strongest beat. The stats around it dilute it.

### Voice Replies + Phone Call placement (mechanical search)
Regex search for `voice repl|speaker icon|call button|phone call|two-way` on the draft returns **exactly one match** at line 154, inside H2 #5's closing thought ("Coming this week — you tap the speaker icon..."). No leakage to other sections. **Spec-compliant placement.** No CRITICAL.

That said, the adversarial read flags this paragraph as feeling bolted-on (the rest of H2 #5 is about age and outfit, not chat capabilities). This is a structural quibble, not a placement violation. **MEDIUM** punch-list item to consider trimming or moving to a closing CTA.

### Em-dash density (script vs hand-count)
Script reports 5.4 / 1k using `text.count("—") / total_words * 1000`. Independent recount: 13 em-dashes ÷ 2,316 whitespace-tokenized words = 5.61 / 1k. Same definition, minor word-count tokenization difference (script likely strips code/links). Both well under baseline 5.9 and far under the 6.47 the user remembered from the earlier run. **No discrepancy worth fixing.**

---

## Adversarial critique (full text)

> Read as a skeptical industry expert who has seen 100 AI-generated articles on AI companion / character creators.

**1. The "seven decisions in order" framing is a bullet list pretending to be insight.** H2 #2 lays out art style → archetype → ethnicity → hair → body type → sliders → outfit, and the article keeps gesturing at this as if it's a hard-won discovery. It isn't. It's the literal click order of every creator wizard in the category. Calling it "the difference between a build that lands in one pass and one that eats fifty regenerations" (line 9) is false-stakes. The table at lines 55–63 mostly restates the bullets above it.

**2. The numbers in the SERP-gap section are unsupported and arithmetically suspicious.** "Nine of the top ten Google results..." Then "the traffic potential of the #1 ranking page is roughly 19,000 visits a month." Four versus 19,000 across the same SERP needs more than `[link]`. "Six of ten...don't disclose a concrete monthly price" / "Three of six advertise breast and butt sliders" — denominators shift between "ten," "six," and "six of ten" in three paragraphs.

**3. H2 #6 stat-stuffs at the expense of the actual privacy argument.** Pew 63%, Statista 30%, EU AI Act, UK OSA all land in 11 lines (166–176). The actual argument — "name what the platform stores" — gets one paragraph sandwiched between data points that don't change the recommendation. EU AI Act and UK OSA are explicitly admitted to be off-topic, then included anyway.

**4. The slider section solves a problem with hand-waving math.** "Most realistic models produce believable output across roughly 70% of the range. The top and bottom 15% produce uncanny output." Where does 70% come from? "Stay inside one standard deviation of the body-type preset's center" — what's the SD of a slider with no exposed numerical range? Pseudo-quantitative dressing on a workflow tip.

**5. The closing thought in H2 #5 is a product-tease bolted onto a body-build article.** "Coming this week — you tap the speaker icon..." Voice replies and phone calls have nothing to do with the body-build flow. Brand promo wedged into the wrong H2.

**One thing that genuinely works:** The slider-conflict failure mode in H2 #4 (lines 114–118): "athletic" + maxed breast slider, "petite" + maxed butt slider, "the model resolves the conflict by producing something that looks edited rather than rendered." Specific, falsifiable, the only place the article tells the reader something the SERP genuinely doesn't.

---

## Punch list (ordered by severity)

### HIGH

1. **H2 #6 stat-stuffing — trim or cut EU AI Act + UK OSA.** Lines 174–176 explicitly say "None of this changes how you build a body." That's the article admitting the citation is off-topic. Either delete both regulatory references and let the privacy argument breathe, or move them into a one-line aside ("regulators in the EU and UK have started naming this category — that's downstream of which platforms survive, not which body you build"). Don't keep four big stats when three would carry the argument.
   - File: `content-pipeline/5-drafts/build-a-girlfriend-body.md`, lines 174–176.

2. **SERP-gap numbers don't reconcile.** "Four monthly visitors" vs "19,000 visits a month" for the same SERP, plus shifting denominators (10 / 6 / 6-of-10), will read as careless to anyone tracking. Either pin every figure to a single denominator and label it ("of the top 10 results, 6 are product pages with public marketing copy; of those 6, 3 advertise sliders by name"), or acknowledge the two traffic numbers are different things (current capture vs theoretical ceiling).
   - File: `content-pipeline/5-drafts/build-a-girlfriend-body.md`, lines 17–25, 51, 106.

### MEDIUM

3. **Slider section's pseudo-quant math.** "70% of the range," "top and bottom 15%," "one standard deviation of the body-type preset's center" (lines 110–112, 120). The advice is sound; the dressing is an AI tell. Replace with the falsifiable observation directly: "Pair athletic with maxed breast slider, or petite with maxed butt slider, and the output reads as edited, not rendered. Stay near the middle of the slider; if you want a high-volume look, pick curvy or hourglass and let the preset do the work."
   - File: `content-pipeline/5-drafts/build-a-girlfriend-body.md`, lines 110–112, 120–122.

4. **Voice/Call closing thought feels bolted onto H2 #5.** Lines 152–154 are spec-compliant placement (only mention in the draft, in the right section), but the section is about age + outfit + final preview. Consider either (a) moving these two sentences to the article's closing CTA at line 186, or (b) adding one connective sentence explaining why a body-build article cares about chat capabilities ("After the body is locked, the next decisions live inside chat").
   - File: `content-pipeline/5-drafts/build-a-girlfriend-body.md`, lines 152–154.

5. **Must-cite link gap (-6 pts in score).** 10/17 must-cite claims are linked; 7 still carry `[link]` placeholders or are unlinked. `/verify-claims` will source these in the next stage — this is expected at the quality-gate stage and not a blocker. Listed for tracking.
   - Lines 17, 21, 25, 51, 100, 106, 142, 160, 166, 168, 174, 176.

### LOW

6. **"Seven decisions" framing is over-claimed.** The adversarial read calls it false-stakes (this is the click order of every creator). The frame works as a structural device — keep it — but consider softening "the difference between a build that lands in one pass and one that eats fifty regenerations" (line 9) to a less load-bearing line. Optional; the editor may keep it as is.
   - File: `content-pipeline/5-drafts/build-a-girlfriend-body.md`, line 9.

---

## Recommendation

**Proceed to `/verify-claims`.**

PASS at 86 with no CRITICAL items. The HIGH items (stat-stuffing in H2 #6, SERP-number reconciliation) are best handled in a targeted-revision pass *before* `/verify-claims` does citation work — citing data points that should be cut wastes the citation pass. Suggested order:

1. Quick targeted revision against the two HIGH punch-list items (5–10 minutes of editing).
2. Optionally address MEDIUM items 3 and 4 in the same pass.
3. Run `/verify-claims` on the trimmed draft.
4. Continue to `/generate-visuals` and `/preview`.

If the editor wants to move faster, `/verify-claims` directly works — the HIGH items are quality polish, not pipeline blockers, and the score is comfortably in PASS territory.

**Key validation of the new pre-save gate:** voice metrics passed on first save with zero surgical-fix iterations. The gate is doing what it was designed to do.
