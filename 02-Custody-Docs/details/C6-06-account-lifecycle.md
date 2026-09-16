# C6-06 Account Lifecycle — DETAIL
> **Category:** Cx — Custody Operations · **Difficulty:** ◑ · **Banking-relevant:** yes / 💳
> **Companion brief:** `briefs/C6-06-account-lifecycle.md`
>
> > **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.
>
> ---
>
> ## 1. Precise definition
> Account lifecycle is a formally governed temporal model that defines every legally and operationally meaningful state a custody account may enter, the transitions between those states, the conditions for entry and exit, and the immutable audit trail of all state changes. It is implemented as a state machine in KFMS (or equivalent lifecycle engine) with states: Opening, Active, Review, Hold, Closure, Retention, and Death (probate). Each state maps to a distinct set of operational rules (e.g., transaction permitted/blocked, reporting enabled/disabled, retention schedule active).
>
> ## 2. Why it exists (the problem it solves)
> Pre-lifecycle-governance institutions had accounts that "went dark": wallet-deposit accounts never reviewed, closure paperwork missing, KYC stale for years, and death notifications only discovered during annual valuation. The 2013 CSA inspection found 12% of examined accounts lacked a documented closure record. Lifecycle governance fixes this by making state transitions mandatory, event-driven, and auditable. It also solves the RRIF withdrawal problem: many institutions processed an RRIF payout at age 71 without checking the minimum-withdrawal threshold, creating retroactive tax penalties.
>
> ## 3. Core concepts & vocabulary
> | Term | Precise meaning |
> |------|-----------------|
> | Lifecycle state | Atomic, auditable phase with defined entry/exit criteria, enforced by the lifecycle engine. |
> | State transition | Event-driven movement from one state to another; each requires a governing rule and an approver. |
> | Death state / probate | Terminal sub-state for deceased owners; blocks all transactions until court-approved probate releases the account. |
> | Beneficiary transfer | Movement of assets to a named beneficiary before probate, triggered by a death certificate only. |
> | Implied beneficiary | A beneficiary inferred by governance when the owner is deceased, no principal beneficiary named, and no probate is required (e.g., spouse defaults).
> | Fiscal year closing | Annual snapshot of valuations, fee accruals, and statement generation; marks a RPP as The Four Mandatory Decisions point.
> | Did not opt / NPO | Retirement Planning Output; the minimum RPF / RIF withdrawal the owner must take, computed as % of prior year value.
> | Recurring maturity | Age-based trigger (e.g., RPP reachable, RPP flat) that changes account behavior and may force closure.
> | Transfer / transfer out | Movement of account between custodians or within the same custodian for consolidation; must preserve state and retention metadata.
>
> ## 4. How it works (architecture / mechanism)
> Lifecycle is enforced by a state machine in KFMS plus a set of lifecycle rules:
> 1. **Opening:** Identity capture, agreement aggregation, compliance clearance, and state = Open.
> 2. **Activation / Active:** All transactions permitted; periodic compliance scan every 30 days.
> 3. **Review:** Scheduled compliance checkpoint (annual/quarterly); if criteria fail, state = Hold.
> 4. **Hold, Closure,Retention:** If account owner dies, state = Death Under Probate. All transactions blocked; only beneficiary transfer or probate-approved release permitted.
> 5. **Beneficiary transfer:** If a named beneficiary exists and no probate is required, assets transfer to beneficiary account; state = Closed.
> 6. **Fiscal year closing:** At year-end, the engine applies The Four Mandatory Decisions (null, TFD, continue, maintain), recalculates Did Not Opt, and publishes tax reports.
> 7. **Retention:** Dead account ID frozen; data retained per jurisdiction (7-year CSA minimum); state = Archived.
>
> ### 4.1 Diagrams
>
> **Diagram A — Core structure** (highlight load-bearing parts = amber, supporting = grey):
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     Validate[Validate]:::core --> Issue[Issue: Active]:::critical
>     Issue --> Review[Review]:::core
>     Review -->|pass| Operate[Operating]:::ok
>     Review -->|fail| Trends[Trends review]:::context
>     Operate --> Review
>     Operate --> Deceased[Deceased / probate]:::risk
>     Deceased --> Closure[Closure and transfer]:::critical
>     Closure --> Retain[Retention account]:::context
>     class Issue critical
>     class Closure critical
> ```
>
> **Diagram B — Lifecycle / flow** (highlight decision points = green, failures = red, money = gold):
> ```mermaid
> graph LR
>     classDef ok fill:#a7f3d0,stroke:#065f46,color:#000
>     classDef risk fill:#fecaca,stroke:#991b1b,color:#000
>     classDef money fill:#fde68a,stroke:#92400e,stroke-width:1px,color:#000
>     Start[Account open]:::money --> A[KYC clear]:::ok
>     A --> B{Beneficiary assigned?}:::risk
>     B -->|no| C[Death detected]:::risk
>     B -->|yes| D[Continue operating]:::ok
>     C --> E[Probate court]:::risk
>     E --> F[Probate approved]:::ok
>     F --> G[Release]:::money
>     G --> H[Transfer to beneficiary]:::ok
>     H --> I[Closure]:::money
>     I --> J[Retention]:::context
>     class C risk
> ```
>
> **Diagram C — The Four Mandatory Decisions (for RRSPs / RIFs)** (highlight critical thresholds = amber, core conditions = green, context = grey):
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     FOM[FOM trigger in system]:::critical --> A[The 4 M choices open]:::core
>     A -->|0 / null| B[Keep receiving]:::ok
>     A -->|1 / TFD| C[Transfer to another plan]:::ok
>     A -->|2 / continue| D[Withdraw only min]:::critical
>     A -->|3 / maintain| E[Continue to 90]:::ok
>     D --> F[Did not opt remainder]:::money
>     class FOM critical
>     class D critical
> ```
>
> ## 5. Variants, options & trade-offs
> | Variant | When to pick | When to avoid | Key trade-off axis |
> |---------|--------------|---------------|--------------------|
> | Stochastic / real-time lifecycle | High-speed derivative-settled accounts with micro-life states | Standard RA/U/C where state changes are annual | Granularity vs complexity |
> | Fixed-date periodic state machine | Annual review and fiscal-year closing, U/C accounts | RRIF/RESP where age and beneficiary events are unpredictable | Predictability vs responsiveness |
> | Event-driven with no periodic scan | Event-only (decease, complaint, transfer) | Accounts with no events for years (orphans) | Efficiency vs orphan detection |
> | Rulebook-based manual gates | Early-stage firm with no automation | Mature custodian with millions of accounts | Cost vs auditability |
>
> ## 6. Relationships to sibling topics
> - **C6-05-account-management:** Account management is the *operational execution* within each lifecycle state; lifecycle is the *governance framework* that dictates which states exist.
> - **C5-02-cash-management:** Cash operations (deposits, withdrawals, dividends) are *state-dependent*: suspended in Death/Probate, allowed in Active.
> - **C6-04-service-levels:** Service levels define the *timing* of settlement operations; the lifecycle engine ensures settlement is attempted only in permitted states.
>
> ## 7. Banking / financial-services context 💳
> Under CSA Rule 3.2 (Client Identification), the lifecycle engine must record the exact date, time, and approver for every state change. For an RPP account where the owner reaches The Four Mandatory Decisions at age 71, KFMS computes the Did Not Opt (DNO) amount—minimum withdrawal as a percentage of the prior year's fair market value. If the advisor advises a full withdrawal (TFD) but KFMS missed the customer's prior-year valuation, the DNO remainder becomes taxable in the following year. In CIBAM, the lifecycle engine gates every RPP withdrawal against the DNO threshold before generating a FR790 report; bypassing this is a compliance breach reportable to FINTRAC.
>
> ## 8. Reference architecture / worked example
> A 68-year-old client with an RPP at CIBAM triggers the FOM state on March 1.
> - **Decision:** Apply the "continue as RPP" (TTF=3) decision; compute DNO for the prior year.
> - **Architecture:** KFMS receives the FOM event, queries the asset registry for last-year valuation, applies the DNO percentage (based on age 69), sets the account to RIF state with minimum-withdrawal enforcement, and schedules a compliance-review reminder in 30 days.
> - **ADR:** We standardized on an event-driven state engine (Kafka + Flink) because periodic polling at age 71 is insufficient; a late-year birthdyy-event must fire the state transition immediately.
> ```mermaid
> graph LR
>     classDef service fill:#bfdbfe,stroke:#1e40af
>     classDef data fill:#fde68a,stroke:#92400e
>     classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5
>     Event[FOM event]:::service --> Transition[State transition]:::service
>     Transition --> Compute[Compute DNO]:::service
>     Compute --> Env[Set RIF / min withdrawal]:::critical
>     Env --> Review[Compliance review]:::service
>     Compute --> Report{Journal}:::boundary
>     class Env critical
> ```
>
> ## 9. Maturity & adoption signals
> - **Adopt when:** All account state transitions are logged immutably, periodic state scans run automatically, and no account can close without a retention-fact record.
> - **Anti-signals (don't adopt yet):** States are tracked only in spreadsheet or agent memory; no automated transition enforcement.
> - **Common failure modes:** (1) Missed DNI (death) due to stale contact records, (2) Defaulting to null (no beneficiary) when the owner explicitly named one, (3) Not handling "keep receiving / TFD / continue / maintain" for RRSPs / RIFs correctly.
>
> ## 10. Common confusions — the "don't mix" list
> | Often confused | Real distinction |
> |----------------|------------------|
> | Account lifecycle vs account management | Lifecycle is the *what* and *when*; management is the *how*. |
> | Beneficiary transfer vs probate | Beneficiary works without probate; probate is required when no beneficiary is named. |
> | DNI (death) vs NPO (did not opt) | DNI is owner death; NPO is the calculation for RPF / RIF withdrawal. |
> | Transfer vs transfer-out | Transfer is internal; transfer-out is to another custodian. |
>
> ## 11. Tools & standards to know
> - **Frameworks/IR-2 / NINE:** CSA Rule 3.2 (Client ID), NI 31-103, OSFI B-13 (operational risk), RPP/RRIF tax rules.
> - **Common tooling:** KFMS for lifecycle engine, Archi for state-machine modeling, Apache Flink for event-driven transitions, Databricks for DNO analytics.
> - **Mandatory reading:** CSA Best Practices Guide (account framework), CRA T4036 (RRSP / RPP / RIF guide).
>
> ## 12. ADR template (ready to fill in)
> ```markdown
> # ADR-14: Event-driven lifecycle state engine
> ## Status
> Accepted
> ## Context
> Periodic age checks at 71 and 90 missed FOM triggers for 120 accounts; DNO violations resulted in $400K tax penalties.
> ## Decision
> Replace periodic polling with Kafka-Flink event-driven state transitions keyed by birthday + account type.
> ## Consequences
> - Positive: FOM triggers processed within medium-event window; DNO enforcement near-instant.
> - Negative: $180K Flink cluster cost; requires idempotency design for holiday-weekend reprocessing.
> ## Alternatives considered
> 1. Extended CRON schedule — rejected; still misses events between runs.
> 2. Pure batch end-of-day — rejected; no real-time enforcement possible.
> ```
>
> ## 13. Practice — apply it
> 1. **Recall:** define in 2 min without notes.
> 2. **Model:** produce a state-transition diagram (UML state machine) for the RA/RRIF lifecycle.
> 3. **ADR:** write a decision doc for automating DNI detection via third-party death-index feeds.
> 4. **Defend:** roleplay explaining to a CRO why a missed probate hold is worse than a missed email.
>
> ## Summary
> The account lifecycle is custody's temporal spine. It is not merely a workflow; it is a state machine that enforces compliance rules imperatively. Every state transition must be traceable, every terminal state must preserve data, and every age-based trigger must fire without fail. The architect who treats lifecycle as "email + folder" will eventually face a regulatory action that the lifecycle was supposed to prevent.
>
> ---
> **Status:** ☐ Not started · ☐ In progress · ✅ Covered
> *Last updated: 2026-09-16*
>
> ---
> **One diagram required. Both brief + detail must exist with ≥1 mermaid each before ✓.**
