# Ahrefs blog component library

The styled, set-apart content blocks that make Ahrefs articles scannable and pleasant to read. This is a **two-sided spec**:
1. **Writer side** — `/draft` reads this so it reaches for the right component at the right moment (it emits the authoring syntax below).
2. **Render side** — the blog page (Strapi + frontend) must style each component. The "Design" notes are the render spec.

**Authoring convention:** fenced blocks `:::name … :::` (some already supported by `/format-for-publish`). The writer emits them; `/format-for-publish` converts them to the markup the page renders. **Restraint matters** — Ahrefs uses these sparingly; 1–2 of each per article, not a wall of boxes.

> **The "taste" is components + spacing, NOT exotic typography.** Ahrefs uses plain heading hierarchy, **bold BLUF lead sentences**, numbered section headings for lists/processes, bolded key phrases, and a "Final thoughts"/"Bottom line" closer. No drop caps, no font changes. Those are *voice rules* (already in `/draft`), not render components.

Legend: ⭐ = house-standard (in nearly every article) · ◆ = situational · ◇ = inferred / not seen in sample (build later).

---

## A. Callouts (boxed asides)

| Component | ⭐/◆ | Purpose / when | Authoring syntax | Design (render spec) |
|---|---|---|---|---|
| **Sidenote** | ⭐ | An aside/caveat/source-note that would derail the sentence. The single most recognizable Ahrefs block. | `:::sidenote … :::` (also `**Sidenote:** …` → auto-converts today) | Pale-grey inset, thin left accent rule, slightly smaller type, bold/italic "Sidenote." lead-in |
| **Methodology** | ⭐ (data posts) | Disclose data source, sample, definitions, stat choice — credibility for any data/benchmark post. Place right after the intro. | `:::methodology updated="monthly" by="…"` + **bold-led bullets** `- **Data source.** …` | **Lavender / pale-purple panel**, rounded, generous padding, "Methodology" header, optional "updated … by [author-link]" line |
| **In a nutshell / TL;DR / Quick answer** | ⭐ | The one-paragraph answer up top for scanners + AI Overviews. One per article, under the byline. | `:::nutshell … :::` (aliases `:::tldr`, `:::quick-answer`) | Tinted background or top/bottom hairline, bold opener, 1–3 sentence direct answer |
| **Key takeaways** | ◆ | Bulleted conclusions front-loaded for skimmers + snippet capture. Long guides / data studies. | `:::key-takeaways` + bullets (bold the figures) | Tinted callout panel, bulleted, bold numbers |
| **Pro tip / Tip** | ⭐ | An expert shortcut next to the step it improves. Sparingly (1–2). | `:::tip … :::` (also `**Pro tip:** …` → auto-converts today) | Tinted box (light blue/green) or left accent bar, bold "Pro tip" label, optional lightbulb icon |
| **Note** | ⭐ | An easily-overlooked caveat. | `:::note … :::` (also `**Note:** …` → today) | Neutral/blue tint, ℹ️ icon, bold label |
| **Warning / Important** | ◇ | A risky step or costly mistake. | `:::warning … :::` | Amber/red tint, ⚠️ icon, bold label |
| **Editor's note** | ⭐ (updates) | Post-publish meta: a newer study supersedes this, a correction. Top of article. | `:::editors-note … :::` (also `**Editor:** …` → today) | Set-apart italic/tinted line, bold "Editor's Note" |
| **Definition** | ◇ | A crisp, quotable one-line definition of the article's core term. First mention. | `:::definition term="…" … :::` | Tinted one-liner or bold-emphasized sentence |
| **"New to X?" primer nudge** | ◆ | Redirect a beginner to a foundational guide early. Top of intermediate/advanced posts. | `:::primer-nudge` (question + link) | Small tinted/bordered one-liner near top |

---

## B. Data, comparison & decision

| Component | ⭐/◆ | Purpose / when | Authoring syntax | Design (render spec) |
|---|---|---|---|---|
| **Stat callout (big number)** | ⭐ | Make one load-bearing number impossible to miss. | `:::stat value="68%" source="…" source_url="…"` + label; wrap multiples in `:::stat-group` | Oversized numeral, muted label, tinted card; pairs sit 2-up |
| **Sourced stat list** | ⭐ (stat posts) | Dense, credible list of findings (number + claim + source). | `- {stat}68%{/stat} … {src}Name\|url{/src}` (plain bullets also fine) | Bold leading figure, small inline source link/pill |
| **Benchmark / data table** | ⭐ (data posts) | Measured data by category, with caption + source + methodology. | `:::table caption="…" source="Ahrefs" emphasize-row=1` + GFM table | Caption above, source below, header tint, **winner row bolded**; often paired with a chart |
| **Data chart (landscape)** | ⭐ (data posts) | Visual distribution/trend. **Title above, source below, landscape always.** | `:::chart type="bar\|line" title="…" source="…"` + `data:` | Horizontal ranked bars / time-series line, caption above, source credit below. *(Deferred until the visual project — emit the block; render later.)* |
| **Best-for summary table** | ⭐ (roundups) | At-a-glance option→use-case map at the top of a listicle. | GFM 2-col table, name = jump-link | Clean 2-col, name links to its section |
| **Roundup entry header** | ⭐ (roundups) | Standardize each option's intro (number + name + "best for" + price). | `### 1. Name {#anchor}` + `:::entry-meta best_for="…" price="…"` | Numbered H2/H3, small "Best for" eyebrow, bold price line |
| **Pros / cons** | ◇ | Balanced two-column verdict on one option. | `:::proscons` → `## Pros` / `## Cons` lists | Side-by-side panels, green ✓ vs red ✕ bullets |
| **Feature matrix (✓/✕)** | ◇ | Head-to-head across features. | GFM table with `:check:` / `:x:` / `:partial:` tokens | Green ✓ / red ✕ glyphs, header tint, first col emphasized |
| **Decision / classification table** | ⭐ (technical) | Ahrefs' signature technical-comparison: classify options, then an explicit **"preferred order"** line + **"use this when you…"** bullets. | GFM table + `:::recommend order="…"` + body | Plain grid + an emphasized recommendation line + conditional bullets (NOT a single "winner" badge) |
| **Rating / scorecard / badge** | ◇ | A comparable verdict. **Ahrefs favors qualitative "Best for X" labels over numeric scores** — match that. | `:::badge type="best-for\|winner\|score" label/value="…"` | Pill/badge with accent; prefer "Best for" labels |
| **Accordion FAQ** | ◇ | Collapsible Q&A + FAQ schema. (Not house-standard; Ahrefs uses plain H2/H3 FAQs.) | `:::faq` + `### Q` / answer pairs | Click-to-expand rows, chevron; emit JSON-LD |

---

## C. Social proof & editorial

| Component | ⭐/◆ | Purpose / when | Authoring syntax | Design (render spec) |
|---|---|---|---|---|
| **Expert / contributor quote** | ⭐ | The signature E-E-A-T unit — a named practitioner with a face. Cluster several for "consensus." | `:::expert name="…" title="…" company="…" company_url="…" photo="…"` + quote (bold the key phrase) | Shaded contained block, circular headshot left, name + role + linked company stacked |
| **Pull quote** | ◆ | Spotlight one memorable line (emphasis/memorability, vs the expert block's testimony). 1–2 per article. | `:::pullquote cite="Name, Title, Org" source="url"` | Larger font, indent, accent/background, attribution beneath |
| **Embedded tweet** | ◆ | Real social proof from the source. Sparingly. | `:::tweet url="…"` (degrade to `:::pullquote` if no live embed) | Native X embed card |

---

## D. Navigation & structure

| Component | ⭐/◆ | Purpose / when | Authoring syntax | Design (render spec) |
|---|---|---|---|---|
| **Table of contents** | ⭐ (long posts) | Orient + jump-nav. 4+ H2s / >1,500 words. **Inline below the intro** (Ahrefs is NOT sticky-sidebar here). | auto-generate from H2s; optional `:::toc` | Inline "Contents" list of anchor links |
| **In-text jump links** | ◆ | Cross-link to a later section. | `[see Step 3](#anchor)` | Standard inline link |
| **Further / Recommended reading** | ⭐ | Hand off to a deeper guide *mid-article* at the moment of relevance (distinct from the end grid). | `:::further-reading` + bulleted link(s); inline single = `**Recommended reading:** *[Title](url)*` | Bold label + bulleted/italic link, light treatment |
| **"Keep Learning" related grid** | ⭐ | Onward journey at the very end. | auto from CMS; optional `:::keep-learning` + slugs | Card grid: thumbnail + linked headline + 1-liner |
| **Author byline + "Reviewed by"** | ⭐ | Authorship + editorial-review credibility (this is the "rated/reviewed" thing). Top. | front-matter `author:`, `reviewed_by:`, `co_authors:`, `date:`, `read_time:`, `categories:` | Circular avatar, name link, role, "Reviewed by ✓ [Name]", muted date/read-time |
| **Author bio box** | ⭐ | Reinforce author authority at the close. | auto-render from `author` front-matter against the author DB | Profile block, larger avatar, 2–3 line bio, social icons; "Contributors" sub-block for co-authors |
| **CTA / product callout** | ⭐ | Reader → product. Once high, once low. Map to a Pleasur.AI product. | `:::cta heading="…" button="…" href="/pricing"` + value prop | Bordered/shaded box, heading + one-line value prop + button |

---

## E. Media (DEFERRED — emit placeholders, render later)

| Component | Purpose / when | Authoring syntax |
|---|---|---|
| **Annotated screenshot** | Show the actual product/chat UI with guidance. | the engine's typed `[VISUAL: screenshot; …]` placeholder (visuals deferred — left as a marker) |
| **Embedded video** | A moving walkthrough beats a screenshot. Rare. | `:::video url="…"` |

---

## What ports vs what to skip for Pleasur.AI
- **Skip / N/A:** the **"Article performance" metrics box** (Ahrefs dogfooding its own SEO data — we have no analogue). Embedded Reddit, drop caps, numeric star scorecards (Ahrefs doesn't use them either).
- **Already done:** `:::tip`/`:::note`/`:::editor` exist in `/format-for-publish`; the **author byline + bio** maps to the 3 Strapi authors we created.
- **Highest-ROI to ship first (confirmed house-standard):** Sidenote · Methodology · In-a-nutshell · Key-takeaways · Stat callout · Benchmark table (caption/source/emphasis) · Expert quote · Further-reading · CTA · Pull quote.

## Build = two halves
1. **Writer knows them** — `/draft` + `/outline` read this file and emit the fences when a section calls for one (each persona favors different blocks: Sloane → methodology/stat/charts; Theo → steps/tables/CTA; Mateo → expert quotes/screenshots).
2. **Page renders them** — `/format-for-publish` **preserves** each `:::fence` in the published markdown body verbatim (it only normalizes the `**Label:**` shorthands into fences; it does NOT convert fences to HTML), and the blog page renderer styles them per the **Render contract** below. The "Design" column is the visual spec; the Render contract is the parsing spec.

---

## Render contract

**This is the spec the blog-page renderer (Strapi `shared.rich-text` → Next.js) must implement.** The publishing pipeline guarantees these fences arrive in the published `article.md` body **verbatim** — `/format-for-publish` neither converts them to HTML nor strips them. The renderer is responsible for parsing each fence and emitting the styled markup (the "Design" notes above are the target look).

### Fence grammar (applies to every component below)

```
:::<name> [attr="value" attr="value" …]
<inner content — markdown>
:::
```

- **Opener:** a line that begins (after optional leading whitespace) with `:::` immediately followed by the component `name` (no space between `:::` and the name). Attributes, when present, follow the name on the **same line** as `key="value"` pairs (double-quoted; space-separated; order-independent; all optional unless marked **required**).
- **Closer:** a line that is exactly `:::` (after optional leading whitespace), with no name.
- **Inner content** is everything between the opener and closer lines. It is **markdown** — the renderer MUST render it as markdown (bold, links, lists, inline code), not as plain text. Inner content MAY be empty for attribute-only components.
- **Nesting:** only one component nests — `:::stat` inside `:::stat-group`. No other nesting is produced. Parse `:::stat-group` by consuming child `:::stat … :::` blocks until the group's closing `:::`.
- **Unknown attribute** → ignore it (forward-compatible). **Unknown fence name** → render the inner content as a plain blockquote/`<aside>` fallback rather than dropping it (never silently delete reader content).
- Fence names are **exact and lowercase**, hyphenated where shown (`key-takeaways`, `stat-group`, `further-reading`). Match the names in this file byte-for-byte.

### The ~10 house-standard components

#### `:::sidenote`
- **Attributes:** none.
- **Inner:** markdown, 1–3 sentences (an aside/caveat/source-note).
- **Render:** pale-grey inset, thin left accent rule, slightly smaller type, bold/italic "Sidenote." lead-in prepended.
```
:::sidenote
Prices reflect the US storefront as of June 2026; regional pricing varies.
:::
```

#### `:::methodology`
- **Attributes:** `updated="<cadence, e.g. monthly>"` (optional), `by="<author name or @author-link>"` (optional).
- **Inner:** markdown, typically a **bullet list** of bold-led items (`- **Data source.** …`, `- **Sample.** …`, `- **Definitions.** …`).
- **Render:** lavender / pale-purple panel, rounded, generous padding, "Methodology" header; if `updated`/`by` present, render an "updated `<updated>` by `<by>`" subline (link `by` to the author page when it resolves).
```
:::methodology updated="monthly" by="Sloane Avery"
- **Data source.** 1,200 app reviews scraped Q1 2026.
- **Sample.** English-language, US App Store only.
- **Definitions.** "Uncensored" = no content filter on text generation.
:::
```

#### `:::nutshell`
- **Attributes:** none. (Authoring aliases `:::tldr` / `:::quick-answer` MAY arrive — treat as synonyms of `:::nutshell`.)
- **Inner:** markdown, a 1–3 sentence direct answer. **One per article**, placed directly under the H1.
- **Render:** tinted background or top/bottom hairline, bold opener, set apart for scanners + AI Overviews.
```
:::nutshell
The three best uncensored AI girlfriend apps are A, B, and C — chosen on no-filter support, price, and memory quality.
:::
```

#### `:::key-takeaways`
- **Attributes:** none.
- **Inner:** markdown **bullet list** (bold the figures/verdicts). Front-loaded conclusions; usually the article's close.
- **Render:** tinted callout panel, bulleted, bold numbers.
```
:::key-takeaways
- **68%** of users cite loneliness as the primary driver.
- Pricing clusters at **$10–$20/mo**.
- Uncensored modes are the top paid-conversion trigger.
:::
```

#### `:::tip`
- **Attributes:** none. (Shorthand `**Tip:**` / `**Pro tip:**` normalize to this fence.)
- **Inner:** markdown, 1–2 sentences (an expert shortcut).
- **Render:** tinted box (light blue/green) or left accent bar, bold "Pro tip" label, optional lightbulb icon.
```
:::tip
Use voice mode for the first session — it lifts day-2 retention noticeably.
:::
```

#### `:::note`
- **Attributes:** none. (Shorthand `**Note:**` / `**Sidenote:**` normalize to this fence today; `:::sidenote` is its own distinct fence above.)
- **Inner:** markdown, 1–2 sentences (an easily-overlooked caveat).
- **Render:** neutral/blue tint, ℹ️ icon, bold "Note" label.
```
:::note
Free tiers reset their message quota monthly, not daily.
:::
```

#### `:::stat`  (and `:::stat-group`)
- **`:::stat` attributes:** `value="<the number/figure, e.g. 68% or $12/mo>"` (**required**), `source="<source name>"` (optional), `source_url="<https URL>"` (optional).
- **`:::stat` inner:** markdown, a short label/claim for the figure.
- **`:::stat` render:** oversized numeral (`value`), muted label (inner), tinted card; if `source`+`source_url` present, render a small inline source link/pill.
- **`:::stat-group` attributes:** none. **Inner:** two or more `:::stat` blocks. **Render:** lay the child stats out as cards, pairs sit 2-up.
```
:::stat value="68%" source="Internal survey" source_url="https://example.com/survey"
of users cite loneliness as the primary driver.
:::

:::stat-group
:::stat value="$12/mo" source="Pricing audit" source_url="https://example.com/pricing"
median paid tier
:::
:::stat value="3.2M" source="Sensor Tower" source_url="https://example.com/downloads"
monthly downloads
:::
:::
```

#### `:::expert`
- **Attributes:** `name="<person>"` (**required**), `title="<role>"` (optional), `company="<org>"` (optional), `company_url="<https URL>"` (optional), `photo="<image URL/path>"` (optional).
- **Inner:** markdown — the quote (bold the key phrase).
- **Render:** shaded contained block, circular headshot (`photo`) left, `name` + `title` + linked `company` (→ `company_url`) stacked. Cluster several adjacent `:::expert` blocks as a "consensus" row.
```
:::expert name="Dr. Jane Roe" title="Researcher" company="MIT Media Lab" company_url="https://media.mit.edu" photo="https://example.com/jane.jpg"
Parasocial bonds with conversational agents are **real, measurable, and durable**.
:::
```

#### `:::pullquote`
- **Attributes:** `cite="<Name, Title, Org>"` (optional), `source="<https URL>"` (optional).
- **Inner:** markdown — the memorable line (one sentence). 1–2 per article.
- **Render:** larger font, indent, accent/background; render `cite` as attribution beneath (link to `source` when present).
```
:::pullquote cite="Jane Roe, Researcher, MIT Media Lab" source="https://media.mit.edu/quote"
The line between tool and companion is thinner than we like to admit.
:::
```

#### `:::further-reading`
- **Attributes:** none.
- **Inner:** markdown — one or more bulleted links (a mid-article hand-off to a deeper guide). (Inline single-link form `**Recommended reading:** *[Title](url)*` may also appear as plain prose; only the fenced form needs special rendering.)
- **Render:** bold "Further reading" label + bulleted/italic link(s), light treatment (distinct from the end-of-article related grid).
```
:::further-reading
- [How LLM companions actually work](/blog/how-llm-companions-work)
- [Uncensored vs filtered: what changes](/blog/uncensored-vs-filtered)
:::
```

#### `:::cta`
- **Attributes:** `heading="<headline>"` (optional), `button="<button label>"` (optional), `href="<destination, e.g. /pricing>"` (optional).
- **Inner:** markdown — a one-line value proposition.
- **Render:** bordered/shaded box, `heading` + the inner value-prop line + a button (`button` label linking to `href`). Used once high, once low; map to a Pleasur.AI product.
```
:::cta heading="Build your AI companion free" button="Start now" href="/pricing"
Spin up a personalized companion in under a minute — no card required.
:::
```

### Renderer acceptance checklist
- [ ] Parses opener `:::<name>` (no space after `:::`) + same-line `key="value"` attrs (any order, all optional unless marked required) + bare-`:::` closer.
- [ ] Renders inner content as **markdown**, not plain text.
- [ ] Handles `:::stat-group` wrapping child `:::stat` blocks (the only nesting case).
- [ ] Renders attribute-only sublines: `methodology` (updated/by), `stat` (source→source_url pill), `expert` (name/title/company→company_url/photo), `pullquote` (cite→source), `cta` (heading/button→href).
- [ ] Unknown attribute ignored; unknown fence name degrades to a plain `<aside>`/blockquote (never dropped).
- [ ] `:::sidenote` and `:::note` styled distinctly (sidenote = grey left-rule inset; note = blue ℹ️).
