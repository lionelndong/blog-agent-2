#!/usr/bin/env python3
"""ContentShake AI optimization — SEO + Quality scoring against target keyword.

Reads SEMRUSH_API_KEY_CONTENTSHAKE (preferred sub-key) or
SEMRUSH_API_KEY_BLOG_AGENT (primary fallback) from env (load via Doppler).
Mirrors the shape of openrouter_research.py: argparse-driven, JSON-to-stdout,
retry/backoff on transient failures.

Usage:
    doppler run -- python .claude/skills/optimize-content/scripts/contentshake_optimize.py \\
        --slug ai-girlfriend --keyword "ai girlfriend" --action optimize

    # Lightweight self-check during drafting:
    doppler run -- python .claude/skills/optimize-content/scripts/contentshake_optimize.py \\
        --slug ai-girlfriend --keyword "ai girlfriend" --action score

Output: JSON to stdout. Stderr carries human-readable progress lines. Exit
code 75 on quota exhaustion (matches the orchestrator's retry convention).

Stable response envelope (consumed by the skill — keep it backwards-compatible):

    {
      "seo_score": float | null,            # 0-10, ContentShake SEO scale
      "quality_score": float | null,        # 0-10, ContentShake Quality scale
      "recommended_terms": [                # absent in --action score
        {"term": str, "frequency": int, "importance": str, "in_draft": bool},
        ...
      ],
      "missing_topics":     [{"topic": str, "reason": str}, ...],
      "readability":        {"grade_level": float|null, "flesch": float|null, "notes": str},
      "voice_signals":      {"tone": str, "issues": [str]},
      "competitor_topics_missing": [{"topic": str, "competitors_covering": [str]}, ...],
      "_meta": {"action": ..., "slug": ..., "keyword": ..., "draft_path": ..., ...}
    }
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DRAFT_DIRS = (
    ROOT / "content-pipeline" / "6-drafts-cited",
    ROOT / "content-pipeline" / "5-drafts",
)
BRAND_CONFIG = ROOT / "brand-config.md"

# Override at runtime via env if Semrush serves ContentShake under a different host.
DEFAULT_API_BASE = os.environ.get(
    "SEMRUSH_CONTENTSHAKE_API_BASE",
    "https://api.semrush.com/contentshake/v1",
).rstrip("/")
ENDPOINT_OPTIMIZE = "/articles/analyze"
ENDPOINT_SCORE = "/articles/score"

TIMEOUT_SECONDS = 90
MAX_RETRIES = 5
BACKOFF_BASE_SECONDS = 1.0
RETRY_STATUS_CODES = frozenset({500, 502, 503, 504})
QUOTA_EXIT_CODE = 75


def load_api_key() -> str:
    """Resolve the ContentShake API key, preferring the ContentShake sub-key.

    Raises KeyError when neither env var is set so the caller can fall back to
    a stub-report flow rather than crashing the pipeline.
    """
    key = os.environ.get("SEMRUSH_API_KEY_CONTENTSHAKE") or os.environ.get(
        "SEMRUSH_API_KEY_BLOG_AGENT"
    )
    if not key:
        raise KeyError(
            "neither SEMRUSH_API_KEY_CONTENTSHAKE nor SEMRUSH_API_KEY_BLOG_AGENT is set; "
            "load via `doppler run -- ...` or export the env var"
        )
    return key


def find_draft(slug: str) -> Path:
    """Locate the draft markdown, preferring the cited copy."""
    for directory in DRAFT_DIRS:
        candidate = directory / f"{slug}.md"
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"no draft found for slug '{slug}' under "
        f"{DRAFT_DIRS[0].relative_to(ROOT)} or {DRAFT_DIRS[1].relative_to(ROOT)}"
    )


def read_brand_summary() -> str:
    """Pull the brand+voice+target-reader block so ContentShake gets audience context."""
    if not BRAND_CONFIG.exists():
        return "(no brand-config.md found)"
    text = BRAND_CONFIG.read_text(encoding="utf-8")
    cutoff = text.find("## Forbidden phrases")
    return text[:cutoff].strip() if cutoff > 0 else text[:3000]


def build_payload(action: str, keyword: str, content: str, brand_summary: str) -> dict:
    """Build the ContentShake request body.

    Field names follow the documented Semrush convention; if the live endpoint
    expects different keys, change them in this one place — the rest of the
    script is endpoint-agnostic.
    """
    return {
        "target_keyword": keyword,
        "content": content,
        "language": "en",
        "country": "us",
        "audience_brief": brand_summary,
        "include_competitor_terms": True,
        "include_readability": True,
        "include_voice_signals": True,
        "mode": "score" if action == "score" else "optimize",
    }


def call_contentshake(endpoint: str, payload: dict, api_key: str) -> dict:
    """POST with retry/backoff on 429 and 5xx; exit 75 on terminal quota.

    Returns the parsed JSON body on success. Raises RuntimeError on
    non-retryable HTTP errors and PermissionError on 401.
    """
    url = f"{DEFAULT_API_BASE}{endpoint}"
    body_bytes = json.dumps(payload).encode("utf-8")
    last_status: int | None = None

    for attempt in range(MAX_RETRIES):
        req = urllib.request.Request(
            url,
            data=body_bytes,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "blog-agent-contentshake/1.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last_status = exc.code
            if exc.code == 401:
                raise PermissionError(
                    f"ContentShake API returned 401 — key invalid or scope missing: {exc.reason}"
                ) from exc
            if exc.code == 429:
                if attempt == MAX_RETRIES - 1:
                    print(
                        f"contentshake: quota exhausted (429); exit {QUOTA_EXIT_CODE} for orchestrator retry",
                        file=sys.stderr,
                    )
                    sys.exit(QUOTA_EXIT_CODE)
                sleep = BACKOFF_BASE_SECONDS * (2 ** attempt)
                print(
                    f"contentshake: 429 on attempt {attempt + 1}/{MAX_RETRIES} — backing off {sleep:.1f}s",
                    file=sys.stderr,
                )
                time.sleep(sleep)
                continue
            if exc.code not in RETRY_STATUS_CODES:
                err_body = ""
                try:
                    err_body = exc.read().decode("utf-8")[:500]
                except Exception:
                    pass
                raise RuntimeError(
                    f"ContentShake API HTTP {exc.code} {exc.reason}: {err_body}"
                ) from exc
            sleep = BACKOFF_BASE_SECONDS * (2 ** attempt)
            print(
                f"contentshake: HTTP {exc.code} on attempt {attempt + 1}/{MAX_RETRIES} — backing off {sleep:.1f}s",
                file=sys.stderr,
            )
            time.sleep(sleep)
        except (urllib.error.URLError, TimeoutError) as exc:
            sleep = BACKOFF_BASE_SECONDS * (2 ** attempt)
            print(
                f"contentshake: network error on attempt {attempt + 1}/{MAX_RETRIES}: {exc}; "
                f"backing off {sleep:.1f}s",
                file=sys.stderr,
            )
            time.sleep(sleep)

    raise RuntimeError(
        f"ContentShake API exhausted {MAX_RETRIES} retries (last status: {last_status})"
    )


def _to_float(value: object) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _normalize_terms(items: list) -> list[dict]:
    normalized: list[dict] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "term": str(item.get("term") or item.get("keyword") or "").strip(),
                "frequency": int(item.get("frequency") or item.get("recommended_count") or 0),
                "importance": str(item.get("importance") or item.get("priority") or "medium"),
                "in_draft": bool(item.get("in_draft", False)),
            }
        )
    return normalized


def _normalize_topics(items: list) -> list[dict]:
    normalized: list[dict] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "topic": str(item.get("topic") or item.get("title") or "").strip(),
                "reason": str(item.get("reason") or item.get("rationale") or "").strip(),
            }
        )
    return normalized


def _normalize_readability(rd: dict) -> dict:
    return {
        "grade_level": _to_float(rd.get("grade_level") or rd.get("grade")),
        "flesch": _to_float(rd.get("flesch") or rd.get("flesch_reading_ease")),
        "notes": str(rd.get("notes") or "").strip(),
    }


def _normalize_voice(voice: dict) -> dict:
    issues = voice.get("issues") or []
    return {
        "tone": str(voice.get("tone") or voice.get("dominant_tone") or "").strip(),
        "issues": [str(i) for i in issues if i],
    }


def _normalize_competitor_topics(items: list) -> list[dict]:
    normalized: list[dict] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        covering = item.get("competitors_covering") or item.get("sources") or []
        normalized.append(
            {
                "topic": str(item.get("topic") or item.get("title") or "").strip(),
                "competitors_covering": [str(c) for c in covering if c],
            }
        )
    return normalized


def normalize_response(action: str, raw: dict) -> dict:
    """Map raw ContentShake response into the stable shape skills depend on.

    Tolerates common naming variants between API versions; returns null for
    missing fields rather than fabricating values.
    """
    scores = raw.get("scores") or {}
    seo_score = _to_float(
        scores.get("seo") or scores.get("seo_score") or raw.get("seo_score")
    )
    quality_score = _to_float(
        scores.get("quality") or scores.get("quality_score") or raw.get("quality_score")
    )

    result: dict = {
        "seo_score": seo_score,
        "quality_score": quality_score,
        "_meta": {
            "action": action,
            "endpoint_base": DEFAULT_API_BASE,
            "raw_keys": sorted(raw.keys()),
        },
    }

    if action == "score":
        return result

    result.update(
        {
            "recommended_terms": _normalize_terms(
                raw.get("recommended_terms") or raw.get("terms") or []
            ),
            "missing_topics": _normalize_topics(
                raw.get("missing_topics") or raw.get("topics_to_add") or []
            ),
            "readability": _normalize_readability(raw.get("readability") or {}),
            "voice_signals": _normalize_voice(raw.get("voice_signals") or raw.get("voice") or {}),
            "competitor_topics_missing": _normalize_competitor_topics(
                raw.get("competitor_topics_missing") or raw.get("competitor_topics") or []
            ),
        }
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", required=True, help="filesystem-safe slug for the draft")
    parser.add_argument("--keyword", required=True, help="target keyword the article ranks for")
    parser.add_argument(
        "--action",
        choices=("optimize", "score"),
        default="optimize",
        help="optimize = full analysis with recommendations; score = lightweight scoreback",
    )
    args = parser.parse_args()

    try:
        api_key = load_api_key()
    except KeyError as exc:
        sys.exit(f"error: {exc}")

    try:
        draft_path = find_draft(args.slug)
    except FileNotFoundError as exc:
        sys.exit(f"error: {exc}")

    content = draft_path.read_text(encoding="utf-8")
    brand_summary = read_brand_summary()
    payload = build_payload(args.action, args.keyword, content, brand_summary)
    endpoint = ENDPOINT_SCORE if args.action == "score" else ENDPOINT_OPTIMIZE

    print(
        f"contentshake: action={args.action} slug={args.slug} draft={draft_path.name} "
        f"({len(content)} chars) endpoint={endpoint}",
        file=sys.stderr,
    )

    t0 = time.time()
    try:
        raw = call_contentshake(endpoint, payload, api_key)
    except PermissionError as exc:
        sys.exit(f"error: {exc}")
    except RuntimeError as exc:
        sys.exit(f"error: {exc}")
    elapsed = time.time() - t0

    result = normalize_response(args.action, raw)
    result["_meta"].update(
        {
            "slug": args.slug,
            "keyword": args.keyword,
            "draft_path": str(draft_path),
            "draft_chars": len(content),
            "elapsed_seconds": round(elapsed, 2),
        }
    )

    print(
        f"contentshake: done in {elapsed:.1f}s — seo={result.get('seo_score')} "
        f"quality={result.get('quality_score')}",
        file=sys.stderr,
    )

    sys.stdout.write(json.dumps(result, indent=2))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
