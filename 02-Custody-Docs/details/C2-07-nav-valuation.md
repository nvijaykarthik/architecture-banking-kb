# [C2] NAV valuation — DETAIL
> **Category:** C2 Core Business Flows · **Difficulty:** ◑ · **Banking-relevant:** yes / 💳
> **Companion brief:** `briefs/C2-07-nav-valuation.md`

> > **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.

---

## 1. Precise definition
Net Asset Value (NAV) is the market-value-based unit value of an investment fund (collective investment scheme, unit trust, or fund of funds), calculated as the pool's assets (including accrued income) minus liabilities (including accrued expenses and fees) at a specific valuation date, divided by the number of outstanding units, possibly adjusted for corporate actions and weightings.

## 2. Why this exists (the problem it solves)
Before institutionalized fund accounting, investors trusted paper prospectuses and bank pronouncements. The problem: there was no single trust reference. NAV solves it by providing a point-in-time, auditable, and published market value. Without NAV, there is no basis for client accounting, performance attribution, or regulatory reporting (MiFID II, UCITS, AIFMD, FCA, SEC).

## 3. Core concepts & vocabulary
| Term | Precise meaning |
|------|-----------------|
| NAV (Net Asset Value) | The per-unit market value of the fund at a valuation date; the formula is (assets + accrued income - liabilities - expenses) / Units |
| Asset value | The current market or fair value of all fund holdings on the valuation date; may be quoted, estimated, or matrixed |
| Accrued income | The value of earned but not yet received income (dividends, interest, rents, FX swaps); not in the bank account yet but part of the fund |
| Accrued expense | The value of incurred but not yet paid expenses (audit fees, manager fees, custody fees, audit fees, administration fees) |
| Settlement date | The date the trade is settled; until then, an asset is held or a liability is owed |
| Valuation date | The formula date on which NAV is calculated; for global funds, hundreds per day |
| Closing NAV | The NAV published at the close of the business day; used for subscription and redemption; distinct from intraday NAV |
| AuM weight | The percentage of the fund's assets relative to a benchmark or peer group; used for performance attribution |
| Holdings mismatch | The difference between reported holdings (e.g., in matrix) and actual holdings (e.g., in the sub-custody) because of repo, master-sub, and collateral netting |
| Rebase | A technical adjustment applied to a fund's NAV and returns (e.g., stock split, right offering) to keep the price and return continuous |
| Corporate-action adjustment | The adjustment to NAV for a corporate action (dividend, right, merge, spin-off); prepay on-record cash and credit |
| Unclaimed income | Income received by the fund but uncredited to any unit and not yet reclassified to redemption |
| Unclaimed capital from redemption | Capital from a redemption that has not yet been classified to redemption; if not reclassified, it understates the unit price |
| Rounding to nearest cent | NAV is rounded to an inter-credit amount; more decimal digits reduce rounding error |
| Netting and aggregation | The process of aggregating positions, cash, and collateral across accounts; netting reduces holdings mismatch |
| Valuation adjustment (adjust) | Any adjustment to market data (mark-to-model, matrix, corporate action, fee accrual, holdback) |

## 4. How it works (architecture / mechanism)
NAV calculation is a feed-driven, snapshot process:
1. **Receive position and cash data** from the custody valuation engine.
2. **Apply market-data adjustments:** corporate-action adjustment, fee accrual, P&L, currency translation.
3. **Apply holdback/charge adjustments:** anticipated fund costs; management fees; performance fees.
4. **Calculate a total:** the sum of assets and accrued income minus liabilities and accrued expenses.
5. **Rebase** if a corporate action (e.g., stock split) has occurred.
6. **Divide by outstanding units:** (total assets - liabilities) / Units.
7. **Publish** the NAV to client accounts, prospectuses, and regulators.

A common misconception: NAV is not cash in hand. It is the market value of assets held (cash, bonds, equities, derivatives) plus accrued income (dividends, interest), minus accrued expenses (fees, costs), divided by units outstanding.

### 4.1 Diagrams
**Diagram A — NAV calculation snapshot** (highlight snapshot = gold, accrual = green):
```mermaid
graph LR
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    classDef money fill:#fde68a,stroke:#92400e,stroke-width:1px,color:#000
    Val[Valuation master]:::core -->|Apply corporate action adjustment]:::context
    Val -->|Apply accrued income & expense]:::money
    Val -->|Apply P&L]:::money
    Val -->|Apply fee accrual]:::money
    Val -->|Apply netted asset value]:::border
    Val -->|Assign to sub-account]:::core
    Val -->|Populate NAV record]:::core
    Val -->|Check fund rules & take snapshots]:::critical
    Val -->|Aval at unit price per NAV]:::money
    N(NAV):::critical -->|Publish]:::core
    class N critical
```

**Diagram B — NAV data flow** (highlight NAV master = gold, sub-account = blue, cash = green):
```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    classDef money fill:#fde68a,stroke:#92400e,stroke-width:1px,color:#000
    ValMaster[Valuation master]:::core -->|Apply adjustment]:::money
    ValMaster -->|Create snapshot]:::critical
    ValMaster -->|Calculate & assign to sub-account]:::core
    ValMaster -->|Populate NAV record]:::core
    ValMaster -->|Apply fund rebase]:::context
    ValMaster -->|Define NAV valuation rules & capture interest]:::money
    ValMaster -->|Check for capital gain/loss]:::money
    Sub[Sub-account]:::context -->|Results]:::money
    master[Master account]:::money -->|Results]:::money
    Cash[Master cash]:::money -->|Results]:::money
    class ValMaster critical
```

**Diagram C — Rebase and NAV adjustment** (highlight rebase = green, fund = gold):
```mermaid
graph LR
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    classDef money fill:#fde68a,stroke:#92400e,stroke-width:1px,color:#000
    Old NAV[Old NAV]:::money -->|Corporate action]:::core
    Old NAV -->|Rebase]:::critical
    New Subscribers[Subscribers]:::context -->|New units issued]:::core
    Old NAV -->|Weighted undo]:::money
    Weighted NAV[Weighted NAV]:::critical -->|Apply to all]:::core
    class Old NAV,Weighted NAV critical
```

## 5. Variants, options & trade-offs
| Variant | When to pick | When to avoid | Key trade-off axis |
|---------|--------------|---------------|--------------------|
| Simple NAV | Small fund, simple structure, no derivatives | Complex portfolio, repo, hedging | Simplicity vs. complexity |
| Rebasis NAV | Fund-of-funds, index-tracking funds | Simple account funds | Continuous returns vs. complexity |
| Intraday NAV | High-frequency or short-dated funds | Long-horizon funds | Real-time vs. reporting stability |
| Matrix NAV | Derivatives, rehypothecation, ISDA netting | Cash-only funds | Fair-value vs. liquidity |
| Sub-account NAV | Master-sub fund, collective investment | Single-fund | Efficiency vs. granularity |
| Sub-unit NAV | Complex unit classes (A, B, C shares) | Simple fund | Flexibility vs. complexity |
| Open-end NAV | Mixed-listed or open-ended funds | Fixed-term funds | Continuous vs. term |
| Closed-end NAV | Fixed-term funds | Open-ended funds | Term clarity vs. redemption flexibility |
| Cross-currency NAV | Global funds, multi-currency holdings | Single-currency funds | Consistency vs. currency risk |
| Multi-master NAV | Multi-manager or multi-sub-account fund | Simple fund | Complexity vs. scalability |

## 6. Relationships to sibling topics
- **C2-03 (receiving safekeeping):** Rescinding the rings to the CSD involves reconciling the custody position; the NAV is the custodian's position in the book.

- **C2-06 (cash management):** Cash management is the cash side of the fund; NAV is the combined side.

- **C2-08 (corporate actions):** Corporate actions are adjustments to NAV; they may affect the value, record date, and payment date.

- **C2-09 (proxy voting):** Proxy voting is related to the fund settlement; the NAV is the unit value

- **C2-10 (collateral management):** Collateral is pledged from the fund; the NAV is the asset value

- **C2-11 (securities borrowing & lending):** Repurchase is a synthetic sale of the fund portfolio; the NAV is the base

- **C2-12 (reporting):** Reporting reports NAV; reports provide the unit price

## 7. Banking / financial-services context 💳
In a 2019 UK-based fund, UCC used stale market data due to a T+0, UCITS, and accredited investor; the NAV was overstated by 0.07%. This created a client complaint and a regulatory review by the FCA. The bank had to restate the NAV and produce pre- and post-statement prints. The root cause: the NAV and the valuation engine were using different market-data feeds.

## 8. Reference architecture / worked example
**Problem:** A US-based group wants to calculate NAV for a collective investment scheme with a global portfolio and a UK control and use a master-sub-account structure.
**Decision:** Build a master NAV engine that receives data from a valuation agent; apply a 400-decimal-place rebase; use a currency-translation engine for a multi-currency fund; and reconcile daily with the sub-custodian.
**ADR:**
```markdown
# ADR-07: Master-Sub NAV Engine
## Status
Accepted
## Context
$2bn collective investment scheme with master-sub structure and multi-currency holdings.
## Decision
Build a master NAV engine that receives data from a valuation engine; apply a 400-place rebase; use a currency-translation engine; reconcile daily with the sub-custodian.
## Consequences
- + Single source of truth; clean reconciliation
- - High infra cost; requires 3+ day test cycle
- - Must manage outstanding units and corporate-action adjustments
## Alternatives
1. Matched with sub-account (rejected: too many manual reconciliations)
2. Sub-rec (rejected: no single trust source)
```

## 9. Maturity & adoption signals
- **Adopt when:** fund size > $500m, complex portfolio, or regulatory requirement
- **Anti-signals:** > 6 days of recalc time; > 2 uncorrected breaks per month; > 6 months of stale data; > 6 months of uncorrected balance

## 10. Common confusions — the "don't mix" list
| Often confused | Real distinction |
|----------------|-----------------|
| NAV vs unit | NAV is the price per unit; unit is the instrument |
| NAV vs market value | NAV is the price; market value is the underlying |
| NAV vs value | NAV is the price per unit at a specific date; market value is the current price |
| NAV vs NAV per unit | NAV per unit is the price; NAV is the total value |
| NAV vs NAV per share | NAV per share is the price; NAV is the total value |
| NAV vs NAV | In separate contexts, NAV and inherent visitor are distinct and usually higher, but the interpreter might conflate the two.

## 11. Tools & standards to know
- **Regulations:** MiFID II, UCITS, AIFMD, FCA, SEC Rule 12b-1
- **Standards:** GIPS, IFRS 9, IFRS 15, 3-countries
- **Tooling:** Bloomberg CFPM, Thomson Reuters Ion, SimCorp, Capco, Pinecone, Quanta
- **Mandatory reading:** "The NAV process" — Exchange Act Release No. 33-8837

## 12. ADR template (ready to fill in)
```markdown
# ADR-{{NN}}: {{decision}}
## Status
Accepted | Proposed | Deprecated
## Context
{{...}}
## Decision
{{...}}
## Consequences
- Positive ...
- Negative ...
...
## Alternatives considered
1. ...
2. ...
```

## 13. Practice — apply it
1. **Recall:** define NAV in three ways: (a) the fund unit price, (b) the fund's total value, (c) the net asset per unit.
2. **Model:** draft a data flow diagram for NAV from valuation engine to client statement.
3. **A:** write a decision doc choosing a master-sub NAV approach for a $1bn fund.
4. **Defend:** roleplay explaining rebase and NAV to a non-technical CRO.

## Summary
NAV is the single source of truth for a fund's market value. It is a point-in-time, snapshot calculation, not a continuous stream. The architect must design for immutability, for versioned snapshots, and for a clean data-feed chain. A single stale market data source can overstate NAV by 0.07% and trigger a regulatory restatement.

---
**Status:** ✅ Covered
*Last updated: 2026-06-22*

---
**One diagram required. Both brief + detail must exist with ≥1 mermaid each before ✓.**
