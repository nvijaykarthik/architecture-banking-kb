# [C4-03] Distributed fundamentals — DETAIL

> **Category:** C4 — System & Software Design · **Difficulty:** ●●
> **Companion brief:** `[briefs/C4-03-distributed-fundamentals.md](../briefs/C4-03-distributed-fundamentals.md)`
>
> > **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.

---

## 1. Precise definition

A **distributed system** is a collection of autonomous computing nodes that coordinate by exchanging messages over a network. The *defining properties* (as per **Leslie Lamport**, 1978; **Barbara Liskov**, 1982) are:

1. **Autonomy:** Nodes operate independently and can fail without halting the entire system.
2. **Asynchrony:** No globally accurate notion of time; message delivery order is unspecified.
3. **Partial failure:** Any component (network, node, storage) may fail independently at any point.

> The "network is the new shared memory" axiom: in distributed systems, communication replaces memory access as the primary abstraction.

**CAP Theorem** (Gilbert & Lynch, 2002): In the presence of network partitions, a distributed data store can guarantee at most two of the following:
- **Consistency (C):** Every read receives the most recent write or an error.
- **Availability (A):** Every request receives a (non-error) response.
- **Partition Tolerance (P):** The system continues to operate despite arbitrary message loss or delay.

Since partitions are inevitable in wide-area networks, the trade-off is effectively **C vs A** in the presence of P.

> **Sources:** Lamport L. *Time, Clocks, and the Ordering of Events in a Distributed System* (1978); Gilbert S. & Lynch N. *Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services* (2002).

## 2. Why it exists (problem it solves)

Before distributed systems, software fit in a single datacenter or on a single mainframe. Banking encountered three pressures:

1. **Geographic regulation:** The **European Banking Authority (EBA)** and **Reserve Bank of India (RBI)** mandate that *payment infrastructure* must reside in-region for data sovereignty.
2. **Fault isolation:** A London flood or a Mumbai earthquake cannot bring down payments to Singapore and Tokyo.
3. **Scale:** 5B+ payment transactions/month global retail banking (e.g., Mastercard, Visa, or a global wholesale payment platform) far exceeds single-node throughput.

Without distributed architecture, banks would suffer:

- **Single point of failure (SPOF):** A datacentre outage halts all clearance and settlement.
- **Vendor lock-in:** A single-region cloud provider becomes a strategic dependency.
- **Regulatory non-compliance:** GDPR Art. 45 requires data to stay within EU; a UK-only system serving multinational customers violates this.

## 3. Core concepts & vocabulary

| Term | Precise meaning |
|------|-----------------|
| **Node** | An autonomous runtime (VM, container, serverless function). |
| **Session** | A stateful interaction between a client and a server across untrusted network. |
| **Message / RPC** | The primitive of distribution; synchronous (REST, gRPC) vs asynchronous (Kafka, SQS). |
| **Partition tolerance** | The system remains operational despite network partitions. |
| **CP vs AP vs CA** | Consistency+Partition-tolerance, Availability+Partition-tolerance, Consistency+Availability (only achievable without partitions). |
| **Byzantine fault** | A node behaves arbitrarily (malicious or crashed-recover) rather than crashing cleanly. |
| **Idempotency** | An operation that, when applied multiple times, has the same effect as if applied once. |
| **Linearizability** | A concurrency model where operations appear to occur instantaneously at a single point between invocation and response. |

## 4. How it works (architecture / mechanism)

### 4.1 Diagrams

**Diagram A — A globally distributed payment platform (critical = partition, decision = gateway):**

```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
    classDef context fill:#dfe6e9,stroke:#636e72
    classDef ok fill:#a7f3d0,stroke:#065f46

    Client[Mobile Client / ATM]:::context --> GW[API Gateway / BGP Anycast]:::decision
    GW --> DNS[Global DNS / GeoDNS]:::context
    DNS --> Mumbai[Mumbai DRDC]:::critical
    DNS --> Dublin[Dublin DRDC]:::critical
    DNS --> Singapore[Singapore DRDC]:::critical
    Mumbai --> MConsist[Ledger: CP (Raft)]:::decision
    Dublin --> DProc[FX & FX-Rate Service: AP]:::ok
    Singapore --> SAuth[Auth Service: CP under quorum]:::decision
```

**Diagram B — CAP trade-off in a payment journey (risk = amber for unavailable, ok = green for available):**

```mermaid
flowchart LR
    classDef ok fill:#a7f3d0,stroke:#065f46
    classDef risk fill:#fecaca,stroke:#991b1b
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px

    Start[1. Authorization Request]:::critical --> AC{Account Check}
    AC -->|CP Ledger| OK1[Block Read]:::ok
    AC -->|CP Ledger| FAIL1[Fail Safe: Reject]:::risk
    OK1 --> FR{Fraud Score}
    FR -->|AP (stale acceptable)| OK2[Proceed with Stale Score]:::ok
    FR -->|AP (stale not ok)| FAIL2[Queue for Re-check]:::risk
```

### 4.2 Mechanism

Distributed systems rely on three *families of mechanisms*:

1. **Consensus & Replication:**
   - **Raft** (preferred in banking for its understandability) for CP ledgers (payment clearing, settlement).
   - **Paxos** for systems requiring higher liveness guarantees.
   - Quorum reads/writes ensure that a majority of nodes agree.

2. **Partition Tolerance Patterns:**
   - **Circuit breaker:** If a downstream service (e.g., FX rate) times out 50% of the time, fail fast rather than propagate latency.
   - **Bulkhead:** Isolate resource pools per critical function (authorization vs reporting) so that a reporting flood cannot starve authorization.
   - **Timeout & retry:** Exponential backoff with jitter; never retry idempotently non-idempotent operations.

3. **Consistency Management:**
   - **CP paths:** Payment ledger = **Raft-based** or **Paxos-based** consensus; reads/writes require quorum; returns 500s on partition rather than diverging.
   - **AP paths:** Fraud scoring is *eventually consistent*; a 30-second delay in stale fraud score does not violate PCI-DSS or PSD2; the system remains available.
   - **Slo-controlling API:** The EA sets *latency SLOs* per path (CP path < 50 ms in non-partition, 500 ms under partition; AP path < 100 ms).

## 5. Variants, options & trade-offs

| Pattern / Mechanism | When to pick | When to avoid | Key trade-off axis |
|---------------------|--------------|---------------|--------------------|
| **Raft-based CP** | Payment ledger, AML transaction monitoring | < 3 nodes, cost-sensitive, single region acceptable | *Safety vs availability* |
| **AP with eventual consistency** | Fraud scoring, recommendation engines | Real-time settlement, regulatory CRR reporting | *Availability vs immediate correctness* |
| **Byzantine-fault tolerance (BFT)** | MPC multi-cloud key issuance, critical-path signing | < 5 regions, cost > 2x Raft | *Security vs cost & complexity* |
| **CAP re-visited: CA (no partition)** | In-memory cache, local session store | Wide-area deployment | *Materiality: not a real distributed system* |
| **Edge distribution** (CDN, edge nodes) | Static KYC documents, non-sensitive marketing | UPI push notifications, real-time balance | *Latency vs data sensitivity* |

## 6. Relationships to sibling topics

- **Layering & modularity (C4-02):** Distributed systems *execute* layered/modular components across nodes.
- **Scalability (C4-04):** Autonomy and asynchrony enable horizontal scaling but complicate scaling-down (state residence).
- **Resilience (C4-05):** Distributed systems *require* resilience; partitions are the canonical failure mode.
- **Observability (C4-12):** Distributed trace IDs (OpenTelemetry) are mandatory to join messages across nodes.
- **APIs (C4-08):** The *contract* over which nodes communicate; RPC vs event is a stylistic and consistency-related choice.

## 7. Banking / financial-services context 💳

### Scenario
A **global retail bank** operates in 18 countries, processing **5B+ transactions/month** (card payments, UPI, SWIFT, RTGS). Each country has a **DRDC (Disaster Recovery Datacentre)** with mandated **data residency** requirements (EU data in EU; India data in India).

### Distributed design

| Subsystem | Deployment | CAP Mode | Rationale |
|-----------|------------|----------|-----------|
| **Payment ledger** | 3-node Raft across Mumbai, Dublin, Singapore | **CP** | Double-spend is illegal; must reject on partition rather than risk inconsistency. |
| **Fraud scoring** | Kafka stream + 5-replica Redis cluster | **AP** | 30s stale fraud score acceptable; downtime = 100% of fraudulent transactions through. |
| **KYC identity proofs** | S3 / MinIO in each region | **AP (read-optimized)** | Data is replicated asymm; updates propagated asynchronously; stale read under rare race acceptable. |
| **Authorization / 3D Secure 2.0** | 2 replicas per region + circuit breaker | **CP under quorum** | Must be available; if quorum lost, fail to fallback 3D Secure 1.0.2 |

### Regulatory tie-in
- **DORA (EU Digital Operational Resilience Act):** Requires ICT risk management for *digital operational resilience*; distributed systems must be *tested* for failure modes including network partitions (DORA Art. 11, 14).
- **RBI (India) cybersecurity framework:** Mandates *isolation of payment systems*; no payment node may share infrastructure with a non-payments workload.
- **PCI-DSS v4.0:** Ability to establish *a logical and physical separation* between payment and non-payment environments; distributed firewalling and segmentation support this.

## 8. Reference architecture / worked example

### Problem
During a **simulated regional datacentre failure** (London DRDC), the bank's EU card payments spike caused the **fraud scoring** AP cluster to experience 300% traffic. The circuit breaker was *not* configured; the scoring service's CPU saturated, and 150ms-latency timeouts cascaded to the authorization path, causing 2% of EU transactions to fail (within the PCI-DSS 3% ~12-hour outage limit).

### Decision
Implement **triple-factor circuit breaking** and **priority-based bulkheads**:

1. **Circuit breaker:** 503s after 5 consecutive > 1s timeouts.
2. **Bulkhead:** Auth gets its own CPU pool (30%); fraud is throttled to 20% between 06:00–22:00.
3. **Timeout:** 200ms for fraud; fallback to *static low-risk score* (AP) rather than hard failure.
4. **Chaos test:** Run Gremlin or Chaos Mesh on London region weekly.

### ADR

```markdown
# ADR-051: Enforce CP authorization and AP fraud with circuit breaking

## Status
Accepted

## Context
- During London DRDC test, fraud scoring overload caused 2% authorization failures.
- PCI-DSS 3% outage limit is close; 2024 hardening is required.
- Fraud scoring is AP; authorization must be CP.

## Decision
1. Deploy Envoy with RateLimitService for bulkheads.
2. Circuit-break fraud scoring after 5x 1s timeout; return 200 + stale-score flag.
3. Route all EU traffic through Dublin/Mumbai fallback via DNS failover.
4. Add weekly Gremlin chaos test: partition London ↔ Dublin for 1h.

## Consequences
- Positive: Auth never blocks on fraud overload; 0% PCI-DSS outages.
- Negative: 30s stale fraud scores may allow low-risk fraud through; accept under PSD2 fraud-chargeback liability.
- Positive: Chaos tests prove DORA Art. 11 resilience evidence.

## Alternatives considered
1. **Higher-cardinality fraud replicas:** Would increase cost 3x; rejected.
2. **Fully CP fraud:** Would require Raft consensus; latency > 500ms; rejected for UX.
```

### Diagram (reference architecture with resilience)

```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
    classDef context fill:#dfe6e9,stroke:#636e72
    classDef ok fill:#a7f3d0,stroke:#065f46

    Client[Card / Mobile Client]:::context --> GW[API Gateway]:::decision
    GW --> Auth[Authorization: CP (Raft)]:::critical
    GW --> FB[Circuit Breaker]:::decision
    FB --> Fraud[Fraud: AP (Kafka + Redis)]:::ok
    Auth --> DW[(Settlement Ledger)]:::context
    Enroute[Kafka]:::decision --> Fraud
```

## 9. Maturity & adoption signals

- **Adopt when:** Multi-region deployment is mandated or cost-optimal; team has SRE/DevOps engineers.
- **Anti-signals (don't adopt yet):** Single-region, < 10 developers, no distributed trace tooling, no IAM least-privilege on inter-node traffic.
- **Common failure modes:**
  1. **Split-brain deadlock:** Two Raft leaders both believe they are primary after a network partition; coordinator writes diverge.
  2. **Timeout cascade / thundering herd:** 100k clients rediscover a cached rate limit after it expires at the same millisecond.
  3. **Data residency leakage:** A YugabyteDB cluster spans a US and an EU region; GDPR Art. 45 is violated.

## 10. Common confusions — the "don't mix" list

| Often confused | Real distinction |
|----------------|------------------|
| Distributed vs decentralized | Distributed = partitioned network; Decentralized = no central coordinator (blockchain). |
| Eventual consistency vs stale data | Eventual consistency = a *system property*; stale data = a *symptom* that may or may not violate SLO. |
| CAP vs PACELC | CAP = partition vs consistency/availability; PACELC = partition vs latency (normal cases). |
| Byzantine fault vs crash fault | Byzantine = arbitrary (malicious) behavior; Crash = total but honest failure (memory safety, power cut). |

## 11. Tools & standards to know

- **Standards/Frameworks:** ISO/IEC 25010 (reliability, security), ISO/IEC 27017 (cloud), DORA (EU), RBI (India), PCI-DSS v4.0.
- **Common tooling:** Apache Kafka, Apache Pulsar, HashiCorp Consul/Raft, etcd, Consul KV, Spanner (CP), Yugabyte (CP/AP boundary), Envoy, Istio (service mesh), KEDA, Chaos Mesh, Gremlin, Jaeger / Tempo.
- **Mandatory reading:** *Designing Data-Intensive Applications* by Martin Kleppmann (2017), *Distributed Systems: Principles and Paradigms* by Tanenbaum (8th ed.), *Database System Concepts* for Raft/Paxos.

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

1. **Recall:** explain the CAP theorem to a non-technical CRO in < 90 seconds.
2. **Model:** produce an ArchiMate diagram of your bank's multi-region deployment; label each component's CAP mode.
3. **ADR:** write an ADR applying distributed consensus to a payment ledger that spans 3 countries.
4. **Defend:** roleplay explaining why a *fully consistent* fraud-scoring system is *not* worth 10x the infrastructure cost for a retail bank.

## 14. Summary (1 paragraph)

Distributed systems are the operational reality of global banking. The network is not a transmission pipe; it is an unreliable, partitioned substrate that introduces partition tails, clock drift, and partial failures. The EA's job is to *classify every subsystem* by its CAP choice—CP for money, AP for insight—and then to enforce that choice through infrastructure, IAM, and chaos engineering. Without this discipline, a single weather event or cloud-provider incident becomes a regulatory event.

---
**Status:** ☐ Not started · ☐ In progress · ✅ Covered · **Last updated:** 2026-09-14
