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
TICKET_RE = re.compile(r"\b([A-Z]{2,8})-(\d+)\b")

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


# --- GitHub --------------------------------------------------------------


def _gh(path: str) -> Any:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("error: GITHUB_TOKEN required")
    return _http_json(
        "GET",
        f"https://api.github.com{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "greptile-pr-watcher/1.0",
        },
    )


def list_open_prs() -> list[dict]:
    prs = _gh(f"/repos/{REPO}/pulls?state=open&per_page=100") or []
    return prs if isinstance(prs, list) else []


def list_pr_reviews(pr_num: int) -> list[dict]:
    out = _gh(f"/repos/{REPO}/pulls/{pr_num}/reviews?per_page=100") or []
    return out if isinstance(out, list) else []


def list_pr_review_comments(pr_num: int) -> list[dict]:
    out = _gh(f"/repos/{REPO}/pulls/{pr_num}/comments?per_page=100") or []
    return out if isinstance(out, list) else []


def list_pr_issue_comments(pr_num: int) -> list[dict]:
    out = _gh(f"/repos/{REPO}/issues/{pr_num}/comments?per_page=100") or []
    return out if isinstance(out, list) else []


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
    if not isinstance(out, dict):
        return None
    items = out.get("issues") or out.get("data") or []
    for entry in items:
        if entry.get("identifier") == identifier:
            return entry.get("id")
    return None


def post_paperclip_comment(issue_id: str, body: str) -> str | None:
    out = _pc("POST", f"/api/issues/{issue_id}/comments", {"body": body})
    return out.get("id") if isinstance(out, dict) else None


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
    pr_state = state["prs"].setdefault(pr_key, {"last_review_id": 0, "last_comment_id": 0, "last_issue_comment_id": 0})

    ticket = extract_ticket(
        pr.get("title", ""),
        pr.get("body") or "",
        (pr.get("head") or {}).get("ref") or "",
    )
    if not ticket:
        return {"pr": pr_num, "skipped": "no PLEAA-NNN ticket in title/body/branch"}

    new_reviews = [r for r in list_pr_reviews(pr_num)
                   if r.get("user", {}).get("login") == GREPTILE_LOGIN
                   and r.get("id", 0) > pr_state["last_review_id"]]
    new_inline = [c for c in list_pr_review_comments(pr_num)
                  if c.get("user", {}).get("login") == GREPTILE_LOGIN
                  and c.get("id", 0) > pr_state["last_comment_id"]]
    new_issue_comments = [c for c in list_pr_issue_comments(pr_num)
                          if c.get("user", {}).get("login") == GREPTILE_LOGIN
                          and c.get("id", 0) > pr_state["last_issue_comment_id"]]

    if not (new_reviews or new_inline or new_issue_comments):
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
    # retry the same items next tick.
    pr_state["last_review_id"] = max([pr_state["last_review_id"]] + [r["id"] for r in new_reviews])
    pr_state["last_comment_id"] = max([pr_state["last_comment_id"]] + [c["id"] for c in new_inline])
    pr_state["last_issue_comment_id"] = max([pr_state["last_issue_comment_id"]] + [c["id"] for c in new_issue_comments])
    return result


def main(argv: list[str]) -> int:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="don't post Paperclip comments or advance cursors")
    parser.add_argument("--reset", action="store_true", help="wipe state file before running (re-bootstrap cursors at HEAD of each PR)")
    parser.add_argument("--bootstrap", action="store_true", help="set cursors to current HEAD without posting (use on first install)")
    args = parser.parse_args(argv)

    if args.reset and STATE_PATH.exists():
        STATE_PATH.unlink()
        sys.stderr.write(f"reset: removed {STATE_PATH}\n")

    state = load_state()
    prs = list_open_prs()
    if not prs:
        print("no open PRs")
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

    if not args.dry_run:
        save_state(state)

    print(json.dumps({"checked": len(prs), "results": results}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
