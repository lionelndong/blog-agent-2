# Money clusters — config (EDITABLE; a living list, never a ceiling)

> The blog strategy is organized into **money clusters** — business-value PARENT topics, each tied to a live Pleasur.AI product/feature. **This file is THE control surface.** Adding a cluster = adding one row here; no code change. The `cluster-planner` skill reads this file, organizes the keyword queue into these clusters, AND **proposes new cluster candidates** whenever research surfaces a high-business-value topic, or a live product, that no cluster covers yet — so the blog **expands as the company expands** and never stays stuck on a fixed list.

## How to add / split / merge a cluster (do this whenever a product ships or a new demand area emerges)
1. Add (or edit) a row in **Active clusters**: a short `id`, a human `name`, the `parent_topic` (the head term — let keyword research confirm the exact highest-volume phrasing), the `product` it showcases, and a few `seeds` for keyword research.
2. Re-run the keyword research pipeline. `cluster-planner` populates the cluster (keystone + supporting ring) on the next run.
3. That's it — the config is the only thing you touch. To retire a cluster, set `status: archived` (don't delete; keeps history).

## Active clusters (seed set — expand freely)
| id | name | parent_topic | product/feature | seeds | status |
|----|------|--------------|-----------------|-------|--------|
| companions | AI Companions | ai girlfriend | AI Companion Creator | ai girlfriend, ai boyfriend, ai companion, virtual girlfriend | active |
| image-gen | NSFW AI Image Generation | ai porn generator | AI Image Generation | nsfw ai image generator, ai porn generator, ai art generator nsfw | active |
| chat-roleplay | Adult Chat, Sexting & Roleplay | nsfw ai chat | Companion chat / sexting | nsfw ai chat, ai sexting, ai roleplay, dirty talk ai | active |
| voice-calls | AI Voice & Calls | ai girlfriend voice | Voice Replies, Phone Call | ai girlfriend voice, call an ai, ai voice chat | active |
| tools-compare | Tools & Comparisons | best ai girlfriend app | (cross-product; buyer-intent) | best ai girlfriend app, ai girlfriend alternatives, [X] vs [Y] | active |

## Planned clusters (add the parent_topic + seeds + flip to active when the product ships)
| id | name | product/feature | status |
|----|------|-----------------|--------|
| interactive | Interactive / Real-time Companion | planned interactive features (live interaction, etc.) | planned |

> When a planned product ships: fill in `parent_topic` + `seeds`, set `status: active`, re-run the pipeline. `cluster-planner` will ALSO auto-flag any planned/uncovered product it detects from the live product set, so you get a reminder even if this file lags.

## Rules (the strategy this config serves — see `STRATEGY.md`)
- **Each cluster maps to a real product/feature** (product-led; business value ≥ 2). A topic area with no product fit is not a money cluster — don't add it here.
- **Authors are NOT owned per cluster.** The author is chosen by the article's *content type* (`examples/authors.md`); a cluster spans types → spans authors.
- **Build winnable members first** (winnability vs our *live* DR — `cache/brand-dr.json`); expand a cluster's ambition (higher-KD members, bigger sub-topics) as DR grows.
- **Each cluster = a keystone** (the parent_topic article) **+ a supporting ring** (sub-topics / long-tail / intent variants), internally linked, with link-juice flowing to the keystone and the money/product page.
