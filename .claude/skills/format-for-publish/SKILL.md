---
name: format-for-publish
description: Convert the cited draft into a Strapi-ready package — clean markdown body + Strapi-shaped JSON payload + a README with paste/publish instructions. Pushes directly to Strapi via API when STRAPI_API_TOKEN is set. With --auto-publish (or BLOG_AGENT_AUTO_PUBLISH=1), publishes the article live (publishedAt = now) instead of as draft.
allowed-tools: Read, Write, Edit, Bash
---

# Format for Publish Skill (Strapi)

Transform the cited draft into a publish-ready package for Strapi. The skill produces three files: a clean markdown body (for pasting into Strapi rich-text fields), a Strapi-shaped JSON payload (for API publish), and a README with step-by-step publish instructions.

## Input

For slug `{slug}`:
- `content-pipeline/6-drafts-cited/{slug}.md` (the cited draft)
- `references/strapi-format.md` (application rules)
- `../../templates/strapi-format.md` (canonical Strapi reference)

## Process

1. **Read the cited draft.** Make a working copy in memory; don't edit the source.
2. **Strip the editor-notes section** if present (everything from `## Editor notes` onward). That's internal pipeline metadata, not for publishing.
3. **Extract the H1 as the title** and remove it from the body. Strapi renders the title separately; an H1 in the body causes duplicate-title bugs.
4. **Apply callout transformations** per `references/strapi-format.md`:
   - `**Tip:** ...` and `**Pro tip:** ...` → `:::tip ... :::`
   - `**Note:** ...` and `**Sidenote:** ...` → `:::note ... :::`
   - `**Editor:** ...` → `:::editor ... :::`
5. **Build the Strapi v5 JSON payload** with title, slug, description (first 1–2 sentences of intro, ≤80 chars), blocks[] (single `shared.rich-text` component holding the markdown body), category (documentId resolved via `/api/categories`), author_name, read_time, cover_image_url. SEO fields are not on the top-level v5 payload — see PLEAA-457 DOD#4.
6. **Run the formatter script:**
   ```bash
   python .claude/skills/format-for-publish/scripts/format_for_strapi.py "<slug>"
   ```
   The script writes the three files to `content-pipeline/8-publish/{slug}/`.
7. **If the user has wired up Strapi API access via Doppler** AND wants direct publish, append `--publish`:
   ```bash
   doppler run -- python .claude/skills/format-for-publish/scripts/format_for_strapi.py "<slug>" --publish
   ```
   Requires `STRAPI_BASE_URL` and `STRAPI_API_TOKEN` env vars. Article is created in Strapi as a DRAFT (publishedAt = null) — editor publishes manually after review.
8. **Tell the user** the output paths and which option (paste vs API) is active.

## Output

`content-pipeline/8-publish/{slug}/`
- `article.md` — clean markdown body (paste in Strapi rich-text field)
- `article.json` — Strapi-shaped payload
- `README.md` — paste-or-publish instructions with title, slug, excerpt, SEO fields, suggested categories/tags

## Quality checklist

- [ ] H1 stripped from body (title lives in JSON only)
- [ ] No `**Tip:**` / `**Note:**` / `**Editor:**` markdown prefixes remaining in body — all converted to `:::` callouts
- [ ] Editor-notes section excluded from output (it's pipeline metadata, not content)
- [ ] `description` is real prose from the intro, not the title or first heading
- [ ] `description` ≤ 80 chars (Strapi v5 cap)
- [ ] `blocks[0].__component == "shared.rich-text"` and `blocks[0].body` non-empty
- [ ] No legacy v4 fields (`excerpt`, `content`, `seo`, `categories[]`) in payload
- [ ] `category` (when set) is a documentId STRING, not an array
- [ ] Slug matches the input slug exactly
- [ ] `publishedAt: null` for draft mode; ISO timestamp only when `--auto-publish` is set

## Customizing for your Strapi schema

The default JSON shape assumes a typical "Article" content type with: `title`, `slug`, `excerpt`, `content`, `seo` (component), `categories` (relation), `tags` (relation), `publishedAt`. If your Strapi has different field names or component shapes:

1. Open `format_for_strapi.py`
2. Edit the `build_payload()` function — adjust field names, nest components per your schema
3. The transformation logic (callouts, excerpt extraction) works regardless of payload shape

## When direct API publish fails

Common causes:
- **401 Unauthorized:** API token missing or wrong scope. Check Strapi admin → Settings → API Tokens; needs at least "Authenticated" or "Full access" for content creation
- **400 Bad Request:** Payload doesn't match your Strapi schema. Check `article.json` against your real content type — likely a missing required field or extra unknown field
- **404 Not Found:** `STRAPI_BASE_URL` is wrong or the endpoint isn't `/api/articles` (e.g., your content type is named differently — check Settings → API Tokens → endpoint list)

When `--publish` fails the script keeps the local files so you can paste manually.

## Auto-publish vs draft modes

The skill supports two publish modes:

**Draft mode** (default; what `--publish` does without `--auto-publish`):
- `publishedAt: null` in the payload
- Article enters Strapi as a draft
- Editor reviews in admin, hand-edits, captures any remaining screenshot placeholders into media library, then clicks Publish
- The human checkpoint is where the last 20% of quality lives

**Auto-publish mode** (`--auto-publish` flag, or `BLOG_AGENT_AUTO_PUBLISH=1` env var):
- `publishedAt` set to the current ISO timestamp in the payload
- Article goes live on Strapi immediately
- Required for `/auto-blog-loop` autonomous mode (no human in the loop, by design)
- Compensating control: a quality precondition gate (see "Quality precondition" below) refuses to publish if the upstream `/quality-check` verdict is FAIL — belt-and-suspenders even if the orchestrator is misconfigured

Pick auto-publish for the cron-driven `/auto-blog-loop` path. Pick draft mode for one-off manual runs where an editor is going to review.

## Quality precondition (auto-publish only)

Before issuing the Strapi POST when `--auto-publish` is set, the script re-reads `content-pipeline/quality-checks/{slug}.md` and parses the verdict line. If the verdict is FAIL OR if the file is missing, the script refuses to publish, exits non-zero, and prints the reason. The orchestrator will then quarantine the slug. This is a safety net — `/blog-pipeline` should never call `/format-for-publish --auto-publish` on a FAIL'd article, but the precondition makes a misconfigured orchestrator harmless.
