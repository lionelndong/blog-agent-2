#!/usr/bin/env python3
"""capture-visuals: resolve bot-walled EXTERNAL placeholders that the headless
visuals pass left `failed`/`manual`, using a PROVIDER-AGNOSTIC capture backend.

The main `generate_visuals` pass captures externals HEADLESS (fast), which bot
walls (Google SERP, Reddit, some competitor UIs) block -> the entry is recorded
`failed` with a `claude_in_chrome` breadcrumb. This script re-attempts those
exact entries with a MODEL-NEUTRAL backend: **headed patchright on the
container's :99 display** (the same mechanism the action-shots use), which
passes walls a headless browser can't. It is pure Python -> it works regardless
of which model the EO runs on (Claude, Codex, ...). Claude-in-Chrome is a
SEPARATE optional backend the SKILL layers on for the rare entry this can't get;
it is NOT required here -- that is the whole point of provider-agnosticism.

For each resolved entry it saves the PNG under content-pipeline/images/<slug>/,
rewrites the cited-draft placeholder -> ![alt](images/<slug>/file.png) (reusing
`generate_visuals._rewrite_draft` so output is byte-identical to the main pass),
and flips the manifest entry to `captured`. Anything it still can't get stays
`failed` for the SKILL's Claude-in-Chrome fallback or an editor -- we NEVER
bypass real site protections.

Usage: python capture_visuals_resolve.py <slug> [--no-headed]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

# Reuse the generate-visuals engine (sibling skill at the same skills/<x>/scripts depth).
_GV_SCRIPTS = Path(__file__).resolve().parents[2] / "generate-visuals" / "scripts"
sys.path.insert(0, str(_GV_SCRIPTS))
import generate_visuals as gv  # noqa: E402
import capture_screenshot as cs  # noqa: E402

# Headed capture needs an X display; the container runs Xvfb on :99.
os.environ.setdefault("DISPLAY", ":99")

_RETRYABLE = {"failed", "manual"}


def _selected(entry: dict[str, Any]) -> bool:
    """An external entry the headed backend should re-attempt."""
    if entry.get("type") != "external":
        return False
    if entry.get("status") not in _RETRYABLE:
        return False
    attrs = entry.get("attrs") or {}
    return bool(attrs.get("url"))


def resolve(slug: str, *, headed: bool = True) -> dict[str, Any]:
    draft_path = gv.DRAFT_DIR / f"{slug}.md"
    out_dir = gv.IMAGES_DIR / slug
    manifest_path = out_dir / "manifest.json"
    if not draft_path.exists():
        return {"status": "error", "reason": f"draft_not_found:{draft_path}"}
    if not manifest_path.exists():
        return {"status": "error", "reason": f"manifest_not_found:{manifest_path}"}

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = manifest.get("visuals") or []
    targets = [e for e in entries if _selected(e)]
    total_ext = sum(1 for e in entries if e.get("type") == "external")
    if not targets:
        return {"status": "noop", "reason": "no_retryable_externals",
                "captured": 0, "remaining": 0, "total_externals": total_ext}

    text = draft_path.read_text(encoding="utf-8")
    replacements: list[tuple[str, str]] = []
    captured_paths: list[Path] = []
    captured = 0
    still_failed: list[dict[str, Any]] = []

    for entry in targets:
        attrs = entry.get("attrs") or {}
        url = attrs.get("url")
        sel = attrs.get("selector") or None
        crop = cs._parse_crop(attrs.get("crop")) if attrs.get("crop") else None
        # SFW blur (our niche is 18+; externals are competitor/adult sites) + a
        # height backstop so we never ship a 4000px full-page. Opt out with blur=off.
        _blur = str(attrs.get("blur", "")).strip().lower()
        blur_images = None if _blur in {"off", "0", "false", "no"} else (int(_blur) if _blur.isdigit() else 64)
        index = entry.get("index") or (entries.index(entry) + 1)
        name = gv._slug(attrs.get("what") or attrs.get("sub") or "external")
        out_path = out_dir / f"external-{index}-{name}.png"

        try:
            result = cs.capture(url, out_path, selector=sel, crop=crop,
                                padding=48, headed=headed, block_check=True,
                                blur_images=blur_images, max_height=3600)
            # Selectors are GUESSED blind (the EO never saw the live DOM), so a
            # wrong selector on a real page is common. If the page LOADED but the
            # selector was missing (bounding_box_failed), fall back to a clean
            # viewport capture rather than failing outright -- a full screenshot
            # of the real page is usually a usable visual, and the quality gate
            # reviews it. (A genuinely dead/blocked URL fails navigation instead,
            # so it does NOT trigger this fallback -- we don't fabricate a shot of
            # a page that isn't there.)
            if (result.get("status") != "captured" and sel
                    and result.get("reason") == "bounding_box_failed"):
                vp = cs.capture(url, out_path, selector=None, crop=crop,
                                padding=0, headed=headed, block_check=True,
                                blur_images=blur_images, max_height=3600)
                if vp.get("status") == "captured":
                    vp["clip"] = "viewport_fallback"
                    vp["selector_missed"] = sel
                    result = vp
        except Exception as exc:  # never let one URL kill the whole resolve
            result = {"status": "failed", "reason": "capture_exception",
                      "error": str(exc)[:300]}
        result.setdefault("sub", attrs.get("sub", "external"))
        result["backend"] = "headed_patchright" if headed else "patchright_headless"

        if result.get("status") == "captured":
            rel = gv._rel_to_root(out_path)              # ROOT-relative, fwd slashes
            result["path"] = rel
            disp = rel[len("content-pipeline/"):] if rel.startswith("content-pipeline/") else rel
            raw = entry.get("raw")
            alt = entry.get("alt") or attrs.get("what") or "external screenshot"
            if raw and raw in text:
                replacements.append((raw, f"![{alt}]({disp})"))
            entry["status"] = "captured"
            entry["result"] = result
            # A viewport fallback fired because the guessed selector missed, so we
            # grabbed the whole page -- it MIGHT be the wrong region, a login wall,
            # or a bot-block page (e.g. Reddit blocks datacenter IPs). Flag it so
            # the VISUAL-CRITIQUE-LOOP vision gate verifies it actually shows the
            # claimed thing before publish -- never present a block/error page as a
            # real cited source.
            if result.get("clip") == "viewport_fallback":
                entry["needs_review"] = True
            captured += 1
            captured_paths.append(out_path)
        else:
            entry.setdefault("result", {})
            entry["result"]["last_backend"] = result.get("backend")
            entry["result"]["last_reason"] = result.get("reason") or result.get("error")
            still_failed.append({
                "index": index, "url": url, "selector": sel,
                "what": attrs.get("what"),
                "reason": result.get("reason") or result.get("error"),
                "fallback": (entry.get("result") or {}).get("fallback"),
            })

    if captured_paths:
        opt = gv._load_optimizer()
        if opt is not None:
            for p in captured_paths:
                try:
                    opt.optimize(p)
                except Exception:
                    pass

    if replacements:
        new_text = gv._rewrite_draft(text, replacements)
        if new_text != text:
            draft_path.write_text(new_text, encoding="utf-8")

    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return {
        "status": "ok",
        "slug": slug,
        "captured": captured,
        "remaining": len(still_failed),
        "still_failed": still_failed,
        "backend": "headed_patchright" if headed else "patchright_headless",
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Resolve bot-walled external visuals (model-neutral headed capture).")
    ap.add_argument("slug")
    ap.add_argument("--no-headed", action="store_true",
                    help="Use headless (debug only; bot walls will block).")
    args = ap.parse_args()
    res = resolve(args.slug, headed=not args.no_headed)
    sys.stdout.write(json.dumps(res, indent=2) + "\n")
    return 0 if res.get("status") in {"ok", "noop"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
