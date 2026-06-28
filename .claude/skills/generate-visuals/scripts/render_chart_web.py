#!/usr/bin/env python3
"""Render premium, ON-BRAND charts with ApexCharts headless in the browser (2026-06-28 v3).

Brand theme: Geist body + IBM Plex Sans title (the blog fonts), brand palette, gradient fills,
rounded bars, donut center-total, light card, and the REAL Pleasur.ai logo composited in.
apexcharts.min.js bundled next to the engine; the `apexcharts` skill supplies configs for all 16 types.

Usage:
  python render_chart_web.py --type bar|bar_h|area|line|donut --title "..." --data '<json>' --out c.png
  python render_chart_web.py --config skill_built.json --title "..." --out c.png   # any of 16 types
"""
import argparse
import base64
import json
import sys
from pathlib import Path

try:
    ROOT = Path(__file__).resolve().parents[4]
except IndexError:
    ROOT = Path.cwd()

PALETTE = ["#2E90FA", "#8B5CF6", "#22B276", "#F5A623", "#E8655A", "#0891B2", "#534AB7"]
FONT = "'Geist', system-ui, -apple-system, Segoe UI, sans-serif"          # blog body font
TITLE_FONT = "'IBM Plex Sans', 'Geist', system-ui, sans-serif"            # blog heading font


def resolve_pairs(spec):
    spec = (spec or "").strip()
    data = None
    if spec.startswith("{") or spec.startswith("["):
        try:
            data = json.loads(spec)
        except json.JSONDecodeError:
            return []
    elif ":" in spec:
        pp, _, kp = spec.partition(":")
        p = ROOT / pp
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                for k in kp.split("."):
                    data = data.get(k) if (k and isinstance(data, dict)) else None
            except Exception:
                data = None
    if isinstance(data, dict):
        return [(str(k), float(v)) for k, v in data.items() if isinstance(v, (int, float)) and not isinstance(v, bool)]
    if isinstance(data, list):
        return [(str(i[0]), float(i[1])) for i in data if isinstance(i, list) and len(i) == 2]
    return []


def opts_js(ctype, labels, values, name):
    L, V, P = json.dumps(labels), json.dumps(values), json.dumps(PALETTE)

    def base(t):
        return ("chart:{type:'%s',height:430,fontFamily:%s,toolbar:{show:false},animations:{enabled:false},background:'transparent'},"
                % (t, json.dumps(FONT)))
    if ctype in ("area", "line"):
        return ("{%s colors:['#2E90FA'],series:[{name:%s,data:%s}],"
                "xaxis:{categories:%s,axisBorder:{show:false},axisTicks:{show:false},labels:{style:{colors:'#7A828F',fontSize:'13px'}}},"
                "yaxis:{labels:{formatter:function(v){return fmt(v);},style:{colors:'#9AA2AE',fontSize:'12px'}}},"
                "stroke:{curve:'smooth',width:3.5,colors:['#2E90FA'],lineCap:'round'},"
                "fill:{type:'gradient',gradient:{shade:'light',type:'vertical',gradientToColors:['#2E90FA'],shadeIntensity:0.2,opacityFrom:0.42,opacityTo:0.02,stops:[0,96]}},"
                "dataLabels:{enabled:false},markers:{size:0,colors:['#2E90FA'],strokeWidth:0,hover:{size:6}},"
                "grid:{borderColor:'#ECEFF4',strokeDashArray:4,xaxis:{lines:{show:false}},padding:{left:8,right:12}},"
                "tooltip:{enabled:false}}" % (base(ctype), json.dumps(name), V, L))
    if ctype == "bar_h":
        return ("{%s colors:%s,series:[{name:%s,data:%s}],"
                "plotOptions:{bar:{horizontal:true,borderRadius:7,borderRadiusApplication:'end',barHeight:'62%%',distributed:true}},"
                "xaxis:{categories:%s,axisBorder:{show:false},axisTicks:{show:false},labels:{show:false}},"
                "yaxis:{labels:{style:{colors:'#1E2430',fontSize:'14px',fontWeight:600}}},"
                "legend:{show:false},dataLabels:{enabled:true,formatter:function(v){return fmt(v);},background:{enabled:false},style:{fontSize:'13px',fontWeight:700,colors:['#fff']}},"
                "grid:{show:false},tooltip:{enabled:false}}" % (base('bar'), P, json.dumps(name), V, L))
    if ctype == "donut":
        return ("{%s colors:%s,series:%s,labels:%s,"
                "plotOptions:{pie:{donut:{size:'68%%',labels:{show:true,"
                "total:{show:true,label:'Total',fontSize:'14px',fontWeight:600,color:'#7A828F',formatter:function(w){return fmt(w.globals.seriesTotals.reduce(function(a,b){return a+b;},0));}},"
                "value:{fontSize:'30px',fontWeight:700,color:'#1E2430',offsetY:6,formatter:function(v){return fmt(v);}}}}}},"
                "dataLabels:{enabled:false},stroke:{width:4,colors:['#fff']},"
                "legend:{position:'right',fontSize:'14px',fontWeight:500,labels:{colors:'#1E2430'},markers:{width:12,height:12,radius:6},itemMargin:{vertical:6}},"
                "tooltip:{enabled:false}}" % (base('donut'), P, V, L))
    return ("{%s colors:%s,series:[{name:%s,data:%s}],"
            "plotOptions:{bar:{borderRadius:9,borderRadiusApplication:'end',columnWidth:'56%%',distributed:true}},"
            "xaxis:{categories:%s,axisBorder:{show:false},axisTicks:{show:false},labels:{style:{colors:'#1E2430',fontSize:'14px',fontWeight:600}}},"
            "yaxis:{show:false},legend:{show:false},"
            "dataLabels:{enabled:true,formatter:function(v){return fmt(v);},offsetY:-24,background:{enabled:false},style:{fontSize:'14px',fontWeight:700,colors:['#1E2430']}},"
            "grid:{show:false},tooltip:{enabled:false}}" % (base('bar'), P, json.dumps(name), V, L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--type", default="bar", choices=["area", "line", "bar", "bar_h", "donut"])
    ap.add_argument("--data", default="")
    ap.add_argument("--name", default="")
    ap.add_argument("--config", default=None, help="full ApexCharts options JSON (from the apexcharts skill)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--apex", default=str(Path(__file__).resolve().parent / "apexcharts.min.js"))
    ap.add_argument("--logo", default=str(Path(__file__).resolve().parent / "pleasurai-logo.png"))
    a = ap.parse_args()

    apex = Path(a.apex).read_text(encoding="utf-8")
    try:
        logo_uri = "data:image/png;base64," + base64.b64encode(Path(a.logo).read_bytes()).decode()
        logo_html = '<img src="%s" height="22" alt="Pleasur.ai">' % logo_uri
    except Exception:
        logo_html = '<span style="font-weight:700;color:#B4BAC4">Pleasur.AI</span>'

    if a.config:
        cfg = Path(a.config).read_text(encoding="utf-8")
        opts_expr = "applyFormatters(deepMerge(THEME, %s))" % cfg
    else:
        pairs = resolve_pairs(a.data)
        if not pairs:
            print(json.dumps({"status": "failed", "reason": "no_numeric_data", "spec": a.data}))
            return 1
        opts_expr = opts_js(a.type, [p[0] for p in pairs], [p[1] for p in pairs], a.name or a.title)

    sub = ('<div id="s">%s</div>' % a.subtitle) if a.subtitle else ""
    theme = ("var PALETTE=%s;var FONT=%s;"
             "function fmt(v){if(v==null)return '';if(typeof v==='string'&&isNaN(parseFloat(v)))return v;var n=+v;if(isNaN(n))return ''+v;var x=Math.abs(n);if(x>=1e6)return (n/1e6).toFixed(1).replace(/\\.0$/,'')+'M';if(x>=1e3)return (n/1e3).toFixed(1).replace(/\\.0$/,'')+'K';return ''+Math.round(n);}"
             "var THEME={chart:{fontFamily:FONT,background:'transparent',toolbar:{show:false},animations:{enabled:false},foreColor:'#7A828F'},"
             "colors:PALETTE,grid:{borderColor:'#ECEFF4',strokeDashArray:4,xaxis:{lines:{show:false}}},"
             "dataLabels:{style:{fontWeight:700,fontSize:'13px'},background:{enabled:false}},"
             "stroke:{curve:'smooth',lineCap:'round',width:3.5},"
             "legend:{fontSize:'14px',fontWeight:500,labels:{colors:'#1E2430'},markers:{width:12,height:12,radius:6},itemMargin:{vertical:6}},"
             "tooltip:{enabled:false},plotOptions:{bar:{borderRadius:8,borderRadiusApplication:'end'}},"
             "xaxis:{axisBorder:{show:false},axisTicks:{show:false},labels:{style:{colors:'#7A828F'}}},"
             "yaxis:{labels:{style:{colors:'#9AA2AE'}}}};"
             "function deepMerge(a,b){var o=Array.isArray(a)?a.slice():Object.assign({},a);if(b==null)return o;for(var k in b){var bv=b[k],av=o[k];o[k]=(bv&&typeof bv==='object'&&!Array.isArray(bv)&&av&&typeof av==='object'&&!Array.isArray(av))?deepMerge(av,bv):bv;}return o;}"
             "function applyFormatters(o){o.dataLabels=o.dataLabels||{};if(o.dataLabels.formatter===undefined)o.dataLabels.formatter=function(v){return fmt(v);};if(o.yaxis&&!Array.isArray(o.yaxis)){o.yaxis.labels=o.yaxis.labels||{};if(o.yaxis.labels.formatter===undefined)o.yaxis.labels.formatter=function(v){return fmt(v);};}try{var rb=o.plotOptions&&o.plotOptions.radialBar&&o.plotOptions.radialBar.dataLabels;if(rb){if(rb.value&&rb.value.formatter===undefined)rb.value.formatter=function(v){return Math.round(v)+'%%';};if(rb.total&&rb.total.formatter===undefined)rb.total.formatter=function(w){var s=w.globals.seriesTotals||w.globals.series||[];var sum=0,k=0;for(var i=0;i<s.length;i++){sum+=(+s[i]||0);k++;}return k?Math.round(sum/k)+'%%':'';};}}catch(e){}return o;}"
             ) % (json.dumps(PALETTE), json.dumps(FONT))
    html = """<!doctype html><html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=IBM+Plex+Sans:wght@600;700&display=swap');
*{box-sizing:border-box} body{margin:0;font-family:%s}
#wrap{display:inline-block;padding:46px;background:#F7F8FA}
#card{width:980px;background:#fff;border:1px solid #EDF0F4;border-radius:20px;padding:28px 32px 16px;box-shadow:0 14px 46px rgba(20,30,50,0.08)}
#t{font-family:%s;font-size:23px;font-weight:700;color:#1E2430;letter-spacing:-0.2px}
#s{font-size:14px;color:#7A828F;margin:4px 0 2px}
#f{text-align:right;margin-top:8px;opacity:.92}
#f img{vertical-align:middle}
</style></head><body>
<div id="wrap"><div id="card"><div id="t">%s</div>%s<div id="chart"></div><div id="f">%s</div></div></div>
<script>%s</script>
<script>%s
new ApexCharts(document.querySelector('#chart'), %s).render();
</script></body></html>""" % (FONT, TITLE_FONT, a.title, sub, logo_html, apex, theme, opts_expr)

    try:
        from patchright.sync_api import sync_playwright
    except ImportError:
        from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--no-sandbox"])
        pg = b.new_context(viewport={"width": 1200, "height": 760}, device_scale_factor=2).new_page()
        pg.set_content(html, wait_until="networkidle")
        try:
            pg.wait_for_selector("#chart svg", timeout=8000)
        except Exception:
            pass
        pg.wait_for_timeout(800)
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        pg.locator("#wrap").screenshot(path=a.out)
        b.close()
    print(json.dumps({"status": "captured", "path": a.out, "mode": "config" if a.config else a.type}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
