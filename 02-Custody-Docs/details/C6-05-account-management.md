# C6-05 Account Management — DETAIL
> **Category:** Cx — Custody Lifecycles · **Difficulty:** ◑ · **Banking-relevant:** yes / 💳
> **Companion brief:** `briefs/C6-05-account-management.md`
>
> > **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.
>
> ---
>
> ## 1. Precise definition
> Account management is the governance-backed lifecycle service that establishes, operates, audits, and terminates custody accounts. It encompasses legal entity onboarding, KYC/AML clearance, agreement execution, identity linkage to the asset registry, and controlled closure with mandatory data retention and audit logging. In Canadian wealth management, it specifically differentiates between Registered (RA/RD/IRPS/RPP/RESP), Unregistered (U/C), and segregated (non-SIF) accounts, each with distinct regulatory triggers for closure and reporting.
>
> ## 2. Why it exists (the problem it solves)
> Without a standardized account lifecycle, institutions created orphaned account numbers (UI12345), stale KYC files, and duplicate identifiers for the same beneficial owner. This produced three failure modes: (1) regulatory reports filed for closed accounts, (2) tax slips issued to wrong owners, and (3) forensic investigations unable to trace asset provenance. Formal account management—introduced in the 2003 CSA Best Practices Guide—imposed a state-machine model: every account must be opened, validated, operated, reviewed, and closed, with each transition audited.
>
> ## 3. Core concepts & vocabulary
> | Term | Precise meaning |
> |------|-----------------|
> | Onboarding | Intake phase: identity capture, beneficial-owner disclosure, account-type selection, agreement signature, and KFS-KFS linkage creation. |
> | KYC/AML | Know your customer / anti-money-laundering; Layer-1 (identity), Layer-2 (source of wealth/funds), Layer-3 (continuous monitoring). |
> | QP holder | Qualified purchaser; the legal entity legally permitted to hold securities in nominee name within a registered plan. |
> | Segregated (non-SIF) | Account type where client assets are held in a dedicated vault/account separate from the custodian's own assets, per NI 31-103. |
> | SIF | Special Investment Fund; netted, pooled account with fixed allocation rules. |
> | Engagement letter / advice agreement | Vertically and horizontally signed agreement between advisor, client, and custodian; required for discretionary accounts. |
> | Trade restriction | A delight rule that blocks all transactions (e.g., deceased owner post-probate); triggers separate closure workflow. |
> | Inter-account transfer | Movement of holdings from one registered account to another without liquidation (e.g., RPP to RD).
> | FOM | Flag of maturity; marks an RPP as matured and triggers conversion or payout.
>
> ## 4. How it works (architecture / mechanism)
> Account lifecycle is a state machine implemented in KFMS:
> 1. **Onboard:** Portal or advisor CLI submits identity JSON; system validates against Lookup-OFAC, performs Layer-1/2 checks, and triggers agreement generation (deposit agreement + CSA mandate).
> 2. **Validate:** CSR/QP holder reviews KYC package, executes engagement letter if discretionary, and publishes the account with final status.
> 3. **Operate:** Daily feed processes incoming deposits/redeems/instructions; system writes to asset registry and settlement queue.
> 4. **Review:** Monthly/annual compliance scan checks for stale KYC, lopsided account balances, and regulatory flag triggers (FOM, etc.).
> 5. **Close:** Initiation (client/advisor request), transfer (to successor or liquidation), retention (7-year archive), and ID release (immediate if SIF, 24 h if segregated).
>
> ### 4.1 Diagrams
>
> **Diagram A — Core structure** (highlight load-bearing parts = amber, supporting = grey):
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     Portal[Portal / CLI]:::context --> KYC[KYC Validation]:::core
>     KYC --> Open[Account Open]:::critical
>     Open --> QM[KYC monitored]:::core
>     QM --> Review[Compliance review]:::core
>     Review --> Close[Closure / transfer]:::critical
>     Close --> Archive[7-year archiving]:::context
>     class Open critical
>     class Close critical
> ```
>
> **Diagram B — Lifecycle / flow** (highlight decision points = green, failures = red, money = gold):
> ```mermaid
> graph LR
>     classDef ok fill:#a7f3d0,stroke:#065f46,color:#000
>     classDef risk fill:#fecaca,stroke:#991b1b,color:#000
>     classDef money fill:#fde68a,stroke:#92400e,stroke-width:1px,color:#000
>     Start[Client request]:::money --> A[Identity captured]:::ok
>     A --> B{Discretionary?}:::risk
>     B -->|yes| C[Engage advisor]:::ok
>     B -->|no| D[Standard RA / U/C]:::ok
>     C --> E[Agreement signed]:::ok
>     D --> E
>     E --> F[Account issued]:::money
>     F --> G{Periodic review}:::risk
>     G -->|pass| H[Continue ops]:::ok
>     G -->|fail| I[Compliance hold]:::risk
> ```
>
> **Diagram C — Account opening state machine** (highlight critical transitions = amber, core states = green, context = grey):
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     Pending[Pending]:::context --> KYC_OK[KYC OK]:::core
>     KYC_OK --> Doc_Signed[Docs signed]:::core
>     Doc_Signed --> Internal[Internal review]:::core
>     Internal --> Active[Active]:::ok
>     Active --> Closed[Closed]:::critical
>     Closed --> Archived[Archived]:::context
>     Active --> Trapped[Status hold]:::risk
>     class Active ok
>     class Closed critical
> ```
>
> ## 5. Variants, options & trade-offs
> | Variant | When to pick | When to avoid | Key trade-off axis |
> |---------|--------------|---------------|--------------------|
> | Digital onboarding (e-Docs + e-Consent) | Retail-scale accounts where speed > advisor touch | High-net-worth or corporate accounts requiring wet signatures | Speed vs regulatory defensibility |
> | Self-service portal | Repeat clients with validated KYC | New investors with complex beneficial ownership | UX vs Layer-3 depth |
> | Manual onboarding (advisor-led) | Discretionary, institutional / RP-specific accounts | Mass-market platforms | Service level vs cost |
> | Segregated (non-SIF) | Non-netted accounts under NI 31-103 | Pooled mutual fund accounts | Individual asset control vs operational scalability |
>
> ## 6. Relationships to sibling topics
> - **C5-02-cash-management:** Cash deposits are a primary onboarding/funding source; account management drives the funds-inbound workflow.
> - **C5-03-direct-security-ownership:** Direct ownership is a holdings-type attribute configured during onboarding; the asset registry links both indirectly.
> - **C6-06-account-lifecycle:** This topic describes the full enclosure; C6-05 is the detailed operationalization of each phase.
>
> ## 7. Banking / financial-services context 💳
> Under NI 31-103 and CSA Rules 11-502 to 11-516, CIBAM cannot accept assets until KYC is complete and the QP holder is validated. For an RA opened for a senior living facility, the QP holder must confirm there is no disqualifying event (death, divorce, disability) before the account goes live. If closure is initiated post-mortem, probate documentation must be attached before release; otherwise the account enters a hold state and generates a compliance exception. The architecture must therefore gate the "Active" state transition with both KYC clearance and successor-attestation documents.
>
> ## 8. Reference architecture / worked example
> Sun Life issues 4,000 SEP-RA accounts under the CIBAM platform.
> - **Decision:** Use digital onboarding with e-consent for agents, but require wet-signature delivery for high-net-worth clients (>1M CAD).
> - **Architecture:** Portal feeds identity to KFMS API; KFMS calls third-party KYC provider; if clean, KFMS auto-populates deposit agreement, routes to advisor for discretionary flag capture, and opens account in 4 minutes.
> - **ADR:** We standardized on OAuth2 + PKCE for portal access; wet-signature files stored in object storage with WORM immutability for 7-year retention.
> ```mermaid
> graph LR
>     classDef service fill:#bfdbfe,stroke:#1e40af
>     classDef data fill:#fde68a,stroke:#92400e
>     classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5
>     Advisor[Sun Life advisor]:::service --> Portal[Client portal]:::service
>     Portal --> KFMS[KFMS onboarding]:::service
>     KFMS --> KYC[KYC provider API]:::service
>     KFMS --> Document[(Document store)]:::data
>     KFMS --> Registry[Asset registry]:::data
>     class KFMS service
> ```
>
> ## 9. Maturity & adoption signals
> - **Adopt when:** >80% onboarding is digital with <10% manual exception rate and KYC revalidation runs automatically.
> - **Anti-signals (don't adopt yet):** Account opening still requires physical mail for any document; no e-consent integration.
> - **Common failure modes:** (1) Stale KYC detected >1 year old, (2) Document expiration not flagged, (3) Account closure not gated by probate for deceased owners.
>
> ## 10. Common confusions — the "don't mix" list
> | Often confused | Real distinction |
> |----------------|------------------|
> | Account management vs portfolio management | Account owns the container; portfolio owns holdings and strategies. |
> | RA vs RD vs U/C | RA is individual registered; RD is any registered; U/C is non-registered. |
> | Engagement letter vs Advice agreement | Engagement letter is advisor-client; advice agreement is advisor-custodian (vertical + horizontal). |
> | Segregated vs SIF | Segregated is individually controlled; SIF is netted and pooled. |
>
> ## 11. Tools & standards to know
> - **Frameworks/IR-2 / NINE:** CSA Rules 11-502 to 11-516 (account requirements), NI 31-103 (custody), OSFI B-13 (operational risk).
> - **Common tooling:** Salesforce/Actinon for onboarding UIs, KFMS for lifecycle engine, Archi for state-machine mapping, Databricks for KYC analytics.
> - **Mandatory reading:** CSA Best Practices Guide, OSFI Guideline B-25 (Account closure and record keeping).
>
> ## 12. ADR template (ready to fill in)
> ```markdown
> # ADR-13: Digital onboarding with digital signatures
> ## Status
> Accepted
> ## Context
> Paper-based onboarding for RA/RD accounts takes 10 business days and causes 15% client drop-off.
> ## Decision
> Adopt DocuSign-integrated portal; digitally signed documents stored in WORM object storage for 7-year retention.
> ## Consequences
> - Positive: 4-minute onboarding, reduced fraud via identity binding.
> - Negative: $85K annual DocuSign cost + legal review for e-consent validity under provincial e-commerce acts.
> ## Alternatives considered
> 1. Private e-signature tool — rejected due to lack of provincial notarization support.
> 2. In-person notarization — rejected due to 15 business-day latency.
> ```
>
> ## 13. Practice — apply it
> 1. **Recall:** define in 2 min without notes.
> 2. **Model:** produce an ArchiMate business-process diagram for the RA onboarding state machine.
> 3. **ADR:** write a decision doc for a senior living operator launching 10,000 PI RA accounts.
> 4. **Defend:** roleplay explaining why a segregated account opening requires prosecutor/notary sign-off under NI 31-103.
>
> ## Summary
> Account management is custody's sine qua non. If the account lifecycle is broken, every downstream system—settlement, reporting, tax, probate, and compliance—inherits bad data. The enterprise architect's job is to make each state transition atomic, auditable, and reversible only through an explicitly-governed workflow, so that no client asset ever disappears into an ungated void.
>
> ---
> **Status:** ☐ Not started · ☐ In progress · ✅ Covered
> *Last updated: 2026-09-16*
>
> ---
> **One diagram required. Both brief + detail must exist with ≥1 mermaid each before ✓.**
