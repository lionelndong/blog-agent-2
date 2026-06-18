# Research Adversarial Review: ai-companion-pricing-guide-2026

Stage 1b adversarial pushback on the research dossier before it feeds `/outline`.
Inputs reviewed: `1-research/ai-companion-pricing-guide-2026.md`, `-deep.md`,
`-data.json`, `0-context/ai-companion-pricing-guide-2026.md`, `brand-config.md`.

## Findings

**1. [HIGH] First-party pricing trace is asserted, not evidenced as a fresh fetch.**
Line 74 claims `source: https://pleasur.ai/pricing (fetched 2026-06-16)` and states the
live page matches the brief and the brand-config canonical block exactly. But every figure
($12.99/1,500; $27.99/5,000; $49.99/10,000; 10/10/50 coins) is identical to brand-config's
canonical block and the context file, and the deep-research file independently sources the
same numbers to *nsfwcaptain.com*, not pleasur.ai. There is no fetch artifact, response
snippet, or differentiating detail proving an actual `pleasur.ai/pricing` GET happened this
run vs. transcribing the canonical block and stamping today's date. The numbers are CORRECT
and rail-compliant (so not CRITICAL), but per PLE-2330's "stale-by-default, re-confirm live"
standard, an unverifiable "trust me, I fetched it" is a HIGH weakness.

**2. [MEDIUM] Two of three "surprising findings" collapse into one real idea.**
- "Metering is universal but unadmitted" (line 112): `actually-surprising` — genuine info-gain hook.
- "Annual-billing distortion" (line 113): `dressed-up-table-stakes` — obvious to any SaaS buyer.
- "Coin depletion is the silent surprise" (line 114): `dressed-up-table-stakes` — restates #1.

**3. [MEDIUM] Strongest competitor angle identified but the beat is generic.**
The incumbent's strongest asset is its first-person spend diary ("$637 over 11 months,"
lines 48/52) — lived evidence that earns citations. The dossier acknowledges it but its three
info-gains (table-with-pleasur.ai, Model column, calculation method) are all structural, not
experiential. The beat spec never asks the writer for first-hand or fresh spend data, so we
may out-organize the incumbent and still lose the citation to the page that *felt* real.

**4. [LOW] Competitor prices are properly attributed and dated — but all trace to one source.**
Every competitor figure (lines 90–106; JSON `competitor_entry_monthly_usd`) is sourced to
`aicompanionguides.com ... March 2026` (Firecrawl 2026-06-16) and explicitly labeled "dated,
not independently re-verified per-vendor." This SATISFIES the rail (sourced + dated, nothing
invented). Residual risk: no competitor cell is cross-checked against the vendor's own page;
dossier defers this to `/verify-claims` (line 88) — acceptable, but the writer must not
present these as independently verified.

**5. [LOW] Coin-metered "phone call" worked example describes a not-yet-live feature.**
The 50-coins/min phone-call example (line 131) uses a price point for a feature brand-config
(lines 36–72) marks `coming-soon`/`roadmap`. Product-mentions must respect Voice/Phone/Video
status and not imply it is live-priced today.

**6. [LOW] Data consistency: JSON ↔ prose are consistent.**
Spot-checks pass: `candy_ai: 12.99` = line 96; `pleasurai standard: 5000` = line 79;
`images_per_tier 150/500/1000` = line 131. One minor asymmetry: prose adds Replika
$299.99 lifetime (line 92) absent from the JSON — not load-bearing.

## What works

Stale-figure quarantine is exemplary. The "$19/mo tier" (pulsemate.ai, line 84) and
"premium video generation" (mariavibe.com, line 115) claims from the deep-research file are
explicitly recorded WITH sources, flagged `[UNVERIFIED]`, and the BEAT SPEC (lines 123–137)
carries NEITHER into the pricing table or required topics. No "flat / no metering / unlimited"
framing for pleasur.ai appears anywhere; pricing matches the verified brief exactly
(Starter $12.99/1500, Standard $27.99/5000, Ultimate $49.99/10000; no $19 tier). This is the
exact PLE-2330 discipline the rails demand.

## Verdict: **PASS**
