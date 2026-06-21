# CLAUDE.local.md — Local Context & Session State
# NOT committed — listed in .gitignore of every repo
# Copy this file to each repo root: docs / infra / platform / sql
#
# PURPOSE:
#   1. Environment identity  — workspace names, IDs, connection strings (never in Git)
#   2. Session state         — paste the Session Handoff block here after every session
#                              so Claude can resume exactly where you left off
#
# HOW TO USE (Cursor):
#   Session start : @-mention CLAUDE.md + gameplan.md + this file (Cursor does NOT
#                   auto-load them the way Claude Code loads CLAUDE.md).
#   Session end   : paste the Session Handoff block (output by Claude per CLAUDE.md §0)
#                   into the SESSION STATE section below, save, close Cursor.
#
# Fill in the ENVIRONMENT IDENTITY + PRE-PHASE-P GATE sections before Phase P.
# Leave fields blank until the relevant phase provisions them.
#
# Aligned to CLAUDE.md §35. Amended 2026-06 per docs/review/program-review.md:
#   adds the §10 pre-Phase-P gate answers, the Phase-P sizing budget ceiling (R-19/G-16),
#   and the break-glass account (G-10). Keeps this file and the §35 template in sync (closes G-23).

# ==============================================================================
# ENVIRONMENT IDENTITY
# ==============================================================================

## Azure
AZURE_SUBSCRIPTION_ID   = "de042197-820a-4f37-b778-c4a0dbef6a6c"   # confirmed 2026-06-10 (portal URL)
AZURE_TENANT_ID         = "c1da4ebf-8959-4d86-93db-4a0b70f777d0"   # Samestantil44outlook.onmicrosoft.com (confirmed via az 2026-06-10)
AZURE_DEVOPS_ORG        = "https://dev.azure.com/earlake"   # discovered + confirmed 2026-06-11 (Sam_estantil44@outlook.com; pre-existing project EarLake NOT touched)
AZURE_DEVOPS_PROJECT    = "Fabric"   # created 2026-06-11; 4 repos pushed main+dev: healthent-fabric-{docs,platform,dataflows,bi}; default empty repo deleted; CLAUDE.md/CLAUDE.local.md gitignored (ADR-37)

## Fabric Trial (Phase P — manual, NOT Terraform-managed)
FABRIC_TRIAL_ACTIVATING_USER = "fabric-admin@Samestantil44outlook.onmicrosoft.com"  # objectId f7c47459-0b86-426f-8e00-38cd9c8d15af; Fabric Administrator role assigned 2026-06-10; temp pwd forced-change-at-first-signin (NOT stored here)
FABRIC_TRIAL_WORKSPACE       = "healthent-pilot"
FABRIC_TRIAL_REGION          = "Australia East"   # confirmed AU East — cannot change without deleting items
FABRIC_TRIAL_CAPACITY_NAME   = "Trial-20260610T063353Z-j99yHvBuvEuUH81DM6gO1g"  # id 1d32dc5f-eeed-4552-a870-4a3997980597, FTL4, Australia East, ACTIVE (started 2026-06-10). CU CONFIRMED 2026-06-16 via Capacity Metrics app = 4 CU (F4-class, NOT F64). Trial is NOT resizable/promotable to F64 - a representative F64 load test needs the paid trial->paid swap (R-19). Second trial Trial-20260608... also FTL4 (verified via Fabric/PBI capacities API 2026-06-16).
FABRIC_TENANT_TRIAL_COUNT    = "2"  # 2026-06-08 + 2026-06-10 activations — 3 remain, use NONE casually

## Paid Fabric Capacity (filled after Phase P sizing sign-off — ADR-21/25)
FABRIC_DEV_CAPACITY     = ""   # e.g. caphealthentdev  (F4, AU East)
FABRIC_TEST_CAPACITY    = ""   # e.g. caphealthenttest (F4, AU East)
FABRIC_UAT_CAPACITY     = ""   # e.g. caphealthentuat  (F8, AU East)
FABRIC_PROD_CAPACITY    = ""   # e.g. caphealthentprod (F64, AU East)
FABRIC_DR_CAPACITY      = ""   # e.g. caphealthentdr   (F32, AU Southeast)

## Azure SQL Control Plane (per env — filled as each env is provisioned in Phase 4/9)
# Reminder (R-15): each control DB needs PITR + geo-backup; see docs/runbooks/control-plane-backup-restore.md
CTRL_CONN_DEV           = ""   # full ADO connection string for sqldb-healthent-control-dev (private endpoint)
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

## Workspace GUIDs (filled as workspaces are provisioned — needed for abfss:// paths)
WS_GUID_PILOT           = "ee46ac62-b9be-48b9-b291-fea8b1b810b8"   # created via API 2026-06-10, on trial capacity; fabric-admin = Admin
WS_GUID_CLINICAL_DEV    = ""
WS_GUID_CLINICAL_PROD   = ""
WS_GUID_FINANCE_DEV     = ""
WS_GUID_FINANCE_PROD    = ""
WS_GUID_OPERATIONS_DEV  = ""
WS_GUID_OPERATIONS_PROD = ""
WS_GUID_HR_DEV          = ""
WS_GUID_HR_PROD         = ""
WS_GUID_AUDIOLOGY_DEV   = "(deleted 2026-06-11 — one-workspace consolidation; was e87a0d11)"
WS_GUID_BI_PILOT        = "1d915b00-37aa-4efa-9053-398172cfa892"  # healthent-bi-pilot (trial cap, 2026-06-11): BI team ws (bi repo-backed, ADR-37); semantic models+reports only; consumers get APPS; fabric-admin=Admin
WS_GUID_AUDIOLOGY_PROD  = ""
WS_GUID_DYNAMICS_DEV    = ""
WS_GUID_DYNAMICS_PROD   = ""

## Lakehouse GUIDs (filled as lakehouses are provisioned — needed for abfss:// paths)
# ADR-49: single lakehouse per layer (lh_bronze/silver/gold/archive). The live pilot
# items were renamed in Fabric 2026-06-19 (REST 200); the GUIDs below are unchanged,
# only the key names were updated from the old per-domain lh_audiology_* scheme.
LH_GUID_BRONZE_PILOT   = "04bee495-7e52-448d-a0b6-5c57947abc2e"   # lh_bronze (was lh_audiology_bronze), schema-enabled, 2026-06-10
LH_GUID_ARCHIVE_PILOT  = "22bfad33-1568-4ef3-a59f-945368155406"   # lh_archive (was lh_audiology_archive), ADR-49 archive zone
LH_GUID_SILVER_PILOT   = "cabdea20-f0e3-4d3c-9aac-6dfcfa53fef0"   # lh_silver (was lh_audiology_silver)
LH_GUID_GOLD_PILOT     = "252c9f44-8ea6-4316-aead-38cac86da20d"   # lh_gold (was lh_audiology_gold)
# wh_audiology created 2026-06-10 (id via /warehouses list when needed)
# NOTE: pilot items created under the personal-user token (pilot = disposable, runbook §10);
#       durable-owner discipline (fabric-admin) applies from Phase 4 paid envs onward.
LH_GUID_CLINICAL_BRONZE_DEV  = ""
LH_GUID_CLINICAL_SILVER_DEV  = ""
LH_GUID_CLINICAL_GOLD_DEV    = ""
LH_GUID_CLINICAL_BRONZE_PROD = ""
LH_GUID_CLINICAL_SILVER_PROD = ""
LH_GUID_CLINICAL_GOLD_PROD   = ""
# ... add per domain/layer/env as provisioned

## Service Principal App IDs (filled in Phase 5)
SP_APPID_FABRIC_DEV     = ""
SP_APPID_FABRIC_PROD    = ""
SP_APPID_DEVOPS         = ""
SP_APPID_PURVIEW        = ""

## Entra security groups (foundation created LIVE 2026-06-11; Terraform-imported at Phase 5)
SG_PLATFORM_ADMIN       = "fddfcbc0-9dbe-458b-9a01-afaa7f1e67ee"  # sg-healthent-platform-admin (member: fabric-admin)
SG_AUDIOLOGY_ENG        = "5e2843b9-00d1-4886-9972-5a9a5ed82042"  # sg-healthent-audiology-eng
SG_AUDIOLOGY_READ       = "bb713783-1ab7-4963-b1c7-36e580242cee"  # sg-healthent-audiology-read
# remaining 5 domains x 3 roles + PIM/CA/access-matrix = Phase 5 (module: infra/modules/entra_groups)

## Break-glass / emergency PHI access (filled in Phase 5 — G-10; docs/runbooks/break-glass-access.md)
BREAKGLASS_ACCOUNT      = ""   # emergency-access account UPN — heavily alerted, audited, time-boxed
BREAKGLASS_APPROVER     = ""   # who authorises activation + runs the mandatory post-use review

## Terraform State Backend (filled after bootstrap in Phase 4)
TF_STATE_STORAGE_ACCOUNT = ""   # e.g. sthealthentstate
TF_STATE_RESOURCE_GROUP  = ""   # e.g. rg-healthent-bootstrap
TF_STATE_CONTAINER       = "tfstate"

## Phase 16 ML Use Case (filled before Phase 16 entry — required ADR-27)
ML_USE_CASE_NAME        = ""   # chosen from gameplan.md §Phase 16 candidates
ML_USE_CASE_ADR         = ""   # e.g. ADR-27-ml-use-case-selection
ML_USE_CASE_CTO_SIGNOFF = ""   # date of CTO approval
ML_LAWFUL_BASIS         = ""   # APP 6 secondary-use basis / HREC position (G-05) — required before any PHI in ML

# ==============================================================================
# PRE-PHASE-P GATE  (answer ALL before activating the trial / before the load test)
# Source: gameplan.md §10 (Q-1..Q-4) + Phase P sizing contingency (R-19 / G-16).
# These gate paid spend — do not skip.
# ==============================================================================

Q1_TENANT_AND_ADMIN     = "YES — Samestantil44outlook.onmicrosoft.com (c1da4ebf-...); signed-in user CONFIRMED Global Administrator via Graph 2026-06-10"
Q2_AU_EAST_CONFIRMED    = "YES — verified via Fabric API 2026-06-10: trial capacity region = Australia East"
Q3_TRIALS_USED          = "2 (of 5) — both active, AU East"
Q4_NAMED_ACTIVATOR      = "fabric-admin@Samestantil44outlook.onmicrosoft.com — durable member user, Fabric Administrator (created+assigned via az/Graph 2026-06-10)"

# Sizing contingency (R-19 / G-16) — agree BEFORE running the Phase P load test:
PHASE_P_BUDGET_CEILING  = "DEFERRED — CTO decision (R-19 OPEN, user 2026-06-14). No number set; capacity recommendation stays INTERIM. NO paid F64 provisioned — stay on the free trial ($0). AU cost reference for when it's set: F8 ~$1,606/mo PAYG (~$1,124 Reserved); F64 ~$12,848 PAYG (~$8,994 Reserved); interim rec (non-prod paused + Prod F8+Pro @250 viewers) ~$5,349/mo."
PHASE_P_ESCALATION_PATH = "CTO + DE Manager set the ceiling when paid spend is funded. Until then: no representative F64 load test (trial is FTL4); recommendation = INTERIM (AU rates + estimator model). Revisit when funded."

# ==============================================================================
# SESSION STATE
# Paste the Session Handoff block output by Claude (CLAUDE.md §0) after each session.
# ==============================================================================

---
SESSION HANDOFF
Date       : 2026-06-21 (session 31c - red-pipeline fixes, visible DDL, HEARING_P4 archival, operating-model corrections; CLOSE)
Phase      : P - Pilot on Trial (OPEN). Next session = PHASE 1 DISCOVERY + requirements gathering (the real start).
             Repo HEADs (all main=dev=uat, pushed): platform 69c9ebf, dataflows 536d6b8, docs 236e60d, bi a569894.
Last step  : (1) Removed the manual EarLake "dashboard" hack (one-off Copy pipeline + copied tables + hand-made
             views + ad-hoc connections/shortcuts) - it violated the metadata-driven rule. (2) Root-cause-fixed
             all 6 RED pipelines (committed): platform-build-wheel (ruff E702 + pyspark importorskip + pyyaml);
             dataflows-pr-validation (gen_ddl Spark->T-SQL type normalise); ops-env-smoke (drop shell=True token
             banner); ops-environment-rebuild (PYTHONUTF8); platform-release (wheel version sync 0.4.5->0.4.12 +
             test_version_sync); finops-cost-report (best-effort push); infra-deploy (named-skip until backends).
             (3) gen_ddl.py NEW = visible CREATE TABLE contract DDL from manifest (bronze+gold, §29 SCD2 cols) +
             DDL-drift gate; generated for P1/P2/P3. gen_views layer-aware; gen_source_catalogue (register from
             meta). (4) HEARING_P4 (df_audiology_archival) scaffolded = Synapse archival backfill (file/Parquet
             from EarLake gold STORAGE, snapshot_archive -> archive zone, rowhash, auto_map/no-discovery);
             validate=OK; gen_seeds now treats columns as OPTIONAL for auto_map. Onboards VIA CICD only.
Next step  : START PHASE 1 - DISCOVERY + REQUIREMENTS. Prereq the USER provides: READ-ONLY org Azure/Synapse
             access (org email + user access) - metadata/volumetrics only, NO PHI. Then run the discovery tooling
             (scripts/discovery/inventory_synapse.py + dictionary_to_manifest.py) -> ADR-45 source dictionaries +
             phase-01 docs (implementation/finops/risk/runbook + dsd). FIRST also resolve the CI-capacity blocker
             (below) so pipelines can run again.
Files created/modified this session: see docs/decisions/session-log.md session 31c (full list + per-commit SHAs).
             Headlines: platform - gen_ddl.py NEW, gen_source_catalogue.py NEW, gen_views.py (layer-aware), 
             gen_seeds.py (optional columns), load_metadata.py, check_env_version.py, wheel pyproject (0.4.12),
             3 test modules (pyspark importorskip) + test_version_sync NEW, 6 devops/pipelines fixes + 2 templates.
             dataflows - metadata/HEARING_P4/** NEW, bronze/DDL + gold/DDL/** (visible DDL), project-register.
             docs - migration/{synapse-archival-ingestion-strategy, ingestion-source-catalogue} NEW,
             architecture/{gold-dim-date-and-conformed-dimensions, ingestion-path-default-and-exceptions} NEW,
             governance/ai-assisted-development-operating-model NEW, finops/capacity-estimate-for-cto NEW,
             delivery/master-delivery-plan + phases/*/dsd.md x20 + templates/phase-dsd-template NEW,
             ADR-52/53 NEW, decisions/session-log, gameplan, cls-rls/access-matrix/dummys-17.
Decisions made (BINDING, recorded as ADR/governance):
  - ADR-51 final: serving = lakehouse SQL-endpoint views (NO separate Warehouse); ADR-52: all object changes via
    CICD/least-privilege; ADR-53: Gold view security = CLS-by-omission + group-only RLS, gen_views-generated.
  - Operating model (Phase 1+): NO manual metadata (all via CICD); NO AI footprint; AI prepares LOCALLY, USER
    reviews + syncs + RUNS pipelines (I do not trigger/the user cancels mine); cloud access = user's + read-only;
    every change ships as a guideline. Default ingestion path = origin source -> Bronze->Silver->Gold->dashboard
    through the framework, with 7 documented exceptions (closed rule).
  - Delivery tracking = master-delivery-plan + per-phase dsd.md (generated from one phase table).
Open items / blockers:
  - **CI CAPACITY (do first next session):** ADO org `earlake` is OUT of free Microsoft-hosted pipeline minutes
    -> all runs fail instantly. The 6 pipeline fixes are committed + correct but UNRUN/UNVERIFIED. Unblock:
    self-hosted agent (free/immediate, set pool: {name: Default}) OR request the free parallelism grant (form,
    ~2-3 days) OR wait for monthly reset OR buy 1 hosted job. USER decision.
  - PHASE 1 needs USER to grant read-only org Synapse/Azure access.
  - Phase-P exit UNCHANGED: R-19 budget ceiling (CTO) -> trial->F64 -> Wave-0 load test -> capacity sign-off.
  - HEARING_P4 + the 3 examples onboard via CICD once capacity returns. EarLake (syn-earlake-dev-aue-001 /
    stearlakedevaue001) gold = Parquet, silver = Parquet, bronze = CSV (none Delta). Trial expiry ~2026-08-08.
Next session start instruction:
  Read CLAUDE.md, gameplan.md, CLAUDE.local.md (this block) + session-log session 31c. (1) Resolve the CI
  capacity blocker (self-hosted agent or parallelism grant) so the committed pipeline fixes can be run-verified.
  (2) BEGIN PHASE 1 DISCOVERY: get read-only org Synapse access from the USER, run the discovery tooling,
  produce the ADR-45 dictionaries + phase-01 docs + dsd. Operate in the new mode: prepare locally, the USER
  reviews + syncs + runs; no manual metadata; no AI footprint.
---

# ----- superseded (session 31) -----
---
SESSION HANDOFF
Date       : 2026-06-21 (session 31 - pilot Git drift FIXED: the session-30 follow-up)
Phase      : P - Pilot on Trial (OPEN; exit gate UNCHANGED). Repo SHAs unchanged (no code commits):
             platform d5435c5, bi 72fc9e5, dataflows 15341cc. docs advanced to 7dba72a (main=dev=uat,
             FF + SHA-verified) = session-log session-31 entry only.
Last step  : Fixed the pilot workspace Fabric Git drift that returned UnknownError on updateFromGit since
             2026-06-11. Root cause = corrupted sync baseline (workspaceHead pinned at 0c1146a3 / 2026-06-11
             vs remote dev d5435c5; 14 drifted items incl. 5 real notebook Conflicts + the env-id/SlvrAudlgy
             workspace-only items). Repair (live Fabric Git REST on ws ee46ac62): (1) confirmed updateFromGit
             -> 400 UnknownError isRetriable:false; (2) /git/disconnect -> NotConnected; (3) /git/connect
             (earlake/fabric/healthent-fabric-platform, dev, /framework/fabric-items) -> Connected;
             (4) /git/initializeConnection PreferRemote -> baseline reset, requiredAction UpdateFromGit;
             (5) /git/updateFromGit PreferRemote+allowOverrideItems -> 202, op 9ab7027d polled to Succeeded.
             RESULT (verified): ConnectedAndInitialized; workspaceHead == remoteCommitHash == d5435c5; deep
             Conflict/SameChanges drift gone; nb_admission + pl_admission_master pulled in; updateFromGit now
             works. 7 remaining git/status items are benign workspace-side re-serialization (conflictType None,
             pilot-specific bindings) and must NOT be committed back to dev.
Next step  : UNCHANGED Phase-P closer (the only thing that closes P): R-19 budget ceiling (USER/CTO) -> upgrade
             trial to F64 -> Wave-0 load test -> capacity_estimator on real CU telemetry -> capacity
             recommendation FINAL -> sign-off. OR start Discovery (Phase 1) the moment the USER grants
             read-only org Azure/Synapse access (az login to the org tenant + Synapse ws + RG; metadata/
             volumetrics only) -> produces the ADR-45 dictionaries + phase-01 docs.
Files created/modified this session:
  - healthent-fabric-docs/docs/decisions/session-log.md (session-31 entry; commit 7dba72a, pushed main=dev=uat)
  - root (gitignored): CLAUDE.local.md (this block)
  - LIVE Fabric: pilot ws ee46ac62 Git connection disconnected/reconnected/re-initialized to dev@d5435c5
Decisions made (locked, no new ADR):
  - Repairing a corrupted Fabric Git sync baseline (UnknownError on updateFromGit, isRetriable:false) =
    disconnect -> reconnect -> initializeConnection(PreferRemote) -> updateFromGit; never a bare retry.
    Pilot-side re-serialized item deltas are benign and are never pushed to the canonical branch.
Open items / blockers:
  - Phase-P closer: R-19 ceiling (USER/CTO) -> F64 load test -> capacity sign-off (the only closer).
  - Discovery (Phase 1): needs read-only org Azure/Synapse access from the USER.
  - ADR-20/31 Dataverse: needs a real Dataverse org. Trial expiry ~2026-08-08.
Next session start instruction:
  Read CLAUDE.md, gameplan.md, CLAUDE.local.md (this block) + session-log session 31. Pilot Git is healthy
  again (ConnectedAndInitialized, synced to dev@d5435c5). To advance Phase P get the R-19 ceiling and run the
  F64 load test, or START DISCOVERY (Phase 1) if read-only org Synapse access has been granted. Push with the
  az-token bearer lane (FF-check, SHA-verify, no force).
---

# ----- superseded (session 30) -----
---
SESSION HANDOFF
Date       : 2026-06-20 (session 30 / CLOSE - greenfield readiness: 4 TF modules + infra/ado + ADR-49
             infra + DE simplification + cold purge-governed keep-store + BI PBIP + one-run rebuild model
             + deep docs; CI all green; pilot-git partial)
Phase      : P - Pilot on Trial (OPEN; exit gate UNCHANGED). Final pushed SHAs (all main=dev=uat,
             FF + SHA-verified): platform d5435c5, docs ad56cf8, bi 72fc9e5, dataflows 15341cc.
             CI ALL GREEN on main: 781 platform-pr-validation, 782 infra-pr-validation, 783 bi-pr-validation,
             748 dataflows-pr-validation. Full unit suite green; terraform validate+fmt clean (bootstrap/dev/
             test/prod + infra/ado).
Last step  : Session close done. Highlights this session (detail: phase-P/runbook.md "Session 2026-06-20
             evidence ledger" + session-log s26-30):
             - Session-25 OPEN list closed (ADR-49 propagation incl. LIVE storage_target reseed to 5 _shared
               rows; Stage-4 5 params -> test_mode; ADO defs 33/34 registered; ops-rebuild admin gate).
             - DE simplification: metadata/{code} = manifest.yml only; gen_seeds -> generated/; drift gate.
             - 4 new TF modules (service_principals, fabric_git, cold_storage, fabric_environment) wired dev +
               promoted test/prod via annotated tag modules-v1.2.0 (-> dc16bf4).
             - ADR-49 infra alignment: dev/test/prod = ONE shared ws_data (lh_bronze/silver/gold/archive +
               wh_serving) + optional isolated_domains. cold_storage = Cool KEEP-store, NO lifecycle policy
               (purge=meta.purge_rule is sole per-table deletion authority), versioning/soft-delete off.
             - infra/ado composition (project/5 repos/branch-policies/varGroups/OIDC SC/16 pipelines;
               azuredevops v1.15.1; validate-clean; tfvars.example). Greenfield/new-org apply ONLY.
             - BI complete PBIP (AudiologyAppointments Direct Lake TMDL model + report shell; Desktop finalises
               the env Direct Lake connection + report pages).
             - One-run rebuild model: deploy.ps1 content fix (stale list -> current pipelines + control-plane
               DDL inline) + ops-environment-rebuild opt-in reonboard_dataflows stage (inlined, no deadlock).
             - Deep docs: greenfield-implementation-guide (+20 per-phase checklists), greenfield-package
               (all-in-ADO + capacity/per-env + portability), dummys/33 platform-engineering, gameplan Phase-4
               IMPORTANT note (dev = real env).
             - Pilot Git: deleted stray pl_copy_sql_bronze (38e5721b); moved Copy templates OUT of the
               Git-bound folder -> framework/copy-templates (commit d5435c5, fixes DiscoverDependenciesFailed
               class). Pilot still returns Fabric UnknownError on updateFromGit (deep drift since 2026-06-11).
Next step  : 1) Phase-P closer (ONLY thing that closes P): R-19 budget ceiling (USER/CTO) -> upgrade trial to
             F64 -> Wave-0 load test -> capacity_estimator on real CU telemetry -> recommendation FINAL -> sign-off.
             2) Discovery (Phase 1) is ready to run the moment the USER grants READ-ONLY org Azure/Synapse
             access (az login to the org tenant here, or a read SP) + gives the Synapse workspace + RG -
             metadata/volumetrics ONLY, no PHI rows; produces the ADR-45 dictionaries + phase-01 docs.
             3) FOLLOW-UP (free): pilot Git - disconnect/reconnect or rebuild the disposable pilot to clear the
             UnknownError drift. 4) Promote: real-env applies + BI live deploy + cold provisioning + purge job
             are paid/capacity-gated. ADR-20/31 Dataverse needs a real org.
Files created/modified this session:
             Full git-derived list in the chat (session-close item 5). Headlines: platform - infra/modules/
             {service_principals,fabric_git,cold_storage,fabric_environment}, infra/ado/*, infra/scripts/
             create_cold_shortcut.py, infra/envs/{dev,test,prod}/{main,variables}.tf, infra/scripts/deploy.ps1,
             framework/copy-templates/* (moved), gen_seeds.py/new_dataflow.py + tests, 9 devops/pipelines/*.
             docs - implementation/greenfield-implementation-guide.md + gen_phase_checklists.py + 20 phases/*/
             checklist.md, runbooks/greenfield-package.md, dummys/33, review/gaps-and-recommendations.md,
             architecture/{naming,storage-tiering}, decisions/{ADR-49,session-log}, runbooks/recreate-platform,
             phases/phase-P/{runbook,implementation,finops,risk}, timeline/gantt, gameplan. bi - the PBIP +
             end-to-end-sample doc. dataflows - HEARING_P{1,2,3}/generated/.
Decisions made (locked, no new ADR numbers):
  - dataflows sync via the metadata framework (MERGE+prune), NOT terraform: terraform=infra plane,
    dataflows-delivery=flows plane (two apply buttons). Capacity = per-env parameter (paid TF-creates in the
    same apply; trial = the only manual pre-step). DEV is a REAL Azure env like Test/Prod (trial = pilot lever
    only). Substitution-templates (pl_copy_*) live OUTSIDE the Git-bound folder. reonboard = opt-in, not default.
Open items / blockers:
  - Phase-P exit: R-19 ceiling (USER/CTO) -> F64 load test -> capacity sign-off (the only closer).
  - Discovery (Phase 1): needs read-only org Azure/Synapse access from the USER.
  - ADR-20/31 Dataverse: needs a real Dataverse org. Pilot-git UnknownError follow-up. Trial expiry ~2026-08-08.
Next session start instruction:
  Read CLAUDE.md, gameplan.md, CLAUDE.local.md (this block) + session-log s26-30 + phase-P/runbook.md ledger.
  Everything pushed + SHA-verified (5 repos main=dev=uat); CI all green. To advance Phase P get the R-19
  ceiling and run the F64 load test. If the USER has granted read-only org Synapse access, START DISCOVERY
  (Phase 1): az login to the org tenant, confirm metadata/volumetrics-only scope, run scripts/discovery/
  inventory_synapse.py + dictionary_to_manifest.py, produce the ADR-45 dictionaries + phase-01 docs. Push with
  the az-token bearer lane (FF-check, SHA-verify, no force).
---

# ----- superseded (session 27) -----
---
SESSION HANDOFF
Date       : 2026-06-20 (session 27 - six user follow-ups + two CI/CD UX asks: cold-storage readiness,
             DE metadata simplification, end-to-end BI sample, ALL pipelines re-run + 2 failures fixed,
             Fabric-vs-ADO explained, greenfield approach + ADR-49 infra alignment)
Phase      : P - Pilot on Trial (OPEN; exit gates UNCHANGED). Final pushed SHAs (all main=dev=uat,
             FF/SHA-verified): platform 98b2406, docs 6d26aef, bi 48bbf9a, dataflows 15341cc. Full unit
             suite green; ALL 4 PR-validation pipelines GREEN (738 platform, 740 bi, 748 dataflows, 749 infra).
Last step  : Done this session:
             - CI/CD look (user): dataflows-delivery run-panel params reordered (PRIMARY first, advanced
               run_* last, [custom only] tags) + super-clear stage names (Stage N | VERB - what it does).
               ADO has no collapsible param sections; split (#4) rejected.
             - #2 DE simplification: metadata/{code} = manifest.yml ONLY; gen_seeds renders into generated/;
               new_dataflow stops writing the seed template (SEED_TMPL moved into gen_seeds); deploy-metadata/
               test/gen-seeds read generated/; drift gate fails seed SQL outside generated/; HEARING_P{1,2,3}
               regenerated; tests added.
             - #1 cold storage: framework READY (archive zone/snapshot_archive/dual-write/external_location/
               purge_rule); storage-tiering doc section 8 = Phase-4 build (ADLS Cool/Cold + lh_archive shortcut +
               VACUUM); wired into greenfield guide Phase 4 + phase-04 checklist.
             - #3 BI end-to-end: bi/docs/end-to-end-sample-HEARING_P1.md (Gold -> Direct Lake model -> dashboard);
               data side READY, BI non-metadata-driven by design; live PBIP deploy capacity-gated.
             - #4 re-run pipelines: 2 failed + FIXED + re-run GREEN. dataflows-pr-validation failed on stale dev
               (gate checks out dev, was 8 behind main) -> FF dev+uat->main all repos. infra-pr-validation failed
               on terraform git-module auth -> System.AccessToken extraheader added to infra-pr-validation +
               infra-deploy + ops-environment-rebuild. Deploy/run/ops/finops pipelines = env/capacity-gated (not
               fired blindly).
             - #5 Fabric vs ADO: pilot ws IS Git-connected (ConnectedAndInitialized -> platform/dev/
               framework/fabric-items). Fabric shows items because that is where they run; containers
               (lakehouse/wh/sqlendpoint/env) are IaC/REST, not Git-as-code, by design (ADR-40 A1).
             - #6 greenfield: approach = ADR-47 + recreate-platform L0/L1/L2 + capacity toggle (config-driven).
               Corrected inventory (fabric_lakehouse/warehouse exist INLINE in fabric_workspace). ADR-49 infra
               follow-up IMPLEMENTED: dev/test/prod now ONE shared ws_data (lh_bronze/silver/gold/archive +
               wh_serving) + optional isolated_domains override; validate+fmt clean all envs (local tf 1.15.3).
Next step  : Phase-P closer UNCHANGED (only thing that closes P): R-19 budget ceiling (USER/CTO) -> trial->F64
             swap -> Wave-0 load test -> capacity_estimator on real CU telemetry -> capacity recommendation FINAL
             -> sign-off. #6 remaining greenfield modules (Phase 4 build): service_principals, fabric_environment,
             fabric_git, ado_* (project/repos/varGroups/serviceConnections/pipelines), private_endpoints,
             conditional_access, purview. Cold external tier + BI live deploy = capacity-gated. ADR-20/31
             Dataverse needs a real org.
Files created/modified this session:
             See session-log session 27. Headlines: platform - gen_seeds.py, new_dataflow.py, dataflows-delivery
             + 3 templates, infra-pr-validation/infra-deploy/ops-environment-rebuild (auth), infra/envs/{dev,test,
             prod} (ADR-49 ws_data) + variables, tests/test_gen_seeds. docs - storage-tiering section 8,
             greenfield-guide Phase 4, gen_phase_checklists + phase-04, ADR-49 follow-up, recreate-platform,
             end-to-end BI sample (bi repo), session-log. dataflows - HEARING_P{1,2,3} generated/.
Decisions made (new ADRs or locked):
  - No new ADRs. Locked: terraform git-module fetch needs the System.AccessToken extraheader; PR-validation gates
    check out dev (keep dev FF'd); ADR-49 infra = one shared data workspace, per-domain only as isolation
    exception; DE authors only manifest.yml (seeds = generated/ machine output, drift-gated).
Open items / blockers:
  - Phase-P closer (R-19 -> F64 -> sign-off). Greenfield module backlog (Phase 4). Cold external tier + BI live
    deploy capacity-gated. ADR-20/31 Dataverse needs an org. Trial expiry ~2026-08-08.
Next session start instruction:
  Read CLAUDE.md, gameplan.md, CLAUDE.local.md (this block) + session-log sessions 26-27. Everything pushed +
  SHA-verified (4 repos main=dev=uat); unit suite + all 4 PR-validations green. To advance Phase P: get the
  R-19 ceiling, upgrade trial->F64, run the Wave-0 load test, produce the FINAL capacity recommendation, sign off.
  Otherwise build the remaining #6 greenfield modules (Phase 4). Push with the az-token bearer lane (FF, SHA-verify).
---

# ----- superseded (session 26) -----
---
SESSION HANDOFF
Date       : 2026-06-20 (session 26 - closed the session-25 OPEN list: ADR-49 propagation
             (scaffold/manifest/naming + LIVE storage_target reseed), Stage-4 param collapse,
             2 ADO defs registered, ops-rebuild admin gate, gaps report)
Phase      : P - Pilot on Trial (OPEN; exit gates UNCHANGED). All free code/config/docs + two LIVE
             changes (ADO def registration + pilot control-DB reseed). No Phase-P cloud exit criterion
             advanced. 4 repos clean + pushed; full unit suite GREEN (exit 0).
Last step  : Final pushed SHAs (FF-checked, SHA-verified, no force): platform 70889aa, docs cb3e125,
             bi 64cd93b (unchanged), dataflows 15617d6 (unchanged). Done, all 7 OPEN items:
             (d) new_dataflow schema-per-layer (--domain optional/derived ADR-49 lineage tag; manifest
                 per-layer schema placeholders, _shared route), self-test 7/7; FIXED latent scaffold-step
                 project-code regex ([A-Z]{2,4}-\d{3} -> HEARING_P\d+); Stage-4 5 params -> one cumulative
                 test_mode (unit/ddl/mock/integration) in dataflows-delivery + the steps template.
             (e) naming-and-structure-standard: Domain row = "Gold/BI lineage tag only" + new section 2A
                 "Storage & lakehouse layout" (one lakehouse per layer + per-layer schema taxonomy).
             (f) root CLAUDE.local lakehouse keys LH_GUID_AUDIOLOGY_* -> LH_GUID_* (values unchanged).
             (a) registered ADO defs: platform-bring-up (33, \Platform) + finops-cost-report (34, \FinOps);
                 16 defs total (TF400898 was transient).
             (b) ops-environment-rebuild now requires admin (HealthEnt Seniors) approval via the
                 healthent-{env} ADO Environment before destroy+rebuild; finops piece = the def-34 registration.
             (c) LIVE pilot storage_target reseed: now exactly 5 _shared rows -> lh_bronze/silver/gold/archive
                 in healthent-pilot; deleted the 10 stale per-domain rows (transactional, BEFORE 10 / AFTER 5,
                 verified). NOTE: the _shared rows had never been deployed live (S25 renamed only the Fabric
                 items) so this was a FULL reseed, not a bare delete; confirmed the renamed lakehouses exist
                 in healthent-pilot so the friendly-name paths resolve.
             (g) docs/review/gaps-and-recommendations.md (honest Phase-P snapshot + tech debt T-1..T-6).
Next step  : Phase-P closer UNCHANGED (the only thing that closes P): R-19 budget ceiling (CTO + DE Manager)
             -> trial->F64 swap -> Wave-0 load test -> capacity_estimator on real CU telemetry -> capacity
             recommendation FINAL -> sign-off. Secondary (free): T-3 prove the scaffold E2E under the
             HEARING_P\d+ fix (run dataflows-delivery mode=scaffold once). F64/integration-gated: T-2 wire
             Tier-0 admission into pl_batch_runner/pl_dag_runner. External: ADR-20/31 Dataverse live verify
             needs a real org. Phase 4: T-1 seed _shared storage_target rows for dev/test/prod.
Files created/modified this session:
  - platform: framework/tools/scaffold/new_dataflow.py; devops/pipelines/dataflows-delivery.yml;
    devops/pipelines/templates/{dataflows-new-project-steps,dataflows-test-one-flow-steps}.yml;
    devops/pipelines/ops-environment-rebuild.yml  (commits a541f52, 70889aa)
  - docs: docs/architecture/naming-and-structure-standard.md; docs/review/gaps-and-recommendations.md (NEW);
    docs/decisions/session-log.md  (commits 3bef23e, cb3e125)
  - root (gitignored): CLAUDE.local.md (lakehouse keys + this block)
  - LIVE: ADO defs 33/34 created; pilot control DB meta.storage_target reseeded (5 _shared rows)
Decisions made (new ADRs or locked decisions):
  - No new ADRs (executes ADR-49 + the session-25 approval model). Locked: service connection stays a
    compile-time parameter; ops pipelines gate on admin via the healthent-{env} ADO Environment.
Open items / blockers:
  - Phase-P exit: R-19 ceiling (USER/CTO) -> F64 load test -> capacity recommendation sign-off (the only closer).
    ADR-20/31 Dataverse needs a real org. Tech debt T-1..T-6 in gaps-and-recommendations.md. Trial expiry ~2026-08-08.
Next session start instruction:
  Read CLAUDE.md, gameplan.md, and CLAUDE.local.md (this block) + session-log session 26. Everything is
  pushed + SHA-verified (4 repos clean); unit suite green. The session-25 OPEN list is closed. To advance
  Phase P you now need the R-19 ceiling -> trial->F64 -> Wave-0 load test -> capacity recommendation sign-off.
  Free next step if desired: T-3 (prove the scaffold E2E under the HEARING_P\d+ regex fix). Push with the
  az-token bearer lane (FF-check, SHA-verify, no force).
---

# ----- superseded (session 25) -----
---
SESSION HANDOFF
Date       : 2026-06-19 (session 25 - capacity toggle, Tier-0 admission, ADR-49 single-lakehouse-per-layer,
             pipeline approval model + systemic service-connection fix, security doc, metadata drift gate)
Phase      : P - Pilot on Trial (OPEN; exit gates UNCHANGED). All free code/docs/ADO-config; no Phase-P
             cloud exit criterion advanced. 4 repos clean + pushed; full unit suite GREEN (exit 0).
Last step  : Continuity checkpoint. Final pushed SHAs: platform bdb5efa, docs 2822c4a, bi 64cd93b,
             dataflows 15617d6. Headlines (all committed + pushed): (1) S23 follow-ups - regen 5 stale
             .Notebook copies; ADR-47 dry-run + capacity_mode trial/paid toggle BUILT + promoted to
             test/prod (tag modules-v1.1.0); Tier-0 admission (DDL 39 + wheel 0.4.12 + nb_admission +
             pl_admission_master). (2) Docs - dummys 31 (greenfield) + 32 (capacity lifecycle);
             storage-tiering-and-cold-storage.md; migration/source-org-strategy-qa.md; security-strategy.md
             EXPANDED (integrations/groups/KV/accesses/ADR-49 PHI). (3) ADR-49 single lakehouse per layer
             (lh_bronze/silver/gold/archive) + per-layer schema (source/subject/business); wheel
             resolve_storage_root decoupled (_shared fallback); LIVE pilot lakehouses renamed in Fabric
             (REST 200) + Git shells + seed; 2 tests; suite green. (4) PIPELINES - systemic fix: ALL 10
             pipelines moved off the runtime $(ARM_SERVICE_CONNECTION) macro (it fails ADO compile-time
             validation -> the "no stages visible" bug) to a compile-time service_connection param.
             Approval model: ADO Environment admin checks created on healthent-dev/test/prod (= ADO group
             HealthEnt Seniors); dataflow/BI free dev/test + admin prod; infra/platform/ops admin all envs;
             inline step-through removed; manual-gate-job.yml deleted; env values -> dev/test/prod only.
             (5) Metadata simplification - gen_seeds.py --check drift gate wired into dataflows-pr-validation
             (manifest.yml = the only DE-authored file; hand-edited seeds fail CI). (6) FinOps cost-report
             pipeline + cost_report.py + meter-map + tests.
Next step  : Finish the OPEN items (user said "fix everything"): (a) RETRY registering platform-bring-up +
             finops-cost-report as ADO pipeline defs - failed with TF400898 transient (POST _apis/pipelines;
             platform repo id 3450aa5c-de3a-40ad-8ef9-097413878353, folders \Platform \FinOps); (b)
             ops-environment-rebuild admin Environment gate + ops/finops pipeline merges; (c) LIVE
             storage_target reseed (delete the per-domain pilot rows so _shared resolves the renamed
             lakehouses) via the firewall+AAD harness; (d) new_dataflow.py schema-per-layer (drop --domain
             structural) + drop/relabel domain run param in dataflows-delivery + Stage 4 cleanup (5 params
             -> test_mode); (e) naming-and-structure-standard update for lh_bronze/silver/gold; (f) update
             this file's lakehouse GUID names lh_audiology_* -> lh_*; (g) gaps/recommendations report.
             Then the Phase-P closer (R-19 ceiling -> F64 load test -> capacity recommendation sign-off).
Files created/modified this session:
             See docs/decisions/session-log.md (session 25) for the full list + the per-area commit SHAs.
             Headlines: platform - wheel common.py (resolve_storage_root) + orchestrate.py + 0.4.12;
             control-plane DDL 39 + 19_meta_storage_target.sql; framework/tools/scaffold/gen_seeds.py
             (--check); fabric-items lakehouse shells renamed; devops/pipelines (10 SC-fixed + approval
             model + finops-cost-report + cost_report.py + meter-map + 2 templates, manual-gate-job deleted);
             tests/unit (storage_routing +2, orchestrate +4, admission +2, cost_report +5). docs - ADR-49 +
             adr-index; dummys 31/32; architecture/storage-tiering; migration/source-org-strategy-qa;
             security/security-strategy; runbooks/recreate-platform; finops/cost-model; decisions/session-log.
             LIVE: 4 Fabric lakehouses renamed; ADO env approval checks (dev/test/prod); modules-v1.1.0 tag.
Decisions made (new ADRs or locked):
  - ADR-49 single lakehouse per layer + per-layer schema taxonomy (supersedes per-domain ADR-36/40).
  - Approval model = ADO Environment checks (HealthEnt Seniors = admin); dataflow/BI free dev/test + admin
    prod; infra/platform/ops admin all envs. Only dev/test/prod environments.
  - Service connection MUST be a compile-time parameter (runtime $(var) fails ADO validation - systemic).
  - manifest.yml is the only DE-authored metadata file (gen_seeds --check enforces it).
  - Capacity toggle promoted to test/prod via modules-v1.1.0; ADR-47 dry-run done.
Open items / blockers:
  - OPEN (next session): pipeline registration retry (TF400898); ops-rebuild gate + ops/finops merges;
    live storage_target reseed; new_dataflow schema-per-layer + dataflows-delivery domain param + Stage 4;
    naming-standard lh_bronze/silver/gold; CLAUDE.local lakehouse names; gaps/recommendations report.
  - Phase-P closer UNCHANGED: R-19 ceiling (USER/CTO) -> trial->F64 -> Wave-0 load test -> capacity
    recommendation FINAL -> sign-off; apply-verify capacity toggle + DDL 39 + admission stack live (F64-gated).
  - Trial expiry ~2026-08-08.
Next session start instruction:
  Read CLAUDE.md, gameplan.md, and CLAUDE.local.md (this block) + session-log.md session 25. All pushed +
  green. Resume the OPEN items above in order (start with the pipeline-registration retry + the live
  storage_target reseed since the lakehouses were renamed), then new_dataflow/domain/Stage-4 cleanup, then
  the gaps report. Push with the az-token bearer lane (FF-check, SHA-verify, no force).
---

# ----- superseded (session 23) -----
---
SESSION HANDOFF
Date       : 2026-06-18 (session 23 - R7 CI/CD COMPLETE incl. LIVE ADO re-registration + Phase-9 framework hardening (drift/volume-drop/recon-enforcement/use_staging/job-aware-order/admission/cross-DAG-deps) + deep BI-developer & environment-onboarding runbooks + extensive architecture docs)
Phase      : P - Pilot on Trial (OPEN; exit gates UNCHANGED). S23 advanced Phase-6 (R7) + Phase-9/10
             framework readiness as free, unit-tested code; NO Phase-P cloud exit criterion advanced.
Last step  : Full session-close done. Final pushed SHAs (all SHA-verified, 4 repos clean): platform
             d5220ac, docs 4e387ed, bi 64cd93b, dataflows 15617d6. Highlights, all unit-tested + pushed:
             (1) R7 CI/CD rationalisation COMPLETE incl. the previously-blocked LIVE ADO re-registration -
             the az-token bearer lane authenticates to the ADO Build Definitions REST API, so I deleted
             12 obsolete defs (HTTP 204) and created def 31 dataflows-delivery (\Dataflows) + 32
             platform-release (\Platform); final = 14 pipelines; deadlock resolved. (2) Phase-9 wheel
             hardening 0.4.6->0.4.11: drift gate (drift.py, both ingestion notebooks, file QUARANTINE +
             mergeSchema + PHI classification gate); volume-drop DQ (dq.py, DDL 38 LIVE, DE-declarable via
             gen_seeds); recon_within extracted; **gen_seeds now seeds row_recon/sum_recon so the per-flow
             COUNT CHECK IS ENFORCED** (was computed then silently dropped - a real silent-data-loss gap;
             examples regenerated 15617d6); use_staging atomic publish; job-aware order (orchestrate.
             build_run_dag, wired nb_pipeline_controller); Tier-0 admission (admit/in_run_window);
             cross-DAG depends_on (deps_met). Full unit suite GREEN (exit 0). (3) DDL 35/36/37/38 deployed
             LIVE to sqldb-healthent-control-pilot (additive, BEFORE/AFTER verified, idempotent). (4) Deep
             runbooks: bi-developer-runbook.md + environment-onboarding-runbook.md; BI scaffolds (bi repo:
             MODEL-REGISTER, AudiologyContacts model + 2 report homes). (5) Architecture docs: migration
             read-strategy (HLA + backfill + cutover-at-scale + per-flow count-check HARD gate), maturity
             ladder, semantic-model refresh/metadata-driven/bi-repo-separation, shared-wheel concurrency,
             connection best practice, framework Complete-Reference sections, Phase 0/1 discovery gaps.
Next step  : The ONLY thing that CLOSES Phase P (unchanged): R-19 budget ceiling (USER/CTO) -> upgrade
             the trial to F64 -> Wave-0 load test -> capacity_estimator on real CU telemetry ->
             capacity-recommendation FINAL -> DE Manager + CTO sign-off. Then: LIVE wiring of the Tier-0
             master (consume orchestrate.admit + df_batch_param) + build_run_dag into pl_batch_runner/
             pl_dag_runner (F64-validated); deploy the gen_seeds recon-rule fix to live control DBs; the
             ADR-47 greenfield dry-run; regenerate the stale .Notebook deploy copies. ADR-20/31 Dataverse
             live verify needs a real Dataverse org.
Files created/modified this session:
             See the FILE LIST in the session-close message + git logs 2026-06-18. Headlines:
             platform - wheel {drift,dq,orchestrate}.py NEW + loadguard/common/writers/__init__ (0.4.6->
             0.4.11) + tests/unit/test_{drift,dq,orchestrate}.py NEW; control-plane 38_*.sql NEW; fabric-
             items/notebooks/ingestion/{incremental,file} + orchestration/nb_pipeline_controller; gen_seeds.py;
             devops/pipelines (R7: 2 staged + 10 step-templates, 13 deleted). docs - runbooks/{bi-developer,
             environment-onboarding}-runbook.md NEW; bi/bi-operating-model (§6/§7/§8); migration/{read-strategy
             (NEW),wave-runbook-template,migration-dictionary-spec}; framework/* Complete-Reference; cicd/
             {ado-setup-record,pipeline-catalogue,master-orchestrators-design}; architecture/{ingestion-source-
             families §3.5, environment-reuse-readiness §2.1}; decisions/{adr-index ADR-44 A3,tradeoffs-index,
             session-log}; phases/phase-{00,01,P}/*; timeline/gantt; gameplan. bi - README + MODEL-REGISTER +
             2 model/2 report scaffolds. dataflows - HEARING_P1/P2/P3 seeds regenerated.
Decisions made (new ADRs or locked decisions):
  - ADR-44 A3 (Accepted): R7 fold-fully staged delivery pipelines (executed incl. live ADO).
  - No other new ADR numbers - S23 features IMPLEMENT existing ADRs (ADR-48 drift/order/staging/recon,
    ADR-42 admission, ADR-41 drift_policy). Locked: per-flow count check is a HARD Synapse-decommission
    gate (read-strategy §3.3) + auto-seeded by gen_seeds; semantic model = metadata-VALIDATED not
    generated; bi repo stays separate; semantic refresh = readiness-triggered (loaded AND reconciled).
Open items / blockers:
  - Phase-P exit: R-19 ceiling (USER/CTO) -> F64 load test -> capacity recommendation sign-off (the only
    closer). ADR-20/31 Dataverse live verify needs an org. Live wiring of admission/order into the
    runner pipelines + the gen_seeds recon-fix deploy to live control DBs are F64/integration-gated.
    .Notebook deploy copies stale (regenerate at deploy). Trial expiry ~2026-08-08.
Next session start instruction:
  Read CLAUDE.md, gameplan.md, and CLAUDE.local.md. Everything is pushed + SHA-verified (4 repos clean);
  full unit suite green. R7 + Phase-9 framework hardening are DONE as unit-tested code; the orchestration
  core (job-aware order + admission + cross-DAG deps) is pure + tested. To advance PHASE P you now need
  funding: get the R-19 ceiling, upgrade the trial to F64, run the Wave-0 load test, produce the FINAL
  capacity recommendation, and get sign-off. Then wire admission/order into pl_batch_runner/pl_dag_runner
  and validate live. Push with the az-token bearer lane (FF-check, SHA-verify, no force).
---

# ----- superseded (session 22) -----
---
SESSION HANDOFF
Date       : 2026-06-17 (session 22 - HEARING_P{n} consolidation EXECUTED + ADR-48 framework rework: layer batches, readiness gate, snapshot archive, multi-target, HLA docs, dummys 30)
Phase      : P - Pilot on Trial (OPEN; exit gates UNCHANGED). This session was Phase-9/10 framework
             design pulled forward as free, unit-tested code; no Phase-P cloud exit criterion advanced.
             Everything is pushed to origin/main (3 repos) and SHA-verified.
Last step  : Full session close done. Final pushed SHAs: platform f90e34f, dataflows 7b6b907,
             docs 1e5a961. Built + unit-tested (suite 91 pass / 5 skip; typography PASS; wheel 0.3.2->0.4.5):
             (1) HEARING_P{n} global project-code scheme (new_dataflow) + the 3 examples regenerated via
             gen_seeds v2 (multi-object manifest -> 3 layer batches bronze/silver/gold -> jobs -> procs ->
             proc_params + opt-in prune); HEARING_P1 = 2-table subject area (appointment+clinic, silver
             fan-in/broadcast), P2 = CRM contact snapshot-archive, P3 = file ingestion. (2) ADR-48 (DAG=
             subject area; layer batches; jobs parallel/sequential; cross-layer correctness + recovery).
             (3) Source-readiness+freshness gate (readiness.py + DDL 35). (4) Managed-table partition_by/
             cluster_by (DDL 36) on the writers. (5) snapshot_archive load type + empty-source guard + EOT/
             manifest gate + file preflight (loadguard.py; nb_ingestion_file). (6) build(spark,sources,params)
             optional 3-arg. (7) Multi-target build ({target:df} split-flow) + ingestion current+archive
             DUAL WRITE (is_archive); use_staging (DDL 37). (8) Docs: ADR-48, 4 framework HLA Mermaid diagrams
             (+ NEW orchestration-framework), dummys 30 (transformation deep how-to), DE templates rewritten
             (PySpark+SparkSQL+multi-target+params + new silver_transform_sql_TEMPLATE.sql). LIVE: deleted
             df_audiology_referrals (AUD-002) from sqldb-healthent-control-pilot (transactional, verified;
             DYN-002 was never live). Confirmed with the user: transform has NO logic limit (full PySpark +
             Spark SQL, mixed); libraries via Fabric Environment only (no inline pip).
Next step  : (1) R7 CI/CD rationalisation (~25 -> ~12 pipelines; single-run staged dataflows-delivery +
             platform-release via template-include; delete deadlocking masters) - the headline remaining build.
             (2) Deploy DDL 35/36/37 to the live control DB (additive). (3) Phase-9 runner wiring: job-aware
             (job_order, proc_order) order + master queue-and-wait; drift allow_additive/quarantine + type-change
             + new-column-classification gate; use_staging staging-then-promote for tables; volume-drop DQ.
             (4) Phase-P REAL exit path (the only thing that closes P): R-19 ceiling (USER/CTO) -> upgrade trial
             to F64 -> Wave-0 load test -> capacity_estimator on real telemetry -> capacity-recommendation FINAL
             -> sign-off. Optional: port the user's UDP Mandos notebook onto build()/multi-target as a worked example.
Files created/modified this session:
  - See the FILE LIST in the session-close message + session-log 2026-06-17 (session 22). Headlines:
    platform framework/tools/scaffold/{new_dataflow,gen_seeds,gen_views}.py; wheel
    {transform,writers,loadguard(NEW),readiness(NEW),common,__init__}.py (0.4.5); control-plane
    35/36/37_*.sql (NEW); fabric-items/notebooks/ingestion/{nb_ingestion_incremental,nb_ingestion_file}.py;
    tests/unit/{test_gen_seeds(v2),test_readiness,test_layout_and_archive,test_build_signature,test_multi_target}.py.
    dataflows metadata/HEARING_P1..P3/** (regenerated) + silver notebooks + gold views + templates/notebooks/**.
    docs decisions/ADR-48-*.md + adr-index; architecture/{framework-rework-spec,naming-and-structure-standard};
    framework/{ingestion,transformation,metadata,orchestration(NEW)}-framework.md (HLA); dummys/30-*.md;
    example-project/crm365-connectivity-example.md; phases/phase-P/{implementation,finops,risk,runbook}.md;
    decisions/session-log.md; timeline/gantt.md; gameplan.md (both root + docs copy).
Decisions made (new ADRs or locked decisions):
  - ADR-48 (Accepted): DAG/batch/layer orchestration grain + multi-object dataflows + cross-layer
    correctness (idempotent re-runs, increment-vs-full-dimension join, succeeded-0-rows vs failed,
    source-readiness/freshness gate, empty-source guard) + recovery + managed-table layout + snapshot
    archive + multi-target. Memory: adr-48-orchestration-grain, example-projects-rationalisation (executed).
  - HEARING_P{n} global project codes (retire {DOM}-{NNN}). Batch grain = 3 layer batches (user-confirmed).
Open items / blockers:
  - R7 CI/CD NOT started. DDL 35/36/37 NOT deployed live. Phase-9 runner wiring designed not wired.
    Notebook wiring (snapshot_archive/EOT/dual-write/readiness/empty-guard) unit-tested but live-validated
    only on F64. Live F64 run + capacity sign-off R-19 gated (the only Phase-P exit blocker).
  - df_dynamics_customer_feedback (DYN-001) live-only, out of scope, left intact. Stale old-code refs in
    some dummys/* + cicd/doc/* not fully swept. ADO password auth still 401 - use the az-token bearer lane.
Next session start instruction:
  Read the operating rules (CLAUDE.md), gameplan.md, and this file. Phase P is OPEN; S22 was framework
  hardening (ADR-48) + the HEARING_P{n} examples, all pushed + unit-tested (91 pass). Start R7 CI/CD
  rationalisation, then deploy DDL 35/36/37 live and the Phase-9 runner wiring; the only thing that CLOSES
  Phase P is the R-19 ceiling -> F64 load test -> capacity recommendation sign-off (USER/CTO).
  Push with the az-token bearer lane (FF-check, SHA-verify, no force).
---

# ----- superseded (session 21) -----
---
SESSION HANDOFF
Date       : 2026-06-17 (session 21 - pushed S20; nb_transform spark_sql audit-wiring; example-projects plan locked)
Phase      : P - Pilot on Trial (OPEN). Short session; user wrapped up mid-way through the example
             rationalisation (planned, not yet executed). All work this session is pushed.
Last step  : (1) PUSHED all session-20 commits to origin/main (docs 69c8e87, platform ff5fc49,
             dataflows 2259a0e) via the az-token bearer lane (ADO password auth = 401); FF-checked,
             SHA-verified, no force; dev+uat FF-converged to main on all repos. (2) R8 nb_transform
             spark_sql audit-wiring DONE: the transform_spark_sql path now wraps the DE Spark SQL as a
             build() closure and runs through the wheel run_transform_core (same engine as pyspark -
             source resolution, Gold masking, empty-source guardrail, audit-stamping writer, SCD2
             invariant); removed the template-local write/mask helpers; BOTH copies (.Notebook + flat).
             (3) Fixed latent wheel bug: transform.resolve_source_paths now accepts dict OR json string
             (load_params hands it a dict -> json.loads(dict) would have raised; F64-gated so never hit);
             regression test tests/unit/test_transform_source_map.py (3 cases PASS). (4) Synced flat
             nb_scd2_processor R2 audit columns (drift vs .Notebook copy). Platform commit ff0ebdb
             pushed (main/dev/uat); gen_seeds + gen_views self-tests + full unit suite GREEN.
Next step  : EXECUTE the USER-LOCKED example-projects consolidation (memory:
             example-projects-rationalisation; session-log 2026-06-17 session 21):
             (1) Keep THREE, rename folders to HEARING_P{n}: HEARING_P1 = df_audiology_appointments
                 (table, was AUD-001); HEARING_P2 = df_dynamics_contact (NEW CRM/Dataverse table, full
                 medallion - build on `contact` for PII+SCD2+DDM two-view demo); HEARING_P3 =
                 df_audiology_devicetelemetry (file, was AUD-FILE-DEMO).
             (2) ELIMINATE AUD-002 (df_audiology_referrals) + DYN-002 (df_dynamics_account) from git
                 AND from the live control DB sqldb-healthent-control-pilot (delete meta/log rows).
             (3) Regenerate every kept project via gen_seeds.py from a rich manifest.yml (standard
                 generated seed file names; gen_seeds already supports mixed ingestion+transform);
                 gen_views for P1/P2; author/port the silver build() notebooks (P1 from existing
                 AUD-001 build; P2 new contact build).
             (4) Change project-code scheme to HEARING_P{n} (global sequential) in
                 new_dataflow.py issue_project_code, the project-register, the naming-standard doc,
                 and rework-spec §2; dag_uid stays df_{domain}_{entity}.
             (5) THEN R7 CI/CD rationalisation (~25 -> ~12; design + skeleton; ADO run-untestable, 401).
             (6) Live F64 run still R-19 gated.
Files created/modified this session:
  - platform: framework/fabric-items/02 Transformation/nb_transform.Notebook/notebook-content.py;
    framework/fabric-items/notebooks/transformation/nb_transform.py; framework/wheel/src/
    healthent_framework/transform.py; framework/fabric-items/notebooks/gold/nb_scd2_processor.py;
    tests/unit/test_transform_source_map.py  (commit ff0ebdb, pushed main/dev/uat)
  - docs: docs/decisions/session-log.md (session 21); gameplan.md §8 (S20/S21)
  - memory: example-projects-rationalisation.md (+ MEMORY.md index)
Decisions made (locked):
  - nb_transform spark_sql path MUST run through the wheel engine (no template-local write/mask) -
    R1/R2 parity; resolve_source_paths is dict-or-str tolerant.
  - USER-LOCKED: examples = THREE only (HEARING_P1/P2/P3); folder naming HEARING_P{n}; regenerate all
    via gen_seeds; eliminate AUD-002 + DYN-002 from git + live control DB.
Open items / blockers:
  - Example consolidation NOT yet executed (next session, first thing). Live-DB deletes need the
    pilot control-DB connection (firewall + AAD token; framework/tools/harness/ensure_sql_firewall.py
    + run_sql.py). R7 CI/CD pending. Live F64 run R-19 gated. ADO password auth still 401 - use the
    az-token bearer lane: TOK=$(az account get-access-token --resource 499b84ac-1321-427f-aa17-267ca6975798
    --query accessToken -o tsv); git -c http.extraHeader="AUTHORIZATION: bearer $TOK" push ...
Next session start instruction:
  Read the operating rules, gameplan.md, and this file. Then EXECUTE the HEARING_P{n} example
  consolidation per memory example-projects-rationalisation + the session-log 2026-06-17 (session 21)
  entry: rename/regenerate the 3 kept projects via gen_seeds, author HEARING_P2 (df_dynamics_contact)
  silver build() + gen_views, delete AUD-002 + DYN-002 from git AND the live control DB, update the
  HEARING_P{n} naming in new_dataflow.py + register + naming-standard + spec. Then R7 CI/CD.
  (Push with the az-token bearer lane; FF-check, SHA-verify, no force.)
---

# ----- superseded (session 20) -----
---
SESSION HANDOFF
Date       : 2026-06-17 (session 20 - UDP-parity framework rework: R1-R6 + compute binding +
             schema/storage/promotion conventions + framework deep-dive docs)
Phase      : P - Pilot on Trial (OPEN). Large rework benchmarked against the 5 UDP PDFs at the
             container root. Single source of truth = docs/architecture/framework-rework-spec.md.
             All work LOCAL only (ADO push still 401 this session).
Last step  : Delivered + unit-tested + committed locally: R1 invert-control transform (wheel
             transform.py run_transform; DE writes build() only) + R2 audit columns (every writer +
             scd2 dims); R3 two ingestion kinds (DDL 33 file columns + source_kind + nb_ingestion_file
             + gen_seeds file support + DDL 34 'copy' proc_type = pipeline+notebook ingestion, UDP
             parity); R4 two views (gen_views.py: consumption masked + tech unmasked, DDM + GRANT
             UNMASK, access model); R5 naming (batch=dag_uid, J_/P_); R6 DE templates + AUD-001
             converted to build(); compute binding (DDL 32 environment_target + resolver). Locked in
             spec: schema convention (Fabric 4-level: layer->lakehouse, purpose->schema, archive->own
             lakehouse, masked->wh, domain never a schema), storage (OneLake store; ADLS landing via
             shortcut only), env promotion (env = boundary, never a name prefix). NEW docs/framework/
             deep-dives (metadata/ingestion/transformation, session-maintained) + CRM-365 connectivity
             worked example + framework-rework-spec. Examples: DYN-002 (CRM table) + AUD-FILE-DEMO
             (file + copy proc) both generate clean. Metadata coherence verified (24 tables, all
             seed columns + enum values valid). Full unit suite GREEN (Spark tests skip locally).
             5 memories written. Commits: platform cc0f172 4b780b9 ff5fc49 ddbbf3d 9f556c8 f319e78
             c51310e e4c84e3 5ec7558 7b0cfd1 23b5718; dataflows 747718b 44d2122 e1e8ba8 2259a0e;
             docs 42b9cc9 c92696e daca613 9abc625 25f6131 d2d64dc f281619 69c8e87.
Next step  : (1) PUSH all session-20 commits to origin/main once auth available (FF-check, SHA-verify,
             no force - 3 repos). (2) R7 CI/CD rationalisation (~25 -> ~12: single-run staged
             dataflows-delivery + platform-release via template-include, delete the deadlocking
             masters, fold in folder=dag_uid rename) - design + skeleton only here (ADO untestable,
             401). (3) R8 remainder: author DYN-001 CRM silver/gold/recon to build(); finish
             nb_transform spark_sql path audit-wiring. (4) Live F64 run still R-19 gated.
Files created/modified this session: see session-log 2026-06-17 (session 20) + the commit list above.
  Headlines: wheel transform.py/writers.py/common.py/__init__ (v0.4.0); nb_ingestion_file;
  nb_scd2_processor + nb_transform (both copies); gen_seeds + gen_views; DDL 32/33/34; DE templates +
  AUD-001; docs/framework/* + framework-rework-spec.md + crm365 example; tests test_ingestion_file +
  test_environment_target.
Decisions made (locked):
  - Invert-control transform (DE build() only; wheel owns I/O); full audit columns; two ingestion
    kinds (file net-new); copy proc_type (pipeline+notebook); two views consumption/tech + access
    model (DE/Admin/Analyst/SP unmasked, Business masked); P_/J_/batch=dag_uid naming; schema=purpose
    not domain (Fabric 4-level); OneLake-only medallion + ADLS-landing-via-shortcut; env=boundary not
    name prefix; framework docs session-maintained.
Open items / blockers:
  - ADO push 401 (all session-20 commits LOCAL only). R7 CI/CD + R8 CRM remainder pending. nb_transform
    spark_sql path still does its own write (audit-wiring follow-up). Live F64 run R-19 gated.
  - DDL 32/33/34 not yet deployed to the live control DB (additive; deploy step, needs connectivity).
Next session start instruction:
  Read the operating rules, gameplan.md, and this file. FIRST push the session-20 commits (3 repos) to
  origin/main + SHA-verify (FF-check, no force). Then R7 CI/CD rationalisation (dataflows-delivery +
  platform-release single-run staged, delete masters) and R8 CRM silver/gold to build(). Spec =
  docs/architecture/framework-rework-spec.md; framework docs = docs/framework/ (keep sharp each session).

# ----- superseded (session 18 FINAL) -----
---
SESSION HANDOFF
Date       : 2026-06-16 (session 18 FINAL - example project CRM->Gold via the framework (live) +
             framework append fix + de-attribution scrub + dummys 25-29 + phase docs + bring-up)
Phase      : P - Pilot on Trial (OPEN). This session: large docs build + a LIVE framework example.
Last step  : Built docs/example-project/ (CRM Excel -> Gold THROUGH THE FRAMEWORK): mock CRM SQL source
             src.* loaded on the control server; meta.* seeded LIVE + verified (df_dynamics_customer_
             feedback / DYN-001, 3 objects, seed_meta_dynamics.py); FIXED the framework append gap
             (ingestion notebook now does load_type=append, source .py committed); triggered
             pl_batch_runner -> batch_run 20 FAILED in launch phase on FTL4 (4 CU throttle, P-R11) -
             no bronze; control plane left CLEAN (locks free, config intact). Also this session:
             de-attribution scrub of all visible docs (CLAUDE.md->"the operating rules" etc.; code +
             gameplan + gitignored files untouched); dummys 25 (migration), 26 (onboard account),
             27 (promotion), 28 (trial), 29 (manual metadata - comprehensive); business area;
             environment-reuse-readiness; ADR-28/32 drafts; phase docs P/1/4/5/6 + placeholders 0-3/
             7-18 under docs/phases/; terraform validate clean (fixed mojibake) + checkov + CI static
             analysis; bring-up driver (deploy.ps1 + platform-bring-up.yml) + config contract;
             gen_pipeline_docs + per-pipeline cicd/doc; discovery tooling (inventory_synapse +
             dictionary_to_manifest, self-tested).
Next step  : Resume per docs/example-project/NEXT-STEPS-AND-BACKLOG.md section D: A1 deploy the append
             fix (.Notebook sync + republish), A3-A5 author crm silver/gold/recon (FREE), A2/A6 run
             (clean only on F64). Or pick a section-B framework capability (all free code/authoring).
Files created/modified this session:
  - docs: dummys/25-29, business/*, architecture/environment-reuse-readiness, decisions/ADR-28/ADR-32,
    phases/** (P/1/4/5/6 + placeholders), cicd/doc/** (generated), example-project/** (README,
    01-source-dictionary, 03-manifest, seed_meta_dynamics.py, BUILD-LOG, NEXT-STEPS-AND-BACKLOG),
    session-log, gameplan, 00-START-HERE, + de-attribution sweep across ~92 md files.
  - platform: infra/scripts/{deploy.ps1, discovery/inventory_synapse.py}, framework/tools/scaffold/
    dictionary_to_manifest.py, framework/tools/quality/gen_pipeline_docs.py, devops/pipelines/
    {platform-bring-up,infra-pr-validation}.yml, infra/.tflint.hcl, config/{README,target.template},
    infra/envs/{test,prod}/variables.tf (mojibake fix), framework/fabric-items/notebooks/ingestion/
    nb_ingestion_incremental.py (append fix). De-attribution in tracked *.md.
  - LIVE (pilot): src.* mock source + meta.* dynamics config seeded in sqldb-healthent-control-pilot.
Decisions made (locked/recorded):
  - Microsoft migration tools = accelerators not strategy; promotion = build-once/values-only;
    framework writers are OneLake-only by design; ingest a file = SQL/Dataverse family (no OneLake-CSV
    template); append fixed in framework; manual metadata seeding = documented fallback (dummys 29).
  - De-attribution: visible docs reference "the operating rules"/"the local session-state file";
    gitignored CLAUDE.md/.local + gameplan + code untouched; git history NOT rewritten; no AI commit trailer.
Open items / blockers:
  - F64 (R-19) for any clean multi-object Bronze->Gold run - FTL4 (4 CU) cannot sustain Spark sessions.
  - Deploy append fix (.Notebook sync + republish); author crm silver/gold/recon (free).
  - Stuck job instance e5e3d69a finalising on Fabric (batch_run 20 already failed; cosmetic).
  - Phase P exit gates unchanged: R-19 ceiling; ADR-20/31 Dataverse org.
Next session start instruction:
  Read the operating rules (CLAUDE.md), gameplan.md, and this file. Then resume the CRM example per
  docs/example-project/NEXT-STEPS-AND-BACKLOG.md section D (deploy append fix -> author silver/gold ->
  recon; run only on F64), or advance a section-B framework capability (free). All pushed; both repos
  on main, FF + SHA-verified.

# ----- superseded (session 18 docs-only handoff) -----
SESSION HANDOFF
Date       : 2026-06-16 (session 18 - docs only: dummys doc 25 one-stop Synapse->Fabric migration playbook)
Phase      : P - Pilot on Trial (REMAINS OPEN, unchanged). Documentation-only session: no telemetry,
             no provisioning, no capacity sign-off, no spikes. Exit gates untouched.
Last step  : Authored docs/dummys/25-migration-playbook-for-dummies.md - entry-point, zero-background
             migration playbook (superset of doc 16): sections 0-18 in reading order with a TOC table;
             core concepts; the map (Mermaid); every Synapse->Fabric asset strategy + 5 rationalisation
             decisions + source families (ADR-41); the Microsoft migration tools IN DEPTH (use-as-
             accelerators verdict per tool, how-to by layer, traps, decision flowchart); full order of
             operations; discovery (ADR-45 dictionaries); target prep on the free trial (Phase P, golden
             rules, the 2 spikes, sizing contingency); when/how-much to buy capacity (buy timeline, why
             F64, whole-bill, Reserved vs PAYG); the exact trial->paid swap via Azure; accesses by job/
             phase; per-workload lifecycle + recon gate + per-object register; waves + rollback; trade-
             offs; risks/gaps; timeline + R-18 caveat; curated best YouTube videos (named, not live);
             recommendations. Registered as #25 in 00-START-HERE. Session-log entry 18 added. Typography
             clean (passes house-style gate).
Next step  : Push the two local docs commits (8ec5371 doc+index, c52d066 session-log) to origin/main and
             SHA-verify (FF-check first; do NOT force - rebase if non-fast-forward). Then resume the real
             Phase P exit path: R-19 ceiling -> upgrade trial to F64 -> load test -> estimator ->
             capacity-recommendation FINAL -> sign-off; OR a Dataverse org for ADR-20/31 live verify.
Files created/modified this session:
  - docs: docs/dummys/25-migration-playbook-for-dummies.md (NEW); docs/dummys/00-START-HERE.md
    (registered #25); docs/decisions/session-log.md (session 18). Commits 8ec5371 + c52d066 (LOCAL only).
  - root: CLAUDE.local.md (this block).
Decisions made (new ADRs or locked decisions):
  - No new ADRs. Recorded position: the Microsoft migration tools (Warehouse Migration Assistant, Spark
    Migration Assistant, Synapse-pipeline-to-Data-Factory, Synapse Pathway, pipeline mounting, OneLake
    shortcuts, Copy job, Dataverse Link to Fabric, fab CLI/REST) are ACCELERATORS inside the metadata-
    driven framework, never the migration strategy itself (consistent with ADR-11/39/41).
Open items / blockers:
  - SYNC: push BLOCKED this session - Azure DevOps 401 (no credentials). 8ec5371 + c52d066 are local-only
    on main; push + remote-SHA verify pending user credentials (owner: user).
  - Phase P exit gates unchanged: R-19 budget ceiling unset (CTO + DE Manager); ADR-20/31 Dataverse live
    verify needs a real Dataverse org (none in tenant); trial expiry ~2026-08-08.
Next session start instruction:
  Read CLAUDE.md, gameplan.md, and CLAUDE.local.md. FIRST push the two local docs commits (8ec5371,
  c52d066) to origin/main and SHA-verify (do not force - rebase if non-fast-forward). Then continue the
  real Phase P exit path (R-19 ceiling -> F64 load test -> capacity recommendation) or the ADR-20/31
  Dataverse live verify if an org becomes available.
---

# ----- superseded (session 17 close) -----
SESSION HANDOFF
Date       : 2026-06-15 (session 17 FINAL - PR close + branch reconcile + typography rule/gate + ADR-19 DDM
             CLOSED + ADR-20/31 design + P-R24 generator proven vs DB + multi-account onboarding pack + Phase-P doc close)
Phase      : P - Pilot on Trial (REMAINS 🟢 OPEN). Every UN-GATED, free-trial-completable item is now DONE.
             The only remaining exit gates need money (F64) or an external system (a Dataverse org).
Last step  : Full session-close run. (A) PR 117 + 118 CLOSED (117 = bad-meter rate 0.2946 vs verified 0.275
             already on main; 118 = incomplete FIN-001 stub) + branches deleted. (B) Branch reconcile: main
             was 20 ahead of dev/uat (S16 pushed to main); FF dev+uat to main lossless - all 4 repos
             main==dev==uat. (C) House-style typography rule (naming-and-structure-standard §6) + sweep
             (255 files/3743 subs) + check_typography.py gate wired into platform/dataflows/bi PR validation,
             CI-proven on build 487 (PASS). (D) ADR-19 DDM CLOSED live on wh_audiology: standard T-SQL DDM,
             Viewer masked / admin exempt, DB+schema+COLUMN GRANT UNMASK verified, NO CREATE USER FROM
             EXTERNAL PROVIDER. (E) ADR-20/31 Dataverse DESIGN (Link default/Copy fallback/metadata-selected;
             7-item live-verify checklist; no org to test against). (F) P-R24 CLOSED: gen_seeds proven vs live
             sqldb-healthent-control-pilot (all 22 batches deploy in a rolled-back txn; 2 GO-batch @obj/@batch
             scoping bugs fixed + regression guard). (G) Multi-account portability: platform/config/ surface +
             docs/runbooks/onboard-new-account.md (access matrix, who-pays-capacity, Fabric-Admin-vs-Capacity-
             Admin, access-request email, tenant toggles, RACI). (H) Phase-P 4 docs + gameplan §8 + Gantt
             updated (honest/evidenced); session-log has 5 S17 entries.
Next step  : Phase P can only be CLOSED with EITHER (a) funding: R-19 ceiling (USER/CTO) -> upgrade trial to
             F64 -> Wave-0 load test -> capacity_estimator on real telemetry -> capacity-recommendation FINAL
             -> DE Manager + CTO sign-off; OR (b) a Dataverse org -> run the ADR-31 7-item checklist. Ask the
             user which. No further un-gated free-trial work remains.
Files created/modified this session:
  - docs: docs/architecture/naming-and-structure-standard.md (section 6), docs/decisions/session-log.md
    (S17); plus the typography sweep across 92 docs files. Commits b19e210, 33746ac (pushed main + FF dev/uat).
  - platform: framework/tools/quality/check_typography.py (NEW), devops/pipelines/platform-pr-validation.yml
    (typography_gate job); plus the sweep across 126 files. Commits 22a4c9c, 53b1a63 (pushed main + FF dev/uat).
  - dataflows: sweep across 29 files. Commit 86555ea (pushed main + FF uat).
  - bi: sweep across 2 files. Commit 7af756d (pushed main + FF, all aligned).
  - ADO: PR 117 + 118 abandoned with audit comments; branches auto/rate-refresh-20260614-428 and
    feature/df_finance_brnz365-scaffold deleted.
  - memory: feedback-no-em-dashes-no-ambiguity.md (+ MEMORY.md index line).
  - LATER SAME DAY: typography gate ROLLED OUT to dataflows + bi PR validation (infra via platform),
    CI-proven on dataflows build 487 (PASS). docs commits 7a054b2, 5154464; platform 1182eda.
  - LATER SAME DAY: ADR-19 Fabric DDM spike CLOSED (live on trial wh_audiology). New ADR-19-fabric-ddm-
    syntax.md; adr-index/security-strategy/ADR-33 updated. docs commit 34bbc53 (pushed main + FF dev/uat).
Decisions made (new ADRs or locked decisions):
  - House-style typography is now a closed rule with an automated gate (no em dashes / smart quotes /
    ambiguity anywhere). Rate file stays at verified 0.275; R-19 deferred, recommendation INTERIM, $0.
  - ADR-19 CLOSED positive: Fabric Warehouse uses STANDARD T-SQL DDM (not Databricks MASK); Viewer sees
    masked, GRANT UNMASK reveals; NO CREATE USER FROM EXTERNAL PROVIDER (access via workspace/item grants,
    so generate_security.py emits role grants + GRANT UNMASK, never CREATE USER). Mask-at-Gold is viable.
Open items / blockers (ALL un-gated free-trial work is now DONE):
  - ALL remaining Phase-P exit items need money or an external system, NOT the free trial:
    (a) R-19 budget ceiling (USER/CTO) -> upgrade trial to F64 -> CU telemetry under load ->
        capacity recommendation FINAL + sign-off. (b) ADR-20/31 Dataverse LIVE verify -> needs a
        real Dataverse org (none in this tenant); 7-item checklist in ADR-31-dataverse-ingestion-path.md.
  - CLOSED this session (free trial): ADR-19 DDM incl. granular column/schema UNMASK; ADR-20/31 DESIGN;
    P-R24 (gen_seeds proven vs live control DB, 2 GO-batch scoping bugs fixed + regression guards);
    typography gate enforced across platform/dataflows/bi.
  - Backlog (deferred to later phases, not free-trial-blocking): meta.ingestion_object.dataverse_path
    ENUM('link','copy') (Phase-9 DDL); validate OneLake-security-first primary path (ADR-33) when GA in
    AU East; P-R23 master 1-job deadlock (Phase 6); G4b OAuth swap; trial expiry ≈2026-08-08.
Next session start instruction:
  Read CLAUDE.md, gameplan.md, and CLAUDE.local.md. Phase P is OPEN but every UN-GATED, free-trial item is
  DONE (ADR-19 closed, ADR-20/31 designed, P-R24 generator proven vs DB, typography enforced). To finish
  Phase P you now need EITHER funding (R-19 ceiling -> F64 load test -> capacity recommendation FINAL ->
  sign-off) OR a Dataverse org (ADR-20/31 live verify). Both are external/user decisions; ask the user.
---

# ----- superseded (session 16 close) -----
SESSION HANDOFF
Date       : 2026-06-14 (session 16 — CI/CD industrialisation, manifest→seed generator, ADR-47 reproducibility)
Phase      : P — Pilot on Trial (OPEN — exit gates NOT met). Parity on the slice is green
             (S15 batch_run 19). This session was DX/CI-CD + reproducibility DESIGN only; no
             telemetry, no capacity sign-off, no DDM/Dataverse spikes.
Last step  : S16 shipped (all SHA-verified): (1) master orchestrators master-development/
             master-platform (defs 23/24) — DEADLOCK on 1-parallel-job free tier, Option-B
             template-include CHOSEN+DEFERRED (cicd/master-orchestrators-template-include-design.md);
             (2) registered+foldered ALL pipelines → defs 7–30 (24) in \Platform\Dataflows\BI\
             Infra\Ops\FinOps\Master; deep-dive dummys/24-cicd-and-yaml-deep-dive.md; (3) finops-
             rate-refresh FIXED ($(Date:)→date -u + build-svc ACE 16404 on platform repo) → run
             428 GREEN, review PR !117; (4) ENV_PROVISIONED guard (test/uat/prod not provisioned)
             + assert-env-provisioned-steps.yml in 4 env pipelines; (5) **manifest→seed generator
             gen_seeds.py** (DEs edit YAML not MERGE; ingestion 01/02 + transform 03/04; 7 unit
             tests) + dataflows-gen-seeds (def 30) + master Stage 1b; scaffolder seed → MERGE-
             upsert; FIN-001 manifest-driven (PR !118); (6) ADR-47 + recreate-platform.md (3-layer
             reproducibility contract, greenfield, capacity_mode trial→paid — DESIGN ONLY).
Next step  : The REAL Phase-P exit path (unchanged, still gating): (1) ADR-19 DDM spike + ADR-20/31
             Dataverse spike on the trial; (2) R-19 budget ceiling (CTO/DE Mgr) → upgrade trial to
             F64 (gameplan P step 1, never done — trial is FTL4) → Wave-0 load test → capacity_
             estimator on real telemetry → capacity-recommendation.md FINAL → sign-off (unlocks
             paid quota). Secondary: prove transform generator via deploy-metadata on pilot (P-R24);
             master Option-B refactor OR a 2nd parallel job (P-R23); merge/close PR !117 + !118;
             ADR-47 L1 Terraform modules if continuing the reproducibility track.
Files created/modified this session: see the FILE LIST in the session-close message + git logs
             2026-06-14: platform cc53906/a4af247/3330290/5bc6300/e017dfc/31c2e73/2f978a2/61291fa/
             02810bb; docs 8e39019/eebe249/6def255/57dcc2b/ea77eb4/342ad7e/1105049/e4048cd/1488e09;
             dataflows d30e19a/b83b29d. ADO: defs 23-30 registered+foldered; build-svc ACE 16404
             (platform repo); ENV_PROVISIONED in 5 env vgs; finops run 428 + PR !117; FIN-001 PR !118.
Decisions made (new ADRs or locked decisions):
  - ADR-47 (Accepted): full-stack 3-layer parametric reproducibility (greenfield; L0/L1/L2;
    capacity_mode trial→paid; residue = explicit runbook steps; one driver).
  - Master orchestrators = Option-B (template-include) CHOSEN, DEFERRED (Phase-6); queue-and-wait
    masters work only on ≥2 parallel jobs.
  - DEs NEVER hand-write MERGE: manifest.yml + gen_seeds.py is the standard (meta=MERGE-upsert,
    log=init-only); applies to ingestion AND transform.
  - Build-svc Contribute (ACE 16404) on platform repo accepted (branch policies still gate).
Open items / blockers:
  - Phase-P EXIT GATES ALL OPEN: CU telemetry under load, capacity recommendation sign-off,
    ADR-19 DDM spike, ADR-20/31 Dataverse spike, R-19 budget ceiling (USER/CTO).
  - P-R23 master 1-job deadlock; P-R24 transform gen unproven vs DB; P-R25 gen-seeds drift;
    P-R26 build-svc write surface. PR !117 (rate refresh) + PR !118 (FIN-001) await review/merge.
  - Trial expiry ≈2026-08-08 (hard deadline for load test). G4b OAuth swap still pending.
Next session start instruction:
  Read CLAUDE.md, gameplan.md, and CLAUDE.local.md. Phase P is OPEN; S16 was tooling/CI-CD only.
  Pick up the REAL exit path: get the R-19 budget ceiling from the user, then run the ADR-19 DDM +
  ADR-20/31 Dataverse spikes on the trial; if funded, upgrade trial→F64 → load test → estimator →
  capacity-recommendation FINAL → sign-off. Optionally first prove the transform generator with one
  deploy-metadata on pilot (P-R24).
---

# ----- superseded (session 15 close) -----
Date       : 2026-06-14 (session 15 — P-R22 CLOSED: FULL CHAIN GREEN end-to-end via pl_batch_runner)
Phase      : P — Pilot on Trial (OPEN). Full orchestrated chain (ingest→silver→scd2→recon) now
             GREEN: log.batch_run 19 = SUCCEEDED (2026-06-14 02:30→02:39) after adding
             retry-on-throttle to the runner (FTL4 was failing back-to-back Spark sessions, not
             code — every step proven green individually first). Exit criteria still unchanged:
             CU telemetry NOT captured (load test gated R-19), recommendation NOT produced,
             DDM/Dataverse spikes NOT run.
Last step  : P-R22 root-caused + FIXED + PROVEN. (1) ROOT CAUSE: pl_batch_runner's
             transform_pyspark/scd2/recon Switch cases never pass lakehouse_base_path/env;
             nb_transform trusted the empty param and the child wrote silver to the WORKSPACE
             ROOT (onelake/<ws>/appointment → 400 Bad Request, log.run_event event_id 3). FIX:
             nb_transform now self-resolves the write base from meta.storage_target (ADR-36),
             mirroring nb_scd2/nb_recon (resolve_proc_domain via proc→job→batch since a transform
             proc has NULL object_id); base = root/<target_schema>; env defaults pilot. (2) 2nd
             bug: my REST updateDefinition pushed the repo's GIT-LOGICAL env id
             (0575664f-…, ws 0000) over the live REAL env id (c5cf66ef-cd9d-49b3-a265-95f40575664f,
             real ws) → InvalidEnvironmentArtifact. FIX = substitute env-id+ws-id at REST deploy
             (DEPLOY-SUBSTITUTION GAP — same class as connection-GUID substitution). (3) 3rd bug:
             nb_reconciliation_harness wrote log.dq_result with ingestion_run_id=None but the
             column is NOT NULL + FK → Spark session cancelled. FIX: recon anchors results to the
             object's latest ingestion_run when none passed. EVIDENCE (live, today): silver proc 3
             Completed (run_event: write merge rows=8 created=true); scd2 obj 5 Completed (hard
             invariant assert inside → held); recon obj 1 Completed (log.dq_result id=2:
             sum_recon PASSED 225.0==225.0 diff0%, ingestion_run_id=4). Dynamic firewall:
             ensure_sql_firewall.py (detect egress IP, upsert single stable rule, prune stale) —
             per USER "IP/network must be dynamic"; one-off rule deleted.
Next step  : (1) Commit this session's fixes across platform repo + SHA-verify (per sync rule):
             nb_transform, nb_reconciliation_harness (both copies), pl_batch_runner retry,
             ensure_sql_firewall.py. NOT YET PUSHED. (2) Then the REAL Phase-P blockers:
             ADR-19 DDM + ADR-20/31 Dataverse spikes; R-19 ceiling (USER) → upgrade trial to F64
             (gameplan P step 1, never done — trial is FTL4) → load test → capacity_estimator →
             F-SKU recommendation (the actual Phase-P gating deliverable, still not started).
             (3) Pipeline contract hardening (deferred, low-risk): pass env to ALL
             transform/scd2/recon cases (works today only via pilot default); add a write-path
             guardrail (target must contain .Lakehouse/Tables) so an empty base fails fast not as
             an opaque 400. (4) Phase-9 polish: ingest proc_run rows left 'running' on idempotent
             no-op (self-resolution path doesn't finish_run); cosmetic, batch still succeeds.
Files created/modified this session:
  - platform: framework/fabric-items/02 Transformation/nb_transform.Notebook/notebook-content.py
    + notebooks/transformation/nb_transform.py (self-resolve base_path from storage_target);
    framework/fabric-items/04 Quality/nb_reconciliation_harness.Notebook/notebook-content.py
    + notebooks/quality/nb_reconciliation_harness.py (ingestion_run_id anchor);
    framework/fabric-items/00 Orchestration/pl_batch_runner.DataPipeline/pipeline-content.json
    (TridentNotebook retry=3/60s on all 5 notebook activities — FTL4 robustness; +fail_batch
    hardening: dependsOn lk_close_batch_run_failed → Completed so the fail object always fires
    even if the serverless close-Lookup errors, + actionable message w/ batch_run_id);
    framework/tools/harness/ensure_sql_firewall.py NEW (dynamic firewall);
    infra/scripts/capacity_estimator.py (+Power BI licensing crossover: licensing_crossover(),
    --prod-report-viewers/--viewer-license, §3A report, Pro/PPU pricing; self-test ALL PASS)
  - docs: finops/sku-cost-justification.md NEW ("why F64?" decision + breakeven table + script);
    phase-P/capacity-recommendation.md (§3A crossover); finops/capacity-plan.md §4 +
    cost-model.md (F64 reframed as TBC-must-survive-crossover, not default);
    dummys/21-finops-deep-dive.md NEW (entry-point FinOps guide: levers/estimator/why-F64/
    trade-offs/risks/reporting) + 00-START-HERE registration;
    BINDING AU rates applied (au_east_rates.json) → capacity-recommendation.md INTERIM BINDING;
    rate-freshness guard (capacity_estimator) + refresh_rates.py + finops-rate-refresh.yml
    (assisted PR refresh, NO silent per-run auto-update); fabric-git-binding-guide.md made
    authoritative (§0/§1A closed list/§6 create+verify); dummys/21 §9A cost-dashboard backlog (BI)
  - git: platform 404c2fb/feb4d24/87bd5ea + docs 3be29f0/4af9b69/b456c90 committed LOCAL only
    (no remote on these checkouts → not pushed; main policy-protected)
  - FABRIC (live): nb_transform, nb_reconciliation_harness, nb_scd2_processor updateDefinition
    (real env id restored); recon/scd2 also had git-logical env, patched; pl_batch_runner
    retry-on-throttle patched live (JSON-walk, preserved live notebookIds/connection)
  - root: CLAUDE.local.md (this)
Decisions made (new ADRs or locked decisions):
  - No new ADR. Facts locked: (a) nb_transform joins the metadata-driven path-resolution
    contract (ADR-36) — NO framework transform notebook may trust a passed abfss; (b) REST
    notebook deploy MUST substitute env-id (git-logical→real) + ws-id (0000→real), same as
    connection-GUID substitution; (c) recon dq_result anchors to the latest ingestion_run;
    (d) runner notebook activities carry retry-on-throttle (retry=3/60s) — required on FTL4,
    also hardens paid capacity under concurrent load (ADR-42-adjacent);
    (e) NO paid SKU is named as a preference — only as the cheaper side of a measured crossover.
    F64 is justified ONLY above the Power BI viewer breakeven (cost(F64)−cost(compute_SKU))/per_user;
    Prod-only question; "why F64?" is answered with a number (sku-cost-justification.md).
Open items / blockers:
  - FTL4 throttling NO LONGER blocks the chain (retry-on-throttle absorbs it; batch_run 19
    green). But each chain run takes ~9 min with retries — a LOAD test on FTL4 will still
    throttle hard (P-R11); representative sizing needs F64 (R-19 ceiling, USER). Trial is FTL4,
    never upgraded to F64 per gameplan P step 1. Trial expiry ≈2026-08-08.
  - Phase-P PRIMARY deliverable (CU telemetry → F-SKU recommendation) still NOT started; R-19
    budget ceiling still unanswered (USER). ADR-19/20/31 spikes pending. G4b OAuth swap (USER).
  - Pipeline contract gaps: env not passed to transform/scd2/recon cases (pilot-default only);
    no write-path guardrail. Commit + SHA-verify the 3 notebook fixes (not yet pushed).
Next session start instruction:
  Read CLAUDE.md, gameplan.md, and CLAUDE.local.md. P-R22 is CLOSED — full chain GREEN
  (batch_run 19 succeeded; retry-on-throttle added). FIRST: commit + SHA-verify this session's
  fixes (nb_transform, nb_reconciliation_harness x2, pl_batch_runner retry, ensure_sql_firewall).
  THEN move to the real Phase-P blocker: get the R-19 budget ceiling from the user → upgrade the
  trial to F64 → load test → capacity_estimator → F-SKU recommendation (the Phase-P exit
  deliverable, still not started). ADR-19 DDM + ADR-20/31 Dataverse spikes also pending.

# ----- superseded (session 14 close) -----
Date       : 2026-06-12 (session 14 CLOSE — marathon: CI hardening, Copy ops, staged onboarding,
             naming v1, dummys 00–20, chain PARTIAL)
Phase      : P — Pilot on Trial (OPEN). Exit criteria NOT met: parity slice partial (ingest
             green via pipeline; silver→gold→recon blocked on P-R22); CU telemetry NOT
             captured (load test gated R-19); recommendation NOT produced; DDM/Dataverse
             spikes NOT run.
Last step  : S14 full record = session-log addenda 1–15 + close note; phase-P implementation
             §E12 (evidence ledger in runbook.md). Headlines: hosted-agent thinning ×2 fixed
             (install templates: terraform 287/288, msodbc 346); F3 Copy proven live (item
             38e5721b, 7 rows) + def 22 per-env deploys (run 318); ADR-44 A2 (dag_uid
             GENERATED, flow_shape dropdown); ADR-45 (migration dictionaries + per-object
             register); ADR-22-A1 (re-affirmed); ADR-46 + DDL 31 (17 v1-name synonyms LIVE);
             DDL 29 (retention value+unit, 2555→7y verified); DDL 30 (born disabled) +
             probe_connectivity (2 PASS) + suite=connectivity; deploy-code REAL (336:
             token_credential fix + flat_to_notebook converter; SlvrAudlgyApptAud001 =
             item 6b7327a5); deploy-metadata REAL (346 + bronze appointment columns seed
             gap fixed); synthetic dbo.appointment (8 rows); CHAIN runs 1–10: dag_run_id=
             'NULL' convention; live runner refs → EXPLICIT ids (zeros/logicalId resolution
             broke mid-day, P-R21); env=pilot not dev (storage_target); nb_transform dict-
             param fix; scd2/recon self-resolution shipped; nb_ingest GREEN via pipeline ×2;
             transform CHILD errors (P-R22). FTL4 430 throttling captured (P-R11 evidence).
             Docs: dummys 00–20 (+story 13, metadata 14, field-ref 20), pipeline-catalogue,
             ingestion-use-case-cookbook, environment-orchestration, migration-dictionary-spec.
Next step  : (1) P-R22: open the transform CHILD run log (Monitor → SlvrAudlgyApptAud001 run
             under chain run 2dd9bbc1 / rerun) → fix → chain green → verify silver Delta +
             gold SCD2 invariant + recon in log.dq_result. Use env=pilot, dag_run_id=NULL,
             batch_id=2. (2) Then ADR-19 DDM + ADR-20/31 Dataverse spikes. (3) R-19 ceiling
             (USER) → load test (NOTE: FTL4 throttles — see finops S14) → estimator →
             recommendation. (4) G4b OAuth swap (USER, 1 min). (5) P-R15 flat-source
             consolidation (converter now exists — fold tests/conftest).
Files created/modified this session: see the FILE LIST in the close message + git log
             2026-06-12 across platform/dataflows/docs (every push SHA-verified).
Decisions made (new ADRs or locked decisions):
  - ADR-44 A2 (tags '-'; dag_uid generated; flow_shape); ADR-45; ADR-22-A1; ADR-46 (+DDL 31
    synonyms live); retention value+unit standard (DDL 29); born-disabled lifecycle (DDL 30);
    convergence standard (meta MERGE-upsert / log init-only); no bronze→gold-direct shape;
    control DB per env re-affirmed; medallion archive = bronze-only re-affirmed (7y retention
    default with minors caveat).
Open items / blockers:
  - P-R22 transform child error (NEXT SESSION FIRST); P-R21 explicit-ids rule for REST
    deploys; P-R20 agent-dependency audit (Phase 6); FTL4 throttling (P-R11) — load test
    needs R-19 ceiling + possibly paid SKU; G4b OAuth swap (USER); trial expiry ≈2026-08-08;
    batch_param consumer (Phase 9, user's Optus columns: schedule/cluster/tag/email/
    concurrency → df_batch_param design); dummys 21 (CI/CD deep troubleshooting doc,
    user-requested — catalogue exists, deep version pending)
Next session start instruction:
  Read CLAUDE.md, gameplan.md, and CLAUDE.local.md. Start at P-R22: fetch the child notebook
  run log for SlvrAudlgyApptAud001 (Monitor, or rerun chain: pl_batch_runner 566c75a5 with
  batch_id=2, dag_run_id=NULL, env=pilot, ctrl_server/db = pilot control DB), fix the child
  error, drive the chain green, then verify silver/gold/recon evidence in log.* and OneLake.

# ----- superseded mid-session (S14 first handoff) -----
OLD-Date   : 2026-06-12 (session 14 — Terraform CI fix; F3 Copy template PROVEN LIVE; ops docs)
Phase      : P — Pilot on Trial (OPEN). Copy edge proven; silver chain still pending.
Last step  : S14: (1) run 282 root-caused — hosted agents no longer ship Terraform → pinned
             install template (templates/install-terraform-steps.yml, 1.10.5) in
             platform-pr-validation + ops-environment-rebuild; a827a85; re-runs 287+288 GREEN
             (4x "configuration is valid" — non-vacuous). (2) F3 Copy template OPERATIONAL:
             repo skeleton Copy JSON shape was WRONG (datasetSettings nests INSIDE source/sink;
             Lookup sibling shape does not apply); fixed + source_database/select_column_list
             params; deployed pl_copy_sql_bronze item 38e5721b (pilot ws, GUIDs substituted:
             conn 4a9f7919 / ws ee46ac62 / lh 04bee495); job 49524d36 Completed = 7 rows
             dbo.referral -> bronze Tables/dbo/referral_copy_smoke (Delta log numRecords:7,
             V-Order). PROVEN: connection GUID deploy-time-only, database runtime-parametric,
             SQL endpoint lags OneLake (verify via Delta log). (3) New docs:
             docs/cicd/pipeline-catalogue.md (16 pipelines: purpose/inputs/OUTPUTS) +
             docs/runbooks/ingestion-use-case-cookbook.md (UC1 D365 CRM, UC2 CSV=Optus file
             pattern, UC3 SQL/Synapse PROVEN, UC4 OData, UC5 REST, UC6 SFTP position =
             ADLS SFTP frontend if discovery finds feeds; Optus/ADF->Fabric mapping).
             (4) Manifests AUD-001/002 stale paths fixed. Pushes SHA-verified: platform
             4f4b6d2 (main/dev/uat), dataflows e24f241, docs 1e3ae86 + session-log/gameplan.
             KEY FINDING: SlvrAudlgyApptAud001 is NOT deployed as a Fabric item (ws listing
             proved it) — the silver chain needs dataflows-deploy-code FIRST.
Next step  : (1) Confirm runs 290-293 green (post-push validation, queued at close).
             (2) SILVER CHAIN on AUD-001: deploy SlvrAudlgyApptAud001 via dataflows-deploy-code
             (project_code=AUD-001, env=pilot, scope=notebooks) -> verify item in ws ->
             trigger pl_batch_runner job 2 (transform: proc 10 silver -> 20 scd2 -> 30 recon)
             -> verify silver Delta + gold dim SCD2 invariant + recon in log.dq_result.
             (3) G4b OAuth swap (USER, 1 min) -> dag-tier green. (4) ADR-19 DDM +
             ADR-20/31 Dataverse spikes. (5) P-R15 flat-source consolidation. (6) R-19
             ceiling (USER) -> load test -> telemetry -> capacity_estimator -> F-SKU rec.
Files created/modified this session:
  - platform: devops/pipelines/templates/install-terraform-steps.yml NEW;
    devops/pipelines/{platform-pr-validation,ops-environment-rebuild}.yml;
    framework/fabric-items/05 Copy Templates/{pl_copy_sql_bronze.DataPipeline/
    pipeline-content.json (correct shape), README.md} — a827a85, 4f4b6d2 (main/dev/uat)
  - dataflows: metadata/{AUD-001,AUD-002}/manifest.yml — e24f241 (main/dev)
  - docs: cicd/pipeline-catalogue.md NEW; runbooks/ingestion-use-case-cookbook.md NEW;
    decisions/session-log.md (S14) — 1e3ae86+ (main/dev)
  - root: gameplan.md §8 (S14), CLAUDE.local.md (this)
  - FABRIC (live): pl_copy_sql_bronze item 38e5721b in ws ee46ac62; bronze table
    dbo.referral_copy_smoke (7 rows, smoke artifact — safe to drop)
Decisions made (new ADRs or locked decisions):
  - No new ADR. Facts recorded: Copy JSON shape (datasetSettings nested); Fabric connections
    are NOT runtime-parametric (deploy-time substitution is the pattern — cookbook §2);
    SFTP position (UC-6: ADLS SFTP frontend as F4 landing, no speculative build);
    Terraform pinned-install required on hosted agents (1.10.5).
Open items / blockers:
  - Runs 290-293 confirmation (background poll was running at close)
  - Silver→scd2→recon chain (deploy notebook first!) — next session start
  - G4b OAuth swap (USER); R-19 budget ceiling (USER) — gates load test
  - ADR-19/20/31 spikes; P-R15; trial expiry ≈2026-08-08
  - Follow-up idea: CI smoke asserting deployed Environment runtime_version == ADR-24 baseline
Next session start instruction:
  Read CLAUDE.md, gameplan.md, and CLAUDE.local.md. Glance runs 290-293 finished green, then
  run dataflows-deploy-code (AUD-001, pilot, notebooks) to deploy SlvrAudlgyApptAud001, verify
  the item exists in ws ee46ac62, and execute the silver→scd2→recon chain (job 2 of
  df_audiology_appointments via pl_batch_runner; procs 10/20/30 already seeded).

# ----- superseded (session 13 close) -----
Date       : 2026-06-12 (session 13 — CI/CD MADE REAL: OIDC, validation evidence, DE clarity)
Phase      : P — Pilot on Trial (OPEN). CI/CD release path now PROVEN; load-test path unchanged.
Last step  : S13 complete (evidence: docs/phase-P/implementation.md §E11): (1) P-R14 CLOSED
             non-vacuously — run 274 "found 9 SQL file(s)… 10/10 passed" (old green was vacuous:
             multi-checkout dirs are REPO NAMES, not aliases — all DF/BI paths were wrong);
             runs 275 (bi) + 276 (notifications) green. (2) G1 CLOSED: OIDC SC sc-healthent-azure
             (fe3ac57a) + federated credential on sp-healthent-fabric-pilot + Reader + all-pipelines
             auth; vgs 3-8 = ARM_SERVICE_CONNECTION etc.; ALL auth now AzureCLI@2 + az tokens
             (zero SP secrets). Root cause of the ~100-run notify flood: SC inputs validate at
             COMPILE time — undefined vg var can never be rescued by a condition; cron now hourly
             until webhook. (3) All 16 YAMLs rewritten+renamed (ADR-44 A1): *-pr-validation,
             dataflows-{new-project,deploy-metadata,deploy-code,run-flow,run-tests,test-one-flow},
             bi-deploy, ops-*; defs 7-21 renamed/repointed; mojibake fixed (Run-form garble);
             project_code = SINGLE DE-typed key (dag_uid resolved from manifest, typed only at
             scaffold); run names parameterised + build TAGS + object-level deploy logs (every
             SQL TABLE/VIEW/PROC, notebook, meta.* table named) + run summary tabs. (4) G2
             CLOSED (build-service ACE 16404 on dataflows repo) after scaffold E2E run 278
             proved auto-issue (AUD-003) but hit TF401027; rerun 279 QUEUED at close. (5) §34
             amended: implementation.md OPENS with Solution Design & HLA (phase-P retrofitted
             §SD). (6) New docs: ingestion-source-families-and-connections.md (ADR-41 A2 — F7
             S3/GCS + F8 SharePoint; Connections vs KV-pointers vs shortcuts vs gateways =
             linked-services answer; JIT-firewall/Terraform pattern), fabric-git-binding-guide.md,
             maintenance-and-operations-manual.md (COMPULSORY: RACI, cadences, expiry register),
             05 Copy Templates (5 generic per-family Copy pipelines, clones prohibited),
             DE runbook §4 rewritten. Pushes SHA-verified: platform 271adbb (main/dev/uat),
             dataflows 2055c2b, docs 535e040+close commit.
Next step  : (1) ✅ DONE AT CLOSE: run 279 (dataflows-new-project) SUCCEEDED — scaffold E2E
             fully green (AUD-003 auto-issued, branch pushed, PR 114 opened); PR 114 abandoned
             + feature branch deleted + verified AUD-003 NOT on dev (register clean; P-R18
             closed). Run 280 (dataflows-pr-validation) green; run 282 (platform-pr-validation)
             was inProgress at close — glance at it first. (2) G4b: USER does 1-min OAuth swap on
             conn-healthent-pipeline-invoke (f7872fcf) → full dag-tier green. (3) Silver chain
             on pilot: proc → nb_transform → SlvrAudlgyApptAud001 → scd2 → recon. (4) P-R15
             flat-source consolidation. (5) DDM (ADR-19) + Dataverse (ADR-20/31) spikes.
             (6) R-19 ceiling (USER) → load test → telemetry → capacity_estimator → F-SKU rec.
             (7) When provisioned: fill WH_SQL_ENDPOINT/WH_NAME, TEST_LOCK_OBJECT_ID,
             TEAMS_WEBHOOK_URL in vgs (then notifications cron → */15 if minutes allow).
Files created/modified this session:
  - platform: devops/pipelines/* (16 files renamed/rewritten + template), framework/fabric-items/
    05 Copy Templates/* (11 files) — commits d742a05, 271adbb (main/dev/uat)
  - dataflows: docs/de-onboarding-runbook.md §4 — commit 2055c2b (main/dev)
  - docs: phase-P/{implementation(§SD+E11),finops,risk,runbook}.md; architecture/{ingestion-
    source-families-and-connections, fabric-git-binding-guide}.md NEW; runbooks/maintenance-
    and-operations-manual.md NEW; decisions/{session-log §13, adr-index ADR-44 A1 + ADR-41 A2};
    cicd/ado-setup-record.md (§2 table, G1/G2 closed, changelog); timeline/gantt.md; gameplan §8
  - root: CLAUDE.md §34.1 (HLA standard), gameplan.md (synced), CLAUDE.local.md (this)
  - ADO/Azure (live): SC fe3ac57a + FIC + Reader role + all-pipelines auth; vgs 3-8; defs 7-21
    renamed; build-service ACE on dataflows repo; runs 274-279
Decisions made (new ADRs or locked decisions):
  - ADR-44 A1: self-explanatory pipeline names; project_code single key; OIDC SC auth;
    tags/object-level logs; anti-vacuous CI guard; checkout dirs = repo names
  - ADR-41 A2: families F7/F8; connection-mechanism matrix (linked-services answer);
    generic Copy templates; JIT-firewall pattern (static=Terraform, per-run=pipeline, prod=PE)
  - §34.1: every phase implementation.md opens with Solution Design & HLA (UDP DSD §2 shape)
  - Maintenance & operations manual = compulsory program artifact (runbooks/)
Open items / blockers:
  - Run 279 + 280/282 confirmation + throwaway-PR cleanup (first thing next session)
  - G4b OAuth swap (USER, 1 min); R-19 budget ceiling (USER) — gates load test
  - Silver→scd2→recon chain; ADR-19/20/31 spikes; P-R15; trial expiry ≈2026-08-08
  - vg placeholders to fill when provisioned: WH_*, TEST_LOCK_OBJECT_ID, TEAMS_WEBHOOK_URL
Next session start instruction:
  Read CLAUDE.md, gameplan.md, and CLAUDE.local.md. Run 279+280 green and PR cleanup already
  done at close; just glance that run 282 (platform-pr-validation) finished green. Then start
  the silver→scd2→recon chain on AUD-001 (proc_registry already points at
  SlvrAudlgyApptAud001); after that the ADR-19 DDM + ADR-20/31 Dataverse spikes.

# ----- superseded (session 12 close) -----
Date       : 2026-06-11 (session 12 — INDUSTRIALISATION SWEEP; sync incident; naming locked)
Phase      : P — Pilot on Trial (OPEN). Framework industrialised; load-test path unchanged.
Last step  : S12 complete (evidence: docs/phase-P/implementation.md §E10): (1) notifications
             LIVE — DDL 26 outbox+quarantined, runner close-queries write rows, dispatcher
             def 20 (skips until G1 webhook); (2) wheel 0.3.0 PUBLISHED (env c5cf66ef) =
             writers (append/overwrite/merge/scd2+§29 invariant) + RunLogger→log.run_event
             (DDL 27); templates+example rewired; 38 tests; (3) test harness def 21 + core10
             deterministic scenarios + tests/regression; (4) policies everywhere: AU-residency
             DENY applied (subscription), Spark timeout 15m, ADO environments 3-7 + Seniors
             approvals uat/prod (G3 closed), resource authorizations (G5 closed),
             policy-register.md; (5) SYNC INCIDENT root-caused: branch policies rejected my
             pushes + suppressed stderr = stale remotes (caused user's YAML error) →
             PolicyExempt(128) admin lane + MANDATORY remote-SHA verify after every push;
             (6) CI/CD centralised: ALL 16 YAMLs in platform devops/pipelines,
             <area>-<action> names (defs 7-21), preview 15/15 OK, trigger flood fixed
             (resource triggers, path scoping, [skip ci]), targets dev/uat/prod (dev-vars→
             pilot infra interim), vgs 4-8 created+authorized; (7) Fabric Git binding LIVE
             ws ee46ac62 ↔ platform / dev / /framework/fabric-items (branches = main/dev/uat
             only); (8) NAMING LOCKED (ADR-43/44 + docs/architecture/naming-and-structure-
             standard.md): {layer}/{DDL|Notebook}/{PROJECT-ID}/ folders, project codes
             AUTO-ISSUED by scaffolder from metadata/project-register.md (DDL 28 UNIQUE;
             AUD-001/002 live incl. proc_registry → SlvrAudlgyApptAud001; SQL NN-bands;
             objects snake_case = option b); (9) BI ws 1d915b00 + bi-operating-model.md
             (DE=numbers / BI=presentation §1A); (10) escalation-matrix.md (W4 closed),
             new-project-quickstart.md, Mermaid diagrams ×4 READMEs, framework purpose
             folders (repo+workspace), framework/tools/{scaffold,harness}, dataflows+bi
             content-only, example flows fixed (manifests/residue/template-parity).
Next step  : (1) FIRST GREEN CI RUNS post-centralisation (P-R14): real commit (no [skip ci])
             on dataflows dev → dataflows-ci green → same for platform-ci/wheel-build.
             (2) Flat-source consolidation (P-R15): switch tests/conftest to canonical
             notebook-content.py, retire flat .py + converter. (3) G4b: USER does 1-min
             OAuth swap on conn-healthent-pipeline-invoke (f7872fcf) → full dag-tier green.
             (4) Silver chain on pilot: proc → nb_transform → SlvrAudlgyApptAud001 → scd2 →
             recon (proc_registry already points at the new name). (5) DDM (ADR-19) +
             Dataverse (ADR-20/31) spikes. (6) R-19 ceiling (USER) → load test → telemetry
             → capacity_estimator → F-SKU recommendation.
Files created/modified this session:
  - ~60 files across all four repos (all pushed + remote-SHA-verified) + live objects
    (DDL 26/27/28; wheel 0.3.0 publish; pipeline patches; Azure policy; ADO envs/vgs/defs;
    Git binding; BI ws). Full list: s12 close message + session-log (docs repo).
Decisions made (new ADRs or locked decisions):
  - ADR-43 Naming & Structure Standard (PROJECT-ID folders, auto-issue register, Optus
    notebooks, EarLake SQL bands, objects snake_case = option b)
  - ADR-44 Central CI/CD topology (platform devops/pipelines, <area>-<action>; amends
    ADR-37/38) + Git binding ws↔dev via bypass identity; branches main/dev/uat only
  - PolicyExempt admin push lane + remote-SHA verification rule (sync-incident RCA)
  - Targets dev/uat/prod only; healthent-dev-vars maps to pilot infra until Phase 4
Open items / blockers:
  - R-19 budget ceiling (user) — gates load test; G4b OAuth swap (user, 1 min)
  - P-R14 first green CI runs; P-R15 flat-source consolidation; G1 OIDC SCs; G2
    build-service grant (scaffold auto-PR); trial expiry ≈2026-08-08; ADR-19/20/31 spikes
Next session start instruction:
  Read CLAUDE.md, gameplan.md, and CLAUDE.local.md. Then start with P-R14: make a real
  commit (no [skip ci]) on dataflows dev → confirm dataflows-ci green → then platform →
  then the silver→scd2→recon chain (step 4 above).

# ----- superseded (session 11 close) -----
Date       : 2026-06-11 (session 11 — FIRST GREEN E2E RUN; ADR-41/42; JD alignment)
Phase      : P — Pilot on Trial; step 4 ingestion leg ✅ GREEN (run a3e20391: rows_copied=4,
             write_confirmed=1, watermark epoch→2026-06-10 09:45, lock free, breaker 0).
Last step  : ROOT CAUSE H8 found+fixed: %run shares one namespace; nb_watermark_manager's
             parameters cell (ctrl_server="" etc.) ran AFTER Fabric injected job params and
             clobbered them — every HYT00 since 06-10 was pyodbc dialing an empty Server=.
             Proof chain: H6 (probe-exact string, kept ,1433) ✗ → H7 (timeout=60 + retry×4) ✗ →
             H8 guard proved ctrl_server='' → minimal probe nb_probe_params (112e90b0) proved
             injection WORKS → restructure ✗ → library-default clobber = cause. Fix:
             globals().get("var", default) in libraries (deployed + repo synced); standards:
             parameters cell = FIRST code cell, typed literals (no None), no banner comments,
             preflight fail-fast on empty targets (ADR-42 W6/W7; CI lint queued Phase 9).
             Unit tests green (35). ALSO: ADR-41 (source families F1-F5; file_landing NEW;
             drift_policy; admission control; runtime-overrun) + ADR-42 (capacity topology;
             scheduled SKU scaling guardrails; intraday workspace-shifting REJECTED; W1-W7)
             + docs/architecture/source-platform-profile.md (JD=Serverless+ADLS only, interview
             =Fabric migration real mandate; no Dedicated pool in JD → Phase 1 question;
             R-18 amplified by BAU duty).
Next step  : ✅ SUPERSEDED LIVE 2026-06-11 LATE SESSION: G4 SOLVED via SP (sp-healthent-fabric-pilot
             e80c2226; conns 4a9f7919 SQL + f7872fcf invoke); PIPELINE E2E GREEN (b96d1aee:
             batch_run 3, rows=2, wm→02:30; DDL 25 + notebook self-resolution; G4b = InvokePipeline
             +SP token gap, fix = one-time user-OAuth swap on invoke conn); WHEEL CUTOVER GREEN
             (1c3b91b9: wheel 0.2.1 via env c5cf66ef, nb_ingestion_incremental zero %run, rows=1,
             wm→05:30). NOW NEXT: (a) switch nb_transform/scd2/recon to wheel imports → delete 3
             library notebooks (ADR-40 A1 end-state); (b) close spine-rows-on-success in runner
             (Phase 9 polish; manual closes done); (c) G4b OAuth swap (user UI) → dag-tier green;
             (d) silver→scd2→recon chain; (e) spikes + R-19 → load test.
             Docs added: framework-troubleshooting.md (16-entry register), fabric-environment-guide.md.
             OLD (done): Create the 2 Fabric CONNECTIONS (control-DB SQL + pipeline-invoke) and patch
             the GUIDs into pl_batch_runner/pl_dag_runner — the ONE manual step blocking the
             metadata-driven pipeline E2E (interactive OAuth in UI, or Phase-5 SP). Then run
             pl_dag_runner(dag_uid=df_audiology_referrals) end-to-end. (2) Silver chain:
             nb_transform via proc → scd2 → recon. (3) ADO gap register G1–G7
             (docs/cicd/ado-setup-record.md §6): OIDC service connections, build-service perms
             for pl-new-dataflow, ADO Environments, first-run auths, build-validation policies,
             KV-linked groups — 13 pipelines REGISTERED (ids 7–19), main policies ×4 repos,
             healthent-pilot-vars exist. (4) DDM + Dataverse spikes.
             (5) R-19 ceiling (user) → load test → estimator → recommendation. EarLake adoptions
             A1-A8 in docs/review/earlake-reference-review.md (A5 firewall script + A6 generator
             are quick wins). (.claude_tmp_run.py = notebook trigger; .claude_tmp_verify.sql =
             telemetry oracle; pilot ws ee46ac62; pl_batch_runner 566c75a5, pl_dag_runner
             4e33a5b0; ADO https://dev.azure.com/earlake project Fabric, 4 repos main+dev.)
             IDEMPOTENCY ✅ verified (no-op on confirmed window). Sessions 11 was: green E2E
             (H8 %run clobber), ADR-41/42, ADR-40 A1 tables+pipelines-only, IP-format runbook v2,
             capacity-plan, one-workspace consolidation, ADO live.
Files created/modified this session:
  - platform: fabric-items/notebooks/framework/{nb_framework_common.py (probe-exact conn str +
    timeout=60/retry×4 + preflight guard), nb_watermark_manager.py (globals().get defaults),
    nb_ingestion_incremental.py (proc_run_id=0 + parameters-cell standards note)}
  - FABRIC (live): nb_framework_common, nb_watermark_manager, nb_ingestion_incremental
    updateDefinition ×5; nb_probe_params created (112e90b0)
  - platform: control-plane/sql/metadata/24_meta_drift_policy_and_backfill.sql NEW —
    drift_policy + run_kind + drift_detail; DEPLOYED LIVE 24/24 (3 cols + 2 CHECKs verified)
  - docs: runbooks/phase-completion-runbook.md REWRITTEN v2 (enterprise Implementation-Plan
    format per user's UDP UC1 example + program evidence bar; §4.A = 7 defensibility fixes;
    phase-P/runbook.md retrofit due at phase close); finops/capacity-plan.md NEW (SKU
    selection formula: smoothed background 24h vs interactive peak + 25-30% headroom +
    F64 licensing floor; Synapse footprint first-cut translation; Spark pool per-env table;
    I/O excluded from SKU — storage billed separately)
  - docs: decisions/{ADR-41-source-family-ingestion-patterns.md NEW,
    ADR-42-capacity-topology-and-scheduled-scaling.md NEW, adr-index.md, session-log.md},
    architecture/source-platform-profile.md NEW, phase-P/implementation.md (E9 to green)
  - root: CLAUDE.md (§21 +ADR-41/42), gameplan.md (§8 Phase P row), CLAUDE.local.md
Decisions made (new ADRs or locked decisions):
  - ADR-41: source-family ingestion patterns (Accepted) + A1: Copy-vs-notebook per family
  - ADR-42: capacity topology + scheduled scaling; intraday workspace-shift REJECTED (Accepted)
  - ADR-40 A1 (user-directed): visible surface = TABLES + PIPELINES only; no notebooks in
    shared workspaces; all code via ADO CI/CD; WHEEL now committed Phase 9/10; DE playground
    ws (healthent-audiology-dev e87a0d11) kept permanently empty
  - Phase-end docs = Implementation-Plan format v2 (phase-completion-runbook.md)
  - Capacity ownership: admin-by-group + fabric-admin svc acct; automation via SP (capacity-plan §3A)
  - Notebook parameters-cell + %run-library standards (W7) + preflight contract everywhere (W6)
Open items / blockers:
  - R-19 budget ceiling (user) — gates the load test
  - Silver→scd2→recon chain + idempotency re-run (next session start)
  - ADR-19 DDM + ADR-20/31 Dataverse spikes; FTL4 P-R11; trial expiry ≈2026-08-08
  - W2 prod scale automation (Phase 4); W3 access matrix (Phase 5); W4 escalation matrix (Phase 14)
  - Phase 1 discovery question: does any Dedicated SQL Pool actually exist? (JD suggests no)
Next session start instruction:
  Read CLAUDE.md, gameplan.md, and CLAUDE.local.md. Then (1) re-run .claude_tmp_run.py unchanged
  to verify idempotent no-op on the confirmed window (watermark must NOT advance, no duplicate
  rows), then (2) build/run the silver transform → scd2 → reconciliation chain on object 4's flow.

# ----- superseded (session 10 close) -----
Date       : 2026-06-10 (session 10 — LIVE pilot day; session close)
Phase      : P — Pilot on Trial — **ENTERED 2026-06-10**; steps 1–3 complete (live evidence,
             runbook §5c); step 4 IN PROGRESS (first E2E run blocked on H6).
Last step  : Steps 1–3 executed live: Entra resolved (P-R7 closed; fabric-admin f7c47459 = Fabric
             Administrator); trial ACTIVE (FTL4 — ~F4-class FINDING P-R11 — AU East verified, capacity
             1d32dc5f, 2/5 trials used); ws ee46ac62 + 4 schema-enabled LHs + wh_audiology; control DB
             sqldb-healthent-control-pilot (GP_S_Gen5 serverless, AAD-ONLY, pause 60m, 2GB, tagged);
             DDL 23/23 + example seeds 8/8 deployed; live resolution gates 6/6 = 0; 8 notebooks deployed;
             runtime PROBE Completed (pyodbc+ODBC18+token+AAD connect proven on RT1.3 — VERIFY #1+#9
             closed); kv-hent-aud-pilot (28-char name bug fixed in seed10+live+cookbook); synthetic
             dbo.referral (4 rows) + spine (object_id=4, proc_run_id=1); E2E run ×5 attempts FAILED —
             isolated to control_connection HYT00; pause theory disproven (DB Online);
             **H6 = conn-string delta vs working probe: drop ',1433' + 'Connection Timeout' (invalid
             ODBC keyword; valid = 'Connect Timeout')**. control_connection now has retry×3/backoff
             (keep — serverless resume hardening); 35 unit tests green. Docs: security-strategy.md,
             tradeoffs-index.md, FinOps actuals (~AU$1–6/mo), implementation E1–E9, runbook §5c.
Next step  : (1) Apply H6 to nb_framework_common conn string → updateDefinition → re-run
             (.claude_tmp_run.py has the trigger; nb id f2a90124, probe nb 96f1e387 for comparison).
             (2) On green: verify Bronze Delta rows + watermark advanced + lock released → run silver
             (nb_transform via proc) → scd2 → recon. (3) DDM + Dataverse spikes. (4) R-19 ceiling from
             user. (5) Load test sized to FTL4 reality → telemetry → estimator → recommendation.
Files created/modified this session (live-day; sessions 8–9 lists in session-log):
  - platform: fabric-items/notebooks/framework/nb_framework_common.py (retry hardening);
    control-plane/sql/metadata/10 (kv name fix), 22, 23 (new); docs/platform-ops-runbook.md;
    devops/pipelines/{ci-platform,pl-test-platform,pl-env-pause-resume,pl-env-rebuild}.yml; README.md
  - dataflows: metadata/df_audiology_appointments/01–06 (guarded-INSERT rewrite);
    metadata/df_audiology_referrals/{01,02} (new flow); docs/{metadata-cookbook,de-onboarding-runbook}.md;
    pipelines/{ci-dataflows,pl-test-dataflows,templates/steps-static-suite}.yml; scripts/new_dataflow.py;
    silver notebook body; gold/DDL view
  - bi: warehouse/{domains}/ (new); pipelines/{ci-bi,pl-bi-sync}.yml; README.md;
    semantic-models/audiology/AudiologyAppointments.SemanticModel/README.md
  - docs: decisions/{ADR-37,38,39,40, adr-index, session-log, tradeoffs-index};
    migration/{wave-plan, wave-runbook-template, delivery-process}.md; security/security-strategy.md;
    phase-P/{implementation,finops,risk,runbook}.md; finops/cost-model.md; timeline/gantt.md
  - root: CLAUDE.md (§10 banner, §21, §24, §4), gameplan.md (§8), CLAUDE.local.md
  - AZURE/FABRIC (live): Entra user fabric-admin + Fabric Admin role; trial capacity; ws ee46ac62;
    4 lakehouses + warehouse; 8 notebooks + probe; rg-healthent-control-pilot {sql server AAD-only,
    sqldb serverless, 2 firewall rules, kv-hent-aud-pilot + secret + 2 role grants}; RG tags;
    Spark settings (1 node); dbo.referral + spine rows; DDL+seeds deployed
Decisions made (new ADRs or locked decisions):
  - ADR-40 workspace topology (framework ws + domain ws; %run forces co-location until wheel)
  - Pilot control DB = Azure SQL serverless (user-confirmed); BI warehouse split + security lint;
    Azure SQL access policy (DE RW dev/test MFA; prod read-only, SP/admin writers)
Open items / blockers:
  - H6 conn-string fix → first green E2E run (the immediate next action)
  - R-19 budget ceiling (user) — gates the load test
  - P-R11 FTL4 sizing; ADR-19 DDM + ADR-20/31 Dataverse spikes; trial expiry ≈2026-08-08
  - ADR-30 retention legal sign-off; per-repo CLAUDE.md stale (root canonical, Phase 6)
Next session start instruction:
  Read CLAUDE.md, gameplan.md, and CLAUDE.local.md. Then apply H6 (mirror the probe connection
  string in nb_framework_common: remove ',1433', use 'Connect Timeout' or none), redeploy that
  notebook, re-run the E2E ingestion (script .claude_tmp_run.py), and continue Phase P step 5.
