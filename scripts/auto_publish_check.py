#!/usr/bin/env python3
"""Verify a freshly auto-published Strapi article is actually live.

After format_for_strapi.py --auto-publish reports success, hit the public Strapi URL
for the slug and assert the page renders with the expected H1. If anything's wrong,
write the slug to content-pipeline/9-needs-review/<slug>.md and exit non-zero.

Reads STRAPI_BASE_URL from env (Doppler).

Exit codes:
    0   Published page reachable, H1 matches expected title.
    1   404 / unreachable / wrong content (slug quarantined).
    2   STRAPI_BASE_URL missing.

Usage:
    python scripts/auto_publish_check.py <slug>
    python scripts/auto_publish_check.py <slug> --expected-title "Foo Bar"
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLISH_DIR = ROOT / "content-pipeline" / "8-publish"
QUARANTINE_DIR = ROOT / "content-pipeline" / "9-needs-review"
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")


def expected_title_from_payload(slug: str) -> str | None:
    payload_path = PUBLISH_DIR / slug / "article.json"
    if not payload_path.exists():
        return None
    try:
        data = json.loads(payload_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    title = data.get("data", {}).get("title")
    return str(title).strip() if title else None


def quarantine(slug: str, reason: str) -> None:
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    target = QUARANTINE_DIR / f"{slug}.md"
    body = (
        f"# Needs review — {slug}\n\n"
        f"- Quarantined at: {datetime.now(timezone.utc).isoformat()}\n"
        f"- Reason: {reason}\n\n"
        "Run /format-for-publish manually after diagnosing, then move this file out of 9-needs-review/.\n"
    )
    target.write_text(body, encoding="utf-8")


def fetch(url: str, timeout: int = 30) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "blog-agent-publish-check/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, ""
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return 0, str(exc)


def first_h1(html: str) -> str | None:
    m = H1_RE.search(html)
    if not m:
        return None
    text = TAG_RE.sub("", m.group(1))
    return re.sub(r"\s+", " ", text).strip() or None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    parser.add_argument("--expected-title", default=None)
    parser.add_argument("--blog-path", default="/blog", help="Path prefix on the public site (default /blog)")
    args = parser.parse_args()

    base = os.environ.get("STRAPI_BASE_URL") or os.environ.get("BLOG_PUBLIC_BASE_URL")
    if not base:
        print("error: STRAPI_BASE_URL (or BLOG_PUBLIC_BASE_URL) env var required", file=sys.stderr)
        sys.exit(2)

    expected = args.expected_title or expected_title_from_payload(args.slug)
    public_url = f"{base.rstrip('/')}{args.blog_path}/{args.slug}"

    status, body = fetch(public_url)
    if status != 200:
        reason = f"public URL {public_url} returned status={status}"
        quarantine(args.slug, reason)
        print(f"FAIL: {reason}", file=sys.stderr)
        sys.exit(1)

    h1 = first_h1(body)
    if expected and h1 and expected.lower() not in h1.lower() and h1.lower() not in expected.lower():
        reason = f"H1 mismatch at {public_url}: expected ~{expected!r}, got {h1!r}"
        quarantine(args.slug, reason)
        print(f"FAIL: {reason}", file=sys.stderr)
        sys.exit(1)

    print(f"OK: {public_url} — H1={h1!r}")


if __name__ == "__main__":
    main()
