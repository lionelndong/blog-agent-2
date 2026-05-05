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


CHECKS = {
    "openrouter": check_openrouter,
    "replicate": check_replicate,
    "browser_use": check_browser_use,
    "strapi": check_strapi,
    "github": check_github,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--targets",
        default="openrouter,replicate,browser_use,github",
        help="comma-separated list of integrations to test (default excludes strapi)",
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
