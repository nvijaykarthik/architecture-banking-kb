# C5-04 Benchmark Fees — BRIEF
> **Category:** C5 — Custody Economics · **Difficulty:** ○ / **Banking-relevant:** yes 💳

> **One-liner:** Benchmark fees are variable custody charges pegged to the complexity of stewardship activities, separated from flat asset-based management or performance fees.

> **Why an enterprise architect / trainee cares:** If you conflate benchmark fees with management fees, you misprice the asset-servicing P&L and misalign vendor incentives. Banks need precise fee disclosure instruments to meet MiFID II transparency and to avoid cross-subsidizing regulation.

## Quick definition
Benchmark fees are recurring, performance-neutral charges paid by asset managers to custodians for discrete stewardship deliverables — e.g., bespoke index replication, physical share lending, or regulatory reporting. They sit outside the standard percentage-of-assets-under-custody (PAUC) model and the performance-fee waterfall.

## Key ideas / terms
- **Benchmark fee:** A fixed or formulaic charge linked to a specific deliverable or responsibility, not to assets under custody.
- **PAUC (Percentage of Assets Under Custody):** The flat, overhead-based custodial charge. Benchmark fees are additive on top.
- **Performance fee:** A share of investment returns; benchmark fees are *not* performance-linked.
- **Unbundling (MiFID II):** Separating execution, custody, and advisory cost components for client disclosure.

## The mental model
Benchmark fees answer the question: "What does it cost to do *this specific thing*?" They are scoped deliverables — think of them as SaaS line-item pricing inside a broader custody relationship. A bank must track them independently in the ledger because they are tax-sensitive, regulatorily disclosed, and often negotiated separately from the master custody agreement.

## One diagram (mandatory)
```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    A[Custody Agreement]:::context --> B[PAUC (flat%):::core]
    A --> C[Benchmark Fees:::critical]
    A --> D[Performance Fees:::core]
    C --> E[Index Benchmarking]:::context
    C --> F[Physical Lending]:::context
    B --> G[Asset Sub-custody]:::context
```
```

## When to use / when NOT to use
- ✅ **Use when:** pricing a new custody line or unbundling cost for a client mandate.
- ⚠️ **Avoid when:** calculating net fund return or gross-to-net performance — the number must exclude benchmark fees, which are a service cost, not a return drag.

## Banking example
Citibank charges a 25 bps PAUC on a UK equity fund, plus a 10 bps benchmark fee for physical share lending and a 15 bps bespoke tracking-error optimization fee. Under MiFID II, the wrapper must show the client: (1) 25 bps PAUC as custody cost, (2) 10 bps lending fee as a separate line, and (3) 15 bps as an extra service — not lumped into a single "custody cost."

## Common confusions (don't mix these up)
- **Benchmark fee** vs **management fee:** Benchmarks are fulfillment charges; management fees are compensation for investment decisions.
- **Benchmark fee** vs **performance fee:** Benchmarks are fixed/formulaic deliverables; performance fees ride on returns.

## Interview / recall prompt
"Explain benchmark fees in 2 minutes without notes."
- Charges are additive, not substitutive, to PAUC.
- They must be disclosed as a separate cost item under MiFID II unbundling.
- They are not linked to portfolio performance; they are linked to scope of service.
- They can be named-rate or formulaic (e.g., per million dollars lent).
- They require separate contract language from the UCITS custody agreement.

## Status
☐ Not started · See detail doc: `details/C5-04-benchmark-fees.md`

---
**One diagram required. Both brief + detail must exist before ✓.**
