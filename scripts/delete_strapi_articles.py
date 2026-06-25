#!/usr/bin/env python3
"""Delete Strapi articles listed in the triage CSV — with mandatory backups.

Two-step safety:
  1. Default behavior is DRY-RUN. Pass --commit to actually delete.
  2. Every article is backed up to disk BEFORE the DELETE HTTP call. Backup failure
     aborts the deletion for that article (we never delete what we couldn't save).

Usage:
    # Preview the first 5 deletes — no API DELETE calls, no backups written
    doppler run --project pleasurai --config dev -- python scripts/delete_strapi_articles.py \\
        --verdict DELETE --limit 5

    # Real delete + backup, first 5 articles only
    doppler run --project pleasurai --config dev -- python scripts/delete_strapi_articles.py \\
        --verdict DELETE --limit 5 --commit

    # Filter to specific slugs
    doppler run --project pleasurai --config dev -- python scripts/delete_strapi_articles.py \\
        --slugs slug-a,slug-b --commit

Required env (Doppler):
    STRAPI_BASE_URL
    STRAPI_API_TOKEN  (must have delete permission on the Article content type)

Outputs:
    content-pipeline/audit/deleted-backups/<slug>.json   per-article backup (full payload)
    content-pipeline/audit/deletion-log.csv              append-only log of every attempt
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRIAGE_CSV = ROOT / "content-pipeline" / "audit" / "blog-triage.csv"
BACKUP_DIR = ROOT / "content-pipeline" / "audit" / "deleted-backups"
LOG_PATH = ROOT / "content-pipeline" / "audit" / "deletion-log.csv"

VALID_VERDICTS = {"DELETE", "CONSOLIDATE", "REVIEW"}
SLEEP_BETWEEN = 0.4  # seconds — gentle rate limit


def http_request(url: str, token: str, method: str = "GET", expect_codes: tuple[int, ...] = (200,)) -> tuple[int, dict[str, Any] | None]:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8") or "{}"
            return resp.status, json.loads(body) if body.strip() else None
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            pass
        return e.code, {"_error": body}
    except urllib.error.URLError as e:
        return 0, {"_error": str(e.reason)}


def fetch_article(base: str, token: str, slug: str) -> dict[str, Any] | None:
    """Lookup by slug; falls through to draft state if not found as published."""
    for status in (None, "draft"):
        params = {"filters[slug][$eq]": slug, "populate": "*"}
        if status:
            params["status"] = status
        url = f"{base.rstrip('/')}/api/articles?{urllib.parse.urlencode(params)}"
        code, payload = http_request(url, token, method="GET")
        if code != 200 or not payload:
            continue
        items = payload.get("data") or []
        if items:
            return items[0]
    return None


def delete_article(base: str, token: str, document_id: str) -> tuple[int, str]:
    url = f"{base.rstrip('/')}/api/articles/{document_id}"
    code, payload = http_request(url, token, method="DELETE")
    if payload and "_error" in payload:
        return code, payload["_error"]
    return code, ""


def load_already_deleted_document_ids() -> set[str]:
    """documentIds marked `action=deleted`. Keyed on documentId (not slug) so
    re-created articles with the same slug but a fresh documentId still get
    processed on subsequent runs.
    """
    if not LOG_PATH.exists():
        return set()
    out: set[str] = set()
    with LOG_PATH.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("action") == "deleted" and row.get("document_id"):
                out.add(row["document_id"])
    return out


def load_targets(verdict_filter: str | None, slug_filter: list[str] | None, limit: int | None) -> list[dict[str, str]]:
    """Direct-slug mode (slug_filter only) bypasses the triage CSV entirely.

    Used to delete articles that aren't in the CSV — drafts, late additions,
    etc. The audit trail still lands in deletion-log.csv via write_log().
    """
    rows: list[dict[str, str]] = []

    # Direct mode: no verdict filter and explicit slugs given. Build synthetic
    # rows so the rest of the pipeline (fetch + backup + delete + log) works
    # without needing a CSV entry per slug. The documentId-based skip happens
    # in main() after we've fetched the article from Strapi.
    if slug_filter and not verdict_filter:
        for slug in slug_filter:
            rows.append({"slug": slug, "verdict": "DIRECT", "publishedAt": ""})
            if limit and len(rows) >= limit:
                break
        return rows

    # Verdict-driven mode: read the triage CSV
    if not TRIAGE_CSV.exists():
        sys.exit(f"error: {TRIAGE_CSV} not found — run scripts/blog_triage.py first")
    with TRIAGE_CSV.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if verdict_filter and row["verdict"] != verdict_filter:
                continue
            if slug_filter and row["slug"] not in slug_filter:
                continue
            rows.append(row)
            if limit and len(rows) >= limit:
                break
    return rows


def write_log(entry: dict[str, str]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    new_file = not LOG_PATH.exists()
    with LOG_PATH.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow([
                "timestamp", "slug", "verdict", "document_id", "http_code",
                "action", "backup_path", "error",
            ])
        w.writerow([
            entry["timestamp"], entry["slug"], entry["verdict"],
            entry.get("document_id", ""), entry.get("http_code", ""),
            entry["action"], entry.get("backup_path", ""), entry.get("error", ""),
        ])


def backup_article(slug: str, payload: dict[str, Any]) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    out = BACKUP_DIR / f"{slug}.json"
    out.write_text(
        json.dumps({"backed_up_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "article": payload}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--verdict", choices=sorted(VALID_VERDICTS), help="Filter triage CSV to a single verdict bucket")
    parser.add_argument("--slugs", help="Comma-separated specific slugs to target (overrides --verdict if both)")
    parser.add_argument("--limit", type=int, help="Stop after N articles (useful for sanity-checking a small batch first)")
    parser.add_argument("--commit", action="store_true",
                        help="Actually run the DELETE HTTP call. Default is DRY-RUN (no deletes, no backups written).")
    parser.add_argument("--skip-recent-days", type=int, default=30,
                        help="Skip articles published more recently than this many days (default 30 — Ahrefs may not have crawled them yet)")
    args = parser.parse_args()

    if not args.verdict and not args.slugs:
        sys.exit("error: must pass --verdict or --slugs")

    base = os.environ.get("STRAPI_BASE_URL")
    token = os.environ.get("STRAPI_API_TOKEN")
    if not base or not token:
        sys.exit("error: STRAPI_BASE_URL and STRAPI_API_TOKEN required (wrap with `doppler run --`)")

    slug_filter = [s.strip() for s in args.slugs.split(",") if s.strip()] if args.slugs else None
    targets = load_targets(args.verdict, slug_filter, args.limit)

    # Skip articles published in the last N days (Ahrefs hasn't crawled them yet)
    if args.skip_recent_days > 0:
        cutoff = datetime.now(timezone.utc).timestamp() - args.skip_recent_days * 86400
        before = len(targets)
        kept = []
        for r in targets:
            pub = r.get("publishedAt") or ""
            if pub:
                try:
                    pub_ts = datetime.fromisoformat(pub.replace("Z", "+00:00")).timestamp()
                    if pub_ts > cutoff:
                        sys.stdout.write(f"skip (too recent, published {pub[:10]}): {r['slug']}\n")
                        continue
                except ValueError:
                    pass
            kept.append(r)
        targets = kept
        if before != len(targets):
            sys.stdout.write(f"\nFiltered out {before - len(targets)} articles published within last {args.skip_recent_days} days.\n\n")

    mode = "COMMIT (REAL DELETE)" if args.commit else "DRY-RUN (no deletes)"
    sys.stdout.write(f"Mode: {mode}\n")
    sys.stdout.write(f"Targets: {len(targets)} articles\n")
    sys.stdout.write("=" * 60 + "\n\n")

    if not targets:
        sys.stdout.write("Nothing to do.\n")
        return

    already_deleted = load_already_deleted_document_ids()

    successes = 0
    failures: list[tuple[str, str]] = []
    skipped_already_deleted = 0
    for i, row in enumerate(targets, 1):
        slug = row["slug"]
        verdict = row["verdict"]
        prefix = f"[{i}/{len(targets)}] {slug}"
        sys.stdout.write(f"{prefix}\n")
        sys.stdout.flush()

        article = fetch_article(base, token, slug)
        if not article:
            sys.stdout.write(f"  WARN: article not found in Strapi (already deleted?)\n")
            write_log({
                "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "slug": slug, "verdict": verdict, "action": "skipped_not_found",
                "error": "article not found via slug filter",
            })
            continue

        document_id = article.get("documentId")
        if not document_id:
            sys.stdout.write(f"  ERROR: article has no documentId — schema unexpected\n")
            failures.append((slug, "no documentId in payload"))
            continue

        # Per-documentId skip: if this exact entity was already successfully
        # deleted on a prior run, don't redo it. Re-created articles with the
        # same slug have a fresh documentId and proceed normally.
        if document_id in already_deleted:
            sys.stdout.write(f"  skip — documentId {document_id} already deleted on a prior run\n")
            skipped_already_deleted += 1
            continue

        if args.commit:
            try:
                backup_path = backup_article(slug, article)
            except Exception as e:
                sys.stdout.write(f"  ERROR: backup failed ({e}); ABORTING delete for this article\n")
                failures.append((slug, f"backup failed: {e}"))
                continue
            sys.stdout.write(f"  backed up -> {backup_path.relative_to(ROOT)}\n")

            code, err = delete_article(base, token, document_id)
            if 200 <= code < 300:
                sys.stdout.write(f"  DELETED (HTTP {code})\n")
                successes += 1
                write_log({
                    "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "slug": slug, "verdict": verdict, "document_id": document_id,
                    "http_code": str(code), "action": "deleted",
                    "backup_path": str(backup_path.relative_to(ROOT)),
                })
            else:
                sys.stdout.write(f"  FAILED (HTTP {code}): {err[:120]}\n")
                failures.append((slug, f"HTTP {code}: {err[:120]}"))
                write_log({
                    "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "slug": slug, "verdict": verdict, "document_id": document_id,
                    "http_code": str(code), "action": "delete_failed",
                    "backup_path": str(backup_path.relative_to(ROOT)),
                    "error": err[:200],
                })
            time.sleep(SLEEP_BETWEEN)
        else:
            sys.stdout.write(f"  would back up + DELETE (documentId={document_id})\n")
            successes += 1

    sys.stdout.write("\n" + "=" * 60 + "\n")
    sys.stdout.write(f"Done. {successes} {'deleted' if args.commit else 'would-delete'}, {len(failures)} failed.\n")
    if failures:
        sys.stdout.write("\nFailures:\n")
        for slug, msg in failures:
            sys.stdout.write(f"  {slug}: {msg}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
