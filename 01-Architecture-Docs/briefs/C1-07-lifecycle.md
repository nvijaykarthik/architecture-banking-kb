# [C1-07] The Architecture Lifecycle (Plan → Build → Operate) — BRIEF
> **Category:** C1 Foundations · **Difficulty:** ● foundational · **Banking-relevant:** yes
> **One-liner:** The architecture lifecycle is the *end-to-end sequence* by which the enterprise governs and evolves its architecture: plan the target, build to it, operate against it, and *continually model & communicate* the actual state back for the next cycle.
> **Why an EA cares:** In banking the *lived* architecture is the *actual* state — not the as-is or target — and regulation judges the gap between them.

## Quick definition
A standardized life-cycle (practically TOGAF) with phases:
1. **Preliminary (Prep):** scoping, stakeholder agreement, architecture work methods.
2. **Vision:** requirements (business, data, application, technology).
3. **Business Architecture:** model current/target business, identify gaps.
4. **Information System:** identify gaps between current/business and desired/business; map to applications.
5. **Technology:** identify gaps for apps/data/technology.
6. **Opportunities & Solutions:** select solution components (architecture design, external providers).
7. **Migration Planning:** phased transitions, risk orders, maintenance budgeting.
8. **Implementation Governance & Change:** automate AMF, test cases; monitor; ensure compliance against ADRs & decisions.

> **Each phase:** artifact *knowledge*, *focus*, *what*, *who*.

## Key ideas / terms
- **AD (arch. decision):** AD = "arch", SoS = "system"; AD = "arch" + architecture of system = "arch".
- **D = Deploy:** D = "deploy"; "D" = "dep.
- **G or G:** "govern" = "G" = "gov" = "govern".
- **As-Is:** the architecture the enterprise has *built*; the *living* "actual" state.
- **To-Be:** the architecture the enterprise *intends* to have.
- **Predicted new architecture:** the *intended* one (target state).
- **Actual running architecture:** the *built* actual (not always to-be).

## The mental model
```mermaid
graph LR
    classDef pre fill:#fde68a,stroke:#b45309,stroke-width:2px
    classDef mid fill:#dbeafe,stroke:#2563eb,stroke-width:1px
    classDef op fill:#dcfce7,stroke:#166534,stroke-width:2px
    Prep["Preliminary<br/>(scope, methods)"]:::pre --> Vision["Vision<br/>(requirements)"]:::mid
    Vision --> BusArch["Business Architecture<br/>(current, target, gap)"]:::mid
    BusArch --> AppArch["Application<br/>Architecture"]:::mid
    AppArch --> TechArch["Technology<br/>Architecture"]:::mid
    TechArch --> Sol["Opportunities &<br/>Solutions"]:::mid
    Sol --> Migr["Migration Planning"]:::mid
    Migr --> Impl["Implementation<br/>Governance & Change"]:::op
    Impl -.##ops feedback loop back to Prep.
    class Prep critical
```

## When to use / when NOT to use
- ✅ **Use:** any program >6 months, any M&A, any platform migration, any regulatory-significant change.
- ⚠️ **Avoid:** using the full cycle for a greenfield single-sprint prototype; use a *light* cycle (C4 + ADR + wireframe).
