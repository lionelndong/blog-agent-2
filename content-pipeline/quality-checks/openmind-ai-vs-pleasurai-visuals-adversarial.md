# Visuals Adversarial — openmind-ai-vs-pleasurai

Stage 9b (visuals-adversarial). Skeptical art-director review of visual placement
density and quality, post-`/generate-visuals`, pre-`/preview`.

## Computed

- **Body word count:** 2,831 (excludes "Editor notes" meta-section)
- **Density band:** 2,000–3,000 words → target **10**, acceptable range **8–13**
- **Captured visuals (`status=captured`):** 7 + 1 GFM comparison table = **8 effective**
- **Distinct types:** 4 — `external` (4), `image`/concept-illustration (2),
  `screenshot` (1), `table` (1 GFM). Target ≥3, met.
- **Trims held:** intro poster (recon #1), H2-1 generic memory-flow diagram
  (recon #2), H2-3 standalone 82%/33% bar chart (recon #3) — all absent from
  manifest and draft. **Confirmed; none reappeared.**
- **Manual fallthrough:** none (manual-capture.md: "none required").
- **Claim guardrail:** clean across all 8 — see below.

## Findings

### MEDIUM — Density sits at the band floor (8 of 10 target); two long sections run visually dark
Eight effective visuals clears the acceptable minimum but is 2 below the 10
target for a 2,800-word piece. Longest dark stretches:
- **H2-4 "the head-to-head" (~470 words, [GAIN] section):** table sits at top;
  back half ("trust layer" + OpenMind free-tier-fairness, lines 65–69) runs
  ~300 words unbroken. A `image` concept-illustration of the
  self-reported-vs-third-party asymmetry ("Company says it" vs "Outside reviewer
  says it" source badges) would anchor the page's central idea.
- **H2-6 "Who should pick which" (~310 words):** decision-split diagram at line
  97 earns its place; no second visual needed.

Not CRITICAL: 8 is inside the 8–13 acceptable range, so density does not trip
the FAIL trigger ("below target by 2+").

### MEDIUM — Crop risk on the two MariaVibe `external` clips
Both MariaVibe captures are large at `crop=padded`. `external-1`
(`selector=figure`, draft line 21, caption "memory drives nearly every positive
review") at 1558×2029 likely pulls more than the one cited line — value may be
buried. File: `images/openmind-ai-vs-pleasurai/external-1-mariavibe-line-that-memory-dri.png`.
Recommend an eyeball confirm it frames the cited sentence; if it's a full-column
dump, tighten the selector or drop it (it's the most expendable of the four —
the line is also stated in prose at line 15). `external-4` (1652×1193, the
82%/33% table row) dimensions look right for a benchmark table.

### LOW — Type mix healthy but external-heavy (4 of 8)
Four `external` clips vs 2 images / 1 screenshot / 1 table. Diversity (≥3) met.
Defensible here — attribution *is* the thesis, so showing sourced lines is
on-message. Adding the H2-4 asymmetry diagram would improve the mix to 3 images
/ 4 external. No action required.

## Visuals that genuinely earn their place

- **`image-2` CFS diagram (line 31):** explains "Conditional Field Subtraction"
  (vector retrieval → dedup filter → consistent reply, with struck-through
  discarded card). Ahrefs-style concept-illustration; explains the mechanism
  faster than prose, labels accurate. Load-bearing.
- **`external-4` MariaVibe 82%/33% benchmark table clip (line 47):** proves the
  most-cited claim by showing the actual third-party source row — reader sees
  the number in someone else's table, not ours. Right call vs the dropped
  standalone bar chart (which would have re-rendered our own version of someone
  else's number — exactly the redundancy recon #3 caught).

## Claim-guardrail audit (all 8 visuals)

- 82%/33% appears only as **MariaVibe-attributed** (alt text + table cell + diagram
  label "Third-party 82% figure"); no "validated," no fabrication. ✅
- No "exited beta" / "1 year" presented as fact in any label or table cell. ✅
- No video visual; no flat-pricing visual (brand pricing screenshot shows real
  coin-metered tiers; OpenMind clip is reviewer-reported tiers). ✅
- All SFW. ✅

## Verdict: **PASS**

No CRITICAL findings. Density at band floor (8, inside 8–13), 4 distinct types,
all 3 prior trims held, zero claim-guardrail violations, ≥2 visuals clearly
earning placement. The H2-4 asymmetry-diagram add and the external-1 crop check
are improvements, not gate-blockers.
