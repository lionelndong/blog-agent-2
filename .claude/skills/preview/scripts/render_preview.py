#!/usr/bin/env python3
"""Render a cited draft to an Ahrefs-styled HTML preview.

Usage:
    python .claude/skills/preview/scripts/render_preview.py <slug>
"""
from __future__ import annotations

import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DRAFT_DIR = ROOT / "content-pipeline" / "6-drafts-cited"
OUT_DIR = ROOT / "content-pipeline" / "7-preview"
TEMPLATE = ROOT / "templates" / "preview.html"


def _preprocess_visual_placeholders(md: str) -> str:
    """Replace [VISUAL:...] / [SCREENSHOT:...] with HTML before markdown processing,
    since the markdown library would otherwise mis-parse them as links."""
    md = re.sub(r"\[VISUAL:(.+?)\]", _render_typed_visual, md)
    md = re.sub(
        r"\[SCREENSHOT:\s*(.+?)\]",
        r'<span class="visual-placeholder visual-placeholder--screenshot">'
        r'<span class="visual-placeholder__icon">&#128247;</span> '
        r'<span class="visual-placeholder__label">screenshot: \1</span></span>',
        md,
    )
    return md


def md_to_html(md: str) -> str:
    md = _preprocess_visual_placeholders(md)
    try:
        import markdown
        return markdown.markdown(
            md,
            extensions=["extra", "fenced_code", "tables", "toc", "sane_lists"],
        )
    except ImportError:
        return _basic_md_to_html(md)


def _basic_md_to_html(md: str) -> str:
    lines = md.split("\n")
    out = []
    in_list = False
    in_para = []

    def flush_para():
        nonlocal in_para
        if in_para:
            text = " ".join(in_para).strip()
            if text:
                out.append(f"<p>{_inline(text)}</p>")
            in_para = []

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            flush_para()
            close_list()
            continue
        if line.startswith("# "):
            flush_para(); close_list()
            out.append(f"<h1>{_inline(line[2:])}</h1>")
        elif line.startswith("## "):
            flush_para(); close_list()
            out.append(f"<h2>{_inline(line[3:])}</h2>")
        elif line.startswith("### "):
            flush_para(); close_list()
            out.append(f"<h3>{_inline(line[4:])}</h3>")
        elif line.startswith("- ") or line.startswith("* "):
            flush_para()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{_inline(line[2:])}</li>")
        else:
            close_list()
            in_para.append(line)
    flush_para()
    close_list()
    return "\n".join(out)


_VISUAL_ICON: dict[str, str] = {
    "screenshot": "&#128247;",
    "image": "&#128444;",
    "table": "&#128203;",
    "chart": "&#128202;",
    "video": "&#127916;",
    "external": "&#127760;",
    "gif": "&#127902;",
}


def _parse_typed_visual(body: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for part in body.split(";"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        key, _, value = part.partition("=")
        attrs[key.strip()] = value.strip()
    return attrs


def _render_typed_visual(match: "re.Match[str]") -> str:
    attrs = _parse_typed_visual(match.group(1))
    vtype = (attrs.get("type") or "screenshot").lower()
    icon = _VISUAL_ICON.get(vtype, "&#128444;")
    label = ""
    for key in ("what", "prompt", "title", "url"):
        value = attrs.get(key)
        if value:
            label = value
            break
    if not label:
        label = f"{vtype} placeholder"
    if attrs.get("safety") == "adult":
        label += " · manual capture (adult content)"
    elif vtype in {"video", "external", "gif"}:
        label += " · manual capture"
    safe_label = label.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        f'<span class="visual-placeholder visual-placeholder--{vtype}">'
        f'<span class="visual-placeholder__icon">{icon}</span> '
        f'<span class="visual-placeholder__label">{vtype}: {safe_label}</span>'
        f"</span>"
    )


def _inline(text: str) -> str:
    text = re.sub(r"\[VISUAL:(.+?)\]", _render_typed_visual, text)
    text = re.sub(
        r"\[SCREENSHOT:\s*(.+?)\]",
        r'<span class="visual-placeholder visual-placeholder--screenshot">'
        r'<span class="visual-placeholder__icon">&#128247;</span> '
        r'<span class="visual-placeholder__label">screenshot: \1</span></span>',
        text,
    )
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"`([^`]+?)`", r"<code>\1</code>", text)
    return text


def extract_title(md: str) -> tuple[str, str]:
    m = re.match(r"^\s*#\s+(.+?)\s*$", md, re.MULTILINE)
    if not m:
        return "Untitled", md
    title = m.group(1).strip()
    rest = md[: m.start()] + md[m.end():]
    return title, rest.lstrip("\n")


_IMG_PATH_RE = re.compile(r'(<img[^>]*\bsrc=)"(?!https?://|file://|data:|/|\.\./|\.\\)([^"]+)"')


def _rewrite_image_paths_for_preview(html: str) -> str:
    """Rewrite relative image paths so the rendered HTML resolves them correctly.

    The cited draft uses `images/{slug}/foo.png` paths, which are relative to the
    project root (where the markdown lives in `content-pipeline/6-drafts-cited/`).
    The rendered HTML lives in `content-pipeline/7-preview/`, so a browser opening
    the HTML resolves `images/...` against `7-preview/`, where there is no
    images directory. Rewrite to `../images/...` which IS correct from the
    HTML's location.
    """
    return _IMG_PATH_RE.sub(r'\1"../\2"', html)


def render(slug: str) -> Path:
    draft_path = DRAFT_DIR / f"{slug}.md"
    if not draft_path.exists():
        print(f"error: draft not found at {draft_path}", file=sys.stderr)
        sys.exit(1)
    md = draft_path.read_text(encoding="utf-8")
    title, body_md = extract_title(md)
    body_html = md_to_html(body_md)
    body_html = _rewrite_image_paths_for_preview(body_html)

    template = TEMPLATE.read_text(encoding="utf-8")
    today = datetime.date.today().isoformat()
    rendered = (
        template.replace("{{TITLE}}", title)
        .replace("{{DATE}}", today)
        .replace("{{BODY_HTML}}", body_html)
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{slug}.html"
    out_path.write_text(rendered, encoding="utf-8")
    return out_path


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(
        description="Render a cited draft to an Ahrefs-styled HTML preview.",
    )
    parser.add_argument("slug", help="The slug of the cited draft to render")
    args = parser.parse_args()
    out = render(args.slug)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
