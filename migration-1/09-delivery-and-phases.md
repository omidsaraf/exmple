# 09 - Delivery and phases

How execution is tracked: the master delivery plan (the spine in 01 section 4), the per-phase documents, and the
per-phase DSD template. One consistent shape per phase; nothing scattered.

## 1. The delivery model
- **Spine:** 01 section 4 (the phase table with entry/exit gates) + section 8 (the status table = authoritative actuals).
- **Per phase:** four governance docs + one DSD, produced from the templates below. A phase is "done" only when
  its exit gate is evidenced, the four docs are accepted, the status table is updated, and risk/FinOps roll-ups
  reflect it. Generated artifacts (seeds/views/DDL) are never hand-written; the manifest is the truth (03).
- **At execution** each phase gets a folder `phases/phase-NN/` holding: `dsd.md`, `implementation.md`,
  `finops.md`, `risk.md`, `runbook.md`, `checklist.md`. Generate these from the templates; keep them in sync with
  the manifest/ADRs in the same change (living docs).

## 2. The four governance docs (per phase)
1. **implementation.md** - opens with a **Solution Design & HLA** section (system-context diagram, ownership
   boundaries, data-flow views, component design), then numbered, executable build steps with exact
   commands/REST/SQL, the repo each artifact lands in, and a verification after each step.
2. **finops.md** - CU/capacity impact, run-cost estimate/delta + post-actuals, optimisation actions.
3. **risk.md** - phase risks: severity, owner, mitigation, "closes when" trigger.
4. **runbook.md** - the phase completion record (Implementation-Plan format): about/audience -> change details ->
   objects to deploy -> ordered deployment steps with per-step verification -> post-implementation sanity with
   captured output -> **validation evidence (proof, not claims) for every exit criterion** -> Definition of Done
   -> decisions/risk/FinOps actuals -> rollback (code+config+data+state, rehearsed) -> approvals -> escalation ->
   follow-ups + handoff. This is what an operator who was not in the room uses to rebuild or roll back the phase.

## 3. Per-phase DSD template (the tracking cover)
> Copy to `phases/phase-NN/dsd.md`. Link to canonical artifacts; never paste large code/DDL here.

```
# Phase {NN} - {NAME} | Detailed Solution Design (DSD)
Owner: _  Status: {Not started|In progress|Done}  Last updated: {date}

1. Summary            objective; scope in/out; why now
2. Gates              entry gate (start when) · exit gate (done when - ties to DoD)
3. Solution Design & HLA   system context · ownership · data flows · components (link implementation.md)
4. Timeline & Gantt   this phase's task Gantt; rolls up to the program timeline
5. Dependencies       what this needs, from whom, status
6. Step-by-step       executable steps (deep version in implementation.md)
7. Deliverables       artifact -> repo/path -> produced by
8. RACI               responsible / accountable / consulted / informed
9. Risks              link risk.md; rolls up to the program risk register
10. FinOps            link finops.md; estimate + post-actuals
11. To-do             tracked checklist
12. Do / Don't        practices + anti-patterns + recommendations
13. Validation & DoD  proof (captured output) per exit criterion + the program DoD checklist
14. Decisions / ADRs  link 08
15. Rollback          code · config · data · state; rehearsed?
16. Change-control    per 06 operating model: AI prepares local, owner reviews + syncs + runs; no AI footprint
17. Sign-offs         role / name / date
18. Status tracker    % complete · current step · blocked on · next action
19. Follow-ups        carry-overs; lessons
20. Links             the four docs + 01 + 08 (canonical; no duplication)
```

## 4. Definition of Done (program-wide, checkable per phase)
- [ ] Code in the correct repo, peer-reviewed, merged via the branch strategy
- [ ] Unit tests pass locally; CI/CD passes (lint, test, deploy) in Dev before promotion
- [ ] Data quality checks in place; monitoring/alerting configured
- [ ] The four governance docs + the DSD produced and accepted
- [ ] ADR logged + status table/Gantt updated; risk/FinOps roll-ups reflected
- [ ] Cost within budget; security review passed (no secrets, least privilege, PHI handled)
- [ ] Non-prod data synthetic/de-identified; rebuild-from-repo dry-run verified (infra-bearing phases)
- [ ] Business/clinical sign-off for Gold/serving changes
- [ ] Exit gate evidenced (proof, not claims)

## 5. Anti-drift rule
The gameplan (01), every topic doc (02-08), every phase doc, and this delivery plan must stay mutually
consistent. When one changes, reconcile the others in the same change. If two documents disagree, fix it - do not
leave the contradiction. Depth honesty: built phases carry real commands/evidence; unbuilt phases carry the
authoritative ordered steps + DoD and are marked "deepen at build" - never fabricate code for an unbuilt phase.
