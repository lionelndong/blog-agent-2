---
name: linkbuild-competitor-mining
description: Off-page playbook (Lesson 9, link building). Mines our competitors' backlink profiles via Ahrefs to produce a VETTED link-prospect list — their "superfans" (sites linking to several of a competitor's best-by-links pages), their "power-linkers" (sites linking to multiple competitors but NOT to us), and their fresh new links — filtered for relevance and de-duped against sites that already link to us. The Link Intersect method, encoded. Output is a prospect queue for /outreach; it does NOT send anything.
allowed-tools: Read, Write, Edit, Bash, mcp__ahrefs__*
---

# Link-Build Competitor Mining — the Link Intersect playbook

> **This is a PLAYBOOK the off-page sub-agent runs, not a live pipeline step.** It only runs once the off-page phase is open (blogs proven + traffic rising — `STRATEGY.md` "Off-page (later)" + the off-page sub-agent charter `examples/off-page-subagent-AGENTS.md`). Its single deliverable is a **vetted prospect list**; the actual reaching-out happens in `/outreach`. Nothing here contacts anyone.

The fastest links to win are the ones our competitors already earned: someone who linked to a rival's "best AI girlfriend apps" roundup is, by construction, a person who links to pages like ours. **Don't guess who might link — replicate the links competitors already have** (`STRATEGY.md` Lesson 9: "replicate competitor links"). This skill turns a few competitor domains into a ranked, trash-filtered, not-already-linking-to-us prospect queue.

> **Data layer: Ahrefs MCP** (`mcp__ahrefs__*`). Read [`../research/references/ahrefs-mcp-cheatsheet.md`](../research/references/ahrefs-mcp-cheatsheet.md) first — params are comma-separated **strings** not JSON arrays, `select` + `country`/`mode` are required on most endpoints, and for any tool you haven't used this run call `doc {tool:"..."}` to get its exact schema. **Never invent tool names.** Ahrefs is the sole backlink source; if it's down, HALT and surface it (same outage policy as the keyword pipeline) — do not fall back to a non-Ahrefs source or guessed links.

## Input

`/linkbuild-competitor-mining` (no args), optionally `--cluster <id>` to bias relevance scoring toward one money cluster.

Reads:
- `brand-config.md` — our domain, audience, products, and the named competitor set (the same competitors `content-gap-analysis` auto-discovers; reuse `content-pipeline/0-keywords/cache/competitors.json` if present).
- `content-pipeline/0-keywords/clusters.md` — the money clusters, so a prospect's topical relevance can be judged against what we actually publish.
- `content-pipeline/0-keywords/cache/brand-dr.json` — our live DR (for the "displaceable / worth-it" read; never hardcode a DR).
- `content-pipeline/off-page/our-backlinks.csv` if it exists — the domains that **already** link to us (so we can subtract them). If absent, fetch our own profile fresh in step 1.

## The three prospect types (what we mine)

1. **Superfans** — sites that link to **multiple** of a SINGLE competitor's best-by-links pages. A site that linked to three of a rival's pages clearly rates that rival's content; it is the warmest possible prospect for ours.
2. **Power-linkers** — sites that link to **several different competitors** but **not to us** (the classic "link intersect": linkers common to ≥ 2 rivals, minus our own linkers). These are the niche's link hubs — resource pages, roundup authors, bloggers who cover the category.
3. **Fresh links** — a competitor's **newest** backlinks (last 30–90 days). Recency means the linking page is live, maintained, and its author is currently active on the topic — a far higher hit-rate than a link earned five years ago.

## Process

1. **Resolve our own backlink footprint first.** If `our-backlinks.csv` is stale (> 30 days) or missing, pull our referring domains via `site-explorer-referring-domains` (`target:"pleasur.ai", mode:"domain", select:"domain,domain_rating,links_to_target,first_seen"`). Persist the domain set — this is the **suppression list** every prospect is checked against. **A prospect that already links to us is not a prospect.**

2. **Lock the competitor set.** Take competitors from `brand-config.md` / `cache/competitors.json`. Cap at the top 4–6 most topically-relevant rivals (more competitors = more intersect noise, not more signal). Record each rival's domain + DR.

3. **Find each competitor's best-by-links pages.** For every rival, `site-explorer-best-by-external-links` (or `site-explorer-top-pages` sorted by referring domains; `select:"url,referring_domains,traffic"`, `mode:"domain"`, tight `limit` ~25). These are the rival's **linkable assets** — the pages that actually attract links (usually data studies, original research, free tools, definitive roundups). The links pointing AT these pages are the target pool.

4. **Mine SUPERFANS (per competitor).** For each rival's top best-by-links pages, pull the referring domains of those *pages* (`site-explorer-referring-domains`, `mode:"exact"`/`"prefix"` on the page URL). A domain that appears across **≥ 2** of one rival's best pages → tag `prospect_type=superfan`, record which competitor + how many of its pages they link.

5. **Mine POWER-LINKERS (link intersect across competitors).** Union the referring-domain sets from step 4 (or, if the MCP exposes it, use the dedicated `link-intersect`-style endpoint — check `doc` for the current tool name). Keep domains that link to **≥ 2 different competitors**. Tag `prospect_type=power_linker`, record the count of distinct competitors linked.

6. **Mine FRESH LINKS (per competitor).** For each rival, `site-explorer-all-backlinks` filtered to new links (`history:"new"` or the `first_seen` window the cheatsheet documents; `select:"url_from,domain_rating,first_seen,anchor,link_type"`, last 30–90 days). Keep the referring domains; tag `prospect_type=fresh_link`, record `first_seen` + the anchor (the anchor hints at what excuse will land in `/outreach`).

7. **Merge + de-dupe to one row per domain.** A domain can qualify under several types — keep the union of its tags and the strongest signals (e.g. superfan-of-2 + power-linker-of-3). One prospect = one row.

8. **VET — filter the trash, keep the relevant (the part that makes this list usable).** For every candidate domain compute:
   - `already_links_to_us` (from step 1) → **drop immediately if true** (the #1 filter — we're replicating links we DON'T have).
   - `relevance` (0–10): topical fit to our clusters/audience — does this site cover dating/relationships/AI/adult-tech/companionship, or anything our reader would plausibly visit? Score from the domain + the linking page's topic. **Relevance beats DR** — a relevant DR-30 niche blog is a better prospect than an irrelevant DR-80 general-news site. (Lesson 9: don't chase high-DR-only.)
   - `link_type` sanity — drop obvious junk: link farms, scraper/auto-generated directories, expired/parked domains, PBN footprints, adult-spam aggregators, comment-spam hosts, sites with no real editorial contact. (`site-explorer-referring-domains` DR + the page's outbound-link density are the tells.)
   - `dr` (Ahrefs Domain Rating of the prospect) — recorded for prioritization, **not** as a gate. (We want links from real, relevant sites at any DR; DR only breaks ties.)
   - `reachability` — is there a plausible human + contact path (a named author, an editor, a working contact/about page)? A page with no human behind it can't be outreached. Flag `no_contact` candidates as low-priority (they may still earn an unsolicited link once our linkable asset exists, but they're not an outreach target).
   - **Suppress affiliate-program domains** that the Head of Affiliates ("Alex") already owns or is actively working — the affiliate channel is coordinated there, NOT cold-outreached here (charter §"Coordination with Alex"). Cross-check `content-pipeline/off-page/affiliate-suppression.csv` if present; otherwise flag `maybe_affiliate` for the sub-agent to reconcile with Alex before any contact.

9. **Score + rank.** `prospect_score` = relevance-dominant, then signal strength (superfan-of-N / power-linker-of-N / fresh), then DR as the tie-breaker. Drop everything below a relevance floor (default `relevance ≥ 4`; tighten if the list is huge). Rank best-first.

10. **Write the prospect queue + the mining report.**
    - `content-pipeline/off-page/link-prospects.csv` — one vetted row per domain: `domain, prospect_type(s), relevance, dr, competitor_evidence (which rivals + which of their pages), best_page_linked, anchor_seen, first_seen, contact_hint, prospect_score, suppressed_reason(blank if live)`. **This is the input to `/outreach`.**
    - `content-pipeline/off-page/mining-report.md` — at-a-glance: candidates found per type, how many dropped (already-link-to-us / trash / no-contact / affiliate), final vetted count, and the top 10 prospects with their one-line "why them + what excuse" so the outreach step has a head start.

11. **Tell the sub-agent / log:** `Mined N competitors → C candidates → V vetted prospects (S superfans, P power-linkers, F fresh); dropped X already-linking, Y trash, Z affiliate-suppressed.` Then the top 5 prospects, one line each.

## Output
- `content-pipeline/off-page/link-prospects.csv` — the vetted, ranked prospect queue (the deliverable; feeds `/outreach`).
- `content-pipeline/off-page/mining-report.md` — the human-readable summary + top prospects.
- `content-pipeline/off-page/our-backlinks.csv` refreshed (the suppression list, reusable next run).

## Quality checklist
- [ ] Every prospect row was checked against our own backlinks; **zero** rows have `already_links_to_us=true` (if any survive, the suppression join is broken).
- [ ] Trash filter actually fired — link farms / parked / PBN / comment-spam domains are absent from `link-prospects.csv` (spot-check 5 rows by eye).
- [ ] Relevance, not DR, drives the ranking — a high-DR irrelevant site does NOT outrank a relevant niche one (if it does, the score weights are wrong).
- [ ] At least one of each prospect type appears when the data supports it (a competitor with best-by-links pages should yield superfans; ≥ 2 rivals should yield power-linkers).
- [ ] `maybe_affiliate` candidates are flagged for Alex reconciliation, not silently queued for cold outreach.
- [ ] Each top prospect carries `competitor_evidence` (which rival page they linked) so `/outreach` can write a them-focused, specific excuse — never a generic blast.

## DO / DON'T
**DO**
- Replicate links competitors **already have** — mine their best-by-links pages, not random pages (`STRATEGY.md` Lesson 9).
- Prefer **relevant** linkers (niche fit) over high-DR-only — a topical DR-30 blog beats an off-topic DR-80 outlet.
- Subtract our existing linkers — only mine links we don't yet have.
- Treat the anchor + the linked competitor page as the seed for the outreach "excuse."
- Hand affiliate-shaped prospects to Alex; keep editorial prospects for `/outreach`.

**DON'T**
- Don't queue link farms, PBNs, scraper directories, parked/expired domains, or comment-spam hosts (Anti-pattern #15 — no spam sources).
- Don't gate on DR or chase high-DR-only (Lesson 9 names "high-DR-only" as a mistake).
- Don't contact anyone here — this skill **only builds the list**; sending is `/outreach`, and any outward send needs operator approval (charter guardrails).
- Don't re-prospect domains already linking to us, and don't cold-outreach Alex's affiliate partners.
- Don't fabricate a link or a contact — if Ahrefs is down, HALT; if a prospect has no human/contact, flag it `no_contact`, don't invent one.

## Winning =
A **steady stream of manual referring domains** (`STRATEGY.md` Lesson 9 "Winning = steady manual RDs") — built from a clean, relevant, de-duped prospect list that `/outreach` can work without wading through trash or burning goodwill on sites that already link to us. The list compounds: every cycle subtracts the wins from last cycle and surfaces the rivals' newest links, so we're always chasing links we don't have yet, never re-mining the same ground.
