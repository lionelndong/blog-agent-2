# Semrush MCP authentication — current state

## TL;DR

`.mcp.json` does **not** set an `Authorization` header. On first use, Claude Code triggers the Semrush OAuth flow itself, completes consent in a browser, and persists the tokens under `/paperclip/.claude/` for all future headless runs.

This works because the SEO agent (the only agent that calls Semrush MCP) runs with `chrome: true` and the `agent-browser` skill, so it can drive the consent screen autonomously.

## Why two paths exist

`scripts/auth_semrush_mcp.py`, `scripts/refresh_semrush_mcp_token.py`, and `scripts/run_pipeline.sh` implement a fully **headless** PKCE bootstrap that stores a refresh token in Doppler. They are kept for the day a Paperclip routine without browser capability needs Semrush MCP, but they require **write access to Doppler `pleasurai/dev`**, which the current agent service token does not have.

When Neo rotates the Doppler token to one with write scope, switch `.mcp.json` back to:

```json
{
  "mcpServers": {
    "semrush": {
      "type": "http",
      "url": "https://mcp.semrush.com/v1/mcp",
      "headers": { "Authorization": "Bearer ${SEMRUSH_MCP_ACCESS_TOKEN}" }
    }
  }
}
```

…and use `scripts/run_pipeline.sh` as the entrypoint instead of bare `claude`.

## Recovery: if OAuth gets revoked or the token cache wipes

1. Make sure the SEO agent (or any chrome-enabled agent) is the one running.
2. Trigger any Semrush MCP call. Claude Code will pop a Semrush authorize URL in chrome.
3. The agent uses agent-browser to log in (creds: `SEMRUSH_USERNAME` / `SEMRUSH_PASSWORD` from Doppler) and click "Authorize".
4. Claude captures the redirect, persists tokens, the original MCP call resumes.
5. Subsequent headless runs reuse the cached tokens.

If chrome is not available on the runtime, fall back to running `scripts/auth_semrush_mcp.py` from a laptop with a browser.
