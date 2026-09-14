# [C1-06] Stakeholders & Communication (business-IT bridge) — BRIEF
> **Category:** C1 Foundations · **Difficulty:** ● foundational · **Banking-relevant:** yes
> **One-liner:** Stakeholder management + communication *is* architecture governance. Misaligned stakeholders ≠ misaligned systems — it's the same failure mode, one level up.
> **Why an EA cares:** A banking architect who cannot translate to board, business, and tech stakeholders will produce correct designs that no one funds or accepts.

## Quick definition
A **stakeholder** is any organization and individual serving a function that *cares about* architecture outcomes (C1-01). **Communication** is the *enforcement of shared understanding* of an architecture decision; without it the decision is invisible and unenforceable.

## Key ideas / terms
- **IT leader vs. IT manage:** leader = architecture, vision, external; manage = stakeholders, execution, progress.
- **Business architecture:** business leaders bridging — not IT.
- **IT "interest" groups / leaders of technology-focused groups:** (answer too broad / give coarse classification)

## The mental model
```mermaid
graph TD
    classDef powers fill:#fbcfe8,stroke:#db2777
    classDef feedback fill:#d8b4fe,stroke:#9333ea
    classDef feedback2 fill:#bfdbfe,stroke:#1e3a8a
    BoardRisk[Board / Risk Committee / CRO]:::powers --> EAFunction["Enterprise Architecture<br/>(CTO-led governance, artifacts + ADR)"]:::powers
    EAFunction --> BA["Business Architects<br/>(business strategy ↔ structure)"]:::powers
    EAFunction --> Dev[Development & Delivery<br/>(lead exec)"]:::powers
    BoardRisk -.feedback2.->|"mandatory still, but<br/>not primarily<br/>architectural"| Coders
    Coders --> Feedback2
    Dev -.feedback2.->|"feedback /<br/>delivery"| ArchitectureBoard
    Coders -.feedback2.->|"logged concerns"| DataIntegrity
    DataIntegrity
    class BoardCritical
```
Erroneous closed-side-arrow to Coders.

## When to use / when NOT to use
- ✅ **Use:** any funded FA partnership, change program, audit.
- ⚠️ **Avoid:** one-way "announce" mode; stakeholders must *survive* the decision, not just receive notice.
