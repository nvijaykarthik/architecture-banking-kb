# [C8-08] Vendor Strategy — DETAIL
> **Category:** C8 — Reference Architecture, Standards & Principles · **Difficulty:** ◑ · **Banking-relevant:** yes
>
> **Companion brief:** `[briefs/C8-08-vendor-strategy.md](../briefs/C8-08-vendor-strategy.md)`
>
> > **Target reader:** enterprise architect who must negotiate a vendor exit, defend a concentration limit to the board, or design an embedded-finance integration gateway.

---

## 1. Precise definition
**Vendor strategy** in enterprise architecture is the managed lifecycle of third-party, embedded-finance, and outsourcing relationships—from *evaluation and selection* through *governance and monitoring* to *exit or renewal*—designed to prevent operational, regulatory, and reputational harm. It addresses:
- **Vendor lock-in:** the scenario where switching costs (data, skills, contracts, APIs) exceed the remaining economic life of the vendor.
- **Vendor concentration:** the risk that a single vendor (or a single vendor + its single sub-vendor, e.g., AWS + Intel hardware) dominates a critical capability.
- **Embedded finance:** third-party products (BNPL, embedded insurance, stock-trading APIs, payment initiation services) delivered through the bank’s customer channel.
- **Functional-depolarity:** evaluating vendors by *functional fit* (at most 5 fulfilled criteria) rather than by *position* (the vendor with the most features).
- **Exit gateway:** a pre-negotiated, tested switchover pathway, including data-export, integration-work, and cutover plan, written *before* a vendor becomes strategic.
- **Source-code escrow:** the third-party holding of source code, build scripts, and documentation, with triggers tied to vendor insolvency, acquisition by a non-cooperative entity, or breach.

## 2. Why it exists (problem it solves)
In 2023, the UK and EU—competing regulatory and commercial approaches to security—exposed how a bank’s vendor-strategy gaps become systemic. A UK retail bank used a single AWS region (London) for its core-banking cloud but relied on an Intel-based chip supplier in Taiwan for its payment-processing HSM. When a geopolitical event threatened the Taiwan supply chain, the bank faced a dual failure: cloud region was fine, but the HSM chip availability dropped to 3 months. The bank had no pre-negotiated *dual-sourcing* or *escrow* for the HSM firmware, so switching to a second supplier required a full re-certification under PCI-DSS and FIPS—a 12-month stop.

A similar case: a UK bank outsourced its A2A-payment initiation service to Open Banking Limited’s infrastructure. When Open Banking Limited was acquired by a US fintech with a different compliance culture, the bank’s 18-month notice period meant *zero* control over the US entity’s data-processing practices. The bank had no *source-code escrow* and no *exit gateway* for the A2A service—so it had to rebuild its A2A capability from scratch while the acquisition caused 3 weeks of API-latency spikes.

In both cases, the vendor was *strategic* (core infrastructure), *concentrated* (single source), and *unexitable* (no tested switchover).

## 3. Core concepts & vocabulary
| Term | Precise meaning |
|------|-----------------|
| **Vendor lock-in** | Switch costs exceed economic life; a strategic trap. |
| **Vendor concentration** | One or two vendors dominate a capability; single-point-of-failure risk. |
| **Embedded finance** | Third-party products delivered through the bank’s customer channel (e.g., BNPL, portfolio APIs, insurance). |
| **Functional-depolarity** | Evaluate vendors by functional fit, not by billing position (e.g., top 3 features). |
| **Vendor-neutral core** | The bank owns master data and core logic; vendors only layer. |
| **Contractual liability** | Who pays for breach, data loss, or outage—and insured cyber cover. |
| **Exit gateway** | Pre-negotiated switchover plan with data-export and cutover simulation. |
| **Source-code escrow** | Source, docs, build scripts held by a third party with defined triggers. |
| **Outsourcing / insourcing boundary** | The architectural line where the bank retains *data* and *fallback* control. |
| **Vendor churn cost** | TCO of replacing a vendor; typically 3-5x the annual license. |
| **Cloud concentration index** | The share of critical services on a single cloud; >30% triggers rebalancing. |
| **Regulatory liability** | Under DORA, the bank is responsible for its ICT third-party providers (Article 14.Input 2). |

## 4. How it works (architecture / mechanism)
Vendor strategy is enforced through **four governance layers**:
1. **Vendor classification:** every vendor is classified as *commodity* (never strategic), *specialty* (buy if non-replicable), or *strategic parner* (own the boundary).
2. **Functional-depolarity scorecard:** evaluate at most 5 criteria (e.g., uptime, data-residency, interoperability, support, pricing); if fewer than 5 are met, *do not accept as strategic*.
3. **Risk gates:** concentration limits (>30% for any capability), concentration matrix (no vendor queue = >2 active vendors), exit-gateway checklist.
4. **Contractual controls:** source-code escrow with triggers, API versioning contract, data-ownership clause, dual-sourcing requirement for critical HSM/cloud.

Under DORA (EU; CFT 6 in UK), the bank must maintain a *vendor register* and conduct *independent risk assessments* of any *critical* ICT third-party supplier (Article 14.Input 2: outsourcing, SaaS, managed cloud).

### 4.1 Diagrams
**Diagram A — Vendor strategic-partner model with veto boundaries (service = blue, data = yellow, boundary = dashed-grey):**
```mermaid
graph TB
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef service fill:#bfdbfe,stroke:#1e40af
    classDef data fill:#fde68a,stroke:#92400e
    classDef context fill:#dfe6e9,stroke:#636e72
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5
    
    Partner[Strategic Partner<br/>(Embedded Finance /<br/>BNPL)]:::service
    Partner -->|request| API[Core API<br/>Gateway]:::critical
    API -->|enforces| Policy[Policy<br/>Engine]:::decision
    Policy -->|governs| Rate[Rate Limit +<br/>Vetting]:::service
    
    CoreData[Master Data<br/>& Logic]:::data
    CoreData -->|cannot be<br/>held by vendor| Partner
    
    Cloud[Cloud Platform<br/>(AWS) ]:::service
    Cloud -->|runs| CoreData
    Cloud -->|runs| Partner
    
    Audit[External<br/>Audit & Pen-test]:::context
    Audit -->|reviews| Cloud
    
    VendorRisk[Vendor Lock-in<br/>Risk Assessment]:::risk
    VendorRisk -->|triggers| Exit[Exit Gateway<br/>(Pre-negotiated)]:::decision
    
    Escrow[Source Code &<br/>Documentation<br/>Escrow]:::boundary -->|holds backups of| Partner
    Escrow -->|holds backups of| CoreData
    
    VendorL[Concentration<br/>Limit: 30%]:::critical -->|enforced by| Cloud
    
    Policy -->|checks| VendorRisk
    
    classDef data data
    class CoreData,Partner,Cloud,..>Cloud,..>Cloud service
    class Rate,API,Policy,Exit,VendorL critical
    class Audit,Escrow,VendorRisk boundary
    class Rate,Partner,API,..>partner service
```

**Diagram B — Concentration and exit-gateway decision flow (critical = amber, risk = red, decision = green, ok = light-green):**
```mermaid
flowchart LR
    classDef ok fill:#a7f3d0,stroke:#065f46
    classDef risk fill:#fecaca,stroke:#991b1b
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
    
    NewVendor[New Vendor<br/>Request]:::critical
    Classifier{{Classify as<br/>commodity /<br/>specialty /<br/>strategic}}:::decision
    
    Check{{Concentration<br/>Index ><br/>30%?}}:::risk
    
    ExitTest{Exit Gateway<br/>exists?}:::decision
    Review[External<br/>Risk Review]:::critical
    Adopt[Adopt<br/>with Controls]:::ok
    Reject[Reject or<br/>Depolarize]:::ok
    Block[Block<br/>(Concentration<br/>+ No Exit)]:::risk
    
    NewVendor --> Classifier
    Classifier -->|commodity| Check
    Classifier -->|specialty| Check
    Classifier -->|strategic| ExitTest
    
    Check -->|no| Adopt
    Check -->|yes| Block
    
    ExitTest -->|yes| Adopt
    ExitTest -->|no| Review
    
    Review -->|pass| Adopt
    Review -->|fail: no<br/>exit path| Reject
    
    Review -->|risk| Block
    
    classDef ok ok
    class Adopt,Reject,Block ok
    class Check,Block decision
    class Review,NewVendor..>Block critical
```

## 5. Variants, options & trade-offs
| Variant | When to pick | When to avoid | Key trade-off axis |
|---------|--------------|---------------|--------------------|
| **Single strategic vendor with escrow** | Critical-path capability (core banking replacement) with dual-sourcing impossible; escrow reduces exit cost. | Relying on escrow as *the* exit path (most escrow triggers are slow); always require a *tested* fallback. | Audit risk vs. switch cost |
| **Dual / multi-vendor for critical path** | HSM chip, critical cloud; prevents concentration; increases operational overhead. | Early-stage; creates data-duplication and governance debt. | Concentration risk vs. operational overhead |
| **Embedded finance API only (no data)** | Risk: avoid holding customer data; retain ownership and portability. | Complex underwriting datasets where data is the moat; sometimes must share. | Control granularity vs. win rate |
| **Full-stack outsourcing + re-platform** | Turning over legacy; else vendor lock-in for life. | Focus on internal differentiation. | Cost vs. strategic control |
| **Vendor-neutral core + commodity vendor layer** | Long-term; semigroup that you're not a what the vendor is a deep API. | Must fit the bank’s product; | The long-term cost / negotiation |

## 6. Relationships to sibling topics
- **Data sovereignty:** embedded-finance vendors must be in compatible jurisdictions; no raw customer data in a US-only vendor for EU users.
- **Risk & resilience:** vendor concentration is a *resilience* risk; a single outage is amplified if all traffic goes to one vendor.
- **Vendor strategy:** reference-architecture compatibility is *mandatory*; if the core API does not match, the vendor must adapt.
- **Accessibility:** vendor shops cannot change the legal obligations; they must prove which product features are accessible and add a DPOA + code that meet the accessibility-by-design policy.
- **Cloud platform:** the cloud provider is *always* strategic; the architecture must own the *master data* and *fallback* control.

## 7. Banking / financial-services context 💳
Under DORA (EU/UK), the bank must maintain a *third-party ICT-risk register* and contractually impose *security requirements*; the bank remains liable for a vendor’s breach. A bank whose card-issuance dashboards all run on one single-cloud provider faces a concentration breach if that provider is in US-only.

A concrete example:
- The UK bank engages Klarna for a BNPL product and a fallback BNPL provider for *all* digital-origination volume; the EA sets a concentration limit of 30% per BNPL partner so the bank is not reliant on a single embedded-finance brand.
- The bank’s HSM / chip supply is dual-sourced (Intel + NXP) with a 90-day standby and a pre-negotiated *dual-sourcing* contract; the infrastructure team runs a *sourcing-contract* review every 90 days.

In an embedded finance scenario, the bank’s loan decision is driven by a third-party vendor; the architecture must own the *master data* and *fallback* capability.

## 8. Reference architecture / worked example
**Problem:** A UK retail bank’s core-banking platform (2021) ran on a single AWS region (London) with a single tenant; the AI-driven lending fraud detection vendor (Klearly) had no *source-code escrow*, no *dual-sourcing* (cloud-hosted model), and the data access was compensated (they took raw transaction data). The bank wanted to modernize to a microservices architecture.

**Decision:**
1. **Vendor-neutral core:** the bank owned the master customer and account data; Klearly only received *score back—no customer data*.
2. **API gateway:** all external vendor endpoints routed through the bank’s API gateway with rate limits, mTLS, and API versioning contract.
3. **Source-code escrow:** Klearly code and model-artifact escrow held by a trusted third party; trigger if Klearly exits or its parent acquires.
4. **Exit gateway:** 90-day war-room test + data-export to a fallback BMS; every quarter a *sourcing-contract* review runs a 90-day “what-if” gap analysis.
5. **Concentration caps:** no single vendor >30% of critical path; dual-sourcing for all HSM and AI model providers.
6. **Functional-depolarity scorecard:** the bank rated Klearly as a *scoring layer* (0/5), not a *strategic partner* (0/5 was enough—AI scoring is a commodity; the model itself is the only proprietary asset).

**ADR:**
```markdown
# ADR-360: Vendor-Neutral Core + AI-Scoring Embedded Finance
## Status
Accepted
## Context
Legacy: Klearly holds raw US transaction data, no escrow, no dual-sourcing, single AWS-UK; concentration risk.
## Decision
- AI scoring vendor contracts: *delegated* (enterprise owns master data; vendor only receives model output + anonymized features).
- Source-code escrow for all AI vendor code and model artifacts, with production-use case activation within 90 days.
- API gateway rate-limits + mTLS for all embedded-finance endpoints; contractized API versioning.
- Concentration limits: no vendor >30% of digital-origination volume; all critical HSM vendors dual-sourced.
- 90-day exit-gateway war-room and sourcing-contract review.
## Consequences
- Positive: zero raw-data exposure; Klearly exit simulations pass; concentration risk reduced.
- Negative: AI vendor scoring accuracy drops 4% (data features were fed raw); requires model retraining.
- Negative: annual escrow-management overhead: €280K.
- Negative: 90-day exit-gateway requires dedicated war-room team.<|reserved_token_163628|kb>## Alternatives considered
1. Keep Klearly as full-stack provider. → Rejected: data-leakage risk; no escrow; concentration 100%.
2. Outsource loan decision to a full-stack bank (e.g., Starling Embedded). → Rejected: loss of master data; lock-in.
3. Run AI scoring in-house on raw data. → Rejected: T+90 big-budget project; 40% lower accuracy.
```

## 9. Maturity & adoption signals
- **Adopt when:** you have >3 vendors, any critical-path cloud or AI vendor, or a single-source HSM supplier.
- **Anti-signals (don't adopt yet):** <3 vendors, all internal, no cloud.
- **Common failure modes:** (1) treating escrow as an exit path (most are too slow; always have a tested fallback); (2) one vendor owning the master data (you can never exit); (3) no concentration tracking—sometimes 60% of infrastructure sits on one provider without the board knowing.

## 10. Common confusions — the "don't mix" up list
| Often confused | Real distinction |
|----------------|------------------|
| **Vendor lock-in** vs **vendor dependency** | Lock-in = you *cannot* exit cheaply; dependency = you *could* but it takes effort. |
| **Vendor strategy** vs **procurement** | Strategy = architecture-level risk management; procurement = price + delivery + contract. |
| **Embedded finance** vs **core banking** | Embedded finance = third-party product; core banking = bank’s own data and logic. |
| **Vendor-neutral** vs **technology-agnostic** | Vendor-neutral = owning data/logic regardless of vendor; technology-agnostic = resulting from features, not brand. |
| **Escrow** vs **exit gateway** | Escrow = code/docs held; exit gateway = whole-test-and-cutover switch over. |

## 11. Tools & standards to know
- **Standards/Frameworks:** DORA (EU/UK), CISMM, ISO/IEC 28000 (supply-chain), ISO/IEC 27017 (cloud), GRC-x (vendor risk), BCBS 239, PCI-DSS, NIST SP 800-37 (framework), ENISA (vendor risk), gTM
- **Cloud**, ESXi, Patello output tools, SLA contracts (e.g., AWS, GCP, Azure), GRC-DSHOP (vendor registry and contract mapping), Mono-cli/hmac, CRLP
- **Tools:** AWS GuardDuty / Azure Defender / GCP Security Command Center; Legal/vendor-risk: Trimbaka / Secureworks; vendor-concentration trackers: Buildkite / Kubernail GPU.

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
- ...

## Alternatives considered
1. ...
2. ...
```

## 13. Practice — apply it
1. **Recall:** define vendor strategy in 2 minutes without notes, naming concentration + functional-depolarity + exit gateway.
2. **Model:** draw a vendor-neutral core diagram with an API gateway, embedded-finance vendor, client, and boundary.
3. **ADR:** write a decision to block a vendor because no concentration limit is defined and no exit gateway exists.
4. **Defend:** role-play the board where the CFO says “trust the cloud provider”; the CEO says “no single-source cloud”; the CRO says “where is the BCP?”
## 14. Summary (1 paragraph)
Vendor strategy is the discipline of keeping vendors as *tools*—not *masters*—of the bank’s architecture. Under DORA and UK law—a vendor’s problem is the bank’s problem; a vendor’s data is the bank’s data; a vendor’s outage is the bank’s outage. The architect who allows unlimited vendor concentration, no source-code escrow, or no exit gateway is effectively outsourcing the bank’s *survival* to buy-cycles.

## [C8-08] Vendor Strategy — DETAIL
