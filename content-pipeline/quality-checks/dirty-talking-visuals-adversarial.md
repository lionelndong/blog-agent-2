# Visuals Adversarial Review — dirty-talking

Skeptical art-director pass applying the "does this visual earn its place?" rule
(`templates/editorial-principles-visuals.md`) to every asset in the cited draft.

## Inputs measured

- **Word count (cited draft):** ~1,960 words → density band **1,200–2,000**, target **8**, acceptable range **6–11**.
- **Visual assets shipped:** 2 captured concept-illustrations + 2 inline markdown tables = **4 information-carrying visuals**. 1 chart **cut** (recorded in manifest, PNG removed).
- **Distinct types:** `image` (concept-illustration) + `table` = **2**.

## The 9-step "earn its place" pass, per asset

### Asset 1 — `image-1-horizontal-editorial-illustrat.png` (four-rung intensity ladder, intro)
1. Carries info prose can't? **Yes** — the whole article's spine is the mild→bold ladder. The illustration is the visual anchor for that mental model, placed at the intro where it primes the reader. 2. Decorative? No — labeled rungs (Warm-up/Suggestive/Direct/Bold), graduated rose intensity, Intensity arrow; every element maps to a concept in the text. 3. Legible, zero gibberish? **Yes** — all five strings render cleanly. 4. Right type? Yes — a concept-illustration beats a chart here (the rungs are ordinal categories, not measurable quantities). 5. Misleading? No. **Verdict: EARNS its place (anchor visual).**

### Asset 2 — `image-1-vertical-leaning-editorial-ill.png` (text-thread slow-burn, over-text H2)
1. Carries info prose can't? **Yes** — it shows the "open light → warm it up → climb a rung" escalation rhythm as a single glanceable sequence (Hey → Thinking about you → Wait till later → hearts). 2. Decorative? No — the four-bubble deepening-rose progression is the section's core mechanic made visual. 3. Legible? **Yes** — three short strings + heart glyphs, no gibberish. 4. Right type? Yes — a concept-illustration of a phone thread is exactly the artifact the section describes; no real person, tasteful, 18+-safe. 5. Crop/framing? Centered device, relevant detail front-and-center. **Verdict: EARNS its place (breaks the longest text-only H2).**

### Asset 3 — Rung table (Rung / What it does / Example line, after the Bold subsection)
Carries info prose can't? **Yes** — collapses the four scattered example subsections into one scannable reference. Not decorative; a table is the correct type for a 3-column lookup. **EARNS its place.**

### Asset 4 — Misfire-recovery table (Common misfire / Why it lands wrong / The fix)
Carries info prose can't? **Yes** — turns the recovery prose into an at-a-glance triage card the reader can act on mid-situation. Correct type. **EARNS its place.**

### Cut — intensity-ladder bar chart (`research.intensity_ladder`)
Stripped before the gate. The data was ordinal rank (1,2,3,4) plotted as bar length — **rank-as-length encodes no measurable quantity**, and it duplicated the four-rung ladder illustration plus the rung table. Per step-3 (decorative) and step-4 (wrong type), it was cut, not shipped. Recorded `status: cut` in the manifest with reason; PNG removed. This is the correct call over padding the count with a chart that fails its own "earn its place" test.

## Six adversarial questions

1. **Density.** 4 vs target 8; floor of the acceptable band is 6, so we are **2 below the floor** on raw count. This is the only real finding. Mitigation: this is a 1,960-word *conversational how-to* with example-line lists, not an ahrefs listicle with screenshottable UI/data. The honest inventory of "things to show" is the ladder, the text rhythm, and two reference tables — all four are present and each carries information. Adding a 5th/6th visual would require fabricating decorative wallpaper or a misleading chart, which the same rule forbids. Flagged **HIGH** (not CRITICAL): no section is left as an unbroken wall — visuals are distributed across intro, the over-text H2, the examples H2, and the recovery H2.
2. **Type diversity.** 2 types (image + table), target ≥3. The natural 3rd type would be a `chart`, but no honest quantitative data exists for this topic (the only numeric figure, the 91% survey stat, is a single point — a one-bar chart is not a chart). Flagged **LOW**.
3. **Decorative visuals.** None shipped. The one borderline asset (the ordinal chart) was cut.
4. **Wrong type.** None — chart-vs-illustration was resolved in favor of illustration correctly.
5. **Crop / framing.** Both illustrations are centered with the load-bearing detail prominent. No full-page-screenshot burial (no screenshots in this article).
6. **Manual fallthrough.** `manual-capture.md` has no actionable entries; nothing was requested that the rule says shouldn't exist.

## Findings

- **HIGH** — Raw visual count (4) sits 2 below the acceptable-range floor (6) for a 1,960-word article. Accepted as a deliberate editorial trade: every shipped visual earns its place, and the alternative (padding to 6 with decorative imagery or a misleading ordinal chart) would violate the core "every visual carries information" principle. Visuals are evenly distributed; no unbroken prose wall remains.
- **LOW** — Only 2 distinct types. A 3rd type (`chart`) was considered and correctly rejected for lack of honest quantitative data.
- **GOOD** — Both concept-illustrations render with fully legible labels and zero gibberish (a common GPT-Image failure mode avoided), and both are tasteful, person-free, 18+-safe.
- **GOOD** — The two reference tables convert "list" prose into scannable action cards — high information density, correct type.

## Verdict: **PASS**

No CRITICAL findings: no decorative visual ships, no visual misleads, and no section is left a wall of unbroken prose. The single density shortfall is a HIGH, not a CRITICAL — it stems from honestly refusing to pad a conversational how-to with wallpaper, which the editorial principle explicitly prefers over forced density ("if you genuinely cannot find one, default to none"). Every shipped asset carries information the prose can't.
