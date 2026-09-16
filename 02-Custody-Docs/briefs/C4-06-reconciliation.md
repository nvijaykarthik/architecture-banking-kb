# [C4-06] Reconciliation — BRIEF

> **Category:** Cx — Custody Ops · **Difficulty:** ◑/◑/○ · **Banking-relevant:** 💳

> **One-liner:** The iterative, rules-and-technology process of identifying and resolving differences between custody books, market data, and collateral positions to achieve a single, auditable source of truth.

> **Why an enterprise architect / trainee cares:** Reconciliation failures are the #1 operational-risk event in custody; without a disciplined reconciliation architecture, balance-sheet mismatches, regulatory fines, and settlement-recovery losses compound silently.

## Quick definition

Reconciliation is the systematic comparison of two or more representations of the same economic reality (e.g. a deposit ledger vs an ISIN-level register) to detect drift in security, quantity, currency, or monetary value, followed by root-cause analysis, correction, and governance sign-off.

## Key ideas / terms
- **Golden record:** The authoritative, reconciled view of an instrument position or cash balance that all downstream systems consume after reconciliation.  
- **Reconciliation rule:** A deterministic or probabilistic linkage and comparison criterion (e.g. `isin` + `quantity` + `currency` + `valuation-date`).  
- **Cash versus security reconciliation:** The most frequent daily cut, balancing cash receipts/payments against securities transferred in/out of the deposit.

## The mental model

Reconciliation sits between *transaction/event feeds* (the inputs) and *settlement/payment* (the outputs). It is where data quality becomes operational risk. It relates closely to *data governance* (which defines the rules) and *integration architecture* (which delivers the feeds reliably).

## One diagram (mandatory)

```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    A[Deposit Ledger]::critical --> B{Reconcile?}
    B -->|Match| C[Golden Record]::core
    B -->|Mismatch| D[Drift Team]::critical
    D -->|Root Cause| E[Correct / Escalate]
    E -->|Re-run| B
    F[ISIN Register]::critical --> B
    G[Market Data]:::context --> B
    H[Cash Position]:::context --> B
    D -->|Report| I[Reg / Risk]:::context
```

## When to use / when NOT to use
- ✅ **Use when:** Ever. Daily cash vs security, month-end, year-end, and regulatory-infrastructure cuts are non-negotiable.
- ⚠️ **Avoid when:** Relying solely on manual spreadsheets for >5 counterparties; automation becomes mandatory once scale passes quiet-morning thresholds.

## Banking example

A global custodian reconciles its US-deposit ledger against the DTC monthly holding report and an internal enforcement list each T+1 morning. A mismatch of 40 shares of an ADR appears because a trade-court settlement in London converted the ADR ratio to 1:1 on a 2025-07-15 basis. The rule set missed the corporate-action *effective-date* key; the drift was caught in 4 hours, flagged via SLA alert, and auto-presented to the enforcement team.

## Common confusions (don't mix these up)
- **Reconciliation** vs **settlement:** Reconciliation is *verification*; settlement is the *act of transferring* securities and cash.
- **Book reconciliation** vs **position reconciliation:** Book reconciles quantity/currency; position reconciles valuation and entitlements.
- **Exception-driven** vs **scheduled:** Exception-driven reacts when a match fails; scheduled runs regardless—both are needed because silent drift can hide for days.

## Interview / recall prompt
“Explain reconciliation in 2 minutes without notes.” →
- It is daily verification that custody books match authoritative sources.
- Rules define what matches; mismatches are exceptions.
- Golden record is the reconciled output.
- Time context (T+0, T+1, X-day) and scope (cash vs security) matter.
- Automation + governance > spreadsheets at scale.

## Status
☐ Not started · See detail doc: `details/C4-06-reconciliation.md`

---
**One diagram required. Both brief + detail must exist before ✓.**
