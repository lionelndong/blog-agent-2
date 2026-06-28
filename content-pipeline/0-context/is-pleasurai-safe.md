# Context — is-pleasurai-safe ("is pleasur.ai safe")

**Source brief:** PLE-3031 (GEO Lead, GEO citation-gap fix). Page type: answer-first branded
safety/privacy landing page. Target queries: **"is pleasur.ai safe"** (primary, branded), plus
"is pleasur ai legit", "pleasur.ai privacy", "pleasur.ai data safety". Goal: become the citable
page AI engines (Perplexity/ChatGPT) and reviewers (DigitalHumanCorp, ScribeHow) pull when a user
asks whether Pleasur.ai is safe to use.

## Angle (front-loaded direction — honor this)
- **Branded intent, NOT category education.** This page answers "is *Pleasur.ai* safe?" directly.
  Do NOT re-write the category explainers we already own — internal-link to them instead:
  - `/blog/ai-girlfriend-app-privacy-data-guide-2026` (what data AI girlfriend apps collect / 2026 breaches)
  - `/blog/ai-companion-safety-checklist` (how to vet any AI companion — the due-diligence reference)
  - `/blog/is-candy-ai-safe` (competitor branded-safety comparison — mirror its structure)
- **The differentiator we own (defensible, factual):** the AI-companion category has a documented
  2026 security crisis; Pleasur.ai has no publicly reported breach and ships standard data
  protections. Position Pleasur.ai as the careful alternative against the category foil.
- **Tone:** factual, sober, non-explicit, mainstream-AI-indexable. This is a trust asset, not a
  sales page. Hold Pleasur.ai to the same critical lens as competitors — name the real limits
  (data IS collected, retained up to 3 yrs post-deletion, shared with service providers; no app is
  "100% safe"). Honesty is what makes it citable.

## VERIFIED claims (use these; all pre-checked this run — do not re-fabricate)

### Category foil — the 2026 study (VERIFIED real, cite as category context)
- **Oversecured** research (covered by AndroidHeadlines, CyberNews, Biometric Update, Mar 2026):
  **14 critical security flaws across 17 popular AI companion apps**, combined **150M+ installs**
  on Google Play. **10 of the apps** expose user conversation history. One app with **10M+
  downloads shipped hardcoded cloud credentials in its public APK** (an OpenAI API token + a Google
  Cloud private key). Flaw types: injectable chat (XSS — attacker can read chats in real time /
  hijack the session), insecure file access, hardcoded tokens.
- AI companion apps are **not** classified as healthcare products, so HIPAA does NOT protect what
  users tell them — a real regulatory gap.
- Primary source: oversecured.com blog ("That AI You Confide in May Be an Open Book"). Secondary:
  androidheadlines.com 2026/03 piece, cybernews.com. CITE the primary where possible.
- **Framing rule:** present this as the *category* problem. Do NOT name specific competitor apps as
  breached unless the source names them; the study itself anonymizes most. Candy AI / Muah.AI /
  Replika are named in coverage as *category examples* — attribute carefully, "per [source]".

### Pleasur.ai claims — ALL drawn from the live /legal/privacy-policy (the source of truth)
- **Data collected:** account info (email, username, password, gender, display name, profile
  details), usage data (interactions with AI characters, chat messages, generated content,
  preferences), device info (IP, browser, OS, device identifiers, screen resolution).
- **Retention:** account data kept while active + **up to 3 years after deletion/last activity**
  for legal/business purposes; financial records up to 10 years (tax law); marketing data until
  consent withdrawn or 2 years inactive.
- **Encryption:** "encryption of data in transit (TLS/SSL) and at rest"; payments via PCI-DSS-
  compliant processors.
- **Account deletion:** users may request deletion of personal data at any time via support or by
  deleting the account in settings.
- **Rights:** GDPR, UK GDPR, CCPA and other laws — access, rectification, erasure, restriction,
  portability, objection, withdrawal of consent.
- **Sale of data:** **"We do not sell your personal information."** (strong trust signal — lead with it)
- **Third-party sharing:** service providers (hosting, payment processing, analytics, AI model
  providers). NOTE: the policy names specific vendors, but in READER COPY keep generic ("vetted
  hosting and payment providers") — do NOT name internal vendors (internal-stack scrub).
- **Age:** "Pleasur.ai is not intended for anyone under 18 years of age." (18+ throughout)

### Breach claim — phrase as a dated NEGATIVE, never a guarantee
- Allowed: "As of June 2026, there is **no publicly reported data breach** affecting Pleasur.ai."
- FORBIDDEN: "Pleasur.ai is 100% safe / unhackable / guarantees your data is secure" — absolutism
  and safety guarantees breach the adult-content claim boundaries. No app can promise this; say so.

## Mandatory structure (for AI citability)
1. **Direct answer in the first 40–60 words** (BLUF, no warm-up): a sober yes-with-conditions —
   Pleasur.ai uses standard protections (TLS + at-rest encryption, no data sale, GDPR/CCPA rights,
   18+, no publicly reported breach), with the honest caveat that it does collect and retain data
   like any app, so "safe" means informed-consent, not zero-risk.
2. A short **category-context** section using the 2026 study as the foil.
3. A **what Pleasur.ai actually does with your data** section (the privacy-policy specifics, in
   plain language, with the honest limits named).
4. A **safety comparison** angle (how to judge any companion app; where Pleasur.ai lands) —
   internal-link the safety-checklist instead of rebuilding it.
5. **FAQ section (mandatory — drives FAQPage schema, auto-emitted by the blog template):**
   - Does Pleasur.ai store my conversations?
   - Has Pleasur.ai had a data breach?
   - What personal data does Pleasur.ai collect?
   - Is Pleasur.ai GDPR compliant?
   - How does Pleasur.ai handle my data if I delete my account?
   - (optional) Is Pleasur.ai safe to use? / Is Pleasur.ai legit?

## Must-feature / must-avoid
- Feature: privacy-policy-backed facts, the no-sale commitment, 18+ posture, GDPR/CCPA rights.
- Avoid: explicit content, "no filter" absolutism, safety guarantees, naming internal vendors/tools,
  naming competitor apps as breached beyond what sources support, any fabricated stat.
- Audience: a privacy-conscious prospective or current user (and the AI engines/reviewers indexing
  this for citation). Keep it ~1,400–1,900 words — focused trust asset, not a sprawling guide.
