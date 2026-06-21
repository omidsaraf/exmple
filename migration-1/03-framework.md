# 03 - Metadata-driven framework

The engine. Control plane, config vs state, the generic runner, orchestration grain, the generators
(manifest in, everything out), and the data-quality / SCD2 / reconciliation standards.

## 1. Control plane (Azure SQL DB) - LOCKED
All `meta.*` (config) and `log.*` (state) live in `sqldb-healthent-control-{env}`, never the Fabric Warehouse,
because the framework depends on enforced PK/FK/UNIQUE/CHECK + IDENTITY. One control DB per env.

- **meta.* = configuration** - written ONLY by engineers via CI/CD (the loader), never at runtime.
- **log.* = state** - written ONLY by the runtime identity during execution (watermarks, run-locks, run history).
- Core meta: `source_connection, ingestion_object, ingestion_column, dag, framework_batch, batch_param,
  job_registry, proc_registry, proc_param, dq_rule, storage_target, external_location, purge_rule`.
- Core log: `dag_run, batch_run, job_run, proc_run, ingestion_run, object_watermark, run_lock, dq_result,
  run_event, notification_outbox`.

## 2. Watermark rules (non-negotiable)
1. Ceiling = MAX(watermark_col) from source, never now(). 2. Upper bound persisted BEFORE copy. 3. Watermark
advances ONLY when write_confirmed=1. 4. Half-open window (lower, upper]. 5. Typed columns only (datetime2(3) or
bigint). 6. Epoch init 1900-01-01. 7. Run-lock prevents concurrent watermark writes.

## 3. Ingestion control flow + circuit breaker
`resolve_config -> acquire_lock -> branch(load_type) -> check_drift -> copy -> write_confirmed=1 ->
advance_watermark -> reset_failures -> release_lock`. On failure: record, increment consecutive_failures, trip
the breaker (is_enabled=0) at threshold, release lock (failed), notify. Everything is idempotent + re-runnable.

## 4. Orchestration (one generic runner; ADR: orchestration)
- **Grain:** DAG (subject area) -> 3 layer **batches** (bronze/silver/gold; the gate + Spark-session boundary)
  -> **jobs** (parallel or sequential by job order) -> **procs** -> proc_params.
- **Two flat ForEach loops only - never nested.** Tier 1 admits/queues by priority, run window, concurrency-group
  cap, and target capacity; throttling = back-pressure (queue + retry-on-throttle), never hard-fail.
- **Triggers:** schedule (cron) and event. Cross-DAG admission because all DAGs share one capacity per env.
- **Onboarding a source = config only** (a manifest -> a few meta rows); no new pipeline is ever written.

## 5. Generators - manifest in, everything out (single source of truth)
The DE authors **one file: `manifest.yml`**. Reusable platform generators produce the rest; CI drift-gates each.
| Generator | Produces | Notes |
|---|---|---|
| `validate_manifest` | (gate) | normalises case/space/identifiers; closed enums; friendly errors; mistake-proof |
| `gen_seeds` | meta.* seeds | rendered at deploy (NOT committed); columns optional for auto_map sources |
| `gen_ddl` | visible CREATE TABLE contract (bronze+gold; gold incl. SCD2 system cols) | committed + drift-gated; normalises Spark types -> T-SQL; silver = notebook-defined |
| `gen_views` | `[domain]_VIEW` + `[domain]_TECH_VIEW` per layer | CLS by omission + group-only RLS; published after tables exist |
| `load_metadata` | meta.* in the control DB | ONE reusable path: validate + render + apply (retry on serverless resume) |
| `gen_source_catalogue` | the registered-sources register | generated from meta.source_connection (can't drift) |
| `new_dataflow` | a project skeleton | stable external project code; no-clobber uniqueness; register index regenerated |

Rule: never hand-write a MERGE, a seed, a view, or table DDL twice. Edit the manifest, regenerate, review in the
PR. Add/change = MERGE-upsert; remove = prune (opt-in). Registration is ALWAYS via CI/CD, never manual.

## 6. Data quality (per layer)
Bronze: non-empty warn, breaking-drift block, dup-key log, volume-drop check. Silver: NOT NULL block, FK block,
range block, SCD2-uniqueness hard block. Gold: row-recon block, SUM/checksum-recon block, PHI-mask hard block
(P1 on failure). Defaults: row/measure tolerance 0.1%, zero nulls on mandatory, zero Gold dup keys, late-arriving
alert > 3 days; override per object via proc_param. Results to `log.dq_result`.

## 7. SCD Type 2 (every Gold dim)
System columns: `hash_key NVARCHAR(64)` (SHA-256 of tracked attrs, sorted, NULL->'', deterministic),
`effective_from`, `effective_to NULL`, `is_current BIT`, `mrg_ind ('A'|'E'|'SD')`, `created_at`, `updated_at`.
MERGE: expire changed current rows (E), insert new versions (A); soft-delete via NOT MATCHED BY SOURCE (SD).
Invariant after every run: zero duplicate current rows per business key - enforced in Spark (Gold won't enforce it).

## 8. Reconciliation (the evidence gate)
(1) row count within tolerance; (2) **SUM** measure within tolerance (catches silent cast/precision loss), or a
**row-hash/checksum** for dimensions/text-heavy tables (selectable per object); (3) SCD2 invariant. Recorded in
`log.dq_result`. **gen_seeds auto-seeds the recon rules so the per-flow check is ENFORCED, not computed-then-dropped.**
No object is trusted, archived, or its source decommissioned until recon passes.

## 9. The Phase-P thin slice vs the hardened framework
Phase P builds a deliberately thin v0 (minimum DDL + one controller + watermark/recon notebooks) to validate
sizing and approach - a throwaway spike. Phases 9/10 build the hardened framework (the wheel + generators above)
and may discard the v0. Do not lock production framework design in Phase P.
