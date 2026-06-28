#!/usr/bin/env bash
# Detached finalizer for PLE-2960. Fully orphaned (setsid) so it survives
# heartbeat teardown, exactly like the nohup'd pipeline does. Waits for the
# pipeline process to exit, then snapshots terminal state to a sentinel file
# that a fresh-token heartbeat reads to post the deliverable + update the ledger.
set -uo pipefail
REPO="/paperclip/instances/default/projects/d11fb003-42e2-4b84-8d88-e1242ad09a70/58966819-f893-4728-ad83-5956700fd1c6/_default/blog-engine"
cd "$REPO" || exit 1
PIPID="${1:-152231}"
SLUG="what-breaks-immersion-ai-roleplay"
URL="https://pleasur.ai/blog/$SLUG"
OUT="/tmp/ple2960-final.txt"
DOPPLER="/paperclip/.local/bin/doppler"

# Wait for pipeline exit (max ~110 min)
for i in $(seq 1 110); do
  kill -0 "$PIPID" 2>/dev/null || { echo "pipeline_exited_after_min=$i" > "$OUT"; break; }
  sleep 60
done
[ -f "$OUT" ] || echo "pipeline_still_running_at_timeout=1" > "$OUT"

{
  echo "finalizer_done_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "--- live_url_check ---"
  echo "url=$URL"
  echo "http=$(curl -s -o /tmp/ple2960-live.html -w '%{http_code}' "$URL" 2>/dev/null)"
  echo "h1=$(grep -oiE '<h1[^>]*>[^<]*</h1>' /tmp/ple2960-live.html 2>/dev/null | head -1 | sed 's/<[^>]*>//g')"
  echo "--- audit_row ---"
  grep -i "$SLUG" content-pipeline/audit/auto-blog-log.csv 2>/dev/null | tail -1 | cut -c1-300
  echo "--- stage_artifacts ---"
  for d in 5-drafts 6-drafts-cited 7-preview 8-publish 9-needs-review quality-checks; do
    f=$(ls -t "content-pipeline/$d/" 2>/dev/null | grep -i immersion | head -1)
    [ -n "$f" ] && echo "$d: $f"
  done
  echo "--- run_log_tail ---"
  tail -25 content-pipeline/audit/run-${SLUG}-20260624-133125.log 2>/dev/null
} >> "$OUT" 2>&1

# Run the canonical post-publish gate check if a publish artifact exists
if ls content-pipeline/8-publish/ 2>/dev/null | grep -qi immersion; then
  echo "--- auto_publish_check ---" >> "$OUT"
  DOPPLER_TOKEN="${DOPPLER_KEY:-${DOPPLER_TOKEN:-}}" "$DOPPLER" run --project pleasurai --config dev -- \
    python3 scripts/auto_publish_check.py --slug "$SLUG" >> "$OUT" 2>&1 || echo "auto_publish_check_rc=$?" >> "$OUT"
fi
echo "SENTINEL_COMPLETE" >> "$OUT"
