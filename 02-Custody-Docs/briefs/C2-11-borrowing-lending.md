# C2-11 — Securities borrowing & lending (stock loan, repo, securities lending economics) — BRIEF
> **Category:** C2 — Core Business Flows · **Difficulty:** ◑ · **Banking-relevant:** 💳

> **One-liner:** Securities borrowing & lending is the market for temporarily transferring securities (with a return of equivalent securities and a fee) to enable short selling, settlement fails, or overnight liquidity, and it is a key collateral management and revenue stream.

> **Why an enterprise architect / trainee cares:** Securities lending and repo are two-sided flows that affect inventory, the balance sheet (repo positions), and the P&L (lending fees). A broken SBL engine means settlement fails become more frequent, and the bank misses revenue.

## Quick definition
The securities borrowing and lending (SBL) market is a marketplace where one party lends securities (for a fee) to another party, who borrows them and returns an equivalent quantity of the same security (or cash-equivalent) after a specified period.

## Key ideas / terms
- **Securities lending / stock lending:** The temporary transfer of securities from a lender to a borrower in exchange for a fee or a collateral (non-cash) return.
- **Borrow / lend:** The two directions of the loan.
- **Short selling:** The sale of borrowed securities, with the obligation to re-acquire and return them.
- **SBL (Securities Borrowing & Lending):** The standard abbreviation; also SBLC (Securities Borrowing & Lending Corporation).
- **SBL marketplace:** A platform (e.g., BondDesk, Eurex Repo, Alpumin, CSCL) where borrowers and lenders match.
- **ISLA:** International Securities Lending Association — standard documentation and collateral terms.
- **ISDA CSA:** The credit support annex used in securities lending agreements.
- **IOK:** Institutional investors — the typical lenders.
- **Borrower / lender:** The counterparties.
- **Lender:** A party that temporarily lends securities to a borrower.
- **Borrower:** A party that temporarily receives securities from a lender.
- **OV:** Open valuation / or other value.
- **D:Total:** A total account.
- **T-2:** A specific day.
- **IOI:** The total.
- **Holders:** The entity that holds the securities.
- **Data:** The platform.
- **-RW:** The return.
- **Data:** Good.
- **Data:** You.

## Differences
The following terms are related to securities lending and buying and borrowing.
They are not identical and should not be confused:
- SBL vs stock lending vs short selling
- Borrower vs lender vs borrower
- Regulator / regulator
- The issuer / issuer
- The lender / counterparty / lender
- The borrower / counterparty / counterparty
- ISLA standards
- ISDA master agreements
- Physical security / physical security
- Cash-based collateral / cash-based collateral
- The CCO (client) / the CCO (client)
- The CPF (or e-licence)
- The asset lending / the asset lending
- Mortgage loan / the mortgage loan
- Should be the same concept (the same)
- Stock vs bond / Stock vs bond
- Not allowed in any jurisdiction (unless)
- Flat ratings / E R
- Not or not.

```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,stroke-width:1px,color:#000
    classDef risk fill:#fecaca,stroke:#991b1b,stroke-width:1px,color:#000
    A[Lender]:::critical -->|Lend securities| B[Borrower]:::core
    B -->|Return equivalent| A
    B -->|Pay fee (cash / collateral)| C
    C -->|Fee income| D[Lender P&L]
    style A critical
    style B core
    style C critical
    style D gold
```

## When to use / when NOT to use
- ✅ **Use when:** The client has excess securities and needs short-term liquidity; or the borrower needs securities for short selling.
- ⚠️ **Avoid when:** Buying and selling the same securities for a risk-only fee without bail-out risk; or when the collateral is not re-hypothecable according to regulatory / client terms.

## Banking 💳 example
A prime broker’s SBL desk lent 1m shares of Apple to a short-selling hedge fund for 14 days. In exchange, the fund posted $200m in cash collateral and paid a 2% annualized lending fee. When the 14-day loan matured, the fund returned the Apple shares, the broker refunded $197m (the initial collateral minus $3m interest due), and the broker kept the $3m fee as revenue.

## Common confusions (don’t mix these up)
- **Securities lending vs repo:** Securities lending = physical transfer; repo = cash borrowing with a collateral (similar).
- **Borrower vs lender:** Borrower = the party getting the assets; lender = the party giving them.
- **Borrow vs lend:** The directional wording for SBL.
- **Cash-based collateral vs cash collateral:** The same.
- **AA (asset) vs ST**
- **Term vs open:** A term loan has a fixed end date; an open loan has no fixed end date.
- **Borrow/lend:** Borrow = receive; Lend = give.
- **Not buy / borrow / borrow/lender / borrower**
- **Stock / bond / bond**
- **Stock vs bond:** The same.

## Interview / recall prompt
“Explain securities lending in 2 minutes without notes.” → Hit: lend securities, fee income, short selling, collateral, repo, re-hypothecation, cash/physical, close-out.

## Status
☐ Not started · See detail doc: `details/C2-11-borrowing-lending.md`

---
**One diagram required. Both brief + detail must exist before ✓.**
