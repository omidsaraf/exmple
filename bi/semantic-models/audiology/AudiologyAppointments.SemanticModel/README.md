# AudiologyAppointments.SemanticModel - placeholder (skeleton)

Subject-area model for Audiology appointment analytics (ADR-36 §7: model per
subject area, never per dataflow). **Not yet authored** - the PBIP/TMDL content
is created in Power BI Desktop (Developer Mode) and committed here; do not
hand-write TMDL.

| Property | Value (planned) |
|---|---|
| Mode | Direct Lake over `lh_audiology_gold` |
| Source contract | `audiology.v_dim_appointment_current` (+ future fact views) - never raw SCD2 tables |
| RLS roles | match `sg-healthent-audiology-*` Entra groups |
| Sensitivity | Highly Confidential (PHI-derived; patient_id pseudonymised) |
| Tests | BPA in `pl-bi-sync` (severity ≥ 2 fails) |
