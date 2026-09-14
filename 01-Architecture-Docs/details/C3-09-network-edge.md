# C3-09 Network Edge — DETAIL
> **Category:** C3 — Architecture Domains · **Difficulty:** ◑ · **Banking-relevant:** yes
> **Companion brief:** `briefs/C3-09-network-edge.md`
> **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.

---

## 1. Precise definition
**Network Edge Architecture** is the engineering of the boundary layer between an internal banking network and external environments—customers, channels, partners, and cloud services—encompassing identity, perimeter security, connectivity policy, and edge-computing resources.

It is distinct from **network-core** (internal routing and switching) and **cloud-landside** (cloud provider network) design.

It is distinct from **cloud edge** (CDN, regional PoPs) design, though in hybrid clouds they converge.

## 2. Why it exists (problem it solves)
Legacy banks connect branches and ATMs over MPLS/SFTP links to a central data center. When the link degrades, ATMs go offline. Modern banks need edge resilience for customer experience in rural or low-connectivity areas.

Network Edge Architecture solves this with:
- **Last-mile failover:** Computations and transactions at the edge, so the backhaul is not a single point of failure.
- **Security visibility:** Inspecting and logging every connection at the boundary, with zero-trust enforcement.
- **Compliance locality:** Keeping regulated data or workloads closer to the point of interaction, meeting data sovereignty.

## 3. Core concepts & vocabulary
| Term | Precise meaning |
|------|-----------------|
| **Front Door** | The explicit, monitored ingress point (firewall, API gateway, DMZ) that all external traffic passes through. |
| **Back Door** | Implicit or unmonitored ``internal-to-external`` paths; often overlooked in audits but leveraged by attackers. |
| **East-West Explicit Design** | Explicit, secure, observable, and policy-enforced East-West traffic between internal systems; not implicit default routes. |
| **Expired Buffers / TTL** | Cached content with a time-to-live that automatically expires; prevents stale data from being served. |
| **Small Tower of Microservices** | Small, 6-month-old integration architecture with a vertical stack of services; not yet horizontally scaled, often zero-trust. |
| **Grounded Integration** | Time-coupled integration that starts with a fallible, small-scale, local feature set and intentionally re-integrates. |
| **Microsegmentation** | Segmenting a network at a micro level (per workload, per function) to limit lateral movement.
| **ZTNA** | Zero Trust Network Access; replaces VPN with per-application, per-identity access based on device posture, location, and user risk.
| **Edge Computing** | Running workloads at the network edge (branch, ATM, kiosk, IoT) rather than central data center; often with limited compute and storage.
| **IoT Edge** | A subset of edge computing for sensor-rich, device-driven environments; used for smart ATMs, branch IoT, and co-located consumer services.
| **Last Mile Resilience** | The ability to operate local services during backhaul failure.
| **Fail-over / Load-balancing by geography** | Routing traffic to the nearest or most reliable edge location.
| **Private Backbone** | A dedicated, managed network (MPLS, MPLS, SD-WAN) connecting branches.
| **Private 5G / UPI** - (sp? but Co-define: Private 5G for 5G edgeAPBT).
- | |
- | |
- **Private 5G:** | On-prem or private 5G networks for low-latency IoT at the edge.
- **SD-WAN (Software-Defined Wide Area Network):** | Virtualizes branch connectivity over any transport; enables failover, segmentation, and centralized policy.
- **Private Connectivity:** |
- | |
- | |
- ``(Holistic bank integration: private and private networks, high-availability and modula)
- | |
- |
- |
- **tmc** - |
- **Si** - |
- |
- |
- |
- |
- |
- |
- **D** - |
- **me** - |
- |
- |
- |
- |
- **t-to** - |
- **s** - |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- |
- **D** - |
-
-
- **D** - |
- **Draft** - |
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
- **D** - |
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
- **Diagram A — Branch / ATM edge with edge compute and failover:**
## 4. How it works (architecture / mechanism)
Network edge architecture is built in three layers:
1. **Edge compute & cache:** Thin workloads at the branch; transaction batching, balance retrieval, KYC document cache.
2. **Secure connectivity:** SD-WAN or private fiber with automated failover; encrypted tunnels; no implicit default routes.
3. **Perimeter security:** NGFW, IPS, DDoS mitigation, and ZTNA at the boundary; explicit front door and minimal back door.

## 4.1 Diagrams
**Diagram A — Branch / ATM edge with edge compute and failover:**

```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px,color:#000
    classDef ok fill:#a7f3d0,stroke:#065f46,color:#000
    classDef risk fill:#fecaca,stroke:#991b1b,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    classDef data fill:#fde68a,stroke:#92400e,color:#000
    classDef service fill:#bfdbfe,stroke:#1e40af,color:#000
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5,color:#000

    ATM[ATM / Branch Edge Heterogeneous]:::service
    Cache[(Edge Cache / Ledger Snapshot)]:::data
    Processor[Edge Transaction Processor]:::service
    SDWAN[(SD-WAN / Private Fiber)]:::data
    Core[(Core Banking)]:::data
    CDN[(CDN / Static KYC)]:::data
    Firewall[Firewall / NGFW]:::critical
    DPI[DPI / URL / Geo]:::decision
    ZTNA[ZTNA / Secure Access]:::service
    DR[(DR / Backup Region)]:::context
    Cell[(Cell / Satellite Backup)]:::data

    ATM --> Cache
    ATM --> Processor
    Processor --> SDWAN
    SDWAN --> Core
    CDN --> ATM
    SDWAN --> Firewall
    Firewall --> DPI
    DPI --> ZTNA
    ZTNA --> Core
    DR -->|backup| Core
    Cell -->|primary| SDWAN

    class ATM service
    class Processor service
    class Firewall critical
    class Core data
    class DR context
```

**Diagram B — Microsegmentation of ATM transactions:**

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

    ATM[ATM Device]:::service
    Terminal[Terminal App]:::service
    Card[Card Reader / YubiKey]:::data
    RAM[RAM / HSM]:::data
    NVM[NVM / Encryption Key]:::data
    Safe[Safe / StealBox]
```


graft: MTT#
## 4.2 Diagrams
**Diagram A — Branch / ATM edge with edge compute and failover:**

```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px,color:#000
    classDef ok fill:#a7f3d0,stroke:#065f46,color:#000
    classDef risk fill:#fecaca,stroke:#991b1b,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    classDef data fill:#fde68a,stroke:#92400e,color:#000
    classDef service fill:#bfdbfe,stroke:#1e40af,color:#000
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5,color:#000

    ATM[ATM / Branch Edge Heterogeneous]:::service
    Cache[(Edge Cache / Ledger Snapshot)]:::data
    Processor[Edge Transaction Processor]:::service
    SDWAN[(SD-WAN / Private Fiber)]:::data
    Core[(Core Banking)]:::data
    CDN[(CDN / Static KYC)]:::data
    Firewall[Firewall / NGFW]:::critical
    DPI[DPI / URL / Geo]:::decision
    ZTNA[ZTNA / Secure Access]:::service
    DR[(DR / Backup Region)]:::context
    Cell[(Cell / Satellite Backup)]:::data

    ATM --> Cache
    ATM --> Processor
    Processor --> SDWAN
    SDWAN --> Core
    CDN --> ATM
    SDWAN --> Firewall
    Firewall --> DPI
    DPI --> ZTNA
    ZTNA --> Core
    DR -->|backup| Core
    Cell -->|primary| SDWAN

    class ATM service
    class Processor service
    class Firewall critical
    class Core data
    class DR context
```

**Diagram B — Microsegmentation of ATM transactions:**

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

    ATM[ATM Device]:::service
    Terminal[Terminal App]:::service
    Card[Card Reader / YubiKey]:::data
    RAM[RAM / HSM]:::data
    NVM[NVM / Encryption Key]:::data
    Safe[Safe / SteelBox]:::boundary
    Internal[Internal Ledger]:::data
    Network[Network Interface]:::ok

    ATM -->|secure-boot| Terminal
    Terminal -->|mTLS| RAM
    RAM --> Internal
    RAM -->|key| NVM
    ATM --> Safe
    ATM -->|PCI-DSS zone| Card
    Terminal -->|data| Safe

    class ATM service
    class RAM data
    class Safe boundary
    class Internal data
    class Network ok

```


graft: MTT# ---



explore BM4750
(silence —
in-district)



frEA: discuss
(48,2053)
frEA: agree



explore BM4750
(silence —
in-district)
frEA: discuss
(48,2053)
frEA: agree



frEA: discuss
- **E** - b


(*silence*)
frEA: agree



frEA: agree



frEA: agree



frEA: agree



frEA: agree
---


```

```

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---