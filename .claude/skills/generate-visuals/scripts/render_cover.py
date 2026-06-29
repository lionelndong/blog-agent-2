#!/usr/bin/env python3
"""Render premium, ON-BRAND article cover / hero images headless in the browser.

v3 (2026-06-28) — "editorial line-motif" redesign, inspired by Linear (one templated dark canvas
+ a unique minimal line-art motif per post), Ahrefs (typographic editorial: small-caps category +
big brand title + byline) and Sam Marsh (bold confident colour-fields). The hero graphic is no
longer a generic app-tile icon — it's a bespoke, elegant LINE-ART concept motif drawn from a single
parametric renderer, so every cover is unmistakably one family yet visually distinct ("a little bit
the same, not the same"). DETERMINISTIC (route A, preferred): no AI, pixel-exact text, reproducible.

Brand system (matches render_chart_web.py): palette #2E90FA/#8B5CF6/#22B276/#F5A623/#E8655A;
title = Plus Jakarta Sans 800 (the live blog hero H1 font, blog-display.ts); eyebrow = IBM Plex Sans;
body = Geist; the REAL Pleasur.ai logo composited per-bg, never AI. Output 16:9 1600×900 (the blog's
featured-image aspect), OG-safe centred safe-zone.

Usage:
  python render_cover.py --content cover.json --out cover.png
  python render_cover.py --title "Best AI Girlfriend Apps" --eyebrow "COMPARISON" \
                         --theme dark --accent blue --motif cluster --out cover.png

content.json: {
  "title","eyebrow"?,"subtitle"?,"author"?,
  "theme": "dark|light|bold|aurora",          # design family (default dark = Linear-like)
  "accent": "blue|purple|mint|coral|amber" | "#RRGGBB",
  "motif": "cluster|orbit|thread|wave|radial|grid",   # line-art layout; auto-picked from title if omitted
  "bg_image": "path"                          # route B: composite over an AI illustration
}
"""
import argparse
import base64
import json
import math
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

# ── Brand palette (matches render_chart_web.py) ─────────────────────────────
PALETTE = {
    "blue":   {"base": "#2E90FA", "deep": "#1A56B0", "light": "#86C2FF", "sec": "#8B5CF6"},
    "purple": {"base": "#8B5CF6", "deep": "#5B30BE", "light": "#C7AEFF", "sec": "#2E90FA"},
    "mint":   {"base": "#22B276", "deep": "#0E7A4E", "light": "#79E2B4", "sec": "#2E90FA"},
    "coral":  {"base": "#E8655A", "deep": "#B23A33", "light": "#FFACA2", "sec": "#8B5CF6"},
    "amber":  {"base": "#F5A623", "deep": "#B6750A", "light": "#FFD489", "sec": "#E8655A"},
}
INK = "#121723"

# ── Slim icon set for the motif hub (Lucide stroke paths, MIT) ───────────────
ICONS = {
    "heart":    '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "chat":     '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "sparkles": '<path d="M9.94 14.06A2 2 0 0 0 8.5 12.6l-5.4-1.4a.5.5 0 0 1 0-1l5.4-1.4A2 2 0 0 0 9.94 7.4l1.4-5.4a.5.5 0 0 1 1 0l1.4 5.4a2 2 0 0 0 1.44 1.44l5.4 1.4a.5.5 0 0 1 0 1l-5.4 1.4a2 2 0 0 0-1.44 1.44l-1.4 5.4a.5.5 0 0 1-1 0Z"/>',
    "phone":    '<path d="M13.83 19.55a16 16 0 0 1-9.38-9.38l1.92-1.6a2 2 0 0 0 .55-2.18l-.9-2.45A2 2 0 0 0 4.63 2.6L3 3a2 2 0 0 0-1.4 2.3 19 19 0 0 0 17.1 17.1A2 2 0 0 0 21 21l.4-1.63a2 2 0 0 0-1.34-2.4l-2.45-.9a2 2 0 0 0-2.18.55Z"/>',
    "shield":   '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1Z"/>',
    "image":    '<rect width="18" height="18" x="3" y="3" rx="3"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.09-3.09a2 2 0 0 0-2.82 0L6 21"/>',
}
# title keyword → (motif layout, hub icon)
KEYWORD_MAP = [
    (r"remember|memory|forget|recall|mind|learn", ("cluster", "sparkles")),
    (r"girlfriend|boyfriend|companion|partner|relationship|dating|love", ("orbit", "heart")),
    (r"sext|dirty|talk|chat|message|conversation|flirt|reply", ("thread", "chat")),
    (r"call|voice|phone|audio|speak", ("wave", "phone")),
    (r"safe|privacy|secure|protect|risk|scam|trust", ("orbit", "shield")),
    (r"image|photo|picture|generate|art|nsfw|nude|selfie", ("radial", "image")),
    (r"best|top|review|compare|vs|alternativ|app", ("grid", "sparkles")),
]


def pick_motif(title):
    t = (title or "").lower()
    for pat, val in KEYWORD_MAP:
        if re.search(pat, t):
            return val
    return ("cluster", "heart")


def resolve_accent(accent):
    if not accent:
        return PALETTE["blue"]
    if accent in PALETTE:
        return PALETTE[accent]
    if re.fullmatch(r"#?[0-9a-fA-F]{6}", accent or ""):
        hx = accent if accent.startswith("#") else "#" + accent
        return {"base": hx, "deep": _shade(hx, -0.42), "light": _shade(hx, 0.45), "sec": PALETTE["purple"]["base"]}
    return PALETTE["blue"]


def _shade(hx, f):
    r, g, b = int(hx[1:3], 16), int(hx[3:5], 16), int(hx[5:7], 16)
    if f >= 0:
        r, g, b = r + (255 - r) * f, g + (255 - g) * f, b + (255 - b) * f
    else:
        r, g, b = r * (1 + f), g * (1 + f), b * (1 + f)
    return "#%02X%02X%02X" % (int(r), int(g), int(b))


def _rgba(hx, a):
    return "rgba(%d,%d,%d,%.2f)" % (int(hx[1:3], 16), int(hx[3:5], 16), int(hx[5:7], 16), a)


def _img_uri(path):
    p = Path(path)
    ext = (p.suffix.lower().lstrip(".") or "png")
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    return "data:image/%s;base64," % mime + base64.b64encode(p.read_bytes()).decode()


def title_size(title):
    n = len(title)
    for lim, sz in ((16, 112), (24, 98), (34, 84), (46, 72), (60, 60)):
        if n <= lim:
            return sz
    return 52


# ── Line-art motif: one parametric renderer, several layouts (the "same family") ─────
# A node network drawn as elegant thin strokes + dot nodes + a glowing hub carrying a small
# icon. Shared styling across all layouts → unmistakably one system; geometry varies by layout.
VB = 640  # square viewBox


def _layout(kind):
    """Return (nodes, edges, decor) for a layout. node=(x,y,role): hub|big|dot|ring. decor=svg str."""
    c = VB / 2
    if kind == "orbit":
        nodes = [(c, c, "hub")]
        edges = []
        rings = [(150, 5, 0.0), (235, 7, 0.6)]
        decor = ""
        for ri, (r, count, rot) in enumerate(rings):
            decor += '<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke-width="1.5" class="ring"/>' % (c, c, r, int(r * 0.84))
            for k in range(count):
                a = rot + k * (2 * math.pi / count)
                x, y = c + r * math.cos(a), c + r * 0.84 * math.sin(a)
                role = "big" if (ri == 0 and k % 2 == 0) else "dot"
                nodes.append((x, y, role))
                if ri == 0:
                    edges.append((0, len(nodes) - 1))
        return nodes, edges, decor
    if kind == "thread":
        a = (160, 430); b = (480, 210)
        mids = [(255, 360), (320, 300), (398, 252)]
        nodes = [(a[0], a[1], "hub"), (b[0], b[1], "big")] + [(m[0], m[1], "dot") for m in mids]
        edges = [(0, 2), (2, 3), (3, 4), (4, 1)]
        path = "M%d %d C %d %d, %d %d, %d %d" % (a[0], a[1], 300, 410, 330, 250, b[0], b[1])
        decor = '<path d="%s" class="thread"/>' % path
        decor += '<path d="M%d %d C %d %d, %d %d, %d %d" class="thread faint"/>' % (a[0], a[1] - 26, 300, 384, 330, 224, b[0], b[1] - 26)
        return nodes, edges, decor
    if kind == "wave":
        nodes, edges, decor = [], [], ""
        for i, (yy, op) in enumerate([(250, 1.0), (320, 0.62), (388, 0.34)]):
            d = "M70 %d" % yy
            for x in range(70, 580, 14):
                d += " L%d %d" % (x, yy + math.sin((x - 70) / 46.0 + i) * (26 - i * 5))
            decor += '<path d="%s" class="wave" style="opacity:%.2f"/>' % (d, op)
        for (x, y) in [(190, 250 - 0), (330, 250 + 8), (470, 250 - 14)]:
            yy = 250 + math.sin((x - 70) / 46.0) * 26
            nodes.append((x, yy, "big" if x == 330 else "dot"))
        nodes.append((330, 320, "hub"))
        return nodes, edges, decor
    if kind == "radial":
        nodes = [(c, c, "hub")]; edges = []; decor = ""
        for r in (120, 185, 250):
            decor += '<circle cx="%d" cy="%d" r="%d" fill="none" stroke-width="1.5" class="ring"/>' % (c, c, r)
        for k in range(8):
            a = k * math.pi / 4 + 0.2
            r = 185 if k % 2 == 0 else 250
            x, y = c + r * math.cos(a), c + r * math.sin(a)
            nodes.append((x, y, "big" if k % 2 == 0 else "dot"))
            edges.append((0, len(nodes) - 1))
        return nodes, edges, decor
    if kind == "grid":
        nodes, edges, decor = [], [], ""
        pts = [(200, 200), (320, 180), (440, 210), (190, 320), (320, 300), (450, 330),
               (210, 440), (330, 430), (440, 450)]
        for i, (x, y) in enumerate(pts):
            nodes.append((x, y, "hub" if i == 4 else ("big" if i % 2 == 0 else "dot")))
        edges = [(4, 1), (4, 3), (4, 5), (4, 7), (1, 0), (1, 2), (3, 6), (5, 8), (0, 3), (2, 5), (6, 7), (7, 8)]
        return nodes, edges, decor
    # cluster (default) — organic constellation
    pts = [(320, 300, "hub"), (175, 195, "big"), (480, 200, "big"), (150, 350, "dot"),
           (505, 330, "big"), (300, 150, "dot"), (235, 430, "big"), (430, 445, "dot"),
           (360, 250, "dot"), (255, 305, "ring")]
    edges = [(0, 1), (0, 2), (0, 4), (0, 5), (0, 8), (0, 9), (1, 5), (2, 4), (3, 6), (4, 7), (6, 7), (1, 3), (2, 8)]
    return pts, edges, ""


def build_motif(theme, ac, kind, icon):
    nodes, edges, decor = _layout(kind)
    dark = theme in ("dark", "bold", "aurora")
    if theme == "bold":
        stroke, faint, node_fill, ring_s, hub_fill, ico = "#FFFFFF", "rgba(255,255,255,.30)", "#FFFFFF", "rgba(255,255,255,.55)", "#FFFFFF", ac["deep"]
        glow = "rgba(255,255,255,.55)"
    elif dark:
        stroke, faint, node_fill, ring_s, hub_fill, ico = ac["light"], _rgba(ac["light"], 0.22), ac["light"], _rgba(ac["light"], 0.5), "url(#hubg)", "#FFFFFF"
        glow = _rgba(ac["base"], 0.85)
    else:
        stroke, faint, node_fill, ring_s, hub_fill, ico = ac["base"], _rgba(INK, 0.10), ac["base"], _rgba(ac["base"], 0.5), "url(#hubg)", "#FFFFFF"
        glow = _rgba(ac["base"], 0.5)

    svg = ['<svg viewBox="0 0 %d %d" class="lineart" xmlns="http://www.w3.org/2000/svg">' % (VB, VB)]
    svg.append(
        '<defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
        '<radialGradient id="hubg"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>'
        '<filter id="gl" x="-60%%" y="-60%%" width="220%%" height="220%%"><feGaussianBlur stdDeviation="7"/></filter>'
        '</defs>' % (ac["light"], ac["base"], ac["light"], ac["base"]))
    # soft hub glow disc (tight + subtle on light, fuller on dark)
    hub = nodes[0]
    gr, go = (52, 0.28) if theme == "light" else (90, 0.5)
    svg.append('<circle cx="%.0f" cy="%.0f" r="%d" fill="%s" filter="url(#gl)" opacity="%.2f"/>' % (hub[0], hub[1], gr, glow, go))
    svg.append(decor.replace('class="ring"', 'class="ring" stroke="%s"' % faint)
                    .replace('class="thread faint"', 'stroke="%s" fill="none" stroke-width="1.5" opacity=".4"' % faint)
                    .replace('class="thread"', 'stroke="url(#lg)" fill="none" stroke-width="2.4"')
                    .replace('class="wave"', 'stroke="url(#lg)" fill="none" stroke-width="2.4" stroke-linecap="round"'))
    # edges
    for i, j in edges:
        x1, y1 = nodes[i][0], nodes[i][1]
        x2, y2 = nodes[j][0], nodes[j][1]
        op = 0.9 if (i == 0 or j == 0) else 0.4
        col = "url(#lg)" if (i == 0 or j == 0) else faint
        svg.append('<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke="%s" stroke-width="%s" opacity="%.2f"/>'
                   % (x1, y1, x2, y2, col, "2.2" if (i == 0 or j == 0) else "1.6", op))
    # nodes
    for idx, (x, y, role) in enumerate(nodes):
        if role == "hub":
            continue
        if role == "big":
            svg.append('<circle cx="%.0f" cy="%.0f" r="9" fill="%s"/>' % (x, y, node_fill))
            svg.append('<circle cx="%.0f" cy="%.0f" r="16" fill="none" stroke="%s" stroke-width="1.4" opacity=".5"/>' % (x, y, node_fill))
        elif role == "ring":
            svg.append('<circle cx="%.0f" cy="%.0f" r="10" fill="none" stroke="%s" stroke-width="2"/>' % (x, y, ring_s))
        else:
            svg.append('<circle cx="%.0f" cy="%.0f" r="5.5" fill="%s"/>' % (x, y, node_fill))
    # hub: ring + filled core + icon
    svg.append('<circle cx="%.0f" cy="%.0f" r="46" fill="none" stroke="%s" stroke-width="1.6" opacity=".55"/>' % (hub[0], hub[1], node_fill))
    svg.append('<circle cx="%.0f" cy="%.0f" r="33" fill="%s"/>' % (hub[0], hub[1], hub_fill))
    inner = ICONS.get(icon, ICONS["heart"])
    svg.append('<g transform="translate(%.0f %.0f) scale(1.5)" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
               '<g transform="translate(-12 -12)">%s</g></g>' % (hub[0], hub[1], ico, inner))
    svg.append('</svg>')
    return "".join(svg)


# ── Logo (real wordmark, themed by background, never AI) ─────────────────────
def logo_data_uri(dark_bg):
    src = SCRIPT_DIR / "pleasurai-logo.png"
    try:
        import warnings
        from PIL import Image
        img = Image.open(src).convert("RGBA")
        if dark_bg:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                pixels = list(img.getdata())
            out = []
            for (r, g, b, a) in pixels:
                if a > 30 and not (b > r + 25 and b > 110) and (0.299 * r + 0.587 * g + 0.114 * b) < 150:
                    out.append((245, 247, 250, a))
                else:
                    out.append((r, g, b, a))
            img.putdata(out)
        import io
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        try:
            return "data:image/png;base64," + base64.b64encode(src.read_bytes()).decode()
        except Exception:
            return ""


# ── Theme backgrounds ────────────────────────────────────────────────────────
def theme_bg(theme, ac):
    if theme == "bold":
        return ("background:"
                "radial-gradient(130%% 130%% at 80%% 12%%, %s 0%%, %s 55%%, %s 120%%);" % (ac["light"], ac["base"], ac["deep"]))
    if theme == "aurora":
        return ("background:"
                "radial-gradient(80%% 90%% at 16%% 8%%, %s 0%%, transparent 50%%),"
                "radial-gradient(70%% 80%% at 92%% 96%%, %s 0%%, transparent 52%%),"
                "#0B0F1A;" % (_rgba(ac["base"], 0.34), _rgba(ac["sec"], 0.30)))
    if theme == "light":
        return "background:#F6F8FB;"
    # dark (Linear-like, default)
    return ("background:"
            "radial-gradient(60%% 80%% at 82%% 30%%, %s 0%%, transparent 60%%),"
            "#0C1019;" % _rgba(ac["base"], 0.16))


PAGE = """<!doctype html><html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=IBM+Plex+Sans:wght@600;700&family=Geist:wght@400;500;600&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1600px;height:900px}
#stage{position:relative;width:1600px;height:900px;overflow:hidden;@@BG@@
  font-family:'Geist',system-ui,-apple-system,'Segoe UI',sans-serif}
.grain{position:absolute;inset:0;opacity:@@GRAINOP@@;mix-blend-mode:@@GRAINBLEND@@;pointer-events:none}
.dotgrid{position:absolute;inset:0;pointer-events:none;@@DOTGRID@@}
.vign{position:absolute;inset:0;pointer-events:none;@@VIGN@@}
.scrim{position:absolute;inset:0;pointer-events:none}
.tick{position:absolute;top:60px;right:72px;width:46px;height:46px;pointer-events:none;@@TICK@@}
.tick::before,.tick::after{content:"";position:absolute;background:@@TICKCOLOR@@}
.tick::before{top:0;right:0;width:46px;height:2px}
.tick::after{top:0;right:0;width:2px;height:46px}
#content{position:absolute;inset:0;display:flex;align-items:center;padding:0 96px}
.left{width:60%;z-index:5}
.eyebrow{display:inline-flex;align-items:center;gap:13px;font-family:'IBM Plex Sans',sans-serif;
  font-weight:700;font-size:17px;letter-spacing:3.6px;text-transform:uppercase;@@EYEBROW_CSS@@;margin-bottom:30px}
.eyebrow .sq{width:15px;height:15px;border-radius:4px;background:@@ACCENT@@;box-shadow:0 0 18px 1px @@ACCENTGLOW@@}
h1{font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:@@TSIZE@@px;line-height:1.035;
  letter-spacing:-2.4px;color:@@TITLECOLOR@@;max-width:15ch}
.sub{font-family:'Geist',sans-serif;font-weight:450;font-size:25px;line-height:1.5;color:@@SUBCOLOR@@;
  margin-top:28px;max-width:30ch}
.right{position:absolute;right:42px;top:50%;transform:translateY(-50%);width:46%;
  display:flex;align-items:center;justify-content:center;z-index:4}
.lineart{width:600px;height:600px;overflow:visible}
.baseline{position:absolute;left:96px;right:96px;bottom:108px;height:1px;background:@@BASELINE@@;z-index:3}
.footer{position:absolute;left:96px;bottom:54px;display:flex;align-items:center;gap:18px;z-index:6}
.footer img{height:30px;display:block}
.byline{font-family:'Geist',sans-serif;font-size:16px;font-weight:500;color:@@METACOLOR@@;
  padding-left:18px;border-left:1.5px solid @@METARULE@@}
</style></head><body>
<div id="stage">
  <div class="dotgrid"></div>
  <div class="vign"></div>
  <div class="scrim" style="@@SCRIM@@"></div>
  <div class="tick"></div>
  <div id="content">
    <div class="left">@@EYEBROW@@<h1>@@TITLE@@</h1>@@SUB@@</div>
    <div class="right">@@MOTIF@@</div>
  </div>
  <div class="baseline"></div>
  <div class="footer"><img src="@@LOGO@@" alt="Pleasur.ai">@@BYLINE@@</div>
  <svg class="grain" width="1600" height="900"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>
</div></body></html>"""


def build_html(c):
    theme = (c.get("theme") or "light").lower()
    ac = resolve_accent(c.get("accent") or ("purple" if theme == "aurora" else "blue"))
    motif_kind, auto_icon = pick_motif(c.get("title", ""))
    motif_kind = (c.get("motif") or motif_kind).lower()
    icon = (c.get("icon") or auto_icon).lower()
    title = (c.get("title") or "Untitled").strip()
    eyebrow = (c.get("eyebrow") or "").strip()
    subtitle = (c.get("subtitle") or "").strip()
    author = (c.get("author") or "").strip()
    dark = theme in ("dark", "bold", "aurora")

    if dark:
        title_color, sub_color = "#FFFFFF", "rgba(255,255,255,.74)"
        eyebrow_css = "color:rgba(255,255,255,.92)"
        meta_color, meta_rule = "rgba(255,255,255,.66)", "rgba(255,255,255,.24)"
        accent_text = "#FFFFFF" if theme == "bold" else ac["light"]
        grain_op, grain_blend = "0.06", "soft-light"
        vign = "background:radial-gradient(120% 120% at 50% 36%, transparent 56%, rgba(5,8,16,.5) 100%)"
        dotgrid = ""
        baseline = "rgba(255,255,255,.12)"
        tick_color = "rgba(255,255,255,.42)" if theme != "bold" else "rgba(255,255,255,.6)"
    else:  # light
        title_color, sub_color = INK, "#5B6472"
        eyebrow_css = "color:%s" % ac["deep"]
        meta_color, meta_rule = "#6B7484", "rgba(18,23,35,.16)"
        accent_text = ac["base"]
        grain_op, grain_blend = "0.04", "multiply"
        vign = f"background:radial-gradient(150% 120% at 80% 16%, {_rgba(ac['light'], 0.5)} 0%, transparent 46%)"
        dotgrid = ("background-image:radial-gradient(rgba(18,23,35,.05) 1.3px, transparent 1.3px);"
                   "background-size:30px 30px;mask-image:linear-gradient(120deg, transparent 42%, black 100%)")
        baseline = "rgba(18,23,35,.10)"
        tick_color = _rgba(ac["base"], 0.55)

    bg_css = theme_bg(theme, ac)
    motif_html = build_motif(theme, ac, motif_kind, icon)
    scrim = ""
    bg_image = c.get("bg_image")
    if bg_image:
        bg_css = "background:#0A0E18 url('%s') center/cover no-repeat;" % _img_uri(bg_image)
        scrim = ("background:"
                 "linear-gradient(90deg, rgba(7,10,18,.88) 0%, rgba(7,10,18,.60) 36%, rgba(7,10,18,.10) 64%, rgba(7,10,18,.34) 100%),"
                 "linear-gradient(0deg, rgba(7,10,18,.58) 0%, transparent 30%)")
        motif_html = ""
        dotgrid = vign = ""
        title_color, sub_color = "#FFFFFF", "rgba(255,255,255,.82)"
        eyebrow_css = "color:rgba(255,255,255,.94)"
        meta_color, meta_rule = "rgba(255,255,255,.72)", "rgba(255,255,255,.32)"
        accent_text = ac["light"]
        baseline = "rgba(255,255,255,.14)"
        tick_color = "rgba(255,255,255,.4)"
        dark = True

    eyebrow_html = ('<div class="eyebrow"><span class="sq"></span>%s</div>' % _esc(eyebrow)) if eyebrow else ""
    sub_html = ('<p class="sub">%s</p>' % _esc(subtitle)) if subtitle else ""
    byline_html = ('<span class="byline">%s</span>' % _esc(author)) if author else ""

    html = PAGE
    for k, v in {
        "@@BG@@": bg_css, "@@GRAINOP@@": grain_op, "@@GRAINBLEND@@": grain_blend,
        "@@VIGN@@": vign, "@@DOTGRID@@": dotgrid, "@@SCRIM@@": scrim,
        "@@TICK@@": "" if bg_image else "", "@@TICKCOLOR@@": tick_color,
        "@@EYEBROW_CSS@@": eyebrow_css, "@@EYEBROW@@": eyebrow_html,
        "@@ACCENT@@": accent_text, "@@ACCENTGLOW@@": _rgba(ac["base"], 0.7),
        "@@TSIZE@@": str(title_size(title)), "@@TITLECOLOR@@": title_color,
        "@@SUBCOLOR@@": sub_color, "@@SUB@@": sub_html, "@@TITLE@@": _esc(title),
        "@@MOTIF@@": motif_html, "@@LOGO@@": logo_data_uri(dark), "@@BYLINE@@": byline_html,
        "@@METACOLOR@@": meta_color, "@@METARULE@@": meta_rule, "@@BASELINE@@": baseline,
    }.items():
        html = html.replace(k, v)
    return html


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(html, out, width, height, supersample):
    try:
        from patchright.sync_api import sync_playwright
    except ImportError:
        from playwright.sync_api import sync_playwright
    out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--no-sandbox", "--force-color-profile=srgb"])
        pg = b.new_context(viewport={"width": width, "height": height}, device_scale_factor=supersample).new_page()
        pg.set_content(html, wait_until="networkidle")
        pg.wait_for_timeout(700)
        big = out.with_suffix(".super.png")
        pg.locator("#stage").screenshot(path=str(big))
        b.close()
    try:
        from PIL import Image
        im = Image.open(big).convert("RGB")
        if im.size != (width, height):
            im = im.resize((width, height), Image.LANCZOS)
        im.save(out)
        big.unlink(missing_ok=True)
    except Exception:
        big.replace(out)


def main():
    ap = argparse.ArgumentParser(description="Render an on-brand article cover / hero image.")
    ap.add_argument("--content")
    ap.add_argument("--title")
    ap.add_argument("--eyebrow", default="")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--theme", default="light", choices=["dark", "light", "bold", "aurora"])
    ap.add_argument("--accent", default="")
    ap.add_argument("--motif", default="", choices=["", "cluster", "orbit", "thread", "wave", "radial", "grid"])
    ap.add_argument("--icon", default="")
    ap.add_argument("--author", default="")
    ap.add_argument("--bg-image", dest="bg_image", default="")
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--supersample", type=int, default=2)
    a = ap.parse_args()

    if a.content:
        c = json.loads(Path(a.content).read_text(encoding="utf-8"))
    else:
        if not a.title:
            print(json.dumps({"status": "failed", "reason": "need --content or --title"}))
            return 1
        c = {"title": a.title, "eyebrow": a.eyebrow, "subtitle": a.subtitle, "theme": a.theme,
             "accent": a.accent, "motif": a.motif, "icon": a.icon, "author": a.author,
             "bg_image": a.bg_image or None}

    render(build_html(c), Path(a.out), a.width, a.height, a.supersample)
    mk, _ = pick_motif(c.get("title", ""))
    print(json.dumps({"status": "captured", "path": a.out, "theme": c.get("theme", "dark"),
                      "motif": c.get("motif") or mk, "dims": "%dx%d" % (a.width, a.height)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
