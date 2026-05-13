# Context for ai-sexting-app (v2 — full pipeline redo)

Category/list intent, 2026 US-focused roundup of AI sexting apps for adult readers. Pleasur.AI is one of four options covered fairly, NOT the centerpiece — list it last with an explicit "this is our app" disclosure.

Avoid concentrating on Muah AI (already covered Mon as muah-ai-review; only reference it as the privacy/breach anchor via HIBP, not as a featured pick). Other picks should reflect the actual top-10 SERP: scribehow listicle, Mashable, Washington Post, myanima, whatsthebigdata — pick the actual competitors with live products (likely Candy.AI, OurDream.AI, CrushOn AI, plus one more like Joi/Soulgen/Nastia/Botify based on SERP).

Apply Ryan Law's BLUF/MECE/Problem→Agitate→Solution rigor. Real prices live-verified on each /pricing page. Privacy section is non-negotiable — Mozilla *Privacy Not Included* Feb 2024 + HIBP Muah breach are anchor citations.

Visuals must EARN their place per `templates/editorial-principles-visuals.md` — default is `none`, use concrete subjects (phone UI mockups, app-store-style cards, comparison matrix) not abstract "glowing rectangles". Aim for ≤3 visuals total, each one carrying specific information the prose can't.

Quality-check FAIL or BORDERLINE-with-CRITICAL halts. ContentShake target SEO+Quality ≥ 8. Word target 2000–2500.

**Publish path:** final article goes into Strapi document `evxrpgjvo6ey7m9kkovmtj55` (slug `ai-sexting-app`, id 1329) via PUT — the slug is already live from the v1 run, do NOT POST a new article. BLOG_AGENT_AUTONOMOUS=1 is implied (no human-in-the-loop prompts).

## Why v2

v1 (this morning) compressed the whole pipeline into one omnibus subagent — Ryan Law's stage discipline (research-adversarial, outline-adversarial, product-mentions, optimize-content, visuals-adversarial) was skipped. CEO rejected the result: "image are not good quality, blog quality not good, did not follow Ryan's law pipeline." This v2 runs every stage as its own fresh Agent dispatch per the orchestrator spec.
