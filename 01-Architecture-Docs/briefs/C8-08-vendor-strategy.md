# [C8-08] Vendor Strategy — BRIEF
> **Category:** C8 — Reference Architecture, Standards & Principles · **Difficulty:** ◑ · **Banking-relevant:** yes
> **One-liner:** Vendor strategy in banking IT architecture is the managed selection, governance, and exit of cloud, embedded-finance, and outsourcing partners—balancing cost, resilience, interoperability, and regulatory liability while avoiding single-vendor lock-in and reputational exposure.
> **Why an EA cares:** A vendor that fails one time — a cloud outage, a data-breach, a compliance gap — can trigger a DORA enforcement action or erode customer trust in months.

## Quick definition
**Vendor strategy** is the deliberate management of third-party and embedded-finance partners—cloud platforms, software-as-a-service (SaaS), cross-border processors, embedded-finance gateways—through due diligence, contractual terms, interoperability standards, and clear exit pathways. It is not procurement shopping; it is architecture-level risk management that determines *which* problems you solve, *which* control lines remain yours, and *which* capabilities can you swap without rebuilding.

## Key ideas / terms
- **Vendor lock-in:** switch costs so high that replacing a vendor requires rebuilding—not just migrating—to escape.
- **Embedded finance:** third-party products embedded in a bank’s customer app (e.g., Klarna BNPL, Starling Embedded, Visa Direct).
- **Vendor concentration:** risk that a single vendor + their sub-vendor (cloud, hardware, chip) dominates critical capabilities.
- **Functional-depolarity:** the discipline of evaluating vendors by *capability* (rating at most 5 criteria), not *position* (giving the top spot to the vendor with the most features).
- **Vendor-neutral core:** the architectural principle that the bank’s own systems must own the *master data* and *core logic*, while vendors only layer on-top.
- **Contractual liability:** who pays for the breach, data loss, or service failure—and whether the vendor carries insured cyber cover.
- **Exit gateway:** a pre-negotiated, tested switchover pathway (data export, integration, and cutover plan) written before a vendor becomes strategic.
- **Escrow:** source code, documentation, and interfaces held in escrow so the bank can continue operating if a vendor exits or is acquired.

## The mental model
A vendor is not a *supplier machine*; it is a *strategic alliance with an interface contract*. The bank’s architecture must be able to *live without* any vendor, not just *live with* them. The EA’s job is to decide:
- **What is a commodity?** (cloud compute, basic identity) → always switch.
- **What is a specialty?** (fraud detection, AML risk models) → sometimes buy.
- **What is a partner?** (embedded finance, core banking replacement) → then the architecture must *own the boundary*; you cannot be the commodity beneath a partner.

## One diagram (mandatory)
```mermaid
graph LR
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef service fill:#bfdbfe,stroke:#1e40af
    classDef data fill:#fde68a,stroke:#92400e
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5
    classDef risk fill:#fecaca,stroke:#991b1b
    
    Bank[Bank Core<br/>(Master Data)]:::data
    Bank -->|owns| Master[Master Data<br/>& Logic]:::data
    Master -->|exposes| API[Core API<br/>Gateway]:::critical
    
    FinTech[Embedded Finance<br/>(Klarna / Starling)]:::service
    FinTech -->|requests| API
    API -->|governs| Policy[Policy Engine<br/>(Gate)]:::decision
    
    Cloud[Cloud Platform<br/>(AWS / GCP)]:::service
    Cloud -->|runs| Bank
    Cloud -->|runs| FinTech
    
    Audit[External<br/>Audit & Pen-test]:::context
    Audit -->|reviews| Cloud
    
    Escrow[Source Code<br/>& Documentation<br/>Escrow]:::boundary -->|holds backups| Bank
    
    VendorL[Vendor Lock-in<br/>Risk: High]:::risk
    Cloud -.->|concentration| VendorL
    FinTech -.->|concentration| VendorL
    
    Exit[Exit Gateway<br/>Pre-negotiated]:::decision -->|planned<br/>switch| Bank
    
    classDef data data
    class Bank,Master,API,API,data
    class FinTech,Cloud,..>Cloud,..>Cloud service
    class Policy,Exit decision
    class Escrow boundary
```

## When to use / when NOT to use
- ✅ **Use when:** evaluating cloud providers, entering embedded-finance partnerships, or outsourcing risk-engine data pipelines—your architecture will live with them for years.
- ⚠️ **Avoid when:** for a one-off vendor license (e.g., a meeting-room booking tool) with no downstream dependency; a lightweight RIBA/SLA suffices.

## Banking 💳 example
A UK retail bank partners with Klarna for an instant-BNPL (buy-now-pay-later) product via an API gateway. The EA’s vendor strategy specifies:
- **API versioning:** all Klarna endpoints are contract-defined v1/v2/v3; breaking changes are blocked until a new v4 is negotiated.
- **Rate limits:** per-user rate limits enforced at the bank’s gateway to prevent Klarna API abuse.
- **Data ownership:** the bank owns the cardholder consent and transaction history; Klarna only sees a transaction token.
- **Source-code escrow:** if Klarna exits or is acquired by a non-cooperative entity, escrow triggers.
- **Exit gateway:** a 90-day switchover plan to a fallback BNPL provider (e.g., Afterpay) with data-export, schema-mapping, and a war-room simulation.
- **Concentration limit:** no single BNPL partner > 30% of digital-origination volume.

## Common confusions (don't mix these up)
- **Vendor lock-in** vs **dependency:** lock-in = you *cannot* exit cheaply; dependency = you *could* but it takes effort.
- **Vendor strategy** vs **procurement:** strategy = architecture-level risk management; procurement = price + delivery + contract.
- **Embedded finance** vs **core banking:** embedded = third-party product surface; core = the bank’s own data and logic.
- **Vendor-neutral** vs **technology-agnostic:** vendor-neutral = owning data and logic irrespective of vendor; technology-agnostic = choosing tech based on features, not brand.

## Interview / recall prompt
“Explain vendor strategy in 2 minutes without notes.” →
- It is not procurement; it is architecture-level risk management.
- Key: vendor lock-in, vendor concentration, exit gateways, source-code escrow.
- Functional-depolarity = evaluate by capability, not just features.
- The bank’s own systems must own master data; vendors only layer on.
- A single vendor can become a single point of regulatory failure.
