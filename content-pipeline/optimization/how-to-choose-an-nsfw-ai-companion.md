# optimize-content — how-to-choose-an-nsfw-ai-companion

**Verdict: SKIPPED (ContentShake unavailable) + voice-polish punch list applied by hand.**

## ContentShake status

ContentShake AI was called but the API returned **HTTP 400 "query type not found"** on
both endpoints (`/articles/analyze` and `/articles/score`). This is an API-side endpoint
failure, not a quota (exit 75) or a missing key — `SEMRUSH_API_KEY_CONTENTSHAKE` is present
in env. Per the skill's fail-soft convention (Phase B step 8), the ContentShake scoring loop
is treated as SKIPPED so the pipeline continues. Raw stderr saved to
`how-to-choose-an-nsfw-ai-companion-errors.log`.

- SEO score before/after: n/a (ContentShake unreachable)
- Quality score before/after: n/a (ContentShake unreachable)
- Iterations used: 0 (no ContentShake scoring loop ran)
- Budget consumed this run: **0** (no 200 response — no slot consumed)
- Budget remaining: 100/100 (month rolled 2026-05 → 2026-06; cap default 100)

Re-run `/optimize-content how-to-choose-an-nsfw-ai-companion` once the ContentShake endpoint
is serving again to capture SEO + Quality numbers.

## Voice-polish punch list — APPLIED BY HAND (the real quality lift)

This was applied directly via Edit on `6-drafts-cited/how-to-choose-an-nsfw-ai-companion.md`,
anchored to `examples/voice/pleasur-privacy-data-guide.md` (self-disclosure honesty pattern).

| Item | Before | After | Done |
|---|---|---|---|
| Trim "explicit" crutch (<8) | 15 uses | **5 uses** (all meaningful: mainstream-refusal distinction, "explicit controls"/"explicit version" = detailed sense, "explicit 18+ confirmation" = idiomatic gate term) | ✅ |
| Reduce "X, not Y" antithesis (<~5) | ~13 body instances | **4 prose instances** (lines: intro commission, "red flag not a feature", "monthly price not annual", "worked example not a verdict") | ✅ |
| Break forward-pointing section closers (~8) | 8 sections close on "and next is X" | **~4** — dissolved/reworked closers after Crit 1, 2, 3, 4, and the privacy→age transition | ✅ |
| Procedural scorecard "test in 5 min" cells | navigational ("search the privacy policy for retention") | **action + expected outcome** for all 8 rows (e.g. say "call me Alex" → it answers unprompted; Ctrl-F policy → each term returns a concrete answer not zero hits; toggle annual→monthly → watch number jump) | ✅ |
| Crit 7 brand age-gate sentence | honesty frame silent on own brand | **added** (line 130): "Pleasur.AI is an 18+ product that gates the adult tier behind an explicit 18+ confirmation on signup, and the subscription step itself — which requires a card before any adult content unlocks — adds a second hard wall…" framed as "stated plainly rather than promised; run the same check on it" — factual, no guarantees, pulled from brand-config.md | ✅ |

## Voice-drift check (local quality_check.py, cited stage)

| | Baseline (iter-0) | Post-edit | Delta |
|---|---|---|---|
| Mechanical score | 89/100 PASS | 89/100 PASS | **0 pts** |
| "explicit" crutch flag | x16 (flagged) | gone | resolved |

Voice drift = **0 pts** — well inside the non-negotiable <8 safety net. No rollback.
The drift is net-positive in substance: the top crutch word ("explicit x16") is eliminated,
scorecard cells are now procedural, and the rhetorical-tic density is down — at identical score.

## Constraints honored

- No coming-soon products (Voice Replies / Phone Call / Video) introduced as live.
- 18+ adult framing kept on-brand — not softened or moralized.
- No made-up stats; all 14 external citations + 11 internal pleasur.ai links preserved.
- All 5 `[VISUAL:...]` placeholders preserved; both GFM tables (scorecard + sub-table) intact.
- No banned internal-tool names in prose.

## One-line summary

optimize-content: ContentShake SKIPPED (HTTP 400 endpoint), punch-list polish applied by hand,
"explicit" 15→5, antithesis ~13→4, scorecard cells procedural, Crit-7 brand age-gate added,
voice drift 0 pts, budget 0/100 consumed.
