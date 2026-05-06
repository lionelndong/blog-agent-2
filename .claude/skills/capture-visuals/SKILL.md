---
name: capture-visuals
description: Walk through the manual-capture.md checklist for a slug, driving Chrome via the Claude in Chrome MCP to capture each visual that needs more than a static URL — multi-step flows, conversation states, settings panels, age gates on third-party sites. Runs equally well locally (your desktop Chrome) or on a VPS with always-on Chrome + the extension installed. Defaults to unattended mode when `BLOG_AGENT_AUTONOMOUS=1` (which forces `UNATTENDED=1`). Use after /generate-visuals has flagged action-shot or failed-screenshot entries.
---

# Capture Visuals (Chrome MCP-driven)

For slug `{slug}`, walk through `content-pipeline/images/{slug}/manual-capture.md` and capture each entry by driving Chrome via the Claude in Chrome MCP.

This is the action-driven counterpart to `/generate-visuals`. Generate-visuals handles deterministic URL→image captures (patchright, headless). Capture-visuals handles anything that needs clicks, typing, waits, or visual judgment.

**Deployment:** runs on whatever machine has Chrome + the extension installed. Locally that's your desktop. On a VPS with always-on Chrome + the extension authenticated to claude.ai + Pleasur.ai (and whatever other sites you want logged in), this skill becomes fully unattended — cron-friendly, no human at the keyboard required.

**Critical: same-machine constraint.** The Chrome MCP's `save_to_disk` parameter writes screenshots to the local filesystem of the machine running Chrome. For the captured PNGs to land in this project's `content-pipeline/images/{slug}/` directory, this skill must be invoked from a Claude Code session running on the same machine as the target Chrome. Cross-machine setups (e.g. Claude Code on Windows driving a remote Linux Chrome) work for visual verification but the screenshot bytes don't reach the project filesystem — only image-data references come back. On the VPS deployment this is not a concern: Chrome and Claude Code both run on the VPS.

## When to use this skill

- After running `/generate-visuals {slug}` you see entries in `manual-capture.md`
- Any time you want to recapture a visual that the deterministic path produced badly
- Visuals that need conversation state, settings flow, or visual judgment
- Captures of sites whose bot protection beats patchright (CF Pro, DataDome, etc.)
- Captures requiring auth on third-party sites where you keep a logged-in Chrome session
- **PLEAA-417:** any `external` entry in the manifest with `status: "failed"` and a `fallback.method == "claude_in_chrome"` block. These are Reddit / tweet / news / competitor-UI visuals where Playwright hit a CF challenge or login wall — the manifest carries the URL + selector + suggested filename so this skill can drive Chrome to the same element and capture it via the real session.

Do NOT use for:
- Bulk captures of static public pages — `/generate-visuals` (patchright headless) is faster and free for those
- Cases where you have no browser path at all (the visual is data → use `chart`, or aesthetic → use `image`)

## Deployment modes

**Local (interactive):** your desktop Chrome with the extension. You watch each capture happen. Useful while drafting, exploring, or verifying.

**VPS (unattended):** an always-on Chrome with the extension authenticated to claude.ai and your target sites. A cron-triggered Claude Code session calls this skill, the skill drives the VPS's Chrome via the MCP, captures land in `content-pipeline/images/{slug}/`. Same skill, no human in the loop.

The skill itself doesn't care which mode — it just calls `mcp__Claude_in_Chrome__*` tools. Whoever's running Chrome (you or the VPS) does the actual work.

## Required tools

The Claude in Chrome MCP must be connected. Tool names start with `mcp__Claude_in_Chrome__*`. If they're not in the deferred-tools list, ask the user to install/connect the Chrome extension.

## Model

Always run this skill on **Sonnet 4.6** (`claude-sonnet-4-6`) — never Opus. Driving a browser is high-throughput, low-reasoning work; Opus is wasted token spend here, and Sonnet 4.6 is meaningfully faster. If you arrive at this skill on Opus, switch to Sonnet via `/model claude-sonnet-4-6` before driving Chrome. The VPS systemd unit and cron triggers should pin `--model claude-sonnet-4-6` so unattended runs don't drift to Opus.

## Process

1. **Read the manual-capture.md** for the slug:
   ```
   content-pipeline/images/{slug}/manual-capture.md
   ```
   Each numbered entry has: type, alt text, source URL (sometimes), goal (for action-shot entries), suggested filename, and the original placeholder.

2. **Determine mode.** Check `os.environ.get('UNATTENDED')`:
   - If `'1'`, run **unattended mode**: skip per-step user confirmations, drive each capture autonomously, only stop on hard errors. The safety check is the goal's specificity plus the post-capture heuristic validation in `templates/visual-types.md`. This is the VPS / cron path.
   - Otherwise, run **interactive mode**: brief the user before each step, wait for confirmation, show captures and ask "good or retry?" This is the editor-at-keyboard path.

3. **For each entry, in order:**

   a. **(Interactive only) Brief the user** on what's about to happen — show the entry's goal and source URL, ask if they want to skip / proceed / customize. **Unattended:** skip this step.

   b. **Navigate.** Use `mcp__Claude_in_Chrome__navigate` to open the source URL.

   c. **Drive the actions.** Use the Chrome MCP tools (`find`, `left_click`, `form_input`, `read_page`, etc.) to perform the goal's described steps. **Interactive:** show each step. **Unattended:** execute through the sequence; if a tool returns an error, log it to the manifest as `failed` with the error message and skip to the next entry rather than blocking the chain.

   d. **Verify the visible state matches the goal.** Use `mcp__Claude_in_Chrome__read_page` or `mcp__Claude_in_Chrome__get_page_text`. If the visible state contradicts the goal:
      - **Interactive:** surface what you see and ask how to proceed.
      - **Unattended:** mark the entry `failed` with reason `state_mismatch` (include the read_page summary) and skip. Don't capture — wrong-state captures are worse than missing ones.

   e. **Capture — handle the same-machine constraint correctly.** The Chrome MCP's `save_to_disk` parameter writes to the machine running Chrome, NOT the machine running this skill. If those are the same host (VPS deployment), `save_to_disk: true` works directly. If they differ (e.g. this skill runs on a developer laptop driving the always-on VPS Chrome), the bytes go to the VPS filesystem and never reach the project on the laptop.

      **Apply this strategy in order — pick the first one that lands bytes in `content-pipeline/images/{slug}/{suggested_filename}` on the local filesystem of THIS skill's machine:**

      1. **Try the screenshot tool WITHOUT `save_to_disk`** (omit the flag, or set false). Inspect the tool result for inline image data — many MCP screenshot tools return base64 in the response when save_to_disk isn't set. If you get bytes, decode (Python: `pathlib.Path(target).write_bytes(base64.b64decode(data))`) and save locally.
      2. **Try `save_to_disk: true` AND then read back**. If save_to_disk writes to a path the local Python can read (i.e. same host), this works in one step. If it writes remote, this is no good — fall through.
      3. **Try `mcp__Claude_in_Chrome__javascript_tool` with native canvas APIs** (no external scripts — CSP will block them). For pages where `document.documentElement` is canvas-renderable, this can produce a base64 dataURL you decode locally. Note: this only captures the page DOM, not the full viewport like a real screenshot.
      4. **If all three fail and Chrome is genuinely on a different host than this skill** — record the entry in the manifest as `status: "captured_remote"` with `host: "vps"` and the path on the VPS. The pipeline editor (or the VPS-side cron) needs to either run this skill from the VPS, or sync `content-pipeline/images/{slug}/` from the VPS back to the local host. Don't claim local capture when bytes aren't local.

      The filename to save under is whatever the `manual-capture.md` entry suggested (or replace `TBD.png` with a sensible slug derived from the goal text).

   f. **Validate the capture** with the heuristics in `templates/visual-types.md` (final URL didn't redirect to login, image dimensions sane, color variance > 0.02, file size > 5KB). If validation fails:
      - **Interactive:** show the capture and ask "retry / accept / skip".
      - **Unattended:** mark `failed` with the validation reason; the entry stays in `manual-capture.md` for the next interactive run.

   g. **(Interactive only) Confirm.** Show the captured PNG to the user. Ask "good or retry?" Loop on retry. **Unattended:** skip this step; the validation in (f) is the gate.

   h. **Move on** to the next entry.

3. **Update the cited draft.** After all captures complete, rewrite `content-pipeline/6-drafts-cited/{slug}.md` to swap the captured `[VISUAL:...]` and `[SCREENSHOT:...]` placeholders with the corresponding `![alt](images/{slug}/file.png)` markdown.

4. **Re-render the preview.**
   ```bash
   python .claude/skills/preview/scripts/render_preview.py {slug}
   ```

5. **Update the manifest.** For each captured entry, add a record to `content-pipeline/images/{slug}/manifest.json` with `status: captured`, `path: ...`, `capture_method: claude_in_chrome`. Keep existing entries; just append or update. If the manifest already has an entry for that index, mark it captured and move on.

## Reporting

After the chain finishes:

```
✓ Capture-visuals complete for {slug}

Captured {N} visuals via Claude in Chrome:
  - images/{slug}/file-1.png — {description}
  - images/{slug}/file-2.png — {description}
  ...

Skipped {M}: {list reasons}

Cited draft updated, preview re-rendered:
  → content-pipeline/7-preview/{slug}.html
```

## Why this skill exists

Most visuals in a blog post are simple — a URL → an image. `/generate-visuals` handles those automatically with patchright on the VPS, no humans needed.

A small fraction need judgment: capture the wizard at the right moment, show the conversation in mid-flow, find a third-party site that has the right thing on it. For those, scripted automation breaks — you need eyes on the page. That's what Claude in Chrome is for, and what this skill drives.

This is the same architecture the source article (Ryan Law's content engineering pipeline) describes: automate the deterministic, human-loop the editorial.

## When the Chrome MCP isn't connected

Tell the user:

> The Claude in Chrome extension isn't connected. Install it from the Chrome Web Store, then come back and re-run `/capture-visuals {slug}`. Alternatively, capture each entry in `manual-capture.md` yourself with your normal screenshot tool and save them to `content-pipeline/images/{slug}/` with the suggested filenames.

Then offer to keep going by reading their captures off disk after they save them.
