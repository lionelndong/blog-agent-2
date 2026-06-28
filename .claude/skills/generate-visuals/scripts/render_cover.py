#!/usr/bin/env python3
"""Render premium, ON-BRAND article cover / hero images headless in the browser (2026-06-28 v1).

This is the DETERMINISTIC cover engine (route A — preferred for consistency). It builds a
designed HTML hero from a content JSON and screenshots it with patchright — no AI, pixel-exact
text, fully reproducible. Brand system matches render_chart_web.py:

  palette  #2E90FA blue / #8B5CF6 purple / #22B276 mint / #F5A623 amber / #E8655A coral
  title    Plus Jakarta Sans 800  (the live blog hero H1 font — src/config/fonts/blog-display.ts)
  eyebrow  IBM Plex Sans 700       (blog heading font)
  body     Geist                   (blog body font)
  logo     the REAL Pleasur.ai wordmark, composited deterministically — NEVER AI-drawn

Output is 16:9 — the blog's featured-image aspect (article hero = `aspect-video` object-cover,
cards = aspect-ratio 16/9, og:image/twitter:image reuse coverImage). Default 1600x900 (2x the
800px content column). A centred safe-zone keeps the title + logo inside a 1.91:1 OG-side crop.

Usage:
  python render_cover.py --content cover.json --out cover.png
  python render_cover.py --title "Best AI Girlfriend Apps" --eyebrow "COMPARISON" \
                         --theme light --accent blue --icon heart --out cover.png

content.json: {
  "title": "...", "eyebrow": "GUIDE", "subtitle": "...",        # subtitle optional
  "theme": "gradient|light|spotlight", "accent": "blue|purple|mint|coral|amber" | "#RRGGBB",
  "icon": "heart|chat|sparkles|phone|shield|image|users|star",  # auto-picked from title if omitted
  "author": "Theo Hart"                                          # optional byline
}
"""
import argparse
import base64
import json
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
INK = "#141A24"        # near-black title on light
MUTE = "#5B6472"       # muted body on light

# ── Icon vocabulary: Lucide stroke paths (MIT), 24x24 viewBox ───────────────
# Rendered as white stroke icons inside the motif anchor — clean, modern, on-brand.
ICONS = {
    "heart":    '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "chat":     '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "sparkles": '<path d="M9.94 14.06A2 2 0 0 0 8.5 12.6l-5.4-1.4a.5.5 0 0 1 0-1l5.4-1.4A2 2 0 0 0 9.94 7.4l1.4-5.4a.5.5 0 0 1 1 0l1.4 5.4a2 2 0 0 0 1.44 1.44l5.4 1.4a.5.5 0 0 1 0 1l-5.4 1.4a2 2 0 0 0-1.44 1.44l-1.4 5.4a.5.5 0 0 1-1 0Z"/><path d="M20 3v4"/><path d="M22 5h-4"/><path d="M4 17v2"/><path d="M5 18H3"/>',
    "phone":    '<path d="M13.83 19.55a16 16 0 0 1-9.38-9.38l1.92-1.6a2 2 0 0 0 .55-2.18l-.9-2.45A2 2 0 0 0 4.63 2.6L3 3a2 2 0 0 0-1.4 2.3 19 19 0 0 0 17.1 17.1A2 2 0 0 0 21 21l.4-1.63a2 2 0 0 0-1.34-2.4l-2.45-.9a2 2 0 0 0-2.18.55Z"/>',
    "shield":   '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1Z"/>',
    "image":    '<rect width="18" height="18" x="3" y="3" rx="3"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.09-3.09a2 2 0 0 0-2.82 0L6 21"/>',
    "users":    '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "star":     '<path d="M11.5 2.4 14 7.5l5.6.8-4 3.9 1 5.6-5-2.6-5 2.6 1-5.6-4-3.9 5.6-.8Z"/>',
    "robot":    '<rect width="16" height="12" x="4" y="8" rx="3"/><path d="M12 8V5"/><circle cx="12" cy="4" r="1.4"/><path d="M9 13h.01M15 13h.01M9.5 17h5"/><path d="M2 14v2M22 14v2"/>',
    "infinity": '<path d="M12 12c-2-3-4-4-6-4a4 4 0 0 0 0 8c2 0 4-1 6-4Zm0 0c2 3 4 4 6 4a4 4 0 0 0 0-8c-2 0-4 1-6 4Z"/>',
}
SATELLITES = {  # small accent icons that orbit the main tile (per main icon)
    "heart": ["chat", "sparkles"], "chat": ["heart", "sparkles"], "sparkles": ["heart", "star"],
    "phone": ["chat", "heart"], "shield": ["sparkles", "heart"], "image": ["sparkles", "heart"],
    "users": ["heart", "chat"], "star": ["heart", "sparkles"], "robot": ["heart", "sparkles"],
    "infinity": ["sparkles", "heart"],
}

KEYWORD_ICON = [
    (r"remember|memory|forget|recall|mind", "sparkles"),
    (r"girlfriend|boyfriend|companion|partner|dating|relationship|love|romance", "heart"),
    (r"sext|dirty|talk|chat|message|conversation|flirt", "chat"),
    (r"call|voice|phone|audio", "phone"),
    (r"safe|privacy|secure|protect|risk|scam", "shield"),
    (r"image|photo|picture|generate|art|nsfw|nude", "image"),
    (r"character|persona|avatar|create", "users"),
    (r"best|top|review|compare|vs|alternativ", "star"),
]


def pick_icon(title: str) -> str:
    t = title.lower()
    for pat, name in KEYWORD_ICON:
        if re.search(pat, t):
            return name
    return "heart"


def resolve_accent(accent: str) -> dict:
    if not accent:
        return PALETTE["blue"]
    if accent in PALETTE:
        return PALETTE[accent]
    if re.fullmatch(r"#?[0-9a-fA-F]{6}", accent or ""):
        hx = accent if accent.startswith("#") else "#" + accent
        return {"base": hx, "deep": _shade(hx, -0.42), "light": _shade(hx, 0.45), "sec": PALETTE["purple"]["base"]}
    return PALETTE["blue"]


def _shade(hx: str, f: float) -> str:
    r, g, b = int(hx[1:3], 16), int(hx[3:5], 16), int(hx[5:7], 16)
    if f >= 0:
        r, g, b = (r + (255 - r) * f, g + (255 - g) * f, b + (255 - b) * f)
    else:
        r, g, b = (r * (1 + f), g * (1 + f), b * (1 + f))
    return "#%02X%02X%02X" % (int(r), int(g), int(b))


def _icon_svg(name: str, size: int, stroke: str, sw: float = 2.0, opacity: float = 1.0) -> str:
    inner = ICONS.get(name, ICONS["heart"])
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="%s" '
            'stroke-width="%.2f" stroke-linecap="round" stroke-linejoin="round" '
            'style="opacity:%.2f">%s</svg>') % (size, size, stroke, sw, opacity, inner)


def title_size(title: str) -> int:
    n = len(title)
    if n <= 16:
        return 104
    if n <= 24:
        return 92
    if n <= 34:
        return 80
    if n <= 46:
        return 68
    if n <= 60:
        return 58
    return 50


# ── Logo (real wordmark, themed by background, never AI) ─────────────────────
def logo_data_uri(dark_bg: bool) -> str:
    """Return a data-URI for the bundled wordmark, recoloured for the bg.

    Bundled `pleasurai-logo.png` = charcoal 'Pleasur.' + blue '.ai' on transparent (light-bg).
    For a dark bg we recolour the charcoal half to white and keep the blue '.ai'.
    Falls back to the bundled file unmodified if PIL is unavailable.
    """
    src = SCRIPT_DIR / "pleasurai-logo.png"
    try:
        import warnings
        from PIL import Image
        img = Image.open(src).convert("RGBA")
        if dark_bg:
            out = []
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                pixels = list(img.getdata())
            for (r, g, b, a) in pixels:
                # charcoal wordmark (dark, low blue dominance) -> white; keep the blue '.ai'
                if a > 30 and not (b > r + 25 and b > 110):
                    lum = 0.299 * r + 0.587 * g + 0.114 * b
                    if lum < 150:
                        out.append((245, 247, 250, a))
                        continue
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


# ── Motif: a designed "app-tile" composition (not clip-art) ──────────────────
def build_motif(theme: str, ac: dict, icon: str) -> str:
    sats = SATELLITES.get(icon, ["heart", "sparkles"])
    if theme == "gradient":
        tile_grad = "linear-gradient(155deg, #FFFFFF 0%, rgba(255,255,255,.86) 100%)"
        icon_stroke = ac["deep"]
        ring_inset = "rgba(255,255,255,.34)"
        chip_bg = _rgba(ac["base"], 0.30)
        chip_stroke = "#FFFFFF"
        chip_border = "rgba(255,255,255,.40)"
        halo = "rgba(255,255,255,.22)"
        glow = ac["light"]
        refl = "rgba(255,255,255,.16)"
    elif theme == "spotlight":
        tile_grad = "linear-gradient(155deg, %s 0%%, %s 100%%)" % (ac["base"], ac["deep"])
        icon_stroke = "#FFFFFF"
        ring_inset = "rgba(255,255,255,.20)"
        chip_bg = _rgba(ac["base"], 0.22)
        chip_stroke = ac["light"]
        chip_border = _rgba(ac["light"], 0.30)
        halo = _rgba(ac["light"], 0.18)
        glow = ac["base"]
        refl = _rgba(ac["base"], 0.22)
    else:  # light
        tile_grad = "linear-gradient(155deg, %s 0%%, %s 100%%)" % (ac["light"], ac["base"])
        icon_stroke = "#FFFFFF"
        ring_inset = "rgba(255,255,255,.45)"
        chip_bg = "#FFFFFF"
        chip_stroke = ac["base"]
        chip_border = "rgba(20,26,36,.08)"
        halo = _rgba(ac["base"], 0.16)
        glow = ac["light"]
        refl = _rgba(ac["base"], 0.14)

    # two confident chips in a tight diagonal orbit hugging the tile
    chips = ""
    placements = [("top:6px;right:24px", 86, sats[0]),
                  ("bottom:18px;left:6px", 74, sats[1] if len(sats) > 1 else sats[0])]
    for pos, sz, ic in placements:
        chips += (
            '<div class="chip" style="%s;width:%dpx;height:%dpx;background:%s;border:1.5px solid %s">%s</div>'
            % (pos, sz, sz, chip_bg, chip_border, _icon_svg(ic, int(sz * 0.46), chip_stroke, 2.1))
        )
    sparks = ('<span class="spark" style="top:24px;left:30px"></span>'
              '<span class="spark sm" style="top:120px;right:6px"></span>'
              '<span class="spark sm" style="bottom:64px;left:-2px"></span>')
    return (
        '<div class="motif">'
        '<div class="glowfield" style="background:radial-gradient(circle at 50%% 46%%, %s 0%%, transparent 60%%)"></div>'
        '<div class="halo" style="width:340px;height:340px;border:1.5px solid %s"></div>'
        '<div class="halo" style="width:248px;height:248px;border:1.5px solid %s;opacity:.6"></div>'
        '<div class="reflection" style="background:radial-gradient(ellipse at center, %s 0%%, transparent 70%%)"></div>'
        '<div class="tile" style="background:%s;box-shadow:0 42px 90px -26px %s, 0 0 0 1px %s inset">'
        '<div class="gloss"></div>%s</div>%s%s</div>'
    ) % (_rgba(glow, 0.6 if theme != "light" else 0.55), halo, halo, refl, tile_grad,
         _rgba(ac["deep"], 0.6), ring_inset, _icon_svg(icon, 150, icon_stroke, 1.9), chips, sparks)


def _rgba(hx: str, a: float) -> str:
    return "rgba(%d,%d,%d,%.2f)" % (int(hx[1:3], 16), int(hx[3:5], 16), int(hx[5:7], 16), a)


def _img_uri(path: str) -> str:
    p = Path(path)
    ext = (p.suffix.lower().lstrip(".") or "png")
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    return "data:image/%s;base64," % mime + base64.b64encode(p.read_bytes()).decode()


# ── Theme backgrounds ────────────────────────────────────────────────────────
def theme_bg(theme: str, ac: dict) -> str:
    if theme == "gradient":
        return (
            "background:"
            "radial-gradient(130%% 150%% at 8%% 6%%, %s 0%%, %s 40%%, %s 78%%, #0A1024 130%%);"
            % (ac["light"], ac["base"], ac["deep"])
        )
    if theme == "spotlight":
        return (
            "background:"
            "radial-gradient(70%% 80%% at 72%% 32%%, %s 0%%, transparent 58%%),"
            "radial-gradient(50%% 60%% at 18%% 90%%, %s 0%%, transparent 60%%),"
            "#0C1018;" % (_rgba(ac["base"], 0.34), _rgba(ac["sec"], 0.16))
        )
    return "background:#F6F8FB;"  # light


# ── Full HTML (token replacement — keeps CSS braces literal) ─────────────────
PAGE = """<!doctype html><html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=IBM+Plex+Sans:wght@600;700&family=Geist:wght@400;500;600&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1600px;height:900px}
#stage{position:relative;width:1600px;height:900px;overflow:hidden;@@BG@@
  font-family:'Geist',system-ui,-apple-system,'Segoe UI',sans-serif}
.grain{position:absolute;inset:0;opacity:@@GRAINOP@@;mix-blend-mode:@@GRAINBLEND@@;pointer-events:none}
.vign{position:absolute;inset:0;pointer-events:none;@@VIGN@@}
.scrim{position:absolute;inset:0;pointer-events:none}
.dotgrid{position:absolute;inset:0;pointer-events:none;@@DOTGRID@@}
.orb{position:absolute;border-radius:50%;filter:blur(46px);pointer-events:none}
#content{position:absolute;inset:0;display:flex;align-items:center;padding:0 96px}
.left{width:62%;z-index:5}
.eyebrow{display:inline-flex;align-items:center;gap:11px;font-family:'IBM Plex Sans',sans-serif;
  font-weight:700;font-size:18px;letter-spacing:3.4px;text-transform:uppercase;@@EYEBROW_CSS@@;margin-bottom:26px}
.eyebrow .rule{width:30px;height:3px;border-radius:2px;background:@@ACCENT@@}
.eyebrow .dot{width:9px;height:9px;border-radius:50%;background:@@ACCENT@@}
h1{font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:@@TSIZE@@px;line-height:1.04;
  letter-spacing:-2px;color:@@TITLECOLOR@@;max-width:15ch}
h1 .hl{color:@@ACCENT@@}
.sub{font-family:'Geist',sans-serif;font-weight:450;font-size:25px;line-height:1.5;color:@@SUBCOLOR@@;
  margin-top:26px;max-width:30ch}
.right{position:absolute;right:80px;top:0;bottom:0;width:40%;display:flex;align-items:center;justify-content:center;z-index:4}
.motif{position:relative;width:380px;height:380px;display:flex;align-items:center;justify-content:center}
.glowfield{position:absolute;inset:-90px;pointer-events:none}
.halo{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);border-radius:50%;pointer-events:none}
.reflection{position:absolute;width:280px;height:74px;bottom:24px;left:50%;transform:translateX(-50%);pointer-events:none;filter:blur(7px)}
.tile{position:relative;width:248px;height:248px;border-radius:62px;display:flex;align-items:center;justify-content:center;z-index:2}
.gloss{position:absolute;inset:0;border-radius:62px;pointer-events:none;
  background:linear-gradient(160deg,rgba(255,255,255,.5) 0%,rgba(255,255,255,0) 42%)}
.chip{position:absolute;border-radius:24px;display:flex;align-items:center;justify-content:center;
  backdrop-filter:blur(6px);box-shadow:0 18px 40px -16px rgba(10,16,30,.5)}
.spark{position:absolute;width:14px;height:14px;border-radius:50%;background:@@ACCENT@@;opacity:.85;
  box-shadow:0 0 18px 3px @@ACCENTGLOW@@}
.spark.sm{width:8px;height:8px;opacity:.6}
.footer{position:absolute;left:96px;bottom:52px;display:flex;align-items:center;gap:18px;z-index:6}
.footer img{height:30px;display:block}
.byline{font-family:'Geist',sans-serif;font-size:16px;font-weight:500;color:@@METACOLOR@@;
  padding-left:18px;border-left:1.5px solid @@METARULE@@}
</style></head><body>
<div id="stage">
  @@ORBS@@
  <div class="dotgrid"></div>
  <div class="vign"></div>
  <div class="scrim" style="@@SCRIM@@"></div>
  <div id="content">
    <div class="left">
      @@EYEBROW@@
      <h1>@@TITLE@@</h1>
      @@SUB@@
    </div>
    <div class="right">@@MOTIF@@</div>
  </div>
  <div class="footer"><img src="@@LOGO@@" alt="Pleasur.ai">@@BYLINE@@</div>
  <svg class="grain" width="1600" height="900"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>
</div></body></html>"""


def build_html(c: dict) -> str:
    theme = (c.get("theme") or "gradient").lower()
    ac = resolve_accent(c.get("accent") or ("blue" if theme != "spotlight" else "purple"))
    icon = (c.get("icon") or pick_icon(c.get("title", ""))).lower()
    title = c.get("title", "Untitled").strip()
    eyebrow = (c.get("eyebrow") or "").strip()
    subtitle = (c.get("subtitle") or "").strip()
    author = (c.get("author") or "").strip()
    dark = theme in ("gradient", "spotlight")

    if dark:
        title_color, sub_color = "#FFFFFF", "rgba(255,255,255,.74)"
        eyebrow_css = "color:rgba(255,255,255,.92)"
        meta_color, meta_rule = "rgba(255,255,255,.66)", "rgba(255,255,255,.26)"
        accent_text = ac["light"]
        grain_op, grain_blend = "0.07", "soft-light"
        vign = "background:radial-gradient(120% 120% at 50% 40%, transparent 55%, rgba(6,10,20,.45) 100%)"
        dotgrid = ""
        orbs = (
            '<div class="orb" style="width:360px;height:360px;left:-90px;top:-120px;background:radial-gradient(circle,%s,transparent 70%%)"></div>'
            '<div class="orb" style="width:300px;height:300px;right:18%%;bottom:-130px;background:radial-gradient(circle,%s,transparent 70%%)"></div>'
            % (_rgba(ac["light"], 0.20), _rgba(ac["sec"], 0.18))
        )
    else:  # light
        title_color, sub_color = INK, MUTE
        eyebrow_css = "color:%s" % ac["deep"]
        meta_color, meta_rule = "#6B7484", "rgba(20,26,36,.16)"
        accent_text = ac["base"]
        grain_op, grain_blend = "0.04", "multiply"
        vign = f"background:radial-gradient(140% 120% at 78% 18%, {_rgba(ac['light'], 0.5)} 0%, transparent 46%)"
        dotgrid = ("background-image:radial-gradient(rgba(20,26,36,.05) 1.4px, transparent 1.4px);"
                   "background-size:26px 26px;mask-image:linear-gradient(120deg, transparent 40%, black 100%)")
        orbs = ('<div class="orb" style="width:520px;height:520px;right:-120px;top:-160px;background:radial-gradient(circle,%s,transparent 70%%)"></div>'
                % _rgba(ac["light"], 0.55))

    # ── route B: AI-illustration background (text-free) + deterministic text overlay ──
    bg_css = theme_bg(theme, ac)
    motif_html = build_motif(theme, ac, icon)
    scrim = ""
    bg_image = c.get("bg_image")
    if bg_image:
        uri = _img_uri(bg_image)
        bg_css = "background:#0A0E18 url('%s') center/cover no-repeat;" % uri
        scrim = ("background:"
                 "linear-gradient(90deg, rgba(7,10,18,.88) 0%, rgba(7,10,18,.60) 36%, rgba(7,10,18,.10) 64%, rgba(7,10,18,.34) 100%),"
                 "linear-gradient(0deg, rgba(7,10,18,.58) 0%, transparent 30%)")
        motif_html = ""          # the AI illustration IS the visual
        orbs = dotgrid = vign = ""
        title_color, sub_color = "#FFFFFF", "rgba(255,255,255,.82)"
        eyebrow_css = "color:rgba(255,255,255,.94)"
        meta_color, meta_rule = "rgba(255,255,255,.72)", "rgba(255,255,255,.32)"
        accent_text = ac["light"]
        grain_op, grain_blend = "0.05", "soft-light"
        dark = True

    # eyebrow markup (rule + dot accents)
    if eyebrow:
        eyebrow_html = '<div class="eyebrow"><span class="rule"></span>%s<span class="dot"></span></div>' % _esc(eyebrow)
    else:
        eyebrow_html = ""
    sub_html = '<p class="sub">%s</p>' % _esc(subtitle) if subtitle else ""
    byline_html = '<span class="byline">%s</span>' % _esc(author) if author else ""

    html = PAGE
    repl = {
        "@@BG@@": bg_css,
        "@@GRAINOP@@": grain_op, "@@GRAINBLEND@@": grain_blend,
        "@@VIGN@@": vign, "@@DOTGRID@@": dotgrid, "@@ORBS@@": orbs, "@@SCRIM@@": scrim,
        "@@EYEBROW_CSS@@": eyebrow_css, "@@EYEBROW@@": eyebrow_html,
        "@@ACCENT@@": accent_text, "@@ACCENTGLOW@@": _rgba(ac["base"], 0.7),
        "@@TSIZE@@": str(title_size(title)),
        "@@TITLECOLOR@@": title_color, "@@SUBCOLOR@@": sub_color, "@@SUB@@": sub_html,
        "@@TITLE@@": _esc(title),
        "@@MOTIF@@": motif_html,
        "@@LOGO@@": logo_data_uri(dark),
        "@@BYLINE@@": byline_html,
        "@@METACOLOR@@": meta_color, "@@METARULE@@": meta_rule,
    }
    for k, v in repl.items():
        html = html.replace(k, v)
    return html


def _esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def render(html: str, out: Path, width: int, height: int, supersample: int) -> None:
    try:
        from patchright.sync_api import sync_playwright
    except ImportError:
        from playwright.sync_api import sync_playwright
    out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--no-sandbox", "--force-color-profile=srgb"])
        pg = b.new_context(viewport={"width": width, "height": height},
                           device_scale_factor=supersample).new_page()
        pg.set_content(html, wait_until="networkidle")
        pg.wait_for_timeout(700)  # let Google Fonts settle
        big = out.with_suffix(".super.png")
        pg.locator("#stage").screenshot(path=str(big))
        b.close()
    # supersample down to the exact target for crisp text/edges
    try:
        from PIL import Image
        im = Image.open(big).convert("RGB")
        if im.size != (width, height):
            im = im.resize((width, height), Image.LANCZOS)
        im.save(out)
        big.unlink(missing_ok=True)
    except Exception:
        big.replace(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Render an on-brand article cover / hero image.")
    ap.add_argument("--content", help="cover JSON file")
    ap.add_argument("--title")
    ap.add_argument("--eyebrow", default="")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--theme", default="gradient", choices=["gradient", "light", "spotlight"])
    ap.add_argument("--accent", default="")
    ap.add_argument("--icon", default="")
    ap.add_argument("--author", default="")
    ap.add_argument("--bg-image", dest="bg_image", default="", help="route B: composite text over an AI illustration")
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
        c = {"title": a.title, "eyebrow": a.eyebrow, "subtitle": a.subtitle,
             "theme": a.theme, "accent": a.accent, "icon": a.icon, "author": a.author,
             "bg_image": a.bg_image or None}

    html = build_html(c)
    render(html, Path(a.out), a.width, a.height, a.supersample)
    print(json.dumps({"status": "captured", "path": a.out, "theme": c.get("theme", "gradient"),
                      "icon": (c.get("icon") or pick_icon(c.get("title", ""))),
                      "dims": "%dx%d" % (a.width, a.height)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
