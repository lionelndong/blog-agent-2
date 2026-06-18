# Visuals Adversarial — is-candy-ai-safe (revision 1 re-run)

Skeptical art-director review of visual placement against
`templates/editorial-principles-visuals.md` (ahrefs density + type diversity),
re-run after the revision pass that added three visuals and replaced the
duplicative scorecard. Each referenced asset was viewed for composition, text
artifacts, legibility, and compliance.

## Computed facts

- Prose word count (cited draft, excluding table rows and image markdown): **~1,252 words** → density band **1,200–2,000 words**.
- Density target: **8** (acceptable range **6–11**).
- Captured + referenced visuals (manifest `status=captured`, all referenced in the draft): **5**
  - Visual 1 `image` (concept-illustration) — designed pull-quote card.
  - Visual 2 `screenshot` — Pleasur.ai privacy-policy page.
  - Visual 3 `image` (concept-illustration) — 5-point safety-checklist diagram.
  - Visual 4 `chart` (matplotlib) — AI-companion regulatory-history timeline (sourced events only).
  - Visual 5 `image` (concept-illustration) — "data Candy AI collects" hub-and-spoke diagram.
- Inline markdown comparison `table` (counts as a visual element): **1**.
- **Effective visual count: 5 assets + 1 table = 6** → at the **floor** of the 6–11 range (no longer below target by 2+).
- Distinct types present: `image`, `screenshot`, `chart`, `table` = **4** (clears the ≥3 diversity floor).

The prior FAIL was pure under-density (3 effective visuals vs floor 6). The revision pass
brought the page to 6 and lifted type diversity from 3 to 4. The intermediate re-review
flagged a 4-platform "App A–D" scorecard CRITICAL twice (it duplicated the comparison table
and carried an ambiguous strong/partial/unstated dot legend); that scorecard was stripped
from the draft and replaced with the non-duplicative data-collection diagram (Visual 5).

## Findings

### LOW — Density sits at the floor, not the centre
6 visuals against a target of 8 for a 1,252-word article. The outline's visual-sanity-check
deliberately holds the intro/FAQ/conclusion to `none` to protect liftable AIO/FAQPage
surfaces — sound reasoning, and the floor is met — but there is no slack above the floor. The
~360-word comparison section and ~250-word verdict section both run long enough to justify
two visuals each; the FAQ should stay clean. No action required; this is a floor pass, not a
comfortable one.

### MEDIUM — Visual 1 (pull-quote card) is the weakest earner, flirts with decorative
It renders one sourced line ("The policy doesn't spell out its encryption posture") as a
Swiss-typography poster, but the same sentence already appears in the adjacent prose, and the
"INDEPENDENT SAFETY REVIEW 2026" attribution is a generic label (a first render fabricated a
named author, correctly killed). It shows no real thing and carries no information the prose
lacks. It sits in an analytical, not serious-stakes, spot and does break a long text wall, so
MEDIUM not CRITICAL. If anything is later cut to raise quality-density, this is the candidate.

### LOW — `image` type carries 3 of 6 slots
Type diversity is healthy (4 types), but three of the five PNGs are gpt-image-2 illustrations.
Visuals 3 and 5 each carry distinct, accurate information, so this is acceptable; noted only
because removing Visual 1 would also improve the balance.

### LOW — Visual 4 (timeline) names "one compared platform", not Replika, in-image
A deliberate non-absolutist compliance hedge; the footer disclaimer holds and the prose above
names Replika. Minor glance-friction, not a defect. No third-party logo / likeness risk.

## Visuals that earn their place

- **Visual 5 — "data Candy AI collects" hub-and-spoke (line in verdict H2):** the standout.
  Six labelled nodes (email/username, chat logs, generated images, device & IP, usage data,
  3rd-party payment) map 1:1 to the sourced Scribe collection list. Turns a prose list into a
  glanceable mental model; accurate, legible, generic icons, no logos, no people. Exactly the
  ahrefs-style concept illustration the principles ask for, and it correctly replaced the
  duplicative scorecard.
- **Visual 4 — regulatory timeline chart:** real type diversity; every node traces to a
  citation already in the draft (Italy Feb 2023 ban, FTC complaint Jan 2025 unresolved, €5M
  fine 2025). Legible, brand-neutral, self-authored (no external-capture / logo / likeness
  risk), accurate to the prose.
- **Visual 2 — Pleasur.ai privacy-policy screenshot:** proves checklist point 1 ("a published,
  readable policy") by showing the real page exists and is readable — information the prose
  cannot self-certify. Real authenticated capture, no likeness issues.

## Compliance check (all referenced visuals)

No real-person likeness, no third-party logos, no invented named people/quotes (the fabricated
author was caught and removed), no internal-stack/vendor names in any caption or alt; 18+
framing intact. Visual 3 spells all five checklist labels correctly and legibly. All pass.

## Manual fallthrough

`manual-capture.md` states "No manual visuals required." All five manifest entries are
`status=captured`; no `manual` or `failed` entries. Clean.

## Verdict: **PASS**

Density is at the floor of the acceptable range (6 effective visual elements vs floor 6, no
longer below target by 2+) with 4 distinct types. No CRITICAL is open: the verdict section is
now supported, no chart contradicts the prose, the comparison stays a real sourced table, and
the duplicative scorecard is correctly absent. The one remaining quality nag (Visual 1) is
MEDIUM, not a CRITICAL decorative-in-a-serious-section breach.
