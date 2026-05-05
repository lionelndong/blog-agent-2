# Voice anchoring examples

This directory contains reference articles that the `/draft` skill reads before writing prose. The voice in these files is the source of truth for how articles in this pipeline should sound.

## Why we use examples instead of just rules

A distilled style guide ("be conversational", "use second person") is a guardrail, not a spec. Large language models infer voice patterns more reliably from real text than from rules. This is the core insight from [Ryan Law's process](https://ahrefs.com/blog/how-i-do-content-engineering-with-claude-code/): give the model the actual writing you want it to imitate.

## What's here

5 publicly available articles from the Ahrefs blog covering different content types:

- `ahrefs-keyword-research.md` — definitive guide format
- `ahrefs-content-gap.md` — methodology / how-to format
- `ahrefs-link-building.md` — comprehensive resource format
- `ahrefs-seo-basics.md` — beginner-friendly explainer format
- `ahrefs-rank-tracking.md` — tactical/practical format

Each file is the markdown text of the article (no images, no shortcodes), captured for voice reference only.

## How the pipeline uses these

The `/draft` skill reads at least 2 of these (preferring topical adjacency) before drafting any new article. The `/outline` skill reads them when deciding section structure.

## Customizing

To shift voice toward your own brand:
1. Replace one or more files here with your own articles (in `.md` format, prose only)
2. Update the file list above
3. Optionally add a `_voice-notes.md` describing what's distinctive about your brand voice

The pipeline favors examples over rules. If you want different output, change the examples.
