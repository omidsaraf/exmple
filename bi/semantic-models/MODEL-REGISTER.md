# Semantic Model & Dashboard Register - subject areas, not dataflows

> Maps the DE dataflows (Gold) to the BI **subject-area** models and dashboards. A model is **per
> subject area, few per domain** (ADR-36 §7) and commonly **spans several dataflows** - so this is NOT a
> 1:1 dataflow list. Authoring + onboarding steps: `docs/runbooks/bi-developer-runbook.md`.
> **Status: planned/scaffold.** A live Direct Lake model needs the Gold tables (silver->gold chain) +
> workspace/lakehouse GUIDs in a paid env (F64-gated); the TMDL is authored in Power BI Desktop, never
> hand-written.

## Audiology domain

| Subject-area model | Gold source (dataflows) | Mode | RLS | Dashboards (reports) |
|---|---|---|---|---|
| **AudiologyAppointments** | HEARING_P1 `df_audiology_appointments` (`audiology.v_dim_appointment_current`) [+ device telemetry HEARING_P3 for utilisation] | Direct Lake on `lh_audiology_gold` | `sg-healthent-audiology-read` (+ clinic-scoped) | **Appointment Volume & Utilisation** |
| **AudiologyContacts** | HEARING_P2 `df_dynamics_contact` (`audiology.v_dim_contact_current` - masked PII) | Direct Lake on `lh_audiology_gold` (MASKED columns only) | `sg-healthent-audiology-read`; clinic-scoped role demo | **Contactable Patients** (masked) |

## Other domains (clinical / finance / operations / hr / dynamics)

Populated as their dataflows land. Same rule: group the domain's Gold into a few certified subject-area
models; reports bind to them; one App per domain.

## How to read this

- **Dataflows -> models is many-to-few:** several dags' Gold dims/facts roll up into one subject-area
  model. Do not create a model per `dag_uid`.
- **Dashboards bind to a model**, not to a dataflow. A dashboard is per analytical question / persona.
- **Refresh** = Direct Lake reframe triggered when the model's Gold dependencies are loaded AND
  reconciled (`bi-operating-model §6`).
