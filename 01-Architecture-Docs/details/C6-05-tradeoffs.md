# [C6-05] Trade-offs — DETAIL

> **Category:** C6 — Design Philosophy & Quality Attributes · **Difficulty:** ◑ · **Banking-relevant:** yes
> **Companion brief:** `[briefs/C6-05-tradeoffs.md](../briefs/C6-05-tradeoffs.md)`
> **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.

---

## 1. Precise definition

A **trade-off** is the conscious, constrained optimisation of at least two *competing* quality attributes or constraints. The term originates in *economics* (the production-possibility frontier) and was adopted by *software architecture* by Parnas & Clements: "You can have *wholesome objectives* or *good* objectives; you cannot have both."

In architecture, a *trade-off* is **not** a *compromise* (which implies *partial satisfaction* of all) and is **not** a *decision* (which implies a *point on the frontier*). A *trade-off* is the *relationship* that defines the *frontier itself* — the *Pareto front*.

A **Pareto-optimal** architecture is one where *no* trade-off can improve one QA without *degrading* another. In practice, *Pareto-optimality* is a *useful approximation* because the true frontier is *multi-dimensional* and *non-linear*.

**Pareto frontier** (P):
P = { 𝑥 ∈ 𝑄 | ¬∃𝑦 ∈ 𝑄 : 𝑦 ≥ 𝑥, 𝑦 ≠ 𝑥 }
where 𝑄 is the set of feasible architectures.

A **compromise** (C) is:
C = { 𝑥 ∈ 𝑄 | ∀QAᵢ, fᵢ(x) ≥ fᵢ(y) for all *acceptable* y }
i.e., *adequate* on every dimension, but not necessarily *optimal* on any.

**Trade-off awareness**: the *absence* of an explicit trade-off analysis is itself a *decision* — an *implicit* trade-off that is usually *poor*.

## 2. Why it exists (problem it solves)

The *2008 financial crisis* exposed many banks' *artificially cheap* trade-offs:
- *Mortgage* underwriting was optimised for *origination speed* (+ *performance*) at the expense of *credit-assessability* (- *maintainability*, - *testability*). The resulting *CRC* (Credit Rating Committee) models could not be *reproduced* because the *trade-off* between *automation* and *explainability* was never *documented*.
- *Operational risk* was ignored: *IT resilience* was traded for *trading-floor throughput*. When Lehman failed, many banks discovered that *back-office* systems had *no *disaster recovery* trade-off* (it was *not budgeted*), not that no one had *chosen* it.

Modern banking faces:
- *DORA (Digital Operations Resilience)*: *availability* vs *operational complexity* vs *cost*.
- *PSD2*: *open-banking* vs *counter-party credit risk* vs *fraud*.
- *Climate-risk* frameworks: *low-latency* trading vs *carbon-budget* real-time accounting.

Every *regulator* will ask: *"What did you trade for?"* The *answer* must be *explicit*.

## 3. Core concepts & vocabulary

| Term | Precise meaning |
|------|-----------------|
| **Pareto frontier** | The set of architectures where no QA can be improved without reducing another. |
| **Satisficing** | Simon (1957): an outcome is *acceptable* rather than *optimal*; in architecture, this means *meeting a threshold* on every QA rather than maximising one. |
| **Opportunity cost** | The *value of the forgone alternative* — often omitted by *optimism bias*. |
| **First-order effect** | Immediate, observable consequence (e.g. *latency*). |
| **Second-order effect** | Delayed, systemic consequence (e.g. *maintainability* eroding over *N* sprints). |
| **Dominated alternative** | An option that is *worse* than another on *all* QAs; should be *discarded*, not "traded". |
| **Arch-trade matrix** | A *matrix* of <attribute₁, attribute₂> with *scores* and *description*, used to make trade-offs *explicit*. |
| **Cost of Delay** | The *economic loss* per unit of time from *not shipping*; used to *weight* trade-offs when *market timing* dominates. |
| **Technical risk** | Trade-off uncertainty: *we do not know* the *second-order* effect. |
| **Primary/secondary## 4. How it works (architecture / mechanism)

### 4.1 Diagrams

**Diagram A — Trade-off decision loop (highlight critical = amber, decision = green, context = grey):**

```mermaid
graph LR
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:2px
    classDef context fill:#dfe6e9,stroke:#636e72
    classDef risk fill:#fecaca,stroke:#991b1b,stroke-width:2px
    classDef ok fill:#a7f3d0,stroke:#065f46,stroke-width:2px

    --------- RECOGNISE ----------
    E[Emergent requirement]:::context --> R[Revisit QA set]:::decision
    R --> T[Truth table: every choice has gain/loss]:::critical
    --------- EVALUATE ----------
    T --> FR[Choose Pareto-optimal option]:::decision
    --------- ACT & MONITOR ----------
    FR --> A[Implement]:::ok
    A --> M[Monitor for second-order drift]:::context
    M -.-> E
    M -.-> risk
```

**Diagram B — Pareto surface visualised (contour, with critical = amber, ok = light-green, context = grey):**

```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:2px
    classDef ok fill:#a7f3d0,stroke:#065f46,stroke-width:2px
    classDef context fill:#dfe6e9,stroke:#636e72

    P1[Performance]:::ok
    P2[Security]:::ok
    P3[Cost]:::ok
    
    FRONTIER[Pareto Frontier Surface]:::critical
    FRONTIER --> P1
    FRONTIER --> P2
    FRONTIER --> P3
    
    DOM[Dominated Zone (reject)]:::risk
    DOM -.x P1
    DOM -.x P2
    DOM -.x P3
    
    POINT[Final Decision Point]:::decision
    POINT --> FRONTIER
```

### 4.2 Mechanism — the *Arch-Trade Matrix*

For every *epic* or *system boundary*, define a matrix:

| Attribute | Option A | Option B | Option C | Notes |
|-----------|----------|----------|----------|-------|
| **Latency** | ⭐⭐⭐ (50 ms) | ⭐⭐ (120 ms) | ⭐⭐⭐⭐ (15 ms) | Option C uses caching; Option B off-loads sorting |
| **Security** | ⭐⭐⭐ (shared secret) | ⭐⭐⭐⭐⭐ (mTLS) | ⭐⭐ (bypass TLS for hot path) | Option B fails at 10× load; Option C externally audited |
| **Cost** | $X | $Y | $Z | Option Y has *pay-as-you-go* elasticity |
| **Maintainability** | $*A | $*A+$B | $*2A | Option C has *ad-hoc scripts* |

*Take the weighted average (e.g. 2× Security at 100, Latency at 50, Cost at 30, Maintenance at 20).*

### 4.3 Mechanism — first-order vs second-order analysis

1. **First-order:** run *performance tests*, *security scans*, and *unit tests*. Record *gains/losses*.
2. **Second-order:** hold a *retro* after *3 sprints* with *operations* and *support*. Ask: "What's *harder* to change now than it was on day one?"
3. **Document:** add a *second-order footnote* to every *ADR*: *"Trading A for B paid off until [date]; now we observe erosion in Z."*

## 5. Variants, options & trade-offs

| Variant | When to pick | When to avoid | Trade-off |
|---------|--------------|---------------|-----------|
| **Multi-objective optimisation (e.g. weighted sum)** | Vendor RFP with defined SLA | Year-1 green-field | Risk: weights drift with *HIPPO* bias |
| **Satisficing (satisfice A, B, C thresholds)** | Regulated product; "must work" | Disruptive-product; need *speed* | Slower; avoids *optimality* |
| **Pareto-front search (NSGA-II, genetic algo)** | Large-scale system with 6+ QAs | Small team | Computationally heavy; requires *abstraction* |
| **First-order-only trade-off** | High-velocity innovation | Regulated bank; DORA compliance | Hidden *second-order* debt |
| **Second-order-only trade-off** | Legacy modernisation | Start-up | Paralysis; can't ship fast enough |
| **Cost-of-delay prioritisation** | Time-sensitive moat (e.g. 6-month first-mover) | Mandated infrastructure | May sacrifice *regulatory *safety* |
| **Risk-adjusted trade-off** | M&A due-diligence | Pure green-field | Over-weights *probability* of *unknowns* |

### 5.1 The "trade-off fallacy"

A common fallacy: *"We can optimize for both security and performance using AI-optimised encryption."* This is only true if there is a *new* *frontier* (e.g. homomorphic encryption). The *trade-off* still exists; it is *P* vs *Q* with *additional R*.

### 5.2 The "trade-off trap"

In *financial services*, *stability* is *valued* higher than *agility*. A *trade-off* on *security* for *speed* is *risky*. But a *trade-off* on *agility* for *security* is *slow*. The *trap* is *not* making the trade-off *visible*, letting *team politics* choose.

## 6. Relationships to sibling topics

- **C4 (Patterns):** Every pattern *encodes* a trade-off (e.g. *cache-aside* trades *consistency* for *latency*).
- **C6-04 (Quality Attributes):** Trade-offs *exist between* QAs; QAs *define* the *axes* of trade.
- **C6-07 (Maintainability):** Maintainability is often the *second-order* casualty of *performance-first* trade-offs.
- **C6-08 (Tech Debt):** *Unmanaged* trade-offs become *tech debt*; the *interest rate* is the *cost of second-order effects*.
- **C6-09 (ADR):** An ADR *records* the trade-off; a *missing* ADR *hides* the trade-off.

## 7. Banking / financial-services context 💳

A **UK-based payments-as-a-service (PaaS)** company (Revolut-type) faced a *platform-API* trade-off:
- *Option A:* Direct *SWIFT gpi* integration: low *latency* (1-2 mins), high *counter-party risk* (no *real-time* tracking), high *cost* (SWIFT membership fees, per-message fees).
- *Option B:* *RTGS* real-time *instant* with *tokenised* *RTGS-Lite*: low *latency* (< 5 secs), lower *counter-party risk* (tokenised), *higher operational complexity* (integration with *BOE* and *CBI*).
- *Option C:* *Clearing-proxy* through *a single correspondent bank*: lowest *cost*, highest *counter-party concentration risk*, opaque *settlement*.

The *trade-off matrix* placed *Option B* on the *Pareto frontier* for *latency + security*; *Option C* was *dominated* on *security* but *dominates* on *cost*.

The *decision* was *B*, with the *cost* accepted by the CFO and the *complexity* accepted by the *platform team* under a *2-year maintenance commitment*.

A *second-order* effect: *Option B* required a *token-vault*; the *token-service* became a *single point of failure* (communcal coupling), requiring a *backup* *crypto* vault. This was a *new trade-off* (cost vs resilience) that emerged 14 months after go-live, documented in *ADR-2027-008*.

## 8. Reference architecture / worked example

### Problem
A *US community bank* wants to launch *instant-settlement* for *ACH*.

### Decision
1. Choose between:
   - *Monolithic*, *queue-based*, *batch* (low *cost*, data *loss* risk, high *operational burden* on weekends)
   - *Micro-services* with *transactions* (high *cost*, tightly-coupled *consistency*, *Saga* *orchestration* *retry* logic)
   - *Hybrid*: *micro-services* only for *integration* (FX, fraud); *batch* for *settlement* (integrity)
2. Quantify *trade-offs*:

| QA | Batch | Transactional Micro | Hybrid |
|----|-------|---------------------|--------|
| Latency | 1 ask / 2 days | 1 ask / < 4 hrs | 1 ask / < 4 hrs (integration only) |
| Counter-party risk | Low | Medium-High | Medium |
| Cost | Low | High | Medium |
| Compliance (SOX) | Simple | Complex (idempotency) | Complex but *bounded* |

3. Choose *Hybrid*.

### Diagram
```mermaid
graph LR
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:2px
    classDef context fill:#dfe6e9,stroke:#636e72
    classDef data fill:#fde68a,stroke:#92400e,stroke-width:2px
    classDef service fill:#bfdbfe,stroke:#1e40af,stroke-width:2px

    ACH[ACH Adapter]:::service
    ACH -.-> TRG[(Transactional Store)]:::data
    ACH -.-> BRD[(Batch Settlement)]:::data
    TRG -.-> FX[FX Rate Engine]:::service
    TRG -.-> FRA[Fraud Check]:::service
    BRD --> SET[(Settlement]]:::data
```

### ADR
```markdown
# ADR-2026-023: Hybrid settlement for Instant ACH
## Status
Accepted
## Context
Instant ACH needed < 4-hour settlement; batch-only was too slow; full real-time was too costly / risky.
## Decision
Use micro-services only for the *transform and route* layer (FX + fraud); use a *light batch* for *end-to-end settlement*.
## Consequences
- Positive: meets instant-ACH timebox; batch simplifies SOX.
- Negative: two-phase-committion for fraud-escrow; latency spike on 3× peak (Black-Friday).
## Alternatives considered
1. Full real-time micro-services — rejected (cost, operational burden).
2. Pure batch — rejected (regulatory / competition).
```

## 9. Maturity & adoption signals

- **Adopt when:** (1) every *epic* has a *trade-off matrix*; (2) *ADRs* name the *algorithm* (weights, thresholds) that selected the final *configuration*; (3) *post-mortem* refers to the *trade-off* decision.
- **Anti-signals:** (1) any *ADR* has *"hard to say"* as the *consequence*; (2) *performance* is *optimised* but *observability* is *ignored*; (3) *cost* is *never* discussed.
- **Common failure modes:**
  1. *Implicit* trade-off: no decision was *said* until *crisis*.
  2. *Dominated* alternative: something chosen that is *worse* than *any* other option.
  3. *Second-order erosion*: a **trade-off** that was *valid* at *t=0* but *invalid* at *t=12 months* because *business* or *operational* context changed (e.g. *cloud-pricing* or *staffing*).

## 10. Common confusions — the "don't mix" list

| Often confused | Real distinction |
|----------------|------------------|
| Trade-off vs compromise | A trade-off is a *frontier*; a compromise is *adequate* on something else. |
| Trade-off vs decision | A decision is a *point*; a trade-off is the *relationship* that defines it. |
| Pareto-optimal vs most-and-best | Pareto-optimal is *no single better* — not: *the best on everything*. |
| First-order vs second-order | First-order is *immediate*; second-order is *delayed* — both are *trade-offs*. |

## 11. Tools & standards to know

- **Standards/Frameworks:** Simon (1957) *Administrative Behavior* (satisficing), Pareto (1896) *Manuel*; *Council* on *Costs* of *Delay*; *DORA* for financial-services *resilience* trade-off measurement.
- **Common tooling:** *Confluence* (Arch-Trade matrix), *Jira* (epic with QA tags), *Datadog* (SLO dashboards), *R Shiny* / *Python* (trade-off frontier simulation), *Archi* EA for *architecture* *decision* *records*.
- **Mandatory reading:** *The Art of Decision Making* (Heath, Larrick, 2009); *Systems Thinking and Complex Systems* (Meadows, Homer); *DORA* guidelines on *resilience*.

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
- Neutral ...
## Alternatives considered
1. ...
2. ...
3. ...
```

## 13. Practice — apply it

1. **Recall:** name the *three* *types* of *trade-off* (necessity, preference, intuition).
2. **Model:** produce an *Arch-Trade matrix* for a *mortgage-origination* service comparing *speed* vs *credit-risk* vs *cost*.
3. **ADR:** write an ADR for *keeping* the *fraud-check* inside the *onboarding* service vs extracting it — explicitly list the *Pareto frontier*.
4. **Defend:** explain to a *CFO* why *trade-off documentation* is *not* overhead but *risk reduction*.

## 14. Summary (1 paragraph)

Trade-offs are the *heartbeat* of architecture: every design is a *move* on the *Pareto frontier*, and the EA's *sole duty* is to *make the move* *visible*, *name the alternatives*, and *avoid the dominated* — because a *hidden* trade-off is *a debt* that *defaults* when the *second-order* *interest rate* is *collected*.

---
**Status:** ✅ Covered · **Last updated:** 2026-09-14
