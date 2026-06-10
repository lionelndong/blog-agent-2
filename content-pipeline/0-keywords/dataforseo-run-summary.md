# DataForSEO Keyword Research Run

- Observed date: 2026-06-10
- Source: DataForSEO API v3, US Google (`location_code=2840`, `language_code=en`)
- Cost logged: $0.646900
- Competitors used: candy.ai, ourdream.ai, nastia.ai
- Candidate rows: 458
- Queue rows: 50
- Source counts: {'competitor_gap': 46, 'competitor_gap+seed_modifier': 17, 'competitor_gap+question_mining+seed_modifier': 1, 'seed_modifier': 375, 'question_mining+seed_modifier': 19}
- Gap-mode counts: {'missing': 64, 'seed_modifier': 375, 'question_mining': 19}
- BID counts: {'FAIL': 168, 'PASS': 290}
- AIO counts: {'UNKNOWN': 388, 'PASS': 49, 'RISKY': 21}

## Top 10 Queue Rows

| Rank | Keyword | Score | Volume | KD | Intent | Source | Gap |
|---:|---|---:|---:|---:|---|---|---|
| 1 | dirty talking | 9.05 | 27100 | 0 | informational | competitor_gap | missing |
| 2 | ai sexting | 9.04 | 33100 | 4 | informational | competitor_gap+seed_modifier | missing |
| 3 | sexting ai | 9.04 | 33100 | 4 | informational | competitor_gap+seed_modifier | missing |
| 4 | ai girlfriend | 8.88 | 135000 | 31 | informational | competitor_gap+seed_modifier | missing |
| 5 | sexting chat | 8.82 | 550000 | 34 | informational | competitor_gap | missing |
| 6 | sex chat | 8.64 | 550000 | 43 | informational | competitor_gap | missing |
| 7 | ai boyfriend | 8.56 | 22200 | 21 | informational | competitor_gap+seed_modifier | missing |
| 8 | ai companion | 8.53 | 18100 | 19 | informational | competitor_gap+seed_modifier | missing |
| 9 | ai girlfriends | 8.43 | 18100 | 24 | informational | competitor_gap | missing |
| 10 | free ai girlfriend | 8.35 | 18100 | 28 | informational | competitor_gap+question_mining+seed_modifier | missing |

## Caveats

- Lens: Search intent alignment. DataForSEO `search_intent_info` is primary when available; SERP shape is fallback.
- Lens: Answer-engine citation readiness. AIO detection uses SERP Advanced `ai_overview`; multi-engine LLM citation gap is skipped because DataForSEO has no equivalent.
- Lens: E-E-A-T. This queue is mechanically vetted; article production still requires the normal research, quality, claim verification, and compliance gates.
