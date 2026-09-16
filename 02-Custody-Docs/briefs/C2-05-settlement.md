# [C2] Settlement: cash and securities — BRIEF
> **Category:** C2 Core Business Flows · **Difficulty:** ◑ · **Banking-relevant:** yes / 💳

> **One-liner:** Settlement is the simultaneous or sequential exchange of cash and securities by means of value-dated payment and transfer to finality (or not), governed by DVP or DvP conventions and trade cut-offs.

> **Why an enterprise architect / trainee cares:** Settlement is where settlement risk is born. The architect must design for finality, for DVP/DvP choices, and for cut-off awareness. A missed cut-off because of batch latency is a financial-loss event.

## Quick definition
Settlement is the final step of a trade, where cash is moved to the seller and securities (or a corresponding amount of currency) is transferred to the buyer according to a pre-agreed value-dated DVP or DvP convention. It is the point at which settlement risk is minimized (but not eliminated).

## Key ideas / terms
- **DVP (Delivery versus Payment):** Cash and securities move simultaneously, simultaneously or with minimal delivery delay; reduces herding and fraud risk.
- **DvP (Delivery versus Value):** Securities move first; cash/value completes at a later date; allows for delivery-before-cash, which can be riskier for the counterparty.
- **Trade cut-off:** The deadline by which a trade must be submitted to the settlement system to meet the value date; missing the cut-off means settlement shifts to the next value date.
- **Value date / effective date:** The calendar date on which the trade is legally effective and settled; T+0, T+1, or T+2.
- **Finality:** The point at which a transfer of title or payment cannot be reversed; e.g., funds are debited from a bank account and released.
- **Settlement risk / Herstatt risk:** The risk that one party pays but does not receive the corresponding asset because of a time-zone or liquidity delay.
- **Pay-in:** The first-time introduction of reserves required; used for securities, margins, or other assets.
- **Buy-in / sell-in:** Short-term repurchase/sale of assets to close a trade that has failed to settle after a pre-agreed period.
- **Schemes:** OTP-II (offline, with central counterparty), OTP-I (online), and T2S.
- **Maturity date:** The date on which a security's term ends and proceeds are generated.
- **Transfer condition:** A condition that must be fulfilled for a transfer to be executed; e.g., both cash and securities must be available before settlement.
- **Standard Settlement Instructions (SSI):** Pre-agreed parameters (BIC, account numbers, address, specimen signatures) that allow the CSD to execute settlements without repeating bilateral checks.
- **Payment instruction:** The cash component of a DVP, sent through an e-money scheme or fed through a TARGET2 gross settlement system.
- **Instruction:** The securities component of a DVP or DvP.
- **Qualifying transaction:** The securities-position update chain in T2S that identifies all holders and their movements.

## The mental model
Settlement sits at the boundary of two systems: the securities settlement system (for securities flow) and the funds / e-money scheme (for cash flow). Finality is the critical output: a successful settlement is one where both legs are confirmed and released. A missed trade cut-off is the most common single error, and it is a latency, not a corruption, bug.

## One diagram (mandatory)
```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    classDef risk fill:#fecaca,stroke:#991b1b,stroke-width:1px,color:#000
    Trade[Trade instruction]:::context --> Cut[Cut-off]:::critical
    Cut -->|Pass| Settlement[Settlement (DVP/DvP)]:::core
    Settlement -->|Fail| Pay[Pay-in (UI)]:::risk
    Settlement -->|Success| Credit[Credit positions]:::core
    Settlement -->|Cash| Transfer[(Cash transfer)]:::context
    Pay -->|Success| Credit
    Pay -->|Fail| Destroy[Destroy]:::risk
    class Cut critical
    class Settlement risk
```

## When to use / when NOT to use
- ✅ **Use when:** Designing a settlement, evaluating T+1 or T+0 migration, or responding to a settlement failure.
- ⚠️ **Avoid when:** When the trade is already settled; use a reversal flow only if the reversal window is open.

## Banking 💳 example
A German bank instructs a €20m equity purchase via DTCC; the cut-off is 16:00 ET, but the trade is submitted to the bank's matching engine at 15:47 with a 7-hour batch window, and a reconciliation bug delays the federal register update. The trade misses the DTCC cut-off and settles T+2 instead of T+1, costing €240k in carry. The root cause was a 7-hour batch window, not a trade instruction error.

## Common confusions (don't mix these up)
- **DVP vs DvP:** DVP = simultaneous exchange; DvP = delivery first, cash later.
- **Trade cut-off vs value date:** Trade cut-off is the submission deadline; value date is the settlement date.
- **Settlement vs mutual:** Settlement is the title transfer; mutual is a process-around-settlement.
- **Pay-in vs settlement:** Pay-in is the first-time introduction of reserves; settlement is the exchange of cash and securities.

## Interview / recall prompt
"Explain DVP and DvP and why settlement risk exists."
- DVP = delivery versus payment: simultaneous exchange reduces settlement risk.
- DvP = delivery versus value: delivery first, cash later; higher risk.
- Settlement risk = herstatt risk: one party pays but does not receive.
- CUT-OFF deadline.
- Time-zone and liquidity windows are the dominant failure mode.
- Buy-in / sell-in = backstop for failed settlement.
- T+0 / T+1 / T+2 conventions.
- Payment instruction = cash; instruction = securities.
- Finality = point-of-no-return.

## Status
☐ Not started · See detail doc: `details/C2-05-settlement.md`

---
**One diagram required. Both brief + detail must exist before ✓.**
