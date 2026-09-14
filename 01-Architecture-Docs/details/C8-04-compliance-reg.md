# [C8-04] Compliance & Regulation — DETAIL
> **Category:** C8 — Reference Architecture, Standards & Principles · **Difficulty:** ● · **Banking-relevant:** yes
>
> **Companion brief:** `[briefs/C8-04-compliance-reg.md](../briefs/C8-04-compliance-reg.md)`
>
> > **Target reader:** enterprise architect who must defend a design to a CRO or regulator and prove that the architecture *produces* compliance evidence at runtime.

---

## 1. Precise definition
**Compliance** in enterprise architecture is the state—continuously maintained, not periodically proven—in which every system, interface, and process satisfies the specific legal, regulatory, contractual, and market-mandated requirements of the jurisdictions in which the bank operates. *Architecture for compliance*—also called *regtech by design*—means that the technical choice, topology, and data-flow themselves encode the control, producing machine-readable evidence that satisfies attestation requirements without manual reconciliation.

Distinguish lines:
- **Hard compliance** = laws (e.g., Banking Act, Basel III). Violation = civil/criminal liability.
- **Soft compliance** = contracts, standards, or market expectations (e.g., vendor SLA, ISO 27001).
- **Regulatory overlap** = one control satisfies multiple requirements (e.g., PCI-DSS 4.0 encryption requirements reduce DORA “strong cryptography” burden).

DORA Article 15 explicitly requires *“documented, up-to-date, and maintained”* information architecture artifacts. This shifts the obligation from “we have a policy” to “our architecture *proves* the policy is enacted.”

## 2. Why it exists (problem it solves)
In 2020, a German cooperative bank’s mortgage origination system was certified under BaFin guidelines. The system passed the initial audit, but six months later a regulator discovered that a “legacy” batch layer in the loan-approval pipeline used a deprecated TLS 1.0 endpoint for a third-party appraisal service. The certificate had not been renewed because the vendor relationship changed three times; nobody owned the endpoint in the architecture register. The bank faced a warning and a €1.2M remediation cost. The root cause was architecture-level: no compliance-by-design gate on new endpoints, no automated certificate monitoring, no architectural mechanism linking vendor contracts to the service catalog.

## 3. Core concepts & vocabulary
| Term | Precise meaning |
|------|-----------------|
| **Hard compliance** | Legally binding; deviation is illegal (e.g., AML, Basel III capital, Consumer Duty). |
| **Soft compliance** | Contractual or market-driven (e.g., SWIFT GSN, vendor SLA). |
| **Regulatory overlap** | A single control satisfies multiple regulatory regimes of different natures. |
| **Attestation** | A formal, periodic statement by an internal or external party that a system or process is compliant. |
| **Auditability by design** | The architecture—not a separate process—produces auditable, queryable evidence. |
| **Evidence API** | A machine-readable endpoint (e.g., /compliance/evidence?control=AML–03) that returns live attestation data. |
| **Compliance-by-design gate** | A pre-commit or pre-deploy check that blocks a change if it would violate a mapped regulatory requirement without a compensating control. |
| **Control card** | A living artifact mapping a regulatory clause to the architectural component that satisfies it, with evidence links. |

## 4. How it works (architecture / mechanism)
compliance for IT architecture operates through **four layers**:
1. **Requirement ingestion** — legal and regulatory text is normalized into machine-readable control clauses (e.g., DORA ART.15.3.1 → “authentication and access control”).
2. **Architectural mapping** — each component in the reference architecture is mapped to a control card; missing mappings trigger a backlog item.
3. **Runtime evidence** — controls are enforced by runtime mechanisms (policy-as-code, secrets rotation, immutable logging, API gateways) that emit event evidence.
4. **Attestation query** — regulators or internal auditors query the evidence API; no human manual reconciliation is needed.

### 4.1 Diagrams
**Diagram A — Evidence generation pipeline (highlighting data = yellow, service = blue, boundary = dashed-grey):**
```mermaid
graph LR
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef service fill:#bfdbfe,stroke:#1e40af,stroke-width:1px
    classDef data fill:#fde68a,stroke:#92400e,stroke-width:1px
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5
    classDef risk fill:#fecaca,stroke:#991b1b,stroke-width:1px
    
    Gov[Regulator /<br/>Compliance Framework]:::boundary -->|requires| Req[Control Requirement<br/>e.g. DORA Art.15.3]:::data
    Req -->|mapped to| CC1[Control Card<br/>Auth & Access]:::data
    
    CC1 -->|implemented by| Pilot[Pilot API Gateway]:::service
    Pilot -->|enforces| mTLS[mTLS + OAuth2]:::critical
    mTLS -->|emits| Evid1[Auth Events<br/>(immutable)"]:::data
    
    CC1 -->|covered by| DLP[Data Loss<br/>Prevention Agent]:::service
    DLP -->|produces| Evid2[DLP Alerts<br/>(log stream)]:::data
    
    Evid1 & Evid2 -->|aggregated to| Sink[Evidence<br/>Data Lake]:::data
    Sink -->|exposed via| API[Evidence API<br/>/compliance/evidence]:::critical
    
    Regulator{{Auditor<br/>Queries API}}:::boundary -->|http GET| API
    API -->|returns JSON<br/>attestation]:::data
    
    classDef data data
    class Req,CC1,Evid1,Evid2,Sink,API data
    class Gov,Regulator,API boundary
    class Pilot,DLP,mTLS,API service
    class CC1,mTLS,API critical
```

**Diagram B — Compliance-by-design gate (highlighting critical = amber, decision = green, risk = red):**
```mermaid
flowchart TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef risk fill:#fecaca,stroke:#991b1b
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
    
    Dev[Developer<br/>Proposes Change]:::risk
    AutoScan[{Auto-Compliance<br/>Scan]}:::decision
    Policy[Policy-as-Code<br/>Evaluate]:::critical
    
    Dev -->|PR / MR| AutoScan
    AutoScan -->|check| Policy
    Policy -->|pass| Deploy[{Deploy to<br/>Staging]:::ok
    Policy -->|fail: new<br/>unmapped endpoint| Block[{Block<br/>Build]:::risk
    
    classDef ok fill:#a7f3d0,stroke:#065f46,stroke-width:1px
    classDev Dev
    class Block,Deploy Block
    class Policy critical
    class Dev risk
    class AutoScan,Deploy decision
```

## 5. Variants, options & trade-offs
| Variant | When to pick | When to avoid | Key trade-off axis |
|---------|--------------|---------------|--------------------|
| **Compliance-by-design (all gates)** | DORA-in scope, core banking, payments | Early M&A integration, green-field prototype | Rigor vs. time-to-market |
| **Compliance-by-design with documented exception** | Need to ship for a regulatory deadline | No compensating control exists | Risk of audit finding vs. launch date |
| **Audit-by-the-control (retroactive mapping)** | Legacy system with unknown dependencies | Any new regulated product | Speed vs. audit exposure |
| **Outsourced attestation** | Limited internal coverage | DORA 4-hour incident response; you still own the architecture | Cost vs. speed |

## 6. Relationships to sibling topics
- **Reference architecture:** the reference architecture *hosts* the control cards; compliance mapping is the *reason* the architecture exists in banks.
- **Standards:** standards are the *input* to compliance; DORA cites ISO 27001 and ISO 20000 as acceptable evidence.
- **Architectural principles:** principles like “data is owned by the domain” simplify compliance mapping because there is one consumer to audit.

## 7. Banking / financial-services context 💳
Dora (Digital Operational Resilience Act, UK CFT 6 & EEA) requires banks to conduct regular ICT risk assessments and maintain *documented, up-to-date* architecture artifacts. The EBA guidelines on ICT risk management explicitly reference ISO 20000, ISO 27001, and NIST 800-53. A bank launching a real-time payments platform must demonstrate:
- **Authentication & access control** (DORA ART.15.3)
- **Strong cryptography** (DORA ART.15.4)
- **Resilience & configuration management** (DORA ART.15.5)
- **Incident reporting** (DORA ART.15.8 — 4-hour initial, 24-hour detailed, 72-hour final)

The architecture must produce *runtime evidence* for each of these+}so that when the JRC (joint supervisory team) requests an attestation, the EA serves a queryable evidence API rather than a 200-page manual PDF.

## 8. Reference architecture / worked example
**Problem:** A UK retail bank needed to onboard 5 payment-gateway vendors for a faster-payments instant service. Each vendor had its own onboarding checklist; the bank’s risk team manually collected evidence, taking 6 weeks per vendor.

**Decision:** Build an evidence API backed by a compliance-by-design gateway. Every gateway is registered in the architecture catalog; every connector is auto-scanned against DORA, PCI-DSS, and SWIFT GSNcontrols.

**ADR:**
```markdown
# ADR-318: Compliance-by-design Gateway for Payment Onboarding
## Status
Accepted
## Context
5 payment-gateway vendors, 6-week manual onboarding, DORA attestation due Q2 2025, no machine-readable evidence pipeline.
## Decision
- Deploy a compliance gateway that enforces mTLS, rate-limiting, and OWASP ASVS Level 2 for every payment-gateway connection.
- Emit every enforcement decision to an immutable audit stream.
- Expose /compliance/evidence?vendor={id} as a REST API.
- Maintain control cards mapping DORA, PCI-DSS, and SWIFT GSN to architectural gates.
## Consequences
- Positive: onboarding reduced to 72 hours; JRC audit queryable in <5 minutes.
- Negative: initial gateway build: 8 sprints, €1.4M; requires platform team headcount.
- Negative: false positives on legacy non-contracted APIs cause blocking; requires a buffer-ADR process.
## Alternatives considered
1. Continue manual evidence collection. → Rejected: cannot meet Q2 DORA attestation.
2. Buy a third-party regtech platform. → Rejected: £2.1M/year, still requires manual vendor mapping.
```

## 9. Maturity & adoption signals
- **Adopt when:** you have >3 regulated systems, DORA in scope, or recurring audit findings from manual evidence gaps.
- **Anti-signals (don't adopt yet):** single unregulated product, no DORA/CFIUS exposure, board-level strategy shift making compliance secondary.
- **Common failure modes:** (1) building gates that block innovation without a buffer path; (2) making evidence too complex for auditors to query (they revert to manual); (3) no executive sponsor—compliance owners deprioritize runtime evidence.

## 10. Common confusions — the "don't mix" list
| Often confused | Real distinction |
|----------------|------------------|
| **Compliance vs Security** | Security is a capability; compliance is *alignment* with external requirements. |
| **Compliance vs Resilience** | Resilience is about failing gracefully; compliance is about *proving* you met requirements. |
| **Attestation vs Audit** | Attestation = a statement (we comply); audit = a test (someone else verifies you). |
| **Hard vs Soft compliance** | Hard = illegal to deviate; soft = contractual or market-driven. |
| **Evidence API vs Logs** | Logs are raw data; an evidence API is a *queryable, attested summary* with control-card linkage. |

## 11. Tools & standards to know
- **Standards/Frameworks:** DORA (EU/UK), Basel III (BIS), CRD V / CRR, NIST 800-53, ISO 27001, ISO 20000, PCI-DSS v4.1, PSD2, GDPR (Art. 32, 33), eIDAS, EBA Guidelines on ICT Outsourcing, FCA Consumer Duty, NYDFS 23-NYCRR 500.
- **Common tooling:** OPA/Rego (policy-as-code), HashiCorp Vault (secrets + audit logging), Splunk / ELK (evidence streaming), Jira Align / Confluence (control cards), OpenChain (supply-chain attestation), AWS Control Tower / Azure Policy (compliance guardrails), Wiz / Prisma Cloud (cloud compliance), CertPro (audit-trail management).
- **Mandatory reading:** DORA regulatory text (EU) / HM Treasury Extended Supervisory Framework (UK); “RegTech by Design” — Deloitte Financial Services; EBA Guidelines on ICT Risk Management (GL/2022/12).

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
1. **Recall:** define compliance-by-design in 2 minutes without notes, naming DORA or PCI-DSS.
2. **Model:** draw a control-card matrix mapping 3 regulatory clauses to 3 architectural components.
3. **ADR:** write a decision to block a build because a new vendor endpoint lacks mTLS; justify with DORA + PCI-DSS.
4. **Defend:** roleplay explaining to a non-technical CRO why a 6-week manual evidence collection process is unacceptable under DORA.

## 14. Summary (1 paragraph)
Compliance is no longer a checkbox exercise performed by lawyers on a static policy; under DORA and Basel-III, regulators demand *living, queryable, architecture-backed attestation*. Embedding controls at the point of design—through policy-as-code, immutable audit streams, and evidence APIs—reduces audit cost, eliminates manual evidence gaps, and makes the architecture itself a defensible statement of compliance. An architect who treats compliance as a post-launch add-on creates the regulatory worst-case: a system that is secure but unprovable, insured but uninsured, and launched but liable.
