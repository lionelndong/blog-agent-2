# Research Adversarial — what-happened-to-replika-users (revision pass 1)

Skeptical-expert re-read of `1-research/what-happened-to-replika-users.md` (plus `-deep.md`, `-data.json`, `0-context/`, `2-reference/`, `brand-config.md`) after the dossier was revised to address the 3 prior CRITICALs (C1 40M/30M anchoring, C2 v2.0 single-sourcing, C3 unsourced verbatim Reddit grief quotes). Special attention: each prior CRITICAL's resolution, disparagement/legal risk, first-party pleasur.ai verification, and the [UNVERIFIED] Semrush-balance caveat.

## Verdict: **PASS**

All three prior CRITICALs (C1, C2, C3) are genuinely resolved — not cosmetically patched. Zero remaining CRITICAL findings. The only price/feature concerns are competitor claims already hedged as "according to outlets" and downgraded off the article spine; every Pleasur.AI first-party claim carries a live this-run source (`fetched 2026-06-22`). Remaining issues are MEDIUM/LOW polish. Cleared to feed the outline.

## Prior CRITICAL resolution status

- **C1 — 40M/30M user figure anchoring: RESOLVED.** §2 now anchors 30M to Wikipedia ("In August 2024… surpassed 30 million") and 40M to Wikipedia ("Replika's user base exceeded 40 million"), with an explicit instruction "**anchor 30M + 40M to Wikipedia directly, not any mid-tier blog**." `-data.json` `replika_user_base_millions._meta` matches. The mid-tier blog (aicompanionpick.com) is no longer the anchor.
- **C2 — v2.0 update claim single-sourcing: RESOLVED.** (a) Now corroborated with three independent outlets (Roborhythms, AI Companion Pick, AIGF.love), not one. (b) Explicitly softened/downgraded: "Treat as attributed, not hard fact," demoted from spine to supporting point and framed "according to multiple companion-app outlets." Date conflict (April vs late-May 2026) disclosed honestly.
- **C3 — unsourced verbatim Reddit grief quotes: RESOLVED.** The two verbatim grief lines are removed. §5 now uses cited/documented reaction (TechXplore, Rob Brooks, peer-reviewed Socius study) plus a forward guardrail barring reintroduction of unsourced verbatim Reddit quotes. The only permitted direct quote is the cited Vice "losing a best friend… crying" line.

## Findings

### MEDIUM
- **M1 — Replika five-tier pricing is a competitor-feature claim with no first-party trace.** §2 / JSON `claimed_changes` asserts Replika "expanded pricing to five tiers (Free, Pro, Ultra, Platinum, MAX)," sourced only to the three companion-app blogs — none is Replika's own pricing page fetched this run. Graded MEDIUM not CRITICAL only because the dossier already downgraded the whole v2.0 block to attributed/supporting and tells the writer not to rest the argument on the feature list. The writer MUST keep the "according to outlets" hedge and not state the tier names as fact.
- **M2 — One prose figure absent from JSON.** Spot-check: `garante_fine_eur_millions.april_2025_fine: 5` ✓, `lobotomy_post_upvotes: 8700` ✓, `pleasur_ai_pricing_monthly_usd` ✓. But the per-action metering (image 10 / voice 10 / phone 50 coins) in prose §4 has no JSON key. `/verify-claims` keys off JSON, so it slips through unverified — load-bearing pricing/coins are present, so minor.

### LOW
- **L1 — Keyword volume/KD marked [UNVERIFIED] (Semrush zero-balance): acceptable degradation, NOT a blocker.** Outline-binding inputs (word/section counts, table usage, competitor angles, consensus topics) were rebuilt from live Firecrawl/WebFetch. Backfill volume on a later run.
- **L2 — feltreal.org cited for timeline (ERP removal, legacy v01.31-23):** redundantly corroborated by Wikipedia, so not sole-sourcing — acceptable.
- **L3 — Deep-research pass added nothing load-bearing.** Dossier honestly flags this; real VoC came from live search. No false confidence.
- **L4 — First-party fact trace clean.** §4 records all three pleasur.ai tiers + coin allowances + per-action metering with `source: https://pleasur.ai/pricing (fetched 2026-06-22)`, mirrored in `-data.json` `_meta.fetched`. Honors the "no $19/mo, not unlimited" guardrail. No own-product price/feature claim lacks a live this-run source.
- **L5 — Strongest competitor angle captured with a beat-plan.** aicompanionpick.com (~2,561 words, 6 tables, 5 ranked alts + FAQ) named as "the page to beat," with a concrete information-gain plan: match structure + add a fully-cited timeline table and feature-stability checklist.

## What works
The C3 fix is exemplary: §5 not only removed the fabrication/defamation hazard but installed a forward guardrail ("Never reintroduce an unsourced verbatim Reddit quote") and pinned the single legal-safe quote to a real Vice URL, with the peer-reviewed Socius study as the defamation-safe anchor for "users felt betrayed." For a disparagement-sensitive article, that is the right legal posture.
