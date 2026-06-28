#!/usr/bin/env bash
# Launch the autonomous blog-pipeline for pleasur-ai-vs-dondi-ai (PLE-2689).
# No doppler CLI in this env -> fetch secrets via Doppler API and export them,
# then run claude with the repo .mcp.json (Semrush MCP) loaded.
set -uo pipefail

REPO="/paperclip/instances/default/projects/d11fb003-42e2-4b84-8d88-e1242ad09a70/58966819-f893-4728-ad83-5956700fd1c6/_default/blog-engine"
cd "$REPO" || exit 1

LOG="$REPO/.runs/pleasur-ai-vs-dondi-ai.log"
ENVFILE="$REPO/.runs/.dondi.env"

# 1. Pull all secrets as a dotenv file from the Doppler API.
curl -sf -u "$DOPPLER_KEY:" \
  "https://api.doppler.com/v3/configs/config/secrets/download?project=pleasurai&config=dev&format=env" \
  -o "$ENVFILE" || { echo "FATAL: doppler API fetch failed" | tee -a "$LOG"; exit 1; }
chmod 600 "$ENVFILE"

# 2. Export them into this shell.
set -a
# shellcheck disable=SC1090
source "$ENVFILE"
set +a

# 3. Autonomous pipeline flags (board doctrine: publish on gate-pass, no human gate).
export BLOG_AGENT_AUTONOMOUS=1
export UNATTENDED=1
export BLOG_AGENT_AUTO_PUBLISH=1
export BLOG_AGENT_REVISION_BUDGET=5
export BLOG_AGENT_RESEARCH_REVISION_BUDGET=1
export BLOG_AGENT_OUTLINE_REVISION_BUDGET=1
export BLOG_AGENT_VISUALS_REVISION_BUDGET=1

echo "=== launch $(date -u +%FT%TZ) slug=pleasur-ai-vs-dondi-ai ===" >> "$LOG"

# 4. Run the orchestrator. Context file already written to 0-context/.
claude --dangerously-skip-permissions \
  "/blog-pipeline pleasur ai vs dondi ai --context 'Use content-pipeline/0-context/pleasur-ai-vs-dondi-ai.md as the binding claim-discipline brief — read it FIRST and obey every gate-enforced rule. Honest C5 competitor-alternatives comparison. Pleasur.ai is coin-metered (NO flat-rate/no-tokens claim), no two-way video. Acknowledge Dondi.ai #1 straight.com press standing; anchor honest contrast on transparent/calculable metering and the documented r/Chatbots uncensored-claim skepticism (keep uncensored-skepticism SEPARATE from billing).'" \
  >> "$LOG" 2>&1

RC=$?
echo "=== exit rc=$RC $(date -u +%FT%TZ) ===" >> "$LOG"
rm -f "$ENVFILE"
exit $RC
