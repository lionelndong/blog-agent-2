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
the reader's world** (competitor tools, Google SERPs, Reddit/forums, real emails, real examples) and only
~20% their own product — and the lone self-heavy post is one literally *about* their tools.

**Adopt this.** Unless the post is genuinely about Pleasur.AI, most visuals should show the **category /
world** — competitor companion apps, real chat patterns, SERPs, market data, Reddit/X discussions.
Reserve our-product shots for on-topic moments. **The same method applies to *any* product the post is
about** — if the post is about another tool, screenshot and annotate *that* tool. A reader who screenshots
a competitor's UI, a SERP, or a real thread gets value whether or not they ever buy.

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

- `type=external;sub=reddit-comment|tweet|linkedin|news-quote|competitor-ui|serp;url=…;selector=…;crop=padded` — **the workhorse.** Screenshot the real third-party thing. (Reddit comment `#t1_<id>`; tweet `article[data-testid="tweet"]`.)
- `type=screenshot;target=<product-slug>;what=…` — our product, **on-topic posts only**.
- `type=action-shot;url=…;goal=…;what=…` — logged-in product, **SFW (blur explicit + PII)**.
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
- **Annotation is selective** — only where the eye needs guidance. Self-evident charts get **zero**.
  When used: a box + **one** bold arrow + a short label (brand blue), never a cluttered swarm.
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
