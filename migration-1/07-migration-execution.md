# 07 - Migration execution

How the actual Synapse-to-Fabric migration runs: rationalise (not lift-and-shift), the wave model, the
parallel-run + reconciliation gate, the Synapse archival strategy, and decommission.

## 1. Principles
- **Rationalise + redesign every asset** - assess each Synapse object, decide its fate, rebuild it Fabric-native.
  Never port 1:1.
- **Steady-state ingestion goes DIRECT from the origin source** (not through Synapse). Synapse is used ONLY for
  the one-time historical/archival backfill + the parallel-run baseline, then decommissioned.
- **Every migration includes:** parallel run -> validation (reconciliation) -> cutover -> rollback plan ->
  per-object decommission after a 30-day clean hypercare.

## 2. Discovery feeds everything (Phase 1)
Read-only inventory produces two machine-readable dictionaries (one row per object): a **source data dictionary**
(volumetrics, columns + classification, update pattern, lineage, source family) and a **target/platform
dictionary** (generated from meta.*/Purview, never authored). A `meta.migration_object` forward-only state machine
tracks each object (discovered -> onboarded -> parallel -> reconciled -> cutover -> decommissioned). The
dictionaries drive a **dictionary -> seeds generator** (Phase 11): "typing becomes reviewing."

## 3. Wave model
Waves are prioritised by business value + complexity. Wave 0 is the "green at load" proof (the framework runs all
objects within SLA under concurrency caps - the exit gate of Phase 9). Each subsequent wave: onboard by config ->
backfill history -> run incrementally in parallel with Synapse -> reconcile -> cutover -> decommission per object.
Nothing in Wave N+1 starts until Wave N's reconciliation is clean.

## 4. The reconciliation gate (the evidence)
Per migrated object: (1) row count within tolerance; (2) SUM measure within tolerance (catches silent
cast/precision loss) OR a row-hash/checksum for dimensions/text-heavy tables; (3) SCD2 invariant (zero duplicate
current rows per business key). Results in `log.dq_result`. **No cutover, no decommission, until recon passes.**
gen_seeds auto-seeds the recon rules so the per-flow check is enforced, not silently dropped.

## 5. Synapse archival / historical backfill (the one Synapse-source path)
- **Read Synapse BRONZE (raw)** by default and re-derive Silver/Gold in Fabric (rationalise). Read silver/gold
  only as a documented per-object exception (curated history too costly to re-derive).
- **Read the STORAGE, not serverless SQL, for bulk.** You cannot shortcut to serverless (it has no storage);
  shortcut the ADLS containers behind it (one connection per container). Use serverless SQL only for
  validation/recon or when you have SQL-but-not-storage access.
- **A shortcut is a transient READ, not the durable end-state.** For data you keep after retiring Synapse:
  **shortcut to read -> write managed Delta into Fabric -> recon -> drop the shortcut.** Now Fabric owns it and
  Synapse + its lake can be decommissioned. Leaving migrated data as a shortcut couples you to the old platform.
- **Active vs cold:** active history -> Bronze->Silver->Gold + age-out to `lh_archive`; cold/retain-only ->
  straight to `lh_archive` after recon, no Silver/Gold.
- **Format:** non-Delta sources (CSV/Parquet) convert to Delta on write (Fabric-native + Direct-Lake-ready).
- This is one finite backfill, retired after recon + hypercare (it is exception #1 in 02 section 3).

## 6. Microsoft migration tools = accelerators, not the strategy
Warehouse/Spark Migration Assistants, Synapse-pipeline-to-Data-Factory, Synapse Pathway, pipeline mounting,
OneLake shortcuts, Copy job, Dataverse Link to Fabric, the fab CLI/REST - use them as accelerators INSIDE the
metadata-driven framework, never as the migration strategy itself.

## 7. Decommission
Synapse assets are turned off only after a 30-day clean hypercare in Fabric, per object, with reconciliation
evidence retained. Archive retention/erasure honoured via meta.purge_rule + VACUUM (see 04 section 5).
