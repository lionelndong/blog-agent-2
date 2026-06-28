#!/usr/bin/env python3
"""Render premium, ON-BRAND comparison / pricing / feature-grid "table cards" (2026-06-28 v3).

Generative image models mangle in-image text, so any [VISUAL] that is fundamentally a
table, checklist, pricing matrix or feature grid is rendered HERE — crisp real text,
the Pleasur.AI brand card (white card on #F7F8FA, IBM Plex Sans title + Geist body via
Google Fonts, brand palette, real logo bottom-right). Rendered HTML headless via patchright,
exactly like render_chart_web.py — screenshots the #wrap element. Free, answer-engine
friendly, accessible.

Spec types (spec.type):
  - "comparison" : rows = features, cols = products, ✓/✗/partial or text cells; OUR col highlighted blue.
  - "pricing"    : cols = plans (name/price/period/tagline), feature rows, popular plan highlighted, optional CTA.
  - "grid"       : a grid of feature cards (icon + title + desc).

Usage:
  python render_table_card.py --spec spec.json --out out.png
  python render_table_card.py --data '<inline json>' --out out.png
"""
from __future__ import annotations
import argparse
import base64
import html as _html
import json
import re
import sys
from pathlib import Path

# ---- Brand system (mirrors render_chart_web.py) ----------------------------------------
PALETTE = ["#2E90FA", "#8B5CF6", "#22B276", "#F5A623", "#E8655A", "#0891B2", "#534AB7"]
BLUE = "#2E90FA"
FONT = "'Geist', system-ui, -apple-system, 'Segoe UI', sans-serif"        # blog body font
TITLE_FONT = "'IBM Plex Sans', 'Geist', system-ui, sans-serif"            # blog heading font
INK = "#1E2430"
MUTE = "#7A828F"
FAINT = "#9AA2AE"
LINE = "#EDF0F4"

# ---- Cell mark chips (clean inline SVG, never emoji) ------------------------------------
CHIP_Y = ('<span class="chip chip-y"><svg width="15" height="15" viewBox="0 0 24 24" fill="none">'
          '<path d="M5 12.5l4.2 4.2L19 7" stroke="#1FA971" stroke-width="2.7" '
          'stroke-linecap="round" stroke-linejoin="round"/></svg></span>')
CHIP_N = ('<span class="chip chip-n"><svg width="13" height="13" viewBox="0 0 24 24" fill="none">'
          '<path d="M6 6l12 12M18 6L6 18" stroke="#B0B7C3" stroke-width="2.6" '
          'stroke-linecap="round"/></svg></span>')
CHIP_P = ('<span class="chip chip-p"><svg width="16" height="16" viewBox="0 0 24 24" fill="none">'
          '<circle cx="12" cy="12" r="8.5" stroke="#E0930F" stroke-width="2.2"/>'
          '<path d="M12 3.5a8.5 8.5 0 0 0 0 17z" fill="#E0930F"/></svg></span>')

YES = {"check", "yes", "true", "✓", "y", "included", "full", "1"}
NO = {"cross", "no", "false", "✗", "✘", "x", "none", "-", "—", "n", "0"}
PART = {"partial", "limited", "~", "◐", "some", "half", "basic"}

# ---- Line-icon set for feature grids (Lucide-style, stroke=currentColor) ----------------
ICONS = {
    "chat": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "heart": '<path d="M19.5 12.6 12 20l-7.5-7.4A5 5 0 0 1 12 6a5 5 0 0 1 7.5 6.6z"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8.5" cy="8.5" r="1.6"/><path d="M21 15l-5-5L5 21"/>',
    "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "sparkle": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
    "infinity": '<path d="M18.2 8a4 4 0 1 0 0 8c-2.5 0-4-2.7-5.2-4-1.2-1.3-2.7-4-5.2-4a4 4 0 1 0 0 8c2.5 0 4-2.7 5.2-4"/>',
    "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17.8 6.6 20l1-6.1L3.2 9.5l6.1-.9z"/>',
    "palette": '<path d="M12 3a9 9 0 1 0 0 18 2 2 0 0 0 2-2 2 2 0 0 1 2-2h1a4 4 0 0 0 4-4 9 9 0 0 0-9-8z"/><circle cx="7.5" cy="10.5" r="1"/><circle cx="12" cy="7.5" r="1"/><circle cx="16.5" cy="10.5" r="1"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18 14 14 0 0 1 0-18z"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "video": '<rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3z"/>',
    "bell": '<path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M10.5 21a2 2 0 0 0 3 0"/>',
    "coin": '<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v6c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 12v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>',
    "memory": '<path d="M9.5 4a2.5 2.5 0 0 0-2.5 2.5A3 3 0 0 0 5 12a3 3 0 0 0 2 4.5A2.5 2.5 0 0 0 12 18V6.5A2.5 2.5 0 0 0 9.5 4z"/><path d="M14.5 4A2.5 2.5 0 0 1 17 6.5 3 3 0 0 1 19 12a3 3 0 0 1-2 4.5A2.5 2.5 0 0 1 12 18"/>',
    "gift": '<rect x="3" y="8" width="18" height="13" rx="2"/><path d="M3 12h18M12 8v13M12 8S10 3 7.5 4 9 8 12 8s2.5-3.5 4.5-4S12 8 12 8z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "check": '<path d="M5 12.5l4.5 4.5L20 6"/>',
}


_MD_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def clean_md(s) -> str:
    """Strip light inline markdown (links, bold/italic, code) so GFM cells read clean."""
    s = _MD_LINK.sub(r"\1", str(s))
    return s.replace("**", "").replace("__", "").replace("`", "")


def esc(s) -> str:
    return _html.escape(str(s if s is not None else ""))


def tint(hexc: str, a: float = 0.12) -> str:
    h = hexc.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{a})"


def icon_svg(name: str, color: str) -> str:
    p = ICONS.get(str(name).strip().lower(), ICONS["sparkle"])
    return (f'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="{color}" '
            f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{p}</svg>')


def cell_html(tok) -> str:
    """Render one comparison/pricing cell: a mark chip or literal text (+optional sub)."""
    if isinstance(tok, bool):
        return CHIP_Y if tok else CHIP_N
    if isinstance(tok, dict):
        icon = str(tok.get("icon", "")).strip().lower()
        inner = ""
        if icon in YES:
            inner = CHIP_Y
        elif icon in NO:
            inner = CHIP_N
        elif icon in PART:
            inner = CHIP_P
        txt = tok.get("text")
        if txt:
            inner += f'<span class="val">{esc(clean_md(txt))}</span>'
        sub = tok.get("note") or tok.get("sub")
        if sub:
            inner += f'<span class="val-sub">{esc(clean_md(sub))}</span>'
        return inner or "—"
    t = str(tok).strip().lower()
    if t == "":
        return ""
    if t in YES:
        return CHIP_Y
    if t in NO:
        return CHIP_N
    if t in PART:
        return CHIP_P
    return f'<span class="val">{esc(clean_md(tok))}</span>'


# Generic GFM-table cell tokens (conservative — only convert unambiguous words/symbols;
# leave "-", "—", "N/A", numbers and prose as literal text so meaning is preserved).
YES_G = {"yes", "✓", "✔", "true"}
NO_G = {"no", "✗", "✘", "✕", "false"}
PART_G = {"partial", "limited", "~", "◐", "sometimes", "some"}


def gen_cell(tok) -> str:
    raw = str(tok).strip()
    t = raw.lower()
    if t in YES_G:
        return CHIP_Y
    if t in NO_G:
        return CHIP_N
    if t in PART_G:
        return CHIP_P
    if raw == "":
        return '<span style="color:#C2C8D2">—</span>'
    return esc(clean_md(raw))


# ---- The brand card shell (token-replaced; CSS braces stay literal) ---------------------
TEMPLATE = """<!doctype html><html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=IBM+Plex+Sans:wght@500;600;700&display=swap');
*{box-sizing:border-box}
body{margin:0;font-family:__FONT__;-webkit-font-smoothing:antialiased}
#wrap{display:inline-block;padding:46px;background:#F7F8FA}
#card{width:__CARDW__px;background:#fff;border:1px solid #EDF0F4;border-radius:20px;padding:30px 34px 20px;box-shadow:0 14px 46px rgba(20,30,50,0.08)}
#t{font-family:__TFONT__;font-size:23px;font-weight:700;color:#1E2430;letter-spacing:-0.3px;line-height:1.25}
#s{font-size:14.5px;color:#7A828F;margin:6px 0 0;line-height:1.5;max-width:760px}
#f{text-align:right;margin-top:18px;opacity:.95}
#f img{vertical-align:middle}

/* ---------- comparison / pricing table ---------- */
table.cmp{border-collapse:separate;border-spacing:0;width:100%;margin-top:22px}
.cmp th,.cmp td{padding:15px 16px;text-align:center;vertical-align:middle}
.cmp .feat-h{text-align:left;color:#9AA2AE;font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.8px;width:34%}
.cmp thead th:not(.ours){border-bottom:1px solid #E6E9EF}
.cmp td.feat{text-align:left}
.cmp .fname{font-weight:600;color:#1E2430;font-size:15px}
.cmp .fnote{display:block;color:#9AA2AE;font-size:12.5px;font-weight:400;margin-top:2px;line-height:1.4}
.cmp tbody tr + tr td:not(.ours){border-top:1px solid #EDF0F4}
.cmp td.cta-cell{border-top:none}
.cmp .prodname{display:block;font-family:__TFONT__;font-size:16.5px;font-weight:700;color:#1E2430}
.cmp .prodsub{display:block;font-size:12px;font-weight:400;color:#9AA2AE;margin-top:3px}

/* mark chips + values */
.chip{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:50%}
.chip-y{background:#E7F7EF}
.chip-n{background:#F1F3F6}
.chip-p{background:#FEF3E2}
.val{display:block;font-weight:600;color:#3A4250;font-size:14px}
.val-sub{display:block;color:#9AA2AE;font-size:11.5px;font-weight:400;margin-top:2px}

/* generic GFM table (legacy format from format-for-publish: cols=strings, rows=lists) */
.cmp.gen th,.cmp.gen td{text-align:left;padding:13px 16px}
.cmp.gen thead th{background:#F5F7FB;font-family:__TFONT__;font-weight:700;color:#1E2430;font-size:14px}
.cmp.gen thead th:first-child{border-radius:10px 0 0 0}
.cmp.gen thead th:last-child{border-radius:0 10px 0 0}
.cmp.gen tbody td:first-child{font-weight:600;color:#1E2430}
.cmp.gen tbody td{color:#3A4250;font-size:14px;line-height:1.5}

/* highlighted (ours / popular) column = a blue card column */
.cmp thead th.ours{color:#fff;background:linear-gradient(180deg,#409DFB,#2E90FA);border-radius:16px 16px 0 0;box-shadow:0 12px 26px rgba(46,144,250,.30);position:relative}
.cmp tbody td.ours{background:#F4F9FF;border-left:2px solid #2E90FA;border-right:2px solid #2E90FA}
.cmp tbody tr:last-child td.ours{border-bottom:2px solid #2E90FA;border-radius:0 0 16px 16px}
.cmp thead th.ours .prodname{color:#fff}
.cmp thead th.ours .prodsub{color:#D6E9FF}
.cmp .badge{display:inline-block;background:rgba(255,255,255,.22);color:#fff;font-size:11px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;padding:4px 11px;border-radius:20px;margin-bottom:9px}

/* pricing header block */
.pname{font-family:__TFONT__;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.7px;color:#7A828F}
th.ours .pname{color:#DCEBFF}
.pprice{font-family:__TFONT__;font-size:31px;font-weight:700;color:#1E2430;margin-top:7px;letter-spacing:-.6px;line-height:1}
th.ours .pprice{color:#fff}
.per{font-size:14px;font-weight:600;color:#9AA2AE;margin-left:2px}
th.ours .per{color:#CFE4FF}
.ptag{font-size:12.5px;color:#9AA2AE;margin-top:6px;font-weight:500}
th.ours .ptag{color:#DCEBFF}

/* pricing CTA row */
.cta-cell{padding-top:20px;padding-bottom:6px}
.cta-btn{display:inline-block;padding:11px 22px;border-radius:11px;font-weight:600;font-size:14px;font-family:__FONT__}
.cta-out{border:1.5px solid #D7DCE4;color:#3A4250}
.cta-fill{background:#2E90FA;color:#fff;box-shadow:0 8px 18px rgba(46,144,250,.28)}

/* ---------- feature grid ---------- */
.grid{display:grid;gap:16px;margin-top:24px}
.gi{background:#FBFCFE;border:1px solid #EDF0F4;border-radius:16px;padding:20px 20px 22px}
.gi-ic{width:46px;height:46px;border-radius:13px;display:flex;align-items:center;justify-content:center}
.gi-t{font-family:__TFONT__;font-size:16.5px;font-weight:700;color:#1E2430;margin-top:15px;letter-spacing:-.2px}
.gi-d{font-size:13.5px;color:#7A828F;margin-top:7px;line-height:1.55}
</style></head><body>
<div id="wrap"><div id="card">
<div id="t">__TITLE__</div>__SUB__
__BODY__
<div id="f">__LOGO__</div>
</div></div></body></html>"""


def card_page(title, subtitle, body, logo_html, card_w) -> str:
    sub = f'<div id="s">{esc(subtitle)}</div>' if subtitle else ""
    return (TEMPLATE
            .replace("__FONT__", FONT)
            .replace("__TFONT__", TITLE_FONT)
            .replace("__CARDW__", str(card_w))
            .replace("__TITLE__", esc(title))
            .replace("__SUB__", sub)
            .replace("__BODY__", body)
            .replace("__LOGO__", logo_html))


def _hi_index(cols):
    for i, c in enumerate(cols):
        if isinstance(c, dict) and c.get("highlight"):
            return i
    return -1


def render_comparison(spec):
    cols = spec["columns"]
    rows = spec["rows"]
    hi = _hi_index(cols)
    nprod = len(cols)
    card_w = max(780, min(1160, 300 + nprod * 230))

    ths = [f'<th class="feat-h">{esc(spec.get("featureHeader", ""))}</th>']
    for i, c in enumerate(cols):
        ours = i == hi
        cls = "prod ours" if ours else "prod"
        badge = f'<div class="badge">{esc(c.get("badge"))}</div>' if c.get("badge") else ""
        sub = f'<span class="prodsub">{esc(c.get("sub"))}</span>' if c.get("sub") else ""
        ths.append(f'<th class="{cls}">{badge}<span class="prodname">{esc(c["name"])}</span>{sub}</th>')
    head = "<thead><tr>" + "".join(ths) + "</tr></thead>"

    trs = []
    for r in rows:
        note = f'<span class="fnote">{esc(r.get("note"))}</span>' if r.get("note") else ""
        tds = [f'<td class="feat"><span class="fname">{esc(r["feature"])}</span>{note}</td>']
        for i, val in enumerate(r["cells"]):
            cls = "cell ours" if i == hi else "cell"
            tds.append(f'<td class="{cls}">{cell_html(val)}</td>')
        trs.append("<tr>" + "".join(tds) + "</tr>")
    body = f'<table class="cmp">{head}<tbody>{"".join(trs)}</tbody></table>'
    return body, card_w


def render_pricing(spec):
    cols = spec["columns"]
    rows = spec["rows"]
    hi = _hi_index(cols)
    nprod = len(cols)
    card_w = max(840, min(1180, 330 + nprod * 250))

    ths = [f'<th class="feat-h">{esc(spec.get("featureHeader", ""))}</th>']
    for i, c in enumerate(cols):
        ours = i == hi
        cls = "prod ours" if ours else "prod"
        badge = f'<div class="badge">{esc(c.get("badge"))}</div>' if c.get("badge") else ""
        per = f'<span class="per">{esc(c.get("period"))}</span>' if c.get("period") else ""
        tag = f'<div class="ptag">{esc(c.get("tagline"))}</div>' if c.get("tagline") else ""
        ths.append(f'<th class="{cls}">{badge}<div class="pname">{esc(c["name"])}</div>'
                   f'<div class="pprice">{esc(c.get("price", ""))}{per}</div>{tag}</th>')
    head = "<thead><tr>" + "".join(ths) + "</tr></thead>"

    trs = []
    for r in rows:
        note = f'<span class="fnote">{esc(r.get("note"))}</span>' if r.get("note") else ""
        tds = [f'<td class="feat"><span class="fname">{esc(r["feature"])}</span>{note}</td>']
        for i, val in enumerate(r["cells"]):
            cls = "cell ours" if i == hi else "cell"
            tds.append(f'<td class="{cls}">{cell_html(val)}</td>')
        trs.append("<tr>" + "".join(tds) + "</tr>")

    cta_label = spec.get("cta")
    if cta_label:
        cells = [f'<td class="feat cta-cell"></td>']
        for i, c in enumerate(cols):
            ours = i == hi
            wrapcls = "cell cta-cell ours" if ours else "cell cta-cell"
            label = c.get("cta") or cta_label
            btn = "cta-btn cta-fill" if ours else "cta-btn cta-out"
            cells.append(f'<td class="{wrapcls}"><span class="{btn}">{esc(label)}</span></td>')
        trs.append("<tr>" + "".join(cells) + "</tr>")

    body = f'<table class="cmp">{head}<tbody>{"".join(trs)}</tbody></table>'
    return body, card_w


def render_grid(spec):
    items = spec["items"]
    gcols = int(spec.get("columns", 3))
    card_w = max(640, min(1100, 290 * gcols + 80))
    cells = []
    for n, it in enumerate(items):
        color = it.get("color") or PALETTE[n % 5]
        chip = f'<div class="gi-ic" style="background:{tint(color,0.12)}">{icon_svg(it.get("icon","sparkle"), color)}</div>'
        desc = f'<div class="gi-d">{esc(it.get("desc"))}</div>' if it.get("desc") else ""
        cells.append(f'<div class="gi">{chip}<div class="gi-t">{esc(it["title"])}</div>{desc}</div>')
    body = f'<div class="grid" style="grid-template-columns:repeat({gcols},1fr)">{"".join(cells)}</div>'
    return body, card_w


def render_table(spec):
    """Generic table-card for a plain GFM table (cols=strings, rows=lists). No highlight
    column — clean brand framing, left-aligned, yes/no/partial → chips, markdown stripped.
    This is the path format-for-publish uses for the PLEAA-567 GFM workaround."""
    cols = list(spec["columns"])
    rows = spec["rows"]
    ncol = max(1, len(cols))
    card_w = max(680, min(1180, 220 * ncol + 150))
    head = "<thead><tr>" + "".join(f"<th>{esc(clean_md(c))}</th>" for c in cols) + "</tr></thead>"
    trs = []
    for r in rows:
        cells = list(r) + [""] * (ncol - len(r))
        tds = "".join(f"<td>{gen_cell(c)}</td>" for c in cells[:ncol])
        trs.append(f"<tr>{tds}</tr>")
    body = f'<table class="cmp gen">{head}<tbody>{"".join(trs)}</tbody></table>'
    return body, card_w


DISPATCH = {"comparison": render_comparison, "pricing": render_pricing,
            "grid": render_grid, "table": render_table}


def detect_type(spec):
    """Resolve spec.type, defaulting legacy/auto cases. Legacy GFM specs have no
    `type` and `columns` as a list of plain strings → generic table."""
    t = spec.get("type")
    if t:
        return t
    if "items" in spec:
        return "grid"
    cols = spec.get("columns")
    if cols and isinstance(cols[0], str):
        return "table"
    return "comparison"


def shoot(html_str, out, card_w):
    try:
        from patchright.sync_api import sync_playwright
    except ImportError:
        from playwright.sync_api import sync_playwright
    vw = card_w + 92 + 140
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--no-sandbox"])
        pg = b.new_context(viewport={"width": vw, "height": 1000}, device_scale_factor=2).new_page()
        pg.set_content(html_str, wait_until="networkidle")
        try:
            pg.wait_for_function("document.fonts && document.fonts.status === 'loaded'", timeout=5000)
        except Exception:
            pass
        pg.wait_for_timeout(450)
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        pg.locator("#wrap").screenshot(path=out)
        b.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", help="path to spec JSON")
    ap.add_argument("--data", help="inline spec JSON")
    ap.add_argument("--out", required=True)
    ap.add_argument("--logo", default=str(Path(__file__).resolve().parent / "pleasurai-logo.png"))
    a = ap.parse_args()

    if a.spec:
        spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    elif a.data:
        spec = json.loads(a.data)
    else:
        print(json.dumps({"status": "failed", "reason": "no_spec"}))
        return 1

    ctype = detect_type(spec)
    fn = DISPATCH.get(ctype)
    if not fn:
        print(json.dumps({"status": "failed", "reason": "unknown_type", "type": ctype}))
        return 1

    try:
        logo_uri = "data:image/png;base64," + base64.b64encode(Path(a.logo).read_bytes()).decode()
        logo_html = f'<img src="{logo_uri}" height="23" alt="Pleasur.ai">'
    except Exception:
        logo_html = '<span style="font-weight:700;color:#B4BAC4">Pleasur.AI</span>'

    body, card_w = fn(spec)
    html_str = card_page(spec.get("title", ""), spec.get("subtitle", ""), body, logo_html, card_w)
    shoot(html_str, a.out, card_w)
    print(json.dumps({"status": "captured", "path": a.out, "type": ctype, "renderer": "table-card", "card_w": card_w}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
