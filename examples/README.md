# Examples — the anchor set

Reference content the pipeline reads before outlining and drafting. LLMs infer quality from real text far more reliably than from rules — the core insight of [Ryan Law's process](https://ahrefs.com/blog/how-i-do-content-engineering-with-claude-code/). Each subfolder anchors exactly ONE thing.

## `voice/` — how we sound (multi-author)

We publish under **3 fictional AI author personas**, each a distinct CRAFT modeled on a great writer (**craft only** — never their name, topic, or words). See **`authors.md`** for the personas, the content-type → persona selection rule, and the hard rules.

Each `voice/<persona>/` folder holds:
- `persona.md` — the persona's bio + craft rules + visual style (the explicit spec).
- 5–8 **anchor articles** (full text), tagged by type in the filename (`opinion--…`, `guide--…`). **Craft reference only** — `/draft` must imitate the *moves* and write ORIGINAL content; never reuse their text (duplicate content tanks SEO and isn't ours). Topic is irrelevant; we extract the craft.

Pull/refresh the anchors with: `doppler run -- python examples/pull_anchors.py`.

> We deliberately do NOT use Pleasur.AI's own past articles as voice anchors — we don't yet have ones good enough. (The retired Pleasur anchors live in `_archive/voice-pleasur/`.)

## `niche/` — depth of a winning listicle (NOT voice)

Best-in-class consumer comparison/listicle content (Zapier's "best AI chatbot", ~6,800 words — note the per-item depth: hands-on detail, screenshots, pricing specifics, a real comparison table, honest cons). Read for *how much substance a winning listicle carries*, never for voice.

## `structure/` — explainer/guide mechanics (NOT voice)

Articles kept for structural craft: BLUF section openers, MECE coverage, evidence placement, product-led demonstration. Read when writing definitive guides and explainers.

## How the pipeline uses these

- `/outline` — 1 structure or niche example closest to the content type
- `/draft` — the selected persona's `persona.md` + 1–2 type-matched anchors from that persona, + 1 structure/niche example
- `/quality-check` — the persona's anchors as the voice baseline

## Customizing

Swap anchors freely — the pipeline favors examples over rules. To change a persona's voice, change its anchor articles + `persona.md`. To change WHO writes what, edit the selection rule in `authors.md`.
