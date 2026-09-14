# Enterprise Architecture — 0 to Professional
### Knowledge Base for IT Portfolio Enterprise Architects (Banking)

> **Owner:** Guru
> **Goal:** Master EA from absolute basics to professional depth. No "basics" gap.
> **Companion:** `LEARNING-PLAN.md` (14 days, 2 hrs/day). **Task tracker:** `TASKS.md`.

---

## What this is

A structured, self-contained reference library. Every topic in `[TASKS.md](./TASKS.md)` is
documented twice:

| Layer | Directory | Purpose |
|-------|-----------|---------|
| **Brief** | `briefs/` | 5–15 min read. Terms, key ideas, 1 diagram, "why it matters". For recall & interviews. |
| **Detail** | `details/` | Full deep-dive. Definitions, comparisons, trade-offs, banking context, patterns, worked examples, diagrams. For mastery. |

## How to navigate

1. **Learn:** Follow `LEARNING-PLAN.md` day-by-day (curated order, ~17 min/topic).
2. **Track:** Every topic has a row in `TASKS.md`. Status: `☐ Not started` → `◐ In progress` → `✅ Covered`.
3. **Refresh:** Open `briefs/` for a rapid refresher, `details/` for exam/consulting depth.

## Directory map

```
01-Architecture-Docs/
├── README.md                 ← you are here (index + legend)
├── TASKS.md                  ← master task tracker (96 topics, status)
├── LEARNING-PLAN.md          ← 14-day / 2hr-per-day study plan
├── templates/
│   ├── BRIEF-TEMPLATE.md     ← format for every brief
│   └── DETAIL-TEMPLATE.md    ← format for every detail
├── briefs/                   ← one file per topic (C1-01 … C10-12)
└── details/                  ← one file per topic (C1-01 … C10-12)
```

## Topic categories (at a glance)

| # | Category | Topics | Path |
|---|----------|--------|------|
| C1 | Foundations & Core Concepts | 8 | `briefs/` `details/` |
| C2 | Frameworks & Methods (TOGAF, Zachman…) | 8 | `briefs/` `details/` |
| C3 | Architecture Domains (Biz/Data/App/Sec…) | 10 | `briefs/` `details/` |
| C4 | System & Software Design | 12 | `briefs/` `details/` |
| C5 | Patterns & Archetypes (GoF → Cloud) | 10 | `briefs/` `details/` |
| C6 | Design Philosophy & Quality Attributes | 10 | `briefs/` `details/` |
| C7 | Enterprise & Organizational Architecture | 8 | `briefs/` `details/` |
| C8 | Reference Architecture, Standards & Principles | 8 | `briefs/` `details/` |
| C9 | Governance, Management & Strategy | 10 | `briefs/` `details/` |
| C10 | Emerging & Advanced (Cloud-native → GenAI) | 12 | `briefs/` `details/` |
| | **Total** | **96** | |

## Legend

- **Status:** `☐ Not started` · `◐ In progress` · `✅ Covered`
- **Difficulty:** `●` foundational · `◑` core · `○` advanced
- **Banking relevance:** `💳` = high relevance to banking / financial services

## Conventions

- Every document includes **at least one Mermaid diagram** (color-coded where it matters).
- Banking context is called out explicitly in a `💳 Banking context` section.
- Terminology is linked to the **Core Vocabulary** in `C1-08`.
