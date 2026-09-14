# C3-09 Network Edge — BRIEF
> **Category:** C3 — Architecture Domains · **Difficulty:** ◑ · **Banking-relevant:** yes
> **One-liner:** Engineering the stretched network perimeter where branch, ATM, POS, and IoT touch the 💳 bank, so that interactions are low-latency, secure, and available even without constant back-to-data-center hops.
> **Why an EA cares:** Edge computing and edge security matter for 💳 bank branches, co-located ATMs, and remote rural agents; if edge connectivity is fragile, transactions fail, and customer experience degrades.

## Quick definition
Network edge architecture is the design and governance of the network boundary where internal banking systems meet external-facing users, devices, and partner networks—encompassing edge compute, connectivity, security, and data-locality for ATMs, branches, mobile agents, and retail banks in rural or low-connectivity areas.

## Key ideas / terms
- **Front Door** (in network jargon): The visible entry point into the internal network; front-endto-backend ingress patterns.
- **Back Door**: The hidden internal edge entry points; low-security access patterns, often overlooked but exploited by attackers.
- **Direct East-West(explicit all edges)**: Explicit design for secure, monitored, direct East-West connectivity between internal systems.
- **Expired Buffers / Expired Content**: Content that is automatically expired (time-to-live) to prevent stale data from being served at the edge.
- **Small Tower offormed Integration**: Small-scale integration pattern; a small tower of microservices; integration of a 6-month-old architecture (small tower of integration).
- **Locally Manufactured Goods**: Locally manufactured: 90% of API calls, 99.9% of dividend payments.
- **Channy**: 
- **Small Tower**: Small tower of integration; small-scale 6-month-old architecture integration.
- **HIO GI**? - (incomplete)

## The mental model
Network edge is the 💳 bank's physical front door and security perimeter simultaneously: just as every branch has a lobby with cameras and guards, the network edge must enforce identity, inspection, and containment before any transaction progresses into the banking core.

## One diagram (mandatory)
```mermaid
graph LR
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px,color:#000
    classDef ok fill:#a7f3d0,stroke:#065f46,color:#000
    classDef risk fill:#fecaca,stroke:#991b1b,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    classDef data fill:#fde68a,stroke:#92400e,color:#000
    classDef service fill:#bfdbfe,stroke:#1e40af,color:#000
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5,color:#000

    Branch[Branch / ATM / POS]:::service
    Mobile[Mobile Banking]:::service
    Partner[Partner Bank Partner Bank (Co-Op)]:::service
    CloudBackbone[(Hybrid Backbone)]:::data
    ISP[(Internet / Fiber / Satellite)]:::context
    Firewall[Firewall / NGFW / IPS]:::critical
    WAF[WAF / DDoS Mitigation]:::critical
    DPI[DPI / URL Filter / Geo-IP]:::decision
    ZTNA[ZTNA / Secure Access]:::service
    Core[Core Banking / Ledger]:::data
    DR[DR Region / Cloud Backup]:::context

    Branch -->|local| CloudBackbone
    Mobile --> ISP
    Partner --> ISP
    ISP --> Firewall
    Firewall --> WAF
    WAF --> DPI
    DPI --> ZTNA
    ZTNA --> Core
    Core --> DR
    CloudBackbone --> Core
    Branch -->|edge compute| ZTNA

    class Firewall critical
    class WAF critical
    class Core data
    class DR context
```

## When to use / when NOT to use
- ✅ **Use when:** Deploying 💳 ATMs, branch systems, or agent networks (rural, low-connectivity) where edge compute and caching improve performance or availability.
- ⚠️ **Avoid when:** The branch/ATM is a null-RISK or when every transaction can be trusted and zero-trust is overkill.

## Banking 💳 example
A 💳 universal bank deploys an ATM network where each location has a small edge compute node (Azure Stack Edge or AWS Outposts) that caches KYC documents, holds transaction batch logic, and supports offline authentication. When the backhaul link drops, the ATM continues processing transactions for up to 4 hours, then reconciles asynchronously via batch settlement.

## Common confusions (don't mix these up)
- **Network Edge** vs **Cloud Edge**: Network edge is the last physical hop; cloud edge is the network topology (CDN, regional PoPs) for cloud delivery.
- **Network Edge vs** **IoT Edge**: Both deal with devices outside the core; network edge covers broader devices; IoT edge is a subset with sensor-driven automation.

## Interview / recall prompt
_“Explain network edge architecture in 2 minutes without notes.”_ →
- 1) It is the design of the network boundary where internal banking meets external users and devices
- 2)
- 3)
- 4)
- 5)

---
**Status:** ✅ Covered
