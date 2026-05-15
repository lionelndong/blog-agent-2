# Outline Adversarial — how-to-make-an-ai-girlfriend (Pass 1)

## Verdict: **PASS**

Pass 1 of 2 (revision budget BLOG_AGENT_OUTLINE_REVISION_BUDGET=1).

## Findings

### CRITICAL

- _None._ The outline's two-path spine is MECE at the structural level (DIY vs off-the-shelf are non-overlapping by definition), every H2 stub leads with a real BLUF (not a "today's world" throat-clear), the visual map clears the 6–11 density band for a ~2,400-word piece with 4 distinct types, and the comparison table in the off-the-shelf H2 includes Pleasur.AI honestly (with a `—` column for in-chat image gen vs body-customization rather than puffery). No structural reason to halt drafting.

### HIGH

- [H2 "What 'good' actually feels like — and what breaks", lines 78–90] **Stanford-loneliness evidence is structurally misplaced.** The "what breaks at week three" section is a craft/engineering claim (memory layer + voice loops + personality drift), but the only Evidence cited is the Cerit et al. N=1006 loneliness study. Those numbers belong in an "is this for me / ethics" frame — they prove the category does something real long-term, not that vector stores fail at week three. The section's BLUF promises one thing and the evidence proves a different thing. Either (a) cite a SERP/forum thread documenting the actual week-three failure modes (Replika 2023 shutdown beat, Reddit complaints, the sibling `ai-girlfriend-experience` piece's "six phrases that break the illusion"), or (b) demote the Stanford visual to an inline aside and drop a different external clip.

- [H2 "The off-the-shelf path", lines 58–75] **Comparison table risks an honesty hole on Pleasur.AI pricing.** The table columns are `App | Body customization | Voice | In-chat image gen | Monthly price (public)`. Five of the six SERP product pages gate pricing (per research), and the outline says cells will use "research-sourced values; '—' when the platform doesn't disclose." If Pleasur.AI is the only row with a published number while every competitor reads `—`, the table prints as a covert ad, not a comparison. Either source third-party-review pricing for every row the way the prose does for Nomi/Candy, or explicitly note in the table caption that competitor numbers are gated. Marketing-flavored comparison tables are a recurring adversarial flag on this codebase.

- [H2 "Choosing your path", lines 94–105 + Intro lines 22] **Two decision visuals risk MECE overlap.** The intro carries a side-by-side decision diagram ("DIY path | Off-the-shelf path"); the H2 "First decide which 'make' you mean" then carries a six-row decision table comparing the same two paths. These are different *types* (image vs table) but the same *job* (help the reader pick a lane). The outline's own "Visual sanity check" acknowledges the proximity and waves it off. Risk: the reader hits the same MECE choice three times in the first 700 words (diagram → table → prose bullets). Cut the intro diagram, or repurpose it as a four-layer DIY *architecture* tease, so the intro is concept-illustrative and the H2 table is decision-grade.

### MEDIUM

- [H2 "The DIY path", line 54 visual] **DIY architecture diagram has a "memory layer" box but the prose calls memory "the thing every DIY guide skips."** If memory is the wedge the article is selling, the diagram should anchor it visually — currently it's one of four equally-weighted layers. Consider a callout treatment (badge / emphasis label / different fill) on the memory layer so the visual carries the prose's actual argument instead of flattening it.

- [H2 "The off-the-shelf path", line 73 action-shot] **Action-shot goal is fragile.** "Log into Pleasur.AI with the saved session. Open `/create`. Dismiss any age-verification dialog. Pick Realistic. Click through to the personality/archetype step." This is a 4-step chain that has to work first time on a Cloudflare-protected, age-gated product. If state.json is stale or the wizard route name drifts, the visual will fail silently to manual-capture. Worth either (a) splitting into two captures (post-age-gate landing + mid-wizard) or (b) flagging in the notes that the screenshot tool should retry from `/create?step=personality` if the click chain breaks.

### LOW

- [H2 "What 'good' actually feels like…", line 87] **Voice-rendering "glitches on certain words" is unsourced.** The prose will need a concrete example or a forum link in `/verify-claims`; flag now so the draft doesn't ship a generic claim. Same with "personality drifts back to a default helpful-assistant tone every fifth reply" — that's a specific frequency that needs a source or needs softening.

- [Visual placeholders, multiple] **"Brand-neutral colors" prompt phrasing is fine for sub:diagram but means the intro diagram and the DIY diagram will likely render in near-identical palettes.** Consider differentiating one (e.g., intro = warm accent, architecture = cool accent) so they don't read as a matched pair the reader is supposed to mentally compare.

## What Works

- [H2 "The DIY path", lines 41–54] **The "honest off-ramp" paragraph is the article's structural superpower.** Most outlines pretending to cover DIY either lie about its difficulty or bury the off-ramp at the end. This outline names the off-ramp inside the DIY section itself ("If reading the last bullet made you tired, the DIY path is not for you. That is fine.") *before* the reader has invested 500 words. That is the exact move that bridges the SERP's split intent — a competitor has to either preach DIY or sell a product, this outline does neither. Keep that paragraph verbatim through drafting.

## Recommendation

- If Verdict is PASS: advance to stage 4 (/product-mentions).
- If Verdict is FAIL: re-dispatch /outline with the CRITICAL items as the revision brief (orchestrator handles this), then re-run this skill.
