# Brand reference: is candy ai safe

**Inventory source:** Strapi API cache `content-pipeline/brand-articles.json` (23 published articles, fetched 2026-06-13T15:23Z via `fetch_strapi_inventory.py` through Doppler; re-run confirmed cache fresh — non-empty, live, no web-crawl fallback needed). All slugs below verified against that inventory. Cache carries titles + URLs + dates but not H2s/excerpts, so voice/module mining was done against the sibling reference dossiers in `2-reference/` (which were mined from the live cited bodies). No research dossier exists yet at `1-research/is-candy-ai-safe.md` — scoring uses the brief's target queries + the brand's safety/privacy cluster.

**Compliance reminders for the drafter (carry into outline + draft):**
- This is a GEO/AEO safety-comparison answer page, ~1,100–1,600 words. Page SHAPE is fixed by the brief (BLUF answer → 4-column safety table → 5-bullet checklist → 6-Q FAQ → CTA). Do NOT pad into a benchmark listicle.
- Do NOT call any platform definitively "unsafe" without a cited regulatory action. Attributed language only ("reviewers have noted", "Italy's regulator required", "the FTC complaint alleged").
- Cite REAL external sources only (nordvpn, expressvpn, aicompanionguides, our own privacy policy). Do NOT fabricate stats or invent numbers.
- Pleasur.ai data-practice claims MUST trace to the live `pleasur.ai/legal/privacy-policy`. Never claim Pleasur.ai is guaranteed "safe"/"private" in absolutes. Positioning = transparency + a published policy, never a direct attack on a competitor.
- NO "no-filter / anything-goes" framing. 18+ throughout. No real-person likeness / deepfake framing in imagery.
- Internal-stack scrub: never name internal tools/vendors (Strapi, Doppler, Semrush, PostHog, OpenRouter, Firecrawl, Paperclip, etc.) in reader-facing copy or metadata.

## Existing articles on this topic (top matches)
- [AI Companion Safety Checklist: What to Check Before You Chat](https://pleasur.ai/blog/ai-companion-safety-checklist) — 2026-05-24 — **REQUIRED / VERIFIED-LIVE INTERNAL LINK** (200 OK, brief 2026-06-15). The site's canonical "how to vet a companion app for safety" page. It owns the safety-checklist head intent — link to it from the 5-bullet checklist section, do NOT re-rank or re-argue the full checklist here (cannibalization risk: keep this page's checklist to 5 tight bullets, then link out for the deep version).
- [Best Replika Alternative in 2026: Memory, Freedom & Privacy](https://pleasur.ai/blog/best-replika-alternative-2026) — 2026-06-12 — **VERIFIED-LIVE INTERNAL LINK** (200 OK, brief 2026-06-15). Our live Replika page (the brief's `/blog/replika-alternative` is a 404 — DO NOT use it). Source of the honest-comparison verdict + privacy/freedom framing. Link from the Replika table row / "Is Replika safe?" FAQ. Closest structural twin (head-to-head + honest verdict + answer-first FAQ).
- [What Data Do AI Girlfriend Apps Really Collect? Privacy Guide 2026](https://pleasur.ai/blog/ai-girlfriend-app-privacy-data-guide-2026) — 2026-06-12 — present in live Strapi inventory; the sibling `pleasur-ai-vs-secrets-ai` reference treated it as LIVE. **Not independently re-verified by the brief — confirm 200 OK at draft/cite time before linking.** Best topical match for the "where do conversations go / what data is collected" axis and the transparency positioning; ideal for the "most private" FAQ and the data-storage table row.

Also adjacent (in inventory, useful as fair-comparison context, not required links): [Muah AI Review](https://pleasur.ai/blog/muah-ai-review) and [CrushOn AI Review 2026](https://pleasur.ai/blog/crushon-ai-review-2026) — single-competitor "honest look, what it does / where it breaks" template that models the attributed, non-disparaging voice the safety page needs.

## Reusable voice modules (mine the framing, not the wording)
- **Honest-comparison verdict module** (from `best-replika-alternative-2026`, `muah-ai-review`, `crushon-ai-review-2026`): name the competitor truthfully, acknowledge what it does, then be specific and sourced about the safety/privacy gap. No disparagement. This is the exact register the brief's compliance notes demand ("reviewers have noted...", "the FTC complaint alleged...").
- **Transparency / "how we handle your data" module** (from the privacy guide + Replika page): frame Pleasur.ai's edge as *a published, readable privacy policy you can check yourself* — not a claim that it is "safe." Anchor every Pleasur.ai data claim to `pleasur.ai/legal/privacy-policy`.
- **Answer-first FAQPage module** (from `ai-companion-safety-checklist`, `best-replika-alternative-2026`, `janitorai-alternatives-2026`): BLUF in the first sentence of each Q&A. Mirror for the brief's 6 required FAQs, each answer ≤50 words. Template auto-emits FAQPage JSON-LD — keep clean Q/A pairs.
- **At-a-glance comparison-table module** (from `character-ai-alternative`, `janitorai-alternatives-2026`): reuse the feature-by-app table shape for the fixed 4-column safety table (Candy AI / Replika / Nomi AI / Pleasur.ai × data storage / privacy policy / regulatory history / age verification).
- **Citeable-checklist module**: the "what to check before you chat" framing already lives in `ai-companion-safety-checklist` — compress to exactly 5 bullets, written to be liftable as an AI-Overview answer.

## Product use-cases to anchor positioning (live products only, from brand-config)
- **AI Companion Creator (`/create`, LIVE)** — the flagship; the "build and chat with a custom companion" payoff. Frame as the transparent-alternative CTA destination, not a safety guarantee.
- **AI Image Generation (`/generate`, LIVE)** — in-chat / on-demand image creation; mention only lightly if the table touches feature scope. No real-person likeness framing.
- Voice Replies / Phone Call are **in-chat capabilities of the Creator, COMING-SOON** — do NOT build a walkthrough around them and do NOT link a `/voice` or `/call` page (none exists). AI Video = roadmap, do not surface.
- Positioning anchor (not a product page): `pleasur.ai/legal/privacy-policy` is the citable proof of the transparency claim — the single most important "product" on this page.

## Internal-linking opportunities (by planned section — VERIFIED-LIVE only as required links)
- **"What to look for in a safe AI companion" (5-bullet checklist)** → [/blog/ai-companion-safety-checklist](https://pleasur.ai/blog/ai-companion-safety-checklist) — anchor: **"AI companion safety checklist"** (one mention, deep-dive link; do not duplicate its full list).
- **Replika table row / "Is Replika safe?" FAQ** → [/blog/best-replika-alternative-2026](https://pleasur.ai/blog/best-replika-alternative-2026) — anchor: **"best Replika alternative in 2026"** (descriptive, matches its H1).
- **Privacy-policy reference + every Pleasur.ai data claim + CTA** → [/legal/privacy-policy](https://pleasur.ai/legal/privacy-policy) — anchor: **"published privacy policy"** / **"its privacy policy"**.
- **"Most private" FAQ / data-storage axis (OPTIONAL — confirm 200 OK first)** → [/blog/ai-girlfriend-app-privacy-data-guide-2026](https://pleasur.ai/blog/ai-girlfriend-app-privacy-data-guide-2026) — anchor: **"what data AI girlfriend apps collect"**.
- Product CTAs (not blog links): `/create`, `/legal/privacy-policy`.

## Voice / framing notes
- House comparison voice: practical, direct, evidence-led, second person; BLUF first. Short paragraphs (1–4 sentences), 8th–9th-grade reading level. Lead with the reader's safety decision, not hype.
- Treat the page as a citeable answer surface: write the opening ~60 words and every FAQ answer to be liftable verbatim by an AI Overview, sourced and non-absolutist.
- Watch the forbidden-phrase list (no "leverage," "delve," "game-changer," "comprehensive guide," "when it comes to," "in the digital age," filler em-dashes, participle-triplet lists). Never name our internal stack.
