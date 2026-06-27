#!/usr/bin/env python3
"""Content scorecard (Piece 1 — MEASURE): per-article rank/traffic + conversion attribution.

The course's thesis is that a blog is a CUSTOMER-acquisition channel, not a traffic one,
and that growth = traffic that COMPOUNDS. This scorecard makes both measurable per article:

  - REACH/COMPOUND : organic (Google) blog pageviews per article (real, from PostHog; no
                     Ahrefs crawl lag). Snapshotted each run -> trajectory over time.
  - CONVERT        : first-touch attribution (PostHog `$initial_pathname` = /blog/<slug>) ->
                     accounts created (subscription property set) -> PAID (starter/premium/ultimate).

Output:
  content-pipeline/scorecard/snapshots/<YYYY-MM-DD>.json   (machine, for trajectory)
  content-pipeline/scorecard/latest.md                     (human report + signals)

Run:  doppler run -- python scripts/content_scorecard.py
Env (Doppler): POSTHOG_HOST, POSTHOG_PERSONAL_API_KEY, POSTHOG_PROJECT_ID,
               NEXT_PUBLIC_SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
"""
from __future__ import annotations

import datetime
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

PAID_TIERS = ("starter", "premium", "ultimate")
BLOG_BASE = "https://pleasur.ai/blog"
ROOT = Path(__file__).resolve().parents[1]
SNAP_DIR = ROOT / "content-pipeline" / "scorecard" / "snapshots"
LATEST_MD = ROOT / "content-pipeline" / "scorecard" / "latest.md"


def _env(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        sys.exit(f"error: {name} not set — run under `doppler run -- python ...`")
    return v


def _post_json(url: str, body: dict, headers: dict) -> dict:
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={**headers, "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def _get_json(url: str, headers: dict):
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode()), r.headers


def hogql(query: str) -> list:
    host = _env("POSTHOG_HOST").rstrip("/")
    pid = _env("POSTHOG_PROJECT_ID")
    key = _env("POSTHOG_PERSONAL_API_KEY")
    url = f"{host}/api/projects/{pid}/query/"
    try:
        j = _post_json(url, {"query": {"kind": "HogQLQuery", "query": query}}, {"Authorization": f"Bearer {key}"})
    except urllib.error.HTTPError as e:
        sys.exit(f"error: PostHog HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")
    return j.get("results", [])


def fetch_articles() -> list[dict]:
    base = _env("NEXT_PUBLIC_SUPABASE_URL").rstrip("/")
    key = _env("SUPABASE_SERVICE_ROLE_KEY")
    url = f"{base}/rest/v1/blog_posts?select=slug,title,category,author_name,published_at,status&status=eq.published&order=published_at.desc"
    rows, _ = _get_json(url, {"apikey": key, "Authorization": f"Bearer {key}"})
    return rows


def convert_by_slug() -> dict[str, dict]:
    """First-touch attribution at the persons level (fast)."""
    q = (
        "SELECT replaceRegexpOne(replaceRegexpOne(properties.$initial_pathname, '^/blog/', ''), '/+$', '') AS slug, "
        "count() AS first_touch, "
        "countIf(isNotNull(properties.subscription)) AS accounts, "
        f"countIf(properties.subscription IN {PAID_TIERS}) AS paid "
        "FROM persons WHERE properties.$initial_pathname LIKE '/blog/%' GROUP BY slug ORDER BY first_touch DESC LIMIT 500"
    )
    out: dict[str, dict] = {}
    for slug, first_touch, accounts, paid in hogql(q):
        out[slug] = {"first_touch": int(first_touch or 0), "accounts": int(accounts or 0), "paid": int(paid or 0)}
    return out


def traffic_by_slug(days: int = 30) -> dict[str, dict]:
    """Organic (Google) vs total blog pageviews per article, last N days (events level, scoped)."""
    q = (
        "SELECT replaceRegexpOne(replaceRegexpOne(properties.$pathname, '^/blog/', ''), '/+$', '') AS slug, "
        "count() AS pv_total, "
        "countIf(properties.$referring_domain LIKE '%google%') AS pv_organic, "
        "uniq(person_id) AS people "
        "FROM events WHERE event = '$pageview' AND properties.$pathname LIKE '/blog/%' "
        f"AND timestamp > now() - INTERVAL {days} DAY GROUP BY slug ORDER BY pv_total DESC LIMIT 500"
    )
    out: dict[str, dict] = {}
    for slug, pv_total, pv_organic, people in hogql(q):
        out[slug] = {"pv_total": int(pv_total or 0), "pv_organic": int(pv_organic or 0), "people": int(people or 0)}
    return out


def load_prior_snapshot() -> dict:
    if not SNAP_DIR.exists():
        return {}
    snaps = sorted(SNAP_DIR.glob("*.json"))
    if not snaps:
        return {}
    try:
        prior = json.loads(snaps[-1].read_text(encoding="utf-8"))
        return {r["slug"]: r for r in prior.get("articles", [])}
    except (json.JSONDecodeError, KeyError):
        return {}


def trajectory(curr: int, prior: int | None) -> str:
    if prior is None:
        return "new"
    if curr > prior * 1.1:
        return f"up (+{curr - prior})"
    if curr < prior * 0.9:
        return f"DOWN ({curr - prior})"
    return "flat"


def main() -> int:
    today = datetime.date.today().isoformat()
    articles = fetch_articles()
    conv = convert_by_slug()
    traf = traffic_by_slug(30)
    prior = load_prior_snapshot()

    rows = []
    for a in articles:
        slug = a["slug"]
        c = conv.get(slug, {})
        t = traf.get(slug, {})
        ft = c.get("first_touch", 0)
        paid = c.get("paid", 0)
        rows.append({
            "slug": slug,
            "title": a.get("title", ""),
            "category": a.get("category", ""),
            "published_at": (a.get("published_at") or "")[:10],
            "pv_organic_30d": t.get("pv_organic", 0),
            "pv_total_30d": t.get("pv_total", 0),
            "first_touch": ft,
            "accounts": c.get("accounts", 0),
            "paid": paid,
            "paid_per_1k_ft": round(paid / ft * 1000, 2) if ft else 0.0,
            "organic_traj": trajectory(t.get("pv_organic", 0), (prior.get(slug) or {}).get("pv_organic_30d")),
        })

    rows.sort(key=lambda r: (r["paid"], r["pv_organic_30d"]), reverse=True)

    published_slugs = {a["slug"] for a in articles}
    ghosts = sorted(
        ({"slug": s, **d} for s, d in conv.items() if s and s not in published_slugs and d.get("first_touch", 0) >= 100),
        key=lambda g: g["first_touch"], reverse=True,
    )

    # snapshot (managed + ghost) — consumed by the audit engine (Piece 2)
    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    (SNAP_DIR / f"{today}.json").write_text(json.dumps({"date": today, "articles": rows, "ghosts": ghosts}, indent=2), encoding="utf-8")

    # totals + signals
    tot_ft = sum(r["first_touch"] for r in rows)
    tot_paid = sum(r["paid"] for r in rows)
    tot_org = sum(r["pv_organic_30d"] for r in rows)
    converters = [r for r in rows if r["paid"] > 0]
    leaky = [r for r in rows if r["first_touch"] >= 200 and r["paid"] == 0]   # high reach, zero paid
    dead = [r for r in rows if r["pv_organic_30d"] == 0 and r["first_touch"] < 20]  # no traffic, no entry

    L = []
    L.append(f"# Content scorecard — {today}\n")
    L.append(f"**{len(rows)} published articles** · organic blog pageviews (30d): **{tot_org:,}** · "
             f"blog first-touch people (all-time): **{tot_ft:,}** · **PAID from blog: {tot_paid}**\n")
    L.append(f"> Blog→paid conversion (first-touch): **{tot_paid}/{tot_ft:,}** "
             f"= {round(tot_paid/tot_ft*100,3) if tot_ft else 0}%. The course's lesson in one number: "
             f"traffic is not customers. Fix = business-value keyword selection + per-article conversion.\n")

    L.append("## Per-article (sorted by paid, then organic traffic)\n")
    L.append("| Article | Pub | Organic/30d | Traj | First-touch | Accounts | Paid | Paid/1k |")
    L.append("|---|---|--:|---|--:|--:|--:|--:|")
    for r in rows:
        L.append(f"| {r['slug']} | {r['published_at']} | {r['pv_organic_30d']:,} | {r['organic_traj']} | "
                 f"{r['first_touch']:,} | {r['accounts']:,} | {r['paid']} | {r['paid_per_1k_ft']} |")

    L.append("\n## Signals\n")
    L.append(f"**Converters (replicate these):** {', '.join(r['slug'] for r in converters) or 'NONE yet — no blog article has driven a paid sub'}\n")
    L.append(f"**Leaky (high first-touch ≥200, ZERO paid — wrong intent or no conversion path):**")
    for r in leaky[:12]:
        L.append(f"- {r['slug']} — {r['first_touch']:,} first-touch, 0 paid")
    L.append(f"\n**Dead (no organic traffic + ~no entry — audit/delete candidates for Piece 2):** "
             f"{', '.join(r['slug'] for r in dead[:15]) or 'none'}\n")

    L.append(f"\n## Ghost traffic — first-touch on slugs NOT in blog_posts ({len(ghosts)})\n")
    L.append("Legacy/unmanaged URLs still pulling entries — Piece-2 audit (reclaim, redirect, or re-adopt into the managed set):\n")
    for g in ghosts[:15]:
        L.append(f"- /blog/{g['slug']} — {g['first_touch']:,} first-touch · {g['paid']} paid")

    LATEST_MD.parent.mkdir(parents=True, exist_ok=True)
    LATEST_MD.write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"scorecard: {len(rows)} articles | organic/30d {tot_org:,} | first-touch {tot_ft:,} | paid {tot_paid}")
    print(f"converters={len(converters)} leaky={len(leaky)} dead={len(dead)} ghosts={len(ghosts)}")
    print(f"wrote {LATEST_MD.relative_to(ROOT)} + snapshots/{today}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
