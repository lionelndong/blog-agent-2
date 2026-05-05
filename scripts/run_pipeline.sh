#!/usr/bin/env bash
# run_pipeline.sh — wrapper that mints a fresh Semrush MCP access token from
# the refresh token in Doppler and launches `doppler run -- claude` with the
# token exported. The .mcp.json picks it up via `Authorization: Bearer
# ${SEMRUSH_MCP_ACCESS_TOKEN}` header substitution.
#
# Usage:
#   ./scripts/run_pipeline.sh "/keyword-research-pipeline --regen"
#   ./scripts/run_pipeline.sh "/blog-pipeline ai chatbot nsfw --context '...'"
#
# Requires:
#   * doppler CLI on PATH (DOPPLER_TOKEN must be in env, or interactive login)
#   * SEMRUSH_MCP_REFRESH_TOKEN in Doppler `pleasurai/dev` (one-time bootstrap
#     via `python3 scripts/auth_semrush_mcp.py`)
#   * python3 on PATH
#
# Headless-safe: no browser, no prompts, no terminal interaction. Exits non-zero
# with a clear message if the refresh token is missing or expired.

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 \"<claude prompt>\"" >&2
  exit 64
fi
PROMPT="$*"

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if ! command -v doppler >/dev/null 2>&1; then
  echo "ERROR: doppler CLI not found on PATH." >&2
  echo "       Install with: curl -Ls https://github.com/DopplerHQ/cli/releases/latest/download/doppler_3.76.0_linux_amd64.tar.gz | tar -xz -C ~/.local/bin/" >&2
  exit 1
fi

# Mint a fresh access token. Run inside `doppler run` so the refresh token
# from Doppler is in env. The token endpoint call is < 1s.
echo "[run_pipeline.sh] minting fresh Semrush MCP access token…" >&2
ACCESS=$(doppler run --project pleasurai --config dev -- python3 scripts/refresh_semrush_mcp_token.py --rotate)
if [[ -z "$ACCESS" ]]; then
  echo "ERROR: refresh_semrush_mcp_token.py returned empty access token." >&2
  exit 2
fi
echo "[run_pipeline.sh] access token minted (length ${#ACCESS})" >&2

# Now launch claude with the access token in env. The .mcp.json substitutes
# ${SEMRUSH_MCP_ACCESS_TOKEN} into the Authorization header.
exec doppler run --project pleasurai --config dev -- env SEMRUSH_MCP_ACCESS_TOKEN="$ACCESS" \
  claude --print --dangerously-skip-permissions --permission-mode bypassPermissions \
  --output-format text "$PROMPT"
