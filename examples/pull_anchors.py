#!/usr/bin/env python3
"""Pull voice-anchor articles (CRAFT REFERENCE ONLY) into examples/voice/<persona>/.

Firecrawls each curated URL -> markdown -> saves tagged by content-type. Run on the
VPS via Doppler so FIRECRAWL_API_KEY is present:

    doppler run -- python examples/pull_anchors.py [--force]

Idempotent: skips files that already exist unless --force. These articles are reference
for learning each persona's CRAFT (structure, rhythm, quote/visual placement). The draft
stage must IMITATE THE MOVES and write ORIGINAL content — never reuse this text (duplicate
content tanks SEO and isn't ours). Topic is irrelevant; we extract craft only.
"""
import os, sys, json, time, urllib.request, pathlib

EX = pathlib.Path(__file__).resolve().parent  # examples/

# Curated best-of, tagged by content-type. Chosen for transferable craft (light on niche
# SEO jargon where possible). 5 per persona to start; expand toward 8-10 over time.
ANCHORS = {
    "sloane-avery": [  # Law craft: opinion / data / contrarian
        ("opinion",   "https://ahrefs.com/blog/ai-content-wasnt-good-enough-now-it-is/"),
        ("listicle",  "https://ahrefs.com/blog/seo-trends/"),
        ("explainer", "https://ahrefs.com/blog/what-is-a-good-ctr/"),
        ("guide",     "https://ahrefs.com/blog/my-complete-ai-content-process-for-ahrefs/"),
        ("opinion",   "https://ahrefs.com/blog/how-to-become-a-thought-leader/"),
    ],
    "theo-hart": [  # Hardwick craft: definitive how-to / comprehensive
        ("listicle",   "https://ahrefs.com/blog/seo-tips/"),
        ("explainer",  "https://ahrefs.com/blog/search-intent/"),
        ("checklist",  "https://ahrefs.com/blog/off-page-seo-checklist/"),
        ("case-study", "https://ahrefs.com/blog/related-keywords/"),
        ("opinion",    "https://ahrefs.com/blog/affiliate-marketing-is-dead/"),
    ],
    "mateo-reyes": [  # Si Quan craft: first-person experiment / conversational
        ("case-study", "https://ahrefs.com/blog/quora-marketing/"),
        ("explainer",  "https://ahrefs.com/blog/what-is-an-ai-agent/"),
        ("listicle",   "https://ahrefs.com/blog/marketing-skills/"),
        ("guide",      "https://ahrefs.com/blog/website-content/"),
        ("listicle",   "https://ahrefs.com/blog/seo-statistics/"),
    ],
}

FORCE = "--force" in sys.argv
KEY = os.environ.get("FIRECRAWL_API_KEY")
if not KEY:
    print("ERR: FIRECRAWL_API_KEY not set — run via `doppler run -- python examples/pull_anchors.py`")
    sys.exit(1)


def slug(url: str) -> str:
    return url.rstrip("/").split("/")[-1]


def firecrawl(url: str) -> str | None:
    body = json.dumps({"url": url, "formats": ["markdown"]}).encode()
    req = urllib.request.Request(
        "https://api.firecrawl.dev/v1/scrape", data=body,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.load(r)
    return (d.get("data") or {}).get("markdown") or d.get("markdown")


total = done = 0
for persona, items in ANCHORS.items():
    d = EX / "voice" / persona
    d.mkdir(parents=True, exist_ok=True)
    for typ, url in items:
        total += 1
        out = d / f"{typ}--{slug(url)}.md"
        if out.exists() and not FORCE:
            print("skip", f"{persona}/{out.name}"); done += 1; continue
        try:
            md = firecrawl(url)
            if not md or len(md) < 500:
                print("WARN thin/empty:", url); continue
            header = (
                f"<!-- CRAFT REFERENCE ONLY — anchor for persona '{persona}', type '{typ}'.\n"
                f"     Source: {url}\n"
                f"     Learn the craft (structure, rhythm, quote/visual placement). NEVER reuse this text;\n"
                f"     write ORIGINAL Pleasur.AI content in our register (brand-config.md). -->\n\n"
            )
            out.write_text(header + md, encoding="utf-8")
            print("saved", f"{persona}/{out.name}", f"({len(md)} chars)"); done += 1
            time.sleep(2)
        except Exception as e:
            print("ERR", url, "->", str(e))

print(f"\n{done}/{total} anchors in place")
