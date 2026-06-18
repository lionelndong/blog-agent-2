"""Firecrawl a list of URLs and report benchmark stats (word count, H2s, tables, app/item count).
Usage: FIRECRAWL_API_KEY=... python firecrawl_bench.py <slug> url1 url2 ...
Writes raw markdown to content-pipeline/1-research/_bench/<slug>/<n>.md and prints a summary table.
"""
import json, os, re, sys, urllib.request, pathlib

KEY = os.environ["FIRECRAWL_API_KEY"]
slug = sys.argv[1]
urls = sys.argv[2:]
outdir = pathlib.Path(__file__).resolve().parent.parent / "content-pipeline" / "1-research" / "_bench" / slug
outdir.mkdir(parents=True, exist_ok=True)


def scrape(url):
    body = json.dumps({"url": url, "formats": ["markdown"], "onlyMainContent": True}).encode()
    req = urllib.request.Request(
        "https://api.firecrawl.dev/v1/scrape", data=body,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        raw = urllib.request.urlopen(req, timeout=120).read().decode()
    except Exception as e:
        return None, f"ERROR {e}"
    d = json.loads(raw)
    md = (d.get("data") or {}).get("markdown") or ""
    return md, None


print(f"{'#':>2} {'words':>6} {'h2':>3} {'h3':>3} {'tbl':>3} url")
for i, url in enumerate(urls, 1):
    md, err = scrape(url)
    if err:
        print(f"{i:>2} {'--':>6} {'--':>3} {'--':>3} {'--':>3} {url}  [{err}]")
        continue
    (outdir / f"{i:02d}.md").write_text(md, encoding="utf-8")
    words = len(re.findall(r"\w+", md))
    h2 = len(re.findall(r"^##\s", md, re.M))
    h3 = len(re.findall(r"^###\s", md, re.M))
    tbl = md.count("\n|") and len(re.findall(r"^\|.+\|\s*$", md, re.M))
    print(f"{i:>2} {words:>6} {h2:>3} {h3:>3} {tbl:>3} {url}")
