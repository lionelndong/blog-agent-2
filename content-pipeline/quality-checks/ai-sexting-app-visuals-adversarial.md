## Round 2 (current)

### Verdict: **PASS**

Slug: `ai-sexting-app`
Stage: 9b (visuals-adversarial)
Date: 2026-05-13
Revision pass: 1 (post-revision re-check)
CRITICAL count: **0**

---

### Density math (round 2)

- Cited draft body word count (frontmatter + voice-flagged tail excluded): **~2,470 words**.
- Density band: 2,000–3,000 words → target 10, **acceptable range 8–13** (per `templates/editorial-principles-visuals.md`).
- Captured visuals in the draft (manifest `status=captured`): **8** (1 table + 1 chart + 6 image).
- Stripped: 1 (index-2 /create screenshot, replaced by image-9 concept flow).
- **8 captured = band floor. PASS.** Round-1 density CRITICAL is resolved.
- Type diversity: 3 distinct types (table / chart / image) — meets ≥3 minimum.

---

### Per-visual 9-step re-check (all 8)

**1. table-1-feature-pricing-matrix.png** — feature/pricing/privacy matrix (KEEP).
Unchanged from round 1. All 9 criteria pass. 4 apps × 7 columns; live-fetched pricing 2026-05-13 caption; Mozilla PNI privacy column carries discriminating signal. Single strongest visual in the set.

**2. screenshot-2 (STRIPPED, confirmed).**
Manifest `status=stripped`, `reason=visuals-adversarial-critical-2-adult-imagery`. PNG renamed out of publish path. No `![...]` reference present in the cited draft (line 102 now points to image-9 concept flow). Round-1 CRITICAL resolved.

**3. chart-3-mozilla-pni-2024.png** — Mozilla PNI 2024 bar chart (KEEP).
Unchanged from round 1. All 9 criteria pass. 5 metrics on 0–100 scale, value labels, footer sourcing, red-for-fail / green-for-pass editorial color logic.

**4. image-4-category-concept-diagram.png** — three-box concept diagram (KEEP).
Visually verified. Three labeled boxes side-by-side: "Generic chatbot" / "One-shot NSFW chatbot" / "AI sexting app" with numbered headers (1/2/3), a distinct icon per box (robot / silhouette / heart-in-chat-bubble), and one-line descriptors underneath ("safety lecture / no character", "no memory / faceless model", "named character, persistent memory, chat plus image plus voice"). Reads cleanly at thumbnail size. SFW. PASS on all 9 criteria including (9) — illustrative but not slop-decorative; labels make it informational, not decorative.

**5. image-5-bundled-chat-mockup.png** — phone chat mockup (KEEP).
Visually verified. Smartphone frame with realistic iOS-style status bar (9:41), header "Maya / Online", an assistant chat bubble ("That sounds lovely! I'd be happy to send a picture from the garden."), a user reply bubble ("send me a picture in the garden"), and a generating-image placeholder card with a flower/tree illustration plus "Generating image..." spinner. Voice-mic icon visible on composer. Conveys the bundled-thread claim (chat + image-gen request in one thread). SFW (illustrated character avatar, no nudity, not a real-person face). PASS.

**6. image-6-candy-app-card.png** — Candy.AI app-store-style card (KEEP).
Visually verified. App-card layout: pink heart icon top-left, "Candy.AI" brand wordmark, tagline "Polished default — 100+ characters", price band "$13–$28 / mo (gated)", three feature dots ("chat", "image gen", "voice notes"). Looks like a real app-card, not a glowing blob. SFW. PASS.

**7. image-7-ourdream-app-card.png** — OurDream.AI app-store-style card (KEEP).
Visually verified. Purple cloud-with-sparkles icon, "OurDream.AI" wordmark, tagline "Visual-led — image + video on demand", price "$19.99 / mo flat", three feature dots ("image gen", "video gen", "dreamcoins"). Clean app-card geometry. SFW. PASS.

**8. image-8-nastia-app-card.png** — Nastia AI app-store-style card (KEEP).
Visually verified. Purple sparkle/spark icon, "Nastia AI" wordmark, tagline "Full-feature value pick", price band "Free tier + paid" with discount tag glyph, three feature dots ("chat", "voice", "image"). Same app-card geometry as 6/7 — consistent visual rhythm across the three competitor cards. SFW. PASS.

**9. image-9-pleasurai-creator-flow.png** — 4-step Companion Creator flow (KEEP).
Visually verified. Four labeled cards in a left-to-right numbered sequence (1/2/3/4) connected by arrows. Step 1 "Appearance" (avatar/silhouette icon, purple), step 2 "Voice" (audio-waveform icon, blue), step 3 "Personality + backstory" (chat-bubbles icon, green), step 4 "Kinks & boundaries" (padlock icon, orange). Each step has a discrete icon and a label — not a row of abstract icons. Conveys the "design the character yourself across four axes" claim the prose makes three paragraphs earlier. SFW. PASS.

---

### Specific questions from the brief

- **Are the 6 new Replicate images SFW?** YES. No nudity, no implied nudity, no real-person faces. Only illustrated avatars (Maya in image-5, silhouette in image-4 + image-9) and product/icon glyphs.
- **Do the 4 app-card images look like app-store cards?** YES. Consistent layout across 6/7/8: square icon top-left, brand wordmark, tagline line, price band, three feature dots with labels. They read as cards, not as abstract glowing blobs. (Image-9 is a flow, not a card — also reads cleanly.)
- **Does the chat-mockup show real UI structure?** YES. Status bar, header with online status, two-sided message bubbles, an image-generation placeholder card, composer with mic icon. Not a generic phone-with-a-screen.
- **Does the concept diagram show three labeled boxes with readable text?** YES. Three boxes, numbered, each with a header, an icon, and a one-line descriptor underneath. Readable at the size it'll render in-article.
- **Does the creator flow show 4 labeled steps in sequence?** YES. Numbered 1→2→3→4, each step a distinct icon + label, connected by arrows. Not a row of abstract icons.

---

### Issues found (non-blocking)

- **Minor (image-6 Candy.AI card):** the price band reads "$13–$28 / mo (gated)" — this is the third-party-clustered range the prose explicitly refuses to quote as fact ("we won't quote that as fact, because the source page doesn't publish it"). The card visualizes the very number the prose disowns. Recommend either (a) editor changes the card to read "Gated — trial required" matching the table, or (b) leave as-is and accept that the third-party range is illustrative not authoritative. Not strip-worthy.
- **Minor (image-5 chat mockup):** the assistant message reads "send a picture from the garden" — a benign garden scene, well clear of the topic. This is a *feature*, not a defect, for SFW publishing, but a few readers may find the disconnect between article topic ("sexting app") and visual content ("garden picture") slightly off. The alt text plus surrounding prose make the bundled-thread point clearly, so it lands. Not strip-worthy.

Neither rises to CRITICAL. Both are editor-judgment polish items.

---

### Advance decision

**ADVANCE to /preview.** Round-2 verdict is PASS with 0 CRITICALs. Density floor met (8/8), all 8 visuals KEEP, both round-1 CRITICALs resolved. Revision budget consumed (pass 1 of default 1) — no further visuals revisions warranted.

---

## Round 1

## Verdict: **FAIL**

Slug: `ai-sexting-app`
Stage: 9b (visuals-adversarial)
Date: 2026-05-13
CRITICAL count: **2**

---

## Density math

- Cited draft body word count (frontmatter + voice-flagged tail excluded): **~2,600 words**.
- Density band: 2,000–3,000 words → **target 10, acceptable range 8–13** (per `templates/editorial-principles-visuals.md`).
- Captured visuals (manifest `status=captured`): **3** (table + screenshot + chart).
- **Gap to target: -7. Gap to floor of band: -5.** This is the failure mode PLEAA-499 explicitly named — "2 lonely visuals and 2,500 words of unbroken prose."
- Type diversity: 3 distinct types (table, screenshot, chart) — hits the ≥3 minimum, but only because each of the three earned-visual slots picked a different type. The diversity floor is met; the *count* is not.

The outline self-capped itself at 3 ("at cap 3/3 per editorial constraint from `0-context/ai-sexting-app.md`"). That cap was set when the band target was lower; under the current editorial-principles-visuals.md table, 2,600 words wants 10. The cap is the bug.

---

## Per-visual 9-step check

### Visual 1 — Table (feature/pricing/privacy matrix)
File: `content-pipeline/images/ai-sexting-app/table-1-feature-pricing-matrix.png`
Section: "The 4 AI sexting apps worth using in 2026" (H2 lead).

| # | Criterion | Result | Note |
|---|---|---|---|
| 1 | Could a sentence convey it? | PASS | 4 apps × 7 substantive columns. A sentence cannot. |
| 2 | Most efficient form? | PASS | Comparison matrix is the canonical shape for "N apps × M dimensions." |
| 3 | Concrete subject? | PASS | App names, real prices, real privacy posture. |
| 4 | Removing it costs information? | PASS | Reader loses the five-second skim path; would have to read all four H3s to compare. |
| 5 | Front-loads info? | PASS | Sits directly under the H2's roll-call sentence. |
| 6 | Matches the section's claim? | PASS | The claim is "these four, and here's how they differ" — the table is that. |
| 7 | Sourced/dated? | PASS | "live-fetched pricing 2026-05-13... Mozilla PNI 2024" — caption is correct. |
| 8 | Crop / framing? | PASS | Clean matplotlib table, no chrome, no truncation. |
| 9 | Avoids AI-tells? | PASS | Tabular, no generated imagery. |

On the "Privacy posture" column being filler: it actually carries information. Two cells say "Mozilla PNI: flagged" (Candy.AI, OurDream.AI) and two say "Says no data sale; deletion allowed" (Nastia AI, Pleasur.AI). That's the discriminating signal the privacy H2 later argues — pulling it into the matrix lets the skim-reader see it without scrolling. Keep.

One nit: the column is "Price (USD/mo)" without indicating annual equivalents the H3s mention. Not a strip-trigger.

**Verdict: KEEP.** Genuinely earns its place — the single strongest visual in the set.

---

### Visual 2 — Screenshot (Pleasur.AI /create, step 1: appearance picker)
File: `content-pipeline/images/ai-sexting-app/screenshot-2-https-pleasur-ai-create.png`
Section: "Pleasur.AI — the build-your-own pick" H3, placed after the four numbered build steps.

| # | Criterion | Result | Note |
|---|---|---|---|
| 1 | Could a sentence convey it? | FAIL-leaning | The surrounding prose already walks all four steps in detail. The screenshot only depicts step 1. |
| 2 | Most efficient form? | FAIL | A multi-step composite (or an action-shot showing a later step) would convey "Companion Creator depth" — a single appearance-picker screen does not. |
| 3 | Concrete subject? | PASS | Real product UI. |
| 4 | Removing it costs information? | WEAK PASS | Reader loses a visual anchor for the brand, but loses no specific information the prose doesn't already give them (the alt text even concedes "the first step in building a custom companion"). |
| 5 | Front-loads info? | PASS | Placed after the BLUF, before the next subsection. |
| 6 | Matches the section's claim? | FAIL | The section's claim is "design the character yourself — appearance, personality, backstory, voice, kinks." The screenshot shows only appearance (and only "Realistic vs Anime" at that — the very first sub-step). It under-delivers on the four-axis promise the prose is making three paragraphs earlier. |
| 7 | Sourced/dated? | N/A | Brand-owned UI; sourcing not required. |
| 8 | Crop / framing? | PARTIAL FAIL | Full viewport with side nav and "Join Pleasur.ai" upsell card visible — irrelevant chrome. A crop to the central picker would carry more signal per pixel. |
| 9 | Avoids AI-tells? | **CRITICAL FAIL** | Both preview thumbnails ("Realistic" and "Anime") show topless characters with visible nipples. The cited draft is SFW prose — the screenshot drops adult-explicit imagery into an article that has, until this point, been safe to publish anywhere. This is a strict editorial-rule violation: `templates/visual-types.md` line 60-66 says "Most blog illustrations should be SFW... keeps the published article SFW for ad-network and embed compatibility." Even though this is `screenshot` not `image`, the published-article-must-be-SFW rule applies to the asset, not the type. The brand's safety field even encoded this — `safety=adult-context-route-via-manual-capture` — and the capture pipeline auto-captured anyway, because the authenticated /create page renders the explicit previews by default. |

**Verdict: REPLACE.** Two routes:

- **Preferred (revision-safe):** strip the screenshot, fall back to prose-only for the Companion Creator walkthrough. The outline explicitly anticipated this: "If `/visuals-adversarial` drops one, drop the Pleasur.AI screenshot first and demonstrate the Companion Creator walkthrough in prose only" (outline line 237). That is the cleanest action.
- **If a Pleasur.AI visual is wanted:** replace with either (a) a SFW-cropped action-shot of the *personality / backstory* step (step 3 — the textarea where the reader writes character context, which is the actual "depth" the prose claims), or (b) a `screenshot` of the homepage / explore grid clipped to a SFW area. Both require new captures — not in scope for an adversarial revision pass.

Recommended action for the revision loop: **strip** (set manifest to `status=stripped`, reason=`visuals-adversarial-critical-9`, remove the `![alt](...)` line from the draft, merge surrounding paragraphs). Backfill the count with image/concept-illustration or external visuals elsewhere (see density additions below).

---

### Visual 3 — Chart (Mozilla PNI 2024, 5 metrics)
File: `content-pipeline/images/ai-sexting-app/chart-3-mozilla-pni-2024.png`
Section: "Privacy is a real buying criterion" H2.

| # | Criterion | Result | Note |
|---|---|---|---|
| 1 | Could a sentence convey it? | PASS | The prose paragraph compresses three of the five stats ("90% may share or sell... only Genesia passed"); the chart adds the two the paragraph drops (73% no published vulnerability process, 64% no clear encryption info) and visually anchors the 90/90/73/64/54 distribution. |
| 2 | Most efficient form? | PASS | A bar chart with value labels is the canonical shape for "5 audit failures across 11 chatbots." |
| 3 | Concrete subject? | PASS | Real audited percentages from a named, dated study. |
| 4 | Removing it costs information? | PASS | The reader loses the 73% / 64% / 54% data points the prose doesn't carry inline. |
| 5 | Front-loads info? | PASS | Title carries the takeaway ("Mozilla Privacy Not Included 2024 — romantic AI chatbots audit"); 90% bars dominate the eye in one glance. |
| 6 | Matches the section's claim? | PASS | Section claim is "Mozilla flagged this whole category" — the chart proves it with five concrete metrics. |
| 7 | Sourced/dated? | PASS | Footer credit "Mozilla Foundation, Privacy Not Included — Romantic AI Chatbots Don't Have Your Privacy at Heart, Feb 14 2024 (n=11 apps audited). Muah.AI breach Sept 2024 1.9M accounts (HIBP)." |
| 8 | Crop / framing? | PASS | Generous chart margins, no truncation. |
| 9 | Avoids AI-tells? | PASS | Matplotlib bar chart, no AI imagery. Color choice (red for failures, green for the one positive metric) is editorial, not slop. |

**Verdict: KEEP.** Earns its place strongly — and the manifest note confirms the v1 chart was already rejected and re-rendered for exactly the right reasons (one-axis percentages + Muah breach quarantined to caption).

---

## Density additions (to clear the CRITICAL density finding)

The article needs **at least 4 more visuals** to reach the band floor of 8, and ideally 5–7 more to hit the target of 10. Listed by H2, with type:

1. **Introduction (H2 0)** — `image` (sub=concept-illustration). Diagram: "AI sexting app vs mainstream chatbot vs one-shot NSFW bot" — a three-panel side-by-side that anchors the contrarian thesis. The intro currently runs ~180 words of pure prose; a visual at the bottom of the intro would break the prose wall before the first H2.
2. **What an AI sexting app actually is** — `image` (sub=concept-illustration). Diagram: the "modern shape" bundling — text + in-conversation image + voice in one thread vs the older split-tabs model. The prose introduces "the modern shape bundles three things into one chat" — a labeled diagram would convey it twice as fast.
3. **Candy.AI H3** — `external` (sub=competitor-ui). Clip to `candy.ai/` homepage hero (the /pricing 404 is a fact worth visualizing — the screenshot is the *evidence* of the gated-pricing claim). Selector clipped to the homepage CTA + the visible 7-day trial signal.
4. **OurDream.AI H3** — `external` (sub=competitor-ui). Clip to `ourdream.ai/pricing` showing the published $19.99/mo + dreamcoin allocation. This is the "only one whose pricing page publishes a flat monthly USD" claim — the page itself is the proof.
5. **Nastia AI H3** — `external` (sub=competitor-ui). Clip to the privacy statement on `nastia.ai/` — the article quotes it verbatim. Showing the quote on the live page is the verification.
6. **Pleasur.AI H3 backfill** — `image` (sub=concept-illustration) replacing the stripped screenshot. Four-panel diagram of the Companion Creator's four build axes (appearance, voice, personality, kinks). SFW illustration; conveys the "depth" the screenshot under-delivered on. Alternative if the editor wants a real-product asset: an action-shot of step 3 (personality/backstory textarea) at SFW crop.

Adding 1–6 lands the article at 8 captured visuals (3 retained, 1 replaced, 5 added) which is **at the band floor**. Adding additionally an `external` for the HIBP Muah breach record (sub=news-quote, selector clipped to the PwnedWebsites row) gets to 9 — comfortably mid-band.

## Manual-capture fallthrough

No `manual-capture.md` entries on disk for this slug (totals: 0 manual). Nothing to drop on that front.

---

## The two earned-its-place visuals to call out

- **Table** (visual 1) is the clearest "earns its place" in the set — it's the article's skim path and the discriminating signal the H3s would otherwise have to repeat four times.
- **Chart** (visual 3) is genuinely informative: it both anchors and *extends* the privacy paragraph (which only cites three of the five Mozilla metrics inline), and the manifest note shows iteration already happened to get the rendering right.

---

## Critical findings (2)

1. **CRITICAL — Density.** 3 captured vs band floor of 8 (target 10). The article will ship with two long unbroken prose runs (privacy → free → FAQ → conclusion has 800+ words and one chart; intro → "what is" → "the 4 picks H2 intro" has ~600 words and one table). Add the visuals listed in "Density additions" above; section names and types are explicit so the revision loop can append `[VISUAL:...]` placeholders verbatim.
2. **CRITICAL — Adult imagery in screenshot.** `screenshot-2-https-pleasur-ai-create.png` contains explicit nudity (bare-breasted character previews on the Realistic + Anime cards). Cannot ship in a SFW-published article regardless of how strong the underlying placement argument is. Strip from the draft and mark the manifest entry `status=stripped` with `reason=visuals-adversarial-critical-2-adult-imagery`. The outline pre-authorized this fallback (line 237).

## Surgical fixes

- **Strip:** remove `![Pleasur.AI Create flow showing the appearance picker — the first step in building a custom companion](images/ai-sexting-app/screenshot-2-https-pleasur-ai-create.png)` from `content-pipeline/6-drafts-cited/ai-sexting-app.md` (line 102). Merge the paragraph before (the four-step walkthrough) with the paragraph after (image generation). Update `content-pipeline/images/ai-sexting-app/manifest.json` visual #2 to `status=stripped` with the reason above.
- **Add:** append the six placeholders listed in "Density additions" to the cited draft at the named H2/H3 boundaries, then re-dispatch `/generate-visuals` for those new entries. Prefer `image` (concept-illustration) for items 1, 2, 6 — fastest to generate, adds type diversity. `external` for items 3, 4, 5 — captures the competitor / source pages already cited in prose.
- **Loop budget:** this is the first FAIL on stage 9b. With default budget 1, the revision pass should run.
