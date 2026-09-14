# [C10-08] AI/ML Architecture — DETAIL
> **Category:** C10 — Emerging & Advanced Topics · **Difficulty:** ●/◑/○ · **Banking-relevant:** yes
>
> **Companion brief:** `[briefs/C10-08-ai-ml-arch.md](../briefs/C10-08-ai-ml-arch.md)`
>
> **Target reader:** enterprise architect who must *explain, justify, and defend* the topic — not just recite it.
>
> ---
>
> ## 1. Precise definition
> AI/ML Architecture is the structural and operational pattern for deploying machine learning models at scale, combining data engineering (feature stores, data pipelines), model training and serving (training pipelines, inference servers), MLOps (CI/CD for models, monitoring, drift detection), and governance (model registries, explainability, regulatory compliance). It bridges the gap between data science experimentation and production software by treating models as first-class code artifacts with their own lifecycle, versioning, and observability.
>
> ## 2. Why it exists (problem it solves)
> Banks historically built ML as a one-off or batch process: a data scientist writes a notebook, the team manually deploys a model to a reporting dashboard, and there is no mechanism for retraining, monitoring, or governance. This leads to model decay, regulatory non-compliance (SAS 90, SR 11-7), and the inability to respond to adversarial fraud patterns within hours. An AI/ML architecture institutionalizes the training-minimizing pipeline (e.g., daily, weekly, or event-driven) and enforces governance at every stage.
>
> ## 3. Core concepts & vocabulary
> | Term | Precise meaning |
> |------|-----------------|
> | MLOps (Machine Learning Operations) | The discipline and tooling that automates the deployment, monitoring, and retraining of ML models; extends DevOps principles to the model lifecycle. |
> | Feature Store | A centralized, versioned repository for features used in both training and inference; enforces training-inference consistency. |
> | Model Registry | A versioned catalog of trained models with metadata (accuracy, lineage, owner, model card) and deployment status. |
> | Training-Inference Skew | The difference between features served at inference and those used during training; caused by feature store drift or schema changes. |
> | MLOps Pipeline (ELSA / CRISP-DM) | The MLOps equivalent of CI/CD: Data Validation → Feature Engineering → Model Training → Model Evaluation → Model Deployment → Monitoring. |
> | ML Observability (e.g., WhyLogs, Evidently, Seldon Monitoring) | Frameworks/Tools for monitoring model prediction distributions, input drift, and data quality. |
> | Explainable AI (XAI) / Interpretability | Techniques (SHAP, LIME) or constraints (monotonicity, fairness) that make model predictions auditable and explainable. |
> | Model Cards / Datasheets for Datasets | Structured documentation of model performance, intended use, limitations, and governance—required for model risk oversight. |
>
> ## 4. How it works (architecture / mechanism)
> ### 4.1 Diagrams
> **Diagram A — Core structure (highlight load-bearing parts = amber, supporting = grey):**
> ```mermaid
> graph TD
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
>     classDef context fill:#dfe6e9,stroke:#636e72
>     classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
>     classDef ok fill:#a7f3d0,stroke:#065f46
>     classDef service fill:#bfdbfe,stroke:#1e40af
>
>     RAW[Raw Data]:::context
>    FEAT[Feature Store]:::service
>     TRAIN[Training Pipeline]:::context
>    MODEL[Model Registry]:::critical
>    INF[Inference API]:::service
>    MON[ ML Observability]:::ok
>
>     RAW -->|ingest| FEAT
>     FEAT -->|train| TRAIN
>     TRAIN -->|evaluate| MODEL
>     MODEL -->|deploy| INF
>     INF -->|monitor| MON
>     MON -->|retrain| TRAIN
> ```
>
> **Diagram B — Model Lifecycle with governance (highlight decision = green, risk = red):**
> ```mermaid
> flowchart LR
>     classDef ok fill:#a7f3d0,stroke:#065f46
>     classDef risk fill:#fecaca,stroke:#991b1b
>     classDef decision fill:#a3e634,stroke:#3f6212,stroke-width:1px
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
>
>     START[Data Ingestion]:::ok
>    VALID[Schema Validation]:::ok
>     TRAIN[Model Training]:::context
>    EVAL[Model Evaluation]:::decision
>    APPROVAL[Model Risk Committee]:::decision
>    ACTIVATE[Model Activation]:::ok
>    DEPRECATE[Model Deprecation]:::risk
>    REJECT[Model Rejection]:::risk
>
>    START --> VALID
>    VALID -->|pass| TRAIN
>    TRAIN -->|train complete| EVAL
>    EVAL -->|meets thresholds| APPROVAL
>   EVAL -->|fails thresholds| DEPRECATE:::risk
>
>    APPROVAL -->|approved| ACTIVATE
>    APPROVAL -->|rejected| REJECT:::risk
> ```
>
> ## 5. Variants, options & trade-offs
> | Variant | When to pick | When to avoid | Key trade-off axis |
> |---------|--------------|---------------|--------------------|
> | Retriable MLOps (Batch / Scheduled) | Monthly or daily batch retraining (credit scoring, customer segmentation) | Real-time fraud with < 50 ms latency | Latency vs. freshness |
> | Stream MLOps (Online / Real-Time) | Event-driven fraud detection, algorithmic trading, real-time risk | Highly regulated models requiring full audit trail | Complexity vs. speed |
> | On-Prem / Air-Gapped MLOps | Strict data residency, sensitive PII, regulatory constraints | Managed cloud-native serving | Control vs. flexibility |
> | Hybrid (Batch + Shadow) | Risk of production drift; need canary deployment | Small teams without MLOps expertise | Safety vs. speed |
>
> ## 6. Relationships to sibling topics
> - **Feature Store (within MLOps):** Acts as a data product between data pipeline and model registry; the "right contract" for every model.
> - **Monolith (C10-01):** Monolithic MLOps pipelines mix training and serving in one codebase; functional but not scalable or independently deployable.
> - **API Gateway (C10-05):** The inference model is served through an API gateway with rate limits, authentication, and cost tracking.
>
> ## 7. Banking / financial-services context 💳
> A global investment bank runs three MLOps pipelines: a fraud-scoring model (real-time, SHAP explanations, weekly retraining), a credit-default prediction model (daily, SAS 90-compliant artifact, model card), and a trade-routing model (monthly, reinforcement learning, with bandit experiment logs). All models are registered in a model registry with full lineage (data source → feature pipeline → training run → evaluation → deployment), and every prediction is write-locked for 7 years for regulatory audit (DORA, Basel III).
>
> ## 8. Reference architecture / worked example
> **Problem:** A retail bank's fraud model predictions were stale because the feature store updated 24 hours after label feedback, and the model was retrained only by a manual data science ticket.
>
> **Decision:** Implement an MLOps pipeline with nightly batch retraining, automated drift prevention (schema validation in feature store), and real-time inference with SHAP explanation.
>
> ```mermaid
> graph LR
>     classDef service fill:#bfdbfe,stroke:#1e40af
>     classDef critical fill:#ffe66d,stroke:#b8860b,stroke-width:2px
>     classDef context fill:#dfe6e9,stroke:#636e72
>     classDef boundary fill:#f1f5f9,stroke:#475569,stroke-dasharray: 5,color:#64748b
>     classDef data fill:#fde68a,stroke:#92400e
>
>     FEAT[Feature Store]:::service
>     TRAIN[Training Pipeline]:::context
>     REG[Model Registry]:::critical
>     INF[Inference API]:::service
>     MON[ drift monitor]:::context
>     LOG[(Audit Log)]:::data
>     XAI[SHAP Explainer]:::service
>     AUTH[API Gateway]:::boundary
>
>     FEAT -->|train| TRAIN
>     TRAIN -->|evaluate| REG
>    REG -->|deploy| INF
>    AUTH -->|protect| INF
>    INF -->|call| XAI
>    INF -->|log| LOG
>    MON -->|alert| INF
> ```
>
> **ADR drafted:**
> ```markdown
> # ADR-2025-073: MLOps Pipeline for Real-Time Fraud Scoring
> ## Status
> Accepted
> ## Context
> 2023 audit found 3 models deployed without lineage; fraud detection accuracy dropped 12% undetected due to training-inference skew.
> ## Decision
> Auto-retrain nightly; enforce feature store feature contracts; integrate SHAP to ML model container; write-lock predictions for 7 years.
> ## Consequences
> - Positive: Detection rate improved 15%; regulatory audit items reduced from 18 to 2.
> - Negative: MLOps platform costs $400k/year; needs 3 data science engineers.
> - ...
> ## Alternatives considered
> 1. Manual retraining only: Rejected (14-day lag).
> 2. On-prem only: Rejected (cloud cost savings > infra savings).
> ```
>
> ## 9. Maturity & adoption signals
> - **Adopt when:** > 3 production models; retraining needed > monthly; regulatory requirement for model card or lineage; MLOps team of >= 2.
> - **Anti-signals (don't adopt yet):** < 2 models; fully rule-based; no model risk oversight.
> - **Common failure modes:** Training-inference skew (largest reported cause); skipped model cards; prediction drift without monitoring; over-fitting to single data shard.
>
> ## 10. Common confusions — the "don't mix" list
> | Often confused | Real distinction |
> |----------------|------------------|
> | MLOps vs DataOps | MLOps = model lifecycle; DataOps = data pipeline reliability. |
> | Feature Store vs Data Vault | Feature store = feature repository; data vault = data architecture (Inmon). |
> | Real-time vs Batch MLOps | Real-time = online inference; streaming training; high cost and complexity. |
>
> ## 11. Tools & standards to know
> - **Standards/Frameworks:** SAS 90 (model risk management); SR 11-7 (strategic risk); PMBOK; CMMI; DORA ICT risk; ISO/SAE 21434 (cybersecurity for ML); IEEE 7003 (algorithmic bias.
> - **Common tooling:** Kubeflow, Seldon, KFServing, MLflow, Weights & Biases, DataRobot, H2O.ai, AWS SageMaker, Azure Machine Learning, Vertex AI; WhyLabs, Evidently AI, Fiddler, Arize; Seldon; SHAP, LIME; Weave; Great Expectations.
> - **Mandatory reading:** "Designing Machine Learning Systems" by Chip Huyen; "Machine Learning Engineering" by Andriy Burkov; "Building a Data Mesh."
>
> ## 12. ADR template (ready to fill in)
> ```markdown
> # ADR-XXX: <decision>
> ## Status
> Accepted | Proposed | Deprecated
> ## Context
> ...
> ## Decision
> ...
> ## Consequences
> - Positive ...
> - Negative ...
> - ...
> ## Alternatives considered
> 1. ...
> 2. ...
> ```
>
> ## 13. Practice — apply it
> 1. **Recall:** Define training-inference skew in 2 min without notes.
> 2. **Model:** Draw an MLOps topology with Data Pipeline → Feature Store → Model Training → Model Registry → Inference API.
> 3. **ADR:** Write an ADR for a model retraining policy using MLOps for a credit-scoring model.
> 4. **Defend:** Explain to a non-technical CRO why "model risk management" is a regulatory requirement, not a best practice.
>
> ## 14. Summary (1 paragraph)
> AI/ML Architecture is the operational backbone that makes machine learning trustworthy in banking: it enforces the chain of provenance from raw data to model prediction, monitors for drift, and provides the audit trail that regulators now require. It is not "data science"; it is the production software that makes ML legal, repeatable, and safe.
>
> ---
> **Status:** ✅ Created · **Last updated:** 2026-09-14
