# Data Engineer Onboarding Runbook - starting and deploying any dataflow

> Companion to the **[metadata-cookbook](metadata-cookbook.md)** (which holds the table-by-table
> entry reference and full examples). This runbook is the **process**: how to start, where to
> work, what to avoid, which pipeline to run, and how to deploy. Same sync rule applies:
> schema or pipeline changes must update this doc in the same PR.

## 1. Day-1 checklist - starting a new dataflow project

| # | Step | Tool / where |
|---|---|---|
| 1 | Pick the `dag_uid` - lowercase snake_case, **stable forever** (it keys folders, metadata, CI/CD, runtime, audit) | naming: `df_{domain}_{subject}` |
| 2 | Branch `feature/{ticket}-{dag_uid}` off `dev` (§25) | dataflows repo |
| 3 | Scaffold: `python scripts/new_dataflow.py --dag-uid <uid> --domain <d> --kind <k> --layers ...` | creates folders + `01_seed_dag.sql` + manifest |
| 4 | Write the metadata seeds 02-06 per the **cookbook scenario matrix** (reuse existing connections/objects - UNIQUE constraints stop duplicates) | `metadata/{uid}/` |
| 5 | Write DE code **only** where the matrix says (transform SQL/PySpark; reference example: `df_audiology_appointments`) | layer `Notebook/{uid}/`, `DDL/{uid}/` |
| 6 | Run the **static test suite**: `dataflows-run-tests` (suite=static) | parse + scaffolder checks |
| 7 | One PR → review per §25 | ADO |
| 8 | Deploy + run (see §4 below) | pipelines |

## 2. Where to work - workspaces & capacity for development/analysis

| Activity | Workspace | Capacity | Rules |
|---|---|---|---|
| Exploratory analysis / notebook dev | **`healthent-{domain}-dev`** (your domain's Dev workspace) | **F4 - the least-capacity paid SKU in the plan (§8), PAUSED when idle** | **Synthetic/de-identified data only (§36 - hard rule, no raw PHI ever in dev)**; attach `env-healthent-framework`; no `pip install` in cells (§33) |
| Pilot-phase work (before paid SKUs exist) | `healthent-pilot` | Trial (≈F64, 60 days) | same data rules |
| Heavier perf experiments | Dev, scheduled window | F4 (resume → run → pause) | if F4 genuinely insufficient, raise it - don't run on UAT/Prod |
| ❌ Never | UAT / Prod workspaces | - | no development, no ad-hoc analysis, no "quick checks" against Prod PHI (JIT/PIM only, §7) |

> Cost note: pausing the Dev capacity when idle is the default lever (ADR-26). If pure-analysis
> demand grows, an **F2 sandbox capacity** is a Phase-4 sizing option - raise it, don't assume it.

## 3. What to AVOID (anti-patterns - most fail CI automatically)

| ❌ Anti-pattern | Why / what catches it |
|---|---|
| Hardcoded `abfss://` paths anywhere | env drift + typos; use logical refs → ADR-36 resolver. Caught in PR review |
| Secrets or connection strings in `param_value` / code | §7; use `is_secret_ref=1` + KV secret **name** (CHECK-enforced) |
| Per-environment config files in the repo | the rejected `app_config/*.json` antipattern; env resolves at run time |
| A new pipeline for your flow | never - the generic runner executes all flows (§15.9); onboarding = metadata |
| Editing framework notebooks (`nb_*` in platform) | framework-owned; raise a PR to platform with platform-engineer review |
| Duplicating an existing `ingestion_object`/connection | reuse via lookup; UNIQUE constraints reject duplicates at deploy |
| Skipping column classification on PHI | **`resolution` test suite fails** on unmasked Gold PHI (ADR-33) |
| Security DDL (GRANT/RLS/DDM) in dataflows or bi SQL | framework-generated only; **bi security lint fails the build** |
| `SELECT *` in serving views / DDL | §5; explicit column lists |
| Raw PHI in dev/test for "realistic testing" | §36 hard boundary - synthetic/de-identified only |
| `dbutils.widgets`, inline `pip install`, nested ForEach | §6/§33/ADR-18 |
| `DELETE + INSERT` instead of MERGE | §5; not idempotent |
| One semantic model per dataflow | ADR-36 §7 - models are per subject area, in `bi` |

## 4. Which CI/CD pipeline to use, when *(names + single key updated 2026-06-12)*

> **The only value you ever type into a pipeline is your `project_code`** (e.g. `HEARING_P1` -
> issued by the scaffolder, see the section below). The `dag_uid` is resolved automatically
> from `metadata/{project_code}/manifest.yml`; you never retype it after scaffolding.

| You want to... | Run pipeline | Key parameters |
|---|---|---|
| **Start a new dataflow project** (folders + PR, code auto-issued) | `dataflows-new-project` | `dag_uid` (typed ONCE, here) + `domain` + `kind` + `layers` |
| Deploy/refresh your flow's **metadata** to the control DB | `dataflows-deploy-metadata` | `project_code` + `env` |
| Deploy your flow's **DDL and/or notebooks** | `dataflows-deploy-code` | `project_code` + `env` + `scope` (DDL/Notebook/Both) + `layers` |
| **Run** your flow end-to-end (incl. the post-run DQ gate) | `dataflows-run-flow` | `project_code` + `env` (+ `wait_for_completion=true`) |
| Validate the whole repo's seeds/DDL **before PR** | `dataflows-run-tests` | `suite=static` |
| Prove env wiring (connections/KV/storage/PHI gates) | `dataflows-run-tests` | `suite=resolution` + `env` |
| Test **your one flow** (mock data, DDL gate, live run) | `dataflows-test-one-flow` | `project_code` + tick-boxes |
| BI: deploy models/reports/warehouse views | `bi-deploy` | `env` + `domain` + `scope` (+ `item`) - BI is keyed by domain, never by project_code (ADR-36 §7) |
| Merge gates (run automatically on every PR - not started by hand) | `dataflows-pr-validation` / `platform-pr-validation` / `bi-pr-validation` | - |

**Standard lifecycle of a new flow (dev):**
1. `dataflows-new-project` → issues your `project_code`, opens the PR.
2. Fill the seeds in the PR (cookbook) → `dataflows-pr-validation` runs automatically → merge.
3. `dataflows-deploy-metadata(project_code, dev)` → seeds land in the control DB.
4. `dataflows-deploy-code(project_code, dev, Both, all)` → only for transform flows (ingestion is metadata-only).
5. `dataflows-run-tests(resolution, dev)` → wiring gates all zero.
6. `dataflows-run-flow(project_code, dev, wait=true)` → run + DQ gate; results in the ADO **Tests** tab + the `log.*` run spine.
Promotion to uat/prod re-runs steps 3-6 per env behind approvals (§25/§31, Phase 6).

## 5. Recommendations (the short list)
1. **Metadata first, code last** - most flows need zero code (ingestion/extraction are config-only).
2. **Copy the worked example** (`df_audiology_appointments`) - it exercises every table and both code surfaces.
3. **Small flows over mega-flows** - one subject area per `dag_uid`; batches give you ordering inside it.
4. Classify columns at seed time (PII/PHI/mask) - retrofitting classification is rework + a CI failure.
5. Pair every PHI table with **purge + vacuum** rules (§37 - a DELETE alone does not erase).
6. Watch your run in `log.dag_run → batch_run → ... → dq_result` - that spine is also the audit trail.


## How do I get my project number? (you DON'T pick it)

You never find, choose, or type a project number, and you never create the folders by hand.

1. Run the **dataflows-new-project** pipeline in Azure DevOps (Run -> fill entity, domain, flow_shape).
2. The scaffolder reads metadata/project-register.md, takes the highest number in the SINGLE
   GLOBAL `HEARING_P{n}` sequence (domain-independent; the domain lives in the dag_uid) and
   **issues the next one** (e.g. HEARING_P4 if HEARING_P3 is the last).
   You see it in the run output: project_code ISSUED by register: HEARING_P4.
3. It then creates ALL your folders named with that code ({layer}/{DDL|Notebook}/HEARING_P4/,
   metadata/HEARING_P4/), writes the manifest (code included), appends the register row, and
   opens your PR. Your only job: fill the seeds and the manifest owner/description.

Race safety: if two engineers scaffold at the same moment, the PR merge conflict on the
register plus the UNIQUE index on meta.dag.project_code catch the collision - first merge
wins, the other re-runs the scaffold (gets the next number). Working locally instead of ADO:
python framework/tools/scaffold/new_dataflow.py --dag-uid ... --domain ... --kind ...
(platform repo tools) - identical auto-issue.
