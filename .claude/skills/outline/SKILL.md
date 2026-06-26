---
name: outline
description: Create a structured H2/H3 outline with BLUF openers and MECE coverage, bound by the research dossier's beat spec. Triggered after /research and /brand-reference.
allowed-tools: Read, Write
---

# Outline Skill

Turn the research dossier into the article's bones. The output is a detailed outline a writer (human or AI) can expand into prose without further research. **The outline is bound by the dossier's BEAT SPEC** — section count, item count, word targets, and required formats come from the SERP, not from habit.

## Input

For slug `{slug}`, reads:
- `content-pipeline/1-research/{slug}.md` (required — especially **BEAT SPEC**, "Recommended angle", consensus/gap topics)
- `content-pipeline/2-reference/{slug}.md` (recommended — brand context)
- `content-pipeline/0-context/{slug}.md` (if exists — user-provided angle; overrides everything else on conflict)
- `brand-config.md` (audience, voice)
- `references/bluf-mece-rules.md` (structural rules — must enforce)
- `../../../templates/outline-template.md` (the file structure)
- `../../../templates/visual-types.md` + `../../../templates/editorial-principles-visuals.md` (visual decisions)
- `examples/ahrefs-components.md` (the `:::component` catalog — plan which components each section carries per step 6a)
- `examples/` — read `examples/README.md`, then the **2 examples closest to this content type** (structure + niche). The examples are the structure/voice spec — Ryan's principle: anchor in real high-performing articles, never work from a distilled rule list alone.

## Process

1. **Read all inputs.** Restate the BEAT SPEC numbers at the top of your outline file so the draft stage sees them without re-opening the dossier.
2. **Choose the article title.** Direct, includes the primary keyword early, under 60 characters when possible.
3. **Write the thesis.** One sentence. The article's central argument.
4. **Decide content type.** Follow the beat spec's format. Deviating from the modal SERP format requires an explicit justification line in the outline ("SERP is listicles; we're doing X because …") — absent that, format parity is mandatory.
5. **Draft the H2 list — sized by the beat spec, not a fixed cap.**
   - Explainer/guide SERPs: typically 5–8 H2s.
   - Listicle/comparison SERPs: **one H2 (or H3 under a roundup H2) per item, item count ≥ beat spec's item target.** A 9-app SERP gets ≥9 apps — never compress to 4 "picks" unless the user's context file explicitly asks for a short list.
   - Every consensus topic from the beat spec maps to a section or a substantial subsection. List which H2 covers which consensus topic in a coverage map at the bottom of the outline.
   - At least one section delivers the beat spec's **information gain** — mark it `[GAIN]`.
   - Read the H2 list aloud as a sequence: does it argue the thesis? Is it MECE?
6. **For each H2, write:**
   - BLUF (one sentence; the section's opening line or close to it)
   - Key points (2–4 bullets)
   - Evidence (stat / quote / example / walkthrough — cite which dossier section it comes from)
   - **Word target** — per-section targets must sum to the beat spec's total ±10%. Weight by SERP attention: comparison/criteria sections get more, boilerplate sections get less.
   - Transition to next section
   - **Visuals** — one or more typed micro-specs (`screenshot` / `action-shot` / `table` / `chart` / `video` / `external` / `gif` / `none` — **no `image`: AI image generation is retired**), format:
     ```
     **Visuals:**
       Visual 1: {type: chart, data: <research.key>, style: bar, title: <title>}
       Visual 2: {type: screenshot, target: create, what: voice profile selector, annotate: arrow on speaker icon}
     ```
     Apply the decision sequence in `templates/editorial-principles-visuals.md`. The default for any non-trivial section (>300 words) is "this section deserves a visual; what kind?". For brand-product UI: `screenshot` if a single URL shows the state, `action-shot` if it takes clicks (routed to `/capture-visuals`). For quoted Reddit/tweets/news: `external` with a `selector`.
6a. **PLAN the Ahrefs components each section carries — with RESTRAINT — from the FULL authored set.** Consult `examples/ahrefs-components.md` (read its `## Render contract` for the exact fence names + attributes) and, for each section, note which `:::component` fence(s) the writer should emit at draft time (the writer EMITS in `/draft`; you PLAN here). Mark them on the section as a `**Components:**` line, e.g. `**Components:** :::stat (the 68% retention figure), :::sidenote (caveat on the sample)`. **Plan for whichever component the section's content + the article's type genuinely calls for — not just the house-standard few.** Restraint is the paramount rule: **1–2 of each per article, only where it genuinely improves scannability — never decorate.** Most sections carry zero. Use the fence names EXACTLY (byte-for-byte, lowercase, hyphenated) as in `ahrefs-components.md`.

   **House-standard triggers → component:**
   - the top/one-paragraph answer (plan ONE, directly under the H1) → `:::nutshell`
   - the conclusion's front-loaded takeaways → `:::key-takeaways`
   - one load-bearing number → `:::stat` (2–4 → `:::stat-group`)
   - a data study's data disclosure → `:::methodology` (place right after the intro)
   - an aside / caveat / source-note → `:::sidenote`
   - a named expert's opinion → `:::expert`
   - a deeper subtopic with its own article (mid-article) → `:::further-reading`
   - a memorable line → `:::pullquote`
   - a reader → product push (once high, once low) → `:::cta`
   - a pro shortcut → `:::tip` (easily-missed caveat → `:::note`)

   **High-value additions — plan these by content type + persona, only where they earn their place:**
   - **first mention of the article's core term** → `:::definition term="…"`
   - **a pitfall / must-know** → `:::warning` (hazard / data-loss / money-loss) or `:::important` (must-not-miss prerequisite that isn't a hazard)
   - **a comparison / technical "which should I use" section** → `:::proscons` (one option, `## Pros`/`## Cons`), `:::feature-matrix` (features × products, `yes`/`no`/`partial`), `:::decision-table` (classification grid) + the `:::preferred-order` ranked list that follows it; a one-line call → `:::verdict`
   - **a cited statistics roundup (5+ sourced figures)** → `:::stat-list` (1–4 hero numbers stay `:::stat`/`:::stat-group` — do not plan `:::stat-list` for fewer than 5)
   - **an FAQ section** → `:::faq` (adds FAQPage schema; plain H2/H3 FAQs are fine when schema isn't the goal)
   - **roundup / listicle scaffolding** → `:::jumplinks` (a "skip to the app" anchor menu) + one `:::entry n= name= url= best_for= price=` header per item; a qualitative award → `:::badge kind="…"`
   - **a captioned data figure / diagram** → `:::figure src= source=` / `:::diagram src=` — but **visuals are DEFERRED**: keep planning visuals as the typed `Visual N:` micro-specs (step 6); only plan a `:::figure`/`:::diagram` fence when a real `src` will exist at draft time, else the `[VISUAL:...]` placeholder carries it
   - **situational embeds** → `:::tweet url=` (degrade to `:::pullquote` if no live embed) · `:::video src= title=` (rare)

   Note the **inline treatments** the draft will apply (no fence, governed by voice — you don't plan them per-section, but keep them in mind when shaping a section): inline `` `code` `` for formulas/literal values, `{lead}…{/lead}` on the opening paragraph, `==mark==` for the rare highlight, plain-link citations (no superscripts), and a "Final thoughts"/"Bottom line" closer.

   **Per-persona favorites** to bias the plan toward (the draft picks the persona; plan for the likely one): **Sloane Avery** → `:::methodology` / `:::stat` / `:::stat-list` / `:::table` / `:::key-takeaways`; **Theo Hart** → tables / numbered steps / `:::decision-table` / `:::preferred-order` / `:::feature-matrix` / `:::cta` / `:::further-reading`; **Mateo Reyes** → `:::expert` / `:::pullquote` / `:::tweet` / `:::nutshell` / `:::sidenote` / `:::figure`.
7. **Comparison table (when the beat spec requires one).** Spec it as a real markdown table skeleton in the outline: columns (from the beat spec's required-columns list), one row per item, plus a `Visual: {type: table}` entry on the section. The draft authors the table in GFM markdown; `/format-for-publish` converts it for the site renderer. Do NOT pre-degrade tables into bullet lists at outline or draft time.
8. **Plan the intro.** Hook + thesis + preview. 150–200 words. The hook earns attention with something specific, surprising, or contrarian — never "In today's digital age".
9. **Plan the conclusion.** Restated thesis + one next step (often a `2-reference/` link). 80–150 words.
10. **Run the visual sanity check (two-way)** — for every H2 with a visual, confirm it earns its place (concrete info lost without it, supports the BLUF, MECE across sections); for every `none` section, check whether a labeled diagram/screenshot/chart/table would make it twice as good. Density target per `editorial-principles-visuals.md` (5/8/10/12 for <1.2k / 1.2–2k / 2–3k / >3k words), ≥3 distinct types.
11. **Run the structural self-check** in `references/bluf-mece-rules.md`.
12. **Run the beat-spec self-check (NEW, blocking):**
   - [ ] Section word targets sum to target word count ±10%
   - [ ] Item count ≥ beat spec item target (if list-shaped)
   - [ ] Every consensus topic appears in the coverage map
   - [ ] `[GAIN]` section exists and is genuinely not on page 1
   - [ ] Comparison table specced iff required
   If any box fails, fix the outline before saving — do not hand the debt to `/draft`.
13. **Save** to `content-pipeline/3-outlines/{slug}.md` using `templates/outline-template.md` structure (beat-spec restatement at top, coverage map at bottom).

## Output

`content-pipeline/3-outlines/{slug}.md` — typically 600–1,200 words. Detailed enough that `/draft` can expand without re-doing research.

## Quality checklist

- [ ] Title direct, includes primary keyword, <60 chars
- [ ] One-sentence thesis
- [ ] H2 list MECE, supports thesis, **sized by beat spec (no arbitrary 4–7 cap)**
- [ ] Each H2: BLUF, key points, evidence source, word target, transition, typed Visuals
- [ ] Components planned per section (`**Components:**` line) where one earns its place, drawn from the full authored set as the content type calls for it (definition/warning/important/proscons/feature-matrix/decision-table/preferred-order/verdict/stat-list/faq/jumplinks/entry/badge/figure/diagram/tweet/video) — restraint applied (1–2 of each max, most sections zero), fence names exact per `examples/ahrefs-components.md`; a `:::nutshell` planned under the H1 and `:::key-takeaways` for the conclusion when the format warrants
- [ ] Word targets sum to beat-spec total ±10%
- [ ] Coverage map: every consensus topic → a section
- [ ] `[GAIN]` section present
- [ ] Table skeleton present iff beat spec requires
- [ ] Visual density within range, ≥3 distinct types
- [ ] Intro = hook + thesis + preview; conclusion = restated thesis + next step
- [ ] Zero forbidden phrases (brand-config)

## Common failure modes to avoid

- **Compression** — the SERP demands 9 items and you outline 4 "best picks". That's how we shipped a 1,100-word listicle into a 2,500-word SERP. Match or beat; never shrink.
- **Section overlap** — "Why X matters" and "Benefits of X" are the same section. Pick one.
- **Consensus amnesia** — research lists must-cover topics; outline silently drops two. The coverage map exists to make that impossible.
- **Skipping the BLUF** — throat-clearing openers lose skim-readers.
- **Hook that says nothing** — "In today's competitive landscape…" is not a hook.
