# C8-02 Account Hierarchy — DETAIL
> **Category:** Custody/Identity — **Difficulty:** ◑ · **Banking-relevant:** yes 💳
> **Companion brief:** `briefs/C8-02-account-hierarchy.md`
>
> > **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.

---

## 1. Precise definition
An *account hierarchy* is a directed tree (or forest) of custody and identity accounts in which each node represents a legal or contractual entity that holds rights over financial instruments, and each directed edge represents a parent-child or custodial relationship. The hierarchy must encode:

- **Legal ownership** (who holds title)
- **Economic rights** (who receives dividends, votes, or collateral)
- **Agency relationships** (who acts on behalf of whom)
- **Regulatory jurisdiction** (which legal framework applies at each node)
- **Temporal validity** (start/end dates for each relationship)

It is an *instance* of the logical layer specified by the reference architecture (C8-01), meaning multiple hierarchies can exist simultaneously, but they must all conform to the same CDM.

## 2. Why it exists (the problem it solves)
Without a formal account hierarchy, a bank cannot answer the simplest question: "Who owns these 50,000 shares of Stock X?" The hierarchy solves *attribution*: it maps every instrument position back to a legal entity so that:

- **Margin allocation** can be calculated per fund or per counterparty.
- **Regulatory reporting** (CSDR, SFTR, Form 13F) can be produced by walking the tree upward.
- **Tax and withholding** can be applied at the correct legal jurisdiction.
- **Proxy voting** can be cascaded from the root (legal entity) to the leaf (instrument) through the Indirect Holder chain.

The historical failure was the 2008 crisis: many banks discovered that their "held" positions were actually held at prime brokers, with repo-style arrangements that were not reflected in their internal hierarchies, leading to massive collateral misallocation.

## 3. Core concepts & vocabulary
| Term | Precise meaning |
|------|-----------------|
| Legal Entity | The corporate or natural person that holds legal title to an account |
| Custody Account | The account at a sub-custodian where securities or cash are held |
| Sub-account / Indirect Holder | An account nested under a parent, representing a segment or investor class |
| Proxy | The mechanism through which indirect holders exercise rights without direct sub-custodian access |
| Chain of Title | The audit trail from the legal entity through every custodial layer to the instrument |
| Beneficial Owner | The person(s) who ultimately own the rights, even if legal title is held by a nominee |
| Omnibus Account | A single custody account representing multiple beneficial owners |
| DVP Settlement | Delivery-versus-payment settlement requires both sides of an account hierarchy to agree |
| GLEIS / ISO 20022 | Messaging standards for account identifiers across jurisdictions |

## 4. How it works (architecture / mechanism)

### 4.1 Diagrams

**Diagram A — Core structure** (highlight load-bearing parts = amber, supporting = grey):
 ```mermaid
 graph TD
     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
     Legal[Legal Entity]:::critical --> Corp[Corporate]:::core
     Legal --> Indiv[Individual]:::core
     Corp --> CustAcc[Custody Account]:::context
     CustAcc --> Indirect[Indirect Holder]:::context
     Indirect --> SubAcc[Sub-account]:::context
     SubAcc --> Holding[Holding]:::core
     Indiv --> Retail[Retail Account]:::context
 ```
 ```

**Diagram B — Lifecycle / flow** (highlight decision points = green, failures = red, money = gold):
 ```mermaid
 flowchart LR
     classDef ok fill:#a7f3d0,stroke:#065f46,color:#000
     classDef risk fill:#fecaca,stroke:#991b1b,color:#000
     classDef money fill:#fde68a,stroke:#92400e,stroke-width:1px,color:#000
     A[Onboard Legal Entity]:::ok --> B{Link to LEM?}:::risk
     B -->|Yes| C[Create Custody Account]:::ok
     B -->|No| D[Block Onboard]:::risk
     C --> E[Sub-Account Allocation]:::ok
     E --> F[Binding Time Mapping]:::money
     E --> G{Reconcile with Sub-Cust}]
 ```

### 4.2 Structural requirements
A robust hierarchy must support:
1. **Multi-parenting:** A legal entity may be nested under multiple corporate structures (e.g., a holding company with subsidiaries).
2. **Temporal versioning:** When a legal entity changes its jurisdictional status, the hierarchy versioning must allow rollback for audit.
3. **Indirect Holder chains:** The path from root to leaf can span 3–5 custodial layers (legal entity → prime broker → sub-custodian → fund administrator → investment manager), each adding latency and reconciliation risk.
4. **Omnium to aggregate reconciliation:** A single sub-custodian omnibus account must reconcile against the sum of all underlying beneficial-owner allocations.

## 5. Variants, options & trade-offs

| Variant | When to pick | When to avoid | Key trade-off axis |
|---------|--------------|---------------|--------------------|
| Centralized Hierarchy (single LEM) | Banks with 1000+ legal entities, high regulatory density | Real-time distributed trading with millisecond needs | Consistency vs. latency |
| Federated Hierarchy (distributed LEMs) | LPs and hedge funds with proprietary legal structures | Regulators requiring a single source of truth | Autonomy vs. reportability |
| Chain-of-Title-First Design | SEC-regulated U.S. broker-dealers | EU UCITS funds with nominee structures | Auditability vs. flexibility |
| ISO 20022-Native Design | Cross-border cash/securities settlement | Legacy SWIFT MT systems with no 20022 path | Standardization vs. integration cost |

## 6. Relationships to sibling topics
- **C8-01 Reference Architecture:** The hierarchy is the *instance* of the logical layer; it cannot be designed without the CDM.
- **C8-03 Capability Mapping:** Capability maps tell you *which* hierarchy features (e.g., multi-parenting, temporal versioning) a business capability requires.
- **C8-05 (new):** Collateral tracing is a *consumer* of the account hierarchy; it reads the tree to aggregate margin and pledge eligibility.

## 7. Banking / financial-services context 💳
A U.S. asset manager under SEC custody rules (Rule 17f-5) must maintain an account hierarchy where every institutional portfolio is a sub-account of a legal entity, and each sub-account maps to a sub-custodian account. The hierarchy is tested daily via SAP / SIX FedTrade reconciliation.

**Regulatory tie-in:** CSDR requires that settlement instructions reference the correct account identifier (ISIN + BIC). If the hierarchy is wrong (e.g., a legal entity is mis-coded as a sub-account), the settlement fails, and the bank is liable for reverse-charge penalties.

**Failure consequence:** In 2021 a prime broker discovered that 12% of its sub-account allocations were orphaned because the Legal Entity Master (LEM) had been updated without propagating the change to the hierarchy. The bank spent three weeks and $2.3M to rebuild the traceable chain of title for SEC Form PF reporting.

## 8. Reference architecture / worked example
**Problem:** The asset manager wants to onboard a new feeder fund for a PE strategy.
**Decision:** Extend the existing hierarchy by adding a "Feeder" node type between Legal Entity and Sub-account, with a new attribute `strategy_code` for PE-specific reporting (carried interest, hurdle rate).
**ADR AD-24:**
```markdown
# ADR-24: Feeder Fund Hierarchy Extension
## Status
Accepted
## Context
PE feeder funds require strategy-specific reporting that standard Sub-account nodes do not capture.
## Decision
Add Feeder node type with strategy_code and hurdle_rate attributes; map to existing Indirect Holder chain.
## Consequences
- Positive: PE performance reporting automated; audit trail clearer.
- Negative: New LEM update pipeline required; 3-month integration.
- Risk: Sponsor reclassification if a feeder is closed early.
## Alternatives considered
1. Use Sub-account with custom tag — rejected; breaks CDM normalization.
2. Standalone PE ledger — rejected; fragment reporting.
```

## 9. Maturity & adoption signals
- **Adopt when:** The bank has multiple funds, a legal entity master, and regular reconciliation cycles.
- **Anti-signals:** Single-product shop with no sub-accounts, or a pure investment bank with no custody function.
- **Common failure modes:** Orphaned nodes (links disconnected from the root), stale LEI mappings, and failure to reconcile sub-custodian statements against the hierarchy.

## 10. Common confusions — the "don't mix" list
| Often confused | Real distinction |
|----------------|------------------|
| Account Hierarchy vs. Organizational Hierarchy | The former is about custody and legal ownership; the latter is about corporate management. |
| Legal Owner vs. Beneficial Owner | Legal owner holds title on paper; beneficial owner enjoys the economic rights. |
| Direct vs. Indirect Holder | Direct holder has a relationship with the sub-custodian; indirect holder does not. |

## 11. Tools & standards to know
- **Standards:** ISO 20022 (pain.001, pain.007), CSDR, SEC Rule 17f-5 (U.S.), UCITS Directive, MiFID II
- **Tools:** SAP/SIX for cash and securities, Clearstream, Euroclear, Bloomberg AIM, Protégé for ontology modeling, draw.io
- **Mandatory reading:** "CME Group Clearing Handbook" (on account hierarchies for derivatives), CSDR RTS on account identification

## 12. ADR template (ready to fill in)
```markdown
# ADR-{{NN}}: {{decision}}
## Status
Accepted | Proposed | Deprecated
## Context
{{...}}
## Decision
{{...}}
## Consequences
- Positive ...
- Negative ...
- ...
## Alternatives considered
1. ...
2. ...
```

## 13. Practice — apply it
1. **Recall:** define in 2 min without notes.
2. **Model:** produce an ArchiMate diagram showing a multi-level indirect holder chain with a failing reconciliation.
3. **ADR:** write a decision doc for adding a "Feeder" node type as in §8.
4. **Defend:** roleplay explaining to a CIO why a centralized hierarchy is necessary despite integration latency.

## Summary
The account hierarchy is the bank's map of ownership. Without it, margin is mis-allocated, taxes are wrong, and regulators cannot be answered. With it, every position is traceable, every right is allocable, and every settlement is defensible.

---
**Status:** ☐ Not started · ☐ In progress · ✅ Covered
*Last updated: 2026-09-16*

---
**One diagram required. Both brief + detail must exist with ≥1 mermaid each before ✓.**
