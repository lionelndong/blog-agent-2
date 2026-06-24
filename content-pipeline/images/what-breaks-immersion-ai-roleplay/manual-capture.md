# Manual capture for what-breaks-immersion-ai-roleplay

Each entry below needs the editor to capture or upload manually:

## 1. external: A Replika user describing the post-update personality change they called "the lobotomy"

- **Reason:** bounding_box_failed
- **Source URL:** https://feltreal.org/blog/what-happened-to-replika
- **Selector:** `blockquote`
- **Hint:** Playwright blocked (bounding_box_failed). Run `/capture-visuals what-breaks-immersion-ai-roleplay` to retry this entry via Claude-in-Chrome (real Chrome session bypasses the wall). The skill picks up `failed` external entries automatically in unattended mode.
- **Fallback:** /capture-visuals (Claude-in-Chrome) — Playwright blocked, retry via real Chrome session.
- **Suggested filename:** `images/what-breaks-immersion-ai-roleplay/external-1-a-replika-user-describing-the.png`

Original placeholder: `[VISUAL:type=external;sub=news-quote;url=https://feltreal.org/blog/what-happened-to-replika;selector=blockquote;crop=padded;what=A Replika user describing the post-update personality change they called "the lobotomy"]`

## 2. action-shot: a companion chat showing the speaker icon on a reply bubble and the Call button on the character header

- **Reason:** wrong_ui_state_action_shot
- **What to capture:** A logged-in, populated **chat** view — a reply bubble with the **speaker icon** visible, and the **Call** button on the character header. This is a post-interaction state, not an empty page.
- **Why headless failed:** The headless capture of `https://pleasur.ai/create` landed on the Create wizard (Basics, Step 1 of 6) with explicit imagery and an unauthenticated header (Login / Join Free visible). It does not show any voice UI. The discarded PNG was the wrong UI state.
- **Annotate:** highlight `#voice-button` (speaker icon + Call button).
- **Fallback:** Run `/capture-visuals what-breaks-immersion-ai-roleplay` — Claude-in-Chrome logs into a real session, opens a companion chat, and captures the populated voice UI.
- **Suggested filename:** `images/what-breaks-immersion-ai-roleplay/action-shot-2-companion-chat-voice-ui.png`

Original placeholder: `[VISUAL:type=action-shot;target=chat;what=a companion chat showing the speaker icon on a reply bubble and the Call button on the character header;annotate=#voice-button]`
