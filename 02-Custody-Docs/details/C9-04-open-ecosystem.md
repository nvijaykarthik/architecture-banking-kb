# [C?] [Topic Name] — DETAIL
> **Category:** C9 — Strategic Themes · **Difficulty:** ● · **Banking-relevant:** yes / 💳
> **Companion brief:** `briefs/C9-04-open-ecosystem.md`
> > **Target reader:** enterprise architect who must explain, justify, and defend the topic — not just recite it.
>
> ---
>
> ## 1. Precise definition
> An open custody ecosystem is a strategic architecture pattern in which a custody-and-administration bank or central custodian exposes curated vault services—safekeeping, corporate actions, collateral matching, and settlement—to external Third-Party Providers (TPPs) through governed APIs and micro-service boundaries, under explicit contractual and regulatory oversight.
>
> ## 2. Why it exists (the problem it solves)
> Legacy custody is a closed-loop back-office function: clients give instructions; operations processes them. Revenue is flat, driven by scale. As digital asset management and T+0 settlement expectations rise, banks face pressure to offer consumption-style services without building bespoke lines. The failure mode without an open ecosystem is a slow-moving utility that loses share to fintech platforms offering modular, self-serve experiences.
>
> ## 3. Core concepts & vocabulary
> | Term | Precise meaning |
> |------|-----------------|
> | API Gateway | Central entry point enforcing authentication, rate limiting, and protocol translation for internal vault services. |
> | TPP | External fintech, asset manager, or prime brokerage consuming custody APIs under a contractual SLA. |
> | Segregation | Physical or logical isolation of TPP client data so that a breach by one TPP cannot affect others. |
> | Collateral Pre-Positioning | Automating custody-lending collateral checks so that TPPs can pledge assets without manual intervention. |
> | Open Banking | Regulatory framework (e.g., PSD2/3) requiring banks to provide payment-account access to TPPs. |
>
> ## 4. How it works (architecture / mechanism)
> The architecture layers API discovery and security controls (edge), orchestration and governance (platform), and vault implementation (core). TPPs are onboarded through a risk-based tiering model. A critical design point is the vault data model: it must remain serializable for audit while supporting real-time event streaming to TPP dashboards.
>
> ### 4.1 Diagrams
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     Edge[API Gateway<br/>IdP + Rate Limit]:::critical --> Onboard[TPP Onboarding<br/>& Key Mgt]:::core
>     Onboard --> Cond[Contract &<br/>Acceptance Test]:::context
>     Onboard --> Vault[Custody Vault<br/>Core Services]:::core
>     Vault --> Path[API Path Layer<br/>Adapter]:::context
>     Path --> Coll[Collateral<br/>Pre-Position]:::core
>     Path --> Corp[Corporate Actions]:::core
>     Path --> Settle[Settlement Engine]:::core
>     Path --> Audit[Immutable Audit Log]:::context
>     Vault --> DLT[DLT / Tokenized<br/>Register]:::core
> ```
>
> ## 5. Variants, options & trade-offs
> | Variant | When to pick | When to avoid | Key trade-off axis |
> |---------|--------------|---------------|--------------------|
> | Full vault open | You have spare platform capacity and want to launch a new business line. | Legacy vault has no event-driven audit trail. | Revenue vs. governance complexity. |
> | Function-level open | You want to monetise a single high-margin function (e.g., proxy voting). | Cross-functional data integration is expensive. | Speed vs. depth. |
> | Read-only open | You need to expose valuation and position data for ESG reporting. | You cannot meet contractual liability requirements. | Transparency vs. legal exposure. |
>
> ## 6. Relationships to sibling topics
> - **Straight-through processing:** A prerequisite; without automated intra-day asset movements, an open ecosystem will generate too much exception volume.
> - **Data mesh:** The same principles of domain ownership and product-thinking, but applied to vault-centric data products rather than domains in general.
> - **MiFID II transparency:** Regulated reporting of algorithmic trading may consume the same audit log that the open ecosystem builds for TPP accountability.
>
> ## 7. Banking / financial-services context 💳
> A Swiss custody bank launches a "Custody as a Service" portal for regional asset managers. The bank uses a PSD3-compliant API gateway, enforces Tier-1 TPP status only for firms with audited SOC 2 controls, and stores all TPP instructions in an append-only log. When a TPP platform experiences a credential leak, the sandbox egress route is revoked within minutes, and the vault’s segregation model prevents lateral movement. The business reason is not technology for its own sake; it is keeping AUM share in a market where T+0 settlement is becoming a table-stake.
>
> ## 8. Reference architecture / worked example
> The Swiss custody bank above represents the canonical worked example: a PSD3-compliant API gateway with Tier-1 TPP controls, a segregated vault data model, and an immutable audit log. The bank's service selector routes TPP traffic to isolated micro-services, while policy enforcement at the edge blocks unauthorized data exfiltration.
>
> ## 9. Maturity & adoption signals
> - **Adopt when:** Platform team is service-oriented, vault operations are SaaS-ready, and CRO has approved a TPP risk tiering policy.
> - **Anti-signals:** Vault runs on bespoke mainframe tape backups; operations team is flat (no one owns a single occupied micro-service).
> - **Common failure modes:** (1) The "open" gateway turns into a single un-monitored splice point; (2) Data-sovereignty rules block cross-border TPP traffic, collapsing the addressable market.
>
> ## 10. Common confusions — the "don't mix" list
> | Often confused | Real distinction |
> |----------------|------------------|
> | Open ecosystem vs Open banking | Open banking is a mandatory regulated data-access requirement for payment accounts; an open custody ecosystem is a commercial platform strategy with no universal legal mandate. |
> | API-gateway vs. micro-service | An API gateway is an edge orchestrator; a micro-service is a vault implementation that can only be reached through a gateway or internal mesh. |
>
> ## 11. Tools & standards to know
> - **Frameworks / TOGAF:** Architecture domain is Application and Business Architecture; use the Open Service Gateway Initiative (OSGi) concepts for modularity.
> - **Common tooling:** Kong / Apigee for API management; HashiCorp Vault for credential lifecycle; Kafka for event streaming; GitHub Actions for deployment pipelines.
> - **Mandatory reading:** ISDA SIMM Bridge FAQ, PSD3 Delegated Regulation (EU) 2024/1689, McKinsey "Custody reinvention" series.
>
> ## 12. ADR template (ready to fill in)
> ```markdown
> # ADR-01: Open Custody Ecosystem
> ## Status
> Accepted
> ## Context
> The bank’s custody line is a cost sink with flat revenue. TPPs are requesting self-serve safekeeping APIs.
> ## Decision
> Expose vault safekeeping and corporate actions through a governed API gateway to TPPs, with sandboxed data isolation and upon proven SOC 2 compliance.
> ## Consequences
> - Positive: New revenue stream, platform operating leverage, real-time audit.
> - Negative: Ongoing TPP risk-monitoring cost, potential brand blowback from a TPP data leak.
> - ...
> ## Alternatives considered
> 1. Build bespoke TPPs per asset class.
> 2. White-label an existing third-party custodian.
> ```
>
> ## 13. Practice — apply it
> 1. **Recall:** Define in 2 min without notes.
> 2. **Model:** Produce an ArchiMate/UML diagram from scratch for the architecture above.
> 3. **ADR:** Write a decision doc applying it to the Swiss custody example in §7.
> 4. **Defend:** Roleplay explaining it to a non-technical CRO / CIO.
>
> ## Summary
> An open custody ecosystem redefines the vault from a closed back-office to a platform product. Success depends on rigorous TPP tiering, immutable audit trails, and a clear contract boundary between the bank’s regulated capital and the TPP’s operational fragility. The pattern is not for every institution, but for those with enough governance maturity it turns a utility into a scalable revenue engine.
>
> ---
> **Status:** ☐ Not started · ☐ In progress · ✅ Covered
> *Last updated: 2025-07-09*
>
> ---
> **One diagram required. Both brief + detail must exist with ≥1 mermaid each before ✓.**
