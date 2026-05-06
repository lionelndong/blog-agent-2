# Automated quality metrics — what-is-an-ai-girlfriend

**Partial score (auto-only):** 78 / 80
(Adversarial review adds the remaining 20 pts; combined report at `quality-checks/{slug}.md`)

## Forbidden phrases
None found.

## Voice metrics vs baseline (examples/)

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 15.8 | 15.9 | [x] |
| median_sentence_words | 14.0 | 15.0 | [x] |
| stdev_sentence_words | 11.9 | 10.7 | [x] |
| avg_paragraph_words | 30.3 | 24.3 | [x] |
| median_paragraph_words | 29.0 | 23 | [x] |
| second_person_per_1k | 32.0 | 41.2 | [x] |
| em_dash_per_1k | 7.2 | 5.9 | [x] |

Draft total words: 2626
Baseline corpus: 5 files

## BLUF heuristic (section openers)
- Sections checked: 7
- Pass: 7 (100.0%)
- Fail: 0

## Claim density

**Must-cite** (numbers, percentages, named studies, year-anchored facts) — these gate the score:
- Count: 9
- Linked: 8 (88.9%)

Sample must-cite claims:
- A Plain-English Definition (2026) By mid-2023, more than a million people were paying Replika for a chatbot relationship, and roughly a third of them treated it as a romantic partner [link].
- It sits inside the broader [AI chatbot app](https://pleasur.ai/blog/ai-chatbot-app-guide-2026) category, but it's tuned for romance and adult interaction rather than productivity.
- Consumer apps typically store 5,000 to 20,000 characters of relevant facts per character — names, preferences, ongoing storylines, things you said matter — in a vector database the model pulls from on...
- First-audio latency on a good app sits around 150 to 400 milliseconds [link].
- Render time runs roughly 2 to 5 seconds [link].

**Voice-flagged** (population claims, superlatives, named brand mentions) — visibility only, NOT gated:
- Count: 21
- Linked: 0 (0.0%)

Sample voice-flagged statements (editor decides — over-citing damages voice):
- Most explainers on this topic do one of two things.
- The longer answer is more useful: the question worth your time isn't "what is it?" but "what's it actually like, and is it for you?" This piece walks you through the plain definition, the parts under ...
- It's a custom character built on a large language model that you can talk to, flirt with, and on most platforms, share an adult conversation with.
- ChatGPT writes you a marketing email.
- It's not the same as ChatGPT or Claude with a flirty system prompt.

## Notes for the adversarial reader (next step)
Run the adversarial sub-agent per the SKILL.md, then combine results into the main quality report.
