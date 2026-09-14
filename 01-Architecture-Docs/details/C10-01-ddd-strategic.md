# [C10-01] Domain-Driven Design (Strategic) — DETAIL
> **Category:** C10 — Emerging & Advanced Topics · **Difficulty:** ●/◑/○ · **Banking-relevant:** yes
>
> **Companion brief:** `[briefs/C10-01-ddd-strategic.md](../briefs/C10-01-ddd-strategic.md)`
>
> **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.
>
> ---
>
> ## 1. Precise definition
> Domain-Driven Design (DDD) is an iterative approach to structuring complex software whose primary goal is to model complex business domains through rich, expressive domain models that reflect the real-world business context (Evans & Evans, 2003). The strategic dimension adds enterprise governance: it prescribes how teams, APIs, contracts, and regulatory artifacts should be aligned with domain boundaries so that a change in one business rule does not unpredictably cascade across the enterprise.
>
> ## 2. Why it exists (problem it solves)
> Pre-DDD, banking systems accumulated "transaction scripts"—flat databases with minimal logic—because business analysts and developers spoke different languages. When Basel capital rules or accounting standards changed, the same code had to serve every line of business, making compliance audits catastrophic. DDD exists to make the code's structure mirrors the domain's economic logic, so that regulatory changes map to isolated, well-tested modules rather than global monoliths.
>
> ## 3. Core concepts & vocabulary
> | Term | Precise meaning |
> |------|-----------------|
> | Aggregate | A cluster of domain objects treated as a single unit for data changes, with one root ensuring consistency; e.g., a `Customer` aggregate containing `Address`, `CreditProfile`, and `KYCCompliance`. |
> | Bounded Context | A specific scope where a particular domain model is valid and unambiguous; different contexts may have different facts about the same entity. |
> | Context Mapping | The explicit negotiation of how two Bounded Contexts interact: Customer-Supplier, Conformist, Anti-Corruption Layer, etc. |
> | Ubiquitous Language | A rigorous, jointly-owned language used in code comments, database schema names, tests, and meetings; enforced by testing tools that reject mismatched vocabulary. |
> | Strategic DDD | The practice of applying DDD at the enterprise level: team topology, API contracts, and compliance documentation are modeled as first-class artifacts. |
>
> ## 4. How it works (architecture / mechanism)
> ### 4.1 Diagrams
> **Diagram A — Core structure (highlight the load-bearing parts = amber, supporting = grey):**
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
>     classDef context fill:#dfe6e9,stroke:#636e72
>     classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
>     
>     UB[Ubiquitous Language]:::critical
>     BC_KYC[KYC BC]:::context
>     BC_RISK[Risk BC]:::context
>     BC_TRADE[Trade BC]:::context
>     AM[Anti-Corruption Layer]:::decision
>     
>     UB --> BC_KYC
>     UB --> BC_RISK
>     UB --> BC_TRADE
>     BC_TRADE --> AM
>     AM --> BC_RISK
> ```
>
> **Diagram B — Context Mapping (highlight decision points = green, failures = red):**
> ```mermaid
> flowchart LR
>     classDef ok fill:#a7f3d0,stroke:#065f46
>     classDef risk fill:#fecaca,stroke:#991b1b
>     classDef service fill:#bfdbfe,stroke:#1e40af
>     
>     KYC[KYC Context]:::service
>     LENDING[Lending BC]:::context
>     Bridge[Loan App BC]:::decision
>     
>     KYC -.->|Customer-Supplier| Bridge:::ok
>     Bridge -->|Conformist| LENDING:::context
>     Lending -->|Anti-Corruption| KYC
> ```
>
> ## 5. Variants, options & trade-offs
> | Variant | When to pick | When to avoid | Key trade-off axis |
> |---------|--------------|---------------|--------------------|
> | Big Ball of Mud (no DDD) | 3-month PoC with flat requirements | Production banking core | Fast-to-market vs. compliance auditability |
> | Transaction Script | Simple CRUD, low business volatility | Complex trade finance | Simplicity vs. domain richness |
> | Strategic DDD (macro-service topology) | Enterprise with 10+ lines of business, regulators watching | Single-team startup | Organizational overhead vs. regulatory alignment |
> | Tactical DDD (aggregate-per-context) | Single or few Bounded Contexts, one team | Multi-national with strong siloes | Modeling depth vs. team collaboration |
>
> ## 6. Relationships to sibling topics
> - **Microservices:** DDD defines *what* the service should be; microservices define *how* to organize services. A bank can have macro-services and still apply DDD; conversely, microservices without a domain model create the worst of both worlds.
> - **Event-Driven Architecture (C10-02):** Domain events are the natural vehicle for bounded-context communication; DDD gives the event its semantics.
> - **API Economy (C10-05):** Bounded Contexts become the natural API product boundaries; the ubiquitous language becomes the API contract.
>
> ## 7. Banking / financial-services context 💳
> A global asset manager restructures its middle-office into four Bounded Contexts: *Data*, *PositionMgmt*, *Risk*, and *TradeCapture*. Each context publishes domain events—`PositionAdjusted`, `RiskLimitExceeded`—via an event mesh. When the regulator changes the definition of "market risk," only the *Risk* Bounded Context changes; its aggregate tests pass, and downstream contexts consume the same event schema. This is now a DORA-aligned practice: the "change in one domain state" pathway is fully classified, logged, and auditable.
>
> ## 8. Reference architecture / worked example
> **Problem:** The bank's loan origination system shares a single `Customer` table with compliance, marketing, and collections. Every schema change requires a 3-month regression cycle because the facts in those three contexts are contradictory ("Customer" in compliance is a legal entity; in marketing it is a preference profile).
>
> **Decision:** Split into two Bounded Contexts: `LoanOrigination` and `KYC`. They share an anti-corruption layer for onboarding but diverge after approval.
>
> ```mermaid
> graph LR
>     classDef service fill:#bfdbfe,stroke:#1e40af
>     classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5,color:#64748b
>     classDef data fill:#fde68a,stroke:#92400e
>     
>     KYC[KYC Context]:::boundary
>     LOAN[Loan Origination]:::service
>     API[Customer API]:::boundary
>     DST[(KYC Datastore)]:::data
>     STS[(Loan DS)]:::data
>     
>     API --> KYC
>     API --> LOAN
>     KYC --> DST
>     LOAN --> STS
> ```
>
> **ADR drafted:**
> ```markdown
> # ADR-2025-047: Loan Origination Bounded Context
> ## Status
> Accepted
> ## Context
> The 2024 DORA audit found that customer-data mutations touched 47 services, creating an unclassified blast radius.
> ## Decision
> Create a Loan Origination Bounded Context with Aggregate Root `LoanApplication` (status: draft → under_review → approved → funded).
> ## Consequences
> - Positive: Blast radius for "application status change" contracts to 4 services.
> - Negative: Onboarding shared-events now require idempotency and deduplication.
> - ...
> ## Alternatives considered
> 1. Monolith table with row-level security: Rejected (non-table-level auditability).
> 2. Purely functional event sourcing: Rejected (too steep for 2025 timeline).
> ```
>
> ## 9. Maturity & adoption signals
> - **Adopt when:** > 30% of your banking systems are "change-hard" (regulatory or product cycles > 6 months); regulators request change-impact analysis for any model change.
> - **Anti-signals (don't adopt yet):** Small portfolio (single product line), flat organizational structure, or team constantly rotates; DDD requires stable domain ownership.
> - **Common failure modes:** Dominant experts creating a "god model"; developers bypassing the language for "it's just faster"; anti-corruption layers becoming mere file-format conversions.
>
> ## 10. Common confusions — the "don't mix" list
> | Often confused | Real distinction |
> |----------------|------------------|
> | DDD vs Microservices | DDD is a modeling methodology; microservices are an organizational/deployment pattern. |
> | Bounded Context vs Service | A Bounded Context *may* map to a service, but a service can host multiple Bounded Contexts (e.g., internal utility). |
> | Strategic vs Tactical DDD | Tactical DDD focuses on patterns within one developer codebase; Strategic DDD adds team boundary and API shape. |
>
> ## 11. Tools & standards to know
> - **Standards/Frameworks:** TOGAF ADM Phase C (Domain Architecture); Domain-Driven Design by Eric Evans; DORA (Regulation (EU) 2022/2554) on ICT risk.
> - **Common tooling:** Archi (ArchiMate modeling), Structurizr (C4 + Bounded Context diagrams), domain-language linters, Axon Framework (Java), Event Sourcing libraries.
> - **Mandatory reading:** "Domain-Driven Design" by Eric Evans; "Strategic Design with Domain-Driven Design" by Vaughn Vernon.
>
> ## 12. ADR template (ready to fill in)
> ```markdown
> # ADR-XXX: <decision>
> ## Status
> Accepted | Proposed | Deprecated
> ## Context
> ...
> ## Decision
> ...
> ## Consequences
> - Positive ...
> - Negative ...
> - ...
> ## Alternatives considered
> 1. ...
> 2. ...
> ```
>
> ## 13. Practice — apply it
> 1. **Recall:** Define DDD's Ubiquitous Language in 2 min without notes.
> 2. **Model:** Draw an ArchiMate or C4 diagram showing 3 Bounded Contexts for a retail bank.
> 3. **ADR:** Write an ADR proposing a Bounded Context for a specific feature (e.g., instant P2P payment settlement).
> 4. **Defend:** Roleplay explaining why a Bounded Context is necessary to your CRO.
>
> ## 14. Summary (1 paragraph)
> Domain-Driven Design is the strategic practice of turning a bank's most complex business logic—regulatory rules, trade lifecycles, customer hierarchies—into first-class code structure. It is not a toolkit but a social contract: the development organization commits to a shared language, and the language commits to reflecting the real economics of banking.
>
> ---
> **Status:** ✅ Created · **Last updated:** 2026-09-14
