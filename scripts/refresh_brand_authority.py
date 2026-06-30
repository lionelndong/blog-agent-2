#!/usr/bin/env python3
"""Refresh brand authority → cache/brand-dr.json (the winnability gate's LIVE calibration).

Fetches our live Domain Rating + referring-domain data from Ahrefs (REST v3, same source as the MCP)
and computes `max_targetable_kd` — the hardest keyword we can realistically rank for given our
authority. The winnability score in `keyword-prioritization` reads `domain_rating` (easy-win floor) +
`max_targetable_kd` (reach ceiling) from this file, so as our DR grows the ambition ladders up
automatically and is NEVER frozen at a hardcoded number (STRATEGY.md §2). Run weekly (a routine) or
whenever you want to recalibrate.

How max_targetable_kd is modeled (a deliberate, documented heuristic — NOT a measured value):
  max_targetable_kd = round(0.72 * DR + 15), clamped [10, 85]
  Anchored on two points: Ahrefs's own course statement (their DR ~90 best pages → they target KD up
  to ~80) and a conservative young-site point (DR ~21 → ~KD 30, which matches our observed
  winnable/unwinnable split). We deliberately do NOT use raw best-page referring domains as the
  ceiling: for a young blog that figure is ~0-1 (no link-building done yet), which would gate out
  everything; and domain-level RDs (~95) over-count, since we can't pour all domain authority onto one
  new page. DR is Ahrefs's normalized rollup of the whole profile and is the honest middle. We DO store
  the raw RD figures below for transparency and future refinement (once we've built content-page links,
  switch the ceiling to the real best-page RD curve).

Ahrefs REST: Authorization: Bearer $AHREFS_API_KEY (or $AHREFS_MCP_KEY); country LOWERCASE (`us`).
Run under doppler:  doppler run -p pleasurai -c dev -- python scripts/refresh_brand_authority.py
"""
import os, json, urllib.request, urllib.parse, datetime

API = "https://api.ahrefs.com/v3"
KEY = os.environ.get("AHREFS_API_KEY") or os.environ.get("AHREFS_MCP_KEY")
TARGET = "pleasur.ai"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "content-pipeline", "0-keywords", "cache", "brand-dr.json"))

def max_targetable_kd(dr):
    """The hardest KD we can realistically rank for at this DR (documented heuristic; see module docstring)."""
    if dr is None:
        return None
    return max(10, min(85, round(0.72 * dr + 15)))

def get(endpoint, params):
    if not KEY:
        raise RuntimeError("AHREFS_API_KEY/AHREFS_MCP_KEY not set — run under `doppler run -- ...`")
    url = f"{API}/{endpoint}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {KEY}", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode())

def dig(obj, *keys):
    if isinstance(obj, dict):
        for k in keys:
            if k in obj and not isinstance(obj[k], (dict, list)):
                return obj[k]
        for v in obj.values():
            r = dig(v, *keys)
            if r is not None:
                return r
    return None

def main():
    today = datetime.date.today().isoformat()
    dr = refdomains = best_page_rd = None
    notes = []

    # 1) Domain Rating
    try:
        d = get("site-explorer/domain-rating", {"target": TARGET, "date": today, "country": "us"})
        dr = dig(d, "domain_rating")
    except Exception as e:
        notes.append(f"domain-rating failed: {e}")

    # 2) Domain-level referring domains (transparency)
    try:
        b = get("site-explorer/backlinks-stats", {"target": TARGET, "mode": "subdomains", "date": today})
        refdomains = dig(b, "live_refdomains", "refdomains", "referring_domains")
    except Exception as e:
        notes.append(f"backlinks-stats failed: {e}")

    # 3) Best page by referring domains — the literal "Best by links" ceiling (transparency / future use)
    try:
        p = get("site-explorer/top-pages", {"target": TARGET, "mode": "subdomains", "date": today,
                                            "country": "us", "order_by": "referring_domains:desc",
                                            "select": "url,referring_domains,sum_traffic", "limit": "20"})
        rows = p.get("pages") or next((v for v in p.values() if isinstance(v, list)), [])
        if rows:
            best_page_rd = max((row.get("referring_domains") or 0) for row in rows if isinstance(row, dict))
    except Exception as e:
        notes.append(f"top-pages failed: {e}")

    max_kd = max_targetable_kd(dr)

    out = {
        "domain": TARGET,
        "domain_rating": dr,
        "max_targetable_kd": max_kd,
        "model": "max_targetable_kd = round(0.72*DR + 15), clamped [10,85]; anchored on Ahrefs course (DR~90 -> KD~80) + young-site point (DR~21 -> KD~30). DR-based on purpose; see refresh_brand_authority.py docstring.",
        "referring_domains_domain": refdomains,
        "best_page_referring_domains": best_page_rd,
        "fetched_at": today + "T00:00:00Z",
        "source": "ahrefs_rest_v3 (domain-rating + backlinks-stats + top-pages)",
        "note": "Winnability reads domain_rating (easy-win floor: kd<=DR) + max_targetable_kd (reach ceiling). "
                "Refresh weekly; if Ahrefs is down and this is stale, HALT rather than gate on a bare KD cutoff.",
        "diagnostics": notes,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"DR={dr}  domain_refdomains={refdomains}  best_page_rd={best_page_rd}  -> max_targetable_kd={max_kd}")
    if notes:
        print("notes:", "; ".join(notes))
    print("wrote:", OUT)

if __name__ == "__main__":
    main()
