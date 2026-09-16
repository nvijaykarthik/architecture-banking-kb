# C6-04 Service Levels — BRIEF
> **Category:** Cx — Custody Operations · **Difficulty:** ● · **Banking-relevant:** yes / 💳
>
> **One-liner:** NISA-defined service-level targets govern how quickly a custodian must settle asset transfers, which directly affect cash-flow planning and regulatory reporting.
>
> **Why an enterprise architect / trainee cares:** You cannot size settlement infrastructure, design monitoring, or justify vendor SLAs without matching them to NISA's prescribed time buckets—missing one deadline exposes the firm to financial penalties and CSA-wide scrutiny.
>
> ## Quick definition
> Service levels in custody are quantifiable thresholds for transaction completion timelines. NISA (National Instrument on Securities Settlement) codifies them into standardized buckets (e.g., T+2, T+3 cash settlement) so that every custodian, broker, and exchanging participant knows the exact window for asset transfer without bespoke bilateral negotiation.
>
> ## Key ideas / terms
> - **NISA:** National Instrument on Securities Settlement; the regulatory rulebook that sets mandatory settlement windows for Canadian clearing and settlement.
> - **T+n settlement:** The number of business days after trade date plus or minus zero. T+2 is the standard for same-day redemption cash; T+1 is for principal-protected funds.
> - **CDS / CSD:** Central securities depository or central securities database; the ledger-keeping entity that records ownership and effectuates transfers.
> - **QP / QP holder:** Qualified purchaser and its designated custodian responsible for final safe-keeping and settlement.
> - **Settlement finality:** The irreversible point at which a transferred security or cash becomes legally binding; failure to reach finality within the service level triggers breach.
>
> ## The mental model
> Service-level frameworks act as the contractual spine of the custody operating model. They sit above operational automation (the engine) and below regulatory sanctions (the ceiling). Every architectural decision—from middleware throughput to API timeout budgets—ultimately traces back to a NISA deadline, making these levels the reference crown for all custody flow design.
>
> ## One diagram (mandatory)
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
>     classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
>     classDef context fill:#dfe6e9,stroke:#636e72,color:#000
>     NISA[Regulatory deadline]:::critical --> SL[Service level bucket]:::core
>     SL --> IN[Custody infrastructure]:::context
>     SL --> OUT[Trade date adjustment]:::context
>     class IN context
> ```
>
> ## When to use / when NOT to use
> - ✅ **Use when:** Estimating end-to-end settlement latency or designing SLA dashboards for settlement operations.
> - ⚠️ **Avoid when:** Discussing micro-second trading commit latency; service levels operate at business-day granularity, not millisecond.
>
> ## Banking example
> A wealth manager instructs CIBAM to deliver 500 Canadian government bond units to a client's RA disc account. Under NISA's T+2 cash settlement service level, the transfer must be identified, the corresponding cash pollination settled, and finality signed off by the close of the second post-trade business day. If the instruction hits CIBAM's KFMS on the trade date, the architecture must provision enough parallel processing threads to clear all steps before the end of business on day two, or the manager breaches the CSA's cash-loading rules and faces a regulatory notice.
>
> ## Common confusions (don't mix these up)
> - **Service level** vs **SLA:** Service level is the regulatory *target*; SLA (service-level agreement) is the *contractual commitment* between a custodian and its client.
> - **T+n** vs **T+n + m days:** Pure T+n is calendar/business-day subject to NISA; some bilateral agreements add a grace period m, but CSAs must not permit it if it exceeds the NISA bucket.
>
> ## Interview / recall prompt
> “Explain NISA settlement service levels in 2 minutes without notes.”
> - Name the three governing buckets: cash settlement, securities transfer, and matched settlement finality.
> - State the standard T+2 window and what triggers T+1 for principal-protected funds.
> - Explain why finality, not identification, is the true deadline.
> - Tie infrastructure sizing directly to the highest-priority bucket.
> - Mention that breached levels trigger CSA financial penalties regulated by OSC or BCSC.
>
> ## Status
> ☐ Not started · See detail doc: `details/C6-04-service-levels.md`
>
> ---
> **One diagram required. Both brief + detail must exist before ✓.**
