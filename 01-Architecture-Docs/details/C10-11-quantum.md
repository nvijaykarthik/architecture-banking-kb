# [C10-11] Quantum Computing — DETAIL
> **Category:** C10 — Emerging & Advanced Topics · **Difficulty:** ○/◑/● · **Banking-relevant:** maybe
>
> **Companion brief:** `[briefs/C10-11-quantum.md](../briefs/C10-11-quantum.md)`
>
> **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.
>
> ---
>
> ## 1. Precise definition
> Quantum computing is an emerging computing paradigm that performs calculations using quantum bits (qubits) and quantum mechanical phenomena—superposition (qubits can be 0 and 1 simultaneously), entanglement (correlations between qubits stronger than classical), and interference (encoding data into wave-like states to amplify correct answers while canceling incorrect ones). In banking, the primary threat is cryptanalysis: Shor's algorithm can break RSA and elliptic-curve cryptography (ECC), which underpin digital signatures and key exchanges in secure financial messaging (SWIFT, TLS).
>
> ## 2. Why it exists (problem it solves)
> Classical supercomputers are bounded by Moore's law and Von Neumann architecture: adding transistors yields linear gains, while quantum mechanics yields exponential speedups for specific problems. Banks face two distinct challenges: (A) optimization problems (portfolio optimization, credit risk aggregation, fraud pattern detection) that are tractable on quantum computers with fewer qubits; and (B) cryptanalysis, where Shor's algorithm factors large integers in polynomial time and breaks RSA/ECC. For banks, the second problem is an existential threat to the security model: RSA/ECC underpins every TLS session, SWIFT message, and digital signature; a quantum adversary with a sufficiently large qubit array and error-corrected coherence could decrypt years of archived financial data.
>
> ## 3. Core concepts & vocabulary
> | Term | Precise meaning |
> |------|-----------------|
> | Qubit | The quantum analog of a classical bit; exists in a superposition of 0 and 1 until measured. |
> | Coherence / T1 (relaxation) and T2 (decoherence) | Qubits lose their quantum state over time; critical for error correction. |
> | Superposition | A qubit can be in multiple states simultaneously; a n-qubit system spans 2^n states. |
> | Entanglement | Two or more qubits correlated such that measuring one instantly determines the other. |
> | Interference | Encoding data into wave-like states (wavefunctions) to amplify correct answers and cancel incorrect ones. |
> | Surface Code / Topological Codes | Error-correction schemes for protecting logical qubits from physical qubit errors. |
> | NISQ / Noisy Intermediate-Scale Quantum | Current generation of quantum processors (50-1000 noisy physical qubits) without full error correction. |
> | Quantum Supremacy | The point where a quantum processor solves a problem infeasible for classical supercomputers. |
> | Quantum Advantage | A quantum processor solving a real problem significantly faster than the best classical algorithm. |
> | Shor's Algorithm | Quantum algorithm for factoring large integers; breaks RSA. |
> | Grover's Algorithm | Quantum search algorithm; quadratic speedup for unstructured search (2^n to 2^{n/2}). |
> | Post-Quantum Cryptography (PQC) | Classical algorithms resistant to quantum attacks; NIST standardized CRYSTALS-Dilithium (signatures), CRYSTALS-Kyber (key exchange), FALCON, SPHINCS+. |
> | Harvest Now, Decrypt Later | An adversary records encrypted data now (e.g., 20-year loan defaults) and decrypts it later with a quantum computer. |
>
> ## 4. How it works (architecture / mechanism)
> ### 4.1 Diagrams
> **Diagram A — Core structure (highlight load-bearing parts = amber, supporting = grey):**
>
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
>     classDef context fill:#dfe6e9,stroke:#636e72
>     classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
>     classDef ok fill:#a7f3d0,stroke:#065f46
>     classDef service fill:#bfdbfe,stroke:#1e40af
>
>     CLASS[Classical Bank]:::context
>    QC[Quantum Co-Processor]:::critical
>    PQC[PQC-Ready Crypto]:::decision
>    RISK[Risk Optimization]:::service
>    ROUTE[Route Optimization]:::service
>    ARCHIVE[Data Archive]:::critical
>
>     CLASS -->|instant reward| PQC
>     CLASS -->|run| RISK
>    CLASS -->|run| ROUTE
>     CLASS -->|archive| ARCHIVE
>    QC -->|simulate| RISK
>    QC -->|simulate| ROUTE
>    QC -->|record| ARCHIVE
> ```
>
> **Diagram B — Cryptographic threat landscape (highlight decision = green, risk = red):**
>
> ```mermaid
> flowchart LR
>     classDef ok fill:#a7f3d0,stroke:#065f46
>     classDef risk fill:#fecaca,stroke:#991b1b
>     classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
>
>     DATA[Legacy Encrypted Data]:::critical
>    DAY[Adversary]:::risk
>    QUANTUM[Quantum Computer]:::critical
>    PQC[PQC Switch]:::decision
>   RISK[Harvest Now]:::decision
>    MITIGATE[Migrate / Re-encrypt]:::ok
>
>    DAY -->|store| DATA
>    QUANTUM -->|decrypt| DATA
>    DAY -->|decrypt later| QUANTUM
>    PQC -->|mitigate| MITIGATE
> ```
>
> ## 5. Variants, options & trade-offs
> | Variant | When to pick | When to avoid | Key trade-off axis |
> |---------|--------------|---------------|--------------------|
> | PQC-first migration | All asymmetric cryptography (TLS 1.2/1.3, code-signing, key exchange) | Nothing; PQC is the only defense against a quantum adversary | Migration burden vs. irreversible risk |
> | Quantum-simulation on cloud | Monte Carlo, risk optimization, fraud detection with near-term >= 100 qubits | If the problem is simple enough for classical HPC | Cost vs. speedup |
> | Full-blown quantum (10^5+ qubits) | Long-term (10+ years) risk register; strategic long-period decisions | No immediate quantum access; too expensive | Future-proofing vs. current spend |
> | Hybrid (classical + quantum co-processor) | Real-world for latency & security; quantum for specific sub-problems | Requires significant MLOps and hybrid architecture | Latency vs. quantum benefit |
>
> ## 6. Relationships to sibling topics
> - **Event-Driven Architecture (C10-02):** Quantum-resistant cryptography is a subset of the event-driven security/encryption layer.
> - **Zero Trust (C10-06):** Quantum-safe TLS is a zero-trust enforcement point.
> - **API Economy (C10-05):** All API security is at risk; PQC must be enforced at the API gateway.
>
> ## 7. Banking / financial-services context 💳
>
> A global bank has identified 2 petabytes of encrypted data (loan defaults, derivatives exposure, SWIFT messages) that must be retained for 20+ years under Basel/trading regulations. The "harvest now, decrypt later" threat means an adversary with a 4-qubit-single logical can decrypt decades-old data. The bank is migrating asymmetric RSA/ECC to NIST PQC (CRYSTALS-Dilithium for signatures, CRYSTALS-Kyber for key exchange).
>
> The bank is also evaluating Google's 433-qubit (2023), 1500-qubit (2024) machines for grid-fitting portfolio optimization and credit-risk aggregation (Monte Carlo), but this is still research-stage.
>
> The bank's quantum strategy is to:
> 1. Cryptographic agility: design the key-exchange pipeline to allow PQC swap.
> 2. Data re-encryption: re-encrypt long-arc archives with PQC-compatible keys.
> 3. Risk modeling: evaluate the "qubit-to-bank" ratio for each asset class.
>
> ## 8. Reference architecture / worked example
>
> **Problem:**
> A bank encrypts all sensitive financial data (customer PII, account balances, records) with RSA-2048/ECC-256. A new quantum adversary (nation-state) has demonstrated a 4-qubit single-logical machine capable of factoring 1024-bit integers. The 20-year retention policy means this data is at risk.
>
>
> **Decision:**
> 1. Immediate migration of asymmetric cryptography to NIST PQC.
> 2. Re-encryption of 2-year-old data with PQC.
> 3. Design the key-management pipeline to be cryptographically agile.
>
>
> ```mermaid
> graph LR
>     classDef service fill:#bfdbfe,stroke:#1e40af
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
>     classDef context fill:#dfe6e9,stroke:#636e72
>     classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5,color:#64748b
>     classDef ok fill:#a7f3d0,stroke:#065f46
>     classDef data fill:#fde68a,stroke:#92400e
>
>     CLASS[Classical Bank]:::context
>    KEY[Key Management]:::critical
>    PQC[PQC Engine]:::decision
>    DATA[(Encrypted Data)]:::data
>    ADVERSARY[Quantum Adversary]:::critical
>    CRYPTO_AGILITY[Crypto Agility Pipeline]:::boundary
>    
>     ADVERSARY -->|harvest now| DATA
>     CRYPTO_AGILITY -->|re-encrypt| DATA
>    KEY -->|sign| PQC
>     PQC -->|protect| DATA
>     CLASS -->|store| DATA
> ```
>
>
>
>
> **ADR drafted:**
>
> ```markdown
> # ADR-2025-084: Quantum-Safe Crypto Migration
>
> ## Status
> Proposed
>
> ## Context
> A nation-state attacker demonstrated a qu adult. A quantum single-logical bit (1 qubit) machine can factor legacy RSA-2048; 2 Petabytes of 20-year-old financial data are at harvest-now-decrypt-later risk.
>
>
> ## Decision
> Immediately migrate all asymmetric cryptography (TLS, SWIFT signing, code-signing) to NIST PQC (CRYSTALS-Dilithium, CRYSTALS-Kyber).
>
>
> ## Consequences
> - Positive: 1) 100% cryptographic resilience to future quantum adversaries; 2) Aligns with FedRAMP 2024 guidelines; 3) Reduces "compatibility" debt.
> - Negative: 1) 15% API throughput decline on PQC; 2) PQC key sizes are 2x-4x larger; 3) Requires HSM recertification.
>
>
> ## Alternatives considered
> 1. 1) Wait for full quantum computers: Rejected (risk is 100%).
> 2. 2) Add more classical crypto: Rejected (not quantum-resistant).
> ```
>
> ## 9. Maturity & adoption signals
> - **Adopt when:** Asymmetric cryptography is used everywhere (TLS, code-signing, key exchange); data retention > 10 years; quantum competitor exists; NIST PQC is adopted by FedRAMP.
> - **Anti-signals (don't adopt yet):** No long-arc data retention; no quantum competitor; cost > benefit.
> - **Common failure modes:** "Quantum theater" (overselling quantum speedups without a concrete use case); insufficient key-escrow for PQC keys; ignoring Grover's algorithm doubling key requirements for symmetric crypto.
>
>
> ## 10. Common confusions — the "don't mix" up list
>
> | Often confused | Real distinction |
> |----------------|------------------|
> | Quantum Supremacy vs Quantum Advantage | Supremacy is a benchmark; advantage is practical. |
> | Qubit vs Classical Bit | Qubit is quantum; bit is classical. |
> | Quantum vs Classical | Quantum is probabilistic; classical is deterministic. |
>
> ## 11. Tools & standards to know
> - **Standards/Frameworks:** NIST SP 800-38F (PQC); NIST PQC competition (2024); NIST SP 141|1; NIST PQC Interim Guidance; 5G NR and 5G (5G NR Total Cost of Ownership) on quantum; ISO/IEC 27001 A.12. characterization; NIST SP 800-197; NIST SP 800-37 (Risk Management Framework) on hardware security (PUF); NIST SP 800-193|2022 COVID-19 (201); FedRAMP (2024) on quantum readiness; NIST SP 800-160 (V&V of quantum systems).
> - **Common tooling:** Amazon Braket, Azure Quantum, IBM Quantum, AWS Three-State (IoT), H2O.ai; GROVER's algorithm is supported by QuS; QGIS; Quark; SQL Server; Intune; OpenAI; Google Cloud; Azure; AWS.
>
> [Tool details not included - truncated]
> ```
