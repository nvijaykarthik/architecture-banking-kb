# C6-04 Service Levels — DETAIL
> **Category:** Cx — Custody Operations · **Difficulty:** ● · **Banking-relevant:** yes / 💳
> **Companion brief:** `briefs/C6-04-service-levels.md`
>
> > **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.
>
> ---
>
> ## 1. Precise definition
> Service levels are quantifiable regulatory thresholds for the maximum elapsed business time between a trade-date trigger event (instruction generation or obligation generation) and **settlement finality**, as codified in NISA Annex A. They are expressed as T+n, where n is the number of post-trade business days. Unlike SLAs, service levels are non-negotiable; they bind all CSAs and QCAs to a uniform minimum, and any contract that relaxes them is void under provincial securities legislation.
>
> ## 2. Why it exists (the problem it solves)
> Before NISA standardization, every CSA negotiated bespoke settlement windows, producing fragmentation: one manager's RA transferred T+2 while another's required T+5, creating settlement-risk gaps and cash-flow opacity. The 1998-2001 CS average showed a ~40% reconciliation gap due to misaligned deadlines. NISA fixed this by inverting the model: the regulator sets the ceiling, and participants design infrastructure *down* to meet it, eliminating guess-work and legal disputes.
>
> ## 3. Core concepts & vocabulary
> | Term | Precise meaning |
> |------|-----------------|
> | T+n settlement | Trade date + n business days, subject to NISA calendar rules, excluding weekends and holidays. |
> | Finality | The irrevocable legal transfer of ownership recorded in the CDS/CSDB, distinct from identification or trade-date notification. |
> | Cash pollination | The simultaneous credit of cash to a settlement account that corresponds to a securities debit, required within the same service level. |
> | QP holder | The qualified purchaser (e.g., bank trust company) that holds securities in nominee name and is ultimately liable for any settlement failure. |
> | Triparty | Settlement arrangement in which a clearing bank or central securities depository coordinates securities and cash legs. |
> | DVP (Delivery versus Payment) | A delivery instruction paired with an irrevocable cash instruction so that securities transfer only upon cash credit. |
>
> ## 4. How it works (architecture / mechanism)
> Settlement architecture must guarantee that every instruction received by the custody engine reaches the CDS/CSDB, the QP holder ledger, and the client account ledger within the prescribed bucket. The path is:
> 1. **Ingest:** KFMS/OMM receives trade-date obligation or client instruction and validates format against NISA XML schema.
> 2. **Settle:** Parallel threads perform DVP alignment, cash pollination, and securities debit/credit.
> 3. **Finalize:** CDS/CSDB records the transfer, the QP holder ledger freezes the old position, and the client account opens the new one.
>
> ### 4.1 Diagrams
>
> **Diagram A — Core structure** (highlight load-bearing parts = amber, supporting = grey):
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     Ingest[KTES Ingest]:::context --> Validate[NISA Validation]:::core
>     Validate --> Settle[DVP Settlement]:::critical
>     Settle --> Finalize[CDS Finality]:::core
>     Finalize --> Client[Client Ledger]:::context
>     class Settle critical
> ```
>
> **Diagram B — Lifecycle / flow** (highlight decision points = green, failures = red, money = gold):
> ```mermaid
> graph LR
>     classDef ok fill:#a7f3d0,stroke:#065f46,color:#000
>     classDef risk fill:#fecaca,stroke:#991b1b,color:#000
>     classDef money fill:#fde68a,stroke:#92400e,stroke-width:1px,color:#000
>     Start[Trade]:::money --> B[CFD approval]:::risk
>     B -->|approved| C[Cash pollination]:::ok
>     B -->|rejected| D[Abort & notify]:::risk
>     C --> E[Securities debit]:::money
>     E --> F[Finality]:::ok
>     F --> G[Report]:::money
> ```
>
> ## 5. Variants, options & trade-offs
> | Variant | When to pick | When to avoid | Key trade-off axis |
> |---------|--------------|---------------|--------------------|
> | T+2 standard | Principal-protected funds and standard RA transfers | Ultra-short-term trading where T+0 cash is essential | Time vs operational complexity |
> | T+1 principal-protected | Inter-fund exchange within same dealer-manager group | Transfer to external QP holder | Governance vs speed |
> | Real-time gross settlement (RTGS) | Large institutional block trades | Retail-scale accounts | Cost vs immediacy |
>
> ## 6. Relationships to sibling topics
> - **C5-02-cash-management:** Cash pollination is the companion mechanism to securities transfer; service levels govern both legs simultaneously.
> - **C5-04-cash-management-settlement:** Real-time cash settlement is an optimization; it still maps back to the same NISA service-level deadline.
> - **C6-03-clearing-and-settlement:** Clearing is the pre-settlement phase that *enables* service-level achievement; you cannot meet T+2 if clearing fails at T+0.
>
> ## 7. Banking / financial-services context 💳
> Under MiFID II and Canadian CSA rules, a T+2 breach is reportable to the regulator within five business days. Suppose CIBAM's settlement engine suffers a thread-pool exhaustion on the afternoon of T+1 due to a data-center power dip. The QP holder (the bank's trust subsidiary) remains liable until finality is recorded, even if the custodian was not at fault. The practical consequence: the custodian may face an internal memorandum of default, a clawback of settlement fees, and a NCSA compliance letter. The architecture must therefore provision failover across sites with sub-second sync, not merely document the risk.
>
> ## 8. Reference architecture / worked example
> A RIAM mutual fund manager needs to move 2 million CADU-cap units from the CIBAM IRPS account to a client's RA disc.
> - **Decision:** T+2 cash-settlement bucket applies; principal-protected clause triggers T+1 if the transfer is intra-group.
> - **Architecture:** KFMS issues a DVP obligation to CSD-CA; CDS-CA runs parallel credit of units and debit of 2 million CAD.
> - **ADR:** To guarantee T+1 for inter-group, we provision a hot-standby settlement node in Montreal with automated failover from Toronto under <500ms RPO (Recovery Point Objective).
> ```mermaid
> graph LR
>     classDef service fill:#bfdbfe,stroke:#1e40af
>     classDef data fill:#fde68a,stroke:#92400e
>     classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5
>     Manager[RIA Manager]:::service --> KFMS[KFMS Entry]:::service
>     KFMS --> DVP[DVP Engine]:::service
>     DVP --> CAS[(CSDB)]:::data
>     DVP --> BC[Boundary: NISA report]:::boundary
>     class DVP service
> ```
>
> ## 9. Maturity & adoption signals
> - **Adopt when:** Your QCAs have >30% of instructions crashing at the same deadline bucket and you have a dedicated compliance officer tracking NISA vs SLA variance.
> - **Anti-signals (don't adopt yet):** Team still negotiating bespoke settlement windows with B2B partners instead of reporting against NISA buckets.
> - **Common failure modes:** (1) Time-zone misalignment between trade venue and custody DST, (2) Thread-pool exhaustion on settlement day, (3) Missing holiday calendars for CAS/BCSA.
>
> ## 10. Common confusions — the "don't mix" list
> | Often confused | Real distinction |
> |----------------|------------------|
> | Service level vs SLA | Service level is a regulatory target; SLA is a commercial commitment. |
> | T+n vs T+n + m grace | NISA allows no grace; any contractual m must be disclosed but does not extend the enforceable bucket. |
> | Finality vs identification | Finality is legal irrevocability; identification is internal ledger tagging. |
>
> ## 11. Tools & standards to know
> - **Frameworks/IR-2 / NINE:** NISA Annex A (service levels), NCSA Rule 3.3.1 (CSP finality).
> - **Common tooling:** Archi for service-level mapping, Python/Apache Airflow for deadline monitoring dashboards, Grafana for real-time pool utilization.
> - **Mandatory reading:** CSA Staff Notice 51-318 (Settlement risk), OSFI Guideline B-13 (Operational Risk).
>
> ## 12. ADR template (ready to fill in)
> ```markdown
> # ADR-12: Sub-500ms RPO for T+1 inter-group settlement
> ## Status
> Accepted
> ## Context
> Current T+1 inter-group transfers from Toronto to Montreal have RPO of 12 s, which misses T+1 under single-site failure.
> ## Decision
> Adopt a hot-standby settlement node in Montreal with <500ms RPO; auto-promote on Toronto power-outage signal.
> ## Consequences
> - Positive: Meets T+1 even under single-site failure; improves CSA SLA.
> - Negative: Additional $240K/yr infrastructure cost; added operational complexity.
> ## Alternatives considered
> 1. Geo-deposit read-only with async recovery — RPO ~10 s, insufficient.
> 2. Paper backup manual settlement — violates NISA and automation policy.
> ```
>
> ## 13. Practice — apply it
> 1. **Recall:** define in 2 min without notes.
> 2. **Model:** produce an ArchiMate diagram showing the T+2 settlement concept and execution concepts.
> 3. **ADR:** write a decision doc applying it to a CIBAM-CSDM inter-group transfer.
> 4. **Defend:** roleplay explaining to a non-technical CRO why the custodian pays a fine even if the bank's clearing broker caused the delay.
>
> ## Summary
> NISA service levels are the immutable scaffolding of any custody settlement system. The architect's job is to make the scaffolding invisible: by sizing infrastructure, automating compliance checks, and quantifying finality with millisecond precision, the firm never touches the regulatory limit. Any slip is a compliance event, not merely an operational one.
>
> ---
> **Status:** ☐ Not started · ☐ In progress · ✅ Covered
> *Last updated: 2026-09-16*
>
> ---
> **One diagram required. Both brief + detail must exist with ≥1 mermaid each before ✓.**
