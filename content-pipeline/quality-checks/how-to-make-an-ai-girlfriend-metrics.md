# Automated quality metrics — how-to-make-an-ai-girlfriend

**Partial score (auto-only):** 63 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Score breakdown
- -8 pts: voice metrics out of baseline range on 2 dimension(s)
- -9 pts: only 42.9% of MUST-CITE claims linked (9/21)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 14.0 | 15.9 | [x] |
| median_sentence_words | 12 | 15.0 | [x] |
| stdev_sentence_words | 9.8 | 10.7 | [x] |
| avg_paragraph_words | 42.6 | 24.3 | [ ] |
| median_paragraph_words | 37.5 | 23 | [ ] |
| second_person_per_1k | 28.8 | 41.2 | [x] |
| em_dash_per_1k | 6.8 | 5.9 | [x] |

Draft total words: 3365
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 6
- Pass: 6 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 21
- Linked: 9 (42.9%)

Sample must-cite claims:
- "Making" an AI girlfriend in 2026 means one of two things.
- You get a real 2026 DIY recipe instead of the 2022 stack the only ranking tutorial still cites [link].
- Here is the 2026 version, with the four components that actually matter and the one thing every guide skips.
- The 2022 tutorial swaps every layer for an obsolete equivalent.
- An A100 80GB on Vast.ai's spot market lists around $0.72 an hour ([Vast.ai vs RunPod 2026 pricing comparison](https://medium.com/@velinxs/vast-ai-vs-runpod-pricing-in-2026-which-gpu-cloud-is-cheaper-b...

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 20
- Linked: 1 (5.0%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- You engineer one from scratch on a rented GPU, which takes a few weeks of evenings and runs around $0.72 per hour while you work.
- Read the first section, pick a lane, skip the other half.
- So the first decision is which path you're on, not which tool.
- The DIY section is honest about why most readers shouldn't take it.
- The Medium post that ranks says "a few weeks." That's honest for someone who already knows PyTorch.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
