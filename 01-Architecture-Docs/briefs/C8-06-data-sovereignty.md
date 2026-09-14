# [C8-06] Data Sovereignty — BRIEF
> **Category:** C8 — Reference Architecture, Standards & Principles · **Difficulty:** ◑ · **Banking-relevant:** yes
> **One-liner:** Data sovereignty is the set of legal, contractual, and technical constraints that dictate where personal or financial data may be stored, processed, and transferred, ensuring compliance with national and regional data-protection laws such as GDPR, DORA, and local residency requirements.
> **Why an EA cares:** A misrouted data flow can trigger a €20M GDPR fine and a DORA enforcement action; sovereignty is not an afterthought—it is a first-class architectural constraint.

## Quick definition
**Data sovereignty** is the rule that data—its storage, processing, and cross-border transfer—must comply with the laws of the jurisdiction in which it is collected, processed, or located. It is enforced through *technical* (data-residency tags, encryption key location, network segmentation) and *governance* (DPO sign-off, data-processing agreements, cross-border transfer mechanisms like Standard Contractual Clauses or BCRs).

## Key ideas / terms
- **Data residency:** the geographical location of physically stored data (e.g., EU customer data must not leave the EEA).
- **Jurisdictional partition:** the logical or physical separation of data by legal domain (e.g., EU-1 vs. US).
- **Encryption jurisdiction:** keys point of management must match the data’s sovereignty domain (e.g., HSM in the EU for EU data).
- **Technical enforcement:** network egress filtering, cloud-provider region locking, data-labeling tags that routes into compliant pipelines.
- **Governance enforcement:** DPOs, data-processing agreements (DPAs), cross-border transfer impact assessments (TIA).
- **Sovereignty gap:** the mismatch between an architecture that assumes global distribution and a legal reality that restricts data to one or more jurisdictions.
- **Data mesh as sovereignty enabler:** because each domain owns its data product, sovereign domains can implement their own connectivity and residency targets locally.

## The mental model
Think of data sovereignty as *border control* for data packets. A digital contract in the UK may not be stored in a US data-center just because the cloud contract cost is lower; that is a sovereignty violation. The EA’s job is to treat jurisdictional boundaries as *real architectural boundaries*—the same way we treat security zones or network subnets. Every data flow must cross a *sovereignty gate*: is PRD A and B in the same jurisdiction? if not, what transfer mechanism (SCCs, Binding Corporate Rules, EU standard replication) legitimizes the flow?

## One diagram (mandatory)
```mermaid
graph LR
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef context fill:#dfe6e9,stroke:#636e72
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5
    
    UK[UK Region<br/>(London & Edinburgh)]:::boundary
    EU2[EU Region<br/>(Frankfurt)]:::boundary
    US[US Region<br/>(US-East / US-West)]:::boundary
    
    UK_Data[(UK Customer<br/>Data)]:::data
    EU_Data[(EU Customer<br/>Data)]:::data
    US_Data[(US Customer<br/>Data)]:::data
    
    UK_Data -->|UK data-subject<br/>request| UK_DPO[DPO + IRM<br/>(UK)]:::decision
    EU_Data -->|dual request| EU_DPO[DPO + IRM<br/>(EU)]:::decision
    
    UK_Data -->|replicate via<br/>SCCs + BCR| EU2
    EU_Data -->|blocked| US
    US_Data -->|allowed; no<br/>special transfer| UK
    
    UK_DPO -->|consent record| UK_Data
    EU_DPO -->|consent record| EU_Data
    
    API[Retail Banking API]:::service -->|reads UK-only| UK_Data
    API -->|reads EU| EU_Data
    API -.->|rejects| US_Data
    
    classDef region boundary
    class UK,EU2,US location
    class UK_Data,EU_Data,US_Data data
    class UK_DPO,EU_DPO decision
```

## When to use / when NOT to use
- ✅ **Use when:** designing a multi-cloud, multi-region data platform, onboarding M&A data, or entering a new jurisdiction (e.g., UAE, Singapore).
- ⚠️ **Avoid when:** the entire repository serves only a single jurisdiction with no cross-border sharing and no sensitive personal data.

## Banking 💳 example
A UK retail bank partners with a US FinTech to offer a co-branded credit card. Under GDPR Art. 44-49 and UK DPA 2018, EU personal data of EU cardholders must not be transferred to the US *unless* the FinTech has approved Standard Contractual Clauses (SCCs) and a Transfer Impact Assessment (TIA). The EA designs a sovereignty layer:
- EU card data is stored only in Frankfurt (UK region is out for EU-only cards due to Brexit regulations—EU data in UK now requires an adequacy decision).
- US-issued cards use US region data; no overlapping residency.
- Cross-border reporting (AML) uses pseudonymized hashes that cannot be re-identified without the keys, which are held in the EU.
- A data-mesh domain (Payments Data Zone) exposes only the required PII slice to the US FinTech via an API gateway with mTLS and rate-limiting, and the EU DPO must sign off on every schema change.

## Common confusions (don't mix these up)
- **Data residency** vs **data sovereignty:** residency = where data is stored; sovereignty = the full legal framework governing that storage and transfer.
- **GDPR** vs **UK DPA 2018:** GDPR = EU regulation; UK DPA = UK in-force version post-Brexit, with UK-specific provisions and an adequacy decision framework.
- **Data mesh** vs **data lakes:** a mesh enforces domain ownership and data-product contracts; a lake is a raw storage pool.
- **Encryption** vs **sovereignty:** encrypting data does *not* remove sovereignty obligations (the key itself is personal data under GDPR).

## Interview / recall prompt
“Explain data sovereignty in 2 minutes without notes.” →
- It is the legal framework governing where data may live, be processed, and be transferred.
- GDPR Art. 44-49 and DORA impose cross-border restrictions.
- Technical enforcement (region locking, encryption-key location) and governance (DPOs, SCCs, TIAs) must work together.
- Data mesh helps because each sovereign domain owns its own products and controls its own boundaries.
