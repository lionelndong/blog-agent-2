#!/usr/bin/env python3
"""Render a side-by-side HTML diff of original vs updated article.

Usage:
    python .claude/skills/update-preview/scripts/render_diff.py <slug>
"""
from __future__ import annotations

import difflib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ORIG_DIR = ROOT / "content-pipeline" / "updates" / "1-extracted"
UPDATED_DIR = ROOT / "content-pipeline" / "updates" / "7-updated-draft"
OUT_DIR = ROOT / "content-pipeline" / "updates" / "5-update-preview"

CSS = """
* { box-sizing: border-box; }
body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 15px; line-height: 1.6; color: #1a1a1a; background: #f5f7fb; }
.diff-header { background: #1a1a1a; color: white; padding: 16px 24px; }
.diff-header h1 { margin: 0; font-size: 1.2rem; }
.diff-header p { margin: 4px 0 0; font-size: 0.85rem; opacity: 0.7; }
.diff { display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background: #ddd; }
.col { background: white; padding: 24px; max-width: 100%; overflow-wrap: break-word; }
.col h2.col-title { background: #f0f0f0; padding: 8px 12px; margin: -24px -24px 24px; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; color: #666; border-bottom: 1px solid #ddd; }
.col-orig h2.col-title { color: #c00; }
.col-updated h2.col-title { color: #060; }
.line { padding: 1px 4px; white-space: pre-wrap; }
.line.add { background: #e6ffec; }
.line.del { background: #ffeef0; text-decoration: line-through; opacity: 0.7; }
.line.same { background: white; }
.line.context { background: #fafafa; color: #999; }
"""


def read_md(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def strip_frontmatter(md: str) -> str:
    if md.startswith("---\n"):
        end = md.find("\n---\n", 4)
        if end != -1:
            return md[end + 5:]
    return md


def diff_lines(orig: str, updated: str) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    o_lines = orig.splitlines()
    u_lines = updated.splitlines()
    matcher = difflib.SequenceMatcher(None, o_lines, u_lines)

    o_out: list[tuple[str, str]] = []
    u_out: list[tuple[str, str]] = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for line in o_lines[i1:i2]:
                o_out.append(("same", line))
                u_out.append(("same", line))
        elif tag == "delete":
            for line in o_lines[i1:i2]:
                o_out.append(("del", line))
                u_out.append(("context", ""))
        elif tag == "insert":
            for line in u_lines[j1:j2]:
                o_out.append(("context", ""))
                u_out.append(("add", line))
        elif tag == "replace":
            del_lines = o_lines[i1:i2]
            add_lines = u_lines[j1:j2]
            for line in del_lines:
                o_out.append(("del", line))
            for line in add_lines:
                u_out.append(("add", line))
            pad = abs(len(add_lines) - len(del_lines))
            if len(del_lines) < len(add_lines):
                for _ in range(pad):
                    o_out.append(("context", ""))
            elif len(add_lines) < len(del_lines):
                for _ in range(pad):
                    u_out.append(("context", ""))
    return o_out, u_out


def render_column(lines: list[tuple[str, str]]) -> str:
    out = []
    for cls, text in lines:
        escaped = (
            text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )
        out.append(f'<div class="line {cls}">{escaped or "&nbsp;"}</div>')
    return "\n".join(out)


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: render_diff.py <slug>", file=sys.stderr)
        sys.exit(2)
    slug = sys.argv[1]
    orig = strip_frontmatter(read_md(ORIG_DIR / f"{slug}.md"))
    updated = read_md(UPDATED_DIR / f"{slug}.md")

    if not orig or not updated:
        print(f"error: missing input — orig empty: {not orig}, updated empty: {not updated}", file=sys.stderr)
        sys.exit(1)

    o_lines, u_lines = diff_lines(orig, updated)

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Update diff: {slug}</title>
<style>{CSS}</style></head>
<body>
<div class="diff-header"><h1>Update diff — {slug}</h1>
<p>Left: original article. Right: updated draft. Removals strikethrough red; additions green.</p></div>
<div class="diff">
  <div class="col col-orig"><h2 class="col-title">Original</h2>{render_column(o_lines)}</div>
  <div class="col col-updated"><h2 class="col-title">Updated</h2>{render_column(u_lines)}</div>
</div>
</body></html>
"""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{slug}.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
