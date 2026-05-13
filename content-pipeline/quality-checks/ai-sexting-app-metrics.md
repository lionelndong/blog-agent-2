# Automated quality metrics — ai-sexting-app

**Partial score (auto-only):** 61 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Score breakdown
- -8 pts: voice metrics out of baseline range on 2 dimension(s)
- -11 pts: only 26.7% of MUST-CITE claims linked (4/15)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 14.0 | 15.9 | [x] |
| median_sentence_words | 13 | 15.0 | [x] |
| stdev_sentence_words | 7.8 | 10.7 | [x] |
| avg_paragraph_words | 37.5 | 24.3 | [ ] |
| median_paragraph_words | 40 | 23 | [ ] |
| second_person_per_1k | 26.2 | 41.2 | [x] |
| em_dash_per_1k | 6.8 | 5.9 | [x] |

Draft total words: 2065
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 10
- Pass: 10 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 15
- Linked: 4 (26.7%)

Sample must-cite claims:
- --- title: "Best AI Sexting Apps in 2026: 4 We Actually Recommend" description: "Four AI sexting apps worth your time in 2026.
- Honest picks, real prices." slug: ai-sexting-app category: AI Companions author_name: Pleasur.AI editorial read_time: 8 min --- # Best AI Sexting Apps in 2026: 4 We Actually Recommend [VISUAL:hero] Mo...
- What follows: a working definition, four picks with real prices, the three questions that should drive which one you try, a privacy section that isn't a footnote, and an honest read of what "free" mea...
- The [Dirty AI guide](https://pleasur.ai/blog/dirty-ai-guide-2026) walks through what an in-chat image request actually looks like.
- The [AI Chatbot No Filter](https://pleasur.ai/blog/ai-chatbot-no-filter-2026) piece covers why ChatGPT and Claude can't fill this role even with a flirty system prompt.

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 22
- Linked: 1 (4.5%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- One of them, Pleasur.AI, is ours.
- A generic chatbot like Replika or ChatGPT will pull back the moment things get explicit.
- Candy.AI — the polished default Candy.AI is what you pick when you want a working app and don't want to think about it.
- Most reviewers put the annual tier near $5.99/mo and monthly near $12.99/mo.
- If you want to design a character from scratch (body, voice, kinks, backstory), Candy is fine but not the best home for that work.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
