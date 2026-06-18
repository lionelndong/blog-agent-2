# Research Adversarial Review: is-candy-ai-safe

Stage: research-adversarial | Slug: is-candy-ai-safe | Date: 2026-06-15

Skeptical pushback on `content-pipeline/1-research/is-candy-ai-safe.md` before it feeds the outline. GEO/AEO answer page (fixed shape per brief PLE-2332): answer-first opening, 4-column safety table, 5-bullet checklist, 6-question FAQ (≤50 words each), CTA; 1,100–1,600 words.

## Findings

**1. [MEDIUM] Trustworthy figure: prose contradicts JSON.** JSON `is_candy_ai_trustworthy=90`. Prose line 38 states "is candy ai trustworthy (70)" as a standalone; line 24 writes "is candy ai trustworthy / is candy.ai trustworthy — 70 + 90/mo." The JSON collapses both spelling variants into one key=90, matching the `.ai` variant, not the "70" the prose presents as the primary-spelling volume. A chart off the JSON would label 90 while the body says 70. Low blast radius (never load-bearing in the answer) but a genuine prose/JSON mismatch to reconcile before any volume callout.

**2. [LOW] Competitor price/feature claims ARE sourced — and correctly fenced as third-party.** Candy AI "premium ~$12.99/mo, 100 tokens; 2 tokens/photo, 0.2/voice msg" traces only to aitoptools + skywork (reviewers), NOT Candy AI's own page. The dossier explicitly flags this (line 111: "a competitor figure, not ours — keep it sourced, do not present as ours"). For a safety-comparison page whose table axes are data-storage / policy / regulatory / age — not price — the figure is not load-bearing and need not enter the table. Reviewer-sourced is acceptable here. Not CRITICAL.

**3. [LOW — adequate] Pleasur.ai first-party facts carry an adequately-recorded live source.** Line 109 records "verified live at pleasur.ai/legal/privacy-policy, last updated 2026-02-23, checked this run"; line 111 affirms the facts trace to the live policy this run, not brief/memory (Rule 3). URL + fetched-this-run + policy last-updated date meets the first-party trace bar. No Pleasur.ai pricing/tier/coin claim appears anywhere (correct — price is not a table axis), so there is no unsourced own-price claim to flag.

**4. [LOW — correct] FTC item is attributed, not overstated.** Line 107 frames "an FTC complaint and Italy's $5.6M fine" and instructs: attribute exactly as "the FTC complaint alleged" / "Italy's regulator required" — do not state as settled fact beyond the source (aicompanionguides.com/blog/replika-review/). Italy Feb-2023 ban is double-sourced (nordvpn + aicompanionguides). Satisfies the compliance rule; not overstated. Caution to pass downstream: both regulatory claims rest on reviewer blogs, not primary FTC/Garante documents — keep the "complaint alleged" framing, do not harden it.

**5. [HIGH] The three "surprising findings" are dressed-up table-stakes.** (a) Candy AI "won't tell you if any of it is encrypted," (b) billing appears as "Everai," (c) "does not sell data in the traditional sense but may train on aggregated/anonymized chats" — all standard category facts. All three rate `dressed-up-table-stakes`. The genuinely ownable beat (first-party provider citing its own published policy line-by-line) is present as the "information gain" but is positioning, not a research finding. The writer should not market these three as revelations.

**6. [LOW] Strongest competitor angle IS captured with a beat-plan.** Strongest SERP angle = skywork.ai's explicit cross-competitor comparison (pos 7) + scribehow's safety-comparison table (pos 3). Dossier names both and gives a concrete beat: 2-platform → four-named-platform table with first-party policy citation (lines 98–99, 127). Captures HOW to beat it, not merely that it exists.

**7. [LOW — correct] BEAT SPEC is right for a concise GEO answer page.** Lines 93, 123–134 explicitly override the ~3,400-word SERP modal, fix 1,100–1,600 words, the 4-column table, exactly-5 checklist, 6-Q FAQ (≤50 words each), CTA. Does NOT push toward SERP length. Correct shape.

**8. [LOW] Skipping OpenRouter deep-research does not materially weaken this dossier.** Brief supplies canonical cited sources; SERP top-4 UGC supplied VOC signal; dossier honestly declines to fabricate user quotes (line 115). The four locked table facts would not change.

**9. [LOW] Brand-ownable material is sufficient, not generic.** First-party policy specifics (TLS/SSL in transit + at rest, no card storage, deletion rights, 18+ verification, Section 8) plus three live internal links and reusable voice modules from `2-reference`.

## What works

First-party sourcing discipline is exemplary — every external claim routes to a named URL, the Candy AI price is explicitly fenced as a non-ours third-party figure, the FTC item is pre-attributed as an allegation, and the Pleasur.ai facts carry URL + fetched-this-run + policy-date trace. The hardest thing to get right on a competitor + adult-adjacent page, and the dossier nails it.

## Verdict: **PASS**

No CRITICAL findings: no unsourced load-bearing stat, no overstated regulatory claim, no missing competitor angle, no JSON keys contradicting prose on a load-bearing figure, no own-product or competitor price/feature claim lacking an adequate live first-party trace. The one real defect — trustworthy 90-vs-70 prose/JSON mismatch — is MEDIUM (that volume is never load-bearing). Downstream writer should: reconcile the trustworthy figure before any volume callout, keep the FTC "complaint alleged" framing, and not sell the three table-stakes facts as surprises.
