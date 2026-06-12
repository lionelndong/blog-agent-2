# Automated quality metrics — best-replika-alternative-2026

**Partial score (auto-only):** 75 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Score breakdown
- -5 pts: only 66.7% of MUST-CITE claims linked (12/18)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 20.2 | 15.9 | [x] |
| median_sentence_words | 20.0 | 15.0 | [x] |
| stdev_sentence_words | 10.9 | 10.7 | [x] |
| avg_paragraph_words | 36.0 | 24.3 | [x] |
| median_paragraph_words | 34 | 23 | [x] |
| second_person_per_1k | 22.1 | 41.2 | [x] |
| em_dash_per_1k | 5.2 | 5.9 | [x] |

Draft total words: 2306
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 8
- Pass: 8 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 18
- Linked: 12 (66.7%)

Sample must-cite claims:
- Replika took away the two things its users wanted most: adult conversation, cut in February 2023, and a companion that remembers you.
- If you typed "2026" into your search, you're done waiting for either one to come back.
- On 2 February 2023, Italy's data-protection regulator, the Garante, [ordered Luka to stop processing Italian users' data](https://techcrunch.com/2023/02/03/replika-italy-data-processing-ban/).
- [VISUAL:type=external;sub=news-quote;url=https://www.vice.com/en/article/ai-companion-replika-erotic-roleplay-updates/;selector=article;crop=padded;what=Vice headline on Replika ERP-removal user distr...
- Vice documented users in genuine crisis, and a [peer-reviewed study of the r/Replika discourse](https://journals.sagepub.com/doi/10.1177/23780231241259627) examined how users responded after the remov...

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 19
- Linked: 3 (15.8%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- The first one still defines the brand.
- Across reviews and community threads, users describe Replika's memory as limited and summary-style — a companion that forgets who you are between conversations.
- Replika is user-reported as limited and summary-style.
- Replika has a free tier with adult roleplay gated.
- Replika's Pro price varies.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
