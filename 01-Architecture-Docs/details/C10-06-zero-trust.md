# [C10-06] Zero Trust Architecture — DETAIL
> **Category:** C10 — Emerging & Advanced Topics · **Difficulty:** ●/◑/○ · **Banking-relevant:** yes
>
> **Companion brief:** `[briefs/C10-06-zero-trust.md](../briefs/C10-06-zero-trust.md)`
>
> **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.
>
> ---
>
> ## 1. Precise definition
> Zero Trust Architecture (ZTA) is a strategic security framework defined by NIST SP 800-207 (2020) and expanded by CISA (2021) and the EU's DORA (2022/2554) as a set of principles: identity and device as the primary enforcement locus, least-privilege access, software-defined perimeters, continuous validation, and assuming breach. It is not a product but a **mandate**: the network border is demoted; every microservice, device, and user must present verified credentials for every request.
>
> ## 2. Why it exists (problem it solves)
> The 2014 Sony Pictures hack, the 2017 Equifax breach, and the 2024 MGM Resorts ransomware incident revealed the flaw in the "trusted internal network" model: lateral movement within the enterprise is the dominant attack path. Banks, holding PCI-DSS Scope, PII, and critical infrastructure, became prime targets. ZTA addresses this by making the internal network as hostile as the public internet, forcing attackers to re-authenticate and re-attest at every hop.
>
> ## 3. Core concepts & vocabulary
> | Term | Precise meaning |
> |------|-----------------|
> | Zero Trust (ZTA) | SAML / mTLS / certificate-based identity as the enforcer; every request is a validated transaction. |
> | Software-Defined Perimeter (SDP) | A virtual network that hides internal infrastructure until the endpoint is authenticated and authorized. |
> | Micro-Segmentation | Network segmentation at the application layer; each service is a separate zone with explicit policies. |
> | Just-In-Time (JIT) Access | Privileges granted for a short duration then revoked; reduces blast radius and escalation windows. |
> | Continuous Validation | Real-time device health checks, certificate rotation, revocation, and re-attestation; done via the risk scoring engine. |
> | Least Privilege | The principle that access is granted only for the specific data/function needed; implemented via ABAC (Attribute-Based Access Control). |
> | Identity & Access Management (IAM) | Centralized authentication; the "new perimeter"; not "the network." |
> | NIST SP 800-207 | The foundational Zero Trust architecture framework; CISA's 5-step migration guide (2021). |
>
> ## 4. How it works (architecture / mechanism)
> ### 4.1 Diagrams
> **Diagram A — Core structure (highlight the load-bearing parts = amber, supporting = grey):**
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
>     classDef context fill:#dfe6e9,stroke:#636e72
>     classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
>     classDef ok fill:#a7f3d0,stroke:#065f46,stroke-width:1px
>     classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5,color:#64748b
>
>     USER[User / Device]:::context
>     MGMT[Identity & Access Mgmt Center]:::critical
>     POL[Policy Engine]:::critical
>     SDP[Software-Defined Perimeter]:::boundary
>     ZONE[Micro-Segmented Zone]:::context
>     PMS[Payment Service]:::ok
>     VAULT[(Vault)]:::critical
>
>     USER -->|authenticate + attest| MGMT
>    MGMT -->|evaluate| POL
>    POL -->|grant| SDP
>    SDP -->|authorize| ZONE
>    ZONE -->|access| PMS
>    PMS -->|retrieve| VAULT
> ```
>
> **Diagram B — Attack path vs. Zero Trust (highlight decision points = green, risks = red):**
> ```mermaid
> flowchart LR
>     classDef ok fill:#a7f3d0,stroke:#065f46
>     classDef risk fill:#fecaca,stroke:#991b1b
>     classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
>
>     BREACH[Breached Outer IP]:::risk
>    TRAD[Traditional Trust]:::critical
>   ZT[Zero Trust]:::decision
>    LATERAL[Lateral Movement Allowed]:::ok
>    BLOCK[Blocked, Re-auth Require]:::ok
>
>    BREACH -->|trusted| TRAD
>    TRAD --> LATERAL:::ok
>    BREACH --> ZT:::decision
>    ZT --> BLOCK:::ok
> ```
>
> ## 5. Variants, options & trade-offs
> | Variant | When to pick | When to avoid | Key trade-off axis |
> |---------|--------------|---------------|--------------------|
> | Full-Cloud ZTA (Cloudflare ZTA, Zscaler) | Hybrid/Multi-cloud, remote workforce | Fully on-prem, strict data-residency | Features vs. latency |
> | Self-Hosted ZTA (HashiCorp, CNI, OPA) | Strict data residency, no cloud vendor lock-in | Small team, budget constraints | Control vs. complexity |
> | SaaS ZTA (Okta, Azure AD, Okta Guardian) | Rapid adoption, pre-built integrations | Custom policy logic, bespoke risk signals | Speed vs. flexibility |
>
> ## 6. Relationships to sibling topics
> - **Kubernetes (C10-04):** Kubernetes network policies and PodSecurityPolicies implement micro-segmentation; but ZTA extends to identity, not just network labels.
> - **API Economy (C10-05):** Every API call is a ZTA transaction; API Gateway and mTLS are the enforcement planes.
> - **Event-Driven (C10-02):** Events should be signed/encrypted in the event stream itself; "never trust a Kafka broker."
>
> ## 7. Banking / financial-services context 💳
> A Tier-1 global investment bank migrated its trading floor to a Zero Trust posture: every trader's workstation passes certificate-based Windows/macOS attestation, risk scoring runs via real-time API, and access to the Bloomberg EMSX is JIT (15 minutes). The network is segmented into dozens of micro-zones: the "Payments Zone" cannot access the "Research Zone," even if the workstation has both IP ranges. This meets DORA's ICT investigative and disclosure requirements and CISA's mandatory detection of lateral movement.
>
> ## 8. Reference architecture / worked example
> **Problem:** A bank's remote DevOps team needs to access production container pods in the payments namespace without granting persistent elevated privileges or a wide-open VPN.
>
> **Decision:** Deploy a self-hosted Zero Trust mesh: Open Policy Agent (OPA) for policy-as-code, SPIFFE/SPIRE for workload identity, and a JIT access service that issues short-lived, audited credentials.
>
> ```mermaid
> graph LR
>     classDef service fill:#bfdbfe,stroke:#1e40af
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
>     classDef context fill:#dfe6e9,stroke:#636e72
>     classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5,color:#64748b
>     classDef data fill:#fde68a,stroke:#92400e
>
>     DEV[DevOps]:::context
>     SPIFFE[SPIFFE / SPIRE]:::critical
>    WORKSPACE[Workload]:::service
>    BUD[Policy Enforcer - OPA]:::critical
>    API[Access API (JIT)]:::service
>    LOG[(Audit Log)]:::data
>
>     DEV -->|request| API
>     API -->|credential| SPIFFE
>     SPIFFE -->|attest| WORKSPACE
>    WORKSPACE -->|request| BUD
>    BUD -->|allow| WORKSPACE
>    API -->|log| LOG
> ```
>
>
>
> **ADR drafted:**
> ```markdown
> # ADR-2025-069: Zero Trust JIT Access for Production DevOps
>
> ## Status
> Accepted
>
> ## Context
> 2024 audit found that 3 critical production accounts had remote VPN access with 1-year-long static keys.
>
> ## Decision
> Implement SPIFFE-based workload identity + OPA policy-as-code; replace static VPN keys with 30-minute JIT credentials.
>
> ## Consequences
> - Positive: Blast radius reduced from "any VM on VPN" to "1 specific credential for 30 min."
> - Negative: 2-month migration; requires 6-person dev team; dev tools need SPIFFE agent.
> - ...
> ## Alternatives considered
> 1. Privileged Access Management (PAM) appliance: Rejected (cannot scale to 2000 pods).
> 2. Self-hosted ZTA mesh: Accepted.
> ```
>
> ## 9. Maturity & adoption signals
> - **Adopt when:** > 50% of workforce is remote or multi-cloud; PCI-DSS v4.0 or DORA audit requirements; any device outside the perimeter.
> - **Anti-signals (don't adopt yet):** Single-site, trusted firewall model; no remote workforce; budget < $500k.
> - **Common failure modes:** "Zero Trust theater" (only one layer is applied, e.g., only MFA, not JIT); policy sprawl (hundreds of OPA rules); latency spikes on real-time risk scoring.
>
> ## 10. Common confusions — the "don't mix" list
> | Often confused | Real distinction |
> |----------------|------------------|
> | Zero Trust vs VPN | VPN = "trust on source IP"; ZTA = "trust on identity, not IP." |
> | Zero Trust vs Micro-Segmentation | Micro-segmentation is a network tactic; ZTA is a strategy.
> | Zero Trust vs SASE / SSE | SASE = converged network/security; SSE = user-service URL policy.
>
> ## 11. Tools & standards to know
> - **Standards/Frameworks:** NIST SP 800-207 (2020); CISA Zero Trust Maturity Model (5-step); PCI-DSS v4.0 (vulnerability management, identity management even at the cloud level); DORA ICT risk (Cybersecurity).
> - **Common tooling:** Zscaler ZPA/ZTNA, Palo Alto Cortex, HashiCorp Vault, SPIFFE/SPIRE, Open Policy Agent (OPA), CNI (Calico, Cilium), Teleport, Okta, Microsoft Entra ID, Duo, Microsoft Defender for Cloud Apps (CASB).
> - **Mandatory reading:** "Zero Trust Architecture" by NIST IR 8273; CISA "Zero Trust Maturity Model"; "SASE: The Definitive Guide."
>
> ## 12. ADR template (ready to fill in)
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
> 1. **Recall:** Define just-in-time access in 2 minutes without notes.
> 2. **Model:** Draw an ArchiMate/UML model showing 3 micro-segments with ZTA policy enforcement.
> 3. **ADR:** Write an ADR for 'Zero Trust access on the payments API gateway' to your mention.
> 4. **Defend:** Role-play to a non-technical CIO that 'Zero Trust is not 'YudrSS a product; why' and.
>
> ## 14. Summary (1 paragraph)
> Zero Trust is the single most important shift in banking cybersecurity in the last decade: it demotes the network boundary from trusted to hostile and places identity, device health, and continuous validation at the center of every interaction. It is not a product but a mandate—enforced by CISA, DORA, and PCI—under which every printer, trader's laptop, and Kubernetes pod must prove its worthiness for each request.
>
>
> ---
> **Status:** ✅ Created · **Last updated:** 2026-09-14
>