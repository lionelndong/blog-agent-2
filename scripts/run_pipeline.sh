#!/usr/bin/env bash
# run_pipeline.sh — launch Claude Code with the pipeline's secrets in env.
#
# Since 2026-06-12 the Semrush MCP authenticates with a plain API key
# (`Authorization: Apikey $SEMRUSH_API_KEY`, expanded by .mcp.json) — no OAuth,
# no refresh tokens, no token minting. This wrapper is now just `doppler run`.
#
# Usage:
#   ./scripts/run_pipeline.sh "/keyword-research-pipeline --regen"
#   ./scripts/run_pipeline.sh "/blog-pipeline ai chatbot nsfw --context '...'"
#
# Requires:
#   * doppler CLI on PATH (DOPPLER_TOKEN in env, or interactive login)
#   * SEMRUSH_API_KEY, FIRECRAWL_API_KEY, OPENROUTER_API_KEY_BLOG_AGENT in
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

if ! command -v doppler >/dev/null 2>&1; then
  echo "ERROR: doppler CLI not found on PATH." >&2
  exit 1
fi

exec doppler run --project pleasurai --config dev -- claude --dangerously-skip-permissions "$PROMPT"
