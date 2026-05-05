#!/usr/bin/env python3
"""Whiteboard — local web UI for the blog pipeline.

A dashboard for inspecting, editing, and re-running pipeline stages —
inspired by the UI Ryan Law showed in the Ahrefs blog post.

Features:
- See every slug in the pipeline + per-stage status (done / pending)
- Preview each stage's output (markdown rendered, HTML embedded)
- Edit outputs in-place and save back to disk
- "Re-run" copies the slash command to your clipboard (paste into Claude Code)
- View the skill definition for any stage

Usage:
    python scripts/whiteboard.py [--port 8765] [--host 127.0.0.1]
    # then open http://localhost:8765 in your browser

No external dependencies (stdlib only).
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
PIPELINE = ROOT / "content-pipeline"
SKILLS_DIR = ROOT / ".claude" / "skills"


# Pipeline stages — the order matches the orchestrator chain.
# Each entry: (key, display_name, skill_name_for_rerun, dir_path_relative_to_pipeline, file_pattern, description, file_kind)
STAGES = [
    ("context", "Context", "blog-pipeline", "0-context", "{slug}.md", "User-provided direction (--context)", "md"),
    ("research", "Research", "research", "1-research", "{slug}.md", "Keyword metrics, SERP, top-page summaries", "md"),
    ("research-deep", "Deep Research", "research", "1-research", "{slug}-deep.md", "Perplexity / OpenRouter web research", "md"),
    ("reference", "Brand Reference", "brand-reference", "2-reference", "{slug}.md", "Existing brand articles + reusable modules", "md"),
    ("outline", "Outline", "outline", "3-outlines", "{slug}.md", "Structured H2/H3 outline with BLUFs", "md"),
    ("annotated", "Product Mentions", "product-mentions", "4-outlines-annotated", "{slug}.md", "Outline annotated with product touchpoints", "md"),
    ("draft", "Draft", "draft", "5-drafts", "{slug}.md", "Full article prose", "md"),
    ("quality-check", "Quality Check", "quality-check", "quality-checks", "{slug}-metrics.md", "Voice metrics, BLUF, forbidden phrases, claim density", "md"),
    ("cited", "Verify Claims", "verify-claims", "6-drafts-cited", "{slug}.md", "Claims with real source links", "md"),
    ("screenshots", "Screenshots", "generate-screenshot", "images/{slug}", "screenshot-urls.md", "Tool URLs for each screenshot placeholder", "md"),
    ("preview", "Preview", "preview", "7-preview", "{slug}.html", "Ahrefs-styled HTML preview", "html"),
    ("publish", "Publish", "format-for-publish", "8-publish/{slug}", "article.md", "Strapi-ready markdown + JSON payload", "md"),
]

# Stages that are part of the standard chain (used for the count: "X / Y completed")
CORE_STAGES = {"research", "reference", "outline", "annotated", "draft", "cited", "preview"}


def stage_path(slug: str, stage: dict) -> Path:
    rel_dir = stage["dir"].format(slug=slug)
    file = stage["file"].format(slug=slug)
    return PIPELINE / rel_dir / file


def stage_dict(t: tuple) -> dict:
    keys = ["key", "name", "skill", "dir", "file", "description", "kind"]
    return dict(zip(keys, t))


STAGE_DICTS = [stage_dict(s) for s in STAGES]
STAGES_BY_KEY = {s["key"]: s for s in STAGE_DICTS}


def list_slugs() -> list[str]:
    """Discover every slug that has at least one stage output."""
    slugs: set[str] = set()
    if not PIPELINE.exists():
        return []
    # Look at every stage dir; collect slug from filenames
    for stage in STAGE_DICTS:
        # Templated dirs (images/{slug}, 8-publish/{slug}) need special handling
        if "{slug}" in stage["dir"]:
            parent = PIPELINE / stage["dir"].split("/{slug}")[0]
            if parent.exists():
                for sub in parent.iterdir():
                    if sub.is_dir():
                        slugs.add(sub.name)
            continue
        d = PIPELINE / stage["dir"]
        if not d.exists():
            continue
        pattern = stage["file"].replace("{slug}", "*")
        for p in d.glob(pattern):
            if "{slug}" in stage["file"]:
                # extract slug from filename
                # e.g. file pattern "{slug}.md" → slug = stem
                # e.g. file pattern "{slug}-deep.md" → strip suffix
                stem = p.stem
                # crude but works for our patterns
                if stage["file"].endswith("-deep.md") and stem.endswith("-deep"):
                    slugs.add(stem[:-5])
                elif stage["file"].endswith("-metrics.md") and stem.endswith("-metrics"):
                    slugs.add(stem[:-8])
                else:
                    slugs.add(stem)
    return sorted(slugs)


def slug_status(slug: str) -> dict:
    """For each stage, return (done bool, file path)."""
    out = {}
    for stage in STAGE_DICTS:
        path = stage_path(slug, stage)
        out[stage["key"]] = {
            "done": path.exists(),
            "path": str(path.relative_to(ROOT)),
        }
    return out


def md_to_html(md: str) -> str:
    try:
        import markdown
        return markdown.markdown(md, extensions=["extra", "fenced_code", "tables", "sane_lists"])
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
            flush_para(); close_list()
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
    flush_para(); close_list()
    return "\n".join(out)


def _inline(text: str) -> str:
    text = re.sub(r"\[SCREENSHOT:\s*(.+?)\]", r'<span class="screenshot-placeholder">[Screenshot: \1]</span>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    text = re.sub(r"`([^`]+?)`", r"<code>\1</code>", text)
    return text


# -------------------- HTML templates --------------------

CSS = """
:root {
  --bg: #0e0f12;
  --panel: #16181d;
  --border: #25272d;
  --text: #e6e8ec;
  --muted: #8a8f99;
  --accent: #f97316;
  --accent-soft: #f9731622;
  --green: #22c55e;
  --green-soft: #22c55e1f;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  font-size: 14px;
  line-height: 1.55;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
.topbar {
  display: flex;
  align-items: center;
  padding: 16px 28px;
  border-bottom: 1px solid var(--border);
  font-weight: 600;
  font-size: 16px;
  background: var(--panel);
}
.topbar .crumb { color: var(--muted); margin: 0 6px; }
.topbar .crumb a { color: var(--muted); }
.layout { display: grid; grid-template-columns: 320px 1fr; min-height: calc(100vh - 57px); }
.sidebar {
  border-right: 1px solid var(--border);
  background: var(--panel);
  padding: 20px 16px;
  overflow-y: auto;
}
.sidebar .meta { color: var(--muted); font-size: 12px; margin-bottom: 18px; }
.sidebar .meta .badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 6px;
  background: var(--accent-soft);
  color: var(--accent);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 10px;
  letter-spacing: 0.5px;
  margin-left: 6px;
}
.stage {
  display: flex;
  align-items: flex-start;
  padding: 10px 12px;
  border-radius: 8px;
  margin-bottom: 4px;
  cursor: pointer;
  position: relative;
}
.stage:hover { background: #1f2228; }
.stage.active { background: #20232a; }
.stage .dot {
  width: 22px; height: 22px;
  border-radius: 50%;
  margin-right: 12px;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
}
.stage .dot.done { background: var(--green-soft); color: var(--green); }
.stage .dot.pending { background: #2a2d33; color: var(--muted); }
.stage .info { flex-grow: 1; }
.stage .info .name { font-weight: 600; font-size: 13px; margin-bottom: 2px; }
.stage .info .desc { color: var(--muted); font-size: 12px; line-height: 1.4; }
.main { padding: 28px 36px; max-width: 1100px; }
.stage-header {
  display: flex;
  align-items: center;
  border: 1px solid var(--border);
  background: var(--panel);
  padding: 18px 22px;
  border-radius: 10px;
  margin-bottom: 20px;
}
.stage-header .icon { font-size: 22px; margin-right: 14px; }
.stage-header .title { font-size: 18px; font-weight: 700; margin: 0; }
.stage-header .desc { color: var(--muted); font-size: 13px; margin-top: 3px; }
.stage-header .actions { margin-left: auto; display: flex; gap: 8px; }
.btn {
  display: inline-block;
  padding: 7px 14px;
  border-radius: 7px;
  font-weight: 600;
  font-size: 12px;
  border: 1px solid var(--border);
  background: #1f2228;
  color: var(--text);
  cursor: pointer;
  font-family: inherit;
}
.btn:hover { background: #2a2d33; }
.btn.done { background: var(--green-soft); color: var(--green); border-color: transparent; }
.btn.accent { background: var(--accent); color: #fff; border-color: transparent; }
.btn.accent:hover { background: #ea6b13; }
.tabs { display: flex; gap: 4px; border-bottom: 1px solid var(--border); margin-bottom: 18px; }
.tab {
  padding: 8px 14px;
  border-radius: 7px 7px 0 0;
  cursor: pointer;
  font-size: 13px;
  color: var(--muted);
  font-weight: 500;
  border-bottom: 2px solid transparent;
}
.tab.active { color: var(--accent); border-bottom-color: var(--accent); }
.tab:hover { color: var(--text); }
.tab-panel { display: none; }
.tab-panel.active { display: block; }
.preview-box, .skill-box {
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 24px 28px;
  background: var(--panel);
  min-height: 200px;
}
.preview-box h1 { font-size: 22px; margin-top: 0; }
.preview-box h2 { font-size: 18px; margin-top: 28px; color: var(--accent); }
.preview-box h3 { font-size: 15px; margin-top: 22px; }
.preview-box p { margin: 0 0 14px; }
.preview-box ul, .preview-box ol { padding-left: 22px; }
.preview-box li { margin-bottom: 4px; }
.preview-box code { background: #20232a; padding: 1px 6px; border-radius: 4px; font-size: 0.9em; }
.preview-box pre { background: #0a0b0e; padding: 14px; border-radius: 8px; overflow-x: auto; }
.preview-box table { border-collapse: collapse; width: 100%; margin: 14px 0; font-size: 13px; }
.preview-box th, .preview-box td { border: 1px solid var(--border); padding: 8px 12px; text-align: left; }
.preview-box th { background: #1c1e23; color: var(--accent); }
.preview-box .screenshot-placeholder {
  display: inline-block;
  background: #20232a;
  border: 1px dashed var(--border);
  padding: 8px 12px;
  border-radius: 6px;
  color: var(--muted);
  font-size: 12px;
}
.preview-iframe { width: 100%; height: 800px; border: 1px solid var(--border); border-radius: 10px; background: white; }
textarea.editor {
  width: 100%;
  min-height: 600px;
  background: #0a0b0e;
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px;
  font-family: "SF Mono", Menlo, Consolas, monospace;
  font-size: 13px;
  line-height: 1.5;
  resize: vertical;
}
.save-row { margin-top: 14px; display: flex; gap: 10px; align-items: center; }
.save-status { color: var(--muted); font-size: 12px; }
.save-status.ok { color: var(--green); }
.save-status.err { color: #ef4444; }
.empty {
  text-align: center;
  padding: 60px 20px;
  color: var(--muted);
}
.empty h2 { color: var(--text); }
.slug-list {
  display: grid;
  gap: 10px;
  margin-top: 16px;
}
.slug-card {
  border: 1px solid var(--border);
  background: var(--panel);
  padding: 16px 22px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--text);
}
.slug-card:hover { border-color: var(--accent); text-decoration: none; }
.slug-card .name { font-weight: 600; font-size: 15px; flex-grow: 1; }
.slug-card .progress { color: var(--muted); font-size: 12px; }
.slug-card .progress .bar { display: inline-block; width: 80px; height: 6px; background: #20232a; border-radius: 3px; margin-left: 8px; vertical-align: middle; overflow: hidden; }
.slug-card .progress .fill { display: block; height: 100%; background: var(--accent); }
.modal {
  display: none;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.6);
  align-items: center;
  justify-content: center;
  z-index: 100;
}
.modal.open { display: flex; }
.modal-box {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  max-width: 540px;
  width: 90%;
}
.modal-box h3 { margin-top: 0; }
.modal-box code {
  display: block;
  background: #0a0b0e;
  padding: 12px;
  border-radius: 8px;
  margin: 12px 0;
  font-family: "SF Mono", Menlo, Consolas, monospace;
  word-break: break-all;
}
"""


def render_index(slugs: list[str]) -> str:
    if not slugs:
        body = '<div class="empty"><h2>No articles yet</h2><p>Run <code>/blog-pipeline &lt;keyword&gt;</code> in Claude Code to start one.</p></div>'
    else:
        cards = []
        for slug in slugs:
            status = slug_status(slug)
            done_count = sum(1 for k, v in status.items() if v["done"] and k in CORE_STAGES)
            total = len(CORE_STAGES)
            pct = round(100 * done_count / total)
            cards.append(f'''
              <a class="slug-card" href="/slug/{html.escape(slug)}">
                <div class="name">{html.escape(slug)}</div>
                <div class="progress">{done_count} / {total} stages
                  <span class="bar"><span class="fill" style="width:{pct}%"></span></span>
                </div>
              </a>
            ''')
        body = f'<h2 style="margin-top:0">Articles</h2><div class="slug-list">{"".join(cards)}</div>'

    return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<title>Whiteboard — Blog Pipeline</title>
<style>{CSS}</style>
</head><body>
<div class="topbar">Whiteboard <span class="crumb">/</span> All articles</div>
<div class="main">{body}</div>
</body></html>"""


def render_slug_page(slug: str, status: dict, active_stage_key: str) -> str:
    sidebar_items = []
    for stage in STAGE_DICTS:
        s = status[stage["key"]]
        dot_class = "done" if s["done"] else "pending"
        dot_content = "✓" if s["done"] else "·"
        active_class = " active" if stage["key"] == active_stage_key else ""
        # truncate description
        desc = stage["description"][:50] + "..." if len(stage["description"]) > 50 else stage["description"]
        sidebar_items.append(f'''
          <a class="stage{active_class}" href="/slug/{html.escape(slug)}?stage={stage["key"]}" style="text-decoration:none;color:inherit;display:flex">
            <span class="dot {dot_class}">{dot_content}</span>
            <div class="info">
              <div class="name">{html.escape(stage["name"])}</div>
              <div class="desc">{html.escape(desc)}</div>
            </div>
          </a>
        ''')
    done_count = sum(1 for k, v in status.items() if v["done"] and k in CORE_STAGES)
    total = len(CORE_STAGES)
    badge = "Done" if done_count == total else "Active"

    main_panel = render_stage_panel(slug, active_stage_key, status[active_stage_key])

    return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<title>{html.escape(slug)} — Whiteboard</title>
<style>{CSS}</style>
</head><body>
<div class="topbar">
  <a href="/" style="color:var(--muted);margin-right:14px">← Back</a>
  Whiteboard <span class="crumb">/</span> <a href="/">Articles</a> <span class="crumb">/</span> {html.escape(slug)}
</div>
<div class="layout">
  <aside class="sidebar">
    <div class="meta">
      Pipeline progress: {done_count} / {total} core stages
      <span class="badge">{badge}</span>
    </div>
    {"".join(sidebar_items)}
  </aside>
  <main class="main">{main_panel}</main>
</div>
<div class="modal" id="rerunModal">
  <div class="modal-box">
    <h3>Re-run this stage</h3>
    <p>Paste this into Claude Code to re-run:</p>
    <code id="rerunCmd"></code>
    <button class="btn accent" onclick="copyCmd()">Copy to clipboard</button>
    <button class="btn" onclick="closeModal()" style="margin-left:8px">Close</button>
  </div>
</div>
<script>
function showRerun(cmd) {{
  document.getElementById('rerunCmd').textContent = cmd;
  document.getElementById('rerunModal').classList.add('open');
}}
function closeModal() {{ document.getElementById('rerunModal').classList.remove('open'); }}
function copyCmd() {{
  const cmd = document.getElementById('rerunCmd').textContent;
  navigator.clipboard.writeText(cmd).then(() => {{
    document.querySelector('#rerunModal .btn.accent').textContent = 'Copied ✓';
    setTimeout(() => closeModal(), 700);
  }});
}}
function showTab(tabName) {{
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tabName));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.toggle('active', p.dataset.panel === tabName));
}}
async function saveEdit(slug, stage) {{
  const body = document.getElementById('editor').value;
  const status = document.getElementById('saveStatus');
  status.textContent = 'Saving...';
  status.className = 'save-status';
  try {{
    const r = await fetch('/api/save?slug=' + encodeURIComponent(slug) + '&stage=' + encodeURIComponent(stage), {{
      method: 'POST',
      headers: {{ 'Content-Type': 'text/plain' }},
      body: body,
    }});
    if (!r.ok) {{ throw new Error(await r.text()); }}
    status.textContent = 'Saved.';
    status.className = 'save-status ok';
  }} catch (e) {{
    status.textContent = 'Error: ' + e.message;
    status.className = 'save-status err';
  }}
}}
</script>
</body></html>"""


def render_stage_panel(slug: str, stage_key: str, stage_status: dict) -> str:
    if stage_key not in STAGES_BY_KEY:
        return f'<div class="empty"><h2>Unknown stage</h2><p>{html.escape(stage_key)}</p></div>'
    stage = STAGES_BY_KEY[stage_key]
    done = stage_status["done"]
    rerun_cmd = f"/{stage['skill']} {slug}"
    status_btn = '<button class="btn done">Done</button>' if done else '<button class="btn">Pending</button>'
    actions = f'''
      {status_btn}
      <button class="btn" onclick="showRerun('{rerun_cmd}')">Re-run</button>
    '''

    if not done:
        body = f'''
          <div class="empty">
            <h2>Stage not run yet</h2>
            <p>Expected output at <code>{html.escape(stage_status["path"])}</code></p>
            <button class="btn accent" onclick="showRerun('{rerun_cmd}')">Run this stage</button>
          </div>
        '''
        return f'''
          <div class="stage-header">
            <span class="icon">🔍</span>
            <div>
              <h2 class="title">{html.escape(stage["name"])}</h2>
              <div class="desc">{html.escape(stage["description"])}</div>
            </div>
            <div class="actions">{actions}</div>
          </div>
          {body}
        '''

    # Stage is done — render preview + edit + skill tabs
    file_path = ROOT / stage_status["path"]
    raw = ""
    try:
        raw = file_path.read_text(encoding="utf-8")
    except Exception as e:
        raw = f"(error reading file: {e})"

    if stage["kind"] == "html":
        preview_html = f'<iframe class="preview-iframe" srcdoc="{html.escape(raw)}"></iframe>'
    else:
        preview_html = f'<div class="preview-box">{md_to_html(raw)}</div>'

    skill_md_path = SKILLS_DIR / stage["skill"] / "SKILL.md"
    skill_raw = skill_md_path.read_text(encoding="utf-8") if skill_md_path.exists() else f"(no SKILL.md found at {skill_md_path})"

    return f'''
      <div class="stage-header">
        <span class="icon">🔍</span>
        <div>
          <h2 class="title">Step: {html.escape(stage["name"])}</h2>
          <div class="desc">{html.escape(stage["description"])}</div>
        </div>
        <div class="actions">{actions}</div>
      </div>
      <div class="tabs">
        <div class="tab active" data-tab="preview" onclick="showTab('preview')">Preview</div>
        <div class="tab" data-tab="edit" onclick="showTab('edit')">Edit</div>
        <div class="tab" data-tab="skill" onclick="showTab('skill')">Skill</div>
        <div class="tab" data-tab="raw" onclick="showTab('raw')">Raw</div>
      </div>
      <div class="tab-panel active" data-panel="preview">{preview_html}</div>
      <div class="tab-panel" data-panel="edit">
        <textarea class="editor" id="editor">{html.escape(raw)}</textarea>
        <div class="save-row">
          <button class="btn accent" onclick="saveEdit('{html.escape(slug)}', '{stage_key}')">Save</button>
          <span class="save-status" id="saveStatus">File: <code>{html.escape(stage_status["path"])}</code></span>
        </div>
      </div>
      <div class="tab-panel" data-panel="skill">
        <div class="preview-box">{md_to_html(skill_raw)}</div>
      </div>
      <div class="tab-panel" data-panel="raw">
        <pre class="preview-box" style="white-space:pre-wrap">{html.escape(raw)}</pre>
      </div>
    '''


# -------------------- HTTP handler --------------------

class WhiteboardHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write(f"[whiteboard] {self.address_string()} {fmt % args}\n")

    def _send(self, status: int, content: str, content_type: str = "text/html; charset=utf-8"):
        body = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        path = u.path
        params = parse_qs(u.query)

        if path == "/" or path == "":
            return self._send(200, render_index(list_slugs()))

        if path.startswith("/slug/"):
            slug = path.split("/slug/", 1)[1].rstrip("/")
            if not slug:
                return self._send(404, "<h1>Slug missing</h1>")
            status = slug_status(slug)
            stage_key = (params.get("stage") or [None])[0]
            if not stage_key:
                # default: pick the first done stage, fall back to research
                done_stages = [s["key"] for s in STAGE_DICTS if status[s["key"]]["done"]]
                stage_key = done_stages[0] if done_stages else "research"
            return self._send(200, render_slug_page(slug, status, stage_key))

        return self._send(404, "<h1>Not found</h1>")

    def do_POST(self):
        u = urlparse(self.path)
        if u.path != "/api/save":
            return self._send(404, "Not found", "text/plain")
        params = parse_qs(u.query)
        slug = (params.get("slug") or [None])[0]
        stage_key = (params.get("stage") or [None])[0]
        if not slug or stage_key not in STAGES_BY_KEY:
            return self._send(400, "missing slug or stage", "text/plain")
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length).decode("utf-8")
        stage = STAGES_BY_KEY[stage_key]
        target = stage_path(slug, stage)
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(body, encoding="utf-8")
        except Exception as e:
            return self._send(500, f"write failed: {e}", "text/plain")
        return self._send(200, json.dumps({"ok": True, "path": str(target.relative_to(ROOT))}), "application/json")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), WhiteboardHandler)
    print(f"Whiteboard running at http://{args.host}:{args.port}", file=sys.stderr)
    print("Press Ctrl+C to stop.", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nshutdown.", file=sys.stderr)


if __name__ == "__main__":
    main()
