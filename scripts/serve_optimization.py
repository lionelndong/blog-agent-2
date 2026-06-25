#!/usr/bin/env python3
"""Tiny CORS-enabled HTTP server to serve optimization HTML to the Ahrefs Content Helper.

Used by the /optimize-content skill: the JS injection in Ahrefs's TipTap editor fetches
the latest HTML from this server, decodes nothing (already HTML), and calls setContent.

Usage:
    python scripts/serve_optimization.py [--port 8766] [--slug ai-girlfriend]

Routes:
    GET /draft.html           Returns the current optimized cited draft as HTML
    GET /healthz              Returns "ok"

Run with --slug to set which slug's draft is served. The server reads the cited draft
from disk on every request (so re-running /optimize-content edits get picked up live).
"""
from __future__ import annotations

import argparse
import re
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "preview" / "scripts"))


def render_html(slug: str) -> str:
    from render_preview import md_to_html, extract_title
    cited = ROOT / "content-pipeline" / "6-drafts-cited" / f"{slug}.md"
    if not cited.exists():
        return "<h1>Draft not found</h1>"
    md = cited.read_text(encoding="utf-8")
    md = re.split(r"^---\s*\n+##\s+Editor notes", md, maxsplit=1, flags=re.MULTILINE)[0].rstrip() + "\n"
    title, body = extract_title(md)
    return f"<h1>{title}</h1>\n{md_to_html(body)}"


class Handler(BaseHTTPRequestHandler):
    slug = "ai-girlfriend"

    def log_message(self, fmt, *args):
        sys.stderr.write(f"[serve_opt] {fmt % args}\n")

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path == "/healthz":
            body = b"ok"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self._cors()
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path.startswith("/draft.html"):
            html = render_html(Handler.slug)
            body = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self._cors()
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_error(404)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--port", type=int, default=8766)
    p.add_argument("--slug", default="ai-girlfriend")
    a = p.parse_args()
    Handler.slug = a.slug
    s = ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    print(f"serving on http://127.0.0.1:{a.port} (slug={a.slug})", file=sys.stderr)
    try:
        s.serve_forever()
    except KeyboardInterrupt:
        print("shutdown.", file=sys.stderr)


if __name__ == "__main__":
    main()
