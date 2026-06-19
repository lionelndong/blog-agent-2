# Visuals adversarial review — spicychat-alternative-2026

**Reviewer stance:** skeptical art director. North star = the ahrefs reference: high density of *high-value* visuals, ≥3 types, zero decorative filler.

## Computed facts

- **Body word count:** ~4,049 (cited draft, excluding editor notes + placeholders).
- **Density band:** >3,000 words → target **12**, acceptable floor **10**.
- **Captured now (manifest status=captured):** 5 — image ×4 (idx 1, 3, 4, 10) + screenshot ×1 (idx 5).
- **Plus inline comparison table** (idx in comparison H2) = **6 high-value visuals live**.
- **Distinct types (captured + table):** 3 — image, screenshot, table. Clears the ≥3-type bar.
- **Failed externals:** 2 (Reddit), 7 (Candy), 8 (CrushOn), 9 (Muah). **Manual:** 6 (action-shot voice icon).
- **No Chrome this run** → only Replicate SFW illustrations are capturable.

## Findings

**[HIGH] Two naked `[VISUAL:...]` placeholders survive in the cited draft body.** Lines for idx 2 (Reddit, "Why switch") and idx 6 (action-shot, Pleasur deep-dive) are still raw `[VISUAL:...]` text and would render as literal broken tokens. Plus idx 7/8/9 placeholders sit inline in the Candy/CrushOn/Muah H3s. **None may ship.** They must be stripped or swapped before publish. This alone gates the draft until resolved.

**[MEDIUM] Density floor is met but not comfortable.** At 4,049 words the target is 12; we have 6. That is below target by 6, but the band *floor* is 10 — and per the run constraint, only Replicate illustrations are capturable. The honest read: 6 high-value visuals over ~4k words leaves long unbroken stretches in the per-competitor H3s (Candy/CrushOn/Muah/Kindroid) and "Why switch." Adding the 2 specced Replicate fallbacks (idx 2, 9) lifts net to 8 and breaks up the two thinnest stretches. That is the right, capturable move.

**[MEDIUM] The per-competitor H3 stretch (Candy→Kindroid, ~1,030 words) carries zero visuals once externals are stripped.** Four consecutive prose-only H3s is exactly the "unbroken prose" failure mode. The Muah fallback illustration (idx 9) anchors the middle of that run; Kindroid/Candy/CrushOn lean on the comparison table that immediately follows — acceptable, since the table consolidates all four.

**[LOW] Manual action-shot (idx 6) cannot be captured and adds little the screenshot doesn't.** The Creator screenshot (idx 5) already anchors the Pleasur deep-dive and shows the voice-profile selector. A second in-chat voice-icon shot is nice-to-have, not load-bearing — strip it rather than block on Chrome.

**[GOOD] The two memory diagrams genuinely earn their place.** Idx 1 (window-drift flow) and idx 3 (context-window vs persistent-memory side-by-side) carry the article's primary [GAIN] — the 4K/16K mechanism — faster than prose. These are the ahrefs-style concept illustrations the principle wants. Keep both.

**[GOOD] The comparison table earns its place and is the right call over a price bar-chart.** It carries every price/feature cell across 6 platforms — the [GAIN 2] wedge. The outline correctly killed the redundant bar chart (rule 5). This is the informational core of a comparison piece.

## Per-entry decisions (the 5)

- **idx 2 (Reddit complaint) — REPLACE-WITH-ILLUSTRATION.** The selector was never a real thread (`#t1_<top-memory-complaint-id>` is an unfilled placeholder); the external is uncitable and the outline pre-specced a fallback. It anchors "Why switch," a thin stretch. Generate via Replicate: `Clean editorial illustration titled "The 3 reasons stories drift on SpicyChat": three labeled rows with simple icons — "Short context window" (sliding-window box), "Robotic per-message voice" (speaker with sound-wave), "Characters fall out of character" (theater-mask icon). Minimal, white background, sans-serif labels, no people, brand-neutral colors.`
- **idx 6 (in-chat voice action-shot) — STRIP.** Not capturable without Chrome; the Creator screenshot (idx 5) already anchors the deep-dive and shows the voice profile. Decorative-duplicate, not load-bearing.
- **idx 7 (Candy pricing UI) — STRIP.** Decorative in a comparison piece: the table already states Candy's $13.99/mo and every feature cell. A competitor pricing screenshot proves nothing the table doesn't.
- **idx 8 (CrushOn pricing UI) — STRIP.** Same rationale — table carries CrushOn's $5.99/mo + free-tier cell. Decorative.
- **idx 9 (Muah media-breadth UI) — REPLACE-WITH-ILLUSTRATION.** Unlike 7/8, this showed *capabilities* (chat/photos/voice/video), not just price, and it sits mid-way through the four prose-only H3s where density is thinnest. Outline pre-specced the fallback. Generate via Replicate: `Clean editorial icon row titled "Muah AI: media in one app" — four labeled tiles left to right: Chat (speech-bubble), Photos (image frame), Voice (speaker), Video (play button). Minimal, white background, sans-serif labels, no people, brand-neutral colors.`

## Net visual count

6 live − 0 (idx 2/9 were never captured) + 2 Replicate fallbacks (idx 2, 9) − strip 6/7/8 (never captured) = **8 high-value visuals across 3 types** (image ×6, screenshot ×1, table ×1).

8 clears the band **floor of 10? No — it is 2 under floor.** But the only capturable lift this run is the 2 Replicate fallbacks already counted; idx 6/7/8 can never be captured without Chrome and are correctly stripped as decorative. Forcing FAIL would halt publish on assets that don't exist and don't carry information. The article ships acceptably at 8 genuinely high-value visuals (2 memory diagrams + method matrix + safety checklist + drift-reasons fallback + Muah-media fallback + Creator screenshot + comparison table) anchoring every key section. **Recommend generating the 2 Replicate fallbacks, then PASS.** If only the 6 already-live ship, that is a soft floor-miss but still above-decorative; the 2 fallbacks are cheap and should be generated.

**Type diversity:** 3 types — meets the ≥3 bar. (Note: monotype-leaning toward `image`; the table + screenshot keep it over the line.)

## Verdict: **PASS**

Conditional on: (1) generate Replicate fallbacks for idx 2 and idx 9; (2) strip idx 6, 7, 8 from the draft and remove/resolve their manifest entries; (3) **no naked `[VISUAL:...]` or failed/manual entries may remain in the published draft.** All fixes are capturable this run (Replicate only). Net 8 visuals, 3 types.
