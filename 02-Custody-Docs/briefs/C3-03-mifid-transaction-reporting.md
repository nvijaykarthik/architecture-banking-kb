# [C3] MiFID II / MiFIR: transaction reporting, best execution — BRIEF

> **Category:** C3 Regulatory, Risk & Compliance · **Difficulty:** ◑ · **Banking-relevant:** yes / 💳

> **One-liner:** MiFID II / MiFIR is the EU framework that mandates Best Execution (best result for the client, not just lowest price) and near-real-time transaction reporting to a trade repository within 10–15 minutes.

> **Why an enterprise architect / trainee cares:** Every execution venue, every order router, and every trade capture system must feed a non-diverting TR pipeline. A latency failure or missing UTP is not a bug — it is a fine from ESMA or FCA.

## Quick definition
MiFID II (an EU directive) is the conduct and framework law for investment services. MiFIR (an EU regulation) is the attached rulebook imposing transaction reporting, transparency, and systematic internaliser obligations. Best Execution (Art. 24) is the single most litigated conduct rule in European custody.

## Key ideas / terms
- **MiFID II:** Directive 2014/65/EU; framework for investment services, conduct, organization.
- **MiFIR:** Regulation 600/2014; transaction reporting, transparency, market structure.
- **Systematic Internaliser (SI):** Non-exchange venue that runs a regular internalisation business; must document Best Execution for every SI trade.
- **Best Execution:** Best *result* on price, speed, costs, likelihood — not just lowest price.
- **Trade Repository (TR):** FCA (UK), ESMA (EU), SEC (US SDR); central reporting target.
- **UTP:** Unique Transaction Identifier; ESMA-assigned, must be unique, static, and appended to every reporting event.
- **Pre-trade Transparency:** Best quotes displayed on exchange / lit venues.
- **Post-trade Transparency:** Published trade details within 15 minutes (equities) or 10 minutes (FX).
- **Systematic Internaliser (SI):** Must comply with SI regime: No Better Off tests, Best Execution documentation.

## The mental model
Every trade in a MiFID II world is a **three-step pipeline**:
1. **Pre-trade:** Route to best venue (exchange, MTF, OTF, dark, or SI).
2. **Execution:** Record price, volume, time — append UTP.
3. **Post-trade:** Report to TR within 10–15 minutes; justify Best Execution.

If any step is manual, the trade is non-compliant and the bank is exposed.

## One diagram (mandatory)
```mermaid
graph TD
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef core fill:#a7f3d0,stroke:#065f46,stroke-width:1px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    A[Client order]:::critical --> B[Quote aggregation: lit + MTF + OTF + dark]:::core
    B --> C[Best Execution Engine]:::critical
    C --> D[Lit venue]:::money
    C --> E[SI / Internalisation]:::risk
    C --> F[Dark pool]:::context
    D --> G[Execution + UTP]:::core
    E --> H[BE documentation + SI report]:::critical
    G --> I[TR Report (10-15 min)]:::core
    H --> I
    I --> J[(Trade Repository)]:::data
```

## When to use / when NOT to use
- ✅ **Use when:** Trading EU / UK; executing on structured products, equities, equities, FX; SI activity.
- ⚠️ **Avoid when:** Assuming "lowest price = Best Execution" or assuming manual TR submission works.

## Banking example
**Deutsche Bank** (global custody) routes retail equity orders through Xetra, MTFs (BATS Chi-X), and internal dark books. Each route is logged; any SI trade generates a written Best Execution analysis per Art. 24.

## Common confusions
- **MiFID II vs MiFIR:** MiFID II = framework; MiFIR = reporting/transparency rules.
- **MTF vs OTF:** MTF = exchange-like; OTF = pure OTB (no pre-trade transparency).
- **Best Execution vs lowest price:** Best Execution = best result on price, speed, costs, likelihood — not just lowest price.

## Interview / recall prompt
- "What are the 6 quote points required G-Turnaround?"
- "Why is the UTP mandatory and how is it assigned?"
- "What is a Systematic Internaliser and what extra obligations does it carry?"
- "What is the deadline for MiFID II transaction reports under MiFIR?"

## Status
☐ Not started · See detail doc: `details/C3-03-mifid-transaction-reporting.md`

---
**One diagram required. Both brief + detail must exist before ✓.**
