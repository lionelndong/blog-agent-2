"""Generate the SemRush MCP tool inventory by live-calling discovery tools + key schemas."""
import json, os, re, sys, urllib.request

URL = "https://mcp.semrush.com/v1/mcp"
KEY = os.environ["SEMRUSH_API_KEY"]
OUT = os.path.join(os.path.dirname(__file__), "semrush-mcp-tool-inventory.md")

_id = [0]

def rpc(method, params=None):
    _id[0] += 1
    body = {"jsonrpc": "2.0", "id": _id[0], "method": method}
    if params is not None:
        body["params"] = params
    req = urllib.request.Request(
        URL,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Apikey {KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
    )
    raw = urllib.request.urlopen(req, timeout=60).read().decode()
    m = re.search(r"data: (.+)", raw)
    return json.loads(m.group(1) if m else raw)


def tool_text(name, args):
    d = rpc("tools/call", {"name": name, "arguments": args})
    if "error" in d:
        return f"RPC ERROR: {d['error']}"
    content = d.get("result", {}).get("content", [])
    return content[0].get("text", "") if content else "(empty)"


def main():
    tools = rpc("tools/list")["result"]["tools"]
    lines = [
        "# Semrush MCP — live tool inventory (source of truth)",
        "",
        f"Generated against `{URL}` with the paid plan key. **Auth: `Authorization: Apikey $SEMRUSH_API_KEY`** (no OAuth, no session id needed).",
        "Workflow per server instructions: **discovery tool -> get_report_schema(report) -> execute_report**. Default database `us`. Use display_limit 30-50 for exploratory pulls.",
        "",
        "## Tools",
        "",
    ]
    discovery = []
    for t in tools:
        lines.append(f"- **{t['name']}** — {t.get('description','').strip()}")
        if t["name"] not in ("get_report_schema", "execute_report"):
            discovery.append(t["name"])
    lines.append("")

    report_names = []
    for name in discovery:
        print(f"discovery: {name}", file=sys.stderr)
        txt = tool_text(name, {})
        lines.append(f"## Toolkit `{name}` — available reports")
        lines.append("")
        try:
            data = json.loads(txt)
            for r in data.get("reports", []):
                usage = (" Usage: " + r["usage"]) if r.get("usage") else ""
                lines.append(f"- `{r['name']}` ({r.get('price','?')}): {r.get('description','').strip()}{usage}")
                report_names.append((name, r["name"]))
        except Exception:
            lines.append("```")
            lines.append(txt[:3000])
            lines.append("```")
        lines.append("")

    # Schemas for the reports the pipeline leans on hardest
    key_reports = [
        ("keyword_research", "phrase_this"),
        ("keyword_research", "phrase_these"),
        ("keyword_research", "phrase_related"),
        ("keyword_research", "phrase_fullsearch"),
        ("keyword_research", "phrase_questions"),
        ("keyword_research", "phrase_kdi"),
        ("keyword_research", "phrase_organic"),
        ("organic_research", "domain_organic"),
        ("organic_research", "domain_organic_organic"),
        ("organic_research", "domain_domains"),
        ("url_research", "url_organic"),
        ("overview_research", "domain_ranks"),
    ]
    valid = {f"{a}/{b}" for a, b in report_names}
    lines.append("## Key report schemas (parameters)")
    lines.append("")
    for toolkit, report in key_reports:
        if f"{toolkit}/{report}" not in valid:
            lines.append(f"### `{report}` — NOT AVAILABLE in `{toolkit}` on this plan/server")
            lines.append("")
            continue
        print(f"schema: {report}", file=sys.stderr)
        txt = tool_text("get_report_schema", {"toolkit": toolkit, "report": report})
        lines.append(f"### `{report}` (toolkit `{toolkit}`)")
        lines.append("")
        lines.append("```json")
        lines.append(txt[:2600])
        lines.append("```")
        lines.append("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"wrote {OUT} ({len(lines)} lines)", file=sys.stderr)


if __name__ == "__main__":
    main()
