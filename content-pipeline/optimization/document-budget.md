# Ahrefs Content Helper Document Budget

> Tracks Content Helper document creation against the cap on the Lite plan.
> The `/optimize-content` skill reads this file before any document creation, increments after, and resets on the 1st of each month.

## Current month

- **Month:** 2026-05
- **Used:** 10 / 51 (live count from Ahrefs page on 2026-05-03)
- **Available:** 41
- **Resets on:** 2026-05-10 (Ahrefs billing cycle, NOT 1st-of-month — confirmed from page)

## Documents created this month (known to pipeline)

| Date | Slug | Keyword | Score | Action |
|---|---|---|---|---|
| 2026-05-03 (~1h ago) | ai-girlfriend | ai girlfriend | 59 | reused (created outside pipeline previously) |

## Hard rules (enforced by skill)

- < 41 used → create freely
- 41–50 used → warn user, require explicit confirmation before each new doc
- 51 used → refuse to create new docs; reuse existing or wait for reset

## Manual override

If you need to override the cap (e.g., upgraded to a higher plan, or want to burn the cap intentionally):
1. Edit the `Used` count above
2. Or edit the `Month` field to a future month (forces a "reset" on next skill run)

## Note: source of truth

Ahrefs shows live remaining quota on the Content Helper page (e.g., "41 / 51 documents available this month"). The skill should READ that string from the page on every run and reconcile against this local file. If they disagree, trust Ahrefs.
