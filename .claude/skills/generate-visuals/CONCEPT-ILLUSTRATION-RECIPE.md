# Concept-illustration recipe — LOCKED 2026-06-28 (the gated AI lane)

The **rare ~6% "illustration" slot** in Ahrefs-style blogs: a SINGLE illustrative image for an
**abstract concept** — "AI memory", "your data stays private", "an AI that understands you" —
where a screenshot, chart, or table genuinely doesn't fit. Use it sparingly. **Prefer a real
screenshot (brand UI), chart, or table whenever the idea is concrete.** Reach for a concept
illustration only when the idea is truly abstract and a metaphor communicates it better than words.

## The policy: AI is allowed here, but in a NARROW, GATED lane
This is the one place we generate imagery with AI. The bar is high — this is the visual type most
likely to look cheap. The rule:

> An **extreme, specific, STRUCTURED prompt → Nano Banana** (Replicate `google/nano-banana`),
> then a **HARD VISION GATE**. If the result reads as "AI slop", generic, or off-brand → **CUT it.**
> Do **not** ship it. Iterate (max 3) or **abandon** the visual. A missing illustration is fine;
> a cheap one is not.

Anti-slop is locked into the prompt itself: strict brand palette, **zero text** (text is the #1 AI
tell and it garbles — the metaphor must carry the meaning), **no AI-drawn logo**, no
watermark/artifacts, hard **SFW** (public indexed blog, even though the product is adult).

## Pipeline
1. **Generate** — `node concept_illustration_engine.js --content c.json --out raw.png`
   `[--style editorial-vector|flat-geometric|luminous-dark] [--aspect 16:9]`
   Builds the structured anti-slop prompt from `c.json` and renders via Nano Banana.
   `REPLICATE_API_KEY` is **mandatory — no fallback** (loud-fail if missing).
2. **Deterministic palette check (first filter)** — `python concept_palette_check.py --in raw.png`
   Cheap machine signal that catches obvious palette drift (e.g. a cyan/teal hero instead of brand
   blue→violet). `WARN` ⇒ look harder. It does **not** decide — the vision gate is decisive.
3. **HARD VISION GATE (decisive)** — the agent **looks at the PNG** against the *Concept
   illustration* checklist in `VISUAL-CRITIQUE-LOOP.md` and returns `{pass, issues[]}`. Be a STRICT
   critic — if it looks even slightly like generic AI art, **fail it**. On fail, fix the spec
   (metaphor wording / style / palette) and re-render. **Max 3 passes, then abandon** — never ship
   a bad one.
4. **Optional logo (where appropriate)** — `python composite_logo.py --in raw.png --out final.png`
   Stamps the **real** Pleasur.ai logo, deterministically (never AI-drawn). **Default OFF** for
   in-body illustrations (the page chrome already shows the brand; a clean illustration reads more
   premium). **Turn it ON for share/OG cards** where the image travels without site chrome.

## Content schema (`c.json`)
```json
{
  "concept": "AI memory — your companion remembers what matters to you",
  "metaphor": "a single friendly rounded chat-bubble that cradles a small, tidy constellation of memory tokens inside it — three or four clean simple icons (coffee cup, birthday cake, little heart) joined by thin connecting threads like a constellation",
  "mood": "warm, intelligent, reassuring",
  "style": "editorial-vector",
  "aspect": "16:9"
}
```
- **`concept`** + **`metaphor`** are required. `mood`, `style`, `aspect` optional (CLI flags override).
- **`aspect`** ∈ `1:1 2:3 3:2 3:4 4:3 4:5 5:4 9:16 16:9 21:9` (passed as a real Nano Banana input).
  Default `16:9` (blog hero / in-body).

## The craft (what makes or breaks it)
- **The `metaphor` is the ONLY creative variable — and it is the whole game.** Write it richly and
  specifically. A strong, concrete metaphor reads instantly; a vague one yields slop. Describe
  **WHAT to depict** (shapes, objects, relationships) — **NOT the finish.** Do not put "glowing /
  glossy / glass / 3D" in the metaphor; **finish is the style's job.** (Finish words in the metaphor
  fight the flat style and produce the generic glossy-blob look.)
- **Zero text.** The engine forbids all text in the image. If a label is ever truly needed,
  composite it deterministically afterward — never let the model write words.
- **Strict brand palette**, baked in: blue `#2E90FA` + violet `#8B5CF6` dominant (gradient hero),
  mint `#22B276` + coral `#FF6B5C` as small accents, on a clean light cool-tinted background.
- **Keep it tidy.** One clear focal element, generous negative space, no cluttered pile of tiny
  objects. High neutral/negative-space area is good (and expected by the palette check).
- **SFW**, always — appropriate for a public, indexed blog.

## Style menu
| Style | Look | Use for |
|---|---|---|
| **`editorial-vector`** (default) | Flat 2D vector, matte, brand gradient, clean line-icons, light bg — Stripe/Linear/Intercom house style | **Primary.** Best legibility + on-brand; the proven winner. |
| `flat-geometric` | Bold cut-paper layered shapes, subtle layer shadows, light bg | A distinct alt; watch interior clutter. |
| `luminous-dark` | Glowing minimal forms on deep near-black, brand-gradient light | Atmospheric/premium for dark placements; lower icon legibility. |

> **Lesson (carried from the infographic/annotation/chart builds):** when stuck iterating, render a
> small **style sampler** on the hardest concept and pick the winner — don't guess-loop one knob.

## Proven examples (passed the gate 2026-06-28, editorial-vector)
| Concept | Metaphor core | Result |
|---|---|---|
| **AI memory** | chat-bubble cradling a constellation of clean memory-icons (coffee/cake/heart) joined by threads | ✅ clean, tidy, on-brand |
| **Data privacy** | chat-bubble sheltered inside a shield with an integrated mint padlock | ✅ palette correct, metaphor instant |
| **Understands you** | two bubbles (dots ↔ coral heart) joined by a connection wave; abstract, no people | ✅ strongest — cleanest read |

## Rejected (honest gate, same day)
- v1 of all three drifted to a **glossy-3D "app-icon" blob** with cluttered emoji-ish interiors;
  data-privacy v1 also drifted **cyan/teal** (palette check `WARN`, 3.7% abs off-color). All cut.
  Fix = harden the style toward FLAT/matte + de-gloss the metaphors → v2 passed.

## Why this is NOT wired into the auto-dispatcher
Like the infographic engine, concept illustrations require the **vision gate** (agent judgment) and
are generated deliberately, not auto-dispatched. `generate_visuals.py` still drops the legacy
`type=image` path; concept illustrations are produced by calling this engine + running the gate.
