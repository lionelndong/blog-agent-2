# Manual capture for build-a-girlfriend-body

Each entry below needs the editor to capture or upload manually:

## 1. action-shot: Companion Creator first step — Realistic vs Anime art style selection

- **Reason:** action_shot_routed_to_editor
- **Source URL:** https://pleasur.ai/create
- **Hint:** Capture interactively via Claude in Chrome. Run `/capture-visuals build-a-girlfriend-body` and walk through this entry, or open the URL in Chrome and capture the moment described in 'goal' yourself.
- **Suggested filename:** `images/build-a-girlfriend-body/action-3-log-into-pleasur-ai-with-the-s.png`

Original placeholder: `[VISUAL:type=action-shot;url=https://pleasur.ai/create;goal=Log into Pleasur.AI with the saved session. Open the Companion Creator at /create. Dismiss any age-verification dialog. Capture the first wizard step showing the Realistic vs Anime style selection cards.;what=Companion Creator first step — Realistic vs Anime art style selection]`

## 2. action-shot: Companion Creator final character preview — full-body render before creation

- **Reason:** action_shot_routed_to_editor
- **Source URL:** https://pleasur.ai/create
- **Hint:** Capture interactively via Claude in Chrome. Run `/capture-visuals build-a-girlfriend-body` and walk through this entry, or open the URL in Chrome and capture the moment described in 'goal' yourself.
- **Suggested filename:** `images/build-a-girlfriend-body/action-6-log-into-pleasur-ai-with-the-s.png`

Original placeholder: `[VISUAL:type=action-shot;url=https://pleasur.ai/create;goal=Log into Pleasur.AI with the saved session. Open the Companion Creator at /create. Move through all wizard steps: Realistic style, any ethnicity preset, any hair, any body type, any size cards, any outfit. Reach the final character preview screen showing the full-body render. Capture that screen.;what=Companion Creator final character preview — full-body render before creation]`

## 3. external: Pew Research pullquote — 53% of US adults say AI hurts personal data privacy

- **Reason:** bounding_box_failed
- **Source URL:** https://www.pewresearch.org/short-reads/2023/08/28/growing-public-concern-about-the-role-of-artificial-intelligence-in-daily-life/
- **Selector:** `.pullquote`
- **Hint:** Playwright blocked (bounding_box_failed). Run `/capture-visuals build-a-girlfriend-body` to retry this entry via Claude-in-Chrome (real Chrome session bypasses the wall). The skill picks up `failed` external entries automatically in unattended mode.
- **Fallback:** /capture-visuals (Claude-in-Chrome) — Playwright blocked, retry via real Chrome session.
- **Suggested filename:** `images/build-a-girlfriend-body/external-3-pew-research-pullquote-53-of-u.png`

Original placeholder: `[VISUAL:type=external;sub=news-quote;url=https://www.pewresearch.org/short-reads/2023/08/28/growing-public-concern-about-the-role-of-artificial-intelligence-in-daily-life/;selector=.pullquote;crop=padded;what=Pew Research pullquote — 53% of US adults say AI hurts personal data privacy]`
