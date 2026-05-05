# Voice Guide

These are guardrails. The source of truth for voice is the actual prose in `examples/`. **Read 2 example articles before drafting** — that's not optional.

## Voice in one paragraph

Direct, second person, evidence-led. Conversational without being chatty. Short sentences that vary in rhythm. Practical examples beat abstract claims. The reader is competent — don't over-explain. Don't sell — demonstrate. Strong opinions, lightly held, with reasons.

## Sentence-level rules

- **Short by default.** Long sentences are fine — but earn them. Don't run two ideas together with a comma when a period works.
- **Vary rhythm.** Three medium sentences in a row reads flat. Mix.
- **Active voice.** "Google ranks pages" not "Pages are ranked by Google."
- **Concrete subjects.** Replace vague subjects ("there are many things") with specific ones ("most blogs make three mistakes").
- **Cut filler.** Drop "very", "really", "quite", "actually", "basically", "essentially", "simply", "just" — almost always nothing is lost.
- **Prefer common words.** "Use" not "leverage." "Look at" not "delve into." "Help" not "facilitate."

## Paragraph-level rules

- **1–4 sentences.** Single-sentence paragraphs are fine for emphasis. Avoid wall-of-text paragraphs that exceed ~80 words.
- **One idea per paragraph.** If the paragraph contains two distinct ideas, split it.
- **Show with examples.** Every other paragraph should contain a concrete example, number, screenshot reference, or named tool. Abstract claims without examples sound like AI.

## Section-level rules (BLUF)

- **Lead with the answer.** The first sentence of a section is the most important sentence in the section. Treat it that way.
- **Then unfold.** Supporting context, examples, and nuance follow.
- **Don't introduce the section.** No "In this section we'll look at…" or "Now that we've covered X, let's…" Just start.

## Article-level rules

- **Inverted pyramid.** Most important info first. The reader who only reads the intro and the first sentence of each H2 should still get the gist.
- **Hook first.** No throat-clearing. The first sentence of the intro is your audition.
- **Demonstrate; don't sell.** When you mention a product, show it doing the thing. Don't list features.
- **Cite numbers.** Every numerical claim needs a hyperlinked source. The `verify-claims` skill enforces this — but write it that way to begin with.

## Forbidden patterns (the AI tells)

These are listed in `brand-config.md` and they're the most common ones. Re-read that list before drafting. The big offenders:

- "In today's [adjective] world / landscape / digital age"
- "Leverage", "delve", "navigate the complexities of", "unlock the power of"
- "Game-changer", "revolutionize", "elevate your..."
- "It's important to note that…"
- "When it comes to X…"
- Three-item parallel lists where every item is a present participle ("Generating…, Optimizing…, Scaling…")
- Em-dashes used as filler. Use them only for genuine asides — like this — not as decoration.
- "Comprehensive guide" in the title or intro
- Any sentence that begins with "Furthermore" or "Moreover"

## What good intros look like

Look at the opening sentence of each `examples/` file:

- "You're here because you need links."
- "A content gap analysis is the process of finding topics your competitors have covered but you haven't."
- "Ninety percent of pages on the internet get no organic search traffic from Google."

Notice: direct, claim-or-fact-first, second-person or third-person, no preamble. The reader knows immediately what they're getting.

## What bad intros look like (to avoid)

- "In the ever-evolving landscape of digital marketing, [topic] has emerged as a critical consideration for businesses looking to stay ahead of the curve."
- "Are you struggling with [topic]? You're not alone. In this comprehensive guide, we'll explore everything you need to know about [topic]."
- "Imagine [scenario]. Now imagine [scenario with stakes]. That's where [topic] comes in."

If your draft has any of these, rewrite from scratch.

## When to break these rules

When breaking the rule serves the reader. The rules exist to remove the most common AI tells; if you have a deliberate reason to write a long sentence or open with a question, do it. Just don't do it by accident.
