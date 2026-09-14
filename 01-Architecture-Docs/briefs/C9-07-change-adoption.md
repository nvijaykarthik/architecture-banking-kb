# [C9-07] Change & Adoption — BRIEF
> **Category:** C9 — Governance, Management & Strategy · **Difficulty:** ●● ●● · **Banking-relevant:** yes
> **One-liner:** Change and adoption in enterprise architecture is the discipline of planning, resourcing, and tracking the human and organizational transition required to realize the value of an architectural vision, not just the technical deliverable.
> **Why an EA cares:** In banking, a perfectly designed architecture fails if the business does not adopt it; change management transforms architectural blueprints into usable banking services.

## Quick definition
Change and adoption is the structured process of preparing, supporting, and transitioning the organization into new ways of working enabled by architectural decisions. It treats technology as a means, and the people, process, and culture shift as the end.

## Key ideas / terms
- **Demand Management:** Prioritizing and sequencing architectural initiatives based on business readiness, risk, and value.
- **Transition Architecture:** The temporary state between the current architecture and the target architecture, managed as a portfolio of transitional releases.
- **ADKAR Model:** Awareness, Desire, Knowledge, Ability, Reinforcement—a structured framework for individual and organizational change.
- **Value Realization:** Measuring whether the architectural change actually delivered the promised business benefit, not just whether it shipped on time.

## The mental model
Architecture is a promise; adoption is the fulfillment. Many banking transformation programs ship great software that is unused because branch staff were not trained, compliance workflows were not updated, or customer communication was absent. The mental model is "readiness before release": the target architecture is only real when the org can operate it safely and efficiently.

## One diagram (mandatory)
```mermaid
graph LR
    classDef ok fill:#a7f3d0,stroke:#065f46,stroke-width:2px,color:#000
    classDef risk fill:#fecaca,stroke:#991b1b,stroke-width:2px
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
    State0[Current State]:::ok --> Ready[Readiness Planning (ADKAR)]:::decision --> Release[Release & Pilot]:::risk --> Adopt[Full Adoption & Reinforcement]:::ok --> Value[Value Realization]:::ok
```

## When to use / when NOT to use
- ✅ **Use when:** The architectural initiative crosses business units, requires behavioral change, or has high uncertainty about adoption.
- ⚠️ **Avoid when:** The change is purely technical, backward-compatible, and has no process or staff impact (e.g., a database engine upgrade with zero business change).

## Banking 💳 example
A bank rolls out a real-time open-banking API gateway for third-party fintech integration. The architecture is sound, but branch tellers rely on batch-based balance queries and advisors are paid by cross-sell on legacy products. Change management introduces a shared incentive for digital onboarding, trains staff on API-based product bundles, and pilots the service in one retail region before nationwide launch—preventing a technically ready but organizationally rejected rollout.

## Common confusions (don't mix these up)
- **Change & Adoption** vs **Project Management:** Change management addresses people and culture; project management addresses scope, schedule, and budget.

## Interview / recall prompt
"Explain change and adoption in EA in 2 minutes without notes." →
- It is about the org transition, not just the tech.
- Readiness must precede release.
- ADKAR is a classic framework for structured change.
- Transition architecture bridges current and target.
- Value realization must be tracked after launch.

---
**Status:** ✅ Covered · See detail doc: `[details/C9-07-change-adoption.md](../details/C9-07-change-adoption.md)`
