# Research Dossier — "ai companion memory"

- **Slug:** ai-companion-memory
- **Intent:** Informational / commercial-investigational. Searcher wants to understand (a) how memory works in AI companions — what it remembers, how it persists, how it fails — and (b) which apps actually have good memory. The SERP is a listicle/explainer hybrid: ranked "best AI companions with memory" lists sit beside "how AI companion memory works" explainers.
- **Brand:** Pleasur.AI — position as a companion built for **memory-driven, persistent roleplay** with a privacy-conscious architecture. Educate honestly about how memory works and degrades; let the practical buying criteria favor a platform that treats continuity as a core feature, not a put-down of rivals. No "unlimited memory" or "never forgets" absolutism. 18+ framing throughout.
- **Run date:** 2026-06-23

> **Tooling note (failure):** Semrush MCP AND the classic Semrush API both returned `API UNITS BALANCE IS ZERO` this run. Primary keyword volume / KD% / CPC could NOT be pulled from Semrush. The SERP benchmark below was rebuilt from live Firecrawl extraction of the top organic pages (2026-06-23) and the deep-research pass (OpenRouter perplexity/sonar-reasoning-pro). All keyword *metrics* are marked `[UNVERIFIED — Semrush units exhausted]`; the SERP *structure* figures (word counts, item counts, format) are measured directly from extracted pages and are reliable. Re-run the Semrush steps once units are topped up to backfill exact volume/KD numbers.

---

## 1. Keyword metrics

| Metric | Value | Source |
|---|---|---|
| Primary keyword | ai companion memory | — |
| Search volume (US/mo) | `[UNVERIFIED — Semrush units exhausted]` — informational head term; SERP depth (5 long-form commercial pages, 6–9 apps each) signals real, growing volume | — |
| KD% | `[UNVERIFIED — Semrush units exhausted]` | — |
| CPC | `[UNVERIFIED]` (informational lead-in; commercial downstream via companion-app signups) | — |
| SERP intent | Informational + commercial-investigational ("how does it work" + "which apps have the best memory") | live SERP shape (Firecrawl, 2026-06-23) |

### Same-intent / secondary keywords (from live SERP titles + topic graph)
Marked `[UNVERIFIED volume]` — fold into outline subtopics: ai companion with memory; ai chatbot that remembers you; best ai companion with long-term memory; how does ai companion memory work; ai girlfriend that remembers conversations; persistent memory ai chatbot; ai companion memory limit; do ai companions remember you; ai companion long-term memory; ai companion that remembers everything; memory in ai roleplay.

### Question themes (PAA + community, grouped)
1. **How it works** — how does AI companion memory work; what does an AI companion actually remember; short-term vs long-term memory; does it use a vector database or just the prompt window.
2. **Limits/failure** — how many messages does it remember; why did my AI companion forget; does memory degrade; what triggers memory loss; is there a memory limit per tier.
3. **Which app** — which AI companion has the best memory; which apps have persistent / long-term memory; free vs paid memory.
4. **Privacy** — where is my memory data stored; is it secure; what happens to memory after I delete my account.

---

## 2. SERP benchmark (rebuilt via Firecrawl extraction; Semrush SERP unavailable)

Top organic pages extracted for "ai companion memory" / "best ai companion with memory" (2026-06-23):

| # | Page | Words | Format | Apps ranked | Comparison table | Hands-on test |
|---|---|---|---|---|---|---|
| 1 | aicompanionguides — *AI companions ranked by memory* | 3,536 | Ranked listicle | 9 | Yes | Yes |
| 2 | scribehow — *AI companions that remember you* | 2,793 | Ranked listicle | 8 | Yes | Yes |
| 3 | affiny — *How AI companion memory works* | 4,524 | Explainer (deep) | n/a | No | No |
| 4 | tekedia — *9 AI chatbots with memory* | 3,429 | Ranked listicle | 9 | Yes | Yes |
| 5 | digitalhumancorp — *Best AI companions with memory* | 3,382 | Ranked listicle | 6 | Yes | Yes |

### Computed benchmark (measured from `ai-companion-memory-data.json`)
- **Median word count (top 3 by relevance):** **3,429.** **Max:** 4,524. **Recommended target:** ~3,400 words.
- **Modal format:** **ranked listicle (4 of 5 pages)** that ranks AI companions by memory quality, with one deep explainer (affiny, 4,524 words) covering the mechanics. The winning shape does BOTH: explain how memory works, THEN rank the apps that do it best.
- **Item count:** ranked lists of **6–9 apps** (median 9). To beat parity, present **≥10** distinctly-described companions.
- **Comparison table:** **4 of 5 pages have one → REQUIRED** for parity.
- **Hands-on test protocol:** **4 of 5 pages describe an actual memory test** (e.g., tell the companion a fact, return N turns later, check recall). This is now table stakes — the article must include a concrete, repeatable memory-test method, not vague "we tried it" claims.

### Consensus topics (covered by 3+ pages — MUST cover)
1. **What AI companion memory is** — short-term (context window) vs long-term (persistent store) distinction.
2. **A ranked set of companions with the best memory** (6–9+ apps).
3. **How to test/evaluate memory** — a concrete recall test.
4. **Memory limits & failure modes** — why companions forget; context-window caps; tier-gated memory.
5. **Privacy/storage of memory data** — at least surface-level treatment.

### Partial topics (1–2 pages — differentiate by going deeper)
- The technical architecture (vector DB / embeddings / summarization vs raw prompt-stuffing).
- Tier-gated memory (memory quality varying by subscription).
- Memory after account deletion / retention.

### Gaps (asked by searchers, covered by nobody well — the information-gain lane)
- **A repeatable, scored memory-test protocol** the reader can run themselves (tell a fact → wait N turns → score recall), presented as a scannable table. Competitors *mention* testing but none hand the reader a reusable scorecard. (Information gain #1.)
- **An honest "how memory actually works vs marketing" explainer** — the #1 coverage gap from deep research: outlets claim "persistent memory" but never quantify retention, degradation, or failure triggers. Naming the real mechanics (context window vs summarized long-term store) is genuine information gain. (Information gain #2.)
- **A privacy-of-memory checklist** — where intimate memory data lives, retention, deletion. The deep-research pass flagged this as systematically ignored by the SERP. Natural, non-salesy place for Pleasur.AI's privacy-conscious positioning.

---

## 3. First-party fact lock (verified LIVE this run)

**Pleasur.AI pricing — source: https://pleasur.ai/pricing (fetched 2026-06-23):**

| Tier | Monthly | Coins/mo |
|---|---|---|
| Starter | $12.99/mo | 1,500 |
| Standard | $27.99/mo | 5,000 |
| Ultimate | $49.99/mo | 10,000 |

Per-action metering (live): AI image gen 10 coins; voice notes 10 coins; phone calls 50 coins/min. **Media is metered on every tier — no tier is unlimited.**

- **Drift check:** Live pricing matches `brand-config.md` canonical block. No drift.
- **What Pleasur.AI can credibly own here:** *memory-driven roleplay / story continuity as a core design goal, paired with a privacy-conscious architecture.* Per deep research, Pleasur.AI markets "memory-driven roleplay" and "priority memory processing" on its Standard tier. State these as Pleasur.AI's own positioning, NOT as an absolute "never forgets" guarantee.
- **Hard guardrails honored:** No "unlimited memory," no "remembers everything forever," no safety/privacy absolutism. Memory in any LLM companion is bounded; say so honestly — that honesty is itself the information-gain edge over the marketing-fluff SERP.

---

## 4. Deep web research findings (from `ai-companion-memory-deep.md`)

- **Pleasur.AI 2025 "memory-driven roleplay":** adaptive memory systems for more responsive, continuous conversation, framed around privacy ("digital intimacy as a sacred trust"). Source: mariavibe.com 2025 evolution write-up. *Treat as attributed brand-positioning, not independently verified fact.*
- **Tier-gated memory:** "priority memory processing" cited as a Standard-tier ($27.99) differentiator — memory quality/persistence may vary by tier. Useful as an honest "memory is a resource, often tiered" teaching point.
- **Category signal:** by early 2026, memory persistence has become a standard comparison axis between adult-AI platforms (multiple 2026 comparison reviews lead with it). Confirms commercial intent behind the keyword.
- **Coverage gaps (load-bearing for differentiation):** (1) mainstream coverage never quantifies how much context is actually retained vs marketing claims, how memory degrades, or what triggers loss; (2) privacy implications of persistent intimate memory (storage, breach surface, post-deletion retention) are ignored; (3) no comparative analysis of memory *architectures* (vector DB vs fine-tune vs prompt-engineering). These three gaps ARE our information-gain lanes.
- **No verifiable third-party statistics** on AI-companion memory specifically were found — so the article must NOT invent retention numbers. Teach the mechanics qualitatively; any quantitative claim must be first-party (our own test protocol results) or cited.

---

## BEAT SPEC (binding on outline + quality gate)
- **Target word count:** 3,400 words (±15%; floor 3,000, cap 3,900) — match the SERP median (3,429) and approach the depth leaders (3,536 / 4,524) without bloat.
- **Format:** **explainer → ranked listicle hybrid.** Open by explaining how AI companion memory actually works (short-term context window vs long-term persistent store), THEN rank the companions with the best memory.
- **Item count:** present **≥10 AI companions** with memory, each distinctly described (SERP range 6–9; beat the median, don't pad — every entry needs a real differentiator on memory).
- **Comparison table:** **REQUIRED.** Two tables ideal: (a) **memory-feature comparison** — App | Memory type (context-window / persistent store) | Long-term recall | Memory across sessions | Notable limit; (b) the **memory-test scorecard** (see information gain).
- **Hands-on test protocol:** **REQUIRED** (4 of 5 SERP pages have one). Include a concrete, repeatable method: state a specific fact early → continue N turns / start a new session → score recall (remembered / partial / forgot). Present results as a table.
- **Must-cover topics (consensus):**
  1. What AI companion memory is — short-term (context window) vs long-term (persistent store), in plain language.
  2. A ranked set of **≥10** companions with the best memory.
  3. A concrete way to test/evaluate a companion's memory.
  4. Memory limits & failure modes — why companions forget (context caps, summarization loss, tier gating).
  5. Privacy/storage of memory data — at least a clear, honest section.
- **Information gain (≥1 REQUIRED — we ship 2):** (1) a **repeatable, scored memory-test protocol + scorecard table** the reader can run themselves; (2) an **honest "how memory really works vs the marketing" explainer** naming context-window vs persistent-store mechanics and the real failure modes the SERP hides. Bonus: a **privacy-of-memory checklist** (storage, retention, post-deletion).
- **Secondary keywords to work in naturally:** ai companion with memory; ai chatbot that remembers you; best ai companion with long-term memory; how does ai companion memory work; ai girlfriend that remembers conversations; persistent memory ai chatbot; ai companion memory limit; do ai companions remember you.
- **Compliance:** 18+ framing throughout; no "unlimited/forever" memory absolutism; no privacy/safety guarantees (say memory is bounded and privacy is a design *priority*, not a promise); no real-person likenesses; internal-stack tools (Firecrawl/Semrush/OpenRouter/Strapi etc.) must NOT appear in reader-facing prose.
- **Beatability:** **Beatable.** The SERP is mid-tier niche blogs (aicompanionguides, scribehow, tekedia, digitalhumancorp) plus one deep explainer (affiny). None pairs an honest mechanics explainer WITH a reader-runnable memory-test scorecard AND a privacy-of-memory section. Match the 3,400-word ranked-listicle structure, add the two information-gain assets, and stay strictly honest about memory's limits to win the trust angle the marketing-fluff competitors abandon.
