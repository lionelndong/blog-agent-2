# Automated quality metrics — ai-porn

**Partial score (auto-only):** 59 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Score breakdown
- -17 pts: voice metrics out of baseline range on 4 dimension(s)
- -4 pts: only 76.2% of MUST-CITE claims linked (16/21)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 19.5 | 15.9 | [x] |
| median_sentence_words | 17.5 | 15.0 | [x] |
| stdev_sentence_words | 14.5 | 10.7 | [x] |
| avg_paragraph_words | 52.5 | 24.3 | [ ] |
| median_paragraph_words | 57 | 23 | [ ] |
| second_person_per_1k | 13.7 | 41.2 | [ ] |
| em_dash_per_1k | 1.8 | 5.9 | [ ] |

Draft total words: 2847
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 7
- Pass: 7 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 21
- Linked: 16 (76.2%)

Sample must-cite claims:
- --- ## What "AI porn" actually means in 2026 AI porn is adult content (images, video, chat, or voice) generated or co-created by a machine learning model on demand.
- Ahrefs puts "ai porn" at 733,000 US searches a month, 83% on mobile, with a click-per-search of 0.83.
- Stable Diffusion popularized the approach in 2022 [link], and the open-source weights are why the entire adult-AI category exists.
- Quality jumped enough between 2024 and 2026 that "ai porn videos" is now a 19,000-per-month search [link].
- Deepfake porn videos in 2023 came in 464% higher than 2022 [link], a useful proxy for the quality leap: the same diffusion advances that made consensual platforms watchable also made the harm side fas...

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 20
- Linked: 0 (0.0%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- It's also not the version most people typing the phrase into Google are looking for.
- Most ranking listicles cover one or two and pretend that's the whole space.
- The mismatch is why none of the top-ten Google results satisfy the searcher.
- The consent split is the only split that matters.
- When the rest of this guide says AI porn, it means the first kind.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
