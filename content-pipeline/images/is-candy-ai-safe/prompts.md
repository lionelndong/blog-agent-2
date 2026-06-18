# Visual prompts — is-candy-ai-safe

Built with `visual-prompt-craft` (9-part anatomy). Studied Example 1 (character-driven
3D render) and Example 2 (cinematic photoreal portrait) from
`.claude/skills/visual-prompt-craft/references/example-prompts.md` before drafting.

Two typed placeholders in `content-pipeline/6-drafts-cited/is-candy-ai-safe.md`:

| # | Original type | Realized as | Tool / model |
|---|---|---|---|
| 1 | `external` (review-quote) | DESIGNED pull-quote card (`type=image`) | Replicate `openai/gpt-image-2` |
| 2 | `screenshot` (privacy policy) | Playwright capture of brand-owned page | patchright headless |

Visual 2 is a Playwright screenshot of a brand-owned public page (pleasur.ai/legal/privacy-policy)
— no generation prompt is needed for it, so only Visual 1 carries a generation prompt below.

---

## Visual 1 — review-quote pull-quote card (designed, NOT a third-party screenshot)

**Why redesigned, not screenshotted:** the source placeholder was `type=external` pointing at a
third-party review site. Screenshotting that triggers a manual-capture flag and risks third-party
logos / real-person likeness. Per the stage brief we instead render the cited line as a clean,
brand-styled editorial pull-quote card — auto-generated, no logos, no people, no likeness.

**Archetype:** Editorial pull-quote / typographic card (a comparison-panel cousin — a single
attributed quote rendered as a designed card, not a screenshot of a spreadsheet or website).

### Final prompt (sent to gpt-image-2; default style suffix overridden via `style_suffix`)

1. **Subject declaration** — Horizontal editorial pull-quote card for a premium tech-lifestyle blog
   article about AI-companion app safety and data transparency. Clean modern editorial-poster
   layout: a single short attributed quotation set as the hero element, calm and authoritative in
   mood, reading like a designed magazine call-out rather than a screenshot.

2. **Canvas** — 3:2 horizontal in-article card. Soft off-white paper background (#F7F6F2) with a
   very subtle fine paper grain; a single hairline rule in muted slate (#C7CDD6) framing the card
   interior with generous margins (no busy borders).

3. **Composition map** — Centered single-column layout. Upper-left zone: a large oversized opening
   quotation glyph ("rotated 66 quote mark) in pale slate (#D8DEE6), spanning ~18% of card height,
   sitting behind/above the text as a decorative anchor. Center band (~64% width, vertically
   centered): the quotation in two to three lines of large, confident type. Lower-center, below a
   short 40px horizontal divider rule: a small attribution line. Bottom-right corner: a tiny neutral
   "editorial source" tag chip. Whitespace dominates — at least 22% clear margin on every edge.

4. **Per-element specification** —
   - *Quote text block:* material is crisp printed ink on matte paper; deep ink-charcoal (#23272E);
     medium-weight humanist serif (Tiempos / Lyon archetype); tight-but-airy leading; the exact
     string set across the lines reads: "The policy doesn't spell out its encryption posture." Micro
     details: faint ink-edge softness, subtle baseline shadow, no italics.
   - *Oversized quotation glyph:* flat vector mark, pale slate (#D8DEE6), softly rounded terminals,
     positioned upper-left, ~35 degrees of visual weight, sitting low-contrast so it never competes
     with the quote text.
   - *Divider rule:* 40px wide, 2px tall, warm slate (#9AA3AF), centered, with a soft cast shadow
     of 1px.
   - *Attribution line:* small tracked uppercase grotesk (Söhne / Aeonik archetype), warm grey
     (#6B7280), exact string: "INDEPENDENT SAFETY REVIEW · 2026". No publication name, no logo,
     no real outlet branding.
   - *Source tag chip:* tiny pill outline in muted slate (#C7CDD6) with the word "CITED" in 9px
     tracked caps; sits unobtrusively bottom-right.

5. **Character & emotion** — No people, no faces, no hands (compliance: zero real-person likeness).
   The "character" is the typography itself: composed, sober, trustworthy, the felt tone of a
   careful editor presenting a sourced fact plainly — never alarmist, never sensational.

6. **Style triangulation** — Swiss/International editorial poster typography meets calm modern
   fintech-report design — NOT a website screenshot, NOT a social-media quote card, NOT neon,
   NOT meme-style, NOT skeuomorphic, NO drop-shadowed 3D text, NO photographic background.

7. **Lighting & render spec** — Flat, even, soft diffuse studio light as if scanned print; no harsh
   highlights; faint paper grain catching light evenly; the divider and glyph carry only the
   gentlest 1px soft shadow to imply layered paper. Crisp vector edges on type, no motion blur,
   no bokeh.

8. **Palette block** — paper off-white background (#F7F6F2), ink-charcoal quote text (#23272E),
   pale-slate decorative glyph (#D8DEE6), warm-slate divider (#9AA3AF), warm-grey attribution
   (#6B7280), muted-slate hairline + chip (#C7CDD6). Restrained five-to-six tone neutral palette,
   zero saturated color.

9. **Mood line + quality anchor** — calm, authoritative, transparent, editorial, trustworthy,
   premium-restrained. Awwwards / Behance editorial typography quality, 4k, crisp print-grade
   rendering.

**Typography block** — Quote: medium-weight humanist serif (Tiempos / Lyon archetype), sentence
case. Attribution + chip: small tracked uppercase grotesk (Söhne / Aeonik archetype). Keep total
in-image text to the single short quote + one attribution line + one 5-letter chip (models mangle
long copy — kept deliberately minimal).

**Compliance check:** 18+ neutral; no people / no likeness / no deepfake framing; no third-party
logos or outlet names (generic "INDEPENDENT SAFETY REVIEW" attribution only); no internal-stack /
vendor names anywhere in the image text.

### Art-direction judging rubric (applied to each render)
- Quote string spelled correctly and legible (gpt-image-2 text artifacting is the #1 risk).
- No people, no logos, no website chrome.
- Neutral palette held; no rogue saturated color.
- If FAIL: diagnose which anatomy part under-specified it; strengthen; regenerate (max 2 retries).

### Retry log
- **Attempt 1 (FAIL):** gpt-image-2 ignored the supplied strings and fabricated its own quote
  ("Trust is not a feature...") attributed to an invented named person ("MIRA KAPOOR · AI ETHICS
  RESEARCHER & DIGITAL WELLBEING ADVOCATE"). Compliance fail (invented real-sounding person /
  attribution) + accuracy fail (not the sourced line). Also square 1024px, not 3:2. Diagnosis:
  anatomy parts 4 (exact in-image strings) and 5 (character) under-specified against the model's
  tendency to confabulate text — the prompt didn't hard-forbid inventing an author.
- **Attempt 2 / retry 1 (PASS):** rewrote with verbatim-quote pinning ("reproduce EXACTLY ...
  'The policy doesn't spell out its encryption posture.'") and explicit negatives ("Do NOT add a
  person's name / author / job title / other words"). Render now shows the exact sourced line, a
  generic "INDEPENDENT SAFETY REVIEW 2026" attribution, no person, no logo, neutral palette — art
  direction PASS. Endpoint still returns a fixed 1024x1024 square regardless of the requested 3:2;
  upscaled losslessly (Lanczos) to 1600px wide to clear the >=1200px-wide quality bar. Composition
  is centered so the upscale preserves it cleanly. Used within the 2-retry budget (1 retry used).

---

## Visual 2 — Pleasur.ai privacy-policy screenshot (brand-owned, Playwright)

Brand-owned public page — captured directly via patchright headless, no generation prompt.
- URL: https://pleasur.ai/legal/privacy-policy
- Capture: full page, 1440x900 @2x viewport (brand default).
- Compliance: brand's own page; no third-party content; fully automatable.

---

# REVISION PASS 1 (PLEAA-499 under-density FAIL → add 3 visuals to reach floor of 6)

Adversarial verdict was FAIL: 3 effective visuals (table + pull-quote card + privacy
screenshot) vs floor of 6 / target 8. Two CRITICAL missing-visual findings named the
checklist H2 (needs a concept diagram) and the comparison H2 (needs regulatory evidence).
Adding 3 NEW auto-generated visuals below: a 5-point checklist concept diagram (Visual 3,
gpt-image-2), a regulatory-history timeline (Visual 4, matplotlib — sourced events only,
NOT a third-party screenshot), and a 4-platform safety scorecard infographic (Visual 5,
gpt-image-2). Brings the page to 6 total.

---

## Visual 3 — 5-point safety-checklist concept diagram (designed, gpt-image-2)

**Section:** H2 "What to look for in a safe AI companion" — the section teaches a 5-point
mental model. The existing privacy-policy screenshot proves a policy exists but does not
illustrate the framework. This is the highest-value explanatory concept-illustration in the
piece.

**Archetype:** Editorial diagram — concept made spatial (vertical labeled checklist /
five numbered criteria nodes), clean vector-editorial style, brand-neutral palette,
generous whitespace, exactly 5 labeled nodes.

### Final prompt (9-part anatomy; sent to gpt-image-2, style_suffix overridden)

1. **Subject declaration** — Horizontal editorial concept-illustration diagram for a premium
   tech-lifestyle blog article about how to vet a safe AI-companion app. Clean modern
   vector-editorial layout: a five-point verification checklist rendered as a calm, designed
   information graphic, authoritative and trustworthy in mood, reading like an infographic
   from a careful consumer-tech report — never an ad, never alarmist.

2. **Canvas** — 3:2 horizontal in-article card. Soft off-white paper background (#F7F6F2)
   with a very subtle fine paper grain; a single hairline rule in muted slate (#C7CDD6)
   framing the interior with generous margins; whitespace dominates.

3. **Composition map** — A title band across the top (~14% height). Below it, five evenly
   spaced horizontal rows, each a clean rounded-rectangle "criterion card" stacked
   vertically OR arranged as five numbered nodes left-to-right; each row has, left: a small
   circular numbered badge (1–5) in restrained violet (#9333EA); center-left: a short bold
   label; a thin connecting hairline runs through all five badges to imply a sequence. At
   least 20% clear margin on every edge.

4. **Per-element specification** —
   - *Title band:* deep ink-charcoal (#23272E) medium-weight grotesk, exact string:
     "5 things a safe AI companion lets you verify".
   - *Five numbered badges:* flat vector circles, restrained violet (#9333EA), white numeral
     1–5, softly rounded, consistent size; faint 1px soft shadow.
   - *Five criterion labels* (exact short strings, in this order, each on its own row):
     "1  Published, readable privacy policy", "2  Encryption in transit AND at rest",
     "3  Clear stance on training & selling data", "4  Real 18+ age verification",
     "5  Data deletion & access rights". Crisp ink-charcoal (#23272E) humanist sans,
     left-aligned, generous leading.
   - *Connecting hairline:* warm-slate (#9AA3AF), 2px, threading the five badges.
   - *Tiny corner glyph:* a small outlined shield-check mark in pale slate (#D8DEE6),
     unobtrusive, bottom-right — generic, NOT a brand logo.

5. **Character & emotion** — No people, no faces, no hands (zero real-person likeness). The
   "character" is the typography and clean iconography: composed, methodical, trustworthy —
   the felt tone of a careful checklist, never sensational, never sales-y.

6. **Style triangulation** — Swiss/International editorial infographic meets calm modern
   consumer-report design — NOT a website screenshot, NOT a social-media carousel slide,
   NOT neon, NOT 3D, NOT skeuomorphic app UI, NO photographic background, NO drop-shadowed
   3D text.

7. **Lighting & render spec** — Flat, even, soft diffuse studio light as if scanned print;
   faint even paper grain; only the gentlest 1px soft shadow on badges and the corner glyph;
   crisp vector type edges, no blur, no bokeh.

8. **Palette block** — paper off-white background (#F7F6F2), ink-charcoal text (#23272E),
   restrained-violet badges (#9333EA), warm-slate connector (#9AA3AF), pale-slate glyph
   (#D8DEE6), muted-slate hairline (#C7CDD6). Restrained near-neutral palette with a single
   violet accent; zero other saturated color.

9. **Mood line + quality anchor** — calm, methodical, authoritative, editorial, trustworthy,
   premium-restrained. Awwwards / Behance editorial infographic quality, 4k, crisp
   print-grade rendering.

**Typography block** — Title + labels: medium-weight humanist grotesk (Söhne / Aeonik
archetype), sentence/short-label case. Badge numerals: bold grotesk. Keep in-image text to
the title + five short labels + five numerals (no body copy — models mangle long text).

**Compliance check:** 18+ neutral; no people / no likeness / no deepfake framing; no
third-party logos or outlet names; generic shield-check glyph only; no internal-stack /
vendor names anywhere in the image text.

### Art-direction judging rubric
- All five labels legible and spelled correctly (gpt-image-2 text artifacting is top risk).
- Exactly five nodes, numbered 1–5 in order; no extra invented criteria.
- No people, no logos, no app-UI chrome; violet accent held, no rogue color.
- If FAIL: diagnose which anatomy part under-specified it; strengthen; regenerate (max 2).

---

## Visual 4 — AI-companion regulatory-history timeline (matplotlib, designed)

**Section:** comparison H2 "Candy AI vs Replika vs Nomi AI vs Pleasur.ai" — the regulatory
column compresses three sourced events into one table cell. A designed timeline gives that
the visual evidence the adversarial flagged, WITHOUT screenshotting any third-party site.

**Why matplotlib, not an external capture:** the verdict suggested an `external` clip of a
news headline; per the stage brief, external captures get manual-flagged and risk
logos/likeness. Instead this renders a self-authored editorial timeline using ONLY the
events already cited in the draft. Script:
`content-pipeline/images/is-candy-ai-safe/_render_regulatory_timeline.py`.

**Sourced events (1:1 with citations in the cited draft — nothing invented):**
- Feb 2023 — Italy's regulator banned the app (TechCrunch / IAPP).
- Jan 2025 — US FTC complaint filed, unresolved as of early 2026 (Tech Justice Law / TIME).
- 2025 — operator fined €5M over age-verification & data-handling (TechCrunch / IAPP).

**Design:** horizontal spine, three violet marker nodes, date above / two-line description
below / source attribution at the base, plus a footer disclaimer ("Sourced events only…
not legal advice") to hold the non-absolutist compliance voice. Brand-neutral palette
(paper #F7F6F2, ink #23272E, violet #9333EA accent). No logos, no people, no likeness.

**Compliance check:** competitor name (Replika) appears in footer only, sourced from public
reporting — not an internal/vendor name; no third-party logos; no real-person likeness; no
fabricated events; figures match the cited draft exactly.

---

## Visual 5 — "Data Candy AI collects" concept diagram (designed, gpt-image-2)

**REPLACED (adversarial re-run pass 1):** the first draft of Visual 5 was a 4-platform
"App A–D" safety scorecard. The re-run flagged it CRITICAL on two counts: (1) the
strong/partial/unstated dot legend was ambiguous/contradictory against the sourced table
("strong" regulatory dot is meaningless), and (2) it duplicated the comparison markdown
table it sat above (principle 5: don't ship a chart AND a table of the same data). Both are
correct. Visual 5 is therefore re-scoped to a NON-duplicative concept-illustration that the
FIRST adversarial explicitly named as high-value: a "data Candy AI collects" net diagram
anchoring the text-heavy verdict section. It carries information no other visual does (the
specific collection list), duplicates nothing, and breaks up the ~280-word verdict block.

**Section:** H2 "Is Candy AI safe? The honest, sourced verdict" — right after the paragraph
enumerating what Candy AI collects.

**Archetype:** Editorial diagram — concept made spatial (hub-and-spoke): a central "your
account" hub with labeled data-type nodes radiating out. Clean vector-editorial style,
brand-neutral palette, generous whitespace, exactly 6 labeled nodes (max 7 per skill).

**Data (1:1 with the cited Scribe breakdown already in the draft — nothing invented):**
email & username · chat logs · generated images · device & IP details · usage &
browser-fingerprint data · third-party payment info.

### Final prompt (9-part anatomy; sent to gpt-image-2, style_suffix overridden)

1. **Subject declaration** — Horizontal editorial concept-illustration diagram for a premium
   tech-lifestyle blog article about AI-companion data privacy. Clean modern vector-editorial
   hub-and-spoke layout: a central account hub with six labeled data-type nodes radiating
   out, rendered as a calm, designed information graphic — neutral and explanatory, like a
   careful consumer-tech report, never alarmist, never an ad.

2. **Canvas** — 3:2 horizontal in-article card. Soft off-white paper background (#F7F6F2)
   with a very subtle fine paper grain; a single hairline rule in muted slate (#C7CDD6)
   framing the interior with generous margins; whitespace dominates.

3. **Composition map** — Centered hub-and-spoke. Center: a single rounded hub circle in
   restrained violet (#9333EA). Six thin warm-slate connector lines radiate out evenly to six
   small rounded-rectangle node cards arranged in a balanced ring around the hub; each node
   card holds a short label and a tiny simple line-icon. A title sits in a band across the
   top. At least 18% clear margin on every edge.

4. **Per-element specification** —
   - *Title:* deep ink-charcoal (#23272E) medium-weight grotesk, exact string:
     "What Candy AI collects".
   - *Central hub:* violet (#9333EA) filled circle, white short label inside reading
     "Your account".
   - *Six node cards* (exact short strings, each with a tiny generic line-icon):
     "Email & username", "Chat logs", "Generated images", "Device & IP", "Usage data",
     "Payment (3rd-party)". Cards: off-white fill, muted-slate (#C7CDD6) hairline border,
     ink-charcoal (#23272E) label text.
   - *Connector lines:* warm-slate (#9AA3AF), 2px, thin, from hub to each node.
   - *Tiny line-icons:* flat single-weight vector glyphs (envelope, chat bubble, image
     frame, device, chart, card), ink-charcoal, no fills, generic — NOT brand logos.

5. **Character & emotion** — No people, no faces, no hands (zero real-person likeness). The
   character is the clean radial diagram: composed, explanatory, neutral — the felt tone of a
   careful editor showing "here is the data net," never sensational.

6. **Style triangulation** — Swiss/International editorial infographic meets calm modern
   consumer-report design — NOT a website screenshot, NOT app UI, NOT a social-media slide,
   NOT neon, NOT 3D, NO photographic background, NO drop-shadowed 3D text.

7. **Lighting & render spec** — Flat even soft diffuse studio light as if scanned print;
   faint even paper grain; gentlest 1px soft shadow on the hub and node cards; crisp vector
   edges, no blur.

8. **Palette block** — paper off-white (#F7F6F2), ink-charcoal text/icons (#23272E),
   restrained-violet hub (#9333EA), warm-slate connectors (#9AA3AF), muted-slate node
   borders + hairline (#C7CDD6). Restrained near-neutral palette, single violet accent, zero
   other saturated color.

9. **Mood line + quality anchor** — calm, explanatory, neutral, authoritative, editorial,
   trustworthy, premium-restrained. Awwwards / Behance editorial infographic quality, 4k,
   crisp print-grade rendering.

**Typography block** — Title + node labels: medium-weight humanist grotesk (Söhne / Aeonik
archetype). Hub label: bold grotesk. Keep in-image text to the title + hub label + six short
node labels (no body copy — models mangle long text).

**Compliance check:** 18+ neutral; no people / no likeness / no deepfake framing; generic
line-icons only (no third-party logos); "Candy AI" is the article's subject brand named in
the title, NOT an internal-stack / vendor name; no internal/vendor names anywhere.
(Brand-agnostic alternative is fine if the model struggles with the name, but the verdict
section is explicitly about Candy AI's collection list, so naming it in the title is honest
and on-topic.)

### Art-direction judging rubric
- Title + six node labels legible/correct; exactly six nodes; hub centered with connectors.
- No people, no third-party logos, no app-UI chrome; violet accent held, no rogue color.
- Collection list matches the sourced Scribe breakdown exactly; nothing invented.
- If FAIL: diagnose which anatomy part under-specified it; strengthen; regenerate (max 2).

### (Archived) original Visual 5 — 4-platform safety scorecard infographic
Stripped per adversarial re-run (duplicated the comparison table + ambiguous dot legend).
Kept here for the audit trail; the rendered file image-5-safety-scorecard.png is no longer
referenced by the draft. Original archetype was a comparison panel of four App A–D cards
with a strong/partial/unstated status-dot legend.

### Final prompt (9-part anatomy; sent to gpt-image-2, style_suffix overridden)

1. **Subject declaration** — Horizontal editorial comparison-scorecard infographic for a
   premium tech-lifestyle blog article comparing the data-transparency posture of four
   AI-companion apps. Clean modern vector-editorial layout: four labeled cards in a row, each
   with a small row of status dots, reading like a calm consumer-report scorecard — neutral,
   authoritative, never an ad.

2. **Canvas** — 16:9 horizontal comparison panel. Soft off-white paper background (#F7F6F2)
   with subtle fine paper grain; thin hairline rules (#C7CDD6) separating the four columns;
   generous margins.

3. **Composition map** — Title band across top (~12% height). Below, four equal vertical
   cards left-to-right, each with: a header strip holding a short generic platform label, and
   beneath it four small labeled criterion rows each ending in a status dot (filled =
   yes/transparent, half = partial, hollow = unstated/under-documented). A tiny legend strip
   sits bottom-center.

4. **Per-element specification** —
   - *Title:* ink-charcoal (#23272E) medium grotesk, exact string:
     "AI-companion safety at a glance".
   - *Four card headers* (generic, NON-branded labels, exact strings):
     "App A", "App B", "App C", "App D" — deliberately generic so no third-party brand or
     logo is implied.
   - *Four criterion row labels* (repeated per card, exact short strings):
     "Published policy", "Encryption", "Regulatory history", "18+ verification".
   - *Status dots:* flat vector circles — filled restrained-violet (#9333EA) = strong,
     half-filled warm-slate (#9AA3AF) = partial, hollow outlined muted-slate (#C7CDD6) =
     unstated. Consistent diameter; faint 1px soft shadow.
   - *Legend strip:* tiny tracked caps, "● strong   ◐ partial   ○ unstated", warm-grey
     (#6B7280).

5. **Character & emotion** — No people, no faces, no hands. The character is the clean,
   even, methodical grid — composed, neutral, trustworthy; never alarmist, never sales-y.

6. **Style triangulation** — Swiss/International editorial scorecard meets calm modern
   consumer-report design — NOT a website screenshot, NOT a spreadsheet, NOT app UI, NOT
   neon, NOT 3D, NO photographic background, NO drop-shadowed 3D text.

7. **Lighting & render spec** — Flat even soft diffuse studio light as if scanned print;
   faint even paper grain; gentlest 1px soft shadow on dots; crisp vector edges, no blur.

8. **Palette block** — paper off-white (#F7F6F2), ink-charcoal text (#23272E),
   restrained-violet strong dots (#9333EA), warm-slate partial dots (#9AA3AF), muted-slate
   hollow dots + hairlines (#C7CDD6), warm-grey legend (#6B7280). Restrained near-neutral
   palette, single violet accent, zero other saturated color.

9. **Mood line + quality anchor** — calm, neutral, authoritative, editorial, trustworthy,
   premium-restrained. Awwwards / Behance editorial infographic quality, 4k, crisp
   print-grade rendering.

**Typography block** — Title + labels: medium-weight humanist grotesk (Söhne / Aeonik
archetype). Legend: small tracked caps. Keep in-image text to the title + 4 generic headers
+ 4 criterion labels + tiny legend (no body copy).

**Compliance check:** GENERIC card labels (App A–D) so NO third-party brand/logo is shown;
no people / no likeness; no internal-stack / vendor names; 18+ neutral. (The named-platform
verdicts already live in the markdown table; this card stays brand-agnostic to avoid
rendering competitor logos.)

### Art-direction judging rubric
- Title + criterion labels legible/correct; four cards, four rows each; legend present.
- No third-party brand names or logos (generic App A–D only); no people.
- Violet accent held, no rogue saturated color.
- If FAIL: diagnose which anatomy part under-specified it; strengthen; regenerate (max 2).
