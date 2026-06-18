# Outline Adversarial — how-to-choose-an-nsfw-ai-companion (Pass 2)

## Verdict: **PASS**

Pass 2 of 2 (revision budget BLOG_AGENT_OUTLINE_REVISION_BUDGET=1).

Re-verification after the stage-3 revision that addressed a prior FAIL.

## Prior FAIL items — re-verification

- **(was CRITICAL) 8 scorecard rows vs collapsed ~6-section spine** — RESOLVED. Scorecard table (lines 79–86) has 8 rows; outline now has 8 matching criterion H2s (lines 90–206) in the same order. Not re-flagged.
- **(was HIGH) pricing 3–4×/token-overage stat uncommitted** — RESOLVED. Committed hard at lines 153–154 ($12.99 monthly vs $5.99 annual = 2.2×; +$15–25/mo tokens; 3–4× net). Not re-flagged.
- **(was HIGH) over-dense decorative visuals** — RESOLVED. Trimmed to 6 visuals, six removals logged at line 271. Not re-flagged.

## Findings

### CRITICAL

- None.

### HIGH

- [scorecard BLUF line 66 vs table line 79] The BLUF enumerates nine nouns ("chat realism, memory, customization, media, adult range, price, privacy, age verification, platform fit") because memory and chat-realism are split out, but the table and Criterion 1 (line 90) fuse them into one row, delivering eight. The drafter inherits an internal count contradiction and will either expand prose to nine (breaking table parity) or silently drop a noun. Restate the BLUF to name eight criteria matching the rows.

### MEDIUM

- [Criterion 3 media / lines 124–126] Outline correctly demonstrates only the live Image Generation product, but brand-config marks Voice/Call as coming-soon. The "voice/video are category context, not a Pleasur.AI walkthrough" guardrail currently lives only in the research dossier. Add it to the C3 stub so the drafter doesn't drift into a coming-soon walkthrough.
- [coverage map / lines 225–235] Research splits consensus topic 1 ("differs from mainstream / won't get refused") from topic 6 ("uncensored as the *core draw*"). The map routes range to Criterion 4 and the definition to the "What it is" H2 (lines 51–52), but the "why someone leaves Character.AI" *draw* framing is only implied. Soft gap — drafter should consciously place the core-draw beat or the definition reads motiveless.

### LOW

- [Visuals 4 & 5 / C2, C3] Two Pleasur.AI screenshots in back-to-back sections. Allowed (different UIs) but edges toward promotional density in a "don't sell" article. Surrounding prose must stay evaluative, not promotional.
- [Visual 2 concept diagram / line 58] Mainstream-vs-companion side-by-side barely clears 9-step rule step 6 (concept is two sentences of prose). Defensible as the section's one anchor and adds skim value — keep it, but it's the first cut if density needs trimming.

## What Works

- [Criterion 5 pricing / lines 149–161] The information-gain spine: committed headline stat, conflicting category figures mapped, a sourced grouped-bar chart wired to exact numbers (so render_chart.py won't fall back to manual), and a practical 5-minute test. Side-by-side with the SERP comparison pages, this is the section the reader keeps — exactly the beat spec's intent.

## Recommendation

- Verdict is PASS — advance to stage 4 (/product-mentions). Fold the HIGH BLUF count fix and the two MEDIUM guardrails into the product-mentions / draft brief; none require re-running /outline.
