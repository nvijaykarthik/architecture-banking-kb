# [C1-05] Architecture Artifacts & Documentation — BRIEF
> **Category:** C1 Foundations · **Difficulty:** ● foundational · **Banking-relevant:** yes
> **One-liner:** An *artifact* is anything that represents a decision, model, or standard (diagrams, ADRs, policy, ADR, survey, catalog) — without artifacts, architecture is consultative advice without enforceable evidence.
> **Why an EA cares:** Regulators and auditors *read* artifacts; if they don't exist, the architecture is invisible and non-defensible.

## Quick definition
Architecture artifacts are the *observable* and *traceable* outputs of EA: diagrams, models, decisions, policies, standards, and surveys. Documentation is not optional — it is *the enforcement mechanism* that makes architecture shared, reviewable, and audit-trackable.

## Key ideas / terms
- **Artifact:** any representation that matters to a stakeholder concern.
- **Document:** *when* and *why* it matters (versioned, owned, reviewed, reviewed-by, reviewed-when).
- **Lineage / traceability:** how one artifact references another (goal→capability→structure→system).
- **Minimal viable document (MVD):** the least artifact that delivers decision confidence.
- **Catalog:** curated, living artifact (skills, pipelines, tech standards, ADR index).

## The mental model
```mermaid
graph LR
    classDef artifact fill:#f1f5f9,stroke:#64748b
    classDef link fill:#c084fc,stroke:#a855f7
    Catalog[Catalog / MVD]:::artifact --links--> Decision[Decision record<br/>(architecture, non-financial)]:::artifact
    Catalog --links--> Board[Architecture decision board<br/>(CTO/BA-team)]:::artifact
    Decision --links--> AB[S/R decisions<br/>(AD/SD/AE)]:::artifact
    AB --links--> System[System / software artifact]:::artifact
    Decision --links--> Dev[Development team artifact]:::artifact
    class Asset Path critical
```
Decision → Business → System → Dev. MVD stops the unmaintainable "everything" document.

## When to use / when NOT to use
- ✅ **Use:** any funded/complianceable program; audits; M&A integrations.
- ⚠️ **Avoid:** writing a "master document" of every model ever produced without MVD discipline.
