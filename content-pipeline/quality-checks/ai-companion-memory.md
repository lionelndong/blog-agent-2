# Quality Check — ai-companion-memory

## Verdict: **PASS**

- **Mechanical:** 96/100 (depth 25/25, consensus 20/20, ai_tells 25/25, structure 15/15, evidence 10.6/15). No CRITICAL findings; no dimension below its 60% floor.
- **Judgment overlay (0.4 weight):** ~86/100 — sounds like the brand voice anchors (second-person, evidence-led, honest concessions before any edge), the four-layer memory model is genuine information gain absent from the SERP's "persistent memory" fluff, product mentions are demonstrative not bolted-on, and after revision the privacy section carries concrete named breaches.
- **Final = 0.6 × 96 + 0.4 × 86 = 92.** Adversarial read does NOT conclude "keep the competitor" for the explainer's target reader.
- Compliance: forbidden phrases CLEAN; internal-stack CLEAN; crutch "honest" reduced to 2; 18+ framing intact; privacy stated as a priority not a guarantee; no fabricated retention numbers (removed). 2 naked `[link]`s remain by design → resolved in `/verify-claims`.

## Adversarial read + how it was resolved

The skeptical-expert read (full text in `ai-companion-memory-adversarial.md`) raised 5 weaknesses. Disposition:

1. **App section asserted verdicts without running the test on each app.** → Added a framing line: the table reflects *documented* 2026 hands-on-review behavior; the reader is directed to run the five-minute test on their shortlist, and the full per-app hands-on ranking lives in the linked sibling. Appropriate for an explainer pillar (the ranking intent is deliberately owned by `ai-companion-best-memory`, not this page).
2. **"82% / 7-day recall" stat was first-party-sourced fabricated precision** (dossier §4 forbids inventing retention numbers). → **REMOVED** the number and the chart visual built on the non-existent dataset; replaced with a qualitative "nails it most of the time, not every time" framing. Integrity fix.
3. **Only 5 apps vs beat-spec breadth.** → Expanded the comparison table to **8 apps** (added Candy AI, Paradot, Anima) for SERP-parity breadth while keeping the explainer (not ranking) shape.
4. **Over-reliance on own-domain citations for factual claims.** → Moved the 7.6/10 review citation to the external source (genfindr); added two external breach citations (`[link]` → verify-claims). Internal links now carry topical-authority weight, not factual proof.
5. **Privacy section all assertion, no specifics.** → Added two concrete, named, verifiable breaches (Oct 2025 43M-message companion-app leak; ~113k explicit-prompt NSFW-platform leak) with `[link]` for verify-claims.

**What genuinely works (per adversarial):** the four-layer memory model (context window / saved-fact list / pinned notes / long-term understanding) — a clean, defensible mental model the SERP lacks, making every later "why it forgot" claim mechanically legible.

## Recommendation

**Proceed to `/verify-claims`** — resolve the 2 breach `[link]`s to their real public sources (e.g. Cybernews / Androidheadlines / Malwarebytes breach reports) and confirm the genfindr review URL. Then continue: optimize → generate-visuals → preview → format-for-publish (auto-publish) → `auto_publish_check.py`.
