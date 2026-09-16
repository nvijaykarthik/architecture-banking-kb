# [C2] NAV valuation — BRIEF
> **Category:** C2 Core Business Flows · **Difficulty:** ◑ · **Banking-relevant:** yes / 💳

> **One-liner:** NAV is the per-unit market value of an investment fund, calculated by aggregating portfolio assets, liabilities, accrued income, and expenses on a valuation date.

> **Why an enterprise architect / trainee cares:** NAV is the central truth source for fund valuation, client accounting, regulatory disclosure, and performance attribution. A NAV error propagates into client statements, fund prospectuses, and MiFID II disclosures. The architect must treat NAV as a single source of truth with immutable, versioned snapshots per valuation date.

## Quick definition
Net Asset Value (NAV) is the market value of a fund's assets minus its liabilities, divided by the number of outstanding units. For a fund of funds, it may be a weighted average of underlying fund NAVs. NAV is calculated at regular intervals (daily, monthly) and used for client accounting, performance reporting, and regulatory disclosure.

## Key ideas / terms
- **Asset value:** The market-value sum of all positions, accrued income, and pending revenue / expenses.
- **Accrued income:** The estimated value of income (dividends, interest) that is earned but not yet received.
- **Accrued expenses:** The estimated value of costs incurred but not yet paid (audit fees, management fees).
- **Settlement date:** The date on which a trade is settled and the position enters the book of record.
- **Valuation date:** The formula date used to calculate NAV; hundreds of these per day for global funds.
- **Closing NAV:** The NAV published at the end of the business day for public funds and fund of funds.
- **AuM weight:** The percentage of a fund's assets under management relative to a benchmark or peer group.
- **Holdings mismatch:** The difference between reported holdings and actual report holdings (e.g., repo, derivative netting, collateral shortfall).
- **Accrual:** The estimate of income / expense at valuation date; it is an accrual, not a cash event.
- **Valuation adjustment (adjust):** Any adjustment to market data (P&L, corporate-action adjustment, fee accrual).
- **Rebase:** The adjustment of a fund's NAV and return by a corporate-action factor (e.g., 2-for-1 split: NAV per unit halves, share count doubles).

## The mental model
NAV calculation is a feed-driven, snapshot process:
1. **Receive position and cash data** (from the custody engine or the valuation agent).
2. **Apply market-data adjustments** (corporate-action adjustment, fee accrual, currency translation).
3. **Calculate the sum of assets and liabilities.**
4. **Divide by outstanding units** (and apply the rebase/split factor).
5. **Publish the NAV** to client accounts, the fund administrator, and the regulator.

It is a **single source of truth** for fund valuations. The architect must treat NAV as a point-in-time snapshot, not a real-time stream.

## One diagram (mandatory)
```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    classDef money fill:#fde68a,stroke:#92400e,stroke-width:1px,color:#000
    Portfolio[Portfolio]:::critical --> Val[Valuation master]:::core
    Val -->|Apply CA, fees, adjustment]:::context
    Val -->|Apply P&L]:::money
    Val -->|Apply accrued income/expense]:::money
    Val --> Accruals[Accrued income/expense]:::money
    Accruals --> Total[(Total assets - liabilities)]:::critical
    Total --> NAV[NAV = (Total assets - liabilities) / Units]:::money
    Val -->|Rebase / split factor]:::money
    NAV -->|Publish]:::core
    class Total critical
```

## When to use / when NOT to use
- ✅ **Use when:** Designing a fund-valuation platform, evaluating a sub-custodian, or responding to a valuation-break
- ⚠️ **Avoid when:** The trade has not settled; use a "pending" or "unsettled" valuation, not a closing NAV

## Banking 💳 example
In 2019, a UK-based collective investment scheme (CIS) fund was valuing a US-listed bond but using stale market data due to a T+0 bond-market delay; the NAV was overstated by 0.07%. This triggered a client complaint to FOS, a regulatory review by FCA, and an advisory report submitted to the Scheme and the FOS. The bank had to restate the NAV and produce pre- and post-restatement prints. The root cause: the NAV and the valuation engine were using different market-data feeds.

## Common confusions (don't mix these up)
- **NAV vs. unit price:** NAV is the market value per unit at a valuation date; unit price is the price at which units are bought and sold (which may differ slightly due to bid-ask spread and subscription/redemption adjustments).
- **Market value vs. settlement value:** Market value is the current quoted price; settlement value is the price at which the trade will settle on the value date.
- **Closing NAV vs. intraday NAV:** Closing NAV is the end-of-day published value; intraday NAV is the mid-bullet or fair-value calculation; for mutual funds, only closing NAV is used for subscription and redemption.

## Interview / recall prompt
"Walk me through a NAV calculation."
- Sum assets (positions + accrued income), subtract liabilities (fees + expenses + accrued expenses), adjust for P&L, corporate actions, and currency translation, rebase for splits, and divide by outstanding units.
- Common break patterns: stale market data (uncorrected rebase), unsettled positions (trade-date vs. settlement-date), off-system accruals (not reflected in the NAV engine).
- For super/master funds, consider holdbacks, manager liquidity rules, and leverage wash

## Status
☐ Not started · See detail doc: `details/C2-07-nav-valuation.md`

---
**One diagram required. Both brief + detail must exist before ✓.**
