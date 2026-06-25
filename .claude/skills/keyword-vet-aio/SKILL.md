---
name: keyword-vet-aio
description: Layer 3 of the keyword research pipeline. For every BID-passing keyword, detects whether Google shows an AI Overview (presence, via the Ahrefs serp-overview SERP-features array) and rejects "AIO-cannibalized" keywords where a thorough AIO leaves no click reason. The single most important defense against writing AI-traffic-dead content.
allowed-tools: Read, Write, Edit, Bash, WebFetch, mcp__ahrefs__*, Task
---

# Keyword Vet — AI Overview Cannibalization Check

> **DATA LAYER (2026-06-24).** This layer runs on the **Ahrefs MCP** (`mcp__ahrefs__*`); Semrush and DataForSEO are retired. Map every data call to the tools pinned in [`../research/references/ahrefs-mcp-cheatsheet.md`](../research/references/ahrefs-mcp-cheatsheet.md) — read it first. Params are comma-separated **strings** (not arrays); `select` + `country` are required; call `doc {tool:"serp-overview"}` (or `doc {tool:"brand-radar-ai-responses"}`) for any tool you haven't used this run. The logic below (filters, thresholds, scoring rubric, output schema) remains binding; only the data calls changed.

For every keyword that passed BID (Layer 2), check:
1. Does the SERP show an AI Overview?
2. If yes, how completely does it answer the query?
3. Is the keyword cannibalized (AIO is so thorough nobody clicks)?

The keyword-research transcript's most counter-intuitive finding: even keywords that pass classic Business / Intent / Difficulty checks can be **traffic-dead** if Google answers them at the top of the SERP. Definitional queries lose 35-77% of clicks when AIOs appear; comparison and tool queries lose much less. This layer surfaces which is which.

## Input

`/keyword-vet-aio`

Reads:
- `content-pipeline/0-keywords/keyword-ideas.csv` (after Layer 2 — must have `bid_verdict`)
- `.claude/skills/keyword-research-pipeline/references/aio-cannibalization-rubric.md` (the 0-10 scoring rubric)
- `content-pipeline/0-keywords/cache/aio-fetch/` (per-keyword AIO body cache)

## Process

1. **Filter to BID-PASS rows only.** Layer 3 doesn't run on FAIL rows — they're already excluded.

2. **For each candidate, detect AIO presence.** Call `serp-overview` (`{keyword:"<kw>", country:"US", select:"url,title,position,serp_features"}`) for the keyword. Look at the `serp_features` array in the response — AI Overview shows up under the **literal key `ai_overview`** (underscore, not hyphen). Other features in the array (`featured_snippet`, `people_also_ask`, etc.) are useful as secondary evidence but only `ai_overview` triggers the cannibalization check.

   - If `ai_overview` not in `serp_features`: `has_aio=false`, `aio_verdict=PASS` (no cannibalization risk), continue.
   - If `ai_overview` in `serp_features`: `has_aio=true`, proceed to step 3.

3. **Source-of-truth exemptions.** These keyword classes are AIO-immune by transcript principle and skip the cannibalization check:
   - `serp_intent=tool-led` — already routed to tool-opportunities, but if any tool-led keyword reaches here, mark `aio_verdict=PASS` reason `tool_led_immune`.
   - `serp_intent=commercial-investigation` AND has affiliate/comparison intent — AIOs rarely satisfy "best X for Y" because users want options, not summary.
   - `source=aio_gap` — these keywords explicitly target AI-search citations; cannibalization is the wrong frame. Mark `aio_verdict=PASS` reason `aio_gap_target`.

4. **For non-exempt AIO-present keywords, fetch the AIO body.** Try in this order (Ahrefs Brand Radar AI-responses → SERP-feature snippet → WebFetch — the migration retired the old Semrush AI Toolkit path):

   1. **`brand-radar-ai-responses`** for the keyword (Ahrefs's Brand Radar AI-citation toolkit — cheatsheet "Bonus capabilities"). It returns the actual AI-engine response body Ahrefs captured during its most recent crawl, the engine (filter to the Google AI Overview engine), the cited sources, and a freshness timestamp. This is the highest-fidelity source — use it first. (`brand-radar-cited-pages` gives the cited URLs if you need them for Layer 4's mentions signal.)
   2. **`serp-overview`** — the `serp_features` payload carries a snippet-level summary of the `ai_overview` feature. Lower fidelity than Brand Radar but always returned alongside the presence check, so use it as the second-line source when Brand Radar doesn't have a recent crawl for the keyword.
   3. **`WebFetch`** the SERP URL `https://www.google.com/search?q={url-encoded-keyword}` and extract the AIO block (parse for `<div data-ai-overview>` or similar — heuristic; will sometimes miss but the lower-tier sources are stronger anyway). This is the last-resort fallback.

   Cache successful fetches under `content-pipeline/0-keywords/cache/aio-fetch/{keyword-slug}.json` with timestamp and a `_meta.source` field set to one of `brand_radar_ai_responses`, `serp_features`, or `webfetch`. Refresh weekly. (Pre-migration cache files have Semrush `ai_toolkit_*` source shapes — treat them as stale on first read and re-fetch.)

   Optionally also use `brand-radar-cited-pages` / `brand-radar-sov-overview` for the keyword to check whether the brand or any competitor is currently cited inside the AIO body — that signal informs the redteam in Layer 4 but isn't required for the cannibalization score.

   If all three sources fail: mark `aio_verdict=UNKNOWN` reason `fetch_failed`, treat as `RISKY` for queue purposes, log to calibration file.

5. **Score AIO completeness via adversarial sub-agent.** Spawn a Task sub-agent with `model="sonnet"` and this brief:

   > You are a reader who just searched **{keyword}** on Google.
   >
   > The AI Overview at the top of the SERP says:
   >
   > """
   > {aio_body}
   > """
   >
   > Your job: rate from **0 to 10** how completely this AI Overview answers the query.
   >
   > - **10** = the AIO fully answers what I needed; clicking any link would be redundant.
   > - **7-9** = the AIO answers most of what I needed; I might click for one specific thing but not deep reading.
   > - **4-6** = the AIO gives a partial answer; I'd still click 1-2 results to get the full picture.
   > - **1-3** = the AIO is shallow / wrong / generic; I'd ignore it and click the regular results.
   > - **0** = the AIO is useless or doesn't address the query.
   >
   > Apply the rubric in {project-root}/.claude/skills/keyword-research-pipeline/references/aio-cannibalization-rubric.md as your scoring guide.
   >
   > Reply in this exact format (one line each, nothing else):
   > ```
   > SCORE: <0-10>
   > CLICK_INTENT: <yes-deep | yes-shallow | no>
   > REASONING: <one sentence — what the AIO does well or fails at, specifically>
   > ```
   >
   > Be honest. If the AIO is genuinely good, score it high — saying everything is shallow when it isn't burns the brand's writing budget on traffic-dead keywords.

6. **Apply the verdict** based on the score + intent:
   - **Score >= 8 AND `serp_intent=informational`** → `aio_verdict=FAIL_CANNIBALIZED`. The AIO is comprehensive on a query type where users won't click past it.
   - **Score 5-7** → `aio_verdict=RISKY`. The AIO partially answers; the article must offer something the AIO can't (depth, examples, opinion, walkthroughs). Stays in queue with the flag so the writer knows to differentiate.
   - **Score 0-4** → `aio_verdict=PASS`. AIO is weak; classic SERP traffic intact.
   - **Score >= 8 AND `serp_intent=commercial-investigation`** → `aio_verdict=PASS`. Commercial intent is AIO-resistant per transcript principle (users want options, not summary).

7. **Persist columns** to `keyword-ideas.csv`:
   - `has_aio` (true/false — derived from the `ai_overview` literal in `serp_features`)
   - `aio_completeness_score` (0-10 or null)
   - `aio_click_intent` (yes-deep / yes-shallow / no / null)
   - `aio_verdict` (PASS / RISKY / FAIL_CANNIBALIZED / UNKNOWN)
   - `aio_reasoning` (one-sentence agent rationale)
   - `aio_body_source` (brand_radar_ai_responses / serp_features / webfetch — informs Layer 4's confidence in the score)

8. **Print summary**:
   ```
   AIO check on N BID-PASS candidates:
     No AIO present (no ai_overview):         X
     AIO present, exempt (tool/CI/aio_gap):   X
     AIO scored 0-4 (PASS):                   X
     AIO scored 5-7 (RISKY):                  X
     AIO scored 8-10 (FAIL_CANNIBALIZED):     X
     Fetch failed (UNKNOWN, treated RISKY):   X
     Body sources: brand_radar=X serp=Y webfetch=Z
   Top 3 cannibalized rejections:
     - <keyword> — score <n>: <reasoning>
   Top 3 risky survivors:
     - <keyword> — score <n>: <reasoning>
   ```

## Output

Updated `content-pipeline/0-keywords/keyword-ideas.csv` with AIO columns.

Cached AIO bodies under `content-pipeline/0-keywords/cache/aio-fetch/`. Each file carries `_meta.source` so the orchestrator can audit fetch-mix drift.

Calibration log at `content-pipeline/0-keywords/cache/aio-calibration.log`.

## Quality checklist

- [ ] Every BID-PASS row has `aio_verdict` populated
- [ ] At least 1 row got each of {PASS, RISKY, FAIL_CANNIBALIZED} (gate is doing real work — if all PASS, scoring is too lenient; if all FAIL, scoring is hallucinating)
- [ ] No row scored 8+ on `aio_completeness_score` was kept as PASS unless it had an exemption
- [ ] `aio_reasoning` is specific (e.g. "fully covers the definition + 3 examples"), not generic ("seems thorough")
- [ ] Cache files written for fetched AIOs; `_meta.source` populated
- [ ] AIO presence detection used the `ai_overview` literal in `serp-overview`'s `serp_features`

## Why this is the most important new layer

The keyword-research transcript: top-ranking pages with AIOs lost 35% of clicks; some pages lost 77% from peak to trough. Existing keyword research methodology (volume + difficulty + brand fit) doesn't see this — a keyword can have great metrics on paper and produce zero traffic in practice. Layer 3 is the only check that sees AIO cannibalization, and it's the difference between an autonomous pipeline that produces dead content and one that produces traffic-relevant content.

## When AIO appears mid-pipeline (vs static at write-time)

AIO presence drifts. A query without an AIO today may have one in 6 months. The orchestrator runs Layer 3 weekly via the keyword-research-pipeline cadence, so the queue gets re-vetted regularly. Articles already published don't get re-vetted (they're in `8-publish/`); the update pipeline runs its own AIO check via `/update-topic-gaps`.

## Calibration

The 0-10 scoring is the most subjective layer in the pipeline. Initial calibration:

1. Run on 20 known queries (see `aio-cannibalization-rubric.md` for canonical examples).
2. Spot-check the verdicts against your own judgment as the editor.
3. If the scorer is over-rating (everything 8+) → strengthen the contrarian language in the brief and re-run.
4. If under-rating (everything 4-) → relax (rare; AIOs are getting better not worse).

After calibration, the discipline check (Layer 4 redteam questioning AIO classifications) is the ongoing safety net.

## Adversarial sub-agent: why Sonnet not Opus

Per project memory ("Claude-in-Chrome work always runs on Sonnet 4.6") and the model-routing principle: scoring an AIO body is high-throughput, low-reasoning judgment. Sonnet is fast and accurate enough; Opus is wasted spend across 50-100 keyword scorings per pipeline run. The brief is structured (rubric + format), which Sonnet handles cleanly.

## Ahrefs API units notes

- `serp-overview` is the most-called tool here — once per BID-PASS keyword. With ~50-100 candidates per run, this is the heaviest API consumer in Layer 3.
- `brand-radar-ai-responses` is the fidelity-leading source for AIO bodies — its call frequency is bounded by the non-exempt-AIO subset (typically ~30-60 keywords per run after exemptions).
- `brand-radar-cited-pages` / `brand-radar-sov-overview` are optional; only call when Layer 4 will use the mentions signal.
- WebFetch fallback bypasses Ahrefs units but is slower and parses inconsistently. Last resort.

If the orchestrator detects units pressure (Ahrefs returns 429), pause Layer 3 mid-run, persist progress to `keyword-ideas.csv`, exit with code 75 (signal: rate-limited, retry after cool-down). The orchestrator handles the retry on next cron cycle.

> **Note on presence-only posture.** The orchestrator's current default for Layer 3 is *presence-only* AIO detection via `serp-overview`'s `serp_features`. The Brand Radar body-fetch + adversarial-scoring path above is the full cannibalization check, preserved from the pre-migration design; it is now genuinely sourceable on Ahrefs (Brand Radar exists where Semrush AI Toolkit / DataForSEO did not). Run the full path when Brand Radar coverage is available; degrade gracefully to presence-only (treat `has_aio=true` non-exempt rows as `RISKY`) when it isn't, rather than blocking.

**No Semrush / DataForSEO fallbacks.** `mcp__semrush__ai-toolkit-*` and the DataForSEO `ai_overview` item are retired; a Semrush or DataForSEO call from this skill is a bug, not a recovery path.
