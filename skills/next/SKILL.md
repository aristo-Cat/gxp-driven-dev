---
name: gdd.next
description: |
  Lightweight workflow orchestrator. Reads `.gxp-dev.yaml` + scans the
  statuses of existing `specs/*.md`, determines the project's position in the
  generative cascade, and recommends the single next artifact to produce plus
  the skill that produces it — respecting `mode`, `gamp_category`, and
  `templates_active`. Read-only: does NO authoring itself, only routes. The
  cascade spine is GXP-ASSESS → VP/RA-INIT → URS → FS → RA-DET → CS/DS →
  IQ/OQ/PQ → RTM → VR.
  Use this skill when:
  - The user says "what's next", "where am I", or "what should I do now"
  - After completing any cascade step, to find the next move
  - Returning to a project and needing orientation
allowed-tools: [Read, Bash, Glob, Grep]
---

# `gdd.next` — Workflow Orchestrator (lightweight)

You look at the project state and recommend **one** next move. You are a router, not an author — you do not write specs (that is the cascade skills' job). Output: the next artifact + the skill that produces it + a one-line why.

## Pre-flight (do this FIRST)

1. **Locate `.gxp-dev.yaml`**: walk up from the cwd. If not found:
   > *"No `.gxp-dev.yaml` manifest found. Start with `/gdd.init`."* — and STOP.

2. **Load the manifest** and note: `mode`, `lifecycle`, `profile`, `gamp_category`, `presets.*`, `templates_active`. `templates_active` is your **scope filter** — never recommend a spec that is not active for this project.

3. **Scan `specs/*.md`.** For each present file, read its frontmatter `status` (`draft` / `in-review` / `approved` / `superseded`; test protocols may be `in-execution` / `executed`). Build a map: `{DOC-TYPE → status}`. Missing files are "absent". Ignore the derived `RTM.md`.

## The cascade spine

The canonical generative order (V-Model left arm down, right arm up):

```
GXP-ASSESS  →  VP / RA-INIT  →  URS  →  FS  →  RA-DET  →  CS (Cat 4) / DS (Cat 5)  →  IQ / OQ / PQ  →  RTM  →  VR
```

Each step's producing skill:

| Artifact | Produced by | Active when |
|---|---|---|
| `GXP-ASSESS` | (manual / future skill) | `profile: pharma` and `GXP-ASSESS` in `templates_active` |
| `VP` | (manual / future skill) | `profile: pharma`, GxP-relevant |
| `RA-INIT` | `/gdd.ra.from-urs` | always (runs against the URS, even draft) |
| `URS` | `/gdd.urs.from-idea` | always |
| `FS` | `/gdd.fs.from-urs` | `gamp_category` 4/5 or `mode: develop` |
| `RA-DET` | `/gdd.ra.detail.from-urs-fs` | when RA-INIT flagged `detailed_ra_required` |
| `CS` | `/gdd.cs.from-fs` | **Cat 4 only** |
| `DS` | (`/gdd.ds.from-fs`, when available) | **Cat 5 / `mode: develop`** |
| `IQ` / `OQ` / `PQ` | `/gdd.tests.from-ra` | always |
| `RTM` | `/gdd.trace.validate` (derived) | always |
| `VR` | (`/gdd.vr.from-tests`, when available) | always (closeout) |

## Decision logic (apply in order; stop at the first match)

Evaluate top-down; recommend the **first** unmet step that is in `templates_active`:

1. **No `URS.md`** → recommend `/gdd.urs.from-idea`. *("No URS yet — start the requirements interview.")*
   - (If `profile: pharma` and `GXP-ASSESS`/`VP` are active but absent, mention them as the true root, but the URS interview can begin in parallel.)
2. **`URS.md` is `draft`** → recommend `/gdd.lint.spec specs/URS.md` first; if it has clarification markers, resolve them before promotion. *("URS is draft — lint and resolve markers before promoting.")*
3. **`URS.md` present (any status) and no `RA-INIT.md`** → recommend `/gdd.ra.from-urs`. *("URS exists — run the Initial Risk Assessment; it decides the GAMP category that scales everything.")*
   - RA-INIT must reach `approved` **before** the URS (the URS inherits `gamp_category` from it).
4. **`RA-INIT.md` present, no `FS.md`** (and FS is active) → recommend `/gdd.fs.from-urs`. *("Category is set — draft the Functional Spec.")*
5. **`FS.md` present, RA-INIT flagged `detailed_ra_required: true`, no `RA-DET.md`** → recommend `/gdd.ra.detail.from-urs-fs`. *("High-risk functions need the detailed FMEA before tests.")*
6. **`FS.md` present, `gamp_category == 4`, no `CS.md`** → recommend `/gdd.cs.from-fs`. *("Cat 4 — document the configuration before IQ/OQ.")*
   - **`gamp_category == 5`** with no `DS.md` → recommend the DS skill (note: stub until available).
7. **FS (+ CS/DS) + RA-DET present, no `IQ`/`OQ`/`PQ`** → recommend `/gdd.tests.from-ra`. *("Specs are in place — draft the IQ/OQ/PQ protocols.")*
8. **All cascade specs present** → recommend `/gdd.trace.validate` to derive the RTM and assert zero dangling refs. *("Run traceability validation before closeout.")*
9. **Traceability passes, all specs `approved`** → recommend `/gdd.vr.from-tests` (Validation Report, closeout). *("Close the V-Model with the Validation Report.")*
10. **VR approved** → the project is validated; recommend moving to the operation phase (Periodic Review `PR`, change control `CC`, incidents `IR`).

### Status nuances

- A spec at `in-review`/`approved` unblocks its downstream the same as "present" for routing, but **flag** when a downstream is being drafted off an *unapproved* upstream ("FS is being drafted off a `draft` URS — fine to start, but approve upstream before promoting downstream").
- If a `[NEEDS CLARIFICATION: …]`-heavy spec is blocking, recommend `/gdd.lint.spec` + marker resolution as the real next move, even if the next *artifact* technically exists.

## Anti-hallucination rules (NON-NEGOTIABLE)

1. **Recommend only skills that exist** for this toolkit version. If the natural next step needs a skill that is still a stub (e.g. the DS skill, the VR skill), say so explicitly and offer the manual path from `docs/methodology.md`.
2. **Respect `templates_active`.** Never recommend producing a spec that the manifest does not activate.
3. **Do no authoring.** This skill routes; it never writes a spec. If the user wants the artifact built, hand off to the producing skill.
4. **Read real statuses.** Base the recommendation on the actual frontmatter `status` values you scanned — do not assume.

## Output

Print, concisely:
1. **Current position** — one line ("Cascade position: URS approved, RA-INIT draft, FS absent").
2. **Status table** — `DOC-TYPE → status` for each active template (absent = not started).
3. **The single next move** — the artifact + the exact skill command + the one-line why.
4. **Blockers**, if any — unresolved markers / unapproved upstream that should be cleared first.

## When to refuse

- `.gxp-dev.yaml` missing → redirect to `/gdd.init` and STOP.
- User asks `gdd.next` to *produce* the spec → clarify that this skill only routes; offer to invoke the producing skill instead.
