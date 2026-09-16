# C8-03 Capability Mapping — BRIEF
> **Category:** Custody/Identity — **Difficulty:** ◔ · **Banking-relevant:** yes 💳
> **One-liner:** Capability mapping is the practice of aligning business outcomes (e.g., "zero days to settle") with architectural requirements, then assigning each requirement to a specific layer, system, or function so that gaps are visible and prioritized.
>
> **Why an enterprise architect / trainee cares:** In banking, capability gaps are the root cause of failed product launches and regulatory breaches. Mapping capabilities to the reference architecture and to the tech stack turns vague "we need faster settlement" into a concrete backlog with owners and success criteria.

## Quick definition
Capability mapping is the structured alignment of enterprise business capabilities (what the bank must be able to do) with architectural components and technical solutions (how it is done), ensuring that every strategic objective has a measurable, testable, and accountable implementation path.

## Key ideas / terms
- **Business Capability:** What the bank does in the market (e.g., "Custody for Retail Clients").
- **Technical Capability:** How it is delivered by systems (e.g., "Automated Reconciliation Engine").
- **Gap:** The mismatch between what the bank wants and what it can currently do.
- **BET (Business Enablement Technology):** The technology that enables a business capability.

## The mental model
Capability mapping sits on top of the reference architecture (C8-01) and the account hierarchy (C8-02). It asks: "Given the structure we have, and the accounts we manage, what *must* we be able to do?" It then assigns each business outcome to a layer (economic, logical, physical, governance) and to a concrete system. The governance angle is about *alignment*: it prevents the architecture from drifting into a system that does not serve the business.

## One diagram (mandatory)
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

## When to use / when NOT to use
- ✅ **Use when:** Strategic planning, M&A integration, or regulatory remediation where you must justify system investments.
- ⚠️ **Avoid when:** Ad-hoc firefighting or one-off features with no strategic anchor.

## Banking example
A regional investment bank wants to offer same-day cash sweeps across all EEA branches. Its capability mapping identifies three gaps: (1) a unified cash CDM, (2) a real-time payment engine connected to T2S, and (3) a governance update to the ARB. The mapping produces a prioritized roadmap: first build the CDM, then the engine, then re-govern. After nine months, the bank achieves zero-days cash sweep and satisfies DORA's liquidity resilience test.

## Common confusions (don't mix these up)
- **Capability Mapping** vs **Gap Analysis:** Capability mapping is the *alignment* activity; gap analysis is the *diagnosis* that feeds into it.

## Interview / recall prompt
"Explain capability mapping in 2 minutes without notes."
- Business capability → technical capability → gap → backlog.
- Anchors architecture to strategy.
- Prevents drift and wasted investment.

## Status
☐ Not started · See detail doc: `details/C8-03-capability-mapping.md`

---
**One diagram required. Both brief + detail must exist before ✓.**
