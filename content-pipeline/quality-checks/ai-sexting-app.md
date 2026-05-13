# Quality check — ai-sexting-app

## Verdict: **PASS**

**Combined score: 85 / 100** (auto 69/80 + adversarial 16/20)

- ≥ 75 → PASS
- 60–74 → BORDERLINE
- < 60 → FAIL

**Recommendation: PROCEED to `/verify-claims`** (with a light revision pass on patches 1–5 below; revision is recommended but not gating — the citation work `/verify-claims` does will resolve the largest score-deduction by itself).

No CRITICAL constraint violations. No forbidden phrases. No out-of-slot coming-soon products. No abstract visuals. No internal-link slug drift. Visual budget at cap (3/3).

---

## Metrics summary (from `quality_check.py`)

- **Auto score:** 69 / 80
- **Forbidden phrases:** 0 hits.
- **Voice metrics vs `examples/` baseline:** All 7 metrics in range (avg sentence 15.7 vs 15.9; median 14 vs 15; paragraph 30.4 vs 24.3; second-person/1k 29.5 vs 41.2; em-dash/1k 7.5 vs 5.9). Paragraphs slightly long-side of baseline but inside tolerance.
- **BLUF compliance:** 12 / 12 H2 openers pass (100%).
- **Claim density:** 24 must-cite claims, 7 linked (29.2%) — **the only score-deduction (-11 pts)**. Most missing `[link]` markers are on numbers `/verify-claims` is about to fetch. The draft trusts the next stage; the script doesn't know that.
- **Draft length:** 2,782 words (target 2,200–2,500 — trimmable in optimize-content if needed).

Raw metrics: `content-pipeline/quality-checks/ai-sexting-app-metrics.md`.

---

## Adversarial critique summary (full file: `ai-sexting-app-adversarial.md`)

- **Voice match: 8 / 10.** Sentences are short, BLUF-led, second-person, concrete — close to `examples/` baseline. Loses 2 pts to: (a) one stat-dump paragraph (Mozilla 5-percentage cluster), (b) over-staged disclosure paragraph (third time saying "we're being honest"), (c) one SEO-volume aside the reader doesn't care about.
- **Five weakest things:**
  1. Candy section recommendation undercut by its own trade-off line — pick a posture.
  2. Semrush 40,500-volume aside is for the writer, not the reader. Cut.
  3. FAQ Q4 ends with a CTA wedged into an answer (4th repetition of the `ai-girlfriend-experience` link).
  4. Mozilla numbers paragraph is a 5-stat dump without synthesis — compress to 2.
  5. "Disclosure" paragraph repeats the intro's disclosure — meta-commentary, cut to one line.
- **What works:** Disclosure structure is genuinely uncommon for the category. Pleasur.AI is pick #4 (not #1), trade-offs are stated honestly, the affiliate-listicle pattern is named in paragraph 1. This is what makes the article publishable — preserve it through revision.
- **Constraint violations:** None.

---

## Punch list (ordered by severity)

### HIGH

1. **Compress the Mozilla 5-percentage paragraph (lines 146–148).** Stat dump without argument. Drop to 2 numbers + the warning-label summary. See adversarial patch 3.
2. **Cut the disclosure paragraph (lines 96–98) to one line.** "Disclosure: this is our product. We'll tell you what it's good at and where it falls short." Drop the "unusual for a publisher's own pick" meta. The intro already disclosed.
3. **Delete the Semrush volume sentence (line 36).** Reader doesn't care about category search volume; this is SEO-internal. Keep the SERP observation that follows it — that one earns its place.

### MEDIUM

4. **Tighten Candy section closer (line 58).** The trade-off line currently swallows the recommendation. Trim to one trade-off sentence + one one-line summary. See adversarial patch 1.
5. **Strip CTA from FAQ Q4 (line 196).** The `ai-girlfriend-experience` link already appears 3× elsewhere (lines 35, 107, 211). The FAQ should answer, not link.

### LOW

6. **`/verify-claims` follow-ups.** Make sure each numbered claim that currently shares one `[link]` tag (Mozilla 5 percentages; OurDream pricing re-stated at line 172; "find a list of about 14" at line 198; WaPo/Reddit SERP positions at line 38; 80% category overlap at line 194) gets its own source or gets softened to opinion.
7. **Watch paragraph length in optimize-content.** Median paragraph is 30 words vs baseline 23 — inside tolerance but on the long side. If ContentShake's quality rewrite re-bloats anywhere, push back.

---

## Recommendation

**PROCEED to `/verify-claims`.**

The 69/80 auto floor is driven entirely by missing `[link]` markers on numerical claims that the writer left for `/verify-claims` to fetch. The adversarial 16/20 confirms the voice and structure are sound. Apply HIGH-severity patches (1–3) before `/verify-claims` if cheap; MEDIUM (4–5) can wait for the editor's preview pass; LOW (6–7) belong downstream by design.

Do **not** kick this back to `/draft`. The article's disclosure-first structure is its competitive advantage in the SERP — a regen risks losing that.
