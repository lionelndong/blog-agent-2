# QA / research-scaffolding scrub — published-article sweep (2026-06-17)

**Issue:** PLE-2646 · **Owner:** EO · **Trigger:** leak found on live `/blog/ai-sexting-app` during PLE-2642.

## What leaked
Internal content-pipeline QA/research metadata was rendering inside published
`shared.rich-text` blocks — never meant for readers. Hurts E-E-A-T/trust and
reads as unfinished. Five distinct leak shapes, none caught by the old
`strip_editor_notes` (which only matches a literal `## Editor notes` heading):

1. HTML-comment QA markers + the tail behind them (`<!-- VOICE-FLAGGED -->`, `<!-- CITATION DENSITY -->`, "Anchor URLs resolution status", "Must-cite claims identified").
2. `_Visual asset: v… . Target section: …_` manifest captions under images.
3. Editor-note anchors mid/end-body (`<a id="editor-note-serp">…Editor: confirm whether…`) + internal file paths (`content-pipeline/1-research/…md`).
4. Raw keyword-research dumps in prose ("keyword baseline", "9,900 US monthly searches", "$3.08 CPC", "research/SERP artifact captured").
5. Self-referential production vocabulary ("our source review", "sampled SERP", "before publication", "the approved draft language is narrow", "this packet", "belongs in the comparison", "SERP competitor").

## Sweep result — 30 live articles scanned (Strapi `publicationState=live`)
**8 articles cleaned** (PUT via Strapi API, `publishedAt` preserved-as-published, media counts preserved, re-fetched + diffed):

| slug | documentId | what was stripped/reworded |
|---|---|---|
| ai-sexting-app | evxrpgjvo6ey7m9kkovmtj55 | full QA tail (VOICE-FLAGGED + CITATION DENSITY + anchor-resolution) off last block; 8181→4854 chars |
| ai-girlfriend-experience | qwb0524sc1k69mumpwv8jahi | `<a id=editor-note-serp>` editor note + 3 dead anchor links + "research dossier" |
| how-to-make-an-ai-girlfriend | wp16nc78psrpxibi1i6h1s3a | keyword-baseline dump (volume/intent/difficulty) + 5× "SERP" jargon |
| ai-chatbot-app-guide-2026 | nb79w3rytvr4uy18jenmp62d | "$3.08 CPC" (×2) + "(keyword baseline, 2026)" |
| character-ai-alternative | vw0i1f36s7bshgfezdfv77d4 | file-path attribution + keyword-baseline/SERP-artifact passage + 11 `_Visual asset:_` captions |
| ai-girlfriend-apps | pjg2gftzwcspxx33dziuldj5 | 13 `_Visual asset:_` captions + ~25 production-vocabulary phrases throughout |
| ai-sexting | g0ktv85eeosy1ddocogy8yxb | "By our count of current search data…" demand-framing reword |
| ai-girlfriend-simulator | clym73j0nrwsik3taapf5xki | "before publication" editorial-process phrasing |

**Verified clean:** final full-corpus grep across 30 articles → **0 QA-marker hits**.
Live-rendered HTML confirmed clean (HTTP 200, correct H1) for the 6 articles
surfaced on the frontend.

## Not-a-leak (false positives, left unchanged)
- `yandere-ai-girlfriend-simulator` — "the adversarial escape room" is legitimate game description.

## Frontend note (NOT caused by this edit → CTO)
- `ai-girlfriend-simulator` is published in Strapi AND in the sitemap, yet the Next.js route returns a genuine 404 (x-powered-by: Next.js, not Cloudflare). A body-only PUT (slug + publish status unchanged) cannot create a 404 → pre-existing ISR/routing issue.
- `ai-chatbot-app-guide-2026` is published in Strapi but absent from the sitemap and 404s on the frontend (orphaned from the live site; created 2026-03-23).
Both routed to CTO (website codebase / revalidation).

## Durable fix (prevents recurrence)
`/.claude/skills/format-for-publish/scripts/format_for_strapi.py` (commit `29806fa`, pushed):
- `scrub_pipeline_scaffolding()` — auto-removes HTML comments + `_Visual asset:_` caption lines before anything reads the body.
- `assert_no_pipeline_leak()` — hard-fails the publish on high-precision inline production vocabulary (same posture as the leftover-`[VISUAL:…]` gate), forcing an editorial fix rather than a silent rewrite.
Tested: auto-strip removes comments/captions + keeps prose; gate fires on all 8 leak classes; clean prose (incl. "adversarial escape room") passes. SKILL.md step 2a documents it (commit `8346700`).
