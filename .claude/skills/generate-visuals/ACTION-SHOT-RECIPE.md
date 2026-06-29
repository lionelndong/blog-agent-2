# Product action-shots — engine + recipe (LOCKED 2026-06-28)

Visual type **C: the PRODUCT ACTION-SHOT** — clean, aspirational, on-brand in-app screenshots (a
chat with a persona, a call screen, the image gallery). Screenshots are ~60% of a product blog's
images, so this is the **biggest** visual. **Quality is #1. SFW only.**

Pipeline (all deterministic, no AI image-gen):

```
navigate (session-aware)  ->  set a clean aspirational state (dismiss the 18+ gate, hide
cookie/support/toast chrome, optionally type an aspirational message)  ->  capture a tight
retina shot (viewport / --selector / --anchor)  ->  soft brand frame (frame_shot.py)  ->
emit <out>_report.json  ->  VISUAL-CRITIQUE-LOOP.md
```

It reuses the proven `capture_screenshot.py` stack — patchright stealth, Cloudflare bypass, the
"I am 18…" age-gate dismissal, and retina `device_scale_factor=2` (1440×900 → 2880×1800;
phones 430×932). Frames match `render_chart_web.py` (light `#F7F8FA` canvas, soft shadow, Geist +
IBM Plex, the real composited Pleasur.ai logo).

---

## ⚠️ Account dependency (the one blocker)

PUBLIC pages (pricing / landing) need **no account** and work today. LOGGED-IN shots
(**chat, call, gallery**) need the **Pleasur.AI showcase session** — and **calls need a Standard+
plan**. Until the session is minted, `action_shot.py` on an authed preset returns
`status:"failed", reason:"session_required"` with a fix hint (it never publishes a login wall).

Mint the session **once** (idempotent), then everything authed unlocks:

```bash
S=.claude/skills/generate-visuals/scripts
# RECOMMENDED on the VPS — works for ANY login method (password / OTP / Google / Apple):
python $S/setup_auth.py --interactive --headed     # then open noVNC, log in, CLOSE the window
#   noVNC: http://100.73.44.58:6080/vnc.html  (VNC pw in CLAUDE.md)

# OR hands-off, ONLY if the showcase account is plain email+password:
python $S/setup_auth.py --email show@pleasur.ai --password '••••' --verify --print-b64

python $S/setup_auth.py --verify                   # confirm: prints "SESSION OK — logged in."
```

Session → `auth/state.json` (cookies + Supabase localStorage). **Never committed** (`auth/.gitignore`).
For cloud/auto runs, `--print-b64` emits `PLEASUR_AUTH_STATE_B64` → paste into Doppler (`pleasurai/dev`);
`capture_screenshot.py` / `action_shot.py` read it automatically.

**Showcase curation (SFW):** the showcase account is **curated by the cockpit** — seed ONE wholesome
SFW conversation, an SFW call, and an SFW image grid, then deep-link to them. We screenshot the
*real* product; we never fake UI.

---

## Capture — `action_shot.py`

```bash
# Curated preset (preferred):
python $S/action_shot.py --preset pricing  --out out.png     # public, works now
python $S/action_shot.py --preset plan_card --out out.png     # public, tight card crop
python $S/action_shot.py --preset chat     --out out.png      # needs the session
python $S/action_shot.py --preset gallery  --out out.png      # needs the session

# Generic (any page):
python $S/action_shot.py --url https://pleasur.ai/pricing --out out.png \
   --frame browser --url-bar "pleasur.ai/pricing" --caption "Simple, transparent pricing" \
   --hide ".cookie,.intercom"

# Tight crops without stable CSS (Next.js hashes classnames):
python $S/action_shot.py --url … --anchor "Standard" --padding 24 --frame plain --out card.png
#   --anchor climbs from the visible text to the surrounding CARD and clips it
#   (reuse later for a chat bubble, the call controls, a gallery tile).
```

Key flags: `--selector` (clip to CSS) · `--anchor "text"` (clip to the card around text) ·
`--padding N` · `--hide "a,b"` (display:none chrome) · `--fill "sel::text"` (type, not send) ·
`--click sel` · `--wait ms` · `--viewport WxH` · `--frame plain|browser|device|none` ·
`--caption` · `--url-bar` · `--no-logo` · `--no-auth` (public) · `--headed/--headless`.

### Frames (`frame_shot.py`)
- **plain** — rounded corners + big-soft shadow on the brand canvas. The versatile hero/tight-crop.
- **browser** — clean macOS chrome (3 dots + URL pill) above the shot. Desktop pages (pricing, gallery).
- **device** — soft phone bezel + notch around a portrait shot. **Chat / call** (mobile-first, intimate).

A dark app screenshot floating on the light canvas reads as premium SaaS marketing — and ties into
the chart-card system.

## Presets (`action_shot_presets.json`)
| preset | auth | viewport | frame | notes |
|---|---|---|---|---|
| `pricing` | public | 1440×900 | browser | works today |
| `plan_card` | public | 1440×900 | plain | anchor="Standard" tight crop, works today |
| `chat` | **session** | 430×932 | device | seed an SFW conversation, deep-link |
| `call` | **session, Standard+** | 430×932 | device | reach the call UI from a conversation (`_verify` route live) |
| `gallery` | **session** | 1440×900 | browser | curate an SFW image grid (route `/generate`, `_verify`) |

Routes for authed presets are best-guesses from the app sidebar (Home/Explore/Chat/Create/Generate/
Profile) — **confirm + tune `url`/`selector`/`steps` live the moment the account lands** (each carries
a `_verify` note).

## SFW — selective blur (`blur_explicit.py`)
The logged-in product is **predominantly explicit** (the Explore/Generate feeds are hardcore; many
persona avatars are nude). Per ndong: **don't blur the whole character — blur only the explicit
part.** `blur_explicit.py` applies a strong gaussian under a FEATHERED rounded mask (soft focus, not
a hard censor box) over just those regions, leaving the face/clothing/UI sharp:

```
# vision-specified regions (precise, for the curated set) — FRACTIONS of w/h:
python blur_explicit.py --in raw.png --out sfw.png --boxes '[[0.12,0.006,0.15,0.062]]'
# auto-detect (NudeNet) — for the future EO auto-pipeline; needs nudenet baked into the image:
python blur_explicit.py --in raw.png --out sfw.png --auto
```
Run BEFORE `frame_shot.py`. The vision critic then verifies **nothing explicit survives**.

**SFW-safe shot recipes (proven):**
- **Chat text-bubble crop** — crop to the message bubbles (the user bubble is brand-blue); no imagery, no blur. Safest hero.
- **Chat device shot** — full phone view; blur ONLY the small avatar circle in the header.
- **UI chrome** — pricing / plan-card / profile / settings: inherently SFW, no blur.
- Use a **custom, clearly-adult, wholesome showcase persona** (create one) — the default personas
  are brand-unsafe (barely-legal / submissive framing). Never build marketing on those.
- Gallery: a full grid of blurred tiles reads as "censored" — prefer a curated few or skip.

Default to the safe recipes; the vision critic hard-fails anything risqué, garbled, or off-brand —
a wasted render is cheap, a bad published visual is not.

## Integrate into the auto-pipeline (follow-up)
`run_action_shot.py` now re-exports the deterministic `action_shot.run(...)`, so
`generate_visuals.py:_handle_action_shot` already calls our engine when it dispatches an action-shot.
To make it the **default** (instead of routing to manual `/capture-visuals`), drop the
`BROWSER_USE_ENABLED` gate in `_handle_action_shot` and call `_load_run_action_shot().run(goal,
out_path, start_url=…)`; on `reason:"session_required"` attach the existing manual fallback hint.
Tracked with the broader `BLOG_AGENT_VISUALS=on` wiring.
