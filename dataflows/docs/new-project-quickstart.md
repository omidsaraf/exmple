# Starting a New Dataflow Project - Quickstart (written for your first day)

> Onboarding a flow is now **one local PR** (ADR-50 R1/R3). You scaffold and generate seeds on your
> machine, commit everything together, open one PR, merge, then deploy and run. No CI scaffold round-trip,
> no second PR for seeds, no shared register to fight over. Reference docs for depth:
> `de-onboarding-runbook.md` (process + anti-patterns), `metadata-cookbook.md` (every seed value
> explained), `../README.md` (repo rules).

## 0. What you need before starting (once)

- The two repos cloned locally: `healthent-fabric-dataflows` (your work) and `healthent-fabric-platform`
  (the tools). Python 3.11 (stdlib only - no installs for scaffolding).
- Access to the ADO project **Fabric** (you're in the *HealthEnt Data Engineers* group).

## 1. Decide three things (the only design decisions up front)

| Decision | How to choose | Example |
|---|---|---|
| **dag_uid** | `df_{domain}_{entity}`, lowercase snake_case, the runtime key - stable forever | `df_audiology_devices` |
| **project_code** | your STABLE EXTERNAL KEY: `HEARING_P{n}` (project convention) or a delivery-system id (Jira/ADO Boards, e.g. `GDDDCI629`). You supply it; it is the folder name everywhere | `HEARING_P4` |
| **kind / layers** | `ingestion` (source -> bronze, NO code) · `transformation` (silver/gold notebooks) · `extraction` (outbound). Layers = where you have artifacts | `mixed` / `bronze,silver,gold` |

`dag_uid` and `project_code` cannot be renamed after first deploy (they key the runtime and the folders).

## 2. Scaffold + generate seeds locally (one command each)

From `healthent-fabric-platform/framework/tools/scaffold/`, pointing `--root` at your dataflows clone:

```bash
# a) scaffold the folders + manifest.yml (you supply the stable key)
python new_dataflow.py --root <path>/healthent-fabric-dataflows \
    --dag-uid df_audiology_devices --project-code HEARING_P4 \
    --kind mixed --layers bronze,silver,gold

# b) edit metadata/HEARING_P4/manifest.yml  (the ONLY file you author by hand - cookbook)

# c) (OPTIONAL local preview) render the seeds to eyeball them - output is gitignored, NEVER committed.
#    Seeds are rendered at DEPLOY time by the reusable platform generator; you never commit seed SQL.
python gen_seeds.py --project-dir <path>/healthent-fabric-dataflows/metadata/HEARING_P4
```

What you get: `{layer}/DDL/HEARING_P4/`, `{layer}/Notebook/HEARING_P4/`, `metadata/HEARING_P4/manifest.yml`,
and (for transform flows) a notebook named to convention (`SlvrAudiologyDevicesHearingP4.py`). Any
`metadata/HEARING_P4/generated/` from the optional preview is **gitignored - do not commit it** (ADR-50 R7:
seeds render at deploy). `metadata/project-register.md` is a **generated index** - `python new_dataflow.py
--reindex --root <dataflows>` (the scaffold step already does this).

## 3. Commit everything in ONE PR (your actual work)

1. `metadata/HEARING_P4/manifest.yml` -> **owner** (your UPN) + **description** (both required to merge),
   plus the ingestion/transform detail per `metadata-cookbook.md`.
2. Transformation only: copy a starting point from `templates/notebooks/` into your `Notebook/HEARING_P4/`
   file; write your logic in `build()`; pick a `write_mode` (default `merge`).
3. Commit **manifest.yml + DDL + notebooks** (NOT seeds - they are not committed), push one feature branch,
   open one PR. `dataflows-pr-validation` runs the **manifest validate + normalize gate** (enums / required /
   watermark / case), the **no-committed-seeds gate**, SQL parse, scaffolder self-test, isolation/boundary and
   typography gates. Get a review, merge to `dev`. The seeds are rendered + applied at deploy time by
   `dataflows-build-deploy` from your manifest (the reusable platform generator).

## 4. Deploy and run (after merge)

| Step | Pipeline | Key you give it |
|---|---|---|
| seed metadata -> control DB, then deploy DDL/notebooks | `dataflows-delivery` (MODE=`deploy`) | **project_code** + env |
| run it (+ DQ gate) | `dataflows-delivery` (MODE=`full` or `custom` Stage 5) | **project_code** + env |

> ADR-50 R2 (in progress) splits these into `dataflows-build-deploy` and `dataflows-run`. Until then use
> `dataflows-delivery` modes. Ingestion objects are **born disabled**; enable with the one-line convergent
> UPDATE after the connectivity suite is green for the env.

## 5. Check your run

`dataflows-delivery` Stage 5 with `wait_for_completion=true` polls to the end and asserts the control-plane
telemetry. Or query the control DB: `log.batch_run` / `log.ingestion_run` / `log.run_event`. Failures notify
per the batch's `notify_group`.

## FAQ (the questions everyone asks in week one)

- **Where does my project_code come from?** You supply it (ADR-50 R3) - `HEARING_P{n}` or a delivery-system id.
  It is NOT issued from a register. Uniqueness is enforced by the filesystem: if the folder exists the scaffolder
  refuses (no-clobber). So two engineers on two branches never collide on a shared file.
- **Two of us scaffolded at the same time.** Different keys -> different folders -> no conflict. Same key ->
  the second person's no-clobber fails locally before any PR. Pick distinct keys.
- **Can I rename my dag_uid / project_code?** No, not after first deploy (they key the runtime and the folders).
- **Where do I put a second SQL object?** Same `DDL/HEARING_P4/` folder, next band number, named after the object.
- **Do I ever write a pipeline?** No. Never. The generic runners execute every flow from your metadata.
- **Something's broken.** `docs/framework-troubleshooting.md` (docs repo) - then ask in the team channel with
  your `batch_run_id`.
