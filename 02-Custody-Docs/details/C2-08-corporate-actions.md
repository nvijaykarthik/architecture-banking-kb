# [C2] Corporate actions — DETAIL
> **Category:** C2 Core Business Flows · **Difficulty:** ◑ · **Banking-relevant:** yes / 💳
> **Companion brief:** `briefs/C2-08-corporate-actions.md`

> > **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.

---

## 1. Precise definition
Corporate actions are events (e.g., dividend, rights, stock split, merger, tender offer, buyback, reorgani- kzation) initiated or approved by an issuer that alter the form, value, or entitlement of a held instrument. The custodian processes them at the issuer direct register; all clients with a position on the record date receive the benefit or must comply with the event.

## 2. Why this exists (the problem it solves)
Before corporate-action processing was institutionalized, banks would learn about a split or a dividend by reading a newspaper, miss the decision date, and lose the cash. The problem was the lack of a structured notice, review, and voting pipeline. The custodian solution: a dedicated corporate-action engine that ingests all notices, maintains a decision calendar, and executes the payout or voting instruction at the issuer register.

## 3. Core concepts & vocabulary
| Term | Precise meaning |
|------|-----------------|
| Record date | The date on which the issuer determines which clients receive the benefit |
| Ex-date | The first calendar day on which the stock trades without the dividend; the price drops by the dividend amount |
| Rights issue | Offering existing shareholders the right to buy new shares at a discount |
| Stock split | Exchanging one share for multiple shares; total value unchanged, price per share drops proportionally |
| Merger / acquisition | Two companies combine; shareholders of the acquired company receive shares of the acquirer at a fixed exchange ratio |
| Tender offer / buyback | The issuer repurchases shares at a fixed price; shareholders may tender |
| Corporate-action election | The client's decision to accept, refuse, or vote on a corporate action |
| Cash dividend | A cash payment from the issuer to shareholders declared on the record date |
| In-kind dividend | A non-cash payment (e.g., additional shares) |
| Special dividend | An irregular, non-recurring cash payment |
| Virtual event | A corporate action that does not affect the instrument but changes accounting (e.g., a name change) |
| Paper-loop | The transfer of securities to the issuer agency account for processing; irrevocable for "hard" events |
| Returns-by-mail | Dividends sent by postal mail; the modern equivalent is a direct bank transfer or CSTS |
| Exchange | A corporate action where bonds are exchanged for new bonds with revised terms |
| Annual general meeting (AGM) | Investor meeting for voting on corporate decisions; the custodian votes according to the signed mandate |
| Aggregate vote / netting | The total of client votes plus the custodian's own vote (the "bank" vote) |
| Hard / no soft loop | A hard event has an irrevocable issuer record; a soft event allows correction before the record date |
| Notifiable event | An event that the bank learns about before any corporate-action instruction |
| Pending event | An event still in the pipeline with an as-yet-unknown outcome |
| Size | The total amount of the event (e.g., a 2-for-1 split, or a 10% stock dividend) |
| Announce date | The date the issuer announces the event |
| Decision date | The date the issuer makes a final decision (not to be confused with the record date)
