# [C4-07] Straight-Through Processing — BRIEF

> **Category:** Cx — Custody Ops · **Difficulty:** ◑/◑/○ · **Banking-relevant:** 💳

> **One-liner:** The fully automated, exception-free end-to-end flow of a custody transaction from trade capture to settlement or notification, with no human intervention required for routine processing.

> **Why an enterprise architect / trainee cares:** STP is the gold standard of operational efficiency in custody; achieving it reduces error rates, settlement latency, and regulatory capital charges, but only when upstream data quality and interface reliability are proven.

## Quick definition

Straight-through processing (STP) is an automated workflow in which a custody transaction—typically a securities transfer, cash movement, corporate-action processing, or standing instruction—flows from initiation to final settlement (or to a controlled escalation point) without manual handling at any routine stage.

## Key ideas / terms
- **Automated suppression:** The automatic clearing of a message/instruction when all validation checks pass, without human review or ticket creation.  
- **Inhibition point:** A control gate where an exception forces human review, which STP avoids for routine cases.  
- **Data quality gate:** The prerequisite that inbound and outbound data meet schema, completeness, and business-rule thresholds before STP can be safely enabled.

## The mental model

STP sits at the intersection of *integration architecture* (which delivers feeds), *reconciliation* (which verifies them), and *workflow automation* (which orchestrates steps). It is the desired state: if your pipeline is not STP-grade, you are holding manual batch latency and error rates that eat into T+1 or T+2 settlement windows.

## One diagram (mandatory)

```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    A[Trade Capture]:::context -->|Valid| B{STP Gate}::critical
    B -->|Pass| C[Pre-Settle]:::core
    B -->|Fail| D[Inhibition Point]:::critical
    D -->|Manual Review| E[Ops Queue]:::context
    E -->|Back-in| C
    C -->|Settle| F[Settlement]:::core
    C -->|Notify| G[Client Notification]:::context
    style B fill:#a7f3d0,stroke:#065f46
    style D fill:#fecaca,stroke:#991b1b
```

## When to use / when NOT to use
- ✅ **Use when:** High volume, low exception rate, proven data quality, and partner systems have stable interfaces and SLAs.
- ⚠️ **Avoid when:** Partners are still on paper, SWIFT MT without MX, or legacy mainframes with no batch-to-external validation; premature STP creates hidden exceptions.

## Banking example

A global fund administrator processes a £200m bond redemption. The trade is captured in the fund-accounting system, mapped via the integration layer to ISO 20022, validated against holdings, and auto-presented to the settlement engine. The CSD confirms settlement by 14:00 CET; the cash is freed for reinvestment by 15:00, and the client receives a confirmation without a single operations ticket.

## Common confusions (don't mix these up)
- **Straight-through processing** vs **high automation:** STP implies *fully automated no-touch* for the entire flow (or with pre-defined, automated inhibition); high automation still involves manual gates.
- **End-to-end STP** vs **interactive STP:** End-to-end is one-way flow; interactive STP requires the client to confirm before settlement (e.g. a mobile-app order confirmation).
- **STP vs auto-reconciliation:** Auto-reconciliation is a *component* of STP; STP is the full end-to-end workflow.

## Interview / recall prompt
“Explain straight-through processing in 2 minutes without notes.” →
- It is end-to-end automation of a custody transaction with zero manual intervention.
- Requires data quality gates and stable partner interfaces.
- Inhibition points exist only for true exceptions.
- Goal: T+0 or T+1 settlement with full auditability, not speed alone.
- The obligation is runtime reliability, not just code.

## Status
☐ Not started · See detail doc: `details/C4-07-straight-through-processing.md`

---
**One diagram required. Both brief + detail must exist before ✓.**
