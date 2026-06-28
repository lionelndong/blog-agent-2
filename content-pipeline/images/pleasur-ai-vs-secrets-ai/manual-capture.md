# Manual capture to-do — pleasur-ai-vs-secrets-ai

Two visuals could not be captured cleanly in the autonomous environment and need an editor with a
real, logged-in Chrome session (use `/capture-visuals pleasur-ai-vs-secrets-ai`). Do NOT fabricate
or substitute an asset — leave the typed placeholder until a real capture exists.

## external-1 — genfindr 7.3/10 rating for Secrets AI
- URL given in draft: https://genfindr.com  (selector `.rating`)
- Why manual: the bare genfindr.com URL renders only the landing page here — it does NOT show the
  Secrets AI rating, and `.rating` never resolves. The 7.3/10 lives on a specific Secrets AI review
  page reached through an NSFW-AI directory that surfaces adult imagery (a context we don't capture
  autonomously). The 7.3/10 number is already cited in prose with the genfindr.com link, so the
  article stands without the screenshot.
- To capture: open the genfindr Secrets AI review page in a real Chrome session, accept the age
  gate, and clip the rating badge (`--padding 24`).

## screenshot-1 — AI Companion Creator panel (appearance / personality / kinks)
- URL: https://pleasur.ai/create  (selector `.traits-section`)
- Why manual: age gate is auto-dismissed, but the Creator is behind login and there is no
  `auth/state.json` in this environment, so `.traits-section` never appears for an anonymous
  headless session.
- To capture: run `python .claude/skills/generate-visuals/scripts/setup_auth.py` once to log in
  (saves cookies), then re-run the screenshot capture, or clip the panel from a logged-in Chrome
  session.
