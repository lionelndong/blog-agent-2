# Automated quality metrics — ai-girlfriend

**Partial score (auto-only):** 56 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Score breakdown
- -13 pts: voice metrics out of baseline range on 3 dimension(s)
- -11 pts: only 25.0% of MUST-CITE claims linked (1/4)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 13.5 | 15.9 | [x] |
| median_sentence_words | 11.0 | 15.0 | [x] |
| stdev_sentence_words | 12.7 | 10.7 | [x] |
| avg_paragraph_words | 39.3 | 24.3 | [ ] |
| median_paragraph_words | 38 | 23 | [ ] |
| second_person_per_1k | 23.0 | 41.2 | [x] |
| em_dash_per_1k | 13.1 | 5.9 | [ ] |

Draft total words: 3821
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 16
- Pass: 16 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 4
- Linked: 1 (25.0%)

Sample must-cite claims:
- The voice — if there was even one — sounded like a 2015 GPS unit.
- The keyword "AI girlfriend" alone gets [hundreds of thousands of searches every month](https://ahrefs.com/keyword-generator) — globally, the demand is well into six figures.
- The top 10 platforms collectively pull in millions of monthly visits.
- Voice runs on a streaming text-to-speech pipeline with a latency budget under 300ms; past that, a call stops feeling like a call.

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 50
- Linked: 1 (2.0%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- Most AI girlfriend platforms are only as good as how naturally chat, memory, voice, and images live in the same conversation.
- Most don't.
- That's why most disappoint.
- That distinction matters more than most reviews acknowledge.
- ChatGPT and Claude are tools.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
