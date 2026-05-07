# {{TITLE}}

**Target keyword:** {{KEYWORD}}
**Search intent:** {{INTENT}}
**Estimated word count:** {{WORDS}}
**Primary reader:** {{PERSONA}}

---

## Introduction

**Target:** ~150-200 words

**Hook:** {{HOOK_TYPE}} — {{HOOK_SENTENCE}}

**Thesis:** {{THESIS}}

**Preview:** {{PREVIEW}}

**Visual (optional, recommended for longer articles):** {type: image, sub: concept-illustration, prompt: ..., safety: sfw} — anchors the thesis with a labeled diagram.

---

## {{H2_TITLE_1}}

**Target:** ~{{WORDS}} words

- **BLUF:** {{ONE_SENTENCE_TAKEAWAY}}
- {{KEY_POINT_1}}
- {{KEY_POINT_2}}
- **Evidence:** {{EVIDENCE_OR_EXAMPLE}}
- **Transition to next section:** {{TRANSITION}}
- **Visuals:** one or more typed entries — see `templates/visual-types.md` and `templates/editorial-principles-visuals.md`. Density target is 1–2 per H2 for sections >300 words; 1 for shorter sections; `{type: none}` only when the section is purely transitional/argumentative. Examples:
  - `{type: screenshot, target: create, what: voice profile selector, annotate: arrow on speaker icon}`
  - `{type: table, columns: [Platform, Memory, Voice, Image gen, Price]}`
  - `{type: chart, data: research.search_volumes, style: bar, title: Monthly searches by platform}`
  - `{type: image, sub: concept-illustration, prompt: Flow diagram showing how memory-augmented chat works. Three labeled components left-to-right: "User Message", "Vector Store" (Embed/Retrieve/Rerank), "LLM Response". Arrows connect each step. Clean editorial illustration, white background, sans-serif labels., safety: sfw}`
  - `{type: external, sub: reddit-comment, url: ..., selector: #t1_..., what: ...}`
  - `{type: video, url: https://youtube.com/watch?v=..., what: ...}`
  - `{type: none}` (use sparingly)
  - **Multi-visual format** (preferred for sections >400 words): write each as its own line:
    - `Visual 1: {type: image, sub: diagram, prompt: ..., safety: sfw}`
    - `Visual 2: {type: chart, data: research.<key>, style: bar, title: ...}`

### {{H3_TITLE_1A}} (optional)
- {{POINT}}
- {{POINT}}

---

(repeat per H2 — aim for 4–7 H2 sections, MECE)

---

## Conclusion

**Target:** ~100-150 words

- **Recap:** Restate thesis in one sentence with new framing
- **Next step:** What should the reader do now (link to a brand resource)
- **Optional CTA:** {{CTA_TEXT}}

---

## Notes

- Internal links to add: {{LIST}}
- Sources to cite: {{LIST}}
