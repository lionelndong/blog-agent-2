# Heartbeat handoff — how-to-choose-an-nsfw-ai-companion (PLE-2308)

**Date:** 2026-06-15 ~14:36Z
**This heartbeat run:** `b1d578fc-0d9b-435e-b1a6-bb3e630ed2c4`
**Issue:** PLE-2308 — "SEO Publishing Pipeline — 5 posts/week" (recurring)

## TL;DR — article is LIVE; do NOT republish

`how-to-choose-an-nsfw-ai-companion` is **published and verified live**:
- URL: https://pleasur.ai/blog/how-to-choose-an-nsfw-ai-companion — HTTP 200, H1 correct (`auto_publish_check.py` OK).
- Strapi id 1395; committed to `main` (cce9398 format package, b676cbd publish live).
- Published by an **earlier PLE-2308 heartbeat** (pipeline_run_id `767b2935-3ca5-41ac-bee4-627daf4dd5f6`, 09:30→14:20Z), quality 86.2 BORDERLINE-no-CRITICAL, 8 visuals + 2 tables.

## What happened (overlapping heartbeats)

Two heartbeats of the **same recurring issue PLE-2308** ran concurrently in the **same shared working dir**:
- Earlier run `767b2935` (09:30→14:20Z): took this slug research→publish, published live at 14:20Z.
- This run `b1d578fc` (started ~13:06Z): woke on a `/blog-pipeline "how to choose an nsfw ai companion"` invocation, saw only 4/11 stages on disk (pre-publish snapshot), and re-ran the pipeline outline→preview before discovering the earlier run had already published.

**Coordination gap to fix:** a long-running recurring pipeline issue can have overlapping heartbeats that both grab the same queue slug. Consider a per-slug lock (e.g. `.runs/<slug>.lock`) or an early "already-published?" check (audit log / Strapi) at the top of `/blog-pipeline` before re-running stages.

## This run's independent result (redundant but clean)

Re-ran and passed every gate independently: research-adversarial PASS, outline-adversarial PASS (1 revision), product-mentions, draft, **quality 86.2 BORDERLINE-no-CRITICAL** (publishable: ≥85, no CRITICAL), verify-claims 8/8 cited, visuals-adversarial PASS (reached **9 visuals** vs the live 8), preview rendered. Did **not** run format-for-publish (would double-publish / overwrite live).

Delta vs live: this run added one extra Crit-8 concept diagram (9 vs 8 visuals) + minor prose polish. **Not worth churning a just-published article** — leave the live version as-is.

## Real tooling fix made this run (apply if wanted)

`quality_check.py` beat-spec parser bug: it failed to parse the dossier's **numbered** must-cover list and the **bolded** `**Target word count:** 2,400` line, silently under-scoring depth (0.6 fallback) + consensus (10/20 neutral) on every spec-compliant dossier. Fixed (format-parsing only; no threshold/weight change). The working-tree edit is in `.claude/skills/quality-check/scripts/quality_check.py`; a standalone patch is saved at `.runs/quality_check_beatspec_parser_fix-20260615.patch` in case the tree edit gets reverted by a concurrent run.

## Next heartbeat — close the loop

1. With fresh auth, confirm the earlier heartbeat already posted PLE-2308's deliverable comment for this slug. If not, post it: slug live, URL above, verdict BORDERLINE-no-CRITICAL, score 86.
2. Verify/commit the `quality_check.py` parser fix deliberately (scoped `git add` of just that file) so it isn't lost or swept into an unrelated commit.
3. Flag the overlapping-heartbeat coordination gap above on the issue.

**Why this run couldn't post it:** the run JWT expired (~14:13Z) mid-pipeline after ~1.5h; all `/api` calls returned 401. Not a content failure.

## Audit

Row appended to `content-pipeline/audit/auto-blog-log.csv` (verdict `COLLISION_NO_DOUBLE_PUBLISH`, action `halted_at_publish_already_live_concurrent_run`).
