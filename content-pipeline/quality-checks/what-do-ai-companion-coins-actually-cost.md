# Quality Check — what do ai companion coins actually cost

> Re-run after surgical revision (BLUF now leads with numbers; Candy.ai named with published prices; top-up-pack hidden-cost angle added). Draft stage. Date: 2026-06-16.

## Verdict: **BORDERLINE** — proceed to /verify-claims (it resolves the gates)

- **Final score: 89/100** (0.6 × mechanical 100 + 0.4 × judgment 73 = 60 + 29.2 ≈ **89**)
- **Mechanical: 100/100** (all five dimensions full, none near floor)
- **Judgment: 73/100** — wins the side-by-side on substance and is compliance-clean, but carries factual defects (uncited stats, wrong Candy.ai sub prices, estimate drift) that bind below a clean PASS until /verify-claims runs.
- **Adversarial conclusion: KEEPS THE DRAFT** over both #1s (Candy vendor page + skywork review). Not adversarial-negative.
- **No CRITICAL findings.** Compliance rails clean; pricing of *our own* product accurate; GEO format present.

Why BORDERLINE not PASS: the article is the strongest thing in this SERP on substance, but two factual issues remain. Un-resolved `[link]` placeholders are expected at draft stage, but the **wrong Candy.ai subscription prices** are a real defect that would mislead a reader and undercut the "we are the accurate source" thesis. These are exactly the class of fix /verify-claims + a one-line price reconciliation owns. No structural/depth deficit — do NOT route back to /outline or /research.

## Prior HIGH items — both RESOLVED

1. **BLUF burying the number → RESOLVED.** Opening 55 words now lead with the answer: *"A coin is a metered unit of media. On Pleasur.ai an AI image or voice note costs 10 coins, a phone call costs 50 coins per minute, and text chat is unlimited — and the tiers run $12.99/mo for 1,500 coins, $27.99/mo for 5,000, and $49.99/mo for 10,000."* Definition + per-action costs + all three tiers, answer-first, inside the 40–60 word window.
2. **Comparison going coy on Candy.ai → RESOLVED (with a caveat).** Candy.ai is now named explicitly in the BLUF, the tier-math section, and the annual-billing trap section, with its subscription price stated directly and its per-action token rates correctly framed as reviewer-estimated. Caveat: the comparison *table* still uses the generic "opaque/estimated competitor" label rather than naming Candy.ai in-cell — a minor leftover, downgraded from HIGH to MEDIUM.

## CRITICAL constraint checks — ALL PASS

- **Compliance rails: PASS.** No "no tokens / no fees / no metering / flat rate / unlimited everything." "Unlimited" is scoped to *text* every time and explicitly contrasted against metered media. Draft states outright "Pleasur.ai meters media by coins like everyone else" and "The win isn't that one platform is unmetered." Differentiator framed as transparency-of-metering throughout.
- **Pricing accuracy (our product): PASS.** $12.99/1,500, $27.99/5,000, $49.99/10,000; image=10 / voice=10 / call=50/min; text unlimited; no phantom $19 tier anywhere. Matches the live fact-lock.
- **Candy.ai per-action TOKEN rates framed as reviewer-estimated: PASS.** "reviewer-estimated, not vendor-published," "confirm in-app," "indicative only" — consistent and correct. Candy's subscription prices are named directly (allowed) — but see HIGH-1: the *values* used are wrong.
- **Internal-stack scrub: PASS.** No Strapi/Doppler/Semrush/Supabase or any internal tooling in reader-facing prose.
- **GEO format: PASS.** Answer-first BLUF leading with numbers in first ~55 words; FAQ present (6 Q&A); both required tables present (coin-tier table + transparent-vs-opaque cost-per-interaction table).

## Metrics summary (mechanical)

| Dimension | Score / Weight |
|---|---|
| Depth vs benchmark | 25 / 25 — 2,279 words vs 2,000 target (1.14×); under top-3 median 2,684 but on-spec for a GEO answer-first density play |
| Consensus coverage | 20 / 20 — all must-cover topics present |
| Evidence | 15 / 15 — claim density 0.31 (42/135 numeric); 9 live hyperlinks + 19 `[link]` placeholders (OK at draft; verify-claims must resolve) |
| AI tells | 25 / 25 — no forbidden phrases, no editorial crutch ≥4×; topical-noun repetition flagged ("published" 21×, "images" 19×) is on-topic, not throat-clearing |
| Structure | 15 / 15 — 7 H2 + FAQ + bottom line; H2/H3 nesting intact |

Paragraph rhythm: mean 42w, CV 0.57 — varied, not the uniform 2-sentence tic the voice notes warn against.

## Judgment read (voice baseline: examples/voice/)

Reads like the brand, not like an AI. Second person, evidence-led, concrete numbers, an opinionated thesis (transparency-of-metering) carried consistently without sliding into the forbidden "no metering" claim. Honest trade-off acknowledged ("The dollar figures may land in the same ballpark; the *knowability* doesn't"). Product mentions (AI Image Generation, Companion Creator) are demonstrated in service of the math, not bolted on. Information gain is real and triple-stacked: published exact per-action costs the SERP can only estimate, the token↔coin "what it buys" translation, and the dated pricing-drift warning. The verdict-formula tic is avoided; section closers vary.

Deductions: (a) factual looseness on the competitor's own numbers is the one place the brand's "we're the accurate source" pitch can be turned against it; (b) the Light/Moderate/Heavy profiles are clean but synthetic — the #4 SERP result is a *lived* Reddit 3-week breakdown, and a sentence of lived framing would harden this.

## Adversarial critique (summary; full at -adversarial.md)

Reviewer keeps the draft over both #1s: it is the only page in the set that publishes exact per-action numbers and does the arithmetic out loud — the axis the whole SERP is starved for. Five weak spots, which in severity order reduce to: bare `[link]` citations, wrong/contradictory Candy.ai sub prices, the comparison body/table softening the Candy entity, the 2–4/2–5 estimate drift, and a body/table voice-note mismatch. The one thing that genuinely works: the "calculate your own monthly cost" three-step section + transparent-vs-opaque wedge — concrete, reproducible, structurally impossible for any page-1 competitor to write.

## Punch list (by severity)

**HIGH (factual — must fix before publish; /verify-claims + reconcile)**
1. **Candy.ai subscription prices are wrong and self-contradictory.** Draft says "~$12.99/mo month-to-month (~$5.99/mo annual)" (tier-math ¶) and "'$5.99/mo' headline ... actual one-month rate closer to $12.99" (annual-trap ¶). Fact-lock is **$13.99 (1-mo) / $8.99 (3-mo) / $3.99 (12-mo)**. The draft also quotes Candy's monthly as $12.99 — identical to Pleasur.ai's own Starter — which a reader with the Candy page open catches instantly. Reconcile all Candy figures to the lock.
2. **Resolve all 19 `[link]` placeholders with dated, real sources** (expected at draft stage; the GEO/citation thesis fails without them). Top-up-pack range "$9.99–$299.99" and the "tokens/image" estimate especially need attached, attributed sources.

**MEDIUM (precision / liftability)**
3. **Estimate drift on the competitor per-image figure:** "2–5" (tier-math ¶), "~2–4" (metering ¶), "~2–5" (table). Lock is **2–4**. Use 2–4 in all three spots — precision on the competitor's number is the whole pitch.
4. **Body/table voice-note mismatch:** the at-a-glance table lists "~500 / ~1,000 voice notes" at Standard/Ultimate but the body only walks images/call-minutes for those tiers. Either validate and mention the voice-note column in body, or trim it.
5. **Name Candy.ai in the comparison table cells**, not just the generic "opaque/estimated competitor" — the named-entity surface is the citation point.

**LOW (polish)**
6. One sentence of *lived* monthly-cost framing (nodding to the Reddit "3 weeks of testing" demand) would harden the synthetic Light/Moderate/Heavy profiles.

## Recommendation

**Proceed to /verify-claims.** The two prior HIGH items are resolved; no CRITICAL findings; compliance and our-product pricing are clean; GEO format is in place. The remaining defects are factual-source and price-reconciliation work that /verify-claims is the correct stage for — there is no depth or structural deficit, so do NOT route back to /outline or /research. The one item /verify-claims cannot infer on its own is the Candy.ai price reconciliation to the fact-lock ($13.99/$8.99/$3.99); flag it explicitly in the verify brief so the cited values match the lock rather than the current wrong draft numbers.
