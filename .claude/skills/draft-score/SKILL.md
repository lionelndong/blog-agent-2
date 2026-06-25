---
name: draft-score
description: Lightweight Ahrefs term-coverage self-check the /draft stage can call before saving. Returns a coverage fraction + term/competitor-topic gap count (no full optimization pass) so the writer knows whether the draft is in winning territory before /quality-check runs. Fails soft when the Ahrefs MCP is unreachable.
allowed-tools: Read, Write, Bash, mcp__ahrefs__*
---

# Draft Score Skill (Ahrefs coverage self-check)

Run a lightweight Ahrefs term-coverage check on the current draft so the writer / orchestrator knows whether the draft is already close to winning territory. Cheaper than the full `/optimize-content` pass — it pulls only the recommended-term pool (no competitor organic-keyword deep-dive) and scans the draft for coverage.

> **DATA LAYER RULING (2026-06-24).** ContentShake AI (a Semrush product) is **dropped** along with Semrush and DataForSEO — there is no `contentshake_optimize.py` and no ContentShake `score` action any more. The "SEO + Quality score" this skill used to return is replaced by an **Ahrefs term-coverage fraction**. Read [`../research/references/ahrefs-mcp-cheatsheet.md`](../research/references/ahrefs-mcp-cheatsheet.md) first; params are comma-separated **strings** not arrays, and `select` + `country` are required.

This skill is **optional** in the pipeline. If the draft already covers the term pool, it lets the orchestrator skip directly to `/quality-check` → `/verify-claims` and save a full `/optimize-content` pass for a future revision. If coverage is thin, it's an early warning that `/optimize-content` will need its full iteration budget.

## Input

`/draft-score {slug}`

Reads:
- `content-pipeline/5-drafts/{slug}.md` (or `6-drafts-cited/{slug}.md` if already cited)
- `content-pipeline/1-research/{slug}.md` (target keyword)

## Process

### Step 1 — Preflight

1. Confirm the draft exists. If not, exit with a clear error.
2. Read the target keyword from the research dossier's frontmatter (or fall back to the slug with hyphens replaced by spaces).
3. Confirm the Ahrefs MCP is reachable (the `mcp__ahrefs__*` tools are loaded).

### Step 2 — Soft-fail when the Ahrefs MCP is unreachable

If the Ahrefs MCP isn't loaded / `AHREFS_MCP_KEY` is unset so calls error:

1. Print to stdout:
   ```
   draft-score: Ahrefs MCP not reachable. Skipping coverage self-check.
                Launch via `doppler run -- claude` so the MCP loads. Pipeline continues.
   ```
2. Write a stub at `content-pipeline/optimization/{slug}-draft-score.json`:
   ```json
   {
     "skipped": true,
     "reason": "Ahrefs MCP not reachable",
     "_meta": {"slug": "{slug}", "action": "score"}
   }
   ```
3. Exit 0. **Same convention `/research` uses for missing OpenRouter** — never block the pipeline on a missing optional data layer.

### Step 3 — Pull the term pool and scan for coverage

1. Call `mcp__ahrefs__keywords-explorer-related-terms` (and `mcp__ahrefs__keywords-explorer-matching-terms` with `match_mode:"phrase"`) on `{keyword}`, `country:"US"`, `select:"keyword,volume,intents"`. Keep same-intent terms — this is the must-cover term pool.
2. Scan the draft text; mark each term `in_draft` true/false. Compute `term_coverage = covered / total`.

This is the lightweight read — it does NOT pull competitor organic keywords (that deep-dive is `/optimize-content`'s job). It counts against the same `BLOG_AGENT_OPTIMIZE_MONTHLY_CAP` budget tracked by `/optimize-content`.

### Step 4 — Persist the result

Save the coverage result (`term_coverage`, covered/total counts, the unmatched terms) to `content-pipeline/optimization/{slug}-draft-score.json`. Increment the budget counter at `content-pipeline/optimization/api-budget.md` (shared with `/optimize-content`).

### Step 5 — Print the verdict

```
draft-score: coverage 0.72 (18/25 terms)   verdict=NEEDS_OPTIMIZE
  → /optimize-content {slug} likely needed before publish
```

Verdict heuristic:

| Condition | Verdict | Implication for orchestrator |
|---|---|---|
| `term_coverage ≥ 0.8` | `WIN_LIKELY` | `/optimize-content` may be skippable — quality-check first, then decide |
| `term_coverage ≥ 0.65` | `BORDERLINE` | Run `/optimize-content` but expect 1–2 iterations to clear |
| Otherwise | `NEEDS_OPTIMIZE` | `/optimize-content` should run with full iteration budget |

## Output

- `content-pipeline/optimization/{slug}-draft-score.json` — the coverage result (or stub if skipped)
- One-line verdict to stdout

## Quality checklist

- [ ] Draft file exists and was readable
- [ ] Target keyword resolved from research dossier or slug
- [ ] Soft-fail path runs cleanly when the Ahrefs MCP is unreachable (exits 0, writes stub)
- [ ] Result JSON persisted to `optimization/{slug}-draft-score.json`
- [ ] Verdict printed with the recommended next action

## When to call this skill

This skill is designed to be called from the `/draft` stage **after the draft is written but before `/quality-check`** — a "is this close to ready?" signal. It's also fine to call standalone:

- During iterative revisions, to see if a manual edit moved coverage
- Before deciding whether to schedule `/optimize-content` (saves a full optimize pass when the draft is already strong)
- After `/update-draft` to see if the refresh moved coverage in the right direction

## When NOT to call this skill

- When `/optimize-content` is about to run anyway — the full optimize pass produces coverage AND the competitor-topic gap list, so the lightweight self-check is redundant and wastes a budget unit
- When the budget is at 100% — `/optimize-content`'s budget gate also covers this skill; skip rather than record another attempted call

## Why not just call `/optimize-content`

`/optimize-content` is a 5-iteration loop that mutates the draft. This skill is a **read-only** coverage check. Call this when you want to know "where do I stand?" without committing to the full optimization. Two distinct jobs.
