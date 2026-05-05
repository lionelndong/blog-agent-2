"""One-off Playwright capture for pleasur.ai/create -> Personality step."""
from __future__ import annotations

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / ".claude" / "skills" / "generate-visuals" / "auth" / "state.json"
OUT_DIR = ROOT / "content-pipeline" / "images" / "ai-boyfriend"
OUT_PATH = OUT_DIR / "action-1-navigate-to-pleasur-ai-create.png"
DEBUG_DIR = OUT_DIR / "_debug"

VIEWPORT = {"width": 1440, "height": 900}


def debug(page, name: str) -> None:
    DEBUG_DIR.mkdir(parents=True, exist_ok=True)
    p = DEBUG_DIR / f"step-{name}.png"
    page.screenshot(path=str(p), full_page=False, type="png")
    print(f"  debug: {p.name}", file=sys.stderr)


def click_card(page, label: str) -> None:
    """Click a wizard card whose visible label is `label` — climbs to the
    button ancestor so the click hits the card, not just the text node."""
    locator = page.locator(f"button:has-text('{label}')")
    locator.first.scroll_into_view_if_needed()
    locator.first.click(timeout=10_000)


def click_next(page) -> None:
    """Click the Next button, waiting for it to be enabled."""
    btn = page.get_by_role("button", name="Next", exact=True)
    btn.first.wait_for(state="visible", timeout=15_000)
    # Wait for it to be enabled (not aria-disabled / not :disabled)
    page.wait_for_function(
        """() => {
          const btns = [...document.querySelectorAll('button')].filter(b => b.textContent.trim().startsWith('Next'));
          return btns.some(b => !b.disabled && b.getAttribute('aria-disabled') !== 'true');
        }""",
        timeout=15_000,
    )
    btn.first.click(timeout=10_000)


def main() -> int:
    if not STATE_PATH.exists():
        print(f"missing auth state: {STATE_PATH}", file=sys.stderr)
        return 2
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=2,
            storage_state=str(STATE_PATH),
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
        )
        page = context.new_page()
        print("nav -> /create", file=sys.stderr)
        page.goto("https://pleasur.ai/create", wait_until="networkidle", timeout=30_000)
        page.wait_for_timeout(1500)
        debug(page, "00-loaded")

        # Dismiss any modal
        for label in ("I am 18 years of age or older", "I am 18 or older", "Yes, I am 18", "Enter site", "I agree", "Continue to site"):
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible(timeout=400):
                    print(f"dismiss: {label}", file=sys.stderr)
                    btn.first.click()
                    page.wait_for_timeout(600)
                    break
            except Exception:
                pass

        # Step 1: Basics
        print("step 1: Basics", file=sys.stderr)
        click_card(page, "Realistic")
        page.wait_for_timeout(400)
        debug(page, "01-basics-after-click")
        click_next(page)

        # Step 2: Ethnicity
        print("step 2: Ethnicity", file=sys.stderr)
        page.wait_for_timeout(1200)
        debug(page, "02-ethnicity")
        click_card(page, "Caucasian")
        page.get_by_role("button", name="Skin tone: Fair").first.click()
        page.get_by_role("button", name="21", exact=True).first.click()
        click_next(page)

        # Step 3: Hair & Eyes
        print("step 3: Hair & Eyes", file=sys.stderr)
        page.wait_for_timeout(1200)
        debug(page, "03-hair")
        # Pick first matching across both Eye + Hair sections — order matters
        # Eye color comes first; clicking 'Brown' will hit Eye Color section first
        page.locator("button:has-text('Brown')").first.click()
        page.locator("button:has-text('Brunette')").first.click()
        click_card(page, "Straight")
        click_next(page)

        # Step 4: Body
        print("step 4: Body", file=sys.stderr)
        page.wait_for_timeout(1200)
        debug(page, "04-body")
        click_card(page, "Slim")
        # Two "Small" cards: Breast first, Butt second — click both
        smalls = page.locator("button:has-text('Small')")
        n = smalls.count()
        print(f"  small variants: {n}", file=sys.stderr)
        for i in range(min(n, 2)):
            smalls.nth(i).click()
        click_next(page)

        # Step 5: Personality
        print("step 5: Personality", file=sys.stderr)
        page.wait_for_load_state("networkidle", timeout=20_000)
        page.wait_for_timeout(2000)
        try:
            page.locator("text=Character name").first.wait_for(state="visible", timeout=10_000)
        except PWTimeout:
            print("warning: Character name field not visible; capturing whatever is on screen", file=sys.stderr)
        debug(page, "05-personality")

        # Final canonical capture
        page.screenshot(path=str(OUT_PATH), full_page=False, type="png")
        size = OUT_PATH.stat().st_size if OUT_PATH.exists() else 0
        print(f"saved: {OUT_PATH} ({size} bytes)")

        context.close()
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
