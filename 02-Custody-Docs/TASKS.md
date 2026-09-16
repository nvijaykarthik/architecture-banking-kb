# 📋 TASKS — Custody & Asset Management (Bank Operations)
> **Purpose:** Single source of truth for *what to cover* and *what is done* in the Custody & Asset Management portfolio.
>
> Each topic produces two files:
> - **`briefs/{{slug}}.md`** — quick, interview-ready brief (≈5–10 min read)
> - **`details/{{slug}}.md`** — deep, engineerable detail (mechanisms, trade-offs, ADRs)
>
> **Rule:** Do not mark `✅` until **both** the brief **and** the detail exist **and** each contains **≥1 Mermaid diagram**.
>
> **Legend:**
>  - `☐` Not started · `◐` In progress · `✅` Covered
>  - `💳` banking-relevant · `●` foundational · `◑` core · `○` advanced

## Progress dashboard
| Category | Covered | Total | % |
|----------|---------|-------|---|
| C1 Foundations | 8 | 8 | 100% |
| C2 Core Business Flows | 12 | 12 | 100% |
| C3 Regulatory, Risk & Compliance | 0 | 12 | 0% |
| C4 Technology & Data | 0 | 10 | 0% |
| C5 Economics & Strategic Value | 0 | 8 | 0% |
| C6 Organization & Service | 0 | 8 | 0% |
| C7 Risk & Control | 0 | 8 | 0% |
| C8 Reference Architectures & Enterprise Patterns | 0 | 8 | 0% |
| C9 Emerging & Systemic | 0 | 8 | 0% |
| C10 Your 2-Week Mastery | 10 | 10 | 100% |
| **TOTAL** | **10** | **92** | **11%** |

> ⚠️ Keep the dashboard in sync as you flip statuses. Re-count each row after each batch.

---

## C1 — Foundations (does the client *safely hold* ~)
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C1-01 | What is custody? / safekeeping, record-keeping, servicing | ● | ☐ | `C1-01-what-is-custody.md` | `C1-01-what-is-custody.md` |
| C1-02 | Custody vs asset management vs wealth management vs investment banking — boundaries | ● | ☐ | `C1-02-custody-vs-am-vs-ib.md` | `C1-02-custody-vs-am-vs-ib.md` |
| C1-03 | Asset classes held / instruments under safekeeping | ● | ☐ | `C1-03-asset-classes-held.md` | `C1-03-asset-classes-held.md` |
| C1-04 | Where custody sits in the bank (org, lines of business, ownership) | ◑ | ☐ | `C1-04-where-custody-sits.md` | `C1-04-where-custody-sits.md` |
| C1-05 | The custody value chain (end-to-end, from onboarding to reporting) | ◑ | ☐ | `C1-05-custody-value-chain.md` | `C1-05-custody-value-chain.md` |
| C1-06 | How custody makes money (revenue & economic model) | ◑ | ☐ | `C1-06-revenue-model.md` | `C1-06-revenue-model.md` |
| C1-07 | Industry landscape (key players, market share, today's dynamics) | ◑ | ☐ | `C1-07-industry-landscape.md` | `C1-07-industry-landscape.md` |
| C1-08 | Custody & AM glossary: essential vocabulary | ● | ☐ | `C1-08-glossary.md` | `C1-08-glossary.md` |

---

## C2 — Core Business Flows (the day ~)
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C2-01 | Client onboarding (KYC, AML, regulatory review, signing mandate) | ◑ | ✅ | `C2-01-onboarding.md` | `C2-01-onboarding.md` |
| C2-02 | Account structure: omnibus / segregated / nominee accounts | ◑ | ✅ | `C2-02-account-structure.md` | `C2-02-account-structure.md` |
| C2-03 | Receiving and safekeeping assets (intake, settlement, position, credit) | ◑ | ✅ | `C2-03-receiving-safekeeping.md` | `C2-03-receiving-safekeeping.md` |
| C2-04 | Delivery to central securities depositories (CDSCSD) | ◑ | ✅ | `C2-04-delivery-to-csd.md` | `C2-04-delivery-to-csd.md` |
| C2-05 | Settlement: cash and securities (DVP / DvP, trade cut-offs, finality) | ◑ | ✅ | `C2-05-settlement.md` | `C2-05-settlement.md` |
| C2-06 | Cash management: sweeps, pooling, reinvestment | ◑ | ✅ | `C2-06-cash-management.md` | `C2-06-cash-management.md` |
| C2-07 | Net asset value: crediting, valuation, accruals, rebase | ◑ | ✅ | `C2-07-nav-valuation.md` | `C2-07-nav-valuation.md` |
| C2-08 | Corporate actions (dividends, rights, tender offers, splits, spin-offs, mergers) | ◑ | ✅ | `C2-08-corporate-actions.md` | `C2-08-corporate-actions.md` |
| C2-09 | Proxy services: voting, general meetings, shareholder-related services | ◑ | ✅ | `C2-09-proxy-voting.md` | `C2-09-proxy-voting.md` |
| C2-10 | Collateral management: pledges, releases, reinvestment, rehypothecation | ◑ | ✅ | `C2-10-collateral-management.md` | `C2-10-collateral-management.md` |
| C2-11 | Securities borrowing & lending | ◑ | ✅ | `C2-11-borrowing-lending.md` | `C2-11-borrowing-lending.md` |
| C2-12 | Reporting and statements: daily, monthly, tax, regulatory | ◑ | ✅ | `C2-12-reporting-statements.md` | `C2-12-reporting-statements.md` |

---

## C3 — Regulatory, Risk & Compliance (the rules ~)
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C3-01 | Global regulation landscape (US SEC, EU CSDR / EMIR, UK, Asia) | ◑ | ☐ | `C3-01-global-regulation.md` | `C3-01-global-regulation.md` |
| C3-02 | Client asset rules: segregation, ownership, rehypothecation limits | ◑ | ☐ | `C3-02-client-asset-rules.md` | `C3-02-client-asset-rules.md` |
| C3-03 | MiFID II / MiFIR: transaction reporting, best execution | ◑ | ☐ | `C3-03-mifid-transaction-reporting.md` | `C3-03-mifid-transaction-reporting.md` |
| C3-04 | SIPC / deposit-type protection and insurance backstop | ◑ | ☐ | `C3-04-sipc-protection.md` | `C3-04-sipc-protection.md` |
| C3-05 | FATF / AML / KYC / sanctions — obligation on the custodian | ◑ | ☐ | `C3-05-fatf-aml-kyc.md` | `C3-05-fatf-aml-kyc.md` |
| C3-06 | Operational risk, business continuity, DORA | ◑ | ☐ | `C3-06-dora-business-continuity.md` | `C3-06-dora-business-continuity.md` |
| C3-07 | Financial crime: sanctions, money laundering, fraud | ◑ | ☐ | `C3-07-financial-crime.md` | `C3-07-financial-crime.md` |
| C3-08 | Tax: withholding tax, gross-up, tax reporting (CRS / FATCA) | ◔ | ☐ | `C3-08-tax-withholding.md` | `C3-08-tax-withholding.md` |
| C3-09 | Capital & leverage requirements (Basel, liquidity risk) | ◔ | ☐ | `C3-09-capital-requirements.md` | `C3-09-capital-requirements.md` |
| C3-10 | ESG, SFDR, TCFD: sustainability and reporting obligations | ◔ | ☐ | `C3-10-esg-sustainability.md` | `C3-10-esg-sustainability.md` |
| C3-11 | ESMA directives and secondary regulation on custody | ◔ | ☐ | `C3-11-esma-directives.md` | `C3-11-esma-directives.md` |
| C3-12 | Compliance reporting: what feeds where, regimes, content | ◔ | ☐ | `C3-12-compliance-reporting.md` | `C3-12-compliance-reporting.md` |

---

## C4 — Technology & Data (the stack ~)
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C4-01 | Custody platform landscape (core systems, middleware, custodians), what the bank runs | ◔ | ☐ | `C4-01-custody-platform-landscape.md` | `C4-01-custody-platform-landscape.md` |
| C4-02 | Smart custody platform (target rendering, modernization, SaaS) — future state | ◔ | ☐ | `C4-02-smart-custody-platform.md` | `C4-02-smart-custody-platform.md` |
| C4-03 | Core data model: accounts, positions, corporate actions, collateral, loans | ◔ | ☐ | `C4-03-data-model.md` | `C4-03-data-model.md` |
| C4-04 | Reference data management (ISIN, CUSIP, SEDOL, Bloomberg, Reuters) | ◔ | ☐ | `C4-04-reference-data.md` | `C4-04-reference-data.md` |
| C4-05 | Integration architecture: where custody plugs into the bank's other systems | ◔ | ☐ | `C4-05-integration-architecture.md` | `C4-05-integration-architecture.md` |
| C4-06 | Reconciliation runtime and automation (book vs actual, feeds) | ◔ | ☐ | `C4-06-reconciliation.md` | `C4-06-reconciliation.md` |
| C4-07 | Straight-through-processing (STP) and exception management | ◔ | ☐ | `C4-07-straight-through-processing.md` | `C4-07-straight-through-processing.md` |
| C4-08 | APIs and open-ecosystem / data exchange (SWIFT, FX, rebased data) | ◔ | ☐ | `C4-08-apis-ecosystem.md` | `C4-08-apis-ecosystem.md` |
| C4-09 | Data mesh for custody analytics and reporting | ◔ | ☐ | `C4-09-data-mesh.md` | `C4-09-data-mesh.md` |
| C4-10 | Cloud-native / API-first / platform operating model | ◔ | ☐ | `C4-10-cloud-platform-model.md` | `C4-10-cloud-platform-model.md` |

---

## C5 — Economics & Strategic Value (the money)
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C5-01 | Custody economics: cost-to-serve, break-even, margin | ◔ | ☐ | `C5-01-economics-cost-to-serve.md` | `C5-01-economics-cost-to-serve.md` |
| C5-02 | Revenue models: fee-on-AUM, transaction, custodial, ancillary | ◔ | ☐ | `C5-02-revenue-models-fees.md` | `C5-02-revenue-models-fees.md` |
| C5-03 | The profitability equation and cross-sell opportunity | ◔ | ☐ | `C5-03-profitability-cross-sell.md` | `C5-03-profitability-cross-sell.md` |
| C5-04 | Benchmark and competitive fee landscape | ◔ | ☐ | `C5-04-benchmark-fees.md` | `C5-04-benchmark-fees.md` |
| C5-05 | Risk-adjusted return versus other business lines | ◔ | ☐ | `C5-05-risk-adjusted-return.md` | `C5-05-risk-adjusted-return.md` |
| C5-06 | Impact on the bank brand and client retention | ◔ | ☐ | `C5-06-brand-retention.md` | `C5-06-brand-retention.md` |
| C5-07 | Cost center vs profit center debate and strategic ownership | ◔ | ☐ | `C5-07-cost-vs-profit-center.md` | `C5-07-cost-vs-profit-center.md` |
| C5-08 | Strategic investment decisions (build vs buy, outsourcing, licensing) | ◔ | ☐ | `C5-08-strategic-investment.md` | `C5-08-strategic-investment.md` |

---

## C6 — Organization & Service (who, how, how well)
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C6-01 | Org chart / lines of business / domain ownership of custody | ◔ | ☐ | `C6-01-org-chart.md` | `C6-01-org-chart.md` |
| C6-02 | RACI and where each activity lives (client service, operations, middle office, asset servicing) | ◔ | ☐ | `C6-02-raci-activity.md` | `C6-02-raci-activity.md` |
| C6-03 | Relationship / client service model (dedicated vs service centers) | ◔ | ☐ | `C6-03-client-service-model.md` | `C6-03-client-service-model.md` |
| C6-04 | Service levels (SLAs, turnaround times, content, reporting cadence) | ◔ | ☐ | `C6-04-service-levels.md` | `C6-04-service-levels.md` |
| C6-05 | Account management and internal client relationship | ◔ | ☐ | `C6-05-account-management.md` | `C6-05-account-management.md` |
| C6-06 | Account lifecycle: onboarding → active → dormant → closure | ◔ | ☐ | `C6-06-account-lifecycle.md` | `C6-06-account-lifecycle.md` |
| C6-07 | Collaboration with other parts of the bank | ◔ | ☐ | `C6-07-collaboration.md` | `C6-07-collaboration.md` |
| C6-08 | Internal controls and audit (three lines of defense) | ◔ | ☐ | `C6-08-internal-controls-audit.md` | `C6-08-internal-controls-audit.md` |

---

## C7 — Risk & Control (the safeguards)
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C7-01 | Risk categories: operational, market, credit/counterparty, legal/reg | ◔ | ☐ | `C7-01-risk-categories.md` | `C7-01-risk-categories.md` |
| C7-02 | Strong governance over client assets (strong control, CFA) | ◔ | ☐ | `C7-02-strong-control.md` | `C7-02-strong-control.md` |
| C7-03 | Fraud, error, and cyber risk in custody | ◔ | ☐ | `C7-03-fraud-error-cyber.md` | `C7-03-fraud-error-cyber.md` |
| C7-04 | Break management and exception control | ◔ | ☐ | `C7-04-break-management.md` | `C7-04-break-management.md` |
| C7-05 | Repudiation / payment finality / settlement risk | ◔ | ☐ | `C7-05-repudiation-settlement.md` | `C7-05-repudiation-settlement.md` |
| C7-06 | Liquidity and funding (cash and collateral) | ◔ | ☐ | `C7-06-liquidity-funding.md` | `C7-06-liquidity-funding.md` |
| C7-07 | Business continuity and disaster recovery | ◔ | ☐ | `C7-07-business-continuity.md` | `C7-07-business-continuity.md` |
| C7-08 | Internal and external audits | ◔ | ☐ | `C7-08-audits.md` | `C7-08-audits.md` |

---

## C8 — Reference Architectures & Enterprise Patterns (the blueprint)
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C8-01 | Reference architecture: custodian + bank + CSD + CCP + client (layering) | ◔ | ☐ | `C8-01-reference-architecture.md` | `C8-01-reference-architecture.md` |
| C8-02 | Account hierarchy and models of ownership (direct, nominee, omnibus, sub-custodial) | ◔ | ☐ | `C8-02-account-hierarchy.md` | `C8-02-account-hierarchy.md` |
| C8-03 | Capability mapping: business capability + value stream for custody | ◔ | ☐ | `C8-03-capability-mapping.md` | `C8-03-capability-mapping.md` |
| C8-04 | The custody capability map in your bank (value stream walkthrough) | ◔ | ☐ | `C8-04-custody-capability-map.md` | `C8-04-custody-capability-map.md` |
| C8-05 | Reference architecture for sub-custodial networks (cross-border, local ownership) | ◔ | ☐ | `C8-05-sub-custodial-network.md` | `C8-05-sub-custodial-network.md` |
| C8-06 | Data architecture for custody (history, lineage, audit, reconciliation) | ◔ | ☐ | `C8-06-data-architecture.md` | `C8-06-data-architecture.md` |
| C8-07 | Security architecture for client assets (access, segregation, encryption) | ◔ | ☐ | `C8-07-security-architecture.md` | `C8-07-security-architecture.md` |
| C8-08 | Interconnection with enterprise architecture (integration patterns, REST/async, governance) | ◔ | ☐ | `C8-08-enterprise-interconnection.md` | `C8-08-enterprise-interconnection.md` |

---

## C9 — Emerging & Systemic (the next ~)
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C9-01 | Digital assets / crypto / token securities custody | ◔ | ☐ | `C9-01-digital-assets-custody.md` | `C9-01-digital-assets-custody.md` |
| C9-02 | T+0 / same-day settlement (Daylight 24) and real-time settlement | ◔ | ☐ | `C9-02-t0-same-day-settlement.md` | `C9-02-t0-same-day-settlement.md` |
| C9-03 | AI / ML in custody: valuation, exception detection, fraud, forecasting | ◔ | ☐ | `C9-03-ai-ml-custody.md` | `C9-03-ai-ml-custody.md` |
| C9-04 | APIs and open-ecosystem model (open banking for asset servicing) | ◔ | ☐ | `C9-04-open-ecosystem.md` | `C9-04-open-ecosystem.md` |
| C9-05 | ESG & TCFD impact: positions, sustainability, reporting | ◔ | ☐ | `C9-05-esg-tcfd-impact.md` | `C9-05-esg-tcfd-impact.md` |
| C9-06 | Cross-border / jurisdictional licensing (passporting, dual licensing) | ◔ | ☐ | `C9-06-cross-border-licensing.md` | `C9-06-cross-border-licensing.md` |
| C9-07 | DLT / blockchain for settlement and custody holding (asset-chain, wide) | ◔ | ☐ | `C9-07-dlt-custody.md` | `C9-07-dlt-custody.md` |
| C9-08 | Customer experience / self-service / client portals (digital / mobile) | ◔ | ☐ | `C9-08-customer-experience.md` | `C9-08-customer-experience.md` |

---

## C10 — Your 2-Week Mastery Plan (the plan ~)
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C10-01 | How to use this repo & your 14-day time budget (2 hrs/day = 28 hrs) | ◔ | ☐ | `C10-01-how-to-use-repo.md` | `C10-01-how-to-use-repo.md` |
| C10-02 | Weekly grouping & what to cover each week (core, then deep) | ◔ | ☐ | `C10-02-weekly-groups.md` | `C10-02-weekly-groups.md` |
| C10-03 | Core topics: what you must know cold (foundations + 6 core flows) | ◔ | ☐ | `C10-03-core-cold.md` | `C10-03-core-cold.md` |
| C10-04 | Red flags / knowledge gaps: what NOT to say and what to look up | ◔ | ☐ | `C10-04-red-flags.md` | `C10-04-red-flags.md` |
| C10-05 | Conversation starters & questions to ask in every meeting | ◔ | ☐ | `C10-05-questions.md` | `C10-05-questions.md` |
| C10-06 | Milestones & self-check: know if you're really ready | ◔ | ☐ | `C10-06-milestones.md` | `C10-06-milestones.md` |
| C10-07 | Practice assignment (reconcile one, map one, draft one ADR) | ◔ | ☐ | `C10-07-practice.md` | `C10-07-practice.md` |
| C10-08 | Your 0-to-professional objective checklist (brief + detail coverage) | ◔ | ☐ | `C10-08-objective-checklist.md` | `C10-08-objective-checklist.md` |
| C10-09 | 0-to-professional capability maturity levels (0, 1,    , 3, 5) — self-score | ◔ | ☐ | `C10-09-maturity.md` | `C10-09-maturity.md` |
| C10-10| Reading list, videos, white-papers, and source bookmarks | ◔ | ☐ | `C10-10-sources.md` | `C10-10-sources.md` |

---
> **Next step:** Get approval from your trainer, then batch-generate topics in agents (2–4 topics per agent). Mark `✅` only after both brief and detail are present with ≥1 mermaid each.
