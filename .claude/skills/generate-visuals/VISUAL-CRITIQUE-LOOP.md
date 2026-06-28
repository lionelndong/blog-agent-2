# Visual critique loop — LOCKED 2026-06-28 (render → critique → fix → re-render → gate)

**Every generated visual (annotation, infographic, chart) MUST pass this loop before it is
published.** AI mistakes — wrong target, garbled/clipped text, covered content, off-brand —
get caught here, not by readers. Modeled on the infographic blueprint-critique loop.

## Loop (max 3 iterations)
1. **Render** the visual.
2. **Deterministic checks** (machine, no AI):
   - *annotation* — read the `<out>_report.json`: is every target `found:true`? any `edge_clipped:true`?
     Always run `annotate_screenshot.py --strict` so a missing target **hard-fails** (NO silent skip — mandate).
   - *infographic / chart* — file exists, non-empty, expected dimensions.
3. **Vision critique** — the agent looks at the rendered PNG against the checklist below and
   returns JSON `{pass: bool, issues: [{idx, problem, fix}]}`. Be a STRICT critic: if unsure, fail it.
4. If not `pass` → **apply the fixes** to the spec and go to 1:
   - annotation: change `selector` / `kind` / `corner` / `pad` / `color`.
   - infographic: fix `content` / wording / layout / item count.
   - chart: fix data / labels / palette.
5. After **3 failed passes** → **DO NOT publish.** Flag a human with the issues + the latest render.

## Checklists
### Annotation
- [ ] Each annotation sits on the **correct** element (matches its note/intent).
- [ ] All target text fully visible — **no clipping** (especially zoom insets), no cut words.
- [ ] No annotation/inset **covers other important content** (prices, CTAs, other annotations).
- [ ] Labels legible, not overlapping each other or key UI.
- [ ] Highlight fill keeps the underlying text readable.
- [ ] Colors on-brand (blue `#2E90FA` default), consistent; numbering reads top→bottom / left→right.

### Infographic
- [ ] Every word + number spelled correctly and **fully inside the frame** (no crop).
- [ ] Text is clean sans (NOT handwritten); only the illustration is hand-drawn.
- [ ] Clear hierarchy, uncluttered; on-brand palette; takeaway present.
- [ ] **Real logo** present (composited via `composite_logo.py`, never AI-drawn).

### Chart
- [ ] Axes / labels / legend correct + legible; numbers **match the source data**.
- [ ] On-brand palette + font; clean canvas (not default matplotlib); no truncated labels.

## Who is the critic
The vision critic is the **agent itself** (it has vision) or a spawned vision sub-agent. The
deterministic report is the cheap first filter; the vision pass catches semantic/aesthetic issues.
Bias toward an extra pass — a wasted render is cheap, a bad published visual is not.
