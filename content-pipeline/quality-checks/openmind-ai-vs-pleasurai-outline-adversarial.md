# Outline Adversarial — openmind-ai-vs-pleasurai (Pass 1)

## Verdict: **PASS**

Pass 1 of 2 (revision budget BLOG_AGENT_OUTLINE_REVISION_BUDGET=1).

No CRITICAL findings — the five gate-enforced claim guardrails (a)–(e) from
`0-context/openmind-ai-vs-pleasurai.md` are all satisfied. HIGH findings are
visual over-density / redundancy; fixing them pre-draft is worth doing but does
not block the spine.

## Findings

### CRITICAL

- None. Guardrail checks (a)–(e) all clear:
  - (a) 82% appears only as an attributed MariaVibe figure + URL (lines 19, 34,
    81, table cell 109, FAQ 159); line 83 explicitly bars "validated"/methodology.
  - (b) OpenMind duration framed self-reported (lines 21, 67, 113, 162, 168); no
    "exited beta" / no "1 year" as fact; maturity cell says "Newer entrant."
  - (c) Pleasur.ai pricing = true coin-metered 3 tiers (Starter $12.99 / Standard
    $27.99 / Ultimate $49.99, unlimited text + coin-metered media; lines 22, 111,
    125); no flat-fee / no-tokens / video-call claims.
  - (d) Lead is the evidence-asymmetry angle (third-party vs self-reported, line
    34), not the raw 82%; H2-4 [GAIN] makes asymmetry the decisive axis.
  - (e) "OpenMind AI" disambiguated early (line 38) — names OpenMind.design,
    rules out Google DeepMind / robotics.

### HIGH

- [Visual sanity check, lines 242–243] Density mis-justified. 11 visuals (5
  generated images + 4 external clips + chart + screenshot + table) sized against
  a 2,840 "prose tally" that conflicts with the ~2,640/~2,600 word estimates
  elsewhere. The reference SERP (research line 104) runs 2–3 images + tables;
  this is ~2x the modal comparison page. Density target is a guideline, not a
  quota.
- [Visuals, multiple] At least three decorative/redundant per the 9-step rule:
  (1) Intro "vs poster" (line 40) restates the thesis as a banner — proves
  nothing, fails step 9. (2) H2-1 generic memory-flow diagram (line 55) overlaps
  the stronger H2-2 CFS retrieve→subtract→reply diagram (line 72) — two abstract
  memory-pipeline graphics in ~700 words. (3) H2-3 has BOTH a chart (line 88) and
  an external clip of the MariaVibe table (line 89) showing the same 82%/33% — the
  "don't chart AND table the same data" violation. Cutting these three lands the
  article at a defensible ~8 visuals.

### MEDIUM

- [H2-4 line 93 vs H2-6 line 136] Partial overlap. Both resolve "which to choose"
  and end on the same OpenMind-free-tier-vs-Pleasur-breadth trade-off (lines 100,
  143). Distinguishable (table/evidence vs persona-routing) but the draft will
  repeat itself unless H2-4 stays strictly evidence/architecture and H2-6 stays
  strictly persona-routing.
- [Table cell, line 111] "Free $0 (unlimited messages, 50/hour cap)" is internally
  contradictory verbatim-from-review phrasing. Render as "50 messages/hour on the
  free tier" so a cited cell doesn't read as self-contradictory.

### LOW

- [Intro, line 32] Problem-Agitate-Solution arc is thin — the hook is contrarian,
  not a reader pain; H2-1 jumps to definition without agitating the "every app
  claims great memory, who do you believe" tension. Acceptable for a GEO page;
  the asymmetry spine carries the argument.

## What Works

- [Table cells 109–113, H2-4 [GAIN] line 97, all H2 BLUFs] Attribution discipline
  is exemplary and is the actual product: every load-bearing claim is tagged by
  *who reported it* at the outline level, the [GAIN] is a real whitespace play
  confirmed by deep research (research line 58), and every H2 stub opens
  answer-first with no throat-clearing. A structure built for AI-engine citation —
  the stated goal.

## Recommendation

- Verdict is PASS: advance to stage 4 (/product-mentions). Optionally trim the
  three flagged visuals (intro poster, duplicate memory diagram, chart-vs-table
  double-up) and fix the line-111 cell phrasing during /product-mentions or
  /draft — neither requires an outline revision pass.
