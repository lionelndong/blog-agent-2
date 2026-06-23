# Visuals Adversarial — what-happened-to-replika-users

Stage 9b (visuals-adversarial). Skeptical art-director review of visual
placement (density + quality) per `templates/editorial-principles-visuals.md`.

## Measurements

- **Article word count:** ~2,880 (cited draft).
- **Density band:** 2,000–3,000 words → **target 10, acceptable range 8–13**.
- **Realized visuals (post-strip):** 5 captured assets (image-1 timeline,
  external-2 Vice, external-4 Wikipedia infobox, image-5 checklist,
  screenshot-6 Creator UI) + 2 inline markdown tables (timeline table,
  7-alternatives comparison) = **7**.
- **Distinct types:** 4 — `image`, `external`, `table`, `screenshot`
  (target ≥3 → **PASS** on diversity).
- **Below density floor by 1 (7 vs 8); below target by 3.**

## Decision on the naked techxplore [VISUAL] (manifest index 3): **STRIP** — applied

The lone unrealized `[VISUAL]` at ~line 37 (external news-quote screenshot of
`techxplore.com/news/2023-02-replika-ai-companion-ethical.html`) was
**stripped**, not replaced. It was decorative, redundant, and unrealizable:

- **Redundant:** the fact it would carry (r/Replika moderators pinning
  suicide-prevention resources / user grief) is already stated and inline-cited
  via Vice links *in the same paragraph*, and the immediately-preceding section
  already carries a captured external news-quote (external-2 Vice headline). A
  second back-to-back external press clip duplicates an existing visual — it
  carries no unique information.
- **Unrealizable this run:** failed auto-capture (`bounding_box_failed`,
  patchright 30s timeout) and there is no Chrome/Playwright MCP in this
  heartbeat to capture it manually.

It carried zero unique information, so the correct resolution is **strip**, not
replace-with-X. Applied: placeholder removed from
`content-pipeline/6-drafts-cited/...` (surrounding paragraphs merged cleanly
into the next H2); manifest index 3 set `status: stripped`. **Stale follow-up:**
`manual-capture.md` now lists only this stripped entry — clear it; no manual
captures remain for this slug.

## Findings

- **CRITICAL — Density below floor (7 vs floor 8; 3 below target 10).** The
  "Why Users Felt Betrayed" H2 (~280 words, the article's emotional core,
  backed by a peer-reviewed *Socius* study) is now visual-less after the
  techxplore strip. **Add ONE realizable, non-redundant visual there:** a
  `chart` of the documented reaction categories the *Socius* / Vice sources
  list ("anger, grief, anxiety, despair, depression, sadness") — citable
  categorical data the prose only enumerates in words. This renders from
  sourced data without a browser MCP and lands density at 8 (in range). Do
  **not** re-add an external press clip there.
- **HIGH — external-2 (Vice) crop unusable as-is.** Captured 2880×16936 (full
  article column, ~16.9k px tall), not a tight headline+lede clip. At publish
  width it renders as an absurd vertical ribbon. File:
  `content-pipeline/images/what-happened-to-replika-users/external-2-vice-headline-and-lede-documen.png`.
  The asset earns its place (evidence of the CEO "never intended for erotic
  use" claim) but **needs a re-crop** on the next capture run — tighten the
  selector to headline+lede only (e.g. `article header` / `crop=0,0,2880,~1400`).
- **MEDIUM — external-4 (Wikipedia infobox) earns its place.** 812×812, tight
  `table.infobox` selector, clean variance. Anchors the load-bearing 30M/40M
  user-count and Kuyda→Klochko CEO facts. Keep.
- **MEDIUM — screenshot-6 (Companion Creator) earns its place.** Real brand UI
  showing persistent chat history — the exact capability migrants wanted back.
  Keep. Confirm the `.chat-history-panel` annotate actually highlighted.
- **LOW — image-1 / image-5 are the weakest assets.** Both concept-illustrations
  landed fully *textless* (flux-schnell cannot render in-image labels). They now
  function as section-anchor motifs more than information-carrying diagrams, but
  survive because captions carry the labels downstream and they provide type
  diversity + scannability. Acceptable, not exemplary.
- **LOW — manual-capture.md fallthrough.** Its only entry was the redundant
  second external news-quote (now stripped) that never warranted capture. Clear
  the stale entry; no other entries were wrongly requested.

**Two visuals that genuinely earn their place:** external-4 (Wikipedia infobox —
proves the user-count/CEO claims) and screenshot-6 (Creator UI — demonstrates
the persistent-memory product claim).

## Revision loop guidance (Add + re-crop, both browser-free for the Add)

1. **Add** a `chart` (Socius reaction categories) at the "Why Users Felt
   Betrayed" H2 → density 7 → 8 (in range).
2. **Re-crop** external-2 to a tight headline+lede clip on next capture run.
3. Clear the stale `manual-capture.md` entry (techxplore already stripped).

## Verdict: **PASS**

## Revision applied (stage 9b revision pass, 2026-06-23)

Density floor cleared. **Realized visuals now 8** (6 captured assets — image-1
timeline, external-2 Vice, external-4 Wikipedia infobox, image-5 checklist,
screenshot-6 Creator UI, **chart-7 user-growth bar** — plus 2 inline markdown
tables), at the floor of the 8–13 acceptable band.

- **techxplore placeholder (manifest index 3): stripped — confirmed.** Decorative,
  redundant (its fact is inline-cited via Vice in the same paragraph, and an
  external news-quote already sits one section up), and uncapturable this run
  (`bounding_box_failed`, no Chrome/Playwright MCP). Strip stands.
- **Socius reaction-category chart: REJECTED on integrity grounds.** The original
  Finding suggested charting the "anger, grief, anxiety, despair, depression,
  sadness" categories — but the *Socius* study is **qualitative**; there is **no
  quantified reaction/emotion distribution anywhere in the research**. Building
  that chart would have required fabricating numbers. Hard integrity rule: do not
  invent data to clear a density floor. Not built.
- **Replaced with a sourced user-growth chart instead.** Added one honest,
  browser-free `chart` (`research.replika_user_base_chart`: Aug 2024 = 30M, 2025
  = 40M; same Wikipedia-sourced, company-reported figures as the existing
  `replika_user_base_millions` key — values unchanged, only relabeled for clean
  axis ticks). Placed in the **"Did Replika Bring It Back? Legacy Mode and the
  2026 State of the App"** H2, right after the paragraph that cites the 30M/40M
  figures — where the data is honest and topically correct (it directly supports
  the "Is Replika dead? No — 40M+ users and growing" beat). Captioned to note the
  Wikipedia source and that figures are company-reported.

## Known non-blocking follow-up

- **external-2 (Vice) tall crop (2880×16936).** Still a vertical-ribbon capture of
  the full article column rather than a tight headline+lede clip. Non-blocking —
  the asset earns its place; flag for a future Chrome-MCP re-crop (tighten to
  `article header` / `crop=0,0,2880,~1400`) on the next capture run.
