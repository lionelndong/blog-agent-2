# Automated quality metrics — build-a-girlfriend-body

**Partial score (auto-only):** 74 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Score breakdown
- -6 pts: only 58.8% of MUST-CITE claims linked (10/17)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 13.1 | 15.9 | [x] |
| median_sentence_words | 11.0 | 15.0 | [x] |
| stdev_sentence_words | 8.5 | 10.7 | [x] |
| avg_paragraph_words | 28.6 | 24.3 | [x] |
| median_paragraph_words | 27.0 | 23 | [x] |
| second_person_per_1k | 23.2 | 41.2 | [x] |
| em_dash_per_1k | 5.4 | 5.9 | [x] |

Draft total words: 2414
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 7
- Pass: 7 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 17
- Linked: 10 (58.8%)

Sample must-cite claims:
- Every AI girlfriend creator on the market in 2026 funnels you through the same seven body decisions: art style, archetype, ethnicity, hair, body type, breast and butt sliders, and outfit.
- Parent topic "ai girlfriend" pulls 80,000 searches per month [link] — small head term, large tail.
- The traffic potential of the #1 ranking page is roughly 19,000 visits a month, which is what Kupid AI's create page actually pulls today.
- Outfit | Match the energy | Most disposable; changeable in chat | For the open-source path where you write the body description in raw character cards, see our [Tavern AI Review 2026](https://pleasur....
- For the broader category context on how a builder fits next to chat, voice, and image gen, [AI Girlfriend Simulator: What It Is and Best Options in 2026](https://pleasur.ai/blog/ai-girlfriend-simulato...

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 19
- Linked: 2 (10.5%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- The character looks worse than the first preset you skipped.
- This guide walks every step in the Pleasur.AI Companion Creator with real screenshots.
- Candy.AI's marketing copy notably leaves the sliders unnamed [link].
- Where most builds break is here.
- **Outfit.** Last, because it's the most disposable.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
