# Authors — the multi-author voice system

Pleasur.AI publishes under **three fictional AI author personas**, each with a distinct CRAFT modeled on a great consumer/marketing writer (**craft only** — never their name, topics, or words). The personas share the brand's register (`brand-config.md`); they differ in *how they construct* an article.

We deliberately do **not** anchor on Pleasur.AI's own past articles — we don't yet have ones good enough to model. We get inspired by the best instead, and we cover the AI-adult space broadly (companions, NSFW image generation, adult chat/roleplay, voice & calls, adult-AI tools and comparisons).

## The personas
| Persona | Craft | Owns | Folder |
|---|---|---|---|
| **Sloane Avery** — the Analyst | opinionated, data-led, contrarian | opinion/argument, data-benchmark explainers, trend listicles, behind-the-scenes | `voice/sloane-avery/` |
| **Theo Hart** — the Guide | methodical, comprehensive, hands-on | definitive how-to guides, checklists, case studies, comparisons | `voice/theo-hart/` |
| **Mateo Reyes** — the Tester | first-person, experiment-led, conversational | "I tried X for N days" write-ups, plain explainers, tactical listicles | `voice/mateo-reyes/` |

## Author selection (by content type / intent)
The pipeline picks ONE persona per article from the content type:
- **opinion / argument / trends / data-benchmark** → **Sloane Avery**
- **definitive how-to / checklist / comparison / X-vs-Y** → **Theo Hart**
- **experiment write-up / plain explainer / tactical listicle / hands-on** → **Mateo Reyes**

When a keyword could fit two, prefer the persona whose anchor set has the closest TYPE match. The chosen persona's type-matched anchors + `persona.md` feed `/draft`; the byline is stamped at `/format-for-publish`.

## Each persona folder holds
- `persona.md` — bio + craft rules + visual style (the explicit spec).
- 5–8 **anchor articles** (full text), tagged by type in the filename (`guide--…`, `opinion--…`, `explainer--…`). Reference for craft inference ONLY — never reproduced. **Topic is irrelevant; we extract the moves, not the subject matter.**

## Hard rules (all personas)
1. **Craft, not register / topic.** Imitate the moves; write in OUR voice/audience (`brand-config.md`). Never import the source's SEO/B2B diction or subject matter.
2. **Never reuse their words, examples, or structure verbatim.** Original content only — duplicate/derivative content tanks SEO and isn't ours.
3. **Bylines are fictional personas** — never a real writer's name.
4. **Visuals are landscape, "explain-then-show".** No AI-generated illustrations (retired) — annotated screenshots + landscape charts/diagrams + real images only.

## Strapi author IDs

These are the **live Strapi Author `documentId`s** that `/format-for-publish` attaches as the article's `author` relation. `/draft` stamps the persona slug into the byline comment (see the byline contract below); the formatter maps that slug → `documentId` and sets `payload.data.author`.

| Persona slug | Byline | Strapi author `documentId` | Owns (content types) |
|---|---|---|---|
| `sloane-avery` | Sloane Avery | `wfmxn1rf6wav1dn9t5bd7hsi` | opinion, argument, trends, data-benchmark, behind-the-scenes |
| `theo-hart` | Theo Hart | `bhofw86kms6ihklbhy72b0vh` | how-to-guide, checklist, comparison, definitive-explainer, x-vs-y |
| `mateo-reyes` | Mateo Reyes | `u42i38c5i95mfj47nenzx25u` | experiment, plain-explainer, tactical-listicle, hands-on, build-log |

Fallback persona when the content type is ambiguous: **`theo-hart`**.

### Byline-comment contract (EXACT — keep in lockstep across `/draft`, `/format-for-publish`, and the visuals stage)

`/draft` writes this as the **very first line** of the draft file, before the H1:

```
<!-- byline: <Byline Name> | persona: <persona-slug> -->
```

Example: `<!-- byline: Sloane Avery | persona: sloane-avery -->`

`/format-for-publish` parses this comment, strips it from the published body, and maps `persona` → the `documentId` above to set the `author` relation. If no byline comment is present, the author relation is left unset (the formatter does not fail).
