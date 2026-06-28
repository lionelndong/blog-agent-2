# Outline — AI Companion Memory: How It Works and How to Test It

## Beat spec (restated from 1-research/ai-companion-memory.md — binding)
- **Target word count:** ~3,400 words (±15%; floor 3,000, cap ~3,900). Section targets below sum to ~3,400 body + ~300 intro/conclusion.
- **Format DEVIATION (justified):** SERP modal is *ranked listicle* (4 of 5 pages rank 6–9 apps). **We deviate to an explainer PILLAR.** Justification: the brand published a dedicated app-ranking listicle — [ai-companion-best-memory](https://pleasur.ai/blog/ai-companion-best-memory) — on 2026-06-19; shipping a second ranked-app listicle into the same cluster is **keyword cannibalization**. The SERP's depth leader (affiny, 4,524 words) **is itself an explainer**, so the explainer lane is SERP-validated. This pillar wins the mechanics / test-protocol / privacy lanes the listicles skip and **links down** to the ranking sibling for the full app list — strengthening topical authority instead of splitting it.
- **Item count:** a *compact* 5-app comparison table (not the ≥10 ranked list — that intent is owned by the sibling). The compare section's job is orientation + a link down, not a ranking.
- **Comparison table:** REQUIRED (parity) — memory-feature comparison, 5 apps.
- **Hands-on test protocol:** REQUIRED — a repeatable, scored memory-test scorecard (the #1 information-gain asset).
- **Consensus must-cover:** (1) what memory is / short vs long-term; (2) which apps remember best; (3) how to test memory; (4) memory limits & failure modes; (5) privacy/storage of memory data. All mapped below.
- **Information gain (ship 3):** [GAIN-1] reader-runnable scored memory-test scorecard; [GAIN-2] honest "how memory really works vs marketing" mechanics (context window vs persistent store, real failure triggers); [GAIN-3] privacy-of-memory checklist.
- **Compliance:** 18+ framing; NO "unlimited / forever / never forgets" absolutism; privacy is a design *priority*, not a guarantee; no real-person likenesses; no internal-stack tool names in prose.

## Title
**AI Companion Memory: How It Works and How to Test It (2026)** (51 chars; primary keyword first)

## Thesis
AI companion "memory" isn't one feature but four distinct layers — and knowing which layer an app actually uses, plus a 5-minute test to verify it, is the only reliable way to tell whether a companion will really remember you.

## Content type
Explainer pillar (see justified deviation above). Skeptical, test-it-yourself voice; honest competitor concessions before any Pleasur.AI edge.

---

## Intro (~180 words)
- **Hook:** Most "AI companion with memory" claims are marketing — almost none tell you *what kind* of memory, how many turns it survives, or what makes it forget. (Specific, contrarian; not "in today's world".)
- **Thesis** (above).
- **Preview:** You'll get the four-layer model of how companion memory works, the failure modes nobody advertises, a 5-minute test you can run on any app, a compact comparison, and the privacy trade-off of being remembered.
- **Visuals:** Visual 1: {type: image, sub: concept-illustration, prompt: a clean labeled diagram showing a single conversation flowing into four stacked memory layers (context window → saved facts → pinned notes → long-term understanding), minimalist editorial style, no text-heavy clutter, safe-for-work, no human likeness, sfw}

## H2 1 — The four types of AI companion memory [consensus #1; GAIN-2 begins]
- **BLUF:** AI companion memory is really four different mechanisms — context window, a saved-fact list, pinned notes, and persistent long-term understanding — and most apps only do one or two well.
- **Key points:**
  - Context window = short-term "RAM": everything in the current conversation, lost or summarized when it overflows.
  - Saved-fact list = explicit key facts the app stores (your name, preferences) and re-injects.
  - Pinned notes = user-controlled facts you tell it to always remember.
  - Persistent long-term understanding = an evolving model of who you/the character are, across sessions.
- **Evidence:** Brand "four types of memory" framework (2-reference; from ai-companion-best-memory). Reuse this taxonomy verbatim in spirit — it's the brand's signature explainer; link to it.
- **Word target:** 600
- **Transition:** These four layers explain the thing every user eventually hits — your companion forgetting something it "knew." That's next.
- **Visuals:** Visual 2: {type: table, what: the four memory types — Type | What it stores | Lasts across sessions? | Who controls it}; Visual 3: {type: image, sub: concept-illustration, prompt: side-by-side comparison illustration of "short-term context window" as a sliding window over a chat vs "long-term store" as a saved profile card, editorial diagram, sfw, no human likeness}

## H2 2 — Short-term vs long-term memory: why your companion forgets [consensus #1+#4; GAIN-2]
- **BLUF:** Companions forget for predictable reasons — the context window fills and older turns get dropped or lossily summarized, and anything never promoted to long-term storage is gone at the next session.
- **Key points:**
  - The context-window cap and the "sliding window" effect; long chats silently lose their oldest details first.
  - Summarization loss: what survives is a compressed gist, not the exact fact.
  - Session boundaries: context-only apps (e.g. Character.AI historically) reset between chats.
  - Marketing says "persistent memory"; reality is bounded — name the gap honestly. No app remembers everything forever.
- **Evidence:** Deep-research coverage gap (1-research §4): outlets never quantify retention/degradation/failure triggers. Honest competitor framing: Character.AI = context-window only.
- **Word target:** 500
- **Transition:** If memory is this variable, you can't trust a spec sheet — you have to test it. Here's how.
- **Visuals:** Visual 4: {type: external, selector: a representative public Reddit/forum thread of users reporting "why did my AI companion forget X", quote the documented complaint pattern, no PII}; Visual 5: {type: image, sub: concept-illustration, prompt: diagram of a context window as a fixed-width frame sliding right over a long message log, oldest messages falling out of frame, labeled, sfw}

## H2 3 — How to test an AI companion's memory in 5 minutes [consensus #3; GAIN-1]
- **BLUF:** You can score any companion's memory with one repeatable test: tell it a specific, unusual fact, leave and return in a new session days later, and check whether it raises the detail unprompted.
- **Key points:**
  - The protocol: plant a specific detail → continue ~30+ turns AND/OR start a fresh session 2 days later → score recall as Remembered / Partial / Forgot.
  - Run it three ways: same-session recall, new-session recall, and contradiction handling (does it update when you correct a fact?).
  - A scorecard table the reader can copy.
  - Caveat: results vary by tier and by how you phrase the fact — note it.
- **Evidence:** Brand "fast check" test (2-reference). MariaVibe 82%/7-day recall data point (from openmind-ai-vs-pleasurai) as a benchmark reference for what "good" looks like.
- **Word target:** 550
- **Transition:** With a test in hand, here's how the major companions actually stack up.
- **Visuals:** Visual 6: {type: table, what: the memory-test scorecard — Test | What to say | When to check | Score (Remembered/Partial/Forgot)}; Visual 7: {type: chart, sub: bar, what: illustrative recall-rate-by-delay reference (e.g., the 82% / 7-day benchmark) — sourced, labeled as a reference point not a universal stat}

## H2 4 — Which AI companions remember best (and how they differ) [consensus #2; compact compare + link-down]
- **BLUF:** No single app wins on every memory layer — Nomi leads on factual recall, Replika on persistent emotional continuity, Character.AI is mostly context-only, and Pleasur.AI is built around across-session persistence for sustained roleplay.
- **Key points:**
  - Compact 5-app comparison on the memory dimensions that matter (memory type, across-session recall, user control, notable limit). Honest concessions first.
  - This is orientation, not a ranking — **link down** to [ai-companion-best-memory](https://pleasur.ai/blog/ai-companion-best-memory) for the full tested ranking, and to [best-replika-alternative-2026](https://pleasur.ai/blog/best-replika-alternative-2026) / [openmind-ai-vs-pleasurai](https://pleasur.ai/blog/openmind-ai-vs-pleasurai).
- **Evidence:** Honest competitor framing (2-reference): Nomi factual / Replika persistent-emotional / Character.AI context-only / Pleasur.AI persistent across-session. Independent 7.6/10 review naming memory Pleasur.AI's strength.
- **Word target:** 550
- **Transition:** Whichever you pick, being remembered has a cost most reviews ignore — your data.
- **Visuals:** Visual 8: {type: table, what: App | Memory type | Across-session recall | User-editable memory | Notable limit — 5 rows: Nomi, Replika, Character.AI, Pleasur.AI, +1}

## H2 5 — The privacy side of memory: what gets stored to remember you [consensus #5; GAIN-3]
- **BLUF:** For a companion to remember you it must store your conversations somewhere — so the real privacy question isn't "does it remember" but "where does that intimate memory live, how long, and can you delete it?"
- **Key points:**
  - Memory = stored data = an attack/retention surface, especially for adult roleplay.
  - A reader checklist: where is it stored, is it encrypted, retention period, deletion-on-account-close, is memory exportable/editable.
  - Pleasur.AI's positioning: privacy-conscious architecture as a design *priority* (not a guarantee). State as our own commitment; link to safety checklist.
- **Evidence:** Deep-research gap (1-research §4): privacy of persistent intimate memory systematically ignored by SERP. Link [ai-companion-safety-checklist](https://pleasur.ai/blog/ai-companion-safety-checklist).
- **Word target:** 450
- **Transition:** Privacy and persistence both cost compute — which is why strong memory is usually a tiered resource.
- **Visuals:** Visual 9: {type: image, sub: concept-illustration, prompt: a clean privacy checklist card listing memory-storage questions (stored where / encrypted / retention / deletion / editable), editorial UI style, sfw, no human likeness}

## H2 6 — What "persistent memory" really costs: tiers and limits [consensus #4]
- **BLUF:** Strong long-term memory isn't free — it's compute-heavy, so most companions gate memory quality behind paid tiers or a usage economy rather than offering "unlimited" recall.
- **Key points:**
  - Memory as a metered/tiered resource; "priority memory processing" style differentiators sit on higher tiers.
  - Honest: no tier is truly unlimited; media and persistence are metered.
  - Pleasur.AI live pricing context (Starter $12.99 / Standard $27.99 / Ultimate $49.99; coin economy) — first-party fact lock from research.
- **Evidence:** 1-research §3 first-party pricing; deep-research tier-gated "priority memory processing" note.
- **Word target:** 400
- **Transition:** So how do you actually get a companion that holds onto what matters? Build it deliberately.
- **Visuals:** Visual 10: {type: screenshot, target: pricing, what: Pleasur.AI tier/coin overview showing memory sits in a metered economy, annotate: highlight the tier column}

## H2 7 — How to build a companion that remembers you [practical; product-led]
- **BLUF:** The most reliable memory comes from setting the character up once — consistent backstory, pinned key facts, and reinforcing details over time — so the long-term layer has something stable to hold.
- **Key points:**
  - Build the character once in the [AI Companion Creator](https://pleasur.ai/create); personality/backstory/preferences persist across sessions.
  - Use saved facts / pinned notes deliberately; reinforce details; correct contradictions early so the model updates.
  - Re-run the 5-minute test after a week to confirm.
- **Evidence:** 2-reference product-led module (Companion Creator; "she stays that character").
- **Word target:** 350
- **Transition:** (to conclusion)
- **Visuals:** Visual 11: {type: screenshot, target: create, what: Companion Creator showing where character backstory/preferences are set, annotate: arrow on the backstory/preferences field}

## Conclusion (~120 words)
- **Restate thesis (fresh framing):** Memory is the difference between a chatbot and a companion — but it's four layers, not a slogan, and the only proof is the test you run yourself.
- **Next step:** Run the 5-minute test on your current app; if it fails the new-session check, see the full tested ranking in [ai-companion-best-memory](https://pleasur.ai/blog/ai-companion-best-memory).

---

## Coverage map (consensus topic → section)
| Consensus topic (beat spec) | Section |
|---|---|
| What memory is / short vs long-term | H2 1 + H2 2 |
| Which apps remember best | H2 4 (compact + link-down) |
| How to test memory | H2 3 [GAIN-1] |
| Memory limits & failure modes | H2 2 + H2 6 |
| Privacy / storage of memory data | H2 5 [GAIN-3] |
| Honest mechanics vs marketing | H2 1 + H2 2 [GAIN-2] |

## Beat-spec self-check
- [x] Section word targets sum to ~3,400 body (600+500+550+550+450+400+350 = 3,400) + ~300 intro/concl → within target ±15%.
- [x] Item count: compact 5-app table (justified deviation from ≥10 — cannibalization; full list owned by sibling).
- [x] Every consensus topic in coverage map.
- [x] 3 `[GAIN]` assets present (scorecard, honest-mechanics, privacy checklist), none on SERP page 1.
- [x] Comparison table specced (H2 4).
- [x] Visual count 11 (target 12, range 10–15 for >3k words); types: image, table, external, chart, screenshot = 5 distinct (≥3). ✔
- [x] MECE: 7 H2s, no overlap (forgetting=H2 limits-mechanics; cost=H2 tiers; build=H2 practical — distinct).
