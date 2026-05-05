# Auto Blog Loop — VPS Operational Runbook

Production-ready operating notes for running `/auto-blog-loop` autonomously on the user's VPS.

## One-time setup

### 1. Doppler env vars

The loop expects these in the project's Doppler config (or exported in cron's environment):

| Var | Purpose | Default |
|---|---|---|
| `BLOG_AGENT_AUTONOMOUS` | Global mode flag | (set per-invocation) |
| `UNATTENDED` | capture-visuals unattended mode | (set per-invocation) |
| `BLOG_AGENT_AUTO_PUBLISH` | format-for-publish auto-publish | (set per-invocation) |
| `BLOG_AGENT_REVISION_BUDGET` | quality-revision retry cap | `2` |
| `BLOG_AGENT_MAX_PER_RUN` | articles per loop invocation | `3` |
| `BLOG_AGENT_REFRESH_AGE_DAYS` | update-mode age threshold | `365` |
| `STRAPI_BASE_URL` | Strapi public base | required for auto-publish |
| `STRAPI_API_TOKEN` | Strapi API token (full access) | required for auto-publish |
| `BLOG_PUBLIC_BASE_URL` | Public blog URL for post-publish check | required (often same as STRAPI_BASE_URL) |
| `OPENROUTER_API_KEY_BLOG_AGENT` | OpenRouter key for /research deep | required for stage 1 |
| `REPLICATE_API_TOKEN` | Replicate for /generate-visuals | required for image visuals |

Sanity-check before first run:
```bash
doppler run -- python -c "import os; [print(k, '=', '***' if 'TOKEN' in k or 'KEY' in k else os.environ.get(k)) for k in ['STRAPI_BASE_URL','STRAPI_API_TOKEN','OPENROUTER_API_KEY_BLOG_AGENT','REPLICATE_API_TOKEN']]"
```

### 2. Ahrefs MCP auth

OAuth flow runs once on first invocation. Approve when prompted. After that, the token persists.

### 3. Chrome + extension (for capture-visuals)

The user's VPS keeps Chrome always-on with the Claude-in-Chrome extension installed and authenticated to claude.ai + the brand's product login (e.g. pleasur.ai). When the loop fires `/capture-visuals`, it drives that Chrome via the MCP. No human at the keyboard required.

If the extension gets logged out (e.g. session expiry), capture-visuals will skip cleanly — the article still publishes, with screenshots reduced to whatever the deterministic Playwright path captured.

### 4. systemd unit (optional, instead of cron)

```ini
# /etc/systemd/system/blog-agent.service
[Unit]
Description=Autonomous blog-agent run (--max 3)
After=network-online.target

[Service]
Type=oneshot
User=ndong
WorkingDirectory=/opt/blog-agent
ExecStart=/usr/local/bin/doppler run -- /usr/local/bin/claude -p "/auto-blog-loop --max 3" --model claude-sonnet-4-6
StandardOutput=append:/var/log/blog-agent.log
StandardError=append:/var/log/blog-agent.log

[Install]
WantedBy=multi-user.target
```

```ini
# /etc/systemd/system/blog-agent.timer
[Unit]
Description=Run blog-agent nightly at 02:00

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now blog-agent.timer
```

### 5. cron alternative

```cron
# /etc/cron.d/blog-agent
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin

# Nightly creation: 3 articles
0 2 * * * ndong cd /opt/blog-agent && doppler run -- claude -p "/auto-blog-loop --max 3" --model claude-sonnet-4-6 >> /var/log/blog-agent.log 2>&1

# Weekly update: 1 stale article
0 4 * * 1 ndong cd /opt/blog-agent && doppler run -- claude -p "/auto-blog-loop --update-mode --max 1" --model claude-sonnet-4-6 >> /var/log/blog-agent.log 2>&1
```

## Inspecting runs

### What ran last night

```bash
tail -50 /var/log/blog-agent.log
tail -10 content-pipeline/audit/auto-blog-log.csv
```

### What's in the queue

```bash
head -10 content-pipeline/0-keywords/keyword-queue.csv
```

Top 10 candidates with priority + verdicts. The selector picks the first not in `8-publish/` or `9-needs-review/`.

### What got quarantined

```bash
ls content-pipeline/9-needs-review/
cat content-pipeline/9-needs-review/<slug>.md
```

Each `.md` has the failure reason + the last good stage. Run `/blog-pipeline <keyword>` manually to reproduce, fix, then `mv content-pipeline/9-needs-review/<slug>.md content-pipeline/audit/resolved-quarantines/` to clear the slug.

### What's in tool-opportunities

```bash
cat content-pipeline/0-keywords/tool-opportunities.csv
```

Tool-led keywords (calculator/checker/generator) the writing pipeline didn't take. Triage offline — these are tool-build opportunities, not blog candidates.

## Calibration checks (monthly)

### BID gate calibration

```bash
cat content-pipeline/0-keywords/cache/bid-calibration.log | tail -20
```

If the BID PASS rate is consistently > 80% or < 20%, tune thresholds per `bid-method.md` "Calibration" section.

### AIO scoring calibration

```bash
cat content-pipeline/0-keywords/cache/aio-calibration.log | tail -20
```

If everything scores 8+ or everything scores 4-, the rubric or the brief needs strengthening per `aio-cannibalization-rubric.md`.

### Redteam KEEP-rate

The auto-blog-loop logs redteam stats per run. If the KEEP rate trends > 80% across runs, the redteam is rubber-stamping — the SKILL has the override built in but you can also manually re-run `/keyword-redteam --regen` with stricter env to reset.

## Emergency stop

To stop the autonomous loop:

```bash
# Stop the timer (systemd)
sudo systemctl stop blog-agent.timer

# OR remove the cron entry
sudo rm /etc/cron.d/blog-agent

# To prevent ongoing runs from publishing:
# In Doppler, unset BLOG_AGENT_AUTO_PUBLISH or rotate STRAPI_API_TOKEN
```

The loop won't crash if Strapi rejects auto-publish — it'll quarantine and continue, so partial damage isn't possible from a token rotation.

## Troubleshooting

### "queue empty, can't refresh"

`/keyword-research-pipeline` failed. Check:
- Semrush MCP auth still valid? (`doppler run -- claude -p "use mcp__semrush__domain-overview with target=pleasur.ai"`)
- Brand Radar quota? (`cat content-pipeline/0-keywords/cache/brand-radar-quota.log`)
- Network: VPS can reach api.ahrefs.com / openrouter.ai / replicate.com?

### "every article gets quarantined"

Probably a structural failure (env var missing, Strapi schema mismatch, etc.) — the same error will appear in every quarantine `.md`. Read one, fix the root cause, restart the timer.

### "loop runs but nothing publishes"

Check `BLOG_AGENT_AUTO_PUBLISH=1` is actually set. The orchestrator brief includes the env vars but the spawned agent inherits the parent's env — if the parent doesn't have it, neither does the agent. Confirm with:

```bash
doppler run -- env | grep BLOG_AGENT
```

### "auto_publish_check fails on every URL"

Probably `BLOG_PUBLIC_BASE_URL` or `--blog-path` mismatch. Default is `<base>/blog/<slug>`. If the brand's URL pattern is different (e.g. `<base>/<slug>` with no `/blog` prefix), pass `--blog-path ""` in the script invocation. Or update the loop's auto_publish_check call.

## Cost monitoring

Per `BLOG_AGENT_MAX_PER_RUN=3`:

| Component | Per article | Per nightly run | Per month |
|---|---|---|---|
| LLM tokens (Opus + Sonnet sub-agents) | ~$1-2 | ~$3-6 | ~$90-180 |
| Replicate (~4 images @ $0.04) | ~$0.16 | ~$0.50 | ~$15 |
| OpenRouter (Perplexity) | ~$0.30 | ~$0.90 | ~$27 |
| Ahrefs (subscription) | included | included | (existing) |

Total: ~$3-9/night, ~$100-220/month for 3 articles/night × 30 nights = 90 articles.

## When to escalate to human

The autonomous loop is intentionally conservative — quarantines accumulate rather than the system silently dying. Escalate to a human if:

- `9-needs-review/` has > 5 entries that share the same `error_reason` (structural issue)
- Strapi inventory grows beyond expected (e.g. duplicates from a slug collision)
- Brand Radar quota is consumed faster than expected (Layer 1c quota churn)
- Quality-check verdicts trend FAIL on the first pass (voice-baseline drift; re-anchor to fresher `examples/`)

The runbook's calibration sections + `cache/*.log` files give you the data; the human applies judgment.
