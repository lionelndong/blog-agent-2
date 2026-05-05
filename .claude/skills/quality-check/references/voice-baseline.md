# Voice baseline reference

What "good" looks like for the Ahrefs editorial voice we're emulating, measured from the corpus in `examples/`.

These are the rough ranges the `quality_check.py` script compares the draft against. A draft that drifts > 50% from these ranges is flagged for voice review.

| Metric | Typical range | What it means |
|---|---|---|
| `avg_sentence_words` | 14–22 | Sentences vary but mostly stay short. Below 12 = staccato. Above 25 = run-on. |
| `median_sentence_words` | 13–18 | Middle of the distribution. Robust to outliers. |
| `avg_paragraph_words` | 35–80 | Short paragraphs win. Above 100 = wall of text. |
| `median_paragraph_words` | 30–60 | Most paragraphs land here. |
| `second_person_per_1k` | 15–35 | "you/your" frequency per 1,000 words. Low = third-person/distant; high = chatty/over-engaged. |
| `em_dash_per_1k` | 2–8 | Em-dashes used for genuine asides, not as filler. Above 12 = AI-tell. |

## How the script computes "in range"

The script computes the same metrics on the entire `examples/` corpus and flags any draft metric that's more than ±50% from the corpus value. That's a deliberately loose tolerance — it should catch obvious drift (a draft with 8 em-dashes per 100 words, or paragraphs averaging 140 words) without flagging healthy variation.

## When to recalibrate the baseline

If you swap the `examples/` files for different reference articles (e.g., to shift voice toward your brand's own existing content), the baseline shifts automatically — the script reads from the directory each run. No code changes needed.

## What the script doesn't catch

Stylistic things only a reader can judge:
- Paragraph rhythm (is the article boring even if metrics look fine?)
- Does the lead actually earn attention?
- Are concrete examples doing real work, or are they decorative?
- Does the conclusion feel earned, or perfunctory?

These are the adversarial sub-agent's job. The script handles measurable drift; the agent handles judgment.

## Default thresholds for the overall verdict

| Score | Verdict | Action |
|---|---|---|
| 75–100 | PASS | Proceed to /verify-claims |
| 60–74 | BORDERLINE | Editor reviews before proceeding |
| 0–59 | FAIL | Send back to /draft for regeneration |

The thresholds are heuristics. The editor can override.
