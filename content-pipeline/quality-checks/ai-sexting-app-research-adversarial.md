# Research adversarial — ai-sexting-app

Skeptical review of `content-pipeline/1-research/ai-sexting-app.md` before it feeds the outline. Cross-checked against `-deep.md`, `-data.json`, `0-context/ai-sexting-app.md`, and `brand-config.md`.

## Round 1

### CRITICAL — Candy.AI pricing in JSON contradicts its own prose disclaimer
The prose dossier is explicit: "Candy.AI homepage live — **No flat monthly USD on homepage** — third-party reviews place it ~$5.99/mo annual. Plan-detail pricing is gated until trial activation." Yet `ai-sexting-app-data.json` flattens this to `"Candy.AI": 5.99` in `pricing_comparison`, with the caveat buried in `pricing_comparison_meta`. A draft that reads the JSON chart values verbatim (or the visuals stage that builds a price-comparison matrix from JSON) will publish "$5.99/mo" as a clean fact and violate the project memory `feedback_recheck_competitor_pricing` (PLEAA-568: brief said Muah $9.99, live was $19.99). Same failure mode applies to **CrushOn AI** — `"CrushOn AI": 5.99` is sourced from "third-party reviews" while the homepage returned 403. Two of four picks have non-live pricing dressed as live data. Either re-verify both (proxy, archive.org, app-store listing) or drop the number from the chart and use "trial-gated / not published" labels.

### CRITICAL — CrushOn as the 4th slot is under-defended vs Joi / Soulgen / Nastia / Botify
The context file explicitly flagged the 4th-slot decision as open: "plus one more like Joi/Soulgen/Nastia/Botify based on SERP." The dossier silently picked CrushOn AI with no comparison shown. Yet the dossier's own SERP data argues against CrushOn: it is **not** in the top-10 SERP for `ai sexting app` (Botify *is* at #3 with 39 traffic; Nastia is live-verified with voice+image+video; CrushOn returned 403 and has no voice/video per the feature matrix). Botify also dominates by cluster volume (botify ai = 18,100 vol vs the primary 480). The angle "honest 4-app roundup" is fatally weakened if the 4th pick is the one with the weakest feature set and worst live verifiability. Force a written defense of CrushOn vs Botify or swap it.

### HIGH — The "MyAnima ranks itself #1, no disclosure" hook is verifiable but pre-emptable
The dossier leans on this as the differentiating ethics angle. It's real (myanima.ai/blog/best-ai-sexting-apps is in the SERP at #8) but (a) it's not actually surprising — affiliate/owned-listicle bias is table-stakes in this niche, and (b) any competitor could neutralize the hook in one sentence ("MyAnima rates themselves #1 on their own blog, we won't"). Rating: `dressed-up-table-stakes`. The "Mozilla PNI + HIBP Muah breach as a buying criterion" angle is stronger and *actually* surprising in this SERP — anchor the differentiation there, demote MyAnima to one sentence.

### HIGH — Deep research returned nothing usable; dossier never flags this as a sourcing risk
`ai-sexting-app-deep.md` is empty by Perplexity's choice (it refused to fabricate sources after a Placer.ai noise hit). The dossier acknowledges this in one line ("we will not cite the deep file") but doesn't downgrade the downstream confidence on regulatory / WaPo / Reddit themes. The dossier asserts WaPo ranks #2 on a "teens-sexting-ai-chatbots-parents" piece but WebFetch was blocked — the URL, headline, and publication date are unverified from the live SERP scrape; a draft that quotes WaPo by name needs the article opened (archive.org or a proxy) or the citation pulled.

### HIGH — Privacy section anchors are correct but undated/unlinked in the dossier
Mozilla PNI Feb 2024 and HIBP Muah Sept 2024 are the right anchors (they're the strongest public data points in this niche and align with `feedback_live_verify_schemas` discipline). But the dossier doesn't include the actual URLs — just the names. A draft will inherit citation-thin claims unless the outline forces URL capture at this stage. Add: `https://foundation.mozilla.org/.../privacy-not-included/articles/happy-valentines-day-romantic-ai-chatbots/` and `https://haveibeenpwned.com/PwnedWebsites#MuahAI`.

### MEDIUM — Pleasur.AI internal modules / brand-reference not surfaced
The dossier mentions Pleasur.AI pricing and "disclose ownership once near the top" but doesn't pull from `content-pipeline/2-reference/ai-sexting-app.md` (which exists) — there's no enumeration of internal modules or related Pleasur.AI articles the draft can cross-link. Brand fit risk: generic roundup feel.

### MEDIUM — JSON `traffic_top_pages` keys "play.google.com (Botify AI)" / "reddit.com (r/ios)" won't render cleanly
If the visuals stage builds a SERP traffic bar chart, the parenthetical-in-key formatting will produce ugly axis labels. Cosmetic but predictable.

## One thing that works (round 1)

The pricing-opacity story for Candy.AI is genuinely a differentiator — "homepage gated until trial activation, Visa/MC + BTC/ETH/USDC/LTC, no flat monthly USD" is observable, specific, and not in any of the SERP-ranking listicles. That's the kind of texture the dossier promises to deliver.

## Round 1 verdict: FAIL

Two CRITICALs blocked handoff. One revision pass requested.

---

## Round 2 (current)

Re-checking the revised dossier + JSON after one revision pass.

### CRITICAL 1 (pricing contradictions) — RESOLVED
`pricing_comparison` no longer launders third-party numbers. Candy.AI = `"gated"`, Nastia = `"free-tier-only-public"`, OurDream = `19.99` (live), Pleasur = `27.99` (live). `pricing_verification` meta is complete, honest, and per-URL: Candy `/pricing` + `/upgrade` both labeled `404`, CrushOn 4 URLs labeled `403`, Botify labeled `live-but-content-not-extractable`. Any downstream visuals stage reading the JSON will get a `"gated"` string, not a fake float. Prose ("JSON records Candy as `gated`. The opacity is part of the story.") matches the data. Clean fix.

### CRITICAL 2 (4th-slot defense) — RESOLVED
The dossier now contains an explicit `## 4th-slot pick: defense of Nastia (vs CrushOn vs Botify)` section that compares all three on live-verifiability, feature matrix, and SERP signal, and ships the "what about Botify?" one-line answer for the article. Nastia is defensible: homepage extractable, full feature set (chat / group chat / voice / image / video / custom character), quotable privacy statement verbatim, free tier verified. The trade-off (loses SERP rank vs Botify, wins on every other criterion) is named, not hidden. Pick stands.

### HIGH (MyAnima / Mozilla anchors) — RESOLVED
MyAnima is demoted to "a one-sentence footnote in the privacy section" in the top-page summary and to a one-line footnote in the recommended-angle section. Mozilla PNI and HIBP Muah are now lede anchors with full URLs + dates + specific stats (90% may share/sell, 90% failed security, 73% no vuln process, 64% no encryption info, 54% deletion option, 1.9M Muah accounts). `_meta.privacy_anchor_urls` carries the URLs in JSON for the citation step.

### NEW findings introduced by the revision

#### LOW — WaPo headline still unverified
The HIGH from round 1 about WaPo body text being unverifiable isn't fully closed — the dossier still names the URL and the May 2025 framing without an archive.org fallback. The editorial constraint "quote the headline + URL only, do not assert body text from this source" is now explicit in the dossier prose, which is the right guardrail; the outline + verify-claims stages will enforce. Not a blocker.

#### LOW — JSON `traffic_top_pages` key formatting still cosmetic
"play.google.com - Botify AI" / "reddit.com - r/ios" replaced the parentheticals but will still produce long axis labels if the visuals stage charts this dict. Cosmetic, easy fix at visuals stage.

#### LOW — Feature matrix gives Candy.AI `video: true` without a live source
`feature_matrix.Candy.AI.video = true` is asserted while the pricing/plan detail page is gated (404). The feature presumably comes from the homepage hero copy, but the dossier prose doesn't cite where the video claim was verified. Outline stage should require a "verified-on-homepage" footnote for any feature claim per app, or downgrade to `unknown`. Not a blocker for outline handoff.

### MEDIUM (brand-reference) — STILL OPEN BUT DEFERRED
The round-1 MEDIUM about Pleasur.AI internal modules not being surfaced isn't directly addressed in the revised dossier, but `/brand-reference` is the next stage and runs in parallel — the orchestrator picks up internal modules there. Acceptable to defer.

## One thing that works (round 2)

The 4th-slot decision section is exactly the kind of decision-log a downstream writer needs: it names the competing options, the criteria, and the trade-off in one paragraph. If every dossier section had this structure, the outline stage would be half-done before it starts.

## Verdict: **PASS**

Both round-1 CRITICALs are resolved. No new CRITICAL items introduced. The three new LOW findings are outline-stage guardrails, not research-stage blockers. Advance to `/outline`.
