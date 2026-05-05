#!/usr/bin/env python3
"""Resolve any [VISUAL:type=action-shot;...] / [VISUAL:type=screenshot;...] placeholders
that now have local PNGs on disk into ![alt](images/{slug}/file.png) markdown,
and update manifest.json statuses accordingly.

Use after `sync_captures_from_vps.sh` lands PNGs from a remote capture host,
or any time PNGs appeared on disk after a captured-remote stage.

Usage:
    python scripts/resolve_captured_visuals.py <slug>
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VISUAL_RE = re.compile(r"\[VISUAL:([^\]]+)\]")


def parse_attrs(body: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in body.split(";"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        k, _, v = part.partition("=")
        out[k.strip()] = v.strip()
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: resolve_captured_visuals.py <slug>", file=sys.stderr)
        return 1
    slug = sys.argv[1]

    cited = ROOT / "content-pipeline" / "6-drafts-cited" / f"{slug}.md"
    images_dir = ROOT / "content-pipeline" / "images" / slug
    manifest_path = images_dir / "manifest.json"
    if not cited.exists():
        print(f"error: cited draft not found at {cited}", file=sys.stderr)
        return 1
    if not manifest_path.exists():
        print(f"error: manifest not found at {manifest_path}", file=sys.stderr)
        return 1

    text = cited.read_text(encoding="utf-8")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    resolved = 0
    skipped_no_png = 0
    new_text = text

    for entry in manifest.get("visuals", []):
        if entry.get("status") not in {"manual", "captured_remote"}:
            continue
        if entry.get("type") not in {"action-shot", "screenshot"}:
            continue

        result = entry.get("result", {})
        local_path_rel = result.get("local_path") or f"content-pipeline/images/{slug}/{result.get('filename', '')}"
        if not local_path_rel:
            continue
        local_path = ROOT / local_path_rel
        if not local_path.exists():
            skipped_no_png += 1
            continue

        # Find the matching placeholder in the draft by `what=` attribute
        target_what = entry.get("attrs", {}).get("what", "")
        replaced_this = False
        for m in VISUAL_RE.finditer(new_text):
            attrs = parse_attrs(m.group(1))
            if attrs.get("type") not in {"action-shot", "screenshot"}:
                continue
            if attrs.get("what") == target_what:
                alt = entry.get("alt", target_what or "image")
                rel_for_md = f"images/{slug}/{local_path.name}"
                replacement = f"![{alt}]({rel_for_md})"
                new_text = new_text[: m.start()] + replacement + new_text[m.end() :]
                replaced_this = True
                break
        if not replaced_this:
            print(f"warn: no placeholder found in draft for what={target_what!r}", file=sys.stderr)
            continue

        # Update manifest entry
        entry["status"] = "captured"
        entry["result"] = {
            "status": "captured",
            "path": local_path_rel,
            "capture_method": result.get("capture_method", "claude_in_chrome_synced"),
        }
        resolved += 1

    if resolved > 0:
        cited.write_text(new_text, encoding="utf-8")
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"resolved={resolved} skipped_no_png={skipped_no_png}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
