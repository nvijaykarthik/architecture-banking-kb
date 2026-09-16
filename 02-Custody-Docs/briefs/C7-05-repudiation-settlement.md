# C7-05 Repudiation Settlement — BRIEF
> **Category:** C7 — Controls · **Difficulty:** ◑ vs ◑ • **Banking-relevant:** yes / 💳

> **One-liner:** _Repudiation settlement is the commercial and legal recovery process a custodian uses when a counterparty denies a matched trade, turning a settlement failure into a forensic, collateralized, and ultimately court-enforced outcome._

> **Why an enterprise architect / trainee cares:** _If you do not understand repudiation settlement, you cannot model the custody balance-sheet risk; counterparties will deny matched trades, leaving uncollateralized margin deficits that hit capital ratios. You need to distinguish this from a break—breaks are operational mismatches, repudiation is a legal / commercial disagreement._

## Quick definition
Repudiation settlement (also called reject or dispute settlement) is the post-match commercial process by which a custodian calls for the return of collateral / delivery of securities when a counterparty denies a trade or settlement instruction that the custodian's systems believe is confirmed. It includes demand letters, legal escalation, credit-committee moratorium, and final court-enforced recovery.

## Key ideas / terms
- **Repudiation / reject:** A counterparty's refusal to honor a matched trade after the window for acknowledgment has closed.
- **Trim / re-release / call-pay:** The sequence of reverse-tripping the rejected leg to unwind the transaction back to pre-settlement.
- **Call letter / demand for settlement:** The legal instrument requiring the rejecting counterparty to return securities or deliver collateral within a fixed window (typically T+1 to T+5).
- **Standstill / moratorium:** A counterparty-imposed hold on the rejected leg, usually triggered by funding stress or insolvency concerns.
- **Cross-default / set-off:** The mechanism by which the custodian nets the repudiated transaction against the counterparty's other exposures, either bilaterally or via a title-transfer / close-out protocol.
- **Sole recovered vs. mixed recovered:** In some jurisdictions, if a fraction of the repudiated lot is traced, the rest can be treated as a generic claim rather than a specific recovery.

## The mental model
Repudiation settlement sits at the boundary between the custody value chain and the counterparty's legal / commercial risk. The custody platform must prove the trade exists (ticket, confirmation, matching evidence), demand return or delivery, and, if the counterparty refuses, escalate through internal credit committees to external courts. The architecture needs a legal-evidence vault, a collateral-matching engine, a dispute-workflow engine, and an integration to the Litigation / Collections CRM. Banks tie this to CSDR-III default-management rules and, for derivative trade, to the conditions of the ISDA Credit Support Annex.

```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    Trade[Matched Trade]:::core --> Confirm[Confirmation]:::core
    Confirm -->|counterparty rejects| Rep[Repudiation Register]:::critical
    Rep --> Demand[Demand Letter / Call"]:::core
    Demand -->|accepted| Xfer[Return / Delivery]:::core
    Demand -->|ignored| Escalate[Escalate: Credit Committee]:::critical
    Escalate -->|settled| Xfer
    Escalate -->|standstill| Hold[Standstill / Moratorium]:::context
    Hold --> Court[Court / ISDA Charge]:::critical
    Court -->|enforced| Recover[Recovery]:::core
```

## When to use / when NOT to use
- ✅ **Use when:** A counterparty denies a matched trade; collateral is missing; a legal / collections process is triggered.
- ⚠️ **Avoid when:** The dispute is a clerical mistake that can be corrected before the acknowledgment window closes—then use break management, not repudiation settlement.

## Banking example
A Swedish custodian's bond desk executes a swap with a US dealer; the trade matches at Markit. The USDC leg is confirmed, but the dealer refuses to deliver the equivalent EUR securities, believing the repo rate was misquoted. The custodian issues a demand letter under the ISDA CSA within T+2, places the dealer on a 10-day standstill, and, when the dealer defaults on the collateral rule, submits the ticket to the court-appointed bailiff. During the litigation window, the custodian rebalances the portfolio by calling the dealer's other matched trades under the cross-default clause, ultimately recovering 83 % of the notional via mandatory set-off.

## Common confusions (don't mix these up)
- **Repudiation settlement** vs **break management:** Repudiation is a legal rejection of a confirmed trade; break is an operational mismatch before or at confirmation.
- **Repudiation** vs **correction:** A correction is a back-office fix; repudiation is a counterparty-level disagreement that requires legal / collections escalation.

## Interview / recall prompt
> "Explain repudiation settlement in 2 minutes without notes."
- A matched trade is denied by the counterparty after acknowledgment.
- The custodian proves the trade with ticket and confirmation, then demands return / delivery.
- Standstills / cross-default let the custodian net against other exposures.
- If unresolved, the case is escalated to credit committee and/or court.
- The goal is recovery of securities / collateral, not merely a break closure.

## Status
☐ Not started · See detail doc: `details/C7-05-repudiation-settlement.md`

---
**One diagram required. Both brief + detail must exist before ✓.**
