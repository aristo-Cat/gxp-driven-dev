---
name: gdd.lifecycle
description: |
  Lifecycle overview + orchestrator. Maps the full V-Model lifecycle for the
  consumer project, shows which templates apply for its `mode` / `gamp_category`
  / `profile`, plots where the project currently is (from `specs/*.md` statuses),
  and lists what remains — left arm (specification) → bottom (build) → right arm
  (qualification) → closeout → operation. Can drive the cascade phase-by-phase
  with a human checkpoint between phases, delegating each step to the matching
  cascade skill. Anti-hallucination: never authors a spec itself except via the
  per-phase skills; never claims a phase complete without the lint/trace gate.
  Use this skill when:
  - The user says "show the lifecycle", "the big picture", or "drive the cascade"
  - Onboarding to a project and needing the full map, not just the next step
  - The user wants "the toolkit drives me" through the phases with checkpoints
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, Task]
---

# `gdd.lifecycle` — V-Model Lifecycle Overview & Orchestrator

You give the **whole-of-lifecycle picture** and (optionally) drive the cascade phase-by-phase with checkpoints. Where `/gdd.next` answers "what is the single next step", **you** answer "what is the full map, where am I on it, and what remains". You orchestrate by delegating each phase to its cascade skill — you do not re-implement them.

## Pre-flight (do this FIRST)

1. **Locate `.gxp-dev.yaml`**: walk up from the cwd. If not found:
   > *"No `.gxp-dev.yaml` manifest. Run `/gdd.init` first."* — and STOP.

2. **Load the manifest**: `mode`, `lifecycle`, `profile`, `gamp_category`, `rigor_level`, `presets.*`, `templates_active`. These select **which arm of the V applies** and which templates are in scope.

3. **Scan `specs/*.md` statuses** (same as `/gdd.next`): build `{DOC-TYPE → status}`; absent = not started. Ignore the derived `RTM.md`.

4. **Resolve `<gdd-path>`** (parent of `skills/`) for the scripts and templates.

## The V-Model map

Render the lifecycle as the V, annotated with this project's status. Left arm = specification (decompose), bottom = build, right arm = qualification (verify upward), then closeout + operation.

```
 LEFT ARM (specify)                                  RIGHT ARM (qualify)
 GXP-ASSESS (concept) ─────────────────────────────► VR  (closeout, §M7)
   │                                                  ▲
 URS (user requirements) ─────────────────────────►  PQ  (fitness for intended use, vs URS)
   │                                                  ▲
 FS (functional spec) ────────────────────────────►  OQ  (functional verification, vs FS)
   │                                                  ▲
 CS (Cat 4) / DS (Cat 5) (configuration/design) ──►  IQ  (install/config verification, vs CS/DS)
                         ╲                          ╱
                          ╲──────  BUILD  ─────────╱
                             (configure / code)

 Cross-cutting, parallel to the left arm:
   RA-INIT (initial RA — sets the GAMP category)  →  RA-DET (FMEA — RPN scales OQ rigor)  →  RTM (derived trace)
```

| V-Model phase | Template(s) | Active when | Produced by |
|---|---|---|---|
| Concept | `GXP-ASSESS`, `VMP` | `profile: pharma` | (manual / future) |
| Planning | `VP`, `SUP-ASSESS`, `RA-INIT` | VP/SUP pharma; RA-INIT always | `RA-INIT` ← `/gdd.ra.from-urs` |
| Specification (left arm) | `URS`, `FS`, `CS`/`DS`, `ADR`, `API-SPEC`, `DBS`, `UC`/`AC` | per mode + category | `/gdd.urs.from-idea`, `/gdd.fs.from-urs`, `/gdd.cs.from-fs` |
| Risk (parallel) | `RA-DET` | RA-INIT flagged it | `/gdd.ra.detail.from-urs-fs` |
| Build (bottom) | (source code) | `mode: develop` / Cat 4 config | (`/gdd.implement-from-specs`, future) |
| Qualification (right arm) | `IQ`, `OQ`, `PQ` (+ `UT/IT/SEC/PERF` plans) | always | `/gdd.tests.from-ra` |
| Cross-cutting | `RTM` | always | `/gdd.trace.validate` (derived) |
| Closeout | `VR`, `RN`, `DEPLOY-RUN` | always | (`/gdd.vr.from-tests`, future) |
| Operation | `PR`, `CC`, `IR`, `CONFIG-BL`, `UAR`, `BRR` | post-validation | (operation-phase, append-only) |
| Retirement | `DECOM-PLAN`, `RETIRE-REPORT` | end-of-life | (future) |

Filter this table to **only `templates_active`** for the actual project. For `mode: hybrid`, render the map twice — once per `hybrid_breakdown` component (vendor side = validate arm, custom side = develop arm).

## Mode / category tailoring (what applies)

- **`mode: validate`** (vendor product): left arm is `URS` + `CS` (Cat 4); the design/build phases are the vendor's, not yours; right arm `IQ/OQ/PQ` verify the vendor product. No `DS`/`ADR`/code.
- **`mode: develop`** (custom): full left arm incl. `DS`/`ADR`/`API-SPEC`/`DBS`, a real build phase, and unit/integration test plans.
- **`mode: hybrid`**: both, split by component.
- **Category scales depth, not the shape**: Cat 1/3 → light right arm; Cat 4 → `CS` + config-baseline IQ; Cat 5 → `DS` + full OQ rigor driven by `RA-DET` RPN.
- **`lifecycle: agile`** maps `URS→UC`, `FS→AC` but keeps the same right-arm qualification.

## Where the project is + what remains

1. **Plot each active template** on the map with its status badge (absent / draft / in-review / approved).
2. **Identify the frontier** — the lowest unmet phase (the same logic as `/gdd.next`, but show the whole remaining list, not just the first step).
3. **List remaining work** in cascade order, each with its producing skill and a one-line gate ("FS — `/gdd.fs.from-urs` — needs RA-INIT category locked").

## Orchestration mode (optional — only if the user asks to "drive" the cascade)

If the user wants the toolkit to drive them phase-by-phase, run this loop. **Checkpoints are mandatory** — never chain phases without human confirmation.

For each unmet phase in cascade order:
1. **Pre-flight**: read the upstream spec(s) and verify status (warn if drafting off an unapproved upstream).
2. **Delegate** to the matching cascade skill (e.g. `/gdd.urs.from-idea`, then `/gdd.ra.from-urs`, then `/gdd.fs.from-urs`, …). You do **not** author the spec yourself — the per-phase skill owns its method and its anti-hallucination rules. You may use `Task` to run an independent phase, but interactive interview phases (URS, RA) run in the foreground with the user.
3. **Gate**: run `python <gdd-path>/skills/_scripts/lint-spec.py specs/<NEW>.md`; for cross-spec coherence run `/gdd.trace.validate`.
4. **Human checkpoint**: summarize what the phase produced (counts, markers, gate verdict) and **pause** — ask the user to review and confirm before the next phase. If rejected, return to the producing skill for revision; do not advance.
5. Continue until closeout (`VR`), then stop and hand to the operation phase.

> Drive sparingly. Most users prefer `/gdd.next` (one step) over full-drive. Offer `/gdd.next` if the user only wants the immediate move.

## Anti-hallucination rules (NON-NEGOTIABLE)

1. **Never author a spec directly.** All authoring goes through the per-phase cascade skill, which carries its own grounding rules. This skill maps and orchestrates only.
2. **Never claim a phase is complete without its gate** (lint passes + traceability green). A produced draft is not a completed phase.
3. **Never skip the human checkpoint** in orchestration mode. Status promotion needs human action.
4. **Respect `templates_active`** — show and drive only the in-scope phases.
5. **Name stub skills as stubs.** If a remaining phase needs a skill not yet operative (DS, VR, implement), say so and give the manual path from `docs/methodology.md` / `docs/project-layout.md`.

## Output

1. **The V-Model map** filtered to this project, with status badges.
2. **Current frontier** + full remaining-work list (cascade order, each with its skill + gate).
3. **Mode/category tailoring note** — which arm applies and why.
4. **Offer**: drive the next phase with checkpoints (orchestration mode), or hand to `/gdd.next` for a single step.

## When to refuse

- `.gxp-dev.yaml` missing → redirect to `/gdd.init` and STOP.
- User asks to drive past a failing gate (lint/trace) → refuse; fix the gate first.
- User asks to set any spec `approved` → refuse; approval is human action outside the toolkit.
