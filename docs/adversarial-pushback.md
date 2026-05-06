# Adversarial pushback — Phase 3 of PLEAA-392

PLEAA-418 (2026-05-06). Neo's brief:

> There's something I really like — pushback where the blog says something
> and a skill basically pushed back, and then he can make multiple drafts.
> It's like a thing kind of pushed back, and maybe if something is wrong, he
> can rethink it. I like that.

Phase 1 was the hard-fail gates between every stage (PLEAA-392). Phase 2 is
visuals broadening (PLEAA-417, in flight). Phase 3 — this doc — extends the
existing adversarial+revision loop (which today only covers prose quality)
to **research**, **outline**, and **visual placement** so structural and
upstream-content problems get caught before they propagate.

## What ships

Three new skills, each with the same shape:

- `.claude/skills/research-adversarial/SKILL.md` — runs after stage 1
  (`/research`) and before stage 3 (`/outline`). Pushes back on citations,
  surprising findings, missed competitor angles, JSON↔prose data
  consistency, and brand fit.
- `.claude/skills/outline-adversarial/SKILL.md` — runs after stage 3 and
  before stage 4 (`/product-mentions`). Pushes back on MECE coverage, BLUF
  on every opener, problem-agitate-solution arc, differentiation vs SERP
  top-5, and whether visuals earn their place.
- `.claude/skills/visuals-adversarial/SKILL.md` — runs after stage 9
  (`/generate-visuals`, plus stage 11 `/capture-visuals` when reachable)
  and before stage 10 (`/preview`). Strips decorative auto-captures and
  flags missing visuals that would carry information.

Each skill writes a verdict file under
`content-pipeline/quality-checks/{slug}-<stage>-adversarial.md` with a
`## Verdict: **PASS**` or `## Verdict: **FAIL**` line that
`scripts/pipeline_gate.py` parses.

## Per-stage revision budgets

The orchestrator owns dispatch; bookkeeping lives in
`.runs/{slug}-budgets.json`. Use `scripts/adversarial_runlog.py` to read or
write it:

```bash
python scripts/adversarial_runlog.py status <slug>
python scripts/adversarial_runlog.py used <slug> <stage>
python scripts/adversarial_runlog.py budget <stage>
python scripts/adversarial_runlog.py increment <slug> <stage>
python scripts/adversarial_runlog.py can-revise <slug> <stage>
   # exit 0 if a revision pass is still within budget, 1 if exhausted
```

Stage keys: `outline`, `research`, `visuals`, `quality`.

Default budgets (each is the *number of revision passes*, not counting the
original generation):

| Stage     | Env var                                   | Default |
| --------- | ----------------------------------------- | ------- |
| research  | `BLOG_AGENT_RESEARCH_REVISION_BUDGET`     | `1`     |
| outline   | `BLOG_AGENT_OUTLINE_REVISION_BUDGET`      | `1`     |
| visuals   | `BLOG_AGENT_VISUALS_REVISION_BUDGET`      | `1`     |
| quality   | `BLOG_AGENT_REVISION_BUDGET` (existing)   | `2`     |

Override per-run:

```bash
BLOG_AGENT_OUTLINE_REVISION_BUDGET=2 ./scripts/run_pipeline.sh "/blog-pipeline keyword cannibalization"
```

## How `pipeline_gate.py` reads the verdicts

```bash
python scripts/pipeline_gate.py research-adversarial <slug>
python scripts/pipeline_gate.py outline-adversarial  <slug>
python scripts/pipeline_gate.py visuals-adversarial  <slug>
```

The gate fails when:

1. The verdict file is missing.
2. The verdict file has no parseable `## Verdict: **PASS|FAIL**` line.
3. The verdict is `FAIL` AND the per-stage revision budget is exhausted.

A `FAIL` with budget remaining is **not** a gate fail — the orchestrator is
expected to re-dispatch the producing stage with the CRITICAL findings as a
revision brief, then re-run the adversarial skill. The gate only halts the
pipeline once the budget is gone.

## Orchestrator flow

```
research          ──┐
                    ├── parallel
brand-reference   ──┘
research-adversarial ──┐  (FAIL → re-/research up to budget; otherwise advance)
                       ▼
outline                ──▶ outline-adversarial (FAIL → re-/outline up to budget)
                       ▼
product-mentions ──▶ draft ──▶ quality-check (existing prose loop)
                                          ▼
verify-claims ──▶ optimize-content ──▶ generate-visuals ──▶ capture-visuals
                                                                ▼
                                            visuals-adversarial (FAIL → strip + add → re-/generate-visuals)
                                                                ▼
                                            preview ──▶ format-for-publish ──▶ publish
```

## Acceptance criteria (PLEAA-418)

- A run with a deliberately-thin outline (e.g. only 3 H2s on a topic that
  needs 6) is caught by the outline adversarial and revised before drafting
  starts. → enforced by `outline-adversarial` skill brief + gate
  `outline-adversarial`.
- The orchestrator never advances past a stage with an unresolved CRITICAL
  adversarial finding. → enforced by `pipeline_gate.py
  <stage>-adversarial` returning non-zero when the verdict is FAIL and
  budget is exhausted.
- Revision budgets are observable in the run log: `outline: 1/2 revisions
  used`. → reported in the orchestrator's final report (see
  `.claude/skills/blog-pipeline/SKILL.md`) using
  `python scripts/adversarial_runlog.py status {slug}`.

## Dependency on PLEAA-417

`visuals-adversarial` ships with full plumbing (skill, gate, orchestrator
dispatch) but its full value depends on PLEAA-417 (visuals broadening):
without it, most external visuals fall to manual capture so the adversarial
mostly strips decorative pleasur.ai screenshots and flags pure-fluff
placeholders. Once PLEAA-417 lands, the skill's "is this external
screenshot the right crop" question becomes meaningful.
