# Quality Check — what-happened-to-replika-users

## Verdict: **PASS**

- **Mechanical:** 87/100
- **Judgment:** 88/100
- **Final (0.6×mech + 0.4×judg):** 87.4 → **PASS**
- **CRITICAL findings:** none
- **Mechanical dimension below 60% floor:** none
- **Adversarial side-by-side:** keeps OUR draft over SERP #1 (aicompanionpick.com)

Meets all four PASS gates: final ≥85, no CRITICAL, no mechanical dimension under floor, adversarial does not pick the competitor. Publish floor is 85; this clears it.

---

## Metrics summary

| Dimension | Score / Weight | Note |
|---|---|---|
| Depth vs benchmark | 15.0 / 25 | 2,053 words vs ~2,000 BEAT SPEC target — on target; required tables BOTH present (timeline + alternatives); 7 alternatives (in 6–8 spec band). |
| Consensus coverage | 16.7 / 20 | All 6 consensus topics present (see false-negative note). |
| AI tells | 25.0 / 25 | No forbidden phrases; no internal-stack leak; rhythm CV 0.58 (varied). |
| Evidence | 15.0 / 15 | Claim density 0.21; 25 hyperlinks; 23 `[link]` placeholders (draft-stage OK, verify-claims must resolve). |
| Structure | 15.0 / 15 | Clean H2/H3, intro + conclusion, two scannable tables. |

**Two script false-negatives to disregard:**
1. *"NO BEAT SPEC found — legacy?"* — the dossier DOES carry a full BEAT SPEC section (the script's regex misses the heading). Not a legacy dossier; no re-research needed.
2. *"MISSING consensus topic: Where users migrated."* — the draft has a full "Where Replika Users Went: 7 Alternatives Compared" section with a comparison table. Topic is covered; the matcher missed it.

**Repetition flags** (crutch words: "romantic"×10, "people"×9, "memory"×9, "million"×8, "feature"×8, "paying"×8): mostly topic-intrinsic for a Replika-feature article, not AI tells. Light trim worthwhile but not blocking.

---

## Adversarial critique (full read in `-adversarial.md`)

**Side-by-side:** searcher keeps OUR draft — it answers the literal question first (dated timeline → the Garante "why" → legacy-mode catch → 2026 state), then hands over the stability checklist and comparison table in tighter, less salesy prose than aicompanionpick's review-led page. The fully-cited Date|Event|Source table is information the #1 page narrates in prose and cannot match.

**What works:** the timeline table delivers information-gain #1 exactly as specified — varied real sources (Wikipedia, EDPB, Vice, Socius, IAPP) no competitor offers in this form.

**Weakest vs the field:** (1) no scannable FAQ block (aicompanionpick + charalt both ship one; forfeits PAA/rich-result real estate); (2) ~5 visuals vs competitors' 10–18, two of them bare external screenshots; (3) alternatives table thin on non-Pleasur rows (em-dash cells), reads self-serving; (4) unresolved `[link]` placeholders undercut the "check the sources yourself" promise; (5) brand pivot lands twice and crowds the migration section.

---

## Constraint scan (CRITICAL checks — all clear)

- **Disparagement / legal risk:** none. Factual, sourced "documented event" framing; "you can defend the destination and still fault the road" is balanced, not a put-down. PASS.
- **Hedged claim hardened to fact:** none. 2026 v2.0 is correctly attributed ("reported rather than confirmed," "disagree on the exact month"). PASS.
- **Product mention in a factual-history section:** none. Feb 2023 / backlash / legacy-mode / timeline sections are product-free; Pleasur.AI appears only in checklist, alternatives, conclusion. PASS.
- **Adult-compliance:** no no-filter absolutism, no safety guarantee, explicitly rejects "unlimited" ("metered by coins… not an 'unlimited' claim"), no real-person likeness. PASS.
- **Internal-stack leak:** none. PASS.

---

## Punch list (ordered by severity)

- **HIGH** — *Where Replika Users Went / How to Pick.* Resolve all `[link]` placeholders to live citations at `/verify-claims`; the article's thesis ("the dates carry the argument," "check the sources yourself") demands every claim be linked, not just the timeline table.
- **MEDIUM** — *Alternatives section.* The brand pivot lands twice (checklist closer + alternatives paragraph with four Pleasur.AI links). Cut one pivot or move the second below the other-app rows so a wary ex-Replika reader gets a clean read of the six competitors before the pitch.
- **MEDIUM** — *Add an FAQ block.* Both the #1 page and charalt ship one; the dossier names "is replika dead / still worth it 2026" as live PAA. A 4–5 Q schema-eligible FAQ captures rich-result real estate the draft currently forfeits in prose.
- **LOW** — *Visuals.* Field carries 10–18 images; draft ~5, two of them bare external screenshots. Consider 1–2 more original assets (or accept as a deliberate lean-text trade-off).
- **LOW** — *Crutch trim.* Light pass on "romantic"/"memory"/"feature" repetition where non-load-bearing.

---

## Recommendation

**Proceed to `/verify-claims`.** This is a clean PASS at 87.4 with zero CRITICAL findings and an adversarial read that keeps our draft over the SERP #1. No structural deficit — the depth, coverage, tables, and information-gain assets are all in place, so this does NOT go back to `/outline` or `/research`. The HIGH item (resolve `[link]`s) is exactly what the next stage does. The FAQ and second-pivot items are MEDIUM polish that can land at verify-claims or editor review without re-drafting.
