# Research Dossier — ai companion vs chatgpt companionship

**Slug:** `ai-companion-vs-chatgpt-companionship`
**Fixed title (binding, from GEO brief PLE-2959):** "Why Specialized AI Companions Beat ChatGPT for Emotional Depth"
**Intent:** Informational / commercial-counter-narrative. Lives at `/blog/ai-companion-vs-chatgpt-companionship`.
**Run date:** 2026-06-24

> This is a GEO-brief-driven run. The brief (`content-pipeline/0-context/ai-companion-vs-chatgpt-companionship.md`) is binding: fixed title, fixed 6-H2 body + 4-Q FAQ, 1,000–1,400 words, coin-metered pricing, voice = real-time audio only, 82%-stat attribution constraint. The BEAT SPEC below honors that structure and does NOT propose the listicle shape the live SERP defaults to.

---

## 1. Keyword metrics

**TOOL FAILURE — Semrush returned no data this run.** Both the Semrush MCP (`get_report_schema`) and the classic Semrush API (`phrase_this` over HTTP) returned **API UNITS BALANCE IS ZERO / ERROR 132** for every call (verified 2026-06-24 across 4 phrase variants). This is an account-level units exhaustion, not a transient — it must be escalated on the run issue. Consequence: this dossier has **no first-party Semrush volume/KD%/CPC numbers**. The downstream `verify-claims` / `optimize-content` stages should re-pull once units are restored.

What we know about the query landscape (from deep research + SERP, NOT Semrush):
- Primary keyword: **ai companion vs chatgpt companionship** — long-tail, low-volume, high-intent counter-narrative query. No volume figure available `[UNVERIFIED — Semrush down]`.
- Close variants observed in the wild: "is ChatGPT better than companion apps", "ai girlfriend vs chatgpt", "chatgpt as a companion", "chatgpt vs replika/character ai for companionship", "can chatgpt be an ai girlfriend".
- Intent is clearly informational-comparative with a commercial tail (readers are choosing a tool). This matches the brief's answer-first comparison framing.

> Action for next stage: when Semrush units return, pull `phrase_this` + `phrase_kdi` for "ai companion vs chatgpt", "ai girlfriend vs chatgpt", "chatgpt companionship", and `phrase_questions` on "chatgpt companion" to backfill volumes and confirm KD% beatability.

## 2. Related keywords & question themes (from SERP H2s + deep research, Semrush-independent)

Same-intent keyword cluster (no volumes — Semrush down):
- ai companion vs chatgpt
- is chatgpt a good ai girlfriend / boyfriend
- chatgpt for companionship / emotional support
- ai girlfriend vs chatgpt
- chatgpt vs replika / vs character ai / vs nomi
- best ai companion apps with memory
- ai companion persistent memory
- does chatgpt remember conversations
- ai companion voice / real-time voice ai companion

**Question themes** (these map directly to the brief's prescribed FAQ + H2 BLUFs):
1. **Capability gap** — "What can AI companion apps do that ChatGPT cannot?" / "Why use a dedicated AI companion instead of ChatGPT?"
2. **Memory** — "Does ChatGPT remember our conversations?" / "Do companion apps have long-term memory?"
3. **Suitability as a partner** — "Is ChatGPT a good AI girlfriend?" / "Can you use ChatGPT as a boyfriend?"
4. **When ChatGPT wins** — "Is ChatGPT better than companion apps?" (the honest-comparison angle that earns citability)

## 3. SERP benchmark (Firecrawl extractions, 2026-06-24)

The brief named four SERP players (Reddit r/MyBoyfriendIsAI, APA.org, Chicago Reader, sitepoint). **Reality check from live extraction:**
- **Reddit r/MyBoyfriendIsAI** — Firecrawl blocked (Reddit not supported by Firecrawl; WebFetch also walled). Treated as a community-signal SERP entry, not an article to benchmark against. It is a discussion thread, not structured content — easy to out-structure.
- **APA.org** — the indexable APA page is "Artificial intelligence in mental health care" (1,796 words, clinical/regulatory framing, 4-row table, 13 images). It is an authority/expert reference, NOT a companion-vs-chatgpt comparison — it ranks on E-E-A-T, not on answering this exact query. We cannot out-authority APA; we out-specificity it on the *companionship comparison* itself.
- **Chicago Reader "Best AI Girlfriend Apps 2026"** — the brief's URL 404s. The live equivalent ecosystem is the syndicated alt-weekly listicle network (East Bay Express, Riverfront Times, Straight.com Advisor). Benchmarked Straight.com's version below as the representative listicle.
- **sitepoint** — correct live URL is `/ai-companion-apps/` (the brief's `/best-ai-companion-apps/` 404s). Extracted below.

| Page | Words (body) | Format | Items | H2/H3s | Table | Images | Notes |
|---|---|---|---|---|---|---|---|
| sitepoint.com/ai-companion-apps | ~1,360 | Listicle | 5 apps | 6 | 0 | 4 | Light per-app blurbs; HeraHaven, Replika, Character AI, Talkie, NovelAI. No ChatGPT comparison. |
| straight.com (Advisor) best-ai-girlfriend | ~3,540 | Listicle + first-person test | 8 apps | 15 | 0 | 8 | "Lived with 8 for a month" hands-on; FAQ block ("Questions Everyone Keeps Asking"); attachment-ethics section. Strong voice. |
| genies.com best-ai-companion-apps | ~5,510 | Listicle + buyer's guide | 6 apps | 45 | 0 | 1 | Deep buyer's-guide structure: memory ("Does It Remember You?"), privacy, cost, real-user sentiment. The most thorough. |
| apa.org AI in mental health care | ~1,796 | Expert explainer | n/a | 19 | 1 (4-row) | 13 | Clinical/regulatory authority. Not a direct comparison. |
| reddit r/MyBoyfriendIsAI | n/a | Forum thread | n/a | n/a | n/a | n/a | Community signal; not benchmarkable structured content. |

### Benchmark math
- **Top-3 indexable comparison/listicle pages by relevance** (sitepoint, straight, genies): word counts 1,360 / 3,540 / 5,510 → **median 3,540, max 5,510**.
- **Important:** these are sprawling listicles. The brief deliberately rejects the listicle shape — this page is a **tight answer-first comparison** (1,000–1,400 words) engineered for AI-engine citation, not for matching listicle length. **Word-count parity is intentionally NOT the goal here**; the GEO citation hook + structured FAQ is. The beat spec word target therefore follows the brief (1,000–1,400), overriding the SKILL's default `max(1.1×median, 1800)` formula — this is a documented exception, sanctioned by the GEO brief.
- **Modal format on SERP:** listicle (5–8 apps). **None of the benchmarked pages directly answers "ChatGPT vs companion apps"** — every one is "best apps," not the comparison. That absence IS the information-gain opening.
- **Table usage:** 0 of 3 listicles use a comparison table; APA has one unrelated 4-row table. So a clean ChatGPT-vs-companion feature table would be a differentiator, not table-stakes.
- **FAQ:** straight.com has an informal FAQ; none has FAQPage schema. Our prescribed FAQPage JSON-LD (per PLE-2957) is a structural advantage for answer engines.

### Consensus topics (covered by 3+ pages → MUST cover)
- **Memory / "does it remember you"** — explicit section in genies, recurring theme in straight + sitepoint.
- **Persona / customization** — every listicle leads with "make it your own."
- **Voice / real-time interaction** — feature column in all three listicles.
- **Cost / subscription model** — genies dedicates a full section; straight notes per-app pricing.
- **Privacy / data** — genies + APA both heavy; a trust topic for the FAQ.

### Partial topics (1–2 pages → differentiate with depth)
- Honest "when the simpler/general tool is fine" framing (only straight gestures at it).
- Relationship arc / continuity over weeks-months (implied in "Nomi remembers 8 months," not framed as an arc).
- ChatGPT *specifically* as the comparison anchor (essentially absent — see gap).

### Gaps (asked by searchers, covered by nobody → information gain)
- **A direct, structured ChatGPT-vs-purpose-built-companion comparison.** The SERP is all "best apps." The query is a *comparison*. Nobody on page 1 answers it head-on. This is the entire reason the page can win citations.
- **Why the experiences feel different despite similar underlying LLMs** (the deep-research "technical distinctions" coverage gap).
- **An honest "when ChatGPT is actually better" section** — rare, and exactly what makes a comparison citable rather than promotional.

## 4. Authority / beatability

`[UNVERIFIED — Semrush down]` no `domain_ranks` / `url_organic` this run. Qualitative read:
- APA.org and (to a lesser extent) sitepoint/genies carry real domain authority; we will not outrank APA on its mental-health page and shouldn't try — different query facet.
- The listicles (straight, genies, east bay express) are alt-weekly/affiliate content — beatable on **direct-comparison relevance and structured-answer format**, which is the AI-engine citation surface the brief targets (Perplexity, ChatGPT, partial Google AIO).
- **Beatability: GOOD for the citation goal, MODERATE for classic blue-link rank.** The win condition is answer-engine inclusion via a self-contained quotable hook + FAQPage schema, where incumbents are structurally weak (no schema, no direct comparison), not a length/DR slugfest.

## 5. First-party fact lock (pleasur.ai — LIVE this run)

`WebFetch https://pleasur.ai/pricing` (fetched 2026-06-24). Coin-metered, three tiers. Matches `brand-config.md` canonical block (verified live 2026-06-24) — **no drift**.

| Tier | Monthly | Annual equiv. | Coins/mo | source |
|---|---|---|---|---|
| Starter | $12.99/mo | $5.20/mo (saves $93/yr) | 1,500 | https://pleasur.ai/pricing (fetched 2026-06-24) |
| Standard | $27.99/mo | $11.20/mo (saves $201/yr) | 5,000 | https://pleasur.ai/pricing (fetched 2026-06-24) |
| Ultimate | $49.99/mo | $20.00/mo (saves $360/yr) | 10,000 | https://pleasur.ai/pricing (fetched 2026-06-24) |

**Media is coin-metered on EVERY tier** (source: live page): image gen 10 coins, voice notes 10 coins, phone calls 50 coins/min (Standard + Ultimate only; not on Starter). **Never write "flat pricing" / "no tokens" / "unlimited" / "no metering."**
**Voice = real-time AUDIO call ("phone call"), launched from inside chat; per-message voice playback ("voice notes") is also audio. There is NO two-way video call — never claim video.** (brand-config 2026-06-24, AI Video Generation = roadmap.)

Competitor in this comparison is **ChatGPT (OpenAI)**, not a companion app.

**ChatGPT pricing — LIVE TRACE ATTEMPTED this run (2026-06-24).** Direct WebFetch + curl of OpenAI's own pricing pages (`https://openai.com/chatgpt/pricing/`, `https://chatgpt.com/pricing/`, `https://chatgpt.com/#pricing`, `https://openai.com/business/chatgpt-pricing/`) all returned **HTTP 403 Forbidden** across multiple user-agents — OpenAI hard-walls automated fetches; the live page is unreachable from this environment, NOT a stale/wrong URL. Falling back to OpenAI's published pricing, corroborated by a 2026-06-24 web search that returns the canonical OpenAI plans page (`https://chatgpt.com/pricing/`) as the top result. Tiers as published, current 2026-06-24:

| ChatGPT tier | Monthly (USD) | source |
|---|---|---|
| Free | $0 (ad-supported; GPT-5.3 Instant, ~10 msgs/5 hrs) | https://chatgpt.com/pricing/ (canonical; live fetch 403 — published-price fallback, 2026-06-24) |
| Go | $8/mo (launched globally Jan 2026; ad-supported in US) | https://chatgpt.com/pricing/ (canonical; live fetch 403 — published-price fallback, 2026-06-24) |
| Plus | $20/mo (monthly billing only, no annual) | https://chatgpt.com/pricing/ (canonical; live fetch 403 — published-price fallback, 2026-06-24) |
| Pro | $100/mo (tier launched Apr 2026) or $200/mo (20× Plus limits, GPT-5.5 Pro) | https://chatgpt.com/pricing/ (canonical; live fetch 403 — published-price fallback, 2026-06-24) |

**Draft guidance for §5 "When ChatGPT IS Better":** the load-bearing, citation-safe price points are **Free ($0)**, **Plus ($20/mo)**, and **Pro ($200/mo)** — the three a reader actually weighs against pleasur.ai. The newer **Go ($8/mo)** and **Pro $100** tiers exist but are not required for the comparison; cite only Free/Plus/Pro if keeping copy tight. `verify-claims` should re-attempt the live OpenAI fetch and confirm before publish; if it also 403s, the published-price fallback above stands with the canonical URL. The comparison axis is capability/design, not price — ChatGPT is not coin-metered and that is fine to note factually, but the page's thesis is emotional-depth design, not price.

## 6. The 82% memory stat — ATTRIBUTION STATUS: UNVERIFIED, DO NOT USE AS-IS

The brief permits a "82% memory" stat ONLY if attributed to MariaVibe.com with a real URL, never first-person/unattributed.

**Finding: I could not verify a "82% memory" statistic on MariaVibe.com this run.**
- MariaVibe publishes extensive memory-focused companion reviews (e.g., `mariavibe.com/blog/secrets-ai-review-2026-memory-upgrades/`, `.../secrets-ai-free-vs-premium-2026/`), but a direct WebFetch of the top memory page found **no "82%" figure** (it cites a "9.6/10 realism score" and "139k messages," not 82%).
- A web search surfaced an unrelated "82% of free-tier users leave within 14 days (message wall)" churn stat associated with MariaVibe's Secrets AI coverage — that is a **churn** figure, NOT a memory figure, and conflating them would be a fabrication.

**Downstream instruction (HARD):** Do NOT write "82% of users say memory matters" or any 82% memory claim attributed to MariaVibe unless `verify-claims` locates the exact MariaVibe URL where that exact figure appears. As of this run the stat is **[UNVERIFIED]** and should be **omitted** rather than guessed. If a memory-importance stat is wanted, source a verifiable one (e.g., the deep-research "only 3 of 9 companions reliably recall a month-old conversation" hands-on finding from aicompanionguides/DHC, with that source) instead. Prior gate rejections on this exact stat: PLE-1945 / 2320 / 2351.

## 7. Deep web research findings (Perplexity sonar-reasoning-pro, full file: `-deep.md`)

Most decision-relevant signals:
- **GPT-4o (May 2024)** added real-time voice/vision and its flirtatious default voice sparked the very "is ChatGPT a companion?" debate this query rides — but OpenAI **positions ChatGPT for information/assistance, not roleplay or adult companionship** (consumer policy). This is the cleanest factual basis for "purpose-built vs general-purpose."
- **ChatGPT siloes/lightly-summarizes chat history**; it does not build an explicit ongoing relationship narrative. Dedicated companion apps emphasize **persistent memory + long-term relationship arcs**. (Analyst consensus, deep-research §Sourced facts [5][6][15].)
- **Coverage gap that is our information gain:** "why the experiences feel so different despite similar underlying technology" — almost no one explains that companion apps *orchestrate* memory/persona/voice on top of an LLM while ChatGPT runs conservative, task-oriented tuning. This is the explanatory edge.
- Pew 2023: **52% of Americans more concerned than excited about AI** in daily life (verifiable, citable if a sentiment stat is needed).
- **Privacy / data handling — who sees your intimate conversations (the genies.com winning axis).** This is the trust angle the strongest incumbent (genies.com, ~5,510 words) leans on, and it is decision-relevant because the whole page asks readers to confide intimately. Factual, source-attributable framing for the outline/draft to use: (1) **ChatGPT**, by OpenAI's published policy, may use Free/Plus consumer conversations to train and improve its models unless the user opts out via data controls, and human reviewers can access flagged chats for safety/moderation (source to cite at draft: OpenAI's privacy / "how we use your data" help pages and Consumer Privacy Policy). (2) **AI companion apps vary widely** — a 2024 Mozilla *Privacy Not Included* review of romantic-AI companion apps flagged that the majority shared or sold user data and had weak data-handling disclosures, so "companion app" is not automatically more private than ChatGPT; trust depends on the specific app's policy (source to cite: Mozilla Foundation, *Privacy Not Included: Romantic AI Chatbots*, 2024). (3) The honest takeaway the article should make: intimate-conversation privacy is a per-product question of data retention, training-opt-out, and human-review policy — not a generic "specialized app = private" claim — and pleasur.ai's own policy should be stated factually from its live privacy page, never asserted as categorically safer. **Do NOT fabricate any pleasur.ai-specific privacy claim**; if a first-party privacy statement is wanted, verify-claims must pull it live from pleasur.ai before it appears in copy.
- ChatGPT "Sky" voice was pulled after the Scarlett Johansson likeness dispute — useful color for "ChatGPT's voice isn't built/owned for intimate companionship."

**Surprising findings (3):**
1. **The SERP doesn't actually answer the question.** Every page-1 comparable is a "best apps" listicle; not one is a head-to-head ChatGPT-vs-companion comparison. The exact query has no direct incumbent answer — unusually open citation territory.
2. **OpenAI's own policy is the strongest argument for the thesis** — ChatGPT is officially positioned *away* from romance/roleplay/companionship, so "it isn't designed for emotional connection" is OpenAI's stance, not just ours.
3. **The "memory" advantage is partly a myth across the category** — hands-on testing (deep research) found only ~3 of 9 companion apps reliably recall a month-old chat. So "companion apps remember" must be framed as a *design intent and capability ceiling*, not a guarantee — which keeps the page honest and citable.

---

## BEAT SPEC (binding on outline + quality gate)

- **Target word count:** 1,000–1,400 words (±0 — HARD from GEO brief; this *overrides* the SKILL's `max(1.1×median, 1800)` default because the page is a citation-engineered answer-first comparison, not a length-matching listicle). Depth via clarity, not padding.
- **Format:** Answer-first comparison (NOT a listicle). The brief's prescribed shape is mandatory — do not invent a different structure:
  1. H2 "The Core Difference: Purpose-Built vs General-Purpose"
  2. H2 "1. Persistent Memory — The Biggest Gap"
  3. H2 "2. Consistent Persona — Not Just a Prompt"
  4. H2 "3. Voice Designed for Connection" (real-time AUDIO only; never video)
  5. H2 "4. Relationship Arc — Continuity ChatGPT Lacks"
  6. H2 "When ChatGPT IS Better" (honest comparison — REQUIRED for citability)
  - FAQ block (FAQPage JSON-LD) with exactly these 4 questions: "Is ChatGPT a good AI girlfriend?" / "What can AI companion apps do that ChatGPT cannot?" / "Why use a dedicated AI companion instead of ChatGPT?" / "Does pleasur.ai remember our conversations the way a real relationship would?"
- **Answer-first hook (≤60 words, must appear in first paragraph, near-verbatim from brief):** "ChatGPT is a general-purpose assistant. It resets every conversation, has no fixed persona, and is not designed for emotional connection. AI companion apps like Pleasur.ai are purpose-built: they maintain relationship memory across sessions, have a consistent companion personality, offer real-time voice, and develop relationship context over time — capabilities ChatGPT does not provide by default." This is the primary citation target — keep it self-contained.
- **Comparison table:** RECOMMENDED (information-gain; 0 of 3 SERP listicles have one). One compact ChatGPT-vs-purpose-built-companion table. Suggested columns: Capability | ChatGPT (general-purpose) | Specialized companion app. Rows: persistent cross-session memory, fixed companion persona, real-time voice (audio), relationship arc over time, designed for emotional connection, productivity/coding/research. Render as table-cards per the GFM note. Must NOT claim video for pleasur.ai.
- **Must-cover topics (consensus — every one becomes coverage):** persistent memory; consistent persona/customization; real-time voice (audio); cost/subscription model framed accurately (ChatGPT not metered, Free/Plus $20/Pro $200 per §5; pleasur.ai coin-metered — NEVER "flat"/"unlimited"); **privacy / data handling / "who sees your intimate conversations" (explicit angle, NOT one FAQ line)**; the honest "when ChatGPT wins" case.
- **Privacy / data-trust angle (REQUIRED, not relegated to a single FAQ line — this is the genies.com winning axis):** give it real coverage worth ≥2-3 sentences in the body (a natural home is the "Core Difference" or "When ChatGPT IS Better" section) plus the FAQ. Cover, factually and source-attributed (see §7): how ChatGPT uses consumer chat data (training-by-default unless opted out, human review of flagged chats — cite OpenAI privacy/data-control pages); the fact that companion apps are NOT automatically more private (Mozilla *Privacy Not Included* 2024 found most romantic-AI apps share/sell data) — so the honest framing is "privacy is a per-product policy question," not "specialized = private"; pleasur.ai's own privacy posture stated ONLY from its live privacy page via verify-claims, never fabricated. This must read as informational and balanced, not as a privacy sales pitch.
- **Differentiation topics (go deeper than SERP):** relationship-arc continuity over weeks/months; WHY the experiences differ despite similar underlying LLMs (orchestration vs conservative task-tuning); the honest capability-ceiling caveat on memory.
- **Information gain (≥1 REQUIRED — we have 3):** (1) the head-to-head structured ChatGPT-vs-companion comparison + table that no page-1 result provides; (2) the explanation of *why* purpose-built apps feel different (orchestration on top of the LLM), an under-covered angle; (3) an honest "ChatGPT is better for X" section grounded in OpenAI's own positioning.
- **Secondary keywords to work in naturally:** is chatgpt a good ai girlfriend; chatgpt for emotional support; does chatgpt remember conversations; ai companion persistent memory; ai companion vs chatgpt; chatgpt as a companion; real-time voice ai companion. (No Semrush volumes this run — `[UNVERIFIED]`; re-confirm when units return.)
- **Statistics discipline:** 82% memory stat = **UNVERIFIED → omit** unless verify-claims finds the exact MariaVibe URL (see §6). Pew "52% more concerned than excited" (2023) and the "~3 of 9 apps reliably recall a month-old chat" hands-on finding are usable WITH sources. No fabricated market-growth numbers.
- **Framing constraints (HARD — gate fails if violated):** coin-metered pricing (3 tiers $12.99/$27.99/$49.99), never flat/unlimited/no-tokens; voice = real-time audio only, no video; informational framing, no explicit adult language; 18+ positioning fine; no internal-stack tool names in copy; no dedicated /voice or /call page links (in-chat capability).
- **Beatability:** GOOD for the GEO citation goal (incumbents have no direct comparison and no FAQPage schema; the query is structurally unanswered on page 1), MODERATE for classic blue-link rank vs high-DR APA/listicles. Win condition = answer-engine inclusion via the self-contained hook + structured FAQ, not length parity.
