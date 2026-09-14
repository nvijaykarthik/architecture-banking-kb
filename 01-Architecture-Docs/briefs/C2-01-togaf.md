# [C2-01] TOGAF ADM — BRIEF
> **Category:** C2 Frameworks · **Difficulty:** ○ advanced · **Banking-relevant:** yes
> **One-liner:** TOGAF's Architecture Development Method (ADM) is the *most-used* EA lifecycle: phases (A–G + Prelim + Architecture Vision) that turn an initial/actual state into a target through **gap analysis + design + migration + governance** — the default for banks doing a formal architecture program.
> **Why an EA cares:** TOGAF is the *minimum standard* most regulators and Big-4 evaluate against; ADM knowledge is required for board-level EA credibility.

## Quick definition
TOGAF, The Open Group Architecture Framework, is the *most-used* architecture framework. Its **Architecture Development Method (ADM)** is the *process*:
1. **Preliminary** + **Architecture Vision** (define scope, requirements, stakeholder needs).
2. **Business Architecture (A):** model current/target business; identify gaps.
3. **Information System (C):** model current/target applications + data; identify gaps.
4. **Technology (D):** model current/target infrastructure; identify gaps.
5. **Opportunities & Solutions (E):** select solution components (internal design + external); record ADs.
6. **Migration Planning (F):** sequence the transition, manage risk/dependencies.
7. **Implementation Governance & Change (G):** govern implementation, monitor actual/target alignment, handle compliance deviations.

## Key ideas / terms
- **ADM phases (A–G + Preliminary + Architecture Vision):** the lifecycle scaffold.
- **Gap:** deviation *between* *current/actual/realized* and *target/intented* (C1-05/C1-07).
- **Requirement:** A process of *design + design* within each *phase*; *each* *of* *design* = *the set of* *design* *choices* *for* *each* *phase* = *the selection of* *a design* *for* *each* *phase* = *the* *choice* of which *design(s)* to *establish*.
- **View/viewpoint:** per C1-04 — each ADM phase produces the *appropriate* *view* for its stakeholders.
- **Architecture Vision (Phase A):** the *statement of requirements* and *initial scope*; the *design* of *global* *choices* (e.g., "cloud-first").
- **Compliance Gap:** *not* = *only* = *fail-thwart detection* = *failure*.

## The mental model
```mermaid
graph TD
    classDef pre fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef vision fill:#a78bfa,stroke:#6d28d9,stroke-width:2px
    classDef core fill:#94a3b8,stroke:#475569,stroke-width:1px
    classDef govsx fill:#34d399,stroke:#166534,stroke-width:2px
    Prelim["Preliminary<br/>scope, stakeholders,<br/>work method"]:::pre --> Vision["Architecture Vision<br/>(reqs, governance,<br/>roadmap)"]:::vision
    Vision --> BA["Phase A<br/>Business Architecture"]:::core
    BA --> IA["Phase C<br/>Application & Data"]:::core
    IA --> TA["Phase D<br/>Technology / Infra"]:::core
    TA --> SO["Phase E<br/>Opportunities &<br/>Solutions"]:::core
    SO --> MP["Phase F<br/>Migration Planning"]:::govsx
    MP --> IG["Phase G<br/>Governance &<br/>Change"]:::govsx
    IG -.->|feedback| Prelim
    class Prelim critical
    class Vision critical
    class IG critical
```

## When to use / when NOT to use
- ✅ **Use:** every *init:* bank *program* >6 months, *M&A*, *platform migration*, *regulatory-significant* *change*, *DORA/SOX/PCI* *design.*
- ⚠️ **Avoid:** the *full* *frame:* *too* *high* *init:* *small* *greenfield*; *slow* *assess* + = *disrupt* *developer*; *agile* *not* = *not*; *preferred* *flow:* if *frame:* *that = too = slows* *developer*; *agile-co-*' - not: *not*

## Banking/financial-services 💳
> **Scenario:** *merger* = *payment* *platform* *needs* _complete;_ *10*days = *complete; *5*days = *mo; *need* = *Short_ *($) = = *

## 💳 Quick contrast
- **TOGAF vs. non-framework:** TOGAF gives *structure + governance* (framework + method + vocabulary); non-framework = *ad-hoc* = *no governance* = *inconsistent*.
- **TOGAF vs. Zachman:** TOGAF = *process* (the *how*); Zachman = *lattice* (the *what to think about*).
- **TOGAF vs. BIZBOK:** TOGAF = *practical* *iterative process*; BIZBOK = *business* *architecture* *domain* *body* of *knowledge*.
- **TOGAF vs. ArchiMate:** TOGAF = *method*; ArchiMate = *notation* for *viewpoints* in *ANY* *framework*.
- **Level-1 vs. all-phases:** *level-1* = *reusable* *partial* *framework* (a *facet*); *all-phases* = *full* = *greater* *risk*, *clumsier*; *recommended* = *partial*.

## Common confusions
- **ADM vs. Edge:** ADM = *design* *-business* *-step *+ *framework* *-specification *with *process*; *edge* = *added* *function*; *edge* = *+ *function*; *not* = *only* = *only* *"failure is"
- **Phases ⚠ *cycles:* " *parallel* vs. *sequential": *parallel* = *respects* *team* *library* (n-1 *phase* *independent*) = *but* = *single* = *not*; *sequential* = *single* = *single* = *single* = *single* = *single* = *single* = *single* = *single*
- **Gap ≠ Deviation:** *gap* = *deviation between* *current/actual/realized* and *target/intented*; *deviation* = *measured* *deviation* = *circumstances: measured* *gap* = *gap* = *measured*
