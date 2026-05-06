---
name: blog-pipeline
description: Master orchestrator for the content creation pipeline. Dispatches each stage as a fresh subagent so the parent context never overflows. Runs research through preview for a target keyword and surfaces stage failures cleanly. Editor reviews between preview and publish.
allowed-tools: Read, Write, Bash, Agent, Glob
---

# Blog Pipeline (Master Orchestrator)

Take a keyword and produce a publish-ready article. The orchestrator does NOT inline-fork via the Skill tool — that fails with `Prompt is too long` once the parent context has any history. Instead each stage is dispatched as a fresh `general-purpose` Agent with a self-contained brief.

## HARD-FAIL GATES — non-negotiable

Neo, PLEAA-392 (2026-05-06): "we cannot skip steps. If something is missing, stop and address it before moving on. Quality is the #1 priority."

Between every stage transition, the orchestrator MUST run:

```bash
python scripts/pipeline_gate.py <stage-key> <slug>
```

Stage keys: `research`, `reference`, `outline`, `annotated`, `draft`, `cited`, `quality`, `visuals`, `preview`, `publish`, `deliverable`. The script's exit code is authoritative — non-zero means HALT, do NOT advance to the next stage. Print the stderr summary to the user.

Specific halt conditions the gate enforces:

- **`visuals`** — every `[VISUAL:...]` placeholder must produce a real asset on disk. Any `manual` or `failed` entry in `manifest.json`, or any naked `[VISUAL:...]` left in the cited draft, is a HALT. Resolution: run `/capture-visuals`, or fix the SKILL/script to actually handle the type, then re-run `/generate-visuals`. Do NOT advance to preview/publish with unresolved visuals — Neo will reject the run.
- **`quality`** — verdict FAIL or BORDERLINE-with-CRITICAL is a HALT. The autonomous-mode revision loop addresses this; if the loop's budget is exhausted and the verdict is still failing, write `9-needs-review/{slug}.md` and STOP — never publish broken prose.
- **`publish`** — `8-publish/{slug}/{article.md, article.json, README.md}` must all exist AND `article.md` must contain zero raw `[VISUAL:...]` placeholders. The format-for-publish skill must strip or substitute these — never ship template syntax.
- **`deliverable`** — for issue-driven runs (PAPERCLIP_TASK_ID set), a deliverable comment with the slug + verdict must be posted to the trigger issue before the run is considered complete. Run-status "succeeded" means nothing if Neo can't see the result.

**Never claim a stage succeeded just because the agent dispatched cleanly.** The gate is the source of truth.

## Invocation

```
/blog-pipeline <keyword> [--context "free-form direction"]
```

Examples:
- `/blog-pipeline keyword cannibalization`
- `/blog-pipeline link building --context "Lean toward beginners. Mention ProductA's link tool early."`
- `/blog-pipeline content gap analysis --context "Audience is technical SEO managers. Use a worked example throughout."`

## Why agent dispatch, not slash-command fork

The `Skill` tool forks with the parent's context. After any compaction or accumulated history, that fork hits `Prompt is too long`. The `Agent` tool starts each stage with a clean window, so the orchestrator can run for as long as the chain needs without context pressure. This is non-negotiable — every stage MUST be an Agent dispatch, not a Skill invocation.

## Autonomous mode (BLOG_AGENT_AUTONOMOUS=1)

When the env var `BLOG_AGENT_AUTONOMOUS=1` is set (the auto-blog-loop sets it; cron-driven runs inherit it from Doppler), the orchestrator's behavior changes:

- **Skip-or-regenerate**: never asks. If a stage's output file exists, skip it (resume-from-failure). If `--regenerate` was passed, overwrite. No middle ground; no prompt.
- **Quality FAIL**: never bails. Auto-revise loop with budget `BLOG_AGENT_REVISION_BUDGET` (default 2). After budget exhausted, write `content-pipeline/9-needs-review/{slug}.md` with the punch list and abort the chain (do NOT continue to verify-claims/visuals/publish on broken prose).
- **Capture-visuals**: `UNATTENDED=1` is set automatically. The skill skips per-step confirmations and treats failures as `manifest=failed` rather than blocking.
- **Format-for-publish**: auto-runs as Stage 12 with `--auto-publish` (publishedAt = now). The article goes live on Strapi rather than entering as draft.
- **Final report**: replaces "Next steps" with "Auto-published to <Strapi URL>" + audit log row reference. No "open in browser" instructions.

When `BLOG_AGENT_AUTONOMOUS` is unset (interactive / dev mode), the original behavior applies — every prompt below this section is the interactive default.

## Process

1. **Parse the input.** Extract the keyword (everything before `--context` if present) and the context string (after `--context`, if present).
2. **Slugify.** Run `python scripts/slugify.py "<keyword>"` and capture the slug.
3. **Capture context.** If context was provided, write `content-pipeline/0-context/{slug}.md`:
   ```markdown
   # Context for {slug}

   {the user's context string verbatim}
   ```
4. **Check pipeline status.** Run `python scripts/pipeline_status.py {slug}`. If any stages already exist:
   - **Autonomous mode (`BLOG_AGENT_AUTONOMOUS=1`)**: skip stages whose output files exist (resume-from-failure). Only overwrite if `--regenerate` was passed. No prompt.
   - **Interactive mode**: ask the user whether to skip-or-regenerate before proceeding. Don't silently overwrite.
5. **Run the chain via parallel + sequential agent dispatches** (see "Stage briefs" below for the exact prompt template per stage):
   - **Parallel:** Stage 1 (`/research`) + Stage 2 (`/brand-reference`). Independent.
   - Wait for both. Verify outputs on disk. If either failed, stop and surface the error.
   - **Sequential:** Stage 3 (`/outline`) → Stage 4 (`/product-mentions`) → Stage 5 (`/draft`)
   - **Quality gate:** Stage 6 (`/quality-check`). Read the verdict.
   - **Autonomous mode revision loop** (when `BLOG_AGENT_AUTONOMOUS=1`):
     - On FAIL or BORDERLINE-with-CRITICAL → dispatch Stage 6b targeted-revision Agent (brief expects to address every CRITICAL+HIGH item, not just CRITICAL). Re-run quality-check.
     - Repeat up to `BLOG_AGENT_REVISION_BUDGET` (default 2) total revision passes. Budget covers FAIL retries AND BORDERLINE+CRITICAL retries (one shared budget).
     - After budget exhausted, if verdict still FAIL or BORDERLINE-with-CRITICAL → write `content-pipeline/9-needs-review/{slug}.md` with the punch list, abort the chain (do NOT advance to verify-claims/visuals/publish on broken prose), and emit verdict=QUARANTINED in the final report.
     - On PASS or BORDERLINE-no-CRITICAL → continue.
   - **Interactive mode** (default when AUTONOMOUS unset):
     - On FAIL: stop and surface the punch list. Do NOT advance.
     - On BORDERLINE with CRITICAL items in punch list: dispatch a single targeted-revision Agent with the punch list as the brief. Re-run quality-check once. If still BORDERLINE without CRITICALs, continue.
     - On BORDERLINE without CRITICALs: continue and flag in the final report.
     - On PASS: continue.
   - **Sequential continued:** Stage 7 (`/verify-claims`) → Stage 8 (`/optimize-content`) → Stage 9 (`/generate-visuals`).
   - **Auto-capture-visuals when the Chrome MCP is connected:** if the manifest from stage 9 has `manual` entries that are `action-shot` or `screenshot` types AND the Claude-in-Chrome MCP is reachable (call `mcp__Claude_in_Chrome__list_connected_browsers`; if it returns at least one browser, the MCP is on), dispatch `/capture-visuals` automatically. The user's VPS keeps Chrome + the extension always-on, so this is the normal-running condition — not an opt-in. Only fall through to "surface manual-capture.md and stop" if the MCP is genuinely unreachable. `UNATTENDED=1` only changes whether the capture skill asks for per-step confirmations, not whether it fires.
   - Stage 10 (`/preview`).

6. **Verify each stage's output file exists** before advancing. If a stage's expected file isn't on disk after the agent reports completion, that's a failure even if the agent claimed success.

7. **`/format-for-publish` behavior depends on mode:**
   - **Autonomous mode (`BLOG_AGENT_AUTONOMOUS=1`)**: auto-run as Stage 12. Dispatch a fresh Agent with the brief at "Stage 12 — Format for publish (autonomous only)" below. The article goes live on Strapi. After format-for-publish returns, run `python scripts/auto_publish_check.py {slug}` to verify the public URL renders. On verification failure, write `content-pipeline/9-needs-review/{slug}.md` with the failure reason and emit verdict=QUARANTINED.
   - **Interactive mode**: never auto-run. Editor review owns the gap between preview and publish. The orchestrator surfaces the recommendation to run it when ready.

## Stage briefs

Each stage's Agent dispatch follows this template. Replace `{KEYWORD}`, `{SLUG}`, `{ROOT}` (= `C:\Users\ndong\Downloads\blog-agent` or whatever the project root is on the host).

The brief MUST be self-contained — the spawned agent has no memory of this conversation. Include: project root, slug, keyword, the SKILL file path, the input file paths, the output file path, the editorial constraints that matter for that stage, and an instruction to return a short summary (250–400 words) NOT a full content dump.

### Stage 1 — Research

```
You are running stage 1 of the blog-agent content pipeline at {ROOT}. Keyword: "{KEYWORD}". Slug: {SLUG}. Brand: see brand-config.md.

Your job: produce a research dossier at content-pipeline/1-research/{SLUG}.md per .claude/skills/research/SKILL.md. Read the SKILL.md first and follow it end-to-end.

Critical requirements:
- Use the Semrush MCP for keyword/SERP data + Topic Research
- WebFetch the top 5 SERP URLs (note Cloudflare blocks; don't crash)
- Run deep research via OpenRouter: doppler run -- python .claude/skills/research/scripts/openrouter_research.py --keyword "{KEYWORD}" --slug "{SLUG}"
- ALSO emit content-pipeline/1-research/{SLUG}-data.json with chartable numbers from the dossier (cluster_volumes, format_share, traffic_distribution, whatever the dossier surfaces) — schema described in the research SKILL
- 800–1500 words

Return: word count, recommended angle (one sentence), 3 most surprising findings from deep research, any failures encountered. Under 400 words.
```

### Stage 2 — Brand reference

```
You are running stage 2 at {ROOT}. Slug: {SLUG}. Keyword: "{KEYWORD}". Brand: see brand-config.md.

Your job: produce content-pipeline/2-reference/{SLUG}.md per .claude/skills/brand-reference/SKILL.md. Read the SKILL first.

Steps:
- Refresh the Strapi inventory: doppler run -- python .claude/skills/brand-reference/scripts/fetch_strapi_inventory.py
- Score articles, take top 3–5
- Catalog reusable modules + product-led examples + internal-linking opportunities by H2
- 300–700 words

Return: inventory size, relevant count, top 3 internal-linking opportunities, any failures. Under 250 words.
```

### Stage 3 — Outline

```
You are running stage 3 at {ROOT}. Slug: {SLUG}. Brand: see brand-config.md.

Your job: produce content-pipeline/3-outlines/{SLUG}.md per .claude/skills/outline/SKILL.md. Read the SKILL first.

Inputs to read in order:
1. .claude/skills/outline/SKILL.md
2. .claude/skills/outline/references/bluf-mece-rules.md
3. templates/outline-template.md
4. templates/visual-types.md
5. templates/editorial-principles-visuals.md (the 9-step decision rule for whether a section earns a visual; default `none`)
6. content-pipeline/1-research/{SLUG}.md
7. content-pipeline/1-research/{SLUG}-deep.md (if present)
8. content-pipeline/2-reference/{SLUG}.md
9. brand-config.md
10. 2 articles from examples/ for structural anchoring

Editorial requirements:
- 4–7 H2s, MECE, BLUF on every opener
- Each H2 has BLUF + 2–4 key points + evidence + transition + typed Visual + word target
- Default Visual is `none` — most sections should have none. AI-content's #1 failure mode is sprinkling visuals
- Run the visual sanity check + structural self-check before saving
- Title under 60 chars, includes primary keyword

Return: title, one-sentence thesis, H2 list with one-line description each, count of non-`none` Visuals (and which type), any structural concerns. Under 350 words.
```

### Stage 4 — Product mentions

```
You are running stage 4 at {ROOT}. Slug: {SLUG}. Brand: see brand-config.md.

Your job: produce content-pipeline/4-outlines-annotated/{SLUG}.md per .claude/skills/product-mentions/SKILL.md. Read the SKILL first — including the **Constraint reconciliation pass** at the top.

Critical: BEFORE annotating, scan the outline for any contradictions on coming-soon products. If the outline both mentions a coming-soon product in a section AND has a rule restricting that product to a different section, DELETE the contradicting bullet and log the deletion at the top of the annotated file under `## Pre-flight reconciliation`. The draft must never see contradictory state.

Editorial requirements:
- Aim for 3–5 product-mention annotations across all H2s — don't shoehorn
- Each annotation specifies HOW (walkthrough / inline / tip box)
- When a walkthrough adds visuals, upgrade the section's existing Visual field to typed form
- Reference existing brand-reference articles so the new piece doesn't re-explain workflows
- No coming-soon products in walkthrough or evergreen sections

Return: number of sections annotated, the H2-by-H2 product plan as a table, any reconciliation deletions logged, any rejected mentions with reason. Under 250 words.
```

### Stage 5 — Draft

```
You are running stage 5 at {ROOT}. Slug: {SLUG}. Brand: see brand-config.md.

Your job: produce content-pipeline/5-drafts/{SLUG}.md per .claude/skills/draft/SKILL.md. Read the SKILL first — particularly the voice metrics targets at the top.

Voice metrics targets (HARD — these are not soft self-edit suggestions):
- Avg paragraph length: 24–35 words
- Em-dash density: 6–8 per 1000 words
- Second-person words ("you", "your") per 1000 words: 25+
- Sentence-length variance: matches examples baseline within 1.5 SD

Read these references in order before drafting:
1. .claude/skills/draft/SKILL.md
2. .claude/skills/draft/references/voice-guide.md
3. .claude/skills/draft/references/prose-patterns.md (includes worked-example paragraph showing right rhythm)
4. brand-config.md (especially forbidden phrases)
5. templates/visual-types.md
6. content-pipeline/4-outlines-annotated/{SLUG}.md
7. content-pipeline/2-reference/{SLUG}.md
8. content-pipeline/1-research/{SLUG}.md (+ {SLUG}-deep.md)
9. At least 2 articles from examples/

Editorial requirements:
- Every section opens with a BLUF
- No forbidden phrases — cut on sight
- Cut "Furthermore", "Moreover", "It is important to note", "very", "really", "quite", "actually" (when not load-bearing), "simply"
- Show, don't sell — for product mentions follow the annotated outline's slot-by-slot plan exactly
- Coming-soon products only in the slots the annotated outline approved
- Internal links from 2-reference woven inline as [anchor](URL)
- Stat citations as [link] markers for verify-claims to resolve
- Visual placeholders use typed [VISUAL:type=...;...] syntax per visual-types.md
- For chart placeholders: use data=research.<key> where <key> is a key in {SLUG}-data.json (the research stage emits it). Don't write data=research.X with a placeholder X — pick a real key.

Self-check before save:
- Run a quick metrics check: count em-dashes, count "you/your", measure avg paragraph length. If any metric is more than 1.5x off the targets above, REVISE before saving rather than saving and letting quality-check fail.

Save to content-pipeline/5-drafts/{SLUG}.md. Word target: per outline.

Return: word count, voice metrics (em-dash/1k, you-words/1k, avg paragraph), [link] count, [VISUAL] count, confirmation no forbidden phrases or out-of-slot product mentions. Under 400 words.
```

### Stage 6 — Quality check (gate)

```
You are running stage 6 at {ROOT}. Slug: {SLUG}. This is the quality gate.

Your job: produce content-pipeline/quality-checks/{SLUG}.md per .claude/skills/quality-check/SKILL.md. Read the SKILL first.

Steps:
1. Run python .claude/skills/quality-check/scripts/quality_check.py {SLUG}
2. Spawn a Task sub-agent for the adversarial read with the brief specified in the SKILL
3. Combine into a verdict report with:
   - Verdict at top: PASS (≥75) / BORDERLINE (60–74) / FAIL (<60)
   - Metrics summary
   - Adversarial critique
   - Punch list ordered by severity (CRITICAL / HIGH / MEDIUM / LOW)
   - Recommendation

Specifically check for constraint violations like coming-soon products appearing in walkthrough sections — these are CRITICAL even if the score is 75+.

Return: verdict, score, top 3 punch-list items by severity, whether any CRITICAL items remain, and whether to proceed/iterate/halt.
```

### Stage 6b — Targeted revision (only if BORDERLINE with CRITICAL items)

```
You are running a surgical revision pass at {ROOT}. Slug: {SLUG}.

The draft scored BORDERLINE on the quality gate with one or more CRITICAL or HIGH punch-list items. Apply ONLY the targeted fixes the punch list calls for — NOT a full re-draft.

Inputs:
- content-pipeline/quality-checks/{SLUG}.md (the punch list)
- content-pipeline/5-drafts/{SLUG}.md (the draft)
- content-pipeline/4-outlines-annotated/{SLUG}.md (the source of truth on constraints)
- brand-config.md, .claude/skills/draft/references/voice-guide.md

Apply each CRITICAL and HIGH item using Edit calls (not Write). Preserve all [link] markers, all typed [VISUAL] placeholders, all internal links. Save back to content-pipeline/5-drafts/{SLUG}.md.

Return: each fix applied (Y/N), key metric deltas (em-dashes before/after, paragraph length before/after), confirmation any CRITICAL constraint violations are resolved.
```

After 6b, the orchestrator re-dispatches stage 6 (quality-check) once. If still BORDERLINE without CRITICAL, continue to stage 7. If FAIL or CRITICAL still present, halt and surface to user.

### Stage 7 — Verify claims

```
You are running stage 7 at {ROOT}. Slug: {SLUG}.

Your job: produce content-pipeline/6-drafts-cited/{SLUG}.md per .claude/skills/verify-claims/SKILL.md. Read the SKILL first — particularly the two-tier citation rule (must-cite vs voice-flagged).

Resolve every [link] placeholder with a real source via WebSearch + WebFetch. Use editor-note anchors for internal-Semrush metrics. Wire internal links from 2-reference. Apply the two-tier density check (must-cite ≥60% linked, voice-flagged listed for editor review — never auto-linked).

Return: [link] placeholders replaced (count), [CITATION NEEDED] flags remaining, internal links wired, must-cite density %, voice-flagged statements listed for review.
```

### Stage 8 — Optimize content (ContentShake AI)

```
You are running stage 8 at {ROOT}. Slug: {SLUG}.

Your job: per .claude/skills/optimize-content/SKILL.md. Run /optimize-content for {SLUG}. The skill calls Semrush ContentShake AI via .claude/skills/optimize-content/scripts/contentshake_optimize.py — no Chrome MCP, no Sonnet sub-agent for browser driving, no TipTap injection, no port-8766 server, no 50-doc/month cap.

Iteration loop: max 5 iterations. Stops on (seo_score >= 8 AND quality_score >= 8) → WIN, OR voice-drift > 8 pts vs baseline → ROLLBACK (revert last iteration), OR < 0.5pt lift twice in a row → PLATEAU, OR 5 iterations → CAPPED. Voice-drift safety net is non-negotiable.

Skip conditions — both write a stub at content-pipeline/optimization/{SLUG}.md and exit 0 so the pipeline continues:
- Neither SEMRUSH_API_KEY_BLOG_AGENT nor SEMRUSH_API_KEY_CONTENTSHAKE set in env (load via Doppler).
- Monthly API budget (BLOG_AGENT_CONTENTSHAKE_MONTHLY_CAP, default 100) already exhausted.
- contentshake_optimize.py exits 75 (mid-run quota — quota convention shared with the orchestrator).

Return: verdict (WIN/ROLLBACK/PLATEAU/CAPPED/SKIPPED), SEO and Quality scores before/after, voice-drift delta, iterations used, budget consumed/remaining, and one-line summary.
```

### Stage 9 — Generate visuals

```
You are running stage 9 at {ROOT}. Slug: {SLUG}.

Your job: per .claude/skills/generate-visuals/SKILL.md. Run the dispatcher:
  doppler run -- python .claude/skills/generate-visuals/scripts/generate_visuals.py {SLUG}

The dispatcher reads typed [VISUAL] placeholders from the cited draft, captures what it can (screenshot via patchright; chart via matplotlib using {SLUG}-data.json keys; image via Replicate), and routes everything else to manual-capture.md.

If the dispatcher reports any chart with status=failed and reason=invalid_data_spec, that means {SLUG}-data.json is missing the key the placeholder references. In that case, read the research dossier, extract the actual numbers, append them to {SLUG}-data.json under the right key, and re-run the dispatcher. Do not hand-render charts; the data file is the single source of truth.

Return: captured / manual / failed counts, manifest path, manual-capture path.
```

### Stage 10 — Preview

```
You are running stage 10 at {ROOT}. Slug: {SLUG}.

Your job: render content-pipeline/7-preview/{SLUG}.html per .claude/skills/preview/SKILL.md. Run:
  python .claude/skills/preview/scripts/render_preview.py {SLUG}

Return: preview path. If render produced warnings, list them.
```

### Stage 11 (auto, when Chrome MCP is connected) — Capture visuals

This stage fires whenever stage 9's manifest has `manual` entries AND the Chrome MCP is reachable. The user's VPS Chrome stays always-on, so the normal expectation is that this fires. `UNATTENDED=1` is a separate signal that controls the *capture skill's* internal behavior (no per-step confirmations) — it does NOT gate whether stage 11 runs.

```
You are running stage 11 at {ROOT}. Slug: {SLUG}.

Your job: per .claude/skills/capture-visuals/SKILL.md. Drive the always-on Chrome via the Claude-in-Chrome MCP for each manual entry in content-pipeline/images/{SLUG}/manual-capture.md. Use Sonnet 4.6 (claude-sonnet-4-6) — Opus is wasted on browser driving.

If UNATTENDED=1 is set, run the skill in unattended mode (no per-step confirmations, errors flagged in manifest, validation heuristics are the safety net). Otherwise run interactively — but in an orchestrator context the user isn't at the keyboard mid-pipeline anyway, so default to autonomous capture even without UNATTENDED.

After captures land, rewrite the cited draft to swap [VISUAL:...] placeholders for ![alt](images/{SLUG}/file.png) markdown, update manifest.json, and re-run the preview script.

Return: captured / skipped / failed counts; updated preview path.
```

### Stage 12 — Format for publish (autonomous only)

```
You are running stage 12 at {ROOT}. Slug: {SLUG}. Autonomous mode.

Your job: per .claude/skills/format-for-publish/SKILL.md (read it first). Run:
  doppler run -- python .claude/skills/format-for-publish/scripts/format_for_strapi.py {SLUG} --auto-publish

The --auto-publish flag (and BLOG_AGENT_AUTO_PUBLISH=1 env) sets publishedAt = now in the Strapi payload, so the article goes live rather than entering as draft.

The script will:
- Re-read content-pipeline/quality-checks/{SLUG}.md and refuse to publish if verdict is FAIL (belt-and-suspenders gate)
- Build the Strapi payload, copy images into the publish folder, optionally upload media
- POST to Strapi with publishedAt set to current ISO timestamp
- Print the public URL on success

After the script returns success, run:
  python scripts/auto_publish_check.py {SLUG}

Confirm exit 0. On non-zero, the script writes content-pipeline/9-needs-review/{SLUG}.md — surface that to the orchestrator's verdict so the article gets QUARANTINED instead of reported as published.

Return: Strapi article ID (if returned), public URL, auto_publish_check exit code, any errors.
```

## Reporting format

When the pipeline finishes, output:

```
✓ Pipeline complete for "{keyword}" (slug: {slug})

Stages run:
  ✓ research              → content-pipeline/1-research/{slug}.md (+ {slug}-deep.md, {slug}-data.json)
  ✓ brand-reference       → content-pipeline/2-reference/{slug}.md
  ✓ outline               → content-pipeline/3-outlines/{slug}.md
  ✓ product-mentions      → content-pipeline/4-outlines-annotated/{slug}.md
  ✓ draft                 → content-pipeline/5-drafts/{slug}.md
  ✓ quality-check         → content-pipeline/quality-checks/{slug}.md (verdict: PASS|BORDERLINE)
  ✓ verify-claims         → content-pipeline/6-drafts-cited/{slug}.md
  ✓ optimize-content      → content-pipeline/optimization/{slug}.md (verdict WIN|ROLLBACK|PLATEAU|CAPPED|SKIPPED)
  ✓ generate-visuals      → content-pipeline/images/{slug}/manifest.json (N captured, M manual)
  ✓ capture-visuals       → (only if UNATTENDED=1; otherwise listed under "Next steps")
  ✓ preview               → content-pipeline/7-preview/{slug}.html

Next steps (interactive mode only):
  1. Open content-pipeline/7-preview/{slug}.html in your browser to review
  2. (If manual-capture.md non-empty AND not UNATTENDED) Run /capture-visuals {slug} to drive Chrome MCP for the remaining visuals
  3. When ready, run /format-for-publish {slug} to package for Strapi
```

In **autonomous mode** (`BLOG_AGENT_AUTONOMOUS=1`), the final report instead reads:

```
✓ Pipeline complete for "{keyword}" (slug: {slug}) — AUTONOMOUS

Stages run:
  ✓ research / brand-reference / outline / product-mentions / draft
  ✓ quality-check         → verdict: PASS|BORDERLINE-no-CRITICAL (after N revision passes)
  ✓ verify-claims / optimize-content / generate-visuals / capture-visuals / preview
  ✓ format-for-publish    → article.md, article.json, README.md
  ✓ Auto-published to <Strapi public URL>
  ✓ auto_publish_check    → verified live H1

Audit log row appended: content-pipeline/audit/auto-blog-log.csv
```

If the article was quarantined (verdict QUARANTINED after revision budget exhausted, or auto_publish_check failed), the report ends:

```
✗ Pipeline halted for "{keyword}" (slug: {slug}) — QUARANTINED

Last good stage: <name>
Failure reason:  <one-line>
Quarantine path: content-pipeline/9-needs-review/{slug}.md

Audit log row appended (action=quarantined).
```

## Quality-check gating

- **PASS (≥75):** advance silently
- **BORDERLINE (60–74), no CRITICAL:** advance, flag in final report
- **BORDERLINE (60–74), CRITICAL present:** dispatch one targeted-revision pass, re-run quality-check, then advance only if CRITICAL is resolved
- **FAIL (<60):** stop, surface punch list, do not advance

## When a stage's agent fails

If an agent reports an error or its expected output file isn't on disk:
- Don't skip ahead. Surface the failure with stage name + agent's error message.
- Save partial state so the user can resume from the failing stage.
- Do NOT retry automatically — agents that fail once usually fail repeatedly without an underlying fix.

## When the user wants to re-run from a stage

The user can dispatch any stage's brief manually (e.g., re-run stage 5 by copying the Stage 5 brief above with their slug). The orchestrator is not the only entry point.
