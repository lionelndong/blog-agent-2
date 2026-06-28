#!/usr/bin/env python3
"""Render premium, ON-BRAND stat / quote / callout cards headless in the browser (2026-06-28 v1).

Fourth visual type after annotation, infographic, chart. Same brand card standard as
`render_chart_web.py`: white card (#fff, border #EDF0F4, radius 20, soft shadow) on #F7F8FA,
IBM Plex Sans title + Geist body (Google Fonts @import), the REAL Pleasur.ai logo bottom-right.
HTML is rendered headless via patchright and the #wrap element is screenshotted at 2x.

Sub-types (set by "kind" in the spec):
  stat    — 1-3 big numbers + label, optional unit / delta-trend pill / icon / sub-line
  quote   — a pull-quote + attribution; 4 styles via "style": bar (default, editorial left
            rule) / mark (big quote glyph) / review (star rating + source chip) / highlight
  callout — a "Key takeaway" / tip / warning box: accent rail + icon + label + text

Usage:
  python render_card_web.py --spec card.json --out card.png
  python render_card_web.py --json '{"kind":"stat","stats":[...]}' --out card.png
"""
import argparse
import base64
import html as _html
import json
import sys
from pathlib import Path

# ---- Brand tokens (identical to render_chart_web.py) -----------------------------------
PALETTE = ["#2E90FA", "#8B5CF6", "#22B276", "#F5A623", "#E8655A", "#0891B2", "#534AB7"]
INK = "#1E2430"        # primary text / big numbers
INK_SOFT = "#2B313C"   # strong labels
BODY = "#39414C"       # body copy
MUTED = "#7A828F"      # secondary text
FAINT = "#9AA2AE"      # tertiary / footnotes
PAGE = "#F7F8FA"
CARD_BORDER = "#EDF0F4"
HAIRLINE = "#F1F3F7"
DIVIDER = "#ECEFF4"

BODY_FONT = "'Geist', system-ui, -apple-system, 'Segoe UI', sans-serif"
TITLE_FONT = "'IBM Plex Sans', 'Geist', system-ui, sans-serif"

# delta pill colours (trend up = positive/green, down = negative/red, flat = neutral)
POS_FG, NEG_FG, NEU_FG = "#1B9D6B", "#D2483A", "#5B6472"


def _tint(hexc, ratio, bg=(255, 255, 255)):
    """Blend `hexc` toward white by `ratio` (0..1 = share of the accent)."""
    h = hexc.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    out = tuple(round(c * ratio + bw * (1 - ratio)) for c, bw in zip((r, g, b), bg))
    return "#%02X%02X%02X" % out


POS_BG = _tint("#22B276", 0.14)
NEG_BG = _tint("#E8655A", 0.15)
NEU_BG = "#EFF1F5"

# ---- Callout variants: default accent + icon + label ----------------------------------
VARIANTS = {
    "takeaway": {"accent": "#2E90FA", "icon": "key", "label": "Key takeaway"},
    "tip":      {"accent": "#22B276", "icon": "lightbulb", "label": "Tip"},
    "success":  {"accent": "#22B276", "icon": "check-circle", "label": "Why it works"},
    "warning":  {"accent": "#F5A623", "icon": "alert-triangle", "label": "Warning"},
    "info":     {"accent": "#0891B2", "icon": "info", "label": "Good to know"},
    "note":     {"accent": "#534AB7", "icon": "pin", "label": "Note"},
}

# ---- Inline icon set (Lucide-style, 24x24, stroke=currentColor) ------------------------
ICONS = {
    "coins": '<circle cx="8" cy="8" r="6"/><path d="M18.09 10.37A6 6 0 1 1 10.34 18"/><path d="M7 6h1v4"/><path d="m16.71 13.88.7.71-2.82 2.82"/>',
    "zap": '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "trending-up": '<path d="M16 7h6v6"/><path d="m22 7-8.5 8.5-5-5L2 17"/>',
    "trending-down": '<path d="M16 17h6v-6"/><path d="m22 17-8.5-8.5-5 5L2 7"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "star": '<path d="M11.5 2.3a.5.5 0 0 1 1 0l2.3 4.7 5.2.8a.5.5 0 0 1 .3.8l-3.7 3.7.9 5.1a.5.5 0 0 1-.8.6L12 16.3l-4.6 2.4a.5.5 0 0 1-.8-.6l.9-5.1L3.8 9.4a.5.5 0 0 1 .3-.8l5.2-.8z"/>',
    "message-circle": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "rocket": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
    "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5A4.8 8 0 0 1 12 8a4.8 8 0 0 1 4.5-5 2.5 2.5 0 0 1 0 5"/>',
    "percent": '<line x1="19" x2="5" y1="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.07-2.14-.22-4.05 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.15.43-2.29 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
    "sparkles": '<path d="M9.94 14.5A2 2 0 0 0 8.5 13.06l-4.14-1.07a.5.5 0 0 1 0-.98L8.5 9.94A2 2 0 0 0 9.94 8.5l1.07-4.14a.5.5 0 0 1 .98 0L13.06 8.5A2 2 0 0 0 14.5 9.94l4.14 1.07a.5.5 0 0 1 0 .98L14.5 13.06a2 2 0 0 0-1.44 1.44l-1.07 4.14a.5.5 0 0 1-.98 0z"/><path d="M20 3v4"/><path d="M22 5h-4"/><path d="M4 17v2"/><path d="M5 18H3"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "key": '<path d="m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4"/><path d="m21 2-9.6 9.6"/><circle cx="7.5" cy="15.5" r="5.5"/>',
    "lightbulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    "alert-triangle": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "check-circle": '<path d="M21.8 10A10 10 0 1 1 17 3.3"/><path d="m9 11 3 3L22 4"/>',
    "pin": '<path d="M12 17v5"/><path d="M9 10.8a2 2 0 0 1-1.1 1.8l-1.8.9A2 2 0 0 0 5 15.2V16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-.8a2 2 0 0 0-1.1-1.8l-1.8-.9A2 2 0 0 1 15 10.8V7a1 1 0 0 1 1-1 2 2 0 0 0 0-4H8a2 2 0 0 0 0 4 1 1 0 0 1 1 1z"/>',
    "bar-chart": '<line x1="12" x2="12" y1="20" y2="10"/><line x1="18" x2="18" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="16"/>',
    "calendar": '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "arrow-up": '<path d="M12 19V5"/><path d="m6 11 6-6 6 6"/>',
    "arrow-down": '<path d="M12 5v14"/><path d="m6 13 6 6 6-6"/>',
    "minus": '<path d="M5 12h14"/>',
}


def esc(s):
    return _html.escape("" if s is None else str(s))


def icon(name, cls="", fill=False):
    p = ICONS.get(name or "")
    if not p:
        return ""
    if fill:
        return ('<svg class="%s" viewBox="0 0 24 24" fill="currentColor" stroke="none" aria-hidden="true">%s</svg>'
                % (cls, p))
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (cls, p))


def logo_html(logo_path):
    try:
        uri = "data:image/png;base64," + base64.b64encode(Path(logo_path).read_bytes()).decode()
        return '<img src="%s" alt="Pleasur.ai">' % uri
    except Exception:
        return '<span class="logo-fallback">Pleasur.AI</span>'


def footer(logo, note="", hairline=True):
    cls = "footer" if hairline else "footer flush"
    note_html = ('<span class="fnote">%s</span>' % esc(note)) if note else "<span></span>"
    return '<div class="%s">%s%s</div>' % (cls, note_html, logo)


# ---- Builders --------------------------------------------------------------------------
def card_style(accent, width):
    return ("--accent:%s;--t05:%s;--t12:%s;--t15:%s;width:%dpx"
            % (accent, _tint(accent, 0.05), _tint(accent, 0.12), _tint(accent, 0.15), width))


def build_stat(spec, logo):
    accent = spec.get("accent") or PALETTE[0]
    stats = spec.get("stats") or []
    n = max(1, len(stats))
    width = spec.get("width") or {1: 540, 2: 760, 3: 940}.get(n, 1000)
    vsize = {1: 76, 2: 54, 3: 44}.get(n, 38)

    eyebrow = ('<div class="eyebrow">%s</div>' % esc(spec["eyebrow"])) if spec.get("eyebrow") else ""

    blocks = []
    for s in stats:
        ic = ('<div class="stat-ic">%s</div>' % icon(s.get("icon"), cls="ic")) if s.get("icon") else ""
        unit = ('<span class="stat-unit">%s</span>' % esc(s["unit"])) if s.get("unit") else ""
        vcolor = (";color:%s" % esc(s["valueColor"])) if s.get("valueColor") else ""
        val = ('<div class="stat-val" style="font-size:%dpx%s">%s%s</div>'
               % (vsize, vcolor, esc(s.get("value", "")), unit))
        label = ('<div class="stat-label">%s</div>' % esc(s["label"])) if s.get("label") else ""

        meta = []
        if s.get("delta"):
            trend = (s.get("trend") or "up").lower()
            tone = (s.get("tone") or {"up": "pos", "down": "neg", "flat": "neu"}.get(trend, "pos")).lower()
            tone = {"positive": "pos", "negative": "neg", "neutral": "neu"}.get(tone, tone)
            arrow = {"up": "arrow-up", "down": "arrow-down", "flat": "minus"}.get(trend, "arrow-up")
            meta.append('<span class="delta %s">%s%s</span>' % (tone, icon(arrow, cls="da"), esc(s["delta"])))
        if s.get("sub"):
            meta.append('<span class="stat-sub">%s</span>' % esc(s["sub"]))
        meta_html = ('<div class="stat-meta">%s</div>' % "".join(meta)) if meta else ""

        blocks.append('<div class="stat-block">%s%s%s%s</div>' % (ic, val, label, meta_html))

    row = ('<div class="vr"></div>'.join(blocks))
    inner = '%s<div class="stat-row">%s</div>%s' % (eyebrow, row, footer(logo, spec.get("footnote", "")))
    return "stat", card_style(accent, width), inner


def _stars(rating):
    try:
        n = max(0, min(5, int(rating)))
    except (TypeError, ValueError):
        n = 5
    cells = "".join('<span class="star %s">%s</span>' % ("on" if i < n else "off",
                    icon("star", cls="st", fill=True)) for i in range(5))
    return '<div class="stars">%s</div>' % cells


def build_quote(spec, logo):
    """Four pull-quote styles (`style`): mark (big quote glyph), bar (editorial left
    accent rule), review (star rating + source chip), highlight (key phrase marked)."""
    accent = spec.get("accent") or PALETTE[0]
    width = spec.get("width") or 760
    style = (spec.get("style") or "bar").lower()
    q = spec.get("quote", "")
    qlen = len(q)
    if style == "review":
        qsize = 25 if qlen <= 120 else (22 if qlen <= 210 else 20)
    else:
        qsize = 31 if qlen <= 110 else (27 if qlen <= 200 else 23)

    # quote text, with one optional highlighted phrase (escape first, then wrap)
    body = esc(q)
    if spec.get("highlight"):
        h = esc(spec["highlight"])
        body = body.replace(h, "<mark>%s</mark>" % h, 1)
    qtext = '<blockquote class="quote-text" style="font-size:%dpx">%s</blockquote>' % (qsize, body)

    # attribution row (name / role / initials avatar / optional source chip)
    a = spec.get("attribution") or {}
    attrib = ""
    if a.get("name") or a.get("role"):
        av = ""
        if a.get("avatar"):
            av = ('<div class="avatar" style="background:%s">%s</div>'
                  % (esc(a.get("avatarColor") or accent), esc(a["avatar"])))
        name = ('<div class="aname">%s</div>' % esc(a["name"])) if a.get("name") else ""
        role = ('<div class="arole">%s</div>' % esc(a["role"])) if a.get("role") else ""
        src = ('<div class="qsource">%s</div>' % esc(a["source"])) if a.get("source") else ""
        attrib = '<div class="attrib">%s<div class="atext">%s%s</div>%s</div>' % (av, name, role, src)

    if style == "bar":
        inner = '<div class="qbar">%s</div>%s%s' % (qtext, attrib, footer(logo))
    elif style == "review":
        inner = "%s%s%s%s" % (_stars(spec.get("rating", 5)), qtext, attrib, footer(logo))
    elif style == "highlight":
        inner = '<div class="qmark sm">&ldquo;</div>%s%s%s' % (qtext, attrib, footer(logo))
    else:  # mark (default) — oversized typographic open-quote glyph
        inner = '<div class="qmark">&ldquo;</div>%s%s%s' % (qtext, attrib, footer(logo))

    return "quote q-%s" % style, card_style(accent, width), inner


def build_callout(spec, logo):
    variant = (spec.get("variant") or "takeaway").lower()
    base = VARIANTS.get(variant, VARIANTS["takeaway"])
    accent = spec.get("accent") or base["accent"]
    ic = spec.get("icon") or base["icon"]
    label = spec.get("label", base["label"])
    width = spec.get("width") or 780

    label_html = ('<div class="clabel">%s</div>' % esc(label)) if label else ""
    heading = ('<div class="cheading">%s</div>' % esc(spec["heading"])) if spec.get("heading") else ""
    text = '<div class="ctext">%s</div>' % esc(spec.get("text", ""))
    body = ('<div class="cbody"><div class="cicon">%s</div>'
            '<div class="ccontent">%s%s%s</div></div>' % (icon(ic, cls="ic"), label_html, heading, text))
    inner = ('<div class="rail"></div><div class="cmain">%s%s</div>'
             % (body, footer(logo, spec.get("footnote", ""), hairline=False)))
    return "callout", card_style(accent, width), inner


BUILDERS = {"stat": build_stat, "quote": build_quote, "callout": build_callout}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:__BODY__;background:__PAGE__;-webkit-font-smoothing:antialiased}
#wrap{display:inline-block;padding:46px;background:__PAGE__}
#card{background:#fff;border:1px solid __CARD_BORDER__;border-radius:20px;
  box-shadow:0 14px 46px rgba(20,30,50,0.08);padding:38px 40px 22px;position:relative}
.footer{display:flex;align-items:center;justify-content:space-between;gap:16px;
  margin-top:28px;padding-top:16px;border-top:1px solid __HAIRLINE__}
.footer.flush{border-top:none;padding-top:10px;margin-top:22px}
.footer .fnote{font-size:12px;color:__FAINT__;line-height:1.4;max-width:72%}
.footer img{height:22px;opacity:.92;display:block;margin-left:auto}
.logo-fallback{font-weight:700;color:#B4BAC4;margin-left:auto}

/* STAT */
.eyebrow{font-size:12.5px;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;
  color:var(--accent);margin-bottom:24px}
.stat-row{display:flex;align-items:stretch;gap:34px}
.stat-block{flex:1;display:flex;flex-direction:column;min-width:0}
.stat-ic{width:42px;height:42px;border-radius:11px;display:flex;align-items:center;justify-content:center;
  background:var(--t12);color:var(--accent);margin-bottom:18px}
.stat-ic .ic{width:22px;height:22px}
.stat-val{font-family:__TITLE__;font-weight:700;color:__INK__;line-height:1;letter-spacing:-1.6px;
  font-variant-numeric:tabular-nums;font-feature-settings:'tnum' 1}
.stat-unit{font-size:.34em;font-weight:600;color:__MUTED__;letter-spacing:-.2px;margin-left:8px}
.stat-label{font-size:15px;font-weight:600;color:__INK_SOFT__;margin-top:15px;line-height:1.4}
.stat-meta{display:flex;align-items:center;gap:11px;margin-top:13px;flex-wrap:wrap}
.delta{display:inline-flex;align-items:center;gap:2px;font-size:12.5px;font-weight:700;
  padding:3px 10px 3px 7px;border-radius:999px}
.delta .da{width:13px;height:13px;stroke-width:2.7}
.delta.pos{color:__POS_FG__;background:__POS_BG__}
.delta.neg{color:__NEG_FG__;background:__NEG_BG__}
.delta.neu{color:__NEU_FG__;background:__NEU_BG__}
.stat-sub{font-size:13px;color:__FAINT__}
.vr{width:1px;background:__DIVIDER__;align-self:stretch;margin:4px 0;flex:none}

/* QUOTE */
#card.quote{padding:34px 42px 24px}
.qmark{font-family:__TITLE__,Georgia,serif;font-weight:700;font-size:96px;line-height:.78;
  color:var(--accent);height:46px;overflow:hidden}
.quote-text{font-family:__TITLE__;font-weight:500;color:__INK__;line-height:1.46;
  letter-spacing:-.3px;margin-top:18px}
.attrib{display:flex;align-items:center;gap:13px;margin-top:28px}
.avatar{width:46px;height:46px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  color:#fff;font-weight:700;font-size:15.5px;letter-spacing:.3px;flex:none}
.aname{font-size:15px;font-weight:700;color:__INK__}
.arole{font-size:13.5px;color:__MUTED__;margin-top:2px}
.qmark.sm{font-size:60px;height:28px}
mark{background:var(--t15);color:inherit;padding:.02em .14em;border-radius:5px;
  box-decoration-break:clone;-webkit-box-decoration-break:clone}
.qsource{margin-left:auto;align-self:center;font-size:12.5px;font-weight:600;
  color:var(--accent);background:var(--t12);padding:5px 12px;border-radius:999px}
/* bar: editorial left accent rule */
#card.q-bar{padding:36px 44px 24px}
.qbar{border-left:4px solid var(--accent);padding-left:26px}
.q-bar .quote-text{margin-top:0}
.q-bar .attrib{margin-top:26px}
/* review: star rating + source chip */
.stars{display:flex;gap:4px}
.stars .st{width:20px;height:20px}
.star.on{color:#F5A623}
.star.off{color:#E4E7EC}
.q-review .quote-text{margin-top:18px}

/* CALLOUT */
#card.callout{padding:0;overflow:hidden;display:flex}
.rail{width:6px;background:var(--accent);flex:none}
.cmain{flex:1;padding:30px 34px 18px;background:var(--t05)}
.cbody{display:flex;gap:18px;align-items:flex-start}
.cicon{width:46px;height:46px;border-radius:12px;flex:none;display:flex;align-items:center;justify-content:center;
  background:var(--t15);color:var(--accent)}
.cicon .ic{width:24px;height:24px}
.ccontent{flex:1;min-width:0;padding-top:1px}
.clabel{font-size:12.5px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;
  color:var(--accent);margin-bottom:8px}
.cheading{font-family:__TITLE__;font-size:18px;font-weight:700;color:__INK__;margin-bottom:7px;line-height:1.32}
.ctext{font-size:16px;color:__BODY__;line-height:1.58}
.callout .footer{margin-top:14px;padding-top:4px}
.callout .footer img{opacity:.9}
"""


def build_css():
    repl = {
        "__BODY__": BODY_FONT, "__TITLE__": TITLE_FONT, "__PAGE__": PAGE,
        "__CARD_BORDER__": CARD_BORDER, "__HAIRLINE__": HAIRLINE, "__DIVIDER__": DIVIDER,
        "__INK__": INK, "__INK_SOFT__": INK_SOFT, "__MUTED__": MUTED, "__FAINT__": FAINT,
        "__POS_FG__": POS_FG, "__NEG_FG__": NEG_FG, "__NEU_FG__": NEU_FG,
        "__POS_BG__": POS_BG, "__NEG_BG__": NEG_BG, "__NEU_BG__": NEU_BG,
    }
    css = CSS
    # BODY (font) vs BODY (copy colour) clash — do the copy colour token first with a unique key
    css = css.replace(".ctext{font-size:16px;color:__BODY__;", ".ctext{font-size:16px;color:%s;" % BODY)
    for k, v in repl.items():
        css = css.replace(k, v)
    return css


def render(spec, out, logo_path, scale=2):
    kind = (spec.get("kind") or "stat").lower()
    builder = BUILDERS.get(kind)
    if builder is None:
        print(json.dumps({"status": "failed", "reason": "unknown_kind", "kind": kind}))
        return 1

    required = {"stat": "stats", "quote": "quote", "callout": "text"}[kind]
    if not spec.get(required):
        print(json.dumps({"status": "failed", "reason": "missing_field", "kind": kind, "field": required}))
        return 1

    classes, style, inner = builder(spec, logo_html(logo_path))
    width = int(style.split("width:")[1].rstrip("px"))

    page = ("""<!doctype html><html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=IBM+Plex+Sans:wght@500;600;700&display=swap');
%s
</style></head><body>
<div id="wrap"><div id="card" class="%s" style="%s">%s</div></div>
</body></html>""" % (build_css(), classes, style, inner))

    try:
        from patchright.sync_api import sync_playwright
    except ImportError:
        from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--no-sandbox"])
        pg = b.new_context(viewport={"width": width + 220, "height": 1100},
                           device_scale_factor=scale).new_page()
        pg.set_content(page, wait_until="networkidle")
        pg.wait_for_timeout(500)
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        pg.locator("#wrap").screenshot(path=out)
        b.close()
    print(json.dumps({"status": "captured", "path": out, "kind": kind, "width": width}))
    return 0


def main():
    ap = argparse.ArgumentParser(description="Render brand stat/quote/callout cards.")
    ap.add_argument("--spec", help="path to a card spec JSON")
    ap.add_argument("--json", help="inline card spec JSON")
    ap.add_argument("--out", required=True)
    ap.add_argument("--logo", default=str(Path(__file__).resolve().parent / "pleasurai-logo.png"))
    ap.add_argument("--scale", type=int, default=2)
    a = ap.parse_args()

    if a.json:
        spec = json.loads(a.json)
    elif a.spec:
        spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    else:
        print(json.dumps({"status": "failed", "reason": "no_spec (need --spec or --json)"}))
        return 1
    return render(spec, a.out, a.logo, a.scale)


if __name__ == "__main__":
    sys.exit(main())
