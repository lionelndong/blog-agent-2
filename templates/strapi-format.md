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

A payload shaped for Strapi's v5 content-types API. The v5 article schema uses a `blocks` component array, a single `category` documentId string (not an array), and a top-level `description` field (≤80 chars) instead of v4's `excerpt`/`content`/`seo`/`categories`:

```json
{
  "data": {
    "title": "Article Title",
    "slug": "article-slug",
    "description": "≤80 char summary (truncated at word boundary).",
    "blocks": [
      {
        "__component": "shared.rich-text",
        "body": "Full markdown body here..."
      }
    ],
    "category": "<documentId-string>",
    "author_name": "Pleasur.AI Team",
    "read_time": 9,
    "cover_image_url": "https://.../uploads/cover.jpg",
    "publishedAt": null
  }
}
```

`publishedAt: null` means the article enters Strapi as a draft. Editor flips it to a published date in the admin UI when ready (or pass `--auto-publish` to set it to `now`).

**Why v5, not v4:** Strapi 5 rejects v4-shaped payloads silently (PLEAA-457). The skill resolves `category` by name to documentId at module load via `/api/categories` and caches it; if the env lacks `STRAPI_BASE_URL`/`STRAPI_API_TOKEN`, the field is omitted so dry-runs still serialise. `cover_image_url` is set to the first uploaded image's URL when present, otherwise omitted.

**SEO metadata path:** v5 does not include `seo.metaTitle` / `seo.metaDescription` / `seo.keywords` inline. Confirm with CTO whether to wire a `seo` component or `/api/seos` relation before adding (PLEAA-457 DOD#4). The `description` field above is the social/search preview source meanwhile.

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
