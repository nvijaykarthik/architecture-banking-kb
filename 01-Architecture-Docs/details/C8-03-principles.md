# [C8-03] Principles — DETAIL
> **Category:** C8 — Reference Architecture, Standards & Principles · **Difficulty:** ● · **Banking-relevant:** yes
>
> **Companion brief:** `[briefs/C8-03-principles.md](../briefs/C8-03-principles.md)`
>
> > **Target reader:** enterprise architect negotiating a trade-off with a product lead and needs to cite the principle and its hierarchy.

---

## 1. Precise definition
An **architecture principle** is a concise, non-negotiable statement of intent—rooted in business strategy, value architecture, and quality attributes—that governs architectural decisions across the enterprise portfolio. It is:
- **Imperative:** stated as a command (“data is owned by business domains”).
- **Concise:** short enough to occupy a single slide without footnotes.
- **Testable:** a developer can answer yes/no to “Does this choice violate principle P7?”
- **Hierarchy-ordered:** strategic principles cascade into design principles, which cascade into implementation guidelines.

TOGAF 10 defines architectural principles as “a small number of rules, guidelines, or assumptions that guide the design.” The key addition for banking is *testability* against regulatory and quality-attribute risk.

## 2. Why it exists (problem it solves)
Before principles, a retail-digital squad built a p2p payment app with customer data cached in local Redis clusters to meet a six-month deadline. Two years later, during a DORA stress test, the tester discovered that the cache was not replicated, not encrypted at rest, and not discoverable in the service catalog. The bank had no principle stating data resilience or discoverability as a non-negotiable; each team chose its own “fastest” approach. The remediation cost €900K and delayed a PSD2-compliance release.

## 3. Core concepts & vocabulary
| Term | Precise meaning |
|------|-----------------|
| **Architectural principle** | A concise, testable, non-negotiable rule about how the architecture must behave. |
| **Driving principle** | Points toward current industry or competitive goals (e.g., “real-time fraud detection”). |
| **Inhibiting principle** | Constrains future architecture (e.g., “on-premise maintenance windows after 2028”). |
| **Buffer principle** | Explicit, time-limited exception to a principle (e.g., “legacy system can bypass zero-trust for 180 days”). |
| **Principle hierarchy** | Strategy → value-architecture → design principles → implementation guidelines. |
| **Principle catalog** | A living, version-controlled registry of all active principles with owners, status, and status (active / deprecated). |
| **Compliance proof point** | A specific business decision or system configuration that demonstrates the principle is satisfied. |

## 4. How it works (architecture / mechanism)
Principles are *enforced* through **three mechanisms**:
1. **Design-review gate:** every architecture review checks the proposal against the principle catalog; a violation requires a buffer-principle ADR.
2. **ADR check-in:** ADR templates include a mandatory field “Principle compliance” with a yes/no/buffer status.
3. **Automated scan:** a policy-as-code scanner can detect principle drift at commit time (e.g., a Terraform module that creates a non-domain-owned database triggers a P-14 violation).

A *buffer principle* is not a loophole; it is a *dated, compensated, reviewed* exception. Every buffer principle carries an expiration and a compensating control.

### 4.1 Diagrams
**Diagram A — Principle hierarchy cascade (strategic down to implementation):**
```mermaid
graph TB
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
    classDef context fill:#dfe6e9,stroke:#636e72,stroke-width:1px
    
    STR[Strategy<br/>Board]:::context
    VAT[Value Architecture<br/>(Value Stream Mapping)]:::context
    
    STR -->|declares| P1["P1: Real-time fraud<br/>detection mandatory"]:::critical
    STR -->|declares| P2["P2: Data owned<br/>by business domain"]:::critical
    
    VAT -->|materializes| D1["D1: Customer 360<br/>via event sourcing"]:::decision
    D1 -->|requires| P2
    
    D1 -->|enforces| I1["I1: Kafka topic<br/>per domain event"]:::context
    
    classDef critical critical
    class P1,P2 critical
    class D1 context
    class I1 context
```

**Diagram B — ADR principle-compliance gate (highlighting ok = light-green, risk = red, critical = amber):**
```mermaid
flowchart LR
    classDef ok fill:#a7f3d0,stroke:#065f46
    classDef risk fill:#fecaca,stroke:#991b1b
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    
    Team[Product Team<br/>Proposes Change]:::critical
    Check{{Check against<br/>Principle Catalog}}:::risk
    Buffer{{Buffer<br/>Required?}:::decision
    ARRB[Architecture Review<br/>Board]:::ok
    
    Team --> Check
    Check -->|no violation| ARRB
    Check -->|violation: no buffer| Team[Team must<br/>re-design or<br/>request buffer]:::risk
    Buffer -->|yes: approved<br/>with comp. control| ARRB
    Buffer -->|no: reject| Team
```

## 5. Variants, options & trade-offs
| Variant | When to pick | When to avoid | Key trade-off axis |
|---------|--------------|---------------|--------------------|
| **Strict non-negotiable** | Security, regulatory, data-privacy | Early-stage innovation, research | Control vs. agility |
| **Non-negotiable with buffer exception** | Mature regulation landscape | Greenfield M&A integration where speed is essential | Governance overhead vs. survivability |
| **Heuristic principle (soft)** | Experimental micro-product with isolated load | Production payments system, settlement | Innovation vs. auditability |
| **Finding/rule-of-thumb** | Ad-hoc pair-programming or team learning | Enterprise-wide rollout, cross-team dependencies | Shadow vs. alignment |

## 6. Relationships to sibling topics
- **Reference architecture:** reference architecture *implements* principles; principles *shape* the reference architecture (e.g., “zero-trust” shapes the identity context in the foundational layer).
- **Standards:** principles often *derive* from standards; the standard is the external rule, the principle is the internal translation (e.g., DORA resilience requirement → principle P11: “no single point of failure in payment routing”).
- **Vendor strategy:** vendor contracts must be principle-compliant; non-compliant vendors are rejected or require a buffer ADR.

## 7. Banking / financial-services context 💳
Under BCBS 239, a bank’s principles must include “data must be complete, accurate, timely, and unique.” A principle like “single source of truth for customer data” forces the central data platform team to own the customer golden record, while product teams consume it via APIs. During a Basel-III reporting re-platform, the lending team wanted to maintain a local customer table for speed. The principle P7: “customer data must be read-only from the golden record” blocked the design; the team instead used a materialized view with row-level security, satisfying both P7 and the performance goal.

## 8. Reference architecture / worked example
**Problem:** The bank’s digital transformation program had 12 product lines, each choosing its own customer-profile storage strategy: SQL in UK, NoSQL in France, graph in Canada. This produced 3 customer-360s, no unified AML score, and a DORA stress-test failure due to undiscoverable data stores.

**Decision:** Publish five strategic principles:
1. P1: Real-time fraud detection is mandatory for all digital channels.
2. P2: Customer data is owned by the domain and must be accessed via API.
3. P3: No new on-premise data store after 2027.
4. P4: Zero-trust network everywhere (mTLS, least-privilege).
5. P5: API first for any new capability.

**ADR:**
```markdown
# ADR-311: P2 Customer-Data Ownership Principle
## Status
Accepted
## Context
12 product lines, 3 customer 360 views, DORA 2024 stress test failed, BaFin audit flagged data-lineage gaps.
## Decision
- All customer data must reside in the Customer-Golden-Record platform.
- Product teams may read via subscribed APIs; no write or storage outside the platform.
- Legacy batch feeds must use streaming CDC with schema registry.
## Consequences
- Positive: single customer 360, auditable lineage, DORA recoverability.
- Negative: product teams lose 4-week local-SQL migration; data engineering demand spikes Q3.
- Negative: EU-GDPR DSAR response time drops from 48h to 8h.
## Alternatives considered
1. Allow each domain to keep its own copy with periodic sync. → Rejected: violates DORA and BCBS 239.
2. Ban all local storage including read replicas. → Rejected: unacceptable for UK core-banking latency requirements.
```

## 9. Maturity & adoption signals
- **Adopt when:** you are federating agile squads, entering regulated markets, or experiencing consistent compliance failures.
- **Anti-signals (don't adopt yet):** fewer than 3 teams, no cross-domain data sharing, and a single CTO.
- **Common failure modes:** (1) too many principles (more than 10 active, they become ignored); (2) vague principles (“be secure”); (3) no buffer exception process, causing teams to work around principles in secret.

## 10. Common confusions — the "don't mix" list
| Often confused | Real distinction |
|----------------|------------------|
| **Principle** vs **Pattern** | Principle = why; pattern = how. |
| **Principle** vs **Standard** | Principle = internal intent; standard = externally prescribed rule. |
| **Guideline** vs **Principle** | Guideline is advisory; principle is non-negotiable and testable. |
| **Driving vs. Inhibiting principle** | Driving points toward a goal; inhibiting constrains the future. |
| **Buffer principle vs. exception** | Buffer is dated, compensated, reviewed; an exception is ad-hoc and often undocumented. |

## 11. Tools & standards to know
- **Standards/Frameworks:** TOGAF (Principle and Governance), ArchiMate (Stakeholder, Value), Agile Architecture (AIA), BCBS 239, DORA.
- **Common tooling:** Confluence (principle catalog, ADR wiki), Jira Align (principle health dashboards), Archi (archimate modeling), ADRiffic (ADR management), SAFe PI planning (principle reviews).
- **Mandatory reading:** “Software Architecture: Fundamentals, Theory, and Practice” by Mark Richard & Pedro Pereira; “The Architecture of Open Source Applications.”

## 12. ADR template (ready to fill in)
```markdown
# ADR-XXX: <decision>
## Status
Accepted | Proposed | Deprecated

## Context
...

## Decision
...

## Consequences
- Positive ...
- Negative ...
- ...

## Alternatives considered
1. ...
2. ...
```

## 13. Practice — apply it
1. **Recall:** define a principle in 2 minutes without notes, using one banking scenario.
2. **Model:** draw a principle hierarchy for a 5-principle set (security, data, cloud, API, resilience).
3. **ADR:** write an ADR defending a product-team decision that *violates* a principle and propose a buffer with compensating controls.
4. **Defend:** role-play a board meeting where a CRO asks why “customer data” is restricted to the central platform despite product-line objections.

## 14. Summary (1 paragraph)
Principles are the constitutional clauses of a bank’s architecture: short, imperative, testable, and hierarchical. They stop feature teams from sub-optimizing for speed at the expense of DORA compliance, BCBS 239 data completeness, or zero-trust security. An architect who writes principles that are vague, numerous, or uncleared by the board creates a culture of silent workarounds—far more dangerous than any single missed deadline.
