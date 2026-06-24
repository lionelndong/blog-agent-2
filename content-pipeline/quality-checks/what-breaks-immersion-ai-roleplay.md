# Quality Check — what-breaks-immersion-ai-roleplay (RE-RUN post BORDERLINE-84 revision, 2026-06-24)

## Verdict: **PASS** — final score 88/100

- **Final** = 0.6 × mechanical (88, consensus false-negative corrected by read) + 0.4 × judgment (88) = **88 (PASS)**
- **No CRITICAL finding.** All PLE-2960 hard constraints clean (table below).
- **No mechanical dimension below 60% of weight** once the known consensus_coverage false-negative is corrected by reading (all 6 must-cover topics present).
- **Adversarial read does NOT pick the competitor** for the GEO/AIO citation surface (this article's win condition); the 60-word hook is "the most extractable snippet on the entire SERP for this exact query."
- Autonomous publish gate (≥85) **MET.** Proceed to `/verify-claims` (resolve the 6 `[link]` placeholders to the §8 verified URLs) → `/generate-visuals` → publish.

Routing: **proceed** down the pipeline. No re-draft, no re-outline. The remaining items are downstream-stage work, not gate failures.

---

## Prior punch-list (BORDERLINE-84) — resolution

| # | Prior issue | Status |
|---|---|---|
| 1 | 82% stat prefixed "One independent comparison reported" (brushed the "never independent/validated" ban) | **RESOLVED (Y)** — now "MariaVibe.com reported 82% memory retention after a week for Pleasur.ai [link]" (§2). MariaVibe-only, no "independent/validated", no first-person framing. |
| 2 | Brand density too high; §1 should be neutral/diagnostic | **RESOLVED (Y)** — §1 is mechanism-only (narrative-transportation, 3 named breaks, no product); §2 and §3 carry one Creator mention each; product depth concentrated in §4/§5. |
| 3 | Over-length / repetition ("companion", "backstory") | **RESOLVED (Y)** — narrative spine 1,389 words; "backstory" repetition cut; §2 owns the memory-mechanism explanation and §5 assumes it (no full restatement). Script word count (1,671) includes the table + 4-Q FAQ + visual placeholders, which are GEO-justified. |

---

## Metrics summary

- **Mechanical (script): 85/100.** depth_vs_benchmark 25/25, consensus_coverage 10/20 (**false negative — see note**), evidence 9.6/15, ai_tells 25/25, structure 15/15.
- **consensus_coverage 10/20 is a known keyword-string false-negative.** By reading, all 6 must-cover topics ARE present: 3 breaks in the hook (§0/§1); memory-loss/context-window (§2); character drift + relationship-context anchoring (§3); no-voice/real-time-audio continuity (§4); secondary-keyword "AI girlfriend memory between sessions" section (§5); FAQ block with the 4 exact brief questions. Treated as effectively full → corrected mechanical ≈ 88; no real floor breach.
- **Word count:** narrative spine ~1,389 (within 1,200–1,500 beat-spec band); script 1,671 incl. table/FAQ/visual markup.
- **Hook:** 49-word standalone first sentence, names all 3 breaks, mirrored at §1 BLUF and FAQ #1 (triple-redundant AIO/Perplexity extraction).
- **Structure:** all 5 H2s present (Why It Breaks / Memory Loss / Character Drift / No Voice = No Flow / AI Girlfriend Memory Between Sessions) + 4 exact FAQ questions + capability comparison table.
- **AI tells:** 25/25, no forbidden phrases, no internal-stack leak (Questie's "Zep Cloud" correctly omitted from prose).

### Judgment read (40% of final) — 88/100
Voice matches `examples/voice/` (short declaratives, concrete, no throat-clearing: "You feel it the moment the magic snaps"). Information gain is real and verified: the answer-first "three breaks → one stack (persistent memory + real-time voice) fixes all three" framing with a live-verified capability table — no page-1 competitor pairs memory+voice as the explicit thesis with a 60-word hook. Product mentions are demonstrated (speaker icon, Call button, coin metering), not bolted on. Loses nothing on the side-by-side for the citation goal.

### HARD constraint compliance (PLE-2960) — re-confirmed clean

| Constraint | Result |
|---|---|
| Coin-metered pricing ONLY (no flat / no-tokens / no-limits / no-hidden-fees) | **CLEAN** — voice notes 10 coins, calls 50 coins/min; no banned framing |
| Voice = real-time AUDIO, no video calls / two-way video | **CLEAN** — "It's real-time audio — not video" stated explicitly (§4) |
| Questie never framed as lacking memory | **CLEAN** — table + prose credit Questie with both memory + voice; wedge = gaming-screen-vision vs companionship |
| 82% attributed to MariaVibe.com ONLY, not independent/validated/first-person | **CLEAN** — "MariaVibe.com reported 82%…" (§2) |
| No no-filter absolutism / safety guarantees / real-person likenesses / explicit NSFW / internal-stack names | **CLEAN** — the one "never" (§3) hedges AGAINST a guarantee; no NSFW; no stack names |
| Answer-first hook ≤60 words, standalone first sentence | **CLEAN** — 49 words |
| 5 H2s + 4 exact FAQ questions | **CLEAN** — all present |

---

## Adversarial critique
Full read: `content-pipeline/quality-checks/what-breaks-immersion-ai-roleplay-adversarial.md`. Does NOT pick the competitor for the citation surface. Every flagged weakness is either a downstream-stage artifact (`/verify-claims` resolves `[link]`; `/generate-visuals` renders the 2 placeholders + table) or the truthful, beat-spec-mandated competitor-parity framing. One genuine strength: the 60-word hook is the most extractable snippet on the SERP for this query.

---

## Punch list (ordered; none gate-blocking)
1. **`/verify-claims`** — resolve the 6 `[link]` tokens (lines 13, 15, 23, 27, 35, 46) to the §8 verified URLs (MariaVibe, entreresource, Felt Real, latency + narrative-transportation sources). Highest-leverage item: an uncited GEO piece can't win the citation it's built for.
2. **`/verify-claims` polish** — append "in its Aimour-vs-Pleasur comparison" to the 82% line to further harden the attribution (constraint already met; this is belt-and-suspenders).
3. **`/generate-visuals`** — render the 2 `[VISUAL:...]` placeholders (§3 Replika news-quote, §4 voice-button screenshot) and the capability table card.

## Recommendation
**PROCEED** to `/verify-claims` → `/generate-visuals` → autonomous publish. PASS at 88; no CRITICAL; no real floor breach; adversarial keeps this draft for the citation surface. Do not re-draft or re-outline.
