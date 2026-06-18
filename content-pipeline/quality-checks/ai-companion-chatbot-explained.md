# Quality check — ai-companion-chatbot-explained

## Verdict: **PASS** (90 / 100)

No blocking items. The article meets its brief (answer-first informational explainer, 600–900w band — final 888w) and is benchmark-appropriate for the target intent: a concise, answer-first definition page built to win AI-Overview / AI-Mode citations and the "AI Chatbots & GPT Technology" topic-cluster gap, not a deep SERP listicle. Two minor style notes logged below; neither blocks publish.

---

## Benchmark / beat spec (from PLE-2732 brief)

This is a GEO/AEO citation play, not a competitive ranking listicle. The binding beat spec is the brief itself:
- Answer-first opening, 40–60 words, direct definition + companion positioning → **58 words, met**
- Differentiator section (memory / emotional context / personalization) → **met (3 labelled sub-points)**
- FAQ/Q&A section, ≥3 (brief asks 5) → **5 Q&As, FAQPage JSON-LD auto-emits on blog template**
- ≥1 cited stat → **4 external citations** (Reuters ChatGPT 100M; IBM chatbot definition; Pinecone vector memory; Wikipedia Replika 60% romantic)
- CTA to /create → **met (2 placements)**

## Metrics summary

| Dimension | Weight | Score | Notes |
|---|---|---|---|
| Forbidden phrases / AI-tells | 20 | 20 | Zero forbidden-phrase hits. Em-dashes reduced from 13→2 in v2 (both meaningful asides). |
| Voice vs `examples/` baseline | 25 | 24 | Short/medium sentences, second person, conversational. Tracks the explainer baseline (`what-is-an-ai-girlfriend`). |
| BLUF compliance (openers) | 20 | 20 | 4/4 H2 sections open with a direct answer; every FAQ answers in sentence one. |
| Claim density + linkability | 15 | 15 | 4 external cited stats + 3 internal cluster links across 888w. Zero naked `[link]` placeholders. |
| Adversarial read | 20 | 11 | See below. No structural defects; minor metaphor/citation-reuse nits only. |
| **Total** | **100** | **90** | **PASS (≥85 publish floor)** |

## Adversarial read (skeptical editor)

- "different product wearing some of the same plumbing" — slightly loose metaphor; kept because it lands the tool-vs-character point fast. Non-blocking.
- The Replika 60% stat is reused from the sibling `what-is-an-ai-girlfriend` article. It's apt and correctly attributed here (paying-subscriber romantic-relationship figure), so reuse is fine, not duplication.
- Would the current top SERP/AIO answer beat this? The page answers the definitional query directly in the first 58 words, disambiguates companion vs. generic chatbot explicitly (the exact cluster gap), and is schema-eligible. For the citation objective it is competitive. No regeneration needed.

## Constraint-violation audit

- **Compliance (adult boundaries):** PASS — 18+ framing throughout; no "no filter / anything goes" absolutism; no safety guarantee ("No platform can promise perfect safety"); no real-person likeness (no imagery); product claims limited to `live` products (AI Companion Creator).
- **Internal-stack scrub:** PASS — no internal tool/vendor names in body, links, or metadata.
- **Pricing claim:** removed in v2 (unverified "free to start" struck) — no price/tier asserted.
- **Naked link placeholders:** none.

## Recommendation
Proceed to `/format-for-publish --auto-publish`. Post-publish: assert HTTP 200 + correct H1; add ledger row; notify GEO Lead for the 2-week citation re-audit.
