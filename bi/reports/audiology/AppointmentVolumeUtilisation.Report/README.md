# AppointmentVolumeUtilisation.Report - placeholder (skeleton)

Dashboard for audiology appointment volume & clinic utilisation. **Not yet authored** - the PBIP `.Report`
is built in Power BI Desktop and committed here. Onboarding steps: `docs/runbooks/bi-developer-runbook.md`
§4.

| Property | Value (planned) |
|---|---|
| Bound model | `AudiologyContacts`? **No** -> `AudiologyAppointments` (reports bind to a certified model, never build their own) |
| Measures | live in the MODEL (no report-level measures) |
| T-SQL | none (forbidden in `bi` reports, ADR-37) |
| Access | App `Audiology`, audience `sg-healthent-audiology-read` (consumers see only the App) |
| Data | dev synthetic only (§36) during development |
| Visuals (planned) | appointments by month, by clinic, utilisation %, avg duration, no-show rate |
