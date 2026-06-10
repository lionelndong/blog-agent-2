# Visual prompts — ai-sexting

Built with the `visual-prompt-craft` skill (9-part anatomy), calibrated against
`.claude/skills/visual-prompt-craft/references/example-prompts.md`. One-line prompts are a gate
failure; every generation call below carries a full structured prompt.

## Visual inventory (frugal by design)

This explainer ships **3** visuals — lean on purpose (real Replicate spend; charts/screens are free):

1. **Hero** — `image` (Replicate, ~$). Photoreal still-life, no people, SFW. Sets the calm, private,
   grown-up mood and earns the SERP/social click.
2. **How-it-works flow diagram** — `image` (Replicate, ~$). The single highest-value concept visual:
   makes the message → persona+memory → model → reply loop spatial. Labeled, brand-clean.
3. **Public Companion Creator screenshot** — `screenshot` (Playwright, free). Public `/create` page,
   no auth required. Shows the real setup surface the "how to start" section describes.

The privacy checklist was converted from a decorative `image` placeholder to an **inline bullet
list** (free, more scannable, no model spend). The original draft's `external` Reddit capture was
**removed** — it cannot render unattended (Cloudflare/login wall) and would HALT the visuals gate;
its point (real-user privacy concern) is already carried by prose + the FBI citation. The comparison
stays an **inline markdown table** (free).

## Working brand palette (intimate, premium, 18+)

- Warm coral (primary accent): `#FF6B6B`
- Charcoal ink (typography / line work): `#222222`
- Warm amber (hero lamp glow): `#E0A458`
- Dark walnut (hero surface): `#3A2A1E`
- Pure white (diagram canvas): `#FFFFFF`

---

## 1. Hero image (`image`, sub=lifestyle, safety=sfw → Replicate)

**1. Subject declaration.** Photorealistic editorial hero still-life for a blog explainer about AI
sexting — a calm, private, grown-up night-table scene, no people, intimate-but-tasteful mood.

**2. Canvas.** 16:9 hero. Background: a dark bedroom at night, dominant surface a dark walnut
(`#3A2A1E`) bedside table; deep shadow falloff to near-black at the frame edges.

**3. Composition map.** Center-right: a single smartphone lying screen-up, tilted ~10°. Foreground
lower-left: a pair of folded reading glasses. Mid-left: a closed paperback book, spine toward camera.
Negative space upper-left where the unseen lamp glow pools. Shallow depth of field, table surface in
sharp focus, background bokeh.

**4. Per-element spec.**
- *Smartphone:* brushed dark-aluminum body, soft-touch matte; screen glowing softly, showing three
  abstract rounded chat bubbles stacked vertically in a warm coral (`#FF6B6B`) tint — NO readable
  text, just smooth bubble shapes. Faint fingerprint smudge on the glass for realism.
- *Reading glasses:* thin tortoiseshell frames, one lens catching a small amber highlight.
- *Paperback:* worn cream cover, slight cover curl, visible paper grain on the page edges.

**5. Character & emotion.** No people. The felt emotion is private calm — late-night, unhurried,
adult, a little intimate. The warm pool of light says "this is a personal moment."

**6. Style triangulation.** Premium product still-life photography meets quiet domestic editorial —
think a New York Times tech-lifestyle photo, NOT a stock "glowing AI brain," NOT neon cyberpunk,
NOT any person or body in frame.

**7. Lighting & render.** Single warm amber (`#E0A458`) practical light from upper-left out of frame,
soft falloff; gentle screen self-illumination from the phone. Soft cast shadows beneath each object.
Cinematic shallow depth of field, crisp commercial product focus on the phone, creamy background blur.

**8. Palette block.** Dark walnut `#3A2A1E` (table), warm amber `#E0A458` (light), coral `#FF6B6B`
(screen bubbles), tortoiseshell brown + cream (props), near-black (edges).

**9. Mood + quality anchor.** Calm, private, intimate, grown-up, unhurried. Crisp commercial beauty
photography, cinematic color grading, 4k.

**Negatives:** no people, no faces, no body parts, no readable text, no logos, no neon, no robot,
no glowing-brain cliché.

---

## 2. How-it-works flow diagram (`image`, sub=concept-illustration, safety=sfw → Replicate)

**1. Subject declaration.** Clean editorial flow diagram for a tech blog explaining how an AI sexting
reply is generated — four labeled stages plus a feedback loop, minimalist vector aesthetic, calm.

**2. Canvas.** 3:2 in-article. Pure white (`#FFFFFF`) background, no texture, generous margins.

**3. Composition map.** Four stages evenly spaced left-to-right across the middle band, connected by
thin coral arrows pointing right. A single curved coral feedback arrow loops from stage 4 back up and
over to stage 2.

**4. Per-element spec.** Each stage = one simple outlined icon (consistent ~2px charcoal line weight)
with a short sentence-case label beneath in charcoal (`#222222`) sans-serif:
- Stage 1: outlined speech-bubble icon — label "Your message".
- Stage 2: outlined document icon — label "Persona + memory".
- Stage 3: outlined microchip icon — label "Model writes reply".
- Stage 4: outlined chat-bubble icon — label "In-character reply".
- Feedback arrow carries a small label "saved to memory".

**5. Character & emotion.** Objects only. Mood: clear, confident, explanatory — the visual equivalent
of a good teacher's whiteboard sketch.

**6. Style triangulation.** Flat two-color editorial vector (coral + charcoal on white) — think a
clean Stripe/Linear docs diagram, NOT skeuomorphic, NOT 3D-rendered, NOT clip-art, NOT hand-drawn.

**7. Lighting & render.** Flat — no shadows, no gradients. Even line weights, crisp vector edges.

**8. Palette block.** White `#FFFFFF` (canvas), coral `#FF6B6B` (arrows + accents), charcoal
`#222222` (icons + labels). Exactly two ink colors.

**9. Mood + quality anchor.** Clear, calm, professional, legible. Awwwards-clean editorial diagram
quality, every label crisp and correctly spelled.

**Negatives:** no other text anywhere, no decorative background, no people, no extra icons, no
gibberish characters, no drop shadows.

**In-image typography block:** clean geometric sans-serif (Inter / Helvetica archetype), sentence
case, charcoal. Only the five exact strings above. Keep text minimal.

---

## 3. Companion Creator screenshot (`screenshot`, public URL → Playwright, free)

- URL: `https://pleasur.ai/create` (public marketing/create surface; no auth needed).
- Crop: top viewport `0,0,1440,900`.
- `what` / alt: the public Companion Creator page showing the character setup surface.
- No prompt anatomy — this is a real screen capture, not a generation.

---

## Spend note

Two `image` generations (hero + diagram) on the default Replicate model. Estimated ~$0.04–$0.10
each → ~$0.08–$0.20 total for this article. Screenshot and inline table/list are free.
