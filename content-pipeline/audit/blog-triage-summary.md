# Blog triage — Pleasur.AI

Inventory: **8 published articles**
Cache snapshot: `content-pipeline/brand-articles.json`
Ahrefs signals dumped to: `scripts/_ahrefs_signals.json`

## Headline finding

**Of 222 published articles, only 8 (3.6%) have any Ahrefs-detected organic signal** (5 ranking + 3 with a single referring domain each, all UR=0).
The other 214 articles are functionally invisible to organic search per Ahrefs. The user's '~90% slop' estimate matches reality.

## Verdict counts

| Verdict | Count | % | Action |
|---|---|---|---|
| **KEEP** | 8 | 100% | leave as-is; these earn rankings/backlinks |
| **CONSOLIDATE** | 0 | 0% | dupe of a stronger sibling — delete + 301 to the canonical |
| **REVIEW** | 0 | 0% | duplicate clusters where nothing ranks — editor picks canonical or deletes whole topic |
| **DELETE** | 0 | 0% | solo article, zero rankings, zero backlinks — slop |

## Caveats — read before approving any batch

1. **Ahrefs only sees organic-search signal.** Direct, social, email, and referral traffic are invisible here. If you have Pleasur.AI internal analytics (Plausible, GA4, etc.), cross-reference the `DELETE` list against your own pageview data before pulling the trigger.
2. **Articles published in the last ~30 days may not be crawled by Ahrefs yet.** A new article that's about to rank but hasn't been picked up will look like 'slop' here. Filter the CSV by `publishedAt` and skip recent posts in your first delete batch.
3. **Internal-link equity isn't measured.** `pages-by-backlinks` shows external referring domains only. An article with zero external backlinks but 20 internal links pointing at it is still load-bearing for site architecture. Run a crawl (Screaming Frog or similar) before deletion to surface internal-link counts per slug.
4. **CONSOLIDATE redirect targets need semantic verification.** The script picks the highest-value cluster member as the canonical, but that's a structural pick, not a semantic one. Example from this run: `ai-rp-chat-guide-2026` (roleplay) consolidates into `dirty-ai-guide-2026` (adult chat) because they cluster on title overlap — but a roleplay-seeking visitor landing on a 'dirty AI' page is a bad UX. Skim each CONSOLIDATE row and either accept the suggested target or retarget to a more semantically appropriate slug.
5. **Deletion is permanent in Strapi unless you have soft-delete enabled.** Confirm your Strapi instance supports soft-delete OR back up the article bodies (export to JSON) before deleting.
6. **301 redirects must be live BEFORE delete.** Strapi articles are served by your frontend (Next.js?) routing. Deleting an article without a redirect = 404 = lost equity. Configure all redirects in your `next.config.js` / Vercel config first, deploy, verify a few with curl, then run the deletes.

## Why the script flagged false-positive clusters in REVIEW

The clustering uses Jaccard similarity on title tokens (after stopword removal). Two known weaknesses:
- **Greedy single-link**: an article joins a cluster if ANY existing member shares ≥50% tokens. Chains can form (A↔B↔C) where A and C are unrelated.
- **Title-only**: I don't have article body content yet (Strapi `populate=*` didn't return content fields in the inventory pull — that's fixable in `fetch_strapi_inventory.py` if needed).

Treat clusters of size ≥5 with skepticism — they may need to be split into sub-clusters by topic. Smaller clusters (size 2-3) are usually right.

## Top duplicate clusters (the slop you specifically called out)

## Suggested batches for approval

Don't approve all at once. Recommend three batches, smallest blast radius first:

### Batch A — `DELETE` solo orphans (lowest risk)
- 0 articles
- Solo articles, zero ranking, zero external referring domains, no duplicate cluster
- These are pure slop with no equity. Delete cleanly (no redirect needed unless internal links point at them).
- **Recommended: review the CSV `DELETE` rows, then approve in batches of ~25 at a time.**

### Batch B — `CONSOLIDATE` losers in clusters with a winner
- 0 articles
- Duplicate of a stronger sibling. Each gets a 301 redirect to its `redirect_target_slug` before deletion.
- Setting up redirects is the load-bearing step. If your stack uses Next.js redirects in `next.config.js` or a Strapi `redirects` collection, batch-write them first, deploy, verify, then delete.

### Batch C — `REVIEW` orphan-cluster duplicates
- 0 articles
- Duplicate clusters where NO member ranks. Pick a canonical by reading the bodies (script doesn't have access to Strapi content yet); 301 the others to it.
- Could also choose to delete the entire cluster if the topic isn't a brand priority.

## Files generated

- `content-pipeline/audit/blog-triage.csv` — full per-article verdict table
- `content-pipeline/audit/clusters.json` — machine-readable cluster groupings
- `content-pipeline/audit/blog-triage-summary.md` — this file

## Next step

Open `blog-triage.csv` and skim the `DELETE` and `CONSOLIDATE` rows. Tell me which batch (A / B / C) to start with and how many at a time. **No deletions hit Strapi until you confirm.**
