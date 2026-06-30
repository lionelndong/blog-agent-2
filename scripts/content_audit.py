#!/usr/bin/env python3
"""Content audit engine (Piece 2 — COMPOUND).

Reads the latest scorecard snapshot (Piece 1) and buckets every article into an action:
  DELETE   - dead weight / test artifacts (prune; Ahrefs deleted ~half their corpus)
  DEFEND   - performers (paid or real organic) -> keep fresh, competitors are coming
  RELAUNCH - LEAKY: high first-touch, 0 paid -> fix business-value/conversion + re-promote
  WATCH    - too new to judge
  REVIVE   - had entry but no organic now -> update / re-target intent
  LEAVE    - modest + stable
Plus: cannibalization candidates (301 weaker->stronger) and ghost-URL reclaim
(high-traffic slugs not in blog_posts -> 301 or re-adopt).

RELAUNCH PLAN (Lesson 5 audit + Lesson 8 "don't abandon old winners"): on top of the buckets,
the audit builds a concrete, per-article relaunch work order — pages that are `compound=="decaying"`
OR rank-slipping vs the PRIOR snapshot, AND were ever valuable (traffic/links). Each row is
{slug, reason, best_rank, referring_domains, what_to_refresh} — the input the `/relaunch` skill
executes (refresh -> bump published date -> re-promote as new). Rank-slip detection needs >=2
snapshots; with one snapshot it relies on the `compound` class alone.

This PRODUCES THE PLAN. Destructive / outward-facing actions (delete, merge/301, ghost
redirect) are flagged REQUIRES APPROVAL — execution is a separate, board-gated step. The relaunch
plan is AUTONOMOUS-SAFE (an update, not a destructive action).

Run:  python scripts/content_audit.py   (after scripts/content_scorecard.py)
"""
from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAP_DIR = ROOT / "content-pipeline" / "scorecard" / "snapshots"
OUT = ROOT / "content-pipeline" / "audit"

# generic words that don't distinguish a topic (so cannibalization compares the real core)
STOP = {"ai", "best", "free", "guide", "2026", "2025", "2024", "the", "a", "an",
        "to", "for", "vs", "how", "what", "is", "your", "my", "top", "and"}


def latest_snapshot() -> dict:
    snaps = sorted(SNAP_DIR.glob("*.json")) if SNAP_DIR.exists() else []
    if not snaps:
        sys.exit("error: no scorecard snapshot — run scripts/content_scorecard.py first")
    return json.loads(snaps[-1].read_text(encoding="utf-8"))


def prior_snapshot() -> dict[str, dict]:
    """The snapshot *before* the latest, keyed by slug — for rank-slip / trend comparison.

    Returns {} when there's only one snapshot (a first audit can't see movement yet). The
    relaunch mechanic degrades gracefully: with no prior, it relies on `compound` alone.
    """
    snaps = sorted(SNAP_DIR.glob("*.json")) if SNAP_DIR.exists() else []
    if len(snaps) < 2:
        return {}
    try:
        prev = json.loads(snaps[-2].read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return {a["slug"]: a for a in prev.get("articles", []) if a.get("slug")}


def core_tokens(slug: str) -> frozenset[str]:
    out = []
    for t in re.split(r"[-_]", slug.lower()):
        t = t.strip()
        if not t or t in STOP:
            continue
        if len(t) > 3 and t.endswith("s"):  # naive singularize: apps->app, reviews->review
            t = t[:-1]
        out.append(t)
    return frozenset(out)


def jaccard(a: frozenset, b: frozenset) -> float:
    return len(a & b) / len(a | b) if (a and b) else 0.0


def age_days(published_at: str, today: datetime.date) -> int:
    try:
        return (today - datetime.date.fromisoformat((published_at or "")[:10])).days
    except ValueError:
        return 9999


def bucket(a: dict, today: datetime.date) -> tuple[str, str]:
    slug, ft, paid, org = a["slug"], a.get("first_touch", 0), a.get("paid", 0), a.get("pv_organic_30d", 0)
    age = age_days(a.get("published_at", ""), today)
    if "test" in slug or "ple-2990" in slug:
        return "DELETE", "test/dev artifact — should not be public"
    if age > 30 and org == 0 and ft < 10:
        return "DELETE", f"dead: {age}d old, 0 organic/30d, <10 first-touch ever"
    if paid > 0:
        return "DEFEND", f"performer ({paid} paid, {org} organic/30d) — keep fresh, defend rank"
    if (ft >= 150 or org >= 50) and paid == 0:
        note = "; rank still maturing" if age <= 21 else ""
        return "RELAUNCH", f"LEAKY: {ft:,} first-touch, {org} organic/30d, 0 paid — fix business-value + conversion, re-promote{note}"
    if age <= 21:
        return "WATCH", f"recent ({age}d) — too new to judge"
    if ft >= 20 and org == 0:
        return "REVIVE", f"{ft} first-touch but 0 organic/30d — faded or wrong intent; update/re-target"
    return "LEAVE", "modest + stable"


# ── Relaunch mechanic (Lesson 5 audit + Lesson 8 "don't abandon old winners") ──────────────
# A decayed-but-valuable page is the course's single best ROI: it already earned rank and links;
# we refresh it and re-promote as new instead of starting cold. This turns the RELAUNCH bucket
# from a flag into a concrete, per-article work order.

# How much rank has to worsen (positions) before we call it a real slip, not noise. Ranks are
# noisy at the bottom; a 3-spot drift near the top matters more than a 3-spot drift at #40, but a
# fixed floor keeps the rule legible and un-gameable (mirrors the scorecard's min-move guards).
RANK_SLIP_MIN = 3


def rank_worsened(curr: dict, prev: dict | None) -> tuple[bool, str]:
    """Did this article's best Google rank slip vs the prior snapshot?

    Lower rank number = better. Worsening = the number went UP by >= RANK_SLIP_MIN. Returns
    (slipped, human_reason). Null/None ranks (no Ahrefs data either run) → not a slip we can prove.
    """
    if not prev:
        return False, ""
    a, b = curr.get("best_rank"), prev.get("best_rank")
    if not isinstance(a, int) or not isinstance(b, int):
        return False, ""
    if a - b >= RANK_SLIP_MIN:
        return True, f"rank slipped #{b}→#{a} (−{a - b}) since last snapshot"
    return False, ""


def had_value(a: dict) -> bool:
    """Was this page ever worth defending? Traffic (organic or first-touch entries) or links.

    Keeps the GIF-trap pages out only via the caller's RELAUNCH gate; here we just ask "did it
    ever pull anything?" so we never relaunch a page that was always dead (that's DELETE's job).
    """
    return (
        a.get("pv_organic_30d", 0) > 0
        or a.get("first_touch", 0) >= 20
        or (a.get("referring_domains") or 0) > 0
    )


def what_to_refresh(a: dict, rank_slipped: bool) -> str:
    """The concrete refresh checklist for ONE article — what the relaunch skill should execute.

    Tailored to the article's own signals (decaying vs slipping, thin links, weak conversion), so
    the plan reads like a work order, not a generic 'update it'. See .claude/skills/relaunch.
    """
    todo: list[str] = []
    if a.get("compound") == "decaying":
        todo.append("freshen data/examples + re-verify intent vs the live SERP (traffic is fading)")
    if rank_slipped:
        todo.append("close the gap to the new #1 — competitors out-updated us; widen the keyword family")
    if (a.get("referring_domains") or 0) == 0:
        todo.append("no referring domains — pair the relaunch with a linkable-asset hook + re-promotion")
    if a.get("first_touch", 0) >= 150 and a.get("paid", 0) == 0:
        todo.append("high reach, 0 paid — sharpen business-value angle + on-page conversion path")
    if not todo:  # valuable + slipping but none of the specific signals fired
        todo.append("refresh data + visuals, re-verify searcher intent, bump published date, re-promote")
    return "; ".join(todo)


def relaunch_candidates(articles: list[dict], prior: dict[str, dict]) -> list[dict]:
    """Decayed-but-valuable pages → a concrete relaunch plan (Lesson 5 audit + Lesson 8).

    A candidate is an article that is `compound == "decaying"` OR rank-slipping vs the prior
    snapshot, AND still has value (traffic / links). Each row is an actionable work order:
    {slug, reason, best_rank, referring_domains, what_to_refresh}. Test/dev artifacts are excluded
    (those are DELETE, not relaunch). Pure-decay-with-no-value is excluded (also DELETE/REVIVE).
    """
    out: list[dict] = []
    for a in articles:
        slug = a["slug"]
        if "test" in slug or "ple-2990" in slug:
            continue
        decaying = a.get("compound") == "decaying"
        slipped, slip_reason = rank_worsened(a, prior.get(slug))
        if not (decaying or slipped) or not had_value(a):
            continue
        reasons = []
        if decaying:
            reasons.append("organic traffic decaying (Lesson 1: it's no longer compounding)")
        if slipped:
            reasons.append(slip_reason)
        out.append({
            "slug": slug,
            "reason": " · ".join(reasons),
            "best_rank": a.get("best_rank"),
            "referring_domains": a.get("referring_domains"),
            "what_to_refresh": what_to_refresh(a, slipped),
        })
    # worst rank-slips and decayers first: order by (slipped?, then best traffic at stake)
    out.sort(key=lambda r: (r["best_rank"] is None, r["best_rank"] or 999))
    return out


def find_cannibalization(articles: list[dict]) -> list[tuple[str, str, float]]:
    cores = {a["slug"]: core_tokens(a["slug"]) for a in articles}
    slugs = list(cores)
    pairs = []
    for i in range(len(slugs)):
        for j in range(i + 1, len(slugs)):
            s1, s2 = slugs[i], slugs[j]
            jac = jaccard(cores[s1], cores[s2])
            if jac >= 0.6 and cores[s1] & cores[s2]:
                pairs.append((s1, s2, round(jac, 2)))
    return sorted(pairs, key=lambda p: p[2], reverse=True)


def main() -> int:
    today = datetime.date.today()
    snap = latest_snapshot()
    prior = prior_snapshot()
    articles = snap.get("articles", [])
    ghosts = snap.get("ghosts", [])
    by_slug = {a["slug"]: a for a in articles}

    order = ["DELETE", "DEFEND", "RELAUNCH", "WATCH", "REVIVE", "LEAVE"]
    buckets: dict[str, list] = {k: [] for k in order}
    for a in articles:
        b, reason = bucket(a, today)
        buckets[b].append((a, reason))

    cannib = find_cannibalization(articles)
    relaunch_plan = relaunch_candidates(articles, prior)

    managed_cores = {a["slug"]: core_tokens(a["slug"]) for a in articles}
    ghost_actions = []
    for g in ghosts:
        gc = core_tokens(g["slug"])
        best_slug, best_jac = None, 0.0
        for s, c in managed_cores.items():
            jac = jaccard(gc, c)
            if jac > best_jac:
                best_slug, best_jac = s, jac
        act = f"301 -> /blog/{best_slug}" if best_jac >= 0.5 else "re-adopt into managed set (no close managed equivalent)"
        ghost_actions.append((g, act))

    prior_note = "" if prior else "  _(no prior snapshot — rank-slip detection waits for run #2)_"
    L = [f"# Content audit — {today.isoformat()}  (from scorecard snapshot {snap.get('date')})\n"]
    L.append(f"{len(articles)} managed · {len(ghosts)} ghost URLs · "
             + " · ".join(f"{k}={len(v)}" for k, v in buckets.items())
             + f" · cannibalization-pairs={len(cannib)} · relaunch-candidates={len(relaunch_plan)}{prior_note}\n")

    L.append("## REQUIRES YOUR APPROVAL (destructive / outward-facing)\n")
    L.append("### Delete (prune dead weight)")
    L += [f"- `{a['slug']}` — {r}" for a, r in buckets["DELETE"]] or ["- none"]
    L.append("\n### Reclaim ghost URLs (driving real traffic, NOT in our system)")
    L += [f"- `/blog/{g['slug']}` — {g['first_touch']:,} first-touch, {g['paid']} paid → {act}" for g, act in ghost_actions] or ["- none"]
    L.append("\n### Merge — cannibalization candidates (301 the weaker into the stronger)")
    if cannib:
        for s1, s2, jac in cannib:
            a1, a2 = by_slug[s1], by_slug[s2]
            k1 = (a1["pv_organic_30d"], a1["first_touch"])
            k2 = (a2["pv_organic_30d"], a2["first_touch"])
            strong, weak = (s1, s2) if k1 >= k2 else (s2, s1)
            L.append(f"- `{weak}` → `{strong}`  (slug overlap {jac}) — keep the stronger, 301 the other")
    else:
        L.append("- none detected")

    L.append("\n## AUTONOMOUS-SAFE (EO can execute via update-pipeline)\n")
    L.append("### Relaunch plan — decayed / rank-slipping winners (Lesson 5 audit + Lesson 8)")
    L.append("> Was-valuable pages whose traffic is fading or whose rank slipped vs the last snapshot. "
             "Each is a work order: run `/relaunch` (refresh → bump date → re-promote as new). "
             "_Don't_ abandon these to drift to page 2.\n")
    if relaunch_plan:
        L.append("| Article | Best rank | RD | Why | What to refresh |")
        L.append("|---|--:|--:|---|---|")
        for c in relaunch_plan:
            rk = "—" if c["best_rank"] in (None, "") else c["best_rank"]
            rd = "—" if c["referring_domains"] is None else c["referring_domains"]
            L.append(f"| `{c['slug']}` | {rk} | {rd} | {c['reason']} | {c['what_to_refresh']} |")
    else:
        L.append("- none — no was-valuable page is decaying or rank-slipping this run "
                 "(needs ≥2 snapshots to spot rank slips)")
    L.append("\n### Relaunch — highest revenue leverage (high traffic, 0 paid)")
    L += [f"- `{a['slug']}` — {r}" for a, r in buckets["RELAUNCH"]] or ["- none"]
    L.append("\n### Defend (refresh to hold rank)")
    L += [f"- `{a['slug']}` — {r}" for a, r in buckets["DEFEND"]] or ["- none"]
    L.append("\n### Revive (fix intent / update)")
    L += [f"- `{a['slug']}` — {r}" for a, r in buckets["REVIVE"]] or ["- none"]

    L.append("\n## Watch (too new) / Leave (stable)\n")
    L.append("**Watch:** " + (", ".join(a["slug"] for a, _ in buckets["WATCH"]) or "none"))
    L.append("\n**Leave:** " + (", ".join(a["slug"] for a, _ in buckets["LEAVE"]) or "none"))

    OUT.mkdir(parents=True, exist_ok=True)
    body = "\n".join(L) + "\n"
    (OUT / f"audit-{today.isoformat()}.md").write_text(body, encoding="utf-8")
    (OUT / "latest.md").write_text(body, encoding="utf-8")

    print("audit:", " ".join(f"{k}={len(v)}" for k, v in buckets.items()),
          f"ghosts={len(ghosts)} cannib={len(cannib)} relaunch={len(relaunch_plan)}")
    print(f"wrote {(OUT / 'latest.md').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
