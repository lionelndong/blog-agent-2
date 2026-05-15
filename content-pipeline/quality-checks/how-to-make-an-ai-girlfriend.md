# Quality check — how-to-make-an-ai-girlfriend

## Verdict: **BORDERLINE** — 73 / 100

Auto-metrics 63/80 + adversarial 10/20.

- **PASS** on: zero forbidden phrases, BLUF compliance 6/6 (100%), no "leads" framing, sentence-length voice band, em-dash density.
- **FAIL** on: paragraph length above baseline (42.6 avg vs 24.3); must-cite link density 42.9% (gate is ≥60%); 5 distinct weak structural issues from adversarial pass (gate is <3).

## Metrics summary
- Word count: 3,005 (count via `wc`) / 3,365 (script tokenizer).
- Brand mentions: 11 Pleasur.AI references across ~3,000 words = 1 per ~273 words. Within the 1/250 threshold.
- Voice metrics out-of-band on 2 of 7 dimensions (paragraph length, both avg and median).
- BLUF: 6/6 H2 openers pass.
- Must-cite claims: 21; linked 9 (42.9%). Below 60% gate.
- Voice-flagged claims: 20; linked 1 (5.0%) — visibility only.
- Forbidden phrases: none.
- Coming-soon products: Voice Replies + Phone Call appear in the explicit permitted slot (Tip box inside the "what breaks" H2). The annotated outline (lines 6–9, 107–108, 169) pre-approved this exact placement and the draft does NOT link out to any non-existent `/voice` or `/call` URL. **Not a CRITICAL violation.**
- "Leads" framing: zero occurrences. Clean.

## Adversarial critique (see `-adversarial.md` for full text)
Five weak structural issues identified:
1. The DIY "recipe" is component-name gestures, not a runnable recipe — less concrete than the 2022 tutorial it mocks.
2. The "memory is the thing every guide skips" thesis collapses into one shallow paragraph.
3. The pricing comparison's disclaimer ("not a covert ad") draws attention to its own asymmetry — Pleasur.AI gets a price-range column the others don't.
4. The Replika/Vice anecdote is reused near-verbatim in two H2s.
5. The Stanford loneliness stat reads as a guilt-shield, not an integrated point.

What works: the six-dimension DIY-vs-off-the-shelf pre-flight comparison. That earns its keep.

## Punch list (severity-ordered)

### CRITICAL
— none

### HIGH
1. **Must-cite link density 42.9% → must reach 60%** (`5-drafts/how-to-make-an-ai-girlfriend.md`).
   - Unlinked claims that need sources: $0.72/hr A100 spot (already linked via Medium — keep); "GPT-Neo 1.3B and waifu-diffusion" 2022 tutorial (`[link]` placeholder line 40 — resolve); ElevenLabs pricing tiers (line 48); "$250–$500 in spot GPU time per month" (line 50); KD 27 / volume 110 / volume 90 Semrush figures (lines 25 — `[link]` placeholder); Nomi/Kupid/RomanticAI "gate pricing behind sign-in" (line 96 `[link]`); Kupid + RomanticAI "no third-party-review pricing" (lines 103, 105) — at minimum cite the search attempts that returned nothing.
   - `/verify-claims` is the right stage to resolve these.
2. **DIY "real 2026 recipe" promises specificity it doesn't deliver** (lines 38–70).
   - Either add one concrete artifact (a LoRA config snippet, a HuggingFace dataset name, or a single training-command example) or soften the H2 promise. The adversarial reader's #1 complaint will be reader-facing too.
3. **Memory section is shallow relative to its setup** (lines 56–63, 130–131).
   - Either name the embedding model (e.g. `text-embedding-3-large`), the re-injection prompt structure, or a summarization cadence — or stop pitching memory as the differentiator. Currently does both: pitches hard, resolves soft.

### MEDIUM
4. **Paragraph length above baseline** — avg 42.6 vs 24.3, median 37.5 vs 23.
   - Break the longest paragraphs (especially in DIY section lines 42–58 and pricing breakdown 100–106) into 1–3 sentence units. The voice-guide ceiling is 1–4 sentences per paragraph.
5. **Pricing-table asymmetry** (lines 102–106).
   - Either (a) collapse Pleasur.AI's "$13.99–$27.99 across regions" into the same flat-monthly format the other rows use, or (b) note the same regional variance for any competitor where it applies. Currently the variance reads as a soft upsell.
6. **Replika/Vice anecdote duplicated** (lines 60 and 122–124).
   - Cite once, reference back the second time ("the same Replika 2023 patch above"). The current double-cite is a structural tell.

### LOW
7. **Stanford loneliness paragraph** (line 134) reads as appended ethics-tax. Either integrate it into the "week-three" thesis (loneliness is the user state the memory layer is fighting to serve) or drop it.
8. **`[link]` placeholders** at lines 9, 25 (×2), 60, 96, 102, 104, 106, 122, 134, 156 — flag for `/verify-claims`.
9. **Visual placeholders** look well-typed; no action.

## Recommendation: ITERATE (one targeted revision pass), then proceed to `/verify-claims`

The article has strong bones: BLUF discipline is perfect, no forbidden phrases, no "leads" language, coming-soon products correctly contained to the permitted slot, and the DIY-vs-off-the-shelf framing is genuinely differentiated content. Failure modes are fixable in a single targeted pass: tighten paragraphs, deliver one concrete artifact in the DIY section, normalize the pricing-table format, dedupe the Replika anecdote.

In autonomous mode, dispatch a revision pass against the HIGH + MEDIUM items above, then re-run quality-check. The `/verify-claims` stage will then naturally lift the must-cite ratio toward the 60% gate by resolving the `[link]` placeholders. Do NOT halt — score is above the 60 FAIL floor and there are no CRITICAL items.
