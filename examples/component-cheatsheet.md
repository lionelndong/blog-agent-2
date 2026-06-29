# Component cheatsheet — the writer's menu

This is the menu `/outline` and `/draft` consult. It answers one question fast: **when do I reach for a component, and exactly how do I write it?** (The full markup/render spec lives in `ahrefs-components.md` — that's the frontend's contract, not yours.)

## The three rules (read first)
1. **Components are scannability tools, never decoration.** A section earns one only when its content genuinely calls for it. Most sections use NONE. A whole article may use two or three — or, like plenty of Ahrefs posts, none at all.
2. **Designed-in at the outline, emitted in the draft.** `/outline` decides which (if any) component each section carries — the same way it decides where to mention the product. `/draft` then writes them. Don't bolt them on mid-draft.
3. **Stay under the caps** (bottom of this file). The pre-publish checker enforces them — an over-decorated or malformed article won't publish.

## Syntax basics
Box components are fenced: an opener line `:::name attr="value"`, the content, then a closing `:::` on its own line. Inline ones are tokens inside a sentence. The fence name must be exact (lowercase, hyphenated). Nest nothing except `:::stat` inside `:::stat-group`.

---

## Reach for it when… (the menu)

### Framing the article (top of the piece — at most ONE of each)
| When | Component | Syntax |
|---|---|---|
| You can answer the title in 1–3 sentences up top | `nutshell` | `:::nutshell`<br>The short answer.<br>`:::` |
| The piece is built on your own data/study | `methodology` | `:::methodology updated="monthly" by="Sloane Avery"`<br>- **Data source.** …<br>`:::` |
| You want the conclusions front-loaded for skimmers | `key-takeaways` | `:::key-takeaways`<br>- point one<br>`:::` |

### Inline asides (use sparingly — these are seasoning)
| When | Component | Syntax |
|---|---|---|
| An expert shortcut next to a step | `tip` (lightbulb) | `:::tip`<br>Do X to save time.<br>`:::` |
| An easy-to-miss caveat | `note` | `:::note`<br>Heads-up: …<br>`:::` |
| A risk or costly mistake | `warning` | `:::warning`<br>Don't do X.<br>`:::` |
| A must-not-miss point (stronger than note) | `important` | `:::important`<br>…<br>`:::` |
| A tangent that would derail the sentence | `sidenote` | `:::sidenote`<br>By the way, …<br>`:::` |
| The crisp definition of the core term, first mention | `definition` | `:::definition term="Coin"`<br>a metered credit…<br>`:::` |

### Numbers & data
| When | Component | Syntax |
|---|---|---|
| 1–4 hero numbers to make impossible to miss | `stat` (wrap multiples in `stat-group`) | `:::stat-group`<br>`:::stat value="61%" source="…"`<br>of apps meter "unlimited"<br>`:::`<br>`:::` |
| 5+ statistics each with a source | `stat-list` | `:::stat-list`<br>- 68% … ([source](url))<br>`:::` |
| A measured data table (caption + source + winner row) | `table` | `:::table caption="…" source="Ahrefs" emphasize-row="1"`<br>(GFM table)<br>`:::` |
| A chart or labelled screenshot | `figure` / `diagram` | `:::figure src="…" source="…"`<br>caption<br>`:::` *(visuals are ON — emit a typed `[VISUAL:]` per `templates/visual-strategy.md`; use a `:::figure`/`:::diagram` fence only when a real `src` already exists on disk)* |

### Comparing / recommending (roundups, "X vs Y", technical)
| When | Component | Syntax |
|---|---|---|
| Balanced verdict on one option | `proscons` | `:::proscons`<br>`## Pros`<br>- …<br>`## Cons`<br>- …<br>`:::` |
| Head-to-head across features | `feature-matrix` | `:::feature-matrix`<br>(GFM table; cells `yes`/`no`/`partial`)<br>`:::` |
| "Which should I use" with a ranked answer | `decision-table` + `preferred-order` | table fence, then `:::preferred-order`<br>A > B > C<br>`:::` |
| A numbered roundup item header | `entry` | `:::entry n="1" name="Tool" url="…" best_for="…" price="Free"` … `:::` |
| A short verdict / "best for" badge | `verdict` / `badge` | `:::verdict`…`:::` · `:::badge kind="best-overall"`…`:::` |

### Credibility & social proof
| When | Component | Syntax |
|---|---|---|
| A named expert's quote (with a face) | `expert` | `:::expert name="Jordan Mills" title="Analyst" company="…"`<br>"quote"<br>`:::` |
| One memorable line worth spotlighting | `pullquote` | `:::pullquote cite="Sloane Avery"`<br>The line.<br>`:::` |
| A real tweet / a video | `tweet` / `video` | `:::tweet url="…"` `:::` · `:::video src="…" title="…"` `:::` |

### Navigation & wrap-up
| When | Component | Syntax |
|---|---|---|
| Hand off mid-article to a deeper guide | `further-reading` | `:::further-reading`<br>- [Title](url)<br>`:::` |
| Let readers jump between roundup items | `jumplinks` | `:::jumplinks`<br>- [Label](#anchor)<br>`:::` |
| A question section (renders as an accordion) | `faq` | `:::faq`<br>`### Question?`<br>Answer.<br>`:::` |
| Push the reader to the product | `cta` | `:::cta heading="Try Pleasur.AI" button="Create" href="/pricing"`<br>value prop<br>`:::` |

> The page adds these **automatically** — you don't write them: table of contents, "Keep Learning" related grid, the author byline + bio, "Reviewed by".

### Inline text treatments
| When | Token |
|---|---|
| A formula / literal value / coin math | inline `` `code` `` → renders as a lavender chip: `` `$0 + 20 × 10 coins` `` |
| The opening paragraph (larger lead) | wrap it: `{lead}` … `{/lead}` |
| A rare highlight | `==text==` |

---

## Caps (the checker enforces these)
- `nutshell`, `methodology`, `key-takeaways`, `cta` → **at most 1 each** per article.
- Inline callouts (`tip`/`note`/`warning`/`important`/`sidenote`/`definition`) → keep it tasteful; **no more than ~1 per 2–3 sections**, never stacked back-to-back.
- `expert` quotes → a few at most (a consensus cluster is fine in a strategy piece; don't pad).
- Every fence must **close** (`:::`), use a **known name**, and carry its **required attributes** (e.g. `stat` needs `value`; `expert` needs `name`; `cta` needs `href`; `figure` needs `src`). A malformed fence ships as broken text, so the checker blocks it.

**Voice conventions (not components):** cite with plain inline links (no footnotes); close with a "Final thoughts" / "Bottom line" heading; no numbered headings; no drop caps; coloured bold only happens inside the box components.
