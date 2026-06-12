# Visual design note — ai-girlfriend-app-privacy-data-guide-2026

## image-1-data-collection-comparison (hero / cover)

**Decision: deterministic table-card render, not a generative image model.**
The [VISUAL] is fundamentally a data-comparison table. Generative image models mangle
in-image text and would be a compliance/legibility risk for a privacy/trust article whose
whole value is factual precision. `render_table_card.py` produces crisp real text in the
brand palette — the most answer-engine-friendly (LLM-readable), accessible, and trustworthy
form for this asset. No API spend, no people, SFW.

The mandatory `visual-prompt-craft` 9-part anatomy governs *generative image-model* calls;
it does not apply to a deterministic text-render. Design intent recorded here per PIPELINE.md
visuals discipline (prompt-quality-is-the-product) regardless.

- **Title:** What AI Girlfriend Apps Collect — and How Pleasur.ai Compares
- **Columns:** Data type | Typical AI girlfriend apps | Pleasur.ai (per published policy)
- **Rows:** 7 data categories (messages, images, IP/device, data selling, financial, encryption, age)
- **Palette:** brand plum header (#1B1430), alternating rose/cream rows
- **Compliance:** SFW, no people, no explicit content, no real-person likeness
- **Source of every Pleasur.ai cell:** https://pleasur.ai/legal/privacy-policy (live, fetched 2026-06-11)
