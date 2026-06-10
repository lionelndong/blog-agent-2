# Visual prompts — ai-girlfriend-simulator (rebuilt per board Addendum 3, 2026-06-10)

Built with the `visual-prompt-craft` skill (9-part anatomy), calibrated against
`references/example-prompts.md`. Every generation call below uses a full structured prompt;
one-line prompts are a gate failure.

## Working brand palette (inferred — no canonical palette doc in repo; documented for consistency)

Pleasur.AI is a premium, intimate, 18+ AI-companion brand. Until a canonical palette ships, these
hexes are the working system used across every visual this run:

- Midnight plum (primary dark canvas): `#1B1430`
- Deep aubergine (secondary surface): `#2E1A3D`
- Warm rose (primary accent): `#E26D9C`
- Deep magenta (accent shadow / emphasis): `#C14A6E`
- Soft blush (light accent / fills): `#F5D6E0`
- Warm cream (light canvas): `#F7F2EC`
- Muted gold (highlight / "verify" markers): `#E0A458`
- Charcoal ink (typography on light): `#1A1A1A`
- Slate (body text on light): `#4A4458`

Confidence: inferred (source: visual-prompt-craft brand constraints + adult-companion category;
no `brand-config.md` palette block exists). Swap to canonical hexes when one is published.

---

## Art-director diagnosis of the PREVIOUS set (why it was weak)

The prior 7 generated images were all **text-heavy infographics** — comparison tables and checklists
with explicit "Rows: … Columns: …" instructions. Generative image models (gpt-image-2 / nano-banana)
**mangle long in-image text into gibberish**; the skill itself says "keep in-image text minimal." So
the weakness was two-layered: (a) one-line prompts with no composition/lighting/palette, AND (b) a
visual-TYPE mismatch — asking a paint model to render a spreadsheet.

**The fix is not "same images, longer prompts." It is the right tool per visual:**

| # | Section | Old approach | New approach | Why |
|---|---------|--------------|--------------|-----|
| HERO | top of article | (none) | **gpt-image-2**, photoreal tasteful companion scene | Article had no click-earning hero; this is what generative imagery is *good* at |
| 2 | "What is…" umbrella | text diagram (gpt) | **gpt-image-2**, icon-driven umbrella diagram, ≤7 nodes, minimal text | concept made spatial — a true diagram archetype |
| 5 | Simulator vs app… | text hub-spoke (gpt) | **gpt-image-2**, icon-driven hub-and-spoke, glyphs + 1-word labels | concept/relationship art, not a table |
| 7 | How to compare | text decision-tree (gpt) | **gpt-image-2**, icon-driven decision flow, arrows + glyphs | flow art, minimal text |
| 1 | Quick answer | comparison "graphic" (gpt) | **matplotlib table-card** (crisp real text) | it IS a 5×4 table — render legible text, not paint it |
| 4 | Simulator vs app | comparison "infographic" (gpt) | **matplotlib table-card** | same — a real comparison table |
| 6 | Evaluation checklist | checklist "graphic" (gpt) | **matplotlib table-card** | a 10-row checklist — needs legible text |
| 9 | Supported/needs-source | claims checklist (gpt) | **matplotlib three-column card** | compliance content must be legible, not gibberish |
| 10 | Pre-chat safety | safety checklist (gpt) | **matplotlib table-card** | a real 8-row checklist |
| 3 | SERP surface mix | chart (matplotlib) | **keep** — already canonical | real data |
| 8 | /create screenshot | screenshot | **keep** — real product capture | evidence |

Net: 4 crafted generative concept visuals + 5 legible table-cards + 1 chart + 1 screenshot. Legible
where text matters, agency-grade where mood matters. Table-cards are free (no API spend).

---

# GENERATIVE PROMPTS (gpt-image-2, style-suffix disabled — the full prompt carries all style)

## HERO — photoreal tasteful companion scene (new, 16:9, top of article)

1. **Subject declaration.** Horizontal 16:9 editorial hero image for a premium adult-tech lifestyle blog article titled "AI Girlfriend Simulator: What It Means and How to Choose." Cinematic, intimate-but-tasteful photoreal scene of a young woman at home at night using an AI-companion app on her phone; calm, warm, considered mood — the emotional promise of "choosing the right companion experience," not titillation.

2. **Canvas.** Full-width 16:9. Background: a softly out-of-focus living room at night in deep midnight-plum (#1B1430) deepening to aubergine (#2E1A3D) at the edges, fine cinematic film grain, gentle bokeh from a string of warm fairy lights behind her.

3. **Composition map.** Subject seated lower-left, occupying ~55% of frame, turned three-quarters toward camera. Phone held at chest height in her hands, its screen the brightest point in the image, casting a warm rose glow up onto her face and collarbone. Right ~40% of frame is negative space (soft dark bokeh) reserved for headline overlay — keep it clean, no text rendered in-image. Thin warm-rim light along her shoulder separating her from the dark background.

4. **Per-element specification.**
   - *Woman:* mid-20s, AI-generated face (NOT any real or famous person), relaxed natural expression — a small private half-smile, eyes lowered to the screen, lips softly closed. Warm sun-kissed skin with realistic micro-detail (faint freckles across the nose, soft baby-hairs catching the rim light, natural skin texture, no plastic retouch). Loose dark-auburn hair tucked behind one ear, a few strands lit by the phone glow. Wearing an oversized soft-knit cream sweater (#F7F2EC) with visible chunky-knit texture, sleeves slightly bunched at the wrists. Tasteful, fully clothed, cozy.
   - *Phone:* matte charcoal phone, screen showing an abstract warm-rose chat interface — soft rounded message bubbles in blush (#F5D6E0) and rose (#E26D9C), NO legible text, NO real app logos, just suggestive UI shapes and a small glowing companion avatar orb.
   - *Environment:* blurred sofa arm in foreground lower-edge, a single lit candle far background-right as a warm bokeh point, throw-blanket texture catching low light.

5. **Character & emotion.** She feels unhurried and a little curious — the expression of someone in a comfortable private moment, not performing for a camera. Jaw relaxed, shoulders soft, weight settled into the sofa. The story is intimacy-with-agency: she is *choosing*, calmly.

6. **Style triangulation.** A24-film still meets premium lifestyle editorial photography — NOT glamour/boudoir, NOT anime, NOT 3D-render, NOT stock-photo "woman smiling at phone." Tasteful, cinematic, restrained.

7. **Lighting & render spec.** Primary light = warm rose screen-glow from below-front (the phone), secondary = cool dark ambient, plus a thin warm rim-light from upper-right separating subject from background. Shallow depth of field (~f/1.8): face and hands tack-sharp, background melting into bokeh. Soft realistic shadows, natural skin specular highlights, gentle filmic color grade.

8. **Palette block.** Midnight-plum→aubergine background (#1B1430→#2E1A3D), warm rose screen glow and accents (#E26D9C / #C14A6E), blush UI shapes (#F5D6E0), cream sweater (#F7F2EC), warm candle/gold points (#E0A458), natural warm skin tones.

9. **Mood line + quality anchor.** Intimate, calm, premium, cinematic, emotionally warm, tasteful. Crisp commercial beauty photography, cinematic color grading, shallow depth of field, fine film grain. Awwwards / Behance editorial hero quality, 4k.

Hard constraints: 18+ adult subject only; AI-generated person, NO real-person/celebrity likeness, NO deepfake framing; suggestive-at-most, NO nudity/explicit content; no real third-party logos; no in-image text.

---

## #2 — Umbrella concept diagram (icon-driven, 3:2)

1. **Subject declaration.** Horizontal 3:2 editorial concept diagram for a premium tech blog showing "AI girlfriend simulator" as one umbrella term that branches into several distinct product formats. Clean vector-editorial illustration, generous whitespace, calm premium mood.

2. **Canvas.** 3:2, warm cream background (#F7F2EC) with very subtle paper grain.

3. **Composition map.** A single large rounded "umbrella" node centered upper-third. Five short connector lines fan downward to five evenly-spaced child nodes across the lower-middle band. One small gold gate-marker sits on the connectors as a "verify" checkpoint.

4. **Per-element specification.** Parent node: soft-rounded rectangle in deep aubergine (#2E1A3D) with a small white umbrella glyph; one short label only. Five child nodes: equal soft-rounded cards in blush (#F5D6E0) with rose (#E26D9C) outline, each carrying ONE simple line-icon and ONE one-word label — speech-bubble (chat), palette/face (creator), phone (app), game-controller (game), sparkles (mixed-media). A small muted-gold (#E0A458) shield-check glyph on the connector band marks the verify gate. Subtle long soft shadows under each card.

5. **Character & emotion.** Orderly, reassuring, "this is simpler than it looks" — the diagram should feel like a calm explainer, not a busy infographic.

6. **Style triangulation.** Modern flat-vector editorial (think Stripe/Linear docs illustration) meets soft rounded friendliness — NOT skeuomorphic, NOT clip-art, NOT 3D, NOT anime. Max 7 labeled nodes, ≤2 words per label.

7. **Lighting & render spec.** Flat even lighting, crisp vector edges, soft consistent drop-shadows beneath cards, no gradients except a faint one on the parent node.

8. **Palette block.** Cream canvas (#F7F2EC), aubergine parent (#2E1A3D), blush cards (#F5D6E0) with rose outlines (#E26D9C), muted-gold gate marker (#E0A458), charcoal labels (#1A1A1A).

9. **Mood line + quality anchor.** Clean, calm, editorial, premium, trustworthy. Awwwards / Behance documentation-illustration quality, 4k. Keep all text crisp and minimal; no paragraph text, single-word labels only.

---

## #5 — Hub-and-spoke relationship diagram (icon-driven, 3:2)

1. **Subject declaration.** Horizontal 3:2 editorial hub-and-spoke diagram positioning "AI Girlfriend Simulator" as the canonical guide at the center, linked to four related topics. Clean vector-editorial style, premium calm mood.

2. **Canvas.** 3:2, warm cream background (#F7F2EC), faint paper grain.

3. **Composition map.** One prominent circular hub dead-center. Four spoke nodes at compass points (up, down, left, right), each joined to the hub by a thin rose connector line. One spoke (lower-left) drawn with a dashed, dimmed line to signal "pending."

4. **Per-element specification.** Hub: circle in deep aubergine (#2E1A3D), small white book/compass glyph, one short center label. Spokes: rose-outlined blush circles, each one line-icon + one short label — wrench/face (make a companion), mask (yandere niche), phone-stack drawn DASHED and 60% opacity (apps — pending), shield-check in gold (safety checklist). Connector lines in rose (#E26D9C); the pending spoke's line dashed in muted slate.

5. **Character & emotion.** Authoritative but friendly — a "you are here, and here is how everything relates" map.

6. **Style triangulation.** Flat-vector knowledge-map (Notion/Obsidian-graph aesthetic, refined) — NOT mind-map clip-art, NOT 3D, NOT anime. ≤6 labeled nodes, single-word labels.

7. **Lighting & render spec.** Even flat lighting, crisp edges, subtle soft shadow under hub only, clean anti-aliased lines.

8. **Palette block.** Cream (#F7F2EC), aubergine hub (#2E1A3D), blush spokes (#F5D6E0)/rose outlines (#E26D9C), gold safety glyph (#E0A458), slate dashed pending line (#4A4458), charcoal labels (#1A1A1A).

9. **Mood line + quality anchor.** Clean, authoritative, calm, premium. Awwwards / Behance infographic quality, 4k. Crisp minimal text only.

---

## #7 — Decision-flow diagram (icon-driven, 3:2)

1. **Subject declaration.** Horizontal 3:2 editorial decision-flow illustration: "choose your format, then pass the checks before you try." Clean vector-editorial, calm confident mood.

2. **Canvas.** 3:2, warm cream background (#F7F2EC), faint grain.

3. **Composition map.** Left third: a starting node with five small format options stacked. A central rose arrow flows left→right into a vertical "gate" bar of four check-markers. Right third: a single calm "ready to try" end node. Flow reads clearly left to right.

4. **Per-element specification.** Start node: aubergine rounded card, one short label, five tiny format glyphs (chat / creator / app / game / mixed) as a small icon row. Gate bar: four stacked muted-gold (#E0A458) shield-check markers, each with one one-word label icon — coin (pricing), lock (privacy), boundary/line (boundaries), exit-door (exit). End node: blush rounded card with a soft rose check, one short label. A bold rose (#E26D9C) directional arrow connects the three zones.

5. **Character & emotion.** Steadying and practical — "slow down, verify, then enjoy." Not bureaucratic; warm and clear.

6. **Style triangulation.** Flat-vector flowchart, premium editorial (Linear/Stripe docs) — NOT corporate-clip-art flowchart, NOT 3D, NOT anime. Minimal text, icon-led.

7. **Lighting & render spec.** Flat even lighting, crisp vector edges, soft shadow under nodes, clean arrowheads.

8. **Palette block.** Cream (#F7F2EC), aubergine start (#2E1A3D), gold gate markers (#E0A458), rose arrow + outlines (#E26D9C), blush end card (#F5D6E0), charcoal labels (#1A1A1A).

9. **Mood line + quality anchor.** Calm, practical, premium, reassuring. Awwwards / Behance flow-diagram quality, 4k. Single-word labels only.

---

# TABLE-CARD SPECS (matplotlib — crisp real text, no API spend)

Rendered via `scripts/render_table_card.py` (brand palette above). These carry real legible content
the generative models cannot. Header band aubergine (#2E1A3D) with cream text; "verify"/gold accents
on key cells; alternating cream/blush row stripes; rounded card framing; ≥1600px wide.

### #1 — "Simulator types" quick-answer table
Columns: Type · What it means · Best fit · What to verify
Rows: Chat companion · Character creator · Mobile app · Dating-sim game · Mixed-media product
(content sourced from article §Quick Answer)

### #4 — "Simulator vs app vs creator vs game"
Columns: Format · Searcher intent · Example surface · What to verify
Rows: Chat companion · Character creator · Mobile app · Dating-sim game

### #6 — Evaluation checklist
Columns: What to check · Question to ask · Where to verify
Rows: Customization · Conversation style · Memory transparency · Media features · Browser-vs-app access · Game mechanics · Pricing · Privacy · Deletion · Support

### #9 — Claims boundary (three columns)
Columns: ✅ Supported · ⚠️ Needs a source · 🚫 Don't claim
Cells from article §Where Pleasur.ai Fits compliance block.

### #10 — Pre-chat safety checklist
Columns: Check · Why it matters · Where to verify
Rows: Age rules · Fictional framing · Content boundaries · Sensitive-data warning · Privacy policy · Deletion & retention · Pricing · Support path

---

## Generation log (filled during this run)

See `manifest.json` for final prompt / model / retries / art-director verdict per visual.
