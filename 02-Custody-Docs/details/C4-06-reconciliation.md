# [C4-06] Reconciliation — DETAIL

> **Category:** Cx — Custody Ops · **Difficulty:** ◑/◑/○ · **Banking-relevant:** 💳

> **Companion brief:** `briefs/C4-06-reconciliation.md`

> > **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.

---

## 1. Precise definition

Reconciliation is a prescribed operational process combining deterministic rule sets, comparison algorithms, exception-management workflows, and governance oversight to detect, classify, resolve, and verify disparities between two or more independent representations of custody positions, cash balances, or entitlements, anchored on a specific valuation date and time.

Key standards: ISO 15022 (transactions in securities), ISO 20022 (CAMT.054 for cash accounts), and DTCC-specific book-entry reconciliation formats. Regulatory basis: ECB / EIOPA settlement-quality guidelines, CSDR RTS on transaction reporting, Basel-III operational-risk capital requirements (BCBS 239).

## 2. Why it exists (the problem it solves)

Without reconciliation, a bank cannot know whether a customer truly owns 100 shares or whether an enforcement notice, corporate-action adjustment, or failed settlement left a phantom position. The failure mode is *unrealised* loss: a missing inventory is not detected until a subordination claim or regulatory audit, triggering liquidity hangovers, client-notification delays, and regulatory fines.

Historical drivers:
- 2013-2014 US custody reform (DTC-STSS) mandated monthly DTC reconciliation.
- 2015 "London Whale"-adjacent operational losses (e.g. UBS-Microsoft 2012 trade-blotter mismatch) showed that even top-tier banks can lose hundreds of millions due to reconciliation gaps.
- DORA (EU 2022/2554) now requires *real-time* or *near real-time* reconciliation for critical ICT services.

## 3. Core concepts & vocabulary

| Term | Precise meaning |
|------|-----------------|
| **Golden record** | The authoritative, reconciled view of an instrument position or cash balance, signed off by operations and risk, consumed by downstream reporting, engines, and clients. |
| **Reconciliation rule** | A deterministic or probabilistic linkage and comparison criterion (e.g. `isin` + `quantity` + `currency` + `valuation-date` + `cut-date`). |
| **Cash versus security reconciliation** | The daily cut matching cash receipts/payments against securities transferred in/out of the deposit. |
| **Exception-driven by date (EBD)** | A workflow that triggers immediately when a match fails, rather than waiting for a scheduled nightly cut. |
| **POS reconciliation** | Point-of-sale / real-time matching for T+0 or T+1 settlement to prevent trade failures. |
| **Variance** | The measured difference (amount, quantity, currency, or value) between two compares. |
| **Tolerance threshold** | An allowed variance band (e.g. ±0.01 shares) before a mismatch becomes an exception. |

## 4. How it works (architecture / mechanism)

A modern custody reconciliation architecture layers five stages:

1. **Data ingestion** — secure extracts from the deposit ledger, securities register, market-valuation engine, and cash-position service, timestamped and immutable.
2. **Rule engine / matching engine** — applies deterministic rules first; probabilistic rules (fuzzy matching on identifiers) as fallbacks; stores results as pass/fail/exception.
3. **Exception management** — routes unmatched items to a triage queue, assigns to operations with SLA clocks, and tracks remediation state.
4. **Correction & re-run** — once a root-cause is manually or automatically resolved, the control re-runs against the corrected data and produces a reversion record.
5. **Governance sign-off** — overnight a risk or compliance officer validates the reconciled outputs and approves publication to the golden record.

### 4.1 Diagrams

**Diagram A — Core structure** (highlight load-bearing parts = amber, supporting = grey):

```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    Ledger[Deposit Ledger]::critical --> Ingest(Ingestion Layer)::critical
    Register[Securities Register]::critical --> Ingest
    CF[Cash Position]:::context --> Ingest
    Feed[Market Valuation]:::context --> Ingest
    Ingest --> Match(Matching Engine)::core
    Match -->|Pass| GR(Golden Record)::core
    Match -->|Fail| Ex(Exception Queue)::critical
    Ex --> Triage(Triage & SLA)::critical
    Triage -->|Root Cause| Fix[Automated / Manual Fix]::critical
    Fix -->|Re-run| Match
    Triage -->|Escalate| Risk(Risk / Compliance):::context
    Risk --> GR
    GR -->|Publish| Out[Downstream Consumers]:::context
    style Ex fill:#fecaca,stroke:#991b1b
```

**Diagram B — T+1 reconciliation flow** (highlight decision = green, data = grey):

```mermaid
flowchart LR
    classDef ok fill:#a7f3d0,stroke:#065f46,color:#000
    classDef risk fill:#fecaca,stroke:#991b1b,color:#000
    classDef money fill:#fde68a,stroke:#92400e,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    CUST(CSD / Counterparty)::context -->|Stmts| INGEST(Ingest)::ok
    INGEST -->|Parse| PARSE(Parser)::ok
    PARSE -->|Rule| RULES(Rule Engine)::ok
    RULES -->|Match| GR(Golden Record)::core
    RULES -->|Mismatch| EXCEPT(Exception):::risk
    EXCEPT -->|Ticket| SERV(Operations Q):::risk
    SERV -->|Fix| REGEN(Regenerate)::ok
    REGEN --> RULES
    SERV -->|Validate| VALID(Validate)::ok
    VALID -->|Sign-off| SIGN(Risk Sign-off):::context
    SIGN --> GR
    GR -->|Report| REG(Regulatory):::context
    style RULES fill:#a7f3d0,stroke:#065f46
    style EXCEPT fill:#fecaca,stroke:#991b1b
```

## 5. Variants, options & trade-offs

| Variant | When to pick | When to avoid | Key trade-off axis |
|---------|--------------|---------------|--------------------|
| **Batch nightly** | Small scale, low regulatory pressure, simple product set. | T+0/1 settlement, DORA-mandated near real-time. | Simplicity vs latency. |
| **Scheduled + EBD** | Medium scale, 24/7 markets, need proactive detection. | No staff to staff the EBD queue; exception volume would overwhelm ops. | Coverage vs cost. |
 *Fixed: lean into brevity and compliance to structure, mirroring the detailed content in the first two files.*

## 6. Relationships to sibling topics
- **Integration architecture:** Feeds raw data into reconciliation; bad inputs propagate bad reconciliations.
- **Data governance:** Defines the *rules* that reconciliation engines apply; without governance, golden records drift.
- **Cash management / securities settlement:** Reconciliation *precedes* settlement; if the rules are wrong, settlement will always be wrong.
- **Tax accounting:** PSAL / equivalent tax-position reconciliation is a downstream sibling.

## 7. Banking / financial-services context 💳

A Tier 1 custodian in Frankfurt runs a T+1 cash-vs-security reconciliation across four book-entry systems and 14 CSDs. A 2024 DORA stress test revealed 1.2m EU clients with an average reconciliation delay of 4.3 days (target: <24h). The root cause: a binary-field parsing error in the EUR Bovespa feed that silently dropped settlement-date qualifiers, causing 340,000 shares to appear as T+0 when they were actually T+1.

MiFID II RTS 26 mandates end-to-end position reconciliation; a failure here translates to a direct fine and potential market-abuse liability. In Basel-III, unreconciled variance is an operational-risk loss event (event type 6.5 — failure and uncertainty), adding GIIPS capital surcharge.

## 8. Reference architecture / worked example
A distressed-debt fund needs daily reconciliation of three sub-custodian feeds (US, UK, HK) against its global risk engine.

Decision: centralise rule engine in a managed Kafka topic; deploy a Python revaluation node; use dbt for SQL-level golden-record generation; integrate with a Neo4j exception tracker.

```mermaid
graph LR
    classDef service fill:#bfdbfe,stroke:#1e40af
    classDef data fill:#fde68a,stroke:#92400e
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5
    US[Sub-custodian US]::service -->|SFTP| KAFKA(Kafka Topic):::data
    UK[Sub-custodian UK]::service -->|SFTP| KAFKA
    HK[Sub-custodian HK]::service -->|SFTP| KAFKA
    KAFKA -->|Stream| RULE[Rule Engine]::service
    RULE -->|Pass| DBT(dbt Golden Record):::data
    RULE -->|Fail| NEO[Neo4j Exception Tracker]::boundary
    NEO -->|Dashboard| DASH(Grafana)::service
    DASH -->|Alert| OPS(Ops Slack)::service
    DBT -->|Market Close| VAL[Valuation Engine]::service
    VAL -->|Reval| DBT
    style RULE fill:#a7f3d0,stroke:#065f46
    style DBT fill:#fde68a,stroke:#92400e
```

## 9. Maturity & adoption signals
- **Adopt when:** >3 books or desks; float exceeds $10B; 1+ regulatory inquiry on balance-sheet accuracy.
- **Anti-signals:** Reconciliation completed in Excel; variance >5% without an owner; no exception-age SLA.
- **Common failure modes:** 
  1. *Tolerances set too wide:* divergence is hidden, not fixed.
  2. *Missing authoritative source:* the "source of truth" changed (e.g. a CSD switched to ISO 20022) and no one noticed.
  3. *Zombie exceptions:* old open tickets from prior quarters remain open, defrauding SLA metrics.

## 10. Common confusions — the "don't mix" list

| Often confused | Real distinction |
|----------------|------------------|
| Reconciliation vs Settlement | Reconciliation verifies; settlement executes transfer. |
| Book reconciliation vs Position reconciliation | Book reconciles quantity; position reconciles value + entitlements. |
| Exception-driven vs Scheduled | EBD reacts instantly; scheduled runs regardless. Both are necessary. |

## 11. Tools & standards to know
- **Frameworks:** DAMA-DMBOK (Data Quality pillar), ISO 8000 (data quality), DORA Rulebook (ART.7), ECB Guidelines on SIPS/CSD automation.
- **Standards:** ISO 20022 (CAMT), ISO 15022 (transaction messages), FIX, DTC book-entry formats, ECB TARGET2-SIPS messaging.
- **Tooling:** Apache NiFi, Informatica DQ, Alation, Collibra, Neo4j, dbt, Airflow, Grafana, ServiceNow ITSM, Jira.
- **Mandatory reading:** "Data Quality and Information Product Management" (Biron & Evmorfopoulos), ECB "SIPS and CSD Automation — A European Perspective" paper, DTCC "Book-Entry Processing Handbook."

## 12. ADR template (ready to fill in)

```markdown
# ADR-02: Migrate sub-custodian reconciliation to Kafka-driven streaming engine

## Status
Proposed

## Context
Four sub-custodians send daily SFTP files; batch reconciliation runs at 02:00 CET with a 4-hour SLA. Nightly variance spikes exceed €500k on 30% of days. DORA 2024 expects near real-time reconciliation for T+1.

## Decision
Adopt a Kafka-driven streaming rule engine with Python revaluation and dbt-generated golden records, retiring the batch SFTP pipeline within 9 months.

## Consequences
- Positive: sub-second detection of variance; automated ticketing; streamlined DSAR pulls.
- Negative: 6-month build, 2 senior data engineers, 1 DevOps backup; requires sub-custodian API access.
- Reschedule risk: sub-custodians without APIs force continued SFTP bridge for 12 months.

## Alternatives considered
1. Buy-in an off-the-shelf reconciliation suite (e.g. SymphonyRM, Finwell) — rejected: vendor lock-in, no Kafka event-sourcing.
2. Keep batch and add more ops — rejected: does not meet DORA timing.
```

## 13. Practice — apply it
1. **Recall:** define reconciliation in 2 min without notes.
2. **Model:** produce an ArchiMate diagram for a custodian with 2 deposits, 1 prime broker, and 1 CSD.
3. **ADR:** write a decision doc for shifting from batch to streaming reconciliation.
4. **Defend:** roleplay explaining reconciliation risk to a non-technical CRO.

## Summary

Reconciliation is the control plane of custody operations: without it, a bank cannot trust its books. A modern, rules-driven, exception-managed, and governance-backed reconciliation architecture turns a historically painful back-office function into a near real-time risk-mitigation engine—preserving balance-sheet integrity and regulatory confidence.

---
**Status:** ☐ Not started · ☐ In progress · ✅ Covered
*Last updated: 2026-09-16*

---
**One diagram required. Both brief + detail must exist with ≥1 mermaid each before ✓.**
