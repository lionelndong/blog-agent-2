# Ahrefs blog component library

The styled, set-apart content blocks that make Ahrefs articles scannable and pleasant to read. This is a **two-sided spec**:
1. **Writer side** — `/draft` reads this so it reaches for the right component at the right moment (it emits the authoring syntax below).
2. **Render side** — the blog page (Strapi + frontend) must style each component. The "Design" notes are the render spec; the **`## Render contract`** at the bottom is the authoritative, exhaustive build spec for the CTO.

**Authoring convention:** fenced blocks `:::name … :::` (some already supported by `/format-for-publish`). The writer emits them; `/format-for-publish` converts the `**Label:**` shorthands to fences and otherwise preserves them verbatim, and the page renderer turns each fence into the matching `cmp-<name>` markup. **Restraint matters** — Ahrefs uses these sparingly; 1–2 of each per article, not a wall of boxes.

> **The "taste" is components + spacing, NOT exotic typography.** Ahrefs uses plain heading hierarchy, **bold BLUF lead sentences**, bolded key phrases, and a "Final thoughts"/"Bottom line" closer. No drop caps, no numbered headings, no font changes. Those are *voice rules* (already in `/draft`), not render components — see **Inline treatments & conventions** (bucket C) at the bottom.

Legend: ⭐ = house-standard (in nearly every article) · ◆ = situational · ◇ = inferred / not seen in sample (build later).

**Status (build state):** **14 BUILT · 25 TODO** (TODO = 18 authored fences + 4 auto-injected blocks + 3 inline treatments; 2 further blocks documented as skips). See the **Render contract** for the per-component checklist. The catalog below is the *taste/when-to-use* map; the Render contract is the *parse/markup* law. On any conflict, the Render contract wins.

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
| **Warning** | ◇ | A risky step, data-loss, or money-loss action — stronger than a note. | `:::warning … :::` | Amber tint, left amber rule, ⚠️ icon, bold "Warning" label |
| **Important** | ◇ | A must-not-miss constraint that isn't a hazard (a key prerequisite/rule). | `:::important … :::` | Accent (purple) tint, left accent rule, ❗ icon, bold "Important" label |
| **Editor's note** | ⭐ (updates) | Post-publish meta: a newer study supersedes this, a correction. Top of article. | `:::editors-note … :::` (also `**Editor:** …` → today) | Set-apart italic/tinted line, bold "Editor's Note" |
| **Definition** | ◇ | A crisp, quotable one-line definition of the article's core term. First mention. | `:::definition term="…" … :::` | Tinted one-liner, bold term lead-in, hangs the definition off it |
| **"New to X?" primer** | ◆ | Redirect a beginner to a foundational guide early, with a thumbnail. Top of intermediate/advanced posts. | `:::primer href="…" thumb="…"` (question + link) | Small bordered card near top: thumb left, "New to X?" + linked title right |

---

## B. Data, comparison & decision

| Component | ⭐/◆ | Purpose / when | Authoring syntax | Design (render spec) |
|---|---|---|---|---|
| **Stat callout (big number)** | ⭐ | Make one load-bearing number impossible to miss. | `:::stat value="68%" source="…" source_url="…"` + label; wrap multiples in `:::stat-group` | Oversized numeral, muted label, tinted card; pairs sit 2-up |
| **Sourced stat list** | ⭐ (stat posts) | Dense, credible *list* of findings (number + claim + source), as a vertical list rather than big-number cards. | `:::stat-list` + cited bullets (`- **68%** … ([Source](url))`) | Bold leading figure per row, claim, small inline source link |
| **Benchmark / data table** | ⭐ (data posts) | Measured data by category, with caption + source + methodology. | `:::table caption="…" source="Ahrefs" emphasize-row=1` + GFM table | Caption above, source below, header tint, **winner row bolded**; often paired with a chart |
| **Best-for summary table** | ⭐ (roundups) | At-a-glance option→use-case map at the top of a listicle. | GFM 2-col table inside `:::table`, name = jump-link | Clean 2-col, name links to its section |
| **Feature matrix (✓/✕)** | ◇ | Head-to-head across many features for many products. | `:::feature-matrix` + GFM table, cell tokens `yes`/`no`/`partial` | Green ✓ / red ✕ / grey – glyphs, header tint, first col emphasized, horizontal scroll on mobile |
| **Decision / classification table** | ⭐ (technical) | Ahrefs' signature technical-comparison: classify options in a grid. | `:::decision-table` + GFM table | Plain grid, header tint, first col emphasized — a *classification* table, not a winner badge |
| **Preferred order** | ⭐ (technical) | The explicit "here's the order I'd pick them in" ranked recommendation that follows a decision table. | `:::preferred-order` + ranked list (`1. … — use when …`) | Numbered ranked list with accent ordinals; each item = pick + "use when you…" qualifier |
| **Verdict** | ◆ | The one-line "bottom line on this option" call, inside a roundup entry or comparison. | `:::verdict … :::` | Accent-tinted band, bold "Verdict" lead-in, one decisive sentence |
| **Badge** | ◇ | A comparable qualitative award on a roundup entry. **Ahrefs favors "Best for X" labels over numeric scores.** | `:::badge kind="best-overall\|editors-pick\|best-free"` | Small pill with accent fill, kind→label text, sits by the entry header |
| **Roundup entry header** | ⭐ (roundups) | Standardize each option's intro (number + name + "best for" + price). | `:::entry n="1" name="…" url="…" best_for="…" price="…"` | Numbered eyebrow, bold linked name as heading, "Best for" eyebrow + bold price line |
| **Pros / cons** | ◇ | Balanced two-column verdict on one option. | `:::proscons` → `## Pros` / `## Cons` lists | Side-by-side panels, green ✓ vs red ✕ bullets |
| **Accordion FAQ** | ◇ | Collapsible Q&A + FAQ schema. (Not house-standard; Ahrefs uses plain H2/H3 FAQs — use only when schema capture is the goal.) | `:::faq` + `### Q` / answer pairs | Click-to-expand rows, chevron; emit FAQPage JSON-LD |

---

## C. Social proof & editorial

| Component | ⭐/◆ | Purpose / when | Authoring syntax | Design (render spec) |
|---|---|---|---|---|
| **Expert / contributor quote** | ⭐ | The signature E-E-A-T unit — a named practitioner with a face. Cluster several for "consensus." | `:::expert name="…" title="…" company="…" company_url="…" photo="…"` + quote (bold the key phrase) | Shaded contained block, circular headshot left, name + role + linked company stacked |
| **Pull quote** | ◆ | Spotlight one memorable line (emphasis/memorability, vs the expert block's testimony). 1–2 per article. | `:::pullquote cite="Name, Title, Org" source="url"` | Larger serif font, indent, accent left-rule, attribution beneath |
| **Embedded tweet** | ◆ | Real social proof from the source. Sparingly. | `:::tweet url="…"` (degrade to `:::pullquote` if no live embed) | Native X embed card, lazy-loaded, no-JS fallback link |

---

## D. Navigation & structure

| Component | ⭐/◆ | Purpose / when | Authoring syntax | Design (render spec) |
|---|---|---|---|---|
| **Table of contents** | ⭐ (long posts) | Orient + jump-nav. 4+ H2s / >1,500 words. **Auto-injected** from the H2/H3 tree — no fence. | *auto* (page template); writer does nothing | Inline "Contents" list below intro **and** a sticky rail on wide viewports, with active-section highlight |
| **In-text jump links** | ◆ | Cross-link to a later section, or a top-of-article jump menu the writer chooses. | inline `[see Step 3](#anchor)`; explicit menu = `:::jumplinks` + link list | Inline link; the menu renders as a compact tinted row of anchor chips |
| **Further / Recommended reading** | ⭐ | Hand off to a deeper guide *mid-article* at the moment of relevance (distinct from the end grid). | `:::further-reading` + bulleted link(s); inline single = `**Recommended reading:** *[Title](url)*` | Bold label + bulleted/italic link, light tinted treatment |
| **"Keep Learning" related grid** | ⭐ | Onward journey at the very end. **Auto-injected** from related-post metadata — no fence. | *auto* (page template) | Card grid: thumbnail + linked headline + 1-liner |
| **Author byline + "Reviewed by"** | ⭐ | Authorship + editorial-review credibility (this is the "rated/reviewed" thing). **Auto-injected** from the article/author record. Top. | front-matter `author:`, `reviewed_by:`, `co_authors:`, `date:`, `read_time:`, `categories:` | Circular avatar, name link, role, "Reviewed by ✓ [Name]", muted date/read-time |
| **Author bio box** | ⭐ | Reinforce author authority at the close. **Auto-injected** from the author record — no fence. | *auto* from `author` front-matter against the author DB | Profile block, larger avatar, 2–3 line bio, social icons |
| **Contributors / "Reviewed by"** | ⭐ | Surface co-authors + the named reviewer at the close. **Auto-injected** from metadata. | *auto* from `co_authors:` / `reviewed_by:` | Sub-block under the bio: small avatars + linked names + role label |
| **CTA / product callout** | ⭐ | Reader → product. Once high, once low. Map to a Pleasur.AI product. | `:::cta heading="…" button="…" href="/pricing"` + value prop | Bordered/shaded box, heading + one-line value prop + button |

---

## E. Media

| Component | ⭐/◆ | Purpose / when | Authoring syntax | Design (render spec) |
|---|---|---|---|---|
| **Figure (image + caption + source)** | ◆ | Any standalone image that needs a caption and an attribution line. | `:::figure src="…" source="…"` + caption text | Centered image, rounded, small muted caption below, "Source: …" credit line |
| **Diagram** | ◆ | A produced explanatory diagram (the captioned, framed variant of figure for schematics). | `:::diagram src="…"` + caption | Framed/tinted figure, "Diagram" treatment, caption below |
| **Embedded video** | ◆ | A moving walkthrough beats a screenshot. Rare. | `:::video src="…" title="…"` | Responsive 16:9 embed/iframe, lazy-loaded, `title` as caption |
| **Annotated screenshot** | ◆ (DEFERRED) | Show the actual product/chat UI with guidance. *Visuals project — emit the marker, render later.* | the engine's typed `[VISUAL: screenshot; …]` placeholder | (deferred — left as a marker) |
| **Data chart (landscape)** | ⭐ (DEFERRED) | Visual distribution/trend. Title above, source below, landscape always. *Visuals project — emit the marker, render later.* | the engine's typed `[VISUAL: chart; …]` placeholder | (deferred — left as a marker) |

---

## What ports vs what to skip for Pleasur.AI
- **Skip / N/A:** the **"Article performance" metrics box** (Ahrefs dogfooding its own SEO data — we have no analogue) and the **newsletter signup form** (no list yet) → both **OPTIONAL / likely-skip**; documented as render-only stubs at the end of the Render contract, not built. Also skip embedded Reddit, drop caps, numeric star scorecards (Ahrefs doesn't use them either).
- **Already done:** 14 fences/auto-blocks render today (byline, nutshell, methodology, key-takeaways, sidenote, tip, note, stat, stat-group, table, expert, pullquote, further-reading, cta).
- **Highest-ROI to ship next:** Warning/Important · Definition · Pros/cons · Feature-matrix · Decision-table + Preferred-order · Verdict/Badge · Roundup entry header · FAQ (+JSON-LD) · Figure · the three **auto-injected** blocks (TOC, keep-learning grid, author-bio/contributors) · the **inline treatments** (lead paragraph, inline-code/formula, mark).

## Build = two halves
1. **Writer knows them** — `/draft` + `/outline` read this file and emit the **bucket-A** fences when a section calls for one (each persona favors different blocks: **Sloane** → methodology / stat / stat-list / table / chart-markers; **Theo** → steps / decision-table / preferred-order / feature-matrix / CTA; **Mateo** → expert quotes / pullquotes / tweets / figures / screenshots). Bucket-B blocks are **auto-injected** by the page template — the writer never emits a fence for them. Bucket-C is **inline treatment** governed by voice rules, not fences (except `{lead}` / `==mark==`).
2. **Page renders them** — `/format-for-publish` **preserves** each `:::fence` in the published markdown body verbatim (it only normalizes the `**Label:**` shorthands into fences; it does NOT convert fences to HTML), and the blog page renderer styles them per the **Render contract** below. The "Design" column is the visual spec; the Render contract is the parsing spec.

---

## Render contract

**This is the authoritative, complete build spec the blog-page renderer (Strapi `shared.rich-text` → Next.js) must implement — every component, BUILT and TODO.** The publishing pipeline guarantees authored fences arrive in the published `article.md` body **verbatim** — `/format-for-publish` neither converts them to HTML nor strips them. The renderer parses each fence (bucket A) or reads article/author metadata (bucket B) or applies an inline rule (bucket C) and emits the styled markup. Every component below names its exact authoring form and its `cmp-<name>` class (or inline element). The **`examples/component-mockup.html`** file is the pixel/CSS target for the BUILT set — match it (or improve), and extend the same token system to the TODO set.

**Build legend:** **[BUILT]** = renders today (see `component-mockup.html`). **[TODO]** = to implement.

### Shared design tokens (from `component-mockup.html` — reuse these, do NOT introduce new hexes ad hoc)

```css
:root{
  --ink:#1d1d1f;     /* body text                */
  --mut:#6b7280;     /* muted labels/captions     */
  --hint:#9ca3af;    /* faint source/credit lines */
  --line:#e5e7eb;    /* hairlines/borders         */
  --surf:#f6f6f4;    /* neutral surface tint      */
  --accent:#534ab7;  /* BRAND purple — the only brand color */
}
/* Derived role colors already in use by BUILT components (keep consistent across TODO too): */
/* link            #185fa5                          */
/* lavender panel  bg #eeedfe  text #26215c  link #3c3489   (methodology / important) */
/* info/related    bg #e6f1fb                         (further-reading / table winner row) */
/* positive/tip    bg #eaf3de  text #173404           (tip / pros / yes ✓ = #178a3c text) */
/* success accent  #0f6e56                           (reviewed-by ✓ / expert avatar) */
/* sidenote rule   #b4b2a9                            */
/* warning         bg #fdf3e3  text #6b4710  rule #d99a2b  (warning) */
/* negative/cons   ✕ = #c2371f text                   (cons / no ✕) */
/* partial         – = var(--mut)                     (feature-matrix partial) */
/* code/formula    bg #efeefc  text #4338ad           (inline-code — soft on-brand, NOT Ahrefs crimson) */
/* mark/highlight  bg #efe9c8                          (==text==) */
```

> **Brand-color rule (bucket C):** we do **NOT** copy Ahrefs' exact hexes (their crimson `#c7254e` on pink `#f9f2f4`, their blue links, etc.). Inline code/formula and every accent use **our** purple `#534ab7` system — the code chip above is a soft on-brand lavender tint, not crimson.

### Fence grammar (applies to every bucket-A component)

```
:::<name> [attr="value" attr="value" …]
<inner content — markdown>
:::
```

- **Opener:** a line that begins (after optional leading whitespace) with `:::` immediately followed by the component `name` (no space between `:::` and the name). Attributes, when present, follow the name on the **same line** as `key="value"` pairs (double-quoted; space-separated; order-independent; all optional unless marked **required**).
- **Closer:** a line that is exactly `:::` (after optional leading whitespace), with no name.
- **Inner content** is everything between the opener and closer lines. It is **markdown** — the renderer MUST render it as markdown (bold, links, lists, inline code, GFM tables), not as plain text. Inner content MAY be empty for attribute-only components.
- **Nesting:** two cases only — `:::stat` inside `:::stat-group`, and a GFM table inside the table-bearing fences (`:::table`, `:::feature-matrix`, `:::decision-table`). No other nesting is produced.
- **Unknown attribute** → ignore it (forward-compatible). **Unknown fence name** → render the inner content as a plain blockquote/`<aside>` fallback rather than dropping it (never silently delete reader content).
- Fence names are **exact and lowercase**, hyphenated where shown (`key-takeaways`, `stat-group`, `further-reading`, `feature-matrix`, `decision-table`, `preferred-order`, `stat-list`). Match the names in this file byte-for-byte.

---

### Bucket A — AUTHORED (the writer emits a `:::fence`)

#### `:::byline`  **[BUILT]**
- **Source:** rendered from front-matter (`author`, `reviewed_by`, `date`, `read_time`) — emitted by the template at the top, not hand-written. (Listed here because it carries the same `cmp-` contract; metadata-driven like bucket B.)
- **Render:** `<div class="cmp-byline">` — circular avatar (initials on `--accent`), `.nm` name link, `.mt` muted meta with `.rev` "✓ Reviewed by [Name]" in `#0f6e56`, then `· date · N min read`.

#### `:::nutshell`  **[BUILT]**
- **Attributes:** none. (Authoring aliases `:::tldr` / `:::quick-answer` MAY arrive — treat as synonyms.)
- **Inner:** markdown, 1–3 sentence direct answer. **One per article**, directly under the H1.
- **Render:** `<div class="cmp-nutshell">` — `--surf` background, rounded, bold "In a nutshell." opener prepended.
```
:::nutshell
The three best uncensored AI girlfriend apps are A, B, and C — chosen on no-filter support, price, and memory quality.
:::
```

#### `:::methodology`  **[BUILT]**
- **Attributes:** `updated="<cadence>"` (optional), `by="<author name or @author-link>"` (optional).
- **Inner:** markdown, typically a **bullet list** of bold-led items (`- **Data source.** …`).
- **Render:** `<div class="cmp-methodology">` — lavender panel (`#eeedfe`/`#26215c`), "Methodology" `.h` header; if `updated`/`by` present, a `.fresh` "Updated `<updated>` … by `<by>`" subline (link `by` to the author page, link `#3c3489`).
```
:::methodology updated="monthly" by="Sloane Avery"
- **Data source.** 1,200 app reviews scraped Q1 2026.
- **Sample.** English-language, US App Store only.
- **Definitions.** "Uncensored" = no content filter on text generation.
:::
```

#### `:::key-takeaways`  **[BUILT]**
- **Attributes:** none.
- **Inner:** markdown **bullet list** (bold the figures/verdicts).
- **Render:** `<div class="cmp-key-takeaways">` — `--surf` panel with left `--accent` rule, bold "Key takeaways" `.l` label, bulleted list.
- **Dedupe — study-lead variant:** a "key findings from our study" lead is the **same component**, not a new fence. If a study lead is wanted, add `variant="findings"` (optional) → renderer may swap the label to "Key findings"; markup/class unchanged. Do NOT create a separate `:::key-findings` fence.
```
:::key-takeaways
- **68%** of users cite loneliness as the primary driver.
- Pricing clusters at **$10–$20/mo**.
:::
```

#### `:::sidenote`  **[BUILT]**
- **Attributes:** none.
- **Inner:** markdown, 1–3 sentences.
- **Render:** `<div class="cmp-sidenote">` — `--surf` inset, 3px `#b4b2a9` left rule, smaller type, bold/italic "Sidenote." `.l` lead-in.
```
:::sidenote
Prices reflect the US storefront as of June 2026; regional pricing varies.
:::
```

#### `:::tip`  **[BUILT]**
- **Attributes:** none. (Shorthand `**Tip:**` / `**Pro tip:**` normalize to this fence.)
- **Inner:** markdown, 1–2 sentences.
- **Render:** `<div class="cmp-tip">` — green box (`#eaf3de`/`#173404`), bold "💡 Pro tip." `.l` label.
```
:::tip
Use voice mode for the first session — it lifts day-2 retention noticeably.
:::
```

#### `:::note`  **[BUILT]**
- **Attributes:** none. (Shorthand `**Note:**` / `**Sidenote:**` normalize to a fence; `:::sidenote` is its own distinct fence above.)
- **Inner:** markdown, 1–2 sentences.
- **Render:** `<div class="cmp-note">` — neutral/blue tint, ℹ️ icon, bold "Note" label.
```
:::note
Free tiers reset their message quota monthly, not daily.
:::
```

#### `:::warning`  **[TODO]**
- **When:** a risky step / data-loss / money-loss action — stronger than a note.
- **Attributes:** none.
- **Inner:** markdown, 1–2 sentences.
- **Render:** `<div class="cmp-warning">` — amber tint `#fdf3e3`, text `#6b4710`, 3px left rule `#d99a2b`, ⚠️ icon, bold "Warning" label prepended.
```
:::warning
Deleting a companion is permanent — its memory and chat history cannot be recovered.
:::
```

#### `:::important`  **[TODO]**
- **When:** a must-not-miss constraint/prerequisite that isn't a hazard.
- **Attributes:** none.
- **Inner:** markdown, 1–2 sentences.
- **Render:** `<div class="cmp-important">` — lavender tint `#eeedfe`, text `#26215c`, 3px left `--accent` rule, ❗ icon, bold "Important" label prepended.
```
:::important
You must verify your email before the free uncensored trial unlocks.
:::
```

#### `:::definition`  **[TODO]**
- **When:** a crisp, quotable one-line definition of the article's core term, at first mention.
- **Attributes:** `term="<the term>"` (**required**).
- **Inner:** markdown — the definition (one sentence).
- **Render:** `<div class="cmp-definition">` — `--surf` one-liner with left `--accent` rule; render `<strong class="term">term</strong>` as a lead-in, then the inner definition. (Optionally emit `DefinedTerm` JSON-LD — nice-to-have, not required.)
```
:::definition term="Parasocial bond"
A one-sided emotional attachment a user forms toward a conversational agent that cannot reciprocate.
:::
```

#### `:::primer`  **[TODO]**
- **When:** redirect a beginner to a foundational guide early ("New to X?"). Top of intermediate/advanced posts.
- **Attributes:** `href="<destination URL>"` (**required**), `thumb="<image URL/path>"` (optional).
- **Inner:** markdown — the prompt line and/or linked title (e.g. `New to AI companions? Start with **[our beginner's guide](…)**`). If `href` is set and the inner omits a link, the renderer links the whole card to `href`.
- **Render:** `<a class="cmp-primer" href="…">` — small bordered card near the top: `thumb` image left (omit the slot if absent), prompt + linked title right.
```
:::primer href="/blog/ai-companions-101" thumb="/img/primer-101.png"
**New to AI companions?** Start with our beginner's guide.
:::
```

#### `:::proscons`  **[TODO]**
- **When:** balanced two-column verdict on one option.
- **Attributes:** none.
- **Inner:** markdown with exactly two H2s — `## Pros` then `## Cons`, each followed by a bullet list.
- **Render:** `<div class="cmp-proscons">` with two `.col` panels side-by-side (stack on mobile). Pros panel: positive tint `#eaf3de`, each `<li>` prefixed with a green ✓ (`#178a3c`). Cons panel: neutral/`--surf`, each `<li>` prefixed with a red ✕ (`#c2371f`). Parse the two H2 sections; render their bullets, drop the literal "Pros"/"Cons" headings into the panel labels.
```
:::proscons
## Pros
- Flat pricing, no coin meter
- Strong long-term memory
## Cons
- No mobile app yet
- Smaller character library
:::
```

#### `:::feature-matrix`  **[TODO]**
- **When:** head-to-head across many features × many products.
- **Attributes:** none.
- **Inner:** a single **GFM table**. First column = feature/product label. Body cells use the tokens `yes` / `no` / `partial` (case-insensitive) to mean ✓ / ✕ / –; any other cell text renders as-is (markdown).
- **Render:** `<div class="cmp-feature-matrix">` wrapping a styled `<table>`: header `--surf` tint, first column emphasized (`font-weight:600`), horizontal scroll on narrow viewports. Map cell tokens: `yes`→`<span class="yes">✓</span>` (`#178a3c`), `no`→`<span class="no">✕</span>` (`#c2371f`), `partial`→`<span class="partial">–</span>` (`--mut`). Provide `aria-label` ("Yes"/"No"/"Partial") on each glyph for a11y.
```
:::feature-matrix
| Feature            | Pleasur.AI | Comp A  | Comp B  |
|--------------------|------------|---------|---------|
| Uncensored chat    | yes        | partial | no      |
| Voice calls        | yes        | no      | partial |
| Persistent memory  | yes        | yes     | no      |
:::
```

#### `:::decision-table`  **[TODO]**
- **When:** Ahrefs' signature technical classification grid — categorize options without declaring a single winner. Pair with `:::preferred-order`.
- **Attributes:** none.
- **Inner:** a single **GFM table**.
- **Render:** `<div class="cmp-decision-table">` wrapping a styled `<table>`: header `--surf` tint, first column emphasized, hairline rows, horizontal scroll on mobile. No winner-row treatment (that's `:::table emphasize-row`). Renders the same cell tokens as feature-matrix if present, else plain markdown.
```
:::decision-table
| Scenario                  | Best model type     | Why                          |
|---------------------------|---------------------|------------------------------|
| Roleplay, long memory     | Local 70B           | No filter, full context      |
| Quick mobile chat         | Hosted small model  | Latency + cost               |
:::
```

#### `:::preferred-order`  **[TODO]**
- **When:** the explicit ranked recommendation that follows a decision/feature comparison ("here's the order I'd pick them").
- **Attributes:** none.
- **Inner:** markdown **ordered list** (`1. … — use when …`). Each item = a pick + a "use when you…" qualifier.
- **Render:** `<ol class="cmp-preferred-order">` — accent-colored ordinals (`--accent`), each `<li>` shows the pick (bold lead) then the qualifier in `--mut`. This replaces the old `:::recommend` idea — there is **no** single "winner badge".
```
:::preferred-order
1. **Pleasur.AI** — use when you want flat pricing and the strongest memory.
2. **Competitor A** — use when you only need casual, occasional chat.
3. **Competitor B** — use when a mobile app is non-negotiable today.
:::
```

#### `:::verdict`  **[TODO]**
- **When:** the one-line "bottom line on this option" inside a roundup entry or comparison.
- **Attributes:** none.
- **Inner:** markdown — one decisive sentence.
- **Render:** `<div class="cmp-verdict">` — accent-tinted band (`#eeedfe`), bold "Verdict." lead-in, the sentence after.
```
:::verdict
The best all-round pick for daily users who hate coin meters.
:::
```

#### `:::badge`  **[TODO]**
- **When:** a qualitative award on a roundup entry. Prefer "Best for X" labels over numeric scores.
- **Attributes:** `kind="best-overall|editors-pick|best-free"` (**required**; unknown kind → render the raw kind text title-cased).
- **Inner:** optional markdown — override label text; if empty, derive from `kind` (`best-overall`→"Best overall", `editors-pick`→"Editor's pick", `best-free`→"Best free").
- **Render:** `<span class="cmp-badge cmp-badge--<kind>">` — small pill, `--accent` fill, white text; place adjacent to the entry header. Inline element (no block margin).
```
:::badge kind="best-overall"
:::
```

#### `:::stat`  (and `:::stat-group`)  **[BUILT]**
- **`:::stat` attributes:** `value="<the figure>"` (**required**), `source="<name>"` (optional), `source_url="<https URL>"` (optional).
- **`:::stat` inner:** markdown, a short label/claim.
- **`:::stat` render:** `<div class="cmp-stat">` — oversized `.v` numeral (`value`), `.l` muted label (inner); if `source`+`source_url` present, a small inline source link/pill.
- **`:::stat-group` render:** `<div class="cmp-stat-group">` — auto-fit grid of child stat cards, pairs sit 2-up. (The only block-nesting case besides table fences.)
```
:::stat-group
:::stat value="$12/mo" source="Pricing audit" source_url="https://example.com/pricing"
median paid tier
:::
:::stat value="3.2M" source="Sensor Tower" source_url="https://example.com/downloads"
monthly downloads
:::
:::
```

#### `:::stat-list`  **[TODO]**
- **When:** a dense, cited *list* of findings (vs the big-number `:::stat` cards).
- **Attributes:** none.
- **Inner:** markdown **bullet list**, each bullet a cited finding (`- **68%** of users … ([Internal survey](https://…))`).
- **Render:** `<ul class="cmp-stat-list">` — each `<li>` keeps its bold leading figure at full emphasis, claim in body color, the trailing link rendered as a small `--mut` source link. No card; a clean vertical list with comfortable row spacing.
- **Dedupe:** this is the list cousin of `:::stat`/`:::stat-group`; use `:::stat-group` for 2–4 hero numbers, `:::stat-list` for 5+ cited rows.
```
:::stat-list
- **68%** of users cite loneliness as the primary driver. ([Internal survey](https://example.com/s))
- **$21.40** median real monthly cost across 14 apps. ([Pricing audit](https://example.com/p))
:::
```

#### `:::table`  **[BUILT]**
- **Attributes:** `caption="<above-table caption>"` (optional), `source="<credit>"` (optional), `emphasize-row=<1-based row index>` (optional).
- **Inner:** a single **GFM table** (also used for the "best-for summary" 2-col variant — name cells may be jump-links).
- **Render:** `<div class="cmp-table">` — `.cap` caption above (`--mut`), styled `<table>` (header `--surf` tint), the `emphasize-row` body row gets `.win` (bold, `#e6f1fb` bg), `.src` source credit below (`--hint`). GFM links inside cells render normally.
```
:::table caption="Real median monthly cost by app tier, May 2026" source="14-app pricing audit" emphasize-row=1
| Tier | List price | Real cost | Metered? |
|------|-----------|-----------|----------|
| Pleasur.AI Standard | $27.99 | $27.99 | Flat |
| Competitor A "Unlimited" | $12.99 | $34.10 | Coins |
:::
```

#### `:::expert`  **[BUILT]**
- **Attributes:** `name="<person>"` (**required**), `title="<role>"` (optional), `company="<org>"` (optional), `company_url="<https URL>"` (optional), `photo="<image URL/path>"` (optional).
- **Inner:** markdown — the quote (bold the key phrase).
- **Render:** `<div class="cmp-expert">` — circular `.av` headshot (`photo`, else initials on `#0f6e56`) left, `.q` quote, then `.nm` name + `.ro` role with linked `company`→`company_url`. Cluster adjacent `:::expert` blocks as a "consensus" row.
```
:::expert name="Dr. Jane Roe" title="Researcher" company="MIT Media Lab" company_url="https://media.mit.edu" photo="https://example.com/jane.jpg"
Parasocial bonds with conversational agents are **real, measurable, and durable**.
:::
```

#### `:::pullquote`  **[BUILT]**
- **Attributes:** `cite="<Name, Title, Org>"` (optional), `source="<https URL>"` (optional).
- **Inner:** markdown — the memorable line (one sentence).
- **Render:** `<blockquote class="cmp-pullquote">` — larger serif, left `--accent` rule; `<cite>` attribution beneath (link to `source` when present).
```
:::pullquote cite="Jane Roe, Researcher, MIT Media Lab" source="https://media.mit.edu/quote"
The line between tool and companion is thinner than we like to admit.
:::
```

#### `:::tweet`  **[TODO]**
- **When:** real social proof from the source. Sparingly; degrade to `:::pullquote` if no live embed is wanted.
- **Attributes:** `url="<tweet/X status URL>"` (**required**).
- **Inner:** optional markdown — a plain-text fallback rendering of the tweet (used in no-JS / failed-embed cases).
- **Render:** `<figure class="cmp-tweet" data-tweet-url="…">` — lazy-load the native X embed widget client-side; if it fails or JS is off, render the inner fallback inside a bordered card with a "View on X" link to `url`. Never block render on the third-party script.
```
:::tweet url="https://x.com/someuser/status/123456789"
@someuser: AI companions crossed the line from novelty to habit this year.
:::
```

#### `:::video`  **[TODO]**
- **When:** a moving walkthrough beats a screenshot. Rare.
- **Attributes:** `src="<video or embed URL>"` (**required**), `title="<caption/title>"` (optional).
- **Inner:** optional markdown — caption/fallback text.
- **Render:** `<figure class="cmp-video">` — responsive 16:9 wrapper (`aspect-ratio:16/9`) holding a lazy-loaded `<iframe>` (YouTube/Vimeo/self-hosted) titled `title`; `title` (or inner) renders as a small `--mut` caption below. Lazy-load; never autoplay with sound.
```
:::video src="https://www.youtube.com/embed/abc123" title="Setting up your first companion"
:::
```

#### `:::faq`  **[TODO]**
- **When:** collapsible Q&A + FAQ schema (when schema capture is the goal; otherwise plain H2/H3 FAQs are house-standard).
- **Attributes:** none.
- **Inner:** markdown — repeated `### Question` headings, each followed by its answer (markdown).
- **Render:** `<div class="cmp-faq">` — each Q/A as a `<details class="cmp-faq__item"><summary>` (the H3 text) + answer body, chevron affordance, hairline rows. **Also emit `FAQPage` JSON-LD** (`<script type="application/ld+json">`) built from every Q/A pair. Parse by splitting inner on `###` boundaries.
```
:::faq
### Are AI companion apps free?
Most offer a limited free tier; uncensored modes are typically paid.
### Do they remember past conversations?
The better ones keep persistent memory across sessions; basic ones reset.
:::
```

#### `:::jumplinks`  **[TODO]**
- **When:** an explicit writer-chosen jump menu (distinct from the auto TOC) — e.g. "skip to the app you want".
- **Attributes:** none.
- **Inner:** markdown **link list** of in-page anchors (`- [Best overall](#best-overall)`).
- **Render:** `<nav class="cmp-jumplinks">` — a compact tinted row/wrap of anchor "chips" (`--surf` pills, `#185fa5` text). Each links to its `#anchor`. (The auto TOC in bucket B is separate and metadata-driven.)
```
:::jumplinks
- [Best overall](#best-overall)
- [Best free](#best-free)
- [Best for roleplay](#best-roleplay)
:::
```

#### `:::figure`  **[TODO]**
- **When:** any standalone captioned image with an attribution line.
- **Attributes:** `src="<image URL/path>"` (**required**), `source="<credit text or URL>"` (optional).
- **Inner:** markdown — the caption.
- **Render:** `<figure class="cmp-figure">` — centered `<img>` (rounded, `max-width:100%`, lazy-loaded; derive `alt` from the caption text), `<figcaption>` with the caption (`--mut`) and, if `source` present, a "Source: …" line (`--hint`; linked if `source` is a URL).
```
:::figure src="/img/pricing-chart.png" source="https://example.com/data"
Median real monthly cost across 14 apps, May 2026.
:::
```

#### `:::diagram`  **[TODO]**
- **When:** a produced explanatory diagram/schematic (the framed cousin of figure).
- **Attributes:** `src="<image/SVG URL/path>"` (**required**), `source="…"` (optional).
- **Inner:** markdown — the caption.
- **Render:** `<figure class="cmp-diagram">` — framed/tinted container (`--surf` bg, `--line` border, generous padding) around the `<img>`/inline SVG, `<figcaption>` caption below (`--mut`). Same a11y/lazy rules as figure.
```
:::diagram src="/img/memory-architecture.svg"
How persistent memory flows from chat → embedding store → recall.
:::
```

#### `:::entry`  (roundup entry header)  **[TODO]**
- **When:** standardize each roundup option's intro (number + name + "best for" + price). One per option section.
- **Attributes:** `n="<rank number>"` (**required**), `name="<option name>"` (**required**), `url="<option's external URL>"` (optional), `best_for="<one-line use case>"` (optional), `price="<price string>"` (optional).
- **Inner:** optional markdown — a short lead-in blurb under the header.
- **Render:** `<header class="cmp-entry" id="<slug(name)>">` — `.n` numbered eyebrow (accent), the `name` as the section heading (linked to `url` when present, opens its own anchor `id`), a `.best-for` eyebrow ("Best for: …") and a bold `.price` line; then the inner blurb. The auto-generated `id` lets `:::jumplinks` / best-for tables link to it.
```
:::entry n="1" name="Pleasur.AI" url="https://pleasur.ai" best_for="Daily users who want flat pricing" price="$27.99/mo"
The all-round pick: flat pricing, strong memory, uncensored modes.
:::
```

#### `:::further-reading`  **[BUILT]**
- **Attributes:** none.
- **Inner:** markdown — one or more bulleted links (a mid-article hand-off to a deeper guide). (Inline single-link form `**Recommended reading:** *[Title](url)*` may also appear as plain prose; only the fenced form needs special rendering — distinct from the end-of-article `cmp-keep-learning` grid in bucket B.)
- **Render:** `<div class="cmp-further-reading">` — info-tinted band (`#e6f1fb`), bold "Further reading" `.l` label, bulleted/italic link(s).
```
:::further-reading
- [How LLM companions actually work](/blog/how-llm-companions-work)
- [Uncensored vs filtered: what changes](/blog/uncensored-vs-filtered)
:::
```

#### `:::cta`  **[BUILT]**
- **Attributes:** `heading="<headline>"` (optional), `button="<button label>"` (optional), `href="<destination, e.g. /pricing>"` (optional).
- **Inner:** markdown — a one-line value proposition.
- **Render:** `<div class="cmp-cta">` — bordered/shaded box (centered), `<h3>heading</h3>` + the inner value-prop line (`--mut`) + a `.btn` button (`button` label, `--accent` fill, linking to `href`). Used once high, once low; map to a Pleasur.AI product.
```
:::cta heading="Build your AI companion free" button="Start now" href="/pricing"
Spin up a personalized companion in under a minute — no card required.
:::
```

---

### Bucket B — AUTO-INJECTED (page template renders from article/author metadata — NO writer fence)

These are **render-only**: the writer emits nothing. The CTO builds the page template to read the article body / front-matter / author record and inject these. Documented here so the markup contract is unambiguous.

#### Table of contents — `cmp-toc`  **[TODO]**
- **Source:** built automatically from the rendered **H2/H3 tree** (each heading must carry a stable slug `id`). No fence; trigger when ≥4 H2s or >1,500 words.
- **Variants (build both):**
  - **Inline** — `<nav class="cmp-toc cmp-toc--inline">` placed directly below the intro: "Contents" label + nested `<ol>` of anchor links (H3s indented under their H2).
  - **Sticky** — `<nav class="cmp-toc cmp-toc--sticky">` in a side rail on wide viewports (hidden on mobile, where the inline one serves).
- **Active-section highlight:** an IntersectionObserver adds `.is-active` to the link whose section is in view (accent text/left-rule on the active item). Smooth-scroll on click.

#### "Keep learning" related-posts grid — `cmp-keep-learning`  **[TODO]**
- **Source:** related posts from CMS metadata (same category / tags / explicit related slugs). No fence; rendered at the **very end** (after the bio).
- **Render:** `<section class="cmp-keep-learning">` — "Keep learning" heading + a responsive card grid (`auto-fit minmax(220px,1fr)`); each card = thumbnail + linked headline + 1-line dek. 3–6 cards.

#### Author bio box — `cmp-author-bio`  **[TODO]**
- **Source:** the `author` front-matter resolved against the author DB (the Strapi authors we already create). No fence; rendered at the close.
- **Render:** `<aside class="cmp-author-bio">` — larger circular avatar, name (linked to author page), role/title, 2–3-line bio, social icons. Reuses byline data but in the long form.

#### Contributors / "Reviewed by" — `cmp-contributors`  **[TODO]**
- **Source:** `co_authors:` and `reviewed_by:` from metadata. No fence; a sub-block under the bio (or beside it).
- **Render:** `<div class="cmp-contributors">` — small section: "Contributors" with co-author avatars + linked names, and a "Reviewed by ✓ [Name]" line (`#0f6e56` check) for the reviewer. Mirrors the byline's reviewed-by but expanded with roles.

#### OPTIONAL / likely-skip (document as stubs; do NOT build unless asked)
- **Article-performance metrics box** — `cmp-article-performance` — Ahrefs dogfoods its own SEO traffic data here; we have **no analogue**. **Skip.** If ever built: a small stat-strip near the top (traffic / keywords / backlinks).
- **Newsletter signup form** — `cmp-newsletter` — we have **no list yet**. **Skip.** If ever built: an inline email-capture band (heading + email field + submit), once mid/end.

---

### Bucket C — INLINE treatments & writer conventions

Verified against Ahrefs' live CSS, then **adapted to our brand** (purple `#534ab7` — we do **not** copy Ahrefs' hexes). The first three are render rules on inline elements; the rest are **writer voice-rules** (no render component).

#### Inline code / formula — `code` (not inside `<pre>`)  **[TODO]**
- **What:** a standard inline `` `code` `` span — this is the "colored formula" device for math, formulas, literal values, tokens, file names, short commands. **Ahrefs uses crimson `#c7254e` on pink `#f9f2f4`; we use a soft on-brand lavender instead.**
- **Authoring:** plain backticks — `` the formula is `CAC = spend / signups` ``. No fence.
- **Render contract:**
```css
code{
  background:#efeefc;        /* soft on-brand lavender (NOT Ahrefs pink) */
  color:#4338ad;             /* on-brand purple ink (NOT crimson)        */
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:.875em;
  padding:.1em .4em;
  border-radius:4px;
  white-space:nowrap;        /* keep short formulas/values intact        */
}
pre code{                    /* code BLOCKS opt out of the inline chip    */
  background:none;color:inherit;padding:0;border-radius:0;white-space:pre;
}
```
- Applies only to **inline** `<code>`; fenced/indented code blocks (` ``` `) keep normal block styling.

#### Lead paragraph — `cmp-lead`  **[TODO]**
- **What:** the opening paragraph rendered larger for an editorial open. **Ahrefs ≈ 22px, weight 400 (NOT bold).**
- **Authoring:** wrap the first paragraph in `{lead}…{/lead}`, OR let the renderer auto-detect the **first `<p>`** after the H1/byline (and after nutshell, if present) and apply the class. Support both; `{lead}` wins if present.
- **Render contract:**
```css
.cmp-lead{
  font-size:1.375rem;   /* ~22px */
  line-height:1.5;
  font-weight:400;      /* larger, NOT bold */
  color:var(--ink);
  margin:0 0 1.25rem;
}
```
```
{lead}AI companion pricing is full of "unlimited" claims that quietly meter you. We subscribed to 14 apps and tracked what a real month costs.{/lead}
```

#### Mark / highlight — `<mark>`  **[TODO]**
- **What:** highlight a few key words. Use **sparingly**.
- **Authoring:** `==highlighted text==` → `<mark>highlighted text</mark>`.
- **Render contract:**
```css
mark{
  background:#efe9c8;   /* soft on-brand highlight */
  color:inherit;
  padding:0 .12em;
  border-radius:2px;
}
```

#### Writer conventions (voice rules — NOT render components)
These belong in `/draft`'s voice guardrails, not in the renderer. Stated here so the catalog is complete and nobody builds a component for them:
- **Inline citations are plain links** — every stat/claim links to its source as ordinary inline anchor text. **NO superscript footnote markers**, no `[1]`-style endnotes.
- **Colored bold only inside box components** — emphasis in body prose is plain `**bold**` (inherits `--ink`). Accent/colored bold is a property of box components (methodology, key-takeaways, etc.), **not** a free inline token the writer reaches for.
- **Close with a "Final thoughts" / "Bottom line" H2** — the standard closer heading; not a styled component.
- **No numbered headings** — section headings are plain text, never "1. …", "2. …".
- **No drop caps, no font changes** — the open is the `cmp-lead` size bump only.

---

### Renderer acceptance checklist (complete — BUILT + TODO)

**Parser core**
- [ ] Parses opener `:::<name>` (no space after `:::`) + same-line `key="value"` attrs (any order, all optional unless required) + bare-`:::` closer.
- [ ] Renders inner content as **markdown** (incl. **GFM tables** and inline `<code>`), not plain text.
- [ ] Handles the two nesting cases only: `:::stat` inside `:::stat-group`; GFM table inside `:::table` / `:::feature-matrix` / `:::decision-table`.
- [ ] Unknown attribute ignored; unknown fence name degrades to a plain `<aside>`/blockquote (never dropped).

**Bucket A — authored fences (each emits `cmp-<name>`)**
- [ ] **[BUILT]** byline · nutshell · methodology · key-takeaways · sidenote · tip · note · stat · stat-group · table · expert · pullquote · further-reading · cta — all match `component-mockup.html`.
- [ ] **[TODO]** warning · important · definition (`term`) · primer (`href`,`thumb`) · proscons (`## Pros`/`## Cons` → ✓/✕ panels) · feature-matrix (GFM + `yes`/`no`/`partial`→✓/✕/–) · decision-table (GFM grid) · preferred-order (ranked list) · verdict · badge (`kind`) · stat-list (cited bullets) · tweet (`url`, lazy embed + fallback) · video (`src`,`title`, 16:9 lazy) · faq (`### Q`/A → `<details>` **+ FAQPage JSON-LD**) · jumplinks (anchor chips) · figure (`src`,`source`) · diagram (`src`) · entry (`n`,`name`,`url`,`best_for`,`price` → header + anchor id).
- [ ] Attribute-only sublines render: methodology (updated/by), stat (source→source_url pill), expert (name/title/company→company_url/photo), pullquote (cite→source), cta (heading/button→href), definition (term lead-in), primer (card→href), entry (best_for/price + anchor id), badge (kind→label).
- [ ] `:::sidenote` vs `:::note` vs `:::warning` vs `:::important` styled distinctly (grey rule / blue ℹ️ / amber ⚠️ / lavender ❗).
- [ ] Comparison glyph tokens map consistently everywhere: `yes`→✓ `#178a3c`, `no`→✕ `#c2371f`, `partial`→– `--mut`, each with an a11y label.

**Bucket B — auto-injected (no fence; from metadata)**
- [ ] `cmp-toc` inline **and** sticky variants, auto from H2/H3 slugs, active-section highlight + smooth scroll.
- [ ] `cmp-keep-learning` related grid at end (from CMS related metadata).
- [ ] `cmp-author-bio` at close (from author record) + `cmp-contributors` ("Reviewed by ✓" + co-authors).
- [ ] `cmp-article-performance` and `cmp-newsletter` left as documented **skips** (not built).

**Bucket C — inline treatments**
- [ ] Inline `<code>` styled as the on-brand lavender chip (`#efeefc`/`#4338ad`); `pre code` opts out.
- [ ] `cmp-lead` from `{lead}…{/lead}` **or** first-paragraph auto-detect (22px / weight 400).
- [ ] `==text==` → `<mark>` (on-brand highlight).
- [ ] Voice conventions enforced in `/draft`, not the renderer: plain-link citations (no superscripts), colored bold only in boxes, "Final thoughts/Bottom line" closer, no numbered headings, no drop caps.

> **Brand guardrail:** every accent/tint above derives from our purple `#534ab7` token system (see *Shared design tokens*). Do not reintroduce Ahrefs' crimson/pink/blue hexes — the inline-code chip in particular is on-brand lavender, by design.
