# Automated quality metrics — ai-sexting

**Partial score (auto-only):** 73 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Score breakdown
- -7 pts: only 50.0% of MUST-CITE claims linked (2/4)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 13.7 | 15.9 | [x] |
| median_sentence_words | 13.0 | 15.0 | [x] |
| stdev_sentence_words | 8.1 | 10.7 | [x] |
| avg_paragraph_words | 31.4 | 24.3 | [x] |
| median_paragraph_words | 28 | 23 | [x] |
| second_person_per_1k | 31.0 | 41.2 | [x] |
| em_dash_per_1k | 6.0 | 5.9 | [x] |

Draft total words: 2321
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 7
- Pass: 7 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 4
- Linked: 2 (50.0%)

Sample must-cite claims:
- The phrase "ai sexting" and its twin "sexting ai" pull tens of thousands of US searches a month [link], yet the pages that rank are conversion funnels and app lists.
- Replika, once a go-to, stripped out its erotic roleplay back in 2023 [link].
- All labels in a clean sans-serif, dark charcoal (#222222), sentence case, no other text anywhere.
- [VISUAL:type=screenshot;url=https://pleasur.ai/create;what=The public Companion Creator page, showing the character setup surface where you choose appearance and style;crop=0,0,1440,900] Want the full...

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 5
- Linked: 0 (0.0%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- Some apps let you generate images mid-chat, and a few are starting to add spoken replies and calls.
- Forum threads on the topic keep hitting the same wall: the mainstream bots they already use, like ChatGPT and Claude, are too locked down for this.
- Most platforms store your conversations.
- Most pages dodge it.
- Some platforms are starting to add spoken replies and calls inside the chat, so text-only won't be the only option for long.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
