## Pre-flight reconciliation

No contradictions found.

Constraint-reconciliation scan results:
- **Coming-soon products:** none remain in `brand-config.md`. Voice Replies and Phone Call were `coming-soon` on 2026-06-15 but were refreshed to `live` on 2026-06-24 (verified on pleasur.ai/pricing). They are therefore eligible for normal mentions — but neither naturally fits a memory/forgetting article, so neither is annotated below.
- **Roadmap products:** AI Video Generation is `roadmap`. It is NOT referenced anywhere in the outline, and no annotation introduces it. (Compliant with brand-config L66–68: roadmap items only in dedicated future-of-platform posts.)
- **False review-site facts:** the outline's only product mention (H2 5) already frames memory as a bounded capability and explicitly disclaims "$19 plan" / "priority memory processing" / "unlimited." No bullet asserted any of those, so no deletion was required. Every annotation below re-states the bounded-capability framing and sources memory to brand-config (`live`: Companion Creator + saved/resumed chat history) — never to a tier, price, or "priority memory" claim.

No bullets were deleted.

---

# Outline — Why Does My AI Companion Forget? (And How to Fix It)

**Target keyword:** why does my ai companion forget
**Search intent:** Informational / troubleshooting ("why does X happen + how do I fix it")
**Estimated word count:** ~2,200 (±10% → 1,980–2,420)
**Primary reader:** Frustrated AI companion / AI girlfriend users whose chatbot keeps forgetting names, past conversations, preferences, or story/roleplay details.

> **Validation run (PLE-2983) — produce through PREVIEW only, DO NOT PUBLISH.**

## Beat spec (restated from 1-research/why-ai-companion-forgets.md — BINDING)
- **Target word count:** **2,200** (±20% per dossier; this outline holds to ±10%). Section targets below sum to ~2,030 body + ~300 intro/conclusion = ~2,330.
- **Format:** **Explainer** ("why it forgets" → "what's really happening" → "how to fix it"). **NOT a listicle** — SERP modal is the explainer/mechanism essay, zero listicles in top results. Format parity, no deviation.
- **BLUF mandatory:** first sentence of the intro and of every H2 directly answers its question.
- **Comparison table:** **RECOMMENDED** (only 1 of 6 SERP pages has one — easy differentiation win). Spec'd in H2 3: short-term context vs. true persistent memory. Columns: *What it is | What it can do | What it can't | Survives a new chat?*
- **Must-cover (consensus, 6 — ALL mapped in coverage map):**
  1. Context window = the model's short-term working memory, measured in tokens
  2. Older messages get dropped as a chat grows (the literal cause)
  3. Chat history / logs are not the same as the model remembering
  4. "Memory features" = a layer that re-injects saved facts into the window, not true model memory
  5. Why a bigger context window doesn't cleanly fix it (cost + accuracy drop / context rot)
  6. Concrete fixes: summarize/re-anchor key facts; pick an app built for persistent memory
- **Information gain (≥1 REQUIRED) → `[GAIN]`:** a concrete, plain-language walkthrough tracing ONE message from "in view" to "dropped" as the conversation crosses the context-window boundary, framed for adult/roleplay companions (character facts, scenario, preferences). No page-1 result delivers this. Lives in H2 2.
- **Differentiation (go deeper than the 1–2 pages that touch them):** name and explain **"context rot"**; a **reader-runnable test** for real vs. decorative memory; the short-term-vs-persistent **table**.
- **Secondary keywords (work in naturally):** why does character ai forget; how to make character ai remember; does AI remember past conversations; AI companion memory; how many messages does an AI companion remember; persistent memory vs context window; why do AI assistants forget between sessions.
- **Product mention:** Pleasur.AI as the "built for long-term memory" example — shown, not sold, same critical lens as competitors. `live` only (Companion Creator, saved/resumed chat history). Memory = a capability, NEVER tied to an unverified "$19 plan" or "priority memory processing" tier.
- **Compliance:** 18+ framing where relevant; no "unlimited / forever / never forgets" absolutism; no "no-filter/anything-goes"; privacy is a design priority, not a guarantee; no real-person likenesses; no internal-stack tool names in prose.
- **Real competitor:** the **AI Overview**, not the ranking pages — beat it with the message-level walkthrough and the runnable test the AIO can't replicate.

## Title
**Why Does My AI Companion Forget? (And How to Fix It)** (48 chars; primary keyword first)

## Thesis
Your AI companion forgets because every message lives inside a fixed-size "context window" that quietly drops the oldest text as the chat grows — so the fix isn't a magic setting but understanding the gap between short-term context and true persistent memory, then re-anchoring key facts and choosing a companion built to remember.

## Content type
Explainer (mechanism → walkthrough → fix). Honest, mechanism-first voice; second person, plain English, "context window" explained inline. Pleasur.AI shown under the same critical lens as any app. This is the focused "why it forgets" deep-dive; it links **up** to the brand's memory pillar for "which ones remember" and the full test protocol.

---

## Introduction

**Target:** ~180 words

**Hook:** Problem-statement that names the reader's pain — You tell your AI companion something that matters — your name, a detail about your last scene together, a preference — and a few messages later it's gone, like the conversation never happened. (Specific, not "in today's world".)

**Thesis:** (above) — forgetting is a built-in limit of how these models read a conversation, not a glitch you caused; once you see the mechanism, the fixes are obvious.

**Preview:** You'll get the real reason in plain English, a step-by-step look at what actually happens to a single message as a chat gets long, why a "bigger memory" isn't the clean fix it sounds like, a quick test to tell real memory from decorative memory, and concrete things you can do today.

**Visuals:**
  Visual 1: {type: image, sub: concept-illustration, prompt: Clean editorial diagram of a fixed-width frame labeled "context window" sliding right across a long horizontal strip of chat bubbles; the oldest bubbles on the left fall outside the frame and fade out, labeled "dropped". White background, sans-serif labels, no human likeness, brand-neutral colors., style: illustration, safety: sfw}

**Product mentions:** None. Intro is foundational/problem-framing — the reader hasn't earned a product callout yet. (Skill rule: keep "what is X" foundational sections product-free.)

---

## H2 1 — Your companion has short-term memory, not a memory [consensus #1, #3]

**Target:** ~380 words

- **BLUF:** Your AI companion forgets because it doesn't "remember" your conversation at all — it re-reads a limited window of recent text every time it replies, and anything outside that window simply isn't there.
- **Key points:**
  - The **context window** is the model's short-term working memory: the chunk of recent conversation it can actually read at once, measured in **tokens** (roughly word-pieces). Explain "token" inline.
  - Every reply is generated by re-reading that window from scratch — there's no running mental model of you between messages.
  - The chat log you see on screen is a **UI feature**, not the model's memory: the app stores the transcript so *you* can scroll it, but the model only ever sees what fits in the window (consensus #3 — logs ≠ remembering). This answers "does AI remember past conversations" and "how many messages does an AI companion remember".
- **Evidence:** Consensus across LLMnesia (context window = working memory; history is a UI feature) and DigitalHumanCorp (logs ≠ memory), 1-research SERP summaries; deep-research "Lost in the Middle" / short-range-attention findings as the technical backing.
- **Transition to next section:** So if the window is all the model can see, what happens to a fact once the conversation grows past it? Let's trace one message.
- **Visuals:**
  Visual 2: {type: image, sub: diagram, prompt: Side-by-side editorial diagram. Left panel labeled "What you see": a long scrollable chat transcript. Right panel labeled "What the model reads": only the last few message bubbles inside a bracket labeled "context window (tokens)". An arrow shows the model ignoring the older bubbles. White background, sans-serif labels, no human likeness., style: illustration, safety: sfw}

**Product mentions:** None. This is the foundational "what is the context window" mechanism section — keep it product-free so the explanation reads as honest education, not a setup for a pitch. (Skill: "What is X" sections stay product-free.)

---

## H2 2 — What actually happens to one message as the chat grows [GAIN] [consensus #2]

**Target:** ~500 words

- **BLUF:** Here's the part no one shows you: a single fact you typed — say, your companion's backstory or a kink you established in an early scene — stays in view only until enough newer text pushes it past the window's edge, and the moment it falls off, the model literally cannot see it anymore.
- **Key points (the literal walkthrough — trace ONE message, framed for roleplay/adult companions):**
  - **Turn 1 — you plant it.** "Remember, your name is Mara and you grew up on a fishing boat." It sits at the top of the window; the model reads it on every reply. The companion stays in character.
  - **Turns 2–40 — it drifts toward the edge.** Each new message (yours and the companion's) adds tokens. The window is fixed-size, so it behaves like a sliding frame: as new text enters one side, the oldest text is pushed toward the other. Your "Mara / fishing boat" line moves further from the live edge.
  - **The boundary — it gets dropped.** Once the conversation's total tokens exceed the window, the oldest lines are evicted to make room. "Mara grew up on a fishing boat" is now outside what the model can read. Nothing flagged it; it's just gone from view.
  - **The next reply — the forgetting you feel.** You reference the fishing boat; the model has no record of it, so it invents something or asks "what boat?" That's the immersion-break — the early part of the story "just disappears". (Ties to the brand's "what breaks immersion" angle.)
  - Name the related trap: even *before* a fact is fully evicted, models read the **middle** of a long window worst ("lost in the middle") — so a detail can be technically present but effectively ignored. (Sets up "context rot" in H2 3.)
- **Evidence:** Information-gain section per beat spec — every SERP page hand-waves this; we trace it literally. Backed by deep-research "Lost in the Middle" (performance worst for mid-context info) and sliding-window mechanics. Sentiment quotes (paraphrased, not attributed): "the early part of our story just disappears," "it forgets who I am after a few messages."
- **Transition to next section:** The obvious thought is "just give it a bigger window." It helps less than you'd expect — and here's why.
- **Visuals:**
  Visual 3: {type: image, sub: concept-illustration, prompt: Four-step horizontal flow diagram titled "What happens to one message". Step 1 "You type a fact" (bubble at left edge of a frame labeled context window). Step 2 "New messages push it toward the edge" (the bubble slides left as new bubbles enter from the right). Step 3 "It falls outside the window" (the bubble drops below the frame, faded, labeled "dropped"). Step 4 "Companion forgets" (a confused speech bubble "what boat?"). Clean editorial illustration, white background, sans-serif labels, no human likeness., style: illustration, safety: sfw}
  Visual 4: {type: external, sub: reddit-comment, url: https://www.reddit.com/r/CharacterAI/, selector: #t1_<comment-id>, crop: padded, what: A representative public user complaint about a character forgetting established facts after a few messages (no PII; documents the real pain pattern). Manual selector to be confirmed at capture.}

**Product mentions:** Inline mention (light, one clause). When landing the "immersion-break" beat, note in passing that forgetting an established detail is the single most common immersion-killer in roleplay, and link OUT to the brand's existing [What Breaks Immersion in AI Roleplay](https://pleasur.ai/blog/what-breaks-immersion-ai-roleplay) article rather than re-explaining it here. No product/CTA — this section is mechanism, and a tool pitch would interrupt the walkthrough. (Cross-reference of an existing brand article per skill step 5, not a product placement.)

---

## H2 3 — Why a bigger context window isn't the fix (and what "context rot" means) [consensus #5; differentiation]

**Target:** ~340 words

- **BLUF:** A bigger context window helps at the margins but doesn't cleanly fix forgetting, because larger windows cost more to run and, worse, models get *less* accurate at using a window the fuller it gets — a degradation people now call **"context rot."**
- **Key points:**
  - **Cost:** processing more tokens per reply is more compute, so providers cap windows or charge for the large ones — it's not free to "just make it bigger."
  - **Context rot / "lost in the middle":** as the window fills, the model attends worst to the middle, so even facts that are technically still in view get effectively ignored. Bigger window ≠ better recall. (Name the term — only Kenotic does on the SERP.)
  - The honest takeaway: a window is short-term memory by design; scaling it pushes the wall back a bit, it doesn't remove the wall. This is why "why can't a bigger context window fix this" keeps coming up.
- **Evidence:** Kenotic Labs ("context rot," the one SERP page that names it); deep-research "Lost in the Middle" finding (mid-context accuracy drop). 1-research consensus #5.
- **Transition to next section:** If a bigger window isn't real memory, what is? The difference between short-term context and true persistent memory is the whole game.
- **Visuals:**
  Visual 5: {type: chart, data: research.context_rot_accuracy, style: line, title: Recall accuracy drops as the context window fills (illustrative, sourced from "Lost in the Middle"-style findings). NOTE TO DRAFT: only render if a real sourced data series is available; if not, downgrade to {type: none} and keep the point in prose — do not fabricate numbers.}

**Product mentions:** None. This section's whole point is that scaling the window is NOT the fix — inserting a product here would undercut the argument and read as opportunistic. Hold the mechanism honest; the product belongs in H2 4–5 where persistent memory is the actual subject.

---

## H2 4 — Short-term context vs. true persistent memory [consensus #4; differentiation table]

**Target:** ~380 words

- **BLUF:** Real "memory" in an AI companion is a separate layer bolted on top of the context window — it saves chosen facts to storage and re-injects them into the window on future chats — so the honest question isn't "does it have memory" but "which kind, and does it survive a new chat?"
- **Key points:**
  - **"Memory features" explained (consensus #4):** they don't make the model remember; they save key facts (your name, preferences, character backstory) to a store, then paste the relevant ones back into the context window when you return. It's re-injection, not recall.
  - This is why some apps feel like they remember across sessions and others reset to zero: context-only apps (e.g. Character.AI historically) keep nothing once the window clears; persistent-memory apps re-load saved facts. Answers "why do AI assistants forget between sessions".
  - **Decorative vs. real memory:** a "memory" badge can be cosmetic. The contrast table below shows exactly what each layer can and can't do.
- **Evidence:** Consensus #4 across LLMnesia / DigitalHumanCorp / Kenotic (memory = re-injection layer). 2-reference: short-term context window vs. long-term persistent store (link to memory pillar). Honest competitor framing: Character.AI historically context-only.
- **Comparison table (RECOMMENDED — spec'd as GFM skeleton; draft authors rows):**

  | | Short-term context (context window) | True persistent memory |
  |---|---|---|
  | **What it is** | The recent conversation the model re-reads each reply, measured in tokens | A saved store of chosen facts, re-injected into the window on future chats |
  | **What it can do** | Hold the current scene; keep continuity within one long-enough chat | Recall your name, preferences, character/backstory facts across sessions |
  | **What it can't** | Survive past its token limit; recall anything evicted or never saved | Remember *everything* — it stores selected facts, not the whole history |
  | **Survives a new chat?** | No — clears when the window resets | Yes — that's the point (within limits) |

- **Transition to next section:** Knowing the two layers exist is useless if you can't tell which one your app actually has — so here's a test and a short list of fixes.
- **Visuals:**
  Visual 6: {type: table, columns: [Dimension, Short-term context, True persistent memory]}

**Product mentions:** Inline mention (one sentence, same critical lens as the Character.AI contrast). After the "context-only apps vs. persistent-memory apps" point, give a concrete example of the persistent-memory side: apps like Pleasur.AI keep a saved store of character facts and saved chat history that reloads on a new session — exactly the "re-injection" layer described, no more. State the same caveat the table already makes: persistent memory stores *selected* facts, not everything, and is bounded, not "forever." Source the capability to brand-config (`live`: Companion Creator + saved/resumed chat history) — do NOT attach it to any tier, "$19 plan," "priority memory processing," or "unlimited messages." Link UP to the [Best AI Girlfriend With Memory](https://pleasur.ai/blog/ai-companion-best-memory) pillar for "which ones remember." Keep it shown-not-sold: name it as the example of the right column, not as a recommendation. No screenshot here — the table is the anchor visual.

---

## H2 5 — How to make your companion remember (test it, then fix it) [consensus #6; differentiation: runnable test; product-led]

**Target:** ~430 words

- **BLUF:** You can't fix forgetting with a hidden setting, but you can do three concrete things: test whether your app has real memory, re-anchor key facts as you chat, and — if it fails the test — switch to a companion built for persistent memory.
- **Key points:**
  - **The runnable test (differentiation — reader can do it now):** state a specific, unusual fact early ("my favorite color is oxblood; your name is Mara") → keep chatting ~30+ turns *or* start a brand-new session a day later → ask about it. **Remembered / partial / forgot** tells you if memory is real or decorative. Link UP to the brand's full memory-test protocol rather than duplicating it.
  - **Re-anchor / summarize (consensus #6, fix #1):** periodically restate the facts that matter, or drop a one-line recap ("quick recap: I'm Sam, you're Mara, we're mid-fishing-trip scene"). This pushes the key facts back to the live edge of the window. Practical for "how to make character ai remember".
  - **Set the character up once (fix #2, product-led, shown not sold):** apps with a persistent store let you bake backstory, personality, and preferences into the character at creation, so the long-term layer always has something stable to re-inject. In Pleasur.AI's [AI Companion Creator](https://pleasur.ai/create) you set appearance, personality, and backstory once, and saved chats resume across sessions — held to the same test above as any app, not a magic-memory claim. No "unlimited/forever" framing; memory is a capability, bounded.
  - **Pick an app built to remember (consensus #6, fix #3):** if your current app fails the new-session test, that's a design choice, not your fault — choose one whose memory survives a fresh chat.
- **Evidence:** Consensus #6 fixes (re-anchor; choose a persistent-memory app). 2-reference reusable memory-test protocol + Companion Creator/resume-saved-chat modules. Live brand-config: Companion Creator + saved/resumed chat history are `live`; pricing facts NOT load-bearing here.
- **Transition to next section:** (to conclusion)
- **Visuals:**
  Visual 7: {type: screenshot, target: create, what: Companion Creator showing where backstory / personality / preferences are set (the fields that seed long-term memory), annotate: arrow on the backstory/personality field}
  Visual 8: {type: image, sub: concept-illustration, prompt: A simple editorial scorecard card titled "Memory test", with three rows: "State an unusual fact early", "Continue 30+ turns OR start a new session a day later", "Ask about it — score Remembered / Partial / Forgot". Clean UI-style illustration, white background, sans-serif labels, no human likeness., style: illustration, safety: sfw}

**Product mentions:**
- **(a) Walkthrough — AI Companion Creator (fix #2).** This is the primary, designed-in product slot. Walk through setting backstory / personality / preferences once in the [AI Companion Creator](https://pleasur.ai/create) so the persistent layer has stable facts to re-inject, and note that saved chats resume across sessions. Hold it to the SAME test the section just gave the reader — apply the runnable test to Pleasur.AI exactly as to any competitor; do NOT exempt it. Bounded-capability framing only: memory stores selected facts and persists across sessions within limits — never "unlimited / forever / never forgets," never tied to a tier name, "$19 plan," "priority memory processing," or message caps. Source: brand-config `live` (Companion Creator; saved/resumed chat history). Visual 7 is the anchor screenshot (already typed: `{type: screenshot, target: create, what: backstory/personality/preferences fields, annotate: arrow on the backstory/personality field}`) — pull the setup detail from the 2-reference Companion Creator module rather than re-explaining the full creation flow.
- **(b) Tip box — re-anchoring (fix #1).** "Pro tip: drop a one-line recap every dozen or so turns ('quick recap: I'm Sam, you're Mara, mid-fishing-trip scene') to push the facts that matter back to the live edge of the window." App-agnostic tip — works on any companion, reinforces the honest/practical voice and keeps the section from reading product-only.

---

## Conclusion

**Target:** ~120 words

- **Recap (restate thesis, fresh framing):** Your companion forgets not because it's broken but because it reads your chat through a fixed-size window that drops the oldest text first — real continuity comes from a separate persistent-memory layer, and the only proof is the test you run yourself.
- **Next step:** Run the quick memory test on your current app; if it fails the new-session check, see which companions actually hold onto you in [Best AI Girlfriend With Memory: Which Ones Actually Remember You?](https://pleasur.ai/blog/ai-companion-best-memory).
- **Optional CTA:** Set your character up once so the memory layer has something to hold — start in the [AI Companion Creator](https://pleasur.ai/create).

**Product mentions:** Soft CTA only (already in outline) — single link to the [AI Companion Creator](https://pleasur.ai/create) as an optional next step, plus the internal link UP to the memory pillar. Keep it one line; do not expand into a pitch. Bounded framing, no tier/price/"unlimited" claims.

---

## Coverage map (every consensus topic → section)

| # | Consensus / must-cover topic (beat spec) | Section |
|---|---|---|
| 1 | Context window = short-term working memory, measured in tokens | H2 1 |
| 2 | Older messages get dropped as the chat grows (the literal cause) | H2 2 **[GAIN]** |
| 3 | Chat history / logs are not the same as the model remembering | H2 1 |
| 4 | "Memory features" = a re-injection layer, not true model memory | H2 4 (+ table) |
| 5 | Why a bigger window doesn't cleanly fix it (cost + context rot) | H2 3 |
| 6 | Concrete fixes: re-anchor key facts; pick a persistent-memory app | H2 5 |
| — | **Differentiation:** name "context rot" | H2 3 |
| — | **Differentiation:** reader-runnable real-vs-decorative memory test | H2 5 |
| — | **Differentiation:** short-term-vs-persistent comparison table | H2 4 |
| — | **[GAIN]:** trace ONE message in→dropped, roleplay-framed | H2 2 |

## Internal links to add
- H2 4 + Conclusion → [Best AI Girlfriend With Memory](https://pleasur.ai/blog/ai-companion-best-memory) (memory pillar; "which ones remember" + full test protocol)
- H2 2 → [What Breaks Immersion in AI Roleplay](https://pleasur.ai/blog/what-breaks-immersion-ai-roleplay) (forgetting as #1 immersion-breaker)
- H2 4 → [Kindroid Alternative: The Continuity Problem, Solved](https://pleasur.ai/blog/kindroid-alternative-video-calls-2026) (cross-session forgetting)
- H2 5 → [OpenMind AI vs Pleasur.ai: Which One Actually Remembers You?](https://pleasur.ai/blog/openmind-ai-vs-pleasurai) and [Best Replika Alternative 2026](https://pleasur.ai/blog/best-replika-alternative-2026)

## Product-mention plan (H2-by-H2 summary — added by /product-mentions)

| Section | Product / asset | How | Notes |
|---|---|---|---|
| Intro | — | none | Foundational/problem-framing; reader hasn't earned a callout |
| H2 1 | — | none | "What is the context window" — kept product-free (honest education) |
| H2 2 | (brand article cross-ref) | inline link | Link to *What Breaks Immersion in AI Roleplay*; no product/CTA — mechanism section |
| H2 3 | — | none | Section argues bigger window is NOT the fix; a product here would undercut it |
| H2 4 | AI Companion Creator (saved store + saved chat history) | inline mention | One sentence as the "true persistent memory" example, same lens as Character.AI; bounded, sourced to brand-config; link up to memory pillar |
| H2 5 | AI Companion Creator | (a) walkthrough + (b) app-agnostic tip box | Primary slot; held to the same runnable test; Visual 7 screenshot anchor; tip box = re-anchoring |
| Conclusion | AI Companion Creator | soft CTA (existing) | One-line optional next step |

**Count:** 3 meaningful product annotations (H2 4 inline, H2 5 walkthrough, H2 5 tip box) + 1 soft conclusion CTA + 1 brand-article cross-reference. Within the 3–5 target; not shoehorned. Only `live` products used; no roadmap (Video) or false-fact (tier/price/"priority memory"/"unlimited") claims.

## Beat-spec self-check (blocking)
- [x] **Word targets sum:** 380+500+340+380+430 = 2,030 body + 180 intro + 120 concl = **2,330**. Target 2,200 → +5.9%, within ±10% (1,980–2,420). ✔
- [x] **Format = explainer**, not listicle — SERP parity, no deviation needed. ✔
- [x] **All 6 consensus topics in coverage map** → sections H2 1–5. ✔
- [x] **`[GAIN]` present** (H2 2, message-level walkthrough) and genuinely not on SERP page 1 (every page hand-waves it). ✔
- [x] **Comparison table spec'd** (recommended) as GFM skeleton in H2 4 with the beat-spec columns. ✔
- [x] **MECE:** H2 1 = what it is (logs≠memory); H2 2 = the eviction mechanism; H2 3 = why bigger fails; H2 4 = the two-layer contrast; H2 5 = test + fixes. No overlap; H2 list alone reads as a complete map. ✔
- [x] **Each H2:** BLUF + 2–4 key points + evidence source + transition + typed Visuals + word target. ✔
- [x] **Visual density/diversity:** 8 visuals (target 8 for 1,200–2,000w; range 6–11 — note body+intro/concl ≈2,330 sits at the 2k boundary, 8 is on-target). Types: image, external, chart, table, screenshot = **5 distinct** (≥3). ✔ Chart (Visual 5) is conditional — drops to `none` if no sourced data, no fabrication.
- [x] **Title** <60 chars (48), primary keyword first. ✔
- [x] **Compliance:** no "unlimited/forever," memory framed as bounded capability, no tier-price/"priority memory processing" claims, no internal-stack names, 18+/roleplay framing kept honest. ✔
- [x] **Product mentions (added by /product-mentions):** 3–5 annotations across H2s; each specifies HOW; `live` only; brand held to same critical lens as competitors; no coming-soon/roadmap products; no false review-site facts. ✔
