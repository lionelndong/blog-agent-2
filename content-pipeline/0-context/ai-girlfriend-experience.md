# Context for ai-girlfriend-experience

Reddit-flavored SERP. Validate PLEAA-418 visuals-adversarial loop end-to-end.

This is a validation run for PLEAA-435 (child of PLEAA-421). Goal: exercise the /visuals-adversarial loop on a topic whose SERP naturally pulls Reddit testimonial captures via PLEAA-417 broadened external sourcing.

Acceptance criteria:
- AC #1: /visuals-adversarial strips ≥1 decorative entry, flags ≥1 missing visual, triggers exactly one revision pass through /generate-visuals.
- AC #2: Final orchestrator report shows `visuals: 1/1 revisions used`.

Run env: BLOG_AGENT_AUTONOMOUS=1 BLOG_AGENT_VISUALS_REVISION_BUDGET=1 BLOG_AGENT_AUTO_PUBLISH=0 (validation; NOT a publish). If pipeline finishes PASS, leave as draft for the CMO-coordinated publish cadence.

Audience: anonymous adult-curious consumers researching what an AI girlfriend chat is actually like. Educational + experiential framing — what the experience feels like, what the limits are, how Pleasur.AI fits as a recommended option (not the topic of every paragraph).

Voice: see blog-agent-2/examples/ and brand-config.md. Reverse-engineer; do not invent tone. Pleasur.AI mentions thin (≤1 per ~250 words). Brand spelling: Pleasur.AI — never "Pleasure AI", "Pleasure Ai", or "Pleasurai".
