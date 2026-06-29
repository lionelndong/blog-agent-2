# Visual types — controlled vocabulary

> **Governing spec: `templates/visual-strategy.md`.** That file decides *whether* a visual earns its
> place (need-driven, not a quota), *whose world* it shows (value-first ~80/20 — mostly third-party),
> and *what must never become a `[VISUAL:]`* (anything a native `:::` component renders). **Read it
> first.** This file is the controlled vocabulary that strategy uses — the `type` values, their
> fields, and the selection guide. `outline`, `draft`, and `generate-visuals` all reference both.

Single source of truth for the `[VISUAL:]` `type` vocabulary. Every visual planned in an outline and
placed in a draft must use one of the types below; the pipeline reads the `type` to decide how to
capture or generate the asset. **Stats, quotes, tables, and callouts are NOT visuals here — they are
native `:::` components** (see §0).

## 0. First gate — is this even a `[VISUAL:]`? (the anti-duplication rule)

The blog renders ~25 native `:::` directives inline. A native component is **always** better than a
PNG of the same content — selectable, accessible, SEO-readable, responsive. So before you reach for a
`[VISUAL:]`, check this table. **If the content is in the left column, emit the native directive and
do NOT make a `[VISUAL:]` of it** (`visual-strategy.md` §4 — the duplicate bug we are killing):

| If the content is… | Use the native directive — NEVER a `[VISUAL:]` |
|---|---|
| a statistic / number | `:::stat` · `:::stat-group` · `:::stat-list` |
| a quote | `:::pullquote` |
| a tip / note / warning / takeaway / definition | `:::tip` · `:::note` · `:::warning` · `:::nutshell` · `:::key-takeaways` · `:::definition` |
| a comparison / feature matrix / pros-cons / simple data table | `:::table` · `:::feature-matrix` · `:::decision-table` · `:::proscons` |
| a captioned figure (you already have a `src` on disk) | `:::figure` |
| FAQ / CTA | `:::faq` · `:::cta` |

**A `[VISUAL:]` PNG is ONLY for what text + natives can't show:** real **screenshots** (a third party,
a SERP, a Reddit/forum thread, an X/LinkedIn post, a real artifact — or our product *on-topic only*),
**charts** (branded, real data), **diagrams/flows** (the concept slot), the rare **cover**, **demos/
GIFs**, **embeds**. If you already authored the data as a `:::decision-table` or `:::table`, you may
**not** also ship a PNG table of it.

## 1. Value-first selection guide — whose world does it show? (~80/20)

Per the Ahrefs audit in `visual-strategy.md` §3 (107 images / 5 varied posts), **~80% of strong
visuals show a third party / the reader's world** and only ~20% the author's own product. Adopt this.
When a section does warrant a `[VISUAL:]`, pick the type that shows the **category**, not us, unless
the post is genuinely about Pleasur.ai:

| Section needs to show… | Value-first type (prefer) | Self type (only when on-topic about us) |
|---|---|---|
| proof a problem is real / widespread | `external` (Reddit/forum thread, a real review) | — |
| what a rival does (or does wrong) | `external;sub=competitor-ui` (the rival's UI) | — |
| how people search for the problem | `external;sub=serp` (Google SERP) | — |
| a real opinion / hot take | `external;sub=tweet\|linkedin` | — |
| a data trend / numeric comparison | `chart` (real data, often third-party) | `chart` (our metered numbers, if on-topic) |
| a concept / system / flow | `diagram` | `diagram` |
| a capability we uniquely solve | — | `screenshot` / `action-shot` (SFW, blurred) |

`type=external` is **the workhorse.** A reader who sees a competitor's UI, a real SERP, or a real
thread gets value whether or not they ever buy. The same method applies to **any** product a post
covers — if the post is about another tool, screenshot and annotate *that* tool.

## 2. Resolvable data — the hard rule for charts, diagrams, and data tables

A `chart` / `diagram` / data-driven visual **MUST** reference data that exists:

- a real **`research.<key>`** — and you must **verify the key is present** in
  `content-pipeline/1-research/{slug}-data.json` before using it, **or**
- a **`config=<file>`** you author (ApexCharts options for a chart; a `{direction,nodes,edges}` /
  nested-tree / cycle spec for a diagram).

**NEVER invent a key.** The failures this rule kills: `data=research.five_failure_taxonomy` and
`data=research.pricing.coin_tiers` when the real keys did not exist — the placeholder loud-failed and
left the section blank. If the data you want isn't in research, either add it to the research JSON,
author a `config=` file, or **drop the visual**. An unresolvable `[VISUAL:]` is a build failure, not a
soft skip.

## 3. The type catalog

| Type | When to use | Capture strategy |
|---|---|---|
| `external` | **The workhorse.** The section cites/shows something the brand doesn't own that adds *specific* value — a Reddit comment, a tweet, a LinkedIn post, a Google SERP, a chart in a news article, a competitor's UI panel, a real artifact. | Patchright headless capture of the URL clipped to a CSS `selector`. `crop=padded` adds breathing room. On Cloudflare / login-wall / nav-fail the entry stays `failed` with a `fallback.method=claude_in_chrome` breadcrumb so `/capture-visuals` retries via a real Chrome session. **No ToS bypasses** — if both paths fail, the entry stays `failed`. |
| `screenshot` | **Our product, on-topic posts only.** A section walks through a brand-owned UI at a **static, navigable URL** that renders the wanted state on load (or after one age-gate/cookie click). | Patchright headless capture (CF/bot bypass). May require auth (`setup_auth.py`). |
| `action-shot` | **Our logged-in product** in a state that only exists after a sequence of actions (a wizard, sending a message, opening settings, mid-form) — or when `screenshot` can't get past bot protection. **SFW: explicit tiles + PII blurred.** | Routed to `/capture-visuals` (Claude in Chrome on the VPS, real session, no token cost). Opt-in `BROWSER_USE_ENABLED=1` delegates to Browser Use Cloud. |
| `chart` | Quantitative data with trends/distributions/proportions. **Resolvable data only (§2).** | ApexCharts PNG (`render_chart_web.py`) from `data=research.<key>` or a `config=` options file. |
| `diagram` | A concept, mental model, workflow, or "how it works" — the **illustration slot** (no AI metaphor art). **Structured nodes only (§2)** — `linear` / `tree` / `flow` / `cycle` via `data=`/`config=`. | `render_diagram_web.py` (dagre). |
| `cover` | The article hero / featured image. | `render_cover.py` — 1600×900, real logo composited (covers carry no in-body logo per strategy §7). |
| `video` | A section embeds a video where motion is essential (a real demo, a YouTube/Loom clip). | Editor-managed embed URL → `<iframe>` / Strapi video block. Not auto-captured. |
| `gif` | An animated multi-step interaction text alone struggles to describe. | Editor-managed screen-recording source; ffmpeg conversion is a future enhancement. |
| `none` | The section is pure argument, a transition, or short — text alone carries it, or its value belongs in a native `:::` component. | Skip — no placeholder, no asset. **Most sections are `none`** (need-driven, not a quota). |

**`type=image` is RETIRED — do not plan it.** AI image generation is off (Ryan-faithful rebuild,
2026-06-25). For a concept use a `diagram`; for data use a `chart`; for real imagery use `external`
(third party) or `screenshot`/`action-shot` (our product, on-topic). If only a hand-made illustration
would truly do, use `none` and let an editor add one later.

## 4. Decision sequence (need-driven, per `visual-strategy.md`)

For each H2, ask **"would a visual here show the reader real value that text + native `:::` components
can't?"** (`visual-strategy.md` §2). If no — `none`. If yes, pick the type, biasing value-first:

1. Is the value **proof / a real example / a rival / how people search** for this? → `external`
   (the workhorse) — pair with `selector=` to clip to the exact element.
2. Is it our **own on-topic capability** the reader needs to see in our UI? → `screenshot` (static URL)
   or `action-shot` (needs clicks / SFW state).
3. Is it a **data trend / numeric comparison** backed by a real key or authored config? → `chart`.
4. Is it a **concept / system / flow**? → `diagram` (structured nodes).
5. Is it a **video/demo where motion is essential**? → `video` / `gif`.
6. Otherwise → `none`.

**There is NO minimum count, no "image every N words," and no "≥3 distinct types" quota.** A missing
visual always beats a weak or duplicate one. Under-showing a genuine value-moment and over-showing
filler are *both* failures — need is the only bar. Never stack two visuals back-to-back.

## `screenshot` vs `action-shot` — the key distinction

The two are easy to confuse. Mistakes here are the most common reason a visual fails or comes back wrong.

**Choose `screenshot` when:**
- The URL renders the wanted state directly. Open URL → see the thing.
- Optional: a single age-gate or cookie banner dismissal is needed (the static dispatcher handles those automatically).
- Cost: free (runs on your VPS).

**Choose `action-shot` when:**
- The reader needs to see what it looks like *after* a click/type/wait sequence. The state isn't reachable by URL alone.
- Or: the page IS at a static URL but the site's bot protection is too aggressive for `screenshot` (Cloudflare Pro, DataDome, etc.).
- Cost: **free.** Routed to `/capture-visuals`, which drives the VPS's always-on Chrome via the Claude in Chrome MCP — uses your real Chrome session, your subscription, your IP. No token billing, no per-task fees. (Opt-in: set `BROWSER_USE_ENABLED=1` to delegate to the Browser Use Cloud agent instead at ~$0.05–$0.15/visual; rarely needed.)
- Model: always **Sonnet 4.6** (`claude-sonnet-4-6`). Browser driving is high-throughput / low-reasoning, and Opus is wasted spend here.

**Examples that map clearly:**

- `pleasur.ai/create` (templates grid, default state) → `screenshot`
- `pleasur.ai/create` after picking Realistic and reaching the Ethnicity step → `action-shot`
- A chat conversation in mid-flow with the typing indicator visible → `action-shot`
- A privacy settings panel with all toggles enabled → `action-shot`
- A static feature page on the marketing site → `screenshot`
- A competitor's product UI behind their bot wall → `action-shot` (when ToS allows) or `external` with the Claude-in-Chrome fallback

## SFW / adult content rule (Pleasur.ai specific)

The product is adult, but **every published visual must be SFW** for ad-network, embed, and
search-index compatibility:

- Any `action-shot` / `screenshot` of the logged-in product runs with PII redaction on (email masked)
  and **explicit image tiles blurred in place** (`VISUAL-CRITIQUE-LOOP.md` action-shot checklist).
- Never depict nudity, suggestive contact, or skin-focus in a published asset — frame the *capability*
  (the memory panel, the voice control, the pricing meter), not explicit content.
- AI generation is retired, so the old "route adult prompts to manual" path is moot — there is no
  Replicate call to refuse. If a SFW capture of an inherently adult screen isn't achievable, use
  `none` rather than ship something risqué.

## Placeholder syntax (for `/draft`)

The draft realizes the outline's typed `Visual N:` plan as a single typed placeholder per planned
visual. Format:

```
[VISUAL:type=<type>;<key>=<value>;<key>=<value>...]
```

### Examples (value-first first — `external` is the workhorse)

```
[VISUAL:type=external;sub=reddit-comment;url=https://www.reddit.com/r/AICompanions/comments/<id>/;selector=#t1_<comment-id>;crop=padded;what=Top reply: a companion app forgot the user after a week]

[VISUAL:type=external;sub=competitor-ui;url=https://competitor.example.com/chat;selector=.message-list;crop=padded;what=Rival app repeating the same stock reply]

[VISUAL:type=external;sub=serp;url=https://www.google.com/search?q=ai+companion+forgets+conversations;selector=#search;crop=padded;what=Google SERP for the memory complaint]

[VISUAL:type=external;sub=tweet;url=https://x.com/<user>/status/<id>;selector=article[data-testid="tweet"];crop=padded;what=User's hot-take on hidden AI-companion pricing]

[VISUAL:type=screenshot;target=chat;what=the memory panel recalling a fact from a prior session unprompted;annotate=#recalled-detail]

[VISUAL:type=action-shot;url=https://pleasur.ai;goal=Log in with the saved session. Open an existing character chat. Tap the speaker icon next to a reply. Capture the chat with the voice control active.;what=In-chat voice playback control]

[VISUAL:type=chart;data=research.search_volumes;style=bar;title=Monthly searches by platform]

[VISUAL:type=diagram;type=cycle;config=content-pipeline/images/<slug>/context-churn.json;what=The context-churn loop]

[VISUAL:type=video;url=https://youtube.com/watch?v=<id>;what=demo of voice reply tap-to-play]
```

Tables are not placeholders — author them as native `:::table` / `:::decision-table` / `:::feature-matrix` (§0).

### `external` placeholder fields (the workhorse — PLEAA-417)

`external` is the right type when the section *quotes* or *cites* something the brand doesn't own and
the visual evidence is a specific element on that page — a single Reddit comment, a tweet, a SERP, a
chart inside an article, a competitor panel. **Always pair with `selector`** to clip to the element; a
viewport-sized screenshot of a whole thread is wasted space.

| Field | Required | Purpose |
|---|---|---|
| `url` | yes | Source URL. Reachable without login when possible; if login-walled, the entry falls back to `/capture-visuals` (real Chrome session). |
| `selector` | strongly recommended | CSS selector clipping to the element that matters. Reddit comment IDs (`#t1_<id>`), tweet `article[data-testid="tweet"]`, SERP `#search`/`#rso`, news `figure.chart`, competitor `.pricing-table`/`.message-list`. |
| `sub` | recommended | `reddit-comment`, `tweet`, `linkedin`, `news-quote`, `competitor-ui`, `serp`, `chart`. |
| `crop` | no | `padded` (default for external, ~48px) or `tight` (~8px). Or `X,Y,W,H` for a manual rectangle. |
| `what` | yes | Short caption / alt text. |
| `validate` | no | `validate=true` adds a Claude-vision sanity check (~$0.003/capture). |

**Sub-type cheatsheet:**

- `sub=reddit-comment` — `selector=#t1_<base36-comment-id>`. Old Reddit (`old.reddit.com`) renders cleaner; prefer it. **Blur usernames/PII.**
- `sub=tweet` — `selector=article[data-testid="tweet"]`. X login-gates many pages; expect the Claude-in-Chrome fallback.
- `sub=serp` — `selector=#search` or `#rso` (the results column). Blur any personalized/PII chrome.
- `sub=competitor-ui` — `.pricing-table`, `.message-list`, `.feature-grid`, etc. ToS check before scraping; if the competitor blocks bots, use the Claude-in-Chrome fallback, never a proxy/CAPTCHA bypass.
- `sub=news-quote` / `sub=chart` — `figure.chart`, `.embedded-chart`, `.article__pull-quote`; inspect the page first.

**ToS rule:** we don't bypass site protections. If both Playwright and Claude-in-Chrome fail, the
entry stays `failed` and the visuals gate records it — do not chain proxies, solve CAPTCHAs, or scrape
rate-limited APIs to force a pass.

### `action-shot` placeholder fields

| Field | Required | Purpose |
|---|---|---|
| `goal` | yes | Natural-language description of the full sequence: navigation + actions + what to capture. Be specific about which screen to land on. |
| `url` | recommended | Starting URL. Speeds up the agent (skips a search step). |
| `what` | yes | Short caption / alt text. |
| `max_steps` | no | Override default of 25. Lower for simple tasks, higher for complex flows. |
| `llm` | no | Override default `claude-sonnet-4-6`. |

### Targeting and quality (`screenshot` / `external`)

A screenshot of a whole viewport is rarely the right capture. Specify what to clip to:

| Directive | When to use | Example |
|---|---|---|
| `selector=<css>` | The thing you want is a specific element (a card, a panel, a post, a Reddit comment, a tweet). Clipped to that element's bbox. | `selector=.companion-card[data-id="123"]` |
| `crop=padded` / `crop=tight` | With `selector`, expand the bbox by ~48px (padded) or ~8px (tight). Padded is the right default for external. | `selector=#t1_xyz;crop=padded` |
| `crop=X,Y,W,H` | No clean selector, but you know the rectangle (CSS pixels, pre-2× scale). | `crop=0,0,1440,720` |
| `annotate=<css>` | Highlight an element (selective — one box + one arrow + a short brand-blue label, per strategy §7). Independent of selector. | `annotate=#voice-button` |
| (none) | Whole 1440×900 viewport. Use sparingly — usually you want a selector. | — |

### Quality validation (post-capture)

Every screenshot capture runs heuristic checks automatically:

- **Final URL didn't redirect to login** — catches expired auth
- **Image dimensions sane** — catches render failures
- **Color variance > 0.02** — catches blank / mostly-uniform captures (login walls, white screens)
- **File size > 5KB** — catches truncated writes

If a check fails → the entry is recorded `failed`/`manual` for `/capture-visuals`. Low-variance →
captured but flagged. Set `validate=true` (or `VISUAL_VALIDATION=true`) to add a Haiku vision check
(~$0.003) that confirms the image shows what `what=` said.

## Backwards compatibility

The pipeline still accepts the legacy `[SCREENSHOT: description]` form; `/generate-visuals` treats it
as `[VISUAL:type=screenshot;what=description]`. New outlines and drafts use the typed form.

## Quality bar per type

| Type | Minimum quality |
|---|---|
| `external` / `screenshot` | clipped to the right element, 2× retina, tight chrome-free crop, PII + explicit blurred |
| `action-shot` | real logged-in product (not a login wall / age gate), SFW, email masked, ~2880 wide desktop |
| `chart` | min 1200px wide, on-brand palette, axis labels + title, numbers match the source |
| `diagram` | structured nodes, on-brand theme, no clipped labels |
| `cover` | exactly 1600×900, exact title in safe-zone, real logo |
| `gif` / `video` | editor-managed; pipeline doesn't enforce |

Every visual gets a markdown caption / alt text derived from `what=`. Captions are part of the
publishable output. **Every captured visual passes `VISUAL-CRITIQUE-LOOP.md`** (the agent *views* it
and redoes until it's genuinely good) before publish — a wasted render is cheap, a weak published
visual is not.
