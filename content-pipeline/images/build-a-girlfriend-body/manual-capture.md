# Manual capture for build-a-girlfriend-body

Two action-shots are **captured-remote** — the bytes live on the VPS Linux filesystem at `/home/blogagent/blog-agent/content-pipeline/images/build-a-girlfriend-body/` because `save_to_disk` writes to whichever machine runs Chrome (the VPS), and this skill ran from a different host (Windows). The navigation succeeded, the wizard reached the right state, the screenshots got taken — they're just not on this filesystem.

## To finish (one command)

From this Windows host, with SSH access to the VPS:

```bash
bash scripts/sync_captures_from_vps.sh build-a-girlfriend-body
```

The sync script `rsync`s the captures back, swaps the `[VISUAL:...]` placeholders in the cited draft for `![alt](images/...)` markdown, re-renders the preview, and rebuilds the publish package. One step.

## Or: run the capture from the VPS itself

If the VPS Claude Code daemon is up (per `docs/vps-deploy.md`), trigger it to capture there:

```bash
ssh blogagent@<vps>
cd ~/blog-agent
claude --model claude-sonnet-4-6 --print '/capture-visuals build-a-girlfriend-body'
```

Captures land directly in `content-pipeline/images/build-a-girlfriend-body/` on the VPS. Then sync that dir back to Windows.

## What was captured (VPS-side state confirmed by the navigation agent)

### action-2 — Ethnicity step
- **URL:** https://pleasur.ai/create (after Realistic template + Next)
- **Wizard state confirmed:** 5 ethnicity preset cards visible — Caucasian, Asian, Latina, Black/Afro, Arab. Skin Tone swatches and Age block on the same screen.
- **Note:** the article was originally drafted for "6 ethnicities"; corrected to 5 in the cited draft after the agent observed the actual UI.

### action-3 — Body type / breast / butt step
- **URL:** https://pleasur.ai/create (after Caucasian + brown eyes + brunette + long hair + Next)
- **Wizard state confirmed:** Body Type cards (Slim, Athletic, Voluptuous, Curvy), Breast Size cards (Small, Medium, Large, Athletic), Butt Size cards — **preset cards, NOT sliders**.
- **Note:** the article was originally drafted for "breast and butt sliders"; corrected throughout to "preset cards" in the cited draft. The cards-vs-sliders distinction is now positioned as a real Pleasur-vs-competitors differentiator (Kupid, OurDream advertise sliders openly).

## Why this happened

`mcp__Claude_in_Chrome__computer`'s screenshot action with `save_to_disk: true` writes to the local filesystem of the machine running Chrome. From this Windows host, that machine is the VPS. The bytes don't traverse back through the MCP. Three workaround strategies were tried (inline-bytes return, `canvas.toDataURL()` via `javascript_tool`, MCP-cache-by-ID lookup) — all blocked by tool-result format, page CSP / canvas tainting, or absent MCP API. The architecture is intentional; the fix is co-locating capture with the project filesystem (run from VPS, or sync after).
