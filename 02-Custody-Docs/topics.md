C1 — Foundations & Fundamentals (why custody exists, 0-to-1 concepts)
- What is custody? 
- What is asset management?
- Why do banks need custody? (client safety, regulatory, revenue)
- The asset lifecycle: why custody is the safekeeping backbone
- Securities vs cash vs commodities vs crypto/digital assets
- Custody vs Asset Management vs Asset Servicing vs Fund Administration (boundaries)
- Client types: retail, institutional, asset managers, pension funds, insurance, sovereigns, HNW
- The value proposition / revenue (fees: custody fees, transaction fees, servicing fees)
- Key participants in the custody universe

C2 — Core Domain Concepts & Vocabulary (the glossary layer)
- Safekeeping
- Settlement
- Reconciliation
- Corporate Actions
- Dividend / distribution processing
- Borrowing & lending (securities lending)
- Collateral management
- Valuation / pricing
- Reinvestment
- Break / exception management
- Demat / DVP / FOP
- ISIN / CUSIP / SEDOL / Bloomberg ticker
- Omnibus vs segregated accounts
- Beneficial owner vs legal owner
- Transfer agent
- Central Securities Depository (CSD)
- CSD, CCP, Trade Repository
- Nominal registration / Global registration
- Street hierarchy / custodian hierarchy
- Sub-custody
- Local custody

C3 — Business Flows (end-to-end processes)
- Onboarding a custodian client / account setup
- Deposit / receipt of assets (inbound)
- Settlement & trade lifecycle (T+1/T+2)
- Inbound & outbound payments (affiliates)
- Corporate actions processing
- Dividend and distribution flows
- Securities lending & repo flows
- Borrow/lend collateral (tri-party)
- Collateral & cash management
- Valuation & reporting
- Reconciliation & exception handling
- Withdrawal / redemption flows
- Client reporting & statement generation
- Break management workflow

C4 — Regulatory & Compliance
- Global custodian regulations: SEC, FCA, CMA, MAS, HKMA, DFSA
- MiFID II (client asset rules)
- CSDR (Central Securities Depositories Regulation)
- CSDP (Central Securities Depositories Regulation - PRR)
- EMIR (derivatives reporting CCPs)
- SEC / FINRA / SIPC (US)
- FCA CLIENT, CASS (UK)
- Basel III (operational risk, counterparty, leverage)
- ICRS (International Custody Rules / IOSCO)
- FATCA / CRS (tax reporting)
- AML / KYC / CDD
- Sanctions / screening
- GDPR / data privacy for client assets
- DORA (Digital Operational Resilience Act)
- CSDR (securities settlement)
- Settlement discipline / fail reporting
- AIFMD (Alternative Investment Fund Managers Directive)
- UCITS
- MiFID II transaction reporting
- AML/KYC for asset managers
- MiFID II client asset segregation
- Tax reporting (FATCA, CRS)
- Operational risk & outsourcing

C5 — Technology & Architecture (relevant to EA)
- Custody core systems (C1: e.g., Charles Schwab Custodian, State Street Apex, BNY Mellon, J.P. Morgan, Citco, SS&C, etc. — vendor landscape)
- CSD interfaces (DTC, Euroclear, Clearstream, CDP, NSDL, CDSL, HKSCC, CCASS, ASX)
- Settlement messaging: ISO 15022, ISO 20022, SWIFT, SIF/MT300, MT3xx
- Trade lifecycle messaging
- Corporate actions feeds (ISS, BLOOMBERG, FACTORY)
- Securities master data management (ISIN/CUSIP/SEDOL)
- Reconciliation engines
- Borrowing & lending platforms (CSL, eSpeed, SFT, Tri-party)
- Collateral management (tri-party vs bi-party)
- Valuation & pricing engines (BVAL, Bloomberg BVAL / FDS, ICE Data Services / Markit)
- Position & transaction ledgers
- Reporting (client statements, valuation reports, regulatory reports)
- Cloud & on-prem trade-offs in custody
- API-first / open API (custodian APIs, C3, Citi Open, Schwab)
- Event-driven architecture for corporate actions
- Real-time vs end-of-day reconciliation
- High availability for settlement cut-offs
- Data model: Account, Instrument, Position, Transaction, Corporate Action, Collateral, Loan
- Integration patterns (CSD, CCPs, sub-custodians, asset managers, trade management systems)
- Security and access control for client asset movement

C6 — Value, Revenue & Financials
- Custody revenue streams: custodial fees (b.p. on AUM), transaction fees, servicing fees, borrowing & lending fees, collateral management fees, reporting fees
- Fee drivers and revenue per asset class
- AUM vs NII (Net Interest Income)
- Cost drivers (settlement ops, regulatory compliance, sub-custody)
- Revenue by client segment (institutional vs retail)
- Profit margins and cost-income ratio in custody
- Competitive landscape and fee benchmarks
- The "custody moat" (stickiness, data, regulatory license)
- Cross-sell and value-added services (asset-backed lending, private markets, digital assets)
- Market sizing ($ trillions in AUM, market cap of custodian market)
- KPIs: AUM growth, revenue per account, cost per unit, retention
- Strategic value to the bank: franchise value, relationship, data, cross-sell
- Impact on the bank's franchise: balance sheet, regulatory capital, operational risk concentration

C7 — Organizational & Operational Model
- Where custody sits in the bank (wealth mgmnt, asset mgmt, investment banking, operations, back office)
- Org structure: front office (sales, onboarding), middle office (risk, compliance, valuation, reconciliation), back office (settlement, corporate actions, ops)
- Operations: straight-through-processing (STP) rates, break rates, operational exceptions
- SLAs / KPIs: settlement fail rate, reconciliation match rate, corporate actions accuracy, break rate, processing turnarounds
- People & roles: custody ops, securities ops, collateral ops, sub-custody relationship management, client service, regulatory reporting
- Risk management in custody: operational risk, market risk (collateral), credit risk (counterparty), settlement risk (Herstatt)
- Business continuity and disaster recovery (critical: client assets)
- Vendor management / sub-custody management
- Quality and audit readiness (SOX, internal audit)
- Change management and release to production (regulatory reports)

C8 — Emerging & Advanced (frontier)
- Digital assets & tokenized securities custody (crypto custody, smart wallets, MPC)
- T+0 / same-day settlement (DTCC Daylight 24)
- ISO 20022 migration
- Real-time settlement and real-time corporate actions
- Blockchain / DLT for custody and settlement (e.g., R3, Corda, Hyperledger)
- AI/ML in operations (exception prediction, reconciliation matching, client servicing)
- Open API economy and custody platform as a service
- Cloud / multi-region deployment for global custody
- ESG data and ESG custody services
- Private markets custody (private equity, hedge fund, real estate)
- Cross-jurisdictional regulatory harmonization
- Central bank digital currencies (CBDC) impact on custody
- Tokenized real-world assets (RWA)
- Data mesh for custody data (positions, valuations)
- Quantum-safe cryptography (PQC) for custody communications
- Sustainable / low-carbon custody operations

C9 — Frameworks, Capability & Governance
- Capability mapping for custody (value stream + capability)
- Value stream: Onboard → Receive → Hold → Settle → Corporate Action → Borrow/Lend → Report
- Business architecture for custody (ArchiMate/BIZBOK)
- Reference architectures for custody platforms
- Technology landscape and integration map
- Application portfolio and rationalization (legacy core vs modernization)
- Vendor evaluation framework
- Maturity model (STP, cloud, API, data)
- Governance and decision rights (committee, change advisory)
- Regulatory compliance as governance (Basel, IOSCO, local)
- KPIs and maturity assessment
- Center of Excellence for custody technology
- Portfolio roadmap and build vs buy
- Standards adoption (ISO 20022, SIF, etc.)
- EA view: As-Is / To-Be, current vs target capability, gaps

C10 — Cross-cutting, Integration & Ecosystem
- Relationship to other bank lines (wealth, retail, investment banking, asset mgnt)
- Cross-sell and integrated client experience
- Integration with trade management (Aladdin, SIMS)
- Integration with middle office (risk, valuation)
- Data flows between custody and other lines
- Client onboarding / KYC integration
- Master data (instrument, counterparty)
- Regulatory reporting integration
- Client communication channel (portal, API, SFTP)
- Multi-custodian / sub-custody network

C11 — Worked scenarios and "Elite" differentiators
- Typical day in a custody ops (day-to-day flow)
- Onboarding a global asset manager (walkthrough)
- T+0 corporate action handling (walkthrough)
- Settlement failure (break) resolution (walkthrough)
- Cross-border custody chain (walkthrough)
- Digital asset onboarding (walkthrough)
- Client valuation dispute (walkthrough)
- Borrow & Lend collateral optimization (walkthrough)

Actually let me not over-fragment. Let me target ~8-10 categories with ~8-12 topics each, to match 01-Architecture-Docs scale (96 topics total). Custody-specific so it should be a bit different.

Let me design:

C1 — Foundations & Why Custody Exists (8 topics, foundational ●)
- C1-01 What is Custody? (Definition, role, value)
- C1-02 What is Asset Management? (AM vs Custody, boundaries)
- C1-03 Why do banks need Custody? (Safety, regulation, revenue, trust)
- C1-04 Custody within the bank (where it sits, org position)
- C1-05 Custody value chain (Onboard→Hold→Serve→Report)
- C1-06 Client segments and their needs (institutional, HNW, retail, sovereign, pension, insurance)
- C1-07 Custody vs Asset Servicing vs Fund Administration (boundaries)
- C1-08 Key vocabulary & glossary (safekeeping, settlement, CSD, ISIN, omnibus, sub-custodian)

C2 — Core Domain Concepts & Objects (10 topics, core ◑)
- C2-01 Accounts and ownership models (segregated, omnibus, nominee, beneficial)
- C2-02 Instruments and master data (ISIN, CUSIP, SEDOL, Bloomberg; equity, bond, fund, derivative, private, digital)
- C2-03 Positions and valuations (market value, cost, accrued, P&L)
- C2-04 Transactions and ledger (trade, settlement, collateral, loan events)
- C2-05 Settlement lifecycle (T+1/T+2, DVP, FOP, settlement fails)
- C2-06 Corporate actions (ex-dividend, split, merger, tender offer, spin-off)
- C2-07 Dividends and distributions
- C2-08 Borrowing & lending (stock loan, repo, securities lending economics)
- C2-09 Collateral & cash management (tri-party, haircuts, reinvestment)
- C2-10 Breaks and exceptions (what they are, why they matter, SLAs)

C3 — End-to-End Business Flows (10 topics, core ◑)
- C3-01 Client onboarding and account setup (KYC, sub-custodian, agreements)
- C3-02 Inbound assets and safekeeping (receipt, safekeeping)
- C3-03 Trade settlement flow (exec→settle→report, DVP/FOP)
- C3-04 Outbound and inbound payments (affiliates)
- C3-05 Corporate actions processing flow (notice → record → instruction → cash)
- C3-06 Securities lending & repo flow (borrow/lend, collateral, return)
- C3-07 Collateral optimization flow (tri-party, margin, reinvest)
- C3-08 Valuation and client reporting
- C3-09 Reconciliation and exception management
- C3-10 Withdrawal and account closure

C4 — Regulatory, Compliance & Standards (12 topics, mixed)
- C4-01 IOSCO and global custodian standards (IOSCO 34, CPM 3)
- C4-02 MiFID II (client assets, transaction reporting)
- C4-03 CSDR / CSD (EU settlement, fail, CSDR PRR)
- C4-04 EMIR, CCPs and derivatives reporting
- C4-05 SEC / FINRA / SIPC (US) 
- C4-06 FCA (CLIENT, CASS, UKMiFID II)
- C4-07 Basel III (custody operational risk, counterparty)
- C4-08 AML / KYC / CDD for custody clientele
- C4-09 Sanctions and trading restrictions
- C4-10 FATCA / CRS (tax reporting)
- C4-11 GDPR and data privacy for client assets
- C4-12 DORA (Digital Operational Resilience)

C5 — Technology & Architecture (12 topics, advanced ○)
- C5-01 Custody core system landscape (SS&C, Citadel, Citi, JPM, BNY, State Street, Citco, Schwab)
- C5-02 Reference architecture (modules: onboarding, core custody, collateral, borrow, corp actions, reporting)
- C5-03 CSD integration (DTC, Clearstream, Euroclear, NSDL, CDSL, HKSCC, CCASS)
- C5-04 Settlement messaging (MT3xx, SIF, ISO 20022, SWIFT)
- C5-05 Corporate actions feeds (ISS, Bloomex, FactSet, Refinitiv)
- C5-06 Securities master data management
- C5-07 Reconciliation engines (position, transaction, cash, collateral)
- C5-08 Borrowing & lending platforms
- C5-09 Collateral management & optimization
- C5-10 Valuation & pricing engines (BVAL, FDS)
- C5-11 Reporting and client portal
- C5-12 Security, access control and settlement cut-off resilience

C6 — Data Architecture & Models (8 topics)
- C6-01 Core data model (Account, Instrument, Position, Txn, Corp Action, Loan, Collateral)
- C6-02 Position & transaction ledger design
- C6-03 Master data (ISIN/CUSIP, counterparty, instrument attributes)
- C6-04 Event-driven data (corporate actions, breaks, exceptions)
- C6-05 Real-time vs end-of-day data
- C6-06 Lineage and audit trail
- C6-08 Data mesh for custody analytics
- C6-09 Data quality and SLAs

C7 — Financials, Revenue & Business Value (8 topics)
- C7-01 Custody revenue streams (b.p. fees, transaction, lending, reporting)
- C7-02 Fee drivers and benchmarks by asset class
- C7-03 Cost model & KPIs (STP rate, break rate, ops cost per lot)
- C7-04 AUM, NII and franchise value
- C7-05 Competitive landscape (market size, market share, fee compression)
- C7-06 The custody moat (stickiness, data, regulatory license)
- C7-07 Cross-sell and value-added services
- C7-08 Strategic value to the bank (balance sheet, regulatory capital, cross-sell)

C8 — Operations, Risk & Governance (10 topics)
- C8-01 Operations model (front/middle/back office in custody)
- C8-02 Straight-Through-Processing (STP) and automation
- C8-03 Break management (settlement breaks, ops exceptions)
- C8-04 SLAs and KPIs (settlement fail rate, reconciliation match, turnarounds)
- C8-05 Risk management in custody (operational, market, credit, settlement/Herstatt)
- C8-06 Business continuity & DR (critical: client assets, settlement cut-offs)
- C8-07 Vendor and sub-custody management
- C8-08 Audit readiness and SOX for custody
- C8-09 Change management and production releases
- C8-10 Capability map and governance (value stream + capability)

C9 — Emerging & Frontier (10 topics)
- C9-01 Digital asset custody (crypto, smart wallets, MPC)
- C9-02 Tokenized securities / RWA custody
- C9-03 T+0 / same-day settlement (Daylight 24)
- C9-04 ISO 20022 migration
- C9-05 DLT / blockchain custody
- C9-06 AI/ML in custody ops
- C9-07 Open APIs and platform economy
- C9-08 Cloud / multi-region and low-carbon custody
- C9-09 Private markets custody (PE, hedge funds, real estate)
- C9-10 Quantum-safe cryptography (PQC) in custody