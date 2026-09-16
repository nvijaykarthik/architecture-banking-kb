# C5-01: Economics — Cost to Serve

## ClassDef
```mermaid
classDef critical fill:#ffe66d,stroke:#ffc107,stroke-width:2px
classDef core fill:#a7f3d0,stroke:#22c55e,stroke-width:2px
classDef context fill:#dfe6e9,stroke:#94a3b8,stroke-width:2px
```

## Mermaid Diagram
```mermaid
flowchart LR
    subgraph cost["Cost to Serve Architecture"]
        A[Customer Segment] --> B[Order Type]
        B --> C[Settlement T+N]
        C --> D[Trade Volume]
    end
    D --> E[Direct Costs]
    D --> F[Overhead Burden]
    E --> G[Technology Fit]
    F --> G
    G --> H[Profit per Account]
    style A critical
    style H critical
    style C core
    style E core
    style F context
    style B context
```

## Problem
Custody platforms charge uniform fees across customer segments even though cost to serve varies dramatically by trade type, settlement cycle, and account activity. Low-frequency retail investors look similar on paper to high-net-worth advisors, but their transaction profiles and support burdens differ by an order of magnitude.

## Impact
Pricing misaligned with cost to serve erodes margin, subsidizes unprofitable accounts, and distorts product investment. It also creates customer defection risk when competitors introduce segment-aware pricing.

## Recommendation
Segment accounts by cost-to-serve tier, assign trade-type surcharges, and publish a transparent fee schedule that correlates price with expected operational load.

## Word Count
198
