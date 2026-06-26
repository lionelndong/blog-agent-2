---
name: quality-check
description: The publish gate. Runs binary completeness floors, then a skeptical 3-reviewer panel that decides whether the article beats the live #1 result. Emits PASS/FAIL — there is no score to game. PASS is required to publish; FAIL routes a revision or quarantines.
allowed-tools: Read, Write, Bash, Task
---

# Quality Check — the publish gate

The question is never "does the draft comply with our rules." It is: **a reader opens this
article and the current #1 result side by side — which one do they keep?** A perfectly
"compliant" draft that loses that comparison is a FAIL.

This gate has no 0–100 score, on purpose. A score invites gaming — a model will add numbers,
links, and headers to clear "85" without making the article better (that is exactly how thin
drafts used to pass at 85 while the adversarial read named five real weaknesses). Instead the
gate is two un-gameable halves, and **both must pass**:

1. **FLOORS** — objective completeness you can only satisfy by doing the work.
2. **PANEL** — three skeptical reviewers who decide whether this beats what's ranking.

## Input

For slug `{slug}`:
- `content-pipeline/5-drafts/{slug}.md` (the draft; use `6-drafts-cited/{slug}.md` with `--stage cited`)
- `content-pipeline/1-research/{slug}.md` (**the BEAT SPEC + SERP benchmark — required**)
- `content-pipeline/3-outlines/{slug}.md` (coverage map)
- `brand-config.md` (forbidden phrases, audience, products)
- `examples/voice/*.md` (the voice the draft must match)

## Gate 1 — Floors (binary, mechanical)

```bash
python .claude/skills/quality-check/scripts/quality_check.py "{slug}"   # add --stage cited after /verify-claims
```

Writes `quality-checks/{slug}-metrics.md`; exits 0 (FLOORS_OK) or 1 (FLOORS_FAIL). Floors:
SERP benchmark present · depth ≥ 80% of SERP median · item count met · comparison table when
the SERP has one · **every** consensus topic covered · citations resolved (cited stage) · **no
internal tooling in the prose** (Semrush/Ahrefs/Strapi/etc.) · no forbidden phrases.

**Any failed floor → the gate FAILs.** Don't run the panel on a draft that fails a floor —
route the fix first: a missing topic or thin depth goes back to `/outline` or `/research`,
prose problems to `/draft`.

## Gate 2 — Reviewer panel (the real signal)

Spawn **three independent `Task` sub-agents**, each a skeptical industry expert who has read
every page-1 result for "{keyword}". Give each the dossier (`1-research/{slug}.md` — note the
BEAT SPEC + top-page summaries), the draft, and 1–2 `examples/voice/` articles. Brand: {brand};
audience: {audience}. Each gets ONE lens:

- **Lens A — Competitiveness:** depth, specificity, usefulness vs the winners.
- **Lens B — Voice & readability:** does it read like the `examples/voice/` anchors (reader-felt,
  concrete, leads with the real decision) or like generic AI? Would a serious blog run it under
  a byline?
- **Lens C — Reader intent & information gain:** does it satisfy the searcher better than the
  SERP, and carry ≥ 1 genuine thing the top 10 don't have?

Each sub-agent answers in this exact shape:
> **VERDICT: KEEP_OURS | KEEP_COMPETITOR | TOSS_UP** — default to KEEP_COMPETITOR / TOSS_UP if
> unsure (be skeptical, not polite). Then: 3 sentences on why; the 5 weakest things vs what's
> ranking (specific sentences/sections); 1 thing that genuinely works.

Save all three to `quality-checks/{slug}-panel.md`. Distrust any all-praise verdict shorter
than 200 words — re-run that lens with a sharper brief.

**Gate 2 passes iff ≥ 2 of 3 say KEEP_OURS AND none says KEEP_COMPETITOR.** A single TOSS_UP is
tolerable; any KEEP_COMPETITOR fails the gate.

## Verdict

Write `content-pipeline/quality-checks/{slug}.md` with the verdict line FIRST:

- `## Verdict: **PASS**` — iff FLOORS_OK **and** Gate 2 passes.
- `## Verdict: **FAIL**` — otherwise.

Then: the floor-table summary, the three panel verdicts, and a **punch list** — specific fixes
ordered by severity, each pointing at a section, each tagged with a **route**: `/draft` for
voice/prose, `/outline` or `/research` for depth/coverage gaps (never ask `/draft` to fix a
structural deficit).

## On FAIL

- **Autonomous mode (`BLOG_AGENT_AUTONOMOUS=1`):** don't stop — emit the verdict + routed punch
  list and return cleanly. The orchestrator owns the retry budget (`BLOG_AGENT_REVISION_BUDGET`,
  now **2**). When the budget is spent, the orchestrator writes `9-needs-review/{slug}.md` and
  moves to the next keyword — **never lower the bar or publish a FAIL.**
- **Interactive mode:** stop and report what failed and where to re-enter the pipeline.

## Why this gate exists

Ryan Law's quality guarantee is a human reading every article before it ships. We auto-publish,
so the panel is that human's stand-in: three skeptics who must agree the piece wins the
side-by-side. The floors guarantee they're judging a complete article, not a stub. Neither half
emits a number — so there is nothing to optimize toward except actually being better than what's
ranking.
