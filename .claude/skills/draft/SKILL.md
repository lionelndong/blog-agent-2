---
name: draft
description: Expand an annotated outline into full article prose using brand voice anchored in example articles. Triggered after /product-mentions.
allowed-tools: Read, Write, Glob
---

# Draft Skill

Turn the annotated outline into a publishable first draft. The draft is **not** final — `verify-claims`, `generate-screenshot`, `preview`, and `format-for-publish` follow. But it should be 80% there.

## Voice metrics — HARD targets (read first, before anything else)

These are not soft suggestions to apply in a self-edit pass. They're the prose-rhythm spec. The previous pipeline run produced a draft that was 2.2× too long per paragraph and 2.5× too em-dash-heavy on first save; the surgical-fix loop after quality-check is expensive. Hit the targets on the first pass.

| Metric | Target | Hard ceiling | Why |
|---|---|---|---|
| Avg paragraph length | 24–35 words | < 45 | Long paragraphs sound like white papers, not a guide |
| Median paragraph length | 20–30 words | < 40 | Skim-readers bail when paragraphs are walls |
| Em-dashes per 1,000 words | 6–8 | ≤ 12 | Em-dash addiction is the cardinal AI tell |
| Second-person words ("you", "your") per 1,000 words | 25+ | — | The voice is *to* the reader, not *about* the topic |
| Forbidden phrases (from brand-config) | 0 | 0 | Non-negotiable |

After drafting each H2, count quickly: how many em-dashes did you write in the section? How many `you/your`? How long are paragraphs? If anything is off, fix it before moving on. Don't accumulate the debt and try to clean it at the end — the surgical-fix pattern is what we're trying to avoid.

## Input

For slug `{slug}`:
- `content-pipeline/4-outlines-annotated/{slug}.md` (required — the outline with product annotations)
- `content-pipeline/0-context/{slug}.md` (if exists — user-provided direction)
- `content-pipeline/2-reference/{slug}.md` (brand context, internal-linking opportunities)
- `content-pipeline/1-research/{slug}.md` (research data — for stats, quotes, evidence references)
- `brand-config.md` (voice, audience, products, **forbidden phrases**)
- `references/voice-guide.md` (structural voice rules)
- `references/prose-patterns.md` (sentence-level patterns)
- `../../../templates/visual-types.md` (controlled vocabulary for `[VISUAL:...]` placeholders)
- **At least 2 articles from `examples/`** — pick the ones whose topic is closest

## Process

1. **Read examples first.** Use Glob to list `examples/*.md`, then read 2 whose topic is closest to the keyword. Read them in full. The voice in those files is the spec.
2. **Read the outline thoroughly.** You're not re-architecting — the outline is the spec.
3. **Read context, brand-reference, research, brand-config.** Hold all this in mind while drafting.
4. **Draft the intro** (150–200 words):
   - Hook — direct claim, surprising cited stat, opinion, or problem-naming
   - Thesis — one sentence
   - Preview — what reader gets
5. **Draft each H2 in order:**
   - Open with the section's BLUF (or a sentence that captures the same idea)
   - Develop the key points using prose patterns from `references/prose-patterns.md`
   - Hit the evidence the outline specified — cite stats with a `[link]` placeholder if you don't have the exact URL (verify-claims will fix)
   - Insert product mentions where the annotated outline says — using the "show, don't sell" pattern
   - Insert internal-linking opportunities from `2-reference/` as `[anchor text](URL)` inline
   - Close with a transition into the next section
6. **Insert typed visual placeholders.** For every H2 with a `Visuals:` block (or legacy single `Visual:` block) in the annotated outline, emit **one placeholder per visual entry** — sections with two `Visual N:` lines emit two placeholders, placed at natural break points (typically: first visual after the BLUF + 1–2 paragraphs of setup; second visual after the key claim or example). The intro can carry one placeholder if the outline includes a `Visual:` line under the introduction. The `generate-visuals` skill realizes these into real assets later.
   - **`screenshot`** → `[VISUAL:type=screenshot;target=<product-slug>;what=<UI element>;annotate=<optional>]` — for static URLs where the wanted state is visible on first load.
   - **`action-shot`** → `[VISUAL:type=action-shot;url=<starting URL>;goal=<full natural-language sequence: navigate, click, type, wait, what to capture>;what=<short caption>]` — for UI states that require multi-step interaction (clicking past step 1 of a wizard, sending a message in a conversation, opening settings, etc.) or for pages where `screenshot` fails due to aggressive bot protection. Be explicit in `goal` about which screen to land on for the capture.
   - **`image`** → `[VISUAL:type=image;sub=<concept-illustration|diagram|flow-diagram|comparison|lifestyle>;prompt=<specific structured prompt>;style=<illustration|photorealistic|flat-vector|isometric>;safety=<sfw|adult>]` — default `sub=concept-illustration`, default `safety=sfw`. **Highest-value `image` use is concept illustrations and labeled diagrams**, not lifestyle/mood. Prompts must be specific (name every labeled component, describe layout, specify connectors like arrows). See `templates/visual-types.md` § `image` placeholder fields for prompt patterns. Use `safety=adult` only when the section genuinely needs adult-themed imagery; this routes to manual capture.
   - **`chart`** → `[VISUAL:type=chart;data=<source>;style=<bar|line|pie>;title=<chart title>]`
   - **`video`** → `[VISUAL:type=video;url=<youtube-or-loom URL>;what=<description>]`
   - **`external`** → `[VISUAL:type=external;sub=<reddit-comment|tweet|news-quote|competitor-ui|chart>;url=<source URL>;selector=<CSS selector>;crop=padded;what=<short caption>]` — **PLEAA-417: auto-captured by default.** When the section quotes a Reddit comment, embeds a tweet, or cites a chart in a news article, emit one of these so the pipeline produces a real cropped PNG of the cited element. Always pair with a `selector` that clips to the specific element (Reddit comment IDs are `#t1_<id>`, tweets are `article[data-testid="tweet"]`, news charts are commonly `figure.chart`). On Cloudflare/login walls the pipeline auto-falls-back to `/capture-visuals` (Claude-in-Chrome). See `templates/visual-types.md` for the selector cheatsheet.
   - **`gif`** → `[VISUAL:type=gif;what=<multi-step interaction description>]`
   - **`table`** → write the markdown table inline. **No placeholder.**
   - **`none`** → write prose only. No placeholder.

   **`action-shot` goal-writing tips:** the dispatcher routes the goal to `/capture-visuals`, where Claude — pinned to **Sonnet 4.6** (`claude-sonnet-4-6`), never Opus — drives the always-on Chrome browser through the Claude-in-Chrome MCP. Browser driving is high-throughput / low-reasoning, so Sonnet is faster and cheaper without quality loss. Write the goal like you'd brief a human assistant who has never seen the site. Specify the URL, every action in order, what to wait for, and which screen is the capture target. Example: "Navigate to pleasur.ai/create. Dismiss the age verification dialog. Click the Realistic template card. Wait for the Ethnicity selection step to load. Capture that screen." Keep it under 60 words; longer goals waste browser steps. No token billing — uses your subscription via the extension.
   Backwards compat: legacy `[SCREENSHOT: description]` still works (treated as `[VISUAL:type=screenshot;what=description]`) but new drafts should use the typed form.
7. **Draft the conclusion** (80–150 words):
   - Restate thesis in fresh framing
   - One next step (often a link to a `2-reference/` URL)
8. **Self-edit pass:**
   - Re-read for forbidden phrases (from `brand-config.md`)
   - Cut any sentence that starts with "Furthermore", "Moreover", "It is important to note"
   - Cut "very", "really", "quite", "actually", "simply" wherever they don't carry weight
   - Verify each section opens with a BLUF
   - Verify product mentions follow the "show, don't sell" pattern
9. **Pre-save metrics gate.** Before writing the file, compute the four voice metrics on the current draft (cheap word/character counts):
   - Avg paragraph length: total words / number of paragraphs
   - Median paragraph length: middle paragraph by word count
   - Em-dashes per 1k words: count of `—` characters / total words × 1000
   - You-words per 1k words: count of `you|your|yours|yourself` (case-insensitive, word-bounded) / total words × 1000

   If any metric is outside the **hard ceiling** (`Voice metrics` table at the top), revise *now* — don't save and let quality-check fail. Specifically:
   - Em-dashes > 12/1k → mechanical pass: convert every other em-dash to a comma, period, or semicolon. Read aloud after.
   - Avg paragraph > 45 words → split long paragraphs at the natural pivot.
   - You-words < 25/1k → rewrite third-person declaratives ("readers want X", "the reader notices Y") as second-person ("you want X", "you notice Y").

   Iterate until all four metrics are inside the targets, then save. This pre-save gate is what prevents the surgical-fix loop after quality-check.

10. **Save** to `content-pipeline/5-drafts/{slug}.md`. Include the article title as H1, then prose. No metadata header in the body — the next stages add what they need.

## Output

`content-pipeline/5-drafts/{slug}.md`

A clean markdown article. Word count should match the sum of section targets from the outline (typically 1500–4000 words).

## Quality checklist

Before saving, confirm:

- [ ] Read 2 example articles before drafting
- [ ] Intro: hook + thesis + preview, 150–200 words, no fluff opener
- [ ] Every section opens with a BLUF (not throat-clearing)
- [ ] Product mentions follow show-don't-sell pattern (problem → manual way → product way → specific output)
- [ ] Internal links from `2-reference/` woven in with descriptive anchor text (not "click here")
- [ ] Stat placeholders use `[link]` markers for `verify-claims` to find later
- [ ] Visual placeholders use typed `[VISUAL:type=...;...]` format (per `templates/visual-types.md`); tables written inline as markdown
- [ ] No forbidden phrases (from `brand-config.md`)
- [ ] Conclusion: restated thesis + one next step
- [ ] Reads aloud naturally — try reading the intro and one H2 out loud

## When the draft feels off

- **Sounds generic** → re-read examples, try again. Probably didn't anchor enough in the example voice.
- **Sounds too salesy** → re-check product mentions. Cut any that don't pass the "competent reader" test.
- **Sounds choppy** → too many short sentences in a row. Vary rhythm.
- **Sounds bloated** → cut filler words (very, really, just, simply, basically); split long paragraphs.

If two voice-fix passes don't help, the problem is upstream — the outline may be wrong, or the research dossier didn't surface a strong angle. Don't fix it in the draft; fix it in the outline.
