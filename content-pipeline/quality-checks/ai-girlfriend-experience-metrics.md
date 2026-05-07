# Automated quality metrics — ai-girlfriend-experience

**Partial score (auto-only):** 75 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Score breakdown
- -5 pts: only 64.3% of MUST-CITE claims linked (9/14)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 14.3 | 15.9 | [x] |
| median_sentence_words | 12 | 15.0 | [x] |
| stdev_sentence_words | 10.3 | 10.7 | [x] |
| avg_paragraph_words | 32.8 | 24.3 | [x] |
| median_paragraph_words | 34.0 | 23 | [x] |
| second_person_per_1k | 27.7 | 41.2 | [x] |
| em_dash_per_1k | 7.1 | 5.9 | [x] |

Draft total words: 2240
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 6
- Pass: 6 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 14
- Linked: 9 (64.3%)

Sample must-cite claims:
- Character.AI's monthly active users dropped from a mid-2024 peak near 28 million to about 20 million by early 2025 ([Business of Apps][link]; [Sacra][link]) — a roughly 28% loss.
- It sits inside the broader [AI chatbot app](https://pleasur.ai/blog/ai-chatbot-app-guide-2026) category, but it's distinct from a one-shot NSFW chatbot, where no character persists.
- The May 2026 SERP top 10 is eight comparison guides, two vendor landings, and zero first-person accounts of what a week-three chat thread looks like.
- The top result is a 6,700-word ranking exercise.
- Wired's first-person 2023 piece ([Wired][link]) is the canonical version of this hook.

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 16
- Linked: 0 (0.0%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- The first 90 seconds are magic.
- It's also distinct from Replika's deliberately platonic "companion" framing.
- That's enough to make most newcomers think the whole experience will keep feeling that way.
- Most platforms let you skip stock characters entirely and design the companion from scratch — appearance, personality, backstory, voice, conversation style.
- Character.AI's much bigger library of pre-made characters is the opposite trade-off.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
