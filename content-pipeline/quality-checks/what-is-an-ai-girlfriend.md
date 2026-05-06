# Quality check — what-is-an-ai-girlfriend

## Verdict: **PASS** (94 / 100)

No CRITICAL items. Two structural HIGH items worth fixing before publish but neither blocks the pipeline. Recommendation: proceed to `/verify-claims`, then revisit the §1 hook freshness and the §2 prose-vs-table redundancy as a light editing pass. No regeneration needed.

---

## Metrics summary

**Auto-only partial: 78 / 80**

| Dimension | Weight | Score | Notes |
|---|---|---|---|
| Forbidden phrases | 20 | 20 | Zero hits. |
| Voice metrics vs `examples/` baseline | 25 | 25 | All seven metrics in range. Sentence/paragraph length and second-person frequency track the baseline closely. |
| BLUF compliance (H2 openers) | 20 | 20 | 7/7 sections (100%) pass the BLUF heuristic. |
| Claim density + linkability | 15 | 13 | 8 of 9 must-cite claims have a link or `[link]` placeholder (88.9%, well above 60% threshold). One missing must-cite link. |
| Adversarial verdict | 20 | 16 | 2 genuinely structural issues (well under the 3-issue PASS bar) plus 3 style/quality complaints. |
| **Total** | **100** | **94** | **PASS (≥75)** |

Draft length: 2,626 words (target 2,000–2,300 — slightly long, not flagged).

## Constraint-violation audit

| Check | Result |
|---|---|
| Coming-soon products in walkthrough (Voice Replies / Phone Call) | **CLEAN** — zero hits. Reconciliation pass held. |
| Brand-string violations (anything other than `Pleasur.AI`) | **CLEAN** — every Pleasur reference is exactly `Pleasur.AI` (lines 25, 144, 152, 154, 158, 170). |
| Out-of-slot product mentions (§2/§3/§4/§5) | **CLEAN** — §2/§3/§4/§5 are product-free per outline. §1 has one inline mention (line 25). §6 owns the walkthrough. Conclusion has the closing CTA (allowed by outline). |
| Article reads informational/definitional, not commercial-comparison | **CLEAN** — the §6 walkthrough is the only pitch slot; everything else holds the explainer voice. |

No CRITICAL items.

## Adversarial critique (verbatim — `quality-checks/what-is-an-ai-girlfriend-adversarial.md`)

**Works:** §3 "week one vs week four" is the only section that does work other AI-girlfriend explainers don't.

**Five weaknesses:**

1. The Replika "1M paid / ~1/3 romantic" hook is recycled across the SERP and the "by mid-2023" anchor reads stale against a 2026 dateline.
2. §2 promises plain-English then delivers a stack diagram in prose AND in a table — the same information twice, exactly what the intro mocked.
3. Three numerical claims in §2 (memory size, voice latency, render time) are unsourced `[link]` placeholders on suspiciously precise numbers; reads like plausible-sounding figures bolted to a citation TODO.
4. §5's EU AI Act / UK ICO bullet is dropped in like a tax disclosure — doesn't change a reader decision and breaks tone.
5. §4's 3-for / 2-against profile matrix reads template-clean rather than honest; the format undercuts the section's "honest" claim.

## Punch list

### CRITICAL — none

### HIGH — fix before publish

1. **§1 hook is stale and SERP-recycled.** Line 3: "By mid-2023, more than a million people were paying Replika…" — this exact frame opens half the explainers on the SERP, and the 2023 date undermines the article's 2026 freshness signal. Either swap to a more recent anchor (Replika user-base 2024/25 if available, or a comparable but less-flogged data point) or strip the date and lead with a different reframe. **Touch:** `content-pipeline/5-drafts/what-is-an-ai-girlfriend.md` line 3.
2. **§2 prose + table is the same information twice and undercuts the intro.** Lines 35–55 walk through the five-component stack in prose; lines 57–63 then put it in a table. The intro at line 5 explicitly mocks "over-engineer the technology into a stack diagram." Fix by collapsing §2 prose to ~150 words of voice-first interpretation (why the architecture matters for the reader's experience) and letting the table carry the spec detail. Cuts ~250 words of §2 redundancy and brings the draft closer to the 2,000–2,300 target. **Touch:** `content-pipeline/5-drafts/what-is-an-ai-girlfriend.md` lines 35–63.
3. **One missing must-cite citation.** The auto-checker flagged 8 of 9 must-cite claims linked. The unlinked claim is line 17 ("It sits inside the broader [AI chatbot app](…) category, but it's tuned for romance and adult interaction rather than productivity") — flagged because of the named entity. This is a category-positioning claim, not a numerical/factual claim, so `/verify-claims` can decide whether to drop it from the must-cite list rather than chase a source. **Touch:** `content-pipeline/5-drafts/what-is-an-ai-girlfriend.md` line 17.

### MEDIUM — consider in light edit

4. **§2's three `[link]` placeholders on suspiciously precise numbers.** Lines 45 (5,000–20,000 chars memory), 51 (150–400ms voice latency), 55 (2–5s render time). `/verify-claims` needs to either source these to a real benchmark (Stillmind / vendor docs / public latency tests) or soften the precision (e.g. "typically a few hundred milliseconds" instead of "150 to 400 milliseconds"). Precise-but-uncited numbers trigger reader skepticism faster than a soft range with no number at all. **Touch:** `content-pipeline/5-drafts/what-is-an-ai-girlfriend.md` lines 45, 51, 55.
5. **§5 regulation bullet doesn't earn its place.** Line 138 (EU AI Act + ICO consultation) is a fact-dump that doesn't change a reader decision. Either cut it or rework it to connect to a real reader concern ("if you're worried about disclosure or data privacy, here's where regulation is going and what it'll mean for these apps"). **Touch:** `content-pipeline/5-drafts/what-is-an-ai-girlfriend.md` line 138.

### LOW — voice polish

6. **§4's 3-for / 2-against bulleted matrix.** The boxed format ("the curious explorer / the writer or roleplayer / the private adult") works for scanability but reads template-clean. Consider lighter prose treatment or fewer-but-meatier profiles for the next revision. Not a blocker. **Touch:** `content-pipeline/5-drafts/what-is-an-ai-girlfriend.md` lines 99–108.

## Recommendation

**Proceed to `/verify-claims`.** Score is comfortably above the PASS threshold, no CRITICAL items, brand-string and slot-discipline are clean, and no coming-soon products leaked into the walkthrough. The two HIGH items (stale hook, §2 prose/table redundancy) are valuable to address but neither warrants regenerating the draft — both are surgical edits a single light pass can fix after citation work.

For an autonomous run: proceed.
For an interactive run: editor should review HIGH items 1–2 before publishing; `/verify-claims` will independently triage MEDIUM item 4.
