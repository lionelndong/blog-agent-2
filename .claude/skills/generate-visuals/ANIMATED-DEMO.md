# Animated demo engine — short looping product demos (GIF / MP4 / WebP)

**Locked 2026-06-28.** The animated-demo visual type: a short, **looping** clip of the
pleasur.ai product *in action* (a toggle flipping, a page scrolling, a chat being typed, an
image generating), captured by scripting a real browser and assembled into a small,
web-friendly GIF + MP4 + WebP wrapped in an on-brand "browser window" frame with the real
Pleasur.ai logo. It is the moving-picture sibling of the annotation/chart engines and reuses
the **same** patchright stealth + Cloudflare-wait + 18+-gate + auth machinery as
`capture_screenshot.py`.

## Why it exists
Static screenshots can't show *interaction*. A 3-second loop of the pricing toggle dropping
prices 60%, or of a reply streaming into a chat, carries information a still frame can't —
and reads as premium, not "vibe-coded". Quality is #1; SFW only (adult product, public blog).

## Run it (public scenes — work now)
Headed under the container's virtual display:
```bash
docker exec -e DISPLAY=:99 paperclip-whwi-paperclip-1 bash -lc '
  cd <repo>/.claude/skills/generate-visuals/scripts &&
  python3 animate_demo.py --scene pricing-toggle --out /tmp/out/pricing.gif --formats gif,mp4,webp'
```
Outputs (next to `--out`, stem reused per format): `pricing.gif`, `pricing.mp4`, `pricing.webp`,
and `pricing_report.json` (the deterministic critique-loop artifact: per-beat actions, clip box,
sizes, warnings).

| Preset | Tier | What it shows |
|---|---|---|
| `pricing-toggle` | **public** | Monthly ⇄ Yearly; prices dissolve, "Save 60%" + annual savings appear. State-mode + crossfade. |
| `pricing-scroll` | **public** | Smooth scroll down the pricing page (plans → compare table). Motion-mode (wheel burst). |
| `chat-typing` | auth | Type a SFW message, send, reply streams in. |
| `image-generating` | auth | Type a SFW prompt, hit Generate, result appears. |
| `call` | auth | Start a voice call (Standard+). |

## ⚠️ Dependency: the auth scenes need the SHOWCASE ACCOUNT
The high-value in-app demos (`chat-typing`, `image-generating`, `call`) are **fully authored and
ready** but require a logged-in session. Until it lands they return:
```json
{ "status": "blocked_on_auth", "dependency": "Showcase-account session required..." }
```
To enable them, provide the session **once**:
```bash
python scripts/setup_auth.py --print-b64   # log in to a SFW showcase account; saves auth/state.json
# put the printed value in Doppler as PLEASUR_AUTH_STATE_B64 (cloud) — or keep auth/state.json (local)
```
Then the *same* command runs unchanged with `--auth` (auto-on for auth scenes). Point it at a SFW
character: `--url https://pleasur.ai/chat/<sfw-character-id>`. **Keep every logged-in demo SFW** —
the showcase account must use a SFW character and SFW prompts/messages.

## Formats & size (keep it small)
`palettegen/paletteuse` GIF + H.264 MP4 (yuv420p, faststart) via the **bundled** ffmpeg
(`imageio_ffmpeg`, no system ffmpeg needed) + animated WebP via PIL.
- **MP4 is tiny** (~50–300 KB) → preferred for the article body.
- **GIF** is the universal fallback (state demos ~0.5–0.7 MB; motion/scroll ~1.5–2 MB).
- **WebP** is the smallest at quality (~20–180 KB).
- The engine warns when a GIF exceeds 3 MB → lower `--max-width`/`--fps` or shorten holds.

## The brand frame
`demo_polish.py` wraps each frame in a soft browser window — same palette / 22px radius / shadow /
real-logo family as the chart card (`render_chart_web.py`): `#F7F8FA` canvas, white card, traffic
lights, a `pleasur.ai/...` URL pill, a footer caption + the real `pleasurai-logo.png` (never
AI-drawn). The captured content's **bottom edge fades into the page's own bg** so list overflow /
unequal-height states read as intentional (the Linear/Vercel screenshot trick). `--frame none`
disables the chrome.

## Author a custom scene
Pass a JSON file to `--scene`. A scene = `url`, `viewport`, `clip` (the fixed CSS-px region every
frame captures — `{"crop":[x,y,w,h]}` or `{"selector":"…"}` or `null` for full viewport), and
`beats`. Each beat runs `actions` then captures either a **keyframe** (`shoot`, with optional
`{"transition":"crossfade","transition_ms":N}`) or a **motion burst** (`motion`: `frames`,
`interval_ms`, optional `each` actions run before every frame).
Actions: `click, hover, type, fill, press, wait, scroll, wheel, mouse_move, eval`.
```json
{ "name":"my-demo","url":"https://pleasur.ai/x","viewport":{"width":1280,"height":900},
  "clip":{"crop":[305,284,920,652]},"fps":12,"url_label":"pleasur.ai/x","caption":"…",
  "beats":[
    {"actions":[{"do":"click","selector":"button:has-text('A')"},{"do":"wait","ms":700}],"shoot":{"hold_ms":1500}},
    {"actions":[{"do":"click","selector":"button:has-text('B')"},{"do":"wait","ms":700}],"shoot":{"hold_ms":1800,"transition":"crossfade","transition_ms":340}}
  ]}
```

## Pipeline integration
`generate_visuals.py` routes `[VISUAL:type=demo;scene=…;what=…]` (and `type=animation|video|gif`)
to this engine. Auth scenes without a session come back `manual` with the dependency in
`manual-capture.md`. The draft is rewritten to reference the **GIF**; the MP4/WebP sit alongside
(`alt_formats` in the manifest) for the editor to embed the MP4 in the body.

## Gotchas (learned building it)
- **pleasur.ai defaults the pricing toggle to *Yearly*** — beat 0 clicks *Monthly* first so both
  crossfades show a real price change.
- **`window.scrollBy` is a no-op** here (an inner container scrolls, not the window) — use the
  `wheel` action (`page.mouse.wheel`) over the content; `mouse_move` to the content first.
- The **clip box is computed once** after settle and reused for every frame — that's what makes the
  content (and only the content) appear to animate. Keep the viewport tall enough that the region
  needn't scroll between beats (unless scrolling *is* the demo).
- Run **headed under `DISPLAY=:99`** (Cloudflare blocks headless). Outputs land *inside the
  container* — `docker cp` them out before `scp`.

Every demo MUST pass `VISUAL-CRITIQUE-LOOP.md` (render → critique → fix → re-render, max 3) before
it ships.
