# [C?] [Topic Name] — BRIEF
> **Category:** C9 — Strategic Themes · **Difficulty:** ● · **Banking-relevant:** yes / 💳
> **One-liner:** Cross-border licensing lets a liquidator or host regulator recognise a custodial entity in one jurisdiction as authorized to operate in another, usually via passporting, equivalence, or a full branch license.
> **Why an enterprise architect / trainee cares:** Architects must design for regulatory-mapping—data, reporting, and legal entities that satisfy multiple host-supervisor requirements simultaneously.
>
> ## Quick definition
> Cross-border licensing is the legal mechanism by which a custodian with an authorization in one jurisdiction obtains permission, often through a single dossier or mutual recognition, to provide custody services to clients or assets located in another jurisdiction.
>
> ## Key ideas / terms
> - **Passporting:** Under MiFID II, a UCITS or AIFM authorized in one EU/EEA state can offer services in others without separate authorization.
> - **Equivalence decision:** A non-EEA jurisdiction's regime is deemed equivalent to the regulator's standards, allowing reliance without full approval.
> - **Host-supervisor:** The regulator where the client resides and where the asset is held.
> - **Branch licence:** A full local operating authorization rather than a service-only passport, often required for deposit-taking or execution-venue activities.
>
> ## The mental model
> The architecture is a legal-entity lattice mapped to regulatory reporting paths. A single custody operation must emit multiple statutory reports, translated into local languages and formats, while keeping client assets segregated per host rules. This is a compliance-mesh problem: the data model must support multi-tenant regulatory views over the same underlying ledger.
>
> ## One diagram (mandatory)
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     Home[Home Regulator<br/>Authorisation]:::critical --> Passport[Passport /<br/>Equivalence Art]:::core
>     Home --> Branch[Branch Licence]:::core
Error message: JSON Parse error: Unterminated string
