#!/usr/bin/env bash
# sync_captures_from_vps.sh <slug>
#
# Pulls the captured PNGs from the VPS back to the local project filesystem,
# swaps any remaining [VISUAL:type=action-shot;...] placeholders in the cited
# draft for ![alt](images/...) markdown, re-renders the preview, and rebuilds
# the publish package. One-shot finish for the cross-machine capture flow.
#
# Why this exists: when /capture-visuals runs from a host other than the VPS
# (e.g. a developer laptop), Chrome's MCP save_to_disk lands the PNGs on the
# VPS filesystem, not locally. This script closes the gap.
#
# Configuration: set BLOG_AGENT_VPS_HOST and BLOG_AGENT_VPS_PATH as env vars
# (or in ~/.blog-agent.env). Defaults assume Doppler-managed values exist.

set -euo pipefail

SLUG="${1:-}"
if [ -z "$SLUG" ]; then
  echo "usage: $0 <slug>" >&2
  exit 1
fi

# Resolve config — env vars first, then optional ~/.blog-agent.env, then doppler
if [ -z "${BLOG_AGENT_VPS_HOST:-}" ] && [ -f "$HOME/.blog-agent.env" ]; then
  # shellcheck source=/dev/null
  source "$HOME/.blog-agent.env"
fi
if [ -z "${BLOG_AGENT_VPS_HOST:-}" ] && command -v doppler >/dev/null 2>&1; then
  BLOG_AGENT_VPS_HOST="$(doppler secrets get BLOG_AGENT_VPS_HOST --plain 2>/dev/null || true)"
  BLOG_AGENT_VPS_PATH="$(doppler secrets get BLOG_AGENT_VPS_PATH --plain 2>/dev/null || true)"
fi

VPS_HOST="${BLOG_AGENT_VPS_HOST:-blogagent@vps}"
VPS_PATH="${BLOG_AGENT_VPS_PATH:-/home/blogagent/blog-agent}"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOCAL_DIR="$ROOT/content-pipeline/images/$SLUG"
REMOTE_DIR="$VPS_PATH/content-pipeline/images/$SLUG"

mkdir -p "$LOCAL_DIR"

echo "==> rsync $VPS_HOST:$REMOTE_DIR/  ->  $LOCAL_DIR/"
rsync -av --include='*.png' --include='*.jpg' --include='*.jpeg' --include='*.webp' \
  --exclude='*' \
  "$VPS_HOST:$REMOTE_DIR/" "$LOCAL_DIR/"

echo "==> Local PNGs after sync:"
ls -lh "$LOCAL_DIR"/*.png 2>/dev/null || echo "(none yet)"

echo "==> Resolving [VISUAL:type=action-shot;...] placeholders in cited draft..."
python "$ROOT/scripts/resolve_captured_visuals.py" "$SLUG"

echo "==> Re-rendering preview..."
python "$ROOT/.claude/skills/preview/scripts/render_preview.py" "$SLUG"

echo "==> Rebuilding publish package..."
python "$ROOT/.claude/skills/format-for-publish/scripts/format_for_strapi.py" "$SLUG"

echo "==> Done."
echo "    Cited draft: $ROOT/content-pipeline/6-drafts-cited/$SLUG.md"
echo "    Preview:     $ROOT/content-pipeline/7-preview/$SLUG.html"
echo "    Publish:     $ROOT/content-pipeline/8-publish/$SLUG/article.md"
