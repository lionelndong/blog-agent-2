# BLUF + MECE Outlining Rules

These are the structural rules every outline must follow. The `outline` skill checks each rule before saving.

## BLUF — Bottom Line Up Front

Every section opens with the most important sentence. The reader should learn the answer first; supporting detail comes after.

**Bad (buries the lede):**
> Keyword cannibalization has been a topic of debate among SEO professionals for years. Some argue it's a myth, while others claim it can devastate rankings. In this section, we'll examine what it really is.

**Good (BLUF):**
> Keyword cannibalization is when two or more pages on your site target the same keyword and intent — and end up competing with each other in Google's results.

The lead sentence carries the punchline. Skim-readers get the answer. Detail-readers keep going.

In the outline, this means **every H2 has a one-sentence "BLUF" field** that becomes (or directly informs) the section's opening sentence.

## MECE — Mutually Exclusive, Collectively Exhaustive

Sections must:

- **Not overlap** — no topic appears in two sections. If the same idea fits two H2s, you have a structure problem; merge or re-cut.
- **Together cover the topic** — a reader who reads only the H2 list should know what the article covers without obvious gaps.

A quick MECE test: write the H2 titles on a single line each, in order, with no other context. Does the list read as a complete map of the topic? If you imagine asking a domain expert "what's missing?" — what would they say?

## Thesis support

The article has one thesis (the one-sentence position). Each H2 must support it — directly or by laying foundational context.

Test: read just the H2 titles in order. Do they argue for the thesis? Or do some feel like detours?

## Section count

Most articles work best at **4–7 H2 sections**. Fewer than 4 means each section will be too long. More than 7 means the article reads as a list, not an argument.

## H3 use

Use H3s only when an H2 has 2+ distinct sub-ideas that benefit from separation. Don't add H3s to look "structured." Prose can do the work without sub-headings most of the time.

## Section length targets

Default: ~250–400 words per H2. Adjust if a section earns more (deep example, table, walkthrough). Note the target word count next to each H2 — the `draft` skill uses this.

## Hook + thesis + preview (the intro)

The introduction has three jobs:

1. **Hook** — open with a hook that earns attention. Options: contrarian observation, surprising stat (cited), opinionated statement, problem-statement that names the reader's pain. Avoid "in today's world" / "more than ever" openers.
2. **Thesis** — state the article's one-sentence position.
3. **Preview** — one sentence telling the reader what they'll get out of reading on. Not a TOC dump. A promise.

Aim for 150–200 words on the intro.

## Conclusion

The conclusion has two jobs:

1. **Restate the thesis** — same idea, fresh framing. Not a recap.
2. **One next step** — what should the reader do now? Link to a resource (often a brand article from `brand-reference`).

Aim for 80–150 words. No "in conclusion" or "to summarize" openers.

## Per-section fields the outline must include

For each H2 the outline file must specify:

- **BLUF** — the one-sentence opening (becomes / informs the section's first sentence)
- **Key points** — 2–4 bullets covering what the section will cover
- **Evidence** — what stat, quote, example, or screenshot supports the section
- **Transition** — how this section flows into the next
- **Visual** — should this section have a table, screenshot, or chart? Note the type.

## Self-check before saving

- [ ] Each H2 has a BLUF that could lead the section
- [ ] No two H2s cover the same idea
- [ ] H2 list (alone) reads as a complete map of the topic
- [ ] Each H2 supports the thesis
- [ ] Total of 4–7 H2s
- [ ] Intro has hook + thesis + preview
- [ ] Conclusion has restated thesis + next step
- [ ] Word counts noted per section
- [ ] Visual / evidence noted per section
