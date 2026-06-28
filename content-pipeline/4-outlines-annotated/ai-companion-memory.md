# Annotated Outline — AI Companion Memory: How It Works and How to Test It

## Pre-flight reconciliation

No contradictions found. The outline mentions no `coming-soon` products (Voice Replies, Phone Call). Only `live` products are annotated below: **AI Companion Creator** (flagship) and **AI Image Generation**. No links to non-existent `/voice` or `/call` pages.

## Beat spec (restated — binding)
- Target ~3,400 words (±15%). Explainer PILLAR (justified deviation from listicle SERP — cannibalization of [ai-companion-best-memory](https://pleasur.ai/blog/ai-companion-best-memory), pub 2026-06-19; the SERP depth leader is itself an explainer). Compact 5-app compare + link-down. Memory-test scorecard REQUIRED. Comparison table REQUIRED. 3 GAIN assets. 18+ framing; no "unlimited/forever/never-forgets" absolutism; privacy = priority not guarantee; no internal-stack tool names; no real-person likeness.

## Title
**AI Companion Memory: How It Works and How to Test It (2026)**

## Thesis
AI companion "memory" isn't one feature but four distinct layers — and knowing which layer an app actually uses, plus a 5-minute test to verify it, is the only reliable way to tell whether a companion will really remember you.

## Content type
Explainer pillar. Skeptical, test-it-yourself voice; honest competitor concessions before any Pleasur.AI edge.

---

## Intro (~180 words)
- **Hook:** Most "AI companion with memory" claims are marketing — almost none tell you *what kind* of memory, how many turns it survives, or what makes it forget.
- **Thesis** (above).
- **Preview:** the four-layer model, the failure modes nobody advertises, a 5-minute test for any app, a compact comparison, and the privacy trade-off of being remembered.
- **Visuals:** Visual 1: {type: image, sub: concept-illustration, prompt: a clean labeled diagram showing a single conversation flowing into four stacked memory layers (context window → saved facts → pinned notes → long-term understanding), minimalist editorial style, sfw, no human likeness}

## H2 1 — The four types of AI companion memory [consensus #1; GAIN-2 begins]
- **BLUF:** AI companion memory is really four different mechanisms — context window, a saved-fact list, pinned notes, and persistent long-term understanding — and most apps only do one or two well.
- **Key points:** context window (short-term RAM); saved-fact list (explicit stored facts re-injected); pinned notes (user-controlled always-remember); persistent long-term understanding (evolving model across sessions).
- **Evidence:** Brand "four types of memory" framework (2-reference; from ai-companion-best-memory). Link to it as the depth source.
- **Word target:** 600
- **Transition:** These four layers explain the thing every user eventually hits — your companion forgetting something it "knew."
- **Visuals:** Visual 2: {type: table, what: Type | What it stores | Lasts across sessions? | Who controls it}; Visual 3: {type: image, sub: concept-illustration, prompt: side-by-side of "context window" sliding over a chat vs "long-term store" as a saved profile card, editorial diagram, sfw, no human likeness}
- **Product mentions:** *Inline mention.* When introducing the 4th layer (persistent long-term understanding), note that this is the layer Pleasur.AI is built around: because you define the character once in the [AI Companion Creator](https://pleasur.ai/create) (appearance, personality, backstory, preferences), there's a stable identity for the long-term layer to hold across sessions. One sentence, not a pitch. Internal-link the taxonomy to [ai-companion-best-memory](https://pleasur.ai/blog/ai-companion-best-memory).

## H2 2 — Short-term vs long-term memory: why your companion forgets [consensus #1+#4; GAIN-2]
- **BLUF:** Companions forget for predictable reasons — the context window fills and older turns get dropped or lossily summarized, and anything never promoted to long-term storage is gone at the next session.
- **Key points:** context-window cap / sliding-window effect; summarization loss (gist not exact fact); session boundaries (context-only apps reset); marketing "persistent memory" vs bounded reality — no app remembers everything forever.
- **Evidence:** Deep-research coverage gap (1-research §4). Honest framing: Character.AI = context-window only.
- **Word target:** 500
- **Transition:** If memory is this variable, you can't trust a spec sheet — you have to test it.
- **Visuals:** Visual 4: {type: external, selector: a representative public Reddit/forum thread of users reporting "why did my AI companion forget X", quote the documented complaint pattern, no PII}; Visual 5: {type: image, sub: concept-illustration, prompt: a context window as a fixed-width frame sliding right over a long message log, oldest messages falling out of frame, labeled, sfw}
- **Product mentions:** *None.* Keep this section vendor-neutral and honest — credibility section. (Over-annotating here would undercut the "we're being straight with you" tone.)

## H2 3 — How to test an AI companion's memory in 5 minutes [consensus #3; GAIN-1]
- **BLUF:** You can score any companion's memory with one repeatable test: tell it a specific, unusual fact, leave and return in a new session days later, and check whether it raises the detail unprompted.
- **Key points:** plant a specific detail → continue ~30+ turns AND/OR fresh session 2 days later → score Remembered/Partial/Forgot; run three ways (same-session, new-session, contradiction handling); copyable scorecard; caveat: varies by tier and phrasing.
- **Evidence:** Brand "fast check" test (2-reference). MariaVibe 82%/7-day recall benchmark (from openmind-ai-vs-pleasurai).
- **Word target:** 550
- **Transition:** With a test in hand, here's how the major companions actually stack up.
- **Visuals:** Visual 6: {type: table, what: memory-test scorecard — Test | What to say | When to check | Score}; Visual 7: {type: chart, sub: bar, what: illustrative recall-rate-by-delay reference (e.g. the 82%/7-day benchmark), sourced, labeled as a reference point not a universal stat}
- **Product mentions:** *Inline mention (light).* Suggest the reader run the test on whatever app they use — and if they want a controllable baseline, a companion built in the [AI Companion Creator](https://pleasur.ai/create) with a fixed backstory makes the new-session recall test easy to set up. One clause; the test stays app-agnostic.

## H2 4 — Which AI companions remember best (and how they differ) [consensus #2; compact compare + link-down]
- **BLUF:** No single app wins on every memory layer — Nomi leads on factual recall, Replika on persistent emotional continuity, Character.AI is mostly context-only, and Pleasur.AI is built around across-session persistence for sustained roleplay.
- **Key points:** compact 5-app comparison (memory type, across-session recall, user control, notable limit), honest concessions first; this is orientation not a ranking — **link down** to [ai-companion-best-memory](https://pleasur.ai/blog/ai-companion-best-memory) for the full tested ranking, plus [best-replika-alternative-2026](https://pleasur.ai/blog/best-replika-alternative-2026) and [openmind-ai-vs-pleasurai](https://pleasur.ai/blog/openmind-ai-vs-pleasurai).
- **Evidence:** Honest competitor framing (2-reference). Independent 7.6/10 review naming memory Pleasur.AI's strength.
- **Word target:** 550
- **Transition:** Whichever you pick, being remembered has a cost most reviews ignore — your data.
- **Visuals:** Visual 8: {type: table, what: App | Memory type | Across-session recall | User-editable memory | Notable limit — rows: Nomi, Replika, Character.AI, Pleasur.AI, +1}
- **Product mentions:** *Inline mention (in-table + one line).* Pleasur.AI's row states its honest edge: persistent across-session memory tuned for sustained adult roleplay, with the character you build in the [AI Companion Creator](https://pleasur.ai/create) persisting between sessions. Concede competitors' strengths first (Nomi factual recall, Replika emotional continuity) before stating the edge. Cite the independent review for E-E-A-T, not self-claim.

## H2 5 — The privacy side of memory: what gets stored to remember you [consensus #5; GAIN-3]
- **BLUF:** For a companion to remember you it must store your conversations somewhere — so the real privacy question isn't "does it remember" but "where does that intimate memory live, how long, and can you delete it?"
- **Key points:** memory = stored data = an attack/retention surface (sensitive for adult roleplay); reader checklist (stored where / encrypted / retention period / deletion-on-close / exportable-editable); Pleasur.AI privacy-conscious architecture as a design *priority* (not a guarantee), stated as our own commitment.
- **Evidence:** Deep-research gap (1-research §4). Link [ai-companion-safety-checklist](https://pleasur.ai/blog/ai-companion-safety-checklist).
- **Word target:** 450
- **Transition:** Privacy and persistence both cost compute — which is why strong memory is usually a tiered resource.
- **Visuals:** Visual 9: {type: image, sub: concept-illustration, prompt: a clean privacy checklist card listing memory-storage questions (stored where / encrypted / retention / deletion / editable), editorial UI style, sfw, no human likeness}
- **Product mentions:** *Inline mention.* Frame Pleasur.AI's privacy-conscious design as a *priority*, explicitly NOT a guarantee — "privacy is treated as a design priority, not a promise no service can make." Link to [ai-companion-safety-checklist](https://pleasur.ai/blog/ai-companion-safety-checklist). Compliance-sensitive: no safety/privacy absolutism.

## H2 6 — What "persistent memory" really costs: tiers and limits [consensus #4]
- **BLUF:** Strong long-term memory isn't free — it's compute-heavy, so most companions gate memory quality behind paid tiers or a usage economy rather than offering "unlimited" recall.
- **Key points:** memory as metered/tiered resource; honest — no tier is truly unlimited, media and persistence are metered; Pleasur.AI live pricing (Starter $12.99 / Standard $27.99 / Ultimate $49.99; coin economy) from first-party fact lock.
- **Evidence:** 1-research §3 first-party pricing; deep-research tier-gated "priority memory processing" note.
- **Word target:** 400
- **Transition:** So how do you actually get a companion that holds onto what matters? Build it deliberately.
- **Visuals:** Visual 10: {type: screenshot, target: pricing, what: Pleasur.AI tier/coin overview showing memory sits in a metered economy, annotate: highlight the tier column}
- **Product mentions:** *Inline mention.* Use Pleasur.AI's real tier/coin pricing as the worked example of "memory is a metered resource." State pricing exactly per fact-lock; do NOT claim any tier is unlimited or that a specific tier guarantees a specific recall length.

## H2 7 — How to build a companion that remembers you [practical; product-led WALKTHROUGH]
- **BLUF:** The most reliable memory comes from setting the character up once — consistent backstory, pinned key facts, and reinforcing details over time — so the long-term layer has something stable to hold.
- **Key points:** build the character once; reinforce/pin key facts; correct contradictions early so the model updates; re-run the 5-minute test after a week.
- **Evidence:** 2-reference product-led module (Companion Creator; "she stays that character").
- **Word target:** 350
- **Transition:** (to conclusion)
- **Visuals:** Visual 11: {type: screenshot, target: create, what: Companion Creator showing where character backstory/preferences are set, annotate: arrow on the backstory/preferences field}
- **Product mentions:** *Walkthrough (primary product section).* Walk through using the [AI Companion Creator](https://pleasur.ai/create): define appearance/personality/backstory/preferences once → that identity persists across sessions, giving the long-term layer a stable anchor. Tie back to the 4-types model (H2 1) and the test (H2 3). Optional one-line: generated images of your companion stay consistent via [AI Image Generation](https://pleasur.ai/generate) (character consistency) — only if it fits naturally; don't force. Keep it demonstrate-don't-sell.

## Conclusion (~120 words)
- **Restate thesis (fresh framing):** Memory is the difference between a chatbot and a companion — but it's four layers, not a slogan, and the only proof is the test you run yourself.
- **Next step:** Run the 5-minute test on your current app; if it fails the new-session check, see the full tested ranking in [ai-companion-best-memory](https://pleasur.ai/blog/ai-companion-best-memory).

---

## Coverage map (consensus topic → section)
| Consensus topic | Section |
|---|---|
| What memory is / short vs long-term | H2 1 + H2 2 |
| Which apps remember best | H2 4 (compact + link-down) |
| How to test memory | H2 3 [GAIN-1] |
| Memory limits & failure modes | H2 2 + H2 6 |
| Privacy / storage of memory data | H2 5 [GAIN-3] |
| Honest mechanics vs marketing | H2 1 + H2 2 [GAIN-2] |

## Product-mention summary
Live products only. Mentions in 5 sections (H2 1 inline, H2 3 light-inline, H2 4 inline+table, H2 5 inline, H2 6 inline) + 1 walkthrough (H2 7, Companion Creator). H2 2 deliberately vendor-neutral. No coming-soon products. Flagship = AI Companion Creator throughout; Image Generation only as an optional single line in H2 7.
