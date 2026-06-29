#!/usr/bin/env python3
"""Capture a clean, aspirational LOGGED-IN product action-shot for the blog (2026-06-28).

This is visual type C — the PRODUCT ACTION-SHOT: a tight, on-brand in-app screenshot (a chat with
a persona, a call screen, an image gallery). Screenshots are ~60% of a product blog's images, so
this is the biggest visual. Pipeline:

  navigate (session-aware) -> set a clean aspirational state (dismiss gates, hide chrome/toasts,
  optionally type an aspirational message) -> capture a tight retina shot -> soft brand frame
  (frame_shot.py) -> emit a critique report.

It reuses the PROVEN capture stack: patchright stealth + Cloudflare bypass + the 18+ age-gate
dismissal + retina device_scale_factor=2, and the session minted by setup_auth.py
(auth/state.json or PLEASUR_AUTH_STATE_B64). Public pages (pricing/landing/explore) need no
account; chat/call/gallery require the showcase login (Standard+ for calls).

SFW ONLY. Action-shot states are curated to be safe-for-work and on-brand; the vision critique
loop (VISUAL-CRITIQUE-LOOP.md) is the backstop.

Usage (generic):
  python action_shot.py --url https://pleasur.ai/pricing --out out.png \
     [--selector ".plan-card"] [--padding 28] [--hide ".cookie,.intercom"] \
     [--fill "textarea::Tell me about your day "] [--click ".tab-yearly"] [--wait 1200] \
     [--viewport 1440x900] [--frame plain|browser|device|none] [--caption "..."] \
     [--url-bar "pleasur.ai/pricing"] [--no-logo] [--no-auth] [--headed]

Usage (curated preset):
  python action_shot.py --preset chat   --out out.png   # needs the showcase session
  python action_shot.py --preset pricing --out out.png  # public, works now
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import capture_screenshot as cs  # proven engine: auth resolver, modal texts, CF + quality helpers  # noqa: E402
import frame_shot  # noqa: E402

PRESETS_FILE = SCRIPT_DIR / "action_shot_presets.json"
LOGIN_HINTS = cs.LOGIN_URL_HINTS

# In-browser SFW pass: blur the explicit IMAGE tiles/avatars in place (keep UI text/labels sharp),
# so a real explicit surface (explore/generate/create/chat) becomes a usable SFW product shot.
# Targets <img>/<video> above `min` px; skips logos/icons. clip-path contains the blur to the box.
BLUR_IMAGES_JS = """
(min) => {
  let n = 0;
  document.querySelectorAll('img, video').forEach(el => {
    const r = el.getBoundingClientRect();
    const s = ((el.currentSrc||el.src||'') + ' ' + (el.alt||'')).toLowerCase();
    if (r.width >= min && r.height >= min && !/logo|icon|wordmark/.test(s)) {
      const px = Math.max(26, Math.round(Math.min(r.width, r.height) / 5));
      el.style.setProperty('filter', 'blur(' + px + 'px)', 'important');
      el.style.setProperty('clip-path', 'inset(0)', 'important');
      n++;
    }
  });
  return n;
}
"""


# ---------------------------------------------------------------------------
# Preset + step resolution
# ---------------------------------------------------------------------------

def _load_presets() -> dict[str, Any]:
    if PRESETS_FILE.exists():
        try:
            return json.loads(PRESETS_FILE.read_text(encoding="utf-8"))
        except Exception as exc:
            sys.stderr.write(f"warning: presets unreadable: {exc}\n")
    return {}


def _parse_viewport(spec: str | None) -> dict[str, int]:
    if spec:
        try:
            w, h = spec.lower().split("x")
            return {"width": int(w), "height": int(h)}
        except Exception:
            sys.stderr.write(f"warning: bad --viewport '{spec}'; using default\n")
    return dict(cs.VIEWPORT)


def _cli_steps(args) -> list[dict[str, Any]]:
    """Translate the simple --hide/--click/--fill/--wait/--scroll flags into recipe steps."""
    steps: list[dict[str, Any]] = []
    for sel in args.click or []:
        steps.append({"click": sel, "optional": True})
    if args.fill:
        sel, _, text = args.fill.partition("::")
        if sel:
            steps.append({"fill": {"selector": sel, "text": text}})
    if args.hide:
        steps.append({"hide": [s.strip() for s in args.hide.split(",") if s.strip()]})
    for sel in args.scroll or []:
        steps.append({"scroll_into_view": sel})
    if args.wait:
        steps.append({"wait": args.wait})
    return steps


# ---------------------------------------------------------------------------
# Browser recipe runner (session-aware) — reuses cs constants/helpers
# ---------------------------------------------------------------------------

def _dismiss_modals(page) -> bool:
    import re
    dismissed = False
    for text in cs.KNOWN_MODAL_DISMISS_TEXTS:
        try:
            loc = page.locator("button", has_text=re.compile(re.escape(text), re.I))
            if loc.count() == 0:
                loc = page.locator("[role='button']", has_text=re.compile(re.escape(text), re.I))
            if loc.count() == 0:
                continue
            first = loc.first
            first.wait_for(state="visible", timeout=1500)
            first.click(timeout=2500, force=True)
            page.wait_for_timeout(700)
            dismissed = True
            sys.stderr.write(f"info: dismissed modal '{text}'\n")
            break
        except Exception:
            continue
    return dismissed


def _wait_out_cloudflare(page) -> str:
    title = ""
    try:
        title = (page.title() or "").lower()
    except Exception:
        pass
    if any(h in title for h in cs.CF_TITLE_HINTS):
        for _ in range(20):
            page.wait_for_timeout(2000)
            try:
                title = (page.title() or "").lower()
            except Exception:
                pass
            if not any(h in title for h in cs.CF_TITLE_HINTS):
                break
    return title


def _run_step(page, step: dict[str, Any]) -> None:
    if "goto" in step:
        page.goto(step["goto"], wait_until="domcontentloaded", timeout=45000)
        page.wait_for_load_state("load", timeout=15000)
        page.wait_for_timeout(1500)
    elif "wait" in step:
        page.wait_for_timeout(int(step["wait"]))
    elif "click" in step:
        try:
            page.locator(step["click"]).first.click(timeout=6000)
            page.wait_for_timeout(800)
        except Exception as exc:
            if not step.get("optional"):
                raise
            sys.stderr.write(f"info: optional click '{step['click']}' skipped: {exc}\n")
    elif "fill" in step:
        f = step["fill"]
        page.locator(f["selector"]).first.fill(f.get("text", ""), timeout=6000)
        page.wait_for_timeout(400)
    elif "hide" in step:
        page.evaluate(
            """(sels)=>{sels.forEach(s=>{document.querySelectorAll(s).forEach(e=>{
                 e.style.setProperty('display','none','important');});});}""",
            step["hide"],
        )
        page.wait_for_timeout(200)
    elif "scroll_into_view" in step:
        try:
            page.locator(step["scroll_into_view"]).first.scroll_into_view_if_needed(timeout=5000)
            page.wait_for_timeout(400)
        except Exception:
            pass
    elif "eval" in step:
        page.evaluate(step["eval"])
        page.wait_for_timeout(300)


def _anchor_bbox(page, text: str, wmin: int = 240, wmax: int = 560) -> dict[str, float] | None:
    """Climb from the deepest element containing `text` to a card-sized ancestor; return its bbox.

    A robust way to clip product UI (a plan card, a chat bubble, the call controls) without
    relying on Next.js hashed classnames — anchor on visible text, grab the surrounding card.
    """
    js = """([label,wmin,wmax])=>{
      const hit=[...document.querySelectorAll('h1,h2,h3,h4,h5,span,div,p,button,article,li')]
        .filter(e=>((e.textContent||'').trim()).includes(label) && e.getBoundingClientRect().width>0);
      // deepest = the one with no child also containing the label
      let leaf=hit.find(e=>![...e.children].some(c=>((c.textContent||'').trim()).includes(label)))||hit[hit.length-1];
      if(!leaf) return null;
      let e=leaf, best=null;
      for(let i=0;i<9&&e;i++){const r=e.getBoundingClientRect();
        if(r.width>=wmin && r.width<=wmax && r.height>=r.width*0.55){best={x:r.x,y:r.y,width:r.width,height:r.height};break;}
        e=e.parentElement;}
      if(!best){const r=leaf.getBoundingClientRect();best={x:r.x,y:r.y,width:r.width,height:r.height};}
      return best;
    }"""
    try:
        return page.evaluate(js, [text, wmin, wmax])
    except Exception:
        return None


def _save_padded_crop(page, out_path: Path, bbox: dict[str, float], padding: int) -> None:
    """Full-page screenshot then PIL-crop to `bbox` expanded by `padding` CSS px (DSF-aware)."""
    from PIL import Image
    tmp_full = out_path.with_suffix(".full.png")
    page.screenshot(path=str(tmp_full), full_page=True)
    try:
        sf = cs.DEVICE_SCALE_FACTOR
        x0 = max(0, int((bbox["x"] - padding) * sf))
        y0 = max(0, int((bbox["y"] - padding) * sf))
        x1 = int((bbox["x"] + bbox["width"] + padding) * sf)
        y1 = int((bbox["y"] + bbox["height"] + padding) * sf)
        with Image.open(tmp_full) as img:
            img.crop((x0, y0, min(x1, img.width), min(y1, img.height))).save(out_path)
    finally:
        tmp_full.unlink(missing_ok=True)


def capture_raw(
    *,
    url: str,
    out_path: Path,
    selector: str | None,
    padding: int,
    steps: list[dict[str, Any]],
    viewport: dict[str, int],
    use_auth: bool,
    headed: bool,
    auth_required: bool,
    anchor: str | None = None,
    anchor_wmin: int = 240,
    anchor_wmax: int = 560,
    blur_images: int | None = None,
) -> dict[str, Any]:
    """Drive the session-aware browser through the recipe and capture a raw retina PNG."""
    try:
        from patchright.sync_api import sync_playwright
        using_patchright = True
    except ImportError:
        try:
            from playwright.sync_api import sync_playwright
            using_patchright = False
        except ImportError:
            return {"status": "failed", "reason": "no_browser_engine",
                    "hint": "pip install patchright && patchright install chromium"}

    auth_state = cs._resolve_auth_state() if use_auth else None
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        ctx_kwargs: dict[str, Any] = {
            "viewport": viewport,
            "device_scale_factor": cs.DEVICE_SCALE_FACTOR,
            "locale": "en-US",
            "timezone_id": "America/New_York",
        }
        if not using_patchright:
            ctx_kwargs["user_agent"] = cs.DEFAULT_USER_AGENT
        if auth_state:
            ctx_kwargs["storage_state"] = auth_state

        if using_patchright:
            browser = p.chromium.launch(headless=not headed)
        else:
            try:
                browser = p.chromium.launch(channel="chrome", headless=not headed,
                                            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
            except Exception:
                browser = p.chromium.launch(headless=not headed, args=["--no-sandbox"])
        context = browser.new_context(**ctx_kwargs)
        if not using_patchright:
            context.add_init_script(cs.STEALTH_INIT_JS)
        page = context.new_page()

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_load_state("load", timeout=15000)
            page.wait_for_timeout(2000)
        except Exception as exc:
            browser.close()
            return {"status": "failed", "reason": "navigation_failed", "error": str(exc), "url": url}

        cf_title = _wait_out_cloudflare(page)
        if any(h in cf_title for h in cs.CF_TITLE_HINTS):
            browser.close()
            return {"status": "failed", "reason": "cloudflare_challenge_unresolved",
                    "url": url, "final_url": page.url, "auth_used": auth_state is not None}

        page.wait_for_timeout(1200)
        _dismiss_modals(page)

        # Run the curated recipe steps
        try:
            for step in steps:
                _run_step(page, step)
        except Exception as exc:
            browser.close()
            return {"status": "failed", "reason": "recipe_step_failed", "error": str(exc), "url": url,
                    "final_url": page.url, "auth_used": auth_state is not None}

        final_url = page.url
        login_redirect = (
            any(h in final_url.lower() for h in LOGIN_HINTS)
            and not any(h in url.lower() for h in LOGIN_HINTS)
        )
        logged_out = login_redirect
        if auth_required and not logged_out:
            # Some apps show a login WALL without changing the URL — detect logged-out CTAs.
            try:
                ctas = page.evaluate(
                    """(texts)=>{const els=[...document.querySelectorAll('a,button,[role=button]')];
                        return els.filter(e=>{const t=(e.textContent||'').trim().toLowerCase();
                          return texts.some(x=>t===x);}).length;}""",
                    ["join free", "sign up free", "log in", "login", "sign in"],
                )
                logged_out = isinstance(ctas, int) and ctas > 0
            except Exception:
                pass
        if auth_required and logged_out:
            # The defining signal that the showcase session is missing/expired.
            try:
                page.screenshot(path=str(out_path))
            except Exception:
                pass
            browser.close()
            return {
                "status": "failed",
                "reason": "session_required",
                "url": url,
                "final_url": final_url,
                "auth_used": auth_state is not None,
                "login_redirect": login_redirect,
                "logged_out": True,
                "hint": "This page needs the Pleasur.AI showcase login. Run setup_auth.py "
                        "(--email/--password or --interactive) to mint auth/state.json, then retry.",
            }

        # SFW pass: blur explicit image tiles/avatars in-browser before capture (UI stays sharp)
        if blur_images:
            try:
                n = page.evaluate(BLUR_IMAGES_JS, blur_images)
                sys.stderr.write(f"info: blurred {n} image element(s) >= {blur_images}px\n")
                page.wait_for_timeout(450)
            except Exception as exc:
                sys.stderr.write(f"warning: blur_images failed: {exc}\n")

        page.wait_for_timeout(600)
        try:
            if selector:
                loc = page.locator(selector).first
                try:
                    loc.scroll_into_view_if_needed(timeout=5000)
                    page.wait_for_timeout(400)
                except Exception:
                    pass
                bbox = loc.bounding_box() if (padding and padding > 0) else None
                if bbox:
                    _save_padded_crop(page, out_path, bbox, padding)
                else:
                    loc.screenshot(path=str(out_path))
            elif anchor:
                bbox = _anchor_bbox(page, anchor, anchor_wmin, anchor_wmax)
                if bbox:
                    _save_padded_crop(page, out_path, bbox, padding or 22)
                else:
                    sys.stderr.write(f"warning: anchor '{anchor}' not found; capturing viewport\n")
                    page.screenshot(path=str(out_path), full_page=False)
            else:
                page.screenshot(path=str(out_path), full_page=False)
        except Exception as exc:
            browser.close()
            return {"status": "failed", "reason": "screenshot_failed", "error": str(exc),
                    "url": url, "final_url": final_url}

        browser.close()

    quality = cs._check_quality(out_path, final_url=final_url, expected_url=url, used_selector=bool(selector))
    if quality["status"] == "failed":
        return {"status": "failed", "reason": quality["reason"], "quality": quality,
                "url": url, "final_url": final_url, "auth_used": auth_state is not None}
    return {"status": "captured", "path": str(out_path), "url": url, "final_url": final_url,
            "auth_used": auth_state is not None, "login_redirect": login_redirect, "quality": quality}


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def action_shot(opts: dict[str, Any]) -> dict[str, Any]:
    """Capture + frame one action-shot. `opts` is a resolved preset/CLI dict."""
    out_path = Path(opts["out"]).resolve()
    raw_path = Path(opts["raw_out"]).resolve() if opts.get("raw_out") else out_path.with_suffix(".raw.png")

    raw = capture_raw(
        url=opts["url"],
        out_path=raw_path,
        selector=opts.get("selector"),
        padding=int(opts.get("padding") or 0),
        steps=opts.get("steps") or [],
        viewport=opts["viewport"],
        use_auth=opts.get("use_auth", True),
        headed=opts.get("headed", True),
        auth_required=opts.get("auth_required", False),
        anchor=opts.get("anchor"),
        anchor_wmin=int(opts.get("anchor_wmin") or 240),
        anchor_wmax=int(opts.get("anchor_wmax") or 560),
        blur_images=int(opts["blur_images"]) if opts.get("blur_images") else None,
    )

    report = {
        "preset": opts.get("preset"),
        "url": opts["url"],
        "final_url": raw.get("final_url"),
        "auth_required": opts.get("auth_required", False),
        "auth_used": raw.get("auth_used"),
        "login_redirect": raw.get("login_redirect"),
        "selector": opts.get("selector"),
        "frame": opts.get("frame"),
        "caption": opts.get("caption") or None,
        "viewport": opts["viewport"],
        "sfw": True,
        "raw_dims": raw.get("quality", {}).get("width") and
                    [raw["quality"]["width"], raw["quality"]["height"]],
        "steps_ran": len(opts.get("steps") or []),
    }

    if raw["status"] != "captured":
        result = {**raw, "report": report}
        _write_report(out_path, result)
        return result

    frame_kind = opts.get("frame") or "plain"
    if frame_kind == "none":
        # No polish — the raw retina shot is the deliverable.
        try:
            raw_path.replace(out_path)
        except Exception:
            out_path.write_bytes(raw_path.read_bytes())
        result = {"status": "captured", "path": str(out_path), "frame": "none",
                  "raw_path": None, "report": report}
        _write_report(out_path, result)
        return result

    framed = frame_shot.frame(
        raw_path, out_path,
        frame=frame_kind,
        caption=opts.get("caption") or "",
        url_bar=opts.get("url_bar") or "",
        max_width=int(opts.get("max_width") or (430 if frame_kind == "device" else 1180)),
        logo=opts.get("logo", True),
    )
    if framed.get("status") != "framed":
        result = {**framed, "raw_path": str(raw_path), "report": report}
        _write_report(out_path, result)
        return result

    report["out_dims"] = framed.get("out_dims")
    report["raw_dims"] = framed.get("src_dims")
    result = {
        "status": "captured",
        "path": str(out_path),
        "raw_path": str(raw_path) if opts.get("keep_raw", True) else None,
        "frame": frame_kind,
        "report": report,
    }
    _write_report(out_path, result)
    return result


def _write_report(out_path: Path, result: dict[str, Any]) -> None:
    """Persist a sidecar report for the VISUAL-CRITIQUE-LOOP deterministic stage."""
    rp = out_path.with_name(out_path.stem + "_report.json")
    try:
        rp.write_text(json.dumps(result.get("report", result), indent=2), encoding="utf-8")
    except Exception as exc:
        sys.stderr.write(f"warning: could not write report: {exc}\n")


def resolve_opts(args) -> dict[str, Any]:
    """Merge a named preset (if any) with CLI flags. CLI overrides preset."""
    opts: dict[str, Any] = {}
    if args.preset:
        presets = _load_presets()
        if args.preset not in presets:
            raise SystemExit(f"unknown preset '{args.preset}'. Known: {', '.join(sorted(presets)) or '(none)'}")
        opts.update(presets[args.preset])
        opts["preset"] = args.preset

    # CLI overrides
    if args.url:
        opts["url"] = args.url
    if args.selector is not None:
        opts["selector"] = args.selector
    if args.anchor is not None:
        opts["anchor"] = args.anchor
    if args.blur_images is not None:
        opts["blur_images"] = args.blur_images
    if args.anchor_wmin is not None:
        opts["anchor_wmin"] = args.anchor_wmin
    if args.anchor_wmax is not None:
        opts["anchor_wmax"] = args.anchor_wmax
    if args.padding is not None:
        opts["padding"] = args.padding
    if args.frame is not None:
        opts["frame"] = args.frame
    if args.caption is not None:
        opts["caption"] = args.caption
    if args.url_bar is not None:
        opts["url_bar"] = args.url_bar
    if args.viewport is not None:
        opts["viewport"] = _parse_viewport(args.viewport)
    if args.max_width is not None:
        opts["max_width"] = args.max_width
    if args.no_auth:
        opts["use_auth"] = False
        opts["auth_required"] = False
    if args.no_logo:
        opts["logo"] = False
    if args.headed:
        opts["headed"] = True
    if args.headless:
        opts["headed"] = False

    # Defaults
    opts.setdefault("viewport", dict(cs.VIEWPORT))
    if isinstance(opts.get("viewport"), str):
        opts["viewport"] = _parse_viewport(opts["viewport"])
    opts.setdefault("frame", "plain")
    opts.setdefault("use_auth", True)
    opts.setdefault("auth_required", False)
    opts.setdefault("headed", True)
    opts.setdefault("logo", True)
    opts["out"] = args.out
    if args.raw_out:
        opts["raw_out"] = args.raw_out

    # Recipe = preset steps (already present) + CLI-appended steps
    steps = list(opts.get("steps") or [])
    steps.extend(_cli_steps(args))
    opts["steps"] = steps

    if not opts.get("url"):
        raise SystemExit("no URL: pass --url or a --preset that defines one")
    return opts


# ---------------------------------------------------------------------------
# Dispatcher compatibility shim (generate_visuals.py -> run_action_shot.run)
# ---------------------------------------------------------------------------

_GOAL_PRESET_KEYWORDS = ("chat", "call", "gallery", "explore", "pricing", "landing", "generate")


def run(goal: str, out_path, *, start_url: str | None = None,
        max_steps: int | None = None, llm: str | None = None) -> dict[str, Any]:
    """Deterministic replacement for the old Browser-Use Cloud path.

    Maps a freeform `goal` to a curated preset when a keyword matches; otherwise does a plain
    framed capture of `start_url`. Keeps the signature generate_visuals._handle_action_shot calls.
    """
    presets = _load_presets()
    chosen = next((k for k in _GOAL_PRESET_KEYWORDS if k in (goal or "").lower() and k in presets), None)
    opts: dict[str, Any] = {}
    if chosen:
        opts.update(presets[chosen])
        opts["preset"] = chosen
    if start_url:
        opts["url"] = start_url
    opts.setdefault("viewport", dict(cs.VIEWPORT))
    if isinstance(opts.get("viewport"), str):
        opts["viewport"] = _parse_viewport(opts["viewport"])
    opts.setdefault("frame", "plain")
    opts.setdefault("use_auth", True)
    opts.setdefault("auth_required", bool(chosen in ("chat", "call", "gallery", "generate")))
    opts.setdefault("headed", True)
    opts.setdefault("logo", True)
    opts.setdefault("caption", goal if not chosen else opts.get("caption", ""))
    opts["out"] = str(out_path)
    opts.setdefault("steps", list(opts.get("steps") or []))
    if not opts.get("url"):
        return {"status": "failed", "reason": "no_url_or_preset", "goal": goal}
    return action_shot(opts)


def main() -> int:
    ap = argparse.ArgumentParser(description="Capture an on-brand product action-shot.")
    ap.add_argument("--preset", default=None, help="named curated preset (action_shot_presets.json)")
    ap.add_argument("--url", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--raw-out", dest="raw_out", default=None, help="also keep the unframed raw PNG here")
    ap.add_argument("--selector", default=None, help="CSS selector to clip the capture to")
    ap.add_argument("--anchor", default=None,
                    help="clip to the card-sized ancestor around this visible text (no stable CSS needed)")
    ap.add_argument("--anchor-wmin", dest="anchor_wmin", type=int, default=None, help="min card width px (anchor)")
    ap.add_argument("--anchor-wmax", dest="anchor_wmax", type=int, default=None, help="max card width px (anchor)")
    ap.add_argument("--padding", type=int, default=None, help="pad the selector/anchor bbox by N CSS px")
    ap.add_argument("--blur-images", dest="blur_images", type=int, default=None,
                    help="SFW pass: blur explicit img/video tiles >= N px in-browser (UI stays sharp). Try 60 for grids, 40 for chat avatars.")
    ap.add_argument("--hide", default=None, help="comma-separated CSS selectors to display:none pre-capture")
    ap.add_argument("--click", action="append", default=None, help="CSS to click (repeatable)")
    ap.add_argument("--fill", default=None, help="'selector::text' to type into a composer (not sent)")
    ap.add_argument("--scroll", action="append", default=None, help="CSS to scroll into view (repeatable)")
    ap.add_argument("--wait", type=int, default=None, help="settle wait (ms) at the end of the recipe")
    ap.add_argument("--viewport", default=None, help="WxH, e.g. 1440x900 (phones: 430x932)")
    ap.add_argument("--frame", default=None, choices=["plain", "browser", "device", "none"])
    ap.add_argument("--caption", default=None)
    ap.add_argument("--url-bar", dest="url_bar", default=None)
    ap.add_argument("--max-width", dest="max_width", type=int, default=None)
    ap.add_argument("--no-logo", dest="no_logo", action="store_true")
    ap.add_argument("--no-auth", dest="no_auth", action="store_true", help="skip the session (public pages)")
    ap.add_argument("--headed", action="store_true", help="visible browser (default; needed for Cloudflare)")
    ap.add_argument("--headless", action="store_true", help="force headless (frame render / public pages)")
    args = ap.parse_args()

    opts = resolve_opts(args)
    result = action_shot(opts)
    json.dump({k: v for k, v in result.items() if k != "report"}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if str(result.get("status", "")).startswith("captured") else 1


if __name__ == "__main__":
    sys.exit(main())
