# Automated quality metrics — ai-girlfriend-app-privacy-data-guide-2026

**Partial score (auto-only):** 63 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Score breakdown
- -8 pts: voice metrics out of baseline range on 2 dimension(s)
- -9 pts: only 40.9% of MUST-CITE claims linked (9/22)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 21.8 | 15.9 | [x] |
| median_sentence_words | 18 | 15.0 | [x] |
| stdev_sentence_words | 18.5 | 10.7 | [x] |
| avg_paragraph_words | 57.8 | 24.3 | [ ] |
| median_paragraph_words | 59.5 | 23 | [ ] |
| second_person_per_1k | 24.6 | 41.2 | [x] |
| em_dash_per_1k | 7.2 | 5.9 | [x] |

Draft total words: 2074
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 6
- Pass: 6 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 22
- Linked: 9 (40.9%)

Sample must-cite claims:
- --- slug: ai-girlfriend-app-privacy-data-guide-2026 title: "What Data Do AI Girlfriend Apps Really Collect?
- Privacy Guide 2026" meta_description: "AI companion apps collect your messages, images, IP, and more — often without clear disclosure.
- Here's what's really being collected, and how Pleasur.ai is different." target_keywords: - ai girlfriend privacy what data collected - ai companion data privacy 2026 - what data does replika collect -...
- Privacy Guide 2026 AI girlfriend apps typically collect your conversation messages, your photos and generated images, your IP address, your device identifiers, and in some cases your financial transac...
- A [2026 security audit of apps with more than 150 million combined installs](https://www.androidheadlines.com/2026/03/ai-girlfriend-apps-security-risk-2026-study.html) found that over half exposed int...

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 6
- Linked: 1 (16.7%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- These apps hold some of the most sensitive data you will ever type into a phone.
- In other words, these apps are designed to extract exactly the data that hurts most when it leaks.
- If an app fails most of these, treat it as a data risk.
- **What it does not do.** The [policy states it plainly](https://pleasur.ai/legal/privacy-policy): "We do not sell your personal information." It does not list third-party advertising partners among it...
- That is the standard many breached apps failed to meet.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
