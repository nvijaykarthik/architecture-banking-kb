# C6-05 Account Management — BRIEF
> **Category:** Cx — Custody Lifecycles · **Difficulty:** ◑ · **Banking-relevant:** yes / 💳
>
> **One-liner:** Account management is the end-to-end lifecycle process that provisions, validates, operates, and terminates client custody accounts under CSA governance.
>
> **Why an enterprise architect / trainee cares:** A single un-terminated legacy account leaks compliance exposure and inflates regulatory reports; the architecture must support full account lineage from onboarding to final closure with immutable audit trails.
>
> ## Quick definition
> Account management covers the creation of every custody account (RA, RD, IRPS, unregistered), validation of agreements and KYC documents, daily operation, periodic review, and final termination/transfer. In Canadian wealth management, this includes the subset of Registered Retirement Income Fund (RRIF) and Registered Education Savings Plan (RESP) accounts, which carry unique regulatory rules separate from unregistered or mutual-fund accounts.
>
> ## Key ideas / terms
> - **Account opening:** The structured intake of client identity, beneficial ownership, and custody agreements to create a new client-account pair.
> - **KYC:** Know your customer; mandatory identity and suitability verification before or at account creation, governed by CSA and OSFI guidelines.
> - **CSR / QP holder:** Compliance service representative and qualified purchaser holder; the compliance/ownership layer that reviews and approves account changes.
> - **Account closure:** The formal termination, including asset transfer, data retention, and statement re-sending per jurisdictional rules.
> - **Asset registry:** The master mapping between client identifier, account type, and underlying holdings.
> - **RA / RD / IRPS / U/C:** Registered account, RD (Registered Retirement Savings), IRPS (In-house Registered Plan Services), U/C (unregistered / non-registered).
>
> ## The mental model
> Account management is the identity engine of custody. It produces the row in the asset registry and the branch in the settlement graph. Bad identity data—stale address, incorrect beneficial ownership—propagates into every downstream system (tax reporting, probate management, swap collateral), making it the highest-impact control surface.
>
> ## One diagram (mandatory)
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     Onboard[Onboarding]:::core --> Validate[KYC & agreement]:::critical
>     Validate --> Operate[Daily ops]:::core
>     Operate --> Review[Periodic review]:::core
>     Review --> Close[Closure]:::critical
>     Close --> Retain[Data retention]:::context
>     Operate --> PSR[Pattern setup]:::context
>     class Validate critical
> ```
>
> ## When to use / when NOT to use
> - ✅ **Use when:** Designing onboarding UX or planning a platform migration that touches client identifiers.
> - ⚠️ **Avoid when:** Talking about microseconds of API latency; account management is governed by SLAs measured in business days.
>
> ## Banking example
> A Crown corporation pension plan opens an RPP-compliant RA at CIBAM. The account manager must collect the corporate indenture, verify QP holder status under SHEA, and register the account in KFMS as type RA with RPP-specific tax-tagging. If the account is later closed because the sponsor divests, CIBAM must preserve the asset registry history for seven years per CSA Record-Keeping requirements, then perform a compliance-approved final transfer to a successor custodian.
>
> ## Common confusions (don't mix these up)
> - **Account management** vs **Portfolio management:** Account management owns the *container*; portfolio management owns the *positions inside*.
> - **RA** vs **RD:** RD is any registered account; RA is specifically an individual Savings/Discretionary/Non-Discretionary plan with distinct tax treatment.
>
> ## Interview / recall prompt
> “Explain account management in 2 minutes without notes.”
> - Name the five lifecycle phases: onboarding, validation, operations, review, closure.
> - State why KYC and QP holder verification are the critical path in onboarding.
> - Mention that RA/RRIF/RESP accounts carry unique regulatory rules not applicable to U/C accounts.
> - Explain that 24-hour closure for segregated (non-SIF) accounts is a regulatory expectation in Canada.
> - Note that seniority means priority in account allocation when an account number is released after closure.
>
> ## Status
> ☐ Not started · See detail doc: `details/C6-05-account-management.md`
>
> ---
> **One diagram required. Both brief + detail must exist before ✓.**
