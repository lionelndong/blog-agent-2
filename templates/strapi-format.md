# Strapi Publish Format

Reference for how the `/format-for-publish` skill formats articles for Strapi. Strapi is a headless CMS — content is markdown-friendly, accessed via REST or GraphQL API, and content types are defined per project.

## Output structure

For slug `{slug}`, the skill produces:

```
content-pipeline/8-publish/{slug}/
├── article.md          # Clean markdown body (paste into Strapi rich-text field)
├── article.json        # Strapi-shaped payload (for direct API publish)
└── README.md           # Notes on what's inside, how to paste / publish
```

## article.md format

Plain markdown body of the article — no front-matter, no shortcodes. Strapi accepts this as-is in any rich-text or markdown field.

Callouts use `:::tip` / `:::note` / `:::editor` fenced syntax (works with most Strapi markdown renderers; if your Strapi project uses a custom block editor, the format-for-publish script can be re-targeted to emit Strapi Blocks JSON instead).

Example:

```markdown
# Article Title

Intro paragraph here.

:::tip
Pro tip text. Replaces WordPress's `[recommendation]` shortcode.
:::

## Section heading

Body...

:::note
Sidenote. Replaces WordPress's `[sidenote]` shortcode.
:::
```

## article.json format — Strapi v5

A payload shaped for Strapi's v5 content-types API. The v5 article schema uses a `blocks` component array, a single `category` documentId string (not an array), and a top-level `description` field (≤80 chars) instead of v4's `excerpt`/`content`/`seo`/`categories`. Verified end-to-end on 2026-05-07 by live POST/DELETE round-trip against production Strapi (PLEAA-457):

```json
{
  "data": {
    "title": "Article Title",
    "slug": "article-slug",
    "description": "≤80 char summary (truncated at word boundary).",
    "blocks": [
      { "__component": "shared.rich-text", "body": "Intro prose..." },
      { "__component": "shared.media", "file": 382 },
      { "__component": "shared.rich-text", "body": "## Section heading\n..." },
      { "__component": "shared.media", "file": 383 }
    ],
    "category": "<documentId-string>",
    "publishedAt": null
  }
}
```

PLEAA-499 follow-up (2026-05-08): image-only paragraphs in the source markdown lift out of the rich-text block and become standalone `shared.media` blocks. `file` is the numeric id returned by `/api/upload`. The frontend then renders each image as a full-width visual block instead of an `<img>` inside a `<p>`. When Strapi creds are absent (paste-mode / dry-runs), the script keeps the legacy single `shared.rich-text` block with the whole body so the editor can drag images in manually.

`publishedAt: null` means the article enters Strapi as a draft. Editor flips it to a published date in the admin UI when ready (or pass `--auto-publish` to set it to `now`).

**Why v5, not v4:** Strapi v5 is in strict mode — it returns HTTP 400 `Invalid key <name>` for any unknown key, failing the whole POST (this is what caused the silent publish failures in PLEAA-86 / 228 / 267). The skill resolves `category` by name to documentId at module load via `/api/categories` and caches it; if the env lacks `STRAPI_BASE_URL`/`STRAPI_API_TOKEN`, the field is omitted so dry-runs still serialise.

**Forbidden / not-in-schema fields** (will 400 if sent — matches the offline-smoke forbidden-key gate in `scripts/_smoke_integrations.py`): `author_name`, `read_time` / `readTime`, `cover_image_url` / `coverImage`, `tags`, `excerpt`, `content`, `seo`, `categories`. These looked plausible but are NOT on the live Article content-type. The `author` and `cover` relations exist (Author content-type + Media) but require correct id types and are usually attached in Strapi admin, not auto-emitted.

**SEO metadata path (DOD#4, resolved 2026-05-07):** the Article content-type has **no** `seo` field, no `seo` component, and no separate `/api/seos` collection — verified by probing `populate=seo`/`populate=seos`/`/api/seos` (all 400/404). `title` + `description` ARE the SEO surface; the frontend renders `<title>` from `title` and `<meta name="description">` from `description`. The 80-char description cap matches Google's mobile snippet ceiling. If a richer SEO model is ever needed, add a `seo` component to the Article content-type in Strapi admin first; do not pre-emit it.

## Adapting to your actual Strapi schema

The default JSON above is a guess based on common Strapi article setups. To map to your real schema:

1. Open Strapi admin → Content-Type Builder → your Article type
2. List the fields your schema actually has (the field names + types)
3. Tell the pipeline (or edit `format_for_strapi.py` directly) so the JSON matches

Common variations:
- **Single-type vs collection-type article:** affects the API endpoint, not the payload shape much
- **Rich text vs Blocks editor:** if you use the Blocks editor, content is JSON not markdown — the script needs a different content adapter
- **Custom components:** featured image, author relation, related-articles relation — script can fill these if you tell it the field names
- **i18n (internationalization):** if enabled, content needs `locale` field

## Direct API publishing (deferred)

The skill currently writes files only — it does NOT POST to the Strapi API. To enable direct publish:

1. Get a Strapi API token (Settings → API Tokens → Create new API Token, scope: full access or content-types)
2. Store it in Doppler under your project (e.g. `STRAPI_API_TOKEN`)
3. Add the Strapi base URL to Doppler too (e.g. `STRAPI_BASE_URL=https://your-strapi-instance.com`)
4. Launch Claude Code via `doppler run -- claude` so the env vars are injected
5. Tell the pipeline to enable direct push — `format_for_strapi.py` has a commented `publish_to_strapi()` function ready to wire up

Until then, copy `article.md` into the Strapi rich-text field manually, fill in the metadata from `README.md`, and publish from the Strapi admin UI.

## Why this approach (not direct .docx)

- **Strapi is markdown-native.** Going markdown → docx → paste into Strapi is two extra hops that lose formatting.
- **Decoupling content from publish.** The intermediate JSON gives you a portable payload — easy to inspect, easy to re-publish, easy to re-target to a different Strapi instance.
- **Easier to wire to API later.** When Doppler creds are ready, flipping on direct publish is a one-line change.
