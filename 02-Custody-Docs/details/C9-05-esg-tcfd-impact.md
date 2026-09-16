# [C?] [Topic Name] — DETAIL
> **Category:** C9 — Strategic Themes · **Difficulty:** ● · **Banking-relevant:** yes / 💳
> **Companion brief:** `briefs/C9-05-esg-tcfd-impact.md`
> > **Target reader:** enterprise architect who must explain, justify, and defend the topic — not just recite it.
>
> ---
>
> ## 1. Precise definition
> TCFD, published by the Financial Stability Board, is a recommendations-based framework for voluntary, consistent, and clear disclosure of climate-related financial risks. In the custody context, compliance means systematically identifying, assessing, and reporting the exposure of client portfolios and the custodian’s own operations to climate transition and physical risks, backed by scenario analysis and governance evidence.
>
> ## 2. Why it exists (the problem it solves)
> Climate risk was previously treated as a philanthropic or reputational concern. Since 2015, it has become a material financial risk: stranded assets, carbon-pricing liabilities, and physical damages to collateral. Custodians without TCFD-aligned processes face (a) regulatory sanctions from the FCA/ECB, (b) client attrition to competitors with better ESG reporting, and (c) untested counterparty risk in collateral chains.
>
> ## 3. Core concepts & vocabulary
> | Term | Precise meaning |
> |------|-----------------|
> | TCFD Governance | Board and management oversight of climate risk strategy and disclosure commitments. |
> | Transition Scenarios | Stress-test narratives for a 2°C, 1.5°C, or 4°C world used to assess portfolio resilience. |
> | ETRM | Enterprise Treasury and Risk Management; often the functional owner of climate exposure reporting. |
> | Scope 3 Dilution | The challenge that a custodian’s highest emissions exposure lies in the value chain of issuers, not its own electricity bill. |
> | As-of-date attestation | Third-party verification that pipeline emissions data are accurate at a specific reporting date. |
>
> ## 4. How it works (architecture / mechanism)
> The architecture is a four-stage pipeline: (1) data ingestion from issuer disclosures, vendor ratings (MSCI, Sustainalytics), and satellite imagery; (2) position normalization mapping each holding to a carbon identifier; (3) aggregation and scenario analysis across client portfolios; (4) report generation and audit-trail storage. Each stage is a data product owned by the climate-risk function, surfaced through APIs consumed by ETRM and client portals.
>
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     Ingestion[Ingestion<br/>ESG Feeds + Issuers]:::context --> Normalize[Position Normalization<br/>Carbon Mapping]:::core
>     Normalize --> Aggr[Portfolio Aggregation]:::core
>     Aggr --> Scenario[Scenario Analysis<br/>2°C / 4°C]:::critical
>     Scenario --> Report[TCFD Report<br/>Generator]:::critical
>     Report --> Archival(Immutable Audit Log):::context
>     Archival --> ClientPortal[Client Risk Dashboard]:::context
> ```
>
> ## 5. Variants, options & trade-offs
> | Variant | When to pick | When to avoid | Key trade-off axis |
> |---------|--------------|---------------|--------------------|
> | Vendor-managed ESG | You need fast time-to-market and have capital to pay for data feeds. | You need issuer-level original data for regulator-level granularity. | Speed vs. granularity. |
> | Self-built ESG | You have internal research and want to own the methodology. | You lack the compute to refresh emissions data monthly. | Control vs. capex. |
> | Scenario-only reporting | Show TCFD alignment without full Scope 3 granularity. | Client demands proof of physical-risk linkage. | Compliance vs. completeness. |
>
> ## 6. Relationships to sibling topics
> - **C3–07 Financial Crime:** Climate-risk due-diligence can flag front-running; ESG data breaches may be classified as cyber incidents under DORA.
> - **C2–09 Proxy Voting:** Shareholder voting agendas now frequently include climate resolutions; custody platforms must integrate proxy-voting workflows with ESG scoring.
> - **C1–05 Custody Value Chain:** Climate data is a new service layer that monetizes between commission generation and settlement cost.
>
> ## 7. Banking / financial-services context 💳
> A Dutch custody bank under ECB DORA Annex III requirements establishes a TCFD workstream. The bank purchases a vendor dataset of issuer-level Scope 1/2/3 emissions, maps roughly 1.2 million positions to these identifiers, and runs a 2°C transition scenario using a stochastic Monte-Carlo simulation. The output reveals a €400m book of coal-exposure that triggers a client-communication campaign and a covenant-review policy. A failure mode not modelled is the sudden insolvency of the emissions-data vendor, which the bank mitigates through a primary-and-secondary vendor model.
>
> ## 8. Reference architecture / worked example
> The Dutch custody bank above is the canonical worked example: a four-stage pipeline ingesting ESG data, mapping carbon, running scenario analysis, and generating a TCFD report. The immutability of the audit log satisfies both DORA and FCA requirements.
>
> ## 9. Maturity & adoption signals
> - **Adopt when:** The bank has a board-mandated net-zero policy and an ETRM team already owning climate-risk appetite statements.
> - **Anti-signals:** The custodian still reconciles holdings monthly on a spreadsheet.
> - **Common failure modes:** (1) Vendors publish inconsistent Scope 3 estimates; (2) Scenario assumptions are not stress-tested; (3) Reports are static PDFs, not living data products.
>
> ## 10. Common confusions — the "don't mix" list
> | Often confused | Real distinction |
> |----------------|------------------|
> | TCFD vs. CSRD | TCFD is a principles-based disclosure framework; CSRD is a mandatory EU reporting directive that adopts TCFD metrics for large filers. |
> | ESG ratings vs. physical risk | ESG ratings are qualitative forward-looking grades; physical risk is a quantitative forward-looking estimate of climate-event losses. |
>
> ## 11. Tools & standards to know
> - **Frameworks / TOGAF:** Business Architecture (governance), Application Architecture (data-product pipeline), and Data Architecture (emissions data model).
> - **Common tooling:** Snowflake / Databricks for compute; FactSet / Bloomberg ESG for data feeds; Python (PyPortfolioOpt, Scikit-learn) for scenario math; Archi or Sparx EA for documentation.
> - **Mandatory reading:** TCFD 2017 Final Report, EU CSRD L2 Draft Delegated Regulation, FSB Climate-related Financial Disclosures 2020.
>
> ## 12. ADR template (ready to fill in)
> ```markdown
> # ADR-02: TCFD-Compliant Custody Reporting
> ## Status
> Proposed
> ## Context
> ECB DORA and FCA rules now require climate-risk disclosure; our current holdings data lack issuer-level carbon identifiers.
> ## Decision
> Purchase vendor ESG data, build a carbon-mapping normalization layer, and deliver TCFD reports quarterly via a live API.
> ## Consequences
> - Positive: Exceeds regulatory minimum, supports net-zero lending.
> - Negative: Vendor concentration risk, ongoing data-refresh cost.
> - ...
> ## Alternatives considered
> 1. Self-build emissions database.
> 2. Static annual PDF reporting.
> ```
>
> ## 13. Practice — apply it
> 1. **Recall:** Define TCFD-aligned custody in 2 min without notes.
> 2. **Model:** Produce an ArchiMate/UML diagram from scratch for the architecture above.
> 3. **ADR:** Write a decision doc applying it to the Dutch custody example in §7.
> 4. **Defend:** Roleplay explaining it to a non-technical CRO / CIO.
>
> ## Summary
> TCFD turns custody from a passive safekeeping function into a climate-risk intelligence platform. Compliance is now a baseline; competitive advantage comes from integrated physical-risk scenario analytics and real-time client transparency. The architectural investment is in data-ingestion, position normalization, and audit-trail immutability.
>
> ---
> **Status:** ☐ Not started · ☐ In progress · ✅ Covered
> *Last updated: 2025-07-09*
>
> ---
> **One diagram required. Both brief + detail must exist with ≥1 mermaid each before ✓.**
