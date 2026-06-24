# Visuals Adversarial Review — ai-companion-vs-chatgpt-companionship

Stage 9b (visuals-adversarial) — **revision pass 1**. Skeptical art-director read
of visual placement against `templates/editorial-principles-visuals.md`.

**Resolution carried into this pass:** the prior FAIL's CRITICAL was the persona
`/create` screenshot shipping explicit/non-SFW content in the wrong UI state.
Chrome MCP is unreachable here, so a clean SFW recapture was not possible. The
correct editorial + compliance call was made: that screenshot was **stripped
entirely** from the draft and the manifest, and its asset file (plus an orphaned
~3.6 KB Mozilla fragment) was **deleted from disk**. The persona-section claim is
now carried by prose + the inline [AI Companion Creator](https://pleasur.ai/create)
text link, with no image.

## Computed numbers

- **Prose body word count:** ~1,250–1,400 (raw `wc -w` = 2,091; inflated by a
  ~70-word image alt-text string, table-cell text, and inline URLs). Confirms the
  TIGHT answer-first GEO format.
- **Density target band:** straddles `<1,200` (target 5, range 4–7) and
  `1,200–2,000` (target 8, range 6–11); acceptable-range floor 4–6. Leaner is
  editorially fine for this answer-first GEO format — the principles default LEAN
  and warn against decorative filler.
- **Captured non-`none` visuals:** **2** — (1) inline GFM comparison table (the
  information gain; manifest `status=skip / type_table_not_an_asset`, but rendered
  information content), (2) `image-2` concept illustration (`status=captured`,
  235 KB on disk).
- **Distinct type count:** **2** (`table` + `image`).

## Core verification (the point of this pass) — all clean

- **Explicit persona /create screenshot is GONE from the draft.** Exactly one
  `![...](...)` embed exists (line 36, the memory diagram). No persona/backstory
  screenshot embed, no broken `![]()` reference, no unresolved `[VISUAL:...]`
  placeholder anywhere. The persona claim (line 48) is carried by prose + the
  inline `[AI Companion Creator](https://pleasur.ai/create)` text link.
- **Explicit asset is GONE from the manifest.** Manifest holds exactly 2 entries
  (table + concept image). No persona/create entry; no reference to the stripped
  asset.
- **Disk is clean.** Directory holds only `image-2-side-by-side-comparison-labele.png`,
  `manifest.json`, `manual-capture.md`. No orphaned persona screenshot, no
  ~3.6 KB Mozilla fragment. Deletion executed.
- **Remaining image is compliant.** SFW, likeness-free (icons / boxes / arrows,
  no people, no real UI), brand-neutral, and accurate to the Persistent Memory
  section's argument.

## Findings

### MEDIUM — stale `manual-capture.md` entry (Mozilla external)
The Mozilla `external` was requested, never captured (`image_too_small`), and is
now absent from the manifest and draft. The underlying claim is carried by prose
+ an inline Mozilla *Privacy Not Included* text link (draft line 80, cited).
Recommend dropping `manual-capture.md` (or the entry) so no future heartbeat
chases a visual the final article doesn't reference. No broken reference results —
not a CRITICAL.

### LOW — density (2 visuals) below nominal target but acceptable
Both surviving visuals are load-bearing (information gain + concept model).
Editorial-principles leans lean for tight GEO pieces and warns against decorative
filler. Per fair-judging, not a FAIL.

### LOW — type diversity = 2, under the "≥3 types" guideline
A direct, justified consequence of removing the non-compliant screenshot with
Chrome MCP unreachable. Removing rather than shipping the explicit asset was the
correct compliance call. Per fair-judging, not a FAIL.

### LOW — manifest table entry carries `status=skip`
Expected `type_table_not_an_asset` convention (tables are inline markdown, not
asset files), not a defect. Table is present and correct in the draft (6 rows,
coin-metered pricing line intact).

### LOW — surviving image alt text is the full ~70-word structured prompt
Accurate, harmless for accessibility, and the main source of raw word-count
inflation. Optional trim, non-blocking.

## Visuals that earn their place

- **image-2 (memory concept illustration)** — earns it emphatically. Accurate to
  prompt, SFW, likeness-free, readable labels; explains reset-vs-persistent memory
  faster than the surrounding paragraph. Textbook concept illustration. No crop
  fix needed.
- **Inline comparison table** — the article's stated information gain (0 of 3 SERP
  pages have one). Skim-able; carries the pricing / voice / memory contrast.

## Summary

- **CRITICAL count: 0.** Explicit asset fully removed from draft, manifest, AND
  disk; no broken image link; no naked `[VISUAL]` placeholder; both surviving
  visuals compliant and accurate.
- Density / type-diversity sit below nominal target by design (compliance-driven
  removal under Chrome MCP outage) and are explicitly not grounds for FAIL in this
  tight GEO format.

## Verdict: **PASS**

The prior CRITICAL (explicit persona screenshot) is fully resolved by removal from
draft, manifest, and disk. No CRITICAL remains. The surviving 2-visual set — an
information-gain comparison table plus one accurate SFW concept illustration — is
acceptable, even good, density for this 1,000–1,400-word answer-first GEO format.
