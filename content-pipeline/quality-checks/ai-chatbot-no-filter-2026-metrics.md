# Automated quality metrics — ai-chatbot-no-filter-2026

**Partial score (auto-only):** 73 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Score breakdown
- -7 pts: only 50.0% of MUST-CITE claims linked (1/2)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 15.0 | 15.9 | [x] |
| median_sentence_words | 12.0 | 15.0 | [x] |
| stdev_sentence_words | 15.6 | 10.7 | [x] |
| avg_paragraph_words | 33.3 | 24.3 | [x] |
| median_paragraph_words | 34 | 23 | [x] |
| second_person_per_1k | 24.0 | 41.2 | [x] |
| em_dash_per_1k | 5.2 | 5.9 | [x] |

Draft total words: 2125
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 16
- Pass: 16 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 2
- Linked: 1 (50.0%)

Sample must-cite claims:
- _Updated June 2026 — for adults (18+) only._ ## Quick Answer: What "AI Chatbot No Filter" Usually Means An "AI chatbot no filter" usually means an adult or open-roleplay chatbot that claims fewer cont...
- For adult-chat language and definitions, the [dirty AI guide](/blog/dirty-ai-guide-2026) goes deeper on terms.

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 3
- Linked: 0 (0.0%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- "Uncensored ai chatbot" pulls the most monthly searches in the US, "ai chatbot no filter" sits a notch below it, and "dirty ai" trails close behind.
- It also prevents the most common mistake here: repeating a no-filter slogan as if it were verified safety, privacy, or quality evidence.
- An AI chatbot with no filter is usually an adult-oriented chat app with fewer sexual-content restrictions than mainstream assistants.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
