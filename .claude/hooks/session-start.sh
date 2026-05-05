#!/bin/bash
# SessionStart hook — load Doppler-managed secrets into the Claude Code session env.
#
# How this works (the only valid mechanism in Claude Code on the web):
#   We append `export KEY=VALUE` lines to $CLAUDE_ENV_FILE. The harness sources
#   that file before each subsequent tool call, so `Bash` / `python` / etc.
#   see the secrets in their environment. We CANNOT mutate the parent shell's
#   env directly — there is no parent shell to mutate.
#
# Activation:
#   Set DOPPLER_TOKEN as a workspace secret in Claude Code on the web settings.
#   The hook is a no-op (exit 0, friendly stderr message) if the token is missing
#   so dev sessions without secrets keep working.
#
# Fail-soft: any error inside this hook is logged to stderr and exits 0. Breaking
# session start over a missing key would block all work, including triage.

set -uo pipefail

log() { printf '[session-start] %s\n' "$*" >&2; }

# Only run in remote (Claude Code on the web). Locally, the user runs
# `doppler run -- claude` themselves; running the hook locally would clobber
# whatever shell env they already have.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  log "skipping (not a remote session)"
  exit 0
fi

if [ -z "${CLAUDE_ENV_FILE:-}" ]; then
  log "CLAUDE_ENV_FILE not set — cannot persist secrets to session env. Skipping."
  exit 0
fi

if [ -z "${DOPPLER_TOKEN:-}" ]; then
  log "DOPPLER_TOKEN not set. Set it as a workspace secret in Claude Code on the web settings."
  log "Skipping secret load — pipeline scripts that need API keys will fail at runtime."
  exit 0
fi

# Install Doppler CLI if missing. Idempotent.
if ! command -v doppler >/dev/null 2>&1; then
  log "installing Doppler CLI..."
  if ! curl -fsSL --retry 3 --max-time 60 'https://cli.doppler.com/install.sh' | sh -s -- --no-install >/dev/null 2>&1; then
    # Fallback: official install in a known prefix without sudo.
    if ! (curl -fsSL --retry 3 --max-time 60 'https://cli.doppler.com/install.sh' -o /tmp/doppler-install.sh \
          && sh /tmp/doppler-install.sh --install-path /usr/local/bin >/dev/null 2>&1); then
      log "Doppler CLI install failed (network or permission). Skipping secret load."
      exit 0
    fi
  fi
fi

# Pull every secret as KEY=VALUE pairs in dotenv format.
# `--no-file` prints to stdout, `--format env` produces shell-safe `KEY="value"` lines.
if ! secrets="$(doppler secrets download --no-file --format env 2>/dev/null)"; then
  log "doppler secrets download failed. Check DOPPLER_TOKEN scope and project bindings."
  exit 0
fi

if [ -z "$secrets" ]; then
  log "doppler returned no secrets. Check the project / config the token is bound to."
  exit 0
fi

# Doppler emits each line as KEY="value". Re-emit as `export KEY="value"` so the
# harness's source step picks them up. Strip Doppler's auto-injected DOPPLER_*
# metadata vars to keep the session env clean.
count=0
while IFS= read -r line; do
  case "$line" in
    ''|\#*) continue ;;
    DOPPLER_PROJECT=*|DOPPLER_CONFIG=*|DOPPLER_ENVIRONMENT=*) continue ;;
    *=*)
      printf 'export %s\n' "$line" >> "$CLAUDE_ENV_FILE"
      count=$((count + 1))
      ;;
  esac
done <<< "$secrets"

log "loaded $count Doppler secrets into session env"
exit 0
