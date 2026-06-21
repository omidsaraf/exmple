# Semantic-model security (RLS / OLS) - certified Direct Lake models

- **Status:** current (ADR-51 dual serving path; ADR-33 column security; ADR-52 least privilege).
- **Audience:** BI developers building certified semantic models on Gold.

Certified, performance-critical dashboards use **Direct Lake over the `lh_gold` tables** (fastest: in-memory,
no refresh). Direct Lake **bypasses the Warehouse `[domain]_VIEW` security**, so the model **must** carry its
own security. Ad-hoc SQL / extracts use the Warehouse views instead (secured there). Both paths key to the
**same Entra groups**, so results are identical.

> Security is enforced in the **model** (here) or the **view** (warehouse) - **never** at the dashboard. Hiding
> visuals is not security; the underlying data stays reachable.

## What every certified model must have

| Control | How (in the .pbip / TMDL model) | Maps to |
|---|---|---|
| **RLS** (rows) | a **role** per audience with a DAX table filter; assign the role to the Entra group | `sg-healthent-{domain}-read` etc. |
| **OLS** (columns/tables) | hide PHI columns/tables from non-privileged roles (model equivalent of the consumption view omitting PHI) | ADR-33 |
| **OneLake roles** | the model identity reads only the permitted `lh_gold` tables | ADR-52 |
| **Masking** | bake into the **Gold build** (masked column) - Direct Lake cannot use T-SQL DDM views | ADR-51 §3 |

## RLS role example (TMDL)

```tmdl
role audiology_read
    modelPermission: read
    tablePermission dim_clinic = "[clinic_id] IN (
        SELECTCOLUMNS( FILTER( clinic_access_map, clinic_access_map[principal] = USERPRINCIPALNAME() ),
                       clinic_access_map[clinic_id] ) )"
    // assign this role to the Entra group sg-healthent-audiology-read (in the workspace/app)
```

- Broad readers (e.g. `sg-healthent-audiology-read`): a role with no row filter, or a wide filter.
- Scoped readers: a role whose DAX filters by a mapping table (`clinic_access_map`) on `USERPRINCIPALNAME()`.
- Privileged/unmasked: a separate role, assigned to `sg-healthent-{domain}-eng`/`-admin` behind **PIM/JIT**.

## OLS example

Hide PHI columns from the read role (TMDL `columnPermission ... = none`) so non-privileged users cannot even
see them in the field list - mirroring the Warehouse `[domain]_VIEW` that omits PHI.

## Rules

- One semantic model **per business subject area**, certified (ADR-36 §7) - never per dataflow.
- Roles map to **Entra groups**, never individuals; tech/unmasked behind PIM/JIT (§7).
- The final Direct Lake binding + role-to-group assignment is completed in Power BI Desktop / the workspace at
  deploy time (env-specific); the model + roles are version-controlled in this repo (`.pbip`/TMDL).
- Warehouse-path equivalent (RLS policy + CLS/DDM on `[domain]_VIEW`/`_TECH_VIEW`):
  `dataflows/templates/gold_security_TEMPLATE.sql` + `docs/security/cls-rls-design.md`.
