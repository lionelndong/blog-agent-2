## Verdict: **PASS**

Slug: `what-ai-companion-apps-get-wrong` · stage: cited · gate run 2026-06-28 · revisions used: 0.

FLOORS_OK **and** Gate 2 passes (KEEP_OURS x3, KEEP_COMPETITOR x0). No revision required.

## Gate 1 — Completeness floors (FLOORS_OK, exit 0)

| Floor | Result | Detail |
|---|---|---|
| depth | PASS | 2,967 words (beat spec has no machine-parseable target; ≥ the ~1,920 self-floor) |
| consensus_coverage | PASS | all must-cover topics present (memory, repetition, drift, paywalls/coins, voice, how-to-choose) |
| citations | PASS | no naked `[link]` placeholders; 16 real hyperlinks |
| no_internal_leak | PASS | no internal tooling named in prose |
| forbidden_phrases | PASS | none |

Non-gating observations: claim density 0.15; [GAIN] marker absent in source (panel confirmed a genuine gain — see below); repetition crutches flagged ("across" x13, "can't"/"persistent"/"model"/"because" x12, "context"/"layer"/"coins" x11, "looping" x10). Routed to editor as polish, not a gate fail.

Brand-constraint spot check (all clear): 3-tier coin pricing only ($12.99/1,500 · $27.99/5,000 · $49.99/10,000), no "flat / no tokens / no hidden fees"; voice-not-video stated explicitly twice; competitor failings hedged ("widely reported"); no first-person 82% stat; 18+ framing present; no internal-stack leak; `## FAQ` with all 4 required questions present verbatim-intent.

## Gate 2 — Reviewer panel (KEEP_OURS x3 → PASSES)

- **Lens A (Competitiveness): KEEP_OURS** — beats the listicle slice on density + a memory-first causal taxonomy; modeled transparent coin meter is gain none of the winners have.
- **Lens B (Voice & readability): KEEP_OURS** — reads like a real byline (concrete open, single thesis, peer hedges); crutch words/transition tics are polish issues, not fails.
- **Lens C (Reader intent & information gain): KEEP_OURS** — real, load-bearing information gain (root-cause taxonomy + named looping failure + live-sourced coin math); FAQ serves FAQPage schema.

Full reviews in `what-ai-companion-apps-get-wrong-panel.md`.

## Punch list (editor polish — non-blocking, PASS stands)

1. **[/generate-visuals dependency]** Render the four `[VISUAL:type=screenshot]` placeholders (lines 37, 73, 103, 121) into real Pleasur.ai UI captures. All three reviewers flagged that the first-hand-walkthrough information gain is currently a promissory note; if these ship as missing/placeholder art the lived-experience edge weakens. Route: `/generate-visuals` (already typed correctly as placeholders — expected at this stage).
2. **[/draft] Repetition/refrain.** Vary the "persistent memory layer earns its keep / holds the character steady / keeps the conversation whole" refrain (lines 47/69/117) and trim §2's triple-restated context-churn mechanism (lines 41–45). Route: `/draft`.
3. **[/draft] Formulaic section-ending transitions** (lines 33/53/71/99) — break up the four near-identical baton-pass hand-offs. Route: `/draft`.
4. **[/draft] Thin VOC breadth** — the chuckmellisa five-app test is cited 4x; diversify lived-experience sourcing or lean a touch less on one author. Route: `/draft`.
5. **[/draft] §4 root-cause overreach** — soften the rhetorical "no memory means a paywall you can't justify"; pricing/voice are arguably independent of the memory root. Route: `/draft`.

None of the above blocks publish. Verdict stands: **PASS**.
