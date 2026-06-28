# Quality Check — character-ai-no-filter-2026 (final re-score)

## Verdict: **PASS** — final score 86/100

Clears the autonomous publish bar (≥85). No CRITICAL findings, no mechanical dimension below its 60% floor, and the adversarial read keeps our draft over the current #1.

- **Final = 0.6 × mechanical (81) + 0.4 × judgment (93) = 86.0**
- Word count **3,119** — within the beat-spec band (2,700–3,100 target; ≤~3,200 acceptable). The surgical Candy AI + Joyland AI thickening added dossier-confirmed detail with **no invented price** (both still rendered "price not publicly listed").

## Mechanical metrics (81/100)

| Dimension | Score | Weight | Floor (60%) |
|---|---|---|---|
| depth_vs_benchmark | 15.0 | 25 | ok |
| consensus_coverage | 12.0 | 20 | ok |
| evidence | 14.3 | 15 | ok |
| ai_tells | 25.0 | 25 | ok |
| structure | 15.0 | 15 | ok |

**Known false negatives confirmed (NOT real deficits):**
- "NO BEAT SPEC found" — beat spec IS present in the dossier (line 187). Script's regex misses the header.
- "MISSING: Answer-first opening" — present, draft lines 5–6 (names Pleasur.ai in the first two sentences).
- "MISSING: 6-platform ranked rundown" — present, draft lines 54–106 (all six platforms with per-tool features + pricing).

The consensus_coverage 12/20 is an artifact of those two false negatives; true consensus coverage is complete.

Other mechanical notes (non-blocking): repetition counts ("platform" ×23, "adult" ×19) are topic-inherent for a comparison of adult-AI platforms, not crutch tics; claim density 0.17; 20 hyperlinks; 4 `[link]` placeholders = **expected draft state**, resolved by /verify-claims.

## HARD compliance re-verification — all hold

- **No own-voice absolutism** — "no rules" / "anything goes" appear only inside scare-quotes as the framing being rejected (lines 17, 39, 92). Pass.
- **No fabricated stats** — the dropped "20M+ DAU / majority cite filter" line stays out.
- **Price-as-fact discipline** — hard numbers only for Pleasur.ai ($12.99/$27.99/$49.99), CrushOn ($0/$4.90/$7.90), DreamGen ($7.83/$19.35/$48.30). Candy/Joyland/Janitor all hedged "price not publicly listed." Candy/Joyland additions introduced no new price. Pass.
- **No coming-soon products** — no Voice Replies / Phone Call / AI Video. Pass.
- **No internal vendor names** — no Strapi/Doppler/Semrush in reader copy. Pass.
- **Correct internal link** — `/blog/character-ai-alternative` (no `-2026`) at all 7 occurrences. Pass.
- **AIO structure** — answer-first opener + "why the filter" explainer + comparison table + 5-Q FAQ all present. Pass.

## Judgment read (93/100, 40% of final)

On voice (read against `examples/voice/`): second-person, evidence-led, opinionated thesis, honest trade-offs (CrushOn credit caps, Janitor's API-key homework, Joyland's "adult-leaning not uncensored," Candy's unlistable price). The verdict-formula tic is largely varied across sections. The intro + "no-filter mode?" section is genuinely strong — concrete mod-APK risk frame, compliant terminology split, on-voice payoff. Information gain is real and not on page 1: the only single side-by-side comparison table across the six platforms, plus a compliant first-hand-framed filter explainer.

## Adversarial read — keeps OUR draft

Side-by-side verdict: keeps this draft over the current #1 (TheKnowledgeAcademy) — it answers in sentence one, ships the only SERP comparison table, and handles the mod-APK question incumbents dodge. Full text in `character-ai-no-filter-2026-adversarial.md`. Its top concerns (empty price cells, Pleasur.ai weighting, dead `[link]`s, unrendered screenshots) are draft-stage states resolved downstream, not blocking deficits.

## Punch list (downstream, non-blocking)

1. **/verify-claims** — resolve the 4 `[link]` markers (Medium citation line 15; Pleasur.ai pricing line 64; CrushOn line 82; DreamGen line 98). All trace to live pages per the dossier.
2. **/generate-visuals** — realize the two Pleasur.ai product screenshots (lines 66, 68) so the page carries ≥1 real product image.
3. Optional polish: tighten the three in-body reminders of the unpriced column (lines 76, 92, 106) to avoid over-flagging the table's honest gap.

## Recommendation

**Proceed to /verify-claims.** Draft clears the gate; remaining items are normal downstream work (citation resolution + visual realization), not depth/coverage/prose defects requiring a re-draft.
