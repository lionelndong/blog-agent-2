# Autonomous Semrush MCP authentication

The Power-1 MCP server at `https://mcp.semrush.com/v1/mcp` requires OAuth.
By default Claude Code's MCP client triggers an interactive consent flow with
a `redirect_uri=http://localhost:56340/callback` — that listener lives inside
the running `claude` process and dies when the headless `claude --print`
process exits, so consent **cannot complete** from a Paperclip headless
heartbeat.

This repo provides a one-time human-in-the-loop bootstrap that converts the
interactive consent into a long-lived refresh token stored in Doppler. After
that, every headless run mints a fresh access token via `refresh_token` grant
— no browser, no prompts.

## One-time bootstrap (Neo's workstation, ~2 minutes)

Pre-reqs:

* Python 3.9+
* `doppler` CLI authenticated to project `pleasurai`, config `dev`
* A browser open on the same machine

```bash
cd blog-agent-2
git pull --ff-only origin main          # to pick up these scripts
python3 scripts/auth_semrush_mcp.py --write-doppler
```

What happens:

1. The script generates a PKCE pair and opens
   `https://api.semrush.com/apis/v4/auth/v0/oauth2/auth?...&scope=mcp.access+offline_access`
   in your default browser.
2. You sign into Semrush and click **Approve**.
3. The browser is redirected to `http://localhost:56340/callback?code=...`.
   The script's local listener captures the code, exchanges it for tokens,
   and (with `--write-doppler`) writes the refresh token to Doppler as
   `SEMRUSH_MCP_REFRESH_TOKEN` in `pleasurai/dev`.
4. Token confirmation lands in the terminal.

If `--write-doppler` is not used (or the CLI isn't on PATH), the script prints
the exact `doppler secrets set …` command to copy-paste.

## Headless runs (Paperclip / cron / unattended)

The wrapper `scripts/run_pipeline.sh` mints a fresh access token each
invocation and exports it as `SEMRUSH_MCP_ACCESS_TOKEN`. The `.mcp.json`
substitutes that env var into the `Authorization: Bearer` header for the
Semrush MCP HTTP server, so Claude Code's MCP client connects without
re-prompting.

```bash
./scripts/run_pipeline.sh "/keyword-research-pipeline --regen"
./scripts/run_pipeline.sh "/blog-pipeline ai chatbot nsfw --context '...'"
```

Internally:

```text
doppler run --project pleasurai --config dev \
  -- python3 scripts/refresh_semrush_mcp_token.py --rotate
        ^ reads SEMRUSH_MCP_REFRESH_TOKEN, mints access_token, prints it,
          writes back any rotated refresh_token to Doppler

doppler run --project pleasurai --config dev \
  -- env SEMRUSH_MCP_ACCESS_TOKEN=<the access token> \
     claude --print --dangerously-skip-permissions ... "<prompt>"
        ^ Claude Code's MCP HTTP client picks up the token from .mcp.json
```

Access tokens are short-lived (the Semrush IdP returns `expires_in` ~1 h);
`run_pipeline.sh` mints a new one for every invocation, so token age never
exceeds the lifetime of a single pipeline run.

## Refresh-token rotation

Some IdP deployments rotate the refresh token on every grant. The
`--rotate` flag on `refresh_semrush_mcp_token.py` writes any new refresh
token back to Doppler so subsequent runs use the latest. Without rotation
support enabled, the bootstrap token would eventually expire — currently
unknown whether Semrush rotates; rotation handling is enabled by default.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `SEMRUSH_MCP_REFRESH_TOKEN is not set` | bootstrap never ran, or Doppler config doesn't have the secret | re-run `auth_semrush_mcp.py --write-doppler` |
| token endpoint HTTP 400 / `invalid_grant` | refresh token expired or revoked | re-run the bootstrap; consider whether the Semrush console revoked the OAuth app |
| MCP tools still 401 after wrapper | scope missing | confirm the auth URL had `scope=mcp.access offline_access`; the bootstrap script enforces both |
| `doppler` CLI missing on the headless host | runtime image hasn't been baked yet | install per the snippet at the top of `run_pipeline.sh` (or apt-style install on a managed host) |

## Threat model

* **Refresh token in Doppler**: lives only in Doppler; no copy on disk in this
  repo. Any agent that wants it must hold a Doppler service token. CTO/CMO
  control rotation.
* **Access token in process env**: lifetime equals one `claude --print`
  invocation. Not written to disk, not echoed in logs by either script.
* **PKCE**: prevents auth-code interception even if a third party reads the
  redirect URL out of browser history.
* **Public client**: per the Semrush IdP metadata
  (`token_endpoint_auth_methods_supported: ["none"]`) — there is no client
  secret to leak.
