# Reviewer Panel — why-does-my-ai-companion-forget

Three independent skeptical experts, each having read every page-1 result for "why does my ai companion forget" / parent "character ai memory". Default bias was KEEP_COMPETITOR / TOSS_UP. Inputs: research dossier (BEAT SPEC + top-page summaries), the draft (`5-drafts/why-does-my-ai-companion-forget.md`), and `examples/voice/` anchors.

Panel rule: passes IFF >= 2 KEEP_OURS AND none KEEP_COMPETITOR.

---

## Lens A — Competitiveness (vs live #1 DHC + page-1 field)

**VERDICT: KEEP_OURS**

This draft out-explains DHC on the one axis the research flags DHC as weak (token/context-window mechanics) while matching it on the framing DHC owns (logs != memory), and it adds a genuine information-gain asset DHC lacks — a concrete, repeatable two-minute memory test that the SERP only has as a video. The mechanics are correct and reader-grade (overflow vs session reset as two named failure modes, Lost in the Middle, memory-as-re-injection workaround), and the emotion-first open lands the felt loss without melodrama, which no incumbent does. On the side-by-side-keep test a frustrated reader keeps this over DHC because it answers "why" and then hands them a test to run tonight — but it is a vulnerable win on citation hygiene and unfinished assets.

**5 weakest things vs what's ranking:**
1. Three naked `[link]` markers carry the entire mechanics-credibility load — the 1,000-tokens/750-words conversion (line 29), the 10M-vs-128K compute claim (line 70), and "Lost in the Middle" (line 72). DHC, llmnesia, and matthopkins all ship a Sources block; the draft asserts its hardest technical facts with zero resolvable citation.
2. The 82% retention stat (line 117) is self-undermining: it cites Pleasur's own blog comparing itself to a rival, then admits "there's no published methodology or sample behind it." Including an unverifiable self-promotional number hands DHC a "reads like an ad" win on the most pitch-like paragraph.
3. Every visual is an unrealized `[VISUAL]` placeholder (lines 9, 23, 35, 49, 76, 78, 90, 104, 119) — nine of them. DHC ships 1 real image, plurality 9; the draft currently renders with zero visuals against a visual-led top page.
4. The `[VISUAL:type=chart;data=research.memory_token_facts]` (line 76) references a research data key the dossier does not contain — the research only has prose, no `memory_token_facts` table. The chart will fail or invent numbers; a fabricated compute bar chart is worse than none.
5. The product section leans on brand-owned internal links — `the four memory types` (line 88) and `which companions actually remember you` (line 144) — presented as authoritative, and the "four memory types / ladder" taxonomy is asserted as fact without external grounding.

**1 thing that genuinely works:** The two-minute memory test (lines 92-102) is a real edge, not filler — it operationalizes the abstract mechanics and explicitly maps each step back to the two failure modes the article just taught. It is the one asset the AI Overview structurally cannot reproduce and that no text competitor offers, and it doubles as the natural bridge to the product.

---

## Lens B — Voice & Readability (vs examples/voice register)

**VERDICT: KEEP_OURS**

This draft genuinely reads like the brand anchors, not generic AI: it leads with a concrete felt scene ("You told it your dog's name on Tuesday. By Friday it asked, brightly, whether you had any pets"), runs the same short declarative rhythm the anchors use, and earns the product mention honestly at the solution end with the verified caveat. The crutch words the floors check flagged ("model," "conversation," "thread," "across sessions") are concentrated in a piece whose subject is models, conversations, and threads across sessions, so the repetition reads as topical necessity rather than filler, and the desk/diary/librarian/ladder metaphors mostly stay fresh. It would run under a byline without embarrassment.

**5 weakest things vs what's ranking:**
1. The "it's not X, it's Y" pattern surfaces twice in close range: "It didn't get bored of you. It never actually kept the memory in the first place" and "It isn't withholding the memory — it doesn't have it." Starts to feel like a tic.
2. Em-dash density is high — several sentences carry two dashes apiece ("logged is not the same as remembered" follows another dash-heavy clause); the anchors use dashes far more sparingly.
3. "Whole threads exist for this ache" — "ache" reaches for poignancy the anchors never make; the boyfriend piece validates feeling with plain lines like "the frustration is earned."
4. Italics-for-emotion crutch repeats: "*it doesn't know me anymore*," "*right there*," "*you*," "*they*," "*logs*," "*remembers*." The anchors rarely lean on italic emphasis to carry a beat.
5. "Once you can picture that, the two ways your companion forgets stop looking like one problem" is a transitional throat-clear that tells the reader what they're about to learn instead of showing it.

**1 thing that genuinely works:** The two-minute memory test (plant "My cat's name is Mango and she's missing a whisker," chat 15-20 messages, return next day, ask "How's the whisker situation?") is concrete, repeatable, reader-felt, and delivers the headline information-gain no page-1 competitor offers in text form.

---

## Lens C — Reader Intent & Information Gain

**VERDICT: KEEP_OURS**

This draft does the two things the AI Overview and page-1 incumbents structurally cannot: it validates the felt loss (the Tuesday-dog cold open, the "it doesn't know me anymore" reframe) AND hands the reader a concrete, repeatable, text-form memory test that the SERP only surfaces as a video. It out-explains every incumbent on mechanics while staying honest about Pleasur.AI's only verified-live capability (save-and-resume, explicitly "not infinite memory"), and it self-polices the unverified retention stat rather than weaponizing it. It clears the "beats the SERP plus genuine gain" test rather than coasting on a tie.

**5 weakest things vs what's ranking:**
1. The H2 still carries the literal "[GAIN]" tag ("How to Test Your Companion's Memory in 2 Minutes [GAIN]") — an editing artifact that looks amateurish next to clean incumbents. Also, step 2's "15 to 20 messages" is arbitrary and won't reliably trigger overflow on large-window models the draft itself says exist, so the in-chat-overflow half of the test can silently false-pass.
2. The 82% retention stat (What to Actually Do) is a self-inflicted trust wound and drags a competitive-comparison link into an emotional explainer SERP where searchers do NOT want a product face-off. Cutting it would strengthen the page.
3. Unfilled placeholders: three `[link]` tokens sit where DHC/llmnesia carry real cited sources, plus a heavy stack of unrendered `[VISUAL:...]` blocks — the draft is not yet at the depth-plus-sourcing the benchmark demands.
4. Product-mention density creeps past "earned": Companion Creator appears in "Memory Features Are Workarounds," again in "What to Actually Do," again in the action-shot visual, plus three internal Pleasur blog links — edging toward the DHC "product pitch leans heavy" failure mode the research flagged.
5. The "ladder of four memory types" is asserted, not sourced, and links to a Pleasur blog as if it were the authority on a general taxonomy — a subtle over-reach in a piece whose credibility depends on neutral mechanics.

**1 thing that genuinely works:** The emotion-first open into mechanics is executed better than anything on page 1 — the Tuesday-dog scene lands the felt loss in three sentences, then "It's Not You" cleanly splits the *feeling* ("it doesn't know me anymore") from the *mechanism* ("it doesn't have it"). That is precisely the gap every cold/technical or B2B incumbent leaves wide open.

---

## Panel tally

| Lens | Verdict |
|---|---|
| A — Competitiveness | KEEP_OURS |
| B — Voice & readability | KEEP_OURS |
| C — Reader intent & information gain | KEEP_OURS |

3 KEEP_OURS, 0 KEEP_COMPETITOR, 0 TOSS_UP. All write-ups exceed 200 words with specific, non-glowing critique — no sharper re-run required. **Panel PASSES.**
