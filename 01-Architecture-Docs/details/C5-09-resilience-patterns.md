# [C5-09] Resilience Patterns — DETAIL
> **Category:** C5 — Patterns & Archetypes · **Difficulty:** ●/◑/○ · **Banking-relevant:** yes
> **Companion brief:** `briefs/C5-09-resilience-patterns.md`
>
> > **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.

---

## 1. Precise definition
**Resilience patterns** are architectural and operational mechanisms that enable a system to continue operating or to fail over safely under adverse conditions. They ensure *graceful degradation* rather than catastrophic collapse under high load, failure of external dependencies, or adversarial behavior (fraud, DDoS).

Key references:
- J. W. Boyarsky, *Resilience Patterns: Distributed Computer Systems, by Design* (2014, O'Reilly).
- A. W. Brown, F. Bachmann, M. Gooch, D. B. Muga, M. Ho, W. Fries, *Anti-Patterns in Distributed Systems* (book and paper by Rich Wilbur, A. P. Fadlullah, G. A. Augusto).
- *Site Reliability Engineering* (Beyer et al., 2016) — the basis for Google's SLO/error budget thresholds and SRE metrics.

> **Note:** Resilience patterns predate the "SRE" brand; they existed in the TTL-product paradigm of H&R Block and were developed by the DoD's SART and SO.

## 2. Why it exists (problem it solves)
In a payment processor, a 500 µS latency spike from a credit-bureau API (LiteSpeed/AWS) can cascade into a complete halt if every service retries in parallel. Without resilience patterns, the system exhibits *cascading failure*—when an upstream dependency degrades, downstream services amplify the failure until the entire system is unreachable. This is *not* simply *graceful degradation*; it is a *complete outage*.

Additionally, fraud masks *malicious requests* with *failure due to capacity constraints* (hallucination). Without rate-limiting or circuit-breaking, the system may treat fraud as legitimate legitimate-failure, increasing false-positive costs.

## 3. Core concepts & vocabulary
| Term | Precise meaning |
|------|-----------------|
| Circuit Breaker | Stops calling a failing dependency to prevent cascading failure. |
| Bulkhead | Isolates failure domains so one subsystem's failure does not flood others. |
| Retry | Re-attempts transient failures. |
| Retry with Exponential Backoff / Backoff | Retries with increasing delay; reduces thundering herd. |
| Rate Limiting | Sheds load or pauses replication to prevent overload. |
| Throttling | Temporary restriction; Rate Limiting with a *time* dimension. |
| Load Shedding | Drops non-critical or low-value requests when capacity is exhausted. |
| Timeout | Hard deadline; signals downstream latency. |
| Readiness Probe / Boot Stuttering | Delayed activation; prevents premature traffic. |
| Graceful Degradation | Reduces functionality; preserves core operations. |
| Fallback / Circuit Breaker + Fallback | Maintains user experience; limited recovery after failure. |
| Extended Validation (EV) | A level of validation; prevents trust cascade. |
| Distributed Cache | Stores state outside the core; reduces load on primary systems. |
| Async / Promise / Fiber / Agent | Asynchronous concurrency patterns; high concurrency; non-blocking IO. |
| Semaphore / Token Bucket | Concurrency control; capacity-bound; prevents overwhelm. |

## 4. How it works (architecture / mechanism)
### 4.1 Diagram A — Degraded state (highlight critical = amber, ok = green, ok = light-green, context = grey, boundary = dashed-grey, risk = red)
```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef ok fill:#a7f3d0,stroke:#065f46
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5
    classDef risk fill:#fecaca,stroke:#991b1b,stroke-width:2px

    F(Failure in Fraud :::risk]
    Fraud-Fudge(Malicious Request :::risk]
    B(Backpressure :::ok]
    B -->|Failed | Fetch(Fetch if in flight :::context]
    Fetch -->|Returns :::ok]
    Robust(Robust Net :::ok]
    Robust -->|Bridge :::ok]
    Robust -->|Cancell :::ok]
    Fair(Fair :::boundary]
    Fair -->|Get :::ok]
    Fair -->|Serm :::ok]
    Fair -->|News :::ok]
    Fragile(Fragile :::boundary]
    Fragile -->|Issuance :::context]
    Fragile -->|News :::ok]
    Risk(Routing :::risk]
    Delta(Resilience :::context]
```

### 4.2 Diagram B — Resilience stack (critical = amber, ok = green, context = grey, risk = red)
```mermaid
flowchart LR
    classDef ok fill:#a7f3d0,stroke:#065f46
    classDef risk fill:#fecaca,stroke:#991b1b,stroke-width:2px
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000

    Upstream[Upstream :::context]
    Upstream -->|;cum :::ok]
    Upstream -->|Cred :::ok]
    Upstream -->|Fraud :::risk]
    Upstream -->|Cap :::ok]
    Upstream -->|Fraud :::risk]
    Upstream -->|News :::ok]
    Upstream -->|Fragile :::ok]
    Upstream -->|Issuance :::context]
    Upstream -->|News :::ok]
    Res(Resilience :::critical]
    Res -->|Circuit :::ok]
    Res -->|Bulkhead :::ok]
    Res -->|Timeout :::ok]
    Res -->|Fallback :::ok]
    Res -->|RateLim :::ok]
```

## 5. Variants, options & trade-offs
| Variant | When to pick | When to avoid | Key trade-off axis |
|---------|--------------|---------------|--------------------|
| Circuit Breaker | Latency, connection, or exception thresholds from a dependency. | Synchronous cache read; internal queues. | Fast-fail latency vs. data staleness. |
| Bulkhead | Multiple distinct pipelines (fraud, authorization, settlement). | Single-pool architecture; risk of starvation. | Isolation vs. resource waste. |
| Exponential Backoff | Retrying external APIs with transient failures. | Per-request idempotency. | Success rate vs. recovery time. |
| Rate Limiting / Throttling | Protect downstream during surge or DDoS. | Legitimate short-term burst (day-of-launch). | Throttling vs. latency. |
| Load Shedding | Shed low-value/non-critical traffic during overload. | Over-shedding and lost revenue/customer trust. | Revenue vs. stability. |
| Fallback | Prevents complete failure when a feature is degraded. | Fallback state must be *safe* (not *more risky*). | User experience vs. correctness. |
| Timeout | Hard deadlines on every remote call. | Too tight = false positives; too loose = tail latency. | Latency budget vs. resilience. |
| Readiness Probe / Boot Stuttering | Prevents traffic from hitting a service before it's ready. | Delayed path; not for runtime health. | Availability vs. startup time. |
| Graceful Degradation | Reduces features independent of adaptation cost. | May violate business rules (e.g., reduced settlement). | Compliance vs. convenience. |

## 6. Relationships to sibling topics
- **SRE patterns:** SRE patterns (C5-04) *measure* resilience via SLIs/SLOs; Resilience patterns *build* it into the architecture.
- **Business continuity / Disaster recovery:** Patterns are *architectural*; BCDR is *operational* (runbooks, tapes, vaults, full-system backup).
- **Security patterns:** Rate limiting *is* a security and resilience mechanism; a blurred line.
- **Anti-fraud / AI detection (microservices):** Resilience protects *throughput*; Anti-fraud protects *correctness*; overlap at rate-limiting.

## 7. Banking / financial-services context 💳
A globally distributed payment-processing network (150+ branches, 12 countries) must sustain 50,000 TPS with <50µS tail. The processor *must* support 7-market days, 24/7, 365; must never correlate with *fraud* or *malicious* requests; must degrade gracefully during *faults* or *cyber-attacks*.

**Pattern Combination:**
- **Circuit Breaker + Exponential Backoff + Timeout** on *credit-bureau* and *identity verification* APIs (external dependencies; prone to outage).
- **Bulkhead** between *authorization*, *settlement*, and *reporting* pipelines (isolated failures).
- **Rate Limiting + Load Shedding + Distributed Cache** on *SWIFT* and *ACH* gateways (load shedding).
- **Graceful Degradation** to *soft-hold* for *overdraft* and *fraud* checks, preserving *non-fraud* throughput.
- **Readiness Probe + Boot Stuttering** for *Fraud* and *AML* services (delayed activation; prevents stall).
- **Firewall / Backpressure + Circuit Breaker** for *DDoS*: resilience to flash-loan-induced bursts (e.g., *3 AM*).
- **Semaphores on Rate Limiting + CDP** for *Sybil protection*: each *KYC* session is *rate-limited*; per-request risk assessment is *fault-tolerant*.
- **Async / Promise / Fiber / Agent** for *high concurrency*: non-blocking IO; avoids cascading latency.
- **Token Bucket** for *rate-limited-by-channel*: adaptive rate-limiting; factors in *fraud score*, *device fingerprint*, *geographic origin*.

## 8. Reference architecture / worked example
**Problem:** A payment processor (150 branches, 12 countries) must sustain 50,000 TPS and integrate with *credit-bureau*, *identity-verification*, and *SWIFT* / *ACH* gateways.
**Decision:** Circuit Breaker + Bulkhead + Rate Limiting + Resilience.
```mermaid
graph LR
    classDef ok fill:#a7f3d0,stroke:#065f46
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5
    classDef data fill:#fde68a,stroke:#92400e
    classDef service fill:#bfdbfe,stroke:#1e40af

    Client[Payment Client]:::service --> GW(Payment Gateway :::service)
    GW --> Auth(AuthN / AuthZ :::service)
    Auth -->|Circuit Breaker| Cred(Credit Bureau :::service)
    Cred -->|Bulkhead| Settlement(Settlement :::service)
    Cred -->|Bulkhead| Fraud(Fraud :::service)
    Cred -->|Bulkhead| Report(Reporting :::service)
    Settlement -->|Rate Limiting| SWIFT(SWIFT :::boundary]
    SWIFT -->|Async IO| ACH(ACH :::boundary]
    Settlement -->|Cache |Cache[(Distributed Cache :::data)]
```
**ADR-093: Resilience Patterns for 50k TPS Payment Processor**
```markdown
# ADR-093: Resilience Patterns for 50k TPS Payment Processor
## Status
Accepted
## Context
Processor must sustain 50k TPS across 12 countries; downstream credit-bureau API is unreliable; PST endpoints (SWIFT/ACH) must absorb bursts; fraud can mask as legitimate traffic.
## Decision
Circuit Breaker on credit-bureau and identity APIs; Bulkhead on authorization/settlement/reporting; Rate Limiting + Token Bucket on all gateway loops; Asynchronous IO for non-blocking concurrency; Graceful Degradation to soft-hold for fraud; Distributed Cache for collateral-data to reduce latency spikes.
## Consequences
- Positive: Capacity to absorb upstream outage without total failure; reduced tail latency.
- Negative: Increased architectural complexity and debugging difficulty (e.g., latent cascading breaker trips).
- Negative: Distributed cache adds operational overhead (cache invalidation, consistency).
## Alternatives considered
1. Single-pool ordering: rejected—catastrophic single failure.
2. Asynchronous server communication: not possible due to latency.
```

## 9. Maturity & adoption signals
- **Adopt when:** >5 independent pipelines; SLOs require 99.99%; external dependencies are unreliable; regulatory resilience mandates (DORA).
- **Anti-signals (don't adopt yet):** <3 pipelines; single team; no on-call SRE; immature reliability measurements.
- **Common failure modes:** 1) *Misconfigured Circuit Breaker* (threshold wrong or always open) and masking real failures; 2) *Bulkhead starvation* (one pool exhausts shared resources); 3) *Load-shedding triggers false positives* and drops legitimate traffic, increasing false-positive *fraud* alerts.

## 10. Common confusions — the "don't mix" up list
| Often confused | Real distinction |
|----------------|------------------|
| Retry vs. Backoff | Retry *sends* the request; Backoff *retries* after delay. |
| Circuit Breaker vs. Bulkhead | Breaker prevents *cascade*; Bulkhead prevents *contention* between subsystems. |
| Rate Limiting vs. Throttling | Rate Limiting is *limit* (e.g., 100/s); Throttling is *temporary restriction* (e.g., 3 per minute, burst 10). |

## 11. Tools & standards to know
- **Standards/Frameworks:** ISO 9001, ISO/IEC 27001, ISO 27001, ISO 26262 (where applicable), PCI-DSS 3.0, DORA, MITRE ATT&CK, NIST SP 800-53.
- **Common tooling:** Hystrix (Netflix), Resilience4j (Lightbend), Envoy (proxies), Kong, Istio (Service Mesh), Kubernetes (HPA/VPA), Prometheus, Grafana, Sentry, PagerDuty, cloud-native metrics (CloudWatch, Azure Monitor), Datadog, Honeycomb.
- **Mandatory reading:** *Site Reliability Engineering* (Beyer et al., O'Reilly, 2016); *Patterns of Enterprise Application Architecture* (Martin Fowler); *Distributed Systems* (Tanenbaum; 3rd ed., 2022).

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
1. **Recall:** define Circuit Breaker vs. Bulkhead in 60 seconds.
2. **Model:** simulate a live diagram showing resilience patterns triggered by an overloaded upstream endpoint.
3. **ADR:** draft a Circuit-Breaker ADR for a Microservice pattern (C5-03).
4. **Defend:** explain to a non-technical CEO why our latency budget justifies (and requires) a 50ms timeout and a 3-retry queue.

## 14. Summary (1 paragraph)
Resilience patterns are the *shock absorbers* of architecture. By baking in circuit breakers, bulkheads, and timeouts you give your payment processor the *right to fail fast* without collapsing. In banking, where a 1-second stall can cost millions per minute, these patterns are not optional add-ons—they are the daily operational reality.

---
**Status:** ✅ Covered · **Last updated:** 2026-09-14
