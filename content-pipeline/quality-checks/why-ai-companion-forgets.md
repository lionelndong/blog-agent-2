## Verdict: **PASS**

Keyword: "why does my ai companion forget" · Slug: why-ai-companion-forgets · Stage: draft
Gate: FLOORS_OK **and** panel passes (≥2 KEEP_OURS, 0 KEEP_COMPETITOR). Both halves passed.

> Note: the research dossier marks this a no-publish validation run (PLE-2983) — produce through PREVIEW only. This gate reports PASS on quality; publishing remains blocked by the validation flag, not by the gate.

---

## Gate 1 — Floors (binary, mechanical)

Command: `python3 .claude/skills/quality-check/scripts/quality_check.py why-ai-companion-forgets` → **exit 0 (FLOORS_OK)**

| Floor | Result | Detail |
|---|---|---|
| depth | PASS | 2377 words; beat spec has no parseable target word count (BEAT SPEC target 2,200 ±20% — 2377 is within range) |
| consensus_coverage | PASS | all must-cover topics present |
| no_internal_leak | PASS | no internal tooling (Semrush/Ahrefs/Strapi/etc.) in prose |
| forbidden_phrases | PASS | none found |

Non-gating observations (for editor): claim density 0.03 (3/120 numeric sentences); 6 real hyperlinks; **3 naked `[link]` placeholders**; structure 6 H2 + 0 H3; `[GAIN]` marker present (leaking into an H2); repetition crutches flagged — model ×20, facts ×17, every ×16, conversation ×11, character ×9, layer ×9; paragraph rhythm mean 62w, CV 0.37.

---

## Gate 2 — Reviewer panel

Three independent skeptical experts, one lens each. Full reviews in
`why-ai-companion-forgets-panel.md`. Pass iff ≥2 KEEP_OURS AND none KEEP_COMPETITOR.

| Lens | Verdict | One-line reason |
|---|---|---|
| A — Competitiveness | **KEEP_OURS** | Out-explains all incumbents via the 4-stage single-message eviction trace they all hand-wave; depth is real, not padded. |
| B — Voice & readability | **KEEP_OURS** | Reads in brand voice (reader-felt, leads with the decision, product held to its own test); a side-by-side loss isn't credible. |
| C — Reader intent & info gain | **KEEP_OURS** | Delivers the required info-gain (staged eviction walkthrough + runnable scorecard) that the SERP and the AI Overview cannot absorb. |

**Panel: 3 KEEP_OURS, 0 KEEP_COMPETITOR → PASSES.** All three verdicts exceeded 200 words with specific critique; no sharper re-run needed.

---

## Punch list (ordered by severity)

These are non-gating polish items — the gate is PASS — but all three reviewers flagged the
first three, so resolve before preview/publish.

1. **Resolve the 3 naked `[link]` placeholders** (draft lines 41, 55, 69) — "lost in the middle" ×2 and the Character.AI claim. All three lenses called this the top liability; ship as real citations or the draft looks less-sourced than LLMnesia/Kenotic on its most technical claims. Route: **/verify-claims** (or **/draft** if inserting inline).
2. **Fix the chart data reference** (line 61, `data=research.context_rot_accuracy`) — dossier records 0 hard citations and no such dataset; risks a fabricated curve or a broken render. Either source a real recall-vs-fill series or replace with the honest static table. Route: **/research** (source the data) → **/draft** (swap visual).
3. **Remove the `[GAIN]` marker leaking into the H2** (line 29, "...as the chat grows [GAIN]") — internal pipeline tag in reader-facing heading text. Route: **/draft**.
4. **Sharpen "context rot"** (lines 49–55) — H2 promises a definition but collapses the term into "lost in the middle"; define it distinctly (degradation as the window fills, broader than middle-neglect) to beat Kenotic instead of matching it. Route: **/draft** (prose) — coverage already present, so not structural.
5. **Trim the limp intro roadmap + manage repetition** (line 7 "This article walks through five things..."; reuse of the Mara/fishing-boat example across 3 sections; "window" stacking). Route: **/draft**.
6. **Add at least one concrete number** (example window size or rough "~X messages") to strengthen the "how many messages does it remember?" answer vs LLMnesia's accuracy bar; give the higher-volume sibling phrasings (does AI remember past conversations / character-ai / grok / claude) a touch more explicit on-page real estate. Route: **/draft** (prose) — topics already covered.

---

## Outcome

**PROCEED** on quality (gate = PASS). Recommend clearing punch-list items 1–3 before preview
since all three are byline-credibility / fabrication risks that every lens flagged. Publishing
itself stays blocked by the dossier's PLE-2983 validation flag (preview only) — that is a
pipeline scope constraint, not a gate failure.
