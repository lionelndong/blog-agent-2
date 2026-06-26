# Brand Configuration

> Edit this file once. Every drafting and editing skill in the pipeline reads from it.

## Brand

- **Name:** Pleasur.AI
- **Blog URL:** https://pleasur.ai/blog
- **Tagline:** The hub for AI adult companions — create, chat, call, and connect with characters built for you.
- **Domain:** pleasur.ai (used by `/brand-reference` to search existing articles)
- **Category positioning:** Not just an AI companion app — a full AI adult content universe (companions, images, voice, calls, video).

## Products / Features

> Listed in priority order. The `product-mentions` skill picks the most relevant product per H2 to demonstrate. Each product has a `status` field (`live` / `coming-soon` / `roadmap`). The `product-mentions` and `update-product-mentions` skills should ONLY recommend `live` products in published articles. `coming-soon` products may be teased in roadmap or feature-announcement posts but never as core walkthroughs.

### Live products

- **AI Companion Creator** — Build a custom AI character: appearance, personality, backstory, voice, kinks, conversation style. Then chat with that character one-on-one. The flagship product.
  - URL: https://pleasur.ai/create
  - Status: **live**
  - Use cases:
    - Design a companion from scratch (appearance, personality, scenario)
    - Pick from community-shared characters and remix them
    - Chat in adult roleplay and fantasy conversations within platform rules and safety boundaries
    - Save chat history and resume conversations across sessions

- **AI Image Generation** — Generate adult-oriented images on demand. Style presets, character consistency, prompt-driven creation.
  - URL: https://pleasur.ai/generate
  - Status: **live**
  - Use cases:
    - Generate images of your created companion in different scenes
    - Explore styles (realistic, anime, art) without prompt-engineering expertise
    - Create images on demand inside an existing chat thread (in-conversation image gen)

### Voice Replies + Phone Call — now `live` (drift refresh 2026-06-24, EO/PLE-2929)

> **Status drift refreshed 2026-06-24:** both features below were flagged `coming-soon (this week)` on 2026-06-15. Live re-confirmation on 2026-06-24 via https://pleasur.ai/pricing shows "Voice notes (10 coins each)" included in all tiers and "Phone calls (50 coins/min)" in Standard + Ultimate, with NO "coming soon" qualifier — they are now billable, included features. Per the live-verification rule below, trusting the live page: both are `live`. (Homepage does not surface them; they are in-chat capabilities with no dedicated page, consistent with the note below.) **AI Video Generation remains `roadmap` — never claim video.**
>
> Both features below live INSIDE the existing chat experience — they are not standalone products and do not have their own URLs. Reference them as in-chat capabilities of the AI Companion Creator, not as separate tools. Articles must not link out to a dedicated `/voice` or `/call` page (none exists).

- **Voice Replies (in-chat)** — Inside any chat with a companion, the user taps a speaker icon on a character's message and the character "speaks" the message aloud in their assigned voice. It's a per-message playback action, not a separate mode. The conversation stays in the same chat thread; voice is one tap on top of text.
  - URL: in-chat feature — no dedicated page; lives inside `https://pleasur.ai/create`
  - Status: **live** (refreshed 2026-06-24 from coming-soon; verified live on pleasur.ai/pricing — "Voice notes (10 coins each)" in all tiers)
  - How to mention in articles:
    - Frame as a feature of the chat experience, not a separate tool
    - Show the speaker icon on the character's message bubble in screenshots
    - Don't say "open Voice Chat" — say "tap the speaker icon next to a reply"
  - Use cases:
    - Hear a companion's reply spoken in their custom voice without leaving the chat
    - Quickly switch between reading and listening on a per-message basis
    - Choose the character's voice profile when creating the companion

- **Phone Call (in-chat)** — Inside the chat, the user taps a "Call" button on the character's profile and starts a real-time two-way voice call with them. The call is launched from the chat — there's no separate phone-call product or URL. After the call ends, the conversation history continues in the same chat thread.
  - URL: in-chat feature — no dedicated page; lives inside `https://pleasur.ai/create`
  - Status: **live** (refreshed 2026-06-24 from coming-soon; verified live on pleasur.ai/pricing — "Phone calls (50 coins/min)" in Standard + Ultimate). Real-time two-way VOICE call, not video.
  - How to mention in articles:
    - Frame as an action you take from inside an existing chat with a companion
    - Show the "Call" button on the character profile / chat header in screenshots
    - Don't say "open the Phone Call app" — say "tap the Call button on the character's profile"
  - Use cases:
    - Have a real two-way voice conversation with a companion you've already been chatting with
    - Move from text to call mid-conversation without losing context
    - Pick up the text chat right where the call ended

### Roadmap (treat as `roadmap` — only mention in dedicated future-of-platform posts)

- **AI Video Generation** — Generate short adult-oriented video clips of companions. Likely starts as in-chat (per the same pattern as image gen) rather than a separate tool. Timing not committed.
  - URL: TBC (likely in-chat under the existing chat surface)
  - Status: **roadmap**
  - Use cases:
    - Generate short clips of your companion in chosen scenarios
    - Convert image-gen prompts into motion

## Canonical pricing (single source of truth — PLE-2330)

> **This block is the ONLY in-repo authority for our own prices/tiers/metering. It is NOT a substitute for live verification.** Any downstream stage that states a Pleasur.AI price, tier name, coin allowance, or media-metering fact must (a) re-confirm it against the live `pleasur.ai/pricing` page during the run and (b) if it differs from this block, trust the LIVE page and flag the drift so this block gets refreshed. Stale-by-default: treat figures here as expired once `Verified live` is older than 30 days.
>
> **Verified live:** 2026-06-15 — source: https://pleasur.ai/pricing (first-party, fetched this date).

| Tier | Monthly | Annual equiv. (billed yearly) | Coin allowance / mo |
| --- | --- | --- | --- |
| Starter | $12.99/mo | $5.20/mo (saves $93/yr) | 1,500 coins |
| Standard | $27.99/mo | $11.20/mo (saves $201/yr) | 5,000 coins |
| Ultimate | $49.99/mo | $20.00/mo (saves $360/yr) | 10,000 coins |

**Media is metered by coins on EVERY tier — no tier is unlimited.** Per-action costs (as of 2026-06-15):
- AI image generation — 10 coins each
- Voice notes — 10 coins each
- Phone calls — 50 coins/min

**Hard facts that have burned us before (do NOT assert the opposite):**
- There is **no** "$19/mo" tier and never has been. Any brief/queue/memory figure other than the three tiers above is stale or wrong — trust the live page.
- We are **not** an unlimited / no-credit-metering product. The price-concession or "no credit meter" angle is FALSE for our product; never let it become a load-bearing pillar.

## Target Reader

- **Primary persona:** Adults (18+) interested in AI companionship, generative AI for adult content, character chat, and immersive interactive experiences. Mostly digitally fluent, varies from curious newcomers ("what is an AI girlfriend / boyfriend") to experienced users comparing platforms (Candy.ai, Ourdream.ai, createporn.com, and alternatives).
- **Secondary persona:** Hobbyists in the wider gen-AI/character-AI community who care about model quality, voice realism, character customization depth, and uncensored chat capability.
- **Pain points:**
  - Mainstream chatbots (ChatGPT, Claude, Replika) are too restricted for adult conversation, roleplay, or fantasy
  - Existing AI companion apps feel repetitive, robotic, or limited in customization
  - Voice and video are still rare or low-quality across the space
  - Privacy concerns — users want a platform that doesn't leak chats or store identifying data
  - Free tiers are too limited; paid tiers are unclear in what they unlock
  - Fragmented experience — image gen, chat, voice all live in different apps; users want one hub
  - Hard to find quality character creators or community-shared companions
- **Reading level:** ~8th–9th grade. Conversational, plain English. The audience isn't here for academic prose. Tech terms are okay when they earn their place; explain inline if non-obvious (e.g. "fine-tuning — adjusting the model's behaviour for a specific style").
- **Knows already:**
  - What an AI chatbot is
  - Basic prompting (they've used ChatGPT or similar)
  - That adult-oriented AI platforms exist as a category
- **Doesn't necessarily know:**
  - Specific feature differences between competitors
  - Why model size / training data affects character quality
  - How voice cloning / TTS voice profiles work technically
  - SEO concepts (irrelevant to them — write for the reader, not for SEO)
- **What they want from the blog:**
  - Honest comparisons of platforms in the space
  - Practical "how to" guides (how to create a great companion, how to write a prompt that works, how to get more realistic images)
  - Feature deep-dives when something new lands (voice chat, phone calls)
  - News and roadmap updates without hype

## Voice

- **Tone keywords:** practical, direct, evidence-led, conversational-but-not-chatty
- **Person:** Second person ("you"), conversational
- **Sentence length:** Short to medium. Vary rhythm. Cut every word that doesn't earn its place.
- **Paragraph length:** 1–4 sentences. Single-sentence paragraphs are fine for emphasis.

## Forbidden phrases

These are AI tells. Never use them:
- "in today's fast-paced world"
- "in the digital age"
- "leverage" (use "use")
- "delve" (use "look at" or "examine")
- "navigate the complexities of"
- "unlock the power of"
- "game-changer"
- "revolutionize"
- "elevate your..."
- "comprehensive guide" (in title or intro)
- "It's important to note that"
- "When it comes to..."
- Em-dashes used as filler instead of meaningful asides
- Three-item lists where each item starts with a present participle ("Generating, Optimizing, Scaling...")

## Style examples

Always read 2–3 articles from `examples/` before drafting. Those files are the source of truth for voice. The rules above are guardrails.

## Internal linking

When `/verify-claims` finds an opportunity to link to a `brand-reference` URL, prefer descriptive anchor text that matches the target page's H1. Avoid "click here" or naked URL anchors.

## Visual generation

The `/generate-visuals` skill produces real assets (PNGs) for typed `[VISUAL:...]` placeholders in the cited draft. See `templates/visual-types.md` for the taxonomy.

- **No AI image generation (Ryan-faithful, 2026-06-25).** Real product imagery and authentic UI screenshots beat AI-generated "slop" on user experience, so we don't generate imagery. Only two automated visual types: **`screenshot`** (real Pleasur.AI UI via Playwright) and **`chart`/`table`** (matplotlib from real research data — graphs ARE fine to render). Any `type=image` placeholder is **dropped** and logged as a manual TODO; no image model is ever called (no Replicate / OpenAI / Google image API).
- **Real imagery is captured, not generated:** when an article truly needs a real photo or an adult-context image, it goes to `manual-capture.md` for the editor to produce/source from `pleasur.ai` — never an AI generator.
- **Default screenshot viewport:** 1440×900 at 2× device pixel ratio
- **Screenshot auth:** Pleasur.AI app pages require login. Run `python .claude/skills/generate-visuals/scripts/setup_auth.py` once to log in and save cookies to `.claude/skills/generate-visuals/auth/state.json` (gitignored). Future headless captures replay that session.
- **Strapi media upload:** when `STRAPI_BASE_URL` and `STRAPI_API_TOKEN` are set and `--publish` is passed, `/format-for-publish` uploads each captured image to Strapi's `/api/upload` endpoint and rewrites the article markdown to reference the hosted URLs. Without those env vars, images are copied to `content-pipeline/8-publish/{slug}/media/` for the editor to drag into Strapi manually.


## Forbidden in reader-facing copy: INTERNAL STACK (hard rule, board 2026-06-10)

NEVER name internal tools, vendors, or data sources in article prose, captions, alt text, or metadata. Cite public sources or use neutral phrasing ("current search results", "our analysis"). Banned terms include: DataForSEO, SemRush, Ahrefs, Strapi, Doppler, PostHog, OpenRouter, Firecrawl, Paperclip, TrafficStars, AgentMail, Trackdesk, Civitai, ComfyUI, Replicate, ContentShake, codex, gpt-5.5, Claude (as our tool). Ahrefs is now our SEO data source — never name it as such; reference it only when an article genuinely needs it as an external product comparison, never to describe how we got our data. Naming these leaks our stack and reads machine-generated. quality-check must FAIL any draft containing them.
