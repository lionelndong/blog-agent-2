# Visuals Adversarial — ai-companion-memory (manual)

## Stage 9b (visuals-adversarial) check

### Computed baseline

- **Word count (cited draft):** ~3,454 → >3,000-word band
- **Density target (editorial-principles-visuals.md):** 12 visuals (acceptable 10–15)
- **Captured non-`none` visuals (`manifest.json`):** 6
  - `image` ×4
  - `screenshot` ×1
  - `external` ×1
- **Distinct types present:** 3 (meets minimum diversity)
- **Naked `[VISUAL:...]` placeholders:** 0
- **Naked `[SCREENSHOT:...]` placeholders:** 0

## Findings

### 1. [CRITICAL] Visual density below target by 6
The article is in the >3,000-word band but currently has only 6 captured visuals. This is materially under the density target (12 required by rule, 10–15 acceptable), and the floor is missed by 2+.

### 2. [CRITICAL] Missing-visual gaps are section-level and specific
The following high-value sections still need visuals that materially improve scannability:

- **## How to Test an AI Companion's Memory in 5 Minutes** — still no concept or score visual in the scorecard area; add a `image` (`concept-illustration`) and/or `chart` tied to the test workflow.
- **## Which AI Companions Remember Best** — comparison section currently relies on markdown table only; add a second visual pass on top of the existing table (e.g., `image` `sub=comparison` by memory layer) or a concise chart of strengths across layers.
- **## The Privacy Side of Memory** — privacy checklist currently visualized, but missing a visual that maps retention + deletion risk flow.
- **## What "Persistent Memory" Actually Costs** — no section-level visual for plan-tier mechanics beyond prose.
- **## How to Build a Companion That Remembers You** — no companion setup flow visual before checklist.
- **Conclusion** currently unbroken by any anchor visual, which is acceptable only if there is true section-level compression elsewhere (not the case here).

### 3. [HIGH] Add density with high-value, low-risk types
Recommended minimum additions: 6 visuals total across this run.

- 2 × `image` (`sub=concept-illustration`) for sections 3, 4, 5
- 1 × `chart` using existing research rows for cost/memory/retention evidence
- 2 × `image` (`sub=diagram`) for test workflow + privacy flow
- 1 × `screenshot` of companion setup screen at a reusable static state

## Revision outcome guidance

- **Revisions remaining for visuals stage:** 1
- **Suggested action:** re-run visuals stage after adding 6 placeholders, then regenerate manifest, preview, and rerun visuals-adversarial.

## Verdict: **FAIL**
