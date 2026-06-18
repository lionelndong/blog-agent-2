# Research Adversarial — how-to-choose-an-nsfw-ai-companion

Stage: 1b (research-adversarial). Skeptical pushback on the dossier before it feeds `/outline`.

Inputs reviewed:
- `content-pipeline/1-research/how-to-choose-an-nsfw-ai-companion.md`
- `content-pipeline/1-research/how-to-choose-an-nsfw-ai-companion-deep.md`
- `content-pipeline/1-research/how-to-choose-an-nsfw-ai-companion-data.json`
- `content-pipeline/0-context/how-to-choose-an-nsfw-ai-companion.md`
- `content-pipeline/2-reference/how-to-choose-an-nsfw-ai-companion.md`
- `brand-config.md`

## Content-policy guardrail: PASS

The dossier explicitly inverts the SERP's age-gate-evasion framing. Line 14 binds it: "Do NOT frame no-ID / no-age-verification / 'no sign-up' as a selling point," and line 93 reframes age verification as a green flag. No violation found.

## Findings

### CRITICAL — Load-bearing pricing/feature numbers are uncited in the prose
The pricing-maze argument (line 106) hangs on specific figures — "~$19/mo," "~$9.99 starter," "~$5.20/mo annual… 500 images + 100 voice minutes" — and the multi-modal claim cites "up to 100 min/month" (line 105). In the prose dossier these carry no source; they exist only as bracketed `[7][9][2]` numerals in `-deep.md`, whose citation list is **not resolved to URLs** in the file. Line 109 claims "the `-deep.md` file retains citations" — it retains inline markers without a reference table. A writer cannot hyperlink these. Citation-thin foundation.

### CRITICAL — One of three "surprises" is dressed-up table-stakes
- (a) "category is moving multi-modal and emotional, not just explicit" (line 105) → **dressed-up-table-stakes.** This has been the category's pitch since Replika ~2020; not an insight.
- (b) pricing is an inconsistent freemium maze (line 106) → **actually-surprising** (mild) and ownable.
- (c) no independent privacy scrutiny / no breach history / no audits (line 107) → **actually-surprising**, the strongest finding.
Only 2 of 3 land; (a) is filler the outline should not elevate.

### HIGH — Strongest competitor angle named but not beaten
The deepest editorial page is `chicagoreader.com/nsfw-ai-chat` (~4,460 words, 11-row comparison table — line 62). The dossier IDs the table as "its spine" (line 73) but its counter is only "we include one too" with a different schema (line 128). It never engineers the beat — what the chicagoreader table gets wrong (affiliate-ranked tools, no "how to test in 5 min" column). Acknowledged, not defeated.

### HIGH — Brand-ownable material is thin and untested
The dossier leans on AI Companion Creator + Image Gen (line 122), but the 2-reference cache warns "all `excerpt` fields are empty… product walkthrough examples cannot be confirmed" — no verified first-hand Pleasur.AI data to make the scorecard ownable. The best ownable asset, the existing **AI Companion Safety Checklist** article, is cited only for internal linking, never mined into the privacy/age-gate criteria that are the actual differentiator (line 92). Brand-fit reads as a survey.

### MEDIUM — JSON vs prose: one orphan key, one soft-fact range
Spot-check matches: `nsfw_ai_companion: 260` ✓, `nsfw_ai_chatbot KD 64` ✓, `target_word_count 2400` ✓. But `ai_companion: 9900` lives in `cluster_volumes` yet appears in prose only in the variation pool, never the keyword-metrics table. And `serp_item_count_range_low: 4 / high: 12` is partly derived from Reddit/scribehow pages the scraper **blocked** (lines 67–68); the writer must not cite "4–12" as a hard count.

## One thing that works
The white-space thesis is sharp and correct — "Nobody owns the decision framework itself… every page tells you *which* tool to pick, not *how to decide*" (line 12). The 8-criteria scorecard with a "test it in 5 minutes" column (line 128) is genuine, defensible information gain.

## Verdict (pass 1): FAIL

Uncited load-bearing pricing figures (no resolvable bibliography in `-deep.md`) plus one dressed-up table-stakes "surprise" mean the writer would build on a citation-thin, partly-generic foundation. Fixable in one revision pass. Content-policy guardrail itself is clean.

---

## Revision 1/1 applied — re-review

The research stage was re-dispatched with the CRITICAL/HIGH findings as a revision brief (research revision budget 1/1 consumed). Re-verified against the revised dossier:

1. **[RESOLVED — was CRITICAL] Uncited pricing figures.** Every load-bearing pricing/feature number now carries a real inline hyperlinked source (OhGirlfriend/Candy AI, AI Companion Guides/Replika, Scribe/Digital Girlfriend AI, AI Journal, Lumichats). A "Source resolution" note maps the former `[n]` markers. `/draft` and `/verify-claims` can now hyperlink each claim.
2. **[RESOLVED — was CRITICAL] Dressed-up surprise.** The "multi-modal/emotional" item is demoted to explicit "context (not a surprise)" and replaced with a sourced, non-obvious insight: the hero price is the annual rate, monthly ~2.2× higher, metered tokens push real cost to 3–4× advertised. The two surprises that held are kept and sharpened.
3. **[RESOLVED — was HIGH] chicagoreader beat engineered.** New "How we beat chicagoreader.com" subsection + updated BEAT SPEC specify three concrete information-gain moves (criteria-axis scorecard, per-criterion 5-minute self-test column, scored privacy/age-gate red-flag column).
4. **[ADDRESSED — was HIGH] Brand material.** Brand-fit now mines the existing AI Companion Safety Checklist article into the privacy/age-gate criteria rather than only internal-linking it.
5. **[ADDRESSED — was MEDIUM] Soft item-count range** softened to "indicative, not a hard count."

Content-policy guardrail remains clean. No CRITICAL or HIGH findings remain.

## Verdict: **PASS**
