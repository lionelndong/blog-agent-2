#!/usr/bin/env python3
"""Scene presets for the animated-demo engine.

A *scene* is a dict: url, viewport, clip (the fixed region every frame captures),
and beats. Each beat is some actions followed by either `shoot` (a held keyframe,
optionally crossfaded in) or `motion` (a burst of real frames, e.g. a scroll).

Two tiers:
  - PUBLIC (needs_auth=False): runnable right now on pleasur.ai public pages.
  - AUTH   (needs_auth=True):  the high-value in-app flows (chat, image gen, call).
    They are fully authored and ready; they just need the SHOWCASE ACCOUNT session
    (PLEASUR_AUTH_STATE_B64 / auth/state.json via setup_auth.py). Until then the
    engine reports `blocked_on_auth` instead of running them.

SFW is mandatory (adult product, public indexed blog): the auth scenes use a SFW
character + SFW prompt, and the operator must point the showcase account at a SFW
character. See `sfw` notes on each scene.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BASE = "https://pleasur.ai"


# --- PUBLIC -----------------------------------------------------------------

PRICING_TOGGLE: dict[str, Any] = {
    "name": "pricing-toggle",
    "needs_auth": False,
    "url": f"{BASE}/pricing",
    "viewport": {"width": 1280, "height": 1080},
    "dismiss_age_gate": True,
    "settle_ms": 1400,
    "fps": 12,
    "url_label": "pleasur.ai/pricing",
    "caption": "Switch Monthly ↔ Yearly — save 60%",
    "sfw": "Pricing page only. No character imagery. Fully SFW.",
    # Toggle + the three plan price cards. Crop tuned to the live layout (probed
    # in both states): toggle-top through the taller Yearly CTA, no subtitle sliver.
    # NB the page DEFAULTS to Yearly, so beat 0 clicks Monthly to set the baseline;
    # both crossfades then show a real price change (the whole point of the demo).
    "clip": {"crop": [305, 284, 920, 652]},
    "beats": [
        {"label": "monthly",
         "actions": [{"do": "click", "selector": "button:has-text('Monthly')"},
                     {"do": "wait", "ms": 700}],
         "shoot": {"hold_ms": 1500}},
        {"label": "yearly",
         "actions": [{"do": "click", "selector": "button:has-text('Yearly')"},
                     {"do": "wait", "ms": 700}],
         "shoot": {"hold_ms": 1900, "transition": "crossfade", "transition_ms": 340}},
        {"label": "back-to-monthly",
         "actions": [{"do": "click", "selector": "button:has-text('Monthly')"},
                     {"do": "wait", "ms": 700}],
         "shoot": {"hold_ms": 1200, "transition": "crossfade", "transition_ms": 340}},
    ],
}

PRICING_SCROLL: dict[str, Any] = {
    "name": "pricing-scroll",
    "needs_auth": False,
    "url": f"{BASE}/pricing",
    "viewport": {"width": 1280, "height": 860},
    "dismiss_age_gate": True,
    "settle_ms": 1400,
    "fps": 14,
    "url_label": "pleasur.ai/pricing",
    "caption": "Plans, coins & FAQ at a glance",
    "sfw": "Pricing page only. No character imagery. Fully SFW.",
    "clip": None,  # full viewport
    "beats": [
        {"label": "top", "actions": [{"do": "mouse_move", "x": 760, "y": 470},
                                     {"do": "wait", "ms": 300}],
         "shoot": {"hold_ms": 900}},
        {"label": "scroll-down",
         "motion": {"frames": 30, "interval_ms": 70,
                    "each": [{"do": "wheel", "dy": 46}]}},
        {"label": "rest", "actions": [{"do": "wait", "ms": 200}],
         "shoot": {"hold_ms": 1100}},
    ],
}


# --- AUTH-GATED (ready; need the showcase account session) ------------------

CHAT_TYPING: dict[str, Any] = {
    "name": "chat-typing",
    "needs_auth": True,
    # Operator: set this to the showcase account's SFW character chat URL.
    "url": f"{BASE}/chat",
    "viewport": {"width": 1280, "height": 900},
    "dismiss_age_gate": True,
    "settle_ms": 2000,
    "fps": 16,
    "url_label": "pleasur.ai/chat",
    "caption": "Chatting with your AI companion",
    "sfw": "Use a SFW character + SFW message. The line below is intentionally tame.",
    "clip": {"selector": "main"},
    "beats": [
        {"label": "open", "actions": [{"do": "wait", "ms": 500}], "shoot": {"hold_ms": 1000}},
        {"label": "type",
         "actions": [{"do": "type",
                      "selector": "textarea, [contenteditable='true'], input[type='text']",
                      "text": "Hey! What's your favorite way to spend a Sunday?", "delay": 55}],
         "shoot": {"hold_ms": 900}},
        {"label": "send",
         "actions": [{"do": "press",
                      "selector": "textarea, [contenteditable='true'], input[type='text']",
                      "key": "Enter"}],
         "motion": {"frames": 30, "interval_ms": 220}},
        {"label": "reply", "actions": [{"do": "wait", "ms": 400}], "shoot": {"hold_ms": 2200}},
    ],
}

IMAGE_GENERATING: dict[str, Any] = {
    "name": "image-generating",
    "needs_auth": True,
    "url": f"{BASE}/generate",
    "viewport": {"width": 1280, "height": 980},
    "dismiss_age_gate": True,
    "settle_ms": 2000,
    "fps": 14,
    "url_label": "pleasur.ai/generate",
    "caption": "Generating an image with AI",
    "sfw": "SFW prompt only. Operator must keep the generation SFW for the blog.",
    "clip": {"selector": "main"},
    "beats": [
        {"label": "prompt",
         "actions": [{"do": "type",
                      "selector": "textarea, input[type='text']",
                      "text": "a cozy sunlit cafe by the sea, watercolor", "delay": 45}],
         "shoot": {"hold_ms": 1100}},
        {"label": "generate",
         "actions": [{"do": "click", "selector": "button:has-text('Generate')"}],
         "motion": {"frames": 44, "interval_ms": 260}},
        {"label": "result", "actions": [{"do": "wait", "ms": 500}], "shoot": {"hold_ms": 2400}},
    ],
}

CALL: dict[str, Any] = {
    "name": "call",
    "needs_auth": True,  # Standard+ plan on the showcase account
    "url": f"{BASE}/chat",
    "viewport": {"width": 1280, "height": 900},
    "dismiss_age_gate": True,
    "settle_ms": 2000,
    "fps": 14,
    "url_label": "pleasur.ai",
    "caption": "Live voice call",
    "sfw": "SFW character + call screen only.",
    "clip": {"selector": "main"},
    "beats": [
        {"label": "open", "actions": [{"do": "wait", "ms": 500}], "shoot": {"hold_ms": 1000}},
        {"label": "start-call",
         "actions": [{"do": "click", "selector": "button:has-text('Call'), [aria-label*='call' i]"}],
         "motion": {"frames": 40, "interval_ms": 240}},
        {"label": "in-call", "actions": [{"do": "wait", "ms": 400}], "shoot": {"hold_ms": 2200}},
    ],
}


PRESETS: dict[str, dict[str, Any]] = {
    s["name"]: s for s in (PRICING_TOGGLE, PRICING_SCROLL, CHAT_TYPING, IMAGE_GENERATING, CALL)
}


def load_scene(name_or_path: str) -> dict[str, Any]:
    """Resolve a preset name or a path to a scene JSON file."""
    if name_or_path in PRESETS:
        # Return a shallow copy so callers can mutate (e.g. override url) safely.
        return dict(PRESETS[name_or_path])
    p = Path(name_or_path)
    if p.exists():
        scene = json.loads(p.read_text(encoding="utf-8"))
        if "name" not in scene:
            scene["name"] = p.stem
        return scene
    raise SystemExit(
        f"unknown scene {name_or_path!r}. Presets: {', '.join(sorted(PRESETS))}; "
        "or pass a path to a scene JSON file."
    )
