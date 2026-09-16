# C1 how custody makes money — DETAIL
> **Category:** C1 Foundations · **Difficulty:** ◑ · **Banking-relevant:** yes / 💳
>
> **Companion brief:** `briefs/C1-06-revenue-model.md`
> >
> > **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.
>
> ---
>
> ## 1. Precise definition
> Custody economics is the set of contractual and operational revenue and cost structures that arise when an asset owner delegates safekeeping, book-entry administration, and corporate-action support to a custodian. Revenue streams are: (a) fixed safekeeping fees charged per account or per AUM (annually, semi-annually); (b) variable securities-lending fees (fixed component + rebate subscription), which are typically 40–60 % of total revenue for large custody banks; (c) withholding-tax capture and reclaim programmes made possible by DTA treaties; (d) transaction charges (settlement, FX, ADR/GDR issuance); (e) fee waivers for institutional clients that trade volume. Costs are: (1) infrastructure (CSD connectivity, mainframe, cloud), (2) compliance (KYC, AML, tax-withholding tracking), (3) people (investment-operations, dispute-resolution, legal), (4) credit risk (client default, cash collateral).
>
> ## 2. Why it exists (the problem it solves)
> Custody did not start as a for-profit utility. Banks held assets because they already held the client deposit account (relationship banking). When asset management grew in the 1980s, asset managers needed a secure, neutral depot account. The custodian solved the *principal-agent* problem by centralising record-keeping and by providing *collateral management* for securities lending. Without a revenue model, there is no incentive to invest in the real-time book-entry, DTA engines, and reconciliation automation that regulators now demand.
>
> ## 3. Core concepts & vocabulary
> | Term | Precise meaning |
> |------|-----------------|
> | Rebate | The portion of the lending fee returned (paid back) to the asset owner; the publisher keeps the rest as the lending income. |
> | Hard-to-borrow | A share for which demand from borrowers exceeds supply; the owner can charge a premium lending fee. |
> | Cash   substitute | Used when physical settlement is impractical (e.g., fractional shares, cert-lite issuers); cash collateral is paid instead. |
> | AUM | Assets Under Management; the base against which safekeeping fees are often calculated. |
> | Drag | Net revenue minus cost; the "profit" of the custody line, often expressed as a percentage of AUM.
>
> ## 4. How it works (architecture / mechanism)
> The revenue model is a fee-calculation engine that takes as input: client type (retail vs institutional), asset class, geography, and regulatory regime, and outputs a periodic invoice. The engine must be *decomposed* because each fee line has a *different* domicile, settlement cycle, and regulatory treatment.
>
> ### 4.1 Diagrams
>
> **Diagram A — Core structure** (highlight load-bearing = amber, supporting = grey, context = light):
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     A[Onboarding]:::context --> B[Account]:::core
>     B --> C[Fee Engine]:::critical
>     C --> D[Pricing Service]:::core
>     D --> E[Invoice]:::critical
>     C --> F[Reconciliation]:::core
>     E --> G[Collection]:::core
>     G --> H[Investment Ops]:::critical
> ```
>
> **Diagram B — Lifecycle / flow** (highlight decision points = green, failures = red, money = gold, context = grey):
> ```mermaid
> flowchart LR
>     classDef ok fill:#a7f3d0,stroke:#065f46,color:#000
>     classDef risk fill:#fecaca,stroke:#991b1b,color:#000
>     classDef money fill:#fde68a,stroke:#92400e,color:#000
>     classDef context fill:#e5e7eb,stroke:#6b7280,color:#000
>     Start[Portfolio Created]:::context --> Analyze[AUM / Asset Mix]:::ok
>     Analyze -->|Stable| Held[Hold & Collect Safekeeping]:::critical
>     Analyze -->|Loanable| Lend[Lending Program]:::money
>     Lend -->|Demand > Supply| HardBorrow[Hard-to-borrow]:::risk
>     Lend -->|Normal| NormalLend[Standard Rebate]:::ok
>     Held --> Tax[Tax Withhold/Reclaim]:::critical
>     Tax -->|Yes| DTA[DTA Engine]:::critical
>     Tax -->|No| Next[Next Invoice]:::ok
>     Next --> Report[Reporting]:::ok
> ```
>
> **Diagram C — Data flow & cost pipeline** (highlight service = blue, data = gold, boundary = grey dashed):
> ```mermaid
> flowchart LR
>     classDef service fill:#bfdbfe,stroke:#1e40af,stroke-width:1px,color:#000
>     classDef data fill:#fde68a,stroke:#92400e,stroke-width:1px,color:#000
>     classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5
>     Client[Client ERP]:::service --> BRF[Billing Rules Engine]:::service
>     BRF --> FL[Fee Ledger]:::data
>     FL --> RE[Rebate Engine]:::service
>     RE --> SUI[Securities Lending Platform]:::service
>     SUI --> DTA[DTA Tax Engine]:::service
>     DTA --> RE
>     FL --> AP[Accounts Payable]:::service
>     AP --> CDP[Cost Distribution Pipeline]:::data
> ```
>
> ```
>
> ## 5. Variants, options & trade-offs
> | Variant | When to pick | When to avoid | Key trade-off axis |
> |---------|--------------|---------------|--------------------|
> | Percentage-of-AUM fee | Stable, long-term institutional mandates | Retail or cash-heavy portfolios where AUM is volatile | Predictability vs pricing sensitivity |
> | Fixed fee per account | Small accounts with limited activity | Large fund-of-funds with €10 bn+ in a single account | Unit economics vs relationship depth |
> | Rebate-only (no fixed fee) | Large asset managers with existing banking relationships | New entrants who need onboarding revenue to cover fixed costs | Revenue timing vs win-rate |
>
> ## 6. Relationships to sibling topics
> - **Custody value chain:** the chain is the *cost driver*; the revenue model is the *recovery mechanism*.
> - **Securities lending:** is the highest-margin revenue line; the value chain provides the inventory.
> - **Tax withholding:** is not a revenue line per se but a *value-retention* mechanism; the architect must keep the DTA engine isolated from the lending engine to prevent leakage.
>
> ## 7. Banking / financial-services context 💳
> The FCA, BaFin, and CSSF scrutinise custody revenue because perceived *front-running* or *collateral rehypothecation* (using client assets for the bank’s own funding) can trigger sanctions. The revenue model must be *transparent* and *segregated*, with claw-back clauses for failed trades or mispriced lending. MiFID II transparency rules require reporting of lending fees and rebates to the asset owner. The business consequence of opacity: a ban on securities lending in a major jurisdiction, destroying up to 30 % of a custody bank’s margin.
>
> ## 8. Reference architecture / worked example
> **Problem:** A custody bank wants to price a new "green-bond-only" custody solution.
>
> **Decision:** Apply a fixed €12 000 annual safekeeping fee + 0.8 % of AUM revenue, *waiving* lending fees because green bonds have low demand but generating DTA revenue from local withholdings.
>
> **Result:**
> - Safekeeping fee provides floor coverage.
> - AUM fee scales with portfolio growth.
> - DTA engine harvests local withholding at source.
> - Low lending revenue is acceptable because the client (ESG fund) does not want to lend.
>
> ```mermaid
> graph LR
>     classDef service fill:#bfdbfe,stroke:#1e40af
>     classDef data fill:#fde68a,stroke:#92400e
>     classDef boundary fill:#f1f5f9,stroke:#6b7280,stroke-dasharray: 5
>     Client[ESG Fund]:::service --> API[Green Custody API]:::service
>     API --> NLM[(Green Bond Ledger)]:::data
>     API --> BSF[Bundled Service Fee]:::service
>     NLM --> DTA[National DTA]:::service
>     BSF --> RE[Zero-Lending Ledger]:::data
> ```
>
> ## 9. Maturity & adoption signals
> - **Adopt when:** fee rules are codified, AUM feeds are near-real-time, and DTA engine is jurisdiction-specific.
> - **Anti-signals:** manual fee review in quarterly board meetings; invoices that only show "total fees" without line breakdown.
> - **Common failure modes:** (1) rebate leakage—SUI records collectible fees but cost engine underestimates infrastructure; (2) AUM double-counting—same AUM included in both safekeeping and lending; (3) DTA mismatch—tax reclaim filed in wrong jurisdiction, losing recovery.
>
> ## 10. Common confusions — the "don't mix" list
> | Often confused | Real distinction |
> |----------------|------------------|
> | Securities-lending fee | What the custodian charges the borrower. |
> | Rebate | What the asset owner receives from the custodian. |
> | Repo rate | Market benchmark; the custodian’s fee is the spread.
> | Withholding tax | Obligation to government; capture is the reclaim business.
>
> ## 11. Tools & standards to know
> - **Standards:** MiFID II Q&A on custody, EMIR, Basel III credit-risk framework, IOSCO Principles 12–16.
> - **Tooling:** Collateral Management Systems (e.g., IHS Markit IRMS), Tax Calculation Engines (e.g., Wolters Kluwer), Billing Platforms (e.g., MassMutual Financial).
> - **Mandatory reading:** "The Economics of Custody" (IFSL white paper); ECB Statistics on Securities Holdings.
>
> ## 12. ADR template (ready to fill in)
> ```markdown
> # ADR-02: Revenue Architecture for Open Custody Platform
> ## Status
> Proposed
> ## Context
> The open banking platform wants to offer custody by-the-API with transparent fee splits.
> ## Decision
> Microservice fee engine with domain-driven pricing, event-sourced ledger, and regulatory audit log.
> ## Consequences
> - Positive: transparency; negative: 3-year build.
> ## Alternatives considered
> 1. Off-the-shelf custodian API. 2. Embedded ERP module.
> ```
>
> ## 13. Practice — apply it
> 1. **Recall:** define in 2 min without notes.
> 2. **Model:** produce an ArchiMate/UML diagram from scratch showing the revenue pipeline.
> 3. **ADR:** write a decision doc applying it to the green-bond example in §8.
> 4. **Defend:** roleplay explaining it to a non-technical CFO.
>
> ## Summary
> Custody is a utility, but it is financed like a profit centre. The revenue model matters because it determines how much the business can invest in the technology和 governance that regulators demand. An architect who cannot explain which fee line pays for which platform component cannot defend the custody investment case.
>
> ---
> **Status:** ☐ Not started · ☐ In progress · ✅ Covered
> *Last updated: 2026-09-14*
>
> ---
> **One diagram required. Both brief + detail must exist with ≥1 mermaid each before ✓.**
