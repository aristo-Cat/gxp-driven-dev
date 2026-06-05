---
name: gdd.trace.validate
description: |
  Validate Requirements Traceability across a project's `specs/`. Wraps
  `skills/_scripts/generate-rtm.py` to derive `specs/RTM.md`, then asserts
  ZERO dangling references and runs the anti-orphan check — every FS / OQ-TC /
  RA-DET row must name a real upstream ID (URS / FS / RA-INIT). Reports gaps,
  explains how to read the RTM, and prescribes the fix (which skill to re-run)
  for each class of break. Read-only on the specs (only writes the derived RTM).
  Anti-hallucination: never invents trace links — it only reports what the
  scripts deterministically find.
  Use this skill when:
  - Before promoting any spec from `draft`/`in-review` to `approved`
  - The user says "check traceability", "is everything traced", or "build the RTM"
  - After a cascade step, to confirm the new spec is wired to its upstream
  - A CI gate needs the URS ↔ FS ↔ RA ↔ Tests coherence verdict
allowed-tools: [Bash, Read, Write, Glob, Grep]
---

# `gdd.trace.validate` — Traceability Validation

You validate **Requirements Traceability** across a consumer project's `specs/` by driving the deterministic `generate-rtm.py` script and interpreting its output. The script does the exhaustive ID-walking; **you** read the result, classify the breaks, and prescribe the fix. Never hand-compute traceability — the script is the source of truth (anti-hallucination).

The headline gate is **zero dangling references**. A dangling reference (an ID cited by a downstream spec that no spec declares) is a *bug* and blocks promotion to `approved` (GAMP 5 backward-traceability / anti-orphan rule, `docs/requirement-id-scheme.md` §"Backward references").

## Pre-flight (do this FIRST)

1. **Locate `.gxp-dev.yaml`**: walk up from the cwd. If not found, **STOP**:
   > *"This project has no `.gxp-dev.yaml` manifest. Run `/gdd.init` first, then re-invoke me."*

2. **Load the manifest** and note: `templates_active` (which spec files *should* exist), `id_scheme` + `custom_alias` (if custom, downstream IDs are aliased — translate when reasoning about expected IDs), `mode`, `gamp_category`.

3. **Confirm `specs/` exists.** If there is no `specs/` directory or it is empty, **STOP** and redirect to `/gdd.init` / `/gdd.urs.from-idea` — there is nothing to trace yet.

4. **Locate the toolkit scripts.** Resolve `<gdd-path>` = the `gxp-driven-dev` install root (parent of `skills/`). The script lives at `<gdd-path>/skills/_scripts/generate-rtm.py`.

## Procedure

### Step 1 — Generate the RTM

From the **consumer project root** (so `specs/` resolves):

```bash
python <gdd-path>/skills/_scripts/generate-rtm.py --specs-dir specs --output specs/RTM.md
```

Capture both the stdout summary and the written `specs/RTM.md`. The script exit code is the primary gate:

| Exit | Meaning | Verdict |
|---|---|---|
| `0` | RTM generated, **0 dangling references** | ✅ traceability gate PASSES |
| `1` | no spec files found in `specs/` | setup error — redirect to `/gdd.urs.from-idea` |
| `2` | RTM generated but **≥1 dangling reference** | ❌ traceability gate FAILS |

> Do not edit `specs/RTM.md` by hand — it is regenerated on every run. The `## Gaps and orphans` section is your report source.

### Step 2 — Assert zero dangling references (hard gate)

Read the **`### Dangling references (referenced but not declared)`** subsection of `specs/RTM.md` (and the stdout `… dangling refs` count). Each listed ID is cited by some spec but declared by none.

- **If 0 dangling references** → the hard gate passes. Proceed to Step 3.
- **If ≥1 dangling reference** → the gate **FAILS**. List each dangling ID and its cause class (below). Do **not** report the project as traceable.

### Step 3 — Anti-orphan check (every downstream row names a real upstream)

Beyond the script's own dangling check, verify the *backward* direction the toolkit requires (`docs/requirement-id-scheme.md`):

- Every `FS-<CAT>-NNN` row must name the `URS-<CAT>-NNN` it implements.
- Every `OQ-TC-NNN` must name the `FS-<CAT>-NNN` (or `URS-<CAT>-NNN`) it verifies.
- Every `RA-DET-NNN` row must name the `URS-<CAT>-NNN` and/or `FS-<CAT>-NNN` it analyses.

The script encodes this row-scoped: an upstream ID with **no downstream consumer** lands in `### IDs with no downstream reference`, and a downstream ID citing a non-existent upstream lands in `### Dangling references`. Read both subsections and Grep the specs to confirm any suspicious row actually carries its upstream ID on the same table row (the RTM links are row-scoped — two IDs only link when they share a line). Use `Grep` to locate the offending row in the source spec before reporting.

> Note: `IDs with no downstream reference` is **not always a bug**. It is expected for last-layer IDs (`PQ-SCEN-*`, `PQ-*`) and for `GxP=N` requirements that are out of validation scope. Flag them for review, but do not fail the gate on them. Only **dangling references** and **GxP=Y downstream-less requirements that should have a test** are true breaks.

## How to read the RTM output

The derived `specs/RTM.md` has four sections:

1. **`## Summary`** — counts: spec files scanned, IDs declared, forward-trace links, IDs-without-downstream, dangling refs. Read this first for the verdict.
2. **`## Requirement IDs per spec file`** — own-ID vs references-others counts per file; a spec that "references others: 0" but should consume upstream IDs is suspicious (likely a missing cascade).
3. **`## Forward traceability`** — the upstream→downstream matrix. Use it to spot a URS-ID with no FS/test consumer.
4. **`## Gaps and orphans`** — the two break lists (no-downstream, dangling). Your report source.

## Fixing breaks (prescribe the right skill)

For each break, name the cause and the remediation:

| Break | Likely cause | Fix |
|---|---|---|
| `FS-<CAT>-NNN` dangling (cited by OQ/RA-DET, not in FS.md) | typo in the citing row, or the FS row was deleted | correct the citation in the downstream spec, or restore the FS row; re-run |
| `URS-<CAT>-NNN` cited by FS but not in URS.md | the FS invented an upstream | edit the FS row to cite a real `URS-<CAT>-NNN`, or add the URS requirement via `/gdd.urs.from-idea` (append) |
| `URS-<CAT>-NNN` (GxP=Y) with no downstream | URS requirement never realized in the FS | run `/gdd.fs.from-urs` to add the missing `FS-<CAT>-NNN` |
| `FS-<CAT>-NNN` (GxP=Y) with no OQ-TC | function never tested | run `/gdd.tests.from-ra` to add the OQ-TC |
| `RA-DET-NNN` citing a non-existent URS/FS ID | RA-DET referenced an upstream that was renumbered | correct the citation; re-run |

After any fix, **re-run Step 1** and confirm the dangling count returns to 0.

## Anti-hallucination rules (NON-NEGOTIABLE)

1. **Never invent a trace link.** Report only what `generate-rtm.py` finds. If you think two IDs should be linked but the script does not link them, the rows do not share a line — that is the finding, not something to paper over.
2. **Never edit a spec to "make the RTM pass" without the user's intent.** Propose the specific row edit (and which skill produces it), then let the user confirm.
3. **Never claim traceability is complete while dangling references remain.** Exit code 2 = FAIL, full stop.
4. **`specs/RTM.md` is derived** — never hand-edit it; re-run the generator.

## Post-flight (after running)

1. **Print verdict**: PASS (exit 0, 0 dangling) or FAIL (exit 2, N dangling), plus the counts from `## Summary`.
2. **List every dangling reference** with its cause class and the prescribed fix skill.
3. **List GxP=Y no-downstream IDs** as review items (distinguish from acceptable last-layer/`GxP=N` orphans).
4. **Suggest next step**:
   - PASS → if all cascade specs are `approved`, suggest `/gdd.vr.from-tests` (Validation Report) to close the V-Model.
   - FAIL → name the single highest-leverage fix skill to run first, then re-invoke `/gdd.trace.validate`.

## When to refuse

- `.gxp-dev.yaml` missing → redirect to `/gdd.init`.
- `specs/` empty → redirect to `/gdd.urs.from-idea`.
- User asks to mark a spec `approved` while dangling references exist → refuse; the gate must pass first.
- User asks you to hand-write the RTM instead of running the script → refuse; the RTM is derived deterministically.
