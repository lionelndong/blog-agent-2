"""Generic Semrush MCP caller. Usage:
  SEMRUSH_API_KEY=... python semrush_call.py <toolkit> <report> 'k=v' 'k2=v2' ...
  SEMRUSH_API_KEY=... python semrush_call.py --schema <toolkit> <report>
  SEMRUSH_API_KEY=... python semrush_call.py --discover <toolkit>
Params parsed as key=value; display_limit cast to int.
"""
import json, os, re, sys, urllib.request

URL = os.environ.get("SEMRUSH_MCP_URL", "https://mcp.semrush.com/v1/mcp")
KEY = os.environ["SEMRUSH_API_KEY"]
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
    raw = urllib.request.urlopen(req, timeout=90).read().decode()
    m = re.search(r"data: (.+)", raw)
    return json.loads(m.group(1) if m else raw)


def tool_text(name, args):
    d = rpc("tools/call", {"name": name, "arguments": args})
    if "error" in d:
        return f"RPC ERROR: {json.dumps(d['error'])}"
    content = d.get("result", {}).get("content", [])
    return content[0].get("text", "") if content else "(empty)"


def main():
    a = sys.argv[1:]
    if a and a[0] == "--discover":
        print(tool_text(a[1], {}))
        return
    if a and a[0] == "--schema":
        print(tool_text("get_report_schema", {"toolkit": a[1], "report": a[2]}))
        return
    toolkit, report = a[0], a[1]
    params = {"database": "us"}
    for kv in a[2:]:
        k, v = kv.split("=", 1)
        if k in ("display_limit",):
            v = int(v)
        params[k] = v
    print(tool_text("execute_report", {"toolkit": toolkit, "report": report, "params": params}))


if __name__ == "__main__":
    main()
