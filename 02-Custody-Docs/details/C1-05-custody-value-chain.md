# C1 custody value chain — DETAIL
> **Category:** C1 Foundations · **Difficulty:** ◑ · **Banking-relevant:** yes / 💳
>
> **Companion brief:** `briefs/C1-05-custody-value-chain.md`
> >
> > **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.
>
> ---
>
> ## 1. Precise definition
> The custody value chain is the full set of interdependent processes that a custodian performs for an asset owner or nominee: (1) onboarding and entitlement verification, (2) settlement and book-entry transfer, (3) safekeeping in segregated, omnibus, or nominee books, (4) corporate action processing and fee collection, (5) securities lending with collateral optimisation, and (6) periodic and event-driven reporting. It is distinct from the *settlement value chain* (which covers DvP/RTGS rails) because custody *maintains* the legal position after title has passed.
>
> ## 2. Why it exists (the problem it solves)
> Before modern securities-holding systems, investors kept physical certificates in safe-deposit boxes. That demanded manual reconciliation, per-account legal ownership records, and physical transport of certificates for corporate actions. The value chain emerged to centralise legal record-keeping, reduce counter-party risk, and scale servicing. Without it, every bank would need a legal, compliance, and IT team per denomination—unaffordable at scale.
>
> ## 3. Core concepts & vocabulary
> | Term | Precise meaning |
> |------|-----------------|
> | Omnibus holding | A single legal position for many clients; the custodian is the beneficial owner of the whole pool. |
> | Nominee holding | The custodian holds in the name of a nominee; true legal ownership is with the nominee. |
> | DTA (Distributor Tax Administration) | A standardised mechanism for withholding taxes at source. |
> | RTGS | Real-Time Gross Settlement; settlement finality. |
> | CLS | Continuous Linked Settlement; mitigates FX settlement risk ("Herstatt risk"). |
>
> ## 4. How it works (architecture / mechanism)
> The custody pipeline is a state machine with six terminal and non-terminal states. State transitions are triggered by external events (trade execution, corporate-action notice, corporate-action settlement) or internal timers (end-of-day cutoff, regulatory reporting deadline).
>
> ### 4.1 Diagrams
>
> **Diagram A — Core structure** (highlight load-bearing parts = amber, supporting = grey, context = light):
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     A[Onboarding]:::context --> B[Settlement]:::core
>     B --> C[Holding]:::critical
>     C --> D[Corporate Actions]:::core
>     D --> E[Securities Lending]:::core
>     E --> F[Reporting]:::core
>     C --> G[Settlement Feed]:::critical
>     G --> B
>     D --> H[Corporate-Action Feed]:::critical
>     H --> C
> ```
>
> **Diagram B — Lifecycle / flow** (highlight decision points = green, failures = red, money = gold, context = grey):
> ```mermaid
> flowchart LR
>     classDef ok fill:#a7f3d0,stroke:#065f46,color:#000
>     classDef risk fill:#fecaca,stroke:#991b1b,color:#000
>     classDef money fill:#fde68a,stroke:#92400e,color:#000
>     classDef context fill:#e5e7eb,stroke:#6b7280,color:#000
>     Start[Client Order]:::context --> Trade[Trade & Settlement]:::ok
>     Trade -->|Pass| Onboard[KYC / Onboard]:::ok
>     Trade -->|Fail| Risk[Risk / Block]:::risk
>     Onboard --> Hold[Physical / Book-Entry Holding]:::critical
>     Hold --> Divid[Corporate Action Notice]:::ok
>     Divid -->|Yes| PayAction[Dividend / Split]:::money
>     Divid -->|No| Lend[Securities Lending]:::ok
>     Lend --> Report[Reporting]:::ot
> ```
>
> **Diagram C — Data flow & audit pipeline** (highlight service = blue, data = gold, boundary = grey dashed):
> ```mermaid
> flowchart LR
>     classDef service fill:#bfdbfe,stroke:#1e40af,stroke-width:1px,color:#000
>     classDef data fill:#fde68a,stroke:#92400e,stroke-width:1px,color:#000
>     classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5,color:#000
>     Client[Client]:::service --> API[Onboarding API]:::service
>     API --> DB[(Nominal Ledger)]:::data
>     DB --> HoldSvc[Holding Service]:::service
>     HoldSvc --> CA[Corporate Action Engine]:::service
>     CA --> Report[Reporting Service]:::service
>     Report --> Audit[Audit Log]:::boundary
>     Report --> DTA[DTA Tax Engine]:::service
> ```
>
> ```
>
> ## 5. Variants, options & trade-offs
> | Variant | When to pick | When to avoid | Key trade-off axis |
> |---------|--------------|---------------|--------------------|
> | Segregated | Institutional mandate, AUM > €5 bn | Very small accounts or fixed-income heavy portfolios | Cost vs legal protection |
> | Omnibus + separate records | Retail / wealth platforms, price-sensitive | DeFi-adjacent clients wanting disclosure | Scale vs transparency |
> | DS (Direct Securities) | Large banks with own clearing, bespoke SLAs | High-frequency trading or ETF-heavy mandates | Control vs standardisation |
>
> ## 6. Relationships to sibling topics
> - **Settlement:** custody consumes settlement output; no settlement, no book-entry transfer.
> - **Client lifecycle management:** onboarding is the entry-point to the custody chain; offboarding is the exit.
> - **Tax withholding / DTA:** embedded in corporate actions and lending fee calculations.
>
> ## 7. Banking / financial-services context 💳
> Under MiFID II and EMIR, a bank in the EU must disclose whether it performs *depositary* custody (risk-mitigation for UCITS/AIFMD) or *custody* alone. The business risk is that a failure in omnibus holdings triggers a *covered bond* liquidity crisis if the underlying asset pool is mis-allocated. A real consequence: the 2020 Archegos collapse revealed how failure-to-deliver was hidden in omnibus structures, forcing margin calls across the repo chain. The architect’s job is to ensure the nominal ledger is a *single source of truth*, not a reconciliation of two部分 pieces.
>
> ## 8. Reference architecture / worked example
> **Problem:** A multi-national retail wealth bank receives a new client with a deposit of USD 5 m and wants to hold Chinese A-shares.
>
> **Decision:** Use a segregated omnibus structure in the depository; book the A-shares in the CSD directly; use a third-party registrar for the share class.
>
> **Result:**
> - Onboarding → KYC + FATCA + China QFII approval.
> - Settlement → USD held in omnibus; A-shares registered in CSD.
> - Holding → segregated sub-account at sub-custodian.
> - Reporting → half-yearly prospectus delivery + annual tax ISIN report.
>
> ```mermaid
> graph LR
>     classDef service fill:#bfdbfe,stroke:#1e40af
>     classDef data fill:#fde68a,stroke:#92400e
>     classDef boundary fill:#f1f5f9,stroke:#6b7280,stroke-dasharray: 5
>     Client[Client]:::service --> SUI[Sub-User Interface]:::service
>     SUI --> ONB[Onboarding Engine]:::service
>     ONB --> NLM[(Nominal Ledger)]:::data
>     NLM --> SUB[(Sub-Custodian Data)]:::data
>     SUB --> BOC[Bonds & Shares CSD]:::boundary
> ```
>
> ## 9. Maturity & adoption signals
> - **Adopt when:** legal entity data is structured, isCUSIP/ISIN mapping is automated, and T+0 to T+2 cut-offs are enforced by middleware.
> - **Anti-signals:** manual email confirmations for every transfer; "segregated" that is actually omnibus.
> - **Common failure modes:** (1) entitlement drift—client A’s shares appear in client B’s position; (2) corporate-action leak—dividend gets to omnibus but not the client; (3) overnight lock-out on manual cut-offs on weekends.
>
> ## 10. Common confusions — the "don't mix" list
> | Often confused | Real distinction |
> |----------------|------------------|
> | Custody value chain | The ordered process from onboarding to reporting. |
> | Settlement process | The DvP/RTGS rail that moves title. |
> | Holding structures | Physical (safe-deposit), book-entry (CSD), nominee, or omnibus. |
> | Securities lending | Fully separate pipeline that uses holding as collateral source. |
>
> ## 11. Tools & standards to know
> - **Standards:** DTCC NCS, ESMA 822, ISO 20022, ISO 20022-2.
> - **Tooling:** T+1 settlement middleware (e.g., Euroclear Shell / Clearstream), ISIN databases, DTA engines.
> - **Mandatory reading:** ICSD model custody agreement; ESMA Guidelines on MiFID/AIFMD depositary duties.
>
> ## 12. ADR template (ready to fill in)
> ```markdown
> # ADR-01: Custody Model for Multi-Asset Retail Platform
> ## Status
> Accepted
> ## Context
> The wealth platform needs to hold equity, bonds, and ETFs across EU, US, and UK with a single onboarding flow.
> ## Decision
> Segregated omnibus at current bank; direct CSD registration for US equities; DS for UK equities.
> ## Consequences
> - Positive: regulatory clarity; negative: higher cost.
> ## Alternatives considered
> 1. Third-party custodian. 2. Direct registration only.
> ```
>
> ## 13. Practice — apply it
> 1. **Recall:** define in 2 min without notes.
> 2. **Model:** produce an ArchiMate/UML diagram from scratch.
> 3. **ADR:** write a decision doc applying it to the Chinese A-shares example in §8.
> 4. **Defend:** roleplay explaining it to a non-technical CRO / CIO.
>
> ## Summary
> The custody value chain is the backbone of every bank that holds assets on behalf of clients. It is not merely "keeping securities safe"; it is a continuous, regulated pipeline that touches KYC, settlement, tax, and reporting systems. A bank that cannot articulate the chain, its data dependencies, and its fail-over paths cannot defend itself to a regulator.
>
> ---
> **Status:** ☐ Not started · ☐ In progress · ✅ Covered
> *Last updated: 2026-09-14*
>
> ---
> **One diagram required. Both brief + detail must exist with ≥1 mermaid each before ✓.**
