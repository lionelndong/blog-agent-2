# Research Adversarial — how-to-make-an-ai-girlfriend (revision pass review)

Re-review of `content-pipeline/1-research/how-to-make-an-ai-girlfriend.md` after
the 2026-05-15 revision pass. Prior verdict was **FAIL** with three CRITICALs:
(C1) `path_comparison` numbers unsourced in `-data.json`, (C2) load-bearing
external stats (Replika 10M / "48% loneliness" / Character.AI $150M) cited only
as sibling-dossier reuse with no primary URL, (C3) "surprising findings" mostly
table-stakes. This pass audits each prior finding against the current dossier
and JSON.

## Verdict: **PASS**

## Prior CRITICAL audit

### C1 — Unsourced `path_comparison` numbers → **FIXED**
`-data.json` now carries an explicit `_meta.sources` map at L53–66 with a URL
per `path_comparison` key: `diy_gpu_hourly_usd_a100_marketplace: 0.72` →
Vast.ai vs RunPod 2026 review (velinxs Medium); `off_the_shelf_monthly_usd_low:
12.99` → AI Tipsters Candy.ai pricing review; `off_the_shelf_monthly_usd_high:
15.99` → AutoGPT.net Nomi.ai pricing review. The two fabricated integers from
the prior pass — `diy_build_weeks: 3` and `diy_gpu_cost_usd: 400` — are listed
in `_meta.dropped_for_lack_of_source` (L68–73) and replaced: weeks → verbatim
"a few weeks" from gmongaras; $400 → hourly marketplace rate. Prose mirrors
this at L58 (gmongaras quote), L64 (Candy.ai link), L68 (Vast.ai link),
L70 (Nomi.ai $15.99 link). Every load-bearing number in the cost/time thesis
now carries a primary URL. Clean.

### C2 — Sibling-cited external stats with no upstream URL → **FIXED**
Prose now has a dedicated `## External citations (corrected this pass)` block
at L75–80 that resolves all three previously-uncited claims with primary URLs:
Replika 10M installs → Sensor Tower news-feed page + ETtech reinforcement;
Character.AI $150M → CNBC (Mar 23 2023), with explicit correction that the
prior "Series B Feb 2024 Reuters" attribution was wrong (it's Series A from
a16z); Stanford/Replika study → PMC10955814 (Cerit et al., npj Mental Health
Research, Jan 2024) with the further correction that the "48% loneliness"
sibling number does not appear in the paper at all (real figures: 90% any
loneliness, 43% Severely/Very Severely Lonely). The JSON's `category_stats`
block carries the same three sources, and `dropped_for_lack_of_source` calls
out the bogus 48% explicitly. `/verify-claims` now has a clean URL per stat.
Clean.

### C3 — "Surprising findings" mostly table-stakes → **FIXED**
The dossier now has a labelled `## Surprising findings (SERP-derived,
re-verified)` H2 at L66–72 with three items, each genuinely non-obvious and
URL-backed: (1) the only DIY tutorial that ranks (gmongaras) is built on
2022 tooling (GPT-Neo 1.3B + waifu-diffusion) — three generations behind 2026
open weights; the 2026 stack swap (Llama-3-8B-Instruct + SDXL on Vast.ai
A100 spot at $0.72/hr) is itself a citation nobody on the SERP carries.
(2) No top-5 product page publishes monthly price on the marketing surface —
review sites disagree on Nomi's monthly within ±$2, and Candy.ai's `/pricing`
404'd today, sourced from a third-party review instead. (3) The sibling
"48% loneliness" stat is factually wrong against the source paper. All three
are `actually-surprising` and converted into draft hooks. Clean.

## Prior HIGH audit (drive-by)

- **Volume drift 140 vs 110 in cluster math** → fixed. L30 now explicitly
  uses live 110, computes 560, rounds to ~550 to flag the drift; the prior
  inflated ~580 is gone. Per keyword-policy-v3.
- **Strongest competitor "beat" plan vague** → fixed via Surprising finding
  #1: the wedge is now "run gmongaras's build on 2026 weights," not the
  generic "honest cost/time table."

## Findings on the current dossier

### LOW — `format_share` JSON key still never surfaces in prose
`-data.json` carries `format_share: {diy 0.27, product 0.40, social 0.27,
video 0.07}`. Prose covers the same idea qualitatively at L46–48
("three formats compete") but never quotes the percentages. Not load-bearing
— the prose narrative is intact without them — but if `/generate-visuals`
reaches for a SERP-mix chart, the writer hasn't been primed to introduce
that number in body text first. Either drop the key or thread a one-line
callout into the SERP overview. Not blocking.

### LOW — Brand-fit material remains thin on Pleasur.AI-specific capabilities
The recommended-angle block at L97–100 still closes with "Pleasur.AI's voice
can deliver the off-the-shelf recommendation honestly" but doesn't name
*which* live capability (Companion Creator's voice profile assignment, in-chat
image gen) beats Nomi or RomanticAI on a specific dimension. Brand-config
lists 2 live + 2 coming-soon pillars; `/outline` will have to invent the
product-mention mapping. Acceptable for a Friday informational, but a
HIGH-leaning LOW — flagging for `/product-mentions` rather than blocking
research.

### LOW — Deep-research file remains effectively empty
`-deep.md` is honestly empty (Perplexity returned an unrelated source set).
The dossier sourcing banner at L5 calls this out at the top now, which was
the prior critique — fixed surface. The downstream skill should still treat
external claims as carrying only the dossier's own URL load, not a
deep-research backstop.

## What works (1, to stay calibrated)

The `## External citations (corrected this pass)` block is the single
strongest addition. It doesn't just add URLs — it openly retracts two
previously-asserted "facts" (Character.AI Series B → Series A, "48%
loneliness" → does not exist in the paper) with the correct primary sources.
That's the kind of revision that turns a citation-thin dossier into one a
writer can actually draft from without `/verify-claims` blowing up.

## New CRITICALs introduced

None. The revision was scoped to the prior CRITICAL/HIGH list and didn't
introduce new load-bearing claims without sources. The two LOW items
(`format_share` JSON↔prose gap, brand-fit thinness) are non-blocking
hand-offs to downstream stages.

## Verdict reasoning

All three prior CRITICALs are concretely fixed with primary URLs inline in
the prose and mirrored in `-data.json._meta.sources`. Two prior HIGHs are
addressed. Remaining findings are LOW and non-blocking. The dossier is safe
to feed `/outline`.

## Verdict: **FAIL** → **PASS**

## Verdict: **PASS**
