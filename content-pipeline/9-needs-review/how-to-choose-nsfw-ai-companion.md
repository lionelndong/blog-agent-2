# SKIP MARKER — how-to-choose-nsfw-ai-companion (slug-normalization duplicate)

**Status:** ALREADY PUBLISHED LIVE — do not re-write.
**Date:** marker added 2026-06-17 (PLE-2632)
**Why:** The queue keyword "how to choose an nsfw ai companion" normalizes to slug `how-to-choose-nsfw-ai-companion` (no "an"), but the article is already live at the canonical slug **how-to-choose-an-nsfw-ai-companion** (with "an"), published 2026-06-15 (Strapi id 1395, quality 86, verified HTTP 200 + correct H1). The auto_keyword_selector treats the de-"an" form as unwritten and keeps surfacing it (score 9.4).

**Action:** Skip from the cadence — re-writing it would create a cannibalizing near-duplicate against the live canonical page (one canonical page per intent cluster). This marker makes the selector advance to the next genuine candidate.

**Owner:** EO. No board/CTO action needed. (Deeper fix = slug-normalization in auto_keyword_selector; logged but not blocking.)
