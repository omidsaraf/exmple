# 05 - FinOps

How capacity is sized, how and when to ask for it, the whole bill (not just CU), and the cost levers. The
Phase-P deliverable is a defensible F-SKU recommendation that gates all paid spend.

## 1. Principles
- **Trial first, then size from telemetry** - validate on the free trial, capture CU under load, then commit paid
  F-SKUs. Never size from guesses.
- **Pause non-prod** when idle (preserves items + OneLake data, stops compute billing). Destroy/rebuild only for
  periodic IaC-drift validation.
- **Cost the whole bill, not just CU** (below).
- **Reserved capacity for Prod only after the F-SKU is validated** (PAYG first, ~30 days, then Reserved).

## 2. Sizing - the estimator (not a peak/average calculator)
Fabric throttles on an accumulated **future-overage backlog**, not instantaneous peak: when demand exceeds the
SKU rate, overage carries forward and the throttle STAGE (interactive delay -> interactive rejection ->
background rejection) depends on how long it would take to burn the backlog down. Interactive and background
smooth over different windows and reject independently. So a `capacity_estimator` must **replay the demand series
through a burndown simulation per candidate SKU** and report **time-above-throttle-threshold per stage** - not a
single averaged number. It can run from real telemetry (Capacity Metrics CSV) OR a transparent workload model
(object counts x runs/day x est CU per run x concurrency) when a representative load test is not yet possible.

Outputs: smoothed sustained/peak profile (interactive vs background split), time-above-threshold per SKU, the
smallest F-SKU with ~25-30% headroom that avoids rejection, PAYG vs Reserved (1yr/3yr), the F64 viewer-licensing
note, and a budget-ceiling gate (non-zero exit + escalate if breached).

## 3. The F64 question = licensing, not compute (the decisive point)
F64+ grants free Power BI read-only viewer consumption; below F64 every consumer needs Pro/PPU. If Prod has many
report viewers, **F64 can be cheaper than F8+Pro even when compute fits on F8**. Size compute from the model, then
if viewer count is above the breakeven, round Prod up to F64 for the licensing saving. State the viewer number.

## 4. Per-environment shape (interim; confirm by load test)
| Env | SKU | Idle strategy |
|---|---|---|
| Dev | F2-F4 | pause when idle |
| Test | F4 | pause post-run; weekly destroy for drift |
| UAT | F8 | pause between cycles |
| Prod | F32-F64 (F64 if viewer count > breakeven) | always on; scale down off-hours |
| DR | F32 (on-demand) | standby |

## 5. The whole bill (track in the cost model, not only CU)
Control-plane Azure SQL DBs (per env), Key Vaults (domains x envs), Private Endpoints / networking, Purview,
storage + egress, Log Analytics, Terraform state storage, and **ADO Microsoft-hosted pipeline minutes** (a real
monthly quota - the free tier is small; options: a self-hosted agent ($0 + a machine), the free parallelism grant
($0, by request), or paid jobs ~A$40/mo each). CU is the big rock, not the whole bill.

## 6. How and WHEN to ask for capacity (the procurement playbook)
Ask in **stages tied to evidence**, never one big upfront commit. Fabric capacity provisions in minutes, so the
gate is **budget approval, not lead time**; Reserved is a 1yr/3yr commitment - buy it only after the PAYG run-rate
is observed.
| When | Ask for | Form |
|---|---|---|
| Now (Phase P) | $0; agree the budget ceiling | a number, not a purchase |
| Dev/Test build (Phase 4) | Dev F2-F4 + Test F4 | PAYG, paused when idle |
| Before the load test | F64 PAYG for ~a few hours (~A$70) | PAYG, delete after |
| Prod cutover (post load test) | Prod F32/F64 at the confirmed run-rate | PAYG first, then Reserved 1yr after ~30 days stable |
| UAT cycles | F8 PAYG during cycles | PAYG, paused between |

**Sizing contingency:** agree the escalation path BEFORE measuring - if the recommended SKU (with headroom)
exceeds the funded envelope, or F64 cannot sustain the representative slice, stop and escalate to CTO + DE Manager
before downstream business-casing proceeds on an assumed number. Record the ceiling so the gate is unambiguous.

## 7. Per-phase FinOps note
Every phase produces a `finops.md`: expected CU/capacity impact, run-cost estimate/delta, and optimisation
actions; rolled up into the program cost model. Weekly cost review vs the CU budget (CU > 80% = P3, > 95% = P2).
