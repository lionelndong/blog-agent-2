# Brand reference: AI porn

> **Source:** Strapi inventory at `content-pipeline/brand-articles.json` (refreshed 2026-05-03, 8 published articles total). Cache fields `excerpt` and `h2s` come back empty for this Strapi schema, so scoring below is title-based; module suggestions are inferred from titles + slugs and validated against the brand-config product list. No `WebFetch` was attempted — pleasur.ai is Cloudflare-protected and would 403 anyway.

## Inventory at a glance

The Pleasur.AI blog has **8 published articles**, all in the adult-AI / uncensored-chatbot space. Of those, **5 score directly relevant** to "AI porn" (semantic neighbors: dirty, unfiltered, uncensored, adult, NSFW, no-filter). The remaining 3 are adjacent (companion-focused, broad chatbot guide, power-user roleplay).

This is a **shallow-but-on-brand corpus.** The new "AI porn" article will be one of the most direct topical pillars on the blog and should anchor cross-links across the other adult-AI pieces. There is no existing piece targeting the bare head term "AI porn" — this becomes the canonical entry point for that intent.

## Existing articles on this topic — direct matches (top 5)

- [Dirty AI in 2026: The Best Apps for Unfiltered Adult AI Chat](https://pleasur.ai/blog/dirty-ai-guide-2026) — published 2026-03-23 — covers: the closest semantic neighbor; "dirty AI" + "unfiltered adult AI chat" maps to the same intent as "AI porn"
- [AI Chatbot No Filter in 2026: The Best Unfiltered AI Apps Reviewed](https://pleasur.ai/blog/ai-chatbot-no-filter-2026) — published 2026-03-23 — covers: unfiltered chatbot rankings; the comparison rubric here is reusable
- [Best Uncensored AI Chatbot Free: No Payment Required (2026)](https://pleasur.ai/blog/best-uncensored-ai-chatbot-free) — published 2026-04-17 — covers: free-tier uncensored options; pairs naturally with a "free AI porn tools" subsection
- [CrushOn AI: Honest Review, What It Actually Does, and Whether It's Worth Your Time (2026)](https://pleasur.ai/blog/crushon-ai-review-2026) — published 2026-04-13 — covers: a direct competitor review; useful as a "platforms compared" link
- [Muah AI Review 2026: What It Does, What It Doesn't, and How It Compares](https://pleasur.ai/blog/muah-ai-review) — published 2026-04-17 — covers: another competitor review with adult-content angle

## Adjacent matches (cross-link candidates, not core)

- [Tavern AI Review 2026: The Power User's Guide to SillyTavern and Alternatives](https://pleasur.ai/blog/tavern-ai-review-2026) — link from a "power user / local model" subsection if the new piece covers DIY/self-hosted angles
- [AI Girlfriend Simulator: What It Is and Best Options in 2026](https://pleasur.ai/blog/ai-girlfriend-simulator) — link from a "companion / character" subsection
- [AI Chatbot App in 2026: Best Apps for Every Use Case](https://pleasur.ai/blog/ai-chatbot-app-guide-2026) — broader category link for the intro

## Reusable modules

Body content wasn't pulled (Strapi `excerpt` empty, no `WebFetch`), so module mining is title-inferred. The new draft should treat these as link-out targets, not paste-in sources:

- **Comparison rubric** — `dirty-ai-guide-2026` and `ai-chatbot-no-filter-2026` both rank "best apps for unfiltered chat." The new piece should NOT re-rank from scratch; instead, link out and reuse the same evaluation criteria (privacy, content limits, image gen, voice, price tier).
- **Free-tier playbook** — `best-uncensored-ai-chatbot-free` already covers "what you actually get free." Link out for the free section instead of expanding inline.
- **Competitor critiques** — `crushon-ai-review-2026` and `muah-ai-review` are detailed honest reviews. The new piece's "platforms compared" subsection should summarize in one line each and link out.
- **SillyTavern / power-user angle** — `tavern-ai-review-2026` already covers self-hosted/DIY. If the new piece touches on local models or open-source, link rather than re-explain.

## Product-led examples in our existing coverage

The brand's two live products are **AI Companion Creator** (`/create`) and **AI Image Generation** (`/generate`). Voice Replies and Phone Call are coming-soon; do not include them in the new article's product walkthroughs (per brand-config's `live`-only rule).

Inferred patterns from existing titles:
- The competitor reviews (Muah, CrushOn, Tavern) almost certainly close with a "Pleasur.AI does this better" pivot — useful framing reference, but the new piece should demonstrate the product positively rather than via direct competitor knock.
- The "best apps" listicles (`dirty-ai-guide-2026`, `ai-chatbot-no-filter-2026`, `best-uncensored-ai-chatbot-free`) place Pleasur.AI inside ranked lists. The new "AI porn" piece can do the same in any "compared platforms" subsection.
- For an "AI porn images" subsection, demonstrate `pleasur.ai/generate` — the image-gen tool is the natural product fit.
- For a "chat-based AI porn / roleplay" subsection, demonstrate `pleasur.ai/create` — the companion creator is the natural product fit.

## Internal-linking opportunities (by planned H2)

The "AI porn" article likely covers: definition, how it works (tech), how to use, comparisons, ethics/safety, free options, image vs chat vs video. Suggested links per probable section:

| Likely H2 | Link target | Why |
|---|---|---|
| "What is AI porn" / definition | `dirty-ai-guide-2026` | closest topical neighbor; supports the definitional close |
| "How AI porn works" / technology | `tavern-ai-review-2026` | covers the SillyTavern / model-driven side for power users |
| "Best AI porn apps" / comparison | `ai-chatbot-no-filter-2026` and `dirty-ai-guide-2026` | both already rank the field; link out instead of duplicating |
| "Free AI porn options" | `best-uncensored-ai-chatbot-free` | exact-match free-tier coverage |
| "Platform reviews" / specific apps | `crushon-ai-review-2026`, `muah-ai-review` | deep individual reviews to link from one-liner mentions |
| "AI porn chat / companions" | `ai-girlfriend-simulator` | character / companion adjacent intent |
| "Apps overview" / intro framing | `ai-chatbot-app-guide-2026` | broader category context |

`/verify-claims` should wire in **at minimum 4** of the above. Prioritize: dirty-ai-guide, no-filter, uncensored-free, and one competitor review.

## Voice / framing notes

Inferred from the title corpus (body not pulled):

- **"Honest" framing dominates** — three of eight titles use "Honest Review" / "What It Actually Does" / "What It Does, What It Doesn't." The new piece should match this contrarian, evidence-led register; avoid hype.
- **Year-anchored** — six of eight titles end with "(2026)" or "in 2026." Add a year tag to the new H1 for freshness signal.
- **Listicle + review duality** — the brand alternates between "best apps" roundups and individual platform reviews. The new "AI porn" piece is a head-term informational/commercial piece; lean toward roundup framing with short reviews embedded.
- **Direct vocabulary** — titles use "dirty," "unfiltered," "uncensored," "no filter," "adult" plainly. No euphemisms. Match this in the new draft.

## Failure-mode flags for the editor

- Strapi cache returned 8 articles total — small corpus. If the editor expected more, run `doppler run -- python .claude/skills/brand-reference/scripts/fetch_strapi_inventory.py --refresh` to confirm.
- `excerpt` and `h2s` fields came back empty. Module-level reuse suggestions above are title-inferred. If `/draft` needs a specific definition, walkthrough, or stat from one of the linked articles, it must be sourced from the research dossier or fetched manually by the editor — `WebFetch` will 403 on pleasur.ai.
- No `1-research/ai-porn.md` exists at write time; this dossier was scored on the keyword alone. Re-run `/brand-reference` after `/research` ships if related-term scoring would change the ranking.
