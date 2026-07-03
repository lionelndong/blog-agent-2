# Manual capture for nsfw-apps

Each entry below needs the editor to capture or upload manually:

## 1. external: Google results for "nsfw apps" showing mixed app categories

- **Reason:** bounding_box_failed
- **Source URL:** https://www.google.com/search?q=nsfw+apps
- **Selector:** `#search`
- **Hint:** Playwright blocked (bounding_box_failed). Run `/capture-visuals nsfw-apps` to retry this entry via Claude-in-Chrome (real Chrome session bypasses the wall). The skill picks up `failed` external entries automatically in unattended mode.
- **Fallback:** /capture-visuals (Claude-in-Chrome) — Playwright blocked, retry via real Chrome session.
- **Suggested filename:** `images/nsfw-apps/external-1-google-results-for-nsfw-apps-s.png`

Original placeholder: `[VISUAL:type=external;sub=serp;url=https://www.google.com/search?q=nsfw+apps;selector=#search;crop=padded;what=Google results for "nsfw apps" showing mixed app categories;annotate=the different result types]`

## 2. external: Google results showing iPhone and app-store availability questions

- **Reason:** bounding_box_failed
- **Source URL:** https://www.google.com/search?q=does+apple+allow+nsfw+apps
- **Selector:** `#search`
- **Hint:** Playwright blocked (bounding_box_failed). Run `/capture-visuals nsfw-apps` to retry this entry via Claude-in-Chrome (real Chrome session bypasses the wall). The skill picks up `failed` external entries automatically in unattended mode.
- **Fallback:** /capture-visuals (Claude-in-Chrome) — Playwright blocked, retry via real Chrome session.
- **Suggested filename:** `images/nsfw-apps/external-2-google-results-showing-iphone.png`

Original placeholder: `[VISUAL:type=external;sub=serp;url=https://www.google.com/search?q=does+apple+allow+nsfw+apps;selector=#search;crop=padded;what=Google results showing iPhone and app-store availability questions;annotate=the iPhone and app-store wording]`

## 3. external: Apple App Store Review Guidelines safety section

- **Reason:** padded_crop_failed
- **Source URL:** https://developer.apple.com/app-store/review/guidelines/
- **Selector:** `#safety`
- **Suggested filename:** `images/nsfw-apps/external-3-apple-app-store-review-guideli.png`

Original placeholder: `[VISUAL:type=external;sub=news-quote;url=https://developer.apple.com/app-store/review/guidelines/;selector=#safety;crop=padded;what=Apple App Store Review Guidelines safety section;annotate=the objectionable-content policy language]`
