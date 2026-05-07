# Visuals Adversarial — ai-girlfriend-experience (re-run after revision)

Second adversarial pass on the visuals manifest + cited draft after the
revision pass (1/1 budget consumed) addressed the prior FAIL's two
CRITICAL findings and one HIGH. Verifies the strip+add ops actually landed
in the cited draft and that the resulting article — now carrying a single
visual across ~2,600 words — still defends its visual budget under the
9-step rule.

The article ships with one visual: the §4 Character.AI MAU chart at
`content-pipeline/images/ai-girlfriend-experience/chart-3-character-ai-monthly-active-us.png`.
§§1, 2, 3, 5 carry no visual. The two prior decorative/wrong-data assets
were stripped; the prior raw §2 `[VISUAL:...]` leak was stripped (and
should ideally be re-captured, but env-blocked in this deployment).

---

## Prior CRITICAL #1 (chart wrong data) — fixed

**Verification.** Manifest entry index 3 (`status=stripped`,
`stripped_finding_id=visuals-adversarial-CRITICAL-1-section-4`) carries
the original three-point chart (28 / 20 / 10) marker. New entry index 4
(`status=captured`, `data_points=2`) is the re-rendered replacement.
The on-disk PNG (`chart-3-character-ai-monthly-active-us.png`, mtime
2026-05-06 22:57, 65,077 bytes vs the prior asset's smaller bytes)
plots exactly two points: `Mid-2024 peak (28M MAU)` → `Early 2025
(~20M MAU)`. Title and Y-axis label both name "Character.AI monthly
active users (millions)". Replika installs has been moved out of
`research.engagement_signals_verified` into `research.replika_installs_aux`,
with a `_meta` note explicitly forbidding the two from being plotted
together. Chart now matches the prose claim ("eight-million-user
shrinkage … 28M → ~20M") in one glance — the inverted-pyramid
takeaway that principle #4 asks for.

## Prior CRITICAL #2 (Mozilla PIL-rendered fake) — fixed

**Verification.** Manifest entry index 2 (`status=stripped`,
`stripped_finding_id=visuals-adversarial-CRITICAL-2-section-3`). Cited
draft contains no `![...](images/...mozilla...)` image line in §3 (Act
2). The Mozilla `Privacy Not Included` claim still lands on the prose
load — three statistics (90% / 73% / 54%) each linked to the same
primary URL on lines 75 of the cited draft, plus a fourth link in §5
test #4 for cross-checking. The fabricated PIL render is no longer in
the publishable file; only the data the prose actually quotes remains.
The PNG file is still on disk (housekeeping drift), but it is unreferenced.

## Prior HIGH (§2 raw `[VISUAL:...]` placeholder leak) — fixed

**Verification.** Manifest entry index 1 (`status=stripped`,
`stripped_finding_id=visuals-adversarial-HIGH-section-2`). A `grep -n
"VISUAL:"` of the cited draft returns no hits — the bare placeholder
line is gone. §2's prose was reflowed to walk the Companion Creator
fields (appearance, personality, backstory, voice) in text alone
(lines 41–47 of the cited draft) so the section reads cleanly without
the screenshot. Pleasur.AI's `/create` is still linked; readers can
follow the link to see the UI. The `byte_transport_unavailable`
deployment-environment limitation (root-owned `/paperclip/Downloads`)
is documented in the manifest hint for a future re-attempt.

---

## Five-question framework — re-run

### 1. Decorative visuals?

The single landed visual (§4 chart) is not decorative. Two-point line
chart, ~30% drop, BLUF-supporting, sourced. No strip needed.

### 2. Missing visuals?

§2 (Act 1) is the open question. The annotated outline asked for a
Pleasur.AI Companion Creator screenshot and the 9-step rule
(decision step #1) does point that section at `screenshot`. The strip
was an environment workaround, not an editorial call. **Honest read:**
this is a `MEDIUM` editorial gap, not a `CRITICAL` — §2's prose now
walks the build flow concretely, the linked URL gives readers a way
to see the UI themselves, and forcing a re-capture from this verdict
would just re-trigger the same `byte_transport_unavailable` block. Flag
for the deployment-fix backlog (manifest entry #1 hint), not for a
revision-budget consumption.

§§1 (definition), 5 (checklist) correctly default to `none` per the
foundational/checklist rules in the editorial principles.

### 3. Wrong type?

The §4 chart is the right type for "Character.AI MAU peak-to-trough" —
two-point line chart conveys the cliff better than a table of two
rows would. No mismatch.

### 4. Crop / framing?

The chart's framing is appropriate: title takes the takeaway, axis
labels name units, two markers sit at the X-axis tick positions,
no extraneous data. Padding around the line is generous but acceptable
at 1178×707.

### 5. Manual fallthrough?

`manual-capture.md` still lists entries #1 (Pleasur.AI screenshot) and
#2 (Mozilla external) as pending fallbacks. Both are now obsolete:
entry #1 has been stripped (env block), entry #2 was retried and
then stripped in this revision. Same housekeeping drift the prior
LOW finding flagged — still a LOW, still not editorially load-bearing.

---

## Findings

### MEDIUM — §2 walkthrough no longer carries a UI screenshot (deployment-env, not editorial)

§2 explicitly walks the Pleasur.AI Companion Creator (appearance →
personality → backstory → voice fields) and the 9-step rule's step #1
points such a section at `screenshot`. The strip was the right call
given `byte_transport_unavailable` blocked byte landing in this
deployment, but the editorial bar is not met until a real screenshot
lands. Action: leave as-is for this article (don't burn revision
budget on a re-capture that would hit the same env block); track
the Chrome-MCP byte-transport fix as a separate backlog item so the
next walkthrough article doesn't strip the same way.

### MEDIUM — `manual-capture.md` is stale

Entries #1 and #2 are both stripped in the manifest but still listed
as pending in `manual-capture.md`. Housekeeping drift, not an
editorial failure. Action: trim during the next bookkeeping pass on
the visuals stage; or at /preview time, suppress entries whose
manifest status is `stripped`.

### LOW — chart PNG file was reused at the same path as the stripped version

The re-rendered chart writes to the same path
(`chart-3-character-ai-monthly-active-us.png`) the original
three-point version used. The manifest tracks this correctly via
two entries (index 3 stripped, index 4 captured), but a reader who
looks only at the file path won't see the version history. Action:
none required — the manifest is the source of truth and the file's
actual content is correct. Noting it for completeness.

### LOW — orphan PNG on disk (`external-2-mozilla-privacy-not-included-h.png`)

The stripped Mozilla render is still on disk (19,050 bytes). It's
unreferenced from the cited draft and marked `stripped` in the
manifest, so it won't ship. Action: delete during the next
bookkeeping pass. No editorial risk.

---

## What works

The §4 chart now earns its place cleanly — two points, same metric,
same platform, sourced (Business of Apps + Sacra), title carries the
takeaway in one glance, and it sits next to the prose claim it
supports rather than competing with the BLUF. This is the strongest
visual the article could carry, and it's the only one. A 2,600-word
piece anchored on a single high-information chart is editorially
defensible (the 9-step rule defaults to `none`; one earned visual
across five H2s is honest, not sparse).

---

## Verdict: **PASS**

All three prior findings are resolved in the current cited draft +
manifest: the §4 chart is re-rendered with only the two Character.AI
MAU points; the §3 Mozilla PIL render is stripped from both the draft
and (effectively) the manifest; the §2 raw `[VISUAL:...]` placeholder
no longer leaks into the cited draft. No new CRITICAL findings. The
remaining MEDIUM/LOW items are housekeeping drift (stale
`manual-capture.md`, on-disk orphan files) and one editorial-vs-env
trade-off (§2 walkthrough without a screenshot, blocked by
`byte_transport_unavailable` — the right call for this article, the
wrong default for the deployment long-term). Ship.
