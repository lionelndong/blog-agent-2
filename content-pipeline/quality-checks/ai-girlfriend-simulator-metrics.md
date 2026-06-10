# Automated quality metrics — ai-girlfriend-simulator

**Partial score (auto-only):** 60 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Score breakdown
- -13 pts: voice metrics out of baseline range on 3 dimension(s)
- -7 pts: only 50.0% of MUST-CITE claims linked (1/2)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 17.0 | 15.9 | [x] |
| median_sentence_words | 14 | 15.0 | [x] |
| stdev_sentence_words | 11.5 | 10.7 | [x] |
| avg_paragraph_words | 36.6 | 24.3 | [ ] |
| median_paragraph_words | 36.0 | 23 | [ ] |
| second_person_per_1k | 25.3 | 41.2 | [x] |
| em_dash_per_1k | 0.0 | 5.9 | [ ] |

Draft total words: 2810
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 13
- Pass: 13 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 2
- Linked: 1 (50.0%)

Sample must-cite claims:
- Our May 25, 2026 research snapshot captured 3,600 US average monthly searches for "ai girlfriend simulator" on 2026-05-25, with product pages, app listings, games, video, People Also Ask, perspectives...
- [VISUAL:type=chart;data=PLE-153 observed SERP surfaces for ai girlfriend simulator on 2026-05-25;style=bar;title=SERP surface mix for AI girlfriend simulator searches] That mix tells you what the term...

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 3
- Linked: 0 (0.0%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- It may be a directory listing many products you still have to vet.
- The trust checks matter most before you share personal details.
- Bullets under do not say: best, free, safer, private, unrestricted, most realistic, therapy replacement.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.

## Visual + dedication redo (board Addendum 3, 2026-06-10)

- query/page: `pleasur.ai/blog/ai-girlfriend-simulator` (target kw "ai girlfriend simulator")
- baseline metric: live HTTP 200, H1 exact, 14 `<img>` tags; meta description = intro line (fixed from leaked hero alt). Visual quality bar: design-agency (D5) — met.
- source: `auto_publish_check.py` (BLOG_PUBLIC_BASE_URL=pleasur.ai) + direct curl of media URLs (hero + table-card HTTP 200); Strapi PUT 200 documentId clym73j0nrwsik3taapf5xki publishedAt 2026-06-10T02:37:17Z
- observed date: 2026-06-10
- gap (closed): prior images were gibberish-text generative infographics; article had no hero.
- recommendation (done): hero + 3 icon-driven diagrams via visual-prompt-craft 9-part prompts (zero gibberish, all labels legible); 5 tables → matplotlib table-cards; dedication v2 score 88.
- impact tier: Medium (CTR/engagement + answer-engine legibility; not a ranking-position change yet — track in weekly GSC report).
- owner: EO.
