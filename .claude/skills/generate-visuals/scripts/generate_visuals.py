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
import subprocess
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


def _load_animate_demo():
    sys.path.insert(0, str(SCRIPT_DIR))
    try:
        import animate_demo  # type: ignore
        return animate_demo
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Engine subprocess plumbing (web-render + AI engines)
# ---------------------------------------------------------------------------
# The deterministic web engines (render_chart_web.py / render_diagram_web.py /
# render_table_card.py / render_cover.py / annotate_screenshot.py) and the gated
# AI engines (infographic_engine.js / concept_illustration_engine.js +
# composite_logo.py) all expose a CLI and run *inside the container* (patchright
# + chromium + node + bundled apexcharts/dagre). We call them as subprocesses
# rather than importing them, exactly the way the recipes document them. No
# silent fallbacks: a non-zero exit, a missing output file, or an engine
# `status != captured` becomes a loud `failed` entry in the manifest — never a
# substitution.

# Default engine timeout (s). Headless-browser renders + Nano-Banana calls can
# take a while; keep generous but bounded so a hung engine can't wedge the run.
_ENGINE_TIMEOUT = int(os.environ.get("VISUAL_ENGINE_TIMEOUT", "240"))


def _engine_path(name: str) -> Path:
    return SCRIPT_DIR / name


def _run_engine(cmd: list[str]) -> dict[str, Any]:
    """Run an engine CLI as a subprocess; return a structured result.

    Returns {ok, returncode, stdout, stderr}. Never raises for an engine
    failure — the caller decides how to surface it (so each visual type can
    loud-fail into the manifest individually).
    """
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(SCRIPT_DIR),
            capture_output=True,
            text=True,
            timeout=_ENGINE_TIMEOUT,
        )
    except FileNotFoundError as exc:
        return {"ok": False, "returncode": 127, "stdout": "", "stderr": f"executable_not_found: {exc}"}
    except subprocess.TimeoutExpired as exc:
        # With text=True the partial stdout is usually str, but on a mid-stream
        # kill it can be bytes — decode defensively so it never lands as bytes in
        # the manifest JSON (which would crash json.dumps).
        return {"ok": False, "returncode": -1,
                "stdout": _as_text(exc.stdout),
                "stderr": f"engine_timeout_{_ENGINE_TIMEOUT}s"}
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": _as_text(proc.stdout),
        "stderr": _as_text(proc.stderr),
    }


def _as_text(val: Any) -> str:
    if val is None:
        return ""
    if isinstance(val, bytes):
        return val.decode("utf-8", errors="replace")
    return str(val)


def _last_json_line(text: str) -> dict[str, Any] | None:
    """Parse the last JSON object printed on stdout (the web engines' contract)."""
    for line in reversed([ln.strip() for ln in text.splitlines() if ln.strip()]):
        if line.startswith("{") and line.endswith("}"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    return None


def _rel_to_root(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _spec_to_tempfile(spec: Any, out_dir: Path, stem: str) -> Path:
    """Write a JSON spec next to the output so engines that want a --config /
    --content / --spec FILE (not inline) can read it. Kept on disk (not
    auto-deleted) so a failed render leaves the exact spec for debugging."""
    p = out_dir / f".{stem}.spec.json"
    p.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    return p


def _engine_captured(result: dict[str, Any], out_path: Path, *, engine: str,
                     extra: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a `captured` manifest result for a web engine that printed
    {"status":"captured","path":...} and actually wrote the file."""
    payload = _last_json_line(result["stdout"])
    if not result["ok"]:
        return _engine_failed(result, engine=engine, out_path=out_path,
                              reason=(payload or {}).get("reason"))
    if not payload or payload.get("status") != "captured":
        return _engine_failed(result, engine=engine, out_path=out_path,
                              reason=(payload or {}).get("reason") or "engine_no_captured_status")
    if not out_path.exists() or out_path.stat().st_size == 0:
        return _engine_failed(result, engine=engine, out_path=out_path,
                              reason="engine_output_missing")
    entry: dict[str, Any] = {
        "status": "captured",
        "path": _rel_to_root(out_path),
        "engine": engine,
    }
    if extra:
        entry.update(extra)
    return entry


def _engine_failed(result: dict[str, Any], *, engine: str, out_path: Path,
                   reason: str | None = None) -> dict[str, Any]:
    """Loud failure: capture enough of stderr/stdout to debug, no substitution."""
    tail = (result.get("stderr") or result.get("stdout") or "").strip()
    return {
        "status": "failed",
        "reason": reason or "engine_error",
        "engine": engine,
        "returncode": result.get("returncode"),
        "filename": out_path.name,
        "error": tail[-500:],
    }


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


# Style-suffix defaults per `sub` (PLEAA-499) — the dispatcher prepends these
# hints when the placeholder doesn't override `style_suffix` explicitly. Diagram
# / concept-illustration prompts default to the clean editorial style that
# reads well in a blog post; lifestyle keeps the photorealistic tone.
_IMAGE_SUB_STYLE_DEFAULTS = {
    "concept-illustration": "Clean editorial illustration style, white background, sans-serif labels, brand-neutral colors, no text artifacts.",
    "diagram": "Clean editorial illustration style, white background, sans-serif labels, brand-neutral colors, clear arrows and connectors, no text artifacts.",
    "flow-diagram": "Clean editorial flow-diagram illustration, white background, sans-serif labels, directional arrows between components, brand-neutral colors, no text artifacts.",
    "comparison": "Clean editorial side-by-side comparison illustration, white background, sans-serif labels, balanced left/right layout, brand-neutral colors, no text artifacts.",
    "lifestyle": "Editorial photorealistic style, natural lighting, no people unless prompt specifies, no readable text on screens.",
}


def _handle_image(item: dict[str, Any], slug: str, index: int, out_dir: Path) -> dict[str, Any]:
    """AI image generation is RETIRED (Ryan-faithful rebuild, 2026-06-25).

    Ryan Law does blog images by hand; we don't spend on generated imagery and we
    don't ship AI-illustrated concept art. An `image` placeholder is therefore
    `drop`ped from the draft (the placeholder is stripped — no naked [VISUAL:] left
    to fail the gate, no Replicate call) and logged as a non-blocking manual TODO so
    an editor can add a real screenshot/diagram later if the visual genuinely earns
    its place. Prefer `type=screenshot` (real brand UI) or `type=chart`/`type=table`
    (real data) at outline/draft time instead of `type=image`.
    """
    a = item["attrs"]
    prompt = a.get("prompt") or a.get("what") or ""
    name = _slug(prompt or "image")
    return {
        "status": "drop",
        "reason": "ai_image_gen_retired",
        "prompt": prompt,
        "filename": f"image-{index}-{name}.png",
        "hint": "AI image generation is retired. Add a real screenshot/diagram by hand if this visual earns its place; otherwise the article ships without it (text publish is not blocked).",
    }


def _handle_action_shot(item: dict[str, Any], slug: str, index: int, out_dir: Path) -> dict[str, Any]:
    """Multi-step / stateful capture → action_shot.run (deterministic patchright +
    brand frame). The default now (per ACTION-SHOT-RECIPE.md): our own retina
    capture, Cloudflare bypass, 18+-gate dismissal, on-brand frame — free, no paid
    cloud agent, no per-task LLM spend.

    `goal` (or `what`) describes the capture; `url`/`target` give the start. Public
    presets (pricing) work today. Logged-in shots (chat/call/gallery) need the
    showcase session minted by setup_auth.py — without it action_shot returns
    `reason:"session_required"`, which we surface as a `manual` entry (showcase-
    login dependency) rather than a hard fail. Cloudflare/nav blocks come back
    `failed` (the gate halts) — no silent substitution either way.
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

    module = _load_run_action_shot()
    if module is None:
        return {
            "status": "manual",
            "reason": "action_shot_engine_unavailable",
            "url": start_url,
            "goal": goal,
            "filename": out_path.name,
            "hint": (
                "action_shot.py could not be imported (patchright missing?). Capture "
                "interactively via `/capture-visuals " + slug + "` instead."
            ),
        }

    max_steps_attr = a.get("max_steps")
    try:
        max_steps = int(max_steps_attr) if max_steps_attr else int(os.environ.get("BROWSER_USE_MAX_STEPS", "25"))
    except (TypeError, ValueError):
        max_steps = 25
    llm = a.get("llm") or os.environ.get("BROWSER_USE_LLM", "claude-sonnet-4-6")

    try:
        result = module.run(
            goal,
            out_path,
            start_url=start_url,
            max_steps=max_steps,
            llm=llm,
        )
    except Exception as exc:  # never let one capture crash the whole stage
        return {"status": "failed", "reason": "action_shot_engine_error",
                "error": str(exc)[:300], "filename": out_path.name, "url": start_url}

    if start_url:
        result.setdefault("url", start_url)

    # Normalize a captured absolute path to ROOT-relative for the rewrite step.
    if result.get("status") == "captured" and isinstance(result.get("path"), str):
        result["path"] = _rel_to_root(Path(result["path"]))

    # The showcase-account dependency is an operator follow-up, not a content
    # failure: surface it as `manual` so the gate doesn't permanently halt on it.
    if result.get("status") == "failed" and result.get("reason") == "session_required":
        return {
            "status": "manual",
            "reason": "session_required",
            "url": start_url,
            "goal": goal,
            "filename": out_path.name,
            "hint": (
                "Logged-in action-shot needs the Pleasur.AI showcase session. Mint it "
                "once with `python .claude/skills/generate-visuals/scripts/setup_auth.py "
                "--interactive --headed` (calls need Standard+), then re-run /generate-visuals."
            ),
        }
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


def _resolve_structured_data(data: str, slug: str) -> tuple[str | None, str | None]:
    """Resolve a structured-data spec for the diagram / table / AI-content engines.

    Like `_resolve_chart_data` but WITHOUT the bare-`:` passthrough (that sugar is
    chart-only and would wrongly accept prose like "Step 1: foo" or a Windows path
    as valid data). Accepts:
      - inline JSON object/list — passed through
      - research.<key> — resolved against content-pipeline/1-research/{slug}-data.json
      - path:KEY — passed through (engines that accept path:KEY resolve it themselves)
    Anything else returns a clear `unrecognized_data_form` error so authoring
    feedback is precise. Returns (resolved, error); exactly one is non-None.
    """
    spec = (data or "").strip()
    if not spec:
        return None, "no_data_spec"
    if spec.startswith("{") or spec.startswith("["):
        return spec, None
    if spec.startswith("path:"):
        return spec, None
    if spec.startswith("research."):
        return _resolve_chart_data(spec, slug)
    return None, f"unrecognized_data_form:{spec}"


# Chart-kind aliases → render_chart_web.py `--type` values.
_CHART_TYPES = {"area", "line", "bar", "bar_h", "donut"}
_CHART_TYPE_ALIASES = {
    "column": "bar", "vertical_bar": "bar", "vbar": "bar",
    "horizontal_bar": "bar_h", "hbar": "bar_h", "barh": "bar_h",
    "pie": "donut", "doughnut": "donut",
    "spline": "line", "trend": "line",
    "stacked": "bar",
}


def _chart_type(raw: str | None) -> str:
    t = (raw or "bar").lower().strip()
    if t in _CHART_TYPES:
        return t
    return _CHART_TYPE_ALIASES.get(t, "bar")


def _handle_chart(item: dict[str, Any], slug: str, index: int, out_dir: Path) -> dict[str, Any]:
    """Chart → render_chart_web.py (ApexCharts headless, brand theme + real logo).

    Replaces the old matplotlib render_chart.py. `style=`/`chart_type=` selects the
    ApexCharts kind (bar|bar_h|area|line|donut); `data=` is inline JSON, `path:KEY`,
    or `research.<key>` (resolved against content-pipeline/1-research/<slug>-data.json).
    A `config=` path (full ApexCharts options JSON, e.g. from the apexcharts skill)
    takes precedence over `data` for the 16 advanced chart types.

    No silent fallback: prose/unresolvable `data` and engine errors loud-fail into
    the manifest as `failed` (the visuals gate then halts) — never substituted.
    """
    a = item["attrs"]
    title = a.get("title") or a.get("what") or "Chart"
    ctype = _chart_type(a.get("chart_type") or a.get("style"))
    name = _slug(title)
    out_path = out_dir / f"chart-{index}-{name}.png"

    cmd = [sys.executable, str(_engine_path("render_chart_web.py")),
           "--title", title, "--out", str(out_path)]
    if a.get("subtitle"):
        cmd += ["--subtitle", a["subtitle"]]

    config = a.get("config")
    if config:
        config_path = (ROOT / config) if not os.path.isabs(config) else Path(config)
        if not config_path.exists():
            return {"status": "failed", "reason": f"chart_config_missing:{config}",
                    "filename": out_path.name}
        cmd += ["--config", str(config_path)]
    else:
        resolved, err = _resolve_chart_data(a.get("data"), slug)
        if err is not None:
            # Loud-fail (NOT manual): unresolved data is a real authoring gap.
            return {
                "status": "failed",
                "reason": f"chart_data_unresolved:{err}",
                "filename": out_path.name,
                "hint": (
                    "Provide chartable data: add it to content-pipeline/1-research/"
                    + slug + "-data.json under the key the placeholder references "
                    "(data=research.<key>), or inline JSON in data=, or a full "
                    "ApexCharts options file via config=. Free-text data= cannot be charted."
                ),
            }
        if resolved.strip() in {"[]", "{}", "null"}:
            return {"status": "failed", "reason": "chart_data_empty",
                    "filename": out_path.name,
                    "hint": "The referenced chart data resolved to an empty value — "
                            "the research key exists but holds no numbers."}
        cmd += ["--type", ctype, "--data", resolved]

    return _engine_captured(_run_engine(cmd), out_path, engine="render_chart_web",
                            extra={"chart_type": "config" if config else ctype})


# Diagram-kind aliases → render_diagram_web.py `--type`.
_DIAGRAM_TYPES = {"linear", "tree", "flow", "cycle"}
_DIAGRAM_TYPE_ALIASES = {
    "process": "linear", "steps": "linear", "step": "linear", "sequence": "linear",
    "decision": "tree", "decision-tree": "tree", "decision_tree": "tree",
    "flowchart": "flow", "flow-chart": "flow",
    "loop": "cycle", "feedback": "cycle", "cyclic": "cycle",
}


def _diagram_type(raw: str | None) -> str:
    t = (raw or "linear").lower().strip()
    if t in _DIAGRAM_TYPES:
        return t
    return _DIAGRAM_TYPE_ALIASES.get(t, "linear")


def _handle_diagram(item: dict[str, Any], slug: str, index: int, out_dir: Path) -> dict[str, Any]:
    """Diagram → render_diagram_web.py (dagre auto-layout + brand-card renderer).

    Clean process flows / decision trees / flow charts / cycles. Needs STRUCTURED
    input: `data=` inline JSON (list of steps / nested tree / list of cycle nodes)
    or `config=` a path to a full {direction,nodes,edges} spec JSON. `style=`/
    `diagram_type=` picks linear|tree|flow|cycle (aliases: process/decision/flowchart/loop).

    A diagram described only in prose (`what=...`, no `data`/`config`) CANNOT be
    rendered deterministically — it loud-fails as `failed` with a hint to add
    structured data, rather than silently substituting anything.
    """
    a = item["attrs"]
    title = a.get("title") or a.get("what") or "Diagram"
    dtype = _diagram_type(a.get("diagram_type") or a.get("style"))
    name = _slug(a.get("title") or a.get("what") or "diagram")
    out_path = out_dir / f"diagram-{index}-{name}.png"

    cmd = [sys.executable, str(_engine_path("render_diagram_web.py")),
           "--title", title, "--out", str(out_path)]
    if a.get("subtitle"):
        cmd += ["--subtitle", a["subtitle"]]
    if a.get("direction") in {"LR", "TB"}:
        cmd += ["--direction", a["direction"]]

    config = a.get("config")
    if config:
        config_path = (ROOT / config) if not os.path.isabs(config) else Path(config)
        if not config_path.exists():
            return {"status": "failed", "reason": f"diagram_config_missing:{config}",
                    "filename": out_path.name}
        cmd += ["--config", str(config_path)]
    else:
        data = (a.get("data") or "").strip()
        if not data:
            return {
                "status": "failed",
                "reason": "diagram_requires_structured_data",
                "filename": out_path.name,
                "hint": (
                    "render_diagram_web.py needs structured nodes, not prose. Add "
                    "data=research.<key> (resolved from content-pipeline/1-research/"
                    "<slug>-data.json) or config=<path to a {direction,nodes,edges} spec>. "
                    "linear: a list of {label,desc}; tree: a nested {label,children}; "
                    "cycle: a list of {label,icon}. See DIAGRAM-THEME.md."
                ),
            }
        # Inline JSON (rare — the [VISUAL:] grammar truncates at the first ']',
        # so bracketed JSON can't survive in a placeholder; research.<key>/path:KEY
        # is the practical form) OR a resolver reference.
        if data.startswith("{") or data.startswith("["):
            resolved = data
        else:
            resolved, err = _resolve_structured_data(data, slug)
            if err is not None:
                return {
                    "status": "failed",
                    "reason": f"diagram_data_unresolved:{err}",
                    "filename": out_path.name,
                    "hint": (
                        "diagram data= must be a research.<key> reference (resolved from "
                        "content-pipeline/1-research/" + slug + "-data.json), a path:KEY, or "
                        "use config=<path> for a full {direction,nodes,edges} spec."
                    ),
                }
        if resolved.strip() in {"[]", "{}", "null"}:
            return {"status": "failed", "reason": "diagram_data_empty",
                    "filename": out_path.name,
                    "hint": "The referenced diagram data resolved to an empty value."}
        cmd += ["--type", dtype, "--data", resolved]

    return _engine_captured(_run_engine(cmd), out_path, engine="render_diagram_web",
                            extra={"diagram_type": "config" if config else dtype})


def _build_table_spec(a: dict[str, str], slug: str, title: str) -> tuple[dict[str, Any] | None, str | None]:
    """Build a render_table_card.py spec from [VISUAL] attrs.

    Forms supported (matching how drafts write table/comparison placeholders):
      - config=<path> / spec=<path>  → load that spec JSON verbatim.
      - data=<inline JSON object>    → a full spec object, passed through.
      - data=research.<key> / path:KEY → resolve to a spec object or a rows array.
      - columns=A,B,C (+ data=rows)  → generic GFM-style table; rows from data or empty.
    Returns (spec, error). Exactly one is non-None.
    """
    spec_path = a.get("config") or a.get("spec")
    if spec_path:
        p = (ROOT / spec_path) if not os.path.isabs(spec_path) else Path(spec_path)
        if not p.exists():
            return None, f"table_spec_missing:{spec_path}"
        try:
            return json.loads(p.read_text(encoding="utf-8")), None
        except (OSError, json.JSONDecodeError) as exc:
            return None, f"table_spec_unreadable:{exc}"

    raw = (a.get("data") or "").strip()
    resolved_obj: Any = None
    if raw:
        if raw.startswith("{") or raw.startswith("["):
            try:
                resolved_obj = json.loads(raw)
            except json.JSONDecodeError as exc:
                return None, f"table_data_bad_json:{exc}"
        else:
            # research.<key> / path:KEY — reuse the chart resolver (same contract).
            resolved, err = _resolve_chart_data(raw, slug)
            if err is not None:
                return None, f"table_data_unresolved:{err}"
            try:
                resolved_obj = json.loads(resolved)
            except json.JSONDecodeError as exc:
                return None, f"table_data_bad_json:{exc}"

    # A fully-formed spec object (has type/rows/columns) is passed through, with
    # the placeholder title/subtitle filled in if the spec omits them.
    if isinstance(resolved_obj, dict) and ("rows" in resolved_obj or "items" in resolved_obj or "columns" in resolved_obj):
        spec = dict(resolved_obj)
        spec.setdefault("title", title)
        if a.get("subtitle"):
            spec.setdefault("subtitle", a["subtitle"])
        if a.get("comparison_type") and "type" not in spec:
            spec["type"] = a["comparison_type"]
        return spec, None

    # columns=A,B,C → generic table; rows come from a resolved list (if any).
    cols_attr = a.get("columns")
    if cols_attr:
        columns = [c.strip() for c in cols_attr.split(",") if c.strip()]
        rows: list[Any] = []
        if isinstance(resolved_obj, list):
            rows = resolved_obj
        elif isinstance(resolved_obj, dict) and isinstance(resolved_obj.get("rows"), list):
            rows = resolved_obj["rows"]
        spec: dict[str, Any] = {"type": "table", "title": title, "columns": columns, "rows": rows}
        if a.get("subtitle"):
            spec["subtitle"] = a["subtitle"]
        return spec, None

    return None, "table_no_spec_columns_or_data"


def _handle_table(item: dict[str, Any], slug: str, index: int, out_dir: Path) -> dict[str, Any]:
    """Table / comparison / pricing / grid → render_table_card.py (brand table card).

    Deterministic crisp text (never an image model). Spec is built from the
    placeholder attrs: `config=`/`spec=` path, an inline `data=` spec object,
    `data=research.<key>` resolving to a spec/rows, or `columns=A,B,C` for a
    generic GFM table. Loud-fails (no substitution) when no usable spec exists or
    the engine errors.
    """
    a = item["attrs"]
    title = a.get("title") or a.get("what") or "Comparison"
    name = _slug(a.get("title") or a.get("what") or item["type"])
    out_path = out_dir / f"table-{index}-{name}.png"

    spec, err = _build_table_spec(a, slug, title)
    if err is not None:
        return {
            "status": "failed",
            "reason": err,
            "filename": out_path.name,
            "hint": (
                "Provide the table data: columns=A,B,C with rows in data= (inline "
                "JSON list or research.<key>), or a full spec via config=<path> / "
                "inline data=<spec object>. See COMPARISON-TABLE.md."
            ),
        }

    spec_file = _spec_to_tempfile(spec, out_dir, f"table-{index}")
    cmd = [sys.executable, str(_engine_path("render_table_card.py")),
           "--spec", str(spec_file), "--out", str(out_path)]
    return _engine_captured(_run_engine(cmd), out_path, engine="render_table_card",
                            extra={"table_type": spec.get("type", "table")})


def _handle_cover(item: dict[str, Any], slug: str, index: int, out_dir: Path) -> dict[str, Any]:
    """Cover / hero → render_cover.py (deterministic line-art, free, no AI).

    The article featured image (1600×900). We route to the free deterministic
    engine (render_cover.py) — never the AI cover lane — so the auto-pipeline
    stays cost-free and SFW. `title` is required (defaults to the article title via
    `what`); `theme` (light|dark|bold|aurora), `accent`, `eyebrow`/`subtitle`,
    `icon`, `motif` map straight to flags. `content=<path>` (a cover JSON) wins.
    """
    a = item["attrs"]
    name = _slug(a.get("title") or a.get("what") or slug)
    out_path = out_dir / f"cover-{index}-{name}.png"
    cmd = [sys.executable, str(_engine_path("render_cover.py")), "--out", str(out_path)]

    content = a.get("content")
    if content:
        content_path = (ROOT / content) if not os.path.isabs(content) else Path(content)
        if not content_path.exists():
            return {"status": "failed", "reason": f"cover_content_missing:{content}",
                    "filename": out_path.name}
        cmd += ["--content", str(content_path)]
    else:
        title = a.get("title") or a.get("what")
        if not title:
            return {"status": "failed", "reason": "cover_requires_title",
                    "filename": out_path.name,
                    "hint": "Add title= (or what=) — the cover needs the article title."}
        cmd += ["--title", title]
        if a.get("eyebrow"):
            cmd += ["--eyebrow", a["eyebrow"]]
        if a.get("subtitle"):
            cmd += ["--subtitle", a["subtitle"]]
        if a.get("theme") in {"light", "dark", "bold", "aurora"}:
            cmd += ["--theme", a["theme"]]
        if a.get("accent"):
            cmd += ["--accent", a["accent"]]
        if a.get("icon"):
            cmd += ["--icon", a["icon"]]
        if a.get("motif"):
            cmd += ["--motif", a["motif"]]

    return _engine_captured(_run_engine(cmd), out_path, engine="render_cover")


def _handle_annotation(item: dict[str, Any], slug: str, index: int, out_dir: Path) -> dict[str, Any]:
    """Annotation → annotate_screenshot.py --strict (callout boxes/arrows on a shot).

    A screenshot of a brand URL with numbered highlight boxes/labels drawn on
    target elements. `url` required; `targets=` is a JSON array of
    {selector, kind?, label?, corner?} (or a single `selector=` is wrapped into
    one target). `dismiss=` clicks an exact-text element first (age/cookie gate);
    `color=` sets the highlight colour.

    Always runs with `--strict` (mandate: a missing target HARD-FAILS, never a
    silent skip). The engine writes <out>_report.json; we read it for the loud
    failure detail. No silent fallback.
    """
    a = item["attrs"]
    url = a.get("url") if "url" in a else _resolve_brand_url(a.get("target") or "create")
    name = _slug(a.get("what") or a.get("target") or "annotation")
    out_path = out_dir / f"annotation-{index}-{name}.png"

    # Build the targets array.
    targets: Any
    raw_targets = a.get("targets")
    if raw_targets:
        try:
            targets = json.loads(raw_targets)
        except json.JSONDecodeError as exc:
            return {"status": "failed", "reason": f"annotation_targets_bad_json:{exc}",
                    "filename": out_path.name}
    elif a.get("selector") or a.get("annotate"):
        sel = a.get("annotate") or a.get("selector")
        targets = [{"selector": sel, "kind": a.get("kind", "box"),
                    "label": a.get("label") or a.get("what")}]
    else:
        return {"status": "failed", "reason": "annotation_requires_targets_or_selector",
                "filename": out_path.name,
                "hint": "Add targets=<JSON array of {selector,kind,label}> or a single selector=."}

    cmd = [sys.executable, str(_engine_path("annotate_screenshot.py")),
           "--url", url, "--out", str(out_path),
           "--targets", json.dumps(targets), "--strict"]
    if a.get("dismiss"):
        cmd += ["--dismiss", a["dismiss"]]
    if a.get("color"):
        cmd += ["--color", a["color"]]

    result = _run_engine(cmd)
    # annotate_screenshot prints "DREW -> <out>" + a *_report.json; --strict
    # exits non-zero when a target is missing/overlapping.
    report_path = Path(str(out_path).rsplit(".", 1)[0] + "_report.json")
    report: dict[str, Any] = {}
    if report_path.exists():
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            report = {}
    missing = report.get("missing") or []
    overlaps = report.get("overlaps") or []
    file_ok = out_path.exists() and out_path.stat().st_size > 0
    # Loud-fail on a non-zero --strict exit, a missing output file, OR a report
    # that shows any unfound target / overlap (defense beyond the exit code — a
    # missing target must never be silently skipped, per the mandate).
    if not result["ok"] or not file_ok or missing or overlaps:
        return {
            "status": "failed",
            "reason": "annotation_strict_failed",
            "engine": "annotate_screenshot",
            "filename": out_path.name,
            "missing": missing,
            "overlaps": overlaps,
            "error": (result.get("stderr") or result.get("stdout") or "").strip()[-500:],
        }
    return {
        "status": "captured",
        "path": _rel_to_root(out_path),
        "engine": "annotate_screenshot",
        "url": url,
        "targets": report.get("targets"),
    }


def _handle_infographic(item: dict[str, Any], slug: str, index: int, out_dir: Path) -> dict[str, Any]:
    """Infographic → infographic_engine.js (Nano Banana) THEN composite_logo.py.

    Two-step gated-AI lane (hand-drawn-edu illustration + clean sans text + the
    real composited logo). Needs a `content=` JSON file (or inline `data=` spec
    object) of {title, subtitle, takeaway, items:[{icon,number,label,sublabel}]}.
    REPLICATE_API_KEY is mandatory in the engine (loud-fail, no fallback).

    Step 1 writes raw.png; step 2 stamps the real logo → final out_path. Any
    failure in either step is a loud `failed` (no substitution). Every output
    still owes the VISUAL-CRITIQUE-LOOP vision gate before publish.
    """
    a = item["attrs"]
    name = _slug(a.get("title") or a.get("what") or "infographic")
    out_path = out_dir / f"infographic-{index}-{name}.png"
    raw_path = out_dir / f".infographic-{index}-{name}.raw.png"

    content_path = _infographic_content_path(a, slug, out_dir, index)
    if isinstance(content_path, dict):
        return content_path  # an error result

    node = _node_bin()
    gen = _run_engine([node, str(_engine_path("infographic_engine.js")),
                       "--content", str(content_path), "--out", str(raw_path)])
    if not gen["ok"] or not raw_path.exists() or raw_path.stat().st_size == 0:
        return _engine_failed(gen, engine="infographic_engine", out_path=out_path,
                              reason="infographic_generate_failed")

    stamp = _run_engine([sys.executable, str(_engine_path("composite_logo.py")),
                         "--in", str(raw_path), "--out", str(out_path)])
    if not stamp["ok"] or not out_path.exists() or out_path.stat().st_size == 0:
        return _engine_failed(stamp, engine="composite_logo", out_path=out_path,
                              reason="infographic_logo_stamp_failed")
    return {"status": "captured", "path": _rel_to_root(out_path),
            "engine": "infographic_engine+composite_logo",
            "needs_vision_gate": True}


def _handle_concept_illustration(item: dict[str, Any], slug: str, index: int, out_dir: Path) -> dict[str, Any]:
    """Concept illustration → concept_illustration_engine.js (Nano Banana), then a
    deterministic palette gate (concept_palette_check.py).

    The single gated AI lane for a truly abstract concept (rare ~6% slot). Needs
    a `content=` JSON file (or inline `data=`) with {concept, metaphor, mood?,
    style?, aspect?}. REPLICATE_API_KEY mandatory (loud-fail, no fallback).

    After render we run the cheap palette check; a `WARN` is attached to the
    manifest (`palette_warn`) so the vision gate scrutinizes it — it does NOT
    auto-fail (the decisive gate is the agent's vision pass per
    VISUAL-CRITIQUE-LOOP.md). Composite logo is intentionally OFF for in-body
    illustrations (page chrome carries the brand). No silent fallback on errors.
    """
    a = item["attrs"]
    name = _slug(a.get("concept") or a.get("what") or "concept")
    out_path = out_dir / f"concept-{index}-{name}.png"

    content_path = _concept_content_path(a, slug, out_dir, index)
    if isinstance(content_path, dict):
        return content_path  # an error result

    node = _node_bin()
    cmd = [node, str(_engine_path("concept_illustration_engine.js")),
           "--content", str(content_path), "--out", str(out_path)]
    if a.get("style"):
        cmd += ["--style", a["style"]]
    if a.get("aspect"):
        cmd += ["--aspect", a["aspect"]]
    gen = _run_engine(cmd)
    if not gen["ok"] or not out_path.exists() or out_path.stat().st_size == 0:
        return _engine_failed(gen, engine="concept_illustration_engine", out_path=out_path,
                              reason="concept_illustration_generate_failed")

    # Deterministic first-filter palette check (advisory, not decisive).
    palette_warn = None
    chk = _run_engine([sys.executable, str(_engine_path("concept_palette_check.py")),
                       "--in", str(out_path), "--json"])
    payload = _last_json_line(chk["stdout"])
    if payload and payload.get("verdict") == "WARN":
        palette_warn = {"brand_pct": payload.get("brand_pct"), "off_pct": payload.get("off_pct")}

    return {"status": "captured", "path": _rel_to_root(out_path),
            "engine": "concept_illustration_engine",
            "needs_vision_gate": True,
            "palette_warn": palette_warn}


def _node_bin() -> str:
    return os.environ.get("NODE_BIN", "node")


def _content_from_attr(a: dict[str, str], slug: str, out_dir: Path, index: int, kind: str,
                       required_keys: tuple[str, ...]) -> Path | dict[str, Any]:
    """Resolve a `content=`/`data=` spec for the AI engines into a JSON file path.

    Accepts `content=<path>`, inline `data=<{...}>`, or `data=research.<key>`
    (resolved from content-pipeline/1-research/<slug>-data.json — same contract as
    chart/diagram). Returns a Path on success, or an error result dict (loud-fail)
    when no valid spec with the required keys is present.
    """
    content = a.get("content")
    if content:
        p = (ROOT / content) if not os.path.isabs(content) else Path(content)
        if not p.exists():
            return {"status": "failed", "reason": f"{kind}_content_missing:{content}",
                    "filename": f"{kind}-{index}.png"}
        return p
    raw = (a.get("data") or "").strip()
    if raw:
        if raw.startswith("{"):
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as exc:
                return {"status": "failed", "reason": f"{kind}_data_bad_json:{exc}",
                        "filename": f"{kind}-{index}.png"}
        else:
            # research.<key> / path:KEY → resolve to a spec object.
            resolved, err = _resolve_structured_data(raw, slug)
            if err is not None:
                return {"status": "failed", "reason": f"{kind}_data_unresolved:{err}",
                        "filename": f"{kind}-{index}.png"}
            try:
                obj = json.loads(resolved)
            except json.JSONDecodeError as exc:
                return {"status": "failed", "reason": f"{kind}_data_bad_json:{exc}",
                        "filename": f"{kind}-{index}.png"}
        if not isinstance(obj, dict):
            return {"status": "failed", "reason": f"{kind}_data_not_object",
                    "filename": f"{kind}-{index}.png"}
        missing = [k for k in required_keys if not obj.get(k)]
        if missing:
            return {"status": "failed", "reason": f"{kind}_missing_keys:{','.join(missing)}",
                    "filename": f"{kind}-{index}.png"}
        return _spec_to_tempfile(obj, out_dir, f"{kind}-{index}")
    return {"status": "failed", "reason": f"{kind}_requires_content",
            "filename": f"{kind}-{index}.png",
            "hint": f"Add content=<path to a {kind} JSON>, inline data=<spec with {', '.join(required_keys)}>, or data=research.<key>."}


def _infographic_content_path(a, slug, out_dir, index):
    return _content_from_attr(a, slug, out_dir, index, "infographic", ("title", "items"))


def _concept_content_path(a, slug, out_dir, index):
    return _content_from_attr(a, slug, out_dir, index, "concept", ("concept", "metaphor"))


def _handle_demo(item: dict[str, Any], slug: str, index: int, out_dir: Path) -> dict[str, Any]:
    """Animated product demo (4th visual type): a short looping GIF/MP4/WebP of a
    scripted pleasur.ai interaction, captured with patchright (headed under :99,
    clears Cloudflare + the 18+ gate) and wrapped in an on-brand browser frame.

    Placeholder grammar:
      [VISUAL:type=demo;scene=pricing-toggle;what=...]
      [VISUAL:type=demo;scene=path/to/scene.json;formats=gif,mp4;what=...]
      [VISUAL:type=demo;scene=chat-typing;auth=1;url=https://pleasur.ai/chat/<id>;what=...]

    Public scenes (pricing-toggle, pricing-scroll) run now. Auth scenes
    (chat-typing, image-generating, call) come back `manual` with the showcase-
    account dependency until a session is provided (see setup_auth.py).
    """
    a = item["attrs"]
    scene = a.get("scene") or a.get("preset")
    name = _slug(a.get("what") or scene or "demo")
    out_path = out_dir / f"demo-{index}-{name}.gif"
    if not scene:
        return {
            "status": "manual", "reason": "demo_requires_scene", "filename": out_path.name,
            "hint": "Add scene=<preset|path>. Presets: pricing-toggle, pricing-scroll, "
                    "chat-typing(auth), image-generating(auth), call(auth).",
        }
    module = _load_animate_demo()
    if module is None:
        return {"status": "manual", "reason": "animate_demo_unavailable", "filename": out_path.name}

    formats = [f.strip() for f in (a.get("formats") or "gif,mp4,webp").split(",") if f.strip()]
    truthy = {"1", "true", "yes"}
    try:
        res = module.generate(
            scene=scene, out=out_path, formats=formats,
            url=a.get("url"), caption=a.get("caption"),
            auth=(a.get("auth") or "").lower() in truthy,
            strict=(a.get("strict") or "").lower() in truthy,
            headed=True, max_width=int(a.get("max_width") or 940),
        )
    except Exception as exc:
        return {"status": "manual", "reason": "demo_engine_error",
                "error": str(exc)[:200], "filename": out_path.name}

    status = res.get("status")
    if status == "captured":
        gif = (res.get("outputs") or {}).get("gif") or {}
        gif_path = gif.get("path")
        if gif_path:
            try:
                res["path"] = str(Path(gif_path).relative_to(ROOT))
            except ValueError:
                res["path"] = gif_path
        # surface mp4/webp for the editor (MP4 is the preferred body embed)
        res["alt_formats"] = {k: (v or {}).get("path") for k, v in (res.get("outputs") or {}).items()
                              if k != "gif"}
        return res
    if status == "blocked_on_auth":
        return {
            "status": "manual", "reason": "blocked_on_auth", "filename": out_path.name,
            "scene": scene, "url": a.get("url") or res.get("url"),
            "hint": res.get("dependency"),
        }
    return {"status": "manual", "reason": res.get("error") or "demo_failed",
            "filename": out_path.name, "scene": scene}


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
    # --- Deterministic, free, on-brand engines (the common path) ---
    if t == "screenshot":
        return _handle_screenshot(item, slug, index, out_dir)
    if t == "chart":
        return _handle_chart(item, slug, index, out_dir)
    if t in {"table", "comparison", "pricing-table", "feature-table"}:
        return _handle_table(item, slug, index, out_dir)
    if t in {"diagram", "process", "decision-tree", "flowchart", "cycle"}:
        return _handle_diagram(item, slug, index, out_dir)
    if t in {"cover", "hero"}:
        return _handle_cover(item, slug, index, out_dir)
    if t == "annotation":
        return _handle_annotation(item, slug, index, out_dir)
    # --- Stateful capture (deterministic; showcase session for authed shots) ---
    if t == "action-shot":
        return _handle_action_shot(item, slug, index, out_dir)
    if t == "external":
        return _handle_external(item, slug, index, out_dir)
    # --- Animated demos (GIF/MP4/WebP) ---
    if t in {"demo", "animation", "video", "gif"}:
        return _handle_demo(item, slug, index, out_dir)
    # --- Gated AI lanes (Replicate; every output owes the vision gate) ---
    if t == "infographic":
        return _handle_infographic(item, slug, index, out_dir)
    if t in {"concept-illustration", "concept"}:
        return _handle_concept_illustration(item, slug, index, out_dir)
    # --- Retired / non-asset ---
    if t == "image":
        # AI image generation is retired: dropped + logged as a manual TODO.
        return _handle_image(item, slug, index, out_dir)
    if t == "card":
        # The blog has native stat/quote/callout components — not a generated
        # asset. Skip (strip the placeholder) so the gate doesn't choke on it.
        return {"status": "skip", "reason": "type_card_uses_native_components"}
    if t == "none":
        return {"status": "skip", "reason": "type_none_not_an_asset"}
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


def _visuals_enabled() -> bool:
    """Visual generation is ON by default (wired 2026-06-29).

    The full dispatcher routes every typed [VISUAL:...] to its on-brand engine
    (chart/diagram/table/cover/annotation deterministic + screenshot/action-shot/
    external capture + the gated AI infographic/concept-illustration lanes). Set
    BLOG_AGENT_VISUALS=off to fall back to the legacy no-op (placeholders left in
    place, no assets generated) — e.g. for a text-only dry run.
    """
    return os.environ.get("BLOG_AGENT_VISUALS", "on").lower() != "off"


def _run_deferred(slug: str, draft_path: Path, out_dir: Path, text: str, items: list[dict[str, Any]]) -> int:
    """No-op visuals path: leave placeholders untouched, write a `deferred` manifest.

    Generates nothing (no screenshots, no charts), does NOT rewrite the draft,
    and records every parsed placeholder as `{"type":..., "status":"deferred",
    "alt":...}` so downstream tooling can see where visuals will eventually go.
    Always returns success — the pipeline must never block on deferred visuals.
    """
    manifest_entries = [
        {"type": item["type"], "status": "deferred", "alt": _alt_text(item)}
        for item in items
    ]
    (out_dir / "manifest.json").write_text(
        json.dumps({"slug": slug, "visuals": manifest_entries}, indent=2),
        encoding="utf-8",
    )
    sys.stdout.write(
        f"visuals deferred (BLOG_AGENT_VISUALS=off) — {len(items)} placeholders left in place\n"
    )
    return 0


def run(slug: str) -> int:
    draft_path = DRAFT_DIR / f"{slug}.md"
    if not draft_path.exists():
        sys.stderr.write(f"error: draft not found at {draft_path}\n")
        return 1

    out_dir = IMAGES_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    text = draft_path.read_text(encoding="utf-8")
    items = _find_placeholders(text)

    if not _visuals_enabled():
        # Visual generation is deferred (its own future project). Leave every
        # placeholder in the draft as a marker, generate nothing, never block.
        return _run_deferred(slug, draft_path, out_dir, text, items)

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
            asset_path = result.get("path")
            if not asset_path:
                # Handler contract violation: captured without a path. Demote to
                # failed rather than crashing the whole run on a KeyError.
                entry["status"] = "failed"
                entry["result"] = {**result, "status": "failed",
                                   "reason": "captured_without_path"}
                manual_items.append({"item": item, "result": entry["result"]})
            elif isinstance(asset_path, str) and not asset_path.startswith(("http://", "https://")):
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
        elif result.get("status") == "drop":
            # Retired AI-image placeholder: strip it from the draft (no naked
            # [VISUAL:] left to fail the gate) and log a non-blocking manual TODO.
            replacements.append((item["raw"], ""))
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
