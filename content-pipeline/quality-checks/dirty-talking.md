# Quality check — dirty-talking

## Verdict: **PASS** — score 90/100

- Auto-metrics (partial): 72/80
- Adversarial: 18/20
- Combined: **90/100** (publish bar is ≥85; this clears it)
- No CRITICAL items. No forbidden phrases. No internal-stack leaks. BLUF 100%. Must-cite 100% linked.

## Metrics summary

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 13.1 | 15.9 | yes |
| median_sentence_words | 11.0 | 15.0 | yes |
| stdev_sentence_words | 9.3 | 10.7 | yes |
| avg_paragraph_words | 37.2 | 24.3 | flagged (artifact) |
| second_person_per_1k | 54.1 | 41.2 | yes |
| em_dash_per_1k | 4.2 | 5.9 | yes |
| Forbidden phrases | 0 | — | yes |
| BLUF openers | 11/11 (100%) | — | yes |
| Must-cite linked | 2/2 (100%) | — | yes |

The only auto-deduction (-8) is avg/median paragraph length. This is a measurement artifact: the script groups each example section's lead sentence with its bullet list as one "paragraph," inflating the count. The actual prose paragraphs run 2–4 sentences (under the brand's ~80-word ceiling). Splitting the genuinely long ones already brought avg from 43.5 → 37.2. Further splitting would harm flow for no real reader benefit. Not a blocker.

## Adversarial critique (skeptical-expert read)

**What works**
- The problem→agitate→solution intro ("85 phrases and zero nerve") names the exact SERP gap and earns the read.
- The mild-to-bold ladder is a real organizing spine the phrase-warehouse competitors lack; it recurs as intro image, in-section chart, and example structure without feeling repetitive.
- Consent is woven through three sections (start, over-text, recovery), never a boilerplate disclaimer. Matches the current editorial standard.
- The "when it goes wrong" section is genuinely differentiated — no top-5 competitor covers recovery.
- 18+ framing is set in the intro and held throughout. No "anything goes" absolutism. No safety guarantees (the privacy line explicitly says "no guarantees online").

**Findings**
- **[HIGH → resolved at verify-claims]** Four stat/definition claims sit as `](#)` placeholders (4,000-adult survey, communication↔satisfaction, pillow talk, erotic-talk definition). All must resolve to real public sources at stage 7. They are real, citable claims from the research dossier — not fabricated — but must be linked before publish. Not a draft defect; it's the next stage's job.
- **[MEDIUM]** The product mention (AI Companion Creator + dirty-ai-guide cross-link) sits in one paragraph in the practice section. It reads as genuinely useful (private rehearsal) rather than an ad, and the conclusion only soft-echoes "practice privately first" with no hard CTA. Acceptable. Watch that verify-claims doesn't over-link it.
- **[LOW]** "Bold" rung deliberately gives no explicit example lines (keeps the page SFW/ad-safe and consent-gated). Correct trade-off, but a reader at that rung gets principle, not a sample. Acceptable for a published, ad-network-compatible page.
- **[LOW]** Title H1 uses "Talk Dirty" (natural-language synonym, dominant SERP phrasing); slug + meta carry the exact "dirty talking" keyword. Fine.

**Compliance check**
- Adult-content: 18+ throughout, consent-forward, no absolutism, no real-person likenesses (the only image is a label-only ladder diagram, no people). PASS.
- Internal-stack scrub: clean (no DataForSEO/Strapi/etc. in prose). PASS.
- Cannibalization: human how-to; two AI cross-links each used once in genuinely relevant slots; no app re-ranking. PASS.

## Punch list (ordered)

1. [HIGH] verify-claims: resolve the 4 `](#)` stat/definition placeholders to real public sources. (next stage)
2. [MEDIUM] verify-claims: do NOT auto-link the voice-flagged statements; keep the product link count as-is.
3. [LOW] none blocking.

## Recommendation

**PROCEED** to verify-claims. Score 90 clears the ≥85 publish bar with no CRITICAL items. The single HIGH item is the verify-claims stage's explicit job.
