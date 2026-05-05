# Automated quality metrics — ai-boyfriend

**Partial score (auto-only):** 78 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 14.1 | 15.9 | [x] |
| median_sentence_words | 12.0 | 15.0 | [x] |
| stdev_sentence_words | 11.9 | 10.7 | [x] |
| avg_paragraph_words | 32.0 | 24.3 | [x] |
| median_paragraph_words | 32.0 | 23 | [x] |
| second_person_per_1k | 48.9 | 41.2 | [x] |
| em_dash_per_1k | 6.5 | 5.9 | [x] |

Draft total words: 2927
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 7
- Pass: 7 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 19
- Linked: 16 (84.2%)

Sample must-cite claims:
- In 2026, it's one of the fastest-growing segments in AI companionship [link] — and the demographic leading adoption might surprise you.
- Search volume for "AI boyfriend" has hit 180,000 annual queries in the US alone [link].
- That's still a fraction of "AI girlfriend" searches (roughly 11% [link]), but the gap is closing faster than the industry expected [link].
- In China, apps like Xingye have hit 500,000 daily active users, with women making up the majority [link].
- The global AI companion market hit $3.08 billion in 2025 [link], with projections north of $19 billion by 2035 [link].

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 23
- Linked: 0 (0.0%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- This guide covers what makes an AI boyfriend worth your time, compares the top platforms on the features that matter, walks you through building your own, and addresses the privacy crisis that most ar...
- That's what separates an AI boyfriend from a general chatbot like ChatGPT or Claude.
- Most apps on the market sit somewhere in the middle.
- Good enough to hook you in the first session, not good enough to keep you coming back after a month.
- Most listicles rate apps by appearance options: how many hairstyles, how many outfits, how many body types.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
