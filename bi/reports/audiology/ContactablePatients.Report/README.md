# ContactablePatients.Report - placeholder (skeleton)

Dashboard for audiology contactability (masked). **Not yet authored** - the PBIP `.Report` is built in
Power BI Desktop and committed here. Onboarding steps: `docs/runbooks/bi-developer-runbook.md` §4.

| Property | Value (planned) |
|---|---|
| Bound model | `AudiologyContacts` (masked Gold; RLS by clinic) |
| Measures | in the model (no report-level measures) |
| T-SQL | none (ADR-37) |
| Access | App `Audiology`, audience `sg-healthent-audiology-read`; RLS limits rows to the viewer's clinic |
| Data | dev synthetic only (§36); PII is masked at Gold, never unmasked in the model |
| Visuals (planned) | contactable counts by clinic/channel (masked), consent status, last-contact recency |
