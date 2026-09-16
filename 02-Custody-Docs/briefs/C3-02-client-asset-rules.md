# [C3] Client asset rules: segregation, ownership, rehypothecation limits — BRIEF

> **Category:** C3 Regulatory, Risk & Compliance · **Difficulty:** ◑ · **Banking-relevant:** yes / 💳

> **One-liner:** Client asset rules are the regulatory obligations that segregate client assets from house assets, clarify legal and beneficial ownership, and cap rehypothecation to protect clients in custodian bankruptcy.

> **Why an enterprise architect / trainee cares:** Every custody architecture decision — account structure, data model, settlement engine — must prove segregation and enforce rehypothecation caps. A design that looks efficient on paper can collapse into £400M in unsettled claims.

## Quick definition
Client asset rules require the bank to hold client assets separately from its own, define who legally owns what (CSD vs internal ledger), and limit how much can be rehypothecated to a hard percentage (140% in EU under CSDR).

## Key ideas / terms
- **Segregation:** Client assets kept in a separate ledger/legal identity from house assets.
- **Legal ownership:** Name on the CSD account; decides who directs the CSD (CSDR).
- **Beneficial ownership:** The client who funded the assets; protected by fiduciary duty.
- **Rehypothecation cap:** EU limit is 140% of client assets; US has no numeric cap but requires daily reserve compliance (140% by calculation).
- **Book-and-claim:** Omnibus structure where legal title is to the custodian but beneficial title is client-specific.
- **LOU:** Letter of Understanding linking legal and beneficial ownership across jurisdictions.

## The mental model
Think of client assets as **two buckets** running in parallel:
1. **Legal-title bucket** (CSD): who can press the button to sell/move the asset.
2. **Beneficial-title bucket** (internal ledger): who owns the economic claim.

Rehypothecation is the *spill* from the beneficial bucket into the CCP/bank-funding pool — capped by law.

## One diagram (mandatory)
```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    A[Client assets]:::critical --> B[House assets (closed)]:::core
    A --> C[Client sub-accounts]:::critical
    C --> D[Legal title: CSD]:::critical
    C --> E[Beneficial title: client]:::core
    F[Rehypothecation cap]:::context --> G[CCP / Bank funding]
```

## When to use / when NOT to use
- ✅ **Use when:** Designing account structures, CSD linkages, or collateral engines.
- ⚠️ **Avoid when:** Assuming omnibus = client-safe; it is efficient but adds traceability risk.

## Banking example
**BNP Paribas** holds legal title in Clearstream for French retail nominee accounts but beneficial title in its own internal ledger. When a shareholder wants to pledge the asset, the LOU must specify whether the pledge attaches to legal or beneficial title — a common source of ambiguity.

## Common confusions
- **Book-and-claim vs segregated:** Book-and-claim = legal title to custodian; segregated = legal title per identifiable client.
- **Legal vs beneficial:** Legal = CSD record; beneficial = client's enforceable claim.
- **Rehypothecation vs pledge:** Rehypothecation = custodian uses client collateral for its own needs; pledge = direct security interest.

## Interview / recall prompt
- "What is the EU rehypothecation cap and where is it codified?"
- "Why does a US custodian use a reserve formula instead of a legal-title regime?"
- "What is the LOU and why is it the weak link in book-and-claim structures?"

## Status
☐ Not started · See detail doc: `details/C3-02-client-asset-rules.md`

---
**One diagram required. Both brief + detail must exist before ✓.**
