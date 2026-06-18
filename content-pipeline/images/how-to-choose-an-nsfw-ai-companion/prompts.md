# Structured image prompts — how-to-choose-an-nsfw-ai-companion (density revision pass)

Built per `.claude/skills/visual-prompt-craft/SKILL.md` (9-part anatomy). All four below are
`type=image;sub=concept-illustration|diagram|comparison;style=illustration;safety=sfw`. SFW diagrams
for an 18+ article: NO people, NO explicit imagery, clean editorial vector style, white background,
sans-serif labels, brand-neutral palette.

Shared style spine (every prompt): Clean modern editorial illustration for a premium tech-lifestyle
blog. Flat vector with subtle depth, generous whitespace, sans-serif labels (Inter/Helvetica
archetype), white (#FFFFFF) background, soft cast shadows. Brand-neutral palette: ink #1A1A2E,
slate #4A5568, calm blue #3B82F6, green #16A34A, amber #F59E0B, red #DC2626. NO people, NO photoreal,
NO explicit content, NO real logos, max ~7 labeled nodes, no text artifacts/garbled labels.

---

## VISUAL A — Criterion 1: Chat realism & memory (3-step memory-test sequence)

- **Subject:** Horizontal editorial sequence diagram of the 5-minute memory test — tell a preference,
  change topics, ask a callback — showing PASS vs FAIL.
- **Canvas:** 3:2, white #FFFFFF.
- **Composition:** Three numbered stylized chat-bubble cards left→right (Step 1 "Tell it a
  preference", Step 2 "Change topics", Step 3 "Ask a callback"), connected by right-pointing arrows.
  Below Step 3 the path forks into two outcome cards: top green "PASS — recalls it unprompted",
  bottom red "FAIL — asks you to repeat".
- **Per-element:** Step 1 bubble holds a small tag glyph reading "call me Alex"; Step 2 bubble shows
  swirl/topic-change glyph; Step 3 bubble shows a question-mark glyph "what's my name?". PASS card:
  green #16A34A border, filled memory-bank/database glyph, reply tag "Alex". FAIL card: red #DC2626
  border, broken-link / empty memory glyph, generic "Sorry, remind me?" reply.
- **Style triangulation:** clean SaaS explainer infographic meets editorial line-icon set — NOT a
  real chat screenshot, NOT anime, NOT photoreal.
- **Lighting/render:** flat, soft drop shadows beneath cards.
- **Palette:** ink #1A1A2E, slate #4A5568, blue #3B82F6, green #16A34A, red #DC2626 on white.
- **Mood + anchor:** clear, diagnostic, confident. Awwwards/Behance editorial-diagram quality.
- **Typography:** sans-serif, short strings only ("call me Alex", "what's my name?", "PASS", "FAIL").

## VISUAL B — Criterion 4: Adult-content range spectrum (safe middle band)

- **Subject:** Horizontal content-range spectrum band showing the safe middle target between two
  red danger zones.
- **Canvas:** 3:2, white #FFFFFF.
- **Composition:** One wide horizontal band split into three labeled segments. Left segment red
  "No-limits / anything-goes" (danger). Center segment green "Explicit within stated rules" (the
  right target) with a small check/target glyph. Right segment hard-dark-red "Illegal / prohibited"
  (hard stop) with a no-entry glyph. A downward arrow + caption marks the center green band as
  "Aim here". Each segment carries 1-2 small descriptor sub-labels.
- **Per-element:** left red #DC2626 with a hidden-line / blurred glyph (hiding the line); center
  green #16A34A with a checkmark + boundary-bracket glyph; right segment deep #7F1D1D with a hard
  no-entry / shield-block glyph and small text "no minors · no real people".
- **Style triangulation:** policy-band infographic meets editorial flat vector — NOT explicit
  imagery, NOT photoreal.
- **Lighting/render:** flat band, subtle inner gradient per segment, soft shadow.
- **Palette:** red #DC2626, green #16A34A, deep red #7F1D1D, slate label text on white.
- **Mood + anchor:** judicious, mature, unambiguous. Editorial-diagram site-of-the-day quality.
- **Typography:** sans-serif short labels only.

## VISUAL C — Criterion 7: Age verification (real hard wall vs fake checkbox)

- **Subject:** Two-panel comparison — a real hard-wall age gate (green flag) vs a fake dismissible
  checkbox gate (red flag).
- **Canvas:** 3:2, white #FFFFFF, vertical divider down the middle.
- **Composition:** Left panel green-bordered "Real gate (green flag)": stylized modal with bold
  "18+ Verification Required" heading, an ID-card / card-check glyph, and a solid brick-wall band
  under it with sub-labels "Hard wall", "ID or card step", "Blocks entry until verified". Right panel
  red-bordered "Checkbox theater (red flag)": a lone ticked checkbox "I am 18+" floating over empty
  space, sub-labels "No wall", "One dismissible click", "Nothing verified".
- **Per-element:** left wall = stacked-brick glyph in slate; green #16A34A border + small green flag
  pennant icon top-corner. Right = single checkbox glyph, red #DC2626 border + small red flag pennant.
- **Style triangulation:** UX before/after explainer meets editorial flat vector — NOT a real
  screenshot, NOT anime.
- **Lighting/render:** flat, soft shadows under each modal card.
- **Palette:** green #16A34A, red #DC2626, slate #4A5568, ink labels on white.
- **Mood + anchor:** reassuring on the green side, hollow on the red side. Editorial quality, 4k.
- **Typography:** sans-serif, strings: "18+ Verification Required", "I am 18+".

## VISUAL D — Criterion 8: Platform fit (use-case → platform-type match) — NEW

- **Subject:** Decision/match diagram mapping a reader's situation to the platform type that fits it.
- **Canvas:** 3:2, white #FFFFFF.
- **Composition:** Left column "Your situation" lists three stylized scenario cards stacked
  vertically: (1) phone-icon "Phone, in private", (2) shared-screen-icon "Shared device", (3)
  fingerprint/lock-icon "Discretion first". Right column "Best-fit platform type" lists three target
  cards: "Polished mobile app", "Web-only browser login", "Light account + vague billing". Matched
  pairs connect left→right with arrows: scenario 1→mobile app, 2→web-only, 3→light account.
- **Per-element:** scenario cards slate #4A5568 outline with simple line glyphs (phone, two-people-
  one-screen, padlock). Target cards blue #3B82F6 accent. Connector arrows curved, color-matched to
  source row. Small footnote chip "test the exit: find cancel + delete first".
- **Style triangulation:** matchmaking / mapping infographic meets editorial flat vector — NOT
  photoreal, NOT anime, NO people depicted (icon glyphs only).
- **Lighting/render:** flat, soft card shadows.
- **Palette:** slate #4A5568, blue #3B82F6, ink #1A1A2E labels on white; green #16A34A on the
  footnote check chip.
- **Mood + anchor:** practical, orienting, decisive. Awwwards editorial-diagram quality, 4k.
- **Typography:** sans-serif short labels ("Phone, in private", "Web-only login", "test the exit").
