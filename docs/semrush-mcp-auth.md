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

## API-unit exhaustion

Semrush API units are account-level. If MCP or classic API calls return:

```text
ERROR 132 :: API UNITS BALANCE IS ZERO
```

or the MCP unit message pointing to `https://www.semrush.com/mcp-access`, treat this as real Semrush API-unit exhaustion after verifying the Doppler names are present. Switching between `SEMRUSH_API_KEY` and `SEMRUSH_API_KEY_BLOG_AGENT` will not help when they resolve to the same key.

## Archived OAuth scripts

`scripts/_archive/auth_semrush_mcp.py` and `scripts/_archive/refresh_semrush_mcp_token.py` are retained only as historical fallback material. They are not part of the current routine path.
