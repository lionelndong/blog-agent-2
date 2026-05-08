#!/usr/bin/env python3
"""Generate an illustrative image via Replicate.

Default model: openai/gpt-image-2 (Replicate-hosted, NEVER direct OpenAI API).
Backup model: google/nano-banana — used automatically on error or content refusal.
Adult-content prompts (safety=adult) are NEVER sent to Replicate; the dispatcher
routes those to manual capture instead.

Standalone usage:
    python generate_image.py --prompt "<text>" --out <path> [--model <slug>]

Reads REPLICATE_API_TOKEN from the environment (load via Doppler).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]

DEFAULT_MODEL = "openai/gpt-image-2"
BACKUP_MODEL = "google/nano-banana"
DEFAULT_STYLE_SUFFIX = "photorealistic, soft natural lighting, no people"


def _model_slug(name: str) -> str:
    """Accept short aliases."""
    aliases = {
        "gpt-image-2": "openai/gpt-image-2",
        "gpt-image2": "openai/gpt-image-2",
        "gptimage2": "openai/gpt-image-2",
        "nano-banana": "google/nano-banana",
        "nano": "google/nano-banana",
    }
    return aliases.get(name.lower(), name)


def _build_prompt(prompt: str, style_suffix: str | None = None) -> str:
    suffix = style_suffix if style_suffix is not None else DEFAULT_STYLE_SUFFIX
    if not suffix:
        return prompt
    if suffix.lower() in prompt.lower():
        return prompt
    return f"{prompt}. {suffix}"


def _run_replicate(model: str, prompt: str, timeout_s: int = 180) -> dict[str, Any]:
    try:
        import replicate
    except ImportError:
        return {
            "status": "failed",
            "reason": "replicate_not_installed",
            "hint": "pip install replicate",
        }

    # Accept either name; the Replicate SDK reads REPLICATE_API_TOKEN by default.
    token = os.environ.get("REPLICATE_API_TOKEN") or os.environ.get("REPLICATE_API_KEY")
    if not token:
        return {
            "status": "failed",
            "reason": "missing_replicate_token",
            "hint": "set REPLICATE_API_TOKEN or REPLICATE_API_KEY (Doppler) and run via doppler run --",
        }
    # Mirror to REPLICATE_API_TOKEN so the SDK picks it up.
    os.environ.setdefault("REPLICATE_API_TOKEN", token)

    try:
        output = replicate.run(model, input={"prompt": prompt})
    except Exception as exc:  # network errors, model errors, content-safety refusals
        msg = str(exc).lower()
        if any(s in msg for s in ("nsfw", "safety", "policy", "content")):
            return {"status": "refused", "reason": "content_safety", "model": model, "error": str(exc)}
        return {"status": "failed", "reason": "replicate_error", "model": model, "error": str(exc)}

    image_url = _extract_image_url(output)
    if not image_url:
        return {"status": "failed", "reason": "no_image_returned", "model": model, "raw": str(output)[:500]}
    return {"status": "ok", "image_url": image_url, "model": model}


def _coerce_url(item: Any) -> str | None:
    """Pull a URL string out of a single Replicate output item.

    Handles plain string URLs and the modern `replicate.helpers.FileOutput`
    object (which exposes `.url` as a string attribute, *not* a callable).
    Older SDKs exposed `.url()` as a method, so try the callable path as a
    fallback for forward/backward compatibility.
    """
    if isinstance(item, str) and item.startswith("http"):
        return item
    # FileOutput.url is a string attribute on current SDKs; older SDKs had it
    # as a method. Try the attribute first, then call as a fallback.
    url_attr = getattr(item, "url", None)
    if isinstance(url_attr, str) and url_attr.startswith("http"):
        return url_attr
    if callable(url_attr):
        try:
            value = url_attr()
            if isinstance(value, str) and value.startswith("http"):
                return value
        except Exception:
            pass
    # FileOutput stringifies to its URL on current SDKs.
    text = str(item) if item is not None else ""
    if text.startswith("http"):
        return text
    return None


def _extract_image_url(output: Any) -> str | None:
    """Replicate's output shape varies by model. Handle the common cases."""
    direct = _coerce_url(output)
    if direct:
        return direct
    if isinstance(output, list) and output:
        first = _coerce_url(output[0])
        if first:
            return first
    if isinstance(output, dict):
        for key in ("image", "url", "output"):
            value = output.get(key)
            url = _coerce_url(value)
            if url:
                return url
    return None


def _download(url: str, out_path: Path, timeout_s: int = 60) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "blog-agent/generate-visuals"})
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            data = resp.read()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(data)
        return out_path.stat().st_size > 1_000
    except (urllib.error.URLError, OSError) as exc:
        sys.stderr.write(f"download failed: {exc}\n")
        return False


def generate(
    prompt: str,
    out_path: Path,
    model: str = DEFAULT_MODEL,
    style_suffix: str | None = None,
    safety: str = "sfw",
) -> dict[str, Any]:
    if safety == "adult":
        return {
            "status": "refused",
            "reason": "adult_content_routed_manual",
            "hint": "produce manually via pleasur.ai/generate",
        }

    full_prompt = _build_prompt(prompt, style_suffix)

    # Try primary model
    primary_model = _model_slug(model)
    result = _run_replicate(primary_model, full_prompt)
    if result["status"] == "ok":
        if _download(result["image_url"], out_path):
            return {
                "status": "captured",
                "path": str(out_path.relative_to(ROOT)),
                "model": result["model"],
                "prompt": full_prompt,
            }
        return {"status": "failed", "reason": "download_failed", "model": result["model"]}

    # Backup model
    if primary_model != BACKUP_MODEL:
        time.sleep(0.5)
        backup_result = _run_replicate(BACKUP_MODEL, full_prompt)
        if backup_result["status"] == "ok":
            if _download(backup_result["image_url"], out_path):
                return {
                    "status": "captured",
                    "path": str(out_path.relative_to(ROOT)),
                    "model": backup_result["model"],
                    "primary_failed": result.get("reason"),
                    "prompt": full_prompt,
                }
            return {"status": "failed", "reason": "download_failed", "model": backup_result["model"]}
        return {
            "status": "failed",
            "reason": "both_models_failed",
            "primary": result,
            "backup": backup_result,
        }

    return {"status": "failed", "reason": result.get("reason", "unknown"), "details": result}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--style-suffix", default=None)
    parser.add_argument("--safety", default="sfw", choices=["sfw", "adult"])
    args = parser.parse_args()

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = ROOT / out_path

    result = generate(args.prompt, out_path, args.model, args.style_suffix, args.safety)
    json.dump(result, sys.stdout)
    sys.stdout.write("\n")
    return 0 if result.get("status") == "captured" else 1


if __name__ == "__main__":
    sys.exit(main())
