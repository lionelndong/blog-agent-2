# Debug index — what-is-an-ai-girlfriend (PLEAA-392 dry-run)

**Commit:** [`d10899a`](https://github.com/lionelndong/blog-agent-2/commit/d10899a) · **Quality verdict:** PASS 94/100

## Step-by-step pipeline output

Click each stage to see exactly what that step produced, in order.

| # | Stage | Output |
|---|---|---|
| 0 | Keyword pick | informational, picked on-the-spot per keyword-policy v3 (no queue) |
| 1 | Research (broad + deep) | [`1-research/what-is-an-ai-girlfriend.md`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/1-research/what-is-an-ai-girlfriend.md) · [`-deep.md`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/1-research/what-is-an-ai-girlfriend-deep.md) · [`-data.json`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/1-research/what-is-an-ai-girlfriend-data.json) |
| 2 | Reference snapshot | [`2-reference/what-is-an-ai-girlfriend.md`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/2-reference/what-is-an-ai-girlfriend.md) |
| 3 | Outline | [`3-outlines/what-is-an-ai-girlfriend.md`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/3-outlines/what-is-an-ai-girlfriend.md) |
| 4 | Outline annotated (cite + visual placement) | [`4-outlines-annotated/what-is-an-ai-girlfriend.md`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/4-outlines-annotated/what-is-an-ai-girlfriend.md) |
| 5 | Draft | [`5-drafts/what-is-an-ai-girlfriend.md`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/5-drafts/what-is-an-ai-girlfriend.md) |
| 6 | Draft + citations | [`6-drafts-cited/what-is-an-ai-girlfriend.md`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/6-drafts-cited/what-is-an-ai-girlfriend.md) |
| 7 | Preview HTML | [`7-preview/what-is-an-ai-girlfriend.html`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/7-preview/what-is-an-ai-girlfriend.html) · **[render in browser](https://raw.githack.com/lionelndong/blog-agent-2/main/content-pipeline/7-preview/what-is-an-ai-girlfriend.html)** |
| 8 | Strapi-ready package | [`8-publish/what-is-an-ai-girlfriend/`](https://github.com/lionelndong/blog-agent-2/tree/main/content-pipeline/8-publish/what-is-an-ai-girlfriend) (article.md + article.json + README.md) |
| Q | Quality checks | [`quality-checks/what-is-an-ai-girlfriend.md`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/quality-checks/what-is-an-ai-girlfriend.md) (verdict) · [`-metrics.md`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/quality-checks/what-is-an-ai-girlfriend-metrics.md) (auto) · [`-adversarial.md`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/quality-checks/what-is-an-ai-girlfriend-adversarial.md) (skeptical reader) |
| O | Optimization (intermediate) | [`optimization/what-is-an-ai-girlfriend.md`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/optimization/what-is-an-ai-girlfriend.md) · [`-baseline-quality.md`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/optimization/what-is-an-ai-girlfriend-baseline-quality.md) · [`-iter-0.md`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/optimization/what-is-an-ai-girlfriend-iter-0.md) · [`-errors.log`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/optimization/what-is-an-ai-girlfriend-errors.log) |
| V | Visuals (manifest only) | [`images/what-is-an-ai-girlfriend/manifest.json`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/images/what-is-an-ai-girlfriend/manifest.json) · [`manual-capture.md`](https://github.com/lionelndong/blog-agent-2/blob/main/content-pipeline/images/what-is-an-ai-girlfriend/manual-capture.md) |

## Visuals on this article

**Zero `<img>` tags in the rendered preview.** One visual placeholder in the draft (action-shot of `https://pleasur.ai/create`); the pipeline's image stage routed it to `manual` status with reason `action_shot_routed_to_editor` because action-shots require live browser capture, not generated illustrations. The raw `[VISUAL:...]` tag is sitting untransformed in `article.md` line 150 — that's a real bug (publish should either capture or strip placeholders, not ship them).

## Quality at a glance

| Dimension | Score |
|---|---|
| Forbidden phrases | 20/20 |
| Voice metrics vs baseline | 25/25 |
| BLUF compliance (H2 openers) | 20/20 |
| Claim density + linkability | 13/15 |
| Adversarial verdict | 16/20 |
| **Total** | **94/100 PASS** |

3 HIGH items (light-edit, not blockers) listed in the quality-check file linked above.
