# Visuals Adversarial — what-breaks-immersion-ai-roleplay

**Context:** GEO/AIO citation piece (PLE-2960), ~1,400 words, extractability-first. By design this is a low-density piece (3 planned visuals); the editorial density target is relaxed because generated decoration hurts the snippet-first goal. The scope of this ruling is the **2 uncaptured visuals** (§3 external Replika quote, §4 voice action-shot) that `/generate-visuals` could not realize. The Claude-in-Chrome MCP is unreachable this session, so `/capture-visuals` cannot run. Per the visuals gate, any naked / manual / failed entry HALTS publish unless resolved. The §5 comparison table is correctly rendered as in-place GFM markdown and is **satisfied** (not an asset, present in the draft).

---

## Visual 1 — §3 external Replika "lobotomy" quote (manifest index 1)

`[VISUAL:type=external;sub=news-quote;url=https://feltreal.org/blog/what-happened-to-replika;selector=blockquote;crop=padded]` — status was `failed` (Playwright bounding_box timeout / bot wall).

**5-step earns-its-place reasoning:**
1. **Earns its place?** The placeholder would screenshot a `blockquote` of a Replika user describing the post-update personality change. But the §3 prose *already* quotes the user verbatim — "like being in love, and your partner got a damn lobotomy" — hyperlinked to scroll.in, and the "lobotomy" community term is hyperlinked to feltreal.org in §1. Removing the screenshot costs the reader **no concrete information the prose doesn't already carry**.
2. **First-sentence-readable?** Yes — §3's BLUF and the inline quote stand alone; the visual was never load-bearing for comprehension.
3. **Concrete?** It shows a real source, but the *same* source text is already quoted-and-cited inline. Per editorial rule #2/#3, an external screenshot of a quote that is already quoted-and-cited inline is decorative.
4. **MECE / overlap?** It directly duplicates the inline quotation and citation — pure overlap.
5. **Capture cost vs value:** capture requires Claude-in-Chrome (unreachable). Chasing a decorative duplicate to unblock the gate is exactly the wrong trade.

**Ruling: DECORATIVE. Action taken: STRIPPED.** Naked `[VISUAL:]` line removed from §3 of the cited draft; manifest index 1 set to `status="stripped"` with reason. Surrounding prose reads cleanly (the quote + citation remain inline; no dangling reference).

---

## Visual 2 — §4 in-chat voice action-shot (manifest index 2)

`[VISUAL:type=action-shot;target=chat;what=companion chat showing the speaker icon + Call button;annotate=#voice-button]` — status was `manual` (requires a logged-in multi-step Chrome session; headless capture landed on the wrong, unauthenticated state and was discarded).

**5-step earns-its-place reasoning:**
1. **Earns its place?** The §4 prose already explains the voice UI in full words: "tap the speaker icon next to a reply" (Voice Replies) and "tap the Call button on the character's profile" (Phone Call), plus the coin-metering in the tip box. The screenshot would illustrate two named buttons whose location and behavior the prose already states.
2. **First-sentence-readable?** Yes — §4's BLUF (text-only caps immersion; real-time audio closes the gap) needs no image.
3. **Concrete / non-obvious UI?** This is the decisive test (rule #3): a product action-shot is decorative *unless it conveys non-obvious UI information*. Two clearly-named, clearly-located controls (speaker icon on a reply; Call button on the profile header) are obvious from the prose. No hidden state, no multi-panel flow, no non-obvious affordance is revealed.
4. **MECE / overlap?** It re-states the feature description already in the paragraph immediately above it.
5. **Capture cost vs value:** requires a logged-in Claude-in-Chrome session (unreachable). It is not load-bearing, so it should drop, not block the gate.

**Ruling: DECORATIVE. Action taken: STRIPPED.** Naked `[VISUAL:]` line removed from §4 of the cited draft; manifest index 2 set to `status="stripped"` with reason. Surrounding prose (feature explanation + Pro-tip coin box + continuity link) reads cleanly.

---

## Visuals that genuinely earn their place (kept)

- **§5 comparison table** (manifest index 3, `type=table`, in-place GFM) — the article's primary information-gain visual. Compares live-verified memory + voice capabilities across Pleasur.ai / Jenova.ai / Questie.ai across 4 dimensions. Carries skim-able structured information the prose cannot match. **Present and satisfied** (no asset to capture).

## Actions summary

| Visual | Ruling | Action | Naked placeholder removed |
|---|---|---|---|
| §3 external Replika quote | DECORATIVE | STRIPPED (manifest → stripped) | Yes |
| §4 voice action-shot | DECORATIVE | STRIPPED (manifest → stripped) | Yes |
| §5 comparison table | LOAD-BEARING | KEPT (in-place GFM, satisfied) | n/a |

**Post-strip state:** `grep '\[VISUAL:'` on the cited draft returns **0** matches. No dangling "see screenshot below"-style references. No load-bearing visual is left uncaptured — the only remaining required visual (§5 table) is rendered in place.

## Verdict: **PASS**
