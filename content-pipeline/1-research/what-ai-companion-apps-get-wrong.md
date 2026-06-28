# Research: what do ai companion apps get wrong

> **Run:** PLE-3034 · **Slug (fixed):** `what-ai-companion-apps-get-wrong` · **Researched:** 2026-06-28
> **Data layer:** Ahrefs REST API v3 (`AHREFS_API_KEY`, `country=us`) + Firecrawl page extraction + live first-party WebFetch.
> ⚠ **AHREFS MCP UNAVAILABLE this run** — the `mcp__ahrefs__*` tools are not loaded in this stage's toolset. Used the **Ahrefs REST API (same source, same units pool)** per the outage ladder. Fix the MCP wiring. NO non-Ahrefs SEO source was used.

## Keyword metrics

The exact target phrase **"what do ai companion apps get wrong"** has **no measurable volume or SERP in Ahrefs** (zero-volume long-tail / question framing). This is expected — it is an *angle*, not a head term. The article must be written to the **parent head term it actually competes in**, while owning the question framing for PAA/AI-Overview capture. Metrics below are the real, volume-bearing cluster (Ahrefs REST, US, fetched 2026-06-28):

| Keyword | Volume (US) | KD | CPC | Parent topic | Intent |
|---|---|---|---|---|---|
| **ai companion** | 17,000 | 65 | $90 | replika | informational + commercial |
| ai companion app | 1,400 | 75 | $110 | ai companion app | informational + commercial |
| **ai companion apps** (benchmark SERP) | 400 | 61 | $110 | ai companion app | informational + commercial |
| best ai companion app | 600 | 50 | $130 | ai friend | informational + commercial |
| free ai companion app | 350 | 70 | — | — | commercial |
| ai companion app for adults | 200 | 53 | — | — | commercial |
| best free ai companion app | 200 | 54 | — | — | commercial |

- **Parent topic:** `ai companion app`. Write to the parent + own the "what apps get wrong / failures / limitations" question space (informational entry that funnels to commercial-investigation).
- **Dominant intent:** informational → commercial-investigation. Reader is frustrated with their current companion app and is evaluating alternatives — exactly the problem-aware framing in the run brief.
- **Beatability:** moderate. The SERP is split between un-beatable navigational results (app-store listings, brand homepages: Replika DR 99/97, Kindroid DR 51, Nomi DR 59) and **beatable editorial articles** (aicompanionguides DR 11, sitepoint, genies, eastbayexpress). We compete with the *editorial* slice — none of it is answer-first on the "what they get wrong" angle, and none anchors on **memory** as the lead failure. That gap is ours.

## Long-tail variations (same parent topic)

- ai companion app (1,400) — commercial-investigation
- best ai companion app (600) — commercial
- free ai companion app (350) — commercial
- ai companion app for adults (200) — commercial (18+ relevance)
- best free ai companion app (200) — commercial
- best ai companion app 2025 (100) — commercial
- nsfw ai companion app (60) — commercial (18+)
- companion ai app (100) — informational
- ai girlfriend app (4,100) — adjacent commercial (related-terms)
- best ai girlfriend (3,200) — adjacent commercial
- Named competitors users compare in this space (related-terms + SERP): character ai, talkie ai, candy ai, nomi, kindroid, replika, anima, paradot, tolan.
- Topic-adjacent terms searchers attach to this cluster (related "also talk about"): **voice** (215k), **emotional support** (5,200), **personality traits** (81k), **real time** (22k), conversational ai (10k), ai voice (37k). → memory/continuity, voice, and personality consistency are the conversation searchers already have around this term.

## Questions people ask

Sourced from Ahrefs `serp-overview` People-Also-Ask features for `ai companion apps` + matching-terms (`match_mode:terms`) + competitor FAQ sections. Grouped into themes:

### Theme: Memory / continuity (the lead failure — anchor here)
- Why do AI chatbots forget conversations? *(required FAQ #1)*
- Does [app] remember previous conversations? *(required FAQ #3)*
- Which AI companion apps have the best memory? *(required FAQ #2)*
- Why do they forget what you told them? (competitor H3, eastbayexpress/genies)

### Theme: What goes wrong / limitations
- What do AI companion apps get wrong? *(required FAQ #4)*
- Are AI Companion apps real? (PAA)
- What are the current limits of AI friends? (genies H2)

### Theme: Cost / value
- Is there any free AI companion? (PAA)
- Do I really need to pay for a subscription to have a good experience? (genies FAQ)
- How much do these apps really cost? (genies H2 — token/coin systems)

### Theme: Choosing / best
- What is the best companion AI? (PAA)
- What is an AI companion app? (PAA)
- What is the best AI companion in 2024/2026? (Reddit/Quora SERP entries)

## SERP overview (benchmark keyword: `ai companion apps`)

- **Dominant intent:** mixed informational + commercial-investigation; SERP blends navigational (app stores, brand homepages) with editorial "best of" listicles and Reddit/Quora discussion.
- **Dominant editorial content type:** **listicle / ranked round-up** ("N best apps") with a comparison table and per-app breakdowns; the strongest pages bolt a *limitations / what-goes-wrong / cost* explainer onto the list.
- **SERP features:** People Also Ask present (4 Q's captured), Reddit + Quora discussion results ranking on page 1 (strong voice-of-customer signal — searchers want honest, lived-experience answers, not spec sheets).
- **Brand/competitor presence:** Replika (DR 99/97 app-store), Nomi (DR 59, tr 17.5k), Kindroid (DR 51, tr 13.4k), aicompanionguides (DR 11), sitepoint, genies, eastbayexpress, Reddit r/Innovation (DR 95).

## Top-ranking pages — summaries (Firecrawl-extracted)

### #1 (editorial): aicompanionguides.com — "10 Best AI Friend Apps 2026: Free Options That Actually Listen"
- **Word count:** ~3,060 · **H2:** 15 · **Format:** listicle, **10 items** · **Tables:** 1 (comparison "At a Glance")
- **Headers:** At-a-glance + comparison table → 10 ranked apps (Pi, Character.AI, Replika, Kuki, Anima, Woebot, Cleverbot, Kindroid, SimSimi, Xiaoice) → **"AI Friend Apps That Failed: Learn From My Mistakes"** → How to Choose → Final Verdict.
- **Does well:** first-person testing voice, comparison table, a "what failed" section.
- **Thin where:** failures are anecdotal (apps that shut down), NOT the *recurring product failures* (memory, repetition, drift, paywalls). No memory-first framing. No answer-first BLUF.

### #2 (editorial): genies.com — "6 Best AI Companion Apps: A Side-by-Side Look"
- **Word count:** ~5,510 (longest on SERP) · **H2:** 13 · **Format:** listicle + explainer hybrid · **Tables:** 0 (prose breakdowns)
- **Headers:** What to look for → top apps → **How Much Do These Apps Really Cost?** (token systems, freemium paywalls) → What Real Users Are Saying → Privacy → AI & real relationships → **The Current Limits of AI Friends** (forgetful, emotional limits, glitches) → Getting started → **FAQ**.
- **Does well:** explicitly covers cost/token models, user-quote synthesis, a limitations section, and a real FAQ. This is the closest competitor to our angle.
- **Thin where:** limitations are lumped into one generic section ("forgetful, emotional, glitches"); memory is one bullet, not the thesis. Cost section stops at "tokens exist" without honest tier transparency. No voice/continuity solution offered.

### #3 (editorial): eastbayexpress.com — "Best AI Girlfriend Apps and Sites of 2026"
- **Word count:** ~4,440 · **H2:** 6 · **Format:** ranked review + essay · **Tables:** 0 (a "Quick Comparison" prose block)
- **Headers:** Quick Comparison → **How I Tested (lived-with, 4+ days)** → The Rankings → **The AI Girlfriend Problem Nobody Talks About** → **Questions Everyone Keeps Asking** (FAQ-ish) → Where This Goes.
- **Does well:** strongest voice-of-customer / lived-experience testing; explicitly tests *memory* ("did they remember my mom's name? reference previous conversations unprompted?"), *voice calls* ("voice calls that feel like phone calls with a real person"), and *generic-bot feel* (personality). Names continuity + voice as the differentiators between "real companions" and "chatbots."
- **Thin where:** adult-leaning, names third-party brands, no structured failure taxonomy, no answer-first lede.

### #4 (editorial): sitepoint.com — "5 Best AI Companion Apps"
- **Word count:** ~1,420 (thinnest) · **H2:** 6 · **Format:** listicle, **5 items** · **Tables:** 0
- Five apps (HeraHaven, Replika, Character AI, Talkie AI, Novel AI) + "Finding Your Perfect Digital Companion." Shallow; no failures/limitations/memory treatment. Easy to beat on depth.

### #5 (discussion): Reddit r/Innovation — "My one-year ranking of AI companion apps" (DR 95, tr 988)
- Extraction blocked (Reddit), but its page-1 presence + the Quora results confirm searchers reward **honest, lived-experience, problem-aware** content over spec sheets. The article's first-person + community-pain framing matches this demand.

## SERP benchmark

| Metric | Value |
|---|---|
| Median word count (top 3 editorial) | **~4,440** (genies 5,510 / eastbay 4,440 / aicompanionguides 3,060) |
| Max word count (top 5) | ~5,510 (genies) |
| Modal format | Listicle / ranked round-up **+ limitations/cost explainer** |
| Item count range (when list-shaped) | 5–10 apps (median ~6) |
| Pages with a comparison table | **1 of 5** explicit table; 2 more use a "quick comparison" prose block → table is a differentiator, not table-stakes |
| Typical visual count | 1 hero/comparison visual + per-app screenshots (lived-experience pages use real app screenshots) |

## Content gaps and opportunities

- **Consensus topics (covered by 3+ of the extracted pages → MUST cover):**
  1. **Memory / forgetting** — every editorial page touches it; eastbay tests it directly, genies leads its limits section with it. *No one makes it the thesis.*
  2. **Cost / paywalls / token (coin) systems** — genies + eastbay both have dedicated cost sections; freemium-paywall frustration is universal.
  3. **Personality consistency / "feels like a generic bot"** — eastbay's core testing axis; genies' "What Real Users Value" = consistent personality + reliable memory.
  4. **What to look for / how to choose** — every listicle has a selection-criteria section.
  5. **Voice / talking to your companion** — eastbay names voice calls as the real-vs-chatbot divider; "voice" is a 215k related term.
- **Partial topics (1–2 pages → differentiate by going deeper):** repetition/looping replies (implied in "feels generic," not named as its own failure anywhere), continuity *across sessions* (vs. within one chat), honest tier-by-tier pricing transparency.
- **Gaps nobody on page 1 owns (information-gain):**
  - A **memory-first failure taxonomy** — naming the five recurring *product* failures (poor memory, repetition/looping, character drift, hidden coin/token costs, missing voice) as a structured framework, not anecdotes.
  - **Repetition / looping replies as a named, explained failure** (why context-window churn causes it) — absent from every page.
  - **Honest paywall transparency** — the editorial pages say "tokens exist, it's confusing"; none models *what transparent coin pricing actually looks like*. We can demonstrate it first-hand (3 named tiers, coin allowances, per-action costs — sourced live).
  - **A first-hand product walkthrough** showing persistent-memory continuity + in-chat voice in action (screenshots), which no editorial page has.

## First-party fact lock (step 6 — fetched LIVE this run)

**Pleasur.ai pricing — source: https://pleasur.ai/pricing (fetched 2026-06-28):**
| Tier | Monthly | Annual equiv. | Coins/mo |
|---|---|---|---|
| Starter | $12.99/mo | $5.20/mo (saves $93/yr) | 1,500 |
| Standard | $27.99/mo | $11.20/mo (saves $201/yr) | 5,000 |
| Ultimate | $49.99/mo | $20.00/mo (saves $360/yr) | 10,000 |

- **Media metered by coins on every tier (live):** AI image generation 10 coins each · voice notes 10 coins each · **phone calls 50 coins/min** (Standard + Ultimate). All tiers: unlimited messages, buy-more coins, cancel anytime, 7-day money-back. **No tier is unlimited; nothing flagged "coming soon."**
- **Drift check:** live page **matches** the `brand-config.md` Canonical pricing block exactly — **no drift, no refresh needed.**
- **Voice/continuity (live):** real-time two-way **VOICE** phone calls + in-chat voice-note playback are **live** (confirmed on live pricing page 2026-06-28; brand-config refreshed 2026-06-24). ✅ The voice-continuity angle is valid this run. ❌ **AI video remains roadmap — never claim two-way video calls.**
- **Memory:** persistent memory layer (saves facts, preferences, relationship history across sessions) is the load-bearing product claim for the thesis. Frame as a persistent-memory *layer/architecture* vs. fixed context windows. Do NOT use the "82% memory" stat first-person (attributed MariaVibe citation w/ URL only, if at all).

## Deep web research findings

OpenRouter deep-research (`BLOG_AGENT_DEEP_RESEARCH`) **not run** (off by default; SERP top-page extraction is primary). Voice-of-customer was captured directly from the Firecrawl-extracted SERP competitors, which surface lived-experience evidence aligned with the community brief (r/AIChatCompanions pain points). Representative themes/quotes from extracted pages:

- **Memory/continuity is the make-or-break test.** eastbayexpress's whole methodology: *"Did they remember my mom's name? Did they reference previous conversations without me prompting them?... The results separated the real companions from the chatbots quickly."* The apps that "work" are the ones whose *"memory system creates continuity that feels earned."*
- **Generic-bot feel = personality failure.** *"The good ones create moments that feel real, and the bad ones feel like talking to a customer service bot immediately... The rest felt artificial from the first message."*
- **Voice is the real-vs-chatbot divider.** *"If you want voice calls that feel like phone calls with a real person, [it] is the clear choice."*
- **Paywalls/tokens frustrate.** genies: *"While many apps advertise themselves as free, the most meaningful experiences are often behind a paywall... from simple monthly subscriptions to more complex token-based systems... without any surprise charges."*
- **Forgetting is the #1 named limitation.** genies' limits section leads with apps being *"forgetful,"* then emotional limits, then glitches.

*Competitor failing claims to keep hedged per brief: any "resets after N messages" stays "widely reported / users report" — never stated as verified fact.*

## Recommended angle

**Thesis:** AI companion apps fail on the same five things — and **memory is the root failure**: an app that forgets you can't hold a consistent character, can't avoid repetition, and can't justify its paywall; we reframe "what they get wrong" as a memory-first failure taxonomy and show what persistent memory + in-chat voice continuity actually fixes (demonstrated first-hand, with transparent coin pricing — not "free/flat").

**Why this angle wins:** the SERP's editorial pages each *touch* memory, cost, and personality but bury them as one-off limitation bullets inside "best app" listicles. **None leads with memory, none names repetition/looping as its own failure, and none models honest paywall transparency.** An answer-first, problem-aware piece that (a) opens with a 40–60 word BLUF answering "what do AI companion apps get wrong," (b) gives each pain point its own H2 with the fix woven in, (c) demonstrates persistent-memory continuity + live voice first-hand, and (d) ends with the four required FAQ questions for FAQPage schema, beats every editorial incumbent on structure, depth, and information gain — while matching their lived-experience credibility that the Reddit/Quora SERP presence rewards.

## BEAT SPEC (guides the outline; the floors enforce only the depth + coverage minimums)

- **Target word count:** **~2,400–2,800 words** (depth bar to match/beat). The editorial top-3 median is ~4,440, but those are 6–10-app *listicles* padded with per-app reviews; this article is a focused *failure-taxonomy explainer*, not a round-up, so it wins on usefulness/density at a tighter count rather than padding to the listicle median. Floor: do not ship thin — must clear ≥80% of its own target (~1,920 words min). Never pad to a number.
- **Format:** problem-aware **explainer**, structured as **5 named-failure H2s + FAQ** (not a listicle). Each failure H2 = the pain point + why it happens + the pleasur.ai fix woven in (answer-first, not bolted on).
- **Comparison table:** **OPTIONAL but recommended** (only 1 of 5 SERP pages has a true table — a table is a differentiator, not table-stakes). If included, a "failure → why it happens → what fixes it" table is higher information-gain than yet another app-spec grid. Do NOT build a competitor-pricing comparison table that asserts unverified competitor numbers.
- **Must-cover topics (consensus — every one becomes outline coverage):**
  1. **Poor memory / forgetting** — THE lead failure; H2 #1, ties to the H1. Fixed-context-window explanation → persistent memory layer.
  2. **Repetition / looping replies** — information-gain H2 (nobody names it); explain the context-churn cause.
  3. **Fake / inconsistent characters (personality drift)** — consistency = what users value most.
  4. **Paywalls / hidden coin (token) costs** — honest angle = *transparent* coin pricing (3 named tiers, sourced live), NOT "free / flat / no tokens."
  5. **Missing voice / text-only** — pleasur.ai's live two-way VOICE + in-chat voice notes (voice ≠ video).
- **Differentiation topics (go deeper than the SERP):** repetition-as-its-own-failure with a mechanism explanation; cross-session continuity vs. within-chat memory; transparent tier-by-tier coin pricing modeled honestly.
- **Information gain (≥1 REQUIRED):** the **memory-first five-failure taxonomy** + a **first-hand product walkthrough** (persistent-memory continuity and in-chat voice shown in real screenshots) — neither exists anywhere on page 1.
- **Secondary keywords to work in naturally:** ai companion app, best ai companion app, free ai companion app, ai companion app for adults, ai companion memory, persistent memory, voice, character consistency; adjacent: ai girlfriend app. (Named competitors only as hedged, neutral references — character ai, replika, nomi, kindroid, candy ai, talkie ai — never with fabricated failure stats.)
- **FAQ (RESERVED — hard requirement for FAQPage JSON-LD; visible `## FAQ` section, these 4 questions verbatim-intent):**
  1. **Why do AI chatbots forget conversations?**
  2. **Which AI companion apps have the best memory?**
  3. **Does pleasur.ai remember previous conversations?**
  4. **What do AI companion apps get wrong?**
- **Beatability:** moderate. App-store/brand-homepage results are un-beatable but irrelevant (different intent). The editorial slice (DR 11–59) is beatable on structure + answer-first depth; none owns the memory-first angle. Win condition: be the *honest, problem-aware* page the Reddit/Quora SERP presence proves searchers want.

## HARD brand constraints (carried from run brief — gate-failing if violated)
- Pricing: 3-tier coin-metered ONLY ($12.99/1,500 · $27.99/5,000 · $49.99/10,000). NEVER "flat / no tokens / no hidden fees." Honest paywall angle = transparent coin pricing.
- Voice/video: real-time two-way **VOICE** + voice notes are live. NEVER claim two-way video calls (AI video = generated clips, roadmap). Anchor continuity on voice + persistent memory.
- Memory stat: no first-person "82%"; attributed MariaVibe citation w/ URL only if used. No fabricated competitor "Nx recall" counters.
- Competitor failings: always hedged ("widely reported," "users report") — never verified fact.
- Compliance: 18+ framing throughout; no "no filter/anything goes"; no safety guarantees; no real-person likenesses.
- Internal-stack scrub: reader-facing copy never names Strapi, Doppler, PostHog, DataForSEO, Ahrefs, Firecrawl, OpenRouter, Paperclip, Semrush.
