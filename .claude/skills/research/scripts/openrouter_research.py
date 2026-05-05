#!/usr/bin/env python3
"""Deep web research via OpenRouter — Perplexity default, OpenAI o4-mini fallback.

Reads OPENROUTER_API_KEY_BLOG_AGENT from env (load via Doppler).

Usage:
    doppler run -- python .claude/skills/research/scripts/openrouter_research.py \\
        --keyword "ai girlfriend" --slug ai-girlfriend

    # Override default model (rarely needed):
    doppler run -- python ... --keyword "..." --slug "..." \\
        --model "perplexity/sonar-deep-research"
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = ROOT / "content-pipeline" / "1-research"
BRAND_CONFIG = ROOT / "brand-config.md"

API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "perplexity/sonar-reasoning-pro"
FALLBACK_MODEL = "openai/o4-mini"
TIMEOUT_SECONDS = 120

# Rough cost estimates (USD per 1M tokens). Used for visibility, not enforcement.
COST_TABLE = {
    "perplexity/sonar-reasoning-pro": (1.0, 5.0),     # input, output
    "perplexity/sonar-pro": (3.0, 15.0),
    "perplexity/sonar-deep-research": (2.0, 8.0),
    "perplexity/sonar": (1.0, 1.0),
    "openai/o4-mini": (1.10, 4.40),
}


def read_brand_summary() -> str:
    """Pull just the Brand + Voice + Target Reader summary so the prompt isn't bloated."""
    if not BRAND_CONFIG.exists():
        return "(no brand-config.md found)"
    text = BRAND_CONFIG.read_text(encoding="utf-8")
    # Take everything up to the Forbidden phrases section to keep the prompt tight
    cutoff = text.find("## Forbidden phrases")
    return text[:cutoff].strip() if cutoff > 0 else text[:3000]


def build_prompt(keyword: str, brand_summary: str) -> tuple[str, str]:
    system = (
        "You are a research librarian compiling a sourced briefing for an editorial team. "
        "Your job is search-and-cite: find what credible public sources have said about a "
        "topic, summarize each finding in 1–2 sentences, and link the source. You never "
        "fabricate quotes or sources. You never need to take a position on the topic; you "
        "only report what others have said. If a particular section makes you uncomfortable, "
        "leave that section empty with a brief note — but do NOT refuse the whole task. "
        "Other sections likely have findable, citable material."
    )
    user = f"""# Research briefing request

## Editorial context
{brand_summary}

## Topic
The editorial team is preparing an article that will discuss the keyword: **{keyword}**.

This is for an established commercial publisher. Ahrefs has already provided keyword volume / SERP / top-page metadata separately. Your job is to add what Ahrefs cannot: discourse, sourced facts, and recent events.

## What to compile

For each section below, return what you can find in credible public sources (news outlets, academic papers, industry reports, named-author blogs, government/regulatory pages, official platform announcements). Cite every claim with a real URL. If a section has no good source material, leave it empty with a one-line note — don't pad and don't refuse.

1. **Recent developments (last 12 months)** — news events, product launches, regulatory changes, public controversies, dated stats. This is the most important section; lean here. Each entry: 1–2 sentences + source URL.

2. **Sourced facts and figures** — named studies, industry reports, government data, peer-reviewed papers, dated benchmarks. Anything an editor can fact-check. Each entry: the number/finding + source URL.

3. **Public discourse signals** — what credible public sources are saying about the topic. News articles, opinion pieces from named authors at established outlets, industry analyst pieces. NOT anonymous forum posts. Each entry: source's framing + URL.

4. **Regulatory / legal context** — relevant laws passed, agencies involved, court cases, public regulatory positions. Each entry: 1-line summary + source URL (prefer .gov, .eu, court documents, official regulator press releases).

5. **Coverage gaps in mainstream reporting** — based on what you found, what angles or facts seem under-covered or missing from the dominant narrative? 2–3 specific gaps with rationale.

## Output format

Return clean markdown, 600–1500 words, with these sections:

```
# Deep research: {keyword}

## Recent developments
(events from the last 12 months; each entry 1–2 sentences + source URL)

## Sourced facts and figures
(named studies / reports / benchmarks; each entry: finding + source URL)

## Public discourse signals
(what named-author sources at credible outlets are saying; each entry: framing + source URL)

## Regulatory / legal context
(laws, agencies, court cases; each entry: 1-line summary + source URL)

## Coverage gaps
(2–3 angles that mainstream coverage under-addresses; each with rationale)
```

## Rules
- Every claim needs a real, verifiable URL. Don't fabricate. If a sentence has no source, drop the sentence.
- Prefer primary sources (the original report, official announcement, court filing) over secondary citations.
- It is fine — and often correct — to leave a section sparse or empty if good sources don't exist for it. Honesty over padding.
- Don't pitch any brand. Don't take editorial positions. Just report what credible sources have said, with links.
- If the topic is sensitive, that doesn't change your job: name credible sources, link them, summarize what they say. You are not endorsing them; you are reporting them. Sections you genuinely can't fill, mark `(no public sources found)` and move on.
"""
    return system, user


REFUSAL_MARKERS = (
    "I cannot",
    "I can't",
    "I'm sorry",
    "I am sorry",
    "I am not able",
    "I'm not able",
    "I won't",
    "I will not",
    "unable to provide",
    "decline to",
    "this request",
)


def looks_shallow_or_refusing(content: str, citations: list[str] | None = None) -> tuple[bool, str]:
    """Detect responses that are technically non-empty but materially useless.

    Returns (is_shallow, reason). Tuned against real Perplexity refusal patterns:
    a 1.4K-char polite-decline body slipped past the original 1200-char threshold,
    so we raised the bar and added a citation-count signal (Perplexity returns 0
    citations only when it refused to actually search).
    """
    text = content.strip()
    if len(text) < 400:
        return True, f"response_too_short:{len(text)}_chars"
    lowered = text.lower()
    refusal_hits = [m for m in REFUSAL_MARKERS if m.lower() in lowered]
    # Refusal markers in anything under ~2K chars is a strong shallow signal
    if refusal_hits and len(text) < 2000:
        return True, f"refusal_markers_in_short_response:{','.join(refusal_hits[:3])}"
    # Perplexity should always return citations on a real answer; 0 + short = shallow
    if citations is not None and len(citations) == 0 and len(text) < 3000:
        return True, f"zero_citations_short_body:{len(text)}_chars"
    return False, ""


def call_openrouter(model: str, system: str, user: str, api_key: str) -> dict:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.3,
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://pleasur.ai",
            "X-Title": "Pleasur AI Blog Pipeline",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body)


def extract_content_and_citations(response: dict) -> tuple[str, list[str]]:
    content = ""
    citations: list[str] = []
    try:
        choice = response["choices"][0]
        msg = choice["message"]
        content = msg.get("content", "") or ""
        # Perplexity returns citations on the message AND/OR at top level
        for source in (msg.get("citations"), response.get("citations")):
            if isinstance(source, list):
                for c in source:
                    if isinstance(c, str) and c not in citations:
                        citations.append(c)
                    elif isinstance(c, dict):
                        url = c.get("url") or c.get("source")
                        if url and url not in citations:
                            citations.append(url)
    except (KeyError, IndexError, TypeError) as e:
        print(f"warning: could not parse response shape: {e}", file=sys.stderr)
    return content, citations


def estimate_cost(model: str, response: dict) -> float | None:
    rates = COST_TABLE.get(model)
    if not rates:
        return None
    usage = response.get("usage", {})
    in_tok = usage.get("prompt_tokens") or 0
    out_tok = usage.get("completion_tokens") or 0
    in_cost = (in_tok / 1_000_000) * rates[0]
    out_cost = (out_tok / 1_000_000) * rates[1]
    return round(in_cost + out_cost, 4)


def try_model(model: str, system: str, user: str, api_key: str) -> tuple[str, list[str], float | None, dict]:
    print(f"calling {model}...", file=sys.stderr)
    t0 = time.time()
    response = call_openrouter(model, system, user, api_key)
    elapsed = time.time() - t0
    content, citations = extract_content_and_citations(response)
    cost = estimate_cost(model, response)
    cost_str = f"${cost}" if cost is not None else "unknown"
    print(f"  done in {elapsed:.1f}s — {len(content)} chars, {len(citations)} citations, ~{cost_str}", file=sys.stderr)
    return content, citations, cost, response


def write_output(slug: str, model_used: str, content: str, citations: list[str], cost: float | None, fallback_used: bool) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{slug}-deep.md"
    header = f"""<!--
Generated by openrouter_research.py
Model: {model_used}
Fallback used: {fallback_used}
Estimated cost: ${cost if cost is not None else 'unknown'}
-->

"""
    citations_block = ""
    if citations:
        citations_block = "\n\n## All citations from this research run\n\n" + "\n".join(f"- {url}" for url in citations) + "\n"
    out_path.write_text(header + content.strip() + citations_block, encoding="utf-8")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keyword", required=True, help="The target keyword to research")
    parser.add_argument("--slug", required=True, help="The filesystem-safe slug for output")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"OpenRouter model id (default: {DEFAULT_MODEL})")
    parser.add_argument("--no-fallback", action="store_true", help="Disable o4-mini fallback")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY_BLOG_AGENT")
    if not api_key:
        sys.exit("error: OPENROUTER_API_KEY_BLOG_AGENT not set. Run via `doppler run -- ...` or export the env var.")

    brand_summary = read_brand_summary()
    system, user = build_prompt(args.keyword, brand_summary)

    primary_model = args.model
    fallback_model = None if args.no_fallback else FALLBACK_MODEL

    try:
        content, citations, cost, _ = try_model(primary_model, system, user, api_key)
        if not content.strip():
            raise ValueError("empty response from primary model")
        shallow, why = looks_shallow_or_refusing(content, citations)
        if shallow:
            raise ValueError(f"primary returned shallow/refusing content: {why}")
        out_path = write_output(args.slug, primary_model, content, citations, cost, fallback_used=False)
        print(str(out_path))
        return
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, ValueError, TimeoutError) as primary_err:
        print(f"primary ({primary_model}) failed: {primary_err}", file=sys.stderr)
        if not fallback_model:
            sys.exit(f"error: primary failed and --no-fallback is set")

    try:
        print(f"falling back to {fallback_model}...", file=sys.stderr)
        content, citations, cost, _ = try_model(fallback_model, system, user, api_key)
        if not content.strip():
            sys.exit("error: fallback also returned empty content")
        out_path = write_output(args.slug, fallback_model, content, citations, cost, fallback_used=True)
        print(str(out_path))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, ValueError, TimeoutError) as fallback_err:
        sys.exit(f"error: fallback ({fallback_model}) also failed: {fallback_err}")


if __name__ == "__main__":
    main()
