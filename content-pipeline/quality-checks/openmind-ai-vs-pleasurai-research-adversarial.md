# Research-Adversarial Review — openmind-ai-vs-pleasurai

Stage: 1b (research-adversarial). Slug: `openmind-ai-vs-pleasurai`. Date: 2026-06-15.
Guardrail: `content-pipeline/0-context/openmind-ai-vs-pleasurai.md` (PLE-2351, binding claim gate — treated as authoritative).

## Findings

This is a defensive dossier built atop a hard claim gate, and it largely holds. I tried to break each guardrail (a–d) and could not.

**CRITICAL — none.** The dossier consistently treats 82% as MariaVibe's reported figure (with URL), never "validated"; labels OpenMind duration self-reported with no "beta"/"1 year" cells; uses the true coin-metered tiers ($12.99 / $27.99 / $49.99, unlimited text, coins meter media, no flat $19/mo, no video); and every table cell is cited or qualitative. The first-party fact trace (step 6) is the strongest part.

**HIGH — Page leans its headline information gain on one unaudited affiliate-style blog.** Dossier lines 83/85 admit MariaVibe discloses "NO methodology / sample size," yet the recommended angle and BLUF lead with 82% as "the strongest third-party memory figure in the space." Attribution is correct, but the dossier flags the figure's weakness, not the source's low authority (same source family asserts false "video generation" for Pleasur per deep.md). Citability risk under adversarial answer-engine read.

**HIGH — Surprising findings are mostly dressed-up table-stakes.** No labeled "3 surprises" block. (1) "no OpenMind-vs-Pleasur comparison exists" = premise of the play, not a finding (dressed-up). (2) "evidence asymmetry: self-reported vs third-party" = actually-surprising, the article's real spine. (3) "OpenMind's edge is free-tier memory access, not architecture" = actually-surprising and ownable.

**MEDIUM — Volume is effectively zero.** "OpenMind AI" entity ~140/mo but the companion sense is "a tiny slice" (line 12). Honest disambiguation, but the play only earns as pure GEO citation; beat spec under-weights this strategic risk.

**MEDIUM — OpenMind half rests on a single review.** Step 6 admits OpenMind's own pricing page not re-pulled; everything is "per independent review" (roborhythms). Satisfies the "or named review" branch (not CRITICAL), but if roborhythms is wrong, the table is wrong.

**LOW — Data-consistency spot-check: clean.** JSON `pleasur_ai_pricing_monthly_usd` (12.99/27.99/49.99), `openmind_ai_pricing_monthly_usd` (0/9.99/19.99/29.99), `memory_retention_7day_pct` (82/33), `pleasur_ai_coin_grants_monthly_by_tier` (1500/5000/10000) all match prose. No orphan keys, no uncited prose numbers.

**LOW — Brand-fit thin on first-party product.** No `2-reference/` modules surfaced; Pleasur's memory *approach* ("emotional-context tracking") is described via MariaVibe, not from brand-config or the live product.

## What works

The step-6 first-party fact lock is exemplary: it re-verified `pleasur.ai/pricing` live this run, confirmed no drift vs brand-config, AND surfaced and quarantined the PLE-2320 trap (stale "$19/mo + lifetime" and "$9.99/$19.99" third-party prices), explicitly marking them FALSE for our product. Exactly the discipline the guardrail demands.

## Verdict: **PASS**
