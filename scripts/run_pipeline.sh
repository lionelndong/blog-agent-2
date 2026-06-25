#!/usr/bin/env bash
# run_pipeline.sh — launch Claude Code with the pipeline's secrets in env.
#
# The Ahrefs MCP authenticates with a plain API key
# (`Authorization: Bearer $AHREFS_MCP_KEY`, expanded by .mcp.json) — no OAuth,
# no refresh tokens, no token minting. This wrapper is now just `doppler run`.
#
# Usage:
#   ./scripts/run_pipeline.sh "/keyword-research-pipeline --regen"
#   ./scripts/run_pipeline.sh "/blog-pipeline ai chatbot nsfw --context '...'"
#
# Requires:
#   * doppler CLI on PATH (DOPPLER_TOKEN in env, or interactive login)
#   * AHREFS_MCP_KEY, AHREFS_API_KEY, FIRECRAWL_API_KEY, OPENROUTER_API_KEY_BLOG_AGENT in
#     Doppler project `pleasurai`, config `dev`
#
# Headless-safe: no browser, no prompts, no terminal interaction.

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 \"<claude prompt>\"" >&2
  exit 64
fi
PROMPT="$*"

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Resolve doppler: prefer PATH, fall back to known Paperclip install location.
if command -v doppler >/dev/null 2>&1; then
  DOPPLER_BIN="doppler"
elif [[ -x "/paperclip/.local/bin/doppler" ]]; then
  DOPPLER_BIN="/paperclip/.local/bin/doppler"
else
  echo "ERROR: doppler CLI not found on PATH or at /paperclip/.local/bin/doppler." >&2
  exit 1
fi

# Allow DOPPLER_KEY as a fallback token name (Paperclip runner injects DOPPLER_KEY).
export DOPPLER_TOKEN="${DOPPLER_TOKEN:-${DOPPLER_KEY:-}}"
if [[ -z "$DOPPLER_TOKEN" ]]; then
  echo "ERROR: neither DOPPLER_TOKEN nor DOPPLER_KEY is set." >&2
  exit 1
fi

exec "$DOPPLER_BIN" run --project pleasurai --config dev -- claude --dangerously-skip-permissions "$PROMPT"
