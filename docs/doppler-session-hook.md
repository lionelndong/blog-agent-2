# Doppler SessionStart hook

## What it does

Every time Claude Code on the web starts a session in this repo, the
`.claude/hooks/session-start.sh` hook:

1. Reads `DOPPLER_TOKEN` from the workspace env (set as a Claude Code on the web
   workspace secret — see below).
2. Installs the Doppler CLI if it's not already present in the runner.
3. Runs `doppler secrets download --no-file --format env` and appends every
   `export KEY=VALUE` line to `$CLAUDE_ENV_FILE`.

The harness sources `$CLAUDE_ENV_FILE` before each subsequent tool call, so all
the keys land in the env that `Bash`, `python`, MCP servers, etc. see —
`SEMRUSH_API_KEY_BLOG_AGENT`, `OPENROUTER_API_KEY_BLOG_AGENT`,
`REPLICATE_API_TOKEN`, `STRAPI_BASE_URL`, `STRAPI_API_TOKEN`,
`BROWSER_USE_API_KEY`, `GITHUB_TOKEN`, plus anything else you've put in the
Doppler project.

## One-time setup

### 1. Generate a Doppler service token

In Doppler:

1. Open the project that holds the blog-agent secrets.
2. Pick the config you want sessions to read from (typically `dev` or `prd`).
3. **Access → Service Tokens → Generate**. Read-only is enough.
4. Copy the token value (`dp.st....`).

### 2. Set it as a Claude Code on the web workspace secret

In Claude Code on the web:

1. Open the workspace settings for this repo.
2. Find the **Secrets** / **Environment Variables** section.
3. Add a secret named `DOPPLER_TOKEN` with the value from step 1.
4. Save. Future sessions in this workspace will see `DOPPLER_TOKEN` in env at
   the moment the SessionStart hook runs.

That's it — no other vars need to be set as workspace secrets. The hook pulls
them all through Doppler.

## Local development

Locally you should keep using `doppler run -- claude` (or your existing setup).
The hook explicitly bails out when `CLAUDE_CODE_REMOTE != true` so it never
clobbers a shell that already has secrets loaded.

## Troubleshooting

The hook is fail-soft: any error (missing token, install failure, network
problem) logs a one-line message to stderr and exits 0 so the session still
starts. To diagnose, look for the `[session-start]` lines in the session
transcript:

| Log line | Meaning | Fix |
|---|---|---|
| `skipping (not a remote session)` | Running outside Claude Code on the web | Expected. Use `doppler run -- claude` locally. |
| `CLAUDE_ENV_FILE not set` | Harness didn't expose the env-file path | File a bug report; this hook can't function without it. |
| `DOPPLER_TOKEN not set` | Workspace secret missing | Set `DOPPLER_TOKEN` per the One-time setup section above. |
| `installing Doppler CLI...` then `Doppler CLI install failed` | Network or permission | Check the runner has outbound HTTPS to `cli.doppler.com`. |
| `doppler secrets download failed` | Token invalid or scoped wrong | Regenerate the service token; confirm it points at the right project + config. |
| `doppler returned no secrets` | Empty config | Add the keys to the Doppler config. |
| `loaded N Doppler secrets into session env` | Success | Nothing — pipeline scripts will see the keys. |

## What the hook does NOT do

- It does NOT set up the Semrush MCP. That's a separate workspace-level MCP
  config (`.mcp.json` declares the server; the workspace owner approves the
  OAuth flow once on first connect). The hook only loads env-var-style API
  keys.
- It does NOT install Python / Node / Playwright deps. `requirements.txt`
  install + `python -m playwright install chromium` should be a separate step
  (either in the hook later or in a dev container build).

## Switching to async mode (optional)

The hook runs synchronously by default — sessions wait for it to finish before
the agent starts. For routine cron-style runs the few extra seconds don't
matter, and we get the guarantee that secrets are available before the first
tool call. If you want faster session boot, change line 1 of the hook body to:

```bash
echo '{"async": true, "asyncTimeout": 300000}'
```

Trade-off: the agent may try to run a Semrush call before the hook has
finished writing `$CLAUDE_ENV_FILE`, leading to a confusing transient
"missing key" failure on the first tool call. Not worth it for this pipeline.
