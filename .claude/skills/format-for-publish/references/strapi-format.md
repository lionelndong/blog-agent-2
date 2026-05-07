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

## JSON metadata extraction rules (Strapi v5 schema)

Extracted from the cited draft:

- **`title`** — H1 of the cited draft
- **`slug`** — file slug (already known)
- **`description`** — first 1–2 sentences of the intro, hard-capped at 80 chars (truncated at last word boundary, trailing punctuation stripped). Replaces the v4 `excerpt` field.
- **`blocks[]`** — array of components. Default is a single `shared.rich-text` block with the full markdown body in `body`. Replaces the v4 `content` string.
- **`category`** — Strapi v5 `documentId` STRING, resolved from category name via `/api/categories` and cached at module load. Replaces the v4 `categories[]` array. Omitted if no Strapi creds available so dry-runs still serialise.
- **`author_name`** — top-level string. Default `"Pleasur.AI Team"`.
- **`read_time`** — integer minutes (220 wpm).
- **`cover_image_url`** — top-level URL string. First absolute image in the body wins; otherwise the first uploaded local image rewritten to `<STRAPI_BASE_URL>/uploads/<file>`. Omitted if neither resolves.
- **`publishedAt`** — `null` for draft, ISO timestamp for live publish (set by `--auto-publish`).

SEO metadata (meta title / description / keywords) is **not** included on the top-level v5 payload. The article content type may expose it via a separate `/api/seos` collection or a `seo` component — confirm with CTO before wiring (PLEAA-457 DOD#4). The `description` field above is what feeds search-engine + social previews in the meantime.

## Edge cases

- **Long titles** — if the article H1 is over 60 chars, the SEO meta title is truncated but the article title field stays full. Strapi's title field has no SEO length limit.
- **No tip/note callouts in source** — JSON `content` field is just clean markdown with no `:::` blocks. That's fine; not every article has callouts.
- **Existing Strapi content with same slug** — the script does NOT check Strapi for existing slugs. Editor must check before publishing to avoid duplicate-slug errors.

## What the skill does NOT do (yet)

- Push to Strapi API (deferred until Doppler creds are wired)
- Upload screenshot images to Strapi media library
- Create or link to Strapi categories/tags by ID (suggests names; editor maps to existing or creates new)
- Validate against the actual Strapi content-type schema (the JSON is a sensible default; editor adjusts for the real schema)
