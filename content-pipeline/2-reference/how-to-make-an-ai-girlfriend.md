# Brand reference: how to make an ai girlfriend

> Source: Strapi inventory (`content-pipeline/brand-articles.json`, refreshed 2026-05-15, **13 published articles**). Excerpts and H2s are empty in the cache, so ranking is title-overlap + topical adjacency + local research dossiers for sibling slugs. No web crawl attempted — pleasur.ai is Cloudflare-protected and `WebFetch` returns 403.

## Existing articles on this topic

The keyword is the head term for the "make / build / create" arc on AI girlfriends. Pleasur.AI has shipped one body-specific deep-dive and three siblings that brush against creation. Ranked by topical adjacency:

- [Build a Girlfriend Body](https://pleasur.ai/blog/build-a-girlfriend-body) — *(planned sibling, body-customization deep-dive — see `content-pipeline/2-reference/build-a-girlfriend-body.md`)* — covers: appearance/body sliders and presets inside the Companion Creator. The "appearance" H2 of the new article should be a 2–3 sentence summary that links here for the full walkthrough.
- [The AI Girlfriend Experience: 90 Seconds to Week Three](https://pleasur.ai/blog/ai-girlfriend-experience) — published 2026-05-08 — covers: the lived journey of a created companion from first message to week three, including the predictable "phrases that break the illusion." Natural follow-on read for the "what to expect after you make her" section.
- [AI Girlfriend Simulator: What It Is and Best Options in 2026](https://pleasur.ai/blog/ai-girlfriend-simulator) — published 2026-04-17 — covers: the simulator/builder category framing and best options. Closest category anchor when defining what "making" an AI girlfriend actually is.
- [Yandere AI Girlfriend Simulator](https://pleasur.ai/blog/yandere-ai-girlfriend-simulator) — published 2026-05-07 — covers: a specific personality archetype you can build. Useful as the example archetype for the personality H2.
- [Best Character AI Alternative for You in 2026 (By Use Case)](https://pleasur.ai/blog/character-ai-alternative) — published 2026-05-08 — covers: where to make a companion when Character.AI's filters block you. Natural link target for the "which app should I use" question.
- [Tavern AI Review 2026](https://pleasur.ai/blog/tavern-ai-review-2026) — published 2026-05-08 — covers: the power-user / open-source path to making a character. Link target for the "DIY / advanced" sidebar.

## Reusable modules

The cache stores titles + dates only — no body. Don't WebFetch (Cloudflare). Treat siblings as link targets, not source material. New definitions, stats, and walkthroughs come from `content-pipeline/1-research/how-to-make-an-ai-girlfriend.md`, not from these articles.

### From [Build a Girlfriend Body](https://pleasur.ai/blog/build-a-girlfriend-body)
- Body / appearance step: summarize in 2–3 sentences, link out. Don't re-walk the sliders — that's this sibling's job.

### From [The AI Girlfriend Experience](https://pleasur.ai/blog/ai-girlfriend-experience)
- "Six phrases that break the illusion" (week-three callout). Reference one-liner + link, so the maker knows what to design around.
- Replika 2023 shutdown beat — frame it as why your companion's portability and unrestricted personality matter from the build step on.

### From [AI Girlfriend Simulator](https://pleasur.ai/blog/ai-girlfriend-simulator)
- The "you build her, you don't pick her" framing. Reuse the phrasing in the intro to keep voice consistent.

### From [Yandere AI Girlfriend Simulator](https://pleasur.ai/blog/yandere-ai-girlfriend-simulator)
- The archetype-as-example pattern: pick one personality (yandere, tsundere, dom, soft girlfriend-next-door) and walk it end-to-end. Mirror that pattern in the personality H2.

## Product-led examples in our existing coverage

The **AI Companion Creator** (https://pleasur.ai/create — `live`) is the one-stop product for this entire keyword. Every sibling listed above already anchors to it. The new article should make the Creator the spine of the walkthrough — every "step" is a step inside `pleasur.ai/create`.

- **AI Companion Creator** — flagship; demonstrate the appearance → personality → backstory → voice flow.
- **AI Image Generation** (https://pleasur.ai/generate — `live`) — the natural follow-up once a companion exists: generate scenes of her. Mention in the "what to do once she's made" section.
- **Voice Replies (in-chat)** — `coming-soon`. Tease as the speaker icon next to a reply. Do NOT link to a `/voice` page.
- **Phone Call (in-chat)** — `coming-soon`. Tease as the Call button on the character profile. Do NOT link to a `/call` page.

## Internal-linking opportunities (by planned section)

- **Intro / "what 'making' actually means"** → [AI Girlfriend Simulator](https://pleasur.ai/blog/ai-girlfriend-simulator) — set the category frame.
- **Step: pick an app** → [Best Character AI Alternative](https://pleasur.ai/blog/character-ai-alternative) — for readers arriving from filter-frustration.
- **Step: design appearance / body** → [Build a Girlfriend Body](https://pleasur.ai/blog/build-a-girlfriend-body) — the dedicated deep-dive; product-mention the **AI Companion Creator**.
- **Step: pick personality / archetype** → [Yandere AI Girlfriend Simulator](https://pleasur.ai/blog/yandere-ai-girlfriend-simulator) — archetype example.
- **Step: advanced / DIY** → [Tavern AI Review 2026](https://pleasur.ai/blog/tavern-ai-review-2026) — power-user sidebar.
- **What happens after you make her** → [The AI Girlfriend Experience](https://pleasur.ai/blog/ai-girlfriend-experience) — the week-three reality check; product-mention **AI Image Generation** for in-chat scene gen and tease in-chat **Voice Replies** / **Phone Call**.

## Voice / framing notes

- Pleasur.AI frames creation as a flow you control: design from scratch or remix a community character — never "pick from a fixed roster." Match that.
- This is a how-to walkthrough, not a review. Don't append a year tag to the title.
- Treat appearance, personality, voice, and scenario as one bundle — the flagship product packages them. Don't split body and personality into separate articles' worth of detail; link to the body sibling for that depth.
- This article is the head of the "make/build/create" cluster. Plan retro-links from `build-a-girlfriend-body`, `ai-girlfriend-simulator`, and `ai-girlfriend-experience` into it once it ships.
