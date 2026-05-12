# Pending GitHub Actions workflows

This directory holds Actions workflow YAML that's blocked from a normal PAT push
because the PAT used by the CI bridge lacks the `workflow` GitHub scope. A
human (or a PAT with `workflow` scope) must move each file from
`.github/workflows-pending/` to `.github/workflows/` and push.

## `sync-publish-approvals.yml` (PLEAA-581 Layer 2)

Required for the Strapi publish gate. On push to `main` it scans
`content-pipeline/8-publish/*/manifest.json` and upserts one row per slug into
the Supabase `blog_publish_approvals` table via PostgREST. The edge function
`sync-blog-posts` (in `lionelndong/pleasurai`) refuses any Strapi
`entry.publish` webhook whose slug has no registry row.

### Repo secrets it needs

| Secret | Where to find it |
|---|---|
| `SUPABASE_URL` | Supabase project settings → API → URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase project settings → API → service_role key (NOT anon) |

Add both at GitHub → repo settings → Secrets and variables → Actions → New
repository secret before moving the workflow into place. Without them the
workflow fails on first run with `ERROR: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set`.

### Move it into place

```bash
git mv .github/workflows-pending/sync-publish-approvals.yml .github/workflows/sync-publish-approvals.yml
git commit -m "PLEAA-581 Layer 2: activate sync-publish-approvals workflow"
git push
```
