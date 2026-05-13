# Quality check — ai-sexting-app

## Verdict: BORDERLINE-NO-CRITICAL → proceed

- Automated partial score: **61/80**
- Adversarial score (editor estimate): ~12/20 — tactical critiques addressed in revision; one residual (privacy section comparative depth) is acceptable as the article is a roundup, not a privacy audit.
- **Combined: ~73/100** → BORDERLINE (60–74 band)
- No CRITICAL items (no forbidden phrases, all 10 H2 openers pass BLUF, em-dash density now in baseline range).

Per the pipeline rule (FAIL or BORDERLINE-with-CRITICAL = HALT), this draft proceeds. BORDERLINE without a CRITICAL flag is normal at draft stage and `/verify-claims` will lift the claim-density score.

## Metrics summary

- Words: 1,916 (in 1,500–2,500 range)
- Sentence avg: 14.1 words (baseline 15.9, in range)
- Em-dash per 1k: 6.7 (baseline 5.9, in range)
- Paragraph avg: 37.8 words (baseline 24.3, **out of range** — listicle picks need longer body paragraphs by design; lifted vs the v1 draft from 40 to 37.8)
- BLUF on H2 openers: 10/10 PASS
- Forbidden phrases: 0
- Must-cite claims linked: 4/16 (25%) — verify-claims stage will raise this

## Adversarial — issues addressed in revision

1. **"Best for:" templated tag** — rewritten to varied "Pick X if..." prose in all four picks. ✓
2. **CrushOn pricing hedge** — replaced with "free tier exists; deeper-dive review for pricing." ✓
3. **Pleasur.AI ordering disclosure** — intro now explicitly says we listed ourselves last on purpose. ✓
4. **Privacy section comparative depth** — not addressed; kept category-level by intent. Roundup scope, not a privacy audit. Acceptable trade-off.
5. **FAQ legal hedge** — trimmed to a cleaner two-sentence answer. ✓

## Recommendation

Proceed to `/verify-claims`. Citation work will close the must-cite gap and lift the score from 73 toward 80+.

## Files

- Metrics: `content-pipeline/quality-checks/ai-sexting-app-metrics.md`
- Adversarial: `content-pipeline/quality-checks/ai-sexting-app-adversarial.md`
- Combined (this file): `content-pipeline/quality-checks/ai-sexting-app.md`
