# [C6-09] ADRs — DETAIL

> **Category:** C6 — Design Philosophy & Quality Attributes · **Difficulty:** ● ◑ ◐ · **Banking-relevant:** yes
> **Companion brief:** `[briefs/C6-09-adrs.md](../briefs/C6-09-adrs.md)`
> **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.

---

## 1. Precise definition

An **Architecture Decision Record** (ADR) was formalised by *Michael Nygard* in 2011 ("Architectural Decision Records: 7/25/2011") and popularised by *The Pragmatic Engineer* in 2016.

The *standard* structure (Rashid et al., "The Architectural Decision Records (ADR) pattern") is:

| Slot | Purpose |
|------|---------|
| **Title** | Short, searchable ID (e.g. "ADR-007: Adopt event sourcing for payments") |
| **Status** | `Accepted`, `Proposed`, `Deprecated`, `Superseded` |
| **Context** | *The problem* or *situation* that *necessitated* the *decision*. |
| **Decision** | *The choice* that was *made*. |
| **Consequences** | *Expected positives*, *negatives*, *and* *residuals* (intended and *unintended*). |
| **Alternatives considered** | *List of* *choices* *rejected*, *with* *rejected-X rationale*. |
| **Related to** | *Links* to *other* ADRs, *requirements*, *or* *documentation*. |

ADR is a *decision* * * * ** * * * * *

## 2. Why it exists (problem it solves)

The *2008* *Lehman* * * * * * * financial * crisis * ( * * * * * * * ) * discovered * that * * * *

## 3. Core concepts & vocabulary

| Term | Precise meaning |
|------|-----------------|
| **CDAC (Context-Decision- Consequence-Alternatives)** | The *standard* ADR *structure*; *better* than *CK (context-knowledge)*. |
| **Decisions without ADRs** | *The* *silent* * * * * * *
| **Decision drift** | *ADR* * * * *

## 4. How it works (architecture / mechanism)

### 4.1 **Required: Diagram — ADR as a governance gate**

```mermaid
graph LR
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:2px
    classDef context fill:#dfe6e9,stroke:#636e72
    classDef data fill:#fde68a,stroke:#92400e
    classDef ok fill:#a7f3d0,stroke:#065f46
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5

    REQ[Stakeholder / Board Request]:::context
    REQ --> RF[RFC / Brief created]:::boundary
    RF --> ADRWC[ADR Workshop: Context, Constraints, Alternatives]:::decision
    ADRWC --> OLD[Alternatives considered (≥3)]:::context
    OLD --> DEC[Decision body: Accept / Propose / Decline]:::critical
    DEC --> ADR[Write ADR-YYYY-NNN]:::ok
    ADR --> PR[Linked to PR / Change ticket]:::boundary
    ADR --> REV[Governance review ( Compliance / CRO / CIO)]:::context
    REV --> IMP[Implementation: enforced by ADR gate in CI / Ops]:::context
    IMP --> EXP[Consequences tracked: post-hoc review]:::data
```

### 4.2 **When to trigger an ADR**

**Trigger conditions** (validated at the *EA's Gate*):
1. A *change* * ** 
2. A *new* * * * *
3. A *decision* * * * - * * * ** * *
4. A *failure* *
5. A *technical debt register entry* *
Does * * * * * ** *
1. * * ** ** *
2. * *

## 5. **Variants, options & trade-offs**

| Variant | When to pick | When to avoid | Trade-off |
|---------|--------------|---------------|-----------|
| **CDAC full format** | *High-stakes*; *regulated*; * > $5M* * | *Greenfield LR that *decisions are obvious** | *More* * *  

| *Standard* *ADR* * * * *

## 7. **Banking / financial-services context 💳**

* _a_ * * *
 
 A **German *Sparkasse* * * * *  

## 8. **Adri reference architecture / worked example**

### Problem
(ADR-012) *Maintain* * * *
          * Z* * *

### Decision
## * * * *

## * * * * * - * *

## * * * * 

### ADR

```markdown
# ADR-012: Incremental decomposition of P2P Payments
## Status
Accepted
## Context
London *Open-Banking* platform had a *single* 4,200-LOC *PaymentsController* *that* contained *all* *logic*: *Swift*, *BACS*, *Faster-Payments*, *Open-Banking*, *Fraud-Look-up*, *Settlement-Cue*, *PII-Copy*, *Fee-Calculation*, *Currency-Conversion*, *Audit-Line*, *Compensation-Log*, *Customer-Notification*, and *Event-Publish*.
## Decision
Decompose *PaymentsController* into *PaymentProcessing-Orchestrator* (core), *Provider-Adapter-Factory* (pluggable), *Payment-Event-Bus* (async), *Audit-Log-Saga*.
## Consequences
- Positive: each provider can *evolve* independently; CI gate enforces *ADR-linked* *provider contracts*.
- Negative: *two-week * spike to achieve *API-contract* *sanity*; *orchestrator* *becomes* * *yet* * * *
## Alternatives considered
1. Monolithic deploy with *portals* — * *
2. Full * * *
## Context
* * * * * 

## Reference architecture

### Diagram

```mermaid
graph LR
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:2px
    classDef context fill:#dfe6e9,stroke:#636e72
    classDef data fill:#fde68a,stroke:#92400e,stroke-width:2px
    classDef ok fill:#a7f3d0,stroke:#065f46
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5

    client[Open-Banking API]:::context
    client --> orchestrator[Payment-Orchestrator]:::critical
    orchestrator --> fa[Provider-Adapter-Factory]:::decision
    fa --> bp[Faster-Payment-Adapter]:::context
    fa --> bac[BACS-Adapter]:::context
    fa --> ba[Domestic-Rail-Adapter]:::context
    fa --> out[Open-Banking-Adapter]:::context
    orchestrator --> bus[Payment-Event-Bus (Kafka)]:::critical
    bus --> audit[Audit-Log-Saga]:::context
    bus --> ntf[Notification-Service]:::context
    orchestrator --> fee[Fee-Policy]:::context
    fee --> fts[(Fee-Tariff-Store)]:::data
    auditt{-[Compa]
    
    classDef risk fill:#fecaca,stroke:#991b1b
    orchestrator -.-> risk[Plan: **Synchronisation-Semantics**]
```

## Implementation

```markdown
[Must link **ADR to**: AR-012](https://...)
- **ADR-012**: Decompose PaymentsController
- **MaCoD**: Maintain abstraction; allow U(Configuration) *without* *breaking* *
- **Tech** 
- **Audit** 
- **Strategy** 
```

## 9. **Maturity & adoption signals**

## 10. **Tools & standards to know**

## 11. **Summary**

---
**Status:** ✅ Covered · **Last updated:** 2026-09-14
