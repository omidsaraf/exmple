# 11 - How to run sessions (start, update, continue)

The operator's cheat-sheet for driving the work across sessions: how to START, how to ask for an UPDATE / WRAP-UP
before you close, and how to CONTINUE later when you open again. Copy-paste the prompts. This keeps every session
consistent with the operating model (06) and the phase gates (01/09).

## 0. The three moments
| Moment | You say | What it does |
|---|---|---|
| **START** | "Read 00-10, confirm where we are, then start <phase/task>" | loads context, confirms the resume point, begins behind the right gate |
| **UPDATE / WRAP** | "Run the session-close sequence" | produces the four docs + DSD, honest exit/DoD check, status/log/ADR updates, the handoff, the file list |
| **CONTINUE** | "Read the handoff and continue" | resumes exactly from the last handoff's Next step |

## 1. START a session (or a phase)
Paste this at the top of a new session:
```
Read migration-1/00-START-HERE.md, 01-gameplan.md, and the SESSION STATE handoff (in 01 section 8 or the
local handoff file). Confirm: current phase, last step done, next step, and any open blockers - in your own
words, no assumptions. Then start <PHASE n / the named task>. Operate per 06: prepare changes locally, I
review + sync + run the pipelines; no manual metadata (all via CI/CD); no AI footprint; cloud access is mine
and read-only. Ask one focused question only if naming/grain/SLA/security is genuinely ambiguous.
```
To start a specific phase: add "Begin Phase N at its entry gate (01 section 4); produce its DSD from the 09
template first, then the build steps." For Discovery (Phase 1): "I have granted read-only org Synapse access;
run the discovery tooling, metadata/volumetrics only, no PHI."

## 2. Ask for an UPDATE / WRAP before you close
Paste this when you are ready to stop:
```
Run the full session-close sequence:
1. Produce/update this phase's four docs (implementation, finops, risk, runbook) - the runbook to the
   "fully documented" bar (evidence + IDs, not claims).
2. Check what we actually did against the phase EXIT criteria (01 section 4) and the Definition of Done
   (09 section 4). Tell me honestly what is met and what is open - mark nothing done that is not evidenced.
3. Update the status table (01 section 8), the session log, the timeline, and the ADR index.
4. Output the Session Handoff block and write it into the SESSION STATE / handoff file so I can resume.
5. List every file you created or changed this session, with its repo and path.
Push nothing I have not reviewed; if anything needs a cloud change, give me the numbered steps to run.
```
Quick mid-session check (not a full close):
```
Give me a status: what is done + evidenced, what is in flight, what is blocked (and on whom), and the
exact next action. No new work - just the honest picture.
```

## 3. CONTINUE later (when you open again)
Paste this:
```
Read migration-1/00-START-HERE.md + 01-gameplan.md + the latest Session Handoff. Tell me the resume point
(phase, last step, next step, blockers) before doing anything. Then continue from "Next step" - unless a
blocker listed there is mine to clear, in which case tell me exactly what you need from me first.
```
If the handoff is missing or stale: "The handoff is missing - ask me for the current phase, the last step done,
and any open blockers, then proceed."

## 4. The Session Handoff block (the continuity record - always produced at close)
```
SESSION HANDOFF
Date       : YYYY-MM-DD
Phase      : <number + name; OPEN/CLOSED>
Last step  : <exact step completed, with evidence/IDs>
Next step  : <exact step to start next time>
Decisions  : <new ADRs or locked decisions>
Blockers   : <item + who owns it>
HEADs      : <repo: commit per repo>
Start next : <one-line instruction to resume>
```
Write this into the SESSION STATE section of the local handoff file (gitignored) AND the session log. The handoff
is what makes "continue later" exact rather than a guess.

## 5. Standing rules every session (so you never have to repeat them)
- I **prepare locally; you review + sync + run** pipelines. I do not trigger CI runs; you control + cancel them.
- **No manual metadata** - registration is via CI/CD. **No AI footprint** - no AI trailer/identity/markers.
- **Evidence over claims** - "done" means a run ID + reconciliation behind an exit gate.
- **One focused question** only when naming/grain/SLA/security is genuinely ambiguous; otherwise proceed with the
  closed rules in 02-08 and tell you what I chose.
- **Blockers are surfaced, not worked around** (CI minutes, F64, org access, Spark capacity) - I name the
  constraint and the decision you need.
- **CI needs agent capacity first** (06 section 6) - arrange a self-hosted agent or the parallelism grant before
  expecting pipelines to run.
