# Visual strategy — when a visual earns its place

> This is the core of blog quality. The `outline` skill decides **where + why** each visual
> belongs; the `draft` skill **places** it; `generate-visuals` realizes it. All three follow this.
> **Quality is the only metric.** Spend whatever time it takes to find or make the *right* visual —
> a missing visual always beats a weak or duplicate one.

## 1. Not a quota — need-driven

There is **NO "image every N words."** A visual appears **only where a specific moment needs one**.
Most paragraphs get none. Never stack two visuals back-to-back — give them room so each feels earned.
**If you can't name the concrete value a visual adds *right here*, don't place it.** (We carry *more*
visuals than past posts only because those posts *missed* real value-moments — fix the misses, never
manufacture filler.)

**Calibration (this matters — we've been UNDER-visualizing).** Ahrefs runs roughly **1 visual per
150–200 words — ~15–25 in a long guide** — because they *show nearly everything they reference*: every
tool they name, every data point, every process, every real artifact. So a 2,500-word post with 4
visuals is **under-visualized, not tastefully restrained.** The discipline is "no filler," NOT "few
visuals": if a paragraph names a showable thing (a tool, a screen, a number, a process, a real example),
that *is* a value-moment — show it. Aim to match Ahrefs' density with real, earned visuals; a sparse
post reads thinner and less credible than the SERP winners we're trying to beat.

## 2. The trigger — value the reader can SEE

Place a visual when a section does one of these **and text alone leaves value on the table**:
- **A claim that proof would strengthen** → screenshot the real evidence (a Google SERP, a Reddit/forum
  thread, a real review, a competitor's page, a tweet, a data source). *Show it; don't just assert it.*
- **A process / how-to** → an annotated screenshot of the actual steps, or a clean diagram.
- **Data / a trend / a numeric comparison** → a branded chart.
- **A concept / system / flow** → a clean labeled diagram.
- **An on-topic product capability** → a real (SFW, blurred) product shot or short demo.
- **A referenced external artifact** → screenshot it instead of describing it.

Pure argument, transition, or text the reader simply reads → **no visual**.

## 3. Value-first — mostly the reader's world, not us (~80/20)

Evidence (Ahrefs audit, 107 images / 5 varied posts): **~80% of their visuals are about a third party /
the reader's world** and only ~20% their own product — the lone self-heavy post is one literally *about*
their tools.

**But "third party" is NOT "Google + Reddit" — that's the mistake to avoid.** The actual Ahrefs mix:
**screenshots of the specific tools/products/sites the post discusses ~30% + their own product ~21% +
charts of real data ~17% + real emails/artifacts ~14% + other real websites ~8% + diagrams ~5% —
Google SERP only ~4%, Reddit a small slice.** So the **default visual for a point is a screenshot of the
specific thing that point is about** (the competitor app you're comparing, the exact feature you're
explaining, the real review/artifact you reference) — or a **chart** when the point is data, or a
**diagram** when it's a concept/flow. A **Google SERP or a Reddit/forum thread is occasional (~a few %) —
use it ONLY when a search result or a real user's own words *is* the point, never by reflex and never as
filler.** If most of a post's visuals are SERPs and Reddit, the type selection is wrong: go screenshot the
actual tools, features, and artifacts instead.

**Adopt this.** Unless the post is genuinely about Pleasur.AI, most visuals should show the **category /
world** — competitor companion apps, real chat patterns, SERPs, market data, Reddit/X discussions.
Reserve our-product shots for on-topic moments. **The same method applies to *any* product the post is
about** — if the post is about another tool, screenshot and annotate *that* tool. A reader who screenshots
a competitor's UI, a SERP, or a real thread gets value whether or not they ever buy.

The point of the ~80% is **showing the reader's WORLD and giving real VALUE — not any one source.**
**A Google SERP is just ONE source among many** — Reddit/forum threads, a competitor's UI, real
reviews/examples, news, other tools, real artifacts all count equally. **Vary the sources** and pick
whichever best proves *this* point; don't reach for a SERP by reflex. **No single-source over-reliance —
e.g. don't fill a post with Google SERP screenshots.** (The Ahrefs "show the world" idea is illustrated
*with* SERPs; it is not a mandate to *use* SERPs — it means show evidence from the reader's world,
whatever form that takes.)

## 4. Never duplicate a native component (hard rule — the duplicate bug)

The blog renders ~25 native `:::` directives inline (see `examples/component-cheatsheet.md`). A native
component is **always** better than a PNG of the same thing — selectable, accessible, SEO-readable,
responsive. So:

| If the content is… | Use the native directive — NEVER a `[VISUAL:]` |
|---|---|
| a statistic / number | `:::stat` · `:::stat-group` · `:::stat-list` |
| a quote | `:::pullquote` |
| a tip / note / warning / takeaway / definition | `:::tip` · `:::note` · `:::warning` · `:::nutshell` · `:::key-takeaways` · `:::definition` |
| a comparison / feature matrix / pros-cons / simple data table | `:::table` · `:::feature-matrix` · `:::decision-table` · `:::proscons` |
| a captioned figure (you already have a src) | `:::figure` |
| FAQ / CTA | `:::faq` · `:::cta` |

**`[VISUAL:]` PNGs are ONLY for what text + natives can't show:** real **screenshots** (product *on-topic
only* / competitors / Google SERP / Reddit/forum / X / LinkedIn / real artifacts), **charts** (branded,
real data), **diagrams/flows**, the rare **illustration** (= a clean labeled *diagram*, never AI metaphor
art), **covers**, **demos/GIFs**, **embeds**.

## 5. The `[VISUAL:]` type catalog

- `type=external;sub=competitor-ui|reddit-comment|tweet|linkedin|news-quote|serp;url=…;selector=…;crop=padded;annotate=<what to point out>` — screenshot a real third-party thing. **Reach for it to show the SPECIFIC tool/site/artifact the point is about** (a competitor app you're comparing via `sub=competitor-ui`, a real review, a genuine forum thread) — this, alongside our-product `type=screenshot`, `type=chart`, and `type=diagram`, is where the bulk of visuals come from (see §3). **`sub=serp` and `sub=reddit-comment` are OCCASIONAL — use only when a search result or a real user's words IS the point; do NOT default to them or fill a post with them.** (Reddit comment `#t1_<id>`; tweet `article[data-testid="tweet"]`.) `annotate=` = the one thing this screenshot proves; run it through `annotate_screenshot.py`.
- `type=screenshot;target=<product-slug>;what=…;annotate=<what to point out>` — our product, **on-topic posts only**. `annotate=` names the specific point to emphasize; realize it via `annotate_screenshot.py`.
- `type=action-shot;url=…;goal=…;what=…;annotate=<what to point out>` — logged-in product, **SFW (blur explicit + PII)**. `annotate=` = the point the shot makes; run it through `annotate_screenshot.py`.
- `type=chart;data=research.<KEY-THAT-EXISTS>|config=<file>;style=…;title=…` — branded chart from **real** data.
- `type=diagram;type=linear|tree|flow|cycle|config=<file>` — concept/process/decision (the "illustration" slot).
- `type=cover` · `type=demo`/`gif` · embeds (real live, only where genuinely valuable — a tweet/video).

## 6. Resolvable data (hard rule — kills the invented-key bug)

A chart / table / diagram **MUST** reference data that exists: a real `research.<key>` (verify it is in
the research JSON) or a `config=<file>` you author. **NEVER invent a key** (the failure we found:
`five_failure_taxonomy`, `pricing.coin_tiers` when the real keys were `pleasurai_*_by_tier`). If the data
you want isn't in research, either add it to the research data, author a config file, or drop the visual.
An unresolvable `[VISUAL:]` loud-fails and leaves the section blank — that is the bug we are killing.

## 7. Taste — the front door

- **Tight, chrome-free crops; retina (2×).** Let the third-party tool's *own* UI do the work — frame it
  cleanly, don't re-skin it.
- **SERP captures — crop to the search bar (query visible) + the AI Overview / results, nothing else.**
  Keep the Google search box *with the query showing* at the top (it sets the context), then go straight
  into the AI Overview and organic results. **Trim the result-type tab-nav row** (`All / Images / Videos /
  News / Forums / Shopping / More / Tools`) and **any empty top space** — keep only what's important. If a
  single selector won't do it, composite two bands (search-bar strip + AI-Overview-onward strip) so the
  tab-nav row is dropped; the seam reads as a clean white gutter. Same principle for any third-party
  capture: clip to the element that carries the value (the comment, the tweet, the panel, the chart), not
  the page chrome around it.
- **Capture product / app screenshots in their NATURAL proportions — let the UI dictate.** A chat / app
  view is fine as it renders (a mobile chat is naturally tall, a desktop panel naturally wider); frame on
  the relevant UI (the memory panel, the speaker/Listen reply, the pricing meter) and trim the dead bottom
  chrome (composer / nav rail / empty scroll). **Do NOT force a wide landscape crop** — it looks unnatural
  on app UIs — and **do NOT force a square**. Match the app's own shape; use the device frame for an
  intimate mobile chat and a plain/browser frame for a desktop panel.
- **The branded frame is the DEFAULT, not mandatory.** The white-card / browser-chrome frame with the
  real logo + caption looks polished and on-brand — keep it as the default for product/feature shots. But
  it's **optional**: a clean frameless / raw screenshot is fine when it simply reads better. Vary it; don't
  force the frame on every shot. (`action_shot.py --frame plain|browser|device|none`; `--no-logo` drops the
  logo.)
- **Public-blog content is SFW even though the product is adult.** Every captured frame must contain **zero
  suggestive/flirty/explicit text or imagery** — it's a public, indexed page. Our companion characters and
  the character-creation flow are adult by default, so don't capture them raw: steer a chat to strictly
  professional content (a hard custom-instruction + clean prompts, regenerate any drift), hide the
  conversation-list / persona side-panels that carry flirty snippets, scroll past any suggestive opener, and
  **view the final frame** to confirm it's clean before shipping. A missing shot beats a risqué one.
  **The engine now ENFORCES this: every `type=external` and `type=screenshot` capture is AUTO-BLURRED**
  (explicit `img`/`video` blurred in place; logos/labels/UI stay sharp) and **size-capped** (no 4,000px
  full-page). Opt out with `blur=off` ONLY for a genuinely text/SFW surface (a pricing/FAQ page). Still your
  job: give a **TIGHT `selector`** so the shot clips to the relevant element — a broad `body`/`main`
  selector trips the size backstop and reads as a bad full-page grab. For a drawn **callout** (box + arrow +
  label pointing at the one thing), use **`type=annotation`** (also auto-blurred now) with a real target
  `selector` — the `annotate=` text on a plain `type=external`/`type=screenshot` is a written hint, NOT a
  drawn overlay, so it will not appear on the image.
- **Annotate SCREENSHOTS by default; leave self-evident visuals clean.** A bare screenshot is vague —
  the reader doesn't know where to look. So **most screenshots** (SERPs, our product UI, competitor UIs,
  third-party artifacts) should carry a **light annotation that POINTS OUT the one thing the screenshot
  proves** — an arrow / highlight / box / short marker label, in **brand blue**, via the annotation engine
  `annotate_screenshot.py` (blue C/bold arrow · box · highlight · marker label, DOM-bbox precise). This is
  how Ahrefs does it: an arrow or marker text calls out exactly what they're showing. **The EXCEPTION is
  self-evident visuals** — clean charts, diagrams, designed cards — which **need NO annotation; don't
  annotate the already-obvious.** Net rule: **annotate screenshots to direct the eye; leave self-evident
  visuals clean.** When you annotate, stay minimal — a box + **one** bold arrow + a short label, never a
  cluttered swarm (`VISUAL-CRITIQUE-LOOP.md` enforces "one clean callout, not a swarm").
- **Always blur PII** (emails, names) and any explicit imagery.
- On-brand (palette, IBM Plex title / Geist body, real logo where appropriate; covers carry **no** logo).
- Every visual passes `VISUAL-CRITIQUE-LOOP.md` — the agent **views** it and redoes until it's genuinely
  good. A wasted render is cheap; a weak published visual is not.

## 8. Where this is enforced

- **`outline`** (4-outlines-annotated): for each section, ask *"would a visual here show the reader real
  value that text + native components can't?"* Only then plan one — naming its **purpose**, the
  **value-first source** (prefer third-party/world), and the **type**. Plan native directives for
  stats/quotes/tables/callouts. Don't plan filler.
- **`draft`**: place the typed `[VISUAL:]` per the plan, at natural breaks, with **resolvable data**, the
  right **type**, and **no native-component duplication**.
- **`generate-visuals`**: realizes each; the critique loop is mandatory before publish.
