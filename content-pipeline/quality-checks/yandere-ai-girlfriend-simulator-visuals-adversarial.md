# Visuals Adversarial: yandere-ai-girlfriend-simulator

_Reviewed against manifest.json and cited draft_

## Visual audit (9-step earn-your-place check)

**Visual 1: external — itch.io game header screenshot**

Applying the 9-step decision rule:
1. Does it walk through a brand product UI at a static URL? No — it's a third-party game page.
2. Does it need multi-step interaction? No — static page.
3. Compare N things on M axes? No.
4. Present quantitative data with trends? No.
5. Reference a third-party artifact we're citing? **YES.** The article discusses the itch.io game directly. Showing the actual game page header (title, platform, price) is concrete and informative — it confirms to the reader that the game is real, free, and downloadable.
6. Animated multi-step demo? No.
7. Embed a video? No.
8. Aesthetic/mood illustration? No.
9. Otherwise → none? Applied step 5 — external reference earns its place.

**Verdict on the visual:** PASS. The itch.io game header screenshot is load-bearing — it shows the game title, "Name your own price" CTA, and platform availability (Windows/macOS/Linux). A reader who is skeptical that the game exists gets visual confirmation. Removing it loses concrete information.

**What to strip:** Nothing to strip. The single visual is genuinely informative.

**What to add:** Nothing to add. The table in the apps section is implemented as markdown (no asset file needed). The article has appropriate visual economy — 6 sections, 1 external screenshot, no decorative images.

## Findings

**[LOW] Screenshot crop could be tighter**
The patchright capture is a full-viewport top crop (1440×300). This includes blank pink background on the left and right sides. A tighter crop focusing on the content area (from approximately x=284 to x=1010) would look cleaner in the published article. This is a presentation issue, not a gate blocker.

## What works

Visual economy is correct. The outline specified 2 non-`none` visuals (1 external + 1 table). The table is correctly implemented inline as markdown — no visual asset needed. The external screenshot is the only asset and it earns its place.

## Verdict: **PASS**
