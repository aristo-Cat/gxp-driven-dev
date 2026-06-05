---
id: ADR-002
title: Durable vs ephemeral artifacts — lifecycle classification
status: accepted
decision_date: 2026-05-31
proposed_date: 2026-05-29
deciders:
  - project-owner
relates_to:
  - docs/inspirations.md  # Framework 5 (bm-prd-creator), "What we reject"
  - docs/project-layout.md
tags:
  - adr
  - artifact-lifecycle
  - architecture
---

# ADR-002 — Durable vs ephemeral artifacts: lifecycle classification

> **Status: ACCEPTED (2026-05-31).** Decision: **Option C** — adopt a `lifecycle: durable | ephemeral` frontmatter field as the contract. **Implementation deferred to Round 2** (per-template assignment + enum enforcement). See the **Decision** section below.

## Context

`bm-prd-creator` (see `docs/inspirations.md` → Framework 5) writes its entire planning output into a `_build_plan/` folder explicitly marked **temporary**: the PRD and milestone prompts carry a verbatim disclaimer that *"no code, configuration, runtime logic, tests, or deployment process should import, read, reference, or depend on anything in `_build_plan/`; once the milestones are built and shipped, the folder is expected to be deleted."* The skill even auto-appends a note to the consumer's `CLAUDE.md`/`AGENTS.md` stating this. This is a clean answer to "the spec rots once the code moves past it."

For `gxp-driven-dev`, **the opposite is true for a subset of artifacts.** A URS and a Validation Report are not scaffolding — they are the **permanent audit record**. Deleting them after shipping would destroy the compliance evidence that is the whole point in a regulated domain. Yet *some* of our artifacts genuinely are scaffolding (a build plan, per-milestone implementation prompts, a working interview transcript). **We currently do not distinguish the two**, which risks (a) treating durable compliance evidence as deletable, or (b) treating throwaway scaffolding as permanent and letting it rot the consumer's tree.

## Question

Should every artifact the toolkit produces be classified on a **durable ⟷ ephemeral** axis, with explicit lifecycle handling per class — and what is the classification rule?

## Options considered

### Option A — Everything is durable (status quo)

- **Description:** All generated files are treated as permanent. No deletion guidance.
- **Pros:** Safe for compliance evidence by default (nothing is ever told to delete). Simple.
- **Cons:** Scaffolding (build plans, implementation prompts) accumulates and rots; future agents may treat a stale build prompt as authoritative. No "this is throwaway" signal.
- **Regulatory fit:** Over-conservative — keeps everything, including noise an auditor must then wade through.

### Option B — Everything is ephemeral (copy `bm-prd-creator` directly)

- **Description:** Mark all planning output as temporary, delete after shipping.
- **Pros:** Clean tree.
- **Cons:** **Unacceptable** — would delete URS/VR/RTM, i.e. the audit record. Directly contradicts the toolkit's reason to exist.
- **Regulatory fit:** Disqualifying.

### Option C — Two-class lifecycle: `durable` vs `ephemeral`, declared in frontmatter (recommended)

- **Description:** Every template declares a `lifecycle:` field in frontmatter — `durable` (compliance record / authoritative spec) or `ephemeral` (scaffolding). Ephemeral artifacts carry a `bm-prd-creator`-style disclaimer and live under a clearly-named transient folder (e.g. `_build_plan/` or `.gdd-scratch/`); durable artifacts live in `specs/`, `evidence/`, `compliance-bundle/`. The `init-project` managed-instruction block tells future agents: *nothing durable may depend on anything ephemeral; ephemeral folders may be archived/deleted after the milestone ships; durable artifacts are never deleted, only superseded with version history.*
- **Pros:** Keeps the audit record permanent AND keeps the tree clean. Gives agents an explicit signal. Cheap (one frontmatter field + a convention).
- **Cons:** Requires auditing all 33 templates to assign a class; a few are genuinely hybrid (e.g. an interview transcript that becomes a URS appendix).
- **Regulatory fit:** Strong — mirrors how regulated shops already separate *working papers* from *the validation package*.

## Comparison matrix

| Criterion | A (all durable) | B (all ephemeral) | C (two-class) |
|---|---|---|---|
| Protects audit record | High | **Fails** | High |
| Keeps tree clean | Low | High | High |
| Signal clarity for agents | Low | Medium | High |
| Implementation cost | None | Low | Low–Medium |
| Regulatory defensibility | Medium | Disqualifying | High |

## Recommendation (for the owner to accept/reject)

**Option C.** Add a `lifecycle: durable | ephemeral` field to the template frontmatter contract. Provisional classification:

- **Durable:** URS, FS, DS, CS, RA-INIT, RA-DET, RTM, VR, VP, GXP-ASSESS, SUP-ASSESS, CR, and all `evidence/` + `compliance-bundle/` outputs.
- **Ephemeral:** build plans, per-milestone implementation prompts, interview working notes, scratch analyses — anything that exists only to drive a build chunk and is captured permanently elsewhere (the spec, the milestone-log) once done.

Defer assignment of the genuinely-hybrid cases to the per-template Round 2 pass.

## Decision (2026-05-31)

**ACCEPTED — Option C. Contract adopted now; implementation deferred to Round 2.**

`lifecycle: durable | ephemeral` becomes part of the template frontmatter contract. The provisional classification above is adopted as the starting point. The work is scheduled, **not** executed in this session, to keep the change atomic and reviewable:

**Round 2 implementation checklist (deferred):**
1. Add `lifecycle:` to every one of the 33 templates' frontmatter, using the provisional durable/ephemeral split above; resolve the genuinely-hybrid cases (e.g. interview transcript → URS appendix) during that pass.
2. Add `lifecycle` to the enforced enum in `skills/_scripts/validate-frontmatter.py` (`{durable, ephemeral}`), and to `docs/canonical-schemas.md`.
3. Define the ephemeral folder convention (open question below) and document it in `docs/project-layout.md`.
4. Have `skills/init-project` emit the durable/ephemeral managed-instruction block: *nothing durable may depend on anything ephemeral; ephemeral folders may be archived/deleted after a milestone ships; durable artifacts are never deleted, only superseded with version history.*
5. (Roadmap) a `gdd.cleanup` skill that safely archives/removes only `ephemeral` artifacts after a milestone ships.

Tracked in `STATE.md` under the Round-2 backlog. Until step 2 lands, `lifecycle` is a documented-but-unenforced field, so adding it early to a template is forward-compatible and will not fail CI.

## Consequences

### Positive
- Audit record is structurally protected from "delete after shipping" guidance.
- The consumer's tree stays legible; agents get an explicit durable/ephemeral signal.

### Negative / risks
- One more frontmatter field to validate (`validate-frontmatter.py` must enforce the enum).
- Misclassification risk for hybrid artifacts (mitigated by deferring those to Round 2).

### Things that become possible
- A `gdd.cleanup` skill that safely archives/removes only `ephemeral` artifacts after a milestone ships.
- The managed-instruction block (Cat B) can state the durable/ephemeral rule to every future agent in the consumer repo.

## Open questions left for later

- Folder convention for ephemeral artifacts: reuse `_build_plan/` (familiar to `bm-prd-creator` users) or a `gdd`-namespaced `.gdd-scratch/`?
- How do hybrid artifacts (interview transcript → URS appendix) get handled — promote-on-lock, or dual-write?
- Should `lifecycle` interact with `rigor_level` (e.g. `light` projects keep fewer durable artifacts)?
