# 10 - Lessons learned (why every rule above exists)

The hard-won lessons from the previous build, distilled. Each shaped a rule in 01-09. Read this to understand the
*why* and to avoid repeating the cost.

## Architecture + serving
1. **Don't add a separate Warehouse for serving.** Tables in the lakehouse + views in the lakehouse SQL analytics
   endpoint is simpler, GA, and one fewer item to govern. A Warehouse is only for writable T-SQL / OPENROWSET over
   non-Delta shortcuts. (Several design flips converged here - 02/ADR-51.)
2. **CLS by omission beats DDM on the lakehouse.** The lakehouse SQL endpoint is read-only - `ALTER TABLE ADD
   MASKED` is unavailable; omitting PHI from the consumption view is both possible and stronger. (ADR-53.)
3. **Separate view schemas (`_VIEW` / `_TECH_VIEW`), exact table names, no `v_`.** Enables clean schema-level
   grants and keeps base tables ungranted. View name = table name (1:1) avoids confusion. (User-directed.)
4. **Security is at the data/model layer, never the dashboard.** Direct Lake bypasses views, so model RLS/OLS is
   mandatory; "hide the visual" is not security.
5. **dim_date and reference data are generated, not ingested.** No source, no SCD2; `date_key = yyyymmdd`; bake AU
   fiscal + holidays in once so every report agrees.

## Framework + metadata
6. **One default ingestion path + a closed list of exceptions.** Everything through the framework keeps the
   platform uniform and reconcilable; ad-hoc bypasses lose a guarantee. Write the exceptions down (7 of them).
7. **The manifest is the single source of truth; generate the rest.** Seeds, table DDL, and views are generated +
   drift-gated. Hand-writing a MERGE or a view twice is how drift starts.
8. **A computed reconciliation that is silently dropped is a data-loss bug.** Auto-seed the recon rules so the
   per-flow row/SUM/checksum check is actually ENFORCED. (Found live - a real gap.)
9. **Make generators tolerant of the real world.** Spark types in manifests (`string`) must normalise to T-SQL
   for the DDL to parse; auto-map sources have no columns; the generator must handle both, not crash.
10. **`shell=True` with a list of args runs only the first arg on Linux** - it returned the az welcome banner as a
    token. Small shell/portability bugs cause baffling failures; prefer the list form without `shell=True`.

## Capacity, cost, CI
11. **The trial is not F64.** A trial capacity is ~F4-class and cannot be resized; it throttles the Spark chain.
    A representative load test needs a short paid F64 PAYG window (~hours), then pause. Don't size from the trial.
12. **Fabric throttles on accumulated backlog, not peak.** Size with a burndown simulation + time-above-threshold,
    split interactive vs background - not a peak/average number.
13. **F64 is a licensing decision, not just compute.** Above the viewer breakeven, F64 (free viewers) beats
    F8+Pro even when compute fits on F8.
14. **Cost the whole bill** - control SQL DBs, Key Vaults, private endpoints, Purview, egress, and **ADO
    pipeline minutes** (the free tier runs out and stalls all CI). Arrange agent capacity before relying on CI.
15. **"All pipelines failed" was a quota wall, not a bug.** Always check the run duration/issue (0s + "no free
    minutes") before chasing code. Read the actual failure; don't assume.

## Migration
16. **A shortcut is a transient read, not the migration end-state.** Leaving migrated data as a shortcut couples
    you to the old platform forever. Shortcut to read -> write Delta -> recon -> drop the shortcut -> decommission.
17. **You cannot shortcut to serverless SQL** (it has no storage) - shortcut the ADLS behind it, one connection
    per container. Read storage for bulk, not the SQL endpoint (which bills compute).
18. **Read Synapse bronze and re-derive** - don't lift its silver/gold transforms. Synapse is a one-time backfill
    source, retired after recon + hypercare.

## Operating model + ways of working
19. **No manual metadata, no manual hacks.** Hand-copying data + hand-creating views to "show a dashboard"
    violated the metadata-driven rule and had to be torn out. Everything via the framework / CI/CD.
20. **No AI footprint; the human owns every apply.** AI prepares locally; the owner reviews, syncs, and runs
    pipelines (and may cancel runs the assistant should not have triggered). Cloud access is the owner's, read-only.
21. **Evidence over claims, every time.** "Done" means a captured run ID + reconciliation result behind an exit
    gate - not an assertion. The phase runbook is proof, not narrative.
22. **No scattered documents, no ambiguity.** Consolidated, numbered, closed rules; IDs issued by mechanism;
    living docs reconciled in the same change. This folder is the antidote to scatter.
23. **Surface blockers as the architect, don't work around them.** When the platform can't run (FTL4 Spark wall,
    no CI minutes, no org access), name the constraint and the decision needed - don't hack past it.
