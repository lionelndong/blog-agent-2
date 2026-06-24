# Research Adversarial — ai-companion-vs-chatgpt-companionship

Stage: 1b (research-adversarial), REVISION PASS 1 (final — research revision budget exhausted
after this). Reviewer: skeptical research lead (Task sub-agent) + adjudication against the prior
FAIL and the skill's CRITICAL definition. Date: 2026-06-24. Inputs: 1-research/{slug}.md,
{slug}-deep.md, {slug}-data.json, 0-context/{slug}.md, brand-config.md.

Prior pass FAILed on ONE CRITICAL: "ChatGPT competitor pricing not traced live this run." This
pass judges whether the revision cured it, plus a fresh read.

## Findings

### CRITICAL

- **None this pass.** The single prior CRITICAL is cured (see below). No remaining finding meets
  the skill's CRITICAL bar once the "internal Semrush/Strapi reference is an acceptable source"
  rule (skill question 1) and the 403-fallback fairness standard are applied. See HIGH items —
  they are real and gate verify-claims, but they are not draft-on-a-wrong-foundation defects.

### Prior CRITICAL — now RESOLVED

- **ChatGPT pricing IS now traced with a documented live attempt + corroborated fallback.** §5
  records: "Direct WebFetch + curl of OpenAI's own pricing pages (...) all returned **HTTP 403
  Forbidden** across multiple user-agents — OpenAI hard-walls automated fetches; the live page is
  unreachable from this environment, NOT a stale/wrong URL." It then falls back to OpenAI's
  published pricing "corroborated by a 2026-06-24 web search," tags **every** ChatGPT table row
  `live fetch 403 — published-price fallback, 2026-06-24`, and instructs `verify-claims` to
  re-attempt the live fetch before publish. This is the best achievable given OpenAI's bot wall and
  is honestly recorded per-line. Per the PLE-2330 competitor-claim standard and the explicit
  fairness rule for documented-403-with-published-fallback, this is **NOT** re-flagged CRITICAL.

### HIGH

- **The "3 of 9 apps reliably recall a month-old chat" stat has no resolvable source in this run's
  artifacts.** It is the backbone of Surprise #3 (the "memory advantage is partly a myth"
  information-gain finding) and is offered in §6 as the *replacement* for the omitted 82% stat.
  §6/§7 attribute it to "aicompanionguides/DHC hands-on testing," and -data.json's
  `sentiment_stats._meta` says "hands-on 9-app recall test" — but **-deep.md contains no 3-of-9
  finding, no 9-app recall test, and no aicompanionguides/DHC source anywhere.** Provenance is
  unresolvable from the artifacts this run produced. The dossier does honestly tag it (it routes the
  number to verify-claims and frames the memory advantage as "design intent and capability ceiling,
  not a guarantee"), so it is not draft-fatal — but `verify-claims` MUST attach a real URL or the
  draft MUST drop the specific "3 of 9" number and keep only the qualitative "not every app
  reliably remembers" framing. HARD gate on verify-claims; do not let "3 of 9" reach copy unsourced.

- **Privacy/data-trust axis is now REQUIRED and source-attributed, but pleasur.ai still cannot OWN
  it.** The revision correctly elevates privacy from one FAQ line to a binding body axis (BEAT SPEC
  "Privacy / data-trust angle (REQUIRED)") with balanced, citable framing: ChatGPT training-by-
  default + human review of flagged chats (OpenAI privacy/data-control pages), and the Mozilla
  *Privacy Not Included* 2024 finding that most romantic-AI apps share/sell data (so "specialized ≠
  private"). This fully addresses the prior HIGH (genies.com privacy depth). BUT §7 deliberately
  forbids any pleasur.ai-specific privacy claim until verify-claims pulls it live — so the page will
  *match* genies on privacy substance, beating it only on structure (FAQPage schema + direct
  comparison), not on owned first-party privacy material. Acceptable for the gate; flagged so the
  draft does not over-promise a privacy differentiator the dossier cannot yet supply.

### MEDIUM

- **ChatGPT fallback prices self-reference the 403'd URL; the corroborating search result is named
  but not linked.** Every row sources to `https://chatgpt.com/pricing/ (canonical; live fetch 403
  — published-price fallback...)` — the corroborating "2026-06-24 web search" is asserted but its
  secondary result (news/Wikipedia/etc.) is not captured as a URL. The load-bearing comparison
  numbers (Free $0, Plus $20, Pro $200) are mainstream-stable, so this is polish, not a blocker —
  but verify-claims should capture the corroborating secondary URL when it re-attempts.

- **Surprise #3 is honest but, as sourced, leans on the unverified 3-of-9 number** (see HIGH). The
  insight (memory is a design intent, not a category guarantee) is genuine and citable as
  qualitative framing; only the specific 3/9 figure is unsupported. Surprises #1 ("the SERP doesn't
  answer the question" — backed by the §3 gap analysis) and #2 ("OpenAI's own policy is the
  strongest argument for the thesis" — §7, OpenAI consumer-policy positioning) are
  `actually-surprising` and load-bearing.

### LOW

- **Bracket-number citations in §7 are an acceptable internal reference, not a CRITICAL gap.** The
  ChatGPT memory-siloing claim cites "deep-research §Sourced facts [5][6][15]." Perplexity's
  -deep.md uses inline [n] markers without a trailing reference list, so [5][6][15] don't resolve to
  bare URLs — but (a) the skill explicitly accepts "an internal Semrush/Strapi reference," and a
  pointer into -deep.md is exactly that, and (b) "ChatGPT siloes/summarizes chat history rather than
  building a relationship narrative" is table-stakes, non-numerical, analyst-consensus framing, not
  a hard stat. Noted for hygiene; not a gate failure.

- **data.json ↔ prose consistency is clean.** Spot-checked `genies 5510` ✓, `straight 3540` ✓,
  `pleasur ultimate 49.99` ✓, `phone_call_coins_per_min 50` ✓, `pages_with_chatgpt_vs_companion_table: 0` ✓,
  `pew_2023... 52` ✓. The only sourcing soft-spot is `companions_reliably_recall_month_old_chat_count: 3`,
  consistent with the HIGH above. ChatGPT $20/$200 appear in prose, not in JSON — consistent with
  them being fallback-tagged.

## First-party fact trace (PLE-2330) — PASS

Every pleasur.ai price/tier/coin/metering claim carries `source: https://pleasur.ai/pricing
(fetched 2026-06-24)` FROM THIS RUN: all three tiers ($12.99/$27.99/$49.99), coin allowances
(1,500/5,000/10,000), and the per-action meter (image 10, voice note 10, phone call 50/min,
Standard+Ultimate only). §5 records a live WebFetch this run, "Matches brand-config.md... no
drift," with the "never flat/unlimited/no-tokens" and "real-time audio only, no video" guards
explicit. Mirrored cleanly in -data.json. No own-product price/feature claim is missing a live
first-party source.

## Notable correct calls (worth preserving)

- **The 82% MariaVibe OMIT remains correct** (pre-adjudicated acceptable; not re-flagged). §6 tried
  to verify, found only a 9.6/10 realism score and a "139k messages" figure (no 82% memory stat),
  caught that the only wild "82%" is a *churn* stat, and warns conflating them "would be a
  fabrication." Disciplined; right given PLE-1945/2320/2351.

- **Semrush units-zero (ERROR 132) honestly quarantined** (pre-adjudicated acceptable; not a
  failure cause). All volume/KD/CPC tagged `[UNVERIFIED — Semrush down]`; the BEAT SPEC's title /
  6-H2 / word-count derive from the GEO brief, independent of Semrush, so zero outline decisions
  depend on the missing metrics. Re-pull routed to verify-claims/optimize-content.

## What works

The exact thing that FAILed last pass is fixed: ChatGPT pricing now carries a documented live-fetch
attempt (403 across multiple UAs, recorded verbatim) + a published-price fallback tagged per-line
with a verify-claims re-attempt instruction — the best achievable against OpenAI's bot wall. On top
of that, the new REQUIRED privacy/data-trust axis (OpenAI training-by-default + Mozilla *Privacy
Not Included* 2024, both source-attributed) cures the prior genies.com privacy HIGH. The
first-party pricing lock (§5) stays exemplary.

## Verdict: **PASS**

The blocking prior CRITICAL is resolved; no finding meets the skill's CRITICAL bar this pass. The
two HIGHs (the unsourced 3-of-9 recall stat; pleasur.ai having no first-party privacy material to
*own* the new axis) are real and carry HARD verify-claims gates, but neither builds the article on a
wrong angle or a wrong own-product fact — the dossier honestly tags both and routes them downstream.
This is the final research revision; the dossier is good enough to feed the outline, with the
verify-claims gates above carried forward.
