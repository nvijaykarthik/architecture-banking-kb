# C8-02 Account Hierarchy — BRIEF
> **Category:** Custody/Identity — **Difficulty:** ◑ · **Banking-relevant:** yes 💳
> **One-liner:** An account hierarchy is the tree-like relationship structure that joins legal entities to custody accounts, then to sub-accounts and instrument positions, so that rights and obligations can be traced from the parent down to the individual holding.
>
> **Why an enterprise architect / trainee cares:** If the hierarchy is wrong, the bank cannot prove who owns what, cannot correctly allocate margin or collateral, and cannot satisfy a regulator's 401(k) or CSDR settlement mandate.

## Quick definition
An account hierarchy is a directed tree (or forest) in which nodes represent accounts (legal entity, corporate account, individual account, wallet) and edges represent ownership or custodial relationships, with each node annotated by economic rights, regulatory jurisdiction, and agency status.

## Key ideas / terms
- **Legal Entity:** The corporate or natural person that holds legal title to an account.
- **Custody Account:** The account at a sub-custodian where securities or cash are held.
- **Sub-account / Indirect Holder:** An account nested under a parent, typically representing a segment, product, or investor class.
- **Proxy:** The mechanism through which indirect holders exercise rights without direct sub-custodian access.

## The mental model
The account hierarchy is the *instance* of the logical layer defined by the reference architecture. It is how a bank maps a legal person (e.g., "Global Investment Corp") down to a specific securities position (e.g., "10,000 shares of Apple"). It must be navigable in both directions: from the top (aggregate exposure) down to the leaf (granular holding), and from the leaf up (collateral tracing or tax reporting).

The governance angle is about *ownership authenticity*: every link must be certified by the sub-custodian and reconciled against the Legal Entity Master (LEM).

## One diagram (mandatory)
 ```mermaid
 graph TD
     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
     A[Legal Entity]:::critical --> B[Corporate]:::core
     A --> C[Individual]:::core
     B --> D[Custody Account]:::context
     D --> E[Indirect Holder]:::context
     E --> F[Sub-account]:::context
     F --> G[Holding]:::core
     C --> H[Retail Account]:::context
 ```
 ```

## When to use / when NOT to use
- ✅ **Use when:** Allocating margin, reporting holdings to regulators, or performing collateral tracing.
- ⚠️ **Avoid when:** Modeling pure transaction flows (use a transaction diagram); the hierarchy is about *structure*, not *movement*.

## Banking example
A European asset manager maintains a hierarchy where the legal entity "EuroGP Fund S.à r.l." sits at the root, with 12 downstream sub-accounts per fund, each holding a mix of equities and government bonds at Euroclear. The sub-account level is critical for NAV calculation: the fund manager's treasury team aggregates the sub-account cash balances to compute the fund-level liquidity, while legal uses the same tree to prove to the CSSF that the fund holds sufficient liquid assets under the UCITS directive.

## Common confusions (don't mix these up)
- **Account Hierarchy** vs **Organizational Hierarchy:** The former is about custody and legal ownership; the latter is about corporate management structure.

## Interview / recall prompt
"Explain account hierarchy in 2 minutes without notes."
- Root = legal entity, leaves = instrument positions.
- Must trace rights and collateral.
- Must support regulatory reporting.

## Status
☐ Not started · See detail doc: `details/C8-02-account-hierarchy.md`

---
**One diagram required. Both brief + detail must exist before ✓.**
