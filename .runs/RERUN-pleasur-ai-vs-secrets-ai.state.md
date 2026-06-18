# State: pleasur-ai-vs-secrets-ai (PLE-2320) — AWAITING BOARD POSITIONING PICK

## Why paused (not failed)
RERUN-1 ran research→draft (quality 86 PASS) and CORRECTLY quarantined at verify-claims: the brief's pleasur.ai "$19/mo" plan does not exist, and it posted a board checkbox interaction (id 1a37f552, idempotencyKey checkbox:pleasur-ai-vs-secrets-ai:pricing-positioning:v1) asking which pricing anchor/framing to use before publishing. That is a legitimate brand-positioning checkpoint, so the issue is in_review awaiting the pick (continuationPolicy wake_assignee).

## Verified-live facts (2026-06-15) — already correct in the card
pleasur.ai: Starter $12.99/$5.20-annual, Standard $27.99/$11.20-annual, Ultimate $49.99/$20-annual; ALL tiers include adult chat + image gen + voice; text chat unlimited, media/voice/calls use coins. Secrets AI: $19.99/$13.33-annual. genfindr live 7.3 (not 7.6).

## Board options
- A (recommended): Standard anchor, honest split (Secrets cheaper monthly, pleasur.ai cheaper annual), keep value-positioning. <- I also recommend A (consistent with CMO "win on value" brief).
- B: Starter anchor, lead with price (pleasur.ai cheaper on both).
- C: a real $19 plan exists (MOOT — verified none on public page).

## Staged corrected inputs (ready for instant resume)
- content-pipeline/0-context/pleasur-ai-vs-secrets-ai.md  (corrected pricing/genfindr/credit-meter)
- content-pipeline/1-research/pleasur-ai-vs-secrets-ai.md  (correction header prepended)
- stale outline/draft/cited/quality archived -> .runs/archive-secrets-rework-20260615/
- adversarial budgets reset.

## ON WAKE (board picks A/B/C):
1. Tune 0-context framing to the pick (A=Standard anchor honest-split / B=Starter anchor lead-price). Re-run from /outline.
2. Relaunch: doppler run -- claude "/blog-pipeline pleasur ai vs secrets ai" with BLOG_AGENT_AUTONOMOUS=1 UNATTENDED=1 BLOG_AGENT_AUTO_PUBLISH=1 BLOG_AGENT_REVISION_BUDGET=5, PAPERCLIP_TASK_ID=PLE-2320, PATH includes /paperclip/.local/bin, DOPPLER_TOKEN=$DOPPLER_KEY.
3. Verify live 200 + H1 + audit row; PATCH PLE-2320 done -> wakes PLE-1955 -> PLE-1944.
4. Weekly cap: how-to-choose = post #1 this week; secrets-ai = #2 (within 5/wk).
