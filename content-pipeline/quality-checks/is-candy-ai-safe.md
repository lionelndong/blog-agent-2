# Quality Check — is-candy-ai-safe

## Verdict: **PASS**

**Score: 97 / 100**

- Final score = 0.6 × mechanical (100) + 0.4 × judgment (92) = **96.8 → 97**
- No CRITICAL findings.
- No mechanical dimension below 60% of its weight.
- Adversarial read concludes **keep our draft** (positive).

PASS conditions all met (≥85, no CRITICAL, no dimension under floor, adversarial not "keep the competitor").

## Mechanical metrics (0.6 weight)

Mechanical score **100/100**. All five dimensions at full weight:

| Dimension | Score / Weight |
|---|---|
| Depth vs benchmark | 25 / 25 |
| Consensus coverage | 20 / 20 |
| AI tells | 25 / 25 |
| Evidence | 15 / 15 |
| Structure | 15 / 15 |

- Word count 1,478 raw / 1,368 (script body count) vs target 1,100 — ratio 1.24, **inside the brief's 1,100–1,600 GEO window** (not penalized for being under the ~3,400-word SERP modal; the BEAT SPEC deliberately overrides length).
- Claim density 0.18 (11/60 numeric sentences); 13 hyperlinks (well above the 8-link floor).
- All required FIXED elements present: answer-first ~60-word BLUF opener; 4-column Candy AI / Replika / Nomi AI / Pleasur.ai table with the 4 required rows; exactly 5-bullet checklist; 6-question FAQ (each answer ≤50 words, answer-first); CTA linking the privacy policy.
- Repetition flags ("policy" ×23, "privacy" ×15, "published" ×12, "source" ×10, "verify"/"yourself" ×8) are **inherent topical vocabulary** for a privacy/sourcing comparison page, not AI crutch phrases — the script correctly left ai_tells at full 25 (no forbidden-phrase or throat-clearing CRITICAL). Worth a light copy-edit, not a gate failure.

## Judgment read (0.4 weight) — 92

- Reads like a real editor, not an AI: non-absolutist "safe-with-caveats" register held consistently from the 60-word opener through "The bottom line."
- Every section teaches something concrete (what Candy AI collects, the encryption-unstated point, Replika's Italy/FTC history) — no gesturing.
- Product mention is natural: Pleasur.ai earns its table column as the only first-party policy on the record, and the CTA is soft and verifiable, not salesy.
- Information gain is real and off page 1: a first-party companion provider comparing four platforms and citing its own published privacy policy line by line — confirmed absent from every page-1 result per the dossier's top-page summaries.

## Adversarial critique (positive — keep our draft)

Full read in `is-candy-ai-safe-adversarial.md`. The expert keeps our draft over the #1 because it is the only candidate offering an AIO a clean, attributed four-platform table to lift verbatim. Five tighten-ups (not structural failures) below feed the punch list.

## Punch list (optional polish — none block PASS)

1. **Candy AI column leans hard on a single source (scribehow), stated aloud.** Consider adding a second corroborating cite for at least the data-collection or training claim so the column does not inherit scribehow's authority weakness.
2. **"Regulatory history" row reads soft on Candy AI** ("No major regulatory action found in cited sources"). Tighten the hedge or note the scope of the search so it does not undercut the "we sourced what others guessed at" thesis.
3. **Replika FTC cell is undated/un-statused** — "an FTC complaint alleged data-handling issues." Add the year and "ongoing/unresolved" framing to stay clearly inside the dossier's strict-attribution compliance rule (line 107/133).
4. **Table is four-wide but two platforms deep of substance** (Nomi + half of Candy AI are "verify yourself"). Acceptable given honest sourcing, but a single concrete Nomi fact (e.g. whether a published policy currently exists) would harden the column.
5. **Encryption "at rest" is over-emphasized** (bolded across table + FAQ + bottom line). Tone down the repetition so the transparency framing isn't undercut by a table-stakes spec presented as the differentiator.

## Compliance flags

None blocking. Verified against the brief's HARD compliance notes:
- No platform called definitively "unsafe"; all competitor claims attributed ("reviewers have noted," "Italy's regulator required," "the FTC complaint alleged"). ✔
- No fabricated stats; no invented numbers. ✔
- 18+ framing throughout; CTA states "It's an 18+ platform." ✔
- Pleasur.ai never claimed absolutely "safe/private"; positioned as transparency/published-policy. ✔ ("that's a transparency point, not a claim that it's the 'safest.'")
- No "no filter / anything goes" framing. ✔
- No internal-stack vendor names in reader-facing copy. ✔
- Internal links correct: /legal/privacy-policy, /blog/ai-companion-safety-checklist, /blog/best-replika-alternative-2026 (the 404 /blog/replika-alternative is NOT used). ✔
- WATCH (advisory only): punch-list item 3 — the undated FTC-complaint cell is the one spot that sits closest to the strict-attribution line; tighten on the next pass.

## Recommendation

**PASS — proceed to `/verify-claims`.** Punch-list items are copy-level polish that a light revision can fold in during or after claim verification; none are depth/coverage/structural deficits and none require a return to /outline or /research.
