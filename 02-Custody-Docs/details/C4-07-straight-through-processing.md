# [C4-07] Straight-Through Processing — DETAIL

> **Category:** Cx — Custody Ops · **Difficulty:** ◑/◑/○ · **Banking-relevant:** 💳

> **Companion brief:** `briefs/C4-07-straight-through-processing.md`

> > **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.

---

## 1. Precise definition

Straight-through processing (STP) is a fully automated, end-to-end operational workflow in which a custody transaction—such as a securities transfer, cash movement, corporate-action, standing instruction, or entitlement replication—progresses from initiation (trade capture, corporate-action event, or standing instruction) to final settlement, post-settlement processing, or client notification without manual intervention at any routine decision or execution point.

STP is not merely code; it is a *contract* between upstream data quality, midstream processing reliability, and downstream settlement capability. An exemption/inhibition mechanism is a *controlled* and *documented* manual override, not a design failure.

Regulatory context: MiFID II RTS 4 (transaction reporting) and RTS 26 (position reconciliation) reward STP through reduced reporting frequency; DORA expects operational resilience even when human override is exercised.

## 2. Why it exists (the problem it solves)

Pre-STP, every custody transaction ran through a manual or semi-manual triage: a trade-supporting clerk reviewed the instruction, a back-office associate validated holdings, an operations team submitted the settlement instruction via FTP or manual window, and another team confirmed with the CSD by phone or email.

Failure modes:
- **Latency:** T+5 became typical; clients paid a 5-bp drag on returns.
- **Error rate:** 1 in 20 instructions required rework; error cost per instruction was ~€45 (staff time + settlement slip).
- **Audit burden:** every manual step required screenshot evidence for regulators; this took 40% of operational capacity.
- **Counterparty friction:** the CSD complained of late or malformed settlement instructions, threatening to delist trades.

MiFID II's 2018 deadlines and DORA's 2025 go-live pulled the industry toward STP.

## 3. Core concepts & vocabulary

| Term | Precise meaning |
|------|-----------------|
| **Automated suppression** | A message, instruction, or transaction is cleared and forwarded when all rule checks pass, without human review, ticket creation, or rekeying. |
| **Inhibition point** | A control gate where business or compliance rules mandate human review; STP is defined by the *count* and *nature* of these points. |
| **Data-quality gate** | Tooling or scripting that validates schema, completeness, and business-rule thresholds before a message enters the STP pipeline. |
| **End-to-end STP** | No manual gates between initiation and settlement. |
| **Interactive STP** | The client (or another system) provides a digital confirmation (e.g. mobile click, XML signature) that is consumed by the pipeline; the pipeline is automated, but a human decision is *predicted* upstream. |
| **Exception rate** | The ratio of inhibited/rejected/reworked messages per month; <0.1% is the benchmark for mature STP. |
| **Sub-second latency** | The target for core STP pipelines (rule evaluation, enrichment, routing); argues against batch windows. |

## 4. How it works (architecture / mechanism)

A maturity-based STP architecture evolves through stages:

**Stage 0 — Batch (no STP):**
- Paper or manual submission.
- Exception: all messages.

**Stage 1 — Batch with workflow:**
- Unattended batch routing; some rules fire automatically; others route to an operator queue.
- Exception rate ~15–20%.

**Stage 2 — Real-time rules engine:**
- Event-driven (Kafka, ESB, or Flink) validation; suppression for ~80% of messages.
- Exception: complex cross-trade or cross-border corporate actions.

**Stage 3 — End-to-end STP:**
- Every message is validated, enriched, suppressed or routed through an inhibition gate *before* settlement.
- Inhibition rate <0.1%; sub-second evaluation.

**Stage 4 — Intelligent STP with AI:**
- ML predicts exception likelihood; pre-empts inhibition.
- Continuous model retraining on exception data.

### 4.1 Diagrams

**Diagram A — Core structure** (highlight load-bearing parts = amber, supporting = grey):

```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    Start[Client / Trader]:::context -->|Submit| API(API Gateway)::context
    API -->|Auth| API
    API -->|Enrich| RECH(Reconciliation Data):::data
    RECH -->|Validate| RULE(Rule Engine)::core
    RULE -->|Suppressed| PN(Pre-settle):(Suppress)::critical
    RULE -->|Inhibit| INS(Inhibition Point)::critical
    INS -->|Review| OPS(Ops Queue):::context
    OPS -->|Fix| RULE
    PN -->|Settle| SETT(Settlement Engine)::core
    SETT -->|Confirm| LOG(Event Log)::context
    LOG -->|Notify| CLNT(Client Notification):::context
    style RULE fill:#a7f3d0,stroke:#065f46
    style INS fill:#fecaca,stroke:#991b1b
```

**Diagram B — Lifecycle with automated inhibition and re-run** (highlight money/data = gold, decisions = green, failures = red):

```mermaid
flowchart LR
    classDef ok fill:#a7f3d0,stroke:#065f46,color:#000
    classDef risk fill:#fecaca,stroke:#991b1b,color:#000
    classDef money fill:#fde68a,stroke:#92400e,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    A(Trade / Directive)::context -->|Submit| B(Validation)::ok
    B -->|Pass| C(Suppression)::ok
    C -->|Settle| D[Settle / Confirm]:::money
    B -->|Fail| E{Inhibition}::risk
    E -->|Review| F[Ops / Agent]:::context
    F -->|Correct| C
    E -->|Auto-reject| G(Reject)::risk
    G -->|Inform| CLNT(Client):::context
    D -->|Archive| AUD(Audit Log):::context
    style B fill:#a7f3d0,stroke:#065f46
    style C fill:#a7f3d0,stroke:#065f46
    style D fill:#fde68a,stroke:#92400e
    style E fill:#fecaca,stroke:#991b1b
```

## 5. Variants, options & trade-offs

| Variant | When to pick | When to avoid | Key trade-off axis |
|---------|--------------|---------------|--------------------|
| **Batch-first STP** | Legacy SFTP/FTP partners, low volume, T+2 windows. | DORA / MiFID II real-time reporting; high-frequency clients. | Simplicity vs latency. |
| **Real-time / event-driven STP** | Sub-second rule evaluation; partner APIs with <100ms SLA. | Legacy mainframes without pub/sub; high on-prem maintenance. | Latency vs infrastructure cost. |
| **Hybrid STP (batch + real-time)** | Tiered product set—some clients demand instant, others accept batch. | Regulatory demands uniform end-to-end timing. | Flexibility vs consistency. |
| **Client-interactive STP** | Client portal with e-signature; regulatory requires explicit client consent. | High client volume; mobile UX constraints; poor KYC freshness. | Control / compliance vs throughput. |

## 6. Relationships to sibling topics
- **Integration architecture:** Without reliable feeds, STP produces dangerous automated outcomes.
- **Data governance / DQ:** STP amplifies upstream errors at scale; a bad ISIN mapping becomes 10,000 failed instructions.
- **Workflow automation / BPMN:** STP uses workflows for *exception* handling, not for the happy path.
- **Settlement infrastructure:** STP cannot prevent a CSD outage; it reduces the surface area exposed to day-to-day operator error.

## 7. Banking / financial-services context 💳

A buy-side firm with €8bn in AUM processes 2,400 daily corporate-action instructions. Engaging an investment bank for 2014 FX forward text instructions, a manual entry clerk keyed 1,200 of them; 40 contained incorrect dates. Five transactions settled incorrectly, incurred €1.2m in correction fees, and drew a regulatory reprimand under MiFID II Conduct of Business (Mandatory Client Information).

DORA-compliant now: the firm runs real-time STP for sell-side trade confirmations (T+0) with an auto-inhibition on any counterparty not on the pre-approved list. Exception rate: 0.04%; average suppression time: 120ms.

DORA operational-resilience testing previously failed because the STP pipeline had no documented inhibition-room reconciliation; manual overrides were not logged and could not be reversed. A revised SOP now logs every inhibition with a reason code, SRE review, and 24-hour reversal SLA.

## 8. Reference architecture / worked example
A client places a cross-border equities order via a mobile app.

Decision: an API gateway validates the submitter against a whitelist; a Flink rule engine evaluates settlement-date, withholding-tax, and ISR/GTS entitlement rules; if all pass, the instruction is suppressed into a pre-settle queue; if a cross-border tax mismatch is detected, the instruction is routed to an inhibition gate.

```mermaid
graph LR
    classDef service fill:#bfdbfe,stroke:#1e40af
    classDef data fill:#fde68a,stroke:#92400e
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5
    Mobile[Mobile App]::service -->|POST| GW(API Gateway)::service
    GW -->|Auth| GW
    GW -->|Validate| RULE[Flink Rule Engine]::service
    RULE -->|Match| DATA[Tax / Entitlement Data]:::data
    RULE -->|Suppressed| PRE(Pre-settle Queue)::pure
    RULE -->|Inhibited| INC(Inhibition):::boundary
    INC -->|Review| WAR(War-room Ops):::context
    PRE -->|Settle| CSD[CSD / DVP]::data
    CSD -->|Confirm| GW
    GW -->|Notify| Mobile
    style RULE fill:#a7f3d0,stroke:#065f46
    style PRE fill:#a7f3d0,stroke:#065f46
    style INC fill:#fecaca,stroke:#991b1b
```

## 9. Maturity & adoption signals
- **Adopt (stage 1) when:** 3+ manual queues, exception rate >5%, regulatory audit flags on operations.
- **Adopt (stage 2-3) when:** sub-second rule throughput, proven partner SLAs, SOX control docs with STP evidence.
- **Anti-signals:** No root-cause analysis on exceptions; no formal inhibition-room SOP; data-quality incidents unmeasured.
- **Common failure modes:**
  1. *Suppressing on incomplete data:* STP hides the gap; the error surfaces at settlement as a breach.
  2. *Inhibition tsunami:* a single partner changes a field format; 50% of messages hit the queue, blocking the pipeline.
  3. *No rollback:* once an STP message is sent, there is no auto-reversal; the ops team runs catch-up.

## 10. Common confusions — the "don't mix" list

| Often confused | Real distinction |
|----------------|------------------|
| STP vs High automation | STP = no manual touch (except controlled inhibition); high automation still has manual gates. |
| End-to-end vs Interactive STP | End-to-end is one-way; interactive requires a human decision upstream. |
| Suppression vs Inhibition | Suppression = automated pass; inhibition = human review required. |

## 11. Tools & standards to know
- **Frameworks:** ISO 26262 (safety) analog for finance, DORA Rulebook (ART.7 / ART.10), ESMA Guidelines on STP and T2S, MiFID II RTS 4/26.
- **Standards:** ISO 20022 (MX messages), ISO 15022 (transaction standards), FIX API v5.0, CTCI, SWIFT gpi.
- **Tooling:** Apache Flink, Kafka Streams, JRules, Drools, ServiceNow / Jira for inhibition tickets, Grafana for suppression metrics, GitHub for requirement-test correlation, Postman / DHC for API contracts.
- **Mandatory reading:** ESMA Report on STP (2021), DAMA-DMBOK (Data Quality and Integration), Building Microservices (Newman), Domain-Driven Design (Evans), DORA rulebook.

## 12. ADR template (ready to fill in)

```markdown
# ADR-03: Graduate bond-settlement to end-to-end STP

## Status
Proposed

## Context
In-house bond settlement runs as manual FTP batch; 40% of instructions require rework. DORA 2026 requires 1% exception reporting for critical services. Our counterparty CSD complains of late or malformed settlement instructions, threatening to delist bond classes.

## Decision
Implement a Kafka-driven real-time rule engine suppressing 98% of instructions, with an inhibition gate for cross-border tax/jurisdiction mismatches.

## Consequences
- Positive: 90% reduction in operations tickets; sub-500ms suppression latency; regulatory evidence and audit trail ready.
- Negative: 8-month build; 2 Flink engineers + 1 SRE; CSD API precondition required.
- Reschedule / risk: if CSD API drops to 99.5% availability, the pipeline stalls; design must incorporate circuit breaker and fallback to batch.

## Alternatives considered
1. Outsource to a custodian STP service — rejected: yet another vendor with lock-in, less control over timestamps and inhibition logic.
2. Keep batch and add 3 clerks — rejected: does not scale past 50,000 instructions/month; non-compliant with DORA operational-resilience and MiFID II trading-concession requirements.
```

## 13. Practice — apply it
1. **Recall:** define STP in 2 min without notes.
2. **Model:** produce an ArchiMate diagram for a custodian with 3 deposits, 1 prime broker, and 1 CSD.
3. **ADR:** write a decision doc applying it to the bonding-settlement worked example in §8.
4. **Defend:** roleplay explaining STP to a non-technical CRO / CIO.

## Summary

Straight-Through Processing is the operational North Star for custody: it reduces error, latency, and cost by removing manual touchpoints, but only when the underlying architecture—data quality, integration reliability, and settlement capability—is sound. The discipline is not about eliminating people; it is about elevating them from data-entry operators to exception-incidents specialists.

---
**Status:** ☐ Not started · ☐ In progress · ✅ Covered
*Last updated: 2026-09-16*

---
**One diagram required. Both brief + detail must exist with ≥1 mermaid each before ✓.**
