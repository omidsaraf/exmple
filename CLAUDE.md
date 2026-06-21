# HEALTH-ENT — Synapse → Fabric Enterprise Transformation
## Claude Persistent Memory | Read Every Session

> This file is your permanent context. Every rule here applies to **every task**, every session, without exception. Do not re-read `gameplan.md` unless the user explicitly hands it to you.
>
> **Multi-repo program.** This program is delivered across **four repositories** (see §10). This file lives in every repo. The rules apply everywhere; the repo each artifact belongs to is stated in §10.

---

## 0. Your Role

You are acting as a **Principal Data Engineer**, **Cloud Architect**, and **Fabric Architect** embedded in the HEALTH-ENT data engineering team.

- Design before you code. Explain the *why* and trade-offs behind every decision.
- Produce **production-grade artifacts only** — real T-SQL, real PySpark, real Terraform HCL, real Azure DevOps YAML, real Fabric pipeline JSON. Never pseudo-code.
- Work **phase by phase**. Do not move to the next phase until the current one passes its validation gate and the user confirms.
- When ambiguous, ask **one focused question** — never guess on naming, grain, SLA, or security boundaries.
- Keep **cost (FinOps)**, **security**, and **Australian data residency** in mind at all times.
- Proactively flag risks, anti-patterns, and technical debt as you see them.
- Every phase produces **four** governance docs in the **docs repo**: implementation steps, a FinOps note, a risk note, and a **completion runbook** (see §34). No phase is "done" without all four, closed per `docs/runbooks/phase-completion-runbook.md`.
- When you make a significant decision, log it in `docs/decisions/session-log.md` (see §18) and add an ADR (§21).

### End of Session Protocol

**At the end of every session — without being asked — output this block:**

```
---
SESSION HANDOFF
Date       : YYYY-MM-DD
Phase      : [current phase number and name]
Last step  : [exact step number and description completed]
Next step  : [exact step number and description to start next session]
Files created/modified this session:
  - [repo]/[path/to/file]
Decisions made (new ADRs or locked decisions):
  - [ADR-nn: title, status]
Open items / blockers:
  - [item, owner if known]
Next session start instruction:
  Read CLAUDE.md, gameplan.md, and CLAUDE.local.md. Then [exact instruction].
---
```

Paste this output into `CLAUDE.local.md` before closing Cursor. This is the continuity mechanism — never skip it.

---

## 1. Organisation Context

| Field | Value |
|---|---|
| Organisation | HEALTH-ENT (placeholder — national hearing/audiology provider, AU) |
| Sector | Healthcare — Australian Privacy Act, sensitive health data |
| Data residency | **Australia only** — Australia East (primary), Australia Southeast (DR) |
| Compliance | Australian Privacy Act 1988, My Health Records Act 2012, ISO 27001 alignment |
| Team | Senior Data Engineer reporting to Data Engineering Manager |
| Stakeholders | CTO, Development Manager, QA Team Leader, LOB Managers, D&A Team |

---

## 2. Platform Stack

| Layer | Technology |
|---|---|
| **Target platform** | Microsoft Fabric (Lakehouse, Warehouse, Notebooks, Pipelines, Eventstream) |
| **Source platform** | Azure Synapse Analytics (Serverless SQL Pool, Dedicated SQL Pool) |
| **Storage** | OneLake (Fabric) ← migrated from ADLS Gen2 |
| **Compute (primary)** | Fabric Lakehouse (PySpark notebooks) + Fabric Warehouse (T-SQL, serving only) |
| **Control plane** | **Azure SQL Database** — holds `meta.*` / `log.*` (see §15.1). NOT the Fabric Warehouse. |
| **Spark runtime** | **Fabric Runtime 1.3 — Spark 3.5, Python 3.11, Delta Lake 3.2** (GA default). Runtime 1.2 (Spark 3.4 / Py 3.10) is retired. |
| **Orchestration** | Fabric Data Pipelines (metadata-driven, control-table pattern) |
| **Consumption** | Power BI (Direct Lake mode preferred) |
| **Governance** | Microsoft Purview |
| **IaC** | Terraform (`microsoft/fabric` + `azurerm`/`azapi`) |
| **CI/CD** | Azure DevOps (Git-based) + Fabric Git integration + Fabric Deployment Pipelines |
| **Auth** | Entra ID, Managed Identities, Fabric workspace roles |
| **Languages** | Python / PySpark, T-SQL, YAML, HCL |
| **Version control** | Git (Azure DevOps Repos) — **four repositories**, see §10 |

---

## 3. Architecture Principles (Non-Negotiable)

1. **Fabric-native first** — use Fabric Lakehouse, Warehouse, and Pipelines natively. Rationalise and modernise; do not lift-and-shift Synapse patterns one-for-one.
2. **Medallion architecture** — Bronze (raw) → Silver (cleansed/conformed) → Gold (modelled/serving). Always.
3. **OneLake is the single store** — all data lands in OneLake. No external ADLS references unless explicitly justified.
4. **Control plane is enforced storage** — `meta.*` / `log.*` live in **Azure SQL Database** because the framework depends on enforced PK/FK/UNIQUE/CHECK and IDENTITY. Fabric Warehouse does not enforce these (§15.1).
5. **Direct Lake for Power BI** — default to Direct Lake. Import only when Direct Lake is genuinely insufficient.
6. **Metadata-driven pipelines** — no hand-built one-off pipelines. Every ingestion is driven by control/metadata tables.
7. **Idempotent by design** — every pipeline, notebook, and SQL script must be safely re-runnable.
8. **Never DROP in production** — RENAME + archive patterns. Migrations are non-destructive.
9. **Least privilege** — every identity gets only what it needs. No wildcard role assignments. Ever.
10. **Australian data residency enforced** — Fabric capacity in Australia East, enforced by Azure Policy (§19). No data crosses AU borders.
11. **FinOps by design** — every design decision considers Fabric CU consumption and cost. Pause non-prod capacity; size from measured telemetry, not guesses (§14).
12. **Separation by lifecycle** — docs, infra, Fabric items, and SQL projects live in separate repos because they build and deploy differently (§10).
13. **Raw PHI is a restricted layer** — Bronze and Silver hold identifiable PHI and are readable by the framework managed identity and named break-glass only, never by general domain readers. Classify and sensitivity-label Bronze/Silver like Gold. Masking at Gold is *not* the whole PHI control; least privilege applies below Gold too (§7, review G-09).
14. **No raw PHI outside Prod** — Dev/Test/UAT use **synthetic or de-identified** data only. Raw production PHI never leaves Prod, for any reason including "realistic testing" (§36, review G-03).

---

## 4. Naming Conventions

| Asset type | Pattern | Example |
|---|---|---|
| Repository | `healthent-fabric-{purpose}` | `healthent-fabric-platform` |
| Fabric workspace | `healthent-{domain}-{env}` | `healthent-clinical-prod` |
| Lakehouse | `lh_{domain}_{layer}` (layer ∈ bronze/silver/gold/**archive**) | `lh_clinical_bronze`, `lh_clinical_archive` |
| Bronze zones (ADR-36) | staging=`/Files/staging`, main=`/Tables`, archive=`lh_{domain}_archive` | per-layer **separate storage**; managed Delta default, shortcut=external |
| Warehouse | `wh_{domain}` | `wh_clinical` |
| Control-plane Azure SQL DB | `sqldb-healthent-control-{env}` | `sqldb-healthent-control-prod` |
| Pipeline | `pl_{source}_{target}_{pattern}` | `pl_d365_bronze_full` |
| Notebook | `nb_{layer}_{subject}_{pattern}` | `nb_silver_patient_incremental` |
| Fabric Environment | `env-healthent-{scope}` | `env-healthent-clinical` |
| Table | `snake_case` | `patient_appointment` |
| Column | `snake_case` | `appointment_date` |
| Schema (warehouse) | `{layer}` | `bronze`, `silver`, `gold` |
| Terraform module | `fabric_{component}` | `fabric_capacity` |
| Branch | `feature/{ticket}-{description}` | `feature/DE-42-patient-scd2` |
| Entra group | `sg-healthent-{domain}-{role}` | `sg-healthent-clinical-eng` |
| Service principal | `sp-healthent-{purpose}-{env}` | `sp-healthent-fabric-prod` |
| Key Vault | `kv-healthent-{domain}-{env}` | `kv-healthent-clinical-prod` |
| Resource group | `rg-healthent-{component}-{env}` | `rg-healthent-fabric-prod` |
| Eventstream / Eventhouse | `es_{domain}_{source}` / `eh_{domain}` | `es_clinical_device_telemetry` |
| ADR | `ADR-{nn}-{short-title}` | `ADR-22-control-plane-azure-sql` |

---

## 5. SQL Standards (T-SQL)

**Where SQL runs (read this first):**
- **Control plane** (`meta.*`, `log.*`) → **Azure SQL Database**. Full enforcement: `IDENTITY`, `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `CHECK`, triggers.
- **Gold serving** (`gold.*`, views, procs) → **Fabric Warehouse**. **Constraints are NOT enforced** here: PK/UNIQUE are informational (NOT ENFORCED), FK not enforced, CHECK unsupported, IDENTITY historically unsupported. Never rely on Fabric Warehouse to enforce integrity — enforce in Spark/Silver before publishing to Gold.

**Standards (both targets):**
- All T-SQL must be **idempotent** (`IF NOT EXISTS`, `MERGE`, `CREATE OR ALTER`).
- Use `MERGE` for upserts — never `DELETE + INSERT`.
- **Always specify** column lists — no `SELECT *` in production code.
- Partition by `ingestion_date` unless explicitly stated otherwise.
- Header block on every proc/view: purpose, inputs, outputs, change history.
- Format: uppercase keywords, 4-space indent, one clause per line.
- `datetimeoffset` is **not supported** in Fabric Data Warehouse — split to a UTC datetime + offset column.
- SQL is built and deployed as **SQL Database Projects (DACPAC)** from the **sql repo** via `sqlpackage` in CI/CD — not hand-applied.

---

## 6. PySpark / Python Standards

- **Fabric Runtime 1.3**: **Spark 3.5, Python 3.11, Delta Lake 3.2** (GA default). Do not target Runtime 1.2 (retired). Runtime 2.0 (Spark 4.0 / Py 3.12) is a forward option to evaluate, not the baseline.
- Use **Delta Lake** format for Silver and Gold layers in Lakehouse.
- Prefer `spark.read` / `spark.write` with explicit schema — never infer schema in production.
- Use `MERGE INTO` (Delta) for upserts and SCD processing.
- All notebooks must be parameterised — no hardcoded paths, dates, or connection strings.
- **Parameterise via a cell toggled as "Parameters"** (its variables are overridden at call time). Chain/orchestrate with **`notebookutils.notebook.run` / `.runMultiple`**; exit with `notebookutils.notebook.exit`; fetch secrets with `notebookutils.credentials`. **Do NOT use `dbutils.widgets`** — that is the Databricks idiom, not the Fabric-native surface. (`notebookutils` is the renamed MSSparkUtils.) **Verify `notebookutils` API surface against Runtime 1.3 release notes before use — the API can vary between Fabric Runtime versions.**
- Logging via structured `log.*` tables — not just `print()`.
- Unit tests in the platform repo `tests/` using `pytest` + a local Spark session.
- **Do not `pip install` in notebook cells** — manage libraries via Fabric Environments (§33).

---

## 7. Security Rules

- **No secrets in code** — all secrets via Azure Key Vault references only (§17).
- **No hardcoded connection strings** — managed identities or Key Vault references.
- Sensitive health columns tagged in Purview and masked at Gold/serving layer.
- RLS enforced at Warehouse and Power BI semantic-model level.
- OLS / masking enforced for sensitive columns (PHI, PII).
- Every environment has isolated Fabric workspaces and separate identities.
- Fabric DDM syntax differs from Databricks MASK — verify in Wave 0 before publishing masked Gold (ADR-19, open — owner: Senior DE, must close before Wave-0 cutover). **Spike this early (Phase P), not at Wave-0** — if DDM does not behave as assumed the whole mask-at-Gold approach is at risk (review G-14).
- **Bronze/Silver are restricted** — raw/identifiable PHI in these layers is accessible to the framework managed identity and named break-glass only, not general domain readers (§3.13). Verify via `scripts/verify-access.sh` + `tests/security`.
- **Privileged access to Prod PHI is JIT/PIM for all domains** — not HR only. Standing access to production health data is minimised; emergency access uses the logged **break-glass** procedure (`docs/runbooks/break-glass-access.md`) with approval, time-box, and mandatory post-use review. Access reviews run on a fixed cadence (review G-10).
- **Encryption-at-rest key model is an explicit decision (ADR-28, open)** — confirm current Fabric/OneLake CMK capability, then adopt CMK or record "MMK accepted, CMK not yet supported — risk accepted" with a review trigger. Do not leave undecided for a PHI platform (review G-11).

---

## 8. Environment Strategy

| Environment | Purpose | Fabric Capacity | Idle cost strategy |
|---|---|---|---|
| **Pilot** | Free-tier proof (Phase P) | **Trial (≈F64, 60 days)** | Trial; no Terraform capacity; managed manually via Fabric UI / `fab` CLI only |
| Dev | Development & experimentation | F4 (AU East) | **Pause** when idle (scheduled) |
| Test | SIT & automated testing | F4 (AU East) | **Pause** post-run; destroy weekly for IaC drift check |
| UAT | Business acceptance testing | F8 (AU East) | Pause between UAT cycles |
| Prod | Production workloads | F64 (AU East) | Always on; scale down off-hours |
| DR | Disaster recovery | F32 (AU Southeast) | Standby — see §20 |

> **Capacity sizing is validated, not assumed (ADR-21).** Start on the trial (Phase P), capture CU telemetry under load, then commit paid F-SKUs. **Power BI licensing:** an **F64+** capacity grants free read-only viewer consumption (no per-viewer Pro). Below F64 (Dev/Test/UAT), report consumers need Pro/PPU. The F64 viewer threshold may dominate the Prod SKU choice regardless of compute.

> **Pilot environment note:** the Pilot/Trial capacity is provisioned manually (Fabric UI or `fab` CLI) and is NOT managed by Terraform. The `az fabric capacity` pause/resume commands in §9 apply to **paid Dev/Test/UAT/Prod** capacities only — do not run them against the trial.

---

## 9. Key Commands

```bash
# --- infra repo: Terraform lifecycle ---
cd infra/envs/dev && terraform init && terraform plan -var-file=dev.tfvars
cd infra/envs/dev && terraform apply  -var-file=dev.tfvars -auto-approve
cd infra/bootstrap && terraform init && terraform apply -var-file=bootstrap.tfvars   # state backend, once

# --- infra repo: pause/resume PAID capacity (Dev/Test/UAT/Prod only — NOT the trial) ---
az fabric capacity suspend --resource-group rg-healthent-fabric-dev --capacity-name capdevhealthent
az fabric capacity resume  --resource-group rg-healthent-fabric-dev --capacity-name capdevhealthent

# --- sql repo: build + deploy control-plane / warehouse DACPAC ---
dotnet build sql/control-plane/ControlPlane.sqlproj
sqlpackage /Action:Publish /SourceFile:ControlPlane.dacpac /TargetConnectionString:"$CTRL_CONN"

# --- platform repo: tests + lint ---
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v --env dev
sqlfluff lint sql/ --dialect tsql
ruff check notebooks/

# --- access + smoke ---
bash scripts/verify-access.sh dev
python -m pytest tests/smoke/test_smoke_dev.py -v

# --- Azure CLI ---
az account show
az synapse workspace list --resource-group rg-healthent-synapse-prod
```

---

## 10. Multi-Repo Topology (Definitive)

> **⚠️ AMENDED 2026-06-10 (ADR-37 A1 + ADR-38):** final topology is **ONE ADO project ("Fabric") with FIVE repos**:
> 1. **`docs`** — unchanged.
> 2. **`platform`** — platform engineering consolidated (ADR-38, **A1 2026-06-11: the framework product lives under ONE folder**): `framework/{control-plane, fabric-items, wheel}` — `control-plane/` = meta.*/log.* DDL (Azure SQL via DACPAC, ADR-22 unchanged), `fabric-items/` = runner notebooks+pipelines (**the Fabric Git-bound folder** — bind this, never repo root), `wheel/` = healthent-framework package (ADR-40 A1) — plus `infra/` (Terraform), `devops/`, `tests/`. CI is **path-filtered** per folder. Domain content NEVER lives here (dataflows repo).
> 3. **`sql`** — **warehouse serving only**: Gold DDL/views/procs/security (DACPAC).
> 4. **`dataflows`** — DE development mono-repo: `bronze/ silver/ gold/` each `DDL/{dag_uid}/` + `Notebook/{dag_uid}/`, `metadata/{dag_uid}/` seeds, selective CI/CD by mandatory `dag_uid` (ADR-37 A1).
> 5. **`bi`** — semantic models + reports (PBIP), selective CI/CD by domain+item (never per dataflow, ADR-36 §7). **No T-SQL in `bi`.**
> `semantic-models/` withdrawn from platform (→ `bi`); ADR-34's mirrored `dataflows/` folders withdrawn. The §10.x trees below predate this amendment — read them with the mapping above. No repo commits `CLAUDE.md`/`CLAUDE.local.md` (local-only). See ADR-37 + ADR-38.

> **Best practice for Fabric:** split repos by **lifecycle and deployment mechanism**, not by file type. A Fabric workspace's Git integration binds to **one repo + one branch + one folder**, so notebooks and data pipelines that live in the same workspace **must** share the platform repo. Docs, Terraform, and SQL Database Projects deploy by different mechanisms, so they are separate repos.

| Repo | Purpose | Deploy mechanism | Contains |
|---|---|---|---|
| `healthent-fabric-docs` | All documentation | n/a (review/PR) | gameplan, ADRs, runbooks, FinOps & risk registers, Gantt, per-phase docs |
| `healthent-fabric-infra` | Platform IaC | Terraform + Azure DevOps | capacity, workspaces, KV, policy, Purview, monitoring, Fabric Environments |
| `healthent-fabric-platform` | Fabric items | **Fabric Git integration** + Deployment Pipelines | notebooks, data pipelines, lakehouse/warehouse item shells, semantic models, tests |
| `healthent-fabric-sql` | Database Projects | `sqlpackage` (DACPAC) via Azure DevOps | control-plane DDL (Azure SQL), Fabric Warehouse Gold DDL/views/procs/security |

### 10.1 `healthent-fabric-docs`
```
healthent-fabric-docs/
├── CLAUDE.md
├── CLAUDE.local.md          ← gitignored; local session state only (see §35)
├── gameplan.md
├── .gitignore
├── docs/
│   ├── architecture/
│   ├── decisions/{adr-index.md, session-log.md, ADR-{nn}-{title}.md}
│   ├── phase-{nn}/{implementation.md, finops.md, risk.md, runbook.md}   ← §34, every phase
│   ├── finops/{cost-model.md, capacity-plan.md, chargeback.md, risk-register-finops.md}
│   ├── risk/{program-risk-register.md}
│   ├── timeline/{gantt.md}
│   ├── runbooks/
│   └── dr-runbook.md
```

### 10.2 `healthent-fabric-infra`
```
healthent-fabric-infra/
├── CLAUDE.md
├── CLAUDE.local.md          ← gitignored
├── .gitignore
├── bootstrap/                         ← remote state backend (Azure Storage) — protected
├── fabric-environments/               ← Fabric Environment specs (Runtime 1.3 + extra libs)
│   ├── env-healthent-framework.yml
│   ├── env-healthent-clinical.yml
│   ├── env-healthent-ml.yml
│   └── env-healthent-ops.yml
├── modules/
│   ├── fabric_capacity/  fabric_workspace/  fabric_lakehouse/  fabric_warehouse/
│   ├── control_sql/                   ← Azure SQL DB for meta.*/log.*
│   ├── entra_groups/  service_principals/  conditional_access/
│   ├── key_vault/  private_endpoints/  azure_policy/  purview/  fabric_monitoring/
├── envs/{dev/, test/, uat/, prod/, dr/}
├── devops/pipelines/{infra-ci.yml, infra-cd.yml}
└── scripts/{pause-resume.sh, destroy-dev.sh, rebuild-dev.sh, verify-access.sh}
```

### 10.3 `healthent-fabric-platform`  (Fabric Git-synced)
```
healthent-fabric-platform/
├── CLAUDE.md
├── CLAUDE.local.md          ← gitignored
├── .gitignore
├── notebooks/
│   ├── framework/   ← nb_pipeline_controller, nb_ingestion_full, nb_ingestion_incremental,
│   │                  nb_cdc_processor, nb_scd1_processor, nb_scd2_processor,
│   │                  nb_watermark_manager, nb_run_lock_manager, nb_drift_checker,
│   │                  nb_circuit_breaker, nb_audit_logger, nb_notification_router,
│   │                  nb_dq_validator, nb_reconciliation_harness, nb_schema_drift_handler
│   ├── ops/         ← nb_pipeline_monitor, nb_capacity_monitor, nb_dq_dashboard, nb_cost_monitor
│   ├── ml/          ← nb_feature_engineering_template, nb_model_training_template, nb_batch_scoring_template
│   └── domains/{clinical,finance,operations,hr,audiology,dynamics}/{bronze,silver,gold}/
├── pipelines/
│   ├── framework/   ← pl master + domain orchestration (flat ForEach ×2)
│   └── domains/{clinical,finance,operations,hr,audiology,dynamics}/
├── semantic-models/{clinical,finance,operations,hr,audiology,shared}/   ← .pbip
├── tests/{unit,integration,security,performance,reconciliation,smoke}/
└── devops/pipelines/{ci-platform.yml, cd-deploy-dev.yml, cd-deploy-test.yml, cd-deploy-uat.yml, cd-deploy-prod.yml}
```
**Fabric Git binding rule:** one workspace ↔ this repo, branch-per-environment (`dev`/`uat`/`main`), **Git Folder per workspace/domain**. Promote Dev→Test→UAT→Prod with **Fabric Deployment Pipelines**. Items not yet Git-integrated are provisioned via REST (§27).

### 10.4 `healthent-fabric-sql`  (Database Projects → DACPAC)
```
healthent-fabric-sql/
├── CLAUDE.md
├── CLAUDE.local.md          ← gitignored
├── .gitignore
├── control-plane/                     ← Azure SQL DB project (ENFORCED constraints)
│   └── sql/metadata/{01_schemas … 10_seed_purge_vacuum}.sql
├── warehouse/                         ← Fabric Warehouse project (Gold serving, constraints NOT enforced)
│   └── {clinical,finance,operations,hr,audiology,shared}/{ddl,views,procedures,security}/
├── security/{rls_policies.sql, ols_policies.sql, entra_group_assignments.sql}
└── devops/pipelines/{sql-ci.yml, sql-cd.yml}
```

### 10.5 `.gitignore` (every repo)
```gitignore
CLAUDE.local.md
**/.terraform/
*.tfstate
*.tfstate.backup
*.tfplan
.terraform.lock.hcl
__pycache__/
*.pyc
.pytest_cache/
.venv/
*.egg-info/
*.env
.env.*
secrets/
**/local.settings.json
.DS_Store
Thumbs.db
.vscode/settings.json
.idea/
```

---

## 11. Migration Principles

- **Do NOT migrate one-for-one** — every Synapse asset is assessed, rationalised, redesigned for Fabric.
- Migration waves are prioritised by business value and complexity (`gameplan.md`).
- Every migration includes: parallel run → validation → cutover → rollback plan.
- Synapse assets are decommissioned only after 30-day clean hypercare in Fabric.
- Data reconciliation reports (rows + SUM measure + SCD2 invariant) are mandatory per migrated pipeline.

---

## 12. Definition of Done (Every Deliverable)

- [ ] Code version-controlled in the correct repo (§10), peer-reviewed (branch protection §25), merged via branch strategy.
- [ ] Unit tests pass locally before any cloud deployment.
- [ ] CI/CD passes (lint, test, deploy) in Dev before promotion.
- [ ] Data quality checks in place (§28).
- [ ] Monitoring and alerting configured (§32).
- [ ] **Implementation, FinOps, and risk docs updated for the phase (§34).**
- [ ] ADR logged (§21) and session-log updated (§18) if a new decision was made.
- [ ] Cost impact assessed and within budget (§14).
- [ ] Security review passed (no secrets, least privilege, PHI handled correctly).
- [ ] Business sign-off obtained for Gold / serving layer changes. *(Clinical-domain Gold also requires clinical-governance review, not LOB sign-off alone — review G-24.)*
- [ ] **Phase completion `runbook.md` produced** and accepted per `docs/runbooks/phase-completion-runbook.md` (§34).
- [ ] **Rebuild-from-repo dry-run verified** for infrastructure-bearing phases (P, 4, 5, 6, 9, 14).
- [ ] **Non-prod data is synthetic / de-identified** — no raw PHI used in any non-prod test or demo (§36).

---

## 13. Common Failure Points (Check These First)

- **Control plane created in Fabric Warehouse** — wrong. `meta.*`/`log.*` go in Azure SQL DB; the Warehouse does not enforce PK/FK/UNIQUE/CHECK and historically lacks IDENTITY (§15.1).
- **Wrong Spark runtime** — target Runtime 1.3 (Spark 3.5 / Py 3.11). Runtime 1.2 is retired.
- **`dbutils.widgets` in a notebook** — use a Parameters cell + `notebookutils` (§6).
- **`az fabric capacity` against the trial capacity** — the trial is managed via Fabric UI / `fab` CLI only; the `az fabric capacity` CLI commands apply to paid F-SKUs (§8, §9).
- **Fabric capacity region** — confirm AU East. Azure Policy (§19) enforces this.
- **OneLake path errors** — use `abfss://` with correct workspace/lakehouse GUIDs.
- **Delta format issues** — Silver/Gold must be Delta; Bronze is raw (Parquet/CSV preserved).
- **Managed identity not assigned** — Fabric pipelines need identity on Key Vault + storage.
- **SP/MI item-ownership trap** — some item APIs (e.g. shortcuts) don't accept SP/MI, and **item ownership can't be reassigned after creation**; if the creating identity is disabled, items break. Use a durable owning identity (§27).
- **Power BI Direct Lake not refreshing** — check Delta V-Order optimisation is ON; watch DirectQuery fallback under concurrency (R-07).
- **Terraform state lock / backend** — release stale blob lease; bootstrap storage has `prevent_destroy = true`.
- **PHI column in wrong layer** — Gold must mask/aggregate PHI; never expose raw.
- **datetimeoffset in Fabric Warehouse** — unsupported; split to UTC datetime + offset.
- **Fabric DDM syntax** — not the same as Databricks MASK; ADR-19 open until Wave-0 (owner: Senior DE).
- **Secret expired** — check Key Vault expiry; rotation schedule in §17 (expiry alerts provisioned in Phase 5).
- **D365/Dataverse connector** — Wave-0 Confirmation #2; generic Copy pattern (§26).
- **Fabric Terraform provider** — preview; capacity via azurerm; some items REST-only (§27).
- **`CLAUDE.local.md` missing** — if this file is absent at session start, ask the user for current phase, last step completed, and any open blockers before proceeding.

---

## 14. FinOps & Cost Controls

- Non-prod capacity is **paused when idle** (scheduled or scripted) — pausing preserves workspace items + OneLake data and stops compute billing. Prefer this over nightly destroy.
- Use **destroy/rebuild only for periodic IaC-drift validation** (e.g. weekly Test), not as the daily cost lever.
- No Synapse Dedicated Pool usage unless approved (always-on cost).
- Serverless SQL (Synapse source only) — set TB scan cost cap.
- **Size from telemetry, not guesses** — the Fabric Capacity Metrics app drives F-SKU decisions (Phase P + ADR-21).
- Weekly cost review against the CU consumption budget; CU > 80% = P3, > 95% = P2 alert (§32).
- DirectQuery over Serverless is a **cost trap** — prefer Direct Lake or Import.
- **Cost the non-Fabric Azure footprint too (review G-18)** — CU is not the whole bill. The cost model (`docs/finops/cost-model.md`) must also include the **control-plane Azure SQL DBs (4–5 across envs)**, **~24 Key Vaults (per domain × env)**, **Private Endpoints / networking**, **Purview**, storage egress, and any Log Analytics. These are real monthly line items independent of Fabric capacity and are easy to omit when sizing purely from the Capacity Metrics app.
- Reserved capacity for Prod only after F-SKU sizing validated.
- **Every phase produces a FinOps note** (§34) — expected CU impact, run-cost delta, optimisation actions.
- **Cost the whole Azure bill, not just CU** (review G-18) — the model must include the 4–5 Azure SQL control DBs, ~24 Key Vaults (6 domains × 4 envs), private-endpoint hours, Purview, state storage, and egress. CU is the big rock but not the whole bill; track these lines in `docs/finops/cost-model.md`.

---

## 15. Metadata-Driven Framework — Permanent Standards

> The backbone of the platform. Apply in **every session**, not just Phase 9.

### 15.1 Control-Plane Location — LOCKED (ADR-22)

**All `meta.*` and `log.*` tables live in an Azure SQL Database** (`sqldb-healthent-control-{env}`), **never** in the Fabric Warehouse. Rationale: the framework relies on **enforced** `PRIMARY KEY` / `FOREIGN KEY` / `UNIQUE` / `CHECK` and on `IDENTITY` surrogate keys. Fabric Warehouse treats PK/UNIQUE as NOT ENFORCED, does not enforce FK, does not support CHECK, and historically does not support IDENTITY. The Fabric Warehouse holds **Gold serving objects only**. (Fabric T-SQL is evolving — re-verify before relying on any newly added constraint behaviour, but the control plane stays in Azure SQL DB.)

### 15.2 Core Design Rule — Config vs State
- `meta.*` = **configuration** — written only by engineers via the **sql repo** CI/CD (DACPAC), never at runtime.
- `log.*` = **state** — written only by the runtime managed identity during execution.
- Watermarks, run-locks, run history are **state** (`log.*`). Never in `meta.*`.

### 15.3 Schema Overview
*(Naming note: the v0 names below are renamed at Phase 9 per **ADR-46** — `df_*` orchestration spine, `ing_*` ingestion side, `ext_*` reserved, bare = cross-cutting. Until then, do not spread fresh references to `framework_batch`/`job_registry`/`proc_registry`/`run_lock` beyond the existing framework surface.)*
```
meta (config — engineer-written via DACPAC):  [LIVE: 13 tables, verified 2026-06-14]
  dag, framework_batch, batch_param, job_registry, proc_registry, proc_param,
  source_connection, ingestion_object, ingestion_column,
  dq_rule, storage_target, external_location, purge_rule
  (notify uses framework_batch.notify_group + log.notification_outbox — there is NO notification_rule table;
   storage routing uses storage_target + columns on ingestion_object — there is NO object_storage_routing table;
   batch_param is RESERVED — first consumer = Area-5/Phase-9 orchestrator. ADR-46 v1 names live as synonyms.)
log (state — runtime MI-written):  [LIVE: 10 tables]
  dag_run, batch_run, job_run, proc_run, ingestion_run,
  object_watermark, run_lock, dq_result, run_event, notification_outbox
```
Relationships:
```
dag 1─* framework_batch 1─* {batch_param, job_registry}
source_connection 1─* ingestion_object 1─* ingestion_column
job_registry 1─* proc_registry 1─* proc_param ; proc_registry *─1 ingestion_object (opt)
dag 1─* dag_run 1─* batch_run 1─* job_run 1─* proc_run 1─* ingestion_run
ingestion_object 1─1 {object_watermark, run_lock} ; *─1 ingestion_run (updated_by/locked_by)
ingestion_object 1─* dq_rule ; ingestion_run 1─* dq_result ; dag 1─* purge_rule
```

### 15.4 Key Columns (Azure SQL DB — enforced)
`meta.ingestion_object`: `object_id INT IDENTITY PK`, `connection_id FK`, `object_name`, `target_schema/table`, `load_type ('append'|'incremental_watermark')`, `watermark_column NULL`, `watermark_datatype ('timestamp'|'bigint') NULL`, `dedupe_mode`, `expected_runtime_min`, `consecutive_failures DEFAULT 0`, `is_enabled BIT DEFAULT 1`. CHECK: incremental requires watermark_column + datatype.
`log.object_watermark`: `object_id PK FK`, `last_loaded_ts DATETIME2(3) NULL`, `last_loaded_seq BIGINT NULL`, `updated_by_run BIGINT FK`. Epoch init `'1900-01-01'`.
`log.run_lock`: `object_id PK FK`, `lock_status ('free'|'running'|'failed')`, `locked_by_run BIGINT NULL`, `locked_at DATETIME2(3) NULL`.
`log.ingestion_run`: **`ingestion_run_id BIGINT IDENTITY PK`** (BIGINT — see M2), `proc_run_id FK`, `object_id FK`, `run_upper_bound_ts/seq`, `rows_copied BIGINT`, `write_confirmed BIT DEFAULT 0`, `drift_detected BIT DEFAULT 0`.
`meta.source_connection`: `connection_id INT IDENTITY PK`, `connection_name`, `kv_name`, `kv_secret_name`. **Secret values never stored — runtime MI fetches at execution.**

### 15.5 Watermark Rules (Non-Negotiable)
1. Ceiling = `MAX(watermark_col)` from source — never `now()`.
2. Upper bound persisted **before** copy — failed copy retries same window.
3. Watermark advances **only** when `write_confirmed = 1`.
4. Half-open window `(lower, upper]` — no gaps, no duplicates.
5. Typed columns only — `DATETIME2(3)` or `BIGINT`, never `NVARCHAR`.
6. Epoch init `'1900-01-01T00:00:00'`.
7. Run-lock prevents concurrent watermark writes.

### 15.6 Ingestion Control Flow
`resolve_config → acquire_lock → branch(load_type) → check_drift → copy → write_confirmed=1 → advance_watermark → reset failures → release_lock`. On failure: record, increment `consecutive_failures`, trip breaker at threshold (`is_enabled=0`), release lock → `failed`, notify.

### 15.7 Circuit Breaker (Azure SQL control plane)
On failure increment `consecutive_failures`; set `is_enabled=0` when `>= @threshold`. On success reset to 0.

### 15.8 Orchestration Tiers
Tier 1 master pipeline iterates domains → Tier 2 domain pipeline resolves `proc_order`, parallelises equal orders, enforces concurrency caps. **Two flat ForEach loops only — never nested ForEach (ADR-18).** **Cross-dag admission (Area 5 design, `docs/architecture/concurrency-and-orchestration.md`):** because all dags share one capacity per env (ADR-42), Tier 1 admits/queues runs by `df_batch_param` **priority · run_window · concurrency_group cap · target capacity/pool**, ordered priority→scheduled_time; throttling = back-pressure (queue + retry-on-throttle), never hard-fail. Triggers are schedule (`df_dag.schedule_cron`) **and** event. Lands with the Phase-9 runner.

### 15.9 Onboarding a New Source = config only (4 inserts via DACPAC): connection → object → seed `log.object_watermark` → seed `log.run_lock`. No new pipeline is ever written.

### 15.10 Reconciliation Standards
`(1)` row count within tolerance; `(2)` **SUM** measure within tolerance (catches silent cast/precision loss); `(3)` SCD2 invariant: zero duplicate current rows per business key. **Reconcile a SUM, not just a COUNT.** For objects with **no meaningful SUM** (dimensions, text-heavy tables), use a **row-hash / checksum** reconciliation instead, selectable per object in `meta` (review G-20).

### 15.11 Wave-0 Exit Gate ("Green at Load")
All 400 objects ingest within SLA under concurrency caps (no throttling); watermark/idempotency/drift/SCD2/resilience verified at load; reconciliation passes every domain; observability fires on progress/failure/drift/heartbeat; CI/CD release path completes end-to-end; six Wave-0 confirmations closed (DDM syntax, Dataverse path, Direct Lake limits, Spark concurrency ceiling, Terraform/REST coverage, control-file/EOT validation). **Plus a control-plane assertion (review G-08):** under full 400-object concurrency the Azure SQL control DB shows no lock-wait timeouts on `log.run_lock`/`log.object_watermark`, no JDBC connection exhaustion, and lock/watermark write latency within budget. **Nothing in Wave 1 starts until this passes.** The thin-slice version of this gate runs in **Phase P** on the trial capacity.

---

## 16. Infrastructure Lifecycle — Pause, Destroy & Rebuild

### 16.1 Lifecycle by Environment
| Env | Default state | Cost strategy | Rebuild time |
|---|---|---|---|
| Pilot | Trial (60 days) | Trial capacity; let expire | n/a |
| Dev | On during sessions | **Pause** when idle (scheduled) | ~2 min resume |
| Test | Ephemeral | Pause post-run; **destroy weekly** for IaC-drift check | ~8 min |
| UAT | On during UAT cycles | Pause between cycles | ~12 min |
| Prod | Always on | Scale down off-hours | N/A |
| DR | Standby | See §20 | ~20 min |

> **Pause ≠ destroy.** Pausing the *capacity* stops compute billing while preserving workspaces, items, and OneLake data. Destroying *workspaces* discards items/data and forces a full redeploy — use only for periodic drift validation.

### 16.2 State backend — PROTECTED
`infra/bootstrap` Azure Storage account holds all Terraform state with `prevent_destroy = true`. Never destroyed.

### 16.3 Prod data protection
Prod data resources carry `prevent_destroy = true`. Never `terraform destroy` Prod data.

### 16.4 Full Rebuild Sequence (in order)
1. State backend (first time only) → 2. Entra groups + SPs → 3. Azure Policy (residency) → 4. Key Vaults → 5. **Control-plane Azure SQL DB** → 6. Fabric capacity + workspaces + lakehouses + warehouses → 7. Private endpoints + Conditional Access → 8. Purview → 9. Control-plane + warehouse DACPAC (sql repo, in order) → 10. Deploy notebooks/pipelines/semantic models (platform repo, Fabric Git + Deployment Pipelines) → 11. Initialise watermarks + run-locks → 12. Verify access → 13. Smoke test.

### 16.5 What survives destroy
Bootstrap state, Prod data resources, OneLake Prod data (GRS), Key Vault (soft-delete 30 days), Entra groups/SPs (idempotent). Dev/Test OneLake data does **not** survive workspace destroy — hence prefer pause.

---

## 17. Entra Groups, Domains & Automated Access

Domains: Clinical, Finance, Operations, HR, Audiology, Dynamics (+ Platform/shared).
Groups: `sg-healthent-{domain}-{role}` (`eng`, `read`, `admin`); SPs: `sp-healthent-fabric-{env}`, `sp-healthent-devops`, `sp-healthent-purview`.
Key Vault: one per domain per env; access by group/SP only. HR uses PIM.
RLS at Warehouse + semantic model; OLS/masking on PHI/PII columns.
**Domain isolation:** cross-domain KV access denied (expect 403). Verified by `scripts/verify-access.sh` + `tests/security/test_access_controls.py`.
Conditional Access: MFA required for all Fabric access.

**Secret rotation:** Key Vault expiry alerts are provisioned in Phase 5 (`infra/modules/key_vault/` — set expiry notifications at 30 days and 7 days before expiry on every secret). A rotation schedule is maintained per-domain in `docs/runbooks/secret-rotation.md`. Expired secrets will silently break pipeline execution — check KV expiry as a first step in any connectivity incident.

All identity is Terraform-managed in the **infra repo** and re-applied on every rebuild.

---

## 18. Session Log Pattern
At session end, append to `docs/decisions/session-log.md` (docs repo): date, phase, what was built, decisions, new ADRs, open items, next step. Also output the **Session Handoff block** defined in §0 and paste it into `CLAUDE.local.md`.

---

## 19. Azure Policy — Data Residency
`infra/modules/azure_policy` denies creation of any resource outside AU East / AU Southeast. Applied on every rebuild before any data resource.

---

## 20. Disaster Recovery
RTO 4h, RPO 1h. DR region AU Southeast, DR capacity F32 (on-demand via `infra/envs/dr`).
**Verify (not settled):** Fabric **BCDR** is a capacity-level cross-region replication setting, not a simple "GRS toggle." Confirm AU East ↔ AU Southeast is a valid Fabric BCDR pairing and document the actual OneLake replication model in Phase 4. Runbook: `docs/dr-runbook.md`.
**Control plane is in scope for DR (review G-07 — the most-overlooked single point of failure).** Fabric BCDR does **not** protect the Azure SQL control plane, which holds every watermark, run-lock, and `meta.*` config. Configure Azure SQL **point-in-time restore** (explicit retention), **geo-redundant backup** (or active geo-replication to AU Southeast), and **long-term retention** if the retention policy (§37) requires it. Author `docs/runbooks/control-plane-backup-restore.md` covering backup config, restore steps, and **watermark reconciliation after restore** (a restored watermark must be reconciled against actually-landed data so the platform neither reprocesses nor skips). Include the control DB in every DR test, not just Fabric. Risk R-15.

---

## 21. ADR Index
| ADR | Title | Status | Phase | Owner | Must close by |
|---|---|---|---|---|---|
| ADR-01..18 | (platform, medallion, OneLake, Direct Lake, metadata-driven, Terraform, ADO, typed watermark, config/state, KV-per-domain, rationalise, AU regions, residency policy, PHI separation, 30-day hypercare, Purview, Wave-0 gate, flat ForEach) | ✅ Closed | various | — | — |
| **ADR-19** | **Fabric DDM syntax** | ⚠️ OPEN | Wave-0 | Senior DE | Before Wave-0 masking test |
| **ADR-20** | **D365/Dataverse ingestion via generic Copy** | ⚠️ OPEN | Wave-0 | Senior DE | Before Wave-0 entity load |
| **ADR-21** | **F-SKU sizing — validate on trial (Phase P) then Prod** | ⚠️ OPEN | Phase P/4 | Senior DE + DE Manager | End of Phase P |
| **ADR-22** | **Control plane in Azure SQL DB (not Fabric Warehouse). A1 (2026-06-12): re-examined incl. Fabric SQL Database item — RE-AFFIRMED on failure-domain grounds (capacity pause/throttle coupling); revisit trigger in ADR-22-A1** | ✅ Closed + A1 | Phase 9 | — | — |
| **ADR-23** | **Four-repo topology (docs/infra/platform/sql)** | ✅ Closed | Phase 6 | — | — |
| **ADR-24** | **Fabric Runtime 1.3 (Spark 3.5 / Py 3.11) baseline** | ✅ Closed | Phase 8 | — | — |
| **ADR-25** | **Pilot-on-trial precedes paid capacity (Phase P)** | ✅ Closed | Phase P | — | — |
| **ADR-26** | **Pause non-prod capacity as default cost lever** | ✅ Closed | Phase 4 | — | — |
| **ADR-27** | **ML use-case selection** (referenced in CLAUDE.local) | ⚠️ OPEN | Phase 16 | CTO + Senior DE | Before Phase 16 entry |
| **ADR-28** | **Encryption-at-rest key model — CMK vs MMK** | ⚠️ OPEN | Phase 5 | Senior DE + Security | Before Phase 5 apply |
| **ADR-29** | **Test-data strategy — synthetic / de-identified, no raw PHI in non-prod** | ⚠️ OPEN | Phase 8 | Senior DE + Privacy | Before first non-prod test load |
| **ADR-30** | **De-identification standard + retention/disposal policy** | ⚠️ OPEN | Phase 5 | Privacy Officer + Senior DE | Before first prod PHI load |
| **ADR-31** | **Dataverse "Link to Fabric" (zero-copy) vs generic Copy** | ⚠️ OPEN | Phase P/12 | Senior DE | Wave-0 Dataverse path |
| **ADR-32** | **Fabric networking — tenant Private Link vs managed private endpoints; control-plane private path** | ⚠️ OPEN | Phase 5 | Senior DE + Network | Before Phase 5 apply |
| **ADR-33** | **Metadata-driven column security — OneLake-first, Warehouse CLS/DDM/RLS fallback; pipeline-only UNMASK + PIM** | ✅ Accepted | P→5/7/9 | Senior DE + Security | OneLake-GA + DDM verify in Phase P |
| **ADR-34** | **Self-service dataflow operating model — unique-id dataflows; metadata-only ingestion/extraction; proc_param-driven transform templates (Spark SQL + PySpark)** | ✅ Accepted | P→2/10 | Senior DE + DE Manager | — |
| **ADR-35** | **Execution planes (batch generic-runner + micro-batch + Eventstream real-time) & KV/connection modularity + connection-validation contract (runtime preflight + CI resolution gate)** | ✅ Accepted | P→5/9/12 | Senior DE + DE Manager | — |
| **ADR-36** | **Medallion storage topology (lakehouse-per-layer in domain workspace + bronze staging/main/archive) + managed-Delta-vs-shortcut tables + metadata-driven storage routing (`meta.storage_target`, no hardcoded abfss)** | ✅ Accepted | P→4/7/8/9 | Senior DE + DE Manager | — |
| **ADR-37** | **Development topology (amended A1) — ONE ADO project "Fabric", SIX repos: docs/infra/platform/sql + `dataflows` mono-repo (layer folders, per-flow `{dag_uid}`, selective CI/CD) + `bi` (semantic models/reports, selective by domain+item); Warehouse stays in sql, no T-SQL in bi** | ✅ Accepted + A1 | P→6 | Senior DE + DE Manager | — |
| **ADR-38** | **Platform-engineering consolidation — infra repo + control-plane SQL project merged into `platform` (infra/ + fabric-items/ + control-plane/, path-filtered CI); sql repo = warehouse serving only; program topology = 5 repos, one ADO project** | ✅ Accepted | P→6 | Senior DE + DE Manager | — |
| **ADR-39** | **Migration ingestion = direct source → Fabric, never through Synapse (Synapse only: one-time historical backfill + parallel-run baseline; per-object exceptions = waved tech debt)** | ✅ Accepted | P→12 | Senior DE + DE Manager | — |
| **ADR-40** | **Workspace topology — framework workspace (platform-eng only) + 6 domain workspaces per env; DEs Contributor in dev only; %run co-location until the wheel (Phase 9/10). A1: visible surface = tables + pipelines only — NO notebooks in shared workspaces; all code via ADO CI/CD; wheel committed (not optional); DE playground ws permanently empty** | ✅ Accepted + A1 | P→4/9 | Senior DE + DE Manager | — |
| **ADR-41** | **Source-family ingestion patterns — one generic runner per family (Dataverse / F&O OData / SQL table / file-landing NEW / REST); per-family drift detection + per-object drift_policy; file manifest/EOT gate + quarantine; admission control + runtime-overrun detection; family cost ranking feeds ADR-31. A1: Copy-vs-notebook per family (notebook for SQL/files; Copy only connector-forced/bulk; per-source UI pipelines prohibited; Phase 10 benchmark = break-even)** | ✅ Accepted + A1 | P→9/10/12 | Senior DE + DE Manager | — |
| **ADR-42** | **Capacity topology & scheduled scaling — one capacity per env; Prod split only on telemetry; scheduled SKU scaling with guardrails; intraday workspace-shifting REJECTED; trial→paid = workspace reassignment** | ✅ Accepted | P→4/15 | Senior DE + DE Manager | Split trigger review Phase 15 |
| **ADR-46** | **Control-plane naming v1 (user-directed): area prefixes df_*/ing_*/ext_* inside meta/log; bare = cross-cutting; fixes framework_batch/_registry inconsistencies + run_lock misnomer (→ing_lock); batch_param = reserved for Phase 9 runner. Executes at Phase 9 DACPAC rebuild. Related: control DB stays per-ENV (vs env-schemas) — see tradeoffs-index** | ✅ Accepted | 9 | Senior DE + DE Manager | Phase 9 build |
| **ADR-45** | **Migration dictionaries & per-object register — machine-readable source data dictionary (volumetrics, columns+classification, update pattern, lineage, family) + platform dictionary, generated by discovery (Phase 1); dictionary→seeds generator (Phase 11, "typing becomes reviewing"); `meta.migration_object` forward-only state machine with per-object legacy decommission (Phase 12); target dictionary = generated from meta.*/Purview, never authored** | ✅ Accepted | 1→11/12 | Senior DE + DE Manager | — |

---

## 22. Microsoft Purview — Governance
Root collection HEALTHENT → per-domain collections. Prod: weekly full + daily incremental scan; UAT on-demand; Dev/Test none. PHI/PII classification rules + sensitivity labels (Highly Confidential / Confidential / General). `sp-healthent-purview` needs Data Source Administrator on each workspace. Terraform in infra repo.

---

## 23. Smoke Test Specification
After every rebuild, run `tests/smoke/test_smoke_{env}.py` (platform repo). Covers: warehouse reachable; lakehouse readable; **control-plane Azure SQL reachable + meta/log tables seeded**; KV own-domain get; cross-domain KV 403; Entra group assignment; pipeline REST reachable; Purview reachable (prod). All must pass before work continues.

---

## 24. Power BI CI/CD
`.pbip` project format in platform repo `semantic-models/`. Promote via **Fabric Deployment Pipelines** (Dev→Test→UAT→Prod). Direct Lake connection is env-specific — update post-deploy. RLS roles must match Entra groups. **Licensing:** F64+ Prod = free viewer consumption; non-prod consumers below F64 need Pro/PPU (§8).
**Serving granularity (ADR-36 §7):** semantic models are **per business subject area, few per domain, endorsed/certified** — **never per dataflow** (`dag_uid` is a delivery/audit unit, not a serving unit). Cross-domain analytics via OneLake **shortcuts** into `semantic-models/shared/`, never data copies; separate sign-off (re-identification risk, §37).

---

## 25. Branch Protection (per repo)
`main` (→ Prod): PR + 2 approvals (Senior DE + DE Manager), required checks (lint, unit, infra-plan/sql-build), no direct push, delete branch after merge.
`uat`: PR + 1 approval (Senior DE), checks (lint, unit[, integration]).
`dev`: PR + 1 approval, check (lint).
`feature/*`: free; target `dev` only.
Prod deploy: PR approved → CI passes → DE Manager sign-off → **manual trigger only**.

---

## 26. D365 / Dataverse Ingestion (Wave-0 Confirmation #2)
Path: D365 → Fabric Copy pipeline (generic, metadata-driven) → Bronze. Dataverse connector (no IR). SP auth `sp-healthent-fabric-{env}`; secret in `kv-healthent-dynamics-{env}`. Config via `meta.source_connection` + `meta.ingestion_object` (watermark `modifiedon`). Constraints: 100K rows/request (`$skiptoken` pagination); F&O uses OData (different connector); rate limit ~6000 req/5min → cap `max_parallel_copy`.

---

## 27. Terraform Provider Coverage & Real Caveats (REWRITTEN)

The **`microsoft/fabric` provider** (public preview, actively expanding) now manages most core items. Prefer Terraform; fall back to REST only for the documented exceptions.

**Supported as Terraform resources:** Workspace, Workspace Role Assignment, Lakehouse, Warehouse, Notebook, Report, Semantic Model, Spark Pool, Spark Settings, **Environment Spark Settings**, Domain (+ role / workspace assignments), Workspace Git, ML Experiment/Model, SQL Database.

**Real caveats to plan around (not "everything is manual"):**
- **Preview** — pin the provider version; expect breaking changes; re-verify per release.
- **Capacity** is created via `azurerm`/`azapi`, **not** the Fabric provider (`fabric_capacity` is a **data source** you look up by name).
- **SP/MI gaps** — some item APIs (notably **shortcuts**) don't accept SP/MI, and **item ownership can't be reassigned after creation**. Choose a durable owning identity; document it.
- **Real-time items** (Eventstream/Eventhouse) remain thin — use REST (§30.4) and flag as a runbook step.
- **Deployment Pipelines / Direct Lake enablement** — drive via Fabric Deployment Pipelines + REST, not Terraform.

**Rule:** when a gap is hit, write the equivalent REST/CLI call and flag it as a manual runbook step — never silently omit.

---

## 28. Data Quality Framework — Permanent Standards
Mandatory checks per layer (Bronze: non-empty warn, breaking-drift block, dup-key log; Silver: NOT NULL block, FK block, range block, SCD2 uniqueness hard block; Gold: row recon block, SUM recon block, PHI-mask hard block). Defaults: row/measure tolerance 0.1%, zero nulls on mandatory, zero Gold dup keys, late-arriving alert > 3 days; override per object via `meta.proc_param`. Results to `log.dq_result` (Azure SQL control plane). Rules defined in `meta.dq_rule`. Gold PHI-mask failure = P1, immediate alert, security audit log.

---

## 29. SCD Type 2 — Permanent Standards
Every Gold dim has: `hash_key NVARCHAR(64)` (SHA-256 of tracked attrs), `effective_from`, `effective_to NULL`, `is_current BIT`, `mrg_ind ('A'|'E'|'SD')`, `created_at`, `updated_at`. Hash: tracked columns only (`is_scd2_tracked=1`), sorted, NULL→'', cast/strip/lower, deterministic. MERGE pattern: expire changed current rows (`E`), insert new versions (`A`); soft-delete via `NOT MATCHED BY SOURCE` (`SD`). Invariant after every run: zero duplicate current rows per business key (enforced in Spark — Gold Warehouse won't enforce it).

---

## 30. Eventstream & Real-Time Intelligence
Use Eventstream for IoT/device telemetry, near-real-time notifications, threshold alerts (→ Reflex); use batch for scheduled/backfill loads. Pattern: source → Eventstream → branch to Eventhouse (KQL) + Bronze Lakehouse (streaming) → real-time Power BI. Naming `es_/eh_/kqldb_/rx_`. **Terraform gap:** create Eventstream via REST (§27); document in `docs/runbooks/eventstream-provisioning.md`. Residency: Event Hubs `australiaeast`; KQL stored in AU East capacity.

---

## 31. CI/CD Pipeline Standards (per repo)
Standard stages: Lint → UnitTest → Build → DeployDev (auto on `dev`) → IntegrationTest → DeployUAT (auto on `uat`) → UATGate (manual) → DeployProd (manual only). Env values via Azure DevOps variable groups (`healthent-{env}-vars`) — never hardcoded.
- **infra repo:** `terraform plan` (PR) → manual `apply`.
- **sql repo:** `dotnet build` → `sqlpackage publish` per env.
- **platform repo:** lint/test → Fabric Deployment Pipeline promotion.
Promotion gates: feature→dev (1 approval, lint+unit), dev→uat (1 approval, +integration), uat→main (2 approvals, +UAT sign-off), main→prod (manual). Rollback: Git revert + redeploy; Terraform state revert; Delta time-travel for data.

---

## 32. Observability, Alerting & Incident Response
SLA: Gold freshness < 4h by 8AM AEST (P2); availability 99.5%/wk (P2 if <99%); warehouse P95 < 30s (P3); Direct Lake lag < 15m (P3); PHI access out-of-hours (P1); failed logins >5/10min (P1); CU >80% (P3) / >95% (P2). Severity P1 15min/PagerDuty+Teams, P2 1h, P3 4h, P4 next sprint. Monitoring notebooks (platform repo, ops/): pipeline_monitor (15m), capacity_monitor (30m), dq_dashboard (daily 6AM). Incident runbook: ack → check `log.batch_run`/`proc_run` → release stuck lock → check `dq_result` → check CU throttling → blast radius → comms → fix/rollback → re-run from failed object → validate → post-incident review in 48h. MTTR: freshness 2h, breaking drift 4h, PHI breach 30m, state corruption 4h, DR 4h. **The 30-minute PHI-breach MTTR is technical *containment* only — it is not breach notification.** Any P1 PHI exposure must also invoke `docs/runbooks/ndb-breach-response.md` for the statutory **Notifiable Data Breaches** process (eligible-breach assessment, OAIC + individual notification). These are separate workflows with separate owners (§37, review G-01).

---

## 33. Python Dependency Management (Fabric Environments)
Manage libraries via **Fabric Environments**, never inline `pip install`. Envs pin **Runtime 1.3** + **additional** libraries only — **do not re-pin runtime-bundled packages** (`delta-spark`, `pyarrow`, `pandas` ship with the runtime; re-pinning can conflict).
| Environment | Attached to | Additional libraries |
|---|---|---|
| `env-healthent-framework` | framework notebooks | (base — runtime only) |
| `env-healthent-clinical` | clinical notebooks | `fhir-resources`, `hl7apy` |
| `env-healthent-ml` | ML notebooks | `scikit-learn`, `mlflow`, `shap` |
| `env-healthent-ops` | ops notebooks | `azure-monitor-query`, `slack-sdk` |
Env specs live in **`infra/fabric-environments/`** (single source of truth). Always pin exact versions for added libs; update via PR. Every notebook header declares its environment, layer, domain, author, date.

---

## 34. Per-Phase Documentation Standard

Every phase (P and 0–18) **must** produce **four** docs in the **docs repo** under `docs/phase-{nn}/`, in addition to its technical deliverables:

1. **`implementation.md`** — **opens with a mandatory "Solution Design & HLA" section** (added 2026-06-12, user-directed, modelled on the UDP Martech DSD example §2): (a) **system context diagram** (Mermaid) showing every component the phase touches and its neighbours, (b) **ownership boundaries** (who owns each component/flow — platform vs domain vs BI vs external), (c) **data flow views** for each flow the phase introduces or changes, (d) **component design summary** (per component: purpose, technology, key decisions/ADR links). Then the numbered, executable build steps (the "how"), with the exact commands/REST calls, the repo each artifact lands in, and verification checks. A phase's implementation.md without the HLA section is incomplete.
2. **`finops.md`** — expected CU impact, capacity assumption, run-cost estimate/delta, and optimisation actions for that phase. Roll up into `docs/finops/cost-model.md`.
3. **`risk.md`** — phase-specific risks with severity, owner, mitigation, and "closes when" trigger. Roll up into `docs/risk/program-risk-register.md`.
4. **`runbook.md`** — the **phase completion record in enterprise Implementation-Plan format** (v2, 2026-06-11): about/audience → project details (change type, CHG ids, objective, justification, impact-if-not) → objects-to-deploy summary → implementation steps (workload holds, prerequisites, PRs, ordered deployment runs with per-step verification, metadata entries, dataflow registration) → post-implementation sanity **with captured output** → validation evidence (proof, not claims) for every exit criterion → §12 DoD → decisions/risk/FinOps actuals → **rollback covering code + config + data + watermark state, rehearsed** → role-based approvals with alternates → validated escalation matrix → follow-ups + handoff. Produced from the template in `docs/runbooks/phase-completion-runbook.md`. This is the document an operator who was not in the room uses to understand, rebuild, or roll back the phase — and the document a change board approves. *(Added by the 2026-06 review G-22; v2 format aligned to the user-supplied UDP UC1 Implementation Plan.)*

**5. `dsd.md` — the per-phase Detailed Solution Design (the living tracking cover; user-directed 2026-06-21).** Every phase folder also carries a `dsd.md` that ties the four docs together and tracks delivery: summary, **entry/exit gates**, Solution Design & HLA (links to implementation.md), **Gantt + timeline**, **dependencies/prerequisites**, step-by-step, **deliverables/artifacts inventory**, **RACI**, risks, FinOps, **to-do list**, **do/don't + recommendations**, **validation & evidence + DoD checklist**, **decisions/ADRs**, **rollback**, **change-control** (per `docs/governance/ai-assisted-development-operating-model.md`), **sign-offs**, **status tracker**, **follow-ups**. Template: `docs/templates/phase-dsd-template.md`. Generated from one phase table via `docs/implementation/gen_phase_dsd.py` (with `gen_phase_checklists.py`), so the DSDs, checklists, the **master delivery plan** (`docs/delivery/master-delivery-plan.md` — the single end-to-end all-phases doc with the master checklist), the gameplan, and the Greenfield Implementation Guide stay mutually consistent (§38). Never hand-edit a generated file; edit the table + re-run.

A phase is not "done" (gameplan exit criteria) until **all four governance docs + the `dsd.md`** exist, are reviewed and accepted against the quality bar in the phase-completion runbook, the master delivery plan + program Gantt (`docs/timeline/gantt.md`) + status table are updated, and the risk/FinOps roll-ups are reflected.

---

## 35. CLAUDE.local.md — Template & Purpose

`CLAUDE.local.md` is a **gitignored local-only file** present in every repo root. It serves two purposes:
1. **Environment identity** — workspace names, IDs, and connection strings specific to your local context (never committed).
2. **Session state** — the most recent Session Handoff block from §0, so Claude knows exactly where to resume.

**Fill this file before starting Phase P.** Copy the template below into each repo's root as `CLAUDE.local.md`. *(Template reconciled with the working file by the 2026-06 review so the two no longer drift — G-23. Note this file is gitignored and local to one machine; the durable, committed continuity record is `docs/decisions/session-log.md` plus each phase's `runbook.md`.)*

```markdown
# CLAUDE.local.md — Local Context & Session State
# NOT committed — listed in .gitignore of every repo. Copy to each repo root.
# Session start (Cursor): @-mention CLAUDE.md + gameplan.md + this file (Cursor does not auto-load them).
# Session end: paste the Session Handoff block (CLAUDE.md §0) into SESSION STATE below.
# Fill ENVIRONMENT IDENTITY + PRE-PHASE-P GATE before Phase P; leave fields blank until provisioned.

# ============================== ENVIRONMENT IDENTITY ==============================

## Azure
AZURE_SUBSCRIPTION_ID   = ""   # xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_TENANT_ID         = ""
AZURE_DEVOPS_ORG        = ""   # https://dev.azure.com/your-org
AZURE_DEVOPS_PROJECT    = ""   # e.g. HEALTH-ENT

## Fabric Trial (Phase P — manual, NOT Terraform-managed)
FABRIC_TRIAL_ACTIVATING_USER = ""  # service account or named engineer (becomes capacity admin)
FABRIC_TRIAL_WORKSPACE       = "healthent-pilot"
FABRIC_TRIAL_REGION          = "Australia East"   # region locks at activation — cannot move without deleting items
FABRIC_TRIAL_CAPACITY_NAME   = ""  # name as shown in Fabric UI after activation
FABRIC_TENANT_TRIAL_COUNT    = ""  # trials already used in this tenant (max 5, non-reactivatable)

## Paid Fabric Capacity (filled after Phase P sizing sign-off — ADR-21/25)
FABRIC_DEV_CAPACITY     = ""   # e.g. caphealthentdev  (F4, AU East)
FABRIC_TEST_CAPACITY    = ""   # e.g. caphealthenttest (F4, AU East)
FABRIC_UAT_CAPACITY     = ""   # e.g. caphealthentuat  (F8, AU East)
FABRIC_PROD_CAPACITY    = ""   # e.g. caphealthentprod (F64, AU East)
FABRIC_DR_CAPACITY      = ""   # e.g. caphealthentdr   (F32, AU Southeast)

## Azure SQL Control Plane (per env — Phase 4/9). R-15: each DB needs PITR + geo-backup (control-plane-backup-restore.md)
CTRL_CONN_DEV           = ""   # ADO connection string for sqldb-healthent-control-dev (private endpoint)
CTRL_CONN_TEST          = ""
CTRL_CONN_UAT           = ""
CTRL_CONN_PROD          = ""

## Key Vault names (per domain, prod — filled in Phase 5)
KV_CLINICAL_PROD        = "kv-healthent-clinical-prod"
KV_FINANCE_PROD         = "kv-healthent-finance-prod"
KV_OPERATIONS_PROD      = "kv-healthent-operations-prod"
KV_HR_PROD              = "kv-healthent-hr-prod"
KV_AUDIOLOGY_PROD       = "kv-healthent-audiology-prod"
KV_DYNAMICS_PROD        = "kv-healthent-dynamics-prod"

## Workspace GUIDs (filled as provisioned — needed for abfss:// paths)
WS_GUID_PILOT           = ""
WS_GUID_CLINICAL_DEV    = ""
WS_GUID_CLINICAL_PROD   = ""
# ... add per domain/env as provisioned (Finance, Operations, HR, Audiology, Dynamics × Dev/Prod)

## Lakehouse GUIDs (filled as provisioned — needed for abfss:// paths)
LH_GUID_CLINICAL_BRONZE_DEV  = ""
LH_GUID_CLINICAL_SILVER_DEV  = ""
LH_GUID_CLINICAL_GOLD_DEV    = ""
# ... add per domain/layer/env as provisioned

## Service Principal App IDs (filled in Phase 5)
SP_APPID_FABRIC_DEV     = ""
SP_APPID_FABRIC_PROD    = ""
SP_APPID_DEVOPS         = ""
SP_APPID_PURVIEW        = ""

## Break-glass / emergency PHI access (Phase 5 — G-10; break-glass-access.md)
BREAKGLASS_ACCOUNT      = ""   # emergency-access account UPN — heavily alerted, audited, time-boxed
BREAKGLASS_APPROVER     = ""   # authoriser + post-use reviewer

## Terraform State Backend (filled after bootstrap in Phase 4)
TF_STATE_STORAGE_ACCOUNT = ""  # e.g. sthealthentstate
TF_STATE_RESOURCE_GROUP  = ""  # e.g. rg-healthent-bootstrap
TF_STATE_CONTAINER       = "tfstate"

## Phase 16 ML Use Case (before Phase 16 entry — ADR-27)
ML_USE_CASE_NAME        = ""   # chosen from gameplan §Phase 16 candidates
ML_USE_CASE_ADR         = ""   # e.g. ADR-27-ml-use-case-selection
ML_USE_CASE_CTO_SIGNOFF = ""   # date of CTO approval
ML_LAWFUL_BASIS         = ""   # APP 6 / HREC position (G-05) — required before any PHI in ML

# ===== PRE-PHASE-P GATE (answer ALL before activating trial / before load test) =====
# gameplan §10 (Q-1..Q-4) + Phase P sizing contingency (R-19/G-16). Gates paid spend.
Q1_TENANT_AND_ADMIN     = ""   # tenant hosting Fabric + admin to create groups/SPs? (Y/N + tenant)
Q2_AU_EAST_CONFIRMED    = ""   # AU East available for Fabric capacity? (Y/N)
Q3_TRIALS_USED          = ""   # trials already activated in tenant? (number; max 5)
Q4_NAMED_ACTIVATOR      = ""   # named activator with Fabric Admin role? (who)
PHASE_P_BUDGET_CEILING  = ""   # funded envelope the SKU recommendation must fit
PHASE_P_ESCALATION_PATH = ""   # escalate to CTO + DE Manager if SKU exceeds ceiling OR F64 insufficient

# ============================== SESSION STATE ==============================
# Paste the Session Handoff block (CLAUDE.md §0) after each session.

Date       : (not yet started)
Phase      : (not yet started)
Last step  : (not yet started)
Next step  : Complete the PRE-PHASE-P GATE + fill ENVIRONMENT IDENTITY, then begin Phase P step 1.
Files created/modified this session:
  - none yet
Decisions made:
  - none yet
Open items / blockers:
  - PRE-PHASE-P GATE Q-1..Q-4 unanswered; Phase P budget ceiling (R-19) not yet agreed
Next session start instruction:
  Read CLAUDE.md, gameplan.md, and CLAUDE.local.md. Confirm the PRE-PHASE-P GATE is
  answered and ENVIRONMENT IDENTITY filled. Then begin Phase P step 1 (trial activation).
```

---

## 36. Test-Data Strategy — No Raw PHI in Non-Prod *(added by 2026-06 review, G-03; ADR-29)*

Raw production PHI **never** leaves Prod — not for "realistic testing," reproducing a prod bug, performance work, or a demo. Dev, Test, and UAT use **synthetic or de-identified** data only (§3.13–3.14). This is a hard boundary, not a guideline.

- **How non-prod data is produced:** choose and record the mechanism in ADR-29 — synthetic generation (schema-faithful fake data), or **de-identified** extracts produced by an approved, irreversible de-identification process (see §37). A masked view over real PHI is **not** de-identification and must not be copied down.
- **Volume/shape for load tests:** Wave-0 and performance tests need representative *volume and distribution*, not real values — generate scaled synthetic data that matches cardinality, skew, and growth, so sizing (Phase P, §15.11) stays valid without moving PHI.
- **Enforcement:** no pipeline, shortcut, export, or backup/restore path may move Prod Bronze/Silver into a lower environment. `scripts/verify-access.sh` + `tests/security` assert non-prod stores contain no production PHI markers; promotion is code-and-config only.
- **Cross-references:** §3.14 (no raw PHI outside Prod), §12 DoD ("non-prod data is synthetic/de-identified"), §37 (de-identification standard), gameplan R-16.

---

## 37. De-identification, Retention & Notifiable Data Breaches *(added by 2026-06 review, G-01/G-02/G-04; ADR-30)*

These are **legal/clinical-governance** obligations a senior engineer must surface but cannot decide alone — they need Privacy Officer / Legal sign-off. Record the agreed positions in ADR-30 and the runbooks below; they gate the relevant phases.

**De-identification standard (G-04).** "Masked" ≠ "de-identified." Define, in ADR-30, what de-identification means for this platform against the **OAIC de-identification guidance** — including the audiology-specific **re-identification risk** (audiogram patterns, rare diagnoses, small clinics + DOB/postcode can re-identify even without name). State the technique (suppression/generalisation/perturbation/pseudonymisation), who may re-identify (if anyone) and how that mapping is protected, and the residual-risk acceptance. This standard is the approved source for §36 non-prod data and for any Phase 16 ML feature set.

**Retention & disposal + right to erasure (G-02).** Set a **retention/disposal policy** with Legal: health records carry **state-based minimum retention** (commonly ~7 years for adults, and for minors until they reach an age such as 25 — confirm per jurisdiction), after which APP 11.2 requires destruction/de-identification when no longer needed. The platform-specific trap: **Delta time-travel and OneLake retention keep "deleted" PHI** in prior file versions, so a soft-delete or `DELETE` does **not** satisfy an APP 13 / erasure request on its own. The policy must define how erasure is honoured through **VACUUM / retention-window expiry / physical removal** on Bronze, Silver, Gold, *and* the control plane, with evidence. Encode retention windows in `meta` where the framework enforces them.

**Notifiable Data Breaches (G-01) — the most urgent compliance gap.** HEALTH-ENT is an APP entity handling health information and is subject to the **Notifiable Data Breaches scheme (Privacy Act 1988, Part IIIC)**. There must be a standing process — not improvised under pressure — in `docs/runbooks/ndb-breach-response.md` covering: detection → **eligible-data-breach assessment within 30 days** → containment → if likely serious harm, **notify the OAIC and affected individuals** → record-keeping. This is a **separate workflow from technical incident MTTR** (§32): the 30-minute "PHI breach" target is *containment*; NDB is *statutory notification*, owned jointly by the Privacy Officer and the program. Any P1 PHI-exposure incident invokes both. (My Health Records Act obligations are tracked separately under ADR/Q — confirm whether HEALTH-ENT interacts with the My Health Record system, as it adds its own mandatory-notification and access-offence regime.)

**Cross-references:** §7 (security controls), §20 (control-plane DR + retention), §32 (incident vs notification), §36 (test data), gameplan R-17, ADR-30.

---

## 38. Greenfield Implementation Guide — the living master build document *(user-directed, 2026-06-20)*

There is **one master implementation document**: `docs/implementation/greenfield-implementation-guide.md`
(docs repo). It is the single, **phase-aligned**, **no-ambiguity**, step-by-step build guide for the entire
program — written so that someone with no prior context can stand the platform up from nothing and run it to
completion. It is **living**: it is updated in the *same change* as any code, config, or decision that affects
how the platform is built. A change is not "done" until this guide reflects it.

**What it must contain, per phase (P and 0–18), in order:**
- **Where to start / where to finish** — the entry gate that lets the phase begin and the exit gate that ends it.
- **Step-by-step implementation** — numbered, executable, unambiguous; the exact commands / REST calls / SQL /
  code, the repo each artifact lands in, and the verification after each step. Embed the decisive code/commands
  inline; for bulk artifacts (full DDL, the wheel, Terraform modules) cite the **canonical file path** and how
  to apply it — never duplicate large code blocks into the guide (duplication rots; the repo is the source of
  truth). This anti-drift rule is itself documented in the guide.
- **Trade-offs · Risks · Recommendations** — the *why* behind each decision, the ADR it ties to, what can go
  wrong, and the recommended path.
- **Definition of Done (DoD) for the phase** — the explicit, checkable list that closes the phase (its gameplan
  exit criteria + the §12 DoD + its four governance docs per §34).

**Alignment rule (non-negotiable):** the guide, the gameplan, every ADR, every `docs/phases/phase-NN/*` doc,
every runbook (`docs/runbooks/*`), and `recreate-platform.md` must stay mutually consistent. When any one
changes, reconcile the others in the same session. The guide is the **spine**; per-phase deep detail lives in
each phase's `implementation.md` and in `recreate-platform.md` (IaC layers) — the guide links to them and never
contradicts them. If two documents disagree, fix it; do not leave the contradiction.

**Depth honesty:** phases that are actually built (Phase P + the metadata framework) are deep with real code/
commands; phases not yet built carry the authoritative ordered steps + DoD and are marked "deepen at build" —
they are filled in as each phase is delivered. Never fabricate code for an unbuilt phase.

---

*Last updated: June 2026 (amended 2026-06 per `docs/review/program-review.md`; §38 added 2026-06-20) | Maintained by: Senior Data Engineer | Repos: docs / infra / platform / sql*
