# Research Adversarial — ai-girlfriend-experience (revision pass review)

Re-review of `content-pipeline/1-research/ai-girlfriend-experience.md` after a
revision pass. Prior verdict was **FAIL** with three CRITICALs (uncited
load-bearing stats; missing/table-stakes "surprising findings"; strongest
competitor angle acknowledged but not beaten) plus three HIGHs (angle-shaped
JSON keys; 900 vs 720–1,200 mismatch; brand-fit thinness). This pass verifies
each prior finding against the current dossier and the JSON.

## Verdict: **PASS**

## Prior CRITICAL audit

### C1 — Load-bearing stats float without primary-source URLs → **FIXED**
The dossier now contains an explicit `## Stats dropped (no primary source in
3 attempts — do not perpetuate)` block at L72–78 that names every prior
offending claim and drops it: "525% YoY," "$2.8B → $9.5B," "Char AI 100M /
67% / $82M / 220M" (with the correct note that $82M is the *category*, not
Char AI), "45% emotional-attachment in 3 weeks," and "74% relationally
drained." The remaining load-bearing stats — Mozilla 90% / 1 of 11 / 73% /
54%, Muah.AI 1.9M emails Sept 17 2024, Char AI MAU 28M → 20M — each carry
inline primary-source URLs at L57–60 and L67–68 (Mozilla Foundation, HIBP,
Linklaters, Business of Apps, Sacra). The JSON `removed_in_revision` array
mirrors the prose drops, so a writer reaching into either artifact can't
resurrect a dead stat. Clean.

### C2 — No "3 surprising findings" section / table-stakes dressed up → **FIXED**
There is now an explicit `## 3 Surprising Findings` H2 at L62 with three
items, each tagged `actually-surprising`, each backed by a primary URL, each
with a one-line "actionable for the draft" hook. The two prior dressed-up
items ("first-person session log," "90s vs week-3 contrast") are explicitly
called out as cut at L70 with the rationale "table-stakes." The genuinely
fresh signal — the templated phrases that break the illusion ("I'm here to
support you," reflexive positivity, memory hallucination) — is now finding
#1, not buried mid-list. Clean.

### C3 — Strongest competitor angle (ourdream.ai) acknowledged, not beaten → **FIXED**
A `## Competitor evidence to absorb` table at L51–60 names the four
ourdream-cited claims the new piece must re-source independently and pairs
each with a verified primary URL and a target H2 placement (privacy / safety
closer / intro+week-three / market callout). This is exactly what the prior
critique demanded: not "narrative beats listicle" hand-wave, but a
specific list of citations to neutralise. Clean.

## Prior HIGH audit (drive-by)

- **Angle-shaped JSON keys** → fixed. `narrative_arc_phases` is gone from
  the JSON (confirmed in `removed_in_revision`).
- **900 vs 720–1,200 split** → fixed. Prose L13 declares "900/mo (point);
  720–1,200 (uncertainty band). Both prose and JSON now agree." JSON
  `primary_keyword_volume_band` matches.
- **Brand-fit thinness** → fixed. New `## Pleasur.AI hooks (brand-fit)`
  section L111–119 maps the three-act arc onto Companion Creator / Image
  Gen / in-chat Voice / in-chat Phone Call, follows brand-config rules
  (no `/voice` or `/call` link, "tap the speaker icon" / "tap the Call
  button"), and pulls reusable modules from `2-reference/`.

## Findings on the current dossier

### LOW — Two JSON-only signals never surface in prose
`mozilla_avg_trackers_per_minute: 2663` and the `search_intent_split` (55 /
40 / 5 / 0) are present in `-data.json` but neither appears in the prose
dossier. Neither is load-bearing — the prose covers intent qualitatively at
L15 and the Mozilla framing at L67 — so this won't break the draft, but if
the visuals stage reaches for a chartable number for "intent" or "tracker
volume," the writer hasn't been primed for it. Either drop these JSON keys
or surface a one-line callout in prose. Not blocking.

### LOW — `serp_format_share_observed` band stays at `0.0` for first-person narrative
Acceptable in this revision because the JSON now carries an explicit
`_methodology` note ("N=10, single search engine, Google blocked headless.
Treat as a SERP snapshot, NOT a market share") and the prose at L36 mirrors
the same caveat. The number is no longer asserted as a share. Fine to ship.

## What works (1, to stay calibrated)
The "Competitor evidence to absorb" table is the strongest single addition.
It converts the prior hand-wavy "narrative beats listicle" into a concrete,
auditable instruction for /outline and /cited-draft: which four citations
to re-source, which H2 each one anchors. That table by itself raises the
ceiling on the eventual article more than any other change in this pass.

## New CRITICALs introduced
None. The revision was scoped to the prior CRITICAL/HIGH list and didn't
break anything else along the way. Two LOW items remain (JSON↔prose
surface-area gaps), neither blocking.

## Verdict reasoning
All three prior CRITICALs are concretely fixed with inline evidence in the
current dossier and JSON. All three prior HIGHs are addressed. Remaining
findings are LOW and non-blocking. The dossier is now safe to feed
`/outline`.

## Verdict: **PASS**
