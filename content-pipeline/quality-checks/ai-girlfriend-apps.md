# Quality Review: AI Girlfriend Apps

Issue: PLE-201  
Draft reviewed: `content-pipeline/5-drafts/ai-girlfriend-apps.md`  
Review date: 2026-05-25  
Reviewer: CMO  
Inputs: PLE-195 keyword brief, PLE-196 research dossier, PLE-197 brand reference, PLE-198 outline, PLE-199 product-mentions annotation, PLE-200 draft, PLE-208 targeted revision  
Rerun note: supersedes the PLE-201 `quality-review` revision 1 FAIL report after PLE-208 revised the comparison/profile sections.

## Verdict: PASS

The revised draft is clear to proceed to claim verification. PLE-208 fixed the prior quality blocker by replacing meta comparison guidance with reader-ready comparison assets: a visible quick-answer table, a source-status comparison table, and concrete app-profile entries for the approved source set. The draft still needs claim verification before publication, but the remaining work is citation/source freshness, not a drafting-quality blocker.

Manual quality score: 88 / 100.

Automated caveat: the generic quality-check script, `brand-config.md`, example articles, and voice guide were not present in this workspace, so this review uses a manual scorecard against the available pipeline artifacts and the stage contract.

## Scorecard

| Dimension | Result | Notes |
|---|---:|---|
| Voice and brand fit | PASS | Practical, trust-led, and adult without sensational framing. The draft avoids unsupported superiority, therapy, safety/privacy, no-filter, free, unlimited, app-store, and competitor-inferiority claims. |
| BLUF and structure | PASS | The intro and H2 openers answer the section jobs directly. The section sequence remains aligned to the approved outline. |
| MECE coverage | PASS | Covers criteria, taxonomy, source discipline, comparison table, app profiles, safety/privacy checks, Pleasur.ai fit, FAQ, and bottom line. |
| Search-intent alignment | PASS | The target query is commercial comparison. Lines 91-99 now provide source-status rows for Candy AI, RomanticAI, Replika, Nomi, Secrets AI, app-store examples, and Pleasur.ai; lines 123-191 now provide matching app profiles. |
| SERP-feature fit | PASS | Includes quick-answer table, comparison matrix, FAQ, checklist language, visual placeholders, and answer-engine-friendly caveats. |
| Product accuracy | PASS | Pleasur.ai remains framed as one factual create-and-chat option to evaluate, not a universal best app or safer/private/free/unlimited alternative. |
| Adult/sensitive claim safety | PASS | Strong caution around age rules, fictional framing, sensitive data, privacy, deletion, pricing, support paths, and app-store endorsement assumptions. |
| Proof density | PASS WITH NEXT-STAGE WORK | Twenty `[link]` placeholders are tied to sourceable claims. Claim verification must replace them with current sources or remove/soften claims before publication. |

## Metrics Checked

- Word count: 4,367.
- Paragraph metrics: 120 paragraphs, average 35.1 words, median 29, max 659. The max is caused by a wide markdown comparison-table row, not prose bloat.
- Source placeholders: 20 `[link]` placeholders.
- Visual placeholders: 13 typed `[VISUAL:...]` placeholders.
- Table rows: 16 markdown table rows across the quick-answer and comparison sections.
- Formatting checks: 0 em dashes.
- Mirror check: `content-pipeline/5-drafts/ai-girlfriend-apps.md` matches `artifacts/PLE-208/draft-ai-girlfriend-apps-targeted-revision.md`.
- Guardrail scan: no affirmative unsupported Pleasur.ai claims for best, safest, most private, free, unlimited, no-filter, app-store availability, therapy, platform endorsement, competitor inferiority, or guaranteed outcomes.

## Adversarial Read

The strongest part of the revised draft is that it now satisfies commercial-comparison intent without becoming an affiliate-style ranking. The table at `content-pipeline/5-drafts/ai-girlfriend-apps.md:91` gives readers named surfaces to compare, but each cell keeps the right burden of proof: supported source note, volatile facts to verify, and fit caveat. The app profiles at lines 123-191 are also materially better than the prior draft because they apply the same format to every named product and keep Pleasur.ai in the same evidentiary lane as competitors.

The weakest remaining point is citation load. Twenty `[link]` placeholders is expected after adding source-status rows, but it means PLE-202 has real work to do. Candy AI, RomanticAI, Replika, Nomi, Secrets AI, app-store examples, Pleasur.ai product surfaces, DataForSEO demand/SERP facts, and Pleasur.ai Terms/Privacy language all need current source confirmation before the page can publish. Verification should remove any row/profile claim that cannot be sourced cleanly rather than patching it with weak third-party evidence.

One production concern remains: the comparison matrix is wide. That is acceptable in the markdown draft, but the preview/package stage should render it as a responsive table or card grid so mobile readers can scan it without layout breakage.

## Required Next-Stage Checks

- Replace all 20 `[link]` placeholders with verified source links from PLE-196/PLE-199 or current official/public sources.
- Verify the DataForSEO demand and SERP-surface statements at lines 37 and 39 against the accepted 2026-05-25 artifacts before final publication.
- Verify each competitor row/profile fact against official product, app-store, terms, privacy, pricing, cancellation, or help pages before linking it.
- Verify Pleasur.ai product claims at lines 99, 187, 189, 231, and 237-239 against current public product/legal/privacy/pricing surfaces before publication.
- Preserve schema restraint: `Article` or `BlogPosting`, `BreadcrumbList`, and `FAQPage` only if visible FAQ remains; no `Product`, `Review`, `AggregateRating`, `Offer`, or `ItemList` schema without later approval.
- Preserve the guardrail language at lines 99, 103, 131, 181, 191, 221, 227, 239, and 247 during citation editing.
- Keep `/blog/ai-girlfriend-apps` draft-only until the blog-pipeline approval record exists; do not publish, submit sitemap, or request indexing from this stage.
- In preview/package work, render the wide comparison matrix responsively.

## Recommendation

Proceed to PLE-202 claim verification. Do not send back to drafting unless claim verification finds that a material comparison row/profile cannot be sourced and cannot be softened without breaking the article's search-intent value.
