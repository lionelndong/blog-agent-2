# Priority keyword clusters (board Addendum 4, 2026-06-10)

Strategy = topical authority via clusters, not ad-hoc picks. Every keyword entering
`keyword-queue.csv` must carry a `cluster` assignment + full vetting trail
(BID / AIO / redteam / priority). A keyword that fits no cluster does not enter the queue.
Publishing order favors **completing a cluster** (hub + 3–5 interlinked spokes) over scattering.

Baseline mapping below reflects the 16 currently-live articles (see
`audit/performance-ledger.csv`). Hubs are the canonical pillar; spokes link up to the hub
and across to siblings.

---

## C1 — ai-girlfriend-core  (the strongest existing footprint)

- **Hub:** `ai-girlfriend-simulator` ("ai girlfriend simulator") — the disambiguation pillar.
- **Spokes:**
  - `how-to-make-an-ai-girlfriend` ("how to make an ai girlfriend") — creation intent
  - `ai-girlfriend-apps` ("ai girlfriend apps") — app-comparison intent (route currently gated)
  - `ai-girlfriend-experience` ("ai girlfriend experience")
  - `yandere-ai-girlfriend-simulator` ("yandere ai girlfriend simulator") — niche; 11 clk/75 imp 7d
  - `is-having-an-ai-girlfriend-cheating` ("is having an ai girlfriend cheating") — POV/relationship
  - `character-ai-alternative` ("character ai alternative") — competitor-alternative bridge to C2
- **Internal-link plan:** every spoke links up to the hub with descriptive anchor; hub links down
  to creation + safety. Gap to fill: a "best ai girlfriend apps" comparison spoke once the app route unblocks.

## C2 — uncensored-nofilter-chat  (high commercial intent, competitive)

- **Hub:** `best-uncensored-ai-chatbot-free` ("best uncensored ai chatbot") — 6 clk/17 imp 7d, pos 29.6
- **Spokes:**
  - `ai-chatbot-no-filter-2026` ("ai chatbot no filter") — 5 clk 7d, pos 19.8 (best ranker in cluster)
  - `ai-chatbot-app-guide-2026` ("ai chatbot app")
  - `tavern-ai-review-2026` ("tavern ai") — product review
  - `crushon-ai-review-2026` ("crushon ai review") — competitor review
  - `muah-ai-review` ("muah ai review") — competitor review
- **Internal-link plan:** reviews link up to the hub "best uncensored" pillar; hub ranks the options.

## C3 — adult-nsfw-interaction  (highest current traffic, lowest AIO risk)

- **Hub:** `dirty-ai-guide-2026` ("dirty ai") — **top performer: 14 clk/245 imp 7d, pos 7.4**
- **Spokes:**
  - `ai-sexting-app` ("ai sexting app")
  - (gap) "dirty talking ai" / "ai roleplay" spokes to build out — board named "dirty-talking"
- **Note:** DataForSEO shows **no AI Overview** on these adult queries (2026-06-10) — low AIO
  cannibalization, so click-through potential stays high. Prioritize completing this cluster.

## C4 — trust-safety  (E-E-A-T spine; links into every other cluster)

- **Hub:** `ai-companion-safety-checklist` ("ai companion safety checklist") — featured-snippet present on SERP
- **Role:** the due-diligence reference every adult article links to. Not a traffic play; an
  authority/trust signal. Keep one strong, current checklist; interlink from all clusters.

---

## C5 — competitor-alternatives  (capture defector/migration waves; Reddit-citation play)

Added 2026-06-10 from the Community Lead Phase 0 Reddit-listening handoff (PLE-1446) + GEO
Lead briefs (PLE-1447). Intent: users actively leaving a named platform searching for "X
alternatives". High commercial-investigation value; designed for AI-citation + organic Reddit
mentions in recommendation threads. **Right-to-win:** honest, fair comparisons (name competitors
truthfully — SpicyChat best-free, CrushOn budget, Nomi emotional depth) + memory differentiator +
pricing transparency + a genuine "not predatory" stance.

- **Hub (in production):** `janitorai-alternatives-2026` ("janitorai alternatives") — PLE-1451 /
  PLE-1448#2. Live JanitorAI age-verification backlog = active acquisition window.
- **Spokes (queued):**
  - `how-to-choose-nsfw-ai-companion` ("how to choose an nsfw ai companion") — buying guide, PLE-1448#5
  - bridges to C2 competitor reviews (`crushon-ai-review-2026`, `muah-ai-review`) and C1
    (`character-ai-alternative`).
- **HARD COMPLIANCE RAIL (content-policy Part 3):** never market "no ID / no age verification" as
  a selling point. Age verification is mandatory under UK/EU/DE/default. Differentiate on memory,
  value, honesty — not verification evasion. See PLE-1448 board escalation.

## C6 — ai-companion-memory  (own the memory story we already win in reviews)

Added 2026-06-10 (PLE-1446/PLE-1447). Memory retention is repeatedly named Pleasur.ai's top
differentiator in independent reviews (genfindr 7.6/10 "best memory system tested"; scribehow
"personas maintain context across conversations"). We own the story but aren't visible for the
queries that ask about it (Google AIO cites Nomi, not us).

- **Hub (in production via PLE-1449):** `ai-companion-best-memory` / memory-comparison page —
  "best ai companion app with memory" + "which ai companion has best memory". Folds in PLE-1448#3
  ("we compared 7 AI companions on memory retention") as the data backbone (one canonical page —
  avoid cannibalizing the comparison intent).
- **Spokes (queued):**
  - `ai-companion-memory` ("ai companion memory") — how memory actually works, PLE-1448#1
  - `why-ai-companion-forgets` ("why does my ai companion forget") — frustration search, PLE-1448#6
- **Stat-provenance rail:** the "82% vs 33% 7-day retention" comparison is a THIRD-PARTY claim
  (attributed to mariavibe.com) — verify-at-source-or-drop; never publish as our own benchmark.

---

## Operating rules

1. New keywords: run the keyword-research-pipeline; only cluster-tagged survivors enter the queue.
2. Publishing cadence (4/wk cap) favors finishing C3 then C2 hubs+spokes (best near-term ROI:
   C3 already ranks page-1 on its hub; C2 has a page-2 ranker to push).
3. AIO: record `ai_overview_present` per keyword in the ledger; deprioritize fully-AIO-answered
   informational terms (no-click risk). Adult/commercial terms here mostly show no AIO — favorable.
4. Decay watch (Thu Performance Rescue): any hub/spoke losing position 2 weeks running → update pipeline.
