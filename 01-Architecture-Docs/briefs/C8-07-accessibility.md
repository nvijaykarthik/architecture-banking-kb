# [C8-07] Accessibility — BRIEF
> **Category:** C8 — Reference Architecture, Standards & Principles · **Difficulty:** ◑ · **Banking-relevant:** yes
> **One-liner:** Accessibility in banking architecture is the design of systems—web, mobile, API, voice, and physical channels—that can be used by people with disabilities, ensuring full participation in financial services and compliance with the Equality Act 2010, Section 508, and EN 301 549.
> **Why an EA cares:** When a bank’s mortgage-approval portal or card-management app fails the accessibility test, it is not a minor UX bug—it is a regulatory anti-discrimination risk and a reputational zero in a market where trust is the only moat.

## Quick definition
**Accessibility** in financial architecture means ensuring that all digital and non-digital channels—CPAs, mobile apps, voice assistants, ATMs, in-person, and alternative formats—are operable by individuals with visual, motor, cognitive, sensor, or speech impairments. It is enforced through *technical* architecture (semantic HTML, color-contrast ratios, keyboard-only navigation, API response contracts) and *regulatory* architecture (Section 508/EI 301 549 audit evidence, WCAG 2.1 AA conformance certificates, Equality Act 2010 reasonable-adjustments protocols).

## Key ideas / terms
- **WCAG:** Web Content Accessibility Guidelines; the W3C standard for web accessibility (versions 2.1, 2.2).
- **Section 508 (US), EN 301 549 (EU), Equality Act 2010 (UK):** regulatory baselines for accessible digital procurement and services.
- **Reasonable adjustment:** under the Equality Act, a bank must make proportionate changes so a disabled person is not disadvantaged.
- **Alternative formats:** accessible PDFs, audio bank statements, accessible forms, knife-safe ATMs, In Braille signage.
- **Semantic HTML:** structure that conveys meaning to assistive technologies (screen readers).
- **Color-contrast ratio:** minimum 4.5:1 for normal text, 3:1 for large text.
- **Keyboard-only navigation:** no user-interface element is usable without a keyboard.
- **API accessibility:** response schemas must be semantically versioned and documented; screen readers (via voice-interface) can only operate if the XML/JSON is not a *data wall*.

## The mental model
Accessibility is the *minimum viable standard* of inclusion. In a world of digital banking, choosing a *web framework* without ARIA attributes is not a  decision—it is a *defect* that produces invisible barriers. The EA’s job is to treat accessibility as a *shared, non-negotiable quality attribute*—like security or availability—because a mortgage application should not be unusable for a blind customer who uses a screen reader, nor a card-management app unreachable by someone with motor impairments who navigates by voice和触.

## One diagram (mandatory)
```mermaid
graph LR
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef context fill:#dfe6e9,stroke:#636e72
    classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
    
    User[User with<br/>impaired Ability]:::critical
    
    Web[Web Portal<br/>(WCAG 2.1 AA)]:::context
    Mobile[Mobile App<br/>(EN 301 549)]:::context
    Voice[Voice Banking<br/>(Azure Cognitive)]:::context
    Physical[ATM Seating<br/>& accessible Form]:::context
    
    User -->|screen reader| Web
    User -->|voice command| Voice
    User -->|touch / sip-and-puff| Physical
    User -->|voice command| Mobile
    
    Web -->|sensitivity check| Monitor[Accessibility<br/>Monitor (axe / lighthouse)]:::decision
    Voice -->|sensitivity check| Monitor
    Mobile -->|sensitivity check| Monitor
    
    Monitor -->|pass| Release[{Release<br/>with cert}]:::ok
    Monitor -->|fail: new<br/>color ratio| Block[Block<br/>Build]:::risk
    
    User -->|alternative<br/>format request| Format[Accessible Form<br/>Generation]:::decision
    Format -->|PDF/HTML/BRF| User
    
    classDef ok fill:#a7f3d0,stroke:#065f46
    
    class User critical
    class Web,Mobile,Voice,Physical context
    class Monitor,Format decision
```

## When to use / when NOT to use
- ✅ **Use when:** every digital channel (CPAs, mobile, web, voice, API) must be compliant; entering over 30% disability-population market; executive sponsorship on inclusive design.
- ⚠️ **Avoid when:** a hidden, internal-only dashboard with no customer-facing surface and no regulated function (subject to anecdotal use).

## Banking 💳 example
A UK bank’s wealth-management platform uses a *chart-heavy* client-performance view: color-coded bars (green for profit, red for loss), interactive tooltips that depend on mouse-hover, and complex keyboard traps in the trade-execution flow. Blind customers with screen readers cannot read the color bars; motor-impaired users cannot navigate to the "buy" button without a mouse; the "portfolio snapshot" loads as an image—no alt text. The EA mandates:
- All color-coded trends must have a semantic *pattern* or textual label (not just color).
- Every interactive element must have keyboard focus and aria-labels.
- Data-presentation libraries must support *semantic* rendering (not just image exports).
- API responses for portfolio summaries must include an `accessible` variant (plain-text + reduced-chart representation).
- A DPO-style Accessibility Officer reviews every new contract with a design agency for WCAG 2.1 AA conformance.

## Common confusions (don't mix these up)
- **Accessibility** vs **Usability:** accessibility = operable by impaired users; usability = efficient/pleasant for all users (can be poor for disabled users).
- **Accessibility** vs **Inclusive design:** inclusive design = designing for *all* from the start (includes accessibility *plus* cognitive, linguistic, and situational needs); accessibility = legal baseline.
- **Semantic HTML** vs **CSS:** semantic HTML conveys meaning to assistive tech (ARIA, screen readers); CSS is styling (can disable copy-paste or keyboard).
- **WCAG 2.1 AA** vs **Section 508:** WCAG is the *criterion* for web content; Section 508 is the *US procurement law* that mandates vendors meet Section 508 (which references WCAG).
- **Alt-text** vs **Descriptive link text:** both close the accessibility gap, but alt-text is for images; single-word "click here" links are inaccessible because screen readers broadcast the text in isolation.

## Interview / recall prompt
“Explain accessibility architecture in 2 minutes without notes.” →
- It is the design of channels (web, mobile, voice, physical, API) usable by people with disabilities.
- It is a regulatory legal baseline (Equality Act, Section 508, EN 301 549).
- It is enforced by ARIA/semantic HTML, keyboard-only navigation, color-contrast ratios, and accessible-format generation.
- It is a non-negotiable quality attribute—like security or availability.
