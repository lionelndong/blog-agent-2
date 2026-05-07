---
name: outline
description: Create a structured H2/H3 outline with BLUF openers and MECE coverage from research and brand-reference dossiers. Triggered after /research and /brand-reference.
allowed-tools: Read, Write
---

# Outline Skill

Turn the research dossier into the article's bones. The output is a detailed outline a writer (human or AI) can expand into prose without further research.

## Input

For slug `{slug}`, reads:
- `content-pipeline/1-research/{slug}.md` (required — the research dossier)
- `content-pipeline/2-reference/{slug}.md` (recommended — brand context)
- `content-pipeline/0-context/{slug}.md` (if exists — user-provided angle)
- `brand-config.md` (audience, voice)
- `references/bluf-mece-rules.md` (structural rules — must enforce)
- `../../../templates/outline-template.md` (the file structure)
- `../../../templates/visual-types.md` (controlled vocabulary for the `Visual:` field — required)
- `../../../templates/editorial-principles-visuals.md` (Ryan's principles applied to visual decisions — **required** before assigning any non-`none` Visual)
- 2 articles from `examples/` whose topic is closest (for structural reference)

## Process

1. **Read all inputs.** Especially the research dossier's "Recommended angle" and "Content gaps" sections.
2. **Choose the article title.** Direct, includes the primary keyword early. Aim for under 60 characters when possible.
3. **Write the thesis.** One sentence. The article's central argument.
4. **Decide content type.** Definitive guide / how-to / explainer / listicle / comparison — based on dominant SERP intent (from research) and the angle.
5. **Draft the H2 list.** 4–7 sections. Read your H2 list aloud as a single sequence — does it argue for the thesis? Does it map the topic? Apply MECE strictly.
6. **For each H2, write:**
   - BLUF (one sentence; the section's opening line or close to it)
   - Key points (2–4 bullets)
   - Evidence (stat / quote / example / walkthrough — preferably from `1-research/` or `2-reference/`)
   - Transition to next section
   - **Visuals** — one or more typed micro-specs. Each visual is one of: `screenshot`, `action-shot`, `image`, `table`, `chart`, `video`, `external`, `gif`, `none`. Format:
     ```
     **Visuals:**
       Visual 1: {type: image, sub: concept-illustration, prompt: <specific structured prompt>, safety: sfw}
       Visual 2: {type: screenshot, target: create, what: voice profile selector, annotate: arrow on speaker icon}
     ```
     For single-visual sections, the legacy `**Visual:** {type: ..., ...}` form is still accepted.

     **How to decide** — apply the 10-step decision sequence in `templates/editorial-principles-visuals.md` (the principles file). The rule maps to types defined in `templates/visual-types.md`. A visual must *earn its place* — but the editorial bar shifted: the new default for any non-trivial section (>300 words) is "this section deserves a visual; what kind?", not "this section gets no visual unless I can justify one." Most sections in a well-researched article have something concrete to show: a diagram of the concept (`image` sub=concept-illustration), a screenshot of the brand UI doing the thing, a chart of the data being cited, a Reddit/tweet/news source being quoted (`external`).

     **The screenshot vs action-shot choice** — when you decide a section needs a brand-product UI capture, ask: "could a developer paste a single URL into a fresh browser and see this state immediately?" If yes → `screenshot` (patchright headless, free, fast). If no — the state requires clicks/typing/wait/login — → `action-shot` (routed to `/capture-visuals`, which drives the VPS's always-on Chrome via the Claude in Chrome MCP; also free, just slower because it's a real browser performing real actions). Examples that clearly map: a static templates grid → `screenshot`; the wizard mid-flow at step 3 → `action-shot`; a chat with a response visible → `action-shot`; a static feature page → `screenshot`. When in doubt, prefer `screenshot` first; the dispatcher will surface failures cleanly and you can upgrade to `action-shot` then.

     **External evidence (PLEAA-417)** — when a section quotes a specific Reddit comment we cite, embeds a tweet, or shows a chart inside a news article / competitor UI, use `external` with a `selector` that clips to that element. The pipeline auto-captures these now (it used to route them to manual). Sub-types: `reddit-comment`, `tweet`, `news-quote`, `competitor-ui`, `chart`. See `templates/visual-types.md` for selector patterns. If the source is login-gated or behind aggressive bot protection, the pipeline transparently falls back to `/capture-visuals` (real Chrome session) rather than failing.
   - Word target
7. **Plan the intro.** Hook + thesis + preview. 150–200 words.
8. **Plan the conclusion.** Restated thesis + one next step (often link to a `2-reference/` article). 80–150 words.
9. **Run the visual sanity check (two-way).** For every H2:
   - **If it has at least one non-`none` Visual** — apply the "Test for an existing `Visual:` assignment" checklist in `templates/editorial-principles-visuals.md`:
     - Does the visual *earn its place* (concrete info the reader would lose without it)?
     - Does it *support* the BLUF, not replace it?
     - Is it *concrete* (real UI / real data / real source / a labeled diagram with accurate components) — not a stylized abstraction?
     - Is it *MECE* across sections (no other section uses the same visual)?
     If any answer is no, change to `none` *or swap the type*.
   - **If the section currently has `none`** — apply the inverse test:
     - Could a labeled `image` (sub=concept-illustration) make this section twice as good?
     - Is there a screenshot, chart, table, external source the prose is currently describing in words?
     If yes, upgrade from `none` to the matching type.
   - **Density check** — count total non-`none` visuals across the outline. Compare against the target table in `editorial-principles-visuals.md` (5/8/10/12 for <1.2k / 1.2–2k / 2–3k / >3k word articles). Aim for at least 3 distinct types across the article (e.g. image + screenshot + chart, or image + external + video).
10. **Run the structural self-check** in `references/bluf-mece-rules.md` before saving.
11. **Save** to `content-pipeline/3-outlines/{slug}.md` using `templates/outline-template.md` structure.

## Output

`content-pipeline/3-outlines/{slug}.md`

500–900 words depending on article complexity. Detailed enough that the `draft` skill can expand without re-doing research.

## Quality checklist

- [ ] Title is direct, includes primary keyword, under 60 chars
- [ ] One-sentence thesis
- [ ] 4–7 H2s, MECE, all support thesis
- [ ] Each H2 has BLUF, key points, evidence, transition, **one or more typed Visuals** (each: screenshot/action-shot/image/table/chart/video/external/gif/none), word target
- [ ] Total non-`none` visual count is within the acceptable range floor (≥4 for <1.2k words, ≥6 for 1.2–2k, ≥8 for 2–3k, ≥10 for >3k — i.e. target − 1) and ideally hits the target (5/8/10/12) — see `templates/editorial-principles-visuals.md`
- [ ] At least 3 distinct visual types across the article (e.g. `image` + `screenshot` + `chart`)
- [ ] Intro plan = hook + thesis + preview
- [ ] Conclusion plan = restated thesis + next step
- [ ] All forbidden phrases (from `brand-config.md`) absent
- [ ] H2 list, read alone, maps the topic with no obvious gaps

## Common failure modes to avoid

- **Section overlap** — "Why X matters" and "Benefits of X" cover the same ground. Pick one.
- **List masquerading as argument** — when every H2 starts with a number ("5 Tips for…"), check whether the article is making a point or just listing.
- **Skipping the BLUF** — a section that opens with throat-clearing ("Now that we've covered the basics…") loses skim-readers.
- **Hook that says nothing** — "In today's competitive landscape…" is not a hook. A hook earns attention with a specific, surprising, or contrarian first line.
