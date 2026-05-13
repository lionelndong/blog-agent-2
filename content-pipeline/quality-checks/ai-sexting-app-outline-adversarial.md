# Outline Adversarial — ai-sexting-app (Pass 1)

## Verdict: **PASS**

Pass 1 of 2 (revision budget BLOG_AGENT_OUTLINE_REVISION_BUDGET=1).

## Findings

### CRITICAL

- None. No CRITICAL structural defects. The outline does not duplicate H2s, the picks H2 + "how to pick" H2 are differentiated (picks = per-app verdicts; how-to-pick = a 3-question routing layer that explicitly defers privacy to the next H2), Pleasur.AI is disclosed inline in its own H3 first line, every pick has an honest trade-off, and the brand-config rule on coming-soon Voice/Call is contained to the Pleasur.AI H3.

### HIGH

- **Picks H2 pacing (lines 50–113).** ~1,050 words across one H2 with four H3s plus a footer is a long scroll. The H3s are already structured as separate subsections, so this is recoverable in drafting (anchor links + ample whitespace), but the *risk* is that mobile readers bail before reaching Pleasur.AI's H3. Mitigation: keep H3s visually distinct in the draft (small `Best for:` line under each H3 as a one-glance summary). Not a structural rewrite — a drafting note.
- **"How to pick" risks duplicating the picks H2's `Best for` column (lines 117–128).** Both surfaces answer "which app for which reader." The outline mitigates this by framing how-to-pick as a *decision tree* (build vs pick, chat vs visuals, privacy floor) rather than per-app rehash, and explicitly defers privacy to the next H2. It works *as written* — but if the drafter loses discipline and turns it into "Pick A if you want X, Pick B if you want Y," the section becomes redundant with the table. Flag for `/draft` and `/quality-check`: this section must stay axis-based, not pick-based.

### MEDIUM

- **FAQ Q3 overlap with the picks H2 (lines 174 vs 56, 76, 102).** "Can the AI generate images of itself?" answers a question the comparison table already answers in the Image-gen column. The Q is still worth keeping because it adds the *quota* nuance (OurDream dreamcoins, Pleasur.AI in-chat integration) that the table can't carry — but the drafter needs to make sure Q3 doesn't restate the table; it must extend it.
- **Intro problem framing is on the edge of publisher-side (lines 16–17, 23–25).** "SERP is saturated with 14-app listicles that disclose nothing" is half reader-pain (you waste a week), half meta-complaint about the genre. The hook works because the reader-pain ("waste a week trying apps that won't keep you in the scene") lands first, but the agitate bullet — "three of them turn out to be the same Candy clone behind different brand skins" — is the stronger reader-side line and should lead the agitate sentence in prose, not the affiliate-playbook meta-frame.
- **Privacy bar chart visual (line 145).** Earns its place per the 9-step rule (concrete sourced data, supports BLUF rather than replacing it, no other section uses it), and the 5 Mozilla numbers benefit from a one-glance horizontal bar. *But* the section already quotes all 5 numbers inline in the same paragraph — the chart's marginal value over the prose is real but modest. Keep it; the table-plus-chart pairing is the article's structural backbone for the SERP differentiation. Flag for visuals-adversarial to confirm the bar chart pulls weight over a simpler inline number callout.

### LOW

- **Word budget math (line 234).** Budget summary table totals 2,610, with the note "trim during draft to land at 2,200–2,400." Better to lock the targets at 2,200 inside the outline (trim the picks H2 from 1,100 → 950 or the privacy H2 from 280 → 240) rather than push the trim decision to the drafter, who tends to over-write when given headroom.
- **Type diversity below density-target bar (line 201).** 2 types (table + chart) vs the ≥3 target in editorial-principles-visuals.md. The outline acknowledges this and cites the context file's ≤3 cap as the override, which is defensible — flagging for visuals-adversarial to confirm, not blocking the outline.

## What Works

- **Pleasur.AI placement + disclosure (lines 94–108).** Last in the lineup, with the disclosure paragraph as the first line of the section body, is exactly the trust move the context file asked for. The trade-off ("no permanent free tier; build-flow takes a few minutes more than picking a pre-built") is a real concession, not a fake one — that line is what separates this from the MyAnima-ranking-itself-#1 pattern the privacy section calls out. The whole article hinges on this section reading honest; it does.

## Recommendation

- Verdict is PASS. Advance to stage 4 (/product-mentions). The HIGH findings (picks H2 pacing, how-to-pick discipline) are drafting concerns, not structural rebuilds, and should be flagged in the product-mentions notes or carried into /quality-check as watch-items. No re-dispatch of /outline needed.
