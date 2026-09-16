# C1 how custody makes money — BRIEF
> **Category:** C1 Foundations · **Difficulty:** ◑ · **Banking-relevant:** yes / 💳
>
> **One-liner:** Custody generates revenue through a mix of account fees, securities-lending fees, withholding-tax capture, and transaction charges, with the economics depending on asset type, client segment, and jurisdiction.
>
> > **Why an enterprise architect / trainee cares:** Revenue is the budget that funds the technology platform; understanding *which* fee lines are recurring, *which* are variable, and *which* require regulatory clearance determines how much autonomy the custody environment can have.
>
> ## Quick definition
> Custody economics is the study of fixed and variable revenue streams a custodian captures for holding, managing, and servicing securities and cash—including safekeeping fees, inventory lending fees, withholding-tax programmes, and settlement transactions—netted against infrastructure and regulatory-compliance costs.
>
> ## Key ideas / terms
> - **Safekeeping fee:** fixed annual or periodical charge per account, often basis-point of AUM.
> - **Securities-lending fee:** fixed fee plus a variable rebate split; primary driver of income.
> - **Withholding tax:** asset-class specific tax, often reclaimable or tax-transparent via DTA.
> - **Impairment loss:** uncorrelated risk write-down; no revenue, but a negative line.
> - **Scale leverage:** the cost curve is sub-linear; an extra €1 bn in AUM raises cost < €1 m.
>
> ## The mental model
> Custody is a *high fixed-cost, low marginal-cost* utility. The architecture must separate *core* revenue-generating pipelines (lending, DTA) from *support* cost centres (reporting, tax forms). A change in one pipeline (e.g., a new DTA engine) must not destabilise the others; therefore, modular fee calculation and independent pricing services are mandatory.
>
> ## One diagram (mandatory)
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     A[Safekeeping Fee]:::core --> Revenue[Total Revenue]:::critical
>     B[Securities Lending]:::critical --> Revenue
>     C[Withholding Tax Capture]:::core --> Revenue
>     D[Settlement Txn Fee]:::context --> Revenue
>     E[Impairment Loss]:::context --> Revenue
> ```
> ```
>
> ## When to use / when NOT to use
> - ✅ **Use when:** pricing a new custody offer, building a fee-allocation model, or defending cost-recovery to a CFO.
> - ⚠️ **Avoid when:** forecasting repo-market rates—use repo economics, not custodial economics.
>
> ## Banking 💳 example
> The same private bank (UBS) charges 1.2 % p.a. on the first €5 m of discretionary AUM as a safekeeping fee, 2.5 % on US equities lent out via securities lending, and 15 % of withholding tax recaptured via the Anglo-German DTA treaty. On a €100 m fund, this yields roughly €1.2 m + €2.5 m + €0.15 m = €3.85 m gross annual revenue; after infrastructure at €2.1 m, it delivers a gross margin of 45 %.
>
> ## Common confusions (don't mix these up)
> - **Securities-lending fee** vs **repo rate:** lending fee is the custodian’s margin; repo is the market benchmark the custodian competes against.
> - **Withholding tax** vs ** Withholding-tax capture:** tax is an obligation; capture is the business of reclaiming it.
>
> ## Interview / recall prompt
> “Explain how custody makes money in 2 minutes without notes.”
> - 1. Name the three main revenue lines.
> - 2. Name the biggest cost driver.
> - 3. Explain why lending dominates margin in developed markets.
>
> ## Status
> ☐ Not started · See detail doc: `details/C1-06-revenue-model.md`
>
> ---
> **One diagram required. Both brief + detail must exist before ✓.**
