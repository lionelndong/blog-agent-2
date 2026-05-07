# Automated quality metrics — yandere-ai-girlfriend-simulator

**Partial score (auto-only):** 80 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 17.9 | 15.9 | [x] |
| median_sentence_words | 15 | 15.0 | [x] |
| stdev_sentence_words | 13.9 | 10.7 | [x] |
| avg_paragraph_words | 31.1 | 24.3 | [x] |
| median_paragraph_words | 33.5 | 23 | [x] |
| second_person_per_1k | 28.3 | 41.2 | [x] |
| em_dash_per_1k | 5.4 | 5.9 | [x] |

Draft total words: 1840
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 6
- Pass: 6 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 3
- Linked: 3 (100.0%)

Sample must-cite claims:
- The character most people recognize first is Yuno Gasai from *Future Diary* [link] (published by Kadokawa from 2006), a girl so utterly devoted to the protagonist that she will kill anyone who threate...
- AI2U holds Very Positive status on Steam: 89% positive across 1,468 reviews, with recent reviews stable at 83% positive [link].
- See our [Tavern AI and SillyTavern guide](https://www.pleasur.ai/blog/tavern-ai-review-2026) if that route interests you.

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 7
- Linked: 1 (14.3%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- Most content about this topic treats them like they are.
- The AI runs on ChatGPT via the OpenAI API, so she doesn't follow a script.
- The real cost is the OpenAI API key you need to make the AI work.
- New OpenAI accounts come with around $5 in free credits, which is enough for several hours of play.
- The Steam version handles its own AI calls with no OpenAI key required, and you get higher production values including optional voice acting.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
