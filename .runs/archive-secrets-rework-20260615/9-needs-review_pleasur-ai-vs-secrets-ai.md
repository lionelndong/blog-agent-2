# NEEDS REVIEW — pleasur-ai-vs-secrets-ai

**Status:** QUARANTINED at Stage 7 (verify-claims). Did NOT advance to optimize / visuals / preview / publish.
**Run issue:** PLE-2320
**Date:** 2026-06-15
**Verdict at halt:** quality-check PASSed (86/100, no CRITICAL) — but verify-claims surfaced a **false factual premise about pleasur.ai's own price** that inverts the article's thesis. This is brand-risk copy and a positioning decision, so it is escalated rather than auto-resolved.

---

## BLOCKER 1 (CRITICAL) — pleasur.ai has no $19/mo plan; the price thesis is inverted

The brief (PLE-1944/PLE-1945) and the research dossier assert pleasur.ai = **$19/mo "Premium"** and instruct the article to *"concede openly that Secrets AI's annual ($13.33/mo) undercuts pleasur.ai's $19/mo, and counter on value."* The whole article — BLUF, comparison table, pricing H2, and the FAQ "Is pleasur.ai cheaper than Secrets AI?" — is built on that.

**The live pleasur.ai/pricing page (verified 2026-06-15) shows no $19/mo plan.** Actual tiers:

| Plan | Monthly | Annual (effective /mo) |
|---|---|---|
| Starter | $12.99 | **$5.20** ($62.40/yr) |
| Standard | $27.99 | **$11.20** ($134.40/yr) |
| Ultimate | $49.99 | $20.00 ($240/yr) |

Secrets AI (standard, non-sale): $19.99/mo monthly · **$13.33/mo annual**.

**Consequence:** on annual billing, pleasur.ai Standard ($11.20) and Starter ($5.20) are **cheaper** than Secrets AI ($13.33). On monthly, pleasur.ai Standard ($27.99) is **more expensive** than Secrets ($19.99). The article's central "they're cheaper on annual, we counter on value" framing is factually backwards for annual.

The dossier (line 107) even noted reviewers reported "$5.20–$27.99/mo" and dismissed them as unreliable in favor of "$19/mo authoritative." The reviewers matched the live page; the $19 figure does not exist on-site.

**Why this is escalated, not auto-fixed:**
- Misstating our own flagship product's price in a published comparison is brand-risk (CLAUDE.md escalation trigger).
- The fix is not mechanical — it inverts the thesis, the BLUF, the FAQ answer, and the pricing section. Per the orchestrator, a thesis-level change routes back through /outline + re-draft, not a surgical edit.
- It requires a **positioning decision the issue owner must make**, not a fact the pipeline can settle:
  1. **Which pleasur.ai tier is the comparison anchor?** The compared feature set is NSFW chat + image generation + memory. Need confirmation of which tier (Starter / Standard) includes that set, so the table compares like-for-like.
  2. **Do we now reframe to lead with "pleasur.ai is cheaper on annual"?** That is a genuine, defensible, *stronger* angle — but it reverses the brief's deliberate "concede price, win on value" strategy and changes the article's whole posture. Owner's call.

### Decision menu for the owner (pick one, then re-run from /outline)
- **(A) Re-anchor to Standard ($27.99 mo / $11.20 annual)** and reframe: annual → pleasur.ai cheaper ($11.20 vs $13.33); monthly → Secrets cheaper ($19.99 vs $27.99). Honest split decision. *(Recommended if Standard is the NSFW+image tier.)*
- **(B) Re-anchor to Starter ($12.99 mo / $5.20 annual)** if Starter already includes NSFW + image gen — then pleasur.ai is cheaper on both axes and the "concede price" framing is dropped entirely.
- **(C) Confirm a real $19/mo plan exists** (grandfathered / region / promo not shown on the public page) and provide a citable source — then the current draft stands with a citation.

## BLOCKER 2 (CRITICAL) — the article's core differentiator ("no credit metering") is false; pleasur.ai also uses coins

The article's information-gain `[GAIN]` and value thesis is: *"win on the value axes pleasur.ai can defend — … transparent card payment with **no credit-metering friction on core chat**"* vs Secrets AI's Moments credit economy. The comparison table, the pricing H2, and the NSFW H2 all lean on this.

**The live pleasur.ai/pricing page (verified 2026-06-15) shows pleasur.ai runs a coin/credit economy too:**
- AI image generation — **10 coins each**
- Voice notes — **10 coins each**
- Phone calls — **50 coins/min**
- Ultimate tier grants **10,000 coins/month**

So pleasur.ai meters media with coins exactly the way Secrets AI meters media with Moments. The only thing not metered is **text chat** ("unlimited messages / unlimited 18+ text"). But Secrets AI Premium also advertises "unlimited messaging" (dossier line 97) — so "unlimited text, metered media" describes **both** products and is not a differentiator.

**Consequence:** the article's reason to exist (`[GAIN]`) and its central value claim are factually wrong. This cannot be surgically edited — the thesis, table cell ("Moments credits" vs implied "no credits"), pricing section, and NSFW-friction section all need to be rebuilt against reality. A new, honest differentiator must be found (e.g. persistent-persona continuity, content-freedom posture, card payment) — but "no credit meter" must be removed entirely.

**This makes the auto-publish gate fail on substance, not just a number.** Combined with Blocker 1, two of the article's load-bearing pillars (price advantage framing + no-credit-meter differentiator) are built on false readings of our own product.

## BLOCKER 3 (HIGH) — genfindr rating: brief says 7.6/10, live page reads 7.3/10

verify-claims read the live genfindr Secrets AI review at **7.3/10**; the brief/dossier and our already-published memory + Replika pages cite **7.6/10**. Cannot cite "7.6" to a page that says "7.3." Reconcile to the live number and consider a cross-page consistency fix on the memory + Replika articles. Until reconciled, the figure is flagged `[CITATION NEEDED]` in the trust section + table.

## MINOR (cut on next pass)
- "16/100 scam validator" (pleasures.ai) — source returns 403, unverifiable → cut/reword.
- "mislabeled as online gambling platform" — no source found → cut/reword.
- Secrets AI annual $13.33/mo is the standard rate; a "Pride Month 77% OFF" sale was live 2026-06-13 — keep "approximately" + dated framing (already handled in draft).

---

## What is good and can be reused once unblocked
- Stages 1–6 artifacts exist and the gates passed mechanically (research + outline adversarial PASS; quality 86 PASS, no CRITICAL) — but the gates did not catch the two factual premises below because they trusted the brief/dossier's pleasur.ai facts rather than the live product. **Root cause: the research dossier (line 107) asserted "$19/mo authoritative" and an implied no-credit-meter model without checking pleasur.ai/pricing.** The research stage should verify first-party pricing/feature facts against the live site, not the brief.
- Draft-level compliance hygiene is clean and reusable: no banned "82% retention" stat, no fabricated "6x recall" counter, Secrets AI features framed as "their claim," no internal-stack leaks, 18+ throughout, no "no-filter" absolutism. The required "no crypto required" H2, the /blog/ai-companion-best-memory internal link, and the FAQ scaffolding survive.
- **What does NOT survive:** the thesis, the `[GAIN]`, the pricing section, the comparison-table pricing + credits cells, and the FAQ "cheaper?" answer — all built on the two false premises. Treat this as a research/outline-level rework, not a prose polish.

**Resume path after board steer:** correct the dossier's first-party facts (real tiers + coin economy + genfindr 7.3) → re-run `/outline` for a thesis that holds against reality → re-draft → quality-check → verify-claims → visuals → publish.
