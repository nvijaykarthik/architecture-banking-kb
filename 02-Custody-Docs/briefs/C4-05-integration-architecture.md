# [C4-05] Integration Architecture — BRIEF

> **Category:** Cx — Custody Ops · **Difficulty:** ◑/◑/○ · **Banking-relevant:** 💳

> **One-liner:** A structured approach to composing custody-system integrations so that data, funds, and fulfilments move reliably across silos without brittle point-to-point hacks.

> **Why an enterprise architect / trainee cares:** Custody platforms live behind banks, CSDs, and prime brokers; without disciplined integration architecture, every new fund, counterparty, or data feed becomes an unmaintainable tangle of bespoke mappings.

## Quick definition

Integration architecture is the discipline of designing how custody components—segment feeds, transfer instructions, corporate-action events, and settlement records—connect, transform, and flow through standardized interfaces rather than ad-hoc scripts.

## Key ideas / terms
- **Integration topology:** The shape of connections—hub-and-spoke, pub/sub mesh, or orchestrated pipeline—deciding routing, governance, and fault isolation.  
- **Canonical model:** A single, normalized data representation (e.g. ISO 20022 CAMT / CMIX) that all adapters map to and from.  
- **ESB / API gateway:** The runtime bus (or set of gates) that enforces routing, transformation, security, and SLA throttling between custody systems.

## The mental model

It fits as the orchestration layer above individual custody engines (deposits, lending, cash, tax) and below external gatekeepers (ISIN managers, DTC, brokers). Think of it as the "universal adapter" for a bank’s custody silo: every external backend speaks through this layer. Sibling concepts are enterprise-service-bus patterns (which this often implements) and data-contract discipline (which this enforces via the canonical model).

## One diagram (mandatory)

```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    B(Custody System)::critical --> G(Canonical Model)::core
    G --> E[External Senders]:::context
    G --> F[External Receivers]:::context
    E -->|Feed| G
    F -->|Request| G
    C[API Gateway]:::context --> G
    C --> H[Security & SLA]:::context
```

## When to use / when NOT to use
- ✅ **Use when:** Multiple custodians, data vendors, and trade-capture systems must interoperate under strict latency and audit requirements.
- ⚠️ **Avoid when:** A single legacy mainframe dominates with no planned expansion; over-architecture will slow down a simple month-end sweep.

## Banking example

A global custodian builds a "universal reference data hub" that normalises ISIN, price, and corporate-action data from Bloomberg, S&P, and a regional benchmark provider into ISO 20022 CMIX. Every downstream system—deposit, lending, and taxes—consumes from this hub rather than subscribing to n feeds; when the hub restructures a taxonomy, only the mapping layer changes.

## Common confusions (don't mix these up)
- **Integration architecture** vs **system architecture:** The former is about *how the pieces talk to each other*; the latter is about *what those pieces are*.
- **Integration topology** vs **integration pattern:** Topology is the physical/logical shape of the mesh; a pattern is a reusable tactic (e.g. pipe-and-filter) applied within that shape.

## Interview / recall prompt
“Explain integration architecture in 2 minutes without notes.” →
- It is the layer that stitches custody silos together via a canonical model and governed interfaces.
- The topology (hub-and-spoke, pub/sub) determines fault isolation and scaling.
- ISO 20022 is the modern canonical contract.
- Without it, every new counterparty or data feed multiplies point-to-point mappings.
- The goal is interoperability without coupling.

## Status
☐ Not started · See detail doc: `details/C4-05-integration-architecture.md`

---
**One diagram required. Both brief + detail must exist before ✓.**
