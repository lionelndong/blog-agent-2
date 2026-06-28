# What AI Companion Apps Get Wrong About Memory (and What Pleasur.ai Fixes)

**Target keyword:** what do ai companion apps get wrong (2026)
**Search intent:** informational → commercial-investigation (reader is frustrated by a companion app, evaluating alternatives)
**Estimated word count:** ~2,600 (band: 2,400–2,800; floor ≥1,920)
**Primary reader:** Someone who already uses an AI companion app, is annoyed by it (it forgets them, loops, feels generic, nickel-and-dimes them, or can't talk), and is shopping for something better. 18+.
**Persona:** Theo Hart (comparison/decision-led explainer — tables, decision-table, feature-matrix, further-reading, cta).

---

## Pre-flight reconciliation

The original outline had 0 contradictions about coming-soon products. No contradictions found.

Reconciliation detail (for downstream /draft):
- The only `roadmap` / coming-soon product in scope is **AI Video (generated clips)**. It is mentioned in the outline ONLY as a negative guardrail ("never claim two-way video calls — AI video = generated clips, roadmap"), never as a feature to demonstrate. That is the permitted use (a constraint note, not a product callout), so nothing is deleted.
- All three product callouts placed below — **persistent memory layer**, **real-time two-way VOICE phone call + voice notes**, and **transparent 3-tier coin pricing** — are `status: live` (re-verified 2026-06-28 in 2-reference). All eligible for normal article mentions.

---

## BEAT SPEC restatement (binding — from 1-research)

- **Format:** problem-aware **explainer**, NOT a listicle. Structure = **5 named-failure H2s + a "how to choose" H2 + `## FAQ`**. Each failure H2 = pain point + why it happens + the pleasur.ai fix woven in (answer-first, not bolted on).
- **Word target:** ~2,400–2,800 (per-section targets below sum to ~2,760, within ±10% of 2,600). Never pad.
- **Comparison table:** OPTIONAL but RECOMMENDED — use a **"failure → why it happens → what fixes it"** table (higher info-gain than an app-spec grid). Do NOT build a competitor-pricing table with unverified competitor numbers.
- **Memory FIRST** as the thesis anchor; the other four failures cascade from it.
- **Information gain [GAIN]:** the memory-first five-failure taxonomy + a first-hand persistent-memory + in-chat-voice walkthrough (neither exists on page 1).
- **FAQ (HARD REQUIREMENT):** final `## FAQ` H2, these 4 questions verbatim-intent (app builds FAQPage JSON-LD from it):
  1. Why do AI chatbots forget conversations?
  2. Which AI companion apps have the best memory?
  3. Does pleasur.ai remember previous conversations?
  4. What do AI companion apps get wrong?
- **HARD constraints:** 3-tier coin pricing ONLY ($12.99/1,500 · $27.99/5,000 · $49.99/10,000) — never "flat / no tokens / no hidden fees." Real-time two-way **VOICE** + voice notes are live — **never claim two-way video calls** (AI video = generated clips, roadmap). Competitor failings always hedged ("widely reported," "users report"). No first-person "82% memory" stat (attributed MariaVibe citation w/ URL only, if at all); no fabricated competitor recall numbers. 18+ throughout; no "no filter / anything goes," no safety guarantees, no real-person likenesses. Reader-facing copy never names internal tools/vendors.

**Thesis:** AI companion apps fail on the same five things — and **memory is the root failure**: an app that forgets you can't hold a consistent character, can't avoid repetition, and can't justify its paywall; persistent memory plus in-chat voice is what actually fixes the experience.

---

## Introduction

**Target:** ~180 words

**Hook:** Problem-statement that names the reader's pain — the moment your "companion" asks a question it already asked yesterday, or forgets the detail you told it an hour ago, and the illusion collapses.

**BLUF lede (40–60 words, answer-first — answers "what do AI companion apps get wrong"):** Most AI companion apps get the same five things wrong: they forget your conversations, repeat themselves, drift out of character, hide real costs behind confusing coins or tokens, and can't talk out loud. Almost every one of those failures traces back to one root cause — weak memory.

**Thesis:** State the one-sentence position (memory is the root failure; the other four cascade from it).

**Preview (a promise, not a TOC dump):** This piece names all five failures, explains *why* each happens, and shows what a persistent memory layer plus real-time voice actually fixes — demonstrated first-hand inside Pleasur.ai, with its pricing modeled openly.

**Visual:** Visual 1: {type: chart, data: research.five_failure_taxonomy, style: horizontal-bar, title: The five things AI companion apps get wrong (memory at the root)}

**Components:** `:::nutshell` (the BLUF answer, one box directly under the H1) — the ONE nutshell for the article. Wrap the opening paragraph in `{lead}…{/lead}`. Internal link in the intro: [Why Specialized AI Companions Beat ChatGPT for Emotional Depth](https://pleasur.ai/blog/ai-companion-vs-chatgpt-companionship) as the "purpose-built vs general chatbot" anchor.

**Product mentions:** None — foundational/answer-first beat. Name the *fixes* in the preview line as a forward promise ("a persistent memory layer plus real-time voice"), but do NOT pitch or walk through any product here. The reader hasn't earned the demo; each failure H2 below carries its own woven-in callout. Keep the brand reference to the single preview clause already in the outline.

---

## 1. They forget you (poor memory is the root failure)   [GAIN]

**Target:** ~430 words

- **BLUF:** The biggest thing AI companion apps get wrong is memory — most run on a fixed context window, so once a conversation gets long enough, your earliest exchanges silently drop off and the app "forgets" who you are.
- **Key point — the mechanism:** Define the context window (the fixed span of recent text a model can "see"). When the chat exceeds it, older turns fall out of view; the app isn't being careless, it literally can't see what you told it last week.
- **Key point — why it's the *root* failure:** Everything else cascades from this. No memory → no consistent character (#3), more generic looping (#2), and a paywall you can't justify (#4). Frame memory as the load-bearing axis.
- **Key point — the fix (woven in, not bolted on):** A **persistent memory layer** sits on top of the chat and saves key facts, preferences, and relationship history *between* sessions — so chats resume with continuity instead of from a blank slate. Distinguish **cross-session continuity** (remembering across days) from **within-chat memory** (just this conversation).
- **Evidence:** eastbayexpress's whole test methodology — *"Did they remember my mom's name? Did they reference previous conversations without me prompting them?"* (1-research, deep web findings + #3 summary). First-hand Pleasur.ai walkthrough: companion recalls a detail from an earlier session unprompted.
- **Hedge guard:** any "resets after N messages" stays "widely reported / users report" — never asserted as fact. No first-person "82%" stat.
- **Transition:** When an app can't remember you, it falls back on generic filler — which is exactly how the second failure, repetition, starts.
- **Visuals:** Visual 1: {type: diagram, what: fixed context window dropping old turns vs. a persistent memory layer retaining facts across sessions, annotate: label "earlier exchanges drop" on the context-window side}; Visual 2: {type: screenshot, target: chat, what: companion recalling a fact from a previous session unprompted, annotate: highlight the recalled detail}
- **Components:** `:::definition term="Context window"` (crisp first-mention definition of the core term). Internal link: [Best AI Girlfriend With Memory (2026): Which Ones Actually Remember You?](https://pleasur.ai/blog/ai-companion-best-memory).
- **Product mentions:** Walkthrough — this is the thesis anchor and the load-bearing product claim. Demonstrate Pleasur.ai's **persistent memory layer** (live, AI Companion Creator) as the fix: a memory layer that saves key facts, preferences, and relationship history *between* sessions, vs. a fixed context window that drops earlier exchanges. Proof = Visual 2 (the screenshot above, upgraded below) showing the companion recall a detail from an earlier session unprompted — the information-gain no SERP page has. GUARDRAILS: frame it as a persistent memory *layer*; do NOT claim "infinite memory," "never forgets," or "unlimited." Do NOT use the "82%" stat first-person (attributed MariaVibe citation w/ URL only, if at all); do NOT counter any competitor "Nx recall" with a fabricated number. Link [Best AI Girlfriend With Memory (2026)](https://pleasur.ai/blog/ai-companion-best-memory) for the deeper memory roundup rather than re-explaining setup. Upgrade Visual 2 → `{type: screenshot, target: chat, what: companion recalling a fact from a previous session unprompted, annotate: highlight the recalled detail}`.

---

## 2. They repeat themselves and loop

**Target:** ~340 words

- **BLUF:** Companion apps loop and repeat because the model keeps losing its grip on context — once earlier turns drop out of the window, it falls back on safe, generic phrasing it has used before.
- **Key point — name the failure:** This is the failure nobody on page 1 names directly. Repetition isn't random; it's the visible symptom of context-window churn.
- **Key point — the mechanism:** When the conversation history a model can see keeps getting truncated, it re-derives responses from thin context and gravitates to high-probability, repeated patterns ("That sounds really interesting, tell me more"). The blank slate breeds sameness.
- **Key point — the relief (woven in):** A persistent memory layer reduces the blank-slate churn — when the companion still holds your facts and recent history, it has something specific to respond *to*, so replies stay varied and on-thread. No dedicated feature to demo here; keep it explanatory and tie relief back to memory.
- **Evidence:** Mechanism explanation (2-reference H2 #2 note); voice-of-customer "feels like a customer service bot" generic-feel quotes (1-research).
- **Transition:** Looping is annoying; losing the *character* entirely is worse — which brings us to personality drift.
- **Visuals:** Visual 1: {type: diagram, what: context-churn loop — truncated history feeding generic repeated replies, contrasted with memory-fed varied replies}
- **Components:** none (keep explanatory; restraint). Optional single `:::sidenote` caveat that not all repetition is a memory issue (some is model temperature/prompting) — use only if it earns its place.
- **Product mentions:** Inline mention (no walkthrough — there is no dedicated feature for this failure). When explaining the relief, tie it back to the same **persistent memory layer** introduced in #1: continuity gives the model something specific to respond to, which reduces blank-slate looping. One clause, same skeptical/explanatory register as the mechanism — do NOT introduce a new product, do NOT add a screenshot. The point is the mechanism; memory is named only as the lever, not re-demoed.

---

## 3. The character drifts or feels fake

**Target:** ~360 words

- **BLUF:** Inconsistent, "fake-feeling" characters are a memory problem wearing a personality mask — a companion that can't remember its own backstory or how it spoke to you yesterday can't stay in character today.
- **Key point — what users actually report:** The "good ones feel real, the bad ones feel like a customer-service bot from the first message." Consistency is what users value most; personality drift is the betrayal.
- **Key point — why it happens:** Persona details (tone, history, preferences, the relationship's running jokes) live in memory. Drop them with the context window and the persona resets to a generic baseline. General-purpose chatbots drift worse because they aren't purpose-built to hold a persona.
- **Key point — the fix (woven in):** Persistence is what lets a persona stay consistent across sessions — the same memory layer that fixes forgetting is what keeps the character *the same character* over weeks, not just within one chat.
- **Evidence:** eastbay "real companions vs chatbots" framing; genies "What Real Users Value = consistent personality + reliable memory" (1-research consensus topic #3).
- **Transition:** A consistent character you actually like makes the next failure sting more — paying to keep talking to it, without understanding what you're paying for.
- **Visuals:** Visual 1: {type: screenshot, target: create, what: AI Companion Creator persona/character setup showing persisted persona traits, annotate: arrow on the saved persona fields}
- **Components:** `:::pullquote` (one memorable line on consistency, e.g. the "real companions vs chatbots" idea, paraphrased — not a real-person quote). Internal links: [What Breaks Immersion in AI Roleplay — And How Pleasur.ai Preserves It](https://pleasur.ai/blog/what-breaks-immersion-ai-roleplay); optionally [Why Specialized AI Companions Beat ChatGPT for Emotional Depth](https://pleasur.ai/blog/ai-companion-vs-chatgpt-companionship) if not already used in intro.
- **Product mentions:** Walkthrough (light) — demonstrate that the **persistent memory layer** (same one from #1, second mapped section) is what holds a **consistent persona** across sessions. Show the **AI Companion Creator** persona/character setup (Visual 1 above) where persona traits are *persisted*, then connect: the same persistence that fixes forgetting keeps the character the same character over weeks. Frame as continuity, not magic — the fix is "the persona doesn't reset because the details don't drop." GUARDRAILS: 18+ persona framing; no real-person likenesses; no "no filter / anything goes." Link [What Breaks Immersion in AI Roleplay](https://pleasur.ai/blog/what-breaks-immersion-ai-roleplay) for the deeper consistency/immersion breakdown rather than re-explaining persona setup.

---

## 4. The paywall hides what you're actually paying for

**Target:** ~390 words

- **BLUF:** Companion apps get pricing wrong not by charging money but by hiding it — "free" apps gate the meaningful experience behind confusing token or coin systems, so you never quite know what an action costs until you've spent it.
- **Key point — the real frustration:** It isn't that good companions cost money; it's surprise charges and opaque token math. genies: *"the most meaningful experiences are often behind a paywall… from simple monthly subscriptions to more complex token-based systems… without any surprise charges."*
- **Key point — the honest angle (woven in, HARD constraint):** Transparency, not "free/flat." Model Pleasur.ai's pricing openly: **three coin-metered tiers — Starter $12.99/mo (1,500 coins) · Standard $27.99/mo (5,000 coins) · Ultimate $49.99/mo (10,000 coins)**. All tiers: unlimited messages, buy-more coins, cancel anytime, 7-day money-back. Per-action coin costs sourced live: AI image gen 10 coins each · voice notes 10 coins each · phone calls 50 coins/min (Standard + Ultimate). **No tier is unlimited.** NEVER say flat / no tokens / no hidden fees.
- **Key point — what "transparent" means in practice:** You can do the coin math up front (e.g. a voice note = 10 coins; a 4-minute call = 200 coins) instead of discovering it after the fact.
- **Evidence:** First-party pricing fact-lock (1-research step 6 / 2-reference); genies cost-section quote.
- **Transition:** Knowing the cost is one thing; many apps still can't do the one thing that makes a companion feel real — talk to you.
- **Visuals:** Visual 1: {type: table, columns: [Tier, Monthly, Coins/mo, Unlimited messages]}; Visual 2: {type: screenshot, target: pricing, what: the three named tiers + per-action coin costs}
- **Components:** `:::table caption="Pleasur.ai coin tiers (live 2026-06-28)" source="pleasur.ai/pricing"` (the tier table) — Theo-favorite. Inline `` `code` `` for coin math (e.g. `` `4-min call = 4 × 50 = 200 coins` ``). Internal link: [What Do AI Companion Coins Actually Cost? (2026)](https://pleasur.ai/blog/what-do-ai-companion-coins-actually-cost) (deeper transparent-pricing breakdown). Optional `:::cta` #1 (high) → /pricing.
- **Product mentions:** Walkthrough — model Pleasur.ai's **transparent 3-tier coin pricing** openly as the honest answer to the hidden-cost failure. Name all three tiers verbatim: **Starter $12.99/mo / 1,500 coins · Standard $27.99/mo / 5,000 coins · Ultimate $49.99/mo / 10,000 coins**, all tiers unlimited messages + buy-more coins + cancel anytime + 7-day money-back; per-action costs (AI image gen 10 coins, voice notes 10 coins, phone calls 50 coins/min on Standard + Ultimate). Show the tier table (Visual 1) + pricing screenshot (Visual 2). The whole point is doing the coin math *up front*. HARD GUARDRAILS (gate-failing): the honest angle is **transparency**, NEVER "flat rate / no tokens / no hidden fees / free." There is no "$19/mo" tier and no unlimited tier — it is coin-metered. Do NOT build a competitor-pricing comparison asserting unverified competitor numbers. Link [What Do AI Companion Coins Actually Cost? (2026)](https://pleasur.ai/blog/what-do-ai-companion-coins-actually-cost) for the deeper coin breakdown. Optional `:::cta` (high) → /pricing.

---

## 5. They're text-only — no real voice

**Target:** ~340 words

- **BLUF:** Most companion apps are text-only, and voice is the divider users name between "a real companion" and "a chatbot" — typing at a character forever keeps the experience flat.
- **Key point — why voice matters:** Voice-of-customer research names it directly: *"voice calls that feel like phone calls with a real person"* is the real-vs-chatbot line (1-research). Voice is also a 215k related term — searchers already attach it to this cluster.
- **Key point — the fix (woven in, HARD constraint — VOICE not video):** Pleasur.ai has two **live** in-chat voice capabilities. **Real-time two-way VOICE phone call:** tap the "Call" button on the character's profile to start a live voice call; when it ends, the text chat continues in the same thread. **Voice replies / voice notes:** tap the speaker icon next to a reply to hear the character speak it aloud. NEVER claim two-way video calls — AI video = generated clips, roadmap.
- **Key point — ties back to the thesis:** Continuity carries from text → voice call → back to text *without losing context*, because the persistent memory layer holds the thread. Voice without memory is just a louder blank slate.
- **Evidence:** First-party voice fact-lock (live, re-verified 2026-06-28); eastbay voice quote.
- **Transition:** Five failures, one root cause — so how do you actually pick an app that avoids all five?
- **Visuals:** Visual 1: {type: screenshot, target: chat, what: the "Call" button on the character profile/chat header AND the speaker icon on a message bubble, annotate: arrow on Call button + arrow on speaker icon}
- **Components:** `:::note` (one caveat: voice calls are metered at 50 coins/min on Standard + Ultimate — ties honesty back to #4) — use the exact phrasing "tap the Call button on the character's profile" / "tap the speaker icon next to a reply."
- **Product mentions:** Walkthrough — demonstrate Pleasur.ai's two **live** in-chat voice capabilities as the fix for the text-only failure. (1) **Real-time two-way VOICE phone call:** "tap the Call button on the character's profile" to start a live voice call; when it ends, the text chat continues in the same thread. (2) **Voice replies / voice notes:** "tap the speaker icon next to a reply" to hear the character speak it aloud. Show Visual 1 (Call button + speaker icon). Tie back to thesis: continuity carries text → voice call → text without losing context because the persistent memory layer holds the thread. HARD GUARDRAILS (gate-failing): **VOICE only — NEVER claim two-way video calls** (AI video = generated clips, roadmap). Use the exact UI phrasing above, NOT "open Voice Chat" or "the Phone Call app." Carry the `:::note` honesty caveat (calls metered 50 coins/min on Standard + Ultimate) so this ties back to #4's transparency angle.

---

## How to choose a companion app that doesn't get these wrong

**Target:** ~300 words

- **BLUF:** Pick a companion app by stress-testing the five failure points directly — does it remember you across sessions, stay varied, hold character, price honestly, and let you talk out loud?
- **Key points — a buyer's checklist (consensus "how to choose" topic):**
  1. **Memory across sessions** — does it recall a fact from days ago unprompted? (the make-or-break test)
  2. **Reply variety** — does it loop into generic filler after a while?
  3. **Character consistency** — is it the same character next week?
  4. **Pricing transparency** — can you see what each action costs *before* you spend?
  5. **Voice** — can it actually talk (voice), not just type?
- **Key point — how to apply it:** Map each criterion to the failure it guards against; this is the reusable decision framework, restating the taxonomy as a shopping tool.
- **Evidence:** Synthesizes the five failures + every SERP listicle's "how to choose / what to look for" section (consensus topic #4).
- **Transition:** With the checklist in hand, the most common questions about memory and companion apps answer themselves — below.
- **Visuals:** Visual 1: {type: table, columns: [What to test, The failure it guards against, Green flag]}
- **Components:** `:::feature-matrix` (the five criteria × outcome, cells `yes`/`no`/`partial`) OR `:::decision-table` + `:::preferred-order` — Theo-favorite; keep to ONE such grid. Optional `:::cta` #2 (low) → /pricing. Optional internal link [Pleasur.ai vs Secrets AI](https://pleasur.ai/blog/pleasur-ai-vs-secrets-ai) for readers actively comparing.
- **Product mentions:** Inline mention (light — keep the checklist brand-agnostic so it reads as a neutral buyer's test, not a planted pitch). The five criteria are deliberately the same five failures Pleasur.ai is built to pass; you may note in one closing clause that Pleasur.ai is designed to clear all five (persistent memory across sessions, transparent 3-tier coin pricing, real-time two-way voice) WITHOUT re-pitching each feature. Optional `:::cta` (low) → /pricing and optional [Pleasur.ai vs Secrets AI](https://pleasur.ai/blog/pleasur-ai-vs-secrets-ai) for comparison-shoppers. Do NOT restate tier numbers or UI steps here — they were demoed above; this is the synthesis.

---

## Conclusion (Bottom line)

**Target:** ~120 words

- **Recap (restated thesis, fresh framing):** Every "what's wrong with my AI companion" complaint — forgetting, looping, drifting, surprise costs, silence — rolls up to one fixable root: memory. Fix memory and add real voice, and the rest of the experience follows.
- **Next step:** Send the reader to test it on the criteria themselves — link to [Best AI Girlfriend With Memory (2026)](https://pleasur.ai/blog/ai-companion-best-memory) as the memory-focused next read, or to Pleasur.ai's pricing to see the coin tiers modeled openly. 18+.
- **Components:** `:::key-takeaways` (the five failures + the one root cause, front-loaded) — the ONE key-takeaways box for the article. Close under a "Bottom line" heading (no "in conclusion").
- **Product mentions:** None (handoff only). Conclusion recaps and points the reader on via the two internal links already in the outline (memory roundup + /pricing). No fresh feature callout — the demos landed in #1, #3, #4, #5; a new pitch here would over-annotate.

---

## FAQ

**Target:** ~320 words (≈4 × 70–90 words). This section is a HARD REQUIREMENT — the app builds FAQPage JSON-LD from the `## FAQ` H2. Keep the four questions verbatim-intent; answers tightened to brand voice, substance + constraints intact. Render as `:::faq` with each question as an `### H3`.

**Product mentions:** Inline only, and only where the verbatim-intent answer already requires it (the memory layer / pricing / voice are named in the Q&A substance per the run brief). Do NOT add walkthroughs, screenshots, or CTAs in the FAQ — keep answers neutral and self-contained so the FAQPage JSON-LD stays clean. Same HARD constraints apply: 3-tier coin pricing only, VOICE not video, competitor resets hedged ("widely reported").

### Why do AI chatbots forget conversations?
Most rely on a fixed **context window** — a limited span of recent text the model can "see." When a conversation exceeds it, the earliest exchanges drop off and effectively get forgotten. Pleasur.ai adds a **persistent memory layer** that saves key facts, preferences, and relationship history *between* sessions, so chats resume with continuity instead of from a blank slate. (~80 words)

### Which AI companion apps have the best memory?
The apps that hold up are the ones with a dedicated **persistent memory** that retains information between sessions rather than resetting each chat (Pleasur.ai and Nomi are examples). Some apps have been **widely reported** to lose track of earlier details once a conversation runs long — phrase any reset claim as widely-reported, never as a verified number. Internal link: [Best AI Girlfriend With Memory (2026)](https://pleasur.ai/blog/ai-companion-best-memory). (~75 words)

### Does pleasur.ai remember previous conversations?
Yes. Pleasur.ai uses a persistent memory layer that stores your preferences, conversation history, and relationship context across sessions — so your companion can recall a detail you mentioned days ago without you re-explaining it, and stay in character over time. (~50 words)

### What do AI companion apps get wrong?
The common failure points are resetting memory between sessions, repeating themselves, drifting out of character (inconsistent personalities), hiding real costs behind confusing token or coin systems, and being text-only with no voice. Most trace back to weak memory. Pleasur.ai is designed to address these — persistent memory, transparent 3-tier coin pricing, and real-time two-way voice (voice, not video). (~70 words)

---

## Coverage map (consensus topic → section)

| Consensus topic (from beat spec) | Covered in |
|---|---|
| Memory / forgetting (lead failure) | H2 #1 (thesis anchor) `[GAIN]` |
| Repetition / looping replies (info-gain) | H2 #2 |
| Personality consistency / "generic bot" | H2 #3 |
| Cost / paywalls / token (coin) systems | H2 #4 |
| Voice / talking to your companion | H2 #5 |
| What to look for / how to choose | "How to choose…" H2 |
| Required FAQ (FAQPage schema) | `## FAQ` (4 questions verbatim-intent) |

**Information gain `[GAIN]`:** the memory-first five-failure taxonomy (H2 #1 anchors it; #2 names repetition as its own failure — absent on page 1) + first-hand persistent-memory & in-chat-voice walkthrough screenshots (no page-1 page has them).

## Product-mention map (this stage → /draft)

| Section | Product callout | Flavor | Status |
|---|---|---|---|
| Introduction | none (forward-promise only) | — | — |
| H2 #1 Memory | **persistent memory layer** (root-failure fix) | walkthrough + screenshot | live |
| H2 #2 Repeat/loop | persistent memory layer (relief, named only) | inline | live |
| H2 #3 Character drift | persistent memory layer → **consistent persona** (Companion Creator) | walkthrough (light) | live |
| H2 #4 Paywall | **transparent 3-tier coin pricing** (tiers + per-action coins) | walkthrough + table | live |
| H2 #5 Voice | **real-time two-way VOICE call + voice notes** | walkthrough + screenshot | live |
| How to choose | Pleasur.ai clears all five (one clause) | inline | live |
| Conclusion | none (handoff) | — | — |
| FAQ | memory / pricing / voice in answer substance only | inline | live |

→ Meaningful product annotations in **5** body sections (#1, #3, #4, #5 walkthroughs + #2 inline) plus a light synthesis mention in "how to choose" — within the 3–5 target for a multi-section article; intro / conclusion / FAQ kept product-light by design.

## Word-target ledger

| Section | Target |
|---|---|
| Introduction | 180 |
| H2 #1 Forget you (memory) | 430 |
| H2 #2 Repeat / loop | 340 |
| H2 #3 Character drift | 360 |
| H2 #4 Paywall / coins | 390 |
| H2 #5 Text-only / no voice | 340 |
| How to choose | 300 |
| Conclusion | 120 |
| FAQ | 320 |
| **Total** | **~2,780** (within band 2,400–2,800; ±10% of 2,600) |

## Visual ledger (density + ≥3 distinct types)

- Intro: chart (taxonomy)
- #1: diagram + screenshot
- #2: diagram
- #3: screenshot
- #4: table + screenshot
- #5: screenshot
- How to choose: table
→ Types used: chart, diagram, screenshot, table = **4 distinct** (≥3 ✓). ~9 visuals for a ~2.8k-word article (target band 10 for 2–3k — close; #2/#3 carry single visuals by design, acceptable for explanatory/transition-heavy sections).

## Component ledger (caps respected)

- `:::nutshell` ×1 (intro) ✓ ≤1
- `:::key-takeaways` ×1 (conclusion) ✓ ≤1
- `:::cta` ≤2 (one high in #4, one low in "how to choose") ✓ ≤2
- `:::definition` ×1 (#1, "context window"), `:::pullquote` ×1 (#3), `:::table` ×1 (#4), `:::feature-matrix` OR `:::decision-table`+`:::preferred-order` ×1 (how-to-choose), `:::note` ×1 (#5), `:::sidenote` optional ×1 (#2), `:::faq` ×1 (FAQ) — 1 of each, never stacked. ✓
- No `:::methodology` (not a data study). No competitor-pricing matrix (constraint).

## Notes — sources & internal links

- **Internal links (verified live, descriptive anchors):** ai-companion-best-memory (#1 + FAQ), what-do-ai-companion-coins-actually-cost (#4), what-breaks-immersion-ai-roleplay (#3), ai-companion-vs-chatgpt-companionship (intro/#3), pleasur-ai-vs-secrets-ai (how-to-choose, optional). Do NOT link `ai-companion-memory` (not in inventory).
- **First-party fact-lock:** pricing + voice/call statuses live-verified 2026-06-28 (pleasur.ai/pricing), match brand-config Canonical block — no drift.
- **Secondary keywords to work in naturally:** ai companion app, best ai companion app, free ai companion app, ai companion app for adults, ai companion memory, persistent memory, voice, character consistency; adjacent: ai girlfriend app. Named competitors (character ai, replika, nomi, kindroid, candy ai, talkie ai) only as hedged, neutral references — never with fabricated failure stats.
- **Constraint guardrails for /draft:** 3-tier coin pricing only (no flat/no-tokens/no-hidden-fees); VOICE not video; competitor failings hedged; no first-person "82%"; 18+ throughout; no internal-tool/vendor names in reader copy.
