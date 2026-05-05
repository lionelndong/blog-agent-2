# Handoff — internal + external link workstream

> Status snapshot for the in-flight `ai-girlfriend` article. Read this before touching the cited draft.

## What's done (Parts 1 + 4 — no conflict with the parallel agents)

These changes only touch `.claude/skills/...` and helper scripts. The cited draft was NOT modified.

- **New script:** `.claude/skills/brand-reference/scripts/fetch_strapi_inventory.py`
  Reads `STRAPI_BASE_URL` + `STRAPI_API_TOKEN` (Doppler), pages through `/api/articles?filters[publishedAt][$notNull]=true`, writes `content-pipeline/brand-articles.json` (TTL 7 days, `--refresh` to force).
  Smoke-tested: `--help` works, missing env vars emit a clear error pointing at `doppler run`.

- **Skill update:** `.claude/skills/brand-reference/SKILL.md`
  Strapi inventory is now the **first** discovery path. WebSearch + `site:` is the fallback for brands without Strapi. The "thin results" section distinguishes "no creds" / "Strapi empty" / "creds set, query failed" so future runs report the correct failure mode instead of silently falling back to a crawl that Cloudflare will block.

- **Skill update:** `.claude/skills/verify-claims/SKILL.md`
  - Defensive backstop: if `2-reference/{slug}.md` lists zero internal-linking opportunities AND `brand-articles.json` exists with `count > 0`, the skill now scores the inventory directly and weaves in 2–3 best matches anyway.
  - New hard gate at step 7: if citation density < 60%, emit a `## Editor notes / Citation gaps` block listing every unlinked factual claim by line — editor decides what to cut/accept.
  - Quality checklist updated to reflect both.

- **Script update:** `.claude/skills/quality-check/scripts/quality_check.py`
  `claim_density()` regex set widened — now catches number-as-words ("hundreds of thousands of"), comparative quantifiers ("most platforms", "almost every", "nearly all"), absolute statements ("every X is", "all X have"), year references, study/research/`according to` phrasings, superlatives ("the only", "the best"), and named competitor brands appearing without a link. Result on the existing cited draft: **51 factual claims detected (was 1)**, link coverage now reported as 3.9% (was 0.0% — both technically true; the 3.9% is the honest one).

The metrics file at `quality-checks/ai-girlfriend-metrics.md` was overwritten with the more accurate detector output. Partial score moved 52 → 53 (negligible; the link-density penalty stayed tight).

## Update — Part 2a + 2b done (no draft conflict)

**Strapi inventory fetched and brand-reference dossier regenerated.** Both files are non-draft outputs; no conflict with the parallel agents.

- `content-pipeline/brand-articles.json` — 222 published articles, 146 with AI-girlfriend topic-cluster keyword overlap. Scoped to `pleasurai/dev` Doppler config.
- `content-pipeline/2-reference/ai-girlfriend.md` — fully regenerated. The previous "no existing brand coverage found" entry is gone. The new dossier:
  - Lists 18+ direct-match articles by URL with one-line summaries
  - Maps a per-section internal-linking table to the cited draft's H2s (memory → `ai-companion-remembers`, voice → `ai-girlfriend-voice-chat`, image → `ai-girlfriend-that-sends-pictures`, create → `create-ai-girlfriend`, security → `ai-girlfriend-app-security`, etc.)
  - Flags an editorial concern: keyword cannibalization with `ai-girlfriend-guide` (and 3 other already-published articles targeting overlapping keywords). Editor needs to decide canonical pillar before publish.

**Remaining Part 2 step (Part 2c — touches the cited draft):** wire the suggested internal links into `6-drafts-cited/ai-girlfriend.md`. Aim for 4-6 anchors using descriptive text per `brand-config.md` § "Internal linking". Update the `Editor notes / Internal links` section to replace "Zero internal links added" with the actual list. **Do this AFTER the parallel agents commit.**

## What's queued (Parts 2c + 3 — must wait for parallel agents)

Both parts edit `content-pipeline/6-drafts-cited/ai-girlfriend.md`, which the image agent and the content-quality agent are also writing to. **Do not start until both have committed and stopped.**

### Part 2 — populate the inventory + add internal links

```bash
# Refresh the Strapi inventory (Doppler must inject STRAPI_BASE_URL + STRAPI_API_TOKEN)
doppler run -- python .claude/skills/brand-reference/scripts/fetch_strapi_inventory.py --refresh
```

Then re-run `/brand-reference ai-girlfriend` so `2-reference/ai-girlfriend.md` is regenerated against the actual published-article inventory (instead of the current "Status: no existing brand coverage found" output that was caused by the Cloudflare block).

Then re-run **only the internal-link portion** of `/verify-claims ai-girlfriend` — the citation work from the prior run is already in place, so the goal is: walk the draft, weave in 2–3 internal links to relevant pleasur.ai/blog articles using descriptive anchor text (per `brand-config.md` § "Internal linking"), and update the `Editor notes / Internal links` section at the bottom of the cited draft to log what was added.

If the Strapi query returns zero published articles, fall back to: link existing product/feature pages mentioned in the draft (`/generate` for image-gen, character-gallery URL if one exists). Note clearly in the Editor notes that this article is the cornerstone for the topic and should be retro-linked from siblings.

### Part 3 — external-link audit + fixes

Goal: lift external-link count from 3 → ~10 by adding citations to claims that already exist in the prose. Do not add new claims.

Targets (from the cited draft):

| Section | Claim | Citation candidate |
|---|---|---|
| Intro | "Replika and Character.AI are companions… apply heavy content moderation" | News article on Replika ERP removal (Feb 2023) |
| Intro | "ChatGPT and Claude are tools" | claude.com / chatgpt.com |
| Section 1 | "Top 10 platforms collectively pull in millions of monthly visits" | Ahrefs Site Explorer share-link or comparable public proxy |
| Section 2 | "Adults have fantasies, scenarios… don't want to share with partners, friends, or therapists" | Pew/academic survey on AI-companion usage motives |
| Section 4 (memory) | "summary memory plus selective long-term recall" | LLM long-context survey paper or vendor doc |
| Section 4 (character coherence) | "fine-tune our own models on character data" | Character.AI engineering blog or analogous |
| Section 5 (limits) | Memory decay / response repetition / privacy claims (3 claims, currently flagged for review) | Academic LLM-context-degradation paper + privacy research |
| Section 6 | "real call is bidirectional speech-to-speech with low latency" | OpenAI Realtime API or comparable tech doc |

For each: WebSearch the strongest source, swap in a markdown link with descriptive anchor text. Update `## Editor notes` to log the additions.

## Verification

After Parts 2 + 3 land, all of these should be true:

- `python .claude/skills/brand-reference/scripts/fetch_strapi_inventory.py` exits 0 and `content-pipeline/brand-articles.json` is non-empty.
- `content-pipeline/2-reference/ai-girlfriend.md` no longer says "Status: no existing brand coverage found" — it lists ≥ 2 brand articles with URLs and per-section linking suggestions (or, if Strapi is genuinely empty, it says so explicitly with that distinction).
- Internal-link count in the cited draft: `grep -oE "\[([^]]+)\]\(https?://pleasur\.ai/blog/[^)]+\)" content-pipeline/6-drafts-cited/ai-girlfriend.md | wc -l` ≥ 2 (currently 0).
- External-link count: `grep -oE "\[([^]]+)\]\(https?://(?!pleasur\.ai)[^)]+\)" content-pipeline/6-drafts-cited/ai-girlfriend.md | wc -l` ≥ 8 (currently 3).
- `python .claude/skills/quality-check/scripts/quality_check.py ai-girlfriend --path content-pipeline/6-drafts-cited/ai-girlfriend.md` reports a higher link-coverage % than 3.9%.
- `/preview ai-girlfriend` renders with the new links clickable.
