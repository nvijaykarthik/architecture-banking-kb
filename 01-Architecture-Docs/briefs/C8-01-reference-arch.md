# [C8-01] Reference Architecture — BRIEF
> **Category:** C8 — Reference Architecture, Standards & Principles · **Difficulty:** ● · **Banking-relevant:** yes
> **One-liner:** A reference architecture is a prescriptive, reusable structural blueprint that defines constraints, patterns, and interaction rules so that systems and enterprise services are built consistently within a bank’s IT landscape.
> **Why an EA cares:** Without a reference architecture, every project reinvents the wheel on integration patterns, technology choices, and risk controls, producing runaway technical debt and compliance gaps that auditors and regulators punish.

## Quick definition
A reference architecture is a standardized structural blueprint—set of constraints, best practices, and explicit patterns—that prescribes how components, data flows, and technologies must interconnect across a bank’s enterprise IT portfolio. It sits one level above a single solution architecture: it is *common across initiatives* and *enforces consistency* while still allowing variation for business context.

## Key ideas / terms
- **Reference architecture:** a reusable blueprint with constraints, not a one-off design; governs by rule, not by recommendation.
- **Solution architecture:** architecture specific to one initiative, constrained *by* the reference architecture but free to vary on implementation details.
- **Architecture governance:** the processes (change control, standards boards, review gates) that ensure projects comply with the reference architecture and escalate trade-offs.
- **Platform engineering:** the practice of delivering capabilities (deployment pipelines, compliance libraries, identity frameworks) as internal products so that downstream teams build *on* reference patterns, not *around* them.

## The mental model
Think of the reference architecture as the *grammar* of the bank’s IT language. Every solution architecture is a *sentence* written in that grammar. The grammar does not dictate the exact words (vendors, flavor of Kafka, or cloud region) but it disallows concatenations that create security holes, latency black holes, or operational blind spots. In practice, the reference architecture is owned by a Center of Excellence that publishes versioned domain maps—payments, core banking, data—and maintains a living architecture decision register.

## One diagram (mandatory)
```mermaid
graph LR
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef context fill:#dfe6e9,stroke:#636e72,stroke-width:1px
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
    
    A[Center of Excellence<br/>(Reference Architecture]:::critical -->|publishes| B[Domain Map]:::context
    B -->|constrains| C[Solution A<br/>Payments]:::decision
    B -->|constrains| D[Solution B<br/>Lending]:::decision
    B -->|constrains| E[Solution C<br/>Wealth]:::decision
    C -->|composes| F[Core API Platform]:::context
    D -->|composes| F
    E -->|composes| F
    B -->|governs| G[ADR Register]:::context
    C -->|justifies deviation via| G
    D -->|submits decision to| G
    E -->|submits decision to| G
```

## When to use / when NOT to use
- ✅ **Use when:** entering a new product line (e.g., instant-settlement B2B payments) or migrating a critical domain (core banking replacement) to a new cloud tenant—you need a consistent starting point and an escape hatch.
- ⚠️ **Avoid when:** the domain is a tiny, low-risk proof-of-concept with no downstream dependencies; a lightweight pattern or guideline is more cost-effective than a full reference architecture.

## Banking 💳 example
A bank operating in the UK, EU, and US launches a cross-border B2B payment rail. The reference architecture mandates a shared API gateway, ISO 20022 message envelopes, strict PCI-DSS tokenization at the gateway, and a unified customer-journey event stream. Each product line (US NACHA-compatible, EU SEPA, UK Faster Payments) references the same gateway and eventing infrastructure, then diverges only in routing rules and regulatory payload enrichment. This prevents six months of duplicated gateway builds and avoids a PCI audit failure.

## Common confusions (don't mix these up)
- **Reference architecture** vs **Solution architecture:** the former is *global* and *constrained*; the latter is *local* and *constrained by the former*.
- **Reference architecture** vs **Enterprise architecture (EA):** EA is the *practice* and *portfolio view*; reference architecture is the *blueprint* that enables that view.

## Interview / recall prompt
“Explain reference architecture in 2 minutes without notes.” →
- It is a set of rules, not a single design.
- It is owned by a CoE and versioned.
- It lets solution architects deviate via ADRs, not inline.
- It reduces duplication and audit risk across the bank’s payment, lending, and data domains.
