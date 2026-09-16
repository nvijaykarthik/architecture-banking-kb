# [C?] [Topic Name] — BRIEF
> **Category:** C9 — Strategic Themes · **Difficulty:** ● · **Banking-relevant:** yes / 💳
> **One-liner:** ESG and TCFD disclosures force custodians to price climate risk, track carbon-footprint per portfolio, and embed scenario analysis into investment governance.
> **Why an enterprise architect / trainee cares:** Architects must extend the custody value-chain with climate-risk data stores, integration to external ESG feeds, and scenario-analysis compute pipelines.
>
> ## Quick definition
> TCFD-mandated climate-risk reporting requires custodians to disclose how carbon exposure and transition pathways affect portfolio value, while ESG data streams enrich investment decisions with non-financial attributes.
>
> ## Key ideas / terms
> - **TCFD:** Task Force on Climate-related Financial Disclosures; a framework for climate risk governance, strategy, risk management, and metrics.
> - **Scope 1/2/3:** Emissions categories; custodians primarily report Scope 2 (indirect energy) and Scope 3 (value-chain) exposure.
> - **Transition risk:** Financial impact from shifting to a low-carbon economy (policy, litigation, technology).
> - **Physical risk:** Financial impact from climate events (acute and chronic).
>
> ## The mental model
> Climate data is a new asset class layer sitting above holdings. The custody data model must therefore evolve from an investor-client-security graph to an investor-client-security-carbon-footprint graph. This is analogous to enhancing a customer-360 with behavioral data, except the source is external, volatile, and often incomplete. The governance angle is dual: regulators (FCA, ECB DORA Annex III) demand disclosure; clients demand actionable analytics.
>
> ## One diagram (mandatory)
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     Client[Client Portfolio]:::critical --> Custody[Custody Ledger]:::core
>     Custody --> Holding[Security Holdings]:::core
>     Holding --> Carbon[Carbon Footprint<br/>Attribution]:::core
>     Carbon --> TCFD[TCFD Disclosure<br/>Engine]:::critical
>     Holding --> ESG[ESG Data Feed<br/>Provider]:::context
>     Sponsor[Sponsor / Custodian]:::context --> ESG
>     Sponsor --> Policy[Investment Policy]:::context
>     Policy --> TCFD
> ```
> ```
>
> ## When to use / when NOT to use
> - ✅ **Use when:** Your bank is subject to FCA climate-risk disclosure rules or has committed to net-zero lending goals.
> - ⚠️ **Avoid when:** You are a small custodian with no climate-research team and the cost of data feeds exceeds margin.
>
> ## Banking example
> A UK custody bank publishes TCFD-aligned disclosures under the FCA’s 2021 disclosure rules. The bank ingests issuer-level Scope 1/2/3 emissions from a third-party provider, maps them to client holdings, and runs two scenario analyses—2°C transition and 4°C physical—using a portfolio-level stochastic model. The output feeds the annual FCA climate report and client risk dashboards.
>
> ## Common confusions (don't mix these up)
> - **ESG ratings vs. TCFD:** ESG ratings are forward-looking assessments of company sustainability; TCFD is a backward-looking governance and disclosure framework, not a rating.
>
> ## Interview / recall prompt
> "Explain why ESG and TCFD matter for custody in 2 minutes without notes."
> - Governance: regulator-driven.
> - Data: emissions + portfolio mapping.
> - Risk: transition vs physical.
>
> ## Status
> ☐ Not started · See detail doc: `details/C9-05-esg-tcfd-impact.md`
