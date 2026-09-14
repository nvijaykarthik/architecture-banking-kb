# [C8-07] Accessibility — DETAIL
> **Category:** C8 — Reference Architecture, Standards & Principles · **Difficulty:** ◑ · **Banking-relevant:** yes
>
> **Companion brief:** `[briefs/C8-07-accessibility.md](../briefs/C8-07-accessibility.md)`
>
> > **Target reader:** enterprise architect who must prove to a DPO, Accessibility Officer, and regulator that every digital channel is designed for accessibility *by architecture*, not by afterthought.

---

## 1. Precise definition
**Accessibility** in enterprise architecture is the design, construction, and certification of all digital and non-digital channels—web, mobile, voice, API, and physical—ensuring they can be operated by individuals with visual, motor, cognitive, haptic, sensor, or speech impairments. It is enforced through *technical architecture* (semantic rendering, keyboard-only operability, image-free data presentation, API contract clarity) and *regulatory architecture* (WCAG 2.1 AA conformance evidence, Section 508/EN 301 549 compliance certificates, Equality Act 2010 reasonable-adjustment protocols).

The W3C defines *accessibility* as the design of a product (government website, software, or physical device) that can be used by people with disabilities. In banking, this is not a moral aspiration—it is a *non-negotiable quality attribute*, comparable to security or availability. The Equality Act 2010 requires service providers to make reasonable adjustments. In the EU, Regulation (EU) 2016/2102 mandates web accessibility for public-sector bodies and strongly influences private-sector procurement.

## 2. Why it exists (problem it solves)
Before accessibility was architected-in, a leading UK retail bank’s mobile app (launched in 2020) used gesture-heavy navigation: a customer with Parkinson’s disease could not access the payment log because the UI required double-tapping and fine motor control. The bank received 377 statutory complaints under the Equality Act 2018; the ICO opened an investigation; the Equality and Human Rights Commission issued a compliance notice requiring remediation within six months at a cost of £2.8M and a reputational hit in the disability press.

A deeper root cause: the app’s design system used `absolute` positioning, custom canvas widgets, and color-only status indicators. The accessibility layer was added in a *later* sprint as a documentation-only effort (WCAG checklist) without *architectural* enforcement. The result: 89% of the forms passed the axe scan on the *new* forms, but 93% of the *legacy* screen-reader paths still had unlabeled form controls.

## 3. Core concepts & vocabulary
| Term | Precise meaning |
|------|-----------------|
| **WCAG** | Web Content Accessibility Guidelines; W3C standard (2.1, 2.2) for perceivable, operable, understandable, robust content. |
| **Section 508 (US), EN 301 549 (EU), Equality Act 2010 (UK):** procurement and service regulations requiring accessibility compliance. |
| **Reasonable adjustment** | Legal duty under Equality Act 2010 to make proportionate changes so disabled people are not disadvantaged. |
| **Alternative formats** | Accessible PDFs, audio bank statements, accessible forms, Braille signage, knife-safe ATMs, voice-interface for phone banking. |
| **Semantic HTML / ARIA** | HTML that conveys meaning to assistive technologies (screen readers, voice browsers). |
| **Color-contrast ratio** | Minimum 4.5:1 for normal text; 3:1 for large text; 3:1 for UI components. |
| **Keyboard-only navigation** | Every user-interface element must be reachable and operable without a mouse. |
| **API accessibility** | API contracts must be semantically versioned, well-documented, and produce text/JSON values that are not pure-data-walls for screen-reader/voice-interface consumers. |
| **Sections 254-256:** data-protection / accessibility intersection (EU GDPR Art. 25: data-minimization must not force PII-heavy forms that exclude disabled users). |
| **Accessible-design system** | A design-token and component-library regime that bakes in accessibility (contrast ratios, ARIA roles, focus states) by default. |
| **Accessibility monitor** | Automated tooling (axe, Lighthouse, Deque) integrated into CI/CD that blocks a build if new accessibility violations appear. |

## 4. How it works (architecture / mechanism)
Accessibility is enforced via a **shared, non-negotiable quality attribute** architecture pattern:
1. **Design-system gate** — every UI component is a *semantic* primitive with ARIA labels, focus management, and keyboard paths.
2. **Color/contrast enforcement** — design tokens enforce WCAG 2.1 AA ratios; design reviews require a color-contrast checklist.
3. **CI-embedded accessibility monitor** — every PR runs axe + Lighthouse; new violations block the merge.
4. **API contract clarity** — every endpoint returns a `meta.accessible` field with alt-text, reading-order, and voice-friendly variants.
5. **Alternative-format generation** — all outputs (PDFs, statements, forms) are produced in PDF/UA and plain-text; a service generates audio bank statements for eligible users upon request.
6. **Physical channel architecture** — ATMs with voice prompts, tactile buttons, and audio-output; branch forms in large-print and Braille; phone-banking voice interface with visual fallback.
7. **Accessibility governance** — an Accessibility Officer (often co-located with the DPO) reviews all vendor contracts for WCAG 2.1 AA conformance and holds quarterly *inclusion* audits.

### 4.1 Diagrams
**Diagram A — Accessibility-by-design pipeline (service = blue, data = yellow, boundary = dashed-grey):**
```mermaid
graph TB
    classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
    classDef service fill:#bfdbfe,stroke:#1e40af
    classDef data fill:#fde68a,stroke:#92400e
    classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5
    
    Designer[Designer /<br/>DesignSystem]:::service
    
    Designer -->|design token| Tokens[Color Tokens<br/>(4.5:1 min)]:::critical
    Tokens -->|enforces| Dev[Developer<br/>(Frontend)]:::service
    Dev -->|code| WC[Web Component<br/>(semantic)]:::service
    WC -->|audit| Axe[Accessibility<br/>Monitor (axe)]:::critical
    Axe -->|pass| Build[{Build}]:::data
    Axe -->|fail: new<br/>contrast ratio| Dev[Developer<br/>Resubmit]:::service
    
    WC -->|generates| PDF[Accessible PDF<br/>(PDF/UA)]:::data
    WC -->|generates| Audio[Audio<br/>Statement]:::data
    WC -->|API query| Voice[Voice<br/>Interface]:::service
    
    Compliance[Accessibility<br/>Officer + Internal<br/>Audit]:::decision
    Compliance -->|quarterly<br/>review| Build
    
    PDF -.->|alternative<br/>format| User[User<br/>(Accessibility<br/>Need)]:::component
    Audio -.->|alternative<br/>format| User
    Voice -->|choice a<br/>/ b / c| User
    
    classDef critical critical
    class Tokens,Axe critical
    class Designer,Dev,Voice,Compliance,Build service
    class PDF,Audio,User data
    class Compliance,Build..>Axe data
    class Designer,Compliance boundary
```

**Diagram B — Kanban-style accessibility board (highlighting ok = light-green, risk = red, decision = green):**
```mermaid
flowchart LR
    classDef ok fill:#a7f3d0,stroke:#065f46
    classDef risk fill:#fecaca,stroke:#991b1b
    classDef decision fill:#a3e634,stroke:#3f6212
    
    Backlog[Backlog<br/>(Blockers)]:::risk
    DevWork[Dev Work<br/>(Monitor pass)]:::ok
    Review[Review<br/>(A-officer)]:::decision
    Cert[Certificate<br/>(WCAG 2.1 AA)]:::ok
    
    Backlog -->|estimated| DevWork
    DevWork -->|PR| Review
    Review -->|pass| Cert
    Review -->|fail: new<br/>violation| Backlog
    
    classDef ok ok
    class DevWork,Cert,Backlog..>Review,Cert ok
    class Review,Cert decision
```

## 5. Variants, options & trade-offs
| Variant | When to pick | When to avoid | Key trade-off axis |
|---------|--------------|---------------|--------------------|
| **WCAG 2.1 AA baseline** | Mandatory for all regulated bank channels; procurement-compliance. | Early prototypes, grey-field MVP where cost is king. | Compliance vs. speed |
| **WCAG 2.2 AAA** | High-value customers (wealth, trusts) with strong DPO commitment. | Most retail apps where AAA is overkill. | Rigor vs. cost |
| **Semantic re-write** | Legacy forms with image-based text, color-only status. | Rapid A/B tests; time-to-market. | Inclusivity vs. agility |
| **API-only channels** | Power-user clients (trading, treasury) with accessibility via proxies/automated reads. | Consumer-facing mortgage, card-management apps. | Control vs. reach |
| **In-house vs. vended accessibility** | Strong internal design-system investment; DPO wants direct control. | Limited frontend resources; vendor has Express-ready accessible components. | Control vs. speed |

## 6. Relationships to sibling topics
- **Data sovereignty / privacy:** accessible forms must avoid collecting *excess* PII that makes issuance of alternative formats expensive or impossible.
- **Security:** accessible interfaces must not weaken security (e.g., voice biometrics must be spoofing-resistant; accessible OTP must not read the code aloud).
- **Compliance & regulation:** accessibility is a *regulatory* compliance line (Equality Act, Section 508, EN 301 549); it is tested by regulators and civil society.
- **Reference architecture:** the reference architecture includes *accessibility as a non-negotiable design constraint*; no digital channel can be released without an accessibility-by-design gate.

## 7. Banking / financial-services context 💳
A UK retail bank’s card-management app (2022) received a formal complaint: the customer’s daughter (living infirm) could not use the app because the trade-execution flow required precise touch targeting. The app’s design system used 29 `div` elements where a `button` was needed; the `div` had no `role`, `aria-label`, or `tabindex`. The engineering team rewrote the component library over two sprints, but the regression testing did not include screen-reader tests.

A richer example: a bank’s mortgage-approval portal uses a *chart-heavy* property-valuation view. Blind customers with screen readers hear: “chart, chart, chart.” The EA mandates an alternative payload: a plain-text property summary (address, price, trend) plus an audio description of the chart’s *narrative* (not pixel data). The voice interface ("Speak to your mortgage") is not a substitute for the written contract—it is an *access route*.

Under the UK *Age-Appropriate Design Code* (launched September 2025), a bank’s app that serves users under 18 must treat accessibility as a legal *age-appropriate* requirement.

## 8. Reference architecture / worked example
**Problem:** A UK wealth-management platform needed a new mobile app for private clients. The legacy design system failed WCAG 2.1 AA audit: 34% of form controls were `div`-based; color-contrast ratios were 3.1:1 (failing 4.5:1); keyboard-trap bugs in the complex trade-execution flow; no `aria-label` on the “verify PII” flow.

**Decision:** Built an accessible-by-design design system with these rules:
1. Every interactive element is a `<button>` or `<a href>` with `aria-label`, `:focus` styles, and `tabindex`.
2. All design-token colors compute contrast; values < 4.5:1 are rejected in Storybook.
3. Every API response includes a `meta.accessible` field with alt-text, semantic summary, and voice-friendly transcript.
4. The trade-execution flow uses a *progressive disclosure* pattern: step-by-step with explicit confirmations and a persistent "Back" button.
5. All PDFs are generated in PDF/UA; audio statements are generated on the server via text-to-speech with a high-quality voice model.

**ADR:**
```markdown
# ADR-355: Accessible-by-Design Mobile Wealth-Management App
## Status
Accepted
## Context
Legacy screen-reader audit failed: 34% div-based controls, 3.1:1 contrast, keyboard traps in trade flow, no alternative-format generation.
## Decision
- Redesign component library: button/aria-label/focus rules; all new components must pass axe on <15 min.
- CI: axe + Lighthouse as blocking gates; disable merge on new violations.
- Add `meta.accessible` to every JSON/XML API response (alt-text, semantic summary, voice-transcript).
- Generate PDF/UA and audio statements server-side; expose via `?format=audio`.
- Quarterly accessibility officer review of vendor contracts.
## Consequences
- Positive: WCAG 2.1 AA audit passed; 40% reduction in accessibility complaint backlog.
- Negative: 6-week redesign, €1.8M; 3rd-party reporting tools (Chart.js) required SV-rebuild for screen-reader support.
- Negative: audio file generation adds 200ms to statement-delivery latency.
## Alternatives considered
1. Outsource accessibility audit after launch. → Rejected: Equality Act notice risk; £3.1M post-fix cost.
2. Use a white-label accessible fintech app. → Rejected: brand dilution; no client data ownership.
3. Progressive enhancement only on critical flows. → Rejected: mortgage and credit-card compliance line now fails audit.
```

## 9. Maturity & adoption signals
- **Adopt when:** EU/UK/US regulatory requirements mandate WCAG; or >15% of the customer base is registered disabled (in the UK, ~16%).
- **Anti-signals (don't adopt yet):** no customer-facing digital channel; no procurement requirement; no customer data about impairment access.
- **Common failure modes:** (1) treating accessibility as a “checklist sprint” after launch (too late, too expensive); (2) relying on design-system defaults that pass axe but have keyboard-trap *flows* (e.g., modal traps); (3) vendors who pass wcag audit but lack an alternative-format generation service.

## 10. Common confusions — the "don't mix" up list
| Often confused | Real distinction |
|----------------|------------------|
| **Accessibility** vs **Usability** | Accessibility = usable by impaired users; usability = efficient/pleasant for all. |
| **Accessibility** vs **Inclusive design** | Inclusive design = design for all (situational, cognitive, linguistic); accessibility = legal baseline. |
| **Semantic HTML** vs **CSS** | Semantic HTML = meaning for assistive tech; CSS = styling (can disable copy-paste or keyboard). |
| **WCAG 2.1 AA** vs **Section 508** | WCAG = criterion; Section 508 = US procurement law mandating standards that reference WCAG. |
| **Alt-text** vs **Descriptive link text** | Both close accessibility gaps, but alt-text is for images; single-word "click here" is inaccessible. |
| **Voice interface** vs **Screen reader** | Voice = proactive spoken system (Azure, Alexa); screen reader = reactive text-to-speech for DOM content. |
| **PDF** vs **PDF/UA** | PDF = any PDF; PDF/UA = accessible PDF with reading-order, tags, and alt-text. |

## 11. Tools & standards to know
- **Standards/Frameworks:** WCAG 2.1, WCAG 2.2, Section 508 (US), EN 301 549 (EU), Equality Act 2010 (UK), Age-Appropriate Design Code (UK 2025), IAB/WCAG 2.1, ISO 9241 (ergonomics), Web Accessibility Course (W3C).
- **Common tooling:** axe (Deque), Lighthouse (Chromium), axe-core (CI), Deque + Jigsaw, Accessibility Insights (Microsoft), TalkBack (Android), VoiceOver (iOS), JAWS + NVDA (Windows screen readers), Flow as a Service (FaaS for PDF generation)? no, use Apache FOP / WeasyPrint for PDF/UA; text-to-speech (Microsoft Azure), Canva / Adobe Express (accessible design), Figma + Stark (design-token contrast), Storybook + Storybook-addon-a11y, Confluence + Grok (accessibility officer wiki), Kotlin Multiplatform (mobile with semantic components), React-ARIA, Vue Accessibility Program.
- **Mandatory reading:** “Designing for Real People” — Ben Shneiderman; “Information For All People” (W3C); British Standard BS 8878 (Web accessibility code of practice).

## 12. ADR template (ready to fill in)
```markdown
# ADR-XXX: <decision>
## Status
Accepted | Proposed | Deprecated

## Context
...

## Decision
...

## Consequences
- Positive ...
- Negative ...
- ...

## Alternatives considered
1. ...
2. ...
```

## 13. Practice — apply it
1. **Recall:** define accessibility in 2 minutes without notes, citing the Equality Act or Section 508.
2. **Model:** draw an accessible-by-design design system diagram with ARIA roles, focus states, and alternative-format generation.
3. **ADR:** write a decision to block a component library update that removes `aria-label` from a form for “concise” code.
4. **Defend:** role-play a board where the CIO wants to shortcut WCAG 2.1 AA to ship faster; the CRO is the Accessibility Officer.

## 14. Summary (1 paragraph)
Accessibility is not a retrofit; it is the design-system baseline for every bank’s digital and physical channels. A customer with a visual impairment should not need a workaround to apply for a mortgage, a consumer with motor impairments should not need a personal assistant to move money, and a blind user should not be denied access to a basic account summary. The architect who treats accessibility as a “nice-to-have compliance document”—rather than as a *first-class, non-negotiable quality attribute*—produces the most damaging and costly asset in a bank’s portfolio: a system that is, in practice, a gated community.
