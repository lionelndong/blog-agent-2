# QUARANTINE (do-not-produce): sexting-ai — keyword cannibalization

**Status:** Excluded from production. NOT a quality failure — a cannibalization exclusion.
**Date:** 2026-06-10
**Owner:** EO
**Rule applied:** cannibalization / topical-authority override (PLE-1371 run procedure step 1; PIPELINE.md "Keyword cannibalization" lens).

## Why excluded
"sexting ai" (slug `sexting-ai`, vol 33,100, KD 4, informational, cluster adult-nsfw-interaction)
is a word-order variant of **"ai sexting"** (slug `ai-sexting`), which was **published live
2026-06-10** (https://pleasur.ai/blog/ai-sexting, Strapi doc g0ktv85eeosy1ddocogy8yxb, quality 91).

Google resolves "ai sexting" and "sexting ai" to the **same query intent** (same SERP, same
informational intent, identical volume). Producing a second article would split authority across
two near-duplicate pages competing for one intent — textbook cannibalization, diluting the
ranking of the page we just shipped.

## Correct handling (no new article)
- The live `ai-sexting` article is the single canonical page for this intent cluster.
- Capture "sexting ai" demand by **targeting it as a secondary keyword within `ai-sexting`**
  (H2/FAQ phrasing using both word orders) — handle on the next `ai-sexting` update-pipeline pass,
  NOT as a separate publish.
- If a standalone "sexting ai" page is ever reconsidered, it must 301/canonical to `ai-sexting`,
  which is a CTO site-side change — do not publish a competing page.

## Effect
This marker removes `sexting-ai` from `auto_keyword_selector.py` candidates (it excludes any slug
present in `9-needs-review/`). Next cadence run advances to the next distinct-cluster target.
