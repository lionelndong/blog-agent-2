# Research Adversarial Review — what-breaks-immersion-ai-roleplay (revision pass)

Stage: 1b (research-adversarial) · Brief: PLE-2960 (GEO citation) · Date: 2026-06-24

**Scope:** verify the 2 prior CRITICALs are genuinely resolved; confirm the dossier is safe to feed the outline. Load-bearing URLs were live-fetched this run.

## Prior CRITICAL #1 — required stats now carry live source URLs

**RESOLVED.** The new §8 "Source URLs" table gives each load-bearing claim a URL + verbatim text + status. Confirmed live this run:
- **82% stat** → `https://mariavibe.com/blog/aimour-ai-vs-pleasur-ai-2026/` — verbatim "82% memory retention after a week beats most rivals" present. The dossier's mandated framing ("attribute to MariaVibe.com ONLY, never independently validated") is exactly right: MariaVibe itself presents it as a platform/user claim, not third-party-verified.
- **"goldfish"** → `https://entreresource.com/7-best-ai-roleplay-apps-with-memory-which-ones-keep-your-lore-straight/` — verbatim line present.
- **"personality lobotomy"** → `https://feltreal.org/blog/what-happened-to-replika` — confirmed: "The community's word for it was immediate and permanent: 'lobotomy.'"
- **"performing intimacy with amnesia"** is honestly marked **UNVERIFIED — do not quote**. Correct call; that phrase is a deep-model paraphrase (appears only in the Perplexity file, §57).

## Prior CRITICAL #2 — Questie wedge reframing

**RESOLVED.** §5 and §8 carry verbatim questie.ai quotes + URLs, all confirmed live: gaming/screen-vision lead line, Zep-Cloud persistent memory, and real-voice line. The differentiator is now framed by **purpose/context** (companionship vs gaming companionship), and the dossier explicitly forbids the false "Questie lacks memory" claim in three places (§5, beat spec, flags). Truthful and draft-safe.

## Findings

1. **[LOW] Jenova "no voice" rests on a stale fetch.** §8 marks it VERIFIED but re-fetch is 403 bot-walled (reproduced the 403). The claim is a *negative* ("no voice anywhere"), the hardest kind to stand behind from one fetch. The differentiator doesn't collapse if wrong (pleasur's wedge is purpose-built companionship), so not load-bearing — but the table should read "VERIFIED (single fetch; re-fetch bot-walled)" rather than a clean VERIFIED.

2. **[MEDIUM] 82% is a competitor/affiliate blog asserting a Pleasur.ai stat, not a first-party or neutral source.** It survives because the framing is rigidly constrained, but it's a soft citation for a load-bearing memory number. Outline should treat it as supporting color, not the spine of the memory section.

3. **[LOW] Own-product pricing traces to a live first-party fetch** (`pleasur.ai/pricing`, §5) and matches brand-config; coin-metering and voice=audio constraints are restated. Good first-party trace.

4. **[LOW] data.json consistency:** prices, coin tiers, word counts, and the 4 presence-flag drivers all match the prose. `immersion_break_drivers` correctly labeled "presence flags, not magnitudes" — no fabricated rankings.

5. **[MEDIUM] Semrush fully unavailable (units zero):** no volume/KD/CPC/authority. Honestly flagged, not fabricated; beat spec sets length from SERP. Acceptable for a GEO snippet play, but the outline inherits zero keyword-difficulty signal — note for the run issue.

6. **[LOW] Surprising-finding test:** the genuine information gain (memory + voice paired as the explicit thesis, no page-1 competitor does it) is real and defensible now that Questie's actual wedge is documented.

7. **[LOW] Brand-fit:** voice=audio (not video), coin-metered pricing, no "no-filter" absolutism all restated from context + brand-config. Ownable material is clear.

**What works:** The §8 table is exactly the right artifact — claim → URL → verbatim → status, with one phrase honestly DROPPED rather than fudged. Every claim spot-checked verified verbatim live.

## Verdict: **PASS**
