# C3-04 Technology Architecture — BRIEF
> **Category:** C3 — Architecture Domains · **Difficulty:** ◑ · **Banking-relevant:** yes
> **One-liner:** Engineering the physical, virtual, and platform layer of the 💳 bank’s technology stack—cloud regions, languages, runtimes, and infrastructure—so that every application runs on the right substrate at the right cost and resilience.
> **Why an EA cares:** Choosing the wrong runtime platform (e.g., Python for high-throughput payments on a single-threaded runtime) or the wrong cloud region (EU vs. US) introduces latency, compliance (localization), cost, and operational risk that orgs cannot afford.

## Quick definition
Technology architecture defines the concrete forms of the platform: which cloud providers, regions, hypervisors, container runtimes, programming languages, operating systems, middleware, and infrastructure-as-code tooling the banking enterprise uses to host its applications and data.

## Key ideas / terms
- **Cloud-Native:** Building applications to exploit cloud elasticity, managed services, and APIs (e.g., auto-scaling, serverless).
- **Infrastructure as Code (IaC):** Provisioning and managing infrastructure via declarative code, not manual UI clicks.
- **Platform Engineering (CpC):** Building an internal developer platform that provides the building blocks for application teams to self-serve.
- **Polyglot Persistence:** Selecting the right data store for each workload rather than forcing everything into one database.
- **DevSecOps / CDSA:** Integrating security practices, secrets management, and continuous delivery for regulated systems.
- **Edge Computing:** Executing compute closer to the user or device to reduce latency (relevant for 💳 ATM and POS workloads).

## The mental model
Technology architecture is the foundation and utilities of a 💳 bank’s data center: just as a building needs the right soil, load-bearing materials, and grid connection, a bank’s platform needs the right cloud region, runtime, and deployment toolchain to support every service without collapse.

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

    USWest[AWS us-west-2 (regulated)]:::critical
    EUWest[Azure West Europe]:::critical
    ProdMktg[(Production / Role-based)]:::data
    DevTest[(Dev / Test)]:::context
    IaC[Terraform / KiND]:::decision
    K8S[Kubernetes]:::context
    Gateway[API Gateway (Kong)]:::service
    App[Application (Java / Go / Python)]:::service
    DB[(Database: Aurora / SQL + Redis)]:::data

    USWest --> K8S
    EUWest --> K8S
    K8S --> App
    App --> Gateway
    App --> DB
    IaC -. defines .-> USWest
    IaC -. defines .-> EUWest
    DevTest -. clones .-> USWest

    class USWest critical
    class EUWest critical
    class IaC decision
```

## When to use / when NOT to use
- ✅ **Use when:** You are selecting a new cloud region, runtime, or database for a regulated 💳 service, or building an internal developer platform.
- ⚠️ **Avoid when:** The workload is a simple internal reporting tool on a laptop with no access boundary.

## Banking 💳 example
A neobank launching across the EU and UK must choose cloud regions: MS Azure in West Europe for UK-localized GDPR data residency and AWS in EU-Central-1 for EU-wide payments; the technology architecture defines VPC peering, CDN endpoints, and a shared secrets manager with role-based access so that UK data never replicates to the US region.

## Common confusions (don't mix these up)
- **Technology Architecture** vs **Infrastructure Architecture:** Technology architecture is the *what* (languages, runtimes, platforms); infrastructure architecture is the *how* (networking, storage, hypervisors, multi-tenancy).

## Interview / recall prompt
_“Explain technology architecture in 2 minutes without notes.”_ →
- 1) It’s the concrete selection of cloud, runtime, languages, and platforms
- 2) It determines cost, latency, compliance, and operational burden
- 3) IaC and platform engineering make it repeatable and self-serve
- 4) Polyglot persistence and edge computing optimize for workload shape
- 5) In banking, region and data-residency rules are non-negotiable constraints

---
**Status:** ✅ Covered
