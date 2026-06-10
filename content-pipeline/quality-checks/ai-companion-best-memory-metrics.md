# Automated quality metrics — ai-companion-best-memory

**Partial score (auto-only):** 72 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Score breakdown
- -8 pts: voice metrics out of baseline range on 2 dimension(s)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 17.5 | 15.9 | [x] |
| median_sentence_words | 15 | 15.0 | [x] |
| stdev_sentence_words | 16.4 | 10.7 | [x] |
| avg_paragraph_words | 39.9 | 24.3 | [ ] |
| median_paragraph_words | 38.5 | 23 | [ ] |
| second_person_per_1k | 39.7 | 41.2 | [x] |
| em_dash_per_1k | 5.4 | 5.9 | [x] |

Draft total words: 1838
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 10
- Pass: 10 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 5
- Linked: 5 (100.0%)

Sample must-cite claims:
- For adult AI companions, Pleasur.AI has the [best memory system tested in 2026](https://genfindr.com/blog/pleasur-ai-review-2026) — an independent review scored it 7.6/10 and singled out memory as the...
- The same [independent review that scored it 7.6/10](https://genfindr.com/blog/pleasur-ai-review-2026) called memory the one thing it does better than anyone else it tested.
- For the broad category, [Nomi has the strongest long-term memory in 2026](https://aicompanionguides.com/blog/memory-systems-compared-who-remembers-best/), with structured fact extraction and a browsab...
- Among adult companions specifically, Pleasur.AI was [rated the best memory system tested by an independent 2026 review](https://genfindr.com/blog/pleasur-ai-review-2026).
- An [independent 2026 review highlighted this as its strongest feature](https://genfindr.com/blog/pleasur-ai-review-2026), noting it holds onto details from past conversations and brings them back natu...

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 25
- Linked: 0 (0.0%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- Across the wider companion category, Nomi and Replika lead on raw long-term recall.
- Replika.
- That's where Pleasur.AI is built to win.
- Most apps run on a context window that resets when the session ends.
- Nomi and Replika are the broad-category leaders.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
