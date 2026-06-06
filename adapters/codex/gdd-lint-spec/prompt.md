---
description: |
  Lint one spec file (or all of `specs/`) before promoting status from
  `draft` → `in-review`. Wraps `skills/_scripts/lint-spec.py`, which combines
  frontmatter validation + clarification-marker check + an RTM coherence
  dry-run in one pass. Reports per-check OK/FAIL, explains the exit codes, and
  states the pass/fail gate for status promotion. Anti-hallucination: never
  edits a spec to force a pass — it reports the deterministic script verdict
  and prescribes the fix.
argument-hint: "[path to a spec, e.g. /gdd-lint-spec specs/URS.md]"
---

# gdd.lint.spec — Spec Linting (Codex prompt)

> **Codex invocation.** Place this file under your Codex prompts/skills directory so it is exposed as the slash command **`/gdd-lint-spec`** (Codex derives the command name from the filename). `$ARGUMENTS` (if provided) is the spec path to lint (e.g. `specs/URS.md`) or the flag `--all` to lint the whole `specs/` set. If `$ARGUMENTS` is absent, default to the file the user is currently working on; if that is ambiguous, present the explicit choice below.
>
> **Two-part port.** This prompt carries the *procedure*. The *always-on guardrails* (anti-hallucination, linear status, "never weaken a gate to go green") live in `../AGENTS.snippet.md`, which the consumer pastes into their project `AGENTS.md` so they hold even when this prompt is not the active turn. See `../PORTING.md`.
>
> **Shared core — the heavy lifting is the Python.** The deterministic work — frontmatter validation, clarification-marker scan, RTM coherence dry-run — is done by the harness-agnostic Python in `skills/_scripts/`, invoked by path. This prompt **orchestrates** those scripts; it does **not** re-implement them. Do not reason your way to a "valid" verdict that the script did not give. Invariant #12 is absolute: **never weaken the gate to go green** — fix the spec, never the script or the rule. Source of truth: `skills/lint-spec/SKILL.md`.
>
> **Shared guardrails.** `../AGENTS.snippet.md` already covers all gxp-driven-dev skills. Do **not** paste it here; it belongs in the consumer's `AGENTS.md` only.

You lint a spec instance (or the whole `specs/` set) by driving the deterministic `lint-spec.py` wrapper and interpreting its three-part output. The script does the YAML parsing, required-field checks, marker grep, and RTM coherence dry-run; **you** read the verdict and prescribe the fix. Never claim a spec is valid based on your own reasoning if the script has not returned exit 0.

`lint-spec.py` runs three checks in sequence:

| # | Check | Script | What it catches |
|---|---|---|---|
| 1 | Frontmatter validation | `validate-frontmatter.py` | wrong `type`, missing `based_on_template`, bad `status`, missing semver, missing required fields per the template's `instance_frontmatter_spec`, unresolved markers when `status > draft` |
| 2 | Clarification markers | `check-clarification-markers.py` | `[NEEDS CLARIFICATION: …]` markers (file + line + question) |
| 3 | RTM coherence (dry-run, `--all` only) | `generate-rtm.py` | dangling references across the spec set |

## Pre-flight (do this FIRST)

1. **Locate `.gxp-dev.yaml`**: walk up from the cwd. If not found, **STOP**:
   > *"This project has no `.gxp-dev.yaml` manifest. Run `/gdd-init` first, then re-invoke `/gdd-lint-spec`."*

2. **Resolve the target.** Use `$ARGUMENTS` if provided. If absent, default to the file the user is currently working on. If the target is still ambiguous, present this explicit choice (Codex has no `AskUserQuestion`):

   > Which target should I lint?
   > 1. `specs/URS.md` — lint the URS only
   > 2. `specs/<other file>` — enter the path
   > 3. `--all` — lint every file in `specs/` (includes RTM coherence check)

3. **Locate the toolkit scripts.** Resolve `<gdd-path>` = the `gxp-driven-dev` install root (the parent of `skills/`). The wrapper lives at `<gdd-path>/skills/_scripts/lint-spec.py`.

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
| `0` | all checks passed | lint PASSES |
| `1` | one or more checks failed (review the per-check FAIL lines) | lint FAILS |
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

- **`[1/3]` FAIL** — a frontmatter problem. The indented `- …` lines name the exact field/rule. Fix the frontmatter, re-run.
- **`[2/3]` FAIL** — unresolved `[NEEDS CLARIFICATION: …]` markers. **In `draft` this is expected** — see the gate logic below.
- **`[3/3]`** — dangling references; if present, hand off to `/gdd-trace-validate` for the full traceability report.

## The pass/fail gate logic (CORE)

The whole point of this skill is the **draft → in-review promotion gate**:

1. **`draft` status** — markers are *legitimate* (the URS / RA / FS skills deliberately leave `[NEEDS CLARIFICATION: …]` for later). A draft with markers is fine; it just **cannot be promoted** yet. Report the marker count as work-remaining, not as a failure of the draft itself.
2. **Promoting to `in-review`** — run the lint. The gate requires **all three** of:
   - `[1/3]` frontmatter **PASSES**, **and**
   - `[2/3]` **zero** clarification markers (every marker resolved), **and**
   - `[3/3]` zero dangling references (when run `--all`).
   Only when all three hold may the user set `status: in-review`.
3. **`approved`** — `validate-frontmatter.py` additionally requires `approved_by` present and a valid semver `version`, and fails on any remaining marker. A clean lint at `in-review` plus human signatures is the path to `approved`. **Never** set `status: approved` yourself.

> **IQ/OQ/PQ status-enum note (finding TF1).** `validate-frontmatter.py` accepts `{draft, in-review, approved, superseded, in-execution, executed}`. Author test protocols at `status: draft`. `in-execution`/`executed` are set at execution time. Do not invent a status to work around a check.

## Draft → in-review promotion flow

If the user asks to promote a spec's status and the lint has not yet been run (or was not run with `--all`), present this explicit choice before proceeding:

> To promote `specs/<FILE>.md` to `in-review` I need to run the lint gate first.
> 1. Run `lint-spec.py specs/<FILE>.md` now and review the results together
> 2. Run `lint-spec.py --all` to lint the full `specs/` set (recommended before promotion)
> 3. Abort — I will handle the lint manually

Do **not** set `status: in-review` or `status: approved` in the frontmatter yourself. If lint passes, tell the user the spec is eligible and instruct them to set the status field — they must do it explicitly.

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
   - Markers > 0 and user wants `in-review` → resolve the markers first (re-run the producing skill or answer in place), then re-lint.
   - `[3/3]` dangling refs → run `/gdd-trace-validate` for the full traceability report.
   - All clean → the spec is eligible for `in-review` (the user sets the field, not you).

## Call the shared Python core (verbatim invocations)

All three scripts below are called by `lint-spec.py` internally. They are also available for direct use when you need the individual check result:

```bash
python <gdd-path>/skills/_scripts/lint-spec.py specs/URS.md
python <gdd-path>/skills/_scripts/validate-frontmatter.py specs/URS.md
python <gdd-path>/skills/_scripts/check-clarification-markers.py specs/URS.md --draft
```

For the full suite with RTM coherence:

```bash
python <gdd-path>/skills/_scripts/lint-spec.py --all
```

Never re-implement these checks in prose. If `validate-frontmatter.py` fails, report the errors and do **not** claim success.

## When to refuse

- `.gxp-dev.yaml` missing → redirect to `/gdd-init`.
- User asks to promote a spec to `in-review` or `approved` while lint fails → refuse; the gate must pass first.
- User asks to delete `[NEEDS CLARIFICATION: …]` markers without answering them → refuse; resolve, don't erase.
- User asks you to edit the spec's `validation_rules`, a preset, or the Python scripts just to make the lint pass → refuse; cite invariant #12 (never weaken the gate to go green).
