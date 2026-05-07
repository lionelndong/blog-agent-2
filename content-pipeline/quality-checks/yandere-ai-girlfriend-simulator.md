# Quality Check: yandere-ai-girlfriend-simulator

## Verdict: **PASS**

**Combined score: 91 / 100**
- Automated metrics: 80 / 80
- Adversarial review: 11 / 20

---

## Automated metrics summary

| Metric | Draft | Baseline | In range |
|---|---|---|---|
| avg_sentence_words | 17.9 | 15.9 | ✓ |
| median_sentence_words | 15 | 15.0 | ✓ |
| stdev_sentence_words | 13.9 | 10.7 | ✓ |
| avg_paragraph_words | 31.1 | 24.3 | ✓ |
| median_paragraph_words | 33.5 | 23 | ✓ |
| second_person_per_1k | 28.3 | 41.2 | ✓ |
| em_dash_per_1k | 5.4 | 5.9 | ✓ |

- **Word count:** 1,840 (target 1,500–2,500) ✓
- **Forbidden phrases:** None found ✓
- **BLUF compliance:** 6/6 sections pass ✓
- **Must-cite density:** 3/3 linked (100%) ✓

---

## Adversarial critique

**[HIGH — -4 pts] Parasocial citation is a [link] placeholder without a real source identified**
"Researchers studying parasocial relationships... have noted..." makes a specific empirical claim but is backed only by a `[link]` placeholder. Verify-claims needs a real academic paper or named researcher here. The claim is currently unsourced. If no good source is available, the sentence should be reframed as editorial interpretation ("The appeal matches what's well-documented in parasocial relationship research") without the citation implication.

**[HIGH — -3 pts] "970+ comments" and TikTok claim need source anchoring**
The itch.io comment count (970+) is stated as a fact with a `[link]` placeholder pointing to the itch.io game page — this is fine and verify-claims will confirm it. The TikTok virality claim ("became a minor TikTok phenomenon") has no citation at all. Either source it (the Monsters Game article that covers TikTok spread) or reframe as "players shared clips widely, which drove search volume beyond the active player base."

**[MEDIUM — -2 pts] AI2U description slightly undersells the differentiation**
The section on AI2U is accurate but the BLUF doesn't fully answer the purchase decision. "Start with the free game" is practical advice but the article could note that AI2U has received recent updates and the roadmap shows active development — which matters for readers deciding whether $14.99 is worth it for an actively-maintained product vs. a 2023 demo.

**[LOW — no deduction] Competitor section is appropriately restrained**
The apps section avoids becoming a competitor comparison — MyAnima and Candy AI each get one sentence. The table is useful and not overselling. Satisfies the "1 competitor comparison per week" constraint.

**[LOW — no deduction] Product mention is natural and well-placed**
The Pleasur.AI mention in the companion apps section is well-placed, not intrusive, and the walkthrough ("write it in directly: 'obsessive devotion...'") is concrete and demonstrates rather than sells.

## What works

The dual-audience structure (game-seekers vs. companion-app users) is the article's biggest editorial strength and it's something no competitor article does. The framing in the intro ("these are not the same product") is both accurate and differentiated. The psychology section adds real depth without moralizing. Overall this reads like it was written by a human editor who knows the topic.

---

## Punch list

| Severity | Item |
|---|---|
| HIGH | Parasocial citation needs a real paper or reframe as editorial |
| HIGH | TikTok virality claim needs source or reframe |
| MEDIUM | AI2U section BLUF could be sharpened on purchase decision |

---

## Recommendation

**PASS — advance to verify-claims.** The HIGH items are citation issues that verify-claims is designed to resolve. They are not structural or voice problems. No content revision needed before verify-claims; the verify-claims stage should prioritize the parasocial citation and the TikTok claim.
