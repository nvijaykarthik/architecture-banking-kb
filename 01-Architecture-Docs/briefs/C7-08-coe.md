# [C7-08] COE — BRIEF
> **Category:** C7 — Enterprise & Organizational Architecture · **Difficulty:** ◑/◑ · **Banking-relevant:** yes
> **One-liner:** _A center of excellence is a cross-functional governance body—typically involving IT, risk, and business leadership—that sets architectural standards, accelerates best practice sharing, and ensures that EA decisions are actionable and defensible across lines of business._
> **Why an EA cares:** _Without a COE, banks end up with 50 conflicting architecture review boards run by siloed product teams; the COE is the anti-pattern that turns architecture governance into a single, coherent, business-aligned voice._

## Quick definition
A center of excellence (COE) is a cross-functional governance body that sets enterprise-wide architectural standards, accelerates best practice sharing, and ensures architecture decisions are actionable and defensible. It is the *human engine* of EA governance.

## Key ideas / terms
- **Architectural Governance:** The right decisions, made at the right time, executed by the right people.
- **Solution architecture:** In-the-moment architecture—usually product/component-level.
- **Enterprise architecture:** Longer-term, strategic architecture—capability, portfolio, and roadmap level.
- **Review board:** Monitored, defended, and championed.
- **Archetype:** The intended model; a hardening guide.

## The mental model
A COE is the *assembly line* for architectural standards. Without it, standards are written by one team, ignored by another, and overwritten by a third. The COE is the *only place* where product, risk, and infrastructure can agree on a shared "right answer" and publish it in a way that is *discovered* and *enforced*.

## One diagram (mandatory)
```mermaid
graph LR
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px,color:#000
    classDef context fill:#dfe6e9,stroke:#636e72,color:#000
    classDef ok fill:#a7f3d0,stroke:#065f46
    classDef decision fill:#a3e634,stroke:#3f6212

    Governance[Architectural<br/>CoE]:::decision -->|harmonises| Product[Product &<br/>Solution<br/>Architects]:::ok
    Governance -->|sets<br/>standards| Standards[Standards<br/>& Policies]:::ok
    Governance -->|advises| Line[Line-of-<br/>Business) Chiefs]:::ok
    Line -->|feed back| Governance

    Silos[Siloed<br/>Review<br/>Boards]:::risk -->|conflicts| Governance
```

## When to use / when NOT to use
- ✅ **Use when:** The bank has >3 business lines; architecture reviews are inconsistent; there is a need for central standards; or an M&A integration is under way.
- ⚠️ **Avoid when:** The bank is a startup with a single product and <10 engineers; or when the organization is too small to justify a dedicated team.

## Banking 💳 example
A mid-tier Scottish bank's finance function had 5 separated architecture review boards: the housing-mortgage divisions, the savings-management divisions, the insurance treasurer's, the retail banking product management, and the trade-finance product management. Each had its own review board and its own standards, leading to contradictory architecture decisions.

The C-suite formed a cross-functional "Architecture & Technology" COE (business product, risk, IT, digital). The COE set:
- A *single* TOGAF-aligned architecture repository (Nutonian and EA repository).
- A *single* application inventory,
- A *single* data categorization matrix,
- A *single* cloud-architecture review process.

The 5 review boards were merged; the new board has a 6-week decision-cycle with a pre-filled decision package. The result: architecture approvals went from 12–16 weeks to 5–7 weeks; 87% of projects now use the same cloud-provider (AWS); and the bank's internal audit reported zero "departmentally inconsistent architecture decisions" in its 2024 audit.

## Common confusions (don't mix these up)
- **COE** vs **Guild / community of practice:** A *guild* is informal; a *COE* is a *governance body* with decision authority.
- **COE** vs **Architecture review board:** A *board* is transient and anchored to a line; a *COE* is permanent and cross-functional.
- **COE** vs **Product organization:** Product owners own the *what*; the COE owns the *how* (standards, patterns, guardrails).

## Interview / recall prompt
_“Explain a COE in 2 minutes without notes.”_ →
- It is the central hub for architectural standards and best-practice sharing.
- It is cross-functional, with representation from product, risk, and IT.
- It makes architecture decisions consistent and defensible.

---
**Status:** ✅ Covered · See detail doc: `[../details/C7_08-coe.md](../details/C7_08-coe.md)`
