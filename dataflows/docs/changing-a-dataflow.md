# Changing a Dataflow - add, modify, remove (the change-lifecycle)

> Your `manifest.yml` is the **declarative desired state** of the dataflow. To change anything, edit the
> manifest, regenerate, and open one PR. Add and modify converge automatically (MERGE). Remove needs one
> opt-in flag. Nothing here ever drops a physical table or its data.

## The loop (same for every change)

```bash
# 1. edit metadata/<project_code>/manifest.yml   (the ONLY file you author)
# 2. (optional) preview the seeds locally - output is gitignored, NOT committed
python framework/tools/scaffold/gen_seeds.py --project-dir metadata/<project_code>
# 3. commit manifest.yml ONLY (+ any DDL/notebook changes), open ONE PR. Seeds render at deploy time
#    from the manifest (reusable platform generator); the manifest validate gate checks your edit.
# 4. after merge: dataflows-build-deploy (project_code + env) then dataflows-run
```

## What each change does

| Change | How | What happens |
|---|---|---|
| **Add a table** | add an object under a layer's `jobs[].objects` | MERGE inserts the `ingestion_object` + columns (+ procs/dq). Born **disabled**; enable after the connectivity suite is green for the env |
| **Add a column** | add a line under that object's `columns` | MERGE inserts the `ingestion_column` |
| **Add a job / proc / param** | add it under the layer | MERGE inserts it |
| **Add a whole layer** | add `silver:`/`gold:` (and the layer to `layers:`) + run `new_dataflow` once to create the folders, or add the folders | MERGE inserts the new layer's batch + jobs + procs |
| **Modify anything** | edit the value in the manifest | MERGE **updates** the row in place (convergent - the manifest always wins) |
| **Remove a table / dim** | delete the object from the manifest + set `prune: true` | its procs/jobs are pruned **and the `ingestion_object` is DISABLED** (`is_enabled=0`) so it stops ingesting. The Delta table + history are **kept**, never dropped |
| **Remove a job / proc / param** | delete it + `prune: true` | the orphaned `proc_param`/`proc`/`job` rows are deleted (FK-safe order) |
| **Remove a whole layer** | delete the `silver:`/`gold:` block + `prune: true` | the layer's batch + its jobs/procs are pruned; the layer's objects are disabled |

## Safety rules (why removal is safe)

- **Never drops data.** Removing a table from the manifest **disables** its `ingestion_object` and prunes its
  orchestration rows; the physical Delta table and its run history are retained (CLAUDE.md 3.8, "never DROP -
  rename + archive"). To physically remove data you use the deliberate FK-safe hard-delete helper + archive,
  outside the normal change loop.
- **`prune: true` is opt-in.** Add/modify never delete anything. Only `prune: true` removes rows the manifest
  no longer declares - so an accidental omission cannot silently drop config unless you explicitly opted in.
- **The manifest is authoritative.** After a change, the control DB is made to match the manifest for this dag.
  Edit the manifest, never the control DB or the generated SQL by hand (the drift gate enforces this).
- **One project per PR** - a change to your project cannot touch another project's config (isolation guard).

## Known limits (being closed by the generic loader, ADR-50 R7)

- Today, removing a **table/dim** correctly **disables** the object (it stops running) and prunes its
  orchestration, but the now-orphaned `ingestion_column` / `dq_rule` rows linger (harmless - nothing executes
  them). The R7 declarative loader will fully reconcile these too (delete orphan columns + dq rules), so the
  control DB matches the manifest exactly after every change.
- Until R7, run removals with `prune: true` and the disable + orchestration prune above cover the functional
  case (the removed thing stops running).
