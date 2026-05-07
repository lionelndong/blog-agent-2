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

Verified end-to-end on 2026-05-07 by live POST/DELETE against production Strapi (PLEAA-457). The schema is strict — Strapi returns HTTP 400 `Invalid key <name>` for any field outside this list.

Emitted fields:

- **`title`** — H1 of the cited draft
- **`slug`** — file slug (already known)
- **`description`** — first 1–2 sentences of the intro, hard-capped at 80 chars (truncated at last word boundary, trailing punctuation stripped). Replaces the v4 `excerpt` field. **This is also the SEO meta description** (DOD#4 resolution): the frontend renders `<meta name="description">` from this field.
- **`blocks[]`** — array of components. Default is a single `shared.rich-text` block with the full markdown body in `body`. Replaces the v4 `content` string.
- **`category`** — Strapi v5 `documentId` STRING, resolved from category name via `/api/categories` and cached at module load. Replaces the v4 `categories[]` array. Omitted if no Strapi creds available so dry-runs still serialise.
- **`publishedAt`** — `null` for draft, ISO timestamp for live publish (set by `--auto-publish`).

**Forbidden / not-in-schema** (will 400 if sent):

- `author_name`, `read_time` / `readTime`, `cover_image_url` / `coverImage`, `tags` — these were on an earlier "verified" memory but live probing showed they don't exist on the Article content-type. The orchestrator-bypass at PLEAA-456 succeeded only because it stripped them too.
- `excerpt`, `content`, `categories`, `seo` — v4 legacy.

**Relations that exist but are not auto-emitted:**

- `author` — relation to Author content-type. Set manually in admin if a byline is needed.
- `cover` — media relation. Upload via `/api/upload` first, then attach the numeric media id. Out of scope for the auto-publish path; left to the editor.

SEO metadata (DOD#4, resolved 2026-05-07): the Article content-type has **no** `seo` field, `seo` component, or separate `/api/seos` collection (verified — `populate=seo`/`populate=seos`/`/api/seos` all return 400/404). `title` + `description` ARE the SEO surface. The 80-char description cap matches Google's mobile snippet ceiling.

## Edge cases

- **Long titles** — if the article H1 is over 60 chars, the SEO meta title is truncated but the article title field stays full. Strapi's title field has no SEO length limit.
- **No tip/note callouts in source** — JSON `content` field is just clean markdown with no `:::` blocks. That's fine; not every article has callouts.
- **Existing Strapi content with same slug** — the script does NOT check Strapi for existing slugs. Editor must check before publishing to avoid duplicate-slug errors.

## What the skill does NOT do (yet)

- Push to Strapi API (deferred until Doppler creds are wired)
- Upload screenshot images to Strapi media library
- Create or link to Strapi categories/tags by ID (suggests names; editor maps to existing or creates new)
- Validate against the actual Strapi content-type schema (the JSON is a sensible default; editor adjusts for the real schema)
