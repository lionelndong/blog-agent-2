# Tool URL Patterns

Reference for common deep-link URL patterns. Use these as templates when generating screenshot URLs. Substitute the actual product URLs from `brand-config.md` if the brand has its own tools.

## Ahrefs URL patterns (from public knowledge)

> Use these only if the brand IS Ahrefs or builds on top of Ahrefs reports. Otherwise refer to the brand's own product URLs.

| Report | URL pattern |
|---|---|
| Site Explorer overview | `https://app.ahrefs.com/site-explorer/overview/v2/[mode]/[target]` |
| Site Explorer top pages | `https://app.ahrefs.com/site-explorer/top-pages/v2/[target]` |
| Site Explorer organic keywords | `https://app.ahrefs.com/site-explorer/organic-keywords/v2/[target]` |
| Site Explorer backlinks | `https://app.ahrefs.com/site-explorer/backlinks/v2/[target]` |
| Keywords Explorer overview | `https://app.ahrefs.com/keywords-explorer/[country]/[keyword]/overview` |
| Keywords Explorer matching terms | `https://app.ahrefs.com/keywords-explorer/[country]/[keyword]/matching-terms` |
| Content Gap | `https://app.ahrefs.com/competitive-analysis/content-gap` |
| Rank Tracker | `https://app.ahrefs.com/rank-tracker/[project-id]/overview` |
| Site Audit issues | `https://app.ahrefs.com/site-audit/[project-id]/issues` |

## URL composition rules

- `[country]` codes: `us`, `uk`, `ca`, `au`, `de`, `fr`, `es`, `in`, `br`, `jp`, etc.
- `[mode]` for Site Explorer: `subdomains` (default), `prefix`, `exact`, `domain`
- `[target]` should be URL-encoded if it contains special characters
- Many reports require a logged-in user — the URL alone won't show the report; the editor must be authenticated

## When the brand has its own tools

Construct URLs based on the brand's product URLs in `brand-config.md`. The pattern usually looks like:

```
https://app.[brand-domain].com/[product-slug]/[report-name]?[query-params]
```

Inspect the brand's actual app URLs (visit the dashboard, copy a report URL, identify the variable parts) to template them properly.

## Generic URL fallback

If no specific report URL fits the placeholder, use the product's landing page or marketing page from `brand-config.md`. The editor can navigate from there.

## Example output entry

```
## Screenshot 4: Top Pages report for a competitor showing high-traffic pages
- **Tool URL:** https://app.ahrefs.com/site-explorer/top-pages/v2/exact/https%3A%2F%2Fcompetitor.com%2F
- **Filename:** screenshot-4-top-pages.png
- **Notes:** Filter "Traffic > 1,000" to keep the screenshot focused on meaningful pages
```
