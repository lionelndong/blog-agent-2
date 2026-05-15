# Research: how to make an ai girlfriend

> **Strategic flag (read before drafting):** This query is split-intent. Some searchers want a literal DIY build (Character.AI persona, fine-tune an open model, code a Gradio app). Most are using "make" as a synonym for "get" — they're lonely or curious and want the experience without the engineering. The SERP currently splits along the same line — half DIY explainers, half product landers — and no page tells the reader which path matches *them*. That's our lane. Pleasur.AI surfaces only as the natural close of the "off-the-shelf" path, never as the topic.

> **Sourcing banner:** Deep-research returned empty — sibling-dossier reuse from the first pass had two **wrong** citations (now corrected). Every numerical claim below has a primary URL.

## Keyword metrics

- **Primary keyword:** `how to make an ai girlfriend`
- **US volume:** 110 / month (Semrush `phrase_this`, live 2026-05-15 — note: context file cites 140; live re-poll today returns 110, follow re-verify policy)
- **KD%:** 27 (winnable for AS=11; weak-link gate AS≤26 holds)
- **CPC:** $0.50 — light commercial interest, not a transactional SERP
- **Competition density:** 0.02 — open
- **Intent (Semrush `In`):** 1 → **informational** (PASS — publish-as-blog territory)
- **SERP features:** `6, 9, 36` → image pack, video, people-also-ask
- **12-mo trend:** flat-with-mid-cycle spike (`0.15, 0.08, 0.08, 0.11, 1.00, 0.11, 0.15, 0.15, 0.11, 0.23, 0.03, 0.01`) — evergreen baseline; currently down-trending. Not seasonal.
- **Parent cluster context:** sits under the parent `ai girlfriend` (80,000/mo, KD 68). This sub-keyword inherits the parent audience but the SERP is far friendlier (weak-link domains).

## Long-tail variations (same cluster — context-supplied; secondary `phrase_related` was API-quota-blocked, see Failures)

| Keyword | US Vol | KD | Notes |
|---|---:|---:|---|
| `how to make an ai girlfriend` | 110 | 27 | primary |
| `how to create an ai girlfriend` | 140 | 71 | exact synonym — cover in same post |
| `how to get an ai girlfriend` | 90 | 36 | "get" framing — off-the-shelf intent |
| `what is an ai girlfriend` | 210 | 19 | definitional pre-step — link out to existing dossier |
| `how to make an ai girlfriend for free` | 10 | — | trending up (12-mo); covers free-tier framing |
| `how to make an ai girlfriend app` | 0 | — | dev-builder edge; mention only |

**Cluster total addressable:** ~550/mo across the five main variants using **live primary volume of 110** (not the context-file 140). Live math: 210+140+110+90+10 = 560; rounding to ~550 to flag the drift. With AS=11, capturing the long tail of "how / what / get / create" inside one honest article is the winning move.

## Questions people ask — grouped into themes

(Context-supplied + sibling-dossier reuse; `phrase_questions` was quota-blocked.)

- **Theme 1 — Path choice:** Can I really build my own? Need to code? Make or use an app? Easiest way to get one?
- **Theme 2 — Tools and tech:** ChatGPT/Claude as the model? Does Character.AI count? What do paid apps run on? How to add voice / image / memory?
- **Theme 3 — Cost and time:** How long to build? Hosting cost? Free options?
- **Theme 4 — Experience:** Will it feel real? Will it remember me? Voice? Image generation?
- **Theme 5 — Ethics / "is this for me":** Is it weird? Is it cheating? Will it make loneliness worse?

## SERP overview

- **Dominant intent:** Informational (Semrush `In=1`), with light commercial bleed via product landers.
- **Dominant content type:** Split — three formats compete:
  1. **DIY tutorial** (gmongaras Medium, TechBrite handbook, Quora threads, YouTube builds)
  2. **Product landing pages** (Nomi, Kupid, Candy.ai, Ourdream, MyDreamCompanion, RomanticAI)
  3. **Social proof / forums** (Reddit r/AIToolTesting, Quora, TikTok)
- **Brand presence in top 15:** Reddit (#1), Nomi.ai (#2), YouTube (#3, #9), gmongaras Medium (#4), Kupid (#5), Quora (#6, #11), RomanticAI (#7), Perfect Corp (#8 — 404'd on fetch, ghost page), TechBrite (#10), TikTok (#12), Candy.ai (#13), MyDreamCompanion (#14), Ourdream (#15).
- **Weak-link domains (per context):** techbrite.com, romanticai.com, kupid.ai — winnable at AS=11.
- **No AI Overview** confirmed by Semrush for this exact query — citation-grab is open.

## Top-ranking pages — summaries

- **#1 Reddit r/AIToolTesting** — "How do I create an AI girlfriend?" 403'd. Help-request thread: the searcher is asking the same question. Mirror an honest "here's how" without sales tone.
- **#2 Nomi.ai** — Free to start, then **$15.99/mo** ([AutoGPT pricing review, 2026](https://autogpt.net/nomi-ai-pricing/); pricing page itself gated). Long-term memory, emotive voice, AI selfies, proactive messaging. Missing: any DIY framing or comparison.
- **#3 / #9 YouTube** — Carousel placement signals SERP rewards walkthrough format. Body not fetchable.
- **#4 gmongaras Medium** — "[Coding a Virtual AI Girlfriend](https://gmongaras.medium.com/coding-a-virtual-ai-girlfriend-f951e648aa46)" (~2,500 words, 2022). Author quotes: build took **"a few weeks"**; aimed to fit on a "reasonable GPU" (A100/RTX class). Stack: **GPT-Neo 1.3B** fine-tuned on anime subs, LED-large-book-summary for memory, gTTS, Google STT, Stable Diffusion + **waifu-diffusion**, Talking-Head-Anime. See Surprising findings for the stack-obsolescence wedge.
- **#5 Kupid.ai** — 403'd. Customization-heavy lander.
- **#6 / #11 Quora threads** — 403'd. VoC goldmine; flag for `/verify-claims`.
- **#7 RomanticAI** — 5-step create flow (style → photo → traits → tone → interests), NSFW toggle. Pure conversion page.
- **#8 Perfect Corp** — 404 ghost. Easy displacement.
- **#10 TechBrite** — ~1,100 words. Generic 5-step recipe, no platforms/code/prices. Direct outrank target.
- **#13 Candy.ai** — Free 7-day trial then **$12.99/mo** monthly or $5.99/mo annual ([AI Tipsters pricing review, 2026](https://aitipsters.com/candy-ai-pricing-2/)). Tokens sold separately (100 = $9.99). No DIY framing.

## Surprising findings (SERP-derived, re-verified)

1. **The only DIY tutorial that ranks is built on obsolete tooling.** The #4 SERP result — gmongaras's Medium post — uses **GPT-Neo 1.3B** (EleutherAI, 2021) and **waifu-diffusion** (unmaintained since 2023). Three generations behind 2026 open weights. Today the same build would use Llama-3-8B-Instruct fine-tuned via LoRA on a marketplace A100 (~**$0.72/hr** on Vast.ai, [Vast.ai vs RunPod 2026 comparison](https://medium.com/@velinxs/vast-ai-vs-runpod-pricing-in-2026-which-gpu-cloud-is-cheaper-bd4104aa591b)) plus SDXL. Anyone following the only DIY guide that ranks is being routed to a 4-year-old stack. **This is the wedge:** an honest 2026 DIY recipe is itself a citation nobody else has.

2. **No top-5 product page publishes a price on the marketing surface.** Nomi, Kupid, RomanticAI all gate pricing behind sign-in. Review sites disagree on Nomi's monthly ($14.99 / $15.99 / $16.99). Candy.ai is the rare exception — though `/pricing` 404'd today and we sourced $12.99 from a third-party review. The "honest cost/time table" angle is novel because **competitors actively hide the number**.

3. **The Stanford Replika "48% loneliness" stat that sibling dossiers cite is wrong.** The peer-reviewed [Stanford 2024 study (n=1006 student Replika users, npj Mental Health Research)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10955814/) actually reports **90% experienced loneliness** and **43% qualified as Severely or Very Severely Lonely**. The 48% figure does not appear in the paper. Use 43% Severely Lonely + 90% any-loneliness in the "is this for me" section.

## External citations (corrected this pass)

- **Replika scale — 10M Google Play installs.** [Sensor Tower, "Replika Reaches 10M on Google Play"](https://app.sensortower.com/news-feed/ai-friend-app-replika-reaches-10-million-on-google-play/62bc87140d41df403960eb59); reinforced by [ETtech (Nov 2024)](https://x.com/ETtech/status/1863423564004602074) — 10M downloads + $25M revenue H1 2024.
- **Investor signal (CORRECTION).** Character.AI's $150M was **Series A led by a16z in March 2023** at a $1B valuation — [CNBC, Mar 23 2023](https://www.cnbc.com/2023/03/23/characterai-valued-at-1-billion-after-150-million-round-from-a16z.html). Sibling memory said "Series B, Feb 2024, Reuters" — incorrect.
- **Stanford Replika study (CORRECTION).** [Cerit et al., Stanford / npj Mental Health Research (Jan 2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10955814/) — N=1006; 90% any loneliness; 43% Severely/Very Severely Lonely; 3% reported Replika halted suicidal ideation.
- **DIY build economics.** gmongaras: "a few weeks" + reasonable GPU. 2026 GPU floor: A100 80GB marketplace ~$0.72/hr (Vast.ai). The unsourced "$400 GPU cost" from the first pass has been dropped.
- **Coverage gap.** Peer-reviewed long-term wellbeing data is genuinely thin — flag honestly rather than weaponize a single study.

## Content gaps and opportunities

**Covered by all — must include:** plain-English definition of what "making" means; a walkthrough of some path; personality / appearance / voice customization.

**Covered by some — differentiation:** the DIY technical stack (only gmongaras + Quora, and gmongaras is on 2022 models); off-the-shelf customization flow (only the vendors themselves); cost/time honesty (basically nobody — competitor pricing is gated).

**Covered by none — angles to own:**
- **A 2026-current DIY recipe:** Llama-3-8B-Instruct + LoRA on a Vast.ai A100 spot, SDXL not waifu-diffusion, ElevenLabs or Coqui XTTS not gTTS.
- **A real cost/time table with sources:** $0.72/hr GPU × evenings of work vs $12.99–$15.99/mo subscription.
- **The path-choice gate:** "are you here to build, or to have one tonight?"
- **A fair off-the-shelf comparison** — Character.AI / Replika / Nomi / Candy.AI / Pleasur.AI side-by-side.

**Format opportunities:** decision flowchart (DIY vs off-the-shelf); cost/time table; "first 10 minutes" walkthrough per path; "what you can't do" bullet for DIY.

## Recommended angle

**Thesis:** *"Making" an AI girlfriend means one of two things — engineering one from scratch (a few weeks of evenings, a $0.72/hr GPU rental, a stack the only Medium tutorial on the SERP hasn't refreshed since 2022) or designing one inside an existing app (10 minutes, no code, $12.99–$15.99/mo). This is the honest guide that tells you which path matches your situation before you start.*

**Why it wins:** (1) SERP is split DIY vs landers, nobody bridges, and the lone DIY tutorial runs on 2022 models. (2) Weak-link competitors (TechBrite, RomanticAI, Kupid) lose to substantive editorial at AS=11. (3) Pleasur.AI's voice can deliver the off-the-shelf recommendation honestly *after* walking the reader through DIY so the conclusion is trusted. (4) Cluster is ~550/mo; even modest top-3 placement plus long-tail pickup is a strong Friday-informational outcome.

---

*Stage 1 dossier — for `/outline`. ~1,500 words (revision pass 2026-05-15).*
