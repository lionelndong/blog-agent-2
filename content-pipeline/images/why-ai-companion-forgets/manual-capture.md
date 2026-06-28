# Manual capture for why-ai-companion-forgets

Each entry below needs the editor to capture or upload manually:

## 1. external: A representative public user complaint about a character forgetting established facts after only a few messages

- **Reason:** bounding_box_failed
- **Source URL:** https://www.reddit.com/r/CharacterAI/
- **Selector:** `#t1_<comment-id>`
- **Hint:** Playwright blocked (bounding_box_failed). Run `/capture-visuals why-ai-companion-forgets` to retry this entry via Claude-in-Chrome (real Chrome session bypasses the wall). The skill picks up `failed` external entries automatically in unattended mode.
- **Fallback:** /capture-visuals (Claude-in-Chrome) — Playwright blocked, retry via real Chrome session.
- **Suggested filename:** `images/why-ai-companion-forgets/external-1-a-representative-public-user-c.png`

Original placeholder: `[VISUAL:type=external;sub=reddit-comment;url=https://www.reddit.com/r/CharacterAI/;selector=#t1_<comment-id>;crop=padded;what=A representative public user complaint about a character forgetting established facts after only a few messages]`

## 2. chart: Recall accuracy drops as the context window fills

- **Reason:** chart_data_unresolved:research_key_not_found:context_rot_accuracy
- **Hint:** Add the data to content-pipeline/1-research/why-ai-companion-forgets-data.json under the key the placeholder references, then re-run /generate-visuals. Or render manually: python .claude/skills/generate-visuals/scripts/render_chart.py --title "Recall accuracy drops as the context window fills" --style line --data '<inline JSON>' --out content-pipeline/images/why-ai-companion-forgets/chart-5-recall-accuracy-drops-as-the-c.png
- **Suggested filename:** `images/why-ai-companion-forgets/chart-5-recall-accuracy-drops-as-the-c.png`

Original placeholder: `[VISUAL:type=chart;data=research.context_rot_accuracy;style=line;title=Recall accuracy drops as the context window fills]`
