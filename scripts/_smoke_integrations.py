"""Smoke-test API auth for external integrations the blog-agent pipeline depends on.

Each test hits the cheapest read-only endpoint the provider exposes (typically
`/account`, `/key`, or `/me`) just to confirm the env-loaded key authenticates.
No content is generated, no quota is consumed beyond a single auth-validating
GET, and nothing is written to the project's content-pipeline directory.

Run via:
    doppler run -- python scripts/_smoke_integrations.py [--targets openrouter,replicate,browser_use,strapi]

Default targets exclude `strapi` because that hits a self-hosted CMS — pass
explicitly when you want to verify that one.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def _get(url: str, headers: dict[str, str], timeout: int = 15) -> dict:
    # Cloudflare-fronted APIs (Replicate, others) reject urllib's default UA.
    headers = {"User-Agent": "blog-agent-smoke/1.0", **headers}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def check_openrouter() -> str:
    key = os.environ.get("OPENROUTER_API_KEY_BLOG_AGENT") or os.environ.get("OPENROUTER_API_KEY")
    if not key:
        return "OPENROUTER FAIL — no key in env"
    try:
        data = _get("https://openrouter.ai/api/v1/key", {"Authorization": f"Bearer {key}"})
        d = data.get("data", {})
        return (
            f"OPENROUTER OK — label={d.get('label', '?')} "
            f"limit_remaining={d.get('limit_remaining')} "
            f"usage={d.get('usage')} "
            f"is_free_tier={d.get('is_free_tier')}"
        )
    except urllib.error.HTTPError as e:
        return f"OPENROUTER FAIL — HTTP {e.code} {e.reason}: {e.read().decode('utf-8', errors='replace')[:200]}"
    except Exception as e:
        return f"OPENROUTER FAIL — {type(e).__name__}: {e}"


def check_replicate() -> str:
    key = os.environ.get("REPLICATE_API_TOKEN") or os.environ.get("REPLICATE_API_KEY")
    if not key:
        return "REPLICATE FAIL — no key in env"
    try:
        data = _get("https://api.replicate.com/v1/account", {"Authorization": f"Bearer {key}"})
        return (
            f"REPLICATE OK — type={data.get('type')} "
            f"username={data.get('username')} "
            f"name={data.get('name')}"
        )
    except urllib.error.HTTPError as e:
        return f"REPLICATE FAIL — HTTP {e.code} {e.reason}: {e.read().decode('utf-8', errors='replace')[:200]}"
    except Exception as e:
        return f"REPLICATE FAIL — {type(e).__name__}: {e}"


def check_browser_use() -> str:
    key = os.environ.get("BROWSER_USE_API_KEY")
    if not key:
        return "BROWSER_USE FAIL — no key in env"
    enabled = os.environ.get("BROWSER_USE_ENABLED", "").lower() in {"1", "true", "yes"}
    # Try the documented Browser Use Cloud API balance endpoint; fall back to
    # tasks list. Both are read-only and validate auth without spending credits.
    for url in (
        "https://api.browser-use.com/api/v1/balance",
        "https://api.browser-use.com/api/v1/tasks?limit=1",
    ):
        try:
            data = _get(url, {"Authorization": f"Bearer {key}"})
            note = "" if enabled else " (note: BROWSER_USE_ENABLED is off — pipeline skips this integration by default)"
            return f"BROWSER_USE OK — endpoint={url.rsplit('/', 1)[-1]} keys={list(data.keys())[:6]}{note}"
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code} {e.reason}"
            continue
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
            continue
    return f"BROWSER_USE FAIL — last error: {last}"


def check_strapi() -> str:
    base = os.environ.get("STRAPI_BASE_URL")
    tok = os.environ.get("STRAPI_API_TOKEN")
    if not (base and tok):
        return "STRAPI FAIL — STRAPI_BASE_URL or STRAPI_API_TOKEN not in env"
    base = base.rstrip("/")
    try:
        data = _get(
            f"{base}/api/articles?pagination[limit]=1",
            {"Authorization": f"Bearer {tok}"},
        )
        total = data.get("meta", {}).get("pagination", {}).get("total")
        return f"STRAPI OK — base={base} total_articles={total}"
    except urllib.error.HTTPError as e:
        return f"STRAPI FAIL — HTTP {e.code} {e.reason}"
    except Exception as e:
        return f"STRAPI FAIL — {type(e).__name__}: {e}"


def check_github() -> str:
    key = os.environ.get("GITHUB_TOKEN")
    if not key:
        return "GITHUB FAIL — no token in env"
    try:
        data = _get(
            "https://api.github.com/user",
            {"Authorization": f"token {key}", "Accept": "application/vnd.github+json"},
        )
        return f"GITHUB OK — login={data.get('login')} type={data.get('type')}"
    except urllib.error.HTTPError as e:
        return f"GITHUB FAIL — HTTP {e.code} {e.reason}"
    except Exception as e:
        return f"GITHUB FAIL — {type(e).__name__}: {e}"


def check_strapi_v5_payload_shape() -> str:
    """Assert format_for_strapi.build_payload emits a Strapi v5 payload.

    No network. Validates the schema invariants that PLEAA-457 fixed:
      - Top-level data fields: title, slug, description, blocks, publishedAt
      - description is ≤80 chars
      - blocks[] non-empty with __component='shared.rich-text' and body markdown
      - legacy v4 fields (excerpt / content / seo / categories[]) are absent
      - category, when supplied, is a STRING (documentId), not an array
    """
    try:
        # Import lazily so the rest of the smoke checks run even if the script
        # path moves or has a syntax error in a feature branch.
        import importlib.util
        from pathlib import Path

        repo_root = Path(__file__).resolve().parents[1]
        target = (
            repo_root
            / ".claude"
            / "skills"
            / "format-for-publish"
            / "scripts"
            / "format_for_strapi.py"
        )
        spec = importlib.util.spec_from_file_location("format_for_strapi", target)
        if spec is None or spec.loader is None:
            return f"STRAPI_V5_SHAPE FAIL — cannot load {target}"
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        body = (
            "Intro line one introducing the topic at length so the description "
            "extractor has more than eighty characters of usable prose to work "
            "from before it gets truncated.\n\n## A heading\n\nMore body.\n"
        )
        payload = mod.build_payload(
            "smoke-slug",
            "Smoke Title",
            body,
            published_at=None,
        )
        d = payload.get("data") if isinstance(payload, dict) else None
        if not isinstance(d, dict):
            return "STRAPI_V5_SHAPE FAIL — payload missing top-level data"

        problems: list[str] = []
        # Required v5 fields (verified by live POST/DELETE 2026-05-07).
        for required in (
            "title",
            "slug",
            "description",
            "blocks",
            "publishedAt",
        ):
            if required not in d:
                problems.append(f"missing {required}")

        desc = d.get("description")
        if not isinstance(desc, str) or len(desc) > 80:
            problems.append(f"description shape (got len={len(desc) if isinstance(desc, str) else 'n/a'}, cap=80)")

        blocks = d.get("blocks")
        if not isinstance(blocks, list) or not blocks:
            problems.append("blocks must be non-empty list")
        else:
            first = blocks[0]
            if not isinstance(first, dict):
                problems.append("blocks[0] not an object")
            else:
                if first.get("__component") != "shared.rich-text":
                    problems.append(f"blocks[0].__component={first.get('__component')!r} (want shared.rich-text)")
                if not isinstance(first.get("body"), str) or not first["body"].strip():
                    problems.append("blocks[0].body must be non-empty string")

        # Strict-mode rejections — Strapi v5 returns HTTP 400 "Invalid key
        # <name>" for any of these. Catching them here prevents the silent
        # publish-failure regression PLEAA-457 was opened to close.
        forbidden = (
            "excerpt", "content", "seo", "categories",  # v4 legacy
            "author_name", "read_time", "readTime",     # not in current v5 schema
            "cover_image_url", "coverImage", "tags",
        )
        for f in forbidden:
            if f in d:
                problems.append(f"forbidden field {f!r} would be rejected by Strapi v5")

        if "category" in d and not isinstance(d["category"], str):
            problems.append(f"category must be documentId string, got {type(d['category']).__name__}")

        if problems:
            return "STRAPI_V5_SHAPE FAIL — " + "; ".join(problems)
        return (
            f"STRAPI_V5_SHAPE OK — fields="
            f"{sorted(d.keys())} description_len={len(d['description'])} blocks={len(d['blocks'])}"
        )
    except Exception as e:
        return f"STRAPI_V5_SHAPE FAIL — {type(e).__name__}: {e}"


CHECKS = {
    "openrouter": check_openrouter,
    "replicate": check_replicate,
    "browser_use": check_browser_use,
    "strapi": check_strapi,
    "strapi_v5_shape": check_strapi_v5_payload_shape,
    "github": check_github,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--targets",
        default="openrouter,replicate,browser_use,github,strapi_v5_shape",
        help="comma-separated list of integrations to test (default excludes strapi network check)",
    )
    args = parser.parse_args()

    targets = [t.strip() for t in args.targets.split(",") if t.strip()]
    unknown = [t for t in targets if t not in CHECKS]
    if unknown:
        print(f"Unknown targets: {unknown}. Valid: {list(CHECKS)}", file=sys.stderr)
        return 2

    fail_count = 0
    for name in targets:
        result = CHECKS[name]()
        print(result)
        if "FAIL" in result:
            fail_count += 1

    print(f"\n{'-' * 60}")
    print(f"PASS: {len(targets) - fail_count} / {len(targets)}")
    return 1 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())
