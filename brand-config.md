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
    - Chat in unrestricted, judgment-free conversations including roleplay and adult themes
    - Save chat history and resume conversations across sessions

- **AI Image Generation** — Generate adult-oriented images on demand. Style presets, character consistency, prompt-driven creation.
  - URL: https://pleasur.ai/generate
  - Status: **live**
  - Use cases:
    - Generate images of your created companion in different scenes
    - Explore styles (realistic, anime, art) without prompt-engineering expertise
    - Create images on demand inside an existing chat thread (in-conversation image gen)

### Coming this week (treat as `coming-soon`)

> Both features below live INSIDE the existing chat experience — they are not standalone products and do not have their own URLs. Reference them as in-chat capabilities of the AI Companion Creator, not as separate tools. Articles must not link out to a dedicated `/voice` or `/call` page (none exists).

- **Voice Replies (in-chat)** — Inside any chat with a companion, the user taps a speaker icon on a character's message and the character "speaks" the message aloud in their assigned voice. It's a per-message playback action, not a separate mode. The conversation stays in the same chat thread; voice is one tap on top of text.
  - URL: in-chat feature — no dedicated page; lives inside `https://pleasur.ai/create`
  - Status: **coming-soon** (this week)
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
  - Status: **coming-soon** (this week)
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

- **Image gen provider:** Replicate (NEVER direct OpenAI / Google API — always proxied through Replicate)
- **Image gen auth env var:** `REPLICATE_API_TOKEN` (load via Doppler — same pattern as `OPENROUTER_API_KEY_BLOG_AGENT`)
- **Default model:** `openai/gpt-image-2`
- **Backup model:** `google/nano-banana` — used automatically on error / rate-limit / safety refusal, or explicitly via `model=nano-banana` in the placeholder
- **Adult-content rule:** any `[VISUAL:type=image;safety=adult;...]` placeholder is routed to `manual-capture.md` for the editor to produce via `pleasur.ai/generate`. Replicate's GPT Image 2 and Nano Banana refuse adult prompts and may flag the API account — never call them with adult content.
- **Default image style suffix** (appended to SFW prompts unless overridden): "photorealistic, soft natural lighting, no people"
- **Default screenshot viewport:** 1440×900 at 2× device pixel ratio
- **Screenshot auth:** Pleasur.AI app pages require login. Run `python .claude/skills/generate-visuals/scripts/setup_auth.py` once to log in and save cookies to `.claude/skills/generate-visuals/auth/state.json` (gitignored). Future headless captures replay that session.
- **Strapi media upload:** when `STRAPI_BASE_URL` and `STRAPI_API_TOKEN` are set and `--publish` is passed, `/format-for-publish` uploads each captured image to Strapi's `/api/upload` endpoint and rewrites the article markdown to reference the hosted URLs. Without those env vars, images are copied to `content-pipeline/8-publish/{slug}/media/` for the editor to drag into Strapi manually.
