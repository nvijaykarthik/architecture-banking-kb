# C8-01 Reference Architecture — BRIEF
> **Category:** Custody/Identity — **Difficulty:** ◑ · **Banking-relevant:** yes 💳
> **One-liner:** A reference architecture is a standardized, reusable structural blueprint that defines components, relationships, and governance rules for a domain so teams can build compliant, interoperable systems without reinventing the wheel.
>
> **Why an enterprise architect / trainee cares:** At a multinational bank, reference architectures prevent siloed bespoke solutions that fragment data rights, break audit trails, and fail regulator inspections. Knowing how they differ from "reference implementations" and "pattern libraries" means you can defend a design choice to internal audit and the external examiner.

## Quick definition
A reference architecture is a descriptive or prescriptive abstraction of a system-of-interest, specifying its structural organization, the core concerns, and the relationships among its parts. In custody and identity domains, it encodes how assets, accounts, rights, and access controls must be wired together to satisfy operational, regulatory, and security requirements.

## Key ideas / terms
- **Reference architecture:** A generic structure delegable to many implementations, not a single working system.
- **ADR (Architecture Decision Record):** A short document that names, dates, and justifies a structural choice tied to the architecture.
- **Canonical Data Model (CDM):** A shared semantic layer that all custody and identity systems map to, preventing integration drift.
- **Governance:** The set of policies, boundaries, and escalation paths that ensure the architecture remains compliant and evolvable.

## The mental model
Reference architecture sits between *patterns* (reusable solutions to common problems) and *reference implementations* (concrete code that realizes the pattern). It is the shared, approved scaffolding that custody and identity teams lean on when onboarding new products, migrating legacy vaults, or integrating with third-party custodians. The governance angle is paramount: without a formally approved reference architecture, every team builds its own vault topology, and the bank ends up with an un-auditable sprawl of asset representations.

## One diagram (mandatory)
 ```mermaid
 graph TD
     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
     A[Reference Architecture]:::critical --> B[Canonical]:::core
     A --> C[Governance]:::core
     B --> D[CDM]:::context
     C --> E[ADR Process]:::context
     B --> F[Pattern Library]:::context
     C --> G[Escalation Paths]:::context
 ```
 ```

## When to use / when NOT to use
- ✅ **Use when:** Starting a new custody product, integrating a third-party custodian, or undergoing a regulatory review where a documented architectural posture is required.
- ⚠️ **Avoid when:** War-room firefighting or one-off proof-of-concepts where speed beats structural clarity; here a pattern library is lighter-weight.

## Banking example
A global investment bank operating 12 jurisdictions runs an "All-Asset Custody" platform. The reference architecture mandates a single CDM for cash, securities, and digital assets, with every zone's sub-custodian mapping through the same canonical exchange. This architecture satisfies DORA's ICT risk-management requirements because it provides one auditable topology: if one region's sub-custodian API goes down, the bank's control framework already defines the fallback routing and root-cause tracking.

## Common confusions (don't mix these up)
- **Reference architecture** vs **Reference implementation:** The former is a blueprint; the latter is working code people often mistake for the former.
- **Reference architecture** vs **Pattern library:** Patterns solve specific problems; the architecture ties them into a systemic whole.

## Interview / recall prompt
"Explain reference architecture in 2 minutes without notes."
- Always distinguish it from a reference implementation.
- Mention the governance and standardization functions.
- Anchor it to a real failure mode (regulatory audit, data-rights fragmentation).

## Status
☐ Not started · See detail doc: `details/C8-01-reference-architecture.md`

---
**One diagram required. Both brief + detail must exist before ✓.**
