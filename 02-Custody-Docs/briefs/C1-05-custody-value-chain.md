# C1 custody value chain — BRIEF
> **Category:** C1 Foundations · **Difficulty:** ◑ · **Banking-relevant:** yes / 💳
>
> **One-liner:** The custody value chain is the end-to-end sequence of activities that moves securities and cash from client onboarding through safekeeping, corporate actions, and periodic reporting.
>
> > **Why an enterprise architect / trainee cares:** Understanding the value chain is what separates a junior from a seasoned architect; it reveals where custody actually sits between trading, settlement, and operations, and it exposes the governance hand-offs that regulators audit first.
>
> ## Quick definition
> Custody is the safekeeping and administration of securities and cash. The value chain is the ordered set of processes—onboarding, settlement, holding, corporate actions, securities lending, reporting—that delivers that service from contract to statement.
>
> ## Key ideas / terms
> - **Onboarding:** account setup, KYC/AML screens, legal entity verification, and entitlement mapping.
> - **Settlement:** the exchange of cash for securities (or vice versa) through DVP/DvP models.
> - **Holding:** legal record-keeping of ownership; nominee, omnibus, and segregated structures.
> - **Corporate actions:** cash distributions, splits, mergers, and voting instructions.
> - **Securities lending:** temporary transfer of borrowed securities for cash collateral management.
>
> ## The mental model
> The custody value chain is not a single product but a pipeline with touch-points at every tripwire: regulatory (money-laundering, tax withholding), operational (CLS netting, weekend cut-offs), and client-service (reporting SLAs). The architect must map vendors, internal lines of defence, and fail-over paths so that no single hand-off is a single point of failure.
>
> ## One diagram (mandatory)
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     A[Onboarding]:::core --> B[Settlement]:::core
>     B --> C[Holding]:::critical
>     C --> D[Corporate Actions]:::core
>     D --> E[Securities Lending]:::core
>     E --> F[Reporting]:::core
> ```
> ```
>
> ## When to use / when NOT to use
> - ✅ **Use when:** describing end-to-end custody liability, estimating operational risk, or defending a separation-of-duties design.
> - ⚠️ **Avoid when:** explaining embedded settlement in RTGS systems—use the settlement value chain instead.
>
> ## Banking 💳 example
> A private bank such as UBS opens a new client account. The custody team must verify the client (onboarding), settle the first cash deposit (settlement), register the client in the internal nominal ledger (holding), distribute the BMW AG dividend via the new DTA mechanism (corporate actions), and generate the year-end tax certificate (reporting). At each step, IRS, FATCA, and local tax withholdings create distinct compliance checkpoints.
>
> ## Common confusions (don't mix these up)
> - **Custody value chain** vs **settlement process:** custody *holds* the asset; settlement *moves* the title.
> - **Holding in omnibus** vs **holding in nominee:** indemnity bailment is the hidden risk.
>
> ## Interview / recall prompt
> “Explain the custody value chain in 2 minutes without notes.”
> - 1. Name the five stages in order.
> - 2. Name the regulatory gate at each stage.
> - 3. Explain why settlement feed is a critical dependency.
>
> ## Status
> ☐ Not started · See detail doc: `details/C1-05-custody-value-chain.md`
>
> ---
> **One diagram required. Both placeholders replaced. Both brief + detail must exist before ✓.**
