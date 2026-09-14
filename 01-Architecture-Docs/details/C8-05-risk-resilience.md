# [C8-05] Risk & Resilience — DETAIL
> **Category:** C8 — Reference Architecture, Standards & Principles · **Difficulty:** ◑ · **Banking-relevant:** yes
>
> **Companion brief:** `[briefs/C8-05-risk-resilience.md](../briefs/C8-05-risk-resilience.md)`
>
> > **Target reader:** enterprise architect who must size infrastructure, justify a DORA outsource decision, or defend an RTO claim to the regulator.

---

## 1. Precise definition
**Risk & resilience architecture** is the design and implementation of *quality attributes*—availability, recoverability, confidentiality, integrity, and performance—that ensure a system continues to function (or degrades gracefully) under abnormal conditions. It is distinguished from *security architecture* by its focus on *unintended* consequences (hardware failures, network partitions, natural disasters) as well as *malicious* actions. Under DORA, resilience is *operational*: it must be documented, tested, and measured.

ISO/IEC 25010 defines these quality attributes:
- **Performance efficiency:** behavior of resource utilization under workload.
- **Compatibility:** ability to perform correctly in diverse environments.
- **Usability:** capability to be used by specified users.
- **Reliability:** capability of a system to perform required functions under stated conditions for a specified period.
- **Security:** capability to protect information and systems from unauthorized access, use, disclosure, modification, or destruction.
- **Maintainability:** effort required to modify a system.
- **Portability:** ease with which a system can be transferred.

In banking, *reliability* and *security* must be jointly optimized because a single control gap (e.g., encryption key rotation failure) undermines both.

## 2. Why it exists (problem it solves)
In 2021, a German cooperative bank’s settlement system ran on a single EU cloud region. When a GCP zone went dark during a maintenance window, the bank could not settle EUR/GBP FX trades for 34 minutes. The impact: €12M in margin calls, three CFTC inquiries, and a BaFin review triggered valuation-adjustment margin. The root cause was architecture-level: the bank had a single-region deployment, no circuit breakers, and no automated failover test in the previous 18 months.

Before this incident, a single P1 production outage in 2019 at a similar bank ran for 2 hours because the manual runbook had the wrong DNS endpoint. The manual process was *documented but not tested*; when under stress, the human operator misread. Resilience architecture replaces reliance on human-under-pressure performance with *self-healing* design.

## 3. Core concepts & vocabulary
| Term | Precise meaning |
|------|-----------------|
| **Availability** | System uptime as measured against SLO (e.g., 99.99% = 52.6 minutes/year max downtime). |
| **RTO** | Recovery-time objective: maximum tolerable downtime after an incident. |
| **RPO** | Recovery-point objective: maximum tolerable data-loss, i.e., acceptable replay window. |
| **N+1 redundancy** | Baseline load N, plus one extra instance for failover. |
| **N+2 redundancy** | Baseline load N, plus two extra instances (for a complex resource with asymmetric scaling, e.g., a database primary+standby). |
| **Circuit breaker** | Pattern that fails fast when a downstream service is unresponsive; prevents cascading. |
| **Bulkhead** | Pattern that isolates resource pools per service or domain (e.g., separate Redis cluster for trade finance). |
| **Active-active** | All instances receive production traffic; no single default; traffic-shifting via L7. |
| **Active-passive** | Single primary; passive standby takes over on failure (simpler, but switchover time matters). |
| **Chaos engineering** | Controlled experiment (kill, partition, latency) to find resilience weaknesses *before* real incident. |
| **Blast-radius containment** | Architectural patterns that limit failure propagation (service-mesh traffic-shifting, namespace isolation). |
| **Tier 1 / 2 / 3** | Classification: Tier 1 = payments/settlement (sub-1-second SLO); Tier 2 = risk/regulatory reporting (<5 min RPO); Tier 3 = internal analytics (no outage SLA). |
| **MTTR / MTBF** | Mean time to repair / mean time between failures; used to refine reliability models. |
| **Independent risk assessment (IRA)** | Under DORA, an external party assesses the bank’s ICT risk profile unless it self-tests to a threshold. |

## 4. How it works (architecture / mechanism)
Resilience architecture is implemented through **four complementary mechanisms**:
1. **Static redundancy** — multiple instances, regions, or availability zones already running.
2. **Dynamic failover** — traffic-shifting mechanisms (DNS, L7 LBs, service mesh) that redirect traffic without human intervention within seconds.
3. **Observability** — distributed tracing, structured logging, and SLO dashboards that detect degradation *before* it hits the user.
4. **Continuous testing** — chaos engineering, disaster-recovery exercises, and pen-testing revert your assumption that “it worked last month.”

Under DORA, the *operational* dimension requires:
- Documented RTO/RPO per Tier-1 system.
- Independent risk assessment (IRA) or validated self-tests (if risk < threshold).
- 4-hour initial incident notification, 24-hour detailed, 72-hour final.
- Annual disaster-recovery test with an independent party.

### 4.1 Diagrams
**Diagram A — Failover topology with blast-radius containment (highlighting service = blue, data = yellow, boundary = dashed-grey):**
```mermaid
graph TB
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef service fill:#bfdbfe,stroke:#1e40af
    classDef data fill:#fde68a,stroke:#92400e
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5
    
    User1[EU Retail<br/>Users]:::service
    User2[US Wholesale<br/>Users]:::service
    
    LB[Global Load Balancer<br/>Anycast + Geo-DNS]:::service
    
    subgraph FW[Firewall<br/>WAF]:::boundary
        Edge[Edge Layer<br/>(WAF / DDoS)]:::service
    end
    
    Edge -->|filtered| LB
    
    LB -->|primary EU| EU[EU Primary<br/>(Frankfurt)]:::service
    LB -->|standby EU| EU_DR[(DR Site<br/>Dublin)]:::data
    LB -->|standby US| US[(US Region<br/>(Lousiville)]:::service
    
    EU -->|writes| EU_DB[(Primary<br/>Database)]:::data
    EU -->|replicates async| EU_DR
    
    EU -.->|circuit breaker| REST[REST API<br/>(Resilience Pattern)]:::service
    REST -->|protects| EU_DB
    
    EU -->|emits events| Kafka[(Event Stream)]:::data
    Kafka -->|mirrored| US
    US -->|reads| US_DB[(US Replica)]:::data
    
    classDef data data
    class User1,User2,LB,REST,Edge,WB service
    class EU,US,EU_DB,US_DB,EU_DR directory service
    class EU_DR..>EU_DB directory data
    class Edge,EU,US boundary
```

**Diagram B — Chaos-engineering experiment timeline (highlighting ok = light-green, risk = red, decision = green):**
```mermaid
flowchart LR
    classDef ok fill:#a7f3d0,stroke:#065f46,stroke-width:1px
    classDef risk fill:#fecaca,stroke:#991b1b,stroke-width:1px
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
    
    Baseline[Baseline<br/>(green)]:::ok
    Phase1[Inject Chaos<br/>(kill DB pool)]:::risk
    Pass1{{OK?}:::decision
    Degradation[Degradation<br/>behaviour observed]:::ok
    Recovery[Auto-recover<br/>within RTO]:::ok
    
    Baseline -->|inject| Phase1
    Phase1 --> Pass1
    Pass1 -->|no| Degradation
    Pass1 -->|yes| Recovery
    
    Degradation -->|check| Recovery
    Recovery -->|deploy| Baseline
    
    classDef ok ok
    class Baseline,Passures,Recovery ok
    class Phase1 risk
    class Passures,Recovery decision
```

## 5. Variants, options & trade-offs
| Variant | When to pick | When to avoid | Key trade-off axis |
|---------|--------------|---------------|--------------------|
| **Active-active multi-region** | Sub-second payment latency, cases where failover must be invisible | Complex eventual-consistency, high cost | Consistency vs. latency |
| **Active-passive with warm standby** | Complex stateful systems (core banking), high RTO tolerance | Must detect failure and switchover < 5 min | Cost vs. RTO |
| **Single-region + circuit breakers + chaos** | Low-cost, non-Tier-1 internal tools, greenfield SaaS | Any Tier-1 payment or settlement system | Cost vs. regulatory compliance |
| **Delegate to cloud DRP** | Banks without cloud ops, need faster time-to-DR | Heavy compliance drag of cloud data-residency; vendor lock-in | Speed vs. autonomy |
| **Independent risk assessment (IRA)** | DORA-in scope, high-risk Tier-1 | Low-risk Tier-3; internal self-tests | Cost vs. external validation |

## 6. Relationships to sibling topics
- **Compliance & regulation:** resilience requirements (RTO, RPO, DORA 4-hour incident response) *are* compliance requirements; compliance ships with the RTO/RPO architecture.
- **Reference architecture:** the reference architecture defines *where* resilience layers sit (e.g., circuit breakers at the gateway, not the database) and *which* pattern applies per domain.
- **Data sovereignty:** resilience design must respect data-residency laws; a standby in a non-EEA region can violate GDPR.

## 7. Banking / financial-services context 💳
Under DORA, the EBA requires:
- **Risk assessment:** annual, documented, covering all Tier-1 and Tier-2 ICT systems.
- **Incident reporting:** 4-hour initial, 24-hour detailed, 72-hour final.
- **Digital operational resilience testing:** annual *independent* (or validated self-test) disaster-recovery test for all ICT assets ≥ Tier-1.
- **Third-party / cloud:** if you use a managed provider, you must verify *their* RTO/RPO maps to yours.

A real example: a UK retail bank designed its corporate-payments platform with a single GCP region in London. During a bank stress test, the synthetic-transaction test detected that a single-region failover added 22 minutes—exceeding the 15-minute RTO for a Tier-2 risk report. The board was instructed of the €4.2M cost to move to active-active config across London and a Frankfurt standby.

## 8. Reference architecture / worked example
**Problem:** A UK bank’s instant-payments target service must sustain 99.99% availability (52.6 min/year max downtime) with a 15-minute RTO and 2-minute RPO.

**Decision:**
1. **Topology:** active-active across UK (Equinix SV4) and EU (Frankfurt) with geo-DNS failover.
2. **Data:** primary SQL instances in each region with synchronous commit; a third region (Dublin) for DR with async replication.
3. **Blast radius:** circuit breakers at the gateway; separate Redis cluster per domain (UK retail, EU corporate).
4. **Testing:** quarterly Gremlin experiments (terminate database connection, inject 4G-latency to 10th percentile, power-cut a pod).
5. **Independent risk assessment:** DORA thresholds exceeded $10T notional; engagement with DORA-registered DORA-IRT.

**ADR:**
```markdown
# ADR-334: Active-Active Multi-Region for Instant Payments
## Status
Accepted
## Context
Current single-region deployment = 22 min RTO; DORA threshold exceeded; CFTC/BBA wants <15 min incident notification.
## Decision
- Deploy active-active UK + Frankfurt with 50/50 traffic splitting.
- Synchronous SQL commit within region; async to Dublin (RPO 2 min).
- Circuit breaker at gateway, per-domain Redis bulkheads.
- Quarterly Gremlin chaos tests; annual independent DR test.
## Consequences
- Positive: RTO < 90 seconds; sub-5-minute incident notification.
- Negative: €3.1M one-time; ongoing multiregion data egress.
- Negative: complex eventually-consistent inventory reconciliation; requires compensation.
## Alternatives considered
1. Single-region + circuit breakers only. → Rejected: fails DORA <15 min RTO.
2. Pure single-region failover via DNS. → Rejected: DNS TTL + health-check propagation > 10 min.
3. Outsource to Stripe / Adyen. → Rejected: loss of analytics, customer data, and CFTC reporting control.
```

## 9. Maturity & adoption signals
- **Adopt when:** Tier-1 system, DORA-in scope, or recurring incident-runbook failure.
- **Anti-signals (don't adopt yet):** all systems are Tier-3, no regulatory deadline, no cross-border operations.
- **Common failure modes:** (1) building a DR plan that is never force-tested; (2) using a failover path that is *slower* than the primary because of complex state transfer; (3) designing for the “happy path” and assuming the DR is the same code.

## 10. Common confusions — the "don't mix" list
| Often confused | Real distinction |
|----------------|------------------|
| **Resilience vs. High availability** | Resilience = surviving unknown stresses; availability = predictable uptime. |
| **RTO vs. RPO** | RTO = time to restore; RPO = data-loss tolerance. |
| **N+1 redundancy vs. Active-active** | N+1 = spare capacity; active-active = simultaneous processing. |
| **Failover vs. Failback** | Failover = moving traffic; failback = returning traffic, which is a distinct and often-overlooked recovery step. |
| **Manual runbook vs. Resilience architecture** | Manual runbooks assume calm operators; resilience architecture assumes stressed operators. |

## 11. Tools & standards to know
- **Standards/Frameworks:** DORA (EU/UK), ISO/IEC 25010 (quality model), ISO 22301 (business continuity), NIST SP 800-53, AICPA SOC 2, PCI-DSS 4.0, IEC 62443 (industrial), ISO 27001 A.16 (information security incident management).
- **Common tooling:** Chaos Monkey / Gremlin / Litmus (chaos engineering), SignalFx / Datadog (observability + SLO), Confluence + Jira (runbooks / scorecards), Kubernetes (high-availability primitives), Istio / Linkerd (service-mesh circuit breakers), Terraform / CloudFormation (terroredred architecture), Splunk / Elastic (centralized logging), ADInstruments (incident classification), Logicify (EU DORA-IRT directory).
- **Mandatory reading:** DORA Final Report / UK Treasury Extended Supervisory Framework; “Engineering Resilient Systems” by O'Reilly; SRE Book (Google); “Observability Engineering” by O'Reilly.

## 12. ADR template (ready to fill in)
```markdown
# ADR-XXX: <decision>
## Status
Accepted | Proposed | Deprecated

## Context
...

## Decision
...

## Consequences
- Positive ...
- Negative ...
- ...

## Alternatives considered
1. ...
2. ...
```

## 13. Practice — apply it
1. **Recall:** define risk & resilience in 2 minutes without notes.
2. **Model:** draw an active-active failover diagram for a payment gateway with circuit breakers and blast-radius containment.
3. **ADR:** write a decision to accept a 22-minute RTO for a Tier-2 risk-reporting system; justify grounding in DORA Tier-2 classification.
4. **Defend:** roleplay an incident-review-board where a CRO asks why the UK retail-payments RTO is 3 minutes, not 10.

## 14. Summary (1 paragraph)
Resilience architecture is the discipline of ensuring that a bank’s critical payment, settlement, and risk-reporting flows survive—and degrade gracefully under—unexpected failure. Under DORA and Basel-III, resilience is not a nice-to-have; it is a measurable, testable, auditable property of the architecture itself. From active-active multi-region deployments to chaos-engineering experiments, every design choice should be readable as a bet: *we bet this pattern will hold under time-pressure, automated judgment, and regulatory observation.* And if we cannot defend that bet, the resilience architecture has failed.
