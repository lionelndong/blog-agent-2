## Verdict: **PASS**

Slug: best-ai-girlfriend-app · Keyword: "best ai girlfriend app" · Stage: 6 quality-check (publish gate)
Re-run after the revision pass (validation dry-run — nothing publishes). Overwrites the prior FAIL verdict.

PASS requires BOTH halves. Both passed:
- **FLOORS_OK** — `quality_check.py best-ai-girlfriend-app` exited 0.
- **Panel PASS** — 3× KEEP_OURS, 0 KEEP_COMPETITOR, 0 TOSS_UP (≥2 KEEP_OURS and none KEEP_COMPETITOR).

The prior FAIL was driven by the feature matrix lacking real competitor data, a "we tested" claim the
method didn't support, and a thin privacy section. The revision fixed all three: the matrix now carries
verified, source-labeled competitor cells; the claim is reframed as an honest criteria-based evaluation;
and the privacy section has per-app substance (Candy/Nomi/CrushOn specifics, three apps honestly marked
unverified). The panel credits these as holding up against the UGC-and-thin-listicle SERP.

---

## Floors summary

| Floor | Result | Detail |
|---|---|---|
| SERP benchmark present | PASS | dossier benchmark table present |
| depth | PASS | 4,376 words; ≥80% of ~3,600 beat-spec target |
| item_count | PASS | 19 H2+H3 sections vs 7-item beat spec; 7 apps ranked |
| comparison table | PASS | criteria feature-matrix present (the required core gain asset) |
| consensus_coverage | PASS | all must-cover topics present |
| no_internal_leak | PASS | no internal tooling names in prose |
| forbidden_phrases | PASS | none (no "$19 unlimited", no "82% retention", no video claim) |

Non-gating observations (for the editor): claim density 0.25, 8 real hyperlinks, 0 naked links;
repetition flags (memory ×39, pricing ×29, reviews ×21); paragraph rhythm mean 48w / CV 0.69.

---

## Panel verdicts (full text in best-ai-girlfriend-app-panel.md)

- **Lens A — Competitiveness: KEEP_OURS.** Out-structures the UGC top and out-substances every editorial listicle on the three gain axes; the only true criteria matrix, the only coin-metering math, the only per-app privacy section. Verified matrix cells read credible, not hedged-into-mush.
- **Lens B — Voice & Readability: KEEP_OURS.** Matches the Theo Hart craft — problem-first hook, BLUF openers, peer hedges, decision-led. De-templating worked on entry openers; repetition crutches and a surviving pros/cons spine are fixable polish, not structural.
- **Lens C — Reader Intent & Information Gain: KEEP_OURS.** Helps a buyer pick and pay better than page one; lands all three gain elements and stays clean on every compliance landmine; the bounded "couldn't verify" honesty is a net strength, not a hole.

---

## Punch list (routed; non-blocking — PASS already; tighten at verify-claims / draft)

1. **Competitor price cells are mostly "(3P reviews)" and load-bearing in the matrix** (5 of 7 — Candy, OurDream, Nomi, GirlfriendGPT, MyAnima; MyAnima's "~$14–22/mo" is an $8 spread). All three lenses flagged this as the top credibility soft spot for a $1.30-CPC compare-to-pick query. **Route: /verify-claims** — re-pin each to a dated first-party page or tighten the range.
2. **Privacy is a differentiator but absent from the matrix and blank for 3 of 7 apps** (OurDream/GirlfriendGPT/MyAnima "couldn't confirm"). The skim-first asset can't be skimmed on the safety criterion it elevates. **Route: /outline** (add a Privacy column to the matrix) **+ /research** (chase published retention/training terms for the three unverified apps).
3. **Voice polish: repetition crutches + surviving pros/cons spine + scaffolding in prose.** Thin the coin/meter and "memory" drumbeat in the back half; vary the identical **Pros:**/**Cons:** internal rhythm across entries; strip reader-facing `[GAIN]` tags and `[VISUAL:...]` placeholders before publish; break the long methodology/privacy paragraphs (CV 0.69). **Route: /draft.**

Secondary (lower severity): justify the ranking order against the rubric (why Pleasur.AI #1 over Nomi); isolate the GirlfriendGPT "images/video" competitor claim from our own no-video constraint.

---

**Proceed / iterate / halt: PROCEED.** Both gates pass; quality clears the ≥85 benchmark-relative bar
(not borderline). This is a validation dry-run, so nothing publishes — the article is publish-ready on
the gate. Punch-list items 1–3 are recommended polish for the next verify-claims/draft pass, not blockers.
