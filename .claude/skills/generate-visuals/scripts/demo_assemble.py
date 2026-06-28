#!/usr/bin/env python3
"""Assembly stage for the animated-demo engine.

Turns the polished frame list into web-friendly outputs:
  - GIF  : two-pass ffmpeg palettegen/paletteuse (best size/quality); PIL fallback.
  - MP4  : H.264 yuv420p, faststart (tiny; best for the blog body).
  - WebP : animated, via PIL (smallest of all — emitted as a bonus).

ffmpeg is the static binary bundled with imageio-ffmpeg (no system ffmpeg needed,
lives on the persistent volume), resolved via imageio_ffmpeg.get_ffmpeg_exe().
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from PIL import Image

from demo_capture import Segment
from demo_polish import crossfade


# ---------------------------------------------------------------------------
# Segments -> ordered (frame, duration) timeline -> constant-fps frame list
# ---------------------------------------------------------------------------

def expand_segments(segments: list[Segment], fps: int) -> list[Image.Image]:
    """Insert crossfade tweens, then resample the whole timeline to constant fps."""
    timeline: list[tuple[Image.Image, int]] = []
    prev: Image.Image | None = None
    for seg in segments:
        if seg.xfade_ms > 0 and prev is not None:
            n = max(1, round(seg.xfade_ms * fps / 1000))
            for tw in crossfade(prev, seg.img, n):
                timeline.append((tw, max(1, round(1000 / fps))))
        timeline.append((seg.img, seg.dur_ms))
        prev = seg.img

    frames: list[Image.Image] = []
    for img, dur_ms in timeline:
        reps = max(1, round(dur_ms * fps / 1000))
        frames.extend([img] * reps)
    return frames


# ---------------------------------------------------------------------------
# ffmpeg
# ---------------------------------------------------------------------------

def _ffmpeg() -> str | None:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return shutil.which("ffmpeg")


def _write_png_seq(frames: list[Image.Image], d: Path) -> None:
    for i, fr in enumerate(frames):
        fr.convert("RGB").save(d / f"f_{i:05d}.png")


def _run(cmd: list[str]) -> bool:
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except Exception:
        return False


def _gif_ffmpeg(seq: Path, fps: int, out: Path, ff: str) -> bool:
    palette = seq / "palette.png"
    pat = str(seq / "f_%05d.png")
    ok = _run([
        ff, "-y", "-framerate", str(fps), "-i", pat,
        "-vf", "palettegen=stats_mode=diff", str(palette),
    ])
    if not ok:
        return False
    return _run([
        ff, "-y", "-framerate", str(fps), "-i", pat, "-i", str(palette),
        "-lavfi", "paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle",
        "-loop", "0", str(out),
    ])


def _gif_pil(frames: list[Image.Image], fps: int, out: Path) -> None:
    pal = [f.convert("P", palette=Image.ADAPTIVE, colors=256) for f in frames]
    pal[0].save(out, save_all=True, append_images=pal[1:], loop=0,
                duration=int(1000 / fps), disposal=2, optimize=True)


def _mp4_ffmpeg(seq: Path, fps: int, out: Path, ff: str) -> bool:
    pat = str(seq / "f_%05d.png")
    return _run([
        ff, "-y", "-framerate", str(fps), "-i", pat,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23", "-preset", "veryslow",
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", "-movflags", "+faststart", str(out),
    ])


def _webp_pil(frames: list[Image.Image], fps: int, out: Path) -> None:
    frames[0].save(out, format="WEBP", save_all=True, append_images=frames[1:],
                   duration=int(1000 / fps), loop=0, quality=72, method=6)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def assemble(frames: list[Image.Image], fps: int, out_base: Path,
             formats: list[str]) -> dict[str, Any]:
    """Write requested formats. `out_base` is a path whose suffix is ignored."""
    out_base.parent.mkdir(parents=True, exist_ok=True)
    stem = out_base.with_suffix("")
    ff = _ffmpeg()
    results: dict[str, Any] = {"fps": fps, "frames": len(frames), "outputs": {}}

    with tempfile.TemporaryDirectory() as td:
        seq = Path(td)
        _write_png_seq(frames, seq)

        if "gif" in formats:
            gif = stem.with_suffix(".gif")
            done = bool(ff) and _gif_ffmpeg(seq, fps, gif, ff)
            if not done:
                _gif_pil(frames, fps, gif)
            results["outputs"]["gif"] = {
                "path": str(gif), "bytes": gif.stat().st_size if gif.exists() else 0,
                "engine": "ffmpeg" if done else "pil",
            }
        if "mp4" in formats:
            mp4 = stem.with_suffix(".mp4")
            done = bool(ff) and _mp4_ffmpeg(seq, fps, mp4, ff)
            results["outputs"]["mp4"] = {
                "path": str(mp4) if done else None,
                "bytes": mp4.stat().st_size if (done and mp4.exists()) else 0,
                "engine": "ffmpeg" if done else "unavailable",
            }
        if "webp" in formats:
            webp = stem.with_suffix(".webp")
            try:
                _webp_pil(frames, fps, webp)
                results["outputs"]["webp"] = {"path": str(webp), "bytes": webp.stat().st_size, "engine": "pil"}
            except Exception as exc:
                results["outputs"]["webp"] = {"path": None, "bytes": 0, "error": str(exc)[:160]}

    return results
