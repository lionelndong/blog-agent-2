# Visuals Adversarial Review — what-is-an-ai-girlfriend

**Reviewer:** Skeptical art director (adversarial pass)
**Date:** 2026-05-07

## Computed metrics

| Metric | Value |
|---|---|
| Estimated word count | ~3,300 words |
| Density target (>3k words) | 12 |
| Acceptable range | 10–15 |
| Captured visuals (status=captured) | 12 |
| Distinct types | 5 (chart, image, external, action-shot, screenshot) |
| Type diversity target met (≥3) | Yes |

---

## Findings

### [MEDIUM-1] External selectors are heading-only — visuals likely show article titles, not evidence

Visuals 4, 7, 9, and 10 all use selectors targeting a heading element (`h2:first-of-type`, `article h1`, `.contents-headline`, `.faculty-publication-title`). A captured article headline is not evidence — it's a link citation that happens to be rendered as an image. Visual 6 (Harvard HBS) captured 72 KB and visual 10 (EU Council) only 39 KB, both consistent with a single-line text clip rather than a meaningful chart, table, or pull-quote. The `sub=news-quote` label implies a quoted passage; a headline is not a quote. Four of the five externals likely deliver near-zero information lift over a plain hyperlink. Swap selector to the actual cited paragraph, figure, or chart element, or replace with inline blockquote text and mark `type=none`.

**Affected:** visuals 4, 6, 7, 9, 10 (five of twelve captured slots)

---

### [HIGH-2] "Common misconceptions" section has no structural visual — 400+ words, one weak external

The "Common misconceptions" section is the longest H2 in the article (~400 words, three distinct myths), and its only visual is external-9 (Japan Times headline). The headline covers only the Loverse tangent — the two heavier myths ("Is it cheating?" and "Will it replace women?") get no visual support. A `table` contrasting myth vs. reality for all three would be the exact right type here per the decision sequence (compare N things across M dimensions). The current state leaves the densest rhetorical section visually bare.

---

### [MEDIUM-3] Visual 11 (action-shot) may be over-typed — static landing page qualifies for screenshot

The action-shot for `pleasur.ai/create` (visual 11) describes: "Dismiss the age verification dialog. Wait for the templates / character-creator landing state to load." A single modal dismissal is explicitly called out in the editorial principles as something the static dispatcher handles automatically (`screenshot`: "Optional: a single age-gate or cookie banner dismissal is needed — the static dispatcher handles those automatically"). The `action-shot` designation adds routing overhead and slower capture for what is likely a one-click dismiss. Should be reclassified as `screenshot` unless the creator flow requires multi-step interaction beyond the age gate.

---

### [MEDIUM-4] External-4 (Pinecone) selector clips to first H2, not the memory diagram

Visual 4 targets `.blog-content h2:first-of-type` on the Pinecone LangChain memory article. The article contains architecture diagrams and flow illustrations that would actually show the memory architecture the prose describes. Capturing only the section heading yields no more information than the prose hyperlink already conveys. The selector should target a figure or diagram element within the article, or this slot should be replaced with a `chart` showing the memory-window size range (5K–20K chars) cited in the body.

---

### [LOW-5] Chart-1 (Replika engagement) is a two-bar chart of two numbers — high overhead for low payload

Visual 1 (chart) renders two data points: 25% and 60%. Both numbers appear verbatim in the article's opening sentence. A two-bar chart adds no structural insight beyond what the sentence already delivers — there is no trend, no distribution, no comparison across more than two items. The data would be better served as an inline callout or a `table` (if adding a third comparison row, e.g. MAU base). A chart type is warranted when the visual form adds comprehension; here it competes with the prose rather than extending it.

---

### [LOW-6] "If you want to try one" section has two visuals but only one earns its place

The section places visual 11 (action-shot of Companion Creator) and visual 12 (screenshot of `/generate` tool) in close succession. Visual 11 is the correct primary for this CTA section — it shows the product the reader is being directed to. Visual 12 (the image generation tool) is discussed only in a blockquote tip, not in the main prose. Placing a full screenshot on a feature mentioned only in a tip box is borderline decorative — the tip functions as a low-commitment aside, not a section claim that demands evidence.

---

## Visuals that genuinely earn their place

**Visual 3 — layered architecture diagram (image, index 3).** This is the clearest example of a visual earning its slot. The prose describes five stacked components across multiple paragraphs. The labeled vertical stack (LLM → Persona → Memory → Voice → Image Gen) lets a skimming reader grasp the architecture in two seconds. The prose and diagram are genuinely complementary — neither is redundant.

**Visual 5 — experience arc timeline (image, index 5).** The "week one vs week four" section hinges on a fork-in-the-road metaphor. The horizontal timeline with diverging arrows at Week 3 makes the branching structure scannable. It's exactly the kind of concept-illustration the editorial principles call for: a labeled diagram that conveys the mental model faster than the surrounding paragraphs.

---

## Verdict: PASS

Density is exactly at target (12/12). Type diversity passes (5 distinct types). No visual actively hurts the article. CRITICAL count: 0.

The main risks are quality of external captures (selectors too shallow to deliver real evidence) and one chart that competes with the prose instead of extending it. These are HIGH/MEDIUM findings that should be resolved before publication but do not trigger a FAIL under the defined criteria.

**Open issues requiring action before publish:**
- Reselector or replace visuals 4, 6, 7, 9, 10 (external heading clips)
- Add a `table` (myth vs. reality) to the Common Misconceptions section to replace the missing structural visual
- Reclassify visual 11 from `action-shot` to `screenshot` if the age-gate is the only interaction
