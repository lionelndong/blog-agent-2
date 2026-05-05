# Semrush migration — progress log

Tracking the Ahrefs → Semrush migration described in `~/.claude/plans/i-need-you-to-dreamy-lecun.md`. Resume from the **In progress** section in a fresh session.

## Done (verified on disk)

### Phase 1 — Configuration cutover
- [x] `.mcp.json` — single Semrush HTTP MCP entry at `https://mcp.semrush.com/v1/mcp` (verify exact URL on first OAuth)
- [x] `CLAUDE.md` — Ahrefs MCP section replaced with Semrush MCP + ContentShake AI sections; pipeline list updated to include `/topic-discovery`, `/keyword-question-mining`, `/optimize-content` (Semrush ContentShake)
- [x] `README.md` — title now "Powered by Semrush"; quick-start references SEMRUSH_API_KEY_BLOG_AGENT; pipeline stage table updated

### Phase 7 — Cache + script hygiene
- [x] `scripts/_ahrefs_signals.json` → moved to `scripts/_archive/_ahrefs_signals.json`
- [x] `scripts/blog_triage.py` — docstring marked LEGACY, `SIGNALS` path updated to `_archive/`
- [x] Wiped stale caches: `cache/competitors.json`, `cache/competitor-keywords-raw.json`, `cache/brand-dr.json`, `cache/brand-radar-quota.log`
- [x] `auto_keyword_selector.py` — confirmed no Ahrefs-specific column reads; no changes needed

### Phase 2 — Authoritative reference docs
- [x] `.claude/skills/research/references/_archive/ahrefs-mcp-cheatsheet.md` (archived)
- [x] `.claude/skills/research/references/semrush-mcp-cheatsheet.md` (new — Keyword Magic, Topic Research, .Trends, KSB, multi-mode Keyword Gap, intent classifier)
- [x] `.claude/skills/keyword-research-pipeline/references/semrush-mcp-tool-inventory.md` (new — placeholder for live discovery)
- [x] `.claude/skills/keyword-research-pipeline/references/semrush-metric-translation.md` (new — DR→AS, KD→KD%, "do not transplant" rules, all threshold deltas)
- [x] `.claude/skills/keyword-research-pipeline/references/bid-method.md` (rewritten — Semrush intent classifier as primary BID-I signal, AS recalibration)
- [x] `.claude/skills/keyword-research-pipeline/references/aio-cannibalization-rubric.md` (header note + AIO source order updated; `ahrefs keyword cannibalization checker` example → `semrush keyword cannibalization checker`)

### Phase 3 (in progress)
- [x] `.claude/skills/research/SKILL.md` — frontmatter swapped (`mcp__semrush__*`), Semrush playbook in Step 3, Topic Research integration, content-gap signals, `_meta.source` string, quality checklist updates

## In progress / remaining

The plan file `~/.claude/plans/i-need-you-to-dreamy-lecun.md` has the full task list; the todo list at session-end was:

### Phase 3 — skill-by-skill swap (remaining)
- [x] `content-gap-analysis/SKILL.md` — Phase 4b multi-mode Keyword Gap (5 modes: missing / weak / unique / common / strong); every row tagged with `gap_mode`; `strong`-mode rows routed to `cache/strong-positions.csv` (NOT writing pool); `cluster_id` + `intents` columns; KD% recalibrated to ≤ 70 default / ≤ 85 relaxed; frontmatter enumerates `mcp__semrush__organic-competitors`, `keyword-gap`, `keyword-magic-{broad,phrase,related,exact}`, `keyword-overview`
- [x] `keyword-vet-bid/SKILL.md` — Phase 4e Semrush intent classifier (`intents` array from `mcp__semrush__keyword-overview`) as primary BID-I signal, URL-pattern derivation demoted to fallback; DR→AS gate recalibrated (`brand_AS + 12` default, `+8` tighten, `+20` relax); `weak_link_count` rule tightened to `AS < brand_AS + 4`; KD% defaults baked in; cache file rename `brand-dr.json` → `brand-as.json`; calibration thresholds + reason codes (`as_gap_too_wide`) updated; frontmatter enumerates `mcp__semrush__keyword-overview`, `serp-overview`, `serp-results`, `domain-overview`
- [x] `keyword-vet-aio/SKILL.md` — frontmatter swapped to `mcp__semrush__serp-overview` / `serp-results` / `ai-toolkit-response` / `ai-toolkit-mentions`; AIO body fetch order set to AI Toolkit AI Response → Semrush SERP Features → WebFetch fallback; SERP feature literal pinned to `ai_overview` (Semrush, underscore) with explicit warning that the Ahrefs `ai-overview` literal will silently miss matches; new `aio_body_source` column; cache files carry `_meta.source ∈ {ai_toolkit_response, serp_features, webfetch}`; pre-migration `brand_radar_*` cache files marked stale
- [x] `keyword-redteam/SKILL.md` — DR→AS, KD→KD% updated in (c) Hidden difficulty; new paragraph instructs agent to reason over Semrush `intents` array + KSB `cluster_id` across (a)-(d)
- [x] `keyword-prioritization/SKILL.md` — Ryan-quote rephrased (no longer Ahrefs-specific); Phase 4f added: `gap_mode` boosts (+0.5 weak / +0.7 unique / -0.3 common / route strong→`cache/strong-positions.csv`), `aio_sov_competitor_top` tie-breaker, `cluster_authority_gap` +0.5 — links to `semrush-metric-translation.md`
- [x] `keyword-research-pipeline/SKILL.md` — orchestrator briefs fully swapped Ahrefs→Semrush; Layer 0 (`/topic-discovery`) and Layer 1d (`/keyword-question-mining`) inserted into the chain (0 → 1a → 1b → 1c → 1d → 2 → 3 → 4 → 5); stage briefs reference the correct Semrush MCP tools (`organic-competitors`, `keyword-gap`, `keyword-magic-*`, `keyword-overview`, `serp-overview`, `serp-results`, `domain-overview`, `ai-toolkit-response`, `ai-toolkit-mentions`, `ai-toolkit-prompts`, `topic-research`, `trends-overview`, `keyword-magic-questions`); failure-handling section covers Layer 0/1d cases (continue) and Layer 1d rate-limit (exit 75); cost notes updated for Semrush quota with Layer 0/1d add-on; reporting summary surfaces gap_mode mix, aio_body_source mix, and intents-vs-URL signal share
- [x] `seed-modifier-prompt/SKILL.md` — three Ahrefs strings → Semrush Keyword Magic Tool / Power 1 MCP / Semrush quota; new "Topic-graph enrichment" section pre-feeds top 5 KSB clusters from `topic-graph.json` with brand-config-only fallback when absent
- [x] `blog-pipeline/SKILL.md` — Stage 1 brief uses Semrush MCP + Topic Research; Stage 7 brief uses internal-Semrush metrics; Stage 8 brief simplified (Chrome dependency removed; ContentShake quota writes a stub and pipeline continues); Process line + reporting summary updated
- [x] `auto-blog-loop/SKILL.md` + `references/runbook.md` — failure-mode prose updated (Semrush MCP auth expired; Semrush AI Toolkit / API quota; Semrush in cool-down list); sanity-check command swapped to `mcp__semrush__domain-overview`
- [x] `update-topic-gaps/SKILL.md` — frontmatter swap (`mcp__semrush__*`), SERP refresh via `mcp__semrush__serp-results`, ADDED Topic Research idea-cluster delta comparison via `mcp__semrush__topic-research`; new `gap_source: serp | topic-graph | both` tagging in audit output + quality checklist
- [x] `verify-claims/SKILL.md` — Ahrefs blog post example replaced with generic third-party-tool / Search Engine Land citation example
- [x] `generate-screenshot/SKILL.md` + `generate-visuals/SKILL.md` — references to `ahrefs-products-catalog.md` repointed to `_archive/ahrefs-products-catalog.md` and reframed as "legacy non-Pleasur reference" / "legacy URL-pattern catalog reference"; brand-config product URLs now stated as the primary source for the Pleasur.AI deployment (catalog is fallback shape hint only). `generate-visuals` reference path adjusted to cross-skill `../generate-screenshot/references/_archive/...` since the catalog physically lives under `generate-screenshot/`.
- [x] Move `.claude/skills/generate-screenshot/references/ahrefs-products-catalog.md` → `_archive/` sibling

### Phase 4 — keyword-research enhancements (new skills)
- [x] **NEW**: `.claude/skills/topic-discovery/SKILL.md` (Layer 0 — Semrush Topic Research + .Trends; outputs `topic-graph.json` + `trends.md`; idempotent on brand-config hash via SHA-256 mirror of seed-modifier-prompt; degraded-mode failure handling never blocks pipeline; allowed-tools `Read, Write, Bash, mcp__semrush__topic-research, mcp__semrush__trends-overview`)
- [x] **NEW**: `.claude/skills/keyword-question-mining/SKILL.md` (Layer 1d — Keyword Magic Questions filter per surviving seed + PAA mining from `serp_features.people_also_ask` for top-30 by current priority; appends rows with `source=question_mining`, new `question_subtype` column ∈ `paa|km_question|both`; merges to `source=both` on overlap; cap 100 rows/run with PAA-tier-wins-tie dedupe; allowed-tools `Read, Write, Edit, Bash, mcp__semrush__keyword-magic-questions, mcp__semrush__serp-results`)

### Phase 5 — heavy rewrite
- [x] `.claude/skills/keyword-aio-gap/SKILL.md` — full rewrite on Semrush AI Toolkit. Allowed-tools dropped every `mcp__ahrefs__brand-radar-*`; replaced with `mcp__semrush__ai-toolkit-prompts`, `mcp__semrush__ai-toolkit-mentions`, `mcp__semrush__ai-toolkit-response`, `mcp__semrush__keyword-overview`, `mcp__semrush__organic-competitors`. Prompt-centric process: read brand+competitors → generate prompt panel from `keyword-ideas.csv` candidates (1–3 phrasings each, cap 200 prompts/run) → register via hash-keyed idempotent call → pull mentions per engine → compute gap → enrich with keyword-overview → append rows. **New CSV columns**: `aio_engines` (comma-list of engines that cited a competitor), `competitor_aio_mention`, `competitor_cited_url`, `aio_sov_competitor_top`. 429 → exit 75 (orchestrator retry on next cron). Fallback proxy when SoV missing: `1/rank` per engine, max across engines.

### Phase 6 — heavy rewrite
- [x] `.claude/skills/optimize-content/SKILL.md` — full rewrite on ContentShake AI. Dropped: `mcp__Claude_in_Chrome__*` from allowed-tools, `Task` (Sonnet sub-agent for browser driving), `window.__pleasurEditor` TipTap injection, port-8766 CORS server, base64 splitting + Windows CRLF handling, 50-doc/month cap, `document-budget.md` enforcement. New flow: Bash → `contentshake_optimize.py` (Doppler-loaded key) → JSON parse → judgment-rewrite in brand voice (Opus-side step preserved) → re-score → re-quality-check. **Iteration loop**: max 5; stops on (`seo ≥ 8 AND quality ≥ 8`) → WIN, OR voice-drift > 8 pts → ROLLBACK, OR < 0.5pt lift twice in a row → PLATEAU, OR 5 cap → CAPPED. **Voice-drift safety net unchanged** (the user's explicit call-out). API-call budget tracked via `BLOG_AGENT_CONTENTSHAKE_MONTHLY_CAP` (default 100): warn-at-80% / refuse-at-100%, counting API calls not docs. Missing key → stub report at `content-pipeline/optimization/{slug}.md`, exit 0 cleanly (matches `/research` ↔ missing-OpenRouter convention).
- [x] **NEW**: `.claude/skills/optimize-content/scripts/contentshake_optimize.py`. PEP 8, type-annotated. Mirrors `openrouter_research.py` shape: stdlib-only urllib, argparse-driven, JSON-to-stdout, stderr progress lines. Args: `--slug`, `--keyword`, `--action {optimize, score}`. Env precedence: `SEMRUSH_API_KEY_CONTENTSHAKE` (preferred sub-key) → `SEMRUSH_API_KEY_BLOG_AGENT` (primary fallback). Retry/backoff on 429 + 5xx (5 attempts, exponential base 1s). 429 final attempt → exit 75. 401 → PermissionError. Endpoint base configurable via `SEMRUSH_CONTENTSHAKE_API_BASE` (default `https://api.semrush.com/contentshake/v1`). Stable response envelope: `{seo_score, quality_score, recommended_terms[], missing_topics[], readability, voice_signals, competitor_topics_missing[], _meta}`.
- [x] **NEW**: `.claude/skills/draft-score/SKILL.md` — lightweight self-check the `/draft` stage can call before saving. Calls `contentshake_optimize.py --action=score`. Soft-fail when key is missing: writes stub at `content-pipeline/optimization/{slug}-draft-score.json`, prints note, exits 0 (mirrors how `/research` handles missing OpenRouter). Verdict heuristic: `seo ≥ 8 AND quality ≥ 8` → `WIN_LIKELY`, `seo ≥ 7 AND quality ≥ 7` → `BORDERLINE`, else → `NEEDS_OPTIMIZE`. Counts as 1 unit against the same `BLOG_AGENT_CONTENTSHAKE_MONTHLY_CAP` budget.
- [x] `.claude/skills/blog-pipeline/SKILL.md` Stage 8 brief simplified — no Chrome MCP gating, no `list_connected_browsers` preflight; single skip-condition note covers both missing-key AND quota-exhausted paths. Final-report status line lists verdict (`WIN|ROLLBACK|PLATEAU|CAPPED|SKIPPED`).

## How to resume

1. Connect the Semrush MCP and run the discovery prompt — paste result into `.claude/skills/keyword-research-pipeline/references/semrush-mcp-tool-inventory.md`. This is the source of truth for actual `mcp__semrush__*` tool names; everything else uses placeholder names that may need correction.
2. Walk down the **In progress / remaining** list above in order. Each `SKILL.md` edit is mechanical — replace `mcp__ahrefs__*` with the corresponding `mcp__semrush__*` tool from the inventory, swap metric names per `semrush-metric-translation.md`, update calibration thresholds.
3. The two heavy rewrites (Phase 5: keyword-aio-gap, Phase 6: optimize-content) are best done as full `Write` operations — the structure changes substantially.
4. Phase 4 (new skills) should follow Ryan Law's existing skill conventions — same SKILL.md frontmatter format, same input/process/output structure as the current skills, same idempotency rules (brand-config hash check for Layer 0).
5. After all SKILL.md edits, do the calibration smoke tests in Phase 8 of the plan.

## Risk reminders (do not skip)

- **Recalibrate, don't transplant.** Semrush KD% is materially stricter than Ahrefs KD; AS tends ~5-10pts lower than DR. Threshold deltas are documented in `semrush-metric-translation.md`. Do not copy Ahrefs thresholds verbatim.
- **`mcp__ahrefs__*` is now a bug.** If you see one in a migrated skill, it's a leftover. Don't add silent Ahrefs fallbacks — Ahrefs is retired.
- **Reversibility is `git revert`** of these changes. The `_archive/` directories preserve the prior cheatsheet/catalog for reference.
