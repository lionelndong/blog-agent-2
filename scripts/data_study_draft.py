#!/usr/bin/env python3
"""Data-study DRAFT scaffold (Phase P4 / Lesson 7 — LINKABLE ASSETS).

Turns a FEW SAFE aggregate product metrics into a DRAFT data-study outline + a data appendix that
the operator reviews and approves before anything is published. The course's Lesson 7: a young brand
can't get links *to its product*, so it builds linkable ASSETS — and the best asset a product company
owns is its OWN aggregate data ("X% of users do Y"). That data is brand-safe (no individual is named),
quotable (the headline stat is the link magnet), and — via internal links DOWN to our money clusters —
it routes the new Domain Rating to the pages that convert. See `STRATEGY.md` Lesson 7 + the
`linkable-asset` skill (the playbook this scaffold serves).

TWO HARD RULES this script enforces in code:

  RULE 1 — AGGREGATE ONLY, NEVER PII.
    Every query is `count()` / `avg()` / a ratio over a POPULATION. The script never SELECTs a person
    field (no email / username / id / distinct_id / Stripe id / IP / free-text). A minimum-cohort
    floor (MIN_COHORT, default 100) drops any metric whose denominator is below the floor — a thin,
    unimpeachable study beats a rich one that re-identifies someone. Suppressed metrics are LISTED
    (count + reason), never silently dropped and never published.

  RULE 2 — DRAFT ONLY. NEVER PUBLISH.
    This scaffold writes local files and stops. It does NOT push to Strapi, call format-for-publish,
    open outreach, or set publishedAt. A data study is a public claim about our company → a human
    (the operator) approves first. The output includes APPROVAL.md stating exactly that.

Output (a DRAFT for operator review — NOT a publish package):
  content-pipeline/linkable-assets/<study-slug>/draft.md          (the study draft: stats + routing)
  content-pipeline/linkable-assets/<study-slug>/data-appendix.md  (the aggregate metrics + suppressed list)
  content-pipeline/linkable-assets/<study-slug>/APPROVAL.md        (the approval gate record)

Run:  doppler run -- python scripts/data_study_draft.py [cluster-id]
Env (Doppler):  POSTHOG_HOST, POSTHOG_PROJECT_ID, POSTHOG_PERSONAL_API_KEY
                (Stripe/finance figures are pulled as ALREADY-AGGREGATED context from the scorecard
                 snapshot when present — never raw customer rows.)
"""
from __future__ import annotations

import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

# --- config -----------------------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "content-pipeline" / "linkable-assets"
SCORECARD_SNAPS = ROOT / "content-pipeline" / "scorecard" / "snapshots"
CLUSTER_MAP = ROOT / "content-pipeline" / "0-keywords" / "cluster-map.md"
BRAND_DR = ROOT / "content-pipeline" / "0-keywords" / "cache" / "brand-dr.json"

# k-anonymity floor: any aggregate whose denominator (people in the cohort) is below this is dropped
# and listed as suppressed — never published. Widen the bucket instead of going below it. (RULE 1)
MIN_COHORT = int(os.environ.get("DATA_STUDY_MIN_COHORT", "100"))

# The data study is authored by the Analyst / data-benchmark persona (examples/authors.md).
BYLINE = "Sloane Avery"
PERSONA_SLUG = "sloane-avery"

# Real money clusters (clusters.md) → the product/money page each study routes link-juice DOWN to.
CLUSTER_PRODUCT_PAGE = {
    "companions": "/companions",
    "image-gen": "/image-generator",
    "chat-roleplay": "/chat",
    "voice-calls": "/voice",
    "tools-compare": "/compare",
}
DEFAULT_CLUSTER = "companions"

# Raw id / contact / device fields that must NEVER appear in a query — selecting any of these emits a
# value that identifies a person. A tripwire so the aggregate-only rule can't silently regress if
# someone edits a query later. (RULE 1)
# NOTE: `person_id` / `distinct_id` are deliberately NOT in this list — counting DISTINCT people with
# `uniq(person_id)` is aggregate and safe (it's how the scorecard counts people). They are policed
# separately below: allowed ONLY inside an aggregate function, never selected raw.
PII_TOKENS = (
    "email", "username", "ip", "phone", "address", "$ip", "device_id", "user_id",
    "cus_", "sub_", "ch_", "pi_",  # Stripe object id prefixes
)
# Person-key columns that are safe ONLY when wrapped in an aggregate (uniq/count/...). Selecting one
# raw would leak an identifier, so we require it to sit inside an aggregate call.
PERSON_KEYS = ("person_id", "distinct_id")
_AGG_FNS = ("uniq", "uniqexact", "count", "countif", "uniqif")


def _person_key_outside_aggregate(query: str) -> str | None:
    """Return a person-key that appears OUTSIDE an aggregate function, else None.

    `uniq(person_id)` / `count(person_id)` are aggregate (safe). A bare `SELECT person_id` is not.
    """
    low = query.lower()
    for key in PERSON_KEYS:
        for mt in re.finditer(re.escape(key), low):
            before = low[:mt.start()].rstrip()
            # safe iff immediately preceded by `<aggfn>(` (allowing whitespace before the paren)
            wrapped = before.endswith("(") and any(
                before[:-1].rstrip().endswith(fn) for fn in _AGG_FNS
            )
            if not wrapped:
                return key
    return None


def _env(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        sys.exit(f"error: {name} not set — run under `doppler run -- python scripts/data_study_draft.py`")
    return v


def _post_json(url: str, body: dict, headers: dict) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(),
        headers={**headers, "Content-Type": "application/json"}, method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def _assert_aggregate_only(query: str) -> None:
    """Tripwire (RULE 1): refuse to run any query that could emit a person-level / id / PII value.

    Belt-and-suspenders on top of writing only count()/avg() queries — it makes a future edit that
    reaches for a raw field fail loudly instead of leaking. Allows `uniq(person_id)`-style aggregation
    (counting distinct people is safe); blocks raw id/contact/device fields and any person-key selected
    outside an aggregate.
    """
    low = query.lower()
    hit = next((t for t in PII_TOKENS if t in low), None)
    if hit is None:
        hit = _person_key_outside_aggregate(query)
    if hit:
        sys.exit(
            f"error: refusing to run a query referencing '{hit}' outside an aggregate — data studies "
            f"are AGGREGATE ONLY, never PII (STRATEGY.md Lesson 7 / linkable-asset RULE 1). "
            f"Query: {query[:160]}"
        )


def hogql(query: str) -> list:
    """Run an AGGREGATE HogQL query against PostHog. Aggregate-only is asserted before the call."""
    _assert_aggregate_only(query)
    host = _env("POSTHOG_HOST").rstrip("/")
    pid = _env("POSTHOG_PROJECT_ID")
    key = _env("POSTHOG_PERSONAL_API_KEY")
    url = f"{host}/api/projects/{pid}/query/"
    try:
        j = _post_json(url, {"query": {"kind": "HogQLQuery", "query": query}}, {"Authorization": f"Bearer {key}"})
    except urllib.error.HTTPError as e:
        sys.exit(f"error: PostHog HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")
    return j.get("results", [])


def _scalar(rows: list, default: int = 0) -> int:
    """First cell of the first row as an int (aggregate queries return a single number)."""
    if rows and rows[0]:
        try:
            return int(rows[0][0] or 0)
        except (TypeError, ValueError):
            return default
    return default


# --- metric pulls (aggregate-only; each returns a numerator/denominator the floor can vet) ----------

def metric_active_people(days: int = 90) -> int:
    """Distinct people with any activity in the window — the population the study describes."""
    return _scalar(hogql(
        f"SELECT uniq(person_id) FROM events WHERE timestamp > now() - INTERVAL {days} DAY"
    ))


def metric_engagement_rate(action_event: str, base_event: str, days: int = 90) -> dict:
    """Share of people who did `base_event` that also did `action_event` — a benchmark stat.

    Returns aggregate counts only (numerator/denominator), so the floor can suppress thin cohorts.
    """
    denom = _scalar(hogql(
        f"SELECT uniq(person_id) FROM events WHERE event = '{base_event}' "
        f"AND timestamp > now() - INTERVAL {days} DAY"
    ))
    numer = _scalar(hogql(
        f"SELECT uniq(person_id) FROM events WHERE event = '{action_event}' "
        f"AND timestamp > now() - INTERVAL {days} DAY"
    ))
    return {"numerator": numer, "denominator": denom}


def metric_qoq_trend(event: str, days: int = 90) -> dict:
    """This-period vs prior-period event volume → a growth multiple (a 'Stories'/trend stat).

    Aggregate event counts only; the denominator for the floor is the prior-period volume.
    """
    this_p = _scalar(hogql(
        f"SELECT count() FROM events WHERE event = '{event}' AND timestamp > now() - INTERVAL {days} DAY"
    ))
    prior_p = _scalar(hogql(
        f"SELECT count() FROM events WHERE event = '{event}' "
        f"AND timestamp <= now() - INTERVAL {days} DAY AND timestamp > now() - INTERVAL {2 * days} DAY"
    ))
    return {"this_period": this_p, "prior_period": prior_p}


# --- floor + formatting -----------------------------------------------------------------------------

def vet_cohort(label: str, denominator: int) -> tuple[bool, str | None]:
    """RULE 1 k-anonymity floor: a metric is publishable only if its cohort ≥ MIN_COHORT."""
    if denominator < MIN_COHORT:
        return False, f"{label}: cohort {denominator} < floor {MIN_COHORT} — SUPPRESSED (re-identification risk)"
    return True, None


def pct(numer: int, denom: int) -> float:
    return round(numer / denom * 100, 1) if denom else 0.0


def study_slug(cluster: str, today: str) -> str:
    return f"{re.sub(r'[^a-z0-9-]', '-', cluster.lower())}-data-study-{today}"


# --- draft assembly ---------------------------------------------------------------------------------

def build_metrics(cluster: str) -> tuple[list[dict], list[str], int]:
    """Pull a FEW safe aggregate metrics. Returns (published_metrics, suppressed_notes, population).

    NOTE: the event names below are illustrative scaffold defaults (override per the live PostHog
    taxonomy). Each metric is vetted against the cohort floor before it can be published.
    """
    population = metric_active_people(90)
    published: list[dict] = []
    suppressed: list[str] = []

    # 1. Engagement benchmark (Numbers + Utility): share of signups who send a first message.
    eng = metric_engagement_rate("message_sent", "signup", 90)
    ok, note = vet_cohort("first-message engagement", eng["denominator"])
    if ok:
        published.append({
            "dimension": "Numbers + Utility (engagement benchmark)",
            "headline": f"{pct(eng['numerator'], eng['denominator'])}% of new users send a message in their first session",
            "value": f"{pct(eng['numerator'], eng['denominator'])}%",
            "basis": f"aggregate over {eng['denominator']:,} new users (90d)",
        })
    elif note:
        suppressed.append(note)

    # 2. Feature-adoption benchmark (Utility): share of active users who use voice replies.
    voice = metric_engagement_rate("voice_reply_used", "message_sent", 90)
    ok, note = vet_cohort("voice adoption", voice["denominator"])
    if ok:
        published.append({
            "dimension": "Utility (feature-adoption benchmark)",
            "headline": f"{pct(voice['numerator'], voice['denominator'])}% of chatting users have used voice replies",
            "value": f"{pct(voice['numerator'], voice['denominator'])}%",
            "basis": f"aggregate over {voice['denominator']:,} chatting users (90d)",
        })
    elif note:
        suppressed.append(note)

    # 3. Trend (Stories): quarter-over-quarter growth in image generations.
    trend = metric_qoq_trend("image_generated", 90)
    ok, note = vet_cohort("image-gen trend (prior period volume)", trend["prior_period"])
    if ok:
        mult = round(trend["this_period"] / trend["prior_period"], 1) if trend["prior_period"] else 0.0
        published.append({
            "dimension": "Stories (trend over time)",
            "headline": f"AI image generations grew {mult}x quarter-over-quarter",
            "value": f"{mult}x QoQ",
            "basis": f"aggregate event volume, this 90d vs prior 90d",
        })
    elif note:
        suppressed.append(note)

    return published, suppressed, population


def render_appendix(cluster: str, today: str, metrics: list[dict], suppressed: list[str], population: int) -> str:
    L = [f"# Data appendix — {cluster} data study ({today})\n",
         "_Operator sanity-check sheet. Every figure below is aggregate (count/rate/trend over a "
         "population). No individual user/customer data, no ids, no free-text. Verify each number "
         "against source before approving._\n",
         f"**Population described:** {population:,} active people (90d) — the denominator base.\n",
         f"**Minimum-cohort floor (k-anonymity):** {MIN_COHORT} (metrics below this are suppressed).\n",
         "\n## Published metrics (aggregate)\n",
         "| Metric | Value | Basis (aggregate) | Linkbait dimension |",
         "|---|---|---|---|"]
    for m in metrics:
        L.append(f"| {m['headline']} | {m['value']} | {m['basis']} | {m['dimension']} |")
    if not metrics:
        L.append("| _(none cleared the cohort floor — widen buckets / extend the window and re-run)_ | — | — | — |")
    L.append(f"\n## Suppressed (below floor — NOT published) — {len(suppressed)}\n")
    if suppressed:
        for s in suppressed:
            L.append(f"- {s}")
    else:
        L.append("- none")
    L.append(
        "\n## Methodology / privacy note (goes in the draft as `:::methodology`)\n"
        "- **Source:** Pleasur.AI first-party product analytics (PostHog) + aggregate billing rates.\n"
        f"- **Sample / window:** {population:,} active people, trailing 90 days as of {today}.\n"
        "- **Aggregation:** all figures are counts, rates, and trends computed over the whole "
        "population. **No individual user or customer data is used, shown, or derivable** — every "
        f"cohort is ≥ {MIN_COHORT} people. No emails, ids, locations finer than country, or message "
        "text were queried.\n"
    )
    return "\n".join(L) + "\n"


def render_draft(cluster: str, today: str, slug: str, metrics: list[dict], population: int) -> str:
    product_page = CLUSTER_PRODUCT_PAGE.get(cluster, "/")
    headline_stat = metrics[0]["headline"] if metrics else "our first-party usage benchmark"
    L = [f"<!-- byline: {BYLINE} | persona: {PERSONA_SLUG} -->",
         f"<!-- DRAFT data study (linkable asset). NOT a publish package. Operator approval required "
         f"before publish — see APPROVAL.md. Generated {today}. -->",
         "",
         f"# The State of {cluster.replace('-', ' ').title()}: What {population:,} Users' Behavior Reveals",
         "",
         "{lead}" + f"We looked at how people actually use Pleasur.AI — aggregate, anonymized, "
         f"{population:,} users over 90 days — and the numbers tell a clearer story than the hype. "
         f"Top line: {headline_stat}." + "{/lead}",
         "",
         "## Top-line findings (the quotable numbers)",
         ""]
    if metrics:
        L.append(":::stat-group")
        for m in metrics:
            L.append(f':::stat value="{m["value"]}" label="{m["headline"]}"')
        L.append(":::")
    else:
        L.append("_No metric cleared the cohort floor this run — extend the window or widen buckets, "
                 "then regenerate. (We never publish a below-floor stat — RULE 1.)_")
    L += [
        "",
        "## What it means",
        "",
        "_(Operator/author: interpret the trend here — the surprising / useful angle. Keep it honest: "
        "a debunked stat is a reputational and SEO loss.)_",
        "",
        "## Methodology",
        "",
        ":::methodology",
        "- **Source:** Pleasur.AI first-party product analytics (aggregate).",
        f"- **Sample:** {population:,} active users, trailing 90 days (as of {today}).",
        "- **Privacy:** all figures are aggregate counts/rates over the population. **No individual "
        f"user or customer data** — every cohort is ≥ {MIN_COHORT} users; no ids, emails, locations, "
        "or message text are used.",
        ":::",
        "",
        "## Explore the data (internal-link routing — Lesson 7: route the juice DOWN to money pages)",
        "",
        "_REQUIRED: descriptive anchors linking DOWN to the cluster keystone + money page + 2–4 "
        f"supporting articles, so the DR this study earns lifts the `{cluster}` cluster. Read "
        "`content-pipeline/0-keywords/cluster-map.md` for the live keystone slug; fill these in:_",
        f"- **Money/product page:** [the {cluster.replace('-', ' ')} product]({product_page})",
        f"- **Cluster keystone:** [keystone article](/blog/<{cluster}-keystone-slug>)  _(from cluster-map.md)_",
        "- **Supporting (2–4):** [supporting #1](/blog/<slug>), [supporting #2](/blog/<slug>) …",
        "",
    ]
    return "\n".join(L) + "\n"


def render_approval(cluster: str, today: str, slug: str, metrics: list[dict], suppressed: list[str]) -> str:
    return (
        f"# APPROVAL GATE — {cluster} data study ({today})\n\n"
        "**STATUS: DRAFT — NOT PUBLISHED. Operator approval REQUIRED before any publish.**\n\n"
        "This data study makes a public, quotable claim about Pleasur.AI under our brand. Per the "
        "`linkable-asset` skill RULE 2, it ships only after a human approves. This scaffold produced a "
        "draft and stopped — it did **not** push to Strapi, call format-for-publish, set publishedAt, "
        "or start outreach.\n\n"
        f"- Draft: `content-pipeline/linkable-assets/{slug}/draft.md`\n"
        f"- Data appendix: `content-pipeline/linkable-assets/{slug}/data-appendix.md`\n"
        f"- Published metrics: {len(metrics)} · Suppressed (below floor): {len(suppressed)}\n\n"
        "## Operator pre-publish checklist (tick ALL before approving)\n"
        "- [ ] **PII sweep:** no email/username/user-id/distinct_id/Stripe-id/IP/device, no free-text, "
        "no single-person anecdote, nothing finer than country / coarse date.\n"
        f"- [ ] **Cohort floor:** every published figure's cohort ≥ {MIN_COHORT}; suppressed list reviewed.\n"
        "- [ ] **Numbers verified** against source (each stat re-checked; nothing inflated/cherry-picked).\n"
        "- [ ] **Internal-link routing filled in** — keystone + money/product page + 2–4 supporting "
        "(Lesson 7: the juice flows DOWN to the cluster).\n"
        "- [ ] **Byline** is Sloane Avery (data-benchmark persona).\n"
        "- [ ] **Brand-safe + on-brand** (Pleasur.AI named as the data source).\n\n"
        "## After approval (still human-driven)\n"
        "1. Run the normal formatter as a **Strapi DRAFT** (NO `--auto-publish`) for a final read.\n"
        "2. Operator clicks Publish in Strapi.\n"
        "3. Promotion / outreach is a **separate, approved** step (Lesson 8) — never automatic.\n"
    )


def main() -> int:
    cluster = (sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CLUSTER).strip().lower()
    if cluster not in CLUSTER_PRODUCT_PAGE:
        print(f"warning: '{cluster}' is not a known cluster {tuple(CLUSTER_PRODUCT_PAGE)} — "
              f"defaulting routing to '/'. (clusters.md is the source of truth.)", file=sys.stderr)
    today = datetime.date.today().isoformat()
    slug = study_slug(cluster, today)

    metrics, suppressed, population = build_metrics(cluster)

    out = OUT_DIR / slug
    out.mkdir(parents=True, exist_ok=True)
    (out / "draft.md").write_text(render_draft(cluster, today, slug, metrics, population), encoding="utf-8")
    (out / "data-appendix.md").write_text(
        render_appendix(cluster, today, metrics, suppressed, population), encoding="utf-8")
    (out / "APPROVAL.md").write_text(
        render_approval(cluster, today, slug, metrics, suppressed), encoding="utf-8")

    print(f"data-study DRAFT (cluster={cluster}): {len(metrics)} published metric(s), "
          f"{len(suppressed)} suppressed, population {population:,}")
    print(f"wrote {(out / 'draft.md').relative_to(ROOT)} + data-appendix.md + APPROVAL.md")
    print("NOT PUBLISHED — operator approval required (see APPROVAL.md). RULE 2.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
