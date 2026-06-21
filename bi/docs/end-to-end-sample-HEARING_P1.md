# End-to-end sample - HEARING_P1 through semantic model + dashboard

> **Repo:** bi - **Owner:** Senior DE / BI - **Status:** SPEC (data path proven; BI artifacts authored from this
> spec; live deploy is capacity/Direct-Lake-gated). This closes the loop: source -> Bronze -> Silver -> Gold
> (metadata framework) -> **semantic model -> report** (this repo).

## 1. Is the metadata framework "ready" for end-to-end incl. semantic + dashboard?

**Yes for the data, by design-separate for BI.** Two different planes:

| Plane | Driven by | Ready? |
|---|---|---|
| Source -> Bronze -> Silver -> Gold | the **metadata framework** (`meta.*` config + the wheel/runner) | READY and PROVEN (HEARING_P1 ran green end-to-end: ingest -> silver -> scd2 -> recon, `log.batch_run` 19) |
| Gold -> **semantic model -> report/dashboard** | the **BI repo** (PBIP), NOT metadata-driven | Deliberately separate (ADR-36 section 7 / operating rules section 24): semantic models are **per business subject area, few per domain, certified** - never per dataflow. |

So the framework does NOT generate semantic models or reports, and that is correct: a `dag_uid` is a delivery
unit, not a serving unit. The BI layer consumes Gold via **Direct Lake** and is deployed by **Fabric Deployment
Pipelines / Git**, capacity-gated (Direct Lake needs the capacity + a populated `lh_gold`).

## 2. What this sample delivers (the complete chain for HEARING_P1)

```
dbo.appointment / dbo.clinic (source)
   -> [metadata framework] lh_bronze.audiology.{appointment,clinic}
   -> [metadata framework] lh_silver.appointments.{appointment,clinic}
   -> [metadata framework] lh_gold.audiology.{dim_appointment, dim_clinic}   (SCD2, PHI masked)
   -> [BI repo] AudiologyAppointments.SemanticModel  (Direct Lake on lh_gold)
   -> [BI repo] AppointmentVolumeUtilisation.Report   (dashboard)
```

## 3. Semantic model - AudiologyAppointments (Direct Lake)

- **Mode:** Direct Lake over `lh_gold` (SQL analytics endpoint), schema = business domain `audiology`.
- **Tables (import the CURRENT rows only - `is_current = 1` view, never raw SCD2 history into the model):**
  - `dim_appointment` (grain: appointment) - `appointment_id` (key, hidden), `clinic_id`, `duration_minutes`,
    `patient_id` (ALREADY pseudonymised at Gold by the framework mask - the model never sees raw PHI).
  - `dim_clinic` (grain: clinic) - `clinic_id` (key), `clinic_name`.
  - A `Date` table (mark as date table) for time intelligence.
- **Relationships:** `dim_appointment[clinic_id] -> dim_clinic[clinic_id]` (single, many-to-one);
  `dim_appointment[appointment_date] -> Date[date]`.
- **Measures (DAX):**
  - `Appointments = COUNTROWS(dim_appointment)`
  - `Avg Duration (min) = AVERAGE(dim_appointment[duration_minutes])`
  - `Utilisation % = DIVIDE([Appointments], [Capacity])` (Capacity from clinic slots when modelled)
  - `Appointments MoM % = DIVIDE([Appointments] - CALCULATE([Appointments], DATEADD(Date[date],-1,MONTH)), ...)`
- **RLS:** role `audiology-read` filtered to the user's clinic(s); roles MUST match the Entra groups
  (`sg-healthent-audiology-read`) - operating rules section 24. No patient-level PII in any visual.
- **Endorsement:** certify after review (per-subject-area, certified).

## 4. Report - AppointmentVolumeUtilisation (dashboard)

- Page 1 "Volume": KPI cards (Appointments, Avg Duration), Appointments by month (line), by clinic (bar).
- Page 2 "Utilisation": Utilisation % by clinic (matrix + heat), trend; clinic slicer.
- Bound to the AudiologyAppointments semantic model (Direct Lake). No raw PHI columns on any visual
  (patient_id is pseudonymised at Gold and is not placed on a visual).

## 5. Build + deploy (the exact path)

1. Author the PBIP in this repo: `semantic-models/audiology/AudiologyAppointments.SemanticModel/`
   (TMDL `definition/` + `definition.pbism`) and `reports/audiology/AppointmentVolumeUtilisation.Report/`
   (`definition.pbir` + report definition). PBIP project format, operating rules section 24.
2. Bind the BI workspace (`healthent-bi-pilot`, ws `1d915b00-...`) to the `bi` repo via Fabric Git; sync.
3. Set the Direct Lake connection to the env's `lh_gold` SQL endpoint (env-specific - update post-deploy).
4. Promote Dev -> Test -> UAT -> Prod with **Fabric Deployment Pipelines**; map RLS roles to Entra groups.
5. Refresh is readiness-triggered (Gold loaded AND reconciled) - not on a blind schedule.

## 6. Status / gating (honest)

- **Data path:** READY and proven on the trial (HEARING_P1 chain green).
- **BI artifacts:** authored from this spec (PBIP). **Live render/deploy is capacity-gated** - it needs a
  populated `lh_gold` on a capacity serving Direct Lake (the trial can, once the chain is re-run to populate
  Gold). Full live deploy + certification rides the same Phase-P -> Phase-4 capacity gate (R-19) as the rest.
- This sample is the template for every future subject-area model: **one certified model per subject area**,
  consuming Gold, never generated per dataflow.
