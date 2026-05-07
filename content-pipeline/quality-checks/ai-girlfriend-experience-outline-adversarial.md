# Outline Adversarial — ai-girlfriend-experience (Pass 1)

## Verdict: **PASS**

Pass 1 of 2 (revision budget BLOG_AGENT_OUTLINE_REVISION_BUDGET=1).

## Findings

### CRITICAL

- _None._ No structural defects severe enough to make the resulting article worse than the SERP top-5 or violate brand-config guardrails. MECE holds, BLUF is present on every H2, the three-act spine is exactly the angle the research dossier prescribed, and visuals are tied to load-bearing claims rather than decoration.

### HIGH

- **§3 Act 2 (line 56–62) packs three distinct arguments under one BLUF.** The section's BLUF is about "compulsive open-the-app behavior," but the section then asks the reader to absorb (a) image generation as a hook, (b) memory as a silent gating function, and (c) the privacy floor + Mozilla/Muah evidence. That last beat is doing the heaviest lifting in the dossier — the privacy stat is one of the three "Surprising Findings" — and burying it in a tri-purpose section is the most likely place this draft will read as muddled. Either narrow Act 2 to engagement/memory and split privacy out, or rewrite the BLUF to telegraph "engagement is real, but week one is also when the privacy bill comes due." As written, the §3 visual (Mozilla headline) cues the privacy beat, but the BLUF doesn't.
- **§4 Act 3 mixes diagnosis with a Pleasur.AI roadmap tease (line 80) inside the same section.** The section's value is the "six phrases that break the illusion" — the cleanest piece of analysis in the outline. Pivoting mid-section to "Pleasur.AI is rolling out voice + call this week" risks both (a) diluting the diagnosis with vendor framing the reader doesn't expect there, and (b) violating brand-config's `coming-soon` rule about "tease, don't demo" if the prose drifts even slightly toward demo. Move the voice/call tease to the conclusion or §5 where the platform-agnostic-tests frame absorbs it more naturally.
- **No section explicitly answers "is it healthy / will I get attached?" — the MIT × OpenAI study is cited but used as a stat, not as a section anchor.** Research dossier Theme 4 ("Is it safe / healthy?") is one of the four reader-question themes the SERP all cover. The outline folds the MIT RCT into §4 as a sentence (line 79). That works as a citation but leaves the "should I worry about getting attached" reader question structurally unanswered. SERP top-5 covers ethics/healthiness in dedicated sections; this outline's argument that it's subsumed under the week-three diagnosis is defensible but thin.

### MEDIUM

- **§1 BLUF (line 28) is two sentences glued with an em-dash and a parenthetical.** It reads as one idea but eats ~50 words before the reader can parse "what 'experience' means." Trim to one assertion: the rest can move into the bullets. Brand-config flags em-dashes-as-filler; this one is borderline meaningful but reads as filler on a skim.
- **Intro hook (line 16) is strong but front-loads two source citations in the same sentence**, which is unusual for the brand voice (short, direct). Consider citing once in-line and parking the second source as a footnote-style aside. Risk is the reader bouncing on a citation-dense opener.
- **§5's five tests (lines 93–97) overlap with §4's six phrases.** Test #3 ("'I'm here for you' count") is literally one of the six phrases from §4. That's not a MECE violation strictly — §4 names the patterns, §5 turns them into checks — but the prose has to be careful not to re-list. Flag for the drafter.

### LOW

- **§4 visual (chart, line 83) is the strongest in the outline but the section already names the "28M → 20M" numbers in the BLUF and again in the evidence bullet.** Three appearances of the same datapoint within one section is heavy. Cut one prose mention so the chart earns its space.
- **Conclusion (line 110) has two CTAs.** The simulator link and the Companion Creator link are both reasonable, but two CTAs in a 120-word conclusion split reader attention. Pick one primary.

## What Works

- **§4's "six templated phrases" frame (lines 70–78) is the article's moat.** It's the angle the dossier identifies as "actually-surprising / SERP regular hasn't seen it primary-cited," and the outline commits to enumerating the phrases rather than gesturing at "memory degrades" abstractly. That single section is what makes this outline beat the SERP top-5 instead of matching them. The chart visual is correctly placed and earns its spot.

## Recommendation

- Verdict is PASS — advance to stage 4 (`/product-mentions`).
- HIGH findings should be addressed during drafting (§3 BLUF tightening, §4 voice/call tease relocation, optional "is it healthy" structural slot) but do not require a re-outline. The drafter can resolve all three at the prose level without touching the H2 spine.
