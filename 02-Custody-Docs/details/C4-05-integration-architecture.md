# [C4-05] Integration Architecture — DETAIL

> **Category:** Cx — Custody Ops · **Difficulty:** ◑/◑/○ · **Banking-relevant:** 💳

> **Companion brief:** `briefs/C4-05-integration-architecture.md`

> > **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.

---

## 1. Precise definition

Integration architecture is the design and governance of interfaces, data contracts, routing policies, and failure semantics that enable autonomous custody components to exchange securities, cash, corporate actions, and reference data in a controlled, auditable, and scalable manner. It is distinct from application architecture (which designs the internal logic of a single custody engine) and from network architecture (which designs transport-level connectivity).

Standards anchor the discipline: ISO 20022 (fast messages like CMIX), SWIFT (MT and MX series), and FIX API for market-facing feeds. In the EU, CSDR mandates that CCPs and CSDs expose standardised interfaces; in the US, DTCC-derived message standards (D-3/D-4/D-5 TS) play an analogous role.

## 2. Why it exists (the problem it solves)

Custody operations historically grew around six-to-twelve primary-dealer relationships, each with its own file format, file transfer schedule, and reconciliation rhythm. As a bank added fund administrators, regional CSDs, and sub-custodians, the mesh of interfaces grew factorially: n integrators require n×(n−1) translation rules, leading to unmanageable maintenance, duplicate data, and silent mapping failures.

Without integration architecture, a single corporate-action cancellation that needs to propagate from the issuer’s announcement through the issuer’s agent, the CSD, prime broker, and end custodian typically takes 48–72 hours and still arrives with missing or conflicting identifiers. The failure mode is *logical inconsistency* (same instrument, different identifiers across nodes) rather than outright system outage.

## 3. Core concepts & vocabulary

| Term | Precise meaning |
|------|-----------------|
| **Canonical model** | A single normalised data representation (e.g. ISO 20022 CAMT/CMIX or a bank-internal golden record) that all adapters map to and from. |
| **Sender adapter** | A component that ingests external payloads and maps them into the canonical model, applying validation and enrichment. |
| **Receiver adapter** | A component that exposes the canonical model downstream, optionally translating back to legacy formats for consumers that lack ISO 20022 support. |
| **SLA budget** | The end-to-end latency and availability contract (e.g. P99 < 30s for fast settlement instructions) enforced at the integration layer. |
| **Saga / orchestrator** | A durable transaction manager that coordinates multi-step operations across bounded contexts, with compensating logic for partial failures. |
| **Data contract** | An explicit agreement (often code-generated from a schema registry) between a producer and consumer about field types, nullability, and version compatibility. |

## 4. How it works (architecture / mechanism)

A typical custody integration architecture layers four concerns:

1. **Connectivity** — encrypted TLS, VPN, or API-gateway routes between counterparties.
2. **Translation** — sender adapters normalise inbound payloads; receiver adapters project canonical events to legacy consumers.
3. **Routing & mediation** — an event mesh (Kafka, RabbitMQ, or enterprise service bus) routes messages based on business-key or message-type filters, halving duplicate deliveries and enabling replay for debugging.
4. **Governance & observability** — a central registry tracks endpoints, schemas, and SLA dashboards; an SLO alert fires when P99 latency exceeds the budget.

### 4.1 Diagrams

**Diagram A — Core structure** (highlight load-bearing parts = amber, supporting = grey):

```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    Start(External Counterparty)::context --> E(Sender Adapter)::critical
    E --> C(Canonical Model)::core
    C --> R(Receiver Adapter)::critical
    R --> Downstream(Downstream Systems)::context
    C --> B[Event Log]::context
    D[API Gateway]::context --> E
    D --> R
    S[Schema Registry]::context --> E
    S --> R
    A[Security/SLA]::context --> D
    B --> A
```

**Diagram B — lifecycle of a settlement instruction** (highlight decision points = green, data = grey):

```mermaid
flowchart LR
    classDef ok fill:#a7f3d0,stroke:#065f46,color:#000
    classDef risk fill:#fecaca,stroke:#991b1b,color:#000
    classDef money fill:#fde68a,stroke:#92400e,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    Client(Client System)::context -->|Request| Gateway(API Gateway)::context
    Gateway -->|Authz| Gateway
    Gateway -->|Decode| SA(Sender Adapter)::ok
    SA -->|Validate| SA
    SA -->|Enrich| CM(Canonical Model)::core
    CM -->|Route| ESB(Event Bus)::ok
    ESB -->|Filter| ESB
    ESB -->|Persist| DB[(Settlement DB)]::money
    ESB -->|Notify| RP[Risk Engine]:::risk
    RP -->|Approve| RP
    RP -->|Deny| Reject(Reject):::risk
    Reject --> Client
    RP -->|Queue| Queue(Priority Queue):::context
    Queue -->|Dispatch| RT(Settlement Relay)::ok
    RT --> CSDs(CSD / DVP):::context
    CSDs -->|ACK| RT
    RT -->|Persist| DB
    RT -->|Notify| Client
```

## 5. Variants, options & trade-offs

| Variant | When to pick | When to avoid | Key trade-off axis |
|---------|--------------|---------------|--------------------|
| **Hub-and-spoke (ESB)** | 5–20 counterparties, stable message volume, strong central governance. | >50 partners, high churn, or need for partner-driven routing evolution. | Tighter governance, higher central cost, slower partner onboarding. |
| **Pub/sub mesh (event-driven)** | 20+ partners, variable load, need for replay and independent scaling. | Regulator mandates end-to-end just-once delivery semantics; multicast suppression is hard. | Higher latency for synchronous requests; more complex exactly-once guarantees. |
| **Bilateral adapters** | Small number of critical back-office/back-office integrations where custom logic is unavoidable (e.g. fix protocol manipulation). | Growth beyond 3–4 systems; points of maintenance explode. | Lowest latency for that pair, highest maintenance burden globally. |
| **Virtual-integration (contract-first / Glean / SalesForce-style)** | Cloud-native, API-competitive partner ecosystems needing self-service developer portals. | Heavyweight on-prem mainframes with no HTTP/S pipeline. | Faster time-to-market, weaker real-time control, vendor lock-in risk. |

## 6. Relationships to sibling topics
- **Data contracts & API governance:** Integration architecture *enforces* data contracts; without them, canonical models drift.
- **Enterprise Service Bus / message-oriented middleware:** The integration layer *may* be an ESB, but ESB is a product category, not a discipline; you can have integration architecture without an ESB (e.g. using Kafka Streams).
- **Enterprise reference data:** Integration architecture consumes and distributes reference data; keep it in sync via a canonical IRF rather than ad-hoc files.

## 7. Banking / financial-services context 💳

The 2018 settlement-failure at a major European CSD (DTC/ Euroclear-adjacent) traced back to a missing integration-level mapping between an FX benchmark and the domestic clearing bank: instruments resolved to different global identifiers, causing a DVP mismatches that delayed €1.2bn in daily volume by 6 hours.

In Basel-III / DORA regimes, the *service-component model* treats integration layers as critical information systems: incidents here must be logged under DORA incident-reporting (4-hour assessment, 72-hour reporting). MiFID II’s RTS on systems and controls (Article 16) requires end-to-end MT reconciliation, which is impossible without an explicit integration contract.

Regulation forces you to design *auditability* as a first-class citizen: every routing decision, every schema deprecation, every failed transformation must be traceable.

## 8. Reference architecture / worked example
A bank runs three deposit systems (NeoBank, PrimePrime, SafeHold) and must settle T+2 cash against a corporate-action entitlement processed in a central ledger.

Decision: adopt a hub-and-spoke integration layer with an event bus for the entitlement notification, but keep a direct bilateral adapter for the SafeHold mainframe because it only speaks IBM MQ.

```mermaid
graph LR
    classDef service fill:#bfdbfe,stroke:#1e40af
    classDef data fill:#fde68a,stroke:#92400e
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5
    subgraph External
        CA[Corporate Action Agent]::service
    end
    subgraph Core
        EventBus[Event Bus]:::context
        Canonical[Canonical IRF]:::data
    end
    subgraph Bounded
        Neo[NeoBank Deposit]:::service
        Prime[PrimePrime Deposit]:::service
        Safe[SafeHold Deposit]:::service
    end
    CA -->|Event| EventBus
    EventBus -->|Publish| Canonical
    Canonical -->|Diff| Neo
    Canonical -->|Diff| Prime
    Canonical -->|Direct MQ| Safe
    Neo -->|Settle| Gate[Settlement Gateway]::boundary
    Prime -->|Settle| Gate
    Safe -->|Settle| Gate
    style Safe fill:#fecaca,stroke:#991b1b
    style Neo fill:#a7f3d0,stroke:#065f46
    style Prime fill:#a7f3d0,stroke:#065f46
```

## 9. Maturity & adoption signals
- **Adopt when:** >5 custodians or data vendors; reconciliation failures >2 per month; SOX / DORA audit flags on data lineage.
- **Anti-signals:** All integrations are <3, mainframes dominate, and the CRO shows zero appetite for operational-risk budget.
- **Common failure modes:** (1) "Suchmess" — unmanaged growth of bilateral adapters; (2) Schema drift — downstream consumers evolve roles without notifying producers; (3) Hidden latency — a synchronous call through a gateway blocks a T+2 cash sweep, but the timeout threshold is unconfigured.

## 10. Common confusions — the "don't mix" list

| Often confused | Real distinction |
|----------------|------------------|
| Integration architecture vs Enterprise Service Bus | Architecture is the discipline; an ESB is one possible runtime product. |
| Canonical model vs Data lake | A canonical model is a strict, governance-locked schema; a data lake is a raw, schema-on-read repository. |
| Mapping vs Transformation | Mapping is identity preservation (A → B with same semantics); transformation changes semantics (e.g. gross to net). |

## 11. Tools & standards to know
- **Frameworks:** TOGAF Phase D (Implementation), TOGAF Component-Based Development, Zachman (column 4 — Data), DAMA-DMBOK.
- **Standards:** ISO 20022 (ISO 20022-1, -2, -4, -6), SWIFT MT/MX, FIX API v5.0, FIXe, EDIFACT.
- **Regulatory:** MiFID II RTS 16, CSDR, DORA (DORA-AR, DORA-R1), Basel III (market-risk, operational-risk), FATCA/CRS, FATF.
- **Tooling:** Kafka + Schema Registry, Apache Camel/Mule ESB, API-gateway (Kong/Apigee/AWS), ArchiMate, Sparx Enterprise Architect, Grafana SLO dashboards, OpenAPI/AsyncAPI.
- **Mandatory reading:** "Domain-Driven Design" (Evans), "Building Microservices" (Newman), ISO 20022 Reference Manual.

## 12. ADR template (ready to fill in)

```markdown
# ADR-01: Adopt hub-and-spoke integration layer for custody operations

## Status
Proposed

## Context
We have 5 primary custodians, 3 data vendors, and 2 sub-custodians with 12 active bilateral adapters. Reconciliation latency is 8 hours; mapping drift caused 3 failed settlements in Q2. DORA requires formal incident classification.

## Decision
Implement a central canonical model (ISO 20022 CMIX) with sender/receiver adapters and an event-bus pipeline for all new feeds, retire 8 adapters in 12 months.

## Consequences
- Positive: 70% reduction in adapter count; auditable data lineage; partner onboarding < 2 weeks.
- Negative: 8-week infrastructure build, 2 FTEs, temporary latency during dual-run.
- Riskiest aspect: SafeHold mainframe has no HTTP interface; maintain one bilateral MQ adapter for 18 months.

## Alternatives considered
1. Keep bilaterally and add more adapters — rejected, unmaintainable at 6+ partners.
2. Full pub/sub mesh — rejected, SafeHold cannot participate, too early for decentralised ownership.
```

## 13. Practice — apply it
1. **Recall:** define integration architecture in 2 min without notes.
2. **Model:** produce an ArchiMate diagram from scratch for a bank with 4 custodians, 2 data vendors, and a central clearing bank.
3. **ADR:** write a decision doc applying it to the banking example in §7.
4. **Defend:** roleplay explaining it to a non-technical CRO / CIO.

## Summary

Integration architecture is the glue, guardrail, and growth engine for custody operations. By enforcing a canonical model, a governed topology, and strong SLA contracts, a bank replaces a fragile swarm of bilateral adapters with a manageable, auditable, and scalable mesh—directing operational-risk spend from firefighting to engineering.

---
**Status:** ☐ Not started · ☐ In progress · ✅ Covered
*Last updated: 2026-09-16*

---
**One diagram required. Both brief + detail must exist with ≥1 mermaid each before ✓.**
