---
name: optimize-content
description: Optimize the cited draft against Ahrefs term/topic coverage. Pulls related/matching terms (keywords-explorer) and competitor organic-keyword coverage (site-explorer) via the Ahrefs MCP to surface what the draft is missing relative to the SERP top-rankers, then judgment-rewrites the additions in brand voice. Iterates until term coverage is saturated and /quality-check passes, or voice drift triggers a rollback. No Chrome MCP, no TipTap injection — MCP data + judgment.
allowed-tools: Read, Write, Edit, Bash, mcp__ahrefs__*
---

# Optimize Content Skill (Ahrefs term + topic coverage)

Uses the Ahrefs MCP to surface what the cited draft is missing relative to the SERP top-rankers — the recommended-term pool and the competitor topic coverage — then applies the gaps **rewritten in brand voice**, not pasted verbatim. Re-runs `/quality-check` after each iteration to catch any voice drift the optimization caused.

> **DATA LAYER RULING (2026-06-24).** ContentShake AI (a Semrush product) is **dropped** along with Semrush and DataForSEO. There is no ContentShake API call and no `contentshake_optimize.py` in this flow any more. The "SEO score / Quality score" that ContentShake returned is replaced by **Ahrefs term-coverage** (objective: which recommended terms/topics the draft already covers) plus the **existing `/quality-check` score** (the real, benchmark-relative quality gate). Read [`../research/references/ahrefs-mcp-cheatsheet.md`](../research/references/ahrefs-mcp-cheatsheet.md) first — params are comma-separated **strings** not JSON arrays, `select` + `country` are required, and you call `doc {tool:"..."}` for any tool you haven't used this run.

## How the signal is sourced now (replaces the ContentShake call)

The Ahrefs Content Helper flow (browser-driven, TipTap injection, port-8766 server, 50-doc/month cap) and the later ContentShake API flow are **both gone**. The same signal — *what concepts and terms do the winning pages cover that this draft doesn't* — comes directly from the Ahrefs MCP:

1. **Recommended-term pool** — `mcp__ahrefs__keywords-explorer-related-terms` ("also rank for" / "also talk about") + `mcp__ahrefs__keywords-explorer-matching-terms` (`match_mode:"phrase"`, then `"terms"`) on the target keyword, `country:"US"`, `select:"keyword,volume,difficulty,intents"`. Keep same-parent-topic, same-intent terms; this is the term list the draft is scored for coverage against.
2. **Competitor topic coverage** — `mcp__ahrefs__site-explorer-organic-keywords` on the top-3 ranking URLs (from the research dossier's SERP benchmark, or `mcp__ahrefs__serp-overview` if absent), `select:"keyword,volume,best_position"`, `limit` tight. Topics ≥2 of the top pages rank for, that the draft doesn't cover, are the **missing-topics** list.
3. **Coverage check is local** — for each recommended term / competitor topic, mark `in_draft` true/false by scanning the draft text. `term_coverage = covered / total`. This is the objective number that replaces ContentShake's `seo_score`; the brand-voice + benchmark judgment that replaces ContentShake's `quality_score` is the existing `/quality-check` score.

> The win target is no longer "SEO ≥ 8 AND Quality ≥ 8" (ContentShake's two numbers). It is now **term coverage ≥ 0.8 of the must-cover terms AND `/quality-check` ≥ 85 (PASS)** — see "Stopping conditions" below. Thresholds elsewhere (voice-drift, budget, iteration cap) are UNCHANGED.

## Hard constraints

### Voice-drift safety net (UNCHANGED — the user explicitly called this out)

Voice integrity is the load-bearing constraint. Term-coverage recommendations are useless if applying them breaks the brand's voice. After every iteration's local edits, run `/quality-check` and compare against the pre-optimization baseline (saved at iteration 0):

- **Voice drift > 8 pts** → REVERT the latest iteration's edits and stop the loop. Surface: `Voice drift triggered at iteration N. Best score reached without drift: X. Final draft is the iteration N-1 version.`
- **Voice drift 4–8 pts** → continue, but flag the iteration in the report so the editor can review whether a partial revert is warranted.
- **Voice drift < 4 pts** → no action; continue.

This rule is non-negotiable. Score lift means nothing if the article reads like AI-stuffed SEO afterwards.

### Ahrefs-units budget — `BLOG_AGENT_OPTIMIZE_MONTHLY_CAP` (default 100)

The legacy 50-doc/month doc-count budget (and the ContentShake API-call budget that replaced it) is now an **Ahrefs-MCP call budget** — Ahrefs units are real money (≈ 50 base + per-row per report; check any time with `subscription-info-limits-and-usage`). Count each iteration's term-pull + competitor-coverage pull as the unit charge. Budget tracked in `content-pipeline/optimization/api-budget.md`:

- **At < 80% of cap:** call freely
- **At 80–99% of cap:** warn the user, list the slug + iteration, ask explicit confirmation before each remaining call
- **At 100% of cap:** REFUSE further calls. Save a stub report at `content-pipeline/optimization/{slug}.md` noting the cap was hit; recommend either waiting for monthly reset or raising `BLOG_AGENT_OPTIMIZE_MONTHLY_CAP`. Pipeline continues without the optimization step.

Reset is automatic at the start of each calendar month (UTC) — the budget file's `month: YYYY-MM` line decides the rollover.

### Ahrefs MCP unavailable — fail soft, pipeline continues

If the Ahrefs MCP isn't reachable (no `mcp__ahrefs__*` tools loaded, or `AHREFS_MCP_KEY` not set so every call errors):

1. Write a stub report to `content-pipeline/optimization/{slug}.md`:
   ```markdown
   # optimize-content — skipped

   - Reason: Ahrefs MCP not reachable (tools not loaded / AHREFS_MCP_KEY unset).
   - Action: launch via `doppler run -- claude` so the Ahrefs MCP loads from .mcp.json, then re-run `/optimize-content {slug}`.
   - Pipeline: continues without the term-coverage optimization. /quality-check still gates publish.
   ```
2. Print the same message to stdout.
3. Exit 0. The blog pipeline must not block on a missing data layer — same convention `/research` uses for a missing OpenRouter key. Note: `/quality-check` remains the publish gate either way, so a skipped optimize-content does not ship unreviewed prose.

## Input

For slug `{slug}`:
- `content-pipeline/6-drafts-cited/{slug}.md` (preferred — the cited draft)
- `content-pipeline/5-drafts/{slug}.md` (fallback if not cited yet)
- `content-pipeline/1-research/{slug}.md` (for the target keyword and SERP context)
- `brand-config.md` + 2 `examples/voice/*.md` (voice anchors for the rewrite step; read `examples/README.md` first)

Locate the draft directly (cited → uncited preference): `content-pipeline/6-drafts-cited/{slug}.md`, else `content-pipeline/5-drafts/{slug}.md`.

## Process

### Phase A — preflight

1. **Load the target keyword** from `content-pipeline/1-research/{slug}.md` frontmatter (or fall back to the slug itself with hyphens replaced by spaces).
2. **Read the budget file** at `content-pipeline/optimization/api-budget.md`. If absent, create with `month: YYYY-MM` and `calls: 0`. If month rolled over, reset.
3. **Verify the Ahrefs MCP is reachable** — confirm `mcp__ahrefs__*` tools are loaded (a quick `doc {tool:"keywords-explorer-related-terms"}` both verifies reachability and fetches the schema). If unreachable → write stub report, exit 0 (see "Ahrefs MCP unavailable" above).
4. **Snapshot the baseline draft** to `content-pipeline/optimization/{slug}-iter-0.md` and run `/quality-check {slug}` to capture the pre-optimization quality score. Persist to `content-pipeline/optimization/{slug}-baseline-quality.md`.

### Phase B — initial Ahrefs coverage pull

5. **Pull the recommended-term pool and competitor coverage** via the Ahrefs MCP (see "How the signal is sourced now"):
   - `mcp__ahrefs__keywords-explorer-related-terms` + `mcp__ahrefs__keywords-explorer-matching-terms` on `{keyword}` → recommended terms.
   - `mcp__ahrefs__site-explorer-organic-keywords` on the top-3 ranking URLs → competitor topic coverage.
6. **Build the coverage report** for iteration 1: for each term/topic, scan the draft and mark `in_draft`; compute `term_coverage`. Increment the budget file's `calls` counter by the number of MCP reports run.
7. **If an Ahrefs call returns a units/quota error (HTTP 429 or a quota message):** save what we have to `content-pipeline/optimization/{slug}.md` noting quota exhaustion, exit 0 cleanly. Pipeline continues.
8. **If an Ahrefs call errors transiently (5xx / network):** retry once; on a second failure save the error to `content-pipeline/optimization/{slug}-errors.log` and exit 0 with a stub report. Don't crash the pipeline on a transient API error.
9. **Save the coverage report** (term list with `in_draft` flags + missing-topics list + `term_coverage`) to `content-pipeline/optimization/{slug}-coverage-iter-1.json`.

### Phase C — iteration loop (max 5)

For each iteration `i` in 1..5:

- Read the latest coverage report (`{slug}-coverage-iter-{i}.json`).
- **Stopping conditions** (check BEFORE doing more edits):
  - **Win:** `term_coverage ≥ 0.8` of the must-cover terms AND the latest `/quality-check` ≥ 85 (PASS) → stop with verdict `WIN`
  - **Voice protection:** quality-check dropped by > 8 pts vs baseline → REVERT iteration `i`'s edits, stop with verdict `ROLLBACK`
  - **Stagnation:** the last two iterations each lifted `term_coverage` by < 0.05 (or quality-check moved < 1 pt across both) → stop with verdict `PLATEAU`
  - **Cap:** `i == 5` → stop with verdict `CAPPED`
- **Otherwise, do the edit pass:**
  - Identify the missing competitor topics and the highest-volume recommended terms not yet `in_draft`. Pick **1–3 surgical edits** per iteration (a new paragraph, a term weave, a section expansion).
  - **Read 1 example article** from `examples/` first to anchor voice for this pass. The voice in those files is the source of truth.
  - For each accepted edit:
    - **Skip if** the term is a synonym for content already in the draft (saturated), OR the topic doesn't fit the brand's positioning, OR adding it would distort the article's thesis, OR it includes forbidden phrases from `brand-config.md`.
    - **Add if** it names a concept the article should cover but doesn't AND it can be incorporated without forcing.
    - **Aim** for applying 60–80% of the gap items; rejecting the rest is normal.
    - **Compose 1–3 sentences in brand voice** — NOT a verbatim keyword paste. Use the recommended term once, naturally, where it fits. Do not keyword-stuff.
  - Apply edits via `Edit`. Preserve existing prose, citations, and `[VISUAL:...]` placeholders.
  - Save the post-edit draft as `content-pipeline/optimization/{slug}-iter-{i}.md` (so revert is a file copy, not a diff replay).
  - **Re-check coverage locally** by re-scanning the edited draft against the same term/topic lists from iteration 1 (no new Ahrefs call needed unless the keyword set changed — this conserves units). Only re-pull from Ahrefs if you suspect the term pool was incomplete.
  - Persist the new coverage report to `{slug}-coverage-iter-{i+1}.json`. Increment budget only if an Ahrefs call was actually made.
  - **Run `/quality-check {slug}`** locally. Compare against baseline. Append the result + voice-drift delta to `content-pipeline/optimization/{slug}-iterations.md`.

### Phase D — finalize

After the loop exits (win, rollback, plateau, or capped):

10. **Save the canonical optimized draft** to its original location (`6-drafts-cited/{slug}.md` if that's what was input, else `5-drafts/{slug}.md`).
11. **Write the optimization report** to `content-pipeline/optimization/{slug}.md`:
    - Verdict (WIN / ROLLBACK / PLATEAU / CAPPED)
    - Term coverage before / after (fraction of must-cover terms `in_draft`)
    - Quality-check score before / after, drift delta
    - Iterations used; budget consumed; budget remaining
    - Terms / topics applied (with reasoning per accepted)
    - Terms / topics skipped (with reasoning)
    - If verdict == ROLLBACK: which iteration triggered the revert and what changed
12. **Re-trigger `/quality-check {slug}` once more** so the next pipeline stage sees fresh voice metrics. This call is free (local script).
13. **Print a one-line summary** to stdout, e.g.:
    `optimize-content: coverage 0.55→0.86, quality 79→84 (drift OK), 3 iterations, verdict=WIN, budget 38/100`

## Output

- `content-pipeline/optimization/{slug}.md` — final report (verdict + coverage/quality scores + terms applied/skipped + budget)
- `content-pipeline/optimization/{slug}-iterations.md` — per-iteration log with coverage lifts and voice drift
- `content-pipeline/optimization/{slug}-iter-{i}.md` — post-edit draft snapshot per iteration (for revert + audit)
- `content-pipeline/optimization/{slug}-coverage-iter-{i}.json` — Ahrefs term/topic coverage reports per iteration (for audit + future training data)
- `content-pipeline/optimization/{slug}-baseline-quality.md` — pre-optimization voice score
- `content-pipeline/optimization/api-budget.md` — running monthly API-call counter
- Updated `content-pipeline/6-drafts-cited/{slug}.md` (or `5-drafts/{slug}.md`) — the optimized draft
- Refreshed `content-pipeline/quality-checks/{slug}-metrics.md`

## Quality checklist

- [ ] Ahrefs MCP reachable (or stub report written + exit 0)
- [ ] Budget file updated; not over cap
- [ ] Baseline quality-check captured at iteration 0
- [ ] At least 5 recommended terms / missing topics evaluated explicitly (accept or reject + reason)
- [ ] Every accepted addition rewritten in brand voice (NOT a verbatim keyword paste)
- [ ] Each addition uses the recommended term ONCE, not stuffed
- [ ] No forbidden phrases from `brand-config.md` introduced by additions
- [ ] `/quality-check` re-run after EVERY iteration's edits
- [ ] Voice-drift > 8 triggered a rollback (when applicable)
- [ ] Report file lists what was applied + skipped + reasoning
- [ ] One-line summary printed with budget status

## When Ahrefs returns a thin term pool

If `keywords-explorer-related-terms` + `matching-terms` return very few same-intent terms (rare — usually a brand-new or zero-volume keyword) and the competitor-coverage pull is also thin:

- Treat as: skip the coverage-based stopping conditions for this iteration, but still apply judgment edits from any missing competitor topics present.
- Note in the report: "Ahrefs returned a thin term pool for iteration N — treating coverage as non-load-bearing for win-detection; `/quality-check` remains the gate."
- Still run `/quality-check` so voice drift is monitored.

## When the iteration loop hits the budget cap mid-run

Persist whatever progress was made (last good iteration draft, last coverage report). Save the report with verdict `BUDGET_EXHAUSTED`. The next `/optimize-content` run on this slug picks up from the saved iteration draft — no re-baselining needed unless the user passes `--regen`.

## When coverage doesn't move across two iterations

This is the `PLATEAU` verdict. Most common cause: the brand-voice rewrites used synonyms or different phrasings rather than the recommended terms verbatim, so a literal term-match coverage scan doesn't tick up. **This is FINE.** Term coverage is a heuristic; voice integrity matters more long-term. Note in the report:

> "Coverage plateaued — additions used voice-appropriate phrasings rather than the recommended terms verbatim. This is intentional."

Don't try harder. Plateau is an acceptable terminal state.

## Why we don't apply recommendations blindly

The Ahrefs term/topic recommendations are based on what's already ranking. Following them mechanically produces content that resembles existing top-rankers — middle-of-the-pack SEO. The article won't outperform what's already there because it'll BE what's already there.

The judgment step is what gets you BOTH ranking benefit AND differentiation. The voice rewrite step is what protects against the Helpful Content Update / AI-detection risks. Skip judgment + voice rewrite and you have an SEO-stuffing skill — that's not what this is.

## When `/draft-score` was already run

If `content-pipeline/optimization/{slug}-draft-score.json` exists from a `/draft-score` self-check pass during drafting, read it as a hint about how close the draft already is — but still do the full Ahrefs term + competitor-coverage pull at iteration 1. The lightweight `/draft-score` self-check doesn't include the competitor-coverage / missing-topics lists this skill needs.
