# 📋 TASKS — Enterprise Architecture Mastery
> **Purpose:** Single source of truth for *what to cover* and *what is done*.

> Each topic must produce **two files**: a `briefs/` brief + a `details/` detail, then status → `✅`.

> **Legend:** `☐` Not started · `◐` In progress · `✅` Covered · `💳` banking-relevant · `●` foundational · `◑` core · `○` advanced

> **Rule:** Do not mark `✅` until BOTH brief + detail exist AND each has ≥1 Mermaid diagram.

## Progress dashboard
| Category | Covered | Total | % |
|----------|---------|-------|----|
| C1 Foundations | 0 | 8 | 0% |
| C2 Frameworks | 0 | 8 | 0% |
| C3 Domains | 0 | 10 | 0% |
| C4 System Design | 0 | 12 | 0% |
| C5 Patterns | 0 | 10 | 0% |
| C6 Philosophy | 0 | 10 | 0% |
| C7 Org Architecture | 0 | 8 | 0% |
| C8 Reference/Standards | 0 | 8 | 0% |
| C9 Governance | 0 | 10 | 0% |
| C10 Emerging | 0 | 12 | 0% |
| **TOTAL** | **0** | **96** | **0%** |

> ⚠️ Keep the dashboard in sync as you flip statuses. Re-count each row after each batch.

---

## C1 — Foundations & Core Concepts 💳
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C1-01 | What is Enterprise Architecture? (Role, value, vs solutions/SA) | ● | ☐ | `C1-01-what-is-ea.md` | `C1-01-what-is-ea.md` |
| C1-02 | Architecture vs Engineering vs Design (definitions & boundary) | ● | ☐ | `C1-02-arch-vs-engineering.md` | `C1-02-arch-vs-engineering.md` |
| C1-03 | Systems & System-of-Systems Thinking | ● | ☐ | `C1-03-systems-thinking.md` | `C1-03-systems-thinking.md` |
| C1-04 | Abstraction, Views & Representations | ● | ☐ | `C1-04-abstraction-views.md` | `C1-04-abstraction-views.md` |
| C1-05 | Architecture Artifacts & Documentation | ● | ☐ | `C1-05-artifacts.md` | `C1-05-artifacts.md` |
| C1-06 | Stakeholders & Communication (business-IT bridge) 💳 | ● | ☐ | `C1-06-stakeholders.md` | `C1-06-stakeholders.md` |
| C1-07 | The Architecture Lifecycle (Plan→Build→Operate) | ● | ☐ | `C1-07-lifecycle.md` | `C1-07-lifecycle.md` |
| C1-08 | Core EA Vocabulary & Glossary | ● | ☐ | `C1-08-glossary.md` | `C1-08-glossary.md` |

## C2 — Frameworks & Methods
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C2-01 | TOGAF (ADM, phases, artifacts, A-B-C-D) — deep | ○ | ☐ | `C2-01-togaf.md` | `C2-01-togaf.md` |
| C2-02 | Zachman Framework (6×6, cell notation) | ○ | ☐ | `C2-02-zachman.md` | `C2-02-zachman.md` |
| C2-03 | DoDAF / MODAF / GAO / NAF (defense govt) | ○ | ☐ | `C2-03-dodaf-govt.md` | `C2-03-dodaf-govt.md` |
| C2-04 | BIZBOK (Business Architecture Body of Knowledge) | ◑ | ☐ | `C2-04-bizbok.md` | `C2-04-bizbok.md` |
| C2-05 | ArchiMate (layers, relationships, motivation) — deep | ○ | ☐ | `C2-05-archimate.md` | `C2-05-archimate.md` |
| C2-06 | IDEF (IDF0, IDEF3, IDEF0 data models) | ◑ | ☐ | `C2-06-idef.md` | `C2-06-idef.md` |
| C2-07 | UML for Enterprise (use cases, class, sequence, deployment) | ● | ☐ | `C2-07-uml.md` | `C2-07-uml.md` |
| C2-08 | Selecting & Combining Frameworks (pragmatic guidance) | ◑ | ☐ | `C2-08-framework-selection.md` | `C2-08-framework-selection.md` |

## C3 — Architecture Domains 💳
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C3-01 | Business Architecture (capability, value, process) 💳 | ● | ☐ | `C3-01-business-arch.md` | `C3-01-business-arch.md` |
| C3-02 | Data Architecture (domain, models, flow, lineage) 💳 | ◑ | ☐ | `C3-02-data-arch.md` | `C3-02-data-arch.md` |
| C3-03 | Application Architecture (layers, SOA, integration) 💳 | ◑ | ☐ | `C3-03-application-arch.md` | `C3-03-application-arch.md` |
| C3-04 | Technology/Infrastructure Architecture (cloud, platform) 💳 | ◑ | ☐ | `C3-04-technology-arch.md` | `C3-04-technology-arch.md` |
| C3-05 | Security Architecture (zero-trust, IABC, PCI-DSS) 💳 | ○ | ☐ | `C3-05-security-arch.md` | `C3-05-security-arch.md` |
| C3-06 | Integration & Messaging Architecture (API, ESB, event) 💳 | ○ | ☐ | `C3-06-integration-arch.md` | `C3-06-integration-arch.md` |
| C3-07 | Information/Data Governance (quality, master data) 💳 | ● | ☐ | `C3-07-data-governance.md` | `C3-07-data-governance.md` |
| C3-08 | Cloud & Platform Architecture (IaaS/PaaS/SaaS, multi-cloud) | ○ | ☐ | `C3-08-cloud-platform.md` | `C3-08-cloud-platform.md` |
| C3-09 | Network & Edge Architecture | ○ | ☐ | `C3-09-network-edge.md` | `C3-09-network-edge.md` |
| C3-10 | Reference vs Target vs Current (As-Is/To-Be) | ● | ☐ | `C3-10-asis-tobe.md` | `C3-10-asis-tobe.md` |

## C4 — System & Software Design
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C4-01 | Architectural Styles (monolith, SOA, micro, event, CQRS) | ◑ | ☐ | `C4-01-architectural-styles.md` | `C4-01-architectural-styles.md` |
| C4-02 | Layering & Modularity (boundaries, cohesion) | ● | ☐ | `C4-02-layering-modularity.md` | `C4-02-layering-modularity.md` |
| C4-03 | Distributed Systems Fundamentals (CAP, partitions) | ◑ | ☐ | `C4-03-distributed-fundamentals.md` | `C4-03-distributed-fundamentals.md` |
| C4-04 | Scalability (horizontal, vertical, load balancing) | ◑ | ☐ | `C4-04-scalability.md` | `C4-04-scalability.md` |
| C4-05 | Resilience & Fault Tolerance (SLOs, fallback, retry) | ○ | ☐ | `C4-05-resilience.md` | `C4-05-resilience.md` |
| C4-06 | Caching, Queues, Asynchrony, Backpressure | ○ | ☐ | `C4-06-caching-async.md` | `C4-06-caching-async.md` |
| C4-07 | Data Architectures (RDBMS, NoSQL, NewSQL, polyglot) 💳 | ◑ | ☐ | `C4-07-datastores.md` | `C4-07-datastores.md` |
| C4-08 | APIs & Interfaces (REST, gRPC, GraphQL, contract) | ◑ | ☐ | `C4-08-apis.md` | `C4-08-apis.md` |
| C4-09 | Concurrency, Idempotency, Consistency | ○ | ☐ | `C4-09-concurrency-consistency.md` | `C4-09-concurrency-consistency.md` |
| C4-10 | High-Availability & Disaster Recovery (RTO/RPO) 💳 | ○ | ☐ | `C4-10-ha-dr.md` | `C4-10-ha-dr.md` |
| C4-11 | Testing & Verification (unit, integration, chaos) | ● | ☐ | `C4-11-testing.md` | `C4-11-testing.md` |
| C4-12 | Observability (logs, metrics, traces, SLOs) | ◑ | ☐ | `C4-12-observability.md` | `C4-12-observability.md` |

## C5 — Patterns & Archetypes
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C5-01 | GoF Design Patterns (all 23, categorized) | ◑ | ☐ | `C5-01-gof-patterns.md` | `C5-01-gof-patterns.md` |
| C5-02 | Architectural Patterns (MVC, MVP, MVVM, Pipes-Filter) | ◑ | ☐ | `C5-02-arch-patterns.md` | `C5-02-arch-patterns.md` |
| C5-03 | Microservice Patterns (saga, CQRS, anti-corruption) | ○ | ☐ | `C5-03-microservice-patterns.md` | `C5-03-microservice-patterns.md` |
| C5-04 | Cloud / 12-Factor / SRE Patterns | ○ | ☐ | `C5-04-cloud-sre-patterns.md` | `C5-04-cloud-sre-patterns.md` |
| C5-05 | Enterprise Integration Patterns (Hofmann/Fowler) | ○ | ☐ | `C5-05-eip-patterns.md` | `C5-05-eip-patterns.md` |
| C5-06 | Domain Patterns (DDD, Bounded Context, Aggregate) 💳 | ○ | ☐ | `C5-06-ddd-patterns.md` | `C5-06-ddd-patterns.md` |
| C5-07 | Data Patterns (CQRS, Event Sourcing, CDC) | ○ | ☐ | `C5-07-data-patterns.md` | `C5-07-data-patterns.md` |
| C5-08 | Security Patterns (AuthN/Z, token, zero-trust) 💳 | ○ | ☐ | `C5-08-security-patterns.md` | `C5-08-security-patterns.md` |
| C5-09 | Resilience Patterns (circuit breaker, bulkhead, retry) | ○ | ☐ | `C5-09-resilience-patterns.md` | `C5-09-resilience-patterns.md` |
| C5-10 | Pattern Catalog & Selection Heuristics | ◑ | ☐ | `C5-10-pattern-catalog.md` | `C5-10-pattern-catalog.md` |

## C6 — Design Philosophy & Quality Attributes
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C6-01 | SOLID, DRY, KISS, YAGNI (OOP principles) | ● | ☐ | `C6-01-solid-dry-kiss.md` | `C6-01-solid-dry-kiss.md` |
| C6-02 | Separation of Concerns, Abstraction, Encapsulation | ● | ☐ | `C6-02-soc-abstraction.md` | `C6-02-soc-abstraction.md` |
| C6-03 | Coupling vs Cohesion (design discipline) | ● | ☐ | `C6-03-coupling-cohesion.md` | `C6-03-coupling-cohesion.md` |
| C6-04 | Quality Attributes & QAW (NFRs, ATAM) | ◑ | ☐ | `C6-04-quality-attributes.md` | `C6-04-quality-attributes.md` |
| C6-05 | Trade-off & Pareto Analysis in Architecture | ◑ | ☐ | `C6-05-tradeoffs.md` | `C6-05-tradeoffs.md` |
| C6-06 | Fitness Functions & Quantifying Quality | ○ | ☐ | `C6-06-fitness-functions.md` | `C6-06-fitness-functions.md` |
| C6-07 | Maintainability, Extensibility, Portability | ● | ☐ | `C6-07-maintainability.md` | `C6-07-maintainability.md` |
| C6-08 | Technical Debt & Rationale Documentation (ADRs) | ◑ | ☐ | `C6-08-tech-debt-adrs.md` | `C6-08-tech-debt-adrs.md` |
| C6-09 | ADRs & Decision Records (MADR, ADR format) | ◑ | ☐ | `C6-09-adrs.md` | `C6-09-adrs.md` |
| C6-10 | Architecture Evaluation (ATAM, C4, reviews) | ○ | ☐ | `C6-10-evaluation.md` | `C6-10-evaluation.md` |

## C7 — Enterprise & Organizational Architecture
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C7-01 | Conway's Law & Org-System Alignment | ● | ☐ | `C7-01-conways-law.md` | `C7-01-conways-law.md` |
| C7-02 | Capability Mapping (value stream, business caps) 💳 | ◑ | ☐ | `C7-02-capability-mapping.md` | `C7-02-capability-mapping.md` |
| C7-03 | Value Chain / Value Stream Mapping 💳 | ◑ | ☐ | `C7-03-value-stream.md` | `C7-03-value-stream.md` |
| C7-04 | Architecture Portfolio & Roadmap | ● | ☐ | `C7-04-portfolio-roadmap.md` | `C7-04-portfolio-roadmap.md` |
| C7-05 | Application Rationalization (retire/refactor/rehost) 💳 | ◑ | ☐ | `C7-05-app-rationalization.md` | `C7-05-app-rationalization.md` |
| C7-06 | Technology Landscape & Standards (TOGAF-STD) | ● | ☐ | `C7-06-technology-landscape.md` | `C7-06-technology-landscape.md` |
| C7-07 | Architecture Maturity Model (0→5) 💳 | ◑ | ☐ | `C7-07-maturity-model.md` | `C7-07-maturity-model.md` |
| C7-08 | Center of Excellence (CoE) & Architecture Team | ◑ | ☐ | `C7-08-coe.md` | `C7-08-coe.md` |

## C8 — Reference Architecture, Standards & Principles
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C8-01 | Reference Architectures (banking, cloud, reference) 💳 | ◑ | ☐ | `C8-01-reference-arch.md` | `C8-01-reference-arch.md` |
| C8-02 | Standards (IEEE, ISO 42010, UML, ArchiMate) | ● | ☐ | `C8-02-standards.md` | `C8-02-standards.md` |
| C8-03 | Architecture Principles (first principles, banking) | ● | ☐ | `C8-03-principles.md` | `C8-03-principles.md` |
| C8-04 | Compliance & Reg Architecture (Basel, SOX, PCI) 💳 | ○ | ☐ | `C8-04-compliance-reg.md` | `C8-04-compliance-reg.md` |
| C8-05 | Risk & Resilience Architecture (operational risk) 💳 | ○ | ☐ | `C8-05-risk-resilience.md` | `C8-05-risk-resilience.md` |
| C8-06 | Data Sovereignty & Residency (banking) 💳 | ○ | ☐ | `C8-06-data-sovereignty.md` | `C8-06-data-sovereignty.md` |
| C8-07 | Accessibility, Usability, Human Factors (UI/UX) | ● | ☐ | `C8-07-accessibility.md` | `C8-07-accessibility.md` |
| C8-08 | Vendor & Ecosystem Strategy (open vs proprietary) 💳 | ◑ | ☐ | `C8-08-vendor-strategy.md` | `C8-08-vendor-strategy.md` |

## C9 — Governance, Management & Strategy
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C9-01 | EA Practice & Governance (policies, AD) | ◑ | ☐ | `C9-01-ea-practice-governance.md` | `C9-01-ea-practice-governance.md` |
| C9-02 | Architecture Board & Decision Rights | ◑ | ☐ | `C9-02-architecture-board.md` | `C9-02-architecture-board.md` |
| C9-03 | Compliance & Audit Readiness (SOX/PCI) 💳 | ○ | ☐ | `C9-03-compliance-audit.md` | `C9-03-compliance-audit.md` |
| C9-04 | Architecture as a Service (self-service) | ○ | ☐ | `C9-04-arch-as-service.md` | `C9-04-arch-as-service.md` |
| C9-05 | Cost & TCO (build vs buy, cloud cost) 💳 | ◑ | ☐ | `C9-05-tco-cost.md` | `C9-05-tco-cost.md` |
| C9-06 | Delivery Models (Agile, DevOps, SAFe, value streams) 💳 | ◑ | ☐ | `C9-06-delivery-models.md` | `C9-06-delivery-models.md` |
| C9-07 | Change Management & Adoption (CMMI, TOGAF-STD) | ◑ | ☐ | `C9-07-change-adoption.md` | `C9-07-change-adoption.md` |
| C9-08 | Architecture Metrics & KPIs (maturity, risk) 💳 | ◑ | ☐ | `C9-08-metrics-kpis.md` | `C9-08-metrics-kpis.md` |
| C9-09 | Enterprise Knowledge & CMDB (asset inventory) | ◑ | ☐ | `C9-09-knowledge-cmdb.md` | `C9-09-knowledge-cmdb.md` |
| C9-10 | Digital Transformation & Strategy (banking) 💳 | ○ | ☐ | `C9-10-digital-transform.md` | `C9-10-digital-transform.md` |

## C10 — Emerging & Advanced Topics
| ID | Topic | Diff | Status | Brief | Detail |
|----|-------|------|--------|-------|--------|
| C10-01 | DDD, Strategic & Tactical Design | ○ | ☐ | `C10-01-ddd-strategic.md` | `C10-01-ddd-strategic.md` |
| C10-02 | Event-Driven & Event-Streaming Architecture (Kafka) | ○ | ☐ | `C10-02-event-driven.md` | `C10-02-event-driven.md` |
| C10-03 | Serverless & FaaS (AWS Lambda, Azure Fn) | ○ | ☐ | `C10-03-serverless.md` | `C10-03-serverless.md` |
| C10-04 | Kubernetes & Container Orchestration | ○ | ☐ | `C10-04-k8s.md` | `C10-04-k8s.md` |
| C10-05 | API Economy, Gateway & BFF patterns | ○ | ☐ | `C10-05-api-economy.md` | `C10-05-api-economy.md` |
| C10-06 | Zero-Trust & BeyondCorp Security | ○ | ☐ | `C10-06-zero-trust.md` | `C10-06-zero-trust.md` |
| C10-07 | Data Mesh & Data Fabric Architecture | ○ | ☐ | `C10-07-data-mesh.md` | `C10-07-data-mesh.md` |
| C10-08 | AI/ML Architecture & MLOps (banking use) 💳 | ○ | ☐ | `C10-08-ai-ml-arch.md` | `C10-08-ai-ml-arch.md` |
| C10-09 | Blockchain / Distributed Ledger (banking) 💳 | ○ | ☐ | `C10-09-blockchain.md` | `C10-09-blockchain.md` |
| C10-10 | 5G, IoT & Edge Computing (banking) | ○ | ☐ | `C10-10-5giot-edge.md` | `C10-10-5giot-edge.md` |
| C10-11 | Quantum Readiness & Post-Quantum Crypto 💳 | ○ | ☐ | `C10-11-quantum.md` | `C10-11-quantum.md` |
| C10-12 | Sustainable / Green IT (carbon, efficient design) | ○ | ☐ | `C10-12-green-it.md` | `C10-12-green-it.md` |

---

## 🎓 Certification & Mastery Checklist (optional add-on)
| Item | Why |
|------|-----|
| TOGAF 9 certification path | Industry default EA framework |
| Zachman / BIZBOK foundation | Completes framework literacy |
| ArchiMate modeling fluency | Industry standard modeling notation |
| AWS/Azure/AWS Solution Architect (Assoc.) | Proves platform fluency |
| Cloud-native / SRE pattern fluency | Production-grade patterns |
| DDD + strategic design | Domain-driven, business-aware EA |
| MLOps / GenAI architecture (C10) | Cutting-edge relevance |

> **Note:** Mastery = you can *explain the why, choose the right one for the right case, and defend it to a business board* — not just recite definitions.
