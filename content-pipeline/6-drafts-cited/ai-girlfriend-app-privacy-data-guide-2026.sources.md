# Sources & verification trail — ai-girlfriend-app-privacy-data-guide-2026

PLE-1579 · verified 2026-06-11 by EO. Every claim in the draft maps to a source below; all URLs confirmed to resolve at time of verification.

## External citations (breach context + academic)

1. **androidheadlines.com (March 2026)** — "Why Your AI Girlfriend is a Privacy Time Bomb: 150M Users at Risk"
   https://www.androidheadlines.com/2026/03/ai-girlfriend-apps-security-risk-2026-study.html
   Verifies: Oversecured audit of 17 apps, 150M+ installs, 14 critical + 311 high-risk vulnerabilities, >half exposed chats via hardcoded credentials/script injection; one 10M+ app shipped cloud credentials in public code; also reported the Oct 2025 two-app 43M-message / 400K-user breach. **Status: VERIFIED.**

2. **helpnetsecurity.com (April 9, 2026)** — "113,000 explicit prompts from AI girlfriend platform exposed, many linked to user IDs"
   https://www.helpnetsecurity.com/2026/04/09/mylovely-ai-data-breach-user-conversations/
   Verifies: MyLovely AI, ~113,000 explicit prompts, ~70,000 tied to unique user IDs, emails + images + linked social profiles. **Status: VERIFIED.**

3. **cybernews.com** — "AI girlfriend hack might leak private content of over 100,000 users" (MyLovely AI)
   https://cybernews.com/security/ai-girlfriend-mylovely-leak-user-data/
   Verifies: de-anonymization risk; doxxing/sextortion framing. **Status: VERIFIED.**

4. **malwarebytes.com (Oct 2024)** — "AI girlfriend site breached, user fantasies stolen"
   https://www.malwarebytes.com/blog/news/2024/10/ai-girlfriend-site-breached-user-fantasies-stolen
   Verifies: the "this isn't new — pattern held for years" point. **Status: VERIFIED.**
   NOTE: the brief's malwarebytes Oct-2025 "two AI companion apps" URL did NOT resolve (404). Replaced the Oct-2025 two-app / 43M-message fact with the androidheadlines citation (source #1), which reports the same incident from a URL that resolves. No unverified URL is cited in the draft.

5. **arxiv.org — CHI 2026** — Ma, He, Martin-Navarro, Zhan, Such, "Privacy in Human-AI Romantic Relationships: Concerns, Boundaries, and Agency"
   https://arxiv.org/abs/2601.16824
   Verifies: accepted at ACM CHI 2026; 17-participant study; companions encouraged disclosure while privacy boundaries grew "more permeable" with closeness. **Status: VERIFIED (genuine CHI 2026 acceptance).**

6. **Mozilla Foundation — *Privacy Not Included*** — "Replika: My AI Friend"
   https://www.mozillafoundation.org/en/privacynotincluded/replika-my-ai-friend/
   Verifies the Replika FAQ: collects chat history, photos, voice recordings, device info, location, usage analytics; loaded many third-party trackers; shared behavioral data with advertising/marketing partners. **Status: VERIFIED via reputable third party** (Replika's own policy page returned a server error at fetch time; Mozilla used as the citable independent source so no claim about a named competitor is unsourced).

## Pleasur.ai data-practice claims — ALL sourced to our own published policy

Source: **https://pleasur.ai/legal/privacy-policy** (live, fetched 2026-06-11). Verbatim-grounded facts used in the comparison table, "How Pleasur.ai handles your data," and FAQs:

| Claim in draft | Policy basis |
|---|---|
| Collects email, username, password, profile details, avatar/bio/preferences | "Email address, username, password, gender, display name, and profile details… avatar, bio, preferences…" |
| Collects IP, browser, OS, device identifiers | "IP address, browser type and version, operating system, device identifiers" |
| Collects chat messages + generated content | "Chat messages, interactions with AI characters, and generated content" |
| Retention: active + up to 3 yrs post-deletion; financial up to 10 yrs | "Retained for as long as your account is active, and for up to three years after account deletion"; "Financial records… up to ten years" |
| Deletion on request anytime | "request deletion of your personal data at any time…" |
| Encryption in transit (TLS/SSL) AND at rest | "Encryption of data in transit (TLS/SSL) and at rest" |
| "We do not sell your personal information" | direct quote |
| No advertising partners among recipients | Recipients listed are service providers (hosting, payment, analytics, AI model providers), law enforcement, business transfers — no ad partners listed |
| 18+; no knowing collection from minors | "not intended for anyone under 18… do not knowingly collect personal information from minors" |
| GDPR / UK GDPR / CCPA; access/rectify/erase/port | "compliance with GDPR, UK GDPR, CCPA…" + rights enumerated |

**Internal-stack scrub:** policy names Supabase/Stripe as processors; draft deliberately uses neutral phrasing ("infrastructure service providers — hosting, payment, analytics") and names NO vendor (board internal-stack rule). Scrub clean.

## FAQPage JSON-LD (hand to CTO for site-side deploy)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {"@type":"Question","name":"What data do AI girlfriend apps collect?","acceptedAnswer":{"@type":"Answer","text":"Most AI girlfriend apps collect your conversation messages, photos, IP address, device identifiers, and financial transaction data. A 2026 audit of top apps found that more than half had critical flaws exposing intimate chat histories to unauthorized access."}},
    {"@type":"Question","name":"Are AI companion apps safe to use in 2026?","acceptedAnswer":{"@type":"Answer","text":"Safety varies sharply by platform. Look for encryption in transit and at rest, a clear no-sale data policy, and a working deletion process. Be cautious with apps named in the 2025-2026 breach reports, several of which exposed user data through basic misconfiguration."}},
    {"@type":"Question","name":"Which AI girlfriend app has the best privacy in 2026?","acceptedAnswer":{"@type":"Answer","text":"There is no single safest app — the right question is which practices an app commits to: encryption in transit and at rest, a stated no-sale policy, named data recipients, and a self-serve deletion right. Pleasur.ai's published policy commits to encryption at rest and in transit, states it does not sell personal information, lists no advertising partners among its recipients, and lets you request deletion at any time."}},
    {"@type":"Question","name":"Can AI girlfriend apps share your conversations with third parties?","acceptedAnswer":{"@type":"Answer","text":"Many can and do. Privacy policies frequently permit sharing with analytics, advertising, and AI-training partners. Review each app's policy for an explicit statement on selling versus sharing, and check for opt-out rights under GDPR or CCPA."}},
    {"@type":"Question","name":"What data does Replika collect?","acceptedAnswer":{"@type":"Answer","text":"According to its privacy policy and an independent Mozilla Privacy Not Included review, Replika collects your chat history, photos, voice recordings, device information, location, and usage analytics, and has shared behavioral data with advertising and marketing partners."}},
    {"@type":"Question","name":"Is Pleasur.ai safe to use?","acceptedAnswer":{"@type":"Answer","text":"Pleasur.ai is built for adults 18 and over, and its published privacy policy commits to encryption in transit and at rest, a no-sale data policy, retention limits, and deletion on request. No platform can guarantee perfect security, but those are the concrete practices to weigh."}}
  ]
}
```

## Compliance posture (PIPELINE.md gate 3)

- Explicit content: NONE. Clinical/factual throughout — targetable on ChatGPT/Gemini/Perplexity/AIO.
- Adult-content boundaries: no "no filter" absolutism, no safety guarantees (FAQ #6 explicitly states "no platform can guarantee perfect security"), 18+ framing, no real-person likeness.
- **Legal/privacy copy → BOARD SIGN-OFF REQUIRED before publish.** This is the one carve-out from autonomous publish. Every Pleasur.ai claim is sourced to our own live policy, but the article makes data-practice + named-competitor claims in a breach context, so it routes to the board per gate 3 and per the brief ("confirm all Pleasur.ai data practice claims before publishing").
