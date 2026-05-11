#!/usr/bin/env python3
"""greptile_pr_watcher — wake the assignee when Greptile responds on a PR.

Designed to run as a Paperclip routine every ~2 minutes. The routine creates
an execution issue assigned to the CTO; this script does the actual work in
that heartbeat:

  1. Lists open PRs in `lionelndong/blog-agent-2`.
  2. For each PR, GETs reviews + review-comments since the per-PR cursor.
  3. Filters for `greptile-apps[bot]`.
  4. On a hit, looks up the Paperclip issue by `PLEAA-NNN` in the PR title
     and posts a comment summarising each new finding/reply, with deep
     links into the GitHub thread.
  5. That comment fires the existing `issue_commented` wake on the assignee
     of the Paperclip issue — closing the loop without anyone having to
     nudge.

State (per-PR cursor markers) is kept at $AGENT_HOME/.cache/greptile-pr-watcher-state.json
so this stays per-agent and survives restarts.

PLEAA-461 (closes the manual-nudge loop in PLEAA-457).
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = "lionelndong/blog-agent-2"
GREPTILE_LOGIN = "greptile-apps[bot]"
# Scoped to the Pleasurai company prefix to avoid spurious cross-project lookups
# (e.g. a branch like `fix/JIRA-456-thing` resolving to a Paperclip issue in the
# wrong company). Widen this if/when the watcher is taught to handle more repos.
TICKET_RE = re.compile(r"\b(PLEAA)-(\d+)\b")

# State file: per-PR `last_seen_review_id` and `last_seen_comment_id` cursors.
# Living under AGENT_HOME means it survives across heartbeats and is scoped
# to me (the CTO) — other agents running this same script in parallel would
# get their own state.
STATE_PATH = Path(os.environ.get("AGENT_HOME", str(Path.home()))) / ".cache" / "greptile-pr-watcher-state.json"


def _http_json(method: str, url: str, *, headers: dict[str, str], body: dict | None = None, timeout: int = 30) -> dict | list | None:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            return json.loads(raw.decode("utf-8")) if raw else None
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode("utf-8", errors="replace")[:500]
        sys.stderr.write(f"warning: {method} {url} -> {e.code} {body_txt}\n")
        return None
    except urllib.error.URLError as e:
        sys.stderr.write(f"warning: {method} {url} -> URLError {e}\n")
        return None


def _http_json_with_headers(
    method: str, url: str, *, headers: dict[str, str], body: dict | None = None, timeout: int = 30
) -> tuple[dict | list | None, dict[str, str]]:
    """Variant of _http_json that also returns response headers — needed for
    GitHub `Link: rel="next"` pagination."""
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            payload = json.loads(raw.decode("utf-8")) if raw else None
            resp_headers = {k.lower(): v for k, v in resp.headers.items()}
            return payload, resp_headers
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode("utf-8", errors="replace")[:500]
        sys.stderr.write(f"warning: {method} {url} -> {e.code} {body_txt}\n")
        return None, {}
    except urllib.error.URLError as e:
        sys.stderr.write(f"warning: {method} {url} -> URLError {e}\n")
        return None, {}


# --- GitHub --------------------------------------------------------------


_LINK_NEXT_RE = re.compile(r'<([^>]+)>;\s*rel="next"')


def _parse_next_link(link_header: str | None) -> str | None:
    """Extract the rel="next" URL from a GitHub Link response header."""
    if not link_header:
        return None
    m = _LINK_NEXT_RE.search(link_header)
    return m.group(1) if m else None


def _gh_headers() -> dict[str, str]:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("error: GITHUB_TOKEN required")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "greptile-pr-watcher/1.0",
    }


def _gh(path: str) -> Any:
    """Single-page GET — kept for callers that don't need pagination."""
    return _http_json("GET", f"https://api.github.com{path}", headers=_gh_headers())


def _gh_paginated(path: str, *, max_pages: int = 50) -> list[dict]:
    """GET a GitHub list endpoint, following Link: rel="next" until exhausted.

    Returns the concatenated list across all pages. Uses `per_page=100` by
    default so each tick stays cheap. `max_pages` is a safety bound so a
    runaway pagination loop can't pin the heartbeat.
    """
    headers = _gh_headers()
    sep = "&" if "?" in path else "?"
    url: str | None = f"https://api.github.com{path}{sep}per_page=100"
    aggregate: list[dict] = []
    pages = 0
    while url and pages < max_pages:
        payload, resp_headers = _http_json_with_headers("GET", url, headers=headers)
        if not isinstance(payload, list):
            break
        aggregate.extend(payload)
        url = _parse_next_link(resp_headers.get("link"))
        pages += 1
    if pages >= max_pages and url:
        sys.stderr.write(f"warning: pagination cap hit ({max_pages} pages) for {path}\n")
    return aggregate


# Window (days) for picking up activity on recently-closed PRs. Greptile often
# leaves follow-up review comments minutes-to-hours AFTER a PR merges
# (e.g. PR #11 merged 22:04 UTC, Greptile comment landed 22:13 UTC). The
# original `state=open`-only listing missed those entirely. We now fetch
# state=all sorted by updated desc and stop once we cross this window —
# bounded work, no flood on first encounter of an old PR.
RECENT_PR_WINDOW_DAYS = 14


def _parse_iso8601(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def list_recent_prs(window_days: int = RECENT_PR_WINDOW_DAYS) -> list[dict]:
    """Fetch PRs (open + recently-closed) sorted by `updated` desc.

    Stops paginating once we see a PR last updated more than `window_days`
    ago — anything older has either already been processed (cursor advanced)
    or is too stale to care about. This catches Greptile activity on PRs
    that have been merged but are still receiving review comments.
    """
    cutoff = datetime.now(timezone.utc).timestamp() - window_days * 86400
    headers = _gh_headers()
    url: str | None = (
        f"https://api.github.com/repos/{REPO}/pulls"
        "?state=all&sort=updated&direction=desc&per_page=100"
    )
    aggregate: list[dict] = []
    pages = 0
    max_pages = 10  # 1000 PRs max scanned per tick — way more than we need
    while url and pages < max_pages:
        payload, resp_headers = _http_json_with_headers("GET", url, headers=headers)
        if not isinstance(payload, list):
            break
        for pr in payload:
            updated = _parse_iso8601(pr.get("updated_at"))
            if updated is None:
                aggregate.append(pr)
                continue
            if updated.timestamp() < cutoff:
                # Sorted desc by updated — once we cross the window, stop.
                return aggregate
            aggregate.append(pr)
        url = _parse_next_link(resp_headers.get("link"))
        pages += 1
    return aggregate


# Backwards-compat alias for any external caller still importing the old name.
def list_open_prs() -> list[dict]:
    return list_recent_prs()


def list_pr_reviews(pr_num: int) -> list[dict]:
    return _gh_paginated(f"/repos/{REPO}/pulls/{pr_num}/reviews")


def list_pr_review_comments(pr_num: int) -> list[dict]:
    return _gh_paginated(f"/repos/{REPO}/pulls/{pr_num}/comments")


def list_pr_issue_comments(pr_num: int) -> list[dict]:
    return _gh_paginated(f"/repos/{REPO}/issues/{pr_num}/comments")


# --- Paperclip -----------------------------------------------------------


def _pc(method: str, path: str, body: dict | None = None) -> Any:
    base = os.environ.get("PAPERCLIP_API_URL")
    key = os.environ.get("PAPERCLIP_API_KEY")
    run_id = os.environ.get("PAPERCLIP_RUN_ID", "")
    if not base or not key:
        sys.exit("error: PAPERCLIP_API_URL + PAPERCLIP_API_KEY required (run inside a Paperclip heartbeat)")
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    if run_id:
        headers["X-Paperclip-Run-Id"] = run_id
    return _http_json(method, f"{base}{path}", headers=headers, body=body)


def find_issue_by_identifier(identifier: str) -> str | None:
    """Resolve PLEAA-457 → issue UUID via the company-issues search endpoint."""
    company_id = os.environ.get("PAPERCLIP_COMPANY_ID")
    if not company_id:
        sys.exit("error: PAPERCLIP_COMPANY_ID required")
    q = urllib.parse.quote(identifier)
    out = _pc("GET", f"/api/companies/{company_id}/issues?q={q}&limit=20")
    # The endpoint returns a bare list of issues. Accept dict-wrapped shapes
    # too in case it ever changes (`{issues: [...]}` / `{data: [...]}`).
    if isinstance(out, list):
        items = out
    elif isinstance(out, dict):
        items = out.get("issues") or out.get("data") or []
    else:
        return None
    for entry in items:
        if entry.get("identifier") == identifier:
            return entry.get("id")
    return None


def post_paperclip_comment(issue_id: str, body: str) -> str | None:
    out = _pc("POST", f"/api/issues/{issue_id}/comments", {"body": body})
    return out.get("id") if isinstance(out, dict) else None


def mark_self_done() -> None:
    """PATCH the executing Paperclip issue to done so it doesn't linger in_progress
    between webhook deliveries and trip long_active_duration productivity reviews.
    Idempotent — safe to call even when no Greptile findings were posted."""
    task_id = os.environ.get("PAPERCLIP_TASK_ID")
    if not task_id:
        return
    _pc("PATCH", f"/api/issues/{task_id}", {"status": "done"})


# --- State ----------------------------------------------------------------


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {"prs": {}}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        sys.stderr.write(f"warning: state file unreadable, starting fresh ({e})\n")
        return {"prs": {}}


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


# --- Core logic ----------------------------------------------------------


def extract_ticket(*haystacks: str) -> str | None:
    """Scan title + body + branch (in order) for the first PLEAA-NNN style id.

    Title is the canonical place to put the ticket and is preferred — but we
    fall back to the PR body and branch name so a missing-from-title ticket
    isn't a hard failure.
    """
    for s in haystacks:
        if not s:
            continue
        m = TICKET_RE.search(s)
        if m:
            return f"{m.group(1)}-{m.group(2)}"
    return None


def summarise_inline(c: dict) -> str:
    body = c.get("body") or ""
    # First non-empty markdown line, stripped of HTML img tags Greptile uses for severity badges.
    body = re.sub(r"<[^>]+>", "", body).strip()
    headline = next((line.strip() for line in body.splitlines() if line.strip()), "(no body)")
    if len(headline) > 240:
        headline = headline[:237] + "…"
    path = c.get("path") or "?"
    line = c.get("line") or c.get("original_line") or "?"
    return f"- [{path}:{line}]({c.get('html_url','')}) — {headline}"


def summarise_review(r: dict) -> str:
    state = r.get("state") or "?"
    body = (r.get("body") or "").strip()
    headline = next((line.strip() for line in body.splitlines() if line.strip()), "(no body)") if body else "(empty review body)"
    if len(headline) > 240:
        headline = headline[:237] + "…"
    return f"- [review {state}]({r.get('html_url','')}) — {headline}"


def process_pr(pr: dict, state: dict, dry_run: bool = False) -> dict:
    pr_num = pr["number"]
    pr_key = str(pr_num)
    first_encounter = pr_key not in state["prs"]
    pr_state = state["prs"].setdefault(pr_key, {"last_review_id": 0, "last_comment_id": 0, "last_issue_comment_id": 0})

    ticket = extract_ticket(
        pr.get("title", ""),
        pr.get("body") or "",
        (pr.get("head") or {}).get("ref") or "",
    )
    if not ticket:
        return {"pr": pr_num, "skipped": "no PLEAA-NNN ticket in title/body/branch"}

    # First-encounter floor for closed/merged PRs: only surface activity that
    # happened AFTER the merge timestamp. Anything pre-merge was visible to
    # the author during the PR review and addressed (or knowingly waived)
    # before the PR landed — re-posting it now would just spam the tracking
    # issue. For open PRs (or PRs we've already seen at least once) this
    # floor is `None` and the cursor-based filter does the work.
    merged_floor = None
    if first_encounter and (pr.get("merged_at") or pr.get("closed_at")):
        merged_floor = _parse_iso8601(pr.get("merged_at") or pr.get("closed_at"))

    def _after_floor(item: dict) -> bool:
        if merged_floor is None:
            return True
        ts = _parse_iso8601(item.get("created_at") or item.get("submitted_at"))
        return ts is not None and ts >= merged_floor

    all_reviews = [r for r in list_pr_reviews(pr_num) if r.get("user", {}).get("login") == GREPTILE_LOGIN]
    all_inline  = [c for c in list_pr_review_comments(pr_num) if c.get("user", {}).get("login") == GREPTILE_LOGIN]
    all_issuecs = [c for c in list_pr_issue_comments(pr_num) if c.get("user", {}).get("login") == GREPTILE_LOGIN]

    new_reviews = [r for r in all_reviews if r.get("id", 0) > pr_state["last_review_id"] and _after_floor(r)]
    new_inline  = [c for c in all_inline  if c.get("id", 0) > pr_state["last_comment_id"] and _after_floor(c)]
    new_issue_comments = [c for c in all_issuecs if c.get("id", 0) > pr_state["last_issue_comment_id"] and _after_floor(c)]

    def _absorb_first_encounter() -> None:
        # On first encounter of a closed PR with no post-merge activity,
        # bootstrap cursors past every Greptile finding we observed so we
        # don't re-evaluate them every tick. Without this, the empty cursor
        # gets persisted, the merged_floor stops applying next run (no
        # longer first_encounter), and pre-merge findings would suddenly
        # flood the tracking issue.
        if first_encounter and merged_floor is not None:
            pr_state["last_review_id"] = max([pr_state["last_review_id"]] + [r.get("id", 0) for r in all_reviews])
            pr_state["last_comment_id"] = max([pr_state["last_comment_id"]] + [c.get("id", 0) for c in all_inline])
            pr_state["last_issue_comment_id"] = max([pr_state["last_issue_comment_id"]] + [c.get("id", 0) for c in all_issuecs])

    if not (new_reviews or new_inline or new_issue_comments):
        _absorb_first_encounter()
        return {"pr": pr_num, "ticket": ticket, "new_findings": 0}

    # Build a single Paperclip comment summarising everything new.
    parts = [f"### Greptile activity on [PR #{pr_num}]({pr['html_url']}) — {pr.get('title','(untitled)')}\n"]
    if new_reviews:
        parts.append(f"**{len(new_reviews)} new review(s):**")
        parts.extend(summarise_review(r) for r in new_reviews)
        parts.append("")
    if new_inline:
        parts.append(f"**{len(new_inline)} new inline comment(s):**")
        parts.extend(summarise_inline(c) for c in new_inline)
        parts.append("")
    if new_issue_comments:
        parts.append(f"**{len(new_issue_comments)} new top-level comment(s):**")
        parts.extend(summarise_inline(c) for c in new_issue_comments)
        parts.append("")
    parts.append(f"_Posted by `greptile-pr-watcher` ({datetime.now(timezone.utc).isoformat(timespec='seconds')})._\n")
    body = "\n".join(parts)

    result: dict = {
        "pr": pr_num, "ticket": ticket,
        "new_reviews": len(new_reviews),
        "new_inline": len(new_inline),
        "new_issue_comments": len(new_issue_comments),
    }

    if dry_run:
        result["dry_run_body_preview"] = body[:400]
        return result

    issue_id = find_issue_by_identifier(ticket)
    if not issue_id:
        result["error"] = f"could not resolve {ticket} → Paperclip issue id"
        return result

    comment_id = post_paperclip_comment(issue_id, body)
    if not comment_id:
        result["error"] = "Paperclip comment POST failed (see stderr)"
        return result

    result["paperclip_issue_id"] = issue_id
    result["paperclip_comment_id"] = comment_id

    # Advance cursors only after a successful post — if anything failed we'll
    # retry the same items next tick. Absorb all observed Greptile IDs (not
    # just the posted ones) so any pre-merge items the floor filtered out
    # also get parked behind the cursor and don't re-surface next tick.
    pr_state["last_review_id"] = max(
        [pr_state["last_review_id"]] + [r.get("id", 0) for r in all_reviews]
    )
    pr_state["last_comment_id"] = max(
        [pr_state["last_comment_id"]] + [c.get("id", 0) for c in all_inline]
    )
    pr_state["last_issue_comment_id"] = max(
        [pr_state["last_issue_comment_id"]] + [c.get("id", 0) for c in all_issuecs]
    )
    return result


def main(argv: list[str]) -> int:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="don't post Paperclip comments or advance cursors")
    parser.add_argument("--reset", action="store_true", help="wipe state file before running (re-bootstrap cursors at HEAD of each PR)")
    parser.add_argument(
        "--bootstrap",
        action="store_true",
        help=(
            "set cursors to current HEAD without posting (use on first install). "
            "State is always persisted when this flag is set, even with --dry-run."
        ),
    )
    args = parser.parse_args(argv)

    if args.reset and STATE_PATH.exists():
        STATE_PATH.unlink()
        sys.stderr.write(f"reset: removed {STATE_PATH}\n")

    state = load_state()
    prs = list_recent_prs()
    if not prs:
        print("no recent PRs")
        return 0

    results = []
    for pr in prs:
        if args.bootstrap:
            # Set cursors to the highest currently-seen ids without posting.
            pr_key = str(pr["number"])
            reviews = list_pr_reviews(pr["number"])
            inline  = list_pr_review_comments(pr["number"])
            issuecs = list_pr_issue_comments(pr["number"])
            state["prs"][pr_key] = {
                "last_review_id": max([0] + [r.get("id", 0) for r in reviews]),
                "last_comment_id": max([0] + [c.get("id", 0) for c in inline]),
                "last_issue_comment_id": max([0] + [c.get("id", 0) for c in issuecs]),
            }
            results.append({"pr": pr["number"], "bootstrapped": True, **state["prs"][pr_key]})
        else:
            results.append(process_pr(pr, state, dry_run=args.dry_run))

    # `--bootstrap` is a setup operation: its whole purpose is to persist
    # cursors at HEAD so the next steady-state run doesn't re-post historical
    # comments. We persist even with `--dry-run` so an operator using
    # `--bootstrap --dry-run` as a "safe first run" doesn't end up with an
    # un-bootstrapped state file. `--dry-run` still suppresses Paperclip
    # comment POSTs (those happen in `process_pr`, not here).
    if args.bootstrap or not args.dry_run:
        save_state(state)

    print(json.dumps({"checked": len(prs), "results": results}, indent=2))

    if not args.dry_run:
        mark_self_done()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
