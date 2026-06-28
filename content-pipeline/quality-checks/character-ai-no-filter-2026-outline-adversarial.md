# Outline Adversarial — character-ai-no-filter-2026 (Pass 2)

## Verdict: **PASS**

Pass 2 of 2 (revision budget BLOG_AGENT_OUTLINE_REVISION_BUDGET=1).

This is the post-revision re-run. The prior FAIL (Pass 1) raised 1 CRITICAL +
2 HIGH; all three are resolved (see below) and no new CRITICAL exists, so the
fair one-revision-budget bar is met: advance.

## Prior-finding resolution

- **(a) Table vs how-to-choose MECE — RESOLVED (Y).** The table section
  (lines 83-87) now explicitly OWNS axis definitions and the hero-price /
  metering caveat, with a hard "draft must not write the criteria rationale
  twice" guard. How-to-choose (lines 171-180) is a pure if-you-want-X-pick-Y
  decision procedure that references the axes in one clause and never
  re-derives them. The two visuals are distinct (axis-free decision-tree flow
  vs. the table). No overlap remains — this is the durable fix for the prior
  CRITICAL.
- **(b) Visual count raised to ~8 honestly — RESOLVED (Y).** 8 non-`none`
  visuals (line 255), screenshots scoped only to confirmed-live pages
  (Pleasur.ai own UI, CrushOn pricing, DreamGen pricing — all marked CONFIRMED
  LIVE in the dossier). Candy (404), Joyland (redirect), Janitor (no price
  page) are correctly left `{none}`. No screenshot is demanded of an
  unreachable page. Honest, not padded.
- **(c) Intro tightened so table lands ~530-550 words — RESOLVED (Y).** Intro
  cut 180→120; Does-it-have 330→280; Why-filter 270→250. Arithmetic
  (120+280+250) puts the comparison table at ~word 550 — a ~150-word earlier
  arrival than Pass 1.

## Findings

### CRITICAL

- None.

### HIGH

- None.

### MEDIUM

- [table H2 / line 84] BLUF is a meta-claim, not the answer. It leads with
  "the only side-by-side table you'll find." The SERP-uniqueness boast is
  self-referential throat-clearing dressed as a BLUF — have the draft lead with
  what the table *shows* and demote the uniqueness claim.
- [collective-exhaustiveness / research line 179] Privacy / data-retention of
  intimate chats was the dossier's other named information-gain lever and the
  outline drops it. Not a SERP-consensus topic (so not CRITICAL), but adding it
  would strengthen differentiation. Optional.

### LOW

- [Joyland line 141 vs DreamGen line 148] Mild semantic adjacency on the
  "stories" axis. Keep Joyland framed on *library breadth* (big bot catalog +
  browsing), DreamGen on *writer tooling* — not a MECE break, just a
  draft-discipline note.
- [how-to-choose BLUF, line 172] "Skip the rubric and match your situation"
  risks reading as a jab at the section above. Phrase as "you don't need to
  re-score anything" rather than implying the table section was skippable.
- [secondary keyword coverage] "character ai no filter reddit" is served by the
  Reddit external visual + thread citation; the fringe "no login" term
  (~40 vol) is unaddressed — acceptable to skip rather than dilute.

## What Works

- [MECE-boundary notes] The boundary notes don't merely exist — they assign
  *ownership* (table owns axes + price caveat; how-to-choose owns the
  situation→pick mapping) with an explicit "don't write the rationale twice"
  guard, and the two visuals reinforce the split. That is the correct, durable
  fix for the prior CRITICAL rather than a cosmetic rewording.

## Recommendation

- Verdict is PASS: advance to stage 4 (/product-mentions). Fold the two MEDIUM
  items (table BLUF leads with substance; consider a short privacy/retention
  beat) into drafting guidance — neither blocks.
