# AudiologyContacts.SemanticModel - placeholder (skeleton)

Subject-area model for audiology contactability / CRM analytics (ADR-36 §7: per subject area, never per
dataflow). **Not yet authored** - PBIP/TMDL is created in Power BI Desktop (Developer Mode) and committed
here; do not hand-write TMDL. Onboarding steps: `docs/runbooks/bi-developer-runbook.md` (approach 3A/3B).

| Property | Value (planned) |
|---|---|
| Mode | Direct Lake over `lh_audiology_gold` |
| Source contract | `audiology.v_dim_contact_current` - the **masked** consumption view (PII redacted via DDM); never the unmasked tech view, never raw SCD2 |
| Columns | masked set only (name/email/phone/DOB/postcode are redacted at Gold, ADR-19/§28) - the model never holds unmasked PII |
| RLS roles | match `sg-healthent-audiology-*`; clinic-scoped role demo (bridge + `USERPRINCIPALNAME()`) |
| Sensitivity | Highly Confidential (PHI/PII-derived) |
| Tests | BPA in `pl-bi-sync` (severity >= 2 fails); CI lint: no unmasked/PHI column |
| Source dataflow | HEARING_P2 `df_dynamics_contact` (CRM/Dataverse `contact`) |
