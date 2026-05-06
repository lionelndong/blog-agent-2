#!/usr/bin/env python3
"""Generate a self-contained Whiteboard-style HTML viewer for a single slug.

Reads every stage's file from the local content-pipeline/ tree and bakes
the contents into a single HTML file. Output renders entirely client-side
with no external fetches — works as an offline file or on any host.
"""
import json
import sys
from pathlib import Path
from html import escape

REPO_ROOT = Path(__file__).resolve().parent.parent
CP = REPO_ROOT / "content-pipeline"

STAGES = [
    {
        "key": "1-research",
        "name": "Research",
        "desc": "SERP analysis + competitor pull + deep-research synthesis",
        "files": lambda slug: [
            ("broad", f"1-research/{slug}.md", "md"),
            ("deep", f"1-research/{slug}-deep.md", "md"),
            ("data", f"1-research/{slug}-data.json", "json"),
        ],
    },
    {
        "key": "2-reference",
        "name": "Reference",
        "desc": "Reference snapshot of competitor article structure / tone",
        "files": lambda slug: [("reference", f"2-reference/{slug}.md", "md")],
    },
    {
        "key": "3-outlines",
        "name": "Outline",
        "desc": "Structured H2/H3 outline with BLUF openers",
        "files": lambda slug: [("outline", f"3-outlines/{slug}.md", "md")],
    },
    {
        "key": "4-outlines-annotated",
        "name": "Outline annotated",
        "desc": "Outline + citation slots + visual placement",
        "files": lambda slug: [("annotated", f"4-outlines-annotated/{slug}.md", "md")],
    },
    {
        "key": "5-drafts",
        "name": "Draft",
        "desc": "Full article draft (target 2,000-2,300 words)",
        "files": lambda slug: [("draft", f"5-drafts/{slug}.md", "md")],
    },
    {
        "key": "6-drafts-cited",
        "name": "Verify Claims",
        "desc": "Source citations + hyperlinks resolved",
        "files": lambda slug: [("cited draft", f"6-drafts-cited/{slug}.md", "md")],
    },
    {
        "key": "visuals",
        "name": "Visuals",
        "desc": "Image generation / action-shot capture manifest",
        "files": lambda slug: [
            ("manifest", f"images/{slug}/manifest.json", "json"),
            ("manual capture", f"images/{slug}/manual-capture.md", "md"),
        ],
    },
    {
        "key": "7-preview",
        "name": "Preview",
        "desc": "Rendered HTML preview as readers will see it",
        "files": lambda slug: [("preview", f"7-preview/{slug}.html", "html")],
    },
    {
        "key": "quality-checks",
        "name": "Quality check",
        "desc": "Auto metrics + adversarial reader + verdict (PASS / FAIL)",
        "files": lambda slug: [
            ("verdict", f"quality-checks/{slug}.md", "md"),
            ("metrics", f"quality-checks/{slug}-metrics.md", "md"),
            ("adversarial", f"quality-checks/{slug}-adversarial.md", "md"),
        ],
    },
    {
        "key": "8-publish",
        "name": "Publish package",
        "desc": "Strapi-ready article.md + article.json + paste/publish README",
        "files": lambda slug: [
            ("article.md", f"8-publish/{slug}/article.md", "md"),
            ("article.json", f"8-publish/{slug}/article.json", "json"),
            ("README", f"8-publish/{slug}/README.md", "md"),
        ],
    },
]


def load_stage(slug, stage):
    out = []
    for label, rel, kind in stage["files"](slug):
        p = CP / rel
        if p.exists():
            try:
                txt = p.read_text(encoding="utf-8")
                out.append({"label": label, "path": rel, "kind": kind, "ok": True, "content": txt})
            except Exception as e:
                out.append({"label": label, "path": rel, "kind": kind, "ok": False, "content": f"read error: {e}"})
        else:
            out.append({"label": label, "path": rel, "kind": kind, "ok": False, "content": ""})
    return out


def build_data(slug):
    stages = []
    for s in STAGES:
        files = load_stage(slug, s)
        any_ok = any(f["ok"] for f in files)
        stages.append({
            "key": s["key"],
            "name": s["name"],
            "desc": s["desc"],
            "done": any_ok,
            "files": files,
        })
    return {"slug": slug, "stages": stages}


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>__SLUG__ · pipeline</title>
<style>
:root { --bg: #0e0e10; --panel: #17171a; --panel-2: #1f1f23; --border: #2a2a30; --text: #e7e7ea; --text-dim: #9a9aa3; --accent: #f59e0b; --green: #22c55e; --gray: #4b5563; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: var(--bg); color: var(--text); font: 14px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; }
a { color: var(--accent); }
header.topbar { display: flex; align-items: center; justify-content: space-between; padding: 14px 22px; border-bottom: 1px solid var(--border); background: var(--panel); }
header.topbar h1 { font-size: 14px; font-weight: 600; margin: 0; color: var(--text-dim); letter-spacing: 0.02em; }
header.topbar .meta { color: var(--text-dim); font-size: 12px; }
.app { display: grid; grid-template-columns: 320px 1fr; min-height: calc(100vh - 50px); }
aside { border-right: 1px solid var(--border); background: var(--panel); padding: 22px 16px; overflow-y: auto; max-height: calc(100vh - 50px); }
.run-header { padding: 4px 6px 18px; border-bottom: 1px solid var(--border); margin-bottom: 14px; }
.run-header .title { font-size: 18px; font-weight: 700; margin: 0 0 4px; }
.run-header .meta { color: var(--text-dim); font-size: 12px; }
.run-header .badge { display: inline-block; background: rgba(245, 158, 11, 0.15); color: var(--accent); font-size: 11px; padding: 2px 9px; border-radius: 4px; margin-top: 8px; font-weight: 600; }
.steps { list-style: none; padding: 0; margin: 0; }
.steps li { display: flex; gap: 10px; padding: 10px 8px; cursor: pointer; border-radius: 6px; border: 1px solid transparent; margin-bottom: 4px; }
.steps li:hover { background: var(--panel-2); }
.steps li.active { background: var(--panel-2); border-color: var(--border); }
.steps .dot { width: 22px; height: 22px; border-radius: 50%; flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; border: 1.5px solid var(--gray); color: var(--text-dim); }
.steps li.done .dot { background: var(--green); border-color: var(--green); color: #0e0e10; }
.steps li.done .dot::before { content: "✓"; }
.steps li.skipped .dot::before { content: "·"; }
.steps li.active .dot { box-shadow: 0 0 0 2px var(--accent) inset; }
.steps .step-name { font-weight: 600; font-size: 13px; }
.steps .step-desc { color: var(--text-dim); font-size: 11.5px; line-height: 1.4; margin-top: 2px; }
main { padding: 22px 28px; overflow-y: auto; max-height: calc(100vh - 50px); }
.viewer-head { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 18px; }
.viewer-head h2 { margin: 0; font-size: 20px; color: var(--accent); font-weight: 700; }
.viewer-head .desc { color: var(--text-dim); margin-top: 4px; font-size: 13px; }
.tabs { display: flex; gap: 0; border-bottom: 1px solid var(--border); margin-bottom: 16px; }
.tab { padding: 8px 16px; cursor: pointer; color: var(--text-dim); font-size: 13px; border-bottom: 2px solid transparent; }
.tab.active { color: var(--accent); border-color: var(--accent); }
.path-line { font-size: 11.5px; color: var(--text-dim); margin-bottom: 12px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.content { background: var(--panel); border: 1px solid var(--border); border-radius: 8px; padding: 22px 26px; min-height: 400px; }
.content h2 { color: var(--accent); border-bottom: 1px solid var(--border); padding-bottom: 6px; margin-top: 28px; }
.content h2:first-child, .content h1:first-child { margin-top: 0; }
.content table { border-collapse: collapse; width: 100%; margin: 12px 0; }
.content th, .content td { border: 1px solid var(--border); padding: 8px 10px; text-align: left; font-size: 13px; }
.content th { background: var(--panel-2); }
.content code { background: var(--panel-2); padding: 1px 5px; border-radius: 3px; font-size: 12.5px; }
.content pre { background: var(--panel-2); padding: 12px; border-radius: 6px; overflow-x: auto; font-size: 12.5px; border: 1px solid var(--border); white-space: pre-wrap; }
.content blockquote { border-left: 3px solid var(--accent); padding: 4px 14px; color: var(--text-dim); margin: 14px 0; }
.content iframe { width: 100%; border: 1px solid var(--border); border-radius: 6px; background: white; }
.empty { color: var(--text-dim); padding: 50px 0; text-align: center; }
.empty .label { font-size: 12px; opacity: 0.6; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.06em; }
</style>
</head>
<body>

<header class="topbar">
  <h1>Whiteboard · Blog pipeline</h1>
  <div class="meta">offline bundle · all data inlined · open this file anywhere</div>
</header>

<div id="app"></div>

<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<script id="data-json" type="application/json">__DATA__</script>
<script>
const DATA = JSON.parse(document.getElementById("data-json").textContent);
const SLUG = DATA.slug;
const STAGES = DATA.stages;
const app = document.getElementById("app");

let active = { stage: STAGES[0].key, file: 0 };
const hash = location.hash.replace(/^#/, "").split("/");
if (hash[0]) active.stage = hash[0];
if (hash[1]) active.file = parseInt(hash[1]) || 0;

window.addEventListener("hashchange", () => {
  const h = location.hash.replace(/^#/, "").split("/");
  active.stage = h[0] || STAGES[0].key;
  active.file = parseInt(h[1]) || 0;
  render();
});

function escapeHtml(s) { return s.replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c]); }

function render() {
  const stage = STAGES.find(s => s.key === active.stage) || STAGES[0];
  const fileIdx = Math.min(active.file, stage.files.length - 1);
  const file = stage.files[fileIdx];
  const doneCount = STAGES.filter(s => s.done).length;

  app.innerHTML = `
    <div class="app">
      <aside>
        <div class="run-header">
          <div class="title">${escapeHtml(SLUG)}</div>
          <div class="meta">github.com/lionelndong/blog-agent-2 (private)</div>
          <span class="badge">${doneCount}/${STAGES.length} stages produced</span>
        </div>
        <ul class="steps">
          ${STAGES.map(s => `
            <li class="${s.key === stage.key ? 'active' : ''} ${s.done ? 'done' : 'skipped'}" onclick="location.hash='#${s.key}'">
              <span class="dot"></span>
              <div>
                <div class="step-name">${escapeHtml(s.name)}</div>
                <div class="step-desc">${escapeHtml(s.desc)}</div>
              </div>
            </li>`).join("")}
        </ul>
      </aside>
      <main>
        <div class="viewer-head">
          <div>
            <h2>${escapeHtml(stage.name)}</h2>
            <div class="desc">${escapeHtml(stage.desc)}</div>
          </div>
        </div>
        <div class="tabs">
          ${stage.files.map((f, i) => `<div class="tab ${i === fileIdx ? 'active' : ''}" onclick="location.hash='#${stage.key}/${i}'">${escapeHtml(f.label)}${f.ok ? "" : " (missing)"}</div>`).join("")}
        </div>
        <div class="path-line">${escapeHtml(file.path)}</div>
        <div class="content" id="content"></div>
      </main>
    </div>`;

  const target = document.getElementById("content");
  if (!file.ok) {
    target.innerHTML = `<div class="empty"><div class="label">stage not produced</div><p>This stage didn't write a file for this slug. Either the pipeline skipped it, or it errored — check the optimization log.</p></div>`;
    return;
  }
  if (file.kind === "html") {
    target.innerHTML = `<iframe srcdoc="${file.content.replace(/"/g, "&quot;")}" style="width:100%;height:80vh;"></iframe>`;
  } else if (file.kind === "json") {
    let pretty = file.content;
    try { pretty = JSON.stringify(JSON.parse(file.content), null, 2); } catch (e) {}
    target.innerHTML = `<pre>${escapeHtml(pretty)}</pre>`;
  } else {
    target.innerHTML = marked.parse(file.content);
  }
}
render();
</script>

</body>
</html>
"""


def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else "what-is-an-ai-girlfriend"
    out_path = REPO_ROOT / "docs" / f"run-{slug}.html"
    data = build_data(slug)
    # Embed JSON safely inside <script type="application/json">: only need to
    # escape </script. JSON itself doesn't need HTML-escaping in this context.
    data_json = json.dumps(data).replace("</", "<\\/")
    html = HTML_TEMPLATE.replace("__SLUG__", slug).replace("__DATA__", data_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"wrote {out_path} ({out_path.stat().st_size:,} bytes)")
    print(f"stages produced: {sum(1 for s in data['stages'] if s['done'])}/{len(data['stages'])}")


if __name__ == "__main__":
    main()
