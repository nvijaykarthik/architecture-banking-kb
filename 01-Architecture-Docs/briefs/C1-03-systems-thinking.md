# [C1-03] Systems & System-of-Systems Thinking — BRIEF
> **Category:** C1 Foundations · **Difficulty:** ● foundational · **Banking-relevant:** yes
> **One-liner:** A *system* is a boundary-drawn whole with emergent behaviors; a *system of systems* (SoS) is a collection of independently managed systems that interoperate enough to produce collective outcomes — the default state of modern banking.
> **Why an EA cares:** SoS complexity is the *primary* source of integration cost, data inconsistency, and emergent-failure modes in banks.

## Quick definition
A **system** is a set of components that interact to deliver measurable outcomes *when treated as a boundary*. **Systems-of-systems (SoS)** are systems that were built independently (outsourced, acquired, legacy) and are *not* centrally planned — yet must interoperate (e.g., bank + card network + liquidity provider).

## Key ideas / terms
- **Boundary/black box** — what we hide vs expose.
- **Emergence** — the whole does behavior no part has alone.
- **Heterogeneity** — different owners, tech stacks, lifecycles.
- **Interoperability** — the minimum exchange needed for collaboration.
- **Constituent systems** — the independent systems that compose the SoS.
- **Virtual enterprise** — a cross-org SoS.

## The mental model
Before microservices each system was a "monolith" *and* an SoS "inside" the bank. Today a bank is a (collective) SoS of systems *even before* external partners. The EA's job is to define *contracts* (behavioral, not physical) between these so the whole behaves predictably.

## One diagram (mandatory)
```mermaid
graph TD
    classDef bank fill:#fde68a,stroke:#b45309,stroke-width:2px
    classDef external fill:#dbeafe,stroke:#2563eb
    classDef internal fill:#dfe6e9,stroke:#636e72
    BankSurfacing[Bank (virtual enterprise)]:::bank --> DTC[Direct-to-consumer app]:::internal
    BankSurfacing --> API[Open banking API]:::external
    CMA[Customer money account]:::internal --> Settle[Settlement system]:::internal
    Settle --> RTGS[RTGS/CHIPS]:::external
    RTGS --> N/[Liquidity Provider]:::external
    class BankSurfacing critical
```

## When to use / when NOT to use
- ✅ **Use:** mergers, acquisitions, APIs, partnerships, microservices.
- ⚠️ **Avoid:** brand-new unified greenfield from scratch (rare in banking except greenfield refactors).
