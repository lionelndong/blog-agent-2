#!/usr/bin/env python3
"""Convert a keyword phrase or URL to a filesystem-safe slug.

Usage:
    python scripts/slugify.py "Keyword Cannibalization in SEO"
    python scripts/slugify.py "https://blog.example.com/some-article-title"
"""
from __future__ import annotations

import re
import sys
from urllib.parse import urlparse


def slugify(text: str) -> str:
    if text.startswith(("http://", "https://")):
        path = urlparse(text).path.strip("/")
        text = path.split("/")[-1] if path else urlparse(text).netloc
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "untitled"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: slugify.py <text-or-url>", file=sys.stderr)
        sys.exit(2)
    print(slugify(" ".join(sys.argv[1:])))
