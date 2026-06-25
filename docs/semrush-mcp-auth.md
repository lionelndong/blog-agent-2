# Semrush MCP authentication — current state

## TL;DR

`.mcp.json` sets `Authorization: Apikey ${SEMRUSH_API_KEY}`. Load it from the company Doppler config before running Semrush MCP or classic Semrush API calls:

```bash
DOPPLER_TOKEN="$DOPPLER_KEY" doppler run --project pleasurai --config dev -- <cmd>
```

Do not use the archived OAuth/bootstrap flow for routine runs. The active Paperclip runner already has `DOPPLER_KEY`, and Doppler `pleasurai/dev` includes `SEMRUSH_API_KEY`, `SEMRUSH_API_KEY_BLOG_AGENT`, `SEMRUSH_API_KEY_CONTENTSHAKE`, and `SEMRUSH_MCP_URL`.

## Current auth path

The Semrush MCP server is a single HTTP endpoint at `https://mcp.semrush.com/v1/mcp`.

```json
{
  "mcpServers": {
    "semrush": {
      "type": "http",
      "url": "https://mcp.semrush.com/v1/mcp",
      "headers": { "Authorization": "Apikey ${SEMRUSH_API_KEY}" }
    }
  }
}
```

In a plain heartbeat session where MCP tools are not loaded, call the classic Semrush API under the same Doppler wrapper. The report names and Semrush CSV output are equivalent for pipeline keyword/SERP pulls:

```bash
DOPPLER_TOKEN="$DOPPLER_KEY" doppler run --project pleasurai --config dev -- \
  curl "https://api.semrush.com/?type=phrase_this&key=$SEMRUSH_API_KEY&phrase=ai+girlfriend&database=us"
```

## ⚠️ Provider retired — use Ahrefs instead (2026-06-24)

As of **2026-06-24**, Semrush is **retired** as the primary SEO data provider. The `blog-engine` CLAUDE.md ruling
supersedes all previous Semrush usage. Use the Ahrefs MCP (`https://api.ahrefs.com/mcp/mcp`,
`Bearer ${AHREFS_MCP_KEY}`) for all keyword, SERP, site-explorer, and **site audit** work.

Ahrefs site audit project for pleasur.ai: **`10006863`** (99% health as of 2026-06-24).

```bash
# Ahrefs MCP — Streamable HTTP (NOT the old http+sse protocol)
curl -s -X POST "https://api.ahrefs.com/mcp/mcp" \
  -H "Authorization: Bearer $AHREFS_MCP_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"cto","version":"1"}}}'
```

After init, use the returned `mcp-session-id` header for subsequent calls:
- `site-audit-projects` — list projects and health scores
- `site-audit-issues` — issue type list with crawled counts
- `site-audit-page-explorer` — filtered page list

## API-unit exhaustion (all keys dead as of 2026-06-18)

Semrush API units are account-level. If MCP or classic API calls return:

```text
ERROR 132 :: API UNITS BALANCE IS ZERO
```

All three Doppler keys (`SEMRUSH_API_KEY`, `SEMRUSH_API_KEY_BLOG_AGENT`, `SEMRUSH_API_KEY_CONTENTSHAKE`)
are exhausted simultaneously — they resolve to the same key. Switching between them does not help.

## Browser dashboard broken (SEMRUSH_PASSWORD stale)

As of 2026-06-25, the `SEMRUSH_PASSWORD` in Doppler `pleasurai/dev` is **incorrect** — browser login at
`https://www.semrush.com/login/` returns "Wrong login or password." The previous browser-based workaround
(PLE-2723) no longer works. Ndong must update `SEMRUSH_PASSWORD` in Doppler to use the dashboard.

## Archived OAuth scripts

`scripts/_archive/auth_semrush_mcp.py` and `scripts/_archive/refresh_semrush_mcp_token.py` are retained only as historical fallback material. They are not part of the current routine path.
