# Editorial principles for visual decisions

> The visual taxonomy in `visual-types.md` tells you *what* kinds of visuals exist. This file tells you *whether to add one at all* — using the same editorial principles that govern the prose.
>
> Read this BEFORE assigning a `Visual:` type to any section. Most sections should not have a visual. The default is `none`.

The core principle is the same as for prose: **every element earns its place**. A visual is an element. If it doesn't make the section more useful for the reader, cut it.

## Ryan's principles, applied to visuals

### 1. BLUF — Bottom Line Up Front

The opening sentence of every section is the most important sentence. A visual that delays the answer is worse than no visual.

- ✅ Visual *after* the BLUF, supporting evidence the reader is now ready to absorb.
- ❌ Visual at the top of the section as decoration (banner image, "hero" graphic).
- ❌ Visual that requires reader explanation before they can read the BLUF.

### 2. Show with examples (not abstract claims)

Concrete beats abstract. A screenshot of the actual UI is concrete; a stylized illustration of "an AI companion" is abstract decoration.

- ✅ `screenshot` — showing the brand product doing the exact thing the section discusses.
- ✅ `chart` — showing real, sourced numbers from the research dossier.
- ✅ `external` screenshot — showing a real Reddit thread or competitor claim being discussed.
- ❌ `image` — generic "lifestyle" / "mood" imagery that says nothing specific.

A good test: would removing this visual leave the reader with less concrete information? If no, cut.

### 3. Demonstrate; don't sell

When the section mentions a brand product, show it working — don't decorate around it.

- ✅ `screenshot` of the actual feature being used (not the marketing page).
- ✅ `action-shot` when the "feature being used" requires interaction — a chat with a response visible, settings with toggles flipped, a wizard mid-flow. Static screenshots can't show these states; action-shots can.
- ❌ `image` of a "happy user" or "abstract concept of the product."
- ❌ Hero shot of a logo. Logos do not earn placement.

### 4. Inverted pyramid (most important info first)

A reader who skims only the intro + first sentence of each H2 should still get the gist. Visuals that *only* make sense after deep reading hurt that.

- ✅ `chart` with a clear title that conveys the takeaway in one glance.
- ✅ `table` placed where the comparison adds skim-able structure.
- ❌ Complex diagram that requires reading the surrounding paragraphs to understand.

### 5. MECE (no overlap, no gaps)

Sections don't repeat each other. Visuals shouldn't either.

- One anchor visual per section, max.
- If the same `screenshot` would fit two sections, the sections probably overlap — fix the outline first.
- Don't use both a chart AND a table to show the same data; pick one.

### 6. Cite everything

If a visual makes a numerical claim, the data behind it has to be sourced.

- ✅ `chart` whose data field references the research dossier or a named source.
- ❌ `chart` with made-up numbers. (`render_chart.py` will not invent data — if data is missing, the chart fails and routes to manual capture.)

### 7. Reader's time is precious

A visual that loads slowly, requires explanation, or doesn't render on mobile costs the reader more than it gives. Captured PNGs at appropriate resolution are fine; embedded videos are heavy and should be reserved for sections where motion is the point.

- ✅ `video` only when the demo genuinely cannot be conveyed as a series of screenshots.
- ✅ `gif` only for short, looping interactions where motion is the meaning.
- ❌ Auto-playing video in the intro.

## Decision sequence (apply per H2)

For each H2 section, work through these questions in order. The first "yes" wins.

1. **Does this section walk through a brand product UI at a static URL** (the wanted state is visible on first load, possibly after one age-gate click)?
   → `screenshot` (target = product slug from brand-config; what = the specific UI element)

2. **Does this section need a UI state that only exists after multi-step interaction** — a chat in mid-flow, a wizard past step 1, settings with toggles flipped, a page behind aggressive bot protection where `screenshot` fails?
   → `action-shot` (goal = full natural-language sequence; url = starting URL; what = caption)

3. **Does this section compare N things across M dimensions?**
   → `table` (write inline as markdown; no asset file)

4. **Does this section present quantitative data with trend / proportion / distribution?**
   → `chart` (data must reference the research dossier or be sourced inline)

5. **Does this section reference a third-party artifact** (Reddit thread, tweet, competitor screenshot)?
   → `external` (manual capture; provide URL) — or `action-shot` if the page is reachable and ToS allows automated capture

6. **Does this section explain a multi-step interaction that text struggles with?**
   → `gif` (manual; flagged for editor)

7. **Does this section embed an existing demo video that motion is essential to?**
   → `video` (manual; provide embed URL)

8. **Would an aesthetic / mood / lifestyle illustration add specific value, SFW?**
   This is the bar most "yes" answers fail. The illustration must convey something the prose can't. If it's decorative, the answer is no.
   → `image` if and only if the answer is yes (Replicate-generated, default `safety=sfw`)

9. **Otherwise:** `none`. Argue with prose.

### `screenshot` vs `action-shot` — quick test

Ask: **"Could a developer paste a single URL into a fresh browser and see this state immediately?"**

- Yes → `screenshot` (patchright headless, free, fast)
- No (state requires clicks/typing/waiting/login chain) → `action-shot` (handed to `/capture-visuals`, which drives the VPS's always-on Chrome via the Claude in Chrome MCP — also free, just slower because it's a real browser doing real actions)

When in doubt between the two, prefer `screenshot` first — it's faster. The dispatcher will surface the failure cleanly if the page truly needs interaction, and you can upgrade the placeholder to `action-shot` then.

## Test for an existing `Visual:` assignment

Before saving the outline, for every section that has a non-`none` Visual, ask:

- **Earns its place?** If the visual is removed, does the reader lose specific, concrete information? If no → change to `none`.
- **First-sentence-readable section?** Would the reader understand the section's BLUF without the visual? (They should — the visual *supports* the BLUF, doesn't *replace* it.) If the section depends on the visual to make sense, the BLUF is wrong.
- **Concrete?** Does it show a real thing (UI, data, source) — not a stylized abstraction?
- **MECE?** Does any other section have the same visual? If yes → consolidate.

## Section types that almost always default to `none`

- Foundational explainers ("What is X")
- Argumentative / persuasive sections
- Conclusion / recap sections
- Transitional sections
- "Why this matters" sections
- "Common mistakes" lists (unless one of the mistakes specifically benefits from a screenshot)

A section can absolutely succeed with prose alone. The fact that AI loves to suggest visuals everywhere is a known failure mode of AI-written content. The reader notices.

## When in doubt

Default to `none`. A section without a visual but with great prose beats a section with a generic visual every time.
