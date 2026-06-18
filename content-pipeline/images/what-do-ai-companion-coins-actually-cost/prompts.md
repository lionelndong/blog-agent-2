# Visual prompts — what-do-ai-companion-coins-actually-cost

Built with `visual-prompt-craft` (9-part anatomy). SFW, no people, no real logos, clean
editorial-diagram style. In-image text kept short and exact (models mangle long copy).
Semicolons are forbidden inside the inline `prompt=` attribute (the parser splits on `;`),
so these strings use commas and periods only.

---

## image-1 — Intro concept diagram: "How a companion coin is spent"

archetype: Editorial diagram (hub-and-spoke, one source node → labeled cost nodes)

1. **Subject declaration** — Horizontal editorial vector diagram for a premium tech-lifestyle blog
   article explaining how a single in-app companion coin is spent, minimalist editorial layout,
   calm and explanatory mood.
2. **Canvas** — 3:2 in-article ratio, flat off-white background hex #FAFAF7 with a barely-there
   paper grain, generous whitespace.
3. **Composition map** — One large coin glyph anchored left-center spanning ~18% width. Three thin
   arrows fan rightward to three evenly stacked rounded rectangles occupying the right 60%. A fourth,
   greyed-out rectangle sits beneath them, visually de-emphasized.
4. **Per-element specification** — Coin: matte brushed-gold disc hex #C9A227 with a subtle bevel rim
   and a soft engraved swirl, no currency symbol. Cost cards: soft-touch matte cards hex #FFFFFF with
   a 1px cool-grey border hex #E2E2DD and a faint drop shadow; each holds a tiny line icon (picture
   frame, sound wave, phone handset) and a short label. Greyed card: 40% opacity, dashed border.
5. **Character & emotion** — Objects only. The coin reads confident and central, the cards orderly and
   reassuring, as if a clean receipt.
6. **Style triangulation** — Clean Scandinavian infographic vector meets modern fintech onboarding
   illustration. NOT 3D render, NOT skeuomorphic, NOT anime, NO photographic texture.
7. **Lighting & render spec** — Flat even lighting, no harsh shadows, crisp vector edges, soft cast
   shadow beneath each card as if gently raised.
8. **Palette block** — background #FAFAF7, coin #C9A227, cards #FFFFFF, borders #E2E2DD, arrows and
   primary labels #2B2B2B, greyed card text #9A9A94, single accent on arrows #6C63FF.
9. **Mood line + quality anchor** — explanatory, tidy, premium-fintech-clean. Awwwards / Behance
   site-of-the-day infographic quality, 4k.

**Typography block** — bold lowercase humanist sans (Inter / Söhne family). Exact strings only:
"AI image = 10", "voice note = 10", "phone call = 50 / min", "text = 0 unlimited".

**Retry 1 (art-director reject):** first render mislabeled the top card "1 coin" — the model bound
the coin-glyph label to card 1 instead of the cost label. Diagnosis: part-4 under-specified (label↔card
mapping ambiguous + a label on the coin invited the mix-up). Fix: removed the coin label entirely
("NO text label on the coin itself") and pinned each of the four cards to an exact string. Regenerated
standalone via generate_image.py — labels now correct (AI image = 10 / voice note = 10 /
phone call = 50 / min / text = 0 unlimited). model=openai/gpt-image-2.

---

## image-4 — 3-step calculator flow diagram: "Calculate your monthly companion cost"

archetype: Editorial flow diagram (left-to-right, 3 numbered steps + arrows)

1. **Subject declaration** — Horizontal three-step editorial flow diagram for a tech-lifestyle blog
   showing how a reader calculates their own monthly AI-companion cost, instructional and friendly mood.
2. **Canvas** — 3:2 in-article ratio, flat off-white background hex #FAFAF7 with faint paper grain.
3. **Composition map** — Three equal rounded-rectangle step cards arranged left-to-right across ~80%
   width, separated by two bold rightward arrows. A small circled step number sits top-left of each card.
4. **Per-element specification** — Step cards: matte white #FFFFFF, 1px border #E2E2DD, soft drop
   shadow. Card 1 holds three tiny line icons (picture frame, sound wave, phone handset) over a short
   label. Card 2 shows a small multiply glyph with three numerals. Card 3 shows a tiny price-tag icon.
   Step circles: solid accent #6C63FF with white numerals 1, 2, 3.
5. **Character & emotion** — Objects only; the row reads as a confident, easy three-step recipe.
6. **Style triangulation** — Clean Scandinavian infographic vector meets fintech onboarding flow.
   NOT 3D, NOT skeuomorphic, NOT anime, NO photo texture.
7. **Lighting & render spec** — Flat even lighting, crisp vector edges, soft cast shadows beneath cards.
8. **Palette block** — background #FAFAF7, cards #FFFFFF, borders #E2E2DD, step circles + arrows
   #6C63FF, labels #2B2B2B, icons #2B2B2B.
9. **Mood line + quality anchor** — instructional, tidy, premium-clean. Awwwards / Behance
   site-of-the-day infographic quality, 4k.

**Typography block** — bold lowercase humanist sans. Exact strings only: "estimate monthly use",
"multiply by coin cost 10 / 10 / 50", "pick cheapest tier that covers it".
