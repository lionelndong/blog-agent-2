# Session state — 2026-05-03 — Pleasur.AI blog pipeline build

> Drop this into a fresh Claude Code session to resume cleanly. Last update: 2026-05-03.

## What this project is

Replication of Ryan Law's Ahrefs blog content engineering pipeline (per [his blog post](https://ahrefs.com/blog/how-i-do-content-engineering-with-claude-code/)) for **Pleasur.AI**, an AI adult companion platform. The pipeline turns a keyword into a publish-ready blog article with brand-voice protection AND high SEO score.

**Project root:** `C:\Users\ndong\Downloads\blog-agent\`

**Quality bar:** Articles must read like an Ahrefs-style human-written guide AND score ≥ 90 on Ahrefs Content Helper. Both matter; voice protection is enforced via `/quality-check` gate.

## Build status: COMPLETE for all 8 originally-planned phases + 2 extensions

All 23 skills built, 1 added (`/quality-check`), 1 added (`/optimize-content`). Skills live under `.claude/skills/`. Pipeline outputs land under `content-pipeline/`. See [README.md](../../README.md) and [CLAUDE.md](../../CLAUDE.md) for full pipeline.

**Key skills:**
- Creation: `content-gap-analysis`, `keyword-prioritization`, `research`, `brand-reference`, `outline`, `product-mentions`, `draft`, `quality-check`, `verify-claims`, `optimize-content`, `generate-screenshot`, `preview`, `format-for-publish`, `blog-pipeline`
- Update: `extract-content`, `update-guidance`, `update-claims`, `update-product-mentions`, `update-topic-gaps`, `update-draft`, `update-preview`, `update-pipeline`

## Critical config files

- [brand-config.md](../../brand-config.md) — Pleasur.AI brand voice + product list with `status: live | coming-soon | roadmap`. Currently: AI Companion Creator (live), AI Image Generation (live), Voice Replies (coming-soon), Phone Call (coming-soon), AI Video Generation (roadmap).
- [.mcp.json](../../.mcp.json) — Ahrefs MCP server config
- [.claude/settings.json](../settings.json) — permissions allowlist
- [examples/](../../examples/) — 5 Ahrefs articles loaded for voice anchoring

## Integrations wired

1. **Ahrefs MCP** — authenticated, working. ~75K of 100K monthly units left.
2. **OpenRouter** for Perplexity deep research — `OPENROUTER_API_KEY_BLOG_AGENT` env var (loaded via Doppler). Default model: `perplexity/sonar-reasoning-pro`. Fallback: `openai/o4-mini`. Script: [.claude/skills/research/scripts/openrouter_research.py](../skills/research/scripts/openrouter_research.py).
3. **Claude in Chrome MCP** — connected to user's Windows browser (deviceId `e42d94da-bc84-4eb6-a209-5e83355212ab`).
4. **Strapi** — formatter wired but no direct API publish yet (Doppler creds available, not yet configured). Script: [.claude/skills/format-for-publish/scripts/format_for_strapi.py](../skills/format-for-publish/scripts/format_for_strapi.py).
5. **Whiteboard UI** — local web dashboard at http://localhost:8765 (run `python scripts/whiteboard.py`).

## Smoke test status — `ai girlfriend` keyword

Ran the full pipeline including Ahrefs Content Helper optimization. Document ID 232113 in Ahrefs (reused, not new — saved budget).

**Confirmed results (iteration 1):**
- Content Helper score: **59 → 65** (+6 confirmed via JS injection + re-score)
- Quality-check score: 60 → 57 (within 8-pt voice tolerance, no drift warning)
- Forbidden phrases: 1 ("leverage" x2) → 0
- BLUF compliance: 14/14 → 17/17 sections pass
- Word count: 2,950 → 3,400

**Iteration 2 status:** Edits applied locally to [content-pipeline/6-drafts-cited/ai-girlfriend.md](../../content-pipeline/6-drafts-cited/ai-girlfriend.md). Push to Ahrefs failed due to CRLF/encoding issue in base64-via-JS-string approach. Predicted lift if pushed: 65 → 74-80.

**Topic-level lift after iteration 1:**
- Emotional and Romantic Interaction: 5 → 34 (+29) — biggest win
- UX & Accessibility: 69 → 80 (+11)
- Companionship: 87 → 88 (+1)
- Customization: 85 → 85
- Privacy: 47 → 47 (terms added but density too low — needs more)
- User Reviews: 81 → 81

**Document budget:** 10 / 51 used this month (Lite plan). Resets **May 10, 2026** (NOT 1st of month — Ahrefs billing cycle).

## What broke and why

The iteration 2 push failed with a JS `SyntaxError` because the base64 string (read from a file Python wrote with `print()`) likely contained CRLF or trailing chars when stuffed inline into a JS string literal. Two clean fixes documented:

1. **Strip CR/LF** when generating base64: `b64 = b64.replace('\r','').replace('\n','')`
2. **Localhost CORS server** — [scripts/serve_optimization.py](../../scripts/serve_optimization.py) is written but needs user permission to run. Path: JS in Ahrefs fetches `http://127.0.0.1:8766/draft.html` directly. Cleaner than 30KB b64 in JS source.

## What's NOT done (next session priorities)

1. **Push iteration 2 + iterate to 90.** The local edits are ready. Either fix the b64 encoding OR get user to approve `python scripts/serve_optimization.py`. Then run the loop documented in [.claude/skills/optimize-content/SKILL.md](../skills/optimize-content/SKILL.md).
2. **Use Sonnet sub-agent for browser work.** The smoke test ran ALL Chrome MCP calls on Opus 4.7 directly, burning ~3-5x the tokens. The SKILL.md documents the correct pattern (Task sub-agent with `model="sonnet"` and `subagent_type="general-purpose"`). MUST use it next time.
3. **Wire iteration loop logic into orchestrator.** [.claude/skills/optimize-content/SKILL.md](../skills/optimize-content/SKILL.md) Phase C describes 5-iteration loop with stopping conditions (score ≥ 90, voice drift > 8pts, < 2pt lift × 2). Skill instructions are written; need to actually exercise on a fresh keyword.

## How to resume

In a fresh Claude Code session:

```
cd C:\Users\ndong\Downloads\blog-agent
doppler run -- claude
```

Then in chat:
> Read .claude/sessions/2026-05-03-blog-pipeline-build.md for full state. Then continue: push iteration 2 of the ai-girlfriend optimization to Ahrefs and run the iteration loop until score ≥ 90 OR voice drift > 8pts. Use a Sonnet 4.6 sub-agent for all Claude in Chrome MCP work (token efficiency). The local cited draft already has both iterations of edits applied.

If running fresh on a different keyword:

```
/blog-pipeline <keyword> --context "..."
```

The orchestrator now includes `/quality-check` and `/optimize-content` stages.

## Important user feedback (durable preferences)

1. **Ryan's method matters** — anything that improves on his pipeline (Perplexity deep research, JS injection of Content Helper, etc.) is welcome AS LONG AS the editorial principles (BLUF, MECE, voice anchoring in `examples/`) hold.
2. **Voice + score both required.** Voice intact AND score ≥ 90. Voice-drift gate (8pt) is hard. The user said "fully autonomous, no human in the loop" — but the voice gate is the safety net.
3. **Strapi, not WordPress.** Already done — `/format-for-publish` outputs Strapi JSON + paste-or-publish README.
4. **Token efficiency** — browser/navigation work goes to Sonnet via Task sub-agent. Brand-voice rewriting stays on the top model.
5. **Existing Ahrefs Content Helper documents must be reused** before creating new ones. 51/month cap. Resets the 10th, not the 1st.
6. **Don't over-engineer or pad.** Article positioning is "evaluation guide for AI girlfriend platforms" — terms like "onlyfans killer", "sexy chat", "motion under your command" are off-brand and skipped per the SKILL.md judgment rules.

## Files to read first in a new session

1. This file (you're reading it)
2. [CLAUDE.md](../../CLAUDE.md) — pipeline philosophy + folder conventions
3. [brand-config.md](../../brand-config.md) — Pleasur.AI products + voice rules
4. [content-pipeline/optimization/ai-girlfriend.md](../../content-pipeline/optimization/ai-girlfriend.md) — full optimization run report
5. [.claude/skills/optimize-content/SKILL.md](../skills/optimize-content/SKILL.md) — autonomous loop architecture

That's everything you need to pick up where this session left off.
