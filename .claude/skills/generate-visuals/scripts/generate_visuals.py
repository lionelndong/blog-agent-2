#!/usr/bin/env python3
"""Visual-pipeline dispatcher.

Reads `content-pipeline/6-drafts-cited/<slug>.md`, finds every typed
[VISUAL:type=...;...] (and legacy [SCREENSHOT:...]) placeholder, dispatches
each to the right capture/generate strategy, writes a manifest, rewrites the
draft to reference the produced PNGs, and emits a manual-capture.md file
for visuals that need editor follow-up.

Usage:
    python generate_visuals.py <slug>
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = Path(__file__).resolve().parent
DRAFT_DIR = ROOT / "content-pipeline" / "6-drafts-cited"
IMAGES_DIR = ROOT / "content-pipeline" / "images"

VISUAL_RE = re.compile(r"\[VISUAL:([^\]]+)\]")
LEGACY_SCREENSHOT_RE = re.compile(r"\[SCREENSHOT:\s*([^\]]+)\]")
NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")


def _slug(text: str, max_len: int = 30) -> str:
    text = text.lower()
    text = NON_ALNUM_RE.sub("-", text).strip("-")
    return text[:max_len].rstrip("-") or "visual"


def _parse_attrs(body: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in body.split(";"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        key, _, value = part.partition("=")
        out[key.strip()] = value.strip()
    return out


def _find_placeholders(text: str) -> list[dict[str, Any]]:
    """Return ordered list of placeholders with metadata."""
    items: list[dict[str, Any]] = []
    for match in VISUAL_RE.finditer(text):
        attrs = _parse_attrs(match.group(1))
        items.append(
            {
                "raw": match.group(0),
                "span": match.span(),
                "attrs": attrs,
                "type": (attrs.get("type") or "screenshot").lower(),
                "legacy": False,
            }
        )
    for match in LEGACY_SCREENSHOT_RE.finditer(text):
        items.append(
            {
                "raw": match.group(0),
                "span": match.span(),
                "attrs": {"what": match.group(1).strip()},
                "type": "screenshot",
                "legacy": True,
            }
        )
    items.sort(key=lambda i: i["span"][0])
    return items


def _alt_text(item: dict[str, Any]) -> str:
    a = item["attrs"]
    return a.get("what") or a.get("prompt") or a.get("title") or f"{item['type']} visual"


def _resolve_brand_url(slug_target: str) -> str:
    """Best-effort resolution: brand-config product URLs first, else marketing root."""
    try:
        text = (ROOT / "brand-config.md").read_text(encoding="utf-8")
    except OSError:
        return f"https://pleasur.ai/{slug_target}"
    match = re.search(rf"URL:\s*(https?://\S*{re.escape(slug_target)}\S*)", text, re.IGNORECASE)
    if match:
        return match.group(1).rstrip(",.")
    if slug_target.startswith("http"):
        return slug_target
    return f"https://pleasur.ai/{slug_target}"


def _load_capture_screenshot():
    sys.path.insert(0, str(SCRIPT_DIR))
    try:
        import capture_screenshot  # type: ignore
        return capture_screenshot
    except ImportError:
        return None


def _load_generate_image():
    sys.path.insert(0, str(SCRIPT_DIR))
    try:
        import generate_image  # type: ignore
        return generate_image
    except ImportError:
        return None


def _load_render_chart():
    sys.path.insert(0, str(SCRIPT_DIR))
    try:
        import render_chart  # type: ignore
        return render_chart
    except ImportError:
        return None


def _load_optimizer():
    sys.path.insert(0, str(SCRIPT_DIR))
    try:
        import optimize_image  # type: ignore
        return optimize_image
    except ImportError:
        return None


def _load_run_action_shot():
    sys.path.insert(0, str(SCRIPT_DIR))
    try:
        import run_action_shot  # type: ignore
        return run_action_shot
    except ImportError:
        return None


def _capture_with_playwright(
    item: dict[str, Any],
    url: str,
    out_path: Path,
    *,
    default_padding: int = 0,
) -> dict[str, Any]:
    """Shared Playwright capture path used by both `screenshot` and `external` types.

    `default_padding` is applied when the placeholder doesn't specify one. Set
    to 0 for brand screenshots (we want pixel-perfect product UI), 48 for
    external sources (Reddit / tweet / chart looks nicer with breathing room).
    """
    a = item["attrs"]
    module = _load_capture_screenshot()
    if module is None:
        return {
            "status": "manual",
            "reason": "playwright_unavailable",
            "url": url,
            "filename": out_path.name,
        }

    crop = module._parse_crop(a.get("crop")) if a.get("crop") else None
    crop_mode = (a.get("crop") or "").lower() if a.get("crop") else ""
    crop_directive_ignored = False
    if crop_mode in {"padded", "tight"}:
        # `crop=padded|tight` is sugar for selector-based padded crops.
        # `tight` ≈ 8px; `padded` ≈ 48px. Caller can override with crop=N.
        crop = None
        padding = 48 if crop_mode == "padded" else 8
        # Greptile P2 (PR #4 PLEAA-417): padded/tight crops require a selector
        # — capture_screenshot only enters the padded branch when selector is
        # truthy. Without one, capture falls through to viewport and silently
        # ignores the directive. Surface it as needs_review so the editor sees
        # the manifest entry didn't honor the crop hint.
        if not a.get("selector"):
            crop_directive_ignored = True
    else:
        try:
            padding = int(a.get("padding")) if a.get("padding") else default_padding
        except (TypeError, ValueError):
            padding = default_padding

    validate = (a.get("validate") or "").lower() in {"1", "true", "yes"} or bool(
        os.environ.get("VISUAL_VALIDATION", "").lower() in {"1", "true", "yes"}
    )
    result = module.capture(
        url,
        out_path,
        selector=a.get("selector"),
        crop=crop,
        annotate_selector=a.get("annotate"),
        validate=validate,
        expected_what=a.get("what"),
        padding=padding,
    )
    result["url"] = url
    if crop_directive_ignored:
        result["needs_review"] = True
        result["warn_crop_ignored"] = (
            f"crop={crop_mode} requires a selector; viewport screenshot was "
            "captured instead. Add a CSS selector to the placeholder to honor "
            "the padded/tight crop directive."
        )
    return result


# Failure reasons from capture_screenshot.capture() that mean Playwright was
# blocked at the page level (bot wall, login, navigation, selector-covered-by-
# overlay). For `external` placeholders these are exactly the cases where
# Claude-in-Chrome (real logged-in session, real IP, visual judgment) is the
# right fallback.
#
# `bounding_box_failed` is in this set per Greptile review on PR #4 (PLEAA-417):
# when a login overlay covers the target selector, locator.bounding_box() raises
# BEFORE _check_quality runs, so `redirected_to_login` never fires. Without
# bounding_box_failed in the set the operator would see a bare `failed` and
# /capture-visuals would have no retry breadcrumb.
_CHROME_FALLBACK_REASONS = {
    "cloudflare_challenge_unresolved",
    "redirected_to_login",
    "navigation_failed",
    "image_dimensions_too_small",
    "bounding_box_failed",
}


def _attach_chrome_fallback_hint(result: dict[str, Any], slug: str, item: dict[str, Any]) -> dict[str, Any]:
    """Annotate a failed external capture with /capture-visuals fallback metadata.

    The visuals stage stays `failed` (so pipeline_gate halts as PLEAA-392
    requires) but the manifest entry now carries enough breadcrumbs that
    /capture-visuals can pick this exact entry up in unattended mode and
    re-attempt via the Claude-in-Chrome MCP.
    """
    if result.get("status") != "failed":
        return result
    if result.get("reason") not in _CHROME_FALLBACK_REASONS:
        return result
    a = item["attrs"]
    result["fallback"] = {
        "method": "claude_in_chrome",
        "skill": "/capture-visuals",
        "url": a.get("url"),
        "selector": a.get("selector"),
        "what": a.get("what"),
        "sub": a.get("sub"),
    }
    result["hint"] = (
        f"Playwright blocked ({result['reason']}). Run `/capture-visuals {slug}` "
        "to retry this entry via Claude-in-Chrome (real Chrome session bypasses "
        "the wall). The skill picks up `failed` external entries automatically "
        "in unattended mode."
    )
    return result


def _handle_screenshot(item: dict[str, Any], slug: str, index: int, out_dir: Path) -> dict[str, Any]:
    a = item["attrs"]
    target = a.get("target") or a.get("url") or "create"
    url = a["url"] if "url" in a else _resolve_brand_url(target)
    name = _slug(a.get("what") or target)
    out_path = out_dir / f"screenshot-{index}-{name}.png"
    return _capture_with_playwright(item, url, out_path, default_padding=0)


def _handle_external(item: dict[str, Any], slug: str, index: int, out_dir: Path) -> dict[str, Any]:
    """Auto-capture an external source (Reddit comment, tweet, news chart, etc.).

    PLEAA-417: this used to short-circuit to manual. Neo overrode that — the
    pipeline now actually attempts the capture. A `selector` is strongly
    recommended (clip to the relevant Reddit comment / tweet card / chart);
    without one we capture the viewport, which is rarely useful for cited
    visuals.

    Sub-types (`sub=reddit-comment|tweet|news-quote|competitor-ui|chart`) are
    free-form metadata at the moment — they round-trip into the manifest for
    downstream tooling (e.g. /capture-visuals retry) but don't change capture
    behavior. Per-sub heuristics (e.g. auto-pick `article > figure` for
    `sub=news-quote`) can layer on later without breaking the placeholder
    grammar.
    """
    a = item["attrs"]
    url = a.get("url")
    if not url:
        return {"status": "failed", "reason": "external_visual_missing_url"}
    sub = (a.get("sub") or "external").lower()
    name = _slug(a.get("what") or sub)
    out_path = out_dir / f"external-{index}-{name}.png"

    result = _capture_with_playwright(item, url, out_path, default_padding=48)
    result.setdefault("sub", sub)
    return _attach_chrome_fallback_hint(result, slug, item)


def _handle_image(item: dict[str, Any], slug: str, index: int, out_dir: Path) -> dict[str, Any]:
    a = item["attrs"]
    safety = (a.get("safety") or "sfw").lower()
    if safety == "adult":
        return {
            "status": "manual",
            "reason": "adult_content_routed_manual",
            "prompt": a.get("prompt", ""),
            "filename": f"image-{index}-{_slug(a.get('prompt', 'adult'))}.png",
            "hint": "produce manually via pleasur.ai/generate",
        }
    prompt = a.get("prompt") or a.get("what") or ""
    if not prompt:
        return {"status": "failed", "reason": "no_prompt"}
    name = _slug(prompt)
    out_path = out_dir / f"image-{index}-{name}.png"

    module = _load_generate_image()
    if module is None:
        return {"status": "manual", "reason": "replicate_unavailable", "prompt": prompt, "filename": out_path.name}

    style_suffix = a.get("style_suffix")
    model = a.get("model", module.DEFAULT_MODEL)
    return module.generate(prompt, out_path, model=model, style_suffix=style_suffix, safety=safety)


def _handle_action_shot(item: dict[str, Any], slug: str, index: int, out_dir: Path) -> dict[str, Any]:
    """Multi-step capture for visuals that require actions (click through age
    gate, log in, open settings panel, send a message, etc.) before the
    capture point.

    Default: routes to manual-capture so the editor handles it interactively
    via Claude in Chrome. The editor has visibility, control, and a real
    Chrome session — better than handing it to a paid AI agent.

    Opt-in: set BROWSER_USE_ENABLED=1 to fall back to the Browser Use Cloud
    agent (requires BROWSER_USE_API_KEY and burns LLM tokens per task).
    """
    a = item["attrs"]
    goal = a.get("goal") or a.get("what")
    if not goal:
        return {"status": "failed", "reason": "no_goal_for_action_shot"}
    start_url = a.get("url") or (
        _resolve_brand_url(a["target"]) if a.get("target") else None
    )
    name = _slug(goal)
    out_path = out_dir / f"action-{index}-{name}.png"

    if os.environ.get("BROWSER_USE_ENABLED", "").lower() not in {"1", "true", "yes"}:
        return {
            "status": "manual",
            "reason": "action_shot_routed_to_editor",
            "url": start_url,
            "goal": goal,
            "filename": out_path.name,
            "hint": (
                "Capture interactively via Claude in Chrome. Run "
                "`/capture-visuals " + slug + "` and walk through this entry, "
                "or open the URL in Chrome and capture the moment described in 'goal' yourself."
            ),
        }

    module = _load_run_action_shot()
    if module is None:
        return {
            "status": "manual",
            "reason": "browser_use_sdk_not_installed",
            "filename": out_path.name,
            "hint": "pip install browser-use-sdk",
        }
    max_steps_attr = a.get("max_steps")
    try:
        max_steps = int(max_steps_attr) if max_steps_attr else int(os.environ.get("BROWSER_USE_MAX_STEPS", "25"))
    except (TypeError, ValueError):
        max_steps = 25
    llm = a.get("llm") or os.environ.get("BROWSER_USE_LLM", "claude-sonnet-4-6")

    result = module.run(
        goal,
        out_path,
        start_url=start_url,
        max_steps=max_steps,
        llm=llm,
    )
    if start_url:
        result.setdefault("url", start_url)
    return result


def _resolve_chart_data(data: str, slug: str) -> tuple[str | None, str | None]:
    """Resolve a chart data spec to something render_chart.py can consume.

    Returns (resolved_spec, error_reason). Exactly one is non-None.

    Supported forms:
      - inline JSON object/list — passed through
      - path:KEY — passed through (render_chart resolves it directly)
      - research.<key> — looks up <key> in content-pipeline/1-research/{slug}-data.json
        and substitutes the resolved JSON. The data file is the contract between
        /research and /generate-visuals; the research stage emits it whenever
        chartable numbers are surfaced.
    """
    spec = (data or "").strip()
    if not spec:
        return None, "no_data_spec"
    if spec.startswith("{") or spec.startswith("[") or ":" in spec:
        return spec, None
    if spec.startswith("research."):
        key = spec[len("research."):].strip()
        if not key:
            return None, "research_key_missing"
        data_file = ROOT / "content-pipeline" / "1-research" / f"{slug}-data.json"
        if not data_file.exists():
            return None, f"research_data_file_missing:{data_file.relative_to(ROOT)}"
        try:
            payload = json.loads(data_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return None, f"research_data_unreadable:{exc}"
        node: Any = payload
        for part in key.split("."):
            if isinstance(node, dict) and part in node:
                node = node[part]
            else:
                return None, f"research_key_not_found:{key}"
        return json.dumps(node), None
    return None, f"unrecognized_data_form:{spec}"


def _handle_chart(item: dict[str, Any], slug: str, index: int, out_dir: Path) -> dict[str, Any]:
    a = item["attrs"]
    title = a.get("title") or a.get("what") or "Chart"
    style = (a.get("style") or "bar").lower()
    raw_data = a.get("data")
    name = _slug(title)
    out_path = out_dir / f"chart-{index}-{name}.png"

    resolved, err = _resolve_chart_data(raw_data, slug)
    if err is not None:
        return {
            "status": "manual",
            "reason": f"chart_data_unresolved:{err}",
            "filename": out_path.name,
            "hint": (
                "Add the data to content-pipeline/1-research/" + slug + "-data.json under "
                "the key the placeholder references, then re-run /generate-visuals. "
                "Or render manually: python .claude/skills/generate-visuals/scripts/render_chart.py "
                "--title \"" + title + "\" --style " + style + " --data '<inline JSON>' --out "
                + str(out_path.relative_to(ROOT))
            ),
        }

    module = _load_render_chart()
    if module is None:
        return {"status": "manual", "reason": "matplotlib_unavailable", "filename": out_path.name}

    return module.render(title, style, resolved, out_path, a.get("x_label"), a.get("y_label"))


def _handle_manual(item: dict[str, Any], index: int) -> dict[str, Any]:
    a = item["attrs"]
    return {
        "status": "manual",
        "reason": f"{item['type']}_requires_manual_capture",
        "url": a.get("url"),
        "what": a.get("what"),
        "filename": f"{item['type']}-{index}-{_slug(a.get('what') or item['type'])}.png",
    }


def _dispatch(item: dict[str, Any], slug: str, index: int, out_dir: Path) -> dict[str, Any]:
    t = item["type"]
    if t == "screenshot":
        return _handle_screenshot(item, slug, index, out_dir)
    if t == "action-shot":
        return _handle_action_shot(item, slug, index, out_dir)
    if t == "image":
        return _handle_image(item, slug, index, out_dir)
    if t == "chart":
        return _handle_chart(item, slug, index, out_dir)
    if t == "external":
        return _handle_external(item, slug, index, out_dir)
    if t in {"video", "gif"}:
        return _handle_manual(item, index)
    if t == "table" or t == "none":
        return {"status": "skip", "reason": f"type_{t}_not_an_asset"}
    return {"status": "failed", "reason": f"unknown_type_{t}"}


def _build_manual_capture_md(slug: str, manual_items: list[dict[str, Any]]) -> str:
    if not manual_items:
        return f"# Manual capture for {slug}\n\nNo manual visuals required.\n"
    lines = [f"# Manual capture for {slug}", "", "Each entry below needs the editor to capture or upload manually:", ""]
    for i, m in enumerate(manual_items, 1):
        item = m["item"]
        result = m["result"]
        lines.append(f"## {i}. {item['type']}: {_alt_text(item)}")
        lines.append("")
        lines.append(f"- **Reason:** {result.get('reason', 'manual')}")
        if result.get("url"):
            lines.append(f"- **Source URL:** {result['url']}")
        if item["attrs"].get("selector"):
            lines.append(f"- **Selector:** `{item['attrs']['selector']}`")
        if result.get("hint"):
            lines.append(f"- **Hint:** {result['hint']}")
        if result.get("prompt"):
            lines.append(f"- **Prompt:** {result['prompt']}")
        if result.get("fallback", {}).get("method") == "claude_in_chrome":
            lines.append(
                f"- **Fallback:** /capture-visuals (Claude-in-Chrome) — Playwright blocked, "
                f"retry via real Chrome session."
            )
        # Build a suggested filename even when the result didn't carry one
        # (`failed` results from capture_screenshot don't, but we still need
        # a stable name for /capture-visuals to write to).
        suggested = result.get("filename") or f"{item['type']}-{i}-{_slug(_alt_text(item))}.png"
        lines.append(f"- **Suggested filename:** `images/{slug}/{suggested}`")
        lines.append("")
        lines.append(f"Original placeholder: `{item['raw']}`")
        lines.append("")
    return "\n".join(lines)


def _rewrite_draft(text: str, replacements: list[tuple[str, str]]) -> str:
    """Apply each (old, new) replacement once, longest first to avoid prefix collisions."""
    seen: set[str] = set()
    for old, _ in replacements:
        seen.add(old)
    for old, new in sorted(replacements, key=lambda p: -len(p[0])):
        text = text.replace(old, new, 1)
    return text


def run(slug: str) -> int:
    draft_path = DRAFT_DIR / f"{slug}.md"
    if not draft_path.exists():
        sys.stderr.write(f"error: draft not found at {draft_path}\n")
        return 1

    out_dir = IMAGES_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    text = draft_path.read_text(encoding="utf-8")
    items = _find_placeholders(text)
    if not items:
        sys.stdout.write("no visual placeholders found; nothing to do.\n")
        manifest = {"slug": slug, "visuals": []}
        (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return 0

    manifest_entries: list[dict[str, Any]] = []
    replacements: list[tuple[str, str]] = []
    manual_items: list[dict[str, Any]] = []
    captured_paths: list[Path] = []

    for index, item in enumerate(items, 1):
        result = _dispatch(item, slug, index, out_dir)
        entry = {
            "index": index,
            "type": item["type"],
            "attrs": item["attrs"],
            "alt": _alt_text(item),
            "status": result.get("status"),
            "result": result,
            "raw": item["raw"],
            "legacy": item.get("legacy", False),
        }
        manifest_entries.append(entry)

        if result.get("status") == "captured":
            asset_path = result["path"]
            if isinstance(asset_path, str) and not asset_path.startswith(("http://", "https://")):
                rel = asset_path.replace("\\", "/")
                if rel.startswith("content-pipeline/"):
                    rel = rel.replace("content-pipeline/", "", 1)
                replacements.append((item["raw"], f"![{_alt_text(item)}]({rel})"))
                captured_paths.append(ROOT / asset_path)
        elif result.get("status") == "manual":
            manual_items.append({"item": item, "result": result})
        elif result.get("status") == "failed":
            # Treat failed captures the same as manual: editor needs to act.
            # Surface the reason so they know it's a CF block / API rejection
            # / etc. and not a missing placeholder.
            manual_items.append({"item": item, "result": result})
        elif result.get("status") == "skip":
            replacements.append((item["raw"], ""))

    if captured_paths:
        opt = _load_optimizer()
        if opt is not None:
            for p in captured_paths:
                opt.optimize(p)

    new_text = _rewrite_draft(text, replacements)
    if new_text != text:
        draft_path.write_text(new_text, encoding="utf-8")

    (out_dir / "manifest.json").write_text(
        json.dumps({"slug": slug, "visuals": manifest_entries}, indent=2),
        encoding="utf-8",
    )
    (out_dir / "manual-capture.md").write_text(_build_manual_capture_md(slug, manual_items), encoding="utf-8")

    summary = {
        "captured": sum(1 for e in manifest_entries if e["status"] == "captured"),
        "manual": sum(1 for e in manifest_entries if e["status"] == "manual"),
        "failed": sum(1 for e in manifest_entries if e["status"] == "failed"),
        "skipped": sum(1 for e in manifest_entries if e["status"] == "skip"),
        "total": len(manifest_entries),
    }
    sys.stdout.write(json.dumps(summary, indent=2) + "\n")
    sys.stdout.write(f"manifest: {out_dir / 'manifest.json'}\n")
    sys.stdout.write(f"manual-capture: {out_dir / 'manual-capture.md'}\n")
    return 0


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(
        description="Realize [VISUAL:...] placeholders in a cited draft into actual assets.",
    )
    parser.add_argument("slug", help="The slug of the cited draft to process")
    args = parser.parse_args()
    return run(args.slug)


if __name__ == "__main__":
    sys.exit(main())
