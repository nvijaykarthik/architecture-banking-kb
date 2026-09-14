# C3-07 Data Governance — BRIEF
> **Category:** C3 — Architecture Domains · **Difficulty:** ◑ · **Banking-relevant:** yes
> **One-liner:** Engineering the policies, roles, and workflows that ensure every 💳 banking data asset is accurate, complete, compliant, and usable—so that regulators, analysts, and customers can trust what the data represents.
> **Why an EA cares:** In a bank, a data governance gap means inaccurate risk models, failed KYC, regulatory fines, and customer churn; governance is the operating system for data architecture.

## Quick definition
Data governance is the management of data as an enterprise asset through formal policies, standards, workflows, and accountability structures—covering quality, security, privacy, classification, lifecycle, and regulatory compliance.

## Key ideas / terms
- **Data Governance Framework:** A set of processes, roles, and policies governing how data is managed (e.g., DAMA-DMBOK).
- **Data Quality:** Completeness, validity, consistency, timeliness, and uniqueness of data values.
- **Data Classification:** Tiering data by sensitivity (e.g., Public, Internal, Confidential, Restricted) to apply appropriate controls.
- **Master Data Management (MDM):** The discipline of creating, maintaining, and governing a single trusted master record for core domains (e.g., Customer, Product, Account).
- **Ownership / Stewardship:** The assignment of accountable individuals (business / data stewards) who can define and enforce policy.
- **DAMA-DMBOK:** Data Management Body of Knowledge; the canonical framework for data governance and management.
- **Privacy Engineering:** Embedding privacy into systems (data minimization, anonymization, consent management).
- **Policy-as-Code:** Applying machine-readable policies (e.g., OPA, Open Policy Agent) to enforce data governance automatically.
- **Data Masking / Redaction:** Transforming PII for non-production use while preserving structural validity.
- **Retention / Disposition:** Rules for how long data is stored, archived, and securely destroyed.

## The mental model
Data governance is the 💳 bank’s parliamentary process: just as stable democracies rely on constitution (policies), independent judiciary (stewards), and elected representatives (owners) to keep laws coherent and respected, a bank relies on governance to keep data accurate, compliant, and usable across silos.

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

    DataCatalog[Data Catalog / Discovery]:::data
    QualMetrics[Quality Metrics / Rules]:::data
    Policies[Policy-as-Code (OPA)]:::critical
    Steward[Data Steward / Owner]:::critical
    Audit[Audit / Compliance Check]:::decision
    MDR[(MDM Hub — Golden Record)]:::data
    Dashboard[Governance Dashboard]:::ok
    Compliance[Regulatory Req: DORA, PCI, GDPR]:::risk

    DataCatalog --> QualMetrics
    QualMetrics --> MDR
    Policies --> MDR
    Steward --> Policies
    Steward --> MDR
    MDR --> Audit
    Audit --> Dashboard
    Compliance -. drives .-> Policies
    Compliance -. drives .-> Audit

    class Policies critical
    class Steward critical
    class MDR data
    class Compliance risk
```

## When to use / when NOT to use
- ✅ **Use when:** Launching a data lake, entering a regulated reporting regime (DORA, Basel), or experiencing data-quality incidents.
- ⚠️ **Avoid when:** A one-off internal exploration project with no reusable asset and no compliance boundary.

## Banking 💳 example
A 💳 retail bank must ensure that every KYC profile is complete, consent is auditable, and sanction screening runs on the golden record (MDM). Without data governance, duplicate customer records cause missed sanctions; inconsistent interest-rate tables cause regulatory misstatement.

## Common confusions (don't mix these up)
- **Data Governance** vs **Data Management:** Governance sets policy and accountability; management executes (cleans, migrates, stores).

## Interview / recall prompt
_“Explain data governance in 2 minutes without notes.”_ →
- 1) It’s the management of data as an enterprise asset through policy, roles, and workflows
- 2) It covers quality, security, privacy, compliance, and lifecycle
- 3) Stewardship + accountability + domain ownership are the pillars
- 4) In banking, it prevents compliance fines and data-quality failures
- 5) Data governance is the operating system for data architecture and analytics

---
**Status:** ✅ Covered
