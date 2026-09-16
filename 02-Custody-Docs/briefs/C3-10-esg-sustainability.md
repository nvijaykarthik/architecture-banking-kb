# C3-10 ESG, SFDR, TCFD: sustainability and reporting obligations — BRIEF
> **Category:** Cx — Regulatory & Compliance · **Difficulty:** ● · **Banking-relevant:** yes / 💳
>
> **One-liner:** _{ESG (Environmental, Social and Governance) integrates sustainability factors into investment decisions, while SFDR (Sustainable Finance Disclosure Regulation) and TCFD (Task Force on Climate-related Financial Disclosures) create mandatory reporting obligations for financial institutions to disclose how sustainability and climate risks are priced into portfolios and business models._
>
> **Why an enterprise architect / trainee cares:** _{If you cannot model sustainability risk as a first-class property of the custody data topology, you cannot answer regulator questions, cannot build SFDR Principal Adverse Impacts (PAI) dashboards, and cannot demonstrate TCFD governance to the board. The rulebook is not optional; the data architecture must prove compliance._
>
> ## Quick definition
> _ESG is a taxonomy of non-financial risk factors—environmental (carbon, water, biodiversity), social (labour standards, community impact), and governance (board independence, anti-corruption)—that materially affect long-term asset returns. SFDR is EU legislation requiring financial firms to disclose sustainability-related information in pre-contractual and periodic communications. TCFD is a G20-endorsed framework mandating disclosure of governance, strategy, risk management, and metrics/targets related to climate-related financial risks._
>
> ## Key ideas / terms
> - **SFDR Level 1:** Pre-contractual disclosures on sustainability risks; no mandatory taxonomy alignment.
> - **SFDR Level 2:** Ongoing periodic disclosures; requires principal adverse impacts (PAI) indicator monitoring.
> - **SFDR Article 8 / 9:** Two product-level regimes—Article 8 must promote environmental/social characteristics; Article 9 must pursue sustainable development as a measurable objective.
> - **TCFD Four Pillars:** Governance, Strategy, Risk Management, Metrics & Targets—disclosing both transition and physical climate risks.
> - **PAI Indicators:** 14 mandatory adverse-impact metrics (e.g., GHG emissions, carbon footprint, exposure to fossil fuel reserves).
> - **EU Taxonomy:** Environmental contribution criteria; "do no significant harm" (DNSH) for six environmental objectives.
>
> ## The mental model
> _Sustainability reporting is an added regulatory layer on top of the existing custody operations, transaction-reporting, and KYC / AML pipeline. The custody system must tag every holding with eligibility status (taxonomy-aligned or not), calculate PAI exposure at the portfolio and product level, and feed TCFD metrics into enterprise risk dashboards. The architecture challenge is to enrich instrument data, to map ownership chains to ultimate beneficial owners, and to emit audit-ready disclosures to regulators without breaking performance or latency budgets._
>
> ## One diagram (mandatory)
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     A[SFDR / ESG / TCFD Reporting Layer]:::critical --> B[Custody Operation]:::core
>     B --> C[Global Custody CWG]:::context
>     B --> D[Middle Office]:::context
>     B --> E[Asset Servicing]:::context
>     C --> F[Daily Custody Report]:::core
>     D --> G[NAV / Valuation Data]:::core
>     E --> H[Proxy Voting / Corporate Actions]:::context
> ```
> ```
>
> ## When to use / when NOT to use
> - ✅ **Use when:** Building a new custody platform or product; onboarding an ESG-focused client; integrating a third-party sustainability data provider.
> - ⚠️ **Avoid when:** You are modelling a vanilla cash-collateral book with no equity or fixed-income exposure; the taxonomy mapping tables are not yet stable; the regulator has not issued specific SFDR nation-country guidelines.
>
> ## Banking example
> _A global custodian sells a fund structured as an Article 9 "sustainable investment" to an EU UCITS manager. The custodian must: (1) filter holdings to only taxonomy-aligned bonds, (2) calculate Scope 3 carbon intensity per portfolio, (3) emit PAI indicators quarterly to the PRI signatory, (4) map the fund's entire ownership chain to verify no conflict-of-interest in proxy votes on climate resolutions, and (5) aggregate TCFD-aligned governance disclosures into the EU's Digital Product Passports. Failure on any step triggers suspension of the fund's UCITS passport under national competent authority rules._
>
> ## Common confusions (don't mix these up)
> - **SFDR vs EU Taxonomy:** SFDR is a *disclosure* and *product-label* regime; the Taxonomy is a *technical screening criteria* for what counts as "environmentally sustainable."
> - **TCFD vs Roadmap on Reporting:** TCFD is a *voluntary* (but de-facto mandatory for many jurisdictions) *disclosure framework*; not all regulators have transposed it into law yet.
> - **ESG vs Impact investing:** ESG is risk management and integration; impact investing deliberately seeks measurable positive outcomes beyond risk-adjusted returns.
>
> ## Interview / recall prompt
> _"Explain ESG, SFDR, and TCFD reporting obligations in 2 minutes without notes."_ →
> - _ESG as the risk taxonomy and its three pillars._
> - _SFDR as the EU product-label and disclosure regime with Level 1, 2, Article 8, and 9._
> - _TCFD as the G20 four-pillar climate-risk disclosure framework._
> - _PAI indicators as mandatory adverse-impact metrics_
> - _The custody system's role: tagging, calculating, and evidencing compliance._
>
> ## Status
> ☐ Not started · See detail doc: `details/C3-10-esg-sustainability.md`
>
> ---
> **One diagram required. Both brief + detail must exist before ✓.**
