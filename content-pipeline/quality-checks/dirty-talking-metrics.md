# Automated quality metrics — dirty-talking

**Partial score (auto-only):** 72 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Score breakdown
- -8 pts: voice metrics out of baseline range on 2 dimension(s)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 13.9 | 15.9 | [x] |
| median_sentence_words | 11.0 | 15.0 | [x] |
| stdev_sentence_words | 10.7 | 10.7 | [x] |
| avg_paragraph_words | 39.5 | 24.3 | [ ] |
| median_paragraph_words | 41.0 | 23 | [ ] |
| second_person_per_1k | 53.9 | 41.2 | [x] |
| em_dash_per_1k | 3.8 | 5.9 | [x] |

Draft total words: 1838
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 11
- Pass: 11 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 2
- Linked: 2 (100.0%)

Sample must-cite claims:
- In a survey of more than 4,000 adults, [dirty talk showed up as one of the most frequently wanted elements in people's sex lives](#).
- If that's the door you want, our guide to [unfiltered adult AI chat](https://pleasur.ai/blog/dirty-ai-guide-2026) covers where to start.

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 4
- Linked: 0 (0.0%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- Sex educators have a saying for it: the brain is the biggest sex organ.
- The fastest way to kill your nerve is to open with your most explicit line and watch it land flat — so start with a compliment and climb one rung at a time.
- A quick, low-stakes question outside the bedroom — "is dirty talk something you'd be into?" — removes most of the fear before you ever say a word.
- Most misfires come from three places.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
