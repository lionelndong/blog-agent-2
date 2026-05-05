# Pipeline fixes plan

After the end-to-end test on the keyword "AI porn" (slug `ai-porn`), several real failure modes surfaced. This plan catalogs them, prioritizes by impact, and lists the concrete fix for each. Every fix is checked against Ryan's editorial principles — if a fix would weaken BLUF, MECE, P-A-S, inverted-pyramid, show-with-examples, product-led, cite-everything, or visuals-earn-their-place, we don't ship it.

The user is away while these land. Execution is autonomous within these guardrails:
- No git pushes / Strapi publishes / destructive shell ops
- No structural rewrites of the editorial principles
- No new agent-y abstractions; fixes target the existing skill files and scripts
- Every fix is verified before being marked done

## Issues observed in the test run

1. **Orchestrator broke immediately** — `/blog-pipeline` invoked via `Skill` tool returned `Prompt is too long`. Root cause: the orchestrator was designed to invoke each child skill via slash command, which forks with parent context. After the long compaction summary plus a few stages, the fork has nowhere to land. **Severity: P0** — main entry point is unusable.

2. **Chart auto-render failed silently** — the draft emitted `[VISUAL:type=chart;data=research.cluster_volumes;...]` but `render_chart.py` accepts only inline JSON or `path:KEY` syntax. The dispatcher returned `invalid_data_spec` and dumped the chart to `manual-capture.md`. Required hand-extraction of numbers from the research dossier and a manual `render_chart.py` invocation. **Severity: P0** — visuals don't ship without human intervention.

3. **Quality-gate caught a real constraint violation late** — the annotated outline contained both a "Step 4 — what's coming this week" bullet (line 89) and a contradictory "coming-soon products only in H2 #6" rule (line 172). The draft followed line 89; the gate caught it; surgical fix took a whole extra agent dispatch. The outline self-contradiction should have been caught at `/product-mentions`, not after drafting. **Severity: P1** — adds an iteration loop the editor has to babysit.

4. **Voice metrics drifted hard on first pass** — paragraph length 2.2× baseline, em-dashes 2.5×, second-person 0.22×. The draft rules already include a "self-edit pass" but it's clearly not biting. **Severity: P1** — voice quality is the single biggest editorial risk.

5. **Action-shot couldn't be captured cross-machine** — the same-machine `save_to_disk` constraint we documented in `vps-deploy.md` forced the action-shot to stay in `manual-capture.md`. On a real VPS deployment this works; in a developer-laptop test it doesn't. The orchestrator should know this and surface the right path. **Severity: P1** — the article shipped with one of three planned visuals.

6. **OpenRouter deep research returned empty twice** — Perplexity refused to fabricate VOC and saw only Pleasur's own blog content. The script ran fine; the prompt is what failed. **Severity: P2** — the dossier is poorer without it but we compensate via direct WebSearch/WebFetch.

7. **`pipeline_status.py` checks stale paths** — looks for legacy `screenshot-urls.md` and `ai-porn.docx`, missing the new typed `manifest.json` and `8-publish/` folder. Reports 7/10 instead of 10/10 even on a clean run. **Severity: P2** — cosmetic but misleading.

## Fix priorities + execution order

P0 fixes ship first. Each carries a verification step.

### P0-1 — Orchestrator dispatches agents, not slash commands

**Problem.** `Skill` tool invocations fork with the parent's context, which is already huge after compaction. `Agent` calls get a fresh window.

**Fix.** Rewrite `.claude/skills/blog-pipeline/SKILL.md` so the process explicitly:
- Dispatches each stage as a `general-purpose` Agent with a tight self-contained prompt
- Runs stages 1+2 in parallel (research and brand-reference are independent)
- Verifies output file exists before advancing
- Surfaces stage failures cleanly rather than crashing the whole chain
- Re-dispatches on quality-gate FAIL with a punch list instead of stopping the chain entirely

The same pattern goes into `.claude/skills/update-pipeline/SKILL.md`.

**Ryan-principle check.** Doesn't touch editorial logic; it's purely orchestration plumbing. Pass.

**Verification.** Smoke-test with a fresh slug — orchestrator dispatches stage 1, stage 1 file appears on disk, stage 2 dispatches, etc. No `Prompt is too long`.

### P0-2 — Chart placeholders auto-resolve

**Problem.** The outline / draft emit `data=research.X` strings that `render_chart.py` can't decode. The format the script accepts (`path:KEY` or inline JSON) is never produced upstream.

**Fix.** Two-part:

A. **Add a `data` resolver in `generate_visuals.py`** that recognizes `research.<key>` and looks up the key in a new `content-pipeline/1-research/{slug}-data.json` file. The research stage emits this companion JSON alongside the markdown dossier when it has chartable numbers — keys like `cluster_volumes`, `serp_traffic`, `format_share`, etc.

B. **Update the `/research` skill** to, when it finds chartable numbers in the dossier, also emit them to `{slug}-data.json` in a documented schema. Update `templates/visual-types.md` so the chart placeholder examples use `data=research.<key>` (the lookup form) rather than ambiguous `research.X` strings.

If `{slug}-data.json` is missing or the key isn't there, the dispatcher falls back to **routing the chart to `manual-capture.md`** with the *current values* extracted from the research markdown shown in the entry — so an editor can render with one `python render_chart.py --data ...` invocation.

**Ryan-principle check.** Charts only render with sourced numbers — that's "cite everything." If we can't source, we don't fabricate. Pass.

**Verification.** Re-dispatch the chart for `ai-porn` after the fix lands; expect `chart-1-ai-porn.png` to regenerate without my hand-extraction.

### P0-3 — `pipeline_status.py` reflects the real layout

**Problem.** Checks `images/{slug}/screenshot-urls.md` (legacy) and `8-publish/{slug}.docx` (legacy `.docx` output). Real pipeline writes `images/{slug}/manifest.json` and `8-publish/{slug}/article.md`.

**Fix.** Update the path checklist. Add `quality-checks/{slug}.md` as a separate stage. Output reads `10/10` on a clean run.

**Ryan-principle check.** Tooling-only. Pass.

**Verification.** Run `python scripts/pipeline_status.py ai-porn` after fix; expect 10/10 (or 9/10 with the action-shot still pending).

### P1-4 — Constraint reconciliation in `/product-mentions`

**Problem.** Outline can contradict itself about coming-soon products. Draft picks one; gate catches the other late.

**Fix.** Add a **constraint reconciliation pass** at the top of `.claude/skills/product-mentions/SKILL.md`:
1. Scan the outline for every `coming-soon` product mention
2. Cross-check against `brand-config.md`'s product status table
3. If a mention sits outside the section the brand-config or the outline's own rules permit, **delete it from the outline before annotating**, and note the deletion at the top of the annotated file
4. The draft never sees the contradictory state

Also: lint the outline before product-mentions runs — surface any internal contradictions in a `## Pre-flight reconciliation` block.

**Ryan-principle check.** Strengthens product-led discipline (no half-shipped feature mentions in evergreen content). Pass.

**Verification.** Run `/product-mentions` against an outline that contains a known contradiction; expect the conflicting bullet to be deleted with a logged reason.

### P1-5 — Voice rules in `/draft` enforce structurally, not via self-edit

**Problem.** Self-edit pass is a step in the SKILL.md but it doesn't bite. We see 2.2× paragraph length, 2.5× em-dash density, 0.22× second-person on first attempts.

**Fix.** Three changes to `.claude/skills/draft/SKILL.md`:

A. **Move metrics targets to the top of the brief**, before the process. The draft model needs to see "paragraph 24–35 words, em-dashes 6–8/1k, second-person 25+/1k" as a hard input, not as a self-edit afterthought.

B. **Add a worked-example paragraph** in the prose-patterns reference showing what the right rhythm looks like — concrete BLUF + body sentences + transition with appropriate em-dash use. The model anchors better on examples than rules.

C. **Add a metrics pre-check before save** — if the draft's voice metrics (cheap regex count) drift more than 1.5× off baseline, the skill returns the draft as `borderline-on-save` and the orchestrator dispatches a single targeted-revision pass *automatically* before stage 6 (quality-check). This is the same surgical-fix pattern we ran by hand, baked in.

**Ryan-principle check.** Voice fidelity is the load-bearing quality lever. This strengthens it. Pass.

**Verification.** Run `/draft` on a fresh slug and check the metrics from `quality_check.py` on first save — paragraph length should land in 24–40 word range without intervention.

### P1-6 — Action-shot auto-flow on VPS deployment

**Problem.** `/capture-visuals` is editor-interactive by design. On the VPS deployment we want it to fire automatically when `manifest.json` has manual entries.

**Fix.** Two-part:

A. **Update the orchestrator** so when stage 8 (`/generate-visuals`) finishes with manual entries AND the env var `UNATTENDED=1` is set (the VPS systemd unit sets this), the orchestrator dispatches `/capture-visuals` as the next stage automatically. Without `UNATTENDED=1`, the orchestrator surfaces the path to `manual-capture.md` and exits as today (interactive editorial review).

B. **Update `.claude/skills/capture-visuals/SKILL.md`** so when invoked with `UNATTENDED=1` it runs without per-step "ask the user" confirmations — the safety check is the heuristic validation already in place plus the action-shot's `goal=` text being explicit.

**Ryan-principle check.** Doesn't change visual-earn-its-place rules; only changes when capture happens. Pass.

**Verification.** Set `UNATTENDED=1`, run a slug whose outline has an action-shot, confirm the orchestrator dispatches capture automatically and a PNG lands.

### P2-7 — Fix OpenRouter deep-research prompt

**Problem.** Perplexity refused to "fabricate VOC" and only saw Pleasur's own blog. The prompt asked for things Perplexity won't return.

**Fix.** Read `openrouter_research.py`, look at the prompt template, rewrite it to:
- Ask for *cited* findings only (not synthesis)
- Specify forum sources we want (Reddit, HN, niche subreddits) by URL pattern
- Frame as "search and cite" rather than "research and synthesize"
- Explicitly tell the model to leave a section empty rather than refusing the whole task if a sub-prompt is uncomfortable

If results stay weak, fall through to `openai/o4-mini` more aggressively (lower error tolerance for retries on Perplexity).

**Ryan-principle check.** Cite-everything. Better citations = better dossier. Pass.

**Verification.** Run `openrouter_research.py` with the new prompt against a known keyword; expect at least 3 verbatim quotes with source URLs in the output.

## Verification at the end

Once all P0/P1 fixes land, run a smoke test on a *new* slug to confirm:
1. `/blog-pipeline <new-keyword>` dispatches all stages cleanly without the `Prompt is too long` failure
2. The chart at H2 #N renders automatically (no hand-extraction)
3. Quality-check first pass clears 75 (no surgical-fix loop needed)
4. The action-shot auto-captures if `UNATTENDED=1` (or stays in `manual-capture.md` if not)
5. `pipeline_status.py` reports 10/10

If verification finds residual issues, we extend the plan rather than declaring victory prematurely.

## Out of scope

These came up in the test but are intentionally **not** in this plan:
- Replacing the `examples/` corpus — the user explicitly chose Ahrefs articles for voice anchoring (per `CLAUDE.md`); voice baseline is correct as-is
- Adding more visuals per article — the editorial doctrine is "default `none`, earn it." Three visuals for a 2,800-word article is correct, not under-scoped
- Auto-publishing to Strapi — the human checkpoint between `format-for-publish` and `Publish` is intentional; no fix needed
- A "pretty" web dashboard for pipeline runs — `whiteboard.py` already exists; no rebuild

## Plan execution log

All items landed. See [pipeline-fixes-report.md](./pipeline-fixes-report.md) for the detailed change-by-change report.

- [x] P0-1 orchestrator dispatch
- [x] P0-2 chart auto-resolve
- [x] P0-3 pipeline_status
- [x] P1-4 constraint reconciliation
- [x] P1-5 voice rules
- [x] P1-6 unattended capture-visuals
- [x] P2-7 deep-research prompt
- [x] Verification smoke battery (11/11)
- [x] Self-test report
