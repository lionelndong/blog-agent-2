#!/usr/bin/env python3
"""Render a cited draft to an Ahrefs-styled HTML preview.

Usage:
    python .claude/skills/preview/scripts/render_preview.py <slug>
"""
from __future__ import annotations

import datetime
import html as _html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DRAFT_DIR = ROOT / "content-pipeline" / "6-drafts-cited"
OUT_DIR = ROOT / "content-pipeline" / "7-preview"
TEMPLATE = ROOT / "templates" / "preview.html"

# Fence names the renderer styles. Anything else degrades to a plain aside
# (cmp-unknown) so reader content is never silently dropped. Keep in sync with
# examples/ahrefs-components.md and scripts/lint_components.py.
KNOWN_FENCES = frozenset(
    {
        "nutshell", "methodology", "key-takeaways", "tip", "note", "warning",
        "important", "sidenote", "definition", "stat", "stat-group", "stat-list",
        "table", "figure", "diagram", "proscons", "feature-matrix",
        "decision-table", "preferred-order", "entry", "verdict", "badge",
        "expert", "pullquote", "tweet", "video", "further-reading", "jumplinks",
        "faq", "cta", "editor",
    }
)

# Tabler icon glyph (webfont class) + human label for each icon-bearing callout.
# Mirrors examples/component-mockup.html.
_CALLOUT_ICON = {
    "tip": ("ti-bulb", "Pro tip."),
    "note": ("ti-info-circle", "Note."),
    "warning": ("ti-alert-triangle", "Warning."),
    "important": ("ti-alert-octagon", "Important."),
    "sidenote": ("ti-message-2", "Sidenote."),
    "editor": ("ti-pencil", "Editor's note."),
}
_OPENER = re.compile(r"^\s*:::(?P<name>[A-Za-z][A-Za-z0-9-]*)\s*(?P<attrs>.*?)\s*$")
_CLOSER = re.compile(r"^\s*:::\s*$")
_ATTR = re.compile(r'([A-Za-z_][\w-]*)\s*=\s*"([^"]*)"')


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


def _markdown_inner(md: str) -> str:
    """Render a fragment of markdown to HTML (used for component inner content).

    Kept separate from md_to_html so component bodies don't recurse through the
    component pre-pass again (the only legal nesting — :::stat in :::stat-group —
    is handled structurally, not by re-parsing)."""
    md = md.strip("\n")
    if not md:
        return ""
    try:
        import markdown
        html = markdown.markdown(
            md, extensions=["extra", "fenced_code", "tables", "sane_lists"]
        )
    except ImportError:
        html = _basic_md_to_html(md)
    # Unwrap a single enclosing <p> so inline component bodies (a one-liner
    # label/quote) don't get an extra block break.
    m = re.fullmatch(r"<p>(.*)</p>", html.strip(), re.S)
    if m and "</p>" not in m.group(1):
        return m.group(1)
    return html


def md_to_html(md: str) -> str:
    md = _preprocess_visual_placeholders(md)
    # Convert :::component fences to styled HTML BEFORE the markdown pass, and
    # shield each rendered block behind a sentinel so the markdown library does
    # not re-wrap or escape the raw HTML.
    md, shields = _render_components(md)
    try:
        import markdown
        html = markdown.markdown(
            md,
            extensions=["extra", "fenced_code", "tables", "toc", "sane_lists"],
        )
    except ImportError:
        html = _basic_md_to_html(md)
    for token, block in shields.items():
        html = html.replace(f"<p>{token}</p>", block).replace(token, block)
    html = _apply_inline_treatments(html)
    return html


# ----------------------- component fence rendering -----------------------


def _render_components(md: str) -> tuple[str, dict[str, str]]:
    """Replace each top-level :::fence block with a sentinel token; return the
    rewritten markdown and a {token: rendered_html} map.

    Only the OUTERMOST fence is consumed here; :::stat children of a
    :::stat-group are rendered by the stat-group handler from the captured
    inner text. Unbalanced/orphan fences are left as-is (the linter/gate is
    responsible for halting on those — the preview just shows them verbatim)."""
    lines = md.split("\n")
    out: list[str] = []
    shields: dict[str, str] = {}
    i = 0
    n = len(lines)
    counter = 0
    in_code = False
    while i < n:
        line = lines[i]
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            out.append(line)
            i += 1
            continue
        m = _OPENER.match(line) if not in_code else None
        if m and not _CLOSER.match(line):
            name = m.group("name")
            attrs = {a.group(1): a.group(2) for a in _ATTR.finditer(m.group("attrs"))}
            # Collect inner lines until the matching closer, tracking nested
            # openers so a :::stat inside :::stat-group doesn't close early.
            depth = 1
            inner: list[str] = []
            j = i + 1
            closed = False
            while j < n:
                cand = lines[j]
                if _CLOSER.match(cand):
                    depth -= 1
                    if depth == 0:
                        closed = True
                        break
                    inner.append(cand)
                elif _OPENER.match(cand):
                    depth += 1
                    inner.append(cand)
                else:
                    inner.append(cand)
                j += 1
            if not closed:
                # Unbalanced — emit verbatim and let the gate catch it.
                out.append(line)
                i += 1
                continue
            counter += 1
            token = f"\x00CMP{counter}\x00"
            shields[token] = _render_one("\n".join(inner), name, attrs)
            out.append("")
            out.append(token)
            out.append("")
            i = j + 1
            continue
        out.append(line)
        i += 1
    return "\n".join(out), shields


def _attr_link(text: str, url: str | None) -> str:
    safe = _html.escape(text)
    if url:
        return f'<a href="{_html.escape(url, quote=True)}">{safe}</a>'
    return safe


def _icon(cls: str) -> str:
    return f'<i class="ti {cls} i"></i>'


def _render_one(inner_md: str, name: str, attrs: dict[str, str]) -> str:
    """Render a single component to its cmp-<name> HTML block."""
    body = _markdown_inner(inner_md)

    if name in _CALLOUT_ICON:
        icon_cls, default_label = _CALLOUT_ICON[name]
        label = default_label
        if name == "definition" and attrs.get("term"):  # not in this map, but guard
            label = _html.escape(attrs["term"]) + "."
        return (
            f'<div class="call cmp-{name}">{_icon(icon_cls)}'
            f'<div><span class="l">{label}</span> {body}</div></div>'
        )

    if name == "definition":
        term = _html.escape(attrs.get("term", "Definition"))
        return (
            f'<div class="call cmp-definition">{_icon("ti-book-2")}'
            f'<div><span class="l">{term}.</span> {body}</div></div>'
        )

    if name == "nutshell":
        return (
            f'<div class="cmp-nutshell">{_icon("ti-bolt")}'
            f'<div><span class="l">In a nutshell.</span> {body}</div></div>'
        )

    if name == "methodology":
        fresh = ""
        upd, by = attrs.get("updated"), attrs.get("by")
        if upd or by:
            bits = []
            if upd:
                bits.append(f"Updated {_html.escape(upd)}")
            if by:
                bits.append(f"by {_attr_link(by, None)}")
            fresh = f'<div class="fresh">{" ".join(bits)}.</div>'
        return (
            f'<div class="cmp-methodology"><div class="h">{_icon("ti-flask-2")}Methodology</div>'
            f'{fresh}{body}</div>'
        )

    if name == "key-takeaways":
        label = "Key findings" if attrs.get("variant") == "findings" else "Key takeaways"
        return (
            f'<div class="cmp-key-takeaways">{_icon("ti-list-check")}'
            f'<div><span class="l">{label}</span>{body}</div></div>'
        )

    if name == "stat":
        value = _html.escape(attrs.get("value", ""))
        src = ""
        if attrs.get("source"):
            src = f' <span class="src">{_attr_link(attrs["source"], attrs.get("source_url"))}</span>'
        return f'<div class="cmp-stat"><div class="v">{value}</div><div class="l">{body}{src}</div></div>'

    if name == "stat-group":
        # Inner is a sequence of :::stat blocks; render each child.
        cards = _render_stat_children(inner_md)
        return f'<div class="cmp-stat-group">{cards}</div>'

    if name == "stat-list":
        return f'<div class="cmp-stat-list">{body}</div>'

    if name == "expert":
        nm = _html.escape(attrs.get("name", ""))
        role_bits = []
        if attrs.get("title"):
            role_bits.append(_html.escape(attrs["title"]))
        if attrs.get("company"):
            role_bits.append(_attr_link(attrs["company"], attrs.get("company_url")))
        role = ", ".join(role_bits)
        initials = "".join(w[0] for w in attrs.get("name", "?").split()[:2]).upper() or "?"
        return (
            f'<div class="cmp-expert"><div class="av">{_html.escape(initials)}</div>'
            f'<div><p class="q">{body}</p><div class="nm">{nm}</div>'
            f'<div class="ro">{role}</div></div></div>'
        )

    if name == "pullquote":
        cite = ""
        if attrs.get("cite"):
            cite = f'<cite>— {_attr_link(attrs["cite"], attrs.get("source"))}</cite>'
        return f'<blockquote class="cmp-pullquote">{_icon("ti-quote")}<div>{body}{cite}</div></blockquote>'

    if name == "verdict":
        return f'<div class="cmp-verdict"><span class="l">Verdict.</span> {body}</div>'

    if name == "badge":
        kind = attrs.get("kind", "")
        label = inner_md.strip() or kind.replace("-", " ").title()
        return f'<span class="cmp-badge cmp-badge--{_html.escape(kind)}">{_html.escape(label)}</span>'

    if name == "proscons":
        return _render_proscons(inner_md)

    if name in ("table", "feature-matrix", "decision-table"):
        cap = ""
        if attrs.get("caption"):
            cap = f'<div class="cap">{_html.escape(attrs["caption"])}</div>'
        src = ""
        if attrs.get("source"):
            src = f'<div class="src">Source: {_html.escape(attrs["source"])}</div>'
        return f'<div class="cmp-{name}">{cap}{body}{src}</div>'

    if name == "preferred-order":
        # body is an <ol>…</ol>; swap its class.
        ol = re.sub(r"<ol>", '<ol class="cmp-preferred-order">', body, count=1)
        return ol if "cmp-preferred-order" in ol else f'<div class="cmp-preferred-order">{body}</div>'

    if name == "further-reading":
        return (
            f'<div class="cmp-further-reading">{_icon("ti-arrow-right")}'
            f'<div><span class="l">Further reading:</span> {body}</div></div>'
        )

    if name == "jumplinks":
        ul = re.sub(r"<ul>", '<ul class="cmp-jumplinks">', body, count=1)
        return ul if "cmp-jumplinks" in ul else f'<nav class="cmp-jumplinks">{body}</nav>'

    if name == "faq":
        return _render_faq(inner_md)

    if name == "figure":
        src = _html.escape(attrs.get("src", ""), quote=True)
        cap = f"<figcaption>{body}" if body else "<figcaption>"
        if attrs.get("source"):
            cap += f' <span class="src">Source: {_html.escape(attrs["source"])}</span>'
        cap += "</figcaption>"
        return f'<figure class="cmp-figure"><img src="{src}" alt="">{cap}</figure>'

    if name == "diagram":
        src = _html.escape(attrs.get("src", ""), quote=True)
        cap = f"<figcaption>{body}</figcaption>" if body else ""
        return f'<figure class="cmp-diagram"><img src="{src}" alt="">{cap}</figure>'

    if name == "entry":
        nm = _attr_link(attrs.get("name", ""), attrs.get("url"))
        eyebrow = f'<span class="n">#{_html.escape(attrs.get("n", ""))}</span> ' if attrs.get("n") else ""
        meta = []
        if attrs.get("best_for"):
            meta.append(f'<span class="best-for">Best for: {_html.escape(attrs["best_for"])}</span>')
        if attrs.get("price"):
            meta.append(f'<span class="price">{_html.escape(attrs["price"])}</span>')
        meta_html = " · ".join(meta)
        return f'<header class="cmp-entry">{eyebrow}<strong>{nm}</strong><div>{meta_html}</div>{body}</header>'

    if name == "tweet":
        url = _html.escape(attrs.get("url", ""), quote=True)
        return f'<figure class="cmp-tweet">{body or "Tweet"} <a href="{url}">View on X</a></figure>'

    if name == "video":
        title = _html.escape(attrs.get("title", "Video"))
        return f'<figure class="cmp-video">{title}{(" — " + body) if body else ""}</figure>'

    if name == "cta":
        heading = _html.escape(attrs.get("heading", ""))
        button = _html.escape(attrs.get("button", "Learn more"))
        href = _html.escape(attrs.get("href", "#"), quote=True)
        return (
            f'<div class="cmp-cta">{_icon("ti-sparkles")}<h3>{heading}</h3>'
            f'<p>{body}</p><a class="btn" href="{href}">{button}</a></div>'
        )

    # Unknown fence — never drop content; render as a plain aside.
    return f'<div class="cmp-unknown">{body}</div>'


def _render_stat_children(inner_md: str) -> str:
    """Render the :::stat children inside a :::stat-group."""
    lines = inner_md.split("\n")
    cards: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        m = _OPENER.match(lines[i])
        if m and m.group("name") == "stat":
            attrs = {a.group(1): a.group(2) for a in _ATTR.finditer(m.group("attrs"))}
            body_lines: list[str] = []
            j = i + 1
            while j < n and not _CLOSER.match(lines[j]):
                body_lines.append(lines[j])
                j += 1
            cards.append(_render_one("\n".join(body_lines), "stat", attrs))
            i = j + 1
        else:
            i += 1
    return "".join(cards)


def _render_proscons(inner_md: str) -> str:
    """Split inner on '## Pros' / '## Cons' into two styled panels."""
    pros, cons = "", ""
    current = None
    buf: dict[str, list[str]] = {"pros": [], "cons": []}
    for line in inner_md.split("\n"):
        low = line.strip().lower()
        if low.startswith("##") and "pros" in low:
            current = "pros"
            continue
        if low.startswith("##") and "cons" in low:
            current = "cons"
            continue
        if current:
            buf[current].append(line)
    pros = _markdown_inner("\n".join(buf["pros"]))
    cons = _markdown_inner("\n".join(buf["cons"]))
    return (
        '<div class="cmp-proscons">'
        f'<div class="col pros"><strong>Pros</strong>{pros}</div>'
        f'<div class="col cons"><strong>Cons</strong>{cons}</div></div>'
    )


def _render_faq(inner_md: str) -> str:
    """Split inner on '### Question' boundaries into <details> rows."""
    parts = re.split(r"(?m)^\s*###\s+", inner_md)
    items: list[str] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        q, _, a = part.partition("\n")
        ans = _markdown_inner(a)
        items.append(
            f'<details class="cmp-faq__item"><summary>{_html.escape(q.strip())}</summary>'
            f'<div>{ans}</div></details>'
        )
    return f'<div class="cmp-faq">{"".join(items)}</div>'


def _apply_inline_treatments(html: str) -> str:
    """Bucket-C inline treatments applied to the rendered HTML:
    {lead}…{/lead} -> a lead paragraph class; ==mark== -> <mark>.
    (Inline `code` chips are already <code> elements styled by the template.)
    Skips the interior of <pre>/<code> by only touching the outer text runs."""
    # ==mark== -> <mark> (non-greedy, single line, avoid empty)
    html = re.sub(r"==(\S.*?\S|\S)==", r"<mark>\1</mark>", html)

    # {lead}…{/lead} -> a single lead paragraph. Collapse any <p> the markdown
    # pass put immediately around the token so we don't nest <p> in <p>.
    def _lead(m: "re.Match[str]") -> str:
        content = m.group(1).strip()
        content = re.sub(r"^<p>(.*)</p>$", r"\1", content, flags=re.S).strip()
        return f'<p class="cmp-lead">{content}</p>'

    html = re.sub(r"<p>\s*\{lead\}(.*?)\{/lead\}\s*</p>", _lead, html, flags=re.S)
    html = re.sub(r"\{lead\}(.*?)\{/lead\}", _lead, html, flags=re.S)
    return html


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
