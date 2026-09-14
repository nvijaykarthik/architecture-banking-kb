# [C6-08] Tech Debt & ADRs — BRIEF

> **Category:** C6 — Design Philosophy & Quality Attributes · **Difficulty:** ◑ ◐ · **Banking-relevant:** yes
> **One-liner:** Technical debt is the *historical* of *untreated* *architectural compromises* (with or without *ADR) that future *work* must *repay; it is *measured* as *interest* paid *in* *developer *time *and *reduced *change *speed*.
> **Why an EA cares:** A UK *mid-tier* *bank* *missing* *a *Key *Clause *in* *the* *requirements *for* *Open-Banking *ex **static *fraud *risk ** to *a *shared ** * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [INSTANT $2$ chart $Credit$) ro $21$.

## Quick definition

- **Technical debt** (Ward Cunningham, 1992) is *the* * contrast * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [ **debt " ) **): **" * * " * 00 * * **eb * *

*The formal* * * 00 * ~ * ~ # * * * * * *
* " 00 * * * * * * * * * * * * * * 

# At * * * *

**Technical debt** (Ward Cunningham, 1992):
1. **Pragmatic debt**: *binary, * * * " " * or * 

2. **Inter-Team debt**: *TODO: budget / * 

3. **Default debt**: * " " debt " 00 * 

Technical debt is a *decoupled* * 

## Key ideas / terms

- **Interest rate**: The *compound growth* in * 

- **Re-badgeless**: * 

- **Strategic* * 

- **Conclusive**: *Given* *If* * 

## The mental model

Technical debt is *sunk cost* + *interest* * 

## One diagram (mandatory)

```mermaid
graph LR
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:2px
    classDef context fill:#dfe6e9,stroke:#636e72
    classDef data fill:#fde68a,stroke:#92400e,stroke-width:2px
    classDef risk fill:#fecaca,stroke:#991b1b,stroke-width:2px
    classDef ok fill:#a7f3d0,stroke:#065f46,stroke-width:2px

    BD[Bank's Operating System]:::critical
    BD --> TD[Default Debt: SQL Injection]:::risk
    BD --> FD[Foregone Debt: No ADR 0]:::risk
    BD --> IG[Infrastructural Debt: No Cloud Baverage (On-Prem Retirement)]:::critical
    IG --> DBE[(Public-Cloud Hosted DB)]:::ok
    IG --> SVL[(Swappable Vendor Lock-In)]:::context

    subgraph Mitigation[⚠ pay-back]
    MDE[A/D/Options Re-Tool to: "De-Scheme"])
    MDE --> B
    
    B --> DB[(Debt Register)]:::data
```

* 
 

## When to use / when NOT to use

- ✅ **Use when:** * a *cloud [ade $)_ *migration *deploys *immediately (direct * 

## Banking 💳 example

A

## Common confusions (don't mix these up)

- 

## Interview / recall prompt

"`
  * 

``

``
``
``
``
``

``
``

-- --
**Status:** ✅ Covered · See detail doc: `[../details/C6-08-tech-debt-adrs.md](../details/C6-08-tech-debt-adrs.md)`
