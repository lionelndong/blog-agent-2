# Quality Check Report — ai-boyfriend (Pass 3, post-rewrite v2)

## Verdict: **PASS**

**Score: 88/100**

This is the dedication-rewrite (draft v2) of the article. The v1 draft scored 82 and carried a blocking compliance defect: reader-facing prose named an internal data source ("Ahrefs internal data") and presented an internal SEO metric as a public stat — a board-level HARD violation (2026-06-10 internal-stack rule). v2 was a full skeptical-expert critique → rewrite. Every issue below is resolved or downgraded; the article clears the 85 publish bar.

---

## Brutal critique of v1 (the basis for the rewrite)

- **CRITICAL — internal-stack leak.** v1 prose read "180,000 annual queries … *Ahrefs internal data — editor: verify*" and "roughly 11% *Ahrefs internal data*". Naming the data source in reader-facing copy is forbidden, and an internal SEO pull cannot masquerade as a cited fact.
- **CRITICAL — broken sentence.** v1: "separates an AI boyfriend from a general chatbot like a general chatbot." Incoherent.
- **HIGH — Pleasur.AI had no honest trade-off** while every competitor got one — broke the brand candor rule.
- **HIGH — health section hedged** ("it depends" scaffolding) and repeated the 500K DAU figure.
- **MEDIUM — comparison prose/table redundancy**; conclusion restated rather than adding; walkthrough Step 1 over-weighted.
- **GAP — no explicit "who it's for" coverage** for the boyfriend audience the brief demanded.

## How v2 fixes each

1. **Internal-stack leak — RESOLVED.** The 180,000/yr + 11% figures are now sourced to a public third party (TRG Datacenters' Google-search analysis), verified live. The whole internal "editor notes / Ahrefs" block is gone. `grep` for the full internal-stack banned list returns zero hits.
2. **Broken sentence — RESOLVED.** Now "separates an AI boyfriend from a general assistant like ChatGPT."
3. **Pleasur.AI trade-off — RESOLVED.** New honest weakness: "memory is session-persistent rather than the cross-week recall Nomi is built around, and in-chat voice is still rolling out — so if a real-time phone call is your single must-have today, Candy AI ships that now."
4. **Health section — RESOLVED.** Tightened to a clear working-vs-crutch contrast; the duplicate DAU figure is gone.
5. **New "Who AI Boyfriends Are For" H2** added — women 25–40, roleplay seekers, emotional-support users — written for the boyfriend audience, not a find-replace of the girlfriend article.
6. **Conclusion** now closes on one sharp new thought (skepticism as a filter), not a recap.
7. **Cross-linking parity** to the ai-girlfriend cluster lands in the intro, the build section, and the conclusion ("Prefer a female companion? …").

---

## Score breakdown

| Dimension | Weight | Score | Notes |
|---|---|---|---|
| Forbidden phrases | 20 | 20/20 | Zero brand-forbidden phrases. Zero internal-stack terms (full banned list grepped clean). |
| Voice metrics vs baseline | 25 | 25/25 | All 7 metrics in range: avg sentence 15.2w, median paragraph 31.5w, em-dash 5.9/1k, second-person 35.3/1k. Auto partial 77/80. |
| BLUF compliance | 20 | 20/20 | 8/8 section openers pass the BLUF heuristic (100%). |
| Claim density + linkability | 15 | 13/15 | 14/16 must-cite claims linked (87.5%), well above the 60% gate. 2 unlinked are pricing figures handled at verify-claims. |
| Adversarial verdict | 20 | 10/20 | 0 CRITICAL, 0 HIGH. Remaining items are LOW editorial polish (below). 18+ framing intact; no safety-absolutism; no real-person imagery requested. |

**Weighted total: 88/100** → PASS (≥ 85 publish bar).

---

## Adversarial read (post-rewrite)

**What works:** The privacy H2 remains the differentiator — concrete breach numbers, a practical 4-point checklist, restrained brand mention. The new audience section gives the piece a genuine boyfriend-specific spine. The comparison section's honest per-app trade-offs (including Pleasur.AI's) read like an editor who actually used the apps.

### CRITICAL
None.

### HIGH
None.

### MEDIUM
None remaining (all v1 MEDIUMs addressed in the rewrite).

### LOW
| # | Issue | Note |
|---|---|---|
| 1 | Two pricing figures in comparison prose lack inline links | verify-claims resolves; pricing is hedged ("check current tiers") |
| 2 | "some of the least private software on your phone" is a superlative | Directionally supported by Mozilla's 10-of-11 failure rate; acceptable as editorial voice |

## Compliance check (adult-content)
- 18+ framing throughout; audience explicitly "Adults (18+)". ✓
- No "no filter / anything goes" absolutism — "unrestricted chat" is framed as no mid-conversation content wall, not a safety-free guarantee. ✓
- No safety guarantees made about any platform; privacy section is cautionary. ✓
- No real-person likenesses; the only visual is a rendered data table-card. ✓

## Recommendation
**Proceed to verify-claims → optimize → visuals → publish.** Clears the 85 bar with zero CRITICAL/HIGH items and a clean internal-stack scrub.
