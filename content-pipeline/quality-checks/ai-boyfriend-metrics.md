# Automated quality metrics — ai-boyfriend

**Partial score (auto-only):** 77 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 15.2 | 15.9 | [x] |
| median_sentence_words | 14.0 | 15.0 | [x] |
| stdev_sentence_words | 9.1 | 10.7 | [x] |
| avg_paragraph_words | 32.7 | 24.3 | [x] |
| median_paragraph_words | 31.5 | 23 | [x] |
| second_person_per_1k | 35.3 | 41.2 | [x] |
| em_dash_per_1k | 5.9 | 5.9 | [x] |

Draft total words: 2865
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 8
- Pass: 8 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 17
- Linked: 14 (82.4%)

Sample must-cite claims:
- In 2026, it's one of the fastest-growing corners of AI companionship, and the people leading adoption aren't who the tech industry expected.
- "AI boyfriend" pulls roughly [180,000 searches a year in the US — about 11% of the volume "AI girlfriend" gets](https://www.trgdatacenters.com/resource/google-search-data-reveals-usa-most-interested-i...
- In China, apps like Xingye have reached [500,000 daily active users, most of them women](https://www.sixthtone.com/news/1015906).
- The global AI companion market hit [$3.08 billion in 2025](https://dataintelo.com/report/ai-girlfriend-app-market), with projections north of [$19 billion by 2035](https://dataintelo.com/report/ai-gir...
- Research from Harvard Business School found AI companions can deliver real emotional benefits, but only when people [feel genuinely heard](https://www.hbs.edu/faculty/Pages/item.aspx?num=67360).

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 28
- Linked: 1 (3.6%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- This guide covers what an AI boyfriend actually is, who they're for, how they work, how to pick one, and the privacy problem most articles in this space skip entirely.
- That's what separates an AI boyfriend from a general assistant like ChatGPT.
- Most apps land in the middle.
- Good enough to hook you in the first session.
- Not good enough to keep you past the first month.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
