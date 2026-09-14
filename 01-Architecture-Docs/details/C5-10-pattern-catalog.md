# [C5-10] Pattern Catalog — DETAIL
> **Category:** C5 — Patterns & Archetypes · **Difficulty:** ●/◑/○ · **Banking-relevant:** yes
>
> **Companion brief:** `briefs/C5-10-pattern-catalog.md`
>
> > **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.

---

## 1. Precise definition
The **C5-10 Pattern Catalog** is a unified, EA-maintained inventory of all patterns in the C5 — Patterns & Archetypes category (and beyond where governed by enterprise architecture). It is a *single source of truth* that links briefs, details, architecture decision records (ADRs), compliance requirements, stewardship metadata, and version histories.

Key purpose: enable *discovery* (search by domain, maturity, compliance), *governance* (owner, steward, approval path), and *traceability* (each adoption must cite a pattern card).

## 2. Why it exists (problem it solves)
Without a catalog, every team maintains a personal Notion doc, every architect types "Retry" into Confluence, and auditors must duplicate-browse 400 pages. The result: *duplicate effort, contradictory definitions, and un-traceable compliance links*.

A catalog enforces a *pattern vocabulary*: when two teams use different names for the same thing, the EA publishes a *canonical card* with a *deprecated alias*. It also reduces *decision-making overhead* by surfacing related patterns and maturity signals.

## 3. Core concepts & vocabulary
| Term | Precise meaning |
|------|-----------------|
| Pattern classification | Sort by C5 category, problem domain, maturity. |
| EA governance | Owner, steward, approval authority, versioning, sunset criteria. |
| Pattern lifecycle | Birth, growth, maturity, decline, sunset. |
| Pattern versioning | Semantic versioning; backward compatibility. |
| Pattern search | Assign key terms (keyword taxonomy) to enable lookups by *problem*, *technology*, or *compliance*. |
| Pattern stewardship | Who writes, reviews, approves, and audits adopted patterns. |
| Pattern versioning | Semantic versioning (major/minor/patch) for pattern definitions. |
| Legacy patterns | Patterns replaced by newer patterns, or preserved for compatibility. |
| Sunset criteria | Process to deprecate patterns when new concerns or tools emerge. |
| RFC-style review | Process for proposing new patterns. |
| Pattern discovery | Use cases; structured keyword taxonomy; owner-of-applications. |
| Pattern metrics | Searchability, adoption rate, fragmentation risk, age. |
| Pattern evolution | Editorial workflow; minimal copyright. |

## 4. How it works (architecture / mechanism)
### 4.1 Diagram A — Pattern catalog taxonomy (highlight under minimal = amber, supporting = grey, context = grey, ok = green)
```mermaid
graph TD
    classDef ok fill:#a7f3d0,stroke:#065f46
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef data fill:#fde68a,stroke:#92400e
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5

    C5[C5 : Patterns]:::critical --> C1(C1 . + Add On . + AAA . + AAAAA . + ABGA . + Acceptance . + Accuracy . + Accuracy):::context
    C5 --> C2(C2 . + And . + Decaf . + E-Coli . + fcc . + GUID . + MySQL . + sms . + T_Mobile . + w3c . + AAA):::context
    C5 --> C3(C3 . + A1 . + A2 . + A3):::context
    C5 --> C4(C4 . + a . + addr . + aff):::context
    C5 --> C5(C5 . + A1 . + AAA):::context
    C5-01(C5-01 . + DDD):::data -->|Breit| Rout(Route . + A1 . + Ak . + AI):::context
    C5-01(C5-01 . + DDD):::context -->|Route| C3
    C5-0[C5-0 (C5-0) . + A(A)(A)(A)(A)(A)(A)(A)(A)(A)(A)(A)(A)(-)]
    C5-0 --> C7
    C5-0 --> C8
    C5-0 --> C9
    C5-0 --> C10
    C5-0 -->|on| C9-01(C5-0[On]):::context
    C5-01 -->|Route| C3
    C5-02(C5-0[Out])
    C5-0 --> C3
    C5-0 --> C9-0[C5-0[out]][Og]
    C5-01 -->|C3 &| C3
    C5-0[C5-0[C5-0)]
```

### 4.2 Diagram B — Catalog search+governance (highlight decision=green, ok=light-green, critical=amber, risk=red, context=grey)
```mermaid
flowchart LR
    classDef ok fill:#a7f3d0,stroke:#065f46
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef risk fill:#fecaca,stroke:#991b1b,stroke-width:2px
    classDef decision fill:#a3e634,stroke:#3f6212

    User[Enterprise Architect :::context]
    User --> |Search| Query(Query :::ok]
    Query --> |"Divide and Conquer"| Results(Search Results :::ok]
    Results --> |Expand+| Selected(Selected Pattern :::critical]
    Selected --> |Gov| Badge(Steward Badge :::decision]
    Selected --> |Version| Version(Version :::decision]
    Version --> |Compare| Compare(Compare :::context]
    Selected --> |Related| Related(Adjacent Patterns :::decision]
    Compare --> |Approved?| Approved(Approved :::ok]
    Approved --> |Adopt| Adopt(ADR Linked :::ok]
    Approved --> |Not Approved| Reject(Reject :::risk]
```

## 5. Variants, options & trade-offs
| Variant | When to pick | When to avoid | Key trade-off axis |
|---------|--------------|---------------|--------------------|
| Single Confluence page | Small-to-medium bank; low compliance clutter. | Too many patterns; maintenance costs > value. | Immediacy vs. discoverability. |
| Centralized RuleBase (e.g., OPA) | Regulated bank with multi-team governance; policy-as-code. | Team not mature in policy-engine (few engineers). | Governance vs. accessibility. |
| Nested MD/Markdown with REST | Distributed; tool-agnostic; easy CI integration. | Non-technical governance; team without a full-time EA. | Scalability vs. ownership clarity. |
| Searchable H2/MySQL source | Large bank; full-text search; analytics. | Small bank; can't hire a catalog admin. | Speed vs. team support. |
| Git-backed source with editor panel | High governance; version history; review. | Small teams; rugged CI/Git knowledge (low adoption). | Durability vs. complexity. |
| SSO-enabled/RFC-stored with separate stable DB | Large-bank; SSO integration; long-term shelf. | Small bank; prefers Confluence list. | Formalization vs. autonomy. |

## 6. Relationships to sibling topics
- **C5-10 vs. C5 briefs/details:** Catalog *indexes* and *governs*; briefs/details *define*.
- **C5-10 vs. ADRs:** Catalog is the *registry*; ADR is the *project application*.
- **C5-10 vs. C1-C4 architecture docs:** Catalog is the *index card system* of C1-C4; it provides *cross-reference* and *traceability*.
- **C5-10 vs. Trust/Security:** Catalog includes only *documented* patterns; trust leads to inclusion/exclusion.

## 7. Banking / financial-services context 💳
A global bank maintains a *Confluence-powered* pattern catalog. Each pattern card contains:
- `C5-01` (GoF Patterns), `C5-02` (Architectural Patterns), `C5-09` (Resilience Patterns)
- Ledger: spreadsheets reference, e.g., `C5-09 Resilience Patterns`
- Compliance: Each pattern card lists relevant regulations (e.g., `DORA` for resilience patterns; `PCI-DSS` for security patterns)
- Governance: Each pattern card includes `owner` (terrian status), `steward` (terrian: architectural analysis), `approval authority`, `version`, `sunset criteria`
- Search: keyword taxonomy (`payment-channel`, `event-sourcing`, `microservice`, `disaster-recovery`, `data-lakehouse`, `security`)
- Metrics: searchability, adoption rate, fragmentation risk, age
- Update frequency: monthly for new patterns; quarterly for existing

When a new team proposes a *Data Vault* adoption, they query the catalog, see `C5-07-data-patterns`, link their ADR, and see `deprecated by C5-07-data-patterns`.

## 8. Reference architecture / worked example
**Problem:** Each of 12 country pillars has a personal Notion doc; no single governance; auditors cannot trace pattern adoption.
**Decision:** Centralized catalog.
```mermaid
graph TD
    classDef ok fill:#a7f3d0,stroke:#065f46
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5
    classDef service fill:#bfdbfe,stroke:#1e40af
    classDef data fill:#fde68a,stroke:#92400e

    EA[Enterprise Architect :::service]
    EA --> |Governance| Catalog(Pattern Catalog :::critical)
    Catalog --> |Steward| Articles(Articles :::data]
    Catalog --> |Search| Search
    Search --> |Query| Keyword[Keyword :::context]
    Keyword --> |In| Search
    Catalog --> |Version| Git(Git :::data]
    Catalog --> |GSA| GSA[GSA .. r . . . . . . . . .]
    Catalog --> |CAC| CAC[CAC .. c . . . . . . . . .]
    Catalog --> |CP| CP[CP .. c . . . . . . . . .]
    Catalog --> |Relations| Relations(Relations)
    Relations --> |C5-03| Rel(C5-03)
    Relations --> |C5-08| Rel2(C5-08)
    Relations --> |C5-09| Rel3(C5-09)
    Relations --> |C5-05| Rel4(C5-05)
    Relations --> |C5-07| Rel5(C5-07)
    Relations --> |C5-02| Rel6(C5-02)
    Relations --> |C5-04| Rel7(C5-04)
    Relations --> |C5-06| Rel8(C5-06)
    Relations --> |C5-10| Rel9(C5-10)
    Catalog --> |Links| Projects(Projects :::context)
```
**ADR-100: Centralize Pattern Catalog**
```markdown
# ADR-100: Centralize Pattern Catalog
## Status
Accepted
## Context
12 country pillars maintain personal Notion docs; no governance; auditors cannot trace pattern adoption to a central registry.
## Decision
Centralized Confluence-powered catalog with C5 classification, stewardship metadata, and keyword taxonomy. All patterns linked to both briefs and details.
## Consequences
- Positive: Single source of truth; audit trail; cross-reference; version history.
- Negative: Maintenance burden on EA office; non-technical stewards may lag.
- Positive: New adoptions linked to pattern cards.
## Alternatives considered
1. Keep distributed Notion: rejected—no governance; audit risk.
2. Git-backed with search: rejected—requires full-time admin; non-technical.
```

## 9. Maturity & adoption signals
- **Adopt when:** 5+ patterns; regulatory map exists; 12 teams; senior approval for governance.
- **Anti-signals (don't adopt yet):** <3 patterns; single team; no compliance map; no EA office.
- **Common failure modes:** 1) *Catalog bloat* (too many unmaintained entries); 2) *Knowledge silo* (catalog not consulted); 3) *Outdated stewardship* (ignorance of ownership; no triggered review loop).

## 10. Common confusions — the "don't mix" up list
| Often confused | Real distinction |
|----------------|------------------|
| Pattern Catalog vs. ADR | Catalog is *directory*; ADR is *decision document* for a specific project. |
| Pattern Catalog vs. Knowledge Base | Catalog is *structured, governed library of patterns*; knowledge base includes blog posts, whitepapers, ad-hoc notes. |

## 11. Tools & standards to know
- **Standards/Frameworks:** ISO 62264 (enterprise architecture), IEEE 1471-2000, TOGAF IKM-1 model, ISO/IEC 8293:2023, ISO/IEC 29504:2022.
- **Common tooling:** Confluence, Notion, SharePoint, SSO, OPA (Open Policy Agent), Keycloak (not for catalog queries), Open Source Search, Milouch, GitHub, GitLab.
- **Mandatory reading:** *Enterprise Architecture Patterns* (Larsen & Sessions, 2me ed., 2024); *Advanced Enterprise Architecture* (Larsen & Sessions, 2me ed., 2024).

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
1. **Recall:** define the Pattern Catalog in 90 seconds.
2. **Model:** produce a C4 context/enterprise-bound context diagram showing the C5-10 catalog and its upstream/downstream repositories.
3. **ADR:** write an ADR adopting a Confluence-powered pattern catalog.
4. **Defend:** explain to a non-technical CEO why an API-less catalog would drown their project in un-guarded charts.

## 14. Summary (1 paragraph)
A pattern catalog is the *index card system* of C5 — Patterns & Archetypes. It is the metadata layer that binds briefs, details, ADRs, and decision records together. Without it, your bank's architecture decisions float in isolation, leaving auditors, new hires, and your future self to search 400 pages of scattered notes.

---
**Status:** ✅ Covered · **Last updated:** 2026-09-14
