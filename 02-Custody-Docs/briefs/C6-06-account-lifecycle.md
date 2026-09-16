# C6-06 Account Lifecycle — BRIEF
> **Category:** Cx — Custody Operations · **Difficulty:** ◑ · **Banking-relevant:** yes / 💳
>
> **One-liner:** Account lifecycle is the continuous stewardship of an account from opening through operation, review, and eventual closure, ensuring regulatory compliance and asset integrity at every phase.
>
> **Why an enterprise architect / trainee cares:** Incomplete lifecycle discipline creates orphaned accounts, stale KYC, and compliance gaps; lifecycle metadata is the foundation for all tax, probate, and regulatory reporting pipelines.
>
> ## Quick definition
> Account lifecycle is a formal, auditable sequence of states that every custody account must pass through: opening (identity, agreement, compliance clearance), operation (settlement, valuation, instruction processing), review (compliance scans, fee reconciliation), and closure (transfer, liquidation, retention). In Canadian wealth management, RRIF and RESP accounts have additional states (FOM trigger, beneficiary transfer) that must be modeled explicitly.
>
> ## Key ideas / terms
> - **Lifecycle state:** An atomic, auditable phase (e.g., Active, Review, Hold, Closed) with defined entry/exit criteria.
> - **Probate:** Legal confirmation of will validity; required before an account can be closed for a deceased owner.
> - **Beneficiary:** A legally designated recipient of account assets upon owner death, before probate is finalized.
> - **Implied beneficiary:** A beneficiary inferred or identified by governance process when the account has a deceased owner but no principled beneficiary is named.
> - **Fiscal year closing:** Year-end process that freezes valuations, calculates fees, and produces custodian statements and tax reports.
> - **SIF / non-SIF:** Special Investment Fund (netted, pooled) vs segregated (dedicated, non-pooled); classification is a lifecycle attribute set at opening and reviewed when directives change.
> - **Rulebook:** The custodian's internal policy document that defines lifecycle gates, retention schedules, and escalation procedures.
>
> ## The mental model
> The account lifecycle is a temporal graph: each account is a node, and each state transition is a directed edge. The architecture must store not just the current state but the full path (provenance) so that auditors can reconstruct when and why an account moved from Active to Closed. Missing one edge gap (e.g., closure without retention) breaks the graph and generates a compliance exception.
>
> ## One diagram (mandatory)
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     Open[Opening]:::core --> Oper[Operation]:::core
>     Oper --> Review[Review]:::core
>     Review --> Closure[Closure]:::critical
>     Closure --> Retain[Retention]:::context
>     Closure --> Beneficiary[Beneficiary transfer]:::core
>     Oper --> Probate[Probate (deceased)]:::context
>     Probate --> Closure
>     class Closure critical
> ```
>
> ## When to use / when NOT to use
> - ✅ **Use when:** Designing a governance dashboard or lifecycle-state machine for custody accounts.
> - ⚠️ **Avoid when:** Discussing high-frequency instruction processing; lifecycle transitions are governed by compliance, not speed.
>
> ## Banking example
> A segregated (non-SIF) RPP account with a deceased owner enters a probation hold when the FP-001 death benefit flag is raised. KFMS triggers a probate-state transition: all transactions are blocked, life-insurance proceeds cannot be released, and the asset registry freezes the position. After probate is approved, exit-to-transition raises allocation, and the account moves to closure. CIBAM must retain the full lifecycle history for seven years under CSA record-keeping rules, and the taxonomy of that retention is itself a lifecycle attribute.
>
> ## Common confusions (don't mix these up)
> - **Account lifecycle** vs **Account management:** Lifecycle is the *framework and metadata*; management is the *operational execution* within each state.
> - **Probate** vs **Beneficiary transfer:** Probate is the court process before distribution; beneficiary transfer can occur if the account has a named beneficiary and no probate is required.
>
> ## Interview / recall prompt
> “Explain account lifecycle in 2 minutes without notes.”
> - Name the four main phases: opening, operation, review, closure.
> - Explain why RRIF/RESP have additional states (FOM trigger, beneficiary transfer).
> - State that probate blocks all transactions and locks the record.
> - Mention that SIF classification is set at opening and reviewed only when directives change.
> - Describe the accounting-retention state as permanent; the account ID is frozen but data is not deleted.
>
> ## Status
> ☐ Not started · See detail doc: `details/C6-06-account-lifecycle.md`
>
> ---
> **One diagram required. Both brief + detail must exist before ✓.**
