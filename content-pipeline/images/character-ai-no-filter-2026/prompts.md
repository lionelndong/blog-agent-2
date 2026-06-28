# Structured generation prompts — character-ai-no-filter-2026

Built with `visual-prompt-craft` (9-part anatomy) before any generation call. Two `[VISUAL:type=image]`
placeholders in the cited draft. Both are clean editorial diagrams (no people — compliant by construction),
so each carries a typography block for the in-image labels. Replicate `openai/gpt-image-2` default,
`google/nano-banana` backup on refusal.

Brand visual constraints (brand-config.md): no real third-party logos/trademarks (generic glyphs only),
no tool/vendor names in image text beyond the platform labels the draft itself names, tasteful adult brand
but these two visuals contain NO people and NO suggestive content — pure concept diagrams.

---

## Image 1 — concept-flow (the "real fix" flow, intro, line 9)

Horizontal editorial diagram for a premium consumer-tech blog explaining that the fix for a blocked
AI chat filter is switching to a dedicated adults-only platform. Minimalist flat-vector editorial layout,
calm and authoritative mood, generous whitespace.

Canvas: 3:2 in-article composition. Pure off-white background (#FBFBFD) with a barely-perceptible fine
paper grain. No border.

Composition map: a single left-to-right flow across the horizontal midline. LEFT third: a rounded phone
chat-bubble card. CENTER: a bold right-pointing arrow with a small label above it. RIGHT third: a larger
rounded panel with a green check badge and a vertical stack of three small labeled feature rows. Equal
vertical centering; ~12% margin all sides.

Per-element specification:
- LEFT card (~26% width): a soft-shadowed rounded-rectangle in white (#FFFFFF) with 16px corner radius,
  containing a single grey chat bubble (#E4E7EC) with three short anonymized line-strokes (NO readable
  text on the chat screen). Overlapping the bubble's lower-right, a flat circular shield glyph in muted
  red (#D14B4B) with a small white slash through it (a "blocked" mark, generic — not any real app icon).
  Micro-details: subtle inner drop-shadow on the bubble, 1px hairline card outline (#EEF0F3).
- CENTER arrow (~14% width): a thick rounded-cap arrow in charcoal (#2A2D34) pointing right, with a small
  caption chip above it.
- RIGHT panel (~30% width): a rounded-rectangle in white (#FFFFFF), 16px radius, with a flat circular
  green check badge (#2E9E6B, white tick) pinned to its top-left corner. Inside, three stacked rows, each
  a tiny rounded mono-line icon (a chat glyph, a clock/memory glyph, a picture-frame glyph) followed by a
  short label. Micro-details: faint row dividers (#F1F3F6), soft ambient shadow under the panel.

Character & emotion: none — this is an object/diagram composition; the "personality" is calm confidence
conveyed by clean geometry and the red-to-green resolution.

Style triangulation: modern SaaS editorial vector illustration in the register of Stripe / Linear marketing
diagrams — flat, geometric, restrained. NOT skeuomorphic, NOT 3D, NOT glossy, NOT anime, no gradients beyond
subtle shadow, no clipart.

Lighting & render spec: flat illustration lighting; soft ambient drop-shadows beneath each card as if gently
raised off the surface; crisp vector edges; no texture beyond the faint paper grain.

Palette: background off-white (#FBFBFD), cards white (#FFFFFF), hairlines/dividers (#EEF0F3 / #F1F3F6),
chat bubble grey (#E4E7EC), blocked shield muted red (#D14B4B), arrow + labels charcoal (#2A2D34), success
green (#2E9E6B).

Typography block: clean medium-weight geometric sans (like Inter or Söhne), sentence case, normal tracking.
Exact strings — LEFT card label below it: "Character.AI filter"; CENTER arrow caption chip: "the real fix";
RIGHT panel header: "Dedicated 18+ platform"; the three RIGHT rows: "Uncensored roleplay", "Persistent
memory", "Image gen". Keep text crisp and minimal; no other words anywhere.

Mood line + quality anchor: clean, authoritative, reassuring, editorial-tech. Awwwards / Behance
site-of-the-day quality vector diagram, 4k.

---

## Image 7 — decision-tree (how to choose, line 123)

Horizontal editorial decision-tree diagram for a premium consumer-tech blog: one question branching to six
labeled outcome chips, each naming a platform recommendation. Minimalist flat-vector editorial layout,
helpful and decisive mood, generous whitespace.

Canvas: 3:2 in-article composition. Pure off-white background (#FBFBFD) with a barely-perceptible fine
paper grain. No border.

Composition map: a single entry node on the LEFT, vertically centered. Six thin connector lines fan out to
the RIGHT into two stacked columns of three outcome chips each (3 upper, 3 lower), evenly spaced. ~12%
margin all sides.

Per-element specification:
- ENTRY node (LEFT, ~22% width): a rounded-rectangle in charcoal (#2A2D34) with a white label; 16px radius,
  soft ambient shadow. Micro-detail: a small white question-mark glyph to the left of the label.
- SIX connector lines: thin (2px) rounded-cap charcoal lines (#2A2D34) fanning from the right edge of the
  entry node to each chip, gently curved (no sharp elbows).
- SIX outcome chips (RIGHT, each ~26% width): pill-shaped rounded-rectangles in white (#FFFFFF) with a 1px
  hairline outline (#EEF0F3) and soft ambient shadow. Each chip holds a short two-part label: a use-case
  in charcoal (#2A2D34) and the platform name in muted teal accent (#2E8C99), separated by a thin dot.
  The FIRST chip (best all-round) gets a subtle green left-edge accent bar (#2E9E6B) to read as the primary
  recommendation. Micro-detail: consistent inner padding, equal chip heights.

Character & emotion: none — object/diagram composition; mood is decisive clarity.

Style triangulation: modern SaaS editorial vector illustration like Stripe / Linear marketing diagrams —
flat, geometric, restrained. NOT skeuomorphic, NOT 3D, NOT glossy, NOT anime, no clipart, no icons inside
the chips.

Lighting & render spec: flat illustration lighting; soft ambient drop-shadows beneath the node and chips;
crisp vector edges; faint paper grain only.

Palette: background off-white (#FBFBFD), entry node charcoal (#2A2D34), connector lines charcoal (#2A2D34),
chips white (#FFFFFF) with hairline (#EEF0F3), use-case text charcoal (#2A2D34), platform-name accent teal
(#2E8C99), primary-recommendation edge green (#2E9E6B).

Typography block: clean medium-weight geometric sans (like Inter or Söhne), sentence case, normal tracking.
Exact strings — ENTRY node: "What do you want?"; the six chips (top column then bottom): "Best all-round -
Pleasur.ai", "Try free first - CrushOn AI", "Long-form writing - DreamGen", "Polished companion - Candy AI",
"Big library - Joyland AI", "Max control / API - Janitor AI". No other words anywhere.

Mood line + quality anchor: clean, helpful, decisive, editorial-tech. Awwwards / Behance site-of-the-day
quality vector decision-tree, 4k.

---

## VISUALS REVISION 2026-06-18 (visuals-adversarial FAIL → surgical fix)

The 3 external third-party screenshots (#2 reddit-comment, #5 CrushOn pricing, #6 DreamGen pricing) were
DECORATIVE (facts already in prose + comparison table + citations) and could not be retried (Chrome MCP
unreachable). They were stripped from the draft body and marked `status: removed` in the manifest. To
recover density honestly and add type diversity, 4 new auto-capturable, information-bearing visuals were
added — 1 matplotlib `chart` + 3 people-free concept diagrams. NO external/third-party screenshots, NO
people, NO real logos, brand-safe by construction. Full 9-part prompts below.

### NEW A — price chart (comparison-table section)

`[VISUAL:type=chart;data=research.entry_paid_tier_usd_monthly;style=bar;title=Entry paid monthly price — platforms with public pricing (USD)]`

Not an image-model prompt — matplotlib bar render from `character-ai-no-filter-2026-data.json`
key `entry_paid_tier_usd_monthly` (Pleasur.ai Starter $12.99 / CrushOn Standard $4.90 / DreamGen Starter
$7.83). Honest scope: only the 3 vendor-confirmed-price platforms; the draft caption states Candy AI /
Joyland / Janitor publish no public price. Adds a 3rd captured type. No people, no text artifacts.

### NEW B — why-the-filter diagram ("Why does Character AI have a filter?" H2)

Horizontal editorial cause-and-effect diagram: three compliance-obligation cards (Protect minors / Terms of
Service / Payment rules) converging through thin connectors into a grey "General-audience filter" funnel
glyph, then a bold arrow to a green-checked "Dedicated 18+ platform" panel. Canvas 3:2, off-white #FBFBFD,
flat-vector Stripe/Linear register. Per-element: white #FFFFFF cards (16px radius, hairline #EEF0F3, soft
shadow), mono-line shield/document/card glyphs, charcoal #2A2D34 connectors, grey #E4E7EC filter glyph,
green #2E9E6B check badge, teal #2E8C99 accent. NO people, no faces, no real logos. Typography: Inter/Söhne
sentence case; exact strings only — "Protect minors", "Terms of Service", "Payment rules",
"General-audience filter", "Dedicated 18+ platform". Style negatives: NOT 3D/skeuomorphic/glossy/anime, no
clipart. Awwwards-quality 4k. (Full prompt inline in the draft placeholder.)

### NEW C — no-mode / bypass-risk illustration ("Does Character AI have a no-filter mode?" section)

Horizontal editorial dead-end flow: an "Unofficial mod-APK" card (download/box glyph + amber #D9962B warning
badge) → charcoal arrow → a "Security & account risk" cluster of three red #D14B4B risk badges (broken
shield / key-with-exclamation / account-alert) → arrow → a "Still filtered" phone chat card with a closed
grey padlock over an unreadable bubble. Canvas 3:2, off-white #FBFBFD, flat-vector Stripe/Linear register.
NO people, no faces, no real app logos or store badges. Typography: Inter/Söhne sentence case; exact strings
only — "Unofficial mod-APK", "Security & account risk", "Still filtered". Style negatives: NOT
3D/skeuomorphic/glossy/anime, no clipart. Awwwards-quality 4k. (Full prompt inline in the draft placeholder.)

### NEW D — persistent-memory illustration (Pleasur.ai section, memory paragraph)

Horizontal editorial two-session timeline: "Session 1 - today" chat card and "Session 2 - next week" chat
card separated by a faint dashed time-gap divider, bridged by a center "Persistent memory" store (teal
#2E8C99 brain/database glyph + green #2E9E6B check) with thin charcoal connectors arcing down to each
session, showing continuity carries across. Cards hold grey #E4E7EC + teal-tint #D6ECEF anonymized bubbles,
NO readable text. Canvas 3:2, off-white #FBFBFD, flat-vector Stripe/Linear register. NO people, no faces, no
readable UI text, no real logos. Typography: Inter/Söhne sentence case; exact strings only — "Session 1 -
today", "Persistent memory", "Session 2 - next week". Style negatives: NOT 3D/skeuomorphic/glossy/anime, no
clipart. Awwwards-quality 4k. (Full prompt inline in the draft placeholder.)
