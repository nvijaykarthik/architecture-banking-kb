# C8-03 Capability Mapping — DETAIL
> **Category:** Custody/Identity — **Difficulty:** ◔ · **Banking-relevant:** yes 💳
> **Companion brief:** `briefs/C8-03-capability-mapping.md`
>
> > **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.

---

## 1. Precise definition
*Capability mapping* is the disciplined practice of identifying, modeling, and aligning enterprise business capabilities (what the organization must be able to do to deliver value) with their enabling technical capabilities, systems, and resources (how the value is delivered), and making the gaps between desired and current state visible through traceability.

In custody and identity domains, this means mapping outcomes like "hold and transfer securities across jurisdictions within T+1" or "trace every cash position to a legal entity for regulatory reporting" to the reference architecture, the account hierarchy, and the underlying technical stack.

It is not merely a matrix; it is a *governance narrative* that ties strategy to execution.

## 2. Why it exists (the problem it solves)
Capability gaps are the architectural equivalent of technical debt: they quietly degrade the bank's ability to enter new markets, onboard new products, and survive regulatory stress tests. The root cause is *decoupling*: business strategy is set in board meetings, but architecture is built by isolated platform teams who do not always know which strategic objective their work serves.

The historical driver was the Basel III liquidity framework and the subsequent DORA/CSDR demands, which required banks to prove that specific business outcomes (settlement assurance, participant risk management) were supported by specific technical capabilities (real-time risk dashboards, automated collateral margining).

## 3. Core concepts & vocabulary
| Term | Precise meaning |
|------|-----------------|
| Business Capability | What the bank does in the market to deliver value |
| Technical Capability | How a system delivers the business capability |
| Gap | The mismatch between desired and current state |
| BET (Business Enablement Technology) | The technology that enables a business capability |
| EVM (Engineering Velocity Model) | A framework for measuring and improving engineering delivery |
| Architecturally Significant Requirement (ASR) | A requirement with broad impact across multiple systems or capabilities |
| Traceability | The ability to link a business outcome to its enabling systems and back |
| Capability Maturity Model (CMM) | A scale (1–5) measuring how well a capability is defined, managed, measured, controlled, and optimized |

## 4. How it works (architecture / mechanism)

### 4.1 Diagrams

**Diagram A — Core structure** (highlight load-bearing parts = amber, supporting = grey):
 ```mermaid
 graph TD
     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
     A[Business Capability]:::critical --> B[Strategic Outcome]:::core
     A --> C[Technical Capability]:::core
     B --> D[Gap Analysis]:::context
     C --> E[System Assignment]:::context
     D --> F[Prioritized Backlog]:::context
     E --> F
 ```
 ```

**Diagram B — Lifecycle / flow** (highlight decision points = green, failures = red, money = gold):
 ```mermaid
 flowchart LR
     classDef ok fill:#a7f3d0,stroke:#065f46,color:#000
     classDef risk fill:#fecaca,stroke:#991b1b,color:#000
     classDef money fill:#fde68a,stroke:#92400e,stroke-width:1px,color:#000
     A[Define Business Capability]:::ok --> B{Align to Reference Arch?}:::risk
     B -->|Yes| C[Assign Technical Capability]:::ok
     B -->|No| D[Redesign Business Goal]:::risk
     C --> E[Build / Buy / Partner]:::ok
     E --> F{Gap Eliminated?}:::risk
     F -->|Yes| G[Adopt & Govern]:::money
     F -->|No| H[Backlog / De-prioritize]:::money
 ```

### 4.2 The capability mapping cycle
1. **Discover:** Identify business capabilities via strategy documents, product roadmaps, and regulatory requirements.
2. **Decompose:** Break each capability into sub-capabilities and assign to layers (economic, logical, physical, governance).
3. **Distribute:** Assign each sub-capability to a system or team.
4. **Diagnose:** Measure current maturity and identify gaps.
5. **Plan:** Prioritize backlog items to close gaps.
6. **Monitor:** Track progress via EVM or similar.
7. **Evolve:** Re-map annually or after M&A.

## 5. Variants, options & trade-offs

| Variant | When to pick | When to avoid | Key trade-off axis |
|---------|--------------|---------------|--------------------|
| Three-Layer Mapping | Greenfield or pre-GTM | Mature, chaotic org | Rigor vs. speed |
| Four-Layer (Economic/Logical/Physical/Governance) | Banking with heavy compliance | Startup / low-regulation | Accuracy vs. overhead |
| CMM-Based | Enterprise seeking CMMI/ISO alignment | Rapid-change environment | Formalism vs. agility |
| Strategy-to-Product Mapping | Board-level transformation | Incremental improvement | Scope vs. precision |

## 6. Relationships to sibling topics
- **C8-01 Reference Architecture:** Capability mapping *rationalizes* the architecture against business goals; it tells you which parts of the architecture must be hardened.
- **C8-02 Account Hierarchy:** The account hierarchy is the *data substrate* for capabilities like collateral tracing; capability mapping tells you *which* capabilities need which hierarchy features.
- **C8-04 (new):** Data architecture and master data management are *enablers* of capability mapping; without clean master data, the traceability chain breaks.

## 7. Banking / financial-services context 💳
A mid-tier European universal bank is undergoing a large SAPI / major change program. The CRO has mandated "zero days to settle across EEA cash and securities" as the strategic outcome. The capability mapping exercise reveals three gaps:

1. **Business:** No unified cash CDM (currently 4 disjoint cash ledgers).
2. **Technical:** No real-time T2S connectivity (currently batch file-drop).
3. **Governance:** The ARB has no process for prioritizing capability gaps against DORA's ICT resilience metrics.

The bank uses the mapping to justify a €40M investment in a Unified Cash Platform, with a three-year roadmap: (1) unify CDM, (2) deploy real-time engine, (3) establish ARB-led governance. After three years, the bank achieves zero-days cash sweep and passes DORA's first stress test on liquidity resilience.

**Failure consequence:** A peer bank skipped capability mapping and built a "real-time" cash dashboard by bolting together three spreadsheets and a banking-as-a-service API. Six months later, during a market stress event, the dashboard showed reconciled data from the previous close, causing a €12M intraday liquidity miscalculation that attracted a formal notification from the national supervisor.

## 8. Reference architecture / worked example
**Problem:** The peer bank above wants to avoid the failure described in §7.
**Decision:** Adopt a Four-Layer Capability Mapping (economic, logical, physical, governance) with explicit gap tracking.
**ADR AD-45:**
```markdown
# ADR-45: Capability Mapping for Zero-Day Settlement
## Status
Proposed
## Context
CRO mandate: zero-days cash sweep across EEA. Current state: 4 cash ledgers, batch T2S.
## Decision
Adopt Four-Layer mapping with maturity scoring; align gaps to DORA resilience targets; backlog CDM unify as P0.
## Consequences
- Positive: Traceability from strategy to code; defensible to supervisor.
- Negative: 12-month investment before first feature ships; requires C-level sponsorship.
- Risk: If M&A overlaps, capability map must be re-ran for acquired entity.
## Alternatives considered
1. Agile-only roadmapping — rejected; no traceability to DORA.
2. Vendor-prescribed capability model — rejected; local regulatory nuance required.
```

## 9. Maturity & adoption signals
- **Adopt when:** The bank has more than one major product line, a strategy office, and an active board-level transformation agenda.
- **Anti-signals:** A single product with no integration needs, or no formal strategy process.
- **Common failure modes:** Mapping to a 2018 strategy document that no longer exists, treating gaps as "technical debt" rather than strategic blockers, and failing to update the map after M&A.

## 10. Common confusions — the "don't mix" list
| Often confused | Real distinction |
|----------------|------------------|
| Capability Mapping vs. Gap Analysis | Mapping is alignment + traceability; gap analysis is the diagnosis step. |
| Business Capability vs. Technical Capability | Business = what the bank does; Technical = how systems deliver it. |
| Capability Maturity vs. Product Maturity | Capability maturity measures organizational ability; product maturity measures product lifecycle stage. |

## 11. Tools & standards to know
- **Frameworks:** TOGAF 10 (Business Architecture Viewpoint), EVM (Engineering Velocity Model), CMMI, DORA

- **Tools:** Archi, Sparx EA, UNIFY, Planview, Jira, Confluence, Grafana
- **Mandatory reading:** "The Architecture of Open Source Applications" (sSOA patterns), DORA Guidelines (ICT resilience), MITRE ATT&CK / enterprise architecture frameworks

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
2. **Model:** produce a capability map for "Retail Securities Trading" with 5 business capabilities, their technical enablers, and 3 gaps.
3. **ADR:** write a decision doc applying it to the banking example in §7.
4. **Defend:** roleplay explaining to a non-technical CIO why a mapping exercise is worth a 6-month investment.

## Summary
Capability mapping is the bridge between "what the business wants" and "what the bank can actually deliver." In custody and identity, where regulatory stakes are high and integration is complex, it is the discipline that prevents wasted investment, compliance breaches, and strategic drift.

---
**Status:** ☐ Not started · ☐ In progress · ✅ Covered
*Last updated: 2026-09-16*

---
**One diagram required. Both brief + detail must exist with ≥1 mermaid each before ✓.**
