---
name: gdd.lint.spec
description: |
  Lint one spec file (or all of `specs/`) before promoting status from
  `draft` → `in-review`. Wraps `skills/_scripts/lint-spec.py`, which combines
  frontmatter validation + clarification-marker check + an RTM coherence
  dry-run in one pass. Reports per-check OK/FAIL, explains the exit codes, and
  states the pass/fail gate for status promotion. Anti-hallucination: never
  edits a spec to force a pass — it reports the deterministic script verdict
  and prescribes the fix.
  Use this skill when:
  - About to promote a spec from `draft` to `in-review` (the gate)
  - The user says "lint", "check this spec", or "is the frontmatter valid"
  - A CI gate needs the validation verdict for one file or the whole `specs/`
allowed-tools: [Bash, Read, Glob, Grep]
---

# `gdd.lint.spec` — Spec Linting

You lint a spec instance (or the whole `specs/` set) by driving the deterministic `lint-spec.py` wrapper and interpreting its three-part output. The script does the YAML parsing, required-field checks, marker grep, and RTM coherence dry-run; **you** read the verdict and prescribe the fix. Never reason your way to a "valid" verdict the script did not give (anti-hallucination).

`lint-spec.py` runs three checks in sequence:

| # | Check | Script | What it catches |
|---|---|---|---|
| 1 | Frontmatter validation | `validate-frontmatter.py` | wrong `type`, missing `based_on_template`, bad `status`, missing semver, missing required fields per the template's `instance_frontmatter_spec`, unresolved markers when `status > draft` |
| 2 | Clarification markers | `check-clarification-markers.py` | `[NEEDS CLARIFICATION: …]` markers (file + line + question) |
| 3 | RTM coherence (dry-run, `--all` only) | `generate-rtm.py` | dangling references across the spec set |

## Pre-flight (do this FIRST)

1. **Locate `.gxp-dev.yaml`**: walk up from the cwd. If not found, **STOP**:
   > *"This project has no `.gxp-dev.yaml` manifest. Run `/gdd.init` first, then re-invoke me."*

2. **Resolve the target.** Either a specific spec path the user named (e.g. `specs/URS.md`) or the whole set (`--all`). If the user did not specify, default to the file they are working on; if unclear, ask.

3. **Locate the toolkit scripts.** Resolve `<gdd-path>` = the `gxp-driven-dev` install root (parent of `skills/`). The wrapper is `<gdd-path>/skills/_scripts/lint-spec.py`.

> The script reads each spec's `based_on_template`, then loads the matching `templates/csv/<TEMPLATE>.md` to know the required fields. The template install must be reachable from the script (it resolves `templates/csv/` relative to its own location), so run with the toolkit install intact.

## Procedure

### Single-file lint (the promotion gate)

From the **consumer project root**:

```bash
python <gdd-path>/skills/_scripts/lint-spec.py specs/URS.md
```

For a single file the RTM step is skipped (it needs the full set); use `--all` to include it.

### Whole-`specs/` lint (CI gate)

```bash
python <gdd-path>/skills/_scripts/lint-spec.py --all
```

`--all` walks every `specs/*.md` (excluding the derived `RTM.md` and `_`-prefixed files) and adds the RTM coherence dry-run as `[3/3]`.

### Reading the exit code (the gate)

| Exit | Meaning | Gate verdict |
|---|---|---|
| `0` | all checks passed | ✅ lint PASSES |
| `1` | one or more checks failed (review the per-check FAIL lines) | ❌ lint FAILS |
| `2` | setup error (no files / `specs/` not found) | configuration error — fix the target path |

## How to read the output

The wrapper prints three labelled blocks:

```
[1/3] Frontmatter validation
  OK URS.md            ← passes
  FAIL FS.md           ← fails; indented lines below are the specific errors
     - Missing required field per template spec: `system_id`
[2/3] Clarification markers
  OK URS.md            ← clean (no markers)
  FAIL FS.md           ← has markers; lines show `L<n>: <question>`
[3/3] RTM coherence — dangling refs listed if any
```

- **`[1/3]` FAIL** → a frontmatter problem. The indented `- …` lines name the exact field/rule. Fix the frontmatter, re-run.
- **`[2/3]` FAIL** → unresolved `[NEEDS CLARIFICATION: …]` markers. **In `draft` this is expected** — see the gate logic below.
- **`[3/3]`** → dangling references; if present, hand off to `/gdd.trace.validate` for the full traceability report.

## The pass/fail gate logic (CORE)

The whole point of this skill is the **draft → in-review promotion gate**:

1. **`draft` status** — markers are *legitimate* (the URS/RA/FS skills deliberately leave `[NEEDS CLARIFICATION: …]` for later). A draft with markers is fine; it just **cannot be promoted** yet. Report the marker count as work-remaining, not as a failure of the draft itself.
2. **Promoting to `in-review`** — run the lint. The gate requires:
   - `[1/3]` frontmatter PASSES, **and**
   - `[2/3]` **zero** clarification markers (every marker resolved), **and**
   - `[3/3]` zero dangling references (when run `--all`).
   Only when all three hold may the user set `status: in-review`.
3. **`approved`** — `validate-frontmatter.py` additionally requires `approved_by` present and a valid semver `version`, and **fails** on any remaining marker. So a clean lint at `in-review` plus signatures is the path to `approved`. Never set `approved` yourself — it needs human signatures.

> [!warning] IQ/OQ/PQ status-enum gap (finding TF1)
> `validate-frontmatter.py` accepts `{draft, in-review, approved, superseded, in-execution, executed}`. Author test protocols at `status: draft` (validates cleanly); `in-execution`/`executed` are set at execution time. Do not invent a status to work around a check.

## Anti-hallucination rules (NON-NEGOTIABLE)

1. **Never edit a spec to force a green lint.** Report the script's verdict; propose the specific frontmatter or marker fix, and let the user confirm.
2. **Never claim a spec is promotable while markers remain** (outside `draft`). Resolve them first.
3. **Never invent a `status`, `version`, or `approved_by`** to satisfy a check — that defeats the gate.
4. **Report exactly what the script printed** — do not summarize a FAIL as a PASS.

## Post-flight (after running)

1. **Print verdict**: PASS (exit 0) or FAIL (exit 1) with the per-check breakdown.
2. **For each `[1/3]` failure**, list the named field/rule and the fix.
3. **For markers**, give the count + the file:line list; state whether they block the user's intended status transition.
4. **Suggest next step**:
   - Markers > 0 and the user wants `in-review` → resolve the markers first (re-run the producing skill or answer in place), then re-lint.
   - `[3/3]` dangling refs → `/gdd.trace.validate` for the full traceability report.
   - All clean → the spec is eligible for `in-review` (set by the user, not by you).

## When to refuse

- `.gxp-dev.yaml` missing → redirect to `/gdd.init`.
- User asks to promote a spec to `in-review`/`approved` while lint fails → refuse; the gate must pass.
- User asks you to delete `[NEEDS CLARIFICATION: …]` markers without answering them → refuse; resolve, don't erase.
