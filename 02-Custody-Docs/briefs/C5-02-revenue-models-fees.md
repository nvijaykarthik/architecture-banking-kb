# C5-02: Revenue Models — Fees

## ClassDef
```mermaid
classDef critical fill:#ffe66d,stroke:#ffc107,stroke-width:2px
classDef core fill:#a7f3d0,stroke:#22c55e,stroke-width:2px
classDef context fill:#dfe6e9,stroke:#94a3b8,stroke-width:2px
```

## Mermaid Diagram
```mermaid
flowchart LR
    subgraph Revenue["Revenue Model"]
        A[AUM-Based] --> B[Fixed | % of AUM]
        C[Transaction-Based] --> D[Trade Volume | Ticket Size]
        E[Service-Based] --> F[Premium | Reporting | Advisory]
    end
    B --> G[Sticky Revenue]
    D --> H[Usage-Linked]
    F --> I[High Margin]
    G --> J[Brand Trust]
    H --> J
    I --> J
    style A critical
    style C critical
    style E critical
    style B core
    style D core
    style F context
```

## Problem
A single fee model limits revenue potential and fails to capture value from high-intensity services or high-concentration products. Platforms that rely purely on AUM-based fees miss high-margin opportunities.

## Impact
Revenue predictability suffers when fair-value assets fluctuate. Transaction-heavy clients generate disproportionate revenue without differentiated pricing. Competitors introducing hybrid models gain share from pure-play schemes.

## Recommendation
Adopt a **hybrid fee architecture** combining AUM, transaction, and service components, with clear caps and minimums to prevent fee shock.

## Word Count
168
