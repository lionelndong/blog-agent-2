# Visuals adversarial review — what-do-ai-companion-coins-actually-cost (2026-06-16)

Stage 9b re-review after two concept illustrations were added to clear the prior density-floor CRITICAL.

## Computed

- **Article-body word count:** ~2,350 (cited draft; excludes alt-text blobs, table rows, editor-notes/citation appendix).
- **Density target:** 2,000–3,000 band → **target 10**, acceptable range **8–13**.
- **Image assets (status=captured, non-none):** **6** — all six verified against the manifest:
  1. intro coin→cost-cards hub diagram (`image-1-...-hu.png`)
  2. coin-vs-token concept illustration (`image-1-...-co.png`) — *newly added*
  3. in-chat coin-counter screenshot (`screenshot-2-...png`)
  4. monthly-vs-annual bar chart (`chart-3-...png`)
  5. transparent-vs-opaque billing-path illustration (`image-2-...-co.png`) — *newly added*
  6. 3-step calculator flow diagram (`image-4-...png`)
- **Inline tables (effective visuals, draft body):** **2** — coin-tier math (H2 #2) + transparent-vs-opaque (H2 #4).
- **Combined effective count:** **8** (6 assets + 2 tables).
- **Distinct type count:** **4** (image, screenshot, chart, table) — target ≥3 met.

## Findings

**HIGH — density at the floor of the acceptable range, not the target.** 8 effective visuals against a target of 10 (acceptable range 8–13). The prior FAIL was at 6 effective (4 assets + 2 tables); the two added concept illustrations (manifest #2, #5) lift it to 8, which lands inside the acceptable band. So the **prior density-floor CRITICAL is resolved** — no longer below target by 2+ AND inside the band. It stays HIGH because the article would read closer to the ahrefs reference at 9–10, and the cheapest remaining win is the trust tail (below).

**MEDIUM — H2 #6 "Trust and billing" is the one section that still deserves a visual and has none.** ~210 words of unbroken prose at `none`. An `external` capture clipping the pleasur.ai/pricing refund line, or a small 3-node `image` (trial → card required → renewal date), would add concrete info and push density toward target. Short section so not a CRITICAL, but it is the single best add if the loop wants 9.

**MEDIUM — distribution is lumpy.** H2 #2 carries three visuals (a concept image, the coin-counter screenshot, AND the tier table) while H2 #6 carries zero. Rebalancing one toward the trust tail would smooth the skim rhythm the editorial doc asks for (a visual every ~200–300 words).

**MEDIUM — image #2 (coin-vs-token) and image #5 (transparent-vs-opaque billing path) share the same visual grammar.** Both are split-canvas "confident itemized left vs hazy question-mark-bill right" pieces in the identical palette/layout. They are not MECE-duplicates — one contrasts coin-vs-token *units*, the other contrasts billing *paths*, and they sit in different H2s — so neither is decorative or a strip candidate. Flag only for the editor to confirm in the rendered preview that they don't read as the same idea twice.

**LOW — every captured asset earns its place; none decorative.** Removal test applied to each: the intro diagram encodes the exact 10/10/50/0 rates; the chart shows the annual-vs-monthly delta the prose only states in words; the screenshot proves the counter actually decrements; the flow diagram makes the 3-step recipe skimmable; both split illustrations carry the transparency thesis the prose argues. No strip candidates.

**LOW — no wrong-type assignments.** Bar chart correctly `chart` (quantitative delta), coin counter correctly `screenshot` (real brand UI), the four concept pieces correctly `image`/concept-illustration (abstract relationships, not real UI). No table-that-should-be-a-chart.

**LOW — crop/framing on the one captured screenshot.** `screenshot-2-in-chat-coin-balance-decrement.png` has `annotate=.coin-counter`, quality `stddev_normalized 0.18`, 2880×1800, 905KB — a healthy capture, not a blank/login wall. A single static frame can't literally show a 10→0 decrement, so the editor should confirm the annotate ring lands on the counter value and the crop foregrounds it; otherwise the `what=` slightly overpromises.

**LOW — manual-capture fallthrough clean.** `manual-capture.md` reads "No manual visuals required." All six assets captured automatically; nothing wrongly routed to manual. No fallthrough to flag.

### Visuals that genuinely earn their place (the good)
- **Intro coin→cost-cards diagram (#1):** answers "what does a coin cost" in one glance with the exact 10/10/50/0 strings — textbook concept-illustration, the ahrefs-reference use.
- **In-chat coin-counter screenshot (#3):** proves the metering claim with real product UI; the "watch the balance move" beat would be an unsupported assertion without it.
- **Monthly-vs-annual bar chart (#4):** anchors the annual-savings delta in sourced first-party numbers — a chart where prose alone would leave the reader doing arithmetic.

## Verdict: **PASS**
