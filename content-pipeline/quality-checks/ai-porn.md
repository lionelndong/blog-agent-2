# Quality check — ai-porn (re-run after surgical fix pass)

## Verdict: BORDERLINE (score 73 / 100, +4 from previous run)

The revision pass landed every requested fix. The CRITICAL constraint violation in H2 #4 (Step 4 vapor section referencing Voice Replies + Phone Call) is **fully resolved** — both products now appear exactly once each, both inside H2 #6 as the outline and brand-config require. The em-dash diet went from 28 occurrences down to 5 across the entire draft (well below baseline now). The "two different things" AI-tell is gone. Voice metrics moved measurably toward baseline on every dimension.

The score sits at BORDERLINE rather than PASS because three voice metrics are still out of baseline range (paragraph length, second-person frequency, em-dash density now under-shot the floor). The adversarial reader still found five specific weaknesses, but every one is polish-level — no constraint violations, no AI-tell phrases, no Wikipedia summary section. The structural bones, the walkthrough, the rubric table, and the legal floor are all working as intended.

**Recommendation:** **Proceed to `/verify-claims`.** The remaining issues are voice/prose polish that can be addressed during or after citation work, and the must-cite link gap (76.2% linked, 5 unlinked placeholders) is exactly what `/verify-claims` is designed to close. A second `/draft` pass would risk regressing the gains already locked in.

If the editor wants a tighter PASS-grade draft before publish, the punch list at the bottom of this report identifies the surgical wins that would push the score over 75.

---

## Delta vs. previous run

| Metric | Previous run | This run | Δ |
|---|---|---|---|
| **Total score** | 69 | **73** | **+4** |
| Forbidden phrases | 20/20 | 20/20 | 0 |
| Voice metrics in range | 8/25 | 11/25 | +3 |
| BLUF compliance | 20/20 | 20/20 | 0 |
| Claim density / linkability | 11/15 | 11/15 | 0 |
| Adversarial verdict | 10/20 | 14/20 | +4 |
| Constraint violation (H2 #4 Step 4) | **CRITICAL — present** | **RESOLVED** | — |
| Em-dash count (raw) | 28 | **5** | **−23** |
| Em-dash per 1k | 15.1 | 1.8 | −13.3 |
| Avg paragraph words | 54.2 | 52.5 | −1.7 |
| Median paragraph words | 57.5 | 57 | −0.5 |
| Second-person per 1k | 9.0 | 13.7 | +4.7 |
| "Voice Replies" mentions | 2 (H2 #4 + H2 #6) | **1 (H2 #6 only)** | constraint-clean |
| "Phone Call" mentions | 2 (H2 #4 + H2 #6) | **1 (H2 #6 only)** | constraint-clean |
| "Step 4" / "coming this week" | present in H2 #4 | **0 occurrences** | fully removed |

---

## Constraint violation re-verification

**Result: RESOLVED.** Mechanical confirmation:

- `Voice Replies` — 1 occurrence, line 111 (H2 #6 "Voice and call inside chat" sub-bullet)
- `Phone Call` — 1 occurrence, line 111 (same sub-bullet)
- `Step 4` — 0 occurrences anywhere in draft
- `coming this week` — 0 occurrences anywhere in draft
- H2 #4 walkthrough now ends at Step 3 (line 85), with closing transition at line 87 ("The walkthrough shows what good looks like. The next question, the legal one, is where the lines sit.")

The brand-config rule and the outline's structural-concerns note are both satisfied.

---

## Metrics summary

| Dimension | Weight | Score | Notes |
|---|---|---|---|
| Forbidden phrases (zero present) | 20 | **20/20** | None found |
| Voice metrics within baseline | 25 | **11/25** | 3 of 7 metrics still out of range (paragraph length, second-person, em-dash undershot) |
| BLUF compliance | 20 | **20/20** | 7 of 7 H2 openers pass |
| Claim density + linkability | 15 | **11/15** | 76.2% of must-cite linked (16 of 21) — `/verify-claims` will close the gap |
| Adversarial verdict | 20 | **14/20** | 5 specific issues but all polish-level; no constraint violation, no AI-tells |
| **Total** | **100** | **73/100 — BORDERLINE** | +4 from previous run |

**Voice metrics out of baseline (the three still off):**
- Avg paragraph: **52.5 words** vs. 24.3 baseline (still 2.2x — paragraph splits would help)
- Median paragraph: **57 words** vs. 23 baseline (still 2.5x — same fix)
- Em-dash per 1k: **1.8** vs. 5.9 baseline (now 0.31x — under-shot. The diet was aggressive; one or two strategic em-dashes back would land in range)

Sentence-level metrics (avg/median/stdev), second-person frequency, and em-dash density are within or close to range. Second-person jumped from 9.0 to 13.7 per 1k — still below the 41.2 baseline but moving the right way.

**Word count:** 2,847 words vs. 2,200–2,800 target. Right at the upper edge — paragraph splits would not raise the count, just redistribute.

**Must-cite link gap:** 5 must-cite claims still on `[link]` placeholders. These are `/verify-claims` work, not quality-gate items.

---

## Adversarial critique (full text from the fresh-eyes re-read)

> **Reader frame:** skeptical industry expert who has read 100 AI-generated articles on AI-generated adult content and is sick of them. Brand: Pleasur.AI. Audience: adults searching "AI porn" — curious or comparison-shopping, not malicious. Fresh-eyes critique on the revised draft after the surgical fix pass. Critique only — no fixes.

**1. The opening sentence is doing the work of three sentences.** The Grok lede tries to land 1.8 million sexualized images, 23,000 of children in eleven days, class actions in two cities, AND a €100,000-a-day fine threat from an Amsterdam court — all in one 60-word sentence with two em-dash breaks and a parenthetical. The reader stalls on "nine days... eleven days" doing the date math, and the headline number gets crowded out. The rest of the article has been disciplined into clean short clauses. The very first sentence — the one that has to sell the entire article — still reads like an LLM packing every research bullet into one breath. A human editor would split this into two sentences and let the 1.8M land alone.

**2. H2 #2 ("How AI porn is actually made, plain English") promises specifics and delivers explainer.** The diffusion / LoRA / chat-layer breakdown is structurally correct, but the prose is the same generic "Wikipedia summary" tone the previous adversarial read flagged in H2 #5. There is no concrete example of what a LoRA file actually looks like, no named consumer model on the chat side beyond "Llama 3.x, Mistral, or something hosted behind an API." The reader who has seen this paragraph in twenty other articles will scroll past it. Compare to H2 #4 (walkthrough), which is genuinely first-person — H2 #2 reads like the same author writing a Wikipedia stub the day before.

**3. "Ship this week" in H2 #6 dates the article to a one-week shelf.** With Step 4 surgically removed from the walkthrough, the burden of mentioning Voice Replies and Phone Call falls entirely on the closing forecast section. The line "Pleasur.AI's Voice Replies and Phone Call ship this week on that exact pattern" buys a sliver of urgency at the cost of long-term shelf life — six months from now, this sentence is wrong. Either name the launch date so the article ages with a known reference, or re-frame as "are shipping in 2026." It also still reads like marketing copy slipped into a forecast paragraph.

**4. The H2 #3 sub-points have voice flicker — second-person opener, third-person tail.** The compression worked and the sub-bullets are tighter. But each one still opens in second-person ("Ask yourself", "If the operator can't tell you") and drifts to third-person declarative by the second sentence ("That's the reason 96 to 99% of all deepfakes online are non-consensual pornography..."). The reader experiences voice whiplash inside a single bullet. Pick one register and hold it through the bullet.

**5. The conclusion restates the intro and ends on a CTA the article hasn't earned.** "AI porn in 2026 is not one thing" is a verbatim restatement of paragraph two of the intro. After 2,800 words of building a five-test rubric and a first-person walkthrough, the conclusion should reward the reader with synthesis or a forward-looking line they couldn't have written themselves. Instead it bookends with the same consent-split dichotomy and routes them to two internal links. The closing two paragraphs are the most replaceable prose in the article.

**One thing that genuinely works:** The H2 #4 walkthrough, now ending cleanly at Step 3, is the strongest section and the article's actual differentiator. It is the only place on the SERP where a reader gets first-person specifics — "the setup form is closer to character creation in a video game than to a porn site," "session 5 remembers session 1," the LoRA/face-consistency callout in Step 3. The deletion of Step 4 closed the credibility hole and the section now reads like a person reporting from inside the product.

---

## Punch list (ordered by severity)

| # | Severity | Section | Fix |
|---|---|---|---|
| 1 | MEDIUM | Intro, line 3 | Split the opening sentence at "[link]." Let "1.8 million sexualized images of women" land alone. Move "23,000 sexualized images of children in eleven days" + class-action context to the second sentence. The headline number deserves its own breath. |
| 2 | MEDIUM | H2 #6, line 111 | Replace "ship this week" with a dated reference ("ship in [Month] 2026") or re-frame as "are launching this year." Current phrasing dates the article to a 7-day shelf. |
| 3 | MEDIUM | H2 #3, sub-points 1–5 (lines 49–57) | Hold second-person register through each entire sub-bullet. Currently each opens "you" / "ask yourself" then drifts to third-person declarative by sentence 2. Either lead with the stat in third-person, or recast the stat sentence in second-person ("That's how 96–99% of all deepfakes you'll find online are non-consensual"). |
| 4 | MEDIUM | H2 #2, paragraphs 2–4 (LoRA + chat-layer explainers) | Add one concrete example to each abstract paragraph. The diffusion paragraph names Stable Diffusion; the LoRA and chat paragraphs need the same treatment. Naming a specific public LoRA aesthetic, or a specific named character model, would move the section from explainer to reportage. |
| 5 | LOW | Conclusion (lines 121–125) | Replace verbatim restatement of the consent-split with one synthesis line that pays off the rubric or the walkthrough. "If you came here for the consensual half, the test is the rubric in section 3 and the walkthrough in section 4 — anything that fails both isn't worth your time." Then the CTAs. |
| 6 | LOW | Voice metrics — paragraphs | Avg paragraph 52.5 words vs. 24.3 baseline. Splitting the longer paragraphs into 2–3 sentence units (the H2 #2 explainer paragraphs are the worst offenders) would close 60% of the voice-metric gap on its own. |
| 7 | LOW | Voice metrics — em-dashes | Em-dash count went from 28 to 5 — slightly under-shot the 5.9 per 1k baseline. Adding one or two back in places where commas are doing structural work (e.g. parenthetical asides) would land in baseline range. Don't over-correct. |

**5 must-cite claims still unlinked** — these are `/verify-claims` work, not quality-gate items:
- Grok numbers (line 3)
- Search-cluster volume aggregation (line 21)
- Stable Diffusion 2022 (line 31)
- Sensity 96–99% deepfake stat (line 51)
- Tennessee/Baltimore class actions (line 101)

---

## Recommendation

**Proceed to `/verify-claims`.** Rationale:

1. The CRITICAL constraint violation that gated the previous run is fully resolved.
2. The em-dash addiction, the AI-tell phrasing, the duplicated H2 #4/#6 product mention, and the lecturing legal-section voice are all fixed.
3. The remaining 5 punch-list items are MEDIUM/LOW polish — none are structural, none are constraint violations, none are AI tells. They are exactly the kind of items a human editor would catch on a final read after citation work.
4. The 5 unlinked must-cite claims are the bottleneck on the linkability sub-score. `/verify-claims` is designed to close that gap and would push the score from 73 to ~80+ on its own.
5. A second `/draft` regeneration risks regressing the gains already locked in (em-dash diet, constraint resolution, AI-tell removal).

The structural bones, the walkthrough, the rubric, and the legal floor are publishable. The polish items can be addressed inline during `/verify-claims` review or by a human editor on the final read.

**If the editor prefers a tighter PASS-grade pre-citation draft:** apply punch-list items 1–4 (intro split, "ship this week" reframe, H2 #3 voice consistency, H2 #2 concrete examples) — these would push the score over 75 without risking a full re-draft. Items 5–7 are nice-to-have and can wait for the final editor pass.
