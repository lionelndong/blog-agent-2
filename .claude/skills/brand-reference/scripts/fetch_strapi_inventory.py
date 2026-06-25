#!/usr/bin/env python3
"""Fetch the brand's published article inventory from Strapi.

Two modes — pick based on corpus size:

    Full-inventory mode (default) — fits up to ~5K articles cleanly.
        Writes a flat JSON cache at content-pipeline/brand-articles.json so
        /brand-reference and /verify-claims can discover existing articles
        without crawling the public site (which Cloudflare blocks).

    Query mode (--query "term1,term2") — for ~5K-50K+ corpora.
        Asks Strapi to return only articles whose title/excerpt/content matches
        any of the comma-separated terms. Returns JSON on stdout. No cache write.
        Use this once the full inventory grows past ~5K articles — at that scale
        the calling skill should ask Strapi per-draft instead of loading the whole
        corpus into context.

Usage:
    # Full inventory (small corpora)
    doppler run -- python .claude/skills/brand-reference/scripts/fetch_strapi_inventory.py
    doppler run -- python .claude/skills/brand-reference/scripts/fetch_strapi_inventory.py --refresh

    # Per-draft search (large corpora)
    doppler run -- python .claude/skills/brand-reference/scripts/fetch_strapi_inventory.py \\
        --query "ai girlfriend,virtual companion,nsfw chat" --limit 30

Required env (Doppler-supplied, same names as format_for_strapi.py):
    STRAPI_BASE_URL    e.g. https://api.pleasur.ai
    STRAPI_API_TOKEN   read-only token is enough

Optional env:
    STRAPI_ARTICLES_ENDPOINT  override path (default: /api/articles)
    STRAPI_BLOG_URL_BASE      public URL prefix used for {slug} links
                              (default: derived from brand-config.md "Blog URL")
    STRAPI_SEARCH_FIELDS      comma-separated fields query mode searches
                              (default: title,excerpt,content)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
CACHE_PATH = ROOT / "content-pipeline" / "brand-articles.json"
BRAND_CONFIG_PATH = ROOT / "brand-config.md"
DEFAULT_TTL_DAYS = 7
PAGE_SIZE = 100
QUERY_DEFAULT_LIMIT = 30
QUERY_DEFAULT_FIELDS = ("title", "excerpt", "content")
SCALE_WARNING_THRESHOLD = 5_000


@dataclass(frozen=True)
class Article:
    slug: str
    url: str
    title: str
    excerpt: str
    publishedAt: str | None
    h2s: list[str] = field(default_factory=list)


def read_brand_blog_url() -> str:
    """Pull the canonical 'Blog URL' line out of brand-config.md."""
    if not BRAND_CONFIG_PATH.exists():
        return ""
    text = BRAND_CONFIG_PATH.read_text(encoding="utf-8")
    m = re.search(r"-\s*\*\*Blog URL:\*\*\s*(\S+)", text)
    return m.group(1).rstrip("/") if m else ""


def cache_is_fresh(ttl_days: int) -> bool:
    if not CACHE_PATH.exists():
        return False
    try:
        payload = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        fetched = datetime.fromisoformat(payload["fetched_at"])
    except (json.JSONDecodeError, KeyError, ValueError):
        return False
    age = datetime.now(timezone.utc) - fetched
    return age.total_seconds() < ttl_days * 86400


def http_get_json(url: str, token: str) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        sys.exit(f"error: Strapi returned HTTP {e.code} for {url}\n{e.read().decode('utf-8', errors='replace')[:500]}")
    except urllib.error.URLError as e:
        sys.exit(f"error: could not reach Strapi at {url}: {e.reason}")
    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        sys.exit(f"error: Strapi response was not JSON: {e}")


def extract_field(item: dict[str, Any], key: str) -> Any:
    """Strapi v4 nests fields under `attributes`; v5 flattens. Handle both."""
    if "attributes" in item and isinstance(item["attributes"], dict) and key in item["attributes"]:
        return item["attributes"][key]
    return item.get(key)


def extract_h2s(content: Any) -> list[str]:
    """Pull H2 headings from markdown, HTML, or Strapi blocks-editor JSON."""
    if not content:
        return []
    if isinstance(content, str):
        md = re.findall(r"^##\s+(.+?)\s*$", content, re.MULTILINE)
        if md:
            return [h.strip() for h in md]
        html = re.findall(r"<h2[^>]*>(.+?)</h2>", content, re.IGNORECASE | re.DOTALL)
        return [re.sub(r"<[^>]+>", "", h).strip() for h in html]
    if isinstance(content, list):
        out: list[str] = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "heading" and block.get("level") == 2:
                children = block.get("children", [])
                text = "".join(c.get("text", "") for c in children if isinstance(c, dict))
                if text.strip():
                    out.append(text.strip())
        return out
    return []


def normalise_article(item: dict[str, Any], blog_url_base: str) -> Article | None:
    slug = extract_field(item, "slug")
    title = extract_field(item, "title")
    if not slug or not title:
        return None
    excerpt = extract_field(item, "excerpt") or ""
    published_at = extract_field(item, "publishedAt")
    content = extract_field(item, "content")
    h2s = extract_h2s(content)
    url = f"{blog_url_base}/{slug}" if blog_url_base else slug
    return Article(
        slug=str(slug),
        url=url,
        title=str(title).strip(),
        excerpt=str(excerpt).strip(),
        publishedAt=str(published_at) if published_at else None,
        h2s=h2s,
    )


def build_query_params(extra_filters: list[tuple[str, str]] | None = None) -> list[tuple[str, str]]:
    """Base Strapi query params shared by full and query modes."""
    params: list[tuple[str, str]] = [
        ("populate", "*"),
        ("pagination[pageSize]", str(PAGE_SIZE)),
        ("filters[publishedAt][$notNull]", "true"),
        ("sort", "publishedAt:desc"),
    ]
    if extra_filters:
        params.extend(extra_filters)
    return params


def search_filter_params(terms: list[str], fields: tuple[str, ...]) -> list[tuple[str, str]]:
    """Build Strapi $or filter across (fields × terms) using $containsi (case-insensitive)."""
    out: list[tuple[str, str]] = []
    idx = 0
    for term in terms:
        for field in fields:
            out.append((f"filters[$or][{idx}][{field}][$containsi]", term))
            idx += 1
    return out


def fetch_query_articles(
    base_url: str,
    endpoint: str,
    token: str,
    blog_url_base: str,
    terms: list[str],
    fields: tuple[str, ...],
    limit: int,
) -> list[Article]:
    """Strapi-side keyword search. Used at scale instead of full inventory."""
    articles: list[Article] = []
    page = 1
    extra = search_filter_params(terms, fields)
    while len(articles) < limit:
        page_params = build_query_params(extra) + [("pagination[page]", str(page))]
        url = f"{base_url.rstrip('/')}{endpoint}?{urllib.parse.urlencode(page_params)}"
        payload = http_get_json(url, token)
        items = payload.get("data") or []
        if not items:
            break
        for item in items:
            article = normalise_article(item, blog_url_base)
            if article:
                articles.append(article)
                if len(articles) >= limit:
                    break
        meta = payload.get("meta", {}).get("pagination", {})
        page_count = meta.get("pageCount")
        if page_count is None or page >= page_count:
            break
        page += 1
    return articles[:limit]


def fetch_all_articles(base_url: str, endpoint: str, token: str, blog_url_base: str) -> list[Article]:
    """Page through Strapi until exhausted."""
    articles: list[Article] = []
    page = 1
    while True:
        page_params = build_query_params() + [("pagination[page]", str(page))]
        url = f"{base_url.rstrip('/')}{endpoint}?{urllib.parse.urlencode(page_params)}"
        payload = http_get_json(url, token)
        items = payload.get("data") or []
        for item in items:
            article = normalise_article(item, blog_url_base)
            if article:
                articles.append(article)
        meta = payload.get("meta", {}).get("pagination", {})
        page_count = meta.get("pageCount")
        if not items or page_count is None or page >= page_count:
            break
        page += 1
    return articles


def write_cache(base_url: str, blog_url_base: str, articles: list[Article]) -> None:
    payload = {
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "strapi",
        "base_url": base_url,
        "blog_url_base": blog_url_base,
        "count": len(articles),
        "articles": [asdict(a) for a in articles],
    }
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_search_fields() -> tuple[str, ...]:
    raw = os.environ.get("STRAPI_SEARCH_FIELDS")
    if not raw:
        return QUERY_DEFAULT_FIELDS
    fields = tuple(f.strip() for f in raw.split(",") if f.strip())
    return fields or QUERY_DEFAULT_FIELDS


def require_strapi_env() -> tuple[str, str, str, str]:
    base_url = os.environ.get("STRAPI_BASE_URL")
    token = os.environ.get("STRAPI_API_TOKEN")
    if not base_url or not token:
        sys.exit(
            "error: STRAPI_BASE_URL and STRAPI_API_TOKEN env vars required\n"
            "       wrap the command in `doppler run -- python ...` (same pattern as format_for_strapi.py)"
        )
    endpoint = os.environ.get("STRAPI_ARTICLES_ENDPOINT", "/api/articles")
    blog_url_base = os.environ.get("STRAPI_BLOG_URL_BASE") or read_brand_blog_url()
    return base_url, token, endpoint, blog_url_base


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--refresh", action="store_true", help="Bypass TTL and fetch even if cache is fresh (full mode only)")
    parser.add_argument("--ttl-days", type=int, default=DEFAULT_TTL_DAYS, help=f"Cache TTL in days (default: {DEFAULT_TTL_DAYS})")
    parser.add_argument(
        "--query",
        default=None,
        help='Comma-separated search terms; switches to per-keyword mode (no cache, JSON to stdout). Use at scale (~5K+ articles).',
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=QUERY_DEFAULT_LIMIT,
        help=f"Max articles returned in --query mode (default: {QUERY_DEFAULT_LIMIT})",
    )
    args = parser.parse_args()

    if args.query is not None:
        if args.refresh:
            sys.exit("error: --query and --refresh are mutually exclusive (query mode does not use the cache)")
        terms = [t.strip() for t in args.query.split(",") if t.strip()]
        if not terms:
            sys.exit("error: --query must contain at least one non-empty term")
        base_url, token, endpoint, blog_url_base = require_strapi_env()
        if not blog_url_base:
            sys.stderr.write("warning: no blog URL base derivable; result URLs will be slugs only\n")
        fields = parse_search_fields()
        articles = fetch_query_articles(base_url, endpoint, token, blog_url_base, terms, fields, args.limit)
        result = {
            "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "source": "strapi",
            "mode": "query",
            "terms": terms,
            "fields": list(fields),
            "limit": args.limit,
            "count": len(articles),
            "articles": [asdict(a) for a in articles],
        }
        sys.stdout.write(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        return

    if not args.refresh and cache_is_fresh(args.ttl_days):
        payload = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        sys.stdout.write(f"cache fresh ({payload['count']} articles, fetched {payload['fetched_at']}); pass --refresh to re-fetch\n")
        return

    base_url, token, endpoint, blog_url_base = require_strapi_env()
    if not blog_url_base:
        sys.stdout.write("warning: no blog URL base derivable; URLs in cache will be slugs only\n")

    articles = fetch_all_articles(base_url, endpoint, token, blog_url_base)
    write_cache(base_url, blog_url_base, articles)
    sys.stdout.write(f"wrote {CACHE_PATH.relative_to(ROOT)} ({len(articles)} articles)\n")
    if len(articles) >= SCALE_WARNING_THRESHOLD:
        sys.stdout.write(
            f"\nNOTE: corpus has {len(articles):,} articles — past ~{SCALE_WARNING_THRESHOLD:,} the full-cache mode\n"
            f"is wasteful. Switch /brand-reference and /verify-claims to invoke this script with\n"
            f"`--query \"<keyword>,<related-term>,...\"` per draft instead of reading the full cache.\n"
        )


if __name__ == "__main__":
    main()
