#!/usr/bin/env python3
"""Animated-demo engine — the 4th blog visual type.

Captures a SEQUENCE of frames of a scripted pleasur.ai interaction (patchright,
headed under DISPLAY=:99 — clears Cloudflare + the 18+ gate exactly like
capture_screenshot.py) and assembles a small, loopable GIF / MP4 / WebP, wrapped
in an on-brand "browser window" frame with the real Pleasur.ai logo.

Pipeline:  scene -> demo_capture.play -> demo_assemble.expand_segments
           -> demo_polish.compose_frames -> demo_polish.fit -> demo_assemble.assemble

CLI:
  python animate_demo.py --scene pricing-toggle --out content-pipeline/images/<slug>/pricing.gif
  python animate_demo.py --scene path/to/scene.json --out out.gif --formats gif,mp4
  python animate_demo.py --scene chat-typing --auth --url https://pleasur.ai/chat/<id> --out chat.gif

Library:
  import animate_demo; animate_demo.generate(scene="pricing-toggle", out=Path(...))

Public scenes run now; auth scenes (chat-typing, image-generating, call) return
status `blocked_on_auth` until the showcase-account session is provided via
PLEASUR_AUTH_STATE_B64 / auth/state.json (see setup_auth.py).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from demo_capture import play, _resolve_auth_state  # noqa: E402
from demo_assemble import expand_segments, assemble  # noqa: E402
from demo_polish import compose_frames, fit  # noqa: E402
from demo_scenes import load_scene  # noqa: E402

GIF_SIZE_WARN = 3_000_000  # 3 MB — nudge to trim if a GIF exceeds this


def _resolve_out(out: str | Path) -> Path:
    p = Path(out)
    if p.is_absolute():
        return p
    try:
        return Path(__file__).resolve().parents[4] / out
    except IndexError:
        return p.resolve()


def _write_report(out_path: Path, report: dict[str, Any]) -> None:
    rp = out_path.with_suffix("")
    rp = rp.with_name(rp.name + "_report.json")
    rp.parent.mkdir(parents=True, exist_ok=True)
    rp.write_text(json.dumps(report, indent=2), encoding="utf-8")


def generate(*, scene: str, out: str | Path, formats: list[str] | None = None,
             max_width: int = 940, inner_width: int = 980, fps: int = 0,
             frame: str = "browser", auth: bool = False, url: str | None = None,
             caption: str | None = None, headed: bool = True, strict: bool = False,
             max_frames: int = 300) -> dict[str, Any]:
    """Core engine. Writes assets + `<out>_report.json`; returns the manifest dict."""
    sc = load_scene(scene)
    if url:
        sc["url"] = url
    if caption is not None:
        sc["caption"] = caption
    if fps:
        sc["fps"] = fps
    formats = formats or ["gif", "mp4", "webp"]

    needs_auth = bool(sc.get("needs_auth"))
    use_auth = auth or needs_auth
    eff_fps = int(sc.get("fps", 12))
    out_path = _resolve_out(out)

    report: dict[str, Any] = {
        "scene": sc.get("name"), "needs_auth": needs_auth, "sfw": sc.get("sfw"),
        "url": sc.get("url"), "frame": frame, "fps": eff_fps, "strict": strict,
    }

    if needs_auth and not _resolve_auth_state():
        report["status"] = "blocked_on_auth"
        report["dependency"] = (
            "Showcase-account session required. Run setup_auth.py to log in, then set "
            "PLEASUR_AUTH_STATE_B64 (Doppler) or auth/state.json. This scene is ready; "
            "it will run unchanged once the session lands."
        )
        _write_report(out_path, report)
        return {"status": "blocked_on_auth", "scene": sc.get("name"),
                "dependency": report["dependency"]}

    cap = play(sc, headed=headed, use_auth=use_auth, strict=strict, max_frames=max_frames)
    report.update({"auth_used": cap.auth_used, "final_url": cap.final_url,
                   "clip": cap.clip, "beats": cap.beats, "captured_segments": len(cap.segments)})

    if not cap.ok or not cap.segments:
        report["status"] = "failed"
        report["error"] = cap.error
        _write_report(out_path, report)
        return {"status": "failed", "scene": sc.get("name"), "error": cap.error, "beats": cap.beats}

    raw = expand_segments(cap.segments, eff_fps)
    if frame == "browser":
        frames = compose_frames(raw, sc.get("url_label", "pleasur.ai"),
                                caption=sc.get("caption", ""), inner_w=inner_width)
    else:
        frames = [f.convert("RGB") for f in raw]
    frames = fit(frames, max_width)

    results = assemble(frames, eff_fps, out_path, formats)
    warnings: list[str] = []
    gif = results["outputs"].get("gif")
    if gif and gif.get("bytes", 0) > GIF_SIZE_WARN:
        warnings.append(
            f"GIF is {gif['bytes'] // 1024} KB (> {GIF_SIZE_WARN // 1_000_000} MB). "
            "Lower --max-width/--fps or shorten holds; prefer the MP4 in the article body."
        )
    if not (results["outputs"].get("mp4") or {}).get("path") and "mp4" in formats:
        warnings.append("MP4 not produced (ffmpeg unavailable) — GIF/WebP only.")

    report.update({"status": "captured", "outputs": results["outputs"],
                   "final_frames": results["frames"], "dimensions": list(frames[0].size),
                   "warnings": warnings})
    _write_report(out_path, report)
    return {
        "status": "captured", "scene": sc.get("name"), "auth_used": cap.auth_used,
        "frames": results["frames"], "dimensions": list(frames[0].size),
        "outputs": results["outputs"], "warnings": warnings,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scene", required=True, help="preset name or path to a scene JSON")
    ap.add_argument("--out", required=True, help="output base path (e.g. .../demo.gif; suffix is per-format)")
    ap.add_argument("--formats", default="gif,mp4,webp")
    ap.add_argument("--max-width", type=int, default=940)
    ap.add_argument("--inner-width", type=int, default=980)
    ap.add_argument("--fps", type=int, default=0, help="override scene fps")
    ap.add_argument("--frame", choices=["browser", "none"], default="browser")
    ap.add_argument("--auth", action="store_true", help="use the saved session (auto-on for auth scenes)")
    ap.add_argument("--url", default=None, help="override the scene start URL")
    ap.add_argument("--caption", default=None, help="override the footer caption")
    ap.add_argument("--no-headed", dest="headed", action="store_false")
    ap.add_argument("--headed", dest="headed", action="store_true")
    ap.set_defaults(headed=True)
    ap.add_argument("--strict", action="store_true", help="hard-fail if a required action fails")
    ap.add_argument("--max-frames", type=int, default=300)
    a = ap.parse_args()

    res = generate(
        scene=a.scene, out=a.out,
        formats=[f.strip() for f in a.formats.split(",") if f.strip()],
        max_width=a.max_width, inner_width=a.inner_width, fps=a.fps, frame=a.frame,
        auth=a.auth, url=a.url, caption=a.caption, headed=a.headed, strict=a.strict,
        max_frames=a.max_frames,
    )
    out_view = dict(res)
    if res.get("status") == "captured":
        out_view["outputs"] = {
            k: {"path": v.get("path"), "kb": (v.get("bytes", 0) // 1024), "engine": v.get("engine")}
            for k, v in res["outputs"].items()
        }
    print(json.dumps(out_view, indent=2))
    status = res.get("status")
    if status == "captured":
        return 0
    if status == "blocked_on_auth":
        return 0 if not a.strict else 3
    return 1


if __name__ == "__main__":
    sys.exit(main())
