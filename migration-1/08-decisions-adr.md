# 08 - Architecture Decision Records (one indexed document)

The locked decisions, distilled. Each has: decision, why, status. When a new decision is made, add a row here
(no scattered per-ADR files unless one grows large). Status: Accepted unless noted.

| ADR | Decision | Why |
|---|---|---|
| 01 | Microsoft Fabric is the target platform | managed lakehouse + pipelines + Direct Lake; consolidate Synapse + ADLS + Power BI |
| 02 | Medallion (Bronze/Silver/Gold), Delta | standard, reconcilable, Direct-Lake-ready |
| 03 | OneLake is the single store | one logical store; no external ADLS in steady state |
| 04 | Direct Lake default for Power BI | no import refresh; fastest; F64 free-viewer benefit |
| 05 | Metadata-driven pipelines (generic runner per family) | onboarding = config; pipeline count flat as objects scale |
| 06 | Typed watermark; config vs state | enforced correctness; meta.* config, log.* state |
| 07 | Terraform IaC (microsoft/fabric + azurerm/azapi) | reproducible; capacity via azapi |
| 08 | Azure DevOps + Fabric Git + Deployment Pipelines | branch-per-env promotion; gated |
| 09 | KV per domain per env; least privilege | blast-radius isolation; no wildcard grants |
| 10 | AU regions only; Azure Policy denies out-of-region | residency (health data) |
| 11 | Rationalise, not lift-and-shift | redesign each asset Fabric-native |
| 12 | 30-day hypercare before Synapse decommission; parallel run + recon mandatory | safe cutover with evidence |
| 13 | Purview governance (classification + sensitivity labels) | PHI/PII discoverable + labelled |
| 14 | PHI restricted below Gold too (Bronze/Silver = framework MI + break-glass only) | masking at Gold is not the whole control |
| 18 | Two flat ForEach loops only - never nested | avoids Fabric pipeline nesting limits; predictable concurrency |
| 19 | Fabric Warehouse uses standard T-SQL DDM (not Databricks MASK); GRANT UNMASK; no CREATE USER FROM EXTERNAL PROVIDER | verified; mask-at-Gold viable (used only in the Warehouse exception) |
| 20/31 | Dataverse: Link-to-Fabric default / generic Copy fallback / metadata-selected | zero-copy where possible; one generic Copy otherwise |
| 21/25 | Validate capacity on the trial first, then size paid F-SKUs; pilot-on-trial precedes paid spend | size from telemetry, not guesses |
| 22 | Control plane in Azure SQL DB (not the Fabric Warehouse) | needs enforced PK/FK/UNIQUE/CHECK + IDENTITY |
| 24 | Fabric Runtime 1.3 baseline | GA default (Spark 3.5 / Py 3.11 / Delta 3.2) |
| 26 | Pause non-prod capacity as the default cost lever | preserves data, stops compute billing |
| 28 | Encryption-at-rest key model (CMK vs MMK) - explicit decision + review trigger | do not leave undecided for a PHI platform |
| 29 | Test data: synthetic / de-identified, no raw PHI in non-prod | hard boundary (privacy) |
| 30 | De-identification standard + retention/disposal policy (Privacy/Legal sign-off) | "masked" != "de-identified"; honour erasure incl. time-travel |
| 33 | Metadata-driven column security (OneLake-first; Warehouse CLS/DDM/RLS fallback) | classification is data in meta, not knowledge in a head |
| 34 | Self-service dataflows: unique-id flows; metadata-only ingestion; template-driven transform | the operating model |
| 36/49 | Medallion storage: lakehouse per layer + bronze staging/main/archive; per-layer schema taxonomy; metadata-driven storage routing | no hardcoded abfss; one lakehouse per layer |
| 37/38 | Repo topology: one ADO project, five repos (docs/platform/sql/dataflows/bi); platform consolidates infra+framework+control-plane | split by lifecycle, not file type |
| 39 | Migration ingestion = direct source -> Fabric, never through Synapse (Synapse only = one-time backfill + parallel baseline) | retire Synapse cleanly |
| 41 | One generic runner per source family + per-family drift/admission; Copy-vs-notebook per family | scalable, uniform ingestion |
| 42 | One capacity per env; scheduled SKU scaling with guardrails; intraday workspace-shifting rejected; trial->paid = workspace reassignment | predictable capacity |
| 45 | Migration dictionaries + per-object register/state machine; dictionary -> seeds generator | "typing becomes reviewing" |
| 46 | Control-plane naming v1 (area prefixes df_/ing_/ext_; bare = cross-cutting) | consistent meta/log naming |
| 47 | Full-stack 3-layer parametric reproducibility (greenfield; capacity_mode trial->paid) | rebuild by running CI/CD |
| 50 | Platform CI/CD + dataflow onboarding reworked to the UDP-aligned model (single-purpose pipelines, manifest-only, isolation/contract gates) | trust + clarity; one project per PR |
| 51 | Serving FINAL: tables in the lakehouse, views in the lakehouse SQL analytics endpoint; NO separate Warehouse (exception only); dual BI path; Gold naming; exact-table-name views | simplest, no extra item, GA |
| 52 | All Fabric/control-plane object create/drop/modify via CI/CD; least privilege; drift detection | no manual changes; auditable |
| 53 | Gold view security: CLS by omission + group-only RLS, auto-generated by gen_views; mapping-table RLS only if per-row scoping needed | strongest CLS; zero DE burden |

> Operating-model decisions (no manual metadata, no AI footprint, prepare-local/owner-runs) live in 06 and are
> binding from Phase 1. The ingestion default-path closed rule (+ 7 exceptions) lives in 02.
