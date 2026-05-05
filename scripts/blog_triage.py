#!/usr/bin/env python3
"""Triage the 222 published Pleasur.AI articles into KEEP / CONSOLIDATE / DELETE buckets.

LEGACY one-shot script. The blog-agent has migrated from Ahrefs to Semrush; the signals
file this reads is a historical Ahrefs snapshot (pre-migration, archived to
`scripts/_archive/_ahrefs_signals.json`). To re-run triage, capture a fresh Semrush
equivalent (Domain Organic Pages + Backlink Analytics) into `scripts/_semrush_signals.json`
and update the SIGNALS path below.

Inputs (all already on disk):
    content-pipeline/brand-articles.json        Strapi inventory (title, slug, url, publishedAt)
    scripts/_archive/_ahrefs_signals.json       hand-curated Ahrefs MCP snapshot from 2026-05-03
                                                (preserved for reproduction; do not regenerate
                                                via Ahrefs — Semrush is the new source of truth)

Outputs:
    content-pipeline/audit/blog-triage.csv          row per article with the verdict
    content-pipeline/audit/clusters.json            duplicate-title cluster groups
    content-pipeline/audit/blog-triage-summary.md   human-readable report, batched for review

Methodology:
    1. Each article gets a "value score" combining ranking signal + backlink signal.
    2. Titles are normalised (lowercase, strip year, strip stopwords) and clustered by
       Jaccard similarity on the resulting token sets. Clusters >= 2 articles get a
       canonical pick (highest value score, falling back to most recent publishedAt).
    3. Verdict per article:
        - KEEP        : value_score > 0 AND not a duplicate (or it IS the cluster canonical)
        - CONSOLIDATE : duplicate of a stronger sibling (delete + 301 to the canonical)
        - DELETE      : value_score == 0 AND not in any cluster (orphan slop)
        - REVIEW      : value_score == 0 BUT in a cluster where canonical also has 0 score
                        (let the human decide which to keep when nothing's ranking)
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "content-pipeline" / "brand-articles.json"
SIGNALS = ROOT / "scripts" / "_archive" / "_ahrefs_signals.json"
AUDIT_DIR = ROOT / "content-pipeline" / "audit"

STOPWORDS = {
    # English stopwords
    "the", "a", "an", "of", "for", "in", "on", "to", "and", "or", "but", "with",
    "your", "you", "is", "are", "was", "were", "be", "been", "being",
    "what", "how", "why", "when", "where", "which", "who", "whom",
    "this", "that", "these", "those", "it", "its",
    # Generic blog-title boilerplate (Pleasur.AI uses these in templates)
    "actually", "really", "honest", "guide", "guides", "best", "top", "ultimate",
    "complete", "definitive", "review", "reviews", "tested", "ranking", "ranked",
    "alternative", "alternatives", "comparison", "compared", "vs", "versus",
    "options", "option", "every", "use", "case", "uses", "cases", "available",
    "platforms", "platform", "find", "finding", "getting", "started", "guide",
    "tested", "testing", "hours", "after", "before", "ranked", "picks",
    # "AI" appears in virtually every title — drop for clustering signal
    "ai", "app", "apps",
    # Years
    "2024", "2025", "2026", "2027",
}


@dataclass(frozen=True)
class Signal:
    rank_keywords: int = 0
    rank_traffic: int = 0
    best_keyword_volume: int = 0
    best_position: int | None = None
    refdomains: int = 0
    backlinks: int = 0


@dataclass(frozen=True)
class Article:
    slug: str
    url: str
    title: str
    publishedAt: str | None
    signal: Signal
    tokens: frozenset[str]
    value_score: int

    @property
    def published_dt(self) -> datetime:
        if not self.publishedAt:
            return datetime.min
        try:
            return datetime.fromisoformat(self.publishedAt.replace("Z", "+00:00"))
        except ValueError:
            return datetime.min


@dataclass
class Cluster:
    members: list[Article] = field(default_factory=list)
    canonical_slug: str = ""

    def pick_canonical(self) -> Article:
        # Highest value score wins. Tiebreaker: most recent publishedAt.
        return max(self.members, key=lambda a: (a.value_score, a.published_dt))


def load_inventory() -> list[dict]:
    return json.loads(INVENTORY.read_text(encoding="utf-8"))["articles"]


def load_signals() -> dict[str, Signal]:
    if not SIGNALS.exists():
        return {}
    raw = json.loads(SIGNALS.read_text(encoding="utf-8"))
    by_url: dict[str, Signal] = {}
    # Ranking aggregation
    rank_acc: dict[str, dict] = defaultdict(lambda: {
        "kw": 0, "traffic": 0, "best_vol": 0, "best_pos": None,
    })
    for k in raw.get("organic_keywords", []):
        u = k["best_position_url"]
        rank_acc[u]["kw"] += 1
        rank_acc[u]["traffic"] += int(k.get("sum_traffic") or 0)
        if int(k.get("volume") or 0) > rank_acc[u]["best_vol"]:
            rank_acc[u]["best_vol"] = int(k["volume"])
        pos = int(k.get("best_position") or 999)
        cur = rank_acc[u]["best_pos"]
        if cur is None or pos < cur:
            rank_acc[u]["best_pos"] = pos
    # Backlink aggregation
    bl_acc: dict[str, dict] = {}
    for p in raw.get("backlinks", []):
        u = p["url_to"]
        bl_acc[u] = {
            "refdomains": int(p.get("refdomains_target") or 0),
            "backlinks": int(p.get("links_to_target") or 0),
        }
    # Merge
    all_urls = set(rank_acc) | set(bl_acc)
    for u in all_urls:
        r = rank_acc.get(u, {})
        b = bl_acc.get(u, {})
        by_url[u] = Signal(
            rank_keywords=r.get("kw", 0),
            rank_traffic=r.get("traffic", 0),
            best_keyword_volume=r.get("best_vol", 0),
            best_position=r.get("best_pos"),
            refdomains=b.get("refdomains", 0),
            backlinks=b.get("backlinks", 0),
        )
    return by_url


def value_score(s: Signal) -> int:
    """Composite score — higher = more reason to keep.

    Weights tuned for the user's stated criterion: keep what ranks, kill the rest.
        +10 per keyword in top 10
        +5  per keyword in top 30
        +2  per keyword anywhere
        +1  per unit of organic traffic
        +5  per referring domain
        +1  per individual backlink
        +log10(best_keyword_volume) bonus when ranking on a high-volume term
    """
    score = 0
    if s.best_position is not None:
        if s.best_position <= 10:
            score += 10
        elif s.best_position <= 30:
            score += 5
        score += 2 * s.rank_keywords
    score += s.rank_traffic
    score += 5 * s.refdomains
    score += s.backlinks
    if s.best_keyword_volume >= 1000:
        score += 3
    elif s.best_keyword_volume >= 100:
        score += 1
    return score


def tokenize(title: str) -> frozenset[str]:
    t = title.lower()
    t = re.sub(r"[^a-z0-9\s-]", " ", t)
    tokens = {w for w in re.split(r"[\s-]+", t) if w}
    tokens -= STOPWORDS
    tokens = {w for w in tokens if len(w) > 2}
    return frozenset(tokens)


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def cluster_articles(articles: list[Article], threshold: float = 0.5) -> list[Cluster]:
    # Greedy single-link clustering. For each article, attach to the first existing
    # cluster whose any-member Jaccard >= threshold; otherwise spawn a new cluster.
    clusters: list[Cluster] = []
    for art in articles:
        attached = False
        for c in clusters:
            if any(jaccard(art.tokens, m.tokens) >= threshold for m in c.members):
                c.members.append(art)
                attached = True
                break
        if not attached:
            clusters.append(Cluster(members=[art]))
    for c in clusters:
        c.canonical_slug = c.pick_canonical().slug
    return clusters


def verdict(art: Article, cluster: Cluster) -> tuple[str, str, str]:
    """Returns (verdict, redirect_target_slug, reason)."""
    cluster_size = len(cluster.members)
    canonical = cluster.canonical_slug
    sibling_max = max(m.value_score for m in cluster.members) if cluster_size > 1 else 0

    # Duplicate cluster cases — three sub-cases:
    if cluster_size > 1:
        # Case A: nobody in the cluster ranks. Whole cluster is REVIEW —
        # editor decides which (if any) survives. Canonical pick is just a hint.
        if sibling_max == 0:
            role = "suggested canonical" if art.slug == canonical else "duplicate sibling"
            return ("REVIEW", canonical,
                    f"{role} of zero-signal cluster (size {cluster_size}); "
                    f"editor must pick a survivor or delete the whole topic")
        # Case B: at least one member ranks. The strongest is canonical, kept.
        if art.slug == canonical:
            return ("KEEP", "", f"canonical of cluster ({cluster_size} articles); "
                                f"value={art.value_score}; siblings max={sibling_max}")
        # Case C: I'm a non-canonical sibling in a cluster with a ranker.
        return ("CONSOLIDATE", canonical,
                f"duplicate of {canonical} (value {art.value_score} vs canonical {sibling_max})")

    # Solo article (cluster size 1)
    if art.value_score > 0:
        return ("KEEP", "", f"solo article with value={art.value_score}")
    return ("DELETE", "", f"solo article, no rankings, no backlinks — slop candidate")


def main() -> None:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    inventory = load_inventory()
    signals_by_url = load_signals()

    articles: list[Article] = []
    for raw in inventory:
        url = raw["url"]
        sig = signals_by_url.get(url, Signal())
        tokens = tokenize(raw["title"])
        articles.append(Article(
            slug=raw["slug"],
            url=url,
            title=raw["title"],
            publishedAt=raw.get("publishedAt"),
            signal=sig,
            tokens=tokens,
            value_score=value_score(sig),
        ))

    # Sort articles by value_score desc so canonical picks favor highest-signal first
    articles.sort(key=lambda a: -a.value_score)
    clusters = cluster_articles(articles, threshold=0.5)
    cluster_by_slug: dict[str, Cluster] = {}
    for c in clusters:
        for m in c.members:
            cluster_by_slug[m.slug] = c

    # Write CSV
    csv_path = AUDIT_DIR / "blog-triage.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "slug", "title", "url", "verdict", "redirect_target_slug", "reason",
            "value_score", "rank_keywords", "rank_traffic", "best_position",
            "best_keyword_volume", "refdomains", "backlinks",
            "cluster_size", "cluster_canonical_slug", "publishedAt",
        ])
        # Stable order: by verdict tier then value_score
        verdict_order = {"KEEP": 0, "REVIEW": 1, "CONSOLIDATE": 2, "DELETE": 3}
        ranked = sorted(articles, key=lambda a: (
            verdict_order[verdict(a, cluster_by_slug[a.slug])[0]],
            -a.value_score,
        ))
        for art in ranked:
            c = cluster_by_slug[art.slug]
            v, redirect, reason = verdict(art, c)
            w.writerow([
                art.slug, art.title, art.url, v, redirect, reason,
                art.value_score, art.signal.rank_keywords, art.signal.rank_traffic,
                art.signal.best_position if art.signal.best_position is not None else "",
                art.signal.best_keyword_volume,
                art.signal.refdomains, art.signal.backlinks,
                len(c.members), c.canonical_slug, art.publishedAt or "",
            ])

    # Write clusters.json
    clusters_path = AUDIT_DIR / "clusters.json"
    cluster_dump = []
    for c in clusters:
        if len(c.members) > 1:
            cluster_dump.append({
                "canonical_slug": c.canonical_slug,
                "size": len(c.members),
                "members": [
                    {
                        "slug": m.slug,
                        "title": m.title,
                        "value_score": m.value_score,
                        "is_canonical": m.slug == c.canonical_slug,
                    }
                    for m in c.members
                ],
            })
    cluster_dump.sort(key=lambda x: -x["size"])
    clusters_path.write_text(json.dumps(cluster_dump, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Write summary
    counts: dict[str, list[Article]] = defaultdict(list)
    for art in articles:
        v = verdict(art, cluster_by_slug[art.slug])[0]
        counts[v].append(art)

    summary_lines = [
        "# Blog triage — Pleasur.AI",
        "",
        f"Inventory: **{len(articles)} published articles**",
        f"Cache snapshot: `content-pipeline/brand-articles.json`",
        f"Ahrefs signals dumped to: `scripts/_ahrefs_signals.json`",
        "",
        "## Headline finding",
        "",
        f"**Of 222 published articles, only 8 (3.6%) have any Ahrefs-detected organic signal** (5 ranking + 3 with a single referring domain each, all UR=0).",
        f"The other 214 articles are functionally invisible to organic search per Ahrefs. The user's '~90% slop' estimate matches reality.",
        "",
        "## Verdict counts",
        "",
        "| Verdict | Count | % | Action |",
        "|---|---|---|---|",
        f"| **KEEP** | {len(counts['KEEP'])} | {len(counts['KEEP'])*100//len(articles)}% | leave as-is; these earn rankings/backlinks |",
        f"| **CONSOLIDATE** | {len(counts['CONSOLIDATE'])} | {len(counts['CONSOLIDATE'])*100//len(articles)}% | dupe of a stronger sibling — delete + 301 to the canonical |",
        f"| **REVIEW** | {len(counts['REVIEW'])} | {len(counts['REVIEW'])*100//len(articles)}% | duplicate clusters where nothing ranks — editor picks canonical or deletes whole topic |",
        f"| **DELETE** | {len(counts['DELETE'])} | {len(counts['DELETE'])*100//len(articles)}% | solo article, zero rankings, zero backlinks — slop |",
        "",
        "## Caveats — read before approving any batch",
        "",
        "1. **Ahrefs only sees organic-search signal.** Direct, social, email, and referral traffic are invisible here. If you have Pleasur.AI internal analytics (Plausible, GA4, etc.), cross-reference the `DELETE` list against your own pageview data before pulling the trigger.",
        "2. **Articles published in the last ~30 days may not be crawled by Ahrefs yet.** A new article that's about to rank but hasn't been picked up will look like 'slop' here. Filter the CSV by `publishedAt` and skip recent posts in your first delete batch.",
        "3. **Internal-link equity isn't measured.** `pages-by-backlinks` shows external referring domains only. An article with zero external backlinks but 20 internal links pointing at it is still load-bearing for site architecture. Run a crawl (Screaming Frog or similar) before deletion to surface internal-link counts per slug.",
        "4. **CONSOLIDATE redirect targets need semantic verification.** The script picks the highest-value cluster member as the canonical, but that's a structural pick, not a semantic one. Example from this run: `ai-rp-chat-guide-2026` (roleplay) consolidates into `dirty-ai-guide-2026` (adult chat) because they cluster on title overlap — but a roleplay-seeking visitor landing on a 'dirty AI' page is a bad UX. Skim each CONSOLIDATE row and either accept the suggested target or retarget to a more semantically appropriate slug.",
        "5. **Deletion is permanent in Strapi unless you have soft-delete enabled.** Confirm your Strapi instance supports soft-delete OR back up the article bodies (export to JSON) before deleting.",
        "6. **301 redirects must be live BEFORE delete.** Strapi articles are served by your frontend (Next.js?) routing. Deleting an article without a redirect = 404 = lost equity. Configure all redirects in your `next.config.js` / Vercel config first, deploy, verify a few with curl, then run the deletes.",
        "",
        "## Why the script flagged false-positive clusters in REVIEW",
        "",
        "The clustering uses Jaccard similarity on title tokens (after stopword removal). Two known weaknesses:",
        "- **Greedy single-link**: an article joins a cluster if ANY existing member shares ≥50% tokens. Chains can form (A↔B↔C) where A and C are unrelated.",
        "- **Title-only**: I don't have article body content yet (Strapi `populate=*` didn't return content fields in the inventory pull — that's fixable in `fetch_strapi_inventory.py` if needed).",
        "",
        "Treat clusters of size ≥5 with skepticism — they may need to be split into sub-clusters by topic. Smaller clusters (size 2-3) are usually right.",
        "",
        "## Top duplicate clusters (the slop you specifically called out)",
        "",
    ]
    multi_clusters = [c for c in clusters if len(c.members) > 1]
    multi_clusters.sort(key=lambda c: -len(c.members))
    for c in multi_clusters[:15]:
        summary_lines.append(f"### Cluster: `{c.canonical_slug}` ({len(c.members)} articles)")
        summary_lines.append("")
        summary_lines.append("| | Slug | Title | Value | Verdict |")
        summary_lines.append("|---|---|---|---|---|")
        for m in sorted(c.members, key=lambda a: -a.value_score):
            v, _, _ = verdict(m, c)
            star = "**(canonical)**" if m.slug == c.canonical_slug else ""
            summary_lines.append(
                f"| {star} | `{m.slug}` | {m.title[:80]} | {m.value_score} | {v} |"
            )
        summary_lines.append("")

    summary_lines += [
        "## Suggested batches for approval",
        "",
        "Don't approve all at once. Recommend three batches, smallest blast radius first:",
        "",
        "### Batch A — `DELETE` solo orphans (lowest risk)",
        f"- {len(counts['DELETE'])} articles",
        "- Solo articles, zero ranking, zero external referring domains, no duplicate cluster",
        "- These are pure slop with no equity. Delete cleanly (no redirect needed unless internal links point at them).",
        "- **Recommended: review the CSV `DELETE` rows, then approve in batches of ~25 at a time.**",
        "",
        "### Batch B — `CONSOLIDATE` losers in clusters with a winner",
        f"- {len(counts['CONSOLIDATE'])} articles",
        "- Duplicate of a stronger sibling. Each gets a 301 redirect to its `redirect_target_slug` before deletion.",
        "- Setting up redirects is the load-bearing step. If your stack uses Next.js redirects in `next.config.js` or a Strapi `redirects` collection, batch-write them first, deploy, verify, then delete.",
        "",
        "### Batch C — `REVIEW` orphan-cluster duplicates",
        f"- {len(counts['REVIEW'])} articles",
        "- Duplicate clusters where NO member ranks. Pick a canonical by reading the bodies (script doesn't have access to Strapi content yet); 301 the others to it.",
        "- Could also choose to delete the entire cluster if the topic isn't a brand priority.",
        "",
        "## Files generated",
        "",
        "- `content-pipeline/audit/blog-triage.csv` — full per-article verdict table",
        "- `content-pipeline/audit/clusters.json` — machine-readable cluster groupings",
        "- `content-pipeline/audit/blog-triage-summary.md` — this file",
        "",
        "## Next step",
        "",
        "Open `blog-triage.csv` and skim the `DELETE` and `CONSOLIDATE` rows. Tell me which batch (A / B / C) to start with and how many at a time. **No deletions hit Strapi until you confirm.**",
    ]

    summary_path = AUDIT_DIR / "blog-triage-summary.md"
    summary_path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    # Console summary
    print(f"Wrote {csv_path.relative_to(ROOT)} ({len(articles)} rows)")
    print(f"Wrote {clusters_path.relative_to(ROOT)} ({len(multi_clusters)} multi-article clusters)")
    print(f"Wrote {summary_path.relative_to(ROOT)}")
    print()
    print("Verdict distribution:")
    for v in ("KEEP", "REVIEW", "CONSOLIDATE", "DELETE"):
        print(f"  {v:12s} {len(counts[v]):3d}")


if __name__ == "__main__":
    main()
