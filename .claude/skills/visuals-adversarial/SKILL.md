---
name: visuals-adversarial
description: Skeptical pushback on visual placement. Reads the annotated outline plus the visuals manifest and asks whether each [VISUAL:...] earns its place per editorial-principles-visuals.md, whether visuals are decorative, and whether sections without one would benefit. One revision pass on FAIL (BLOG_AGENT_VISUALS_REVISION_BUDGET, default 1).
allowed-tools: Read, Write, Bash, Task
---

# Visuals Adversarial Skill

Phase 3 of PLEAA-392 (PLEAA-418, 2026-05-06). Decorative visuals are AI-content's
#1 failure mode (per `templates/editorial-principles-visuals.md`); this skill
strips them out and flags missing visuals that would carry information.

The orchestrator dispatches this skill **after** stage 9 (`/generate-visuals`)
writes the manifest and **before** stage 10 (`/preview`). Stage 11
(`/capture-visuals`) may run between — if so, the adversarial reads the
post-capture manifest. On `FAIL` with budget remaining, the orchestrator
re-dispatches `/generate-visuals` with the critique (specifically: which
visuals to strip and which to add) and re-runs this skill.

## Dependency on PLEAA-417

This skill is most useful **after** PLEAA-417 (visuals broadening) lands. Until
then, most external visuals fall to manual capture, so the adversarial mostly
flags decorative auto-captured screenshots — still useful, but the full value
shows up once Reddit / news / competitor-UI captures are real assets the
adversarial can judge on its own merits.

In degraded mode (PLEAA-417 not landed yet), the adversarial should still:

- Strip decorative auto-captures of pleasur.ai pages.
- Flag manual-capture entries that the editorial rule says don't earn a visual
  at all (so they drop, not move from `manual` to `none`).
- Skip the "is this external screenshot the right crop" question — the assets
  don't exist yet.

## Input

For slug `{slug}`:

- `content-pipeline/4-outlines-annotated/{slug}.md` (the annotated outline —
  source of truth for which sections asked for which visuals)
- `content-pipeline/6-drafts-cited/{slug}.md` (the cited draft, post-visuals
  rewrite — to see where visuals actually landed)
- `content-pipeline/images/{slug}/manifest.json` (status of each visual)
- `content-pipeline/images/{slug}/manual-capture.md` (if present — entries
  routed to manual)
- `templates/editorial-principles-visuals.md` (THE rule)
- `templates/visual-types.md`

## Process

1. Spawn a `Task` sub-agent with the brief below.
2. Combine into `content-pipeline/quality-checks/{slug}-visuals-adversarial.md`.
3. Print the verdict + CRITICAL count.

## Adversarial sub-agent brief

> You are a skeptical art director reviewing the visual placement for
> `{slug}`. The principle is in `templates/editorial-principles-visuals.md`:
> default Visual is `none`. A visual must carry information the prose can't,
> not decorate the section.
>
> Read in order:
> 1. `templates/editorial-principles-visuals.md`
> 2. `templates/visual-types.md`
> 3. `content-pipeline/4-outlines-annotated/{slug}.md`
> 4. `content-pipeline/6-drafts-cited/{slug}.md`
> 5. `content-pipeline/images/{slug}/manifest.json`
> 6. `content-pipeline/images/{slug}/manual-capture.md` (if it exists)
>
> Push back on five questions:
>
> 1. **Decorative visuals.** For each visual that landed in the cited draft,
>    apply the 9-step rule. Which ones are decorative (the prose already
>    explains it; the visual just adds a screenshot for vibes)? List them.
>    These should be stripped.
> 2. **Missing visuals.** Are there sections WITHOUT a visual where one
>    would carry real information — a comparison table the prose
>    forces into bullets, a workflow that needs sequence, a stat that
>    deserves a chart? Name the H2 and the missing-visual type.
> 3. **Wrong type.** Is any visual the wrong type for what the section
>    needs? (Screenshot where a chart would carry the data; chart where a
>    side-by-side comparison would beat it.)
> 4. **Crop / framing.** For visuals that landed as real assets, does the
>    crop highlight the moment that adds value, or is it a full-page
>    screenshot with the relevant detail buried? Be specific by file path.
> 5. **Manual fallthrough.** Any entries in `manual-capture.md` that, by
>    the 9-step rule, shouldn't have been requested at all? These should
>    be dropped from the outline rather than chased.
>
> Output:
>
> - 4–8 findings tagged `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.
>   - `CRITICAL` = the article ships with a visual that hurts (decorative
>     stock-screenshot in a serious section, or a chart whose data
>     contradicts the prose, or missing comparison-table where the prose
>     is forcing 6 platforms into paragraph form).
>   - `HIGH` = visual quality is below brand bar but won't kill credibility.
> - 1 visual that genuinely earns its place.
> - A one-line **Verdict: PASS** or **Verdict: FAIL**.
>
> Do NOT capture replacement visuals or rewrite the draft. Under 600 words.

## Output

`content-pipeline/quality-checks/{slug}-visuals-adversarial.md`. Same skeleton
as the other adversarial skills. `## Verdict:` line must be exact.

## How the orchestrator handles FAIL

Same loop as the other adversarial skills with stage key `visuals`:

1. `python scripts/adversarial_runlog.py can-revise {slug} visuals`
2. If budget remains: increment, dispatch a revision pass.
   - The revision is **two operations** rather than re-running stage 9 wholesale:
     - **Strip:** for each `CRITICAL` decorative finding, edit
       `content-pipeline/6-drafts-cited/{slug}.md` to remove the
       `![alt](images/{slug}/...)` line and merge the surrounding paragraphs.
       Mark the corresponding manifest entry `status=stripped` with the
       adversarial finding ID as the reason.
     - **Add:** for each `CRITICAL` missing-visual finding, append a new
       typed `[VISUAL:...]` placeholder to the cited draft at the named H2
       and re-run `/generate-visuals` for just that placeholder.
3. If exhausted: write `9-needs-review/{slug}.md` and HALT.

## Why this skill exists

A draft that ships with 8 decorative screenshots reads like AI slop even when
the prose is strong. The 9-step rule is in our editorial principles but
nobody enforces it after the visuals land — the orchestrator advances if the
manifest shows everything captured, even if half the captures are wallpaper.
This skill enforces the rule.
