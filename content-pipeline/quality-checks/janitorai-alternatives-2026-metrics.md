# Automated quality metrics — janitorai-alternatives-2026

**Partial score (auto-only):** 77 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 13.2 | 15.9 | [x] |
| median_sentence_words | 10 | 15.0 | [x] |
| stdev_sentence_words | 9.4 | 10.7 | [x] |
| avg_paragraph_words | 34.7 | 24.3 | [x] |
| median_paragraph_words | 34 | 23 | [x] |
| second_person_per_1k | 28.6 | 41.2 | [x] |
| em_dash_per_1k | 5.7 | 5.9 | [x] |

Draft total words: 1225
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 7
- Pass: 7 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 5
- Linked: 4 (80.0%)

Sample must-cite claims:
- JanitorAI's April 2026 age-verification rollout [link] sent its own subreddit looking for the exit.
- Minimal, white background, sans-serif labels, no people, brand-neutral colors.;style=illustration;safety=sfw] ## What changed at JanitorAI in 2026 In April 2026, JanitorAI made age verification mandat...
- Australia's Age-Restricted Material Codes and Brazil's Digital ECA both landed in early 2026 [link], and adult platforms have to respond.
- We've covered it in depth in our [CrushOn AI review](https://pleasur.ai/blog/crushon-ai-review-2026) if you want the full picture.
- If you're still weighing options, our guide to the [Best AI Girlfriend Apps: Choose Safely in 2026](https://pleasur.ai/blog/ai-girlfriend-apps) walks through the same decision with more room to breath...

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 7
- Linked: 3 (42.9%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- The replacement lists mostly read the same — ten apps, a few badges, not much honesty.
- Most of the space is now moving the same direction.
- Starter is $12.99/mo, Standard is $27.99/mo and the most popular tier, Ultimate is $49.99/mo [link].
- Every app here is a reasonable 18+ choice once you know what matters most to you.
- **What is the best budget JanitorAI alternative?** CrushOn.ai, from around $5.99/mo [link], with better long-chat memory than JanitorAI.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
