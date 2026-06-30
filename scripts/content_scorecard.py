#!/usr/bin/env python3
"""Content scorecard (Piece 1 — MEASURE): per-article compound/rank/backlink + conversion attribution.

The course's thesis: a blog is a CUSTOMER-acquisition channel, not a traffic one, and growth =
traffic that COMPOUNDS (Lesson 1). This scorecard makes all of it measurable per article:

  - COMPOUND : organic (Google) blog pageviews per article (PostHog; no Ahrefs crawl lag),
               snapshotted each run -> classified compounding / flatline / decaying over the
               full snapshot history (Lesson 1's "does it add up over time?").
  - RANK     : best Google position per article (Ahrefs top-pages `top_keyword_best_position`).
  - BACKLINKS: referring domains per article (Ahrefs) -> the off-page/DR-building signal (Lesson 7/8).
  - CONVERT  : first-touch attribution (PostHog `$initial_pathname` = /blog/<slug>) -> accounts
               (subscription property set) -> PAID (starter/premium/ultimate).

Ahrefs enrichment is NON-FATAL (a measure tool must still report PostHog data if Ahrefs is down),
but any Ahrefs failure is surfaced loudly in the report — never silently dropped.

Output:
  content-pipeline/scorecard/snapshots/<YYYY-MM-DD>.json   (machine, for trajectory)
  content-pipeline/scorecard/latest.md                     (human report + signals)

Run:  doppler run -- python scripts/content_scorecard.py
Env (Doppler): POSTHOG_HOST, POSTHOG_PERSONAL_API_KEY, POSTHOG_PROJECT_ID,
               NEXT_PUBLIC_SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, AHREFS_API_KEY
"""
from __future__ import annotations

import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
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


def ahrefs_pages_by_slug() -> tuple[dict[str, dict], list[str]]:
    """Per-blog-page authority + rank from Ahrefs top-pages (referring_domains, best position, ahrefs traffic).

    NON-FATAL: returns ({}, [warning]) if Ahrefs is unavailable — the scorecard still reports PostHog data,
    but the warning is surfaced loudly in the report so a silent gap never masquerades as "no backlinks".
    """
    key = os.environ.get("AHREFS_API_KEY") or os.environ.get("AHREFS_MCP_KEY")
    if not key:
        return {}, ["AHREFS_API_KEY not set — backlink/rank columns skipped"]
    today = datetime.date.today().isoformat()
    params = urllib.parse.urlencode({
        "target": "pleasur.ai", "mode": "subdomains", "date": today, "country": "us",
        "order_by": "referring_domains:desc",
        "select": "url,referring_domains,top_keyword,top_keyword_best_position,sum_traffic", "limit": "1000",
    })
    url = f"https://api.ahrefs.com/v3/site-explorer/top-pages?{params}"
    try:
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {}, [f"⚠ Ahrefs top-pages HTTP {e.code} — backlink/rank columns skipped: {e.read().decode('utf-8', 'replace')[:120]}"]
    except Exception as e:  # noqa: BLE001 — measure must not crash on enrichment
        return {}, [f"⚠ Ahrefs top-pages unavailable — backlink/rank columns skipped: {e}"]
    rows = data.get("pages") or next((v for v in data.values() if isinstance(v, list)), [])
    out: dict[str, dict] = {}
    for p in rows:
        u = p.get("url") or ""
        if "/blog/" not in u:
            continue
        slug = u.split("/blog/", 1)[1].strip("/")
        out[slug] = {
            "referring_domains": int(p.get("referring_domains") or 0),
            "best_rank": p.get("top_keyword_best_position"),
            "rank_keyword": p.get("top_keyword") or "",
            "ahrefs_traffic": int(p.get("sum_traffic") or 0),
        }
    return out, []


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


def load_all_snapshots() -> list[dict]:
    if not SNAP_DIR.exists():
        return []
    out = []
    for snap in sorted(SNAP_DIR.glob("*.json")):
        try:
            out.append(json.loads(snap.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    return out


def organic_series(snapshots: list[dict], slug: str) -> list[int]:
    """Prior-snapshot history of pv_organic_30d for one slug (oldest -> newest)."""
    series: list[int] = []
    for snap in snapshots:
        for a in snap.get("articles", []):
            if a.get("slug") == slug:
                series.append(int(a.get("pv_organic_30d") or 0))
                break
    return series


def trajectory(curr: int, prior: int | None) -> str:
    if prior is None:
        return "new"
    if curr > prior * 1.1:
        return f"up (+{curr - prior})"
    if curr < prior * 0.9:
        return f"DOWN ({curr - prior})"
    return "flat"


def compound_class(prior_series: list[int], current: int) -> str:
    """Lesson 1: does the article's organic traffic COMPOUND (rise over time), flatline, or decay?

    Uses the whole snapshot history + this run. Min-absolute-move guards keep tiny numbers from reading
    as a trend.
    """
    pts = prior_series + [current]
    if len(pts) < 2:
        return "new"
    first, last = pts[0], pts[-1]
    if last >= max(first * 1.2, first + 5):
        return "compounding"
    if last <= first * 0.8 and (first - last) >= 5:
        return "decaying"
    return "flatline"


def main() -> int:
    today = datetime.date.today().isoformat()
    articles = fetch_articles()
    conv = convert_by_slug()
    traf = traffic_by_slug(30)
    prior = load_prior_snapshot()
    all_snaps = load_all_snapshots()
    ahrefs, ah_warn = ahrefs_pages_by_slug()

    rows = []
    for a in articles:
        slug = a["slug"]
        c = conv.get(slug, {})
        t = traf.get(slug, {})
        ap = ahrefs.get(slug, {})
        ft = c.get("first_touch", 0)
        paid = c.get("paid", 0)
        org_now = t.get("pv_organic", 0)
        rows.append({
            "slug": slug,
            "title": a.get("title", ""),
            "category": a.get("category", ""),
            "published_at": (a.get("published_at") or "")[:10],
            "pv_organic_30d": org_now,
            "pv_total_30d": t.get("pv_total", 0),
            "referring_domains": ap.get("referring_domains"),
            "best_rank": ap.get("best_rank"),
            "rank_keyword": ap.get("rank_keyword", ""),
            "ahrefs_traffic": ap.get("ahrefs_traffic"),
            "first_touch": ft,
            "accounts": c.get("accounts", 0),
            "paid": paid,
            "paid_per_1k_ft": round(paid / ft * 1000, 2) if ft else 0.0,
            "organic_traj": trajectory(org_now, (prior.get(slug) or {}).get("pv_organic_30d")),
            "rd_traj": trajectory(ap.get("referring_domains") or 0, (prior.get(slug) or {}).get("referring_domains")),
            "compound": compound_class(organic_series(all_snaps, slug), org_now),
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
    compounding = [r for r in rows if r["compound"] == "compounding"]
    decaying = [r for r in rows if r["compound"] == "decaying"]
    flat = [r for r in rows if r["compound"] == "flatline"]

    L = []
    L.append(f"# Content scorecard — {today}\n")
    if ah_warn:
        L.append("> " + " ".join(ah_warn) + "\n")
    L.append(f"**{len(rows)} published articles** · organic blog pageviews (30d): **{tot_org:,}** · "
             f"blog first-touch people (all-time): **{tot_ft:,}** · **PAID from blog: {tot_paid}**\n")
    L.append(f"> Blog→paid conversion (first-touch): **{tot_paid}/{tot_ft:,}** "
             f"= {round(tot_paid/tot_ft*100,3) if tot_ft else 0}%. The course's lesson in one number: "
             f"traffic is not customers. Fix = business-value keyword selection + per-article conversion.\n")

    # Lesson 1 lens: compounding vs flatline
    L.append("## Compounding vs flatline (Lesson 1 — does traffic *add up* over time?)\n")
    L.append(f"compounding: **{len(compounding)}** · flatline: **{len(flat)}** · decaying: **{len(decaying)}** "
             f"· new (need 2+ snapshots): **{len(rows) - len(compounding) - len(flat) - len(decaying)}**\n")
    if compounding:
        L.append("**Compounding (the wins — make more like these):** " + ", ".join(r["slug"] for r in compounding[:15]) + "\n")
    if decaying:
        L.append("**Decaying (relaunch candidates → Piece-2 audit):** " + ", ".join(r["slug"] for r in decaying[:15]) + "\n")

    L.append("## Per-article (sorted by paid, then organic traffic)\n")
    L.append("| Article | Pub | Org/30d | Traj | Compound | RD | Best rank | First-touch | Paid | Paid/1k |")
    L.append("|---|---|--:|---|---|--:|--:|--:|--:|--:|")
    for r in rows:
        rd = "—" if r["referring_domains"] is None else r["referring_domains"]
        rk = "—" if r["best_rank"] in (None, "") else r["best_rank"]
        L.append(f"| {r['slug']} | {r['published_at']} | {r['pv_organic_30d']:,} | {r['organic_traj']} | "
                 f"{r['compound']} | {rd} | {rk} | {r['first_touch']:,} | {r['paid']} | {r['paid_per_1k_ft']} |")

    L.append("\n## Signals\n")
    L.append(f"**Converters (replicate these):** {', '.join(r['slug'] for r in converters) or 'NONE yet — no blog article has driven a paid sub'}\n")
    L.append("**Leaky (high first-touch ≥200, ZERO paid — wrong intent or no conversion path):**")
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
    print(f"compound: {len(compounding)} compounding / {len(flat)} flat / {len(decaying)} decaying | "
          f"converters={len(converters)} leaky={len(leaky)} dead={len(dead)} ghosts={len(ghosts)}")
    if ah_warn:
        print("  " + " ".join(ah_warn))
    print(f"wrote {LATEST_MD.relative_to(ROOT)} + snapshots/{today}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
