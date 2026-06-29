#!/usr/bin/env python3
"""Render premium, ON-BRAND process flows / decision trees / flow diagrams headless (2026-06-28 v1).

The DIAGRAM engine — the 4th blog visual type (alongside annotation, infographic, chart).
Clean + structured + on-brand, deliberately DISTINCT from the hand-drawn infographic: crisp
geometric node cards, smooth connectors, exact blog fonts.

How it works (mirrors render_chart_web.py — same brand card standard):
  * dagre.js (the layout engine that powers Mermaid) computes node coordinates + edge routing.
  * We render the look ourselves: absolutely-positioned HTML node cards (rounded cards, numbered
    badges, decision diamonds, terminal pills — wrapped text, IBM Plex Sans + Geist) over an SVG
    edge layer (smooth rounded connectors + crisp triangle arrowheads + Yes/No edge pills).
  * Wrapped in the brand card (white card on #F7F8FA), the REAL Pleasur.ai logo composited in the
    footer, rendered headless via patchright @2x and screenshotted tight.
  dagre.min.js is bundled next to the engine — no runtime CDN dependency.

Usage:
  # linear "how it works" process (steps + connecting arrows)
  python render_diagram_web.py --type linear --title "How Pleasur.AI works" \
    --data '[{"label":"Create","desc":"..."},{"label":"Chat","desc":"..."}]' --out flow.png

  # decision tree (nested)
  python render_diagram_web.py --type tree --title "Which mode fits you?" \
    --data '{"label":"Want voice?","children":[{"edge":"Yes","tone":"yes","label":"Voice mode"}, ...]}' --out tree.png

  # circular cycle (icons-in-pastel-circles loop — "how X works" as a repeating loop)
  python render_diagram_web.py --type cycle --title "How memory works" \
    --data '[{"label":"You chat","icon":"chat"},{"label":"Saved to memory","icon":"chip"}]' --out cycle.png

  # arbitrary flow (full node/edge spec, supports branching + merges)
  python render_diagram_web.py --type flow --title "..." --data '{"direction":"TB","nodes":[...],"edges":[...]}' --out flow.png
  python render_diagram_web.py --config spec.json --title "..." --out flow.png
"""
import argparse
import base64
import html
import json
import sys
from pathlib import Path

PALETTE = ["#2E90FA", "#8B5CF6", "#22B276", "#F5A623", "#E8655A", "#0891B2", "#534AB7"]
FONT = "'Geist', system-ui, -apple-system, 'Segoe UI', sans-serif"          # blog body font
TITLE_FONT = "'IBM Plex Sans', 'Geist', system-ui, sans-serif"             # blog heading font

THEME = {
    "palette": PALETTE,
    "edge": "#B7BFCC",          # neutral connector
    "pos": "#22B276",           # Yes / true branch
    "neg": "#E8655A",           # No / false branch
    "caution": "#F5A623",       # caution branch
    "decisionBorder": "#2E90FA",
    "diamond": 156,             # decision bbox (px); element = diamond / sqrt(2)
    "cardw": 232,               # default step/process/outcome card width (px)
}

# Semantic tone -> outcome colour
TONE = {
    "yes": "#22B276", "positive": "#22B276", "good": "#22B276", "success": "#22B276",
    "no": "#E8655A", "negative": "#E8655A", "bad": "#E8655A", "stop": "#E8655A",
    "caution": "#F5A623", "warn": "#F5A623", "maybe": "#F5A623",
    "alt": "#8B5CF6", "info": "#2E90FA",
}


# ---------------------------------------------------------------- preset builders
def build_linear(items, direction):
    nodes, edges = [], []
    for i, it in enumerate(items):
        if isinstance(it, str):
            label, desc, color = it, "", None
        else:
            label, desc, color = it.get("label", ""), it.get("desc", ""), it.get("color")
        n = {"id": "n%d" % i, "shape": "step", "num": i + 1, "label": label,
             "color": color or PALETTE[i % 4]}
        if desc:
            n["desc"] = desc
        nodes.append(n)
        if i:
            edges.append({"from": "n%d" % (i - 1), "to": "n%d" % i})
    return {"direction": direction or "LR", "type": "linear", "equalize": True, "nodes": nodes, "edges": edges}


def build_tree(data, direction):
    # `edge` + `tone` on a child colour the EDGE (the branch answer) only.
    # An outcome card's colour is its own identity: explicit `color`, else palette-cycled by leaf order.
    nodes, edges, ctr, leaf = [], [], [0], [0]

    def walk(node):
        nid = "t%d" % ctr[0]
        ctr[0] += 1
        kids = node.get("children") or []
        shape = node.get("shape") or ("decision" if kids else "outcome")
        n = {"id": nid, "label": node.get("label", ""), "shape": shape}
        if node.get("desc"):
            n["desc"] = node["desc"]
        if shape == "outcome":
            n["color"] = node.get("color") or PALETTE[leaf[0] % len(PALETTE)]
            leaf[0] += 1
        elif node.get("color"):
            n["color"] = node["color"]
        nodes.append(n)
        for ch in kids:
            cid = walk(ch)
            e = {"from": nid, "to": cid}
            if ch.get("edge"):
                e["label"] = ch["edge"]
            if ch.get("tone"):
                e["tone"] = ch["tone"]
            edges.append(e)
        return nid

    walk(data)
    return {"direction": direction or "TB", "type": "tree", "nodes": nodes, "edges": edges}


def build_cycle(items):
    """Circular loop of icon nodes — pastel circle + line icon + label, clockwise arrows.
    `items` = list of strings or {label, icon?, color?}. For "how X works" feedback loops."""
    nodes = []
    for i, it in enumerate(items):
        if isinstance(it, str):
            label, icon, color = it, None, None
        else:
            label, icon, color = it.get("label", ""), it.get("icon"), it.get("color")
        nodes.append({"id": "c%d" % i, "shape": "circle", "label": label,
                      "icon": (icon or "dot"), "color": color or PALETTE[i % 4]})
    return {"type": "cycle", "nodes": nodes, "edges": []}


# ------------------------------------------------------------------------- assets
CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=IBM+Plex+Sans:wght@600;700&display=swap');
*{box-sizing:border-box}
body{margin:0;font-family:__FONT__;-webkit-font-smoothing:antialiased}
#wrap{display:inline-block;padding:46px;background:#F7F8FA}
#card{display:inline-block;background:#fff;border:1px solid #EDF0F4;border-radius:20px;
  padding:26px 32px 18px;box-shadow:0 14px 46px rgba(20,30,50,0.08)}
#t{font-family:__TFONT__;font-size:23px;font-weight:700;color:#1E2430;letter-spacing:-0.2px;max-width:1180px}
#s{font-family:__FONT__;font-size:14px;color:#7A828F;margin:5px 0 2px;max-width:1180px;line-height:1.45}
#diagram{position:relative;margin:20px auto 6px}
#f{text-align:right;margin-top:12px;opacity:.92}
#f img{vertical-align:middle}

/* ---- nodes ---- */
.node{box-sizing:border-box;font-family:__FONT__}
.node.step,.node.process,.node.outcome{
  width:var(--cardw);background:#fff;border:1px solid #E7ECF3;border-radius:16px;
  box-shadow:0 6px 20px rgba(20,30,50,0.07);padding:16px 18px}
.node.process{border-left:4px solid var(--accent);padding-left:18px}
.node.outcome{border:1px solid var(--accent-bd);border-left:4px solid var(--accent);background:var(--accent-bg)}
.hd{display:flex;align-items:center;gap:11px}
.badge{flex:0 0 30px;width:30px;height:30px;border-radius:50%;color:#fff;font-weight:700;
  font-size:15px;font-family:__TFONT__;display:flex;align-items:center;justify-content:center;
  box-shadow:0 3px 9px rgba(20,30,50,0.20)}
.n-title{font-family:__TFONT__;font-weight:700;font-size:16px;color:#1E2430;line-height:1.26}
.process .n-title,.outcome .n-title{font-size:15.5px}
.n-desc{font-family:__FONT__;font-size:12.7px;color:#6B7480;line-height:1.46;margin-top:8px}
.outcome .n-desc{color:#5C6573}

/* decision diamond (rounded square rotated 45, text counter-rotated) */
.node.decision{background:#fff;border:2px solid var(--accent);border-radius:18px;
  box-shadow:0 6px 20px rgba(20,30,50,0.09);display:flex;align-items:center;justify-content:center}
.d-inner{text-align:center}
.d-title{font-family:__TFONT__;font-weight:700;font-size:14px;color:#1E2430;line-height:1.24}

/* terminal pill (start / end) */
.node.terminal{border-radius:999px;padding:13px 26px;color:#fff;font-weight:700;
  font-family:__TFONT__;font-size:15px;text-align:center;box-shadow:0 6px 18px rgba(20,30,50,0.16)}

/* edge labels */
.edge-label{position:absolute;font-family:__FONT__;font-size:11.5px;font-weight:600;color:#5B6472;
  background:#fff;border:1px solid #DCE2EB;border-radius:8px;padding:2px 8px;white-space:nowrap;
  box-shadow:0 2px 6px rgba(20,30,50,0.06)}
.edge-label.lbl-pos{color:#198F5C;border-color:#BFE6D2;background:#F0FBF5}
.edge-label.lbl-neg{color:#C2483D;border-color:#F3CFCA;background:#FDF2F1}
.edge-label.lbl-cau{color:#B5790F;border-color:#F3DFB6;background:#FEF8EC}
.edge-layer{position:absolute;left:0;top:0;overflow:visible}

/* ---- cycle (icons-in-pastel-circles loop) ---- */
.node.circle{position:absolute;border-radius:50%;display:flex;align-items:center;justify-content:center;
  box-shadow:0 8px 22px rgba(20,30,50,0.08)}
.node.circle svg{width:46%;height:46%}
.cyc-label{position:absolute;font-family:__TFONT__;font-weight:600;font-size:15.5px;color:#344054;
  text-align:center;line-height:1.3}
"""

JS = r"""
document.fonts.ready.then(function(){
  var SPEC = window.SPEC, T = window.THEME, NS = 'http://www.w3.org/2000/svg';
  var PALETTE = T.palette, dir = SPEC.direction || 'LR';
  var nodes = SPEC.nodes || [], edges = SPEC.edges || [];
  var diagram = document.getElementById('diagram');
  var DIA = T.diamond, DEL = Math.round(DIA / Math.SQRT2);   // diamond element side

  nodes.forEach(function(n, i){ if (n._idx == null) n._idx = i; });

  var ICONS = {
    chat:'<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    message:'<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M8 9h8M8 13h5"/>',
    star:'<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/>',
    sparkle:'<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 14.5l.9 2.4 2.4.9-2.4.9-.9 2.4-.9-2.4-2.4-.9 2.4-.9z"/>',
    chip:'<rect x="5" y="5" width="14" height="14" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>',
    shield:'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    lock:'<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    key:'<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6M15.5 7.5l3 3L22 7l-3-3"/>',
    heart:'<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.29 1.49 4.04 3 5.5l7 7z"/>',
    user:'<circle cx="12" cy="8" r="4"/><path d="M5 21v-1a7 7 0 0 1 14 0v1"/>',
    database:'<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/><path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"/>',
    bell:'<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    clock:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    search:'<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    bolt:'<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
    bulb:'<path d="M9 18h6M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.3h6c0-1 .4-1.8 1-2.3A7 7 0 0 0 12 2z"/>',
    check:'<circle cx="12" cy="12" r="9"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    eye:'<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
    phone:'<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2 4.2 2 2 0 0 1 4 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7A2 2 0 0 1 22 16.9z"/>',
    image:'<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.8"/><path d="m21 15-5-5L5 21"/>',
    gear:'<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9 17 7M7 17l-2.1 2.1"/>',
    dot:'<circle cx="12" cy="12" r="7"/>'
  };
  ICONS.note=ICONS.star; ICONS.recall=ICONS.sparkle; ICONS.memory=ICONS.chip; ICONS.brain=ICONS.chip;
  ICONS.privacy=ICONS.shield; ICONS.idea=ICONS.bulb; ICONS.time=ICONS.clock; ICONS.lightning=ICONS.bolt;
  ICONS.find=ICONS.search; ICONS.gallery=ICONS.image; ICONS.call=ICONS.phone; ICONS.person=ICONS.user;
  ICONS.done=ICONS.check; ICONS.settings=ICONS.gear;

  if ((SPEC.type || '') === 'cycle'){ renderCycle(); return; }

  var POS={yes:1,positive:1,good:1,success:1,proceed:1,"true":1}, NEG={no:1,negative:1,bad:1,stop:1,block:1,"false":1}, CAU={caution:1,warn:1,maybe:1,review:1};
  function colOf(n){ if(n.color) return n.color; if((n.shape||'')==='process') return PALETTE[0]; return PALETTE[n._idx % PALETTE.length]; }
  function tint(hex, a){
    var h = hex.replace('#',''); var r=parseInt(h.substr(0,2),16), g=parseInt(h.substr(2,2),16), b=parseInt(h.substr(4,2),16);
    return 'rgb('+Math.round(r+(255-r)*(1-a))+','+Math.round(g+(255-g)*(1-a))+','+Math.round(b+(255-b)*(1-a))+')';
  }
  function el(cls){ var d=document.createElement('div'); if(cls) d.className=cls; return d; }

  function buildNode(n){
    var shape = n.shape || 'process', color = colOf(n), d;
    if (shape === 'decision'){
      d = el('node decision');
      d.style.width = DEL+'px'; d.style.height = DEL+'px';
      d.style.transform = 'rotate(45deg)';
      d.style.setProperty('--accent', n.color || T.decisionBorder);
      var inner = el('d-inner'); inner.style.transform='rotate(-45deg)'; inner.style.width=(DIA*0.80)+'px';
      var dt = el('d-title'); dt.textContent = n.label; inner.appendChild(dt);
      d.appendChild(inner);
    } else if (shape === 'terminal' || shape === 'start' || shape === 'end'){
      d = el('node terminal');
      d.style.background = n.color || (shape === 'end' ? PALETTE[2] : PALETTE[0]);
      d.textContent = n.label;
    } else { // step / process / outcome
      d = el('node ' + (shape === 'step' ? 'step' : shape === 'outcome' ? 'outcome' : 'process'));
      d.style.setProperty('--cardw', T.cardw + 'px');
      d.style.setProperty('--accent', color);
      if (shape === 'outcome'){ d.style.setProperty('--accent-bg', tint(color, 0.10)); d.style.setProperty('--accent-bd', tint(color, 0.34)); }
      var body = d;
      if (shape === 'step'){
        var hd = el('hd');
        var b = el('badge'); b.style.background = color; b.textContent = (n.num != null ? n.num : '');
        var ht = el('n-title'); ht.textContent = n.label;
        hd.appendChild(b); hd.appendChild(ht); d.appendChild(hd);
      } else {
        var t = el('n-title'); t.textContent = n.label; d.appendChild(t);
      }
      if (n.desc){ var de = el('n-desc'); de.textContent = n.desc; d.appendChild(de); }
    }
    return d;
  }

  // ---- pass 1: build + measure (fonts are ready) ----
  nodes.forEach(function(n){
    var d = buildNode(n);
    d.style.position='absolute'; d.style.left='-9999px'; d.style.top='0';
    document.body.appendChild(d);
    n._el = d;
  });
  nodes.forEach(function(n){
    if ((n.shape||'') === 'decision'){ n._w = n._h = DIA; n._ew = n._eh = DEL; }
    else { n._ew = n._w = n._el.offsetWidth; n._eh = n._h = n._el.offsetHeight; }
  });

  // equalize step-card heights so a "how it works" row reads as a uniform set
  if (SPEC.equalize){
    var steps = nodes.filter(function(n){ return (n.shape||'')==='step'; });
    if (steps.length){
      var mh = Math.max.apply(null, steps.map(function(n){ return n._eh; }));
      steps.forEach(function(n){ n._eh = n._h = mh; n._el.style.height = mh+'px'; });
    }
  }

  // ---- dagre layout ----
  var g = new dagre.graphlib.Graph({multigraph:true});
  var LR = dir === 'LR';
  g.setGraph({rankdir:dir,
    nodesep: SPEC.nodesep != null ? SPEC.nodesep : (LR ? 30 : 42),
    ranksep: SPEC.ranksep != null ? SPEC.ranksep : (LR ? 66 : 58),
    edgesep: 18, marginx: 6, marginy: 6});
  g.setDefaultEdgeLabel(function(){ return {}; });
  nodes.forEach(function(n){ g.setNode(n.id, {width:n._w, height:n._h}); });
  edges.forEach(function(e, i){
    var lbl = e.label || '';
    g.setEdge(e.from, e.to, {label:lbl, width: lbl ? (lbl.length*6.6+20) : 0, height: lbl?22:0, labelpos:'c'}, 'e'+i);
  });
  dagre.layout(g);
  var W = g.graph().width, H = g.graph().height;
  diagram.style.width = W+'px'; diagram.style.height = H+'px';

  // ---- edge layer (svg) ----
  var svg = document.createElementNS(NS,'svg');
  svg.setAttribute('width', W); svg.setAttribute('height', H); svg.setAttribute('class','edge-layer');
  diagram.appendChild(svg);

  function rounded(pts, r){
    if (pts.length < 3) return 'M'+pts[0].x+' '+pts[0].y+' L'+pts[pts.length-1].x+' '+pts[pts.length-1].y;
    var d = 'M'+pts[0].x+' '+pts[0].y;
    for (var i=1;i<pts.length-1;i++){
      var p0=pts[i-1], p1=pts[i], p2=pts[i+1];
      var v1x=p1.x-p0.x, v1y=p1.y-p0.y, v2x=p2.x-p1.x, v2y=p2.y-p1.y;
      var l1=Math.hypot(v1x,v1y)||1, l2=Math.hypot(v2x,v2y)||1, rr=Math.min(r,l1/2,l2/2);
      d += ' L'+(p1.x-v1x/l1*rr)+' '+(p1.y-v1y/l1*rr)+' Q'+p1.x+' '+p1.y+' '+(p1.x+v2x/l2*rr)+' '+(p1.y+v2y/l2*rr);
    }
    var last = pts[pts.length-1]; d += ' L'+last.x+' '+last.y;
    return d;
  }
  function edgeColor(e){
    if (e.color) return e.color;
    var tn = (e.tone||'').toLowerCase();
    if (POS[tn]) return T.pos;
    if (NEG[tn]) return T.neg;
    if (CAU[tn]) return T.caution;
    return T.edge;
  }
  function toneClass(e){
    var tn = (e.tone||'').toLowerCase();
    if (POS[tn]) return 'lbl-pos';
    if (NEG[tn]) return 'lbl-neg';
    if (CAU[tn]) return 'lbl-cau';
    return '';
  }

  edges.forEach(function(e, i){
    var ed = g.edge({v:e.from, w:e.to, name:'e'+i}); if (!ed) return;
    var pts = ed.points.slice(); var col = edgeColor(e);
    var n=pts.length, end=pts[n-1], prev=pts[n-2];
    var vx=end.x-prev.x, vy=end.y-prev.y, L=Math.hypot(vx,vy)||1, ux=vx/L, uy=vy/L;
    var head=10, hw=5.4, base={x:end.x-ux*head, y:end.y-uy*head};
    var path = document.createElementNS(NS,'path');
    path.setAttribute('d', rounded(pts.slice(0,n-1).concat([base]), 14));
    path.setAttribute('fill','none'); path.setAttribute('stroke',col);
    path.setAttribute('stroke-width','2.4'); path.setAttribute('stroke-linecap','round'); path.setAttribute('stroke-linejoin','round');
    svg.appendChild(path);
    var nx=-uy, ny=ux, tri=document.createElementNS(NS,'path');
    tri.setAttribute('d','M'+end.x+' '+end.y+' L'+(base.x+nx*hw)+' '+(base.y+ny*hw)+' L'+(base.x-nx*hw)+' '+(base.y-ny*hw)+' Z');
    tri.setAttribute('fill', col); svg.appendChild(tri);
    e._lx = ed.x; e._ly = ed.y;
  });

  // ---- place nodes ----
  nodes.forEach(function(n){
    var nd = g.node(n.id), d = n._el;
    d.style.left = (nd.x - n._ew/2)+'px'; d.style.top = (nd.y - n._eh/2)+'px';
    diagram.appendChild(d);
  });

  // ---- edge label pills ----
  edges.forEach(function(e){
    if (!e.label) return;
    var p = el('edge-label '+toneClass(e)); p.textContent = e.label;
    diagram.appendChild(p);
    p.style.left = (e._lx - p.offsetWidth/2)+'px'; p.style.top = (e._ly - p.offsetHeight/2)+'px';
  });

  document.body.setAttribute('data-ready','1');

  // ---- cycle renderer (icons-in-pastel-circles loop; bypasses dagre) ----
  function renderCycle(){
    var N = nodes.length;
    var SIZE = 132, R = Math.max(158, 40 * N + 30), PAD = 84;
    var total = 2 * R + SIZE + 2 * PAD, CX = total / 2, CY = total / 2;
    diagram.style.width = total + 'px'; diagram.style.height = total + 'px';
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('width', total); svg.setAttribute('height', total); svg.setAttribute('class', 'edge-layer');
    diagram.appendChild(svg);
    var pos = nodes.map(function(n, i){
      var a = -Math.PI / 2 + i * 2 * Math.PI / N;
      return {x: CX + R * Math.cos(a), y: CY + R * Math.sin(a)};
    });
    for (var i = 0; i < N; i++){ cycArrow(svg, pos[i], pos[(i + 1) % N], CX, CY, SIZE / 2); }
    nodes.forEach(function(n, i){
      var color = colOf(n);
      var c = el('node circle');
      c.style.width = SIZE + 'px'; c.style.height = SIZE + 'px';
      c.style.left = (pos[i].x - SIZE / 2) + 'px'; c.style.top = (pos[i].y - SIZE / 2) + 'px';
      c.style.background = tint(color, 0.16);
      c.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="' + color + '" stroke-width="2" ' +
        'stroke-linecap="round" stroke-linejoin="round">' + (ICONS[(n.icon || 'dot')] || ICONS.dot) + '</svg>';
      diagram.appendChild(c);
      var lab = el('cyc-label'); lab.textContent = n.label; lab.style.width = (SIZE + 64) + 'px';
      diagram.appendChild(lab);
      lab.style.left = (pos[i].x - (SIZE + 64) / 2) + 'px'; lab.style.top = (pos[i].y + SIZE / 2 + 12) + 'px';
    });
    document.body.setAttribute('data-ready', '1');
  }
  function cycArrow(svg, a, b, cx, cy, r){
    var dx = b.x - a.x, dy = b.y - a.y, L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L, gap = r + 18;
    var sx = a.x + ux * gap, sy = a.y + uy * gap, ex = b.x - ux * gap, ey = b.y - uy * gap;
    var mx = (sx + ex) / 2, my = (sy + ey) / 2, ox = mx - cx, oy = my - cy, ol = Math.hypot(ox, oy) || 1, bulge = 30;
    var cpx = mx + ox / ol * bulge, cpy = my + oy / ol * bulge;
    var vx = ex - cpx, vy = ey - cpy, vl = Math.hypot(vx, vy) || 1, u2x = vx / vl, u2y = vy / vl;
    var head = 11, hw = 6, bx = ex - u2x * head, by = ey - u2y * head;
    var path = document.createElementNS(NS, 'path');
    path.setAttribute('d', 'M' + sx + ' ' + sy + ' Q' + cpx + ' ' + cpy + ' ' + bx + ' ' + by);
    path.setAttribute('fill', 'none'); path.setAttribute('stroke', T.edge);
    path.setAttribute('stroke-width', '2.4'); path.setAttribute('stroke-linecap', 'round');
    svg.appendChild(path);
    var nx = -u2y, ny = u2x, tri = document.createElementNS(NS, 'path');
    tri.setAttribute('d', 'M' + ex + ' ' + ey + ' L' + (bx + nx * hw) + ' ' + (by + ny * hw) +
      ' L' + (bx - nx * hw) + ' ' + (by - ny * hw) + ' Z');
    tri.setAttribute('fill', T.edge); svg.appendChild(tri);
  }
});
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--type", default=None, choices=["linear", "tree", "flow", "cycle"])
    ap.add_argument("--data", default="")
    ap.add_argument("--direction", default=None, choices=["LR", "TB"])
    ap.add_argument("--config", default=None, help="full spec JSON: {direction,nodes,edges}")
    ap.add_argument("--out", required=True)
    ap.add_argument("--dagre", default=str(Path(__file__).resolve().parent / "dagre.min.js"))
    ap.add_argument("--logo", default=str(Path(__file__).resolve().parent / "pleasurai-logo.png"))
    ap.add_argument("--scale", type=int, default=2)
    a = ap.parse_args()

    # ---- resolve the spec ----
    if a.config:
        spec = json.loads(Path(a.config).read_text(encoding="utf-8"))
    elif a.type == "linear":
        spec = build_linear(json.loads(a.data), a.direction)
    elif a.type == "tree":
        spec = build_tree(json.loads(a.data), a.direction)
    elif a.type == "cycle":
        spec = build_cycle(json.loads(a.data))
    elif a.type == "flow":
        spec = json.loads(a.data)
    else:
        print(json.dumps({"status": "failed", "reason": "need --type linear|tree|flow or --config"}))
        return 1
    if a.direction:
        spec["direction"] = a.direction
    if not spec.get("nodes"):
        print(json.dumps({"status": "failed", "reason": "no_nodes", "spec": spec}))
        return 1

    dagre_js = Path(a.dagre).read_text(encoding="utf-8")
    try:
        logo_uri = "data:image/png;base64," + base64.b64encode(Path(a.logo).read_bytes()).decode()
        logo_html = '<img src="%s" height="22" alt="Pleasur.ai">' % logo_uri
    except Exception:
        logo_html = '<span style="font-weight:700;color:#B4BAC4">Pleasur.AI</span>'

    css = CSS.replace("__FONT__", FONT).replace("__TFONT__", TITLE_FONT)
    sub = ('<div id="s">%s</div>' % html.escape(a.subtitle)) if a.subtitle else ""
    head = '<!doctype html><html><head><meta charset="utf-8"><style>' + css + "</style></head><body>"
    body = ('<div id="wrap"><div id="card"><div id="t">' + html.escape(a.title) + "</div>"
            + sub + '<div id="diagram"></div><div id="f">' + logo_html + "</div></div></div>")
    scripts = ("<script>" + dagre_js + "</script>"
               + "<script>window.SPEC=" + json.dumps(spec) + ";window.THEME=" + json.dumps(THEME) + ";</script>"
               + "<script>" + JS + "</script>")
    page = head + body + scripts + "</body></html>"

    try:
        from patchright.sync_api import sync_playwright
    except ImportError:
        from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--no-sandbox"])
        pg = b.new_context(viewport={"width": 1500, "height": 1000}, device_scale_factor=a.scale).new_page()
        pg.set_content(page, wait_until="networkidle")
        try:
            pg.wait_for_selector('body[data-ready="1"]', timeout=9000)
        except Exception:
            pass
        pg.wait_for_timeout(450)
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        pg.locator("#wrap").screenshot(path=a.out)
        b.close()
    print(json.dumps({"status": "captured", "path": a.out,
                      "type": spec.get("type", a.type or "flow"), "nodes": len(spec["nodes"])}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
