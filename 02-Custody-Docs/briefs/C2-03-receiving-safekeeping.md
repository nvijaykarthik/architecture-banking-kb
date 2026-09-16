# [C2] Receiving and safekeeping assets — BRIEF
> **Category:** C2 Core Business Flows · **Difficulty:** ◑ · **Banking-relevant:** yes / 💳

> **One-liner:** Receiving and safekeeping is the process of capturing trade instructions, verifying title, crediting positions, and maintaining the perpetual record of who holds what.

> **Why an enterprise architect / trainee cares:** Safekeeping is the first point of failure in the custody chain. A delayed settlement, an incorrect corporate-action election, or a mis-credited GL reset will propagate through valuation, NAV, and reporting with a latency that makes remediation costly. The architect must treat safekeeping as a stateful, auditable ledger with real-time reconciliation.

## Quick definition
Receiving and safekeeping is the end-to-end processing of trade instructions, settlement confirmation, and position custody. It begins when an instruction arrives from the middle office or from an external trading desk and ends when the asset is credited to the client's account with a correct position, valuation, and entitlement trace.

## Key ideas / terms
- **Trade instruction:** The actionable message (buy, sell, transfer) received from a front-office system or a client portal.
- **Settlement date (value date):** The date on which legal title changes hands (T+0, T+1, T+2).
- **Position:** The legal entitlement to a quantity of an instrument, recorded in the custody ledger.
- **Sub-custodian:** The custodian who holds legal title on behalf of the bank.
- **Confirmation:** The exchange of trade details between transfer agent, CSD, and custodian to verify that the trade executed as agreed.
- **Reconciliation:** The daily comparison of the bank's book of record against the sub-custodian and CSD records to detect breaks.
- **Debit (hold):** A temporary reservation of cash or securities to cover a pending settlement.
- **Credit:** A permanent entry crediting an asset to a client account.

## The mental model
Receiving and safekeeping has three phases: **intake** (instructions and funds), **trade execution and confirmation**, and **position custody and reconcile**. At each phase, there is a state transition: submitted \u2192 verified \u2192 settled \u2192 credited. A break anywhere creates a downstream valuation error that can cascade into NAV misstatement and regulatory misreporting. The architect must design safekeeping as a synchronous, idempotent state machine with a checkpoint event after every credit.

## One diagram (mandatory)
```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    classDef risk fill:#fecaca,stroke:#991b1b,stroke-width:1px,color:#000
    SubSub[Trade instruction]:::context --> Verify[Verify & confirm]:::core
    Verify --> Settle[Settle (DVP/DvP)]:::risk
    Settle --> Credit[Credit client position]:::core
    Credit --> Reconcile[Reconcile with CSD]:::core
    Reconcile -->|Pass| Active[Active]:::context
    Reconcile -->|Fail| Break[Break: alert]:::risk
    class Settle risk
    class Credit critical
```

## When to use / when NOT to use
- ✅ **Use when:** Designing a new custody platform, evaluating a settlement-day exception process, or onboarding a new trade-type (e.g., crypto spot vs. securities spot).
- ⚠️ **Avoid when:** When the instruction is already confirmed and credited; use an amendment flow, not a full receive flow.

## Banking 💳 example
A Swiss wealth manager receives a trade instruction from a back-office convert: 5,000 shares of Novartis via CH-1 corporate action. In 2018, the convert trade instructions hit the settlement queue after the corporate-action deadline. The custodian had to reverse the convert and re-issue the dividend; the correction cost the manager €0.8m in carry and a regulatory fine for late customer communication. The bank later moved to real-time position-approval but the corporate-action gate remains the highest-risk interface.

## Common confusions (don't mix these up)
- **Receiving vs safekeeping:** Receiving is the active processing of instructions and credits; safekeeping is the perpetual state of holding and servicing the position after receipt.
- **Trade date vs settlement date:** Trade date is when the trade is agreed; value date is when title passes.

## Interview / recall prompt
"Walk me through receiving a trade from instruction to credited position."
- Instruction arrival, instruction validation, settlement, confirmation, credit, reconcile.
- DVP/DvP conventions (T+0, T+1, T+2).
- Debit/credit entries.
- Reconciliation: book vs. sub-custodian vs. CSD.
- Break response: alert, remediate, accept with justification.
- Common breaks: failed status, wrong status, corporate-action expiry.

## Status
☐ Not started · See detail doc: `details/C2-03-receiving-safekeeping.md`

---
**One diagram required. Both brief + detail must exist before ✓.**
