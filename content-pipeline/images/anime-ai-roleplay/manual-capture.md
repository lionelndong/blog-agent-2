# Manual capture for anime-ai-roleplay

Each entry below needs the editor to capture or upload manually:

## 1. external: the "anime ai roleplay" results are app-store listings and product pages, not a single real guide

- **Reason:** bounding_box_failed
- **Source URL:** https://www.google.com/search?q=anime+ai+roleplay
- **Selector:** `#search`
- **Hint:** Playwright blocked (bounding_box_failed). Run `/capture-visuals anime-ai-roleplay` to retry this entry via Claude-in-Chrome (real Chrome session bypasses the wall). The skill picks up `failed` external entries automatically in unattended mode.
- **Fallback:** /capture-visuals (Claude-in-Chrome) — Playwright blocked, retry via real Chrome session.
- **Suggested filename:** `images/anime-ai-roleplay/external-1-the-anime-ai-roleplay-results.png`

Original placeholder: `[VISUAL:type=external;sub=serp;url=https://www.google.com/search?q=anime+ai+roleplay;selector=#search;crop=padded;what=the "anime ai roleplay" results are app-store listings and product pages, not a single real guide;annotate=the stacked app-store and product listings where a real how-to guide should be]`

## 2. external: a real user complaining their roleplay bot forgot the scenario

- **Reason:** bounding_box_failed
- **Source URL:** https://www.reddit.com/r/AIAssisted/comments/anime-rp-forgot
- **Selector:** `#t1_examplecomment`
- **Hint:** Playwright blocked (bounding_box_failed). Run `/capture-visuals anime-ai-roleplay` to retry this entry via Claude-in-Chrome (real Chrome session bypasses the wall). The skill picks up `failed` external entries automatically in unattended mode.
- **Fallback:** /capture-visuals (Claude-in-Chrome) — Playwright blocked, retry via real Chrome session.
- **Suggested filename:** `images/anime-ai-roleplay/external-2-a-real-user-complaining-their.png`

Original placeholder: `[VISUAL:type=external;sub=reddit-comment;url=https://www.reddit.com/r/AIAssisted/comments/anime-rp-forgot;selector=#t1_examplecomment;crop=padded;what=a real user complaining their roleplay bot forgot the scenario;annotate=the line where the user says the character forgot or reset the story]`

## 3. external: archetype and personality selectors in a real rival product

- **Reason:** bounding_box_failed
- **Source URL:** https://cycleai.ai
- **Selector:** `.character-options`
- **Hint:** Playwright blocked (bounding_box_failed). Run `/capture-visuals anime-ai-roleplay` to retry this entry via Claude-in-Chrome (real Chrome session bypasses the wall). The skill picks up `failed` external entries automatically in unattended mode.
- **Fallback:** /capture-visuals (Claude-in-Chrome) — Playwright blocked, retry via real Chrome session.
- **Suggested filename:** `images/anime-ai-roleplay/external-3-archetype-and-personality-sele.png`

Original placeholder: `[VISUAL:type=external;sub=competitor-ui;url=https://cycleai.ai;selector=.character-options;crop=padded;what=archetype and personality selectors in a real rival product;annotate=the tsundere/yandere archetype selectors]`

## 4. external: a "pick from a gallery" experience versus build-your-own

- **Reason:** bounding_box_failed
- **Source URL:** https://emochi.com
- **Selector:** `.character-grid`
- **Hint:** Playwright blocked (bounding_box_failed). Run `/capture-visuals anime-ai-roleplay` to retry this entry via Claude-in-Chrome (real Chrome session bypasses the wall). The skill picks up `failed` external entries automatically in unattended mode.
- **Fallback:** /capture-visuals (Claude-in-Chrome) — Playwright blocked, retry via real Chrome session.
- **Suggested filename:** `images/anime-ai-roleplay/external-4-a-pick-from-a-gallery-experien.png`

Original placeholder: `[VISUAL:type=external;sub=competitor-ui;url=https://emochi.com;selector=.character-grid;crop=padded;what=a "pick from a gallery" experience versus build-your-own;annotate=the fixed character cards with voice-message and AI-art tags]`

## 5. action-shot: the character recalling a prior-session detail with the in-chat voice control active

- **Reason:** session_required
- **Source URL:** https://pleasur.ai
- **Hint:** Logged-in action-shot needs the Pleasur.AI showcase session. Mint it once with `python .claude/skills/generate-visuals/scripts/setup_auth.py --interactive --headed` (calls need Standard+), then re-run /generate-visuals.
- **Suggested filename:** `images/anime-ai-roleplay/action-6-log-in-open-an-existing-anime.png`

Original placeholder: `[VISUAL:type=action-shot;url=https://pleasur.ai;goal=Log in. Open an existing anime character chat that has prior history. Surface a reply where the character references an earlier scenario detail. Tap the speaker icon on that reply. Keep it SFW — steer to clean content, hide flirty side-panels, blur any PII.;what=the character recalling a prior-session detail with the in-chat voice control active;annotate=the recalled detail plus the active speaker/voice icon]`
