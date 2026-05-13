# Automated quality metrics — ai-sexting-app

**Partial score (auto-only):** 69 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Score breakdown
- -11 pts: only 29.2% of MUST-CITE claims linked (7/24)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 15.7 | 15.9 | [x] |
| median_sentence_words | 14 | 15.0 | [x] |
| stdev_sentence_words | 8.8 | 10.7 | [x] |
| avg_paragraph_words | 30.4 | 24.3 | [x] |
| median_paragraph_words | 30 | 23 | [x] |
| second_person_per_1k | 29.5 | 41.2 | [x] |
| em_dash_per_1k | 7.5 | 5.9 | [x] |

Draft total words: 2782
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 12
- Pass: 12 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 24
- Linked: 7 (29.2%)

Sample must-cite claims:
- --- title: "Best AI Sexting Apps in 2026: 4 Worth Your Time" description: "Four AI sexting apps worth your time in 2026.
- Honest picks, real prices." slug: "ai-sexting-app" category: "ai-companions" author_name: "Pleasur.AI Editorial" read_time: 10 --- # Best AI Sexting Apps in 2026: 4 Worth Your Time Most "best AI sexti...
- Four apps are worth your time in 2026.
- Mozilla flagged this entire category in 2024, and one app on every "best of" list leaked 1.9 million accounts shortly after [link].
- Then: what "free" means in 2026, and quick answers to the questions readers ask after they've picked but before they sign up.

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 21
- Linked: 2 (9.5%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- ChatGPT, Claude, and Replika all filter adult content, break character on contact, or both.
- The [AI Girlfriend Experience](https://pleasur.ai/blog/ai-girlfriend-experience) piece walks a worked example across the first three weeks.
- Google ranks a Washington Post piece at #2 and a Reddit thread at #4.
- [VISUAL:type=table;subject=feature-pricing-privacy-matrix;data=research.feature_matrix+research.pricing_comparison] ### Candy.AI — the polished default Candy.AI is the pick if you want the most polish...
- Pre-built characters dominate the surface; the custom-build flow is shallower than what you get with Pleasur.AI's Companion Creator.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
