#!/usr/bin/env python3
"""Show which pipeline stages have been completed for a given slug.

Usage:
    python scripts/pipeline_status.py keyword-cannibalization
    python scripts/pipeline_status.py keyword-cannibalization --update
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIPELINE = ROOT / "content-pipeline"

CREATION_STAGES = [
    ("0-context", "{slug}.md", "Context (optional)"),
    ("1-research", "{slug}.md", "Research"),
    ("2-reference", "{slug}.md", "Brand reference"),
    ("3-outlines", "{slug}.md", "Outline"),
    ("4-outlines-annotated", "{slug}.md", "Product-annotated outline"),
    ("5-drafts", "{slug}.md", "Draft"),
    ("quality-checks", "{slug}.md", "Quality check"),
    ("6-drafts-cited", "{slug}.md", "Cited draft"),
    ("images/{slug}", "manifest.json", "Visuals manifest"),
    ("7-preview", "{slug}.html", "HTML preview"),
    ("8-publish/{slug}", "article.md", "Publish package"),
]

UPDATE_STAGES = [
    ("updates/0-guidance", "{slug}.md", "Update guidance"),
    ("updates/1-extracted", "{slug}.md", "Extracted content"),
    ("updates/2-update-claims", "{slug}.md", "Updated claims"),
    ("updates/3-update-product-mentions", "{slug}.md", "Updated product mentions"),
    ("updates/4-update-topic-gaps", "{slug}.md", "Topic gaps"),
    ("updates/7-updated-draft", "{slug}.md", "Updated draft"),
    ("updates/5-update-preview", "{slug}.html", "Update preview HTML"),
]


def status(slug: str, stages: list[tuple[str, str, str]]) -> int:
    completed = 0
    for stage_dir, file_pattern, label in stages:
        rel_dir = stage_dir.format(slug=slug)
        path = PIPELINE / rel_dir / file_pattern.format(slug=slug)
        mark = "[x]" if path.exists() else "[ ]"
        if path.exists():
            completed += 1
        print(f"  {mark}  {label:<32} {path.relative_to(ROOT)}")
    return completed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    parser.add_argument("--update", action="store_true", help="Show update pipeline stages instead")
    args = parser.parse_args()

    stages = UPDATE_STAGES if args.update else CREATION_STAGES
    label = "UPDATE" if args.update else "CREATION"
    print(f"Pipeline status for slug: {args.slug}  ({label})\n")
    completed = status(args.slug, stages)
    print(f"\n  {completed}/{len(stages)} stages completed")


if __name__ == "__main__":
    main()
