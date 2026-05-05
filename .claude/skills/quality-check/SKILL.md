---
name: quality-check
description: Score the draft on voice match, BLUF compliance, forbidden phrases, claim density, and run an adversarial read. Inserted between /draft and /verify-claims so quality issues get caught before citation work.
allowed-tools: Read, Write, Bash, Task
---

# Quality Check Skill

Reads the draft and produces a quality scorecard + a punch list of specific fixes. The scorecard catches AI tells, voice drift, weak structure, and unsupported claims BEFORE the editor or `/verify-claims` reads it.

## Input

For slug `{slug}`:
- `content-pipeline/5-drafts/{slug}.md` (the draft to score)
- `brand-config.md` (forbidden phrases, voice config)
- `examples/*.md` (voice baseline)
- `.claude/skills/draft/references/voice-guide.md` (voice rules)

## Process

1. **Run the automated metrics script:**
   ```bash
   python .claude/skills/quality-check/scripts/quality_check.py "<slug>"
   ```
   This produces `content-pipeline/quality-checks/{slug}-metrics.md` with:
   - Forbidden phrase scan (regex against the brand-config list)
   - Voice metrics (sentence length, paragraph length, em-dash density, second-person frequency) compared against the `examples/` baseline
   - BLUF heuristic check (do section openers throat-clear?)
   - Claim density (factual/numerical claims, hyperlink ratio)
   - A 0–100 weighted quality score

2. **Run the adversarial read.** Spawn a Task sub-agent with this brief:
   > Read the draft at `content-pipeline/5-drafts/{slug}.md` as a skeptical industry expert who has seen 100 AI-generated articles on this topic and is sick of them. The brand is {brand from brand-config}. The audience is {audience from brand-config}. Your job: write a critique under 400 words listing the 5 weakest things about this draft. Be specific — point at sentences, sections, and structural choices, not vague impressions. Include 1 thing that genuinely works (so you stay calibrated, not contrarian for its own sake). Do NOT rewrite, suggest fixes, or be polite.
   
   The agent's output is the adversarial review. Save it to `content-pipeline/quality-checks/{slug}-adversarial.md`.

3. **Combine into a single report** at `content-pipeline/quality-checks/{slug}.md` with:
   - **Verdict** at the top: `PASS` (score ≥ 75), `BORDERLINE` (60–74), `FAIL` (< 60)
   - The metrics summary (numbers, not raw data)
   - The adversarial critique
   - **Punch list** — specific fixes ordered by severity, each with file path + line reference
   - **Recommendation** — proceed to `/verify-claims`, send back to `/draft`, or hand to human editor

4. **On FAIL verdict — behavior depends on mode:**
   - **Autonomous mode (`BLOG_AGENT_AUTONOMOUS=1`)**: do NOT stop. Emit the verdict + punch list to disk and return cleanly. The orchestrator (`/blog-pipeline`) reads the verdict and dispatches a targeted-revision Agent, then re-runs this skill. The skill itself does not loop — the orchestrator owns the retry budget (default 2 passes via `BLOG_AGENT_REVISION_BUDGET`).
   - **Interactive mode**: stop the pipeline. Tell the user what failed and recommend either `/draft` regeneration or hand-editing. Don't silently advance to the next stage.

## Output

`content-pipeline/quality-checks/{slug}.md` (combined report)
`content-pipeline/quality-checks/{slug}-metrics.md` (raw metrics)
`content-pipeline/quality-checks/{slug}-adversarial.md` (adversarial read)

## Quality scoring weights

| Dimension | Weight | Pass threshold |
|---|---|---|
| Forbidden phrases (zero present) | 20 | 0 occurrences |
| Voice metrics within baseline range | 25 | All metrics within 1.5x SD of examples baseline |
| BLUF compliance | 20 | At least 80% of H2 openers pass the BLUF heuristic |
| Claim density + linkability | 15 | At least 60% of factual claims have a link or `[link]` placeholder |
| Adversarial verdict | 20 | Critique identifies fewer than 3 "weak" structural issues |

Weighted total → final score 0–100.

## When to override the verdict

The score is a heuristic. The adversarial critique is judgment-based. The editor (human) can override and proceed. The skill prints "Override the verdict by re-running the next stage manually" rather than gating hard.

## When the adversarial sub-agent says everything is fine

Be skeptical of all-praise critiques — they usually mean the agent isn't being adversarial enough. Re-run the sub-agent with a stronger brief if the critique is shorter than 200 words or has zero specific complaints.

## Why this skill exists

Without it, voice drift and AI tells get caught at the editor's review pass — which is the most expensive place to catch them. Catching them here means `/draft` gets the chance to regenerate before `/verify-claims` does expensive citation work on prose that was going to be rewritten anyway.
