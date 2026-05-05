# VPS deploy guide

How to run the blog-agent pipeline unattended on a Linux VPS — including the always-on Chrome that powers `/capture-visuals` via the Claude-in-Chrome MCP.

This is the operational counterpart to the editorial docs (`CLAUDE.md`, the skill files). When everything described here is in place, you can `cron` a `/blog-pipeline keyword …` invocation and walk away — research, draft, screenshots, action-shots, and publish-ready package all complete without you at the keyboard.

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│  VPS (Linux, single host)                                        │
│                                                                  │
│  ┌────────────────────────┐     ┌───────────────────────────┐    │
│  │ Xvfb :99               │ ←── │ google-chrome (systemd)   │    │
│  │ (virtual display)      │     │  ├─ logged into claude.ai │    │
│  └────────────────────────┘     │  ├─ logged into pleasur.ai│    │
│                                 │  └─ Claude-in-Chrome ext. │    │
│                                 └───────────────────────────┘    │
│                                            ▲                     │
│                                            │ MCP                 │
│  ┌────────────────────────────────────────┴──────────────────┐   │
│  │ Claude Code (systemd, doppler-wrapped)                    │   │
│  │  ├─ Ahrefs MCP                                            │   │
│  │  ├─ Claude-in-Chrome MCP (drives the Chrome above)        │   │
│  │  └─ /blog-pipeline triggered by cron / RemoteTrigger      │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

Two long-lived processes: **Chrome** (with the extension and your logged-in sessions) and **Claude Code** (the pipeline orchestrator). Both run as systemd units. Chrome stays up so the extension stays connected; Claude Code stays up so cron can fire `/blog-pipeline` at it via stdin.

The same-machine constraint (see `.claude/skills/capture-visuals/SKILL.md`) is what forces this layout: the Chrome MCP's `save_to_disk` writes to the local FS of whichever machine runs Chrome, so Claude Code has to live on the same host or the captured PNGs never reach `content-pipeline/images/{slug}/`.

## Prereqs

- Ubuntu 22.04+ or Debian 12+ VPS (4 GB RAM minimum; 2 vCPU)
- Root or sudo
- A residential/datacenter IP your target sites don't already block
- A Doppler project (`pleasurai`, config `dev`) with at least: `OPENROUTER_API_KEY_BLOG_AGENT`, `REPLICATE_API_TOKEN`, `STRAPI_API_TOKEN` (optional), `STRAPI_BASE_URL` (optional)
- An Anthropic account on a Pro/Max plan (Claude-in-Chrome uses your subscription, no per-token billing)
- Logins you want pre-authenticated: `claude.ai`, `pleasur.ai`, anything else you'll capture from

## 1. System packages

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
  xvfb x11-utils xdotool \
  fonts-liberation fonts-noto-color-emoji \
  libnss3 libxss1 libasound2 libatk-bridge2.0-0 libgtk-3-0 libgbm1 \
  python3 python3-venv python3-pip \
  curl wget git unzip jq \
  ca-certificates gnupg
```

## 2. Google Chrome

```bash
wget -qO- https://dl.google.com/linux/linux_signing_key.pub \
  | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/google-chrome.gpg
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
  | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update && sudo apt install -y google-chrome-stable
```

Chromium works too, but the Claude-in-Chrome extension is distributed via the Chrome Web Store — Google Chrome is the safe default.

## 3. Always-on Chrome under Xvfb (systemd)

Create a dedicated user so Chrome and the pipeline aren't running as root:

```bash
sudo useradd -m -s /bin/bash blogagent
sudo loginctl enable-linger blogagent   # so user-level systemd survives logout
```

Switch to that user (`sudo -iu blogagent`) and create a profile dir:

```bash
mkdir -p ~/chrome-profile ~/.config/systemd/user
```

`~/.config/systemd/user/xvfb.service`:

```ini
[Unit]
Description=Xvfb virtual display :99
After=default.target

[Service]
ExecStart=/usr/bin/Xvfb :99 -screen 0 1920x1080x24 -ac +extension RANDR
Restart=always
RestartSec=2

[Install]
WantedBy=default.target
```

`~/.config/systemd/user/chrome.service`:

```ini
[Unit]
Description=Long-running Chrome with Claude extension
Requires=xvfb.service
After=xvfb.service

[Service]
Environment=DISPLAY=:99
ExecStart=/usr/bin/google-chrome \
  --user-data-dir=%h/chrome-profile \
  --no-first-run \
  --no-default-browser-check \
  --disable-features=Translate,InfinitePrefetch \
  --disable-background-timer-throttling \
  --window-size=1920,1080 \
  --start-maximized
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

Enable and start:

```bash
systemctl --user daemon-reload
systemctl --user enable --now xvfb.service chrome.service
systemctl --user status chrome.service
```

You now have a Chrome process bound to a virtual display. Use `x11vnc` + an SSH tunnel if you ever need to *see* it:

```bash
sudo apt install -y x11vnc
DISPLAY=:99 x11vnc -localhost -nopw -forever -shared -rfbport 5900 &
# from your laptop:
ssh -L 5900:localhost:5900 blogagent@<vps>
# then point a VNC client at localhost:5900
```

You'll need this VNC view for the one-time auth steps (steps 4 and 6). After that, Chrome runs headlessly to humans but is fully visible to the MCP.

## 4. Install + authenticate the Claude-in-Chrome extension (one-time)

VNC into the VPS (per step 3). Then in that Chrome:

1. Visit the [Claude in Chrome](https://chromewebstore.google.com/) Web Store listing and click **Add to Chrome**.
2. Open the extension, sign into `claude.ai` with your Pro/Max account.
3. Toggle the extension on for the tabs/sites it should be allowed to drive (you can scope to specific origins or grant all-site access — for VPS use, all-site is the right default).
4. Confirm in `chrome://extensions/` that the extension is loaded and *enabled in incognito too if you ever use incognito*.

The extension's auth token persists in the Chrome profile (`~/chrome-profile`) — as long as that dir survives, you don't have to re-auth.

Quick sanity check from a Claude Code session:

```
list_connected_browsers
```

You should see your VPS Chrome with `name: "Browser N (Linux, VPS)"` and a `deviceId`. Note the deviceId — RemoteTrigger / cron can pin to it via `select_browser` so the right window gets driven.

## 5. Project bootstrap

Still as `blogagent`:

```bash
cd ~
git clone <your-fork-of-blog-agent> blog-agent
cd blog-agent

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Patchright (used by `/generate-visuals`) is in `requirements.txt`. Install its browsers:

```bash
python -m patchright install chromium
```

## 6. Pleasur.AI session persistence (one-time)

The screenshot side of `/generate-visuals` reuses an authenticated profile under `.claude/skills/generate-visuals/auth/profile/`. Capture it once via the helper:

```bash
cd ~/blog-agent
xvfb-run -s "-screen 0 1920x1080x24" \
  python .claude/skills/generate-visuals/scripts/setup_auth.py
```

This launches a real Chrome via patchright with stealth enabled. Sign into `pleasur.ai`, click through the age gate, then close the browser. Cookies persist on disk.

The Claude-in-Chrome side is independent: that lives in your *long-running* Chrome's `~/chrome-profile` (step 4). Sign into Pleasur once there too, while you're VNC'd in. Both auth stores need to be primed — `/generate-visuals` and `/capture-visuals` use different browsers and different profiles.

**Refresh cadence:** Pleasur sessions seem to last ~30 days. Recapture via the same script when `/generate-visuals` starts producing login-wall captures (the heuristic checks in `templates/visual-types.md` flag this automatically — look for entries downgraded to `manual-capture.md` with `final_url=login`).

## 7. Doppler

Install:

```bash
curl -Ls https://cli.doppler.com/install.sh | sudo sh
```

As `blogagent`:

```bash
doppler login            # interactive, one time
doppler setup            # pick project pleasurai, config dev
doppler secrets          # verify the secrets you expect
```

From here, `doppler run -- <cmd>` injects all configured secrets as env vars.

## 8. Claude Code as a systemd unit

Install Claude Code (per Anthropic's docs) and authenticate as `blogagent`:

```bash
# whatever the current install command is — check claude.ai/code
claude --version
claude login            # interactive once
```

`~/.config/systemd/user/claude-code.service`:

```ini
[Unit]
Description=Claude Code session for blog-agent
After=chrome.service
Requires=chrome.service

[Service]
WorkingDirectory=%h/blog-agent
Environment=DISPLAY=:99
ExecStart=/usr/local/bin/doppler run -- claude --headless --model claude-sonnet-4-6 --resume blog-agent
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

`--headless --resume <name>` keeps a long-lived session you can fire prompts into via RemoteTrigger or a named-pipe shim. Adjust the flag set to whatever your Claude Code build supports — the goal is a process that stays up and accepts new turns.

```bash
systemctl --user daemon-reload
systemctl --user enable --now claude-code.service
journalctl --user -u claude-code.service -f
```

## 9. Cron the pipeline

Two patterns, pick one.

### A. RemoteTrigger (preferred)

If your Claude Code build exposes RemoteTrigger, register a trigger in the running session and `curl` it from cron:

```cron
# /etc/cron.d/blog-pipeline
0 6 * * 1 blogagent curl -sS -X POST -H 'Content-Type: application/json' \
  -d '{"prompt":"/blog-pipeline ai content marketing tools"}' \
  http://127.0.0.1:7878/trigger/blog-run
```

The session runs the slash command, produces stage outputs under `content-pipeline/`, and goes idle until the next cron firing.

### B. Fresh session per run

If you don't want a persistent session, drop the `--resume` and have cron spawn one-shot runs:

```cron
0 6 * * 1 blogagent cd /home/blogagent/blog-agent && \
  doppler run -- claude --headless --model claude-sonnet-4-6 --print '/blog-pipeline ai content marketing tools' \
  >> /home/blogagent/blog-agent/.claude/logs/pipeline.log 2>&1
```

Cheaper on memory; more cold-start latency; loses the in-session prompt cache between runs.

Either way, after the run finishes, `content-pipeline/8-publish/{slug}/` has the Strapi-ready package. If you've configured Strapi creds in Doppler, `/format-for-publish` can publish directly via API — otherwise the package waits for a human to paste it.

**Pin Sonnet 4.6 for Claude-in-Chrome work.** Both unit and one-shot examples above use `--model claude-sonnet-4-6`. Browser driving (`/capture-visuals` and any other Claude-in-Chrome MCP work) is high-throughput, low-reasoning — Sonnet 4.6 is meaningfully faster and cheaper than Opus, and the quality bar for "click the right button, capture the right state" doesn't need Opus's reasoning depth. Don't run the cron daemon on Opus by accident; the model name is part of the systemd unit for a reason.

## 10. Capture-visuals in the unattended flow

`/blog-pipeline` will hit `/generate-visuals` automatically. That handles every `screenshot` placeholder via patchright headless and every `image` placeholder via Replicate. Anything that comes back as `action-shot`, `external`, `video`, `gif`, or a flagged failure goes into `content-pipeline/images/{slug}/manual-capture.md`.

For the unattended setup, a second cron job runs `/capture-visuals {slug}` after the main pipeline:

```cron
30 6 * * 1 blogagent curl -sS -X POST -H 'Content-Type: application/json' \
  -d '{"prompt":"/capture-visuals ai-content-marketing-tools"}' \
  http://127.0.0.1:7878/trigger/blog-run
```

The session reads `manual-capture.md`, drives the always-on Chrome via the MCP for each `action-shot` entry, saves PNGs into `content-pipeline/images/{slug}/`, swaps the placeholders in `6-drafts-cited/{slug}.md`, and re-renders the preview. Items still marked `external` / `video` / `gif` stay in `manual-capture.md` for the next time you sit down at the dashboard.

## 11. Recovery

| Symptom | Cause | Fix |
|---|---|---|
| `list_connected_browsers` returns empty | Chrome crashed; extension lost connection | `systemctl --user restart chrome.service`; the extension reconnects on launch |
| Capture lands on a `claude.ai/login` URL | Anthropic session expired | VNC in, re-login to claude.ai, restart `claude-code.service` |
| `/generate-visuals` keeps producing blank PNGs of `pleasur.ai` | Pleasur session expired | Re-run `setup_auth.py` (step 6); then re-run `/generate-visuals {slug}` |
| Captures look right in MCP previews but no PNGs land in `content-pipeline/images/` | You're driving from a different host than Chrome | Same-machine constraint (see capture-visuals SKILL.md) — must invoke from the VPS, not your laptop |
| Cloudflare challenge on a previously working site | IP reputation degraded, or site upgraded its bot wall | Check `screenshots-failed.md`; consider rotating to a residential proxy via `SCREENSHOT_PROXY` env var |
| Chrome keeps OOMing | 4 GB ceiling hit during large pages | Add swap (2–4 GB), or upsize VPS to 8 GB; avoid `--single-process` (worse memory pressure on long sessions) |
| `claude-code.service` keeps restarting | Auth token expired or stdin closed | `journalctl --user -u claude-code.service -n 100`; usually re-running `claude login` interactively fixes it |

## Hardening checklist

- [ ] Both systemd services running (`systemctl --user list-units --state=running`)
- [ ] `list_connected_browsers` returns the VPS Chrome with a stable deviceId
- [ ] `setup_auth.py` profile created and loads pleasur.ai without the age gate
- [ ] Doppler injects `OPENROUTER_API_KEY_BLOG_AGENT`, `REPLICATE_API_TOKEN`
- [ ] Cron lines visible in `/etc/cron.d/blog-pipeline` (or user crontab)
- [ ] One end-to-end smoke run via `/blog-pipeline test-keyword --context "smoke"` produces `content-pipeline/8-publish/test-keyword/article.md`
- [ ] Logs under `~/blog-agent/.claude/logs/` rotate (add to logrotate if filling disk)

## What's intentionally not automated

- **Brand voice changes.** Edit `brand-config.md` and the `examples/` folder by hand; voice drift is exactly where editorial judgment matters.
- **Per-article context.** Ryan-style content engineering still benefits from a human writing `--context "..."` for each pipeline run. Cron a generic prompt only for genuinely templatable runs.
- **Publishing.** `/format-for-publish` produces a Strapi-ready package and can publish via API if `STRAPI_API_TOKEN` is set, but the human-in-the-loop default is to review the preview and click publish from the dashboard.
- **Visual judgment for `action-shot` entries.** When `/capture-visuals` runs unattended, it captures what `goal=` says. If `goal=` was poorly written upstream in the outline, you'll get a wrong capture. The dashboard is where you spot-check before the post goes live.

## Where to read more

- `.claude/skills/capture-visuals/SKILL.md` — the editorial step that drives Chrome
- `.claude/skills/generate-visuals/SKILL.md` — the static-URL screenshot path (patchright)
- `templates/visual-types.md` — the full visual taxonomy and capture-strategy table
- `CLAUDE.md` — pipeline overview and editorial principles
