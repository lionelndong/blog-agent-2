# Quality Check — why-does-my-ai-companion-forget

## Verdict: **PASS**

FLOORS_OK (exit 0) AND panel passes (3 KEEP_OURS, 0 KEEP_COMPETITOR). Both halves of the gate clear.

Keyword: "why does my ai companion forget" · Slug: `why-does-my-ai-companion-forget` · Stage: draft · Run: VALIDATION (PREVIEW only — do NOT publish).

---

## Gate 1 — Floors (FLOORS_OK)

`python3 .claude/skills/quality-check/scripts/quality_check.py why-does-my-ai-companion-forget` → exit 0.

| Floor | Result | Detail |
|---|---|---|
| depth | PASS | 2628 words; beat spec target 2,300 (+/-20%) — within ceiling |
| consensus_coverage | PASS | all must-cover topics present (context window, two failure modes, logs != memory, bigger-window cost + Lost in the Middle, memory workarounds, FAQ) |
| no_internal_leak | PASS | no internal tooling (Semrush/Ahrefs/Strapi) in prose |
| forbidden_phrases | PASS | no forbidden phrases |
| comparison_table | N/A→PASS | SERP has 0/5 tables; optional clarity table (logs vs memory) present, allowed |

Non-gating observations from the script (for the editor): claim density 0.08 (10/131 numeric sentences); 6 real hyperlinks + **3 naked `[link]`**; 10 H2 / 0 H3; `[GAIN]` marker present; repetition flags — "model" x18, "conversation" x12, "every" x10, "thread" x9, "that's" x9, "what's" x8, "come back" x5, "across sessions" x5; paragraph rhythm mean 58w, CV 0.41.

---

## Gate 2 — Reviewer panel (PASS)

Full write-ups in `why-does-my-ai-companion-forget-panel.md`. All three exceeded 200 words with specific critique — no glowing-and-short re-run triggered.

| Lens | Verdict | One-line why |
|---|---|---|
| A — Competitiveness | **KEEP_OURS** | Out-explains DHC on token/context mechanics (its weak axis) and adds the text memory test no incumbent has; vulnerable only on citations + unrendered assets. |
| B — Voice & readability | **KEEP_OURS** | Reads like the brand anchors — concrete felt cold open, short declarative rhythm, honest earned product mention; would run under a byline. |
| C — Reader intent & info gain | **KEEP_OURS** | Validates the felt loss AND hands a repeatable test the AIO/SERP can't; stays honest on save-and-resume (not "infinite memory"). |

Panel rule (>=2 KEEP_OURS AND none KEEP_COMPETITOR): **satisfied.**

---

## Punch list (ordered by severity)

The gate PASSES; these are pre-publish polish items. None blocks the verdict, but items 1–3 are unanimous across reviewers and should be fixed before any live push.

1. **Resolve the 3 naked `[link]` markers with real citations** — lines 29 (1,000 tokens ≈ 750 words), 70 (10M vs 128K compute), 72 ("Lost in the Middle"). All three reviewers flagged this; the AIO-beating thesis depends on credibility, and the top incumbents (DHC, llmnesia, matthopkins) ship Sources blocks. → **/verify-claims** (or **/draft** to insert citations inline).
2. **Cut or hard-soften the 82% retention stat** (line 117) — self-undermining (cites own blog, then admits no methodology) and drags a competitor face-off link into an emotional explainer SERP. Flagged by all three lenses. → **/draft**.
3. **Strip the literal `[GAIN]` tag from the H2** ("How to Test Your Companion's Memory in 2 Minutes [GAIN]", line 92) — editing artifact that ships as amateurish. → **/draft**.
4. **Fix the chart VISUAL data reference** (line 76) — `data=research.memory_token_facts` points to a key the dossier does not contain; will fail to render or fabricate numbers. Either add a sourced compute table to research or change the visual. → **/research** (add the data) or **/draft** (re-spec the visual).
5. **Tighten the in-chat-overflow test step** (step 2, "15 to 20 messages", line 97) — arbitrary count won't reliably trigger overflow on large-window models the draft itself says exist, so that half of the headline test can false-pass. Give a token/length-based trigger or caveat. → **/draft**.
6. **Trim product-mention density / brand-link reliance** — Companion Creator appears 2x before the conclusion plus the action-shot, and the "four memory types ladder" is asserted via a brand link as if authoritative. Keep the earned end-of-article mention; thin the mid-article repeats. → **/draft** (prose); the ladder taxonomy framing is a structure call → **/outline** if the section is reorganized.
7. **Voice polish (minor):** reduce the "it's not X, it's Y" pattern (used 2x close together), em-dash density, italic-for-emotion crutch, and the "ache" reach. → **/draft**.

---

## Recommendation

**PROCEED** (with pre-publish polish). The gate is a clean PASS — floors clear and all three skeptics keep ours over the live #1. This is a VALIDATION/PREVIEW run, so do not publish regardless. Before any future live push, apply punch-list items 1–4 (citations, the retention stat, the `[GAIN]` artifact, the broken chart data ref) via the routed stages; items 5–7 are polish that further widens the lead but are not blockers.
