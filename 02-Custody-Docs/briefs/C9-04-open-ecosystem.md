# [C?] [Topic Name] — BRIEF
> **Category:** C9 — Strategic Themes · **Difficulty:** ● · **Banking-relevant:** yes / 💳
> **One-liner:** Open custody ecosystems share vault capabilities with fintechs via standardized APIs, unlocking new revenue while preserving core risk posture.
> **Why an enterprise architect / trainee cares:** Architects must evaluate integration risks, data sovereignty, and vendor consolidation when opening custody.
>
> ## Quick definition
> An open custody ecosystem exposes selected vault functions—typically safekeeping, corporate actions, and settlement—to external firms through governed APIs, turning the custody line into a platform.
>
> ## Key ideas / terms
> - **API:** Contract specifying what data or actions a client can request from an internal system.
> - **TPP:** Third-Party Provider; a fintech or asset manager consuming the custody platform.
> - **Sandboxing:** Isolated runtime environment that enforces strict boundaries so a TPP cannot affect production systems.
> - **Data sovereignty:** Legal requirement that certain client data remain within a geographic jurisdiction.
>
> ## The mental model
> Open ecosystems function like a modern API-first platform: a core vault (the monolith) exposes curated contracts (the micro-frontends) to TPPs through an API gateway. Governance sits at the edge as an access-control and logging layer. This pattern mirrors the data-mesh approach—data products for external consumption—but introduces custody-specific obligations around collateral, segregation, and audit. The trade-off is between reach and control.
>
> ## One diagram (mandatory)
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     Guard[API Gateway<br/>Auth & Rate Limit]:::critical --> Onboard[Onboarding &<br/>Risk Assessment]:::core
>     Onboard --> Vet[TPP Vetting<br/>& Agreements]:::context
>     Onboard --> Vault[Custody Vault]:::core
>     Vault --> Settle[Settlement Engine]:::core
>     Vault --> CorpAct[Corporate Actions]:::core
>     Settle --> Client[Client / CMOs]:::context
>     CorpAct --> Ops[Operations]:::context
> ```
>
> ## When to use / when NOT to use
> - ✅ **Use when:** You need to monetize surplus vault capacity and reduce time-to-market for new products.
> - ⚠️ **Avoid when:** Mandatory data-residency rules prohibit external hosting, or the institution cannot commit to 24/7 operational availability.
>
> ## Banking example
> A major European custody bank exposes safekeeping and proxy-voting APIs to asset managers via PSD3-aligned open-banking rails. The bank vets each TPP against MiFID II suitability criteria, enforces a data-access tiering model, and runs TPP traffic on dedicated non-internet-facing LDAP-backed gateways. A ransomware attack on a TPP does not propagate because the sandbox is strictly network-isolated.
>
> ## Common confusions (don't mix these up)
> - **Open ecosystem** vs **Open banking:** Open banking is a regulated framework for payment accounts; an open custody ecosystem is a commercial strategy to expose vault services, with no mandatory PSD requirement.
>
> ## Interview / recall prompt
> "Explain open custody ecosystems in 2 minutes without notes."
> - Custody as a platform, not a utility.
> - TPP risk tiering and sandboxing.
> - Balance between revenue and control.
>
> ## Status
> ☐ Not started · See detail doc: `details/C9-04-open-ecosystem.md`
