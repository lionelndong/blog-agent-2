# Outline Adversarial — joi-ai-alternative-2026 (Pass 1)

## Verdict: **PASS**

Pass 1 of 2 (revision budget BLOG_AGENT_OUTLINE_REVISION_BUDGET=1).

No CRITICAL findings. Compliance scaffolding holds end-to-end; the gating
concerns are competitiveness weaknesses (HIGH), not gate failures.

## Findings

### CRITICAL

- None. (See compliance verification below — all five baked-in rules hold.)

### HIGH

- **[Problem-agitate-solution arc / app sections, lines 73–190]** Agitation is
  front-loaded then dropped. After "Why people are leaving Joi AI" (lines 53–66),
  six of seven app sections (Candy, OurDream, LoveScape, Kindroid, CrushOn,
  Character AI) are described on their own merits with no callback to *which Joi
  pain* they fix. Only §3 Pleasur.ai ties back. A reader escaping a specific pain
  wants each pick scored against that pain — the middle reads like a generic
  roundup. Passes the gate; feels weak.
- **[Differentiation vs SERP top-5, lines 112/152/174 vs §3]** The outline beats
  scribehow on *coverage* (matches its 7-col table, adds a privacy axis line 199
  and a memory-first no-cap pick §3) but does not beat it on the thing the
  dossier names as the moat: first-hand "I tested across multiple sessions"
  credibility. The only first-hand proof is §3's Pleasur-only action-shot
  (line 139). The brand-reference flagged a reusable "how we tested" module
  (line 18) that the outline omits. Out-covers scribehow but doesn't
  out-*credibility* it.

### MEDIUM

- **[BLUF, line 73 "best Joi AI alternatives at a glance"]** Opener
  ("Seven apps cover almost everyone… the table shows where each one wins")
  narrates that a table follows rather than stating the answer. The load-bearing
  answer is the table itself. Minor; every other opener is genuinely BLUF.
- **[Visuals — Intro Visual 1, line 49]** "Leaving Joi AI? Pick by what you want"
  flow box duplicates the §3 memory diagram and the at-a-glance table — a
  decorative restatement of the thesis, the "delays the BLUF with a banner"
  failure (visuals principle #1). Borderline cut.
- **[Visuals — "How to switch off Joi", line 215]** This 4-step procedural
  (write down personality → rebuild → cancel → delete) defaults to `none`, but
  it's a numbered-flow diagram/image candidate per decision-steps 6/7 — and it's
  the migration GAIN no competitor has. Under-visualed exactly where a visual
  would differentiate.

### LOW

- **[MECE, lines 53–66 vs 87 vs FAQ Q2 line 235]** "Why people are leaving Joi
  AI", the table's Media-billing column, and FAQ Q2 all carry the 115-char Joi
  cap / billing explanation. Acceptable skim-vs-depth listicle redundancy, not a
  structural flaw. No SERP-covered gap is missing; privacy + migration are gaps
  the *incumbents* lack.

## Compliance Verification (CRITICAL if breached — none breached)

- **Joi 115-char cap / Neurons "reviewers/users report":** Holds. Lines 21,
  57–59, 235 frame Joi specs + Media billing as reviewer/user-reported with
  "verify current"; forbidden literal phrasings explicitly banned.
- **Pleasur.ai #3, FACT-LOCK pricing only:** Holds. Placed #3; only
  $12.99/$27.99/$49.99/~$5.20 used; poisoned $9.99/$19.99/$19/"unlimited"
  figures quarantined (line 23).
- **Memory attributed to genfindr 7.6/10:** Holds. Lines 22, 131, 236 — never a
  bare self-asserted "best."
- **No "no filter" absolutism:** Holds. §7 explicitly bans it (line 191).
- **Competitor facts "verify current":** Holds. Table cells lines 75, 85–91.

## What Works

- **[Compliance scaffolding, lines 21–26, 57–59, 131, 191, 235–236]** Every
  load-bearing risky claim (Joi specs, our pricing, memory rating) is
  pre-attributed, and the poisoned-figure quarantine is restated inline so
  /draft cannot miss it. This is a spine you can draft on without legal/brand
  risk — the strongest part of the outline.

## Recommendation

- Verdict is PASS: advance to stage 4 (/product-mentions). The two HIGH items
  (pain-callback per app section; a first-hand "how we tested" credibility
  module) are worth folding in at /draft to actually out-compete scribehow, but
  they do not block the gate.
