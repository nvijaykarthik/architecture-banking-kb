# [C10-03] Serverless Computing — DETAIL
> **Category:** C10 — Emerging & Advanced Topics · **Difficulty:** ○/◑/● · **Banking-relevant:** yes
>
> **Companion brief:** `[briefs/C10-03-serverless.md](../briefs/C10-03-serverless.md)`
>
> **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.
>
> ---
>
> ## 1. Precise definition
> Serverless computing is a cloud execution model in which code executes in ephemeral, immutable environments provisioned and managed by the cloud provider, with the consumer billed strictly on-demand (per-invocation, per-duration, or per-request count), without colocally managed servers, clusters, or containers (IaaS, PaaS, SaaS excluded) (Crockford, 2021). In banking, "serverless" is frequently used as shorthand for both Lambda/Azure Functions (FaaS) and managed container services (maybe included if required).
>
> ## 2. Why it exists (problem it solves)
> The traditional on-premise or IaaS model requires banks to staff 24/7 operations, purchase and patch servers for predictable peaks, and pay for idle capacity during off-hours. For workloads with sub-1% utilization (e.g., annual report generation, compliance document ingestion), serverless removes the fixed cost. It also reduces the TCO of site-reliability engineering (SRE) staff because the provider handles the flatlined components.
>
> ## 3. Core concepts & vocabulary
> | Term | Precise meaning |
> |------|-----------------|
> | Function-as-a-Service (FaaS) | The dominant serverless model: code is shipped and invoked in response to events, typically with < 15-minute execution timeouts. |
> | Concurrency | The maximum number of functions that may execute simultaneously; billed per request and per GB-second. |
> | Provisioned Concurrency | A premium feature that pre-warms functions to colocate execution contexts in memory, eliminating cold-start latency at higher unit cost. |
> | Eviction | The provider can terminate and destroy a container instance at any time; state cannot be assumed to persist between invocations. |
> | Payload Size Limit | Standard FaaS imposes a maximum function input and output size (e.g., Lambda: 6 MB input, 10 MB output); this is a hard boundary in banking if you must pass large files. |
> | Erlang / Libc | Critical for latency; underlying OS runtime libraries and garbage-collection pauses directly affect cold-start time. |
>
> ## 4. How it works (architecture / mechanism)
> ### 4.1 Diagrams
> **Diagram A — Core structure (highlight the load-bearing parts = amber, supporting = grey):**
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
>     classDef context fill:#dfe6e9,stroke:#636e72
>     classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
>     
>     API[API Gateway]:::context
>     AUTH[AuthZ Lambda]:::decision
>     KV[Fraud Filter Lambda]:::context
>     OCR[DocProcessor Lambda]:::context
>     S3[Object Store]:::context
>     
>     API -->|invoke| AUTH
>     AUTH -->|allow| KV
>     KV -->|pass| OCR
>     OCR -->|store| S3
> ```
>
> **Diagram B — Cold start to provisioned (highlight decision points = green, risks = red):**
> ```mermaid
> flowchart LR
>     classDef ok fill:#a7f3d0,stroke:#065f46
>     classDef risk fill:#fecaca,stroke:#991b1b
>     classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
>     
>     REQ[Request]:::ok
>     COLD[Cold Start]:::risk
>     WARM[Provisioned]:::decision
>     
>     REQ -->|low traffic| COLD:::risk
>     REQ -->|high traffic| WARM:::decision
>     WARM -->|sub-100ms| OK[Fast Return]:::ok
> ```
>
> ## 5. Variants, options & trade-offs
> | Variant | When to pick | When to avoid | Key trade-off axis |
> |---------|--------------|---------------|--------------------|
> | AWS Lambda / Azure Functions (Cold) | Bursty workloads, < 10 ms p99 not needed (CI/CD, batch jobs) | Fraud APIs with < 50 ms SLA | Cost vs. latency |
> | Provisioned Concurrency | Real-time fraud scoring, KYC biometric gates, payment-gate APIs | Infrequent long-running jobs | Cost vs. latency |
> | FaaS on-Kubernetes (Knative / OpenFaaS) | Needs local data residency, avoids multi-cloud lock-in | Less mature operational tooling; higher TCO | Vendor lock-in vs. compliance |
> | Serverless functions with persistent storage (DB-side) | Micro-services with fast startup but stateful backends (DynamoDB, CosmosDB) | Highly chatty workloads hitting provider endpoints | Control vs. ops |
>
> ## 6. Relationships to sibling topics
> - **Kubernetes (C10-04):** Serverless workloads are often *running on* Kubernetes (e.g., Knative), but managed FaaS abstracts the node. K8s is relevant for legacy container-based banks, serverless for greenfield fintech.
> - **Microservices (C3-01):** Serverless is an operational strategy for microservices; it is orthogonal to microservices existence.
> - **Event-Driven Architecture (C10-02):** Serverless functions are often the consumer side of an event-driven system; triggers (S3 events, Kafka topic events) are the bridge.
>
> ## 7. Banking / financial-services context 💳
> A retail bank runs its AML screening pipeline on serverless: downloads 100 MB of watch-list JSON, runs it through the browser-based VLOOKUP filtering algorithm, and writes a classification result to DynamoDB—in ~3 seconds total, at 1/100th the cost of a constantly-on VM. The fraud team uses provisioned concurrency for the p95 < 50 ms score-push API. The CIO must ensure that the third-party function image passes PCI-DSS runtime scanning; the provider's SOC 2 Type II does not exhaust the bank's own audit scope.
>
> ## 8. Reference architecture / worked example
> **Problem:** A bank's credit-card fraud system must score a transaction within 50 ms for authorization. Currently running on auto-scaling EC2, it costs $28k/month at 60% utilization because the peak applies to the *average* load.
>
> **Decision:** Keep the core scoring engine on a private K8s cluster (latency, p99 bound), but extract simpler "risk signal aggregation" into serverless functions triggered by transaction events from Kafka.
>
> ```mermaid
> graph LR
>     classDef service fill:#bfdbfe,stroke:#1e40af
>     classDef decision fill:#a364,stroke:#3f6212,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     classDef data fill:#fde68a,stroke:#92400e
>     
>     K8S[Scoring Core on K8s]:::context
>     FNS[Signal Agg Lambda]:::service
>     KAFKA[KAFKA Events]:::data
>     API[AuthZ API]:::decision
>     
>     API --> K8S
>     K8S -->|event| KAFKA
>     KAFKA --> FNS
>     FNS --> K8S
> ```
>
> **ADR drafted:**
> ```markdown
> # ADR-2025-061: Hybrid K8s + Serverless Fraud Scoring
> ## Status
> Accepted
> ## Context
> The 2024 annual audit found that 34% of our infrastructure cost is allocated to a constantly-idling fraud-scoring tier.
> ## Decision
> Extract "risk signal aggregation" to provisioned-concurrency Lambda; maintain real-time path on K8s.
> ## Consequences
> - Positive: $18k/month savings; sub-50ms path unchanged.
> - Negative: Split-brain monitoring (two APMs); requires cross-platform observability.
> - ...
> ## Alternatives considered
> 1. All-serverless: Rejected (cold-start risk on critical path).
> 2. All-on-K8s: Rejected (unable to achieve $28k/month at low utilization).
> ```
>
> ## 9. Maturity & adoption signals
> - **Adopt when:** Workloads > 25% idle; peak-to-avg ratio > 10; latencyReadiness acceptable; provider passes audit (SOC 2 Type II, PCI-DSS Level 1).
> - **Anti-signals (don't adopt yet):** < 3 years provider audit inspection; latency < 10 ms; payload > 5 MB.
> - **Common failure modes:** "Function sprawl" (hundreds of unmanaged functions); unmonitored cold-start penalties; cost overruns due to un-throttled burst traffic.
>
> ## 10. Common confusions — the "don't mix" list
> | Often confused | Real distinction |
> |----------------|------------------|
> | Serverless vs Microservices | Serverless is an *execution* model; microservices is an *organizational* pattern. |
> | FaaS vs Containers | Containers still require node provisioning; FaaS abstracts everything. |
> | Serverless vs Edge (C10-10) | Edge runs *near* the user (lora, roadside); serverless runs *in* the cloud (AWS/Azure/GCP).
>
> ## 11. Tools & standards to know
> - **Standards/Frameworks:** AWS Well-Architected Framework (Security Pillar); Azure Shared Responsibility Model; PCI-DSS v4.0 on virtualized environments; DORA ICT resilience.
> - **Common tooling:** AWS Lambda, Azure Functions, Google Cloud Functions, Knative, OpenFaaS, Terraform/CDK for IaC, Datadog RUM + APM for cold-start tracing, SpeedScale for profiling.
> - **Mandatory reading:** "Serverless Design Patterns" by MarioCortellucci; "Designing Distributed Systems" by Martin Kleppmann.
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
> 1. **Recall:** Define cold start and idempotency in 2 min without notes.
> 2. **Model:** Draw a sequence diagram for a serverless KYC pipeline (upload → Lambda → API → response).
> 3. **ADR:** Write an ADR for a provisioned-concurrency tier on an AWS Lambda.
> 4. **Defend:** Explain to a non-technical CRO why "serverless cuts infra cost" but not "serverless means no servers."
>
> ## 14. Summary (1 paragraph)
> Serverless computing is the operational abstraction layer that collapses operational staffing and over-provisioning into a pay-per-use model. In banking, it shines on bursty, low-criticality workloads like document processing and sandbox enumeration, but critical paths demand either provisioned-concurrency premiums or a hybrid with a managed container fleet.
>
> ---
> **Status:** ✅ Created · **Last updated:** 2026-09-14
