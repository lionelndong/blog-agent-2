# Visuals adversarial — ai-girlfriend

**Computed inputs**

| Metric | Value |
|---|---|
| Word count (cited draft, excl. editor notes) | 3,805 |
| Density target (>3,000 words) | 12 |
| Acceptable range | 10–15 |
| Captured visuals in manifest | **12** |
| Distinct types | **3** (image, screenshot, action-shot) |

---

## Findings

### MEDIUM-1 — Two action-shots in the same section (MECE)

`action-shot` indices 11 and 12 both sit inside **§ How to create a companion that doesn't feel generic**. Same section, back-to-back, both showing the Companion Creator wizard. The section is ~500 words; the two captures cover nearly the same UI state (backstory panel → ethnicity step). Per the MECE rule: two visuals in one section must cover *different* aspects. A backstory panel and an ethnicity selector are adjacent wizard steps, not different aspects of character depth.

**Suggested fix:** Keep action-shot 11 (backstory / traits — the one with visible personality fields, directly supporting the "backstory matters more than appearance" argument). Move action-shot 12 to a different section — or drop it if it can't earn a distinct place.

---

### MEDIUM-2 — Screenshot #7 shows a generic create page, not the per-message voice feature

Screenshot `screenshot-7-pleasur-ai-companion-creator-v.png` is placed in **§ Voice — not as a separate mode, but inside chat**, captioned "voice profile selector step." The prose's key claim is *per-message playback as a speaker icon on each message* — a live chat interface, not the wizard. A wizard step showing voice profile selection supports voice onboarding, not the "tap to hear this message" UX that makes §4 distinctive.

**Suggested fix:** Ideal replacement is a screenshot or action-shot of the actual chat surface with a voice icon visible on a message. Since that requires a live session, a `image` (sub=comparison) of "text thread with speaker icon per message vs. separate voice mode toggle" would substitute well.

---

### LOW-1 — §5 Friction and §6 Uncensored have no visuals

**§ 5. Friction to start a conversation** (≈200 words) and **§ 6. Honest uncensored claims** (≈200 words) have no visual support. Both are short enough (~200 words each) that `none` is acceptable per the editorial principles. The density target is met at 12, so this is not a density gap — just a note that both sections make testable claims (friction = onboarding speed; uncensored = the day-one test) that a screenshot or action-shot could substantiate. Not worth adding at the cost of inflating density above 14.

---

### LOW-2 — image-1 alt text is excessively long (rendering risk)

The alt text on `image-1-three-column-labeled-compariso.png` is the full gpt-image-2 prompt (~160 words). Alt text at this length is a screen-reader burden and breaks in CMS fields with character limits. Trim to one descriptive sentence at publish time.

---

## Visuals that genuinely earn their place

**image-4 (§ Memory — flow diagram):** The labeled pipeline — chat turns → summarize → vector store → retrieval → next prompt — explains the architectural distinction between good and weak platforms in a single glance. This is the ahrefs reference done right: removes a paragraph of "and then it does this" prose and replaces it with a labeled diagram.

**image-8 (§ Why hard to build — architecture stack):** Five-layer vertical diagram (LLM → fine-tune → RAG → diffusion → TTS) with an integration-complexity brace on the left. The section explains why most platforms get 3/6 criteria right; the diagram gives the reader a mental model to carry forward. The prose could describe this in 150 words; the diagram does it in five labels.

---

## Verdict

## Verdict: PASS

Density: 12 captured at the target. Type diversity: 3 types present. No CRITICAL findings. The two MEDIUM findings (action-shot duplication, screenshot misalignment with §4 claim) warrant a revision pass if budget allows, but neither causes the article to actively mislead. The revision budget is at 1; the strip-and-add loop is optional here.
