# Outline Adversarial — what-breaks-immersion-ai-roleplay (Pass 2)

## Verdict: **PASS**

Pass 2 of 2 (revision budget BLOG_AGENT_OUTLINE_REVISION_BUDGET=1).

Re-run after the outline was revised to fix the 2 CRITICALs + 1 HIGH from Pass 1.

## Prior Findings — Verification

1. **One consistent set of per-section word targets summing to 1,200–1,500? — RESOLVED (Y).** Single authoritative set, stated twice and matching: Intro 150 · §1 200 · §2 270 · §3 220 · §4 210 · §5 270 · FAQ 180 · Conclusion 100 = **1,400**. Per-section headers match the summary line exactly.
2. **Exactly 3 load-bearing visuals, no decorative diagrams (§1/§2 = none)? — RESOLVED (Y).** Non-none: §3 external Replika quote, §4 screenshot, §5 comparison table — three distinct types. §1, §2, Intro, FAQ, Conclusion all `{type: none}`.
3. **§2/§5 no longer overlap on the memory mechanism? — RESOLVED (Y).** §2 explicitly claims ownership of the context-window-vs-persistent-memory mechanism; §5 enforces the boundary ("Do NOT re-explain the MECHANISM — §2 owns that") and redirects to the secondary keyword + table. Overlap is structurally fenced.

## Findings

### CRITICAL

- None.

### HIGH

- **[§3 vs §5] Same "consistency anchoring" fix stated twice.** §3's fix ("anchor consistency in saved relationship context") is re-invoked in §5 ("the saved backstory also anchors consistency, fixing break #2"). §5 is an explicit synthesis section so it's not a CRITICAL, but /draft will be tempted to re-derive the §3 mechanism. Add a one-line fence in §5: name the anchoring as a benefit, don't re-argue the §3 mechanism.

### MEDIUM

- **[§3] Consensus topic (d) "safety-filter refusals" folded into Character Drift, not its own break.** Every SERP competitor treats "I can't talk about that" as a first-class immersion-killer. The 3-break spine is brief-mandated, so subsuming refusals under §3 is correct structurally — flag only so /draft gives OOC refusals real estate inside §3 and doesn't drop them.
- **[§4] Visual is typed `{type: screenshot, target: create}` but the desired state is post-interaction (reply bubble + speaker icon + Call button).** Per the visuals decision tree this is an **action-shot**, not a single-URL screenshot; as specced it will route to a failed/empty headless capture. Right section, right intent, wrong type — will cost a capture cycle. Re-type to action-shot before /generate-visuals.
- **[§2 / §5] MariaVibe 82% stat allowed in both sections.** Double-citation risk: the dossier calls this "supporting color, NOT the spine." Spend it once (recommend §2); §5 already hedges "only if used as light color" — tighten to "do not repeat if spent in §2."

### LOW

- **[§3] BLUF/visual alignment is clean** — §3 BLUF ("model/policy update rewrites its personality") and the external Replika quote prove the same claim; no contradiction.
- **[Coverage] MECE holds at the H2 level** — all 6 beat-spec must-cover topics map via the coverage table; no SERP consensus topic missing.

## What Works

- The compliance landmines are defused **at the outline level**, not deferred to /draft: the comparison table hard-codes "do NOT print Questie: no memory," voice is fenced as audio-only in §4, pricing is coin-metered, and the unverified "performing intimacy with amnesia" quote is explicitly banned. Combined with the §2/§5 ownership fence and per-section attribution rules, a competent draft can't trip the brand-config rules by accident. The hard part is done right.

## Recommendation

- Verdict is **PASS** — advance to stage 4 (/product-mentions).
- Before /generate-visuals, re-type the §4 visual from screenshot → action-shot (MEDIUM, the one change worth making first). F1/F5 are drafting fences worth carrying into /draft as notes.
