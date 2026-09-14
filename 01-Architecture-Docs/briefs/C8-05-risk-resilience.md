# [C8-05] Risk & Resilience — BRIEF
> **Category:** C8 — Reference Architecture, Standards & Principles · **Difficulty:** ◑ · **Banking-relevant:** yes
> **One-liner:** Risk & resilience architecture is the design of system behaviors under stress—failures, attacks, disasters—so that banking operations (payments, settlements, KYC) continue to meet their service levels and regulatory recovery-time objectives.
> **Why an EA cares:** A resilience failure in payments or risk-reporting is not a blip; it is a Q4 write-down, a regulatory investigation, or a systemic counterparty trust failure.

## Quick definition
**Risk & resilience** architecture encompasses the design patterns, runbooks, and infrastructure behaviors that keep a bank’s critical systems operational under abnormal conditions—hardware failures, cloud-region outages, cyberattacks, supply-chain compromises, and natural disasters. It is expressed in the *quality attributes* of availability, recoverability, modifiability, and security (ISO/IEC 25010), and measured by *service-level objectives* (SLOs) and *recovery-time objectives* (RTOs/RPOs).

## Key ideas / terms
- **Availability:** the probability (or percentile) that a system meets its SLO over a measurement window.
- **RTO / RPO:** recovery-time objective (max tolerable downtime) and recovery-point objective (max tolerable data-loss).
- **N+1 / N+2 redundancy:** spinning up one or two extra instances beyond the baseline load.
- **Chaos engineering:** the practice of injecting controlled failures to test resilience *before* real incidents.
- **Blast-radius containment:** architectural patterns (circuit breakers, bulkheads, service-mesh traffic-shifting) that limit the propagation of a failure.
- **Tier 1 / Tier 2 / Tier 3 systems:** classification of criticality (1 = payments, settlement; 3 = internal analytics).

## The mental model
Imagine a UK real-time payment gateway: if it goes down for 30 minutes during a trading day, that is not merely a reliability issue—because the Bank of England and Treasury observe GBP/EUR liquidity from that stream, a gap can trigger a *systemic liquidity warning*. Resilience architecture is therefore not about *computers*; it is about *confidence in trust*. It asks: if the underground fiber cut in Frankfurt, does the euro-landscape settlement still flow within 500ms?

## One diagram (mandatory)
```mermaid
graph LR
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef risk fill:#fecaca,stroke:#991b1b,stroke-width:1px
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
    classDef ok fill:#a7f3d0,stroke:#065f46,stroke-width:1px
    
    Reg[Regulators<br/>(EBA / BoE)]:::critical -->|enforce|<4h[RTO 4 hours<br/>DORA]]:::risk
    
    User[Cardholder /<br/>Corporate User]:::decision
    User -->|initiates| Tx[Transaction]:::critical
    Tx -->|routed via| Gateway[API<br/>Gateway]:::service
    
    Gateway -->|circuit breaker| Svc2[Service B<br/>(Redis Cache)]:::service
    Gateway -->|bulkhead| Svc1[Service A<br/>(Core]:::service
    
    Svc1 -->|logger| LogStore[(Immutable<br/>Event Store)]:::data
    
    Svc1 -.->|degraded| Alert[Alert /<br/>Escalation]:::risk
    
    LogStore -->|replay| DR1[DR Site<br/>(Azure West Europe)]:::decision
    
    classDef service blue
    class Gateway,Svc1,Alert,DR1 service
    class Tx,User,Reg critical
    class <4h risk
    class LogStore data
```

## When to use / when NOT to use
- ✅ **Use when:** payments, risk-reporting, or KYC systems must meet DORA 4-hour incident-response and sub-5-minute payment-SLA; or when designing across multiple cloud regions.
- ⚠️ **Avoid when:** purely internal analytics or a one-off reporting dashboard with no customer impact and no regulatory SLA.

## Banking 💳 example
A payment gateway processes £40B/day. The EA mandates:
- **Circuit breaker:** pricing service failure does not block card-authorization.
- **Bulkhead:** the UK retail-credit scoring path uses a separate Redis cluster from the corporate-trade-finance path.
- **Chaos:** weekly Gremlin rollouts kill the database connection pool for the stress-pricing engine; if users still see rates and the gateway routes to the fallback, greenlight.
- **BGP multi-homing:** dual upstream at both Equinix SV4 and BT East London to survive a fiber cut, with automatic failover.
- **RPO 5 min / RTO 15 min:** any data written to the primary is replicated to the DR site; if the primary fails, a cold-standby containerized stack spins within 15 minutes.

## Common confusions (don't mix these up)
- **Resilience** vs **High availability:** resilience = surviving unknown/fail-pattern stress; availability = predictable uptime percentage.
- **RTO vs. RPO:** RTO = time to restore; RPO = data-loss tolerance.
- **N+1 redundancy** vs **active-active failover:** N+1 is spare capacity; active-active is simultaneous processing.
- **Failover** vs **Failback:** failover = moving traffic; failback = returning traffic, which is a distinct and often-overlooked recovery step.

## Interview / recall prompt
“Explain risk & resilience architecture in 2 minutes without notes.” →
- It is the design for *abnormal* conditions, not normal loads.
- Measured by SLO, RTO, RPO, and blast-radius containment.
- Applies tiered classification: Tier 1 = payments, Tier 2 = reporting, Tier 3 = internal tools.
- Verified by chaos engineering and independent disaster-recovery tests.
