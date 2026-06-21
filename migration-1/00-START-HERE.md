# migration-1 - Synapse to Microsoft Fabric: the distilled migration blueprint

> A clean, self-contained, ordered blueprint for migrating an enterprise Synapse + ADLS estate to Microsoft
> Fabric, written from scratch with everything learned on the previous build folded in. **Consolidated, not
> scattered:** eleven numbered documents, each a complete topic, read top to bottom. No ambiguity - every rule is
> closed (one right way), every phase has an entry gate and an exit gate, every decision has an ADR.

## How to read this (in order)

| # | Document | What it answers |
|---|---|---|
| 00 | **START-HERE** (this) | what this is, the order, how to use it |
| 01 | **gameplan** | the program: principles, locked decisions, the phases (P, 0-18), timeline, exit gates |
| 02 | **architecture** | target platform, medallion + serving, the default ingestion path + the only exceptions, source families, naming |
| 03 | **framework** | the metadata-driven engine: control plane, generic runner, orchestration, the generators (manifest in, everything out), DQ/SCD2/reconciliation |
| 04 | **security** | identity/groups, RLS/CLS/DDM, PHI by layer, the view vs tech_view access model, de-identification/retention/breach |
| 05 | **finops** | capacity sizing (the estimator), how and when to ask for capacity, the whole bill (not just CU), pipeline-minute capacity |
| 06 | **cicd-and-operating-model** | the repos, the pipelines + gates, and the human/AI operating model (no manual metadata, prepare-local then the owner applies, no AI footprint) |
| 07 | **migration-execution** | rationalise (not lift-and-shift), waves, parallel run, the reconciliation gate, the Synapse archival strategy, decommission |
| 08 | **decisions-adr** | the locked architecture decisions, in one indexed document |
| 09 | **delivery-and-phases** | the master delivery plan, the per-phase DSD template, and how each phase is tracked |
| 10 | **lessons-learned** | the hard-won lessons that shaped every rule above |
| 11 | **how-to-run-sessions** | how to ask to START, how to ask for an UPDATE/WRAP before closing, how to CONTINUE later - copy-paste prompts + the handoff block |

## The five things that make this "the best migration", in one breath
1. **Metadata-driven, always.** One generic runner per source family executes any flow from config. Onboarding a
   source is a YAML manifest, never a new pipeline. Pipeline count stays flat as object count scales to thousands.
2. **One default path, a closed list of exceptions.** Everything flows origin source -> Bronze -> Silver -> Gold
   -> serving, through the framework, with the same guarantees. Deviations (shortcuts, mirroring, archival,
   streaming) are a documented, finite list - never ad hoc.
3. **Single source of truth + generators.** The manifest is the truth; seeds, table DDL, and serving views are
   generated from it (and drift-gated). Nothing important is hand-written twice.
4. **Evidence over claims.** Every phase closes on proof (row + SUM/checksum + SCD2 reconciliation, captured run
   IDs), not assertions. A phase is "done" only behind its exit gate + four governance docs + a DSD.
5. **Cost, security, residency, and the operating model are first-class** - sized from telemetry, least-privilege
   by default, data stays in-region, and changes go through CI/CD with the human owning every apply.

## How to use this blueprint
- Start at **01-gameplan**; build phase by phase behind each exit gate.
- Each phase produces its four governance docs + a DSD from the **09** template; track status in **01 section 8**.
- When a decision is made, record it in **08**; when a rule is set, it lives in **02-07** (one place, closed).
- This folder is the *design*; the running platform is delivered across the repos described in **06**.
