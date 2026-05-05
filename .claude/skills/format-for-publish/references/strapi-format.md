# Strapi Format — Application Rules

Quick reference for the `/format-for-publish` skill. Detailed spec: `templates/strapi-format.md`.

## What gets produced

Three files under `content-pipeline/8-publish/{slug}/`:

1. **`article.md`** — clean markdown body, no front-matter, no shortcodes
2. **`article.json`** — Strapi-shaped payload ready for API publish or admin paste
3. **`README.md`** — human-readable summary: title, slug, excerpt, suggested categories/tags, character counts, what to do next

## Markdown transformation rules

Apply in this order:

1. **Strip the H1** from the body. The title goes in the JSON metadata, not in the markdown body. (Strapi typically renders the title separately; H1 in body causes a duplicate-title bug.)
2. **Convert tip / pro-tip paragraphs:**
   - `**Tip:** ...` → fenced `:::tip ... :::` block
   - `**Pro tip:** ...` → fenced `:::tip ... :::` block (collapse to same callout type)
3. **Convert note / sidenote paragraphs:**
   - `**Note:** ...` → fenced `:::note ... :::` block
   - `**Sidenote:** ...` → fenced `:::note ... :::` block
4. **Convert editor notes:**
   - `**Editor:** ...` → fenced `:::editor ... :::` block
5. **Preserve everything else as-is** — H2/H3, lists, tables, code blocks, links, image references, screenshot placeholders.

## JSON metadata extraction rules

Extracted from the cited draft:

- **`title`** — H1 of the cited draft
- **`slug`** — file slug (already known)
- **`excerpt`** — first 2 sentences of the intro, capped at 160 chars; if the second sentence pushes over the cap, take only the first
- **`content`** — full markdown body (post-transformation, without H1)
- **`seo.metaTitle`** — same as title if ≤60 chars, otherwise truncate at the last word boundary before 60
- **`seo.metaDescription`** — same as excerpt
- **`seo.keywords`** — primary keyword (from the slug) + 2–3 related keywords from the research dossier if available
- **`categories`** — derive from brand-config product affinity if obvious; otherwise `["Guides"]` as default
- **`tags`** — slugified key terms from the article (extracted from H2 headings, max 5)
- **`publishedAt`** — `null` (article enters Strapi as draft; editor publishes manually)

## Edge cases

- **Long titles** — if the article H1 is over 60 chars, the SEO meta title is truncated but the article title field stays full. Strapi's title field has no SEO length limit.
- **No tip/note callouts in source** — JSON `content` field is just clean markdown with no `:::` blocks. That's fine; not every article has callouts.
- **Existing Strapi content with same slug** — the script does NOT check Strapi for existing slugs. Editor must check before publishing to avoid duplicate-slug errors.

## What the skill does NOT do (yet)

- Push to Strapi API (deferred until Doppler creds are wired)
- Upload screenshot images to Strapi media library
- Create or link to Strapi categories/tags by ID (suggests names; editor maps to existing or creates new)
- Validate against the actual Strapi content-type schema (the JSON is a sensible default; editor adjusts for the real schema)
