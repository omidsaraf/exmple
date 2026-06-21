# gold/DDL - one folder per project ({dag_uid}/), banded file numbering

File naming: `NN_{object_name}.sql` - one file per object, named after it,
two-digit band prefix drives deploy order (deterministic sort):

| Band | Contents | Example |
|---|---|---|
| 00 | setup (schema/external sources) | 00_setup.sql |
| 10-19 | dimensions / base tables | 12_dim_patient_scd2.sql |
| 20-29 | facts | 20_fact_appointment.sql |
| 30-39 | views | 30_v_dim_appointment_current.sql |
| 40-49 | procedures | 40_p_refresh_gold.sql |
| 50-69 | security (RLS/grants) - FRAMEWORK-owned, never in dataflows | 50_security_rls.sql |
