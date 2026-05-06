# Visual types — controlled vocabulary

Single source of truth for visual placement decisions across the pipeline. Every visual planned in an outline must use one of the `type` values below. The pipeline reads the type to decide how to capture or generate the asset.

## The 9 types

| Type | When to use | Capture strategy |
|---|---|---|
| `screenshot` | Section walks through a brand-owned product UI at a **static, navigable URL**. The page renders the wanted state immediately on load (or after a known modal dismissal). No multi-step interaction required. | Patchright headless capture (Playwright fork with CF/bot bypass). May require auth (`setup_auth.py`). |
| `action-shot` | Section needs the UI in a state that **only exists after a sequence of actions** — clicking through a wizard, sending a message in a conversation, opening settings, dismissing a non-trivial modal, mid-form state. Also the right tool when `screenshot` can't get past the site's bot protection. | Default: routed to `manual-capture.md` for the editor to handle interactively via `/capture-visuals` (driven by Claude in Chrome — full visibility and control, no token cost, uses the editor's real Chrome session). Opt-in agent fallback: set `BROWSER_USE_ENABLED=1` to delegate to Browser Use Cloud (~$0.05–$0.15/visual). |
| `image` | Section makes an aesthetic / lifestyle / mood / conceptual point that benefits from visual context. **SFW only.** | AI-generated via Replicate. Default model `openai/gpt-image-2`, backup `google/nano-banana`. |
| `table` | Section compares N items across M dimensions, or presents structured comparison data. | Inline markdown table — no asset file. The draft writes the table directly. |
| `chart` | Section presents quantitative data with trends, distributions, or proportions (search volumes, percentages, rankings). | matplotlib PNG rendered from data in the research dossier. |
| `video` | Section references an embedded video (YouTube, Loom, screen recording, demo). | Editor-managed: provide an embed URL; rendered as `<iframe>` or Strapi video block. Not auto-captured. |
| `external` | Section references something the brand doesn't own that adds *specific* value — a Reddit comment we cite, a tweet, a chart in a news article, a competitor UI panel, a third-party tool screen. **PLEAA-417 (2026-05-06): auto-captured by default**, not routed to manual. | Patchright headless capture of the URL plus a CSS `selector` that clips to the relevant element (the comment, the tweet, the chart). `crop=padded` adds breathing room around the bbox. On Cloudflare / login-wall / nav-fail, the manifest entry stays `failed` with a `fallback.method=claude_in_chrome` breadcrumb so `/capture-visuals` retries via a real Chrome session. ToS bypasses (puzzle-solving, IP rotation chains) are out of scope: if both paths fail, the entry stays `failed` and the visuals gate halts. |
| `gif` | Section needs an animated GIF for a multi-step interaction text alone struggles to describe. | Editor-managed: provide a screen-recording source; ffmpeg conversion is a future enhancement. |
| `none` | Section is foundational, conceptual, or argumentative — a forced visual would dilute it. | Skip — no placeholder rendered, no asset generated. |

## Decision rule (one-pass check)

For each H2 section in an outline, ask in this order:

1. Does the section walk through a **brand product UI at a static URL**, where the wanted state is visible on first load (or after one age-gate/cookie click)? → `screenshot`
2. Does the section need a UI state that **only exists after multi-step interaction** (clicks through a wizard, sending messages, opening settings, mid-form state)? → `action-shot`
3. Does the section **compare N things on M axes**? → `table`
4. Does the section present **quantitative data with trends**? → `chart`
5. Does the section **reference a third-party artifact** (a Reddit comment we quote, a tweet, a chart in a news article, a competitor UI panel)? → `external` — pair with `selector=` so we capture the exact element, not the whole page. Use `action-shot` instead only when the artifact is reachable just from a multi-step flow (logged-in dashboard, after-click state).
6. Does the section need an **animated multi-step demo**? → `gif`
7. Does the section embed a **video / demo**? → `video`
8. Would an **aesthetic / mood / lifestyle illustration** add real value, SFW? → `image`
9. Otherwise → `none` — argue with prose, not pictures

The default for sections that don't have an obvious match is `none`. A forced visual is worse than no visual.

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
- Model: always **Sonnet 4.6** (`claude-sonnet-4-6`). Browser driving is high-throughput / low-reasoning, and Opus is wasted spend here. The VPS systemd unit and cron triggers pin `--model claude-sonnet-4-6` for the same reason.

**Examples that map clearly:**

- `pleasur.ai/create` (templates grid, default state) → `screenshot`
- `pleasur.ai/create` after picking Realistic and reaching the Ethnicity step → `action-shot`
- A chat conversation in mid-flow with the typing indicator visible → `action-shot`
- A privacy settings panel with all toggles enabled → `action-shot`
- A static feature page on the marketing site → `screenshot`
- A competitor's product UI behind their bot wall → `action-shot` (when ToS allows)

## SFW / adult content rule (Pleasur.AI specific)

Replicate's `openai/gpt-image-2` and `google/nano-banana` will refuse adult prompts and may flag the API account. For visuals that depict adult content (companion characters in suggestive scenarios, etc.):

- Use `safety=adult` in the placeholder
- The pipeline routes the placeholder to `manual-capture.md` — the editor produces the image manually using the brand's own tooling at `pleasur.ai/generate`
- **Never** call Replicate with adult prompts, even if `safety` is unset and the prompt happens to imply adult content

Default for any `image` placeholder is `safety=sfw`. Most blog illustrations should be SFW (lifestyle, abstract, scene-setting, no people) — that also keeps the published article SFW for ad-network and embed compatibility.

## Placeholder syntax (for `/draft`)

The draft realizes the outline's typed `Visual:` block as a single typed placeholder per section. Format:

```
[VISUAL:type=<type>;<key>=<value>;<key>=<value>...]
```

### Examples

```
[VISUAL:type=screenshot;target=create;what=character backstory & traits panel;selector=.backstory-panel;annotate=#voice-button]

[VISUAL:type=screenshot;target=create;what=top-of-page hero with sign-up CTA;crop=0,0,1440,720]

[VISUAL:type=action-shot;url=https://pleasur.ai/create;goal=Navigate to pleasur.ai/create. Dismiss the age verification dialog. Click the Realistic template card. Wait for the Ethnicity selection step to load. Capture that screen.;what=Companion Creator Ethnicity step]

[VISUAL:type=action-shot;url=https://pleasur.ai;goal=Log into Pleasur with the saved session. Open an existing character chat. Send the message "Tell me about your day." Wait for the typing indicator to appear and the response to arrive. Capture the chat with the response visible.;what=Mid-conversation chat with typing indicator and response]

[VISUAL:type=image;prompt=modern apartment interior with warm evening light, no people;style=photorealistic;safety=sfw]

[VISUAL:type=image;prompt=portrait of a custom-designed companion character;safety=adult]

[VISUAL:type=chart;data=research.search_volumes;style=bar;title=Monthly searches by platform]

[VISUAL:type=video;url=https://youtube.com/watch?v=<id>;what=demo of voice reply tap-to-play]

[VISUAL:type=external;sub=reddit-comment;url=https://www.reddit.com/r/AICompanions/comments/<id>/;selector=#t1_<comment-id>;crop=padded;what=Top reply on memory-limit complaints]

[VISUAL:type=external;sub=tweet;url=https://x.com/<user>/status/<id>;selector=article[data-testid="tweet"];crop=padded;what=User's hot-take on AI girlfriend pricing]

[VISUAL:type=external;sub=news-quote;url=https://example.com/article;selector=figure.chart;crop=tight;what=Chart of monthly active users by AI companion app]

[VISUAL:type=external;sub=competitor-ui;url=https://competitor.example.com/pricing;selector=.pricing-table;crop=padded;what=Competitor pricing tiers]
```

Tables are not placeholders — `/draft` writes them inline as markdown.

### `action-shot` placeholder fields

| Field | Required | Purpose |
|---|---|---|
| `goal` | yes | Natural-language description of the full sequence: navigation + actions + what to capture. Be specific about which screen to land on. |
| `url` | recommended | Starting URL. Speeds up the agent (skips a search step). |
| `what` | yes | Short caption / alt text. Used for the published image. |
| `max_steps` | no | Override default of 25. Lower for simple tasks (saves $), higher for complex flows. |
| `llm` | no | Override default `claude-sonnet-4-6`. Try `gpt-4.1-mini` for cheaper / faster on simple tasks. |

### `external` placeholder fields (PLEAA-417)

`external` is the right type when the section *quotes* or *cites* something the brand doesn't own and the visual evidence is a specific element on that page — a single Reddit comment, a tweet, a chart inside an article, a competitor pricing tier. Always pair with `selector` to clip to the element; a viewport-sized screenshot of a Reddit thread is wasted space.

| Field | Required | Purpose |
|---|---|---|
| `url` | yes | Source URL. Must be reachable without login when possible; if login-walled, the manifest entry will fall back to `/capture-visuals` (real Chrome session). |
| `selector` | strongly recommended | CSS selector clipping to the element that matters. Reddit comment IDs (`#t1_<id>`), tweet `article[data-testid="tweet"]`, news `figure.chart`, competitor `.pricing-table`. |
| `sub` | recommended | One of `reddit-comment`, `tweet`, `news-quote`, `competitor-ui`, `chart`. Free-form metadata today; future heuristics may auto-pick selectors per sub. |
| `crop` | no | `padded` (default for external, ~48px breathing room around the bbox) or `tight` (~8px). Or `X,Y,W,H` for a manual rectangle if no selector works. |
| `what` | yes | Short caption / alt text. Used for the published image. |
| `validate` | no | Set `validate=true` to add a Claude-vision sanity check (~$0.003/capture). |

**Sub-type cheatsheet:**

- `sub=reddit-comment` — `selector=#t1_<base36-comment-id>` (the data-fullname suffix on the comment node). Old Reddit (`old.reddit.com`) renders cleaner than new Reddit; prefer it when you can.
- `sub=tweet` — `selector=article[data-testid="tweet"]`. X/Twitter login-gates many pages; expect the Claude-in-Chrome fallback to handle most of these.
- `sub=news-quote` — selectors vary by publication. `figure.chart`, `.embedded-chart`, `.article__pull-quote` are common starting points; inspect the page first.
- `sub=competitor-ui` — `.pricing-table`, `.feature-grid`, etc. ToS check before scraping; if competitor blocks bots aggressively, flag and use a manual capture.
- `sub=chart` — when the source is a chart (vs the page that hosts it). Often the same selector as `news-quote` with a tighter crop.

**ToS rule:** we don't bypass site protections. If both Playwright and Claude-in-Chrome fail, the entry stays `failed` and the visuals gate halts — do not chain proxies, solve CAPTCHAs, or scrape rate-limit-protected APIs to make it pass.

## Targeting and quality (`screenshot` and `external`)

A screenshot of a whole viewport is rarely the right capture. Specify what to clip to:

| Directive | When to use | Example |
|---|---|---|
| `selector=<css>` | The thing you want to show is a specific element on the page (a card, a panel, a single post, a Reddit comment, a tweet). The capture is clipped to that element's bounding box. | `selector=.companion-card[data-id="123"]` |
| `crop=padded` / `crop=tight` | With `selector`, expand the bbox by ~48px (padded) or ~8px (tight) before clipping. Padded is the right default for external visuals — bbox-tight Reddit/tweet captures look cramped. | `selector=#t1_xyz;crop=padded` |
| `crop=X,Y,W,H` | No clean selector is available, but you know the rectangle. Coordinates in CSS pixels (pre-2x scale). | `crop=0,0,1440,720` (top-of-viewport hero) |
| `annotate=<css>` | Highlight an element with a red outline before capture. Independent of selector — you can highlight one thing inside a larger element. | `annotate=#voice-button` |
| (none) | Capture the whole 1440×900 viewport. Use sparingly — usually you want a selector. | — |

### Quality validation (post-capture)

Every screenshot capture runs heuristic checks automatically:

- **Final URL didn't redirect to login** — catches expired auth
- **Image dimensions sane** — catches render failures
- **Color variance > 0.02** — catches blank / mostly-uniform captures (login walls, white screens)
- **File size > 5KB** — catches truncated writes

If a check fails → the visual is flagged in `manual-capture.md` for the editor to handle. If it's "suspect" (low color variance) → captured but flagged for review.

### Optional vision validation

Set `validate=true` on the placeholder (or `VISUAL_VALIDATION=true` env var) to additionally ask Claude (Haiku) to look at the image and verify it shows what `what=` said it would. Costs ~$0.003/check; off by default. Catches subtler failures the heuristics miss (e.g., the page rendered a different feature than expected).

```
[VISUAL:type=screenshot;target=create;what=companion creator backstory panel;selector=.create-panel;validate=true]
```

## Backwards compatibility

The pipeline still accepts the legacy `[SCREENSHOT: description]` form. `/generate-visuals` treats it as `[VISUAL:type=screenshot;what=description]`. New outlines should use the typed form.

## Quality bar per type

| Type | Minimum quality |
|---|---|
| `screenshot` | 1440×900 viewport, 2× retina (2880×1800 PNG), Pillow-optimized |
| `image` | 1024×1024 minimum (model default); upscale only if model supports it |
| `chart` | Min 1200px wide, brand-neutral palette, axis labels & title |
| `gif` / `video` | Editor-managed quality; pipeline doesn't enforce |

Every visual gets a markdown caption / alt text derived from the placeholder's `what=` or `prompt=` field. Captions are part of the publishable output, not an afterthought.
