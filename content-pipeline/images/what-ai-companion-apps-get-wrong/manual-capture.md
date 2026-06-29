# Manual capture for what-ai-companion-apps-get-wrong

Each entry below needs the editor to capture or upload manually:

## 1. chart: The five things AI companion apps get wrong (memory at the root)

- **Reason:** chart_data_unresolved:research_key_not_found:five_failure_taxonomy
- **Hint:** Provide chartable data: add it to content-pipeline/1-research/what-ai-companion-apps-get-wrong-data.json under the key the placeholder references (data=research.<key>), or inline JSON in data=, or a full ApexCharts options file via config=. Free-text data= cannot be charted.
- **Suggested filename:** `images/what-ai-companion-apps-get-wrong/chart-1-the-five-things-ai-companion-a.png`

Original placeholder: `[VISUAL:type=chart;data=research.five_failure_taxonomy;style=bar;title=The five things AI companion apps get wrong (memory at the root)]`

## 2. diagram: fixed context window dropping old turns vs. a persistent memory layer retaining facts across sessions

- **Reason:** diagram_requires_structured_data
- **Hint:** render_diagram_web.py needs structured nodes, not prose. Add data=research.<key> (resolved from content-pipeline/1-research/<slug>-data.json) or config=<path to a {direction,nodes,edges} spec>. linear: a list of {label,desc}; tree: a nested {label,children}; cycle: a list of {label,icon}. See DIAGRAM-THEME.md.
- **Suggested filename:** `images/what-ai-companion-apps-get-wrong/diagram-2-fixed-context-window-dropping.png`

Original placeholder: `[VISUAL:type=diagram;what=fixed context window dropping old turns vs. a persistent memory layer retaining facts across sessions;annotate=label "earlier exchanges drop" on the context-window side]`

## 3. diagram: context-churn loop — truncated history feeding generic repeated replies, contrasted with memory-fed varied replies

- **Reason:** diagram_requires_structured_data
- **Hint:** render_diagram_web.py needs structured nodes, not prose. Add data=research.<key> (resolved from content-pipeline/1-research/<slug>-data.json) or config=<path to a {direction,nodes,edges} spec>. linear: a list of {label,desc}; tree: a nested {label,children}; cycle: a list of {label,icon}. See DIAGRAM-THEME.md.
- **Suggested filename:** `images/what-ai-companion-apps-get-wrong/diagram-4-context-churn-loop-truncated-h.png`

Original placeholder: `[VISUAL:type=diagram;what=context-churn loop — truncated history feeding generic repeated replies, contrasted with memory-fed varied replies]`

## 4. table: Pleasur.ai coin tiers

- **Reason:** table_data_unresolved:unrecognized_data_form:pricing.coin_tiers
- **Hint:** Provide the table data: columns=A,B,C with rows in data= (inline JSON list or research.<key>), or a full spec via config=<path> / inline data=<spec object>. See COMPARISON-TABLE.md.
- **Suggested filename:** `images/what-ai-companion-apps-get-wrong/table-6-pleasur-ai-coin-tiers.png`

Original placeholder: `[VISUAL:type=table;data=pricing.coin_tiers;style=table;title=Pleasur.ai coin tiers]`

## 5. table: What to test, the failure it guards against, and the green flag

- **Reason:** table_data_unresolved:research_key_not_found:choose_checklist
- **Hint:** Provide the table data: columns=A,B,C with rows in data= (inline JSON list or research.<key>), or a full spec via config=<path> / inline data=<spec object>. See COMPARISON-TABLE.md.
- **Suggested filename:** `images/what-ai-companion-apps-get-wrong/table-9-what-to-test-the-failure-it-gu.png`

Original placeholder: `[VISUAL:type=table;data=research.choose_checklist;style=table;title=What to test, the failure it guards against, and the green flag]`
