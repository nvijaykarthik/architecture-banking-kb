# [C10-10] 5G / IoT / Edge — DETAIL
> **Category:** C10 — Emerging & Advanced Topics · **Difficulty:** ○/◑/● · **Banking-relevant:** yes
>
> **Companion brief:** `[briefs/C10-10-5giot-edge.md](../briefs/C10-10-5giot-edge.md)`
>
> **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.
>
> ---
>
> ## 1. Precise definition
> 5G / IoT / Edge computing is the convergence of the fifth-generation cellular radio access network (5G), the Internet of Things (IoT), and edge computing, where stateless or semi-stateless compute is deployed close to the data source to reduce latency and bandwidth. In banking, this trend is particularly acute for: ATM cash management and telemetry, branch video surveillance, real-time low-latency payment processing, secure device access (biometrics, smart cards), and asset tracking for cash-in-transit.
>
> ## 2. Why it exists (problem it solves)
> Banks have long used 4G for ATM status reporting and branch connectivity. However, 4G (and 3G) cannot guarantee ultra-low latency (< 1 ms) and cannot scale to hundreds of thousands of devices per branch. The new business requirements are: safety (OSM3G/5G standards for real-time analytics that detect ATM fraud in camera), customer experience (instant top-ups, digital onboarding in branch via smart kiosks), and operational efficiency (automated ATM replenishment via real-time telemetry). 5G/IoT/Edge solves all three by decoupling latency from distance.
>
> ## 3. Core concepts & vocabulary
> | Term | Precise meaning |
> |------|-----------------|
> | 5G Radio Access Network (RAN) | The wireless access network infrastructure (gNodeBs), that connects devices (cell phones, ATMs, IoT) to the core via URLLC and mMTC.
> | URLLC (Ultra-Reliable Low-Latency Communication) | A 5G capability tier that provides ultra-low latency (sub-1 ms) and 99.999% reliability for applications like real-time trading and bank branch security.
> | mMTC (Massive Machine-Type Communications) | A 5G capability tier supporting millions of low-power IoT devices per square kilometer.
> | Network Slicing | Virtualized partitioning of the 5G RAN into multiple logical networks, each optimized for a specific use case (e.g., a high-priority slice for ANS, a low-bandwidth slice for ATM telemetry).
> | Edge Computing | Processing data at or near the edge server (e.g., in the ATM or branch), reducing data travel distance and latency.
> | IoT (Internet of Things) | Devices like ATMs, kiosks, biometric readers, sensors, and cash-in-transit vehicles that generate telemetry and require connectivity.
> | PDU Isolation (PDU Session Isolation) | The carrier's request for a separate IP path for a logical service.
> | Multi-access Edge Computing (MEC) | A standardized framework for placing compute and storage as close to the network edge as possible.
>
> ## 4. How it works (architecture / mechanism)
> ### 4.1 Diagrams
> **Diagram A — Core structure (highlight load-bearing parts = amber, supporting = grey):**
>
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
>     classDef context fill:#dfe6e9,stroke:#636e72
>     classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
>     classDef ok fill:#a7f3d0,stroke:#065f46
>     classDef service fill:#bfdbfe,stroke:#1e40af
>
>     ATM[ATM / Branch]:::context
>    BANK[Virtual Cell Site]:::critical
>    EDGE[Edge Compute]:::service
>    CLOUD[Cloud Bank]:::context
>    DB[(Core)]:::ok
>    
>     BANK -->|5G RAN| ATM
>     BANK -->|MEC| EDGE
>     EDGE -->|cache| CLOUD
>     EDB -->|query| DB
> ```
>
> **Diagram B — Edge vs Cloud data flow (highlight decision = green, risk = red):**
>
> ```mermaid
> flowchart LR
>     classDef ok fill:#a7f3d0,stroke:#065f46
>     classDef risk fill:#fecaca,stroke:#991b1b
>     classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
>
>     ATM[ATM]:::ok
>    CAM[Video Sensor]:::ok
>     EDGE[Edge Compute]:::decision
>     CLOUD[Cloud Bank]:::ok
>
>    ATM -->|telemetry| EDGE
>    CAM -->|raw video| EDGE
>    EDGE -->|metadata| CLOUD
> ```
>
> ## 5. Variants, options & trade-offs
> | Variant | When to pick | When to avoid | Key trade-off axis |
> |---------|--------------|---------------|--------------------|
> | 5G + Edge | ATM cash management, branch video, real-time payment processing, low-latency use cases | High security, air-gapped | Latency vs. security |
> | 5G + Cloud | Aggregate bank reporting, CRM, cloud-native core | Offline ATM, branch | Latency vs. scalability |
> | 5G + IoT + Edge + 5G + Cloud + Edge (hybrid)
> | 5G + On-Prem (edge at branch / ATM) | Network outage tolerance, real-time processing, data privacy | High operational cost, small-scale | Latency vs. cost |
>
> ## 6. Relationships to sibling topics
> - **Zero Trust (C10-06):** Edge computing is the riskiest part of the 5G/IoT/Edge architecture; ZTA must enforce per-device identity, device attestation, and micro-segmentation at the edge.
> - **Kubernetes (C10-04):** Edge can run a lightweight K8s cluster for edge compute.
> - **Smart Contracts? (C10-09):** No; smart contract is a blockchain concept, not 5G/IoT/Edge.
> - **Serverless (C10-03):** Edge can be implemented with serverless functions at the edge, but the stack must be managed.
>
> ## 7. Banking / financial-services context 💳
>
> A major European bank (6,000 ATMs, 200 branches) operates a private 5G network (S2S) connecting ATM status telemetry, cash vault inventory, and branch video to a central control center. The bank uses a 5G network slice for ATMs (high priority, low latency) and a separate slice for surveillance cameras (high bandwidth, moderate latency). 5G is the riskiest part of the 5G/IoT/Edge architecture because it is the only part with a public API and the most direct attack surface; ZTA must enforce per-device identity, device attestation, and micro-segmentation at the edge.
>
> A U.S.-centric bank deploys 5G with a single tower and private LTE to connect 500 manager-less ATMs (mATMs) over a shared 5G network (providing an even smaller attack surface). The bank uses 5G to enable real-time fraud detection at the ATM (sudden alerts) and to provide automated PIN verification (using a local AI model on the edge).
>
> A specialized blockchain firm is deploying 5G and edge to retail bank branches in a cashless environment (e.g., an ATM branch with a single ATM, no cash-handling staff).
>
> 5G is the riskiest part of the 5G/IoT/Edge architecture because it is the only part with a public API and the most direct attack surface; ZTA must enforce per-device identity, device attestation, and micro-segmentation at the edge.
>
> ## 8. Reference architecture / worked example
>
> **Problem:**
> A UK bank operates 12,000 ATMs and wants real-time cash-level telemetry and video surveillance. With 4G, latency is too high for real-time fraud alerts; video processing requires cloud bandwidth that is unreliable in rural branches.
>
>
> **Decision:**
> Deploy a 5G network with a dedicated network slice for ATMs, leveraging edge compute at each branch for local video analytics and pre-processing; send only metadata (metadata) to the cloud; centralize the control plane.
>
>
> The architecture diagram:
>
> ```mermaid
> graph LR
>     classDef service fill:#bfdbfe,stroke:#1e40af
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
>     classDef context fill:#dfe6e9,stroke:#636e72
>     classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5,color:#64748b
>     classDef ok fill:#a7f3d0,stroke:#065f46
>     classDef data fill:#fde68a,stroke:#92400e
>
>     ATM1[ATM 1]:::context
>    ATM2[ATM 2]:::context
>     CAM[Camera]:::context
>    SCP[ATM / Edge Compute]:::service
>     EDGE[MEC]:::service
>    NET[5G RAN]:::critical
>    CEN[Cloud Bank]:::boundary
>    DB[(Core / Cloud)]:::data
>
>     ATM1 -->|5G| NET
>    ATM2 -->|5G| NET
>    CAM -->|5G| NET
>    NET -->|slice| EDGE
>    EDGE -->|metadata| CEN
>    NET -->|slice| CEN
>    CEN -->|store| DB
> ```
>
>
>
>
> **ADR drafted:**
>
> ```markdown
> # ADR-2025-078: 5G + Edge for ATM + Branch Operations
>
> ## Status
> Accepted
>
> ## Context
> 2024 regulatory review (DORA) flagged ATM cash management as having > 200 ms average alert latency; branch video upload requires 5-second video, causing missed alerts.
>
> ## Decision
> Deploy 5G with a dedicated network slice for ATM telemetry and a second slice for branch surveillance; place edge compute in each branch for local video, AI fraud detection, with metadata-only upload to a central 5G-connected cloud.
>
> ## Consequences
> - Positive: < 50 ms alert latency; 10 Gbps bandwidth per slice; reduced cloud egress by 85%.
> - Negative: $2M/year 5G slice costs; 5G network maintenance costs.
> - ...
> ## Alternatives considered
> 1. Wi-Fi + edge: Rejected (unreliable coverage for remote branches).
> 2. 4G + centralized: Rejected (500 ms latency, unsustainable).
> ```
>
> ## 9. Maturity & adoption signals
> - **Adopt when:** ATM count > 1,000; remote branches require video; real-time fraud is mission critical; DORA requires low latency.
> - **Anti-signals (don't adopt yet):** < 100 ATMs; fully centralized (no smart branch); no regulatory latency requirement.
> - **Common failure modes:** 5G signal interference (EMF), single-carrier dependency (reduce risk via multi-carrier network slicing), and lack of multi-Tenancy in 5G cell sites.
>
> ## 10. Common confusions — the "don't mix" list
>
> | Often confused | Real distinction |
> |----------------|------------------|
> | 5G vs 4G vs LTE-A | 5G is a generation of radio access; 5G also includes URLLC and network slicing.
> | IoT vs Edge vs Fog | IoT = devices; Edge = compute close to device; Fog = intermediate layer between edge and cloud.
> | 5G vs Wi-Fi | 5G is a cellular network and a radio; Wi-Fi is a local area network; 5G can be used in enterprise Wi-Fi with a network.
> | 5G vs Edge | 5G is the transport; Edge is the compute placement.
> | 5G vs 5G | (self-confused).
>
> ## 11. Tools & standards to know
> - **Standards/Frameworks:** 3GPP 5G NR (NR standards) for radio; 5G NR: eMBB, URLLC, mMTC; NIST 800-217 (cybersecurity for CPS); ETSI MEC for multi-access edge computing; gbps/gigabit for throughput.
> - **Common tooling:** Cisco 5G Core, Nokia Multi-Access Edge Compute (MEC), Oracle Cloud Infrastructure (OCI) 5G; Nokia, Ericsson, Alcatel-Lucent, Juniper Networks, Proxelynx, 5G RedCap, O-RAN, Cdr, Wanchain.
> - **Mandatory reading:**
>   - *5G: A Technology Guide* by Adrian Hope-Baily;
>   - *Building Smart Cities: Using Sensors and the Internet of Things* by Thomas Terry.
>
> ## 12. ADR template (ready to fill in)
>
> ```markdown
> # ADR-XXX: <decision>
> ## Status
> Accepted | Proposed | Deprecated
> ## Context
> ...
> ## Decision
> ...
> ## Consequences
> - Positive ...
> - Negative ...
> - ...
> ## Alternatives considered
> 1. ...
> 2. ...
> ```
>
> ## 13. Practice — apply it
> 1. **Recall:** Define URLLC in 2 min without notes.
> 2. **Model:** Draw a 5G network slice architecture.
> 3. **ADR:** Write an ADR for a 5G slice for a bank branch.
> 4. **Defend:** Explain to a non-technical CRO why "5G" does not make edge security automatic.
>
> ## 14. Summary (1 paragraph)
>
> 5G/IoT/Edge is the bank's new nervous system: it extends the central bank's reach to every ATM, branch, and cash-in-transit vehicle via ultra-reliable, low-latency radio. The risk is not the edge compute—it's the radio.

---
**Status:** ✅ Created · **Last updated:** 2026-09-14
