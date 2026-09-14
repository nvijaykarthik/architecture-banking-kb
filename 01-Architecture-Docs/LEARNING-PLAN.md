# 🗓️ Learning Plan — 2 Weeks, 2 hrs/day
> **Goal:** Cover all **96 topics** in `[TASKS.md](./TASKS.md)` in **14 days** (≈2 hrs/day).

> **Cadence:** Each day = one **thematic cluster** of tasks. Brief first, then detail for priority topics.

> **Daily rhythm (2h):** `30 min` brief skim → `45 min` detail deep-dive + diagram recall → `25 min` practice (draw the ArchiMate/UML or write an ADR) → `20 min` self-test.

---

## How the 2 hours are split (consistent every day)
| Block | Time | Activity |
|-------|------|----------|
| A | 0:00–0:30 | Read **briefs** for the day's cluster (fast, high-recall) |
| B | 0:30–1:15 | Read **detail** docs; sketch the key Mermaid by hand |
| C | 1:15–1:40 | **Apply**: write an ADR / model in ArchiMate / map capabilities for a banking scenario |
| D | 1:40–2:00 | **Self-test**: explain each topic aloud in 2 min (Feynman) + mark `✅` in TASKS.md |

> Tip: Do the **brief** for ALL of a day's topics in block A. Do **details** only for the ◑/○ (core/advanced) ones that day; foundational ● ones the brief may be enough, but you still mark them `✅`.

---

## Phase 1 — Foundations (Days 1–2)
| Day | Focus | Tasks (IDs) |
|-----|-------|-------------|
| **1** | What is EA, system-of-systems, views, artifacts, lifecycle, stakeholders, glossary | C1-01 … C1-08 |
| **2** | Frameworks: TOGAF, Zachman, ArchiMate, UML, BIZBOK, IDEF, DoDAF, selection | C2-01 … C2-08 |

## Phase 2 — Domains (Days 3–4)
| Day | Focus | Tasks (IDs) |
|-----|-------|-------------|
| **3** | Business, Data, Application, Technology, Data-Governance, As-Is/To-Be | C3-01, C3-02, C3-03, C3-04, C3-07, C3-10 |
| **4** | Security, Integration, Cloud-Platform, Network-Edge, (finish C3) | C3-05, C3-06, C3-08, C3-09 |

## Phase 3 — Design (Days 5–6)
| Day | Focus | Tasks (IDs) |
|-----|-------|-------------|
| **5** | Styles, Layering, Distributed, Scalability, Resilience, Caching/Async | C4-01 … C4-06 |
| **6** | Datastores, APIs, Concurrency, HA/DR, Testing, Observability | C4-07 … C4-12 |

## Phase 4 — Patterns (Days 7–8)
| Day | Focus | Tasks (IDs) |
|-----|-------|-------------|
| **7** | GoF, Architectural, Microservice, DDD, Resilience patterns | C5-01, C5-02, C5-03, C5-06, C5-09 |
| **8** | Cloud/SRE, EIP, Data patterns, Security patterns, Catalog/selection | C5-04, C5-05, C5-07, C5-08, C5-10 |

## Phase 5 — Philosophy & Quality (Days 9–10)
| Day | Focus | Tasks (IDs) |
|-----|-------|-------------|
| **9** | SOLID/DRY/KISS, SoC, Coupling/Cohesion, Maintainability | C6-01 … C6-03, C6-07 |
| **10** | QAs & NFRs, Trade-offs, Fitness, Tech-Debt, ADRs, Evaluation (ATAM/C4) | C6-04, C6-05, C6-06, C6-08, C6-09, C6-10 |

## Phase 6 — Org Architecture (Day 11)
| Day | Focus | Tasks (IDs) |
|-----|-------|-------------|
| **11** | Conway, Capabilities, Value Stream, Portfolio, Rationalization, Landscape, Maturity, CoE | C7-01 … C7-08 |

## Phase 7 — Reference/Standards (Day 12)
| Day | Focus | Tasks (IDs) |
|-----|-------|-------------|
| **12** | Reference arch, Standards, Principles, Compliance/Risk/Sovereignty, Accessibility, Vendor | C8-01 … C8-08 |

## Phase 8 — Governance & Strategy (Days 13–14)
| Day | Focus | Tasks (IDs) |
|-----|-------|-------------|
| **13** | EA practice, Board, Compliance, Arch-as-Service, TCO, Delivery, Change, Metrics, CMDB, Transformation | C9-01 … C9-10 |
| **14** | Emerging: DDD, EventBus, Serverless, K8s, API, ZeroTrust, DataMesh, AI/ML, Blockchain, 5G/IoT, Quantum, Green | C10-01 … C10-12 |

---

## 🎯 End-of-Week checkpoints (verify progress)
- **Day 7 (midpoint):** C1–C5 done. You should be able to model a banking app in **ArchiMate** and explain **TOGAF ADM** end-to-end.
- **Day 14 (end):** All 96 ✅. You should be able to write a **target state reference architecture** for a banking core-banking modernization and defend each decision with an **ADR**.

## 🧭 Self-test rubric (apply the "no-basics-gap" bar)
For each topic, you are **done** only when you can:
1. Define it precisely (no vague "it's about architecture").
2. Contrast it with the 2–3 most confusingly-named neighbors (e.g., Saga vs CQRS vs Event Sourcing).
3. Give a **banking-specific** example.
4. State the main **trade-off** and when you'd *not* use it.

> If any topic fails 2+ of these, re-run the detail doc + sketch before marking ✅.
