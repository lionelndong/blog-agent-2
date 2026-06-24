# Quality Check — ai-companion-vs-chatgpt-companionship (Stage 6, post-revision re-run)

## Verdict: **PASS** — final 87 / 100 (0.6 × 88 mechanical-corrected + 0.4 × 86 judgment). No CRITICAL findings. No corrected dimension below 60% of weight. Adversarial keeps THIS draft over the SERP.

**Run context:** Re-run after Stage 6b revision of the prior BORDERLINE-84 punch list. Verified the revisions landed: crutch repetition cut (built 16→6, every 8→2, character 10→3), memory caveat now crisp + qualitative + `[VERIFY]` (no fabricated number), balanced privacy sentence in the FAQ, concrete orchestration example added to §4.

---

## Metrics summary (mechanical script + corrections)

Raw mechanical score: 71/100. **Two mechanical false-negatives corrected per the documented GEO-brief exception → corrected mechanical 88/100:**

| Dimension | Raw | Corrected | Note |
|---|---|---|---|
| depth_vs_benchmark | 21.2/25 | 23/25 | Script uses hardcoded 1,000-word target and counts table cells + FAQ + headings + placeholders → reports 1,752w / 1.75 ratio. **Measured PROSE BODY = 1,302 words** (excludes GFM table cells, FAQ Q&A 258w, headings, `[VISUAL]`/`[link]` markers). 1,302 is squarely in the binding 1,000–1,400 prose band. Not over ~1,450 → no real word-count problem. |
| consensus_coverage | 0.0/20 | 19/20 | **False negative** — verified by reading: memory (§1), persona (§2), voice/audio (§3), cost (table + §6 "When ChatGPT IS Better"), privacy/data-trust (§6 body ≥2-3 sentences + FAQ) are ALL covered, factually and balanced. The "MISSING privacy" flag is the script keying on a literal beat-spec string, not a real gap. |
| evidence | 10.0/15 | 10/15 | 8 hyperlinks + 10 `[link]` stubs — expected at draft stage; verify-claims resolves. Density 0.08. OK floor. |
| ai_tells | 25.0/25 | 25/25 | No forbidden phrases, no crutch ≥8 after revision (top is "model" / "history" x8 — topical nouns, not throat-clearing tics). Para rhythm CV 0.48 (varied). |
| structure | 15.0/15 | 15/15 | All 6 prescribed H2s present, ordered, exact names; intro hook + conclusion present; FAQ block present. |

**Judgment read (40%): 86/100.** Reads human, not AI. Voice matches `examples/voice/` — declarative openers, varied rhythm, "Same engine, different car." The transition spine (each section hands to the next) is genuinely strong and is the draft's competitive weapon for citation. Information gain is real and present (head-to-head table no page-1 result has; the orchestration "why it feels different" explanation; the honest "When ChatGPT IS Better" section). Product mentions (Creator, Call button, voice notes) are demonstrated, not bolted on. Marked down for residual modal-verb softness on Pleasur.ai memory ("designed to" / "built to carry") and the privacy axis conceding genies' ground without a first-party counter — both fixable downstream, neither AI-tell nor structural.

---

## CRITICAL constraint checks (GEO brief — all PASS)

- Title EXACT "Why Specialized AI Companions Beat ChatGPT for Emotional Depth" — PASS
- Hook ≤60 words, verbatim, in para 1 — PASS (self-contained citation target)
- All 6 prescribed H2s present, ordered, named — PASS
- 4 FAQ questions verbatim — PASS
- Pricing coin-metered $12.99/$27.99/$49.99; ChatGPT Free $0/Plus $20/Pro $200 framed as "not a price war" — PASS; no flat/unlimited/no-tokens anywhere
- Voice = audio only — PASS ("In-chat voice notes plus real-time audio calls (audio only)"; "Audio only, no two-way video")
- No "82%" memory stat — PASS (0 occurrences)
- No fabricated hard recall number — PASS (caveat is qualitative + `[VERIFY]`)
- No explicit adult language — PASS
- No internal-stack names (Strapi/Doppler/Supabase) — PASS
- No coming-soon/roadmap product in walkthrough — PASS (Call + voice notes are live per brand-config 2026-06-24; AI Video never claimed)

**No CRITICAL findings remain.**

---

## Adversarial critique (summary)

Side-by-side verdict: **keeps THIS draft** over the #1 incumbent — it is the only page that answers the literal ChatGPT-vs-companion question head-on with a comparison table and a liftable self-contained hook; the genies/straight.com listicles are "best apps" roundups that make the reader do the comparison themselves. Caveat: load-bearing claims still on `[link]`/`[VERIFY]` stubs (expected at draft stage). Weakest points: (1) citation stubs on the thesis-bearing OpenAI-positioning / Mozilla / pricing claims; (2) the 3-of-9 recall stat and source dropped from §1; (3) Pleasur.ai memory asserted via modal verbs, not shown; (4) "why they feel different" idea restated ~4 ways; (5) doubled-bracket typo `[privacy policy [link]]` in FAQ + privacy axis thinner than genies'. One thing that works: the transition architecture / continuous spine. Full text: `*-adversarial.md`.

---

## Punch list (top 3 by severity — for verify-claims, NOT a re-draft)

1. **Resolve all `[link]` / `[VERIFY]` stubs** (verify-claims). Priority: OpenAI "positioned away from roleplay" (appears 3×), Mozilla *Privacy Not Included* 2024, ChatGPT pricing $0/$20/$200, Sky-voice pull, and the §1 memory `[VERIFY]`. These are the thesis's load-bearing facts; ship uncited = citation risk.
2. **Fix doubled-bracket typo in FAQ #4:** `[privacy policy [link]]` → single clean link (verify-claims).
3. **Optional depth upgrade (not blocking):** ground §1's memory caveat with the dossier's verifiable "~3 of 9 companions reliably recall a month-old chat" hands-on finding + source, and reduce one of the ~4 restatements of "same model, different layer." Improves citability without a re-draft.

---

## Recommendation: **PROCEED to /verify-claims.**

The draft earns ≥85 now that crutch repetition is fixed, the memory caveat is honest, privacy is balanced in-body + FAQ, and the §4 orchestration example is concrete. No depth/coverage deficit and no CRITICAL → this is a citation-resolution job for verify-claims, not a structural re-draft or re-outline.
