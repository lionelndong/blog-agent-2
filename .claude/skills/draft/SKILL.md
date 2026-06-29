---
name: draft
description: Expand an annotated outline into full article prose using brand voice anchored in example articles, hitting the outline's per-section depth targets. Triggered after /product-mentions.
allowed-tools: Read, Write, Glob
---

# Draft Skill

Turn the annotated outline into a publishable first draft. The draft is **not** final — `quality-check`, `verify-claims`, `generate-visuals`, `preview`, `format-for-publish` follow. But it should be 80% there.

## What changed (2026-06-12) — read this if you remember the old rules

The old skill enforced numeric voice quotas (24–35-word paragraphs, em-dashes per 1,000 words, you-words per 1,000 words). Optimizing those quotas produced metric-compliant, soulless prose: uniform 2-sentence paragraphs, choppy rhythm, one rhetorical tic repeated eight times — exactly the AI tells we're paid to avoid. **Those quotas are gone.** Voice now comes from the example articles, depth comes from the outline's word targets, and the only mechanical rules left are the ones that catch real failure (crutch repetition, forbidden phrases, throat-clearing).

## The three commitments

1. **Depth.** Hit every section's word target ±20%, and the article total ±15% of the beat-spec target (restated at the top of the outline). If you finish a section 40% under target, you skipped evidence or specifics — go back to the dossier and add the missing concrete material. Never pad with abstractions to hit a number; depth = more specifics, not more words about words.
2. **Specificity.** Every section earns its length with concrete material: named tools, real numbers (cited), steps a reader can follow, first-hand product detail, real user language from the deep-research file. A paragraph with no specific noun or number in it is a candidate for deletion.
3. **Voice from examples.** Before writing a word: read `examples/README.md`, then **2 voice articles from `examples/voice/` in full, plus the 1 structure/niche example closest to this content type**. The prose in those files is the spec. Rules below are guardrails only.

## Input

For slug `{slug}`:
- `content-pipeline/4-outlines-annotated/{slug}.md` (required — outline with product annotations; includes beat-spec restatement + per-section word targets)
- `content-pipeline/0-context/{slug}.md` (if exists — user direction; wins all conflicts)
- `content-pipeline/2-reference/{slug}.md` (brand context, internal-link opportunities)
- `content-pipeline/1-research/{slug}.md` + `{slug}-deep.md` (evidence, stats, user quotes)
- `brand-config.md` (voice, audience, products, **forbidden phrases**)
- `references/voice-guide.md` (structural voice rules) + `references/prose-patterns.md` (sentence-level patterns)
- `../../../templates/visual-strategy.md` (**THE GOVERNING SPEC for placing `[VISUAL:]` — read it**: resolvable data, no native-component duplication, value-first ~80/20, the type catalog)
- `../../../templates/visual-types.md` (the controlled `[VISUAL:...]` vocabulary + selection guide; follows visual-strategy.md)
- `examples/authors.md` (the persona map + content-type → persona selection rule + byline-comment contract)
- `examples/component-cheatsheet.md` (**PRIMARY component reference — the writer's menu**: when to reach for each component, how to write it, and the caps; consult this first per step 5a)
- `examples/ahrefs-components.md` (the deep `:::component` spec — fence grammar + exact attribute names; consult when the cheatsheet isn't enough)
- `examples/voice/` (per-persona `persona.md` + type-tagged anchor articles) — and the rest of `examples/` per commitment #3

## Process

1. **Read examples first** (commitment #3). Then the outline thoroughly — you're not re-architecting; the outline is the spec. Then context, references, research, brand-config.
2. **Select the author persona.** From the article's content-type (per the outline / beat-spec format), pick the persona using `examples/authors.md`'s selection rule; when ambiguous, fall back to **theo-hart**. Load `examples/voice/<persona>/persona.md` AND the type-matched anchor article in that persona's folder (fetch it live if it isn't cached). Write the whole draft in **THAT persona's craft, but in OUR register** (`brand-config.md`) — craft, not register; never reuse the anchor's text, examples, or structure. **Stamp the byline as the very first line of the draft file** (before the H1), using the exact contract from `examples/authors.md`:
   ```
   <!-- byline: <Byline Name> | persona: <persona-slug> -->
   ```
   e.g. `<!-- byline: Sloane Avery | persona: sloane-avery -->`. `/format-for-publish` reads this line to attach the Strapi author relation, so keep the format byte-for-byte exact.
3. **Draft the intro** (150–200 words): hook (direct claim, surprising cited stat, opinion, or problem-naming), thesis, preview.
4. **Draft each H2 in order:**
   - Open with the section's BLUF (or a sentence capturing the same idea)
   - Develop key points using `references/prose-patterns.md`; pull the evidence the outline specified — stats carry a `[link]` placeholder when you lack the exact URL (verify-claims resolves them; they must NOT survive past that stage)
   - Hit the section word target ±20% with specifics, per commitments #1–2
   - Product mentions exactly where annotated — "show, don't sell"
   - Internal links from `2-reference/` inline as `[anchor](URL)`
   - Close with a transition
5. **Tables are content, not decoration.** Where the outline specs a comparison table, author it as a real GFM markdown table with every column and row filled from research. `/format-for-publish` handles site-renderer conversion (PLEAA-567) — never pre-degrade a table into bullets at draft time. The preview and the editor see the real table.
5a. **Emit the Ahrefs component fences the outline planned — with RESTRAINT — drawing on the FULL authored set.** Consult **`examples/component-cheatsheet.md` first — it is the writer's menu** (when to reach for each component, the exact authoring syntax, and the caps), and drop to `examples/ahrefs-components.md` (the deep spec — its `## Render contract` has the exact fence grammar + attribute names) when the cheatsheet isn't enough. EMIT the `:::component` fences where a section genuinely calls for one. The outline already *planned* which components each section carries; your job is to *emit* them in the prose. **Reach for whatever component the content actually calls for — not just the house-standard few — but stay disciplined.** Restraint is the paramount rule: **1–2 of each per article, only when it improves scannability — never decorate, never wrap a section in a box just because it can be.** A typical article uses only the handful its content demands; most sections carry zero. A wall of boxes reads worse than clean prose. Use the fence names EXACTLY (byte-for-byte, lowercase, hyphenated) as in the cheatsheet. **The pre-publish `components` checker (`scripts/lint_components.py`, run by `scripts/pipeline_gate.py`) enforces the caps and every fence's required attributes — an over-decorated or malformed article HALTS before publish, so author within the menu's limits.**

   **House-standard triggers → component:**
   - the top/one-paragraph answer (one, directly under the H1) → `:::nutshell`
   - an article's conclusions, front-loaded for skimmers → `:::key-takeaways`
   - one load-bearing number you want impossible to miss → `:::stat` (wrap 2–4 in `:::stat-group`)
   - a data study's data disclosure (source, sample, definitions) → `:::methodology`
   - an aside / caveat / source-note that would derail the sentence → `:::sidenote`
   - an expert opinion attributed to a named person → `:::expert`
   - a deeper subtopic that has its own article (mid-article hand-off) → `:::further-reading`
   - a memorable, quotable line → `:::pullquote`
   - a reader → product push (once high, once low) → `:::cta`
   - a pro shortcut next to the step it improves → `:::tip` (also `:::note` for an easily-missed caveat)

   **High-value additions — emit these when (and only when) the content type + section call for them:**
   - **first mention of the article's core term** → `:::definition term="…"` (one crisp, quotable sentence)
   - **a pitfall / must-know** → `:::warning` (risky, data-loss, or money-loss action) or `:::important` (a must-not-miss prerequisite/constraint that isn't a hazard)
   - **a comparison / "which should I use" section** → `:::proscons` (one option's balanced verdict, `## Pros` then `## Cons`), `:::feature-matrix` (many features × many products; cells `yes`/`no`/`partial`), `:::decision-table` (classify options in a grid — no single winner), and the `:::preferred-order` ranked list that follows it (`1. **Pick** — use when you…`). One decisive call on an option → `:::verdict`.
   - **a cited statistics roundup (5+ sourced figures)** → `:::stat-list` (one cited finding per bullet, `- **68%** … ([Source](url))`). Keep `:::stat`/`:::stat-group` for 1–4 hero numbers — do NOT use `:::stat-list` for fewer than 5.
   - **an FAQ section** → `:::faq` (repeated `### Question` + answer; the renderer adds FAQPage schema). Plain H2/H3 FAQs remain fine — reach for `:::faq` only when schema capture is the point.
   - **roundup / listicle scaffolding** → `:::jumplinks` (a writer-chosen "skip to the app you want" anchor menu) + one `:::entry n="1" name="…" url="…" best_for="…" price="…"` header per option section; a qualitative award → `:::badge kind="best-overall|editors-pick|best-free"`.
   - **a captioned data figure / diagram** → `:::figure src="…" source="…"` / `:::diagram src="…"` only when you already have a real `src` on disk. **Visuals are ON (2026-06-29):** for every visual the outline planned, emit the typed `[VISUAL:...]` placeholder (step 6) and let `/generate-visuals` realize it into `![alt](images/<slug>/file.png)`. Reach for a `:::figure`/`:::diagram` fence only when pointing at an asset that already exists.
   - **situational embeds** → `:::tweet url="…"` (real social proof; degrade to `:::pullquote` if no live embed) · `:::video src="…" title="…"` (a moving walkthrough beats a screenshot; rare).

   **INLINE treatments (no fence — these are the typographic devices, governed by voice):**
   - **inline `` `code` `` for math / formulas / literal values** — this is the "colored formula" device. Wrap any formula, equation, token, file name, or short literal value in backticks: `` the formula is `CAC = spend / signups` ``. The renderer styles inline code as the on-brand chip. (Fenced ```` ``` ```` code BLOCKS opt out — keep those for multi-line code only.)
   - **wrap the opening paragraph in `{lead}…{/lead}`** — the editorial lead (rendered ~22px, weight 400, NOT bold). One per article, the first paragraph after the H1/byline (and after `:::nutshell` if present).
   - **`==text==` for the rare highlight** → `<mark>`. Use sparingly — a few key words at most.

   **Voice conventions (already partly in force — hold the line):**
   - **inline citations are plain links** — every stat/claim is an ordinary inline anchor to its source. **NO superscript footnotes, no `[1]`-style endnotes.**
   - **colored bold lives only inside box components** — body-prose emphasis is plain `**bold**`; never reach for accent/colored bold as a free inline token.
   - **close with a "Final thoughts" / "Bottom line" H2** — the standard closer heading.
   - **no numbered headings** ("1. …", "2. …") and **no drop caps** — the open is the `{lead}` size bump only.

   **Per-persona favorites** (lean toward your selected persona's set; don't force the others): **Sloane Avery** → `:::methodology` / `:::stat` / `:::stat-list` / `:::table` / `:::key-takeaways`; **Theo Hart** → tables / numbered steps / `:::decision-table` / `:::preferred-order` / `:::feature-matrix` / `:::cta` / `:::further-reading`; **Mateo Reyes** → `:::expert` / `:::pullquote` / `:::tweet` / `:::nutshell` / `:::sidenote` / `:::figure`. The shorthands `**Tip:**` / `**Note:**` / `**Sidenote:**` / `**Methodology:**` / `**In a nutshell:**` / `**Key takeaways:**` are also accepted — `/format-for-publish` normalizes them to their fences — but prefer authoring the explicit `:::fence` so the preview matches the published page.
6. **Place the typed `[VISUAL:]` placeholders — governed by `templates/visual-strategy.md`.** Emit one per `Visual N:` entry the outline planned, at a natural break in the section it belongs to (never two stacked back-to-back). Four hard rules gate every placeholder — break any one and the visual loud-fails the visuals stage, duplicates a component, or ships vague:

   - **(a) RESOLVABLE DATA (kills the invented-key bug).** A `chart` / `diagram` / data `table` **MUST** reference data that actually exists: either a real `research.<key>` that you have **verified is present in `content-pipeline/1-research/{slug}-data.json`**, or a `config=<file>` you author yourself. **NEVER invent a key.** (The real failures we shipped: `data=research.five_failure_taxonomy` and `data=research.pricing.coin_tiers` when the keys did not exist — the placeholder loud-failed and left the section blank.) If the number/structure you want isn't in the research JSON: add it to the research data, author a `config=` file, or **drop the visual**. Never point at a key on faith.
   - **(b) NO native-component duplication (the duplicate bug).** Do **NOT** emit a `[VISUAL:]` for anything a native `:::` directive renders inline — a stat (`:::stat`), a quote (`:::pullquote`), a comparison / pros-cons / feature matrix / decision grid / simple data table (`:::table` · `:::feature-matrix` · `:::decision-table` · `:::proscons`), a tip/note/warning/takeaway/definition (`:::tip` · `:::note` · `:::warning` · `:::key-takeaways` · `:::definition`). A native component is **always** better than a PNG of the same thing (selectable, accessible, SEO-readable, responsive). If you already wrote the data as a `:::decision-table` or `:::table`, you may NOT also make a PNG table of it. `[VISUAL:]` PNGs are **only** for what text + natives can't show: real screenshots, branded charts of real data, concept diagrams/flows, covers, demos/GIFs, embeds.
   - **(c) VALUE-FIRST type choice (~80/20 — `type=external` is the workhorse).** Most placeholders should screenshot a **third party / the category** (a competitor companion app, a Reddit/forum thread, a real review/artifact, news, another tool — or a Google SERP). Reserve `type=screenshot`/`action-shot` of **our** product for moments the post is genuinely on-topic about Pleasur.ai. The same method applies to any product a post covers. **Vary the sources** — a Google SERP is just ONE source among many; **don't lean on SERP screenshots or fill a post with them** (strategy §3). Pick whichever source best proves *this* point.
   - **(d) ANNOTATE the callout on screenshots (don't ship a vague shot).** For every screenshot-type placeholder (`external`/`screenshot`/`action-shot`), **set `annotate=<what to point out>`** to the one thing the screenshot proves — a selector or a short phrase naming the element. A bare screenshot is vague; the reader doesn't know where to look (strategy §7). `/generate-visuals` runs it through `annotate_screenshot.py` (one brand-blue box + arrow + marker label). **Self-evident visuals — charts, diagrams, designed cards — carry NO `annotate`;** don't annotate the already-obvious.

   **Type catalog** (full field reference + selector cheatsheet in `templates/visual-types.md`):
   - `[VISUAL:type=external;sub=<reddit-comment|tweet|linkedin|news-quote|competitor-ui|serp|chart>;url=<source>;selector=<CSS>;crop=padded;what=<caption>;annotate=<what to point out>]` — **the workhorse: real third-party evidence.** Auto-captured (PLEAA-417). Reddit comments `#t1_<id>`, tweets `article[data-testid="tweet"]`, a SERP or competitor panel with the right `selector`. Always clip with `selector` — a viewport shot of a whole thread is wasted space. **Set `annotate=`** to the one thing the shot proves (rule d).
   - `[VISUAL:type=screenshot;target=<product-slug>;what=<UI element>;annotate=<what to point out>]` — **our product, on-topic posts only.** **Set `annotate=`** to the specific point (rule d).
   - `[VISUAL:type=action-shot;url=<starting URL>;goal=<explicit click-path under 60 words>;what=<caption>;annotate=<what to point out>]` — our logged-in product (**SFW — blur explicit + PII**); `/capture-visuals` drives Chrome (pinned to Sonnet); write the goal like briefing a human who has never seen the site. **Set `annotate=`** to the point the shot makes (rule d).
   - `[VISUAL:type=chart;data=research.<KEY-THAT-EXISTS>|config=<file>;style=<bar|line|pie>;title=<title>]` — branded chart from **real** data (rule a).
   - `[VISUAL:type=diagram;type=<linear|tree|flow|cycle>|config=<file>;what=<…>]` — concept / process / decision (the "illustration" slot); needs structured nodes via `data=`/`config=`, not prose (rule a).
   - `[VISUAL:type=cover;…]` · `[VISUAL:type=video;url=<…>;what=<…>]` · `[VISUAL:type=gif;what=<…>]`.
   - (`type=image` is **retired** — no AI metaphor art. Real imagery is captured from `pleasur.ai` or the third party, never generated. For a concept, use `diagram`; for data, `chart`.)
7. **Draft the conclusion** (80–150 words): thesis restated fresh + one next step.
8. **Self-edit pass — the human-editor read.** Read the full draft top to bottom and fix:
   - **Crutch repetition (the #1 tell):** any distinctive word or rhetorical move used 3+ times ("honest", "Here's the thing", "stated plainly", a verdict-sentence formula repeated per section). Two uses max; rewrite the rest with different constructions.
   - **Uniform rhythm:** if every paragraph is 1–3 short sentences, merge and vary. Good prose mixes one-sentence punches with 4–6-sentence developed paragraphs (look at how the example articles breathe). Avoid walls of text past ~90 words too — but vary, don't cap.
   - **Forbidden phrases** (brand-config list) — zero tolerance.
   - Sentences starting with "Furthermore", "Moreover", "It is important to note".
   - Filler intensifiers ("very", "really", "quite", "actually", "simply") where they carry no weight.
   - Every section opens with its BLUF; no section opens with throat-clearing.
   - Product mentions demonstrate, never list features.
   - **The empty-paragraph test:** any paragraph with no concrete noun, number, step, or example → cut it or make it concrete.
9. **Depth gate (replaces the old metrics gate).** Count words per section against the outline targets. Any section <80% of target → return to the dossier/deep file and add real material (an example, a number, a step, a user quote). Article total within ±15% of the beat-spec target. Only then save.
10. **Save** to `content-pipeline/5-drafts/{slug}.md` — byline comment first line, then the H1 title, then prose. No other metadata header.

## Output

`content-pipeline/5-drafts/{slug}.md` — word count per the beat spec (typically 1,800–4,000 words).

## Quality checklist

Before saving, confirm:
- [ ] Author persona selected from the content-type via `examples/authors.md`; drafted in that persona's craft, OUR register
- [ ] Byline comment is the **very first line** of the file (`<!-- byline: <Name> | persona: <slug> -->`), before the H1, exact format
- [ ] Read 2 voice examples + 1 structure/niche example this run (not from memory)
- [ ] Every outline section drafted; word targets hit ±20%; total ±15% of beat-spec target
- [ ] Listicle item count matches the outline (no compression)
- [ ] Comparison table authored as real markdown (when specced)
- [ ] Ahrefs `:::component` fences emitted where the outline planned them, drawn from the full authored set (definition/warning/important/proscons/feature-matrix/decision-table/preferred-order/verdict/stat-list/faq/jumplinks/entry/badge/figure/diagram/tweet/video as the content calls for them), with restraint (1–2 of each max, most sections zero); fence names exact per `examples/ahrefs-components.md`; never decorative
- [ ] Inline treatments applied where they fit: inline `` `code` `` for formulas/literal values, `{lead}…{/lead}` on the opening paragraph, `==mark==` only for the rare highlight
- [ ] Voice conventions held: plain-link citations (no superscripts), colored bold only inside boxes, a "Final thoughts"/"Bottom line" closer, no numbered headings, no drop caps
- [ ] No crutch word/move used 3+ times; paragraph rhythm varied
- [ ] Zero forbidden phrases; zero "Furthermore/Moreover/It is important to note" openers
- [ ] Every numerical claim cited or carrying `[link]` for verify-claims
- [ ] Product mentions only where annotated, demonstrative
- [ ] Every `[VISUAL:]` follows `templates/visual-strategy.md`: resolvable data (chart/diagram/table point at a real `research.<key>` or authored `config=` — NO invented keys), no native-component duplication (no PNG of a stat/quote/table/callout already in a `:::` directive), value-first ~80/20 (`type=external` third-party is the default; our-product only when on-topic), **sources varied** (not all Google SERPs), **screenshot-type visuals carry `annotate=<what to point out>`** (self-evident charts/diagrams don't), spaced (none stacked)
- [ ] Internal links from `2-reference/` woven in with descriptive anchors

## When the draft feels off

- **Sounds generic** → you didn't anchor in the examples. Re-read them, rewrite the worst two sections.
- **Sounds salesy** → cut product mentions that fail the "competent reader" test.
- **Sounds choppy** → rhythm is uniform. Merge paragraphs, vary sentence length.
- **Sounds thin** → it IS thin. Back to the dossier for specifics; never pad.

If two voice-fix passes don't help, the problem is upstream — fix the outline or the research, not the prose.
