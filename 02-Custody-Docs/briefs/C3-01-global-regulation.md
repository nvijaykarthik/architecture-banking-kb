# [C3] Global regulation landscape (US SEC, EU CSDR / EMIR, UK, Asia) — BRIEF

> **Category:** C3 Regulatory, Risk & Compliance · **Difficulty:** ◑ · **Banking-relevant:** yes / 💳

> **One-liner:** Global custody regulation is a patchwork of sovereign securities-laws frameworks (SEC, CSDR/EMIR, FCA, APAC MTF) that govern legal ownership, settlement, reporting, and ICT resilience.

> **Why an enterprise architect / trainee cares:** Every custody design decision — account structure, CSD selection, data model, reconciliation rules — must map to at least one regulator. Neutral design choices (e.g., one global ledger) become expensive liabilities when jurisdictions conflict on legal ownership.

## Quick definition
Custody regulation is the set of cross-border rules that determine who legally owns client assets, how they must be held, where they must be reported, and what resilience standards apply. No two major jurisdictions write the same rule, so the bank's architecture must be parameterized by jurisdiction, not monolithic.

## Key ideas / terms
- **CSDR:** EU law forcing legal ownership in CSD records and T+1 settlement; failure = restricted CSD participation.
- **EMIR:** EU OTC derivatives rule requiring trade reporting to repositories and clearing where mandated.
- **SEC Rule 15c3-3:** US reserve formula — daily collateral coverage must exceed debits.
- **DORA:** EU digital-operational-resilience regulation with incident-reporting and testing mandates.
- **LOU:** Letter of Understanding between custodian and CSD; defines rights, obligations, and account structure.
- **FATF-9:** Wire-transfer and VAS-provider rules applied to custody and crypto.

## The mental model
Treat jurisdiction as the horizontal axis of your custody reference architecture, and function (assets, settlement, reporting) as the vertical axis. A 2×2 matrix of (EU, US, UK, APAC) × (assets, settlement, reporting, resilience) is the minimal model a bank designs for. Ignoring this matrix means designing a "global" solution that works in 70% of jurisdictions and fails audibly in 30%.

## One diagram (mandatory)
```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    A[Client]:::core --> B[Bank (Custodian)]:::critical
    B --> C[CSD (Legal title)]:::critical
    B --> D[CCP (Margin)]:::core
    B --> E[Local CSD (Cross-border)]:::context
    E -.-> C
```

## When to use / when NOT to use
- ✅ **Use when:** Designing a cross-border custody stack, choosing a CSD, or mapping legal-ownership rules.
- ⚠️ **Avoid when:** Treating regulation as a one-time compliance checklist; it is an ongoing architecture driver.

## Banking example
**BNP Paribas Securities Services** maintains separate legal entities in DE, FR, and NL to comply with CSDR legal-ownership rules. A single "European" account structure fails because French courts require legal separation for ERISA-type pension assets, while German rules allow omnibus for retail segregation.

## Common confusions
- **EMIR vs CSDR:** EMIR is OTC derivatives and repo; CSDR is CSDs and settlement discipline.
- **MiFID II vs MiFIR:** MiFID II = markets framework; MiFIR = transaction reporting details.
- **DORA vs NIS2:** DORA = financial-sector ICT resilience; NIS2 = broader EU critical infrastructure.

## Interview / recall prompt
- "Name three regulators that govern custody in your jurisdiction and one rule each."
- "Why can't we run one global ledger for all client assets?"
- "What does CSDR legal-ownership actually mean in a custody platform?"

## Status
☐ Not started · See detail doc: `details/C3-01-global-regulation.md`

---
**One diagram required. Both brief + detail must exist before ✓.**
