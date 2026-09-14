# [C8-03] Principles — BRIEF
> **Category:** C8 — Reference Architecture, Standards & Principles · **Difficulty:** ● · **Banking-relevant:** yes
> **One-liner:** An architecture principle is a concise, non-negotiable truth about the architecture—such as “data is owned by business domains”—that orients decisions, resolves trade-offs, and can be tested with a yes/no check.
> **Why an EA cares:** Principles prevent feature teams from optimizing locally at the expense of latency, security, or regulatory compliance; they are the guardrails that keep a bank’s architecture from drifting into fragmentation.

## Quick definition
An **architecture principle** is a short, imperative statement about how the enterprise architecture is *intended* to behave, rooted in business strategy, value architecture, and quality attributes. It is *non-negotiable* for most decisions, *testable* (you can ask “Does this decision violate principle P4?”), and *owned* by a governance council.

## Key ideas / terms
- **Driving principle:** a principle that points toward current goals (e.g., “real-time fraud detection for digital channels”).
- **Inhibiting principle:** a principle that constrains the future (e.g., “no on-premises core-banking data stores after 2028”).
- **Buffer principle:** an explicit exception to a principle, allowing temporary deviation (e.g., “new regulatory reporting can bypass the API gateway for 180 days”).
- **Named principle vs. named pattern:** principles answer *why*; patterns answer *how*.
- **Principle hierarchy:** strategic principles cascade into design principles, which cascade into implementation guidelines.

## The mental model
Think of principles as *constitutional law* for architecture. They are not code, not diagrams, not frameworks—they are *true statements about intent* that outlive any single project. In a bank with 12 product lines, principles prevent the card team from choosing a 24-hour batch fraud model while the payments team chooses real-time because “that’s faster.” Both teams might be right operationally, but the principle “real-time fraud detection is mandatory for all digital channels” says otherwise.

## One diagram (mandatory)
```mermaid
graph LR
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef context fill:#dfe6e9,stroke:#636e72,stroke-width:1px
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
    
    Board[Board / Strategy<br/>(Strategic Principles)]:::critical -->|cascades to| Arch[Enterprise Architecture<br/>(Design Principles)]:::decision
    Arch -->|guides| TeamA[Payments Team<br/>(Guidelines)]:::context
    Arch -->|guides| TeamB[Lending Team<br/>(Guidelines)]:::context
    
    Board -->|controls| A[“Data owned<br/>by domain?”]:::decision
    Board -->|controls| B[“Real-time<br/>fraud?”]:::decision
    Board -->|controls| C[“Zero-trust<br/>network?”]:::decision
    
    TeamA -->|applies| A
    TeamB -->|applies| A
    TeamA -->|breaks| B:::context
    TeamB -->|breaks| B:::context
    
    A:::critical -->|resolves| Tie[Payment vs. Lending<br/>Shared Customer View]:::decision
    check{{Is the decision<br/>principle-compliant?}}:::decision
    A --> check
```

## When to use / when NOT to use
- ✅ **Use when:** a product team proposes a local optimization that conflicts with an enterprise quality attribute (security, latency, cost).
- ⚠️ **Avoid when:** evaluating a tiny, isolated component with no cross-team or cross-domain impact; a guideline is more lightweight than a principle.

## Banking 💳 example
A retail bank’s “fast-track digital” squad wants to launch a 30-second lending approval by bypassing the KYC microservice and caching customer data in node memory. The architecture principle “customer data must be owned by the KYC domain and accessed via API” blocks the design. The team instead uses an event-driven cache with TTL ≤ 5 minutes and explicit CDC streaming from the KYC domain—aligning with the principle while meeting the business timeline.

## Common confusions (don't mix these up)
- **Principle** vs **Pattern:** principle = why; pattern = how.
- **Principle** vs **Standard:** principle = intent; standard = externally prescribed rule.
- **Guideline** vs **Principle:** guideline is advisory; principle is non-negotiable.

## Interview / recall prompt
“Explain architecture principles in 2 minutes without notes.” →
- A principle is a non-negotiable truth about architecture intent.
- It is testable with a yes/no question.
- It is owned by a governance council and cascades from strategy to design to implementation.
- It resolves trade-offs between product teams and enterprise constraints.
