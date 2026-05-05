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

## article.json format

A payload shaped for Strapi's content-types API. Default schema assumes a typical "Article" content type with these fields:

```json
{
  "data": {
    "title": "Article Title",
    "slug": "article-slug",
    "excerpt": "First two sentences of the intro, ~160 chars max — used for previews and SEO description fallback.",
    "content": "# Article Title\n\nFull markdown body here...",
    "publishedAt": null,
    "seo": {
      "metaTitle": "Article Title (≤60 chars)",
      "metaDescription": "≤160 char description for search engines",
      "keywords": "primary keyword, related, related"
    },
    "categories": ["Category Name"],
    "tags": ["tag-one", "tag-two"]
  }
}
```

`publishedAt: null` means the article enters Strapi as a draft. Editor flips it to a published date in the admin UI when ready.

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
