---
name: brand-reference
description: Surface the live Pleasur.AI product FEATURES + use-cases relevant to this topic (what the article can actually demonstrate), re-verified against the live site for freshness — plus any existing on-topic articles, used only for internal linking. Product-led: the unique value is showing our features in action, not citing old blog posts.
allowed-tools: Read, Write, Bash, WebFetch, WebSearch
---

# Brand Reference Skill

Pleasur.AI content is **product-led** (Ryan Law's principle: the unique thing AI can pull from
our coverage is *the use-cases of our own tools* — not generic prose). So the primary job of this
step is **not** to dig up old blog posts. It is to surface **which of our current features this
article can demonstrate, and how**. Existing articles are secondary — used only for internal links.

Produce two things, in this order of importance:

1. **Features to showcase** (primary) — the live Pleasur.AI features relevant to this topic, the
   concrete use-cases that fit, and how to demonstrate them in the article.
2. **Internal links** (secondary) — existing on-topic articles to link to (avoid repetition, pass
   link equity). The blog is young; expect few or none, and that's fine.

## Input

- `brand-config.md` → the **Products / Features** section (the maintained feature list).
- `content-pipeline/1-research/{slug}.md` → the topic angle + related terms.
- `content-pipeline/brand-articles.json` → Strapi inventory cache (for internal links only).

## 1. Features to showcase (PRIMARY)

Read the **Products / Features** section of `brand-config.md` — the master feature list (AI
Companion Creator, AI Image Generation, Voice Replies, Phone Call, …), each with a `status`
(`live`/`coming-soon`/`roadmap`), use-cases, and "how to mention" notes.

- **Freshness check — we ship features weekly, so this list goes stale fast.** For every feature
  you plan to reference, RE-VERIFY its status against the live site THIS run (`pleasur.ai/pricing`
  for billable features; the product pages for capabilities) — exactly as brand-config's
  pricing/feature drift rule requires. If the live site differs from brand-config, **trust the
  live site**, use it, and flag the drift so brand-config gets refreshed. NEVER reference a
  `coming-soon`/`roadmap` feature as a live walkthrough (e.g. AI Video is roadmap — never claim it).
- Pick the **1–3 features most relevant to demonstrate** on this topic. For each capture: what it
  does, the specific use-case that fits THIS article, and **how to show it** (follow the feature's
  "how to mention" notes — e.g. Voice Replies = "tap the speaker icon on a reply", not "open Voice
  Chat"; Phone Call = "tap Call on the character's profile", launched from inside a chat).
- This is the payload the outline + product-mentions + draft stages build on. If the topic genuinely
  has no product fit, say so plainly — don't force a feature in.

## 2. Internal links (SECONDARY)

Existing Pleasur.AI articles on the topic — ONLY for internal linking + avoiding repetition.

- Strapi inventory first: `doppler run -- python .claude/skills/brand-reference/scripts/fetch_strapi_inventory.py`
  (add `--query "<keyword>,<related-1>,<related-2>"` once the corpus is large). Read
  `content-pipeline/brand-articles.json`; score by title/H2 overlap with the keyword + related terms;
  take the top 3–5.
- pleasur.ai is Cloudflare-protected (403s `WebFetch`/`site:` search), so the Strapi API is the
  path. Only fall back to `WebSearch` when Strapi returns zero AND the script exited 0. If Strapi
  creds are missing (script errors with `STRAPI_BASE_URL…`), **STOP** and tell the user to wrap the
  command in `doppler run --` — do not silently web-crawl (it 403s anyway).
- No existing articles yet → say so. This becomes a foundational piece; plan retro-links once
  sibling articles ship.

## Output

`content-pipeline/2-reference/{slug}.md`:

```
# Brand reference: {keyword}

## Features to showcase (primary)
### <Feature name>  (status: live — re-verified <date>)
- What it is: ...
- Use-case for THIS article: ...
- How to demonstrate: ...  (per brand-config "how to mention")

## Internal links (secondary)
- [Existing article title](URL) — link from the planned section on "..."
  (or: "No existing on-topic articles yet — foundational piece; retro-link later.")

## Voice / framing notes
- How we talk about this topic / these features: ...
```

300–600 words. The `outline`, `product-mentions`, and `draft` skills all read this.

## Quality checklist

- [ ] ≥ 1 **live** feature selected to showcase, with a concrete use-case + how-to-demonstrate
- [ ] Every referenced feature's status **re-verified against the live site this run** (no stale
      `coming-soon`/`roadmap` claims; AI Video never claimed as live)
- [ ] Internal links are real existing articles (or "none yet" stated explicitly)
- [ ] If the topic has no genuine product fit, that's stated — not forced

> Keeping the feature list current is brand-config's job (the `## Products / Features` block).
> If you notice it drifting from the live site repeatedly, raise a task to refresh it on a weekly
> cadence — features ship faster than the list is edited.
