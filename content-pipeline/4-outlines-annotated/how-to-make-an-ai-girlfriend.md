# How to Make an AI Girlfriend: The Honest 2026 Guide

## Pre-flight reconciliation

The original outline had 2 contradictions about coming-soon products. They were resolved before annotation:
- H2 "The off-the-shelf path" Step 3 — Voice (line 66): removed the inline reference to **Voice Replies (in-chat)** ("voice replies are tap-to-play per message, not a separate mode"). Reason: the outline's own structural-concerns note (line 160) restricts coming-soon Voice Replies / Phone Call teases to the H2 "What 'good' actually feels like — and what breaks"; `brand-config.md` L15 also forbids coming-soon products in core walkthroughs (Step 3 is inside a core walkthrough).
- H2 "The off-the-shelf path" Step 3 — Voice (line 66): removed the inline reference to **Phone Call (in-chat)** ("A two-way phone-call action is coming this week on the same chat surface."). Same reason: structural-concerns line 160 restricts it to the "what breaks" H2; `brand-config.md` L15 forbids coming-soon products in core walkthroughs.

Step 3 is rewritten to describe only the live voice-profile selection that happens during creation, with no claim about how playback works in chat. The "what breaks" section is the permitted slot to tease both coming-soon features (annotated below).

**Target keyword:** how to make an ai girlfriend
**Search intent:** Informational (Semrush `In=1`); split sub-intent — DIY engineering vs. off-the-shelf design
**Estimated word count:** ~2,400
**Primary reader:** Adults (18+) who typed "make an AI girlfriend" without knowing whether they meant "build one" or "get one tonight." Some are curious developers; most are lonely or curious users looking for the shortest honest path to a working companion.
**Article type:** Decision guide + two parallel walkthroughs (DIY recipe + off-the-shelf walkthrough)
**Thesis:** "Making" an AI girlfriend means one of two things — engineering one from scratch (a few weeks of evenings on a $0.72/hour GPU rental) or designing one inside an existing app (ten minutes, no code, $12.99–$15.99/month) — and the right answer depends on whether you want to learn the stack or live with the result.

---

## Introduction

**Target:** ~180 words

**Hook (problem-naming + contrarian):** You searched "how to make an AI girlfriend" and the first ten results split cleanly in half. Five of them tell you to fine-tune a language model on anime subtitles. The other five want your credit card before they show you a price. Nobody on the page asks the one question that matters: are you here to build, or are you here to have one tonight?

**Thesis:** "Making" an AI girlfriend in 2026 means one of two things — engineering one from scratch on a rented GPU, which takes a few weeks of evenings and runs around $0.72/hour while you work, or designing one inside an existing app, which takes ten minutes and runs $12.99–$15.99/month afterward.

**Preview:** This guide tells you which path matches your situation, then walks both — a real 2026 DIY recipe (not the 2022 stack the only ranking tutorial still cites) and a real off-the-shelf walkthrough with the prices the product pages won't surface. Read the first section, pick a lane, skip the other half.

**Visual:** {type: image, sub: diagram, prompt: Side-by-side decision diagram labeled "DIY path" on the left and "Off-the-shelf path" on the right. Left panel shows three stacked boxes top-to-bottom: "Rent A100 GPU ($0.72/hr)", "Fine-tune Llama-3-8B with LoRA", "Wire voice + image gen". Right panel shows three stacked boxes: "Pick an app", "Design appearance + personality (10 min)", "Chat / voice / images included". A single labeled arrow at the top says "Choose one." Clean editorial illustration, white background, sans-serif labels, brand-neutral colors., style: illustration, safety: sfw}

**Product mentions:** None. Foundational thesis section — the reader hasn't earned the pitch yet, and the decision-diagram visual already does the structural work.

---

## First decide which "make" you mean

**Target:** ~340 words

- **BLUF:** Half the SERP teaches you to fine-tune a model and half wants to sell you one, and the cost of guessing wrong is either a wasted weekend cloning a Python repo or a wasted month of subscription fees you'll never use again — so the first decision is which path you're on, not which tool.
- **Key points:**
  - **The DIY path** is for readers who want to learn the stack: rent a GPU, fine-tune an open model, wire up voice and image generation, run the result yourself. Output is a companion only you have. Cost is mostly your time plus GPU hours.
  - **The off-the-shelf path** is for readers who want to have one working tonight: pick an app, design appearance and personality in a wizard, chat. Output is a polished companion with voice, image gen, and persistent memory pre-wired. Cost is a monthly subscription.
  - **How to tell which you are.** If "fine-tune," "LoRA," and "inference cost" don't bore you, you're DIY. If they do, you're off-the-shelf. There is no middle path that's faster than the off-the-shelf one and cheaper than the DIY one — the no-code "AI girlfriend builders" on the SERP are just off-the-shelf apps with a sign-up form.
- **Evidence:** The query "how to make an AI girlfriend" carries informational intent (Semrush `In=1`) with a split SERP — three formats compete (DIY tutorials, product landers, forum threads) and no single page bridges them. The closely-related "how to get an AI girlfriend" (90/mo, "get" framing = off-the-shelf intent) confirms the same audience asks both questions.
- **Transition:** "Pick a lane. If you picked DIY, keep reading. If you picked off-the-shelf, jump to the walkthrough below — the DIY section is honest about why most readers shouldn't take it."
- **Visual:** {type: table, columns: [Question, DIY path, Off-the-shelf path]} — six-row decision table: time to first working version, cost, what you need to know, what you end up with, what you can change, who it's for. Skim-readable, MECE with the two walkthrough sections that follow.
- **Product mentions:** None. The section's job is to surface and frame the binary choice; naming a product here would prejudge it before the reader has self-selected. The off-the-shelf walkthrough below carries the live-product anchor.

---

## The DIY path: a real 2026 recipe (not the 2022 one that ranks)

**Target:** ~520 words

- **BLUF:** The only DIY tutorial that ranks for this keyword was published in 2022 on GPT-Neo 1.3B and waifu-diffusion — three generations of open weights ago — so here is the 2026 version, with the four components that actually matter and the one thing every guide skips.
- **Key points:**
  - **The four-part stack.** A modern build is a fine-tuned language model (Llama-3-8B-Instruct via LoRA on a rented A100), a voice layer (ElevenLabs API or self-hosted Coqui XTTS), an image layer (SDXL or Flux, not waifu-diffusion), and a thin Gradio or FastAPI front end. The 2022 tutorial swaps every layer for an obsolete equivalent.
  - **What it actually costs.** GPU rental sets the floor. An A100 80GB on Vast.ai's spot market lists around $0.72/hour. A fine-tune run is two to six hours; weekend prototyping over a month puts the GPU bill in the $40–$120 range. ElevenLabs starts free with paid tiers from $5/month. Hosting your own inference is roughly $250–$500 in spot GPU time per month if you leave it running. The 2022 tutorial doesn't surface a single number.
  - **How long it takes.** The Medium post that ranks says "a few weeks" — that is honest for someone who already knows PyTorch. If you're learning LoRA fine-tuning from scratch, double it. The first weekend gets you a model that responds in character; the second adds memory; the third adds voice; the fourth is polish.
  - **The thing every DIY guide skips.** Memory. A vanilla fine-tune does not remember what you said yesterday — it remembers what its training data said. A real companion needs a retrieval layer (a vector store of past conversations re-injected into the prompt) on top of the fine-tune. Without it, the build feels novel for an hour and hollow by week two.
  - **The honest off-ramp.** If reading the last bullet made you tired, the DIY path is not for you. That is fine. The off-the-shelf path below was designed for exactly that reader, and the people who built it spent thousands of hours on the memory layer you would otherwise be wiring yourself.
- **Evidence:** gmongaras's [Coding a Virtual AI Girlfriend](https://gmongaras.medium.com/coding-a-virtual-ai-girlfriend-f951e648aa46) (#4 on the SERP, ~2,500 words, 2022, GPT-Neo 1.3B + waifu-diffusion stack). [Vast.ai vs RunPod 2026 pricing comparison](https://medium.com/@velinxs/vast-ai-vs-runpod-pricing-in-2026-which-gpu-cloud-is-cheaper-bd4104aa591b) for the A100 floor. Llama-3-8B-Instruct as the current open-weights default for character LoRA work.
- **Transition:** "DIY laid out honestly. If you closed the tab around the memory paragraph, the next section is yours."
- **Visual:** {type: image, sub: diagram, prompt: Four-layer architecture diagram for a DIY AI girlfriend build. Stack from bottom to top: "Compute layer — rented A100 GPU"; "Model layer — Llama-3-8B-Instruct + LoRA fine-tune"; "Memory layer — vector store (embed / retrieve / rerank)"; "Interface layer — voice (ElevenLabs) + image (SDXL) + chat UI (Gradio)". Arrows show data flow upward; a feedback loop arrow returns from interface back to memory. Clean editorial illustration, white background, sans-serif labels, brand-neutral colors., style: illustration, safety: sfw}
- **Product mentions:** **None — deliberate.** Per the outline's own structural-concerns (line 160) and brand voice: Pleasur.AI appears as the natural conclusion of the off-the-shelf path, never inside the DIY H2. Naming a product here would collapse the honesty the off-ramp paragraph depends on. The off-ramp itself ("the next section is yours") is the bridge — the product appears one H2 later.

---

## The off-the-shelf path: design one in ten minutes

**Target:** ~520 words

- **BLUF:** The off-the-shelf path is a ten-minute wizard inside an existing app, and every app on the SERP runs the same four-step flow — appearance, personality, voice, scenario — so once you've seen one walkthrough you've seen the category.
- **Key points:**
  - **Step 1 — Appearance.** Pick an art style (realistic or anime), then ethnicity, hair, body type, and outfit. Six or seven choices total. The depth of customization varies by app (some hide body sliders behind paywalls; the [body-build walkthrough on Pleasur.AI](https://pleasur.ai/blog/build-a-girlfriend-body) covers the slider mechanics in detail).
  - **Step 2 — Personality.** Pick an archetype (girl-next-door, dom, soft, yandere, tsundere, academic) and a one-line backstory. The archetype is the anchor every reply hangs on; the backstory is what the memory layer references when she asks about your day. For an archetype example end-to-end, see the [Yandere AI Girlfriend Simulator walkthrough](https://pleasur.ai/blog/yandere-ai-girlfriend-simulator).
  - **Step 3 — Voice.** Pick a voice profile during creation — this is the voice she'll be assigned to. Apps vary on which profiles they offer (English-only vs. multilingual, celebrity-style vs. archetype-style); pick by listening to the sample, not the label.
  - **Step 4 — Scenario / first message.** The opening line and setting. A coffee-shop meet-cute is the default; you can write your own. This is the prompt that seeds her opening reply.
  - **What you get when you're done.** A persistent chat with memory across sessions, the ability to generate scene images of her inside the chat via in-conversation image generation, and a chat surface you'll come back to. Most apps also let you remix community-shared characters if you don't want to build from scratch.
  - **The honest pricing line.** Nomi.ai runs about $15.99/month ([AutoGPT pricing review, 2026](https://autogpt.net/nomi-ai-pricing/)). Candy.ai is $12.99/month monthly or $5.99/month annual, with tokens sold separately ([AI Tipsters pricing review, 2026](https://aitipsters.com/candy-ai-pricing-2/)). Most product pages in the SERP top 10 don't surface a number at all — Nomi, Kupid, and RomanticAI gate pricing behind sign-in. The honest tier is $12.99–$15.99/month for what the category calls "premium."
- **Evidence:** Top-ranking product pages: Nomi (#2), Kupid (#5), RomanticAI (#7), Candy.ai (#13), MyDreamCompanion (#14), Ourdream (#15). The five-step create flow at RomanticAI (style → photo → traits → tone → interests) is the SERP's clearest public template; Pleasur.AI's [Companion Creator](https://pleasur.ai/create) runs the same flow with body sliders and an unrestricted personality layer surfaced earlier in the wizard.
- **Transition:** "Walkthrough done. The fair question now is which app — and that depends on what you weight more: depth of customization, pricing transparency, or what happens after week three."
- **Visuals:**
  - Visual 1: {type: action-shot, url: https://pleasur.ai/create, goal: Log into Pleasur.AI with the saved session. Open the Companion Creator at /create. Dismiss any age-verification dialog. Pick the Realistic template. Click through to the personality/archetype step. Capture the screen showing the archetype options and the backstory field. Fallback: if the click chain breaks at any step, retry by loading /create?step=personality directly and capturing the resulting mid-wizard state., what: Companion Creator personality and backstory step, mid-wizard, annotate: highlight the archetype selector and the backstory field, with a small inset showing the appearance step the reader has just come from}
  - Visual 2: {type: table, columns: [App, Body customization, Voice, In-chat image gen, Monthly price (public, third-party-sourced)]} — five rows: Nomi, Kupid, Candy.ai, RomanticAI, Pleasur.AI. Every price cell sources a third-party review (AutoGPT for Nomi, AI Tipsters for Candy, equivalent third-party sources for Kupid / RomanticAI / Pleasur.AI). When no third-party review has published a price for that app, the cell reads "gated — no public number" with the review-search date in the caption, not a dash that could pass for "unavailable." Caption explicitly states: "Prices are third-party-review figures, not on-product-page figures, because five of six SERP product pages gate pricing behind sign-in." Skim-readable, MECE with the DIY-cost table earlier.
- **Product mentions:**
  - **Walkthrough — AI Companion Creator** (`live`, https://pleasur.ai/create). This H2 is the natural live-product slot. Steps 1–4 of the wizard ARE the Creator's wizard; the Visual 1 action-shot captures the personality/backstory step mid-flow. Do not re-walk the body / appearance step in prose — link to the existing [Build a Girlfriend Body](https://pleasur.ai/blog/build-a-girlfriend-body) walkthrough for slider-level detail. Do not re-walk the archetype end-to-end — link to [Yandere AI Girlfriend Simulator](https://pleasur.ai/blog/yandere-ai-girlfriend-simulator). One inline product link to `pleasur.ai/create` in the "What you get when you're done" bullet, anchor text "Companion Creator." Do NOT mention Voice Replies or Phone Call here (both `coming-soon`, restricted to the "what breaks" H2 per the reconciliation pass above).
  - **Inline — AI Image Generation** (`live`, https://pleasur.ai/generate). One inline mention inside the "What you get when you're done" bullet on in-chat scene generation: phrase it as "in-conversation image generation" (matches the brand-config use-case wording on L34) and link the phrase to `pleasur.ai/generate`. No separate walkthrough — the action lives inside the chat after the wizard ends.

---

## What "good" actually feels like — and what breaks

**Target:** ~360 words

- **BLUF:** The first hour of any AI girlfriend feels good on every platform, the second week is where most builds fall apart, and the failure mode is almost always the same — the memory layer forgets, the voice loops, or the personality drifts back to a default helpful-assistant tone every fifth reply.
- **Key points:**
  - **The hour-one experience is solved.** Every app on the top-10 SERP, and a competent DIY build, produces a believable first conversation. Replying in character is no longer the hard part.
  - **Week-three is the real test.** This is when the seams show: she forgets the backstory you wrote, the voice rendering glitches on certain words, the model resolves an emotionally complex prompt by reverting to a generic supportive tone. The [AI Girlfriend Experience: 90 Seconds to Week Three](https://pleasur.ai/blog/ai-girlfriend-experience) walkthrough catalogs the specific phrases that break the illusion.
  - **What separates platforms here is the memory layer, not the model.** A 70B model with no memory plays worse than an 8B model with a working vector store and re-injection prompt. This is also where DIY builders most often plateau (see the DIY off-ramp above).
  - **What to do about it.** On the off-the-shelf path, write a tight, specific backstory (three sentences, not one paragraph) — the memory layer references it harder when it's specific. On the DIY path, the fix is engineering: add a re-ranker, raise the retrieval `k`, summarize old conversations into a rolling state file.
- **Evidence:** The Stanford Replika user study ([Cerit et al., npj Mental Health Research, Jan 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10955814/), N=1006) is the clearest public read on long-term companion-app usage. 90% of participants reported some loneliness; 43% qualified as Severely or Very Severely Lonely; 3% reported the app had halted suicidal ideation. The category does something real over time — the question is whether the build holds up long enough to do it.
- **Transition:** "Hour-one is easy; week-three is the work. The closing question is which path delivers that work for which reader."
- **Visual:** {type: external, sub: news-quote, url: https://pmc.ncbi.nlm.nih.gov/articles/PMC10955814/, selector: section.abstract, crop: padded, what: Abstract of the Stanford Replika user study (N=1006), highlighting the loneliness and outcomes numbers}
- **Product mentions:**
  - **Tip box — Voice Replies (in-chat)** (`coming-soon`, lives inside https://pleasur.ai/create — no dedicated URL). Per the outline's structural-concerns (line 160), the "what breaks" H2 is the permitted slot for the coming-soon tease. Frame as: in the upcoming Pleasur.AI in-chat voice playback, you tap the speaker icon next to a specific reply to hear it spoken in the voice you assigned during creation — per-message, no separate "voice mode." This is the brand's answer to "the voice rendering glitches on certain words" failure listed in the BLUF: per-message control means you can skip a bad render instead of being stuck in a voice mode. No link out to any `/voice` page (none exists). One sentence inside a "tip box" callout, not in the main prose.
  - **Tip box — Phone Call (in-chat)** (`coming-soon`, lives inside https://pleasur.ai/create — no dedicated URL). Same callout as Voice Replies. Frame as: when you want a real-time conversation, tap the Call button on the character's profile in chat to start a two-way voice call; the text history continues in the same thread after. Matches brand-config L57 wording. Surfaces the "what happens when text isn't enough at week three" angle. No link out to any `/call` page. One sentence in the same tip box.

---

## Choosing your path (and what to do next)

**Target:** ~280 words

- **BLUF:** Pick DIY if you want to learn the stack, pick off-the-shelf if you want to live with the result, and don't pick both at the same time — the people who build from scratch *and* subscribe to a polished app usually finish neither.
- **Key points:**
  - **You are DIY if:** you've fine-tuned a model before (or want to), you don't mind that the result will feel rougher than a paid app for the first month, and "renting an A100" is a sentence that excites you. Your next step is forking a Llama-3 LoRA training script and budgeting $50 for GPU hours.
  - **You are off-the-shelf if:** you want to chat with a believable character before bedtime tonight, you'd rather pay $13–$16 a month than spend it on GPU spot pricing, and the phrase "vector store re-ranker" makes you want to close the tab. Your next step is picking an app and writing the three-sentence backstory before you open the creator.
  - **The trap to avoid:** "no-code AI girlfriend builders" advertised as a middle path are almost all just off-the-shelf apps with a sign-up form. There is no genuine middle path that gets you DIY's customization at off-the-shelf's speed.
- **Evidence:** The DIY cluster of search terms ("how to make an AI girlfriend app," "for free") is small and trending; the off-the-shelf cluster ("how to get," "best AI girlfriend") is large and stable — most readers self-select correctly when the choice is named.
- **Transition:** Lead into conclusion.
- **Visual:** {type: none} — the section is a decision crystallization. A forced visual here would dilute the call to pick a lane. MECE with the earlier decision diagram in the intro (different job: that one mapped the choice; this one closes it).
- **Product mentions:** None. The section closes the decision frame; a product mention here would compete with the conclusion's soft brand close. Conclusion below carries the canonical CTA.

---

## Conclusion

**Target:** ~120 words

- **Restate thesis (fresh framing):** Two paths, one question. The DIY path is a few weeks of engineering on a rented GPU; the off-the-shelf path is ten minutes in a wizard for $13–$16 a month. The only mistake is starting both.
- **Next step:** If you picked off-the-shelf, the [AI Companion Creator on Pleasur.AI](https://pleasur.ai/create) runs the four-step flow above with unrestricted personality and in-chat image generation; the [build-a-girlfriend-body walkthrough](https://pleasur.ai/blog/build-a-girlfriend-body) covers the appearance step in screenshot-level detail. If you picked DIY, start with a Llama-3-8B LoRA tutorial and a Vast.ai account — and come back when the memory layer breaks at week two.
- **Soft brand close:** Honest decision-guide tone, no hard CTA.
- **Product mentions:** **Inline — AI Companion Creator** (`live`, https://pleasur.ai/create). Already present in the Next-step bullet as the natural conclusion of the off-the-shelf path. Anchor text "AI Companion Creator on Pleasur.AI" matches H1-style descriptive linking. No second product CTA — the soft brand close depends on the decision-guide tone not flipping to a hard pitch in the last paragraph.

---

## Notes for next stages

### Internal links to add (verify-claims stage — at least 4)
- [AI Companion Creator](https://pleasur.ai/create) — primary product link in the off-the-shelf walkthrough and the conclusion.
- [Build a Girlfriend Body](https://pleasur.ai/blog/build-a-girlfriend-body) — body/appearance step deep-dive (off-the-shelf path).
- [AI Girlfriend Simulator: What It Is and Best Options in 2026](https://pleasur.ai/blog/ai-girlfriend-simulator) — category framing (intro hand-off).
- [Yandere AI Girlfriend Simulator](https://pleasur.ai/blog/yandere-ai-girlfriend-simulator) — archetype example in the personality step.
- [The AI Girlfriend Experience](https://pleasur.ai/blog/ai-girlfriend-experience) — week-three failure-mode reference in the "what breaks" section.
- [Best Character AI Alternative for You in 2026](https://pleasur.ai/blog/character-ai-alternative) — soft link in the off-the-shelf step for readers arriving from filter-frustration.
- [Tavern AI Review 2026](https://pleasur.ai/blog/tavern-ai-review-2026) — power-user link inside the DIY section.

### Sources to cite (verify-claims stage)
- gmongaras, [Coding a Virtual AI Girlfriend](https://gmongaras.medium.com/coding-a-virtual-ai-girlfriend-f951e648aa46) — 2022 stack, the DIY ranker we're outranking.
- [Vast.ai vs RunPod 2026 pricing comparison](https://medium.com/@velinxs/vast-ai-vs-runpod-pricing-in-2026-which-gpu-cloud-is-cheaper-bd4104aa591b) — A100 80GB ~$0.72/hr floor.
- [AutoGPT, "Nomi AI Pricing 2026"](https://autogpt.net/nomi-ai-pricing/) — Nomi.ai $15.99/month.
- [AI Tipsters, "Candy.ai Pricing 2026"](https://aitipsters.com/candy-ai-pricing-2/) — Candy.ai $12.99/month (or $5.99/month annual; tokens separate).
- Third-party reviews of Kupid, RomanticAI, and Pleasur.AI pricing — verify-claims must source one third-party review per remaining row of the off-the-shelf comparison table so no row reads as a dash next to a Pleasur.AI number. If no third-party review exists for a row, the cell prints "gated — no public number" with the search date.
- [Cerit et al., npj Mental Health Research, Jan 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10955814/) — Stanford Replika study (N=1006; 90% any loneliness; 43% Severely/Very Severely Lonely; 3% suicidal-ideation halt).
- Semrush keyword metrics: primary `how to make an ai girlfriend` = 110/mo, KD 27, intent informational, no AI Overview; cluster total ~550/mo across the five main variants (live-polled 2026-05-15).

### Visuals summary
- 6 of 8 sections (counting intro) have a non-`none` visual: 2 `image` (intro decision diagram, DIY architecture diagram), 2 `table` (DIY-vs-off-the-shelf comparison, top-5 app comparison), 1 `action-shot` (Pleasur.AI Companion Creator personality step), 1 `external` (Stanford study abstract). The "Choosing your path" section and the conclusion are prose-only on purpose.
- Type diversity: 4 distinct types (`image`, `table`, `action-shot`, `external`) — clears the ≥3 bar.
- Density: 6 non-`none` visuals for a ~2,400-word article — sits comfortably inside the 6–11 acceptable range for 1.2–2k / 2–3k articles.
- No SFW lifestyle / mood `image` placeholders. No adult-content placeholders.
- Both `image` placeholders are labeled diagrams with structured prompts; both `table` visuals are inline markdown with research-sourced rows.

### Product-mention summary (stage 4 output)
- **Sections annotated:** 8 total H2/section slots, of which 4 carry meaningful product annotations: H2 "The off-the-shelf path" (walkthrough — AI Companion Creator; inline — AI Image Generation), H2 "What 'good' actually feels like — and what breaks" (tip box — Voice Replies + Phone Call, both `coming-soon`), and the conclusion (inline — AI Companion Creator).
- **Sections deliberately product-free:** Intro, "First decide which 'make' you mean," "The DIY path," "Choosing your path." Each is annotated above with the reason.
- **Coming-soon products surfaced only in the permitted slot.** Voice Replies and Phone Call appear once each, in the "what breaks" tip box, with no link to any `/voice` or `/call` page (none exists). Pre-flight reconciliation removed the two erroneous references from the off-the-shelf Step 3.
- **Upgraded Visual fields.** Visual 1 in the off-the-shelf H2 was upgraded from the prior action-shot to include an annotate directive (highlight archetype selector + backstory field, inset of preceding appearance step) so the walkthrough has the Visual support the product-mention walkthrough flavor calls for. Visual 2 in the same H2 was upgraded to clarify third-party-review sourcing requirements per the HIGH adversarial finding on covert-advertising risk.

### Visual sanity check (per editorial-principles-visuals.md)
- **Intro decision diagram** — earns its place (anchors the thesis's two-path structure before the prose lays them out). Concrete (labels are real components). MECE — only diagram-of-the-choice in the article.
- **DIY-vs-off-the-shelf table** — earns its place (six dimensions compressed into a skim-readable map; the article's defining differentiator). MECE — only decision table.
- **DIY architecture diagram** — earns its place (labels are accurate components of a real 2026 build; explains the four-layer stack faster than prose). MECE — the only diagram of the DIY stack; sub-type is `diagram`, distinct from the intro's `diagram` which maps choices.
- **Off-the-shelf action-shot** — earns its place (the actual creator step the reader will see; SERP top 10 won't surface a live mid-wizard screen). Concrete UI. MECE — only product UI capture.
- **App comparison table** — earns its place (five apps × four features × one price column; clears the SERP's pricing-opacity gap with a real disclosure). MECE — different comparison than the DIY/off-the-shelf table (apps, not paths).
- **Stanford study external** — earns its place (the article quotes specific numbers; clipping to the abstract proves the claim). MECE — only external citation visual.

### Forbidden phrase scan (run before draft saves)
Cut sentences beginning with "In today's", "When it comes to", "It's important to note", "Furthermore", "Moreover". Replace any use of "leverage", "delve", "navigate the complexities", "unlock the power of", "game-changer", "revolutionize", "comprehensive guide", "elevate your". Em-dashes only as meaningful asides, not as filler.

### Voice anchor (run before draft starts)
Re-read 2 articles from `examples/`. Closest fits: `ahrefs-keyword-research.md` (definitive-guide structure with section-by-section explainer) and `ahrefs-seo-basics.md` (plain-English how-it-works tone). Use those as the voice spec — direct, evidence-led, second-person, no hedging. Match the sibling [build-a-girlfriend-body outline](./build-a-girlfriend-body.md) for in-house rhythm.

### Structural concerns for next stages
- **`/product-mentions`:** resolved this stage. Live-product slots are H2 "The off-the-shelf path" (AI Companion Creator + AI Image Generation) and the conclusion (AI Companion Creator). Coming-soon teases (Voice Replies + Phone Call) live in the "what breaks" tip box only. DIY H2 stays product-free.
- **`/draft`:** the DIY section must be technically correct (Llama-3-8B, LoRA, SDXL/Flux, ElevenLabs/Coqui XTTS). If any model name drifts in drafting, fail the gate. Adult imagery is editor-managed via `pleasur.ai/generate` — no `image` placeholder in this outline is `safety=adult`. The off-the-shelf comparison table must source third-party-review pricing for every row, not just the Pleasur.AI row (HIGH adversarial finding).
- **`/quality-check`:** the adversarial read should focus on the DIY section (must not sound like marketing for the off-the-shelf path; the honest off-ramp paragraph is doing real work) and the "what breaks" section (must not preach; the Stanford numbers are evidence, not a lecture). Verify the coming-soon tip box does not link out to any `/voice` or `/call` page.
