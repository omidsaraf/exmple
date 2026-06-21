# 01 - Gameplan (master plan)

The program spine: who/why, the non-negotiable principles, the locked decisions, the phases (P, 0-18) each with
an entry and exit gate, the timeline, and the status table. Strategy lives here; deep how-to lives in 02-09.

## 1. Context (fill per engagement)
| Field | Value |
|---|---|
| Organisation | <national health/audiology provider, AU> - sensitive health data |
| Compliance | Privacy Act 1988 (APPs + NDB Part IIIC), My Health Records Act, ISO 27001 alignment |
| Residency | Australia only - AU East (primary), AU Southeast (DR). Enforced by Azure Policy |
| Source | Azure Synapse (Serverless SQL + ADLS Gen2; Dedicated pool only if it exists - confirm in Discovery) |
| Target | Microsoft Fabric (Lakehouse, Pipelines, Notebooks, Eventstream; Warehouse = exception only) |
| Control plane | Azure SQL Database (enforced PK/FK/UNIQUE/CHECK + IDENTITY) - NOT the Fabric Warehouse |
| Runtime | Fabric Runtime 1.3 (Spark 3.5 / Python 3.11 / Delta 3.2) |

## 2. Principles (non-negotiable)
1. **Fabric-native, rationalise not lift-and-shift** - redesign every asset; never port Synapse patterns 1:1.
2. **Metadata-driven** - one generic runner per source family; onboarding = config; no hand-built per-flow pipeline.
3. **Medallion** - Bronze (raw) -> Silver (conformed) -> Gold (modelled/served), Delta in OneLake.
4. **One store** - OneLake; no external ADLS in steady state (shortcuts are a named exception).
5. **Control plane is enforced storage** - meta.*/log.* in Azure SQL DB (Fabric Warehouse does not enforce constraints).
6. **Idempotent by design** - every pipeline/notebook/script is safely re-runnable.
7. **Never DROP in prod** - rename + archive; migrations are non-destructive.
8. **Least privilege** - no wildcard grants, ever; PHI restricted below Gold too.
9. **AU residency enforced** - Azure Policy denies out-of-region resources.
10. **FinOps by design** - size from telemetry, pause non-prod, cost the whole bill (not just CU).
11. **Single source of truth + generators** - manifest in; seeds/DDL/views generated + drift-gated.
12. **Evidence over claims** - reconciliation (rows + SUM/checksum + SCD2) gates every migrated object.
13. **No manual metadata, no AI footprint** - all meta.* via CI/CD; AI prepares locally, the owner applies.

## 3. Locked decisions (the closed rules - detail + ADR in 02-08)
| Concern | Decision |
|---|---|
| Control plane | Azure SQL DB for meta.*/log.* |
| Serving | Tables in the lakehouse; serving VIEWS in the lakehouse's SQL analytics endpoint - NO separate Warehouse (exception only, for writable T-SQL over shortcuts) |
| Gold views | `[domain]_VIEW` (consumption, PHI omitted = CLS) + `[domain]_TECH_VIEW` (full), exact table name (no v_), per layer |
| Row security | Group-only RLS (IS_MEMBER of domain groups), auto-generated; mapping-table RLS only if a flow needs per-row scoping |
| Direct Lake security | semantic-model RLS/OLS (Direct Lake bypasses views) keyed to the same Entra groups |
| Ingestion | default path origin->Bronze->Silver->Gold->serving through the framework; 7 documented exceptions (02 section 3) |
| Source families | one generic runner per family (Dataverse / F&O OData / SQL table / file-landing / REST / object-store / streaming) |
| Orchestration | DAG -> 3 layer batches -> jobs -> procs; two flat ForEach loops only (never nested); admission control |
| Conformed dims | dim_date + public_holiday are GENERATED/seeded (not ingested); date_key = yyyymmdd; no SCD2 |
| Reproducibility | repos are the source of truth; rebuild by running CI/CD; config-per-target (capacity_mode trial/paid) |
| Capacity | validate on the trial first, size paid F-SKUs from telemetry; F64 decided by Power BI viewer licensing |
| Repos | docs / platform (infra + framework + control-plane) / sql (warehouse serving) / dataflows / bi |
| Operating model | no manual metadata (via CI/CD); no AI footprint; AI prepares local, owner reviews + syncs + runs; cloud read-only via the owner |

## 4. Phases (P, 0-18) - each with entry/exit gates
> Build in order, behind each exit gate. Each phase produces four governance docs (implementation, finops, risk,
> runbook) + a DSD (09). A phase is "done" only when its exit gate is evidenced and the docs are accepted.

| # | Phase | Objective | Exit gate (evidenced) |
|---|---|---|---|
| P | Pilot on Trial | prove the thin-slice framework end to end on the free trial; produce the F-SKU recommendation | parity on the slice (rows+SUM+SCD2) · CU telemetry under representative (F64) load · capacity recommendation signed off |
| 0 | Business Case & Mobilisation | sponsor, funding, benefits, governance, RACI | steering sign-off on business case + roadmap |
| 1 | **Discovery & Assessment** | read-only inventory of the Synapse estate: objects, volumetrics, update patterns, lineage, families; requirements gathering | machine-readable source + platform dictionaries (one per object) accepted; requirements baselined |
| 2 | Target Operating Model | self-service dataflow model, roles, ownership boundaries | operating model signed off |
| 3 | Enterprise Architecture | domains, workspaces, capacity topology, networking, residency | architecture board sign-off |
| 4 | Platform Foundation | IaC: capacity, workspaces, lakehouses, control SQL, KV, identity, environments | rebuild-from-repo dry-run green; smoke test passes |
| 5 | Networking & Security | private endpoints, conditional access, KV-per-domain, PIM/break-glass, CMK decision | access matrix verified; security review passed |
| 6 | DevOps & CI/CD | repos, branch policies, pipelines, Fabric Git, deployment pipelines | Dev->Test promotion proven; gates enforced |
| 7 | Enterprise Data Architecture & Modelling | conformed model, Gold naming, serving design, dim_date | model + serving standard signed off |
| 8 | Data Platform Design | environments, test-data strategy (synthetic/de-identified), Spark/env config | non-prod data strategy approved (ADR) |
| 9 | **Metadata-Driven Framework** | the hardened control plane + generic runner + generators; the Wave-0 "green at load" gate | all objects ingest within SLA under concurrency; control-DB lock/latency within budget |
| 10 | Data Engineering Framework | the wheel, DE templates, scaffolder, per-family benchmark | framework GA; onboarding = config proven |
| 11 | Migration Factory | dictionary -> seeds generator; per-object register/state machine | factory produces onboarded objects from dictionaries |
| 12 | Migration Execution | wave-by-wave: parallel run -> validate -> cutover -> per-object decommission | each wave reconciled + 30-day hypercare clean |
| 13 | Testing & Validation | SIT/UAT, performance, security, reconciliation | all suites green; UAT signed off |
| 14 | Observability & Operations | monitoring, alerting, incident runbooks, ops dashboard | SLAs instrumented; on-call ready |
| 15 | FinOps | chargeback, reserved-capacity decision, cost dashboards | cost model validated against telemetry |
| 16 | AI & Future State | ML use case (lawful basis first), feature store | use case + lawful basis approved (CTO/HREC) |
| 17 | Cutover & Hypercare | final cutover + 30-day hypercare | Synapse decommissioned after clean hypercare |
| 18 | Final Deliverables | handover, runbooks, lessons | program closure accepted |

## 5. Pre-flight checklist (before Phase P)
- [ ] Tenant + admin to create groups/SPs confirmed; AU East available; trials remaining noted (max 5/tenant)
- [ ] Named activator with Fabric Admin role; budget ceiling (R-19) agreed for the sizing test
- [ ] Repos created (06); environment-identity file filled (local, gitignored)
- [ ] Pipeline-minute capacity arranged (self-hosted agent or parallelism grant) - else CI cannot run

## 6. Timeline (indicative - refine against Discovery)
P 4w · 0 2w · 1 4w · 2 3w · 3 3w · 4 4w · 5 4w · 6 3w · 7 3w · 8 2w · 9 4w · 10 3w · 11 3w · 12 20w (long pole,
overlaps testing) · 13 12w · 14 4w · 15 6w · 16 6w · 17 4w · 18 2w. Migration execution (12) is the critical path.

## 7. FinOps summary (program-level)
Trial = $0. Paid F-SKUs sized from Phase-P telemetry (05). Whole bill includes control SQL DBs (per env),
Key Vaults (per domain x env), private endpoints, Purview, storage/egress, Log Analytics, and ADO pipeline
parallelism - not only Fabric CU.

## 8. Status table (the authoritative actuals)
| Phase | Status | Last updated |
|---|---|---|
| P | not started | - |
| 0-18 | not started | - |
> Update this row-by-row as phases close; each entry cites the evidence (run IDs, recon results, sign-off).
