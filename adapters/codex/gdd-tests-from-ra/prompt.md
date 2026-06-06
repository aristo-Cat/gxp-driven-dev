---
description: |
  Test protocols (IQ / OQ / PQ) from the cascade. The risk bridge: each RA-DET
  high-RPN function gets positive + negative testing in the OQ; the IQ verifies
  installation/config against CS/FS scaled by RA-INIT priority; the PQ verifies
  fitness-for-intended-use end-to-end by end users against the URS prio=H set.
  Produces draft protocols (templates filled, "Actual result" columns left for
  execution) — NEVER fabricates test results. Anti-hallucination: uses
  [NEEDS CLARIFICATION: …] for environment/baseline/tester gaps.
  Output: specs/IQ.md, specs/OQ.md, specs/PQ.md.
argument-hint: "[nothing needed — inputs are specs/FS.md, specs/RA-INIT.md, specs/RA-DET.md, specs/URS.md, plus CS or DS depending on gamp_category]"
---

# gdd.tests.from-ra — Test Protocols IQ / OQ / PQ (Codex prompt)

> **Codex invocation.** Place this file under your Codex prompts/skills directory so it is exposed as the slash command **`/gdd-tests-from-ra`** (Codex derives the command name from the filename). This skill takes no seed argument — it reads all inputs from the `specs/` directory and `.gxp-dev.yaml`. `$ARGUMENTS`, if provided, is ignored (the cascade is self-describing).
>
> **Two-part port.** This prompt carries the *procedure*. The *always-on guardrails* (anti-hallucination, anonymization, "never set status: approved", read-manifest-first) live in `../AGENTS.snippet.md`, which the consumer pastes into their project `AGENTS.md` so they hold even when this prompt is not the active turn. See `../PORTING.md`.
>
> **Shared core.** The deterministic work — frontmatter validation, RTM generation, clarification-marker scan, anti-leak guard — is done by the harness-agnostic Python in `skills/_scripts/`, invoked by path. Do **not** re-implement it here. Source of truth: `skills/tests-from-ra/SKILL.md` + `generation-flow.md` + `output-template.md`.

You produce the three **qualification protocols** from the cascade, in V-Model order. Each is a *protocol* (`status: draft`) — the test steps and expected results are written; the **"Actual result" / pass columns are left blank for execution**. Follow `templates/csv/IQ.md`, `OQ.md`, `PQ.md`.

| Protocol | Verifies | Against | Owner of rigor |
|---|---|---|---|
| **IQ** (installation verification) | the system is correctly installed/configured | CS (Cat 4) / DS (Cat 5) + FS | RA-INIT Risk Priority |
| **OQ** (functional verification) | each GxP function operates per the FS | FS | **RA-DET RPN** (the bridge) |
| **PQ** (fitness-for-intended-use) | the system is fit for intended use end-to-end | URS (prio=H) | RA-INIT Risk Priority |

## Pre-flight (do this FIRST, before any generation)

1. **Locate `.gxp-dev.yaml`** by walking up from the working directory. If absent, **STOP**: *"This project has no `.gxp-dev.yaml` manifest. Run `/gdd-init` first, then re-invoke `/gdd-tests-from-ra`."*
2. **Load the manifest**: `gamp_category` (Cat 4 → IQ uses CS; Cat 5 → IQ uses DS), `rigor_level`, `language`.
3. **Locate the inputs** (warn if any is not `status: approved` — protocols verify approved specs):
   - `specs/FS.md` (required — OQ source)
   - `specs/URS.md` (required — PQ source)
   - `specs/CS.md` (Cat 4) or `specs/DS.md` (Cat 5) — IQ source
   - `specs/RA-INIT.md` (required — scales IQ/PQ rigor + Risk Priority)
   - `specs/RA-DET.md` (required — RPN scales OQ rigor)
   - If any required input is missing, **STOP** and name the missing file: redirect to the skill that produces it.
4. **Read the three source templates** `templates/csv/IQ.md`, `templates/csv/OQ.md`, `templates/csv/PQ.md`.
5. **Check existing** `specs/IQ.md`, `specs/OQ.md`, `specs/PQ.md`. For each that already exists, present: *"specs/IQ.md already exists. Reply 1 = replace / 2 = append / 3 = abort for this file."* Wait for the reply before proceeding with that file.

## Interaction principles (every question)

Codex has no `AskUserQuestion`; pose discrete choices as an explicit enumerated prompt.

1. **Propose each test step with reasoning, then confirm.** Propose the verification step + expected result with the *why*, and let the user adjust. A confirmed expected-result is grounded; an invented one is hallucination. Example: *"For the unauthorized-threshold-change negative test I'd expect: action denied + attempt logged in the audit trail. Reply 1 = agree / 2 = adjust."*
2. **Offer discrete choices as an explicit enumerated prompt** (which special test types to activate; whether a low-risk function is tested or risk-accepted); free text for step/expected-result descriptions.
3. **One protocol (or one test case) at a time.** Do not dump all three protocols in one message.
4. **Adapt depth to RPN / Risk Priority.** High-RPN functions get the most test detail (positive + negative + stress); low-risk get Good Engineering Practice / risk-acceptance.

## Generation flow

Generate in **V-Model order — IQ, then OQ, then PQ** (each later protocol references the earlier as prerequisite).

### IQ — Installation Qualification

1. **Parse install/config items** from CS (Cat 4) / DS (Cat 5) + FS: product version, hardware, configuration baseline values, connectivity/interfaces, security settings, documentation.
2. **For each item** → ≥1 `IQ-TC-NNN`: cite the CS/FS-ID (+ RA-INIT-NNN if it ties to a risk), the verification step, and the expected result (baseline value from the CS/DS).
3. **Scale rigor** by RA-INIT Risk Priority: H exhaustive / M sampling / L basic.
4. **Sections** (mirror `templates/csv/IQ.md`): §0 identity + signatures (author/approvers + Tester + independent Reviewer) + overall-result checkboxes (unmarked); §1 objective; §4 risk-based strategy; §5 verification procedure — §3.2 prerequisites, §5.2 equipment, §5.3 components, §5.4 config baseline against CS, §5.5 connectivity/interfaces/security, §5.6 documentation; §8 summary (counts); §10 related; §11 revision.
5. IQ is the **prerequisite of the OQ** — note it in the OQ header.

### OQ — Operational Qualification (the RPN bridge)

1. **Parse GxP `FS-<CAT>-NNN`** from `specs/FS.md` with their Risk Priority (from RA-INIT) and RPN (from RA-DET).
2. **Per function, apply the RPN→rigor rule**:
   - **RPN ≥ 12** → a **positive** test case AND a **negative** test case (both cite the same `RA-INIT-NNN`). Add stress where the failure mode is performance/resilience.
   - **RPN 6-9** → positive test.
   - **RPN 1-4** → Good Engineering Practice / risk-accepted (documented, not falsely covered).
3. **Negative-test attribution (lesson TF2).** A function's negative/resilience test may exercise the FS-ID of the *mitigation* that protects it. In that case **cite both FS-IDs** on the `OQ-TC` "Verifies" cell, and reflect that in §6 — so the "every Priority-H function has positive+negative" check passes.
4. **Activate special test types** per active URS presets (present as enumerated choice if unclear):

   | If active in URS | Add to OQ |
   |---|---|
   | URS-EREC | audit-trail test (old/new/reason captured; peer review) |
   | URS-ESIG | e-signature test (manifestation + linking + tamper-evidence/negative) |
   | URS-SEC | access/MFA test (roles, segregation, MFA enforced — negative on unauthorized) |
   | URS-API | interface test (validated end-to-end + failure/retry negative) |

5. **§6 functional coverage table** must agree with the OQ-TC "Verifies" cells; low-risk untested functions are listed as **risk-accepted** (GAMP 5 §D5), never claimed as covered.
6. **Sections** (mirror `templates/csv/OQ.md`): §0 identity (FS + IQ prerequisite + RA) + roles/testers table + signatures + result checkboxes; §1 objective; §4 risk-based strategy + special test types; §5 test cases (positive + negative, one table per case): `OQ-TC | Verifies (FS-ID) | Risk (RA-INIT) | step | expected | actual | passed`; §6 functional coverage table; §8 summary; §10 related; §11 revision.

### PQ — Performance Qualification (end-to-end)

1. **Parse `URS-<CAT>-NNN` with prio=H** from `specs/URS.md`.
2. **Group them into end-to-end business processes** (not isolated functions) → each group becomes one `PQ-SCEN-NNN` with: the URS-IDs it covers, the RA-INIT-NNN risk, the **end-user role** that executes it, and the process steps.
3. **Scale depth** by Risk Priority (H: full scenario + boundary + realistic volume).
4. **§8 statement of fitness** (GAMP 5 §M7): write the formal declaration template with the intended-use from the URS, left unmarked (decided at execution).
5. PQ is executed by **end users**, not IT; environment is **production-like**.
6. **Sections** (mirror `templates/csv/PQ.md`): §0 identity (URS + OQ prerequisite + RA) + end-user executors table + signatures (author = Process Owner) + result checkboxes; §1 objective; §4 risk-based end-to-end strategy; §5 scenarios `PQ-SCEN-NNN` (each: covers URS-IDs + risk + executing end-user role + step table); §6 fitness coverage (URS prio=H → PQ-SCEN); §8 summary + `> [!quote]` statement of fitness (§M7) left unmarked; §10 related; §11 revision.

## Anti-hallucination rules (NON-NEGOTIABLE — also enforced via AGENTS.md)

1. **Never fabricate test results, evidence, versions, or data.** Protocols are authored at `status: draft`; the "Actual result" / pass columns are blank until real execution.
2. **Never invent environment/baseline/tester values.** Use `[NEEDS CLARIFICATION: which test environment / installation baseline / tester?]` for unknowns.
3. **Cite real IDs only.** IQ-TC → CS/FS-ID; OQ-TC → FS-ID + RA-INIT-NNN; PQ-SCEN → URS-IDs + RA-INIT-NNN. Never reference an ID not present in its source spec.
4. **Tester ≠ Reviewer** (segregation of duties); the PQ is executed by **end users**, not IT.
5. **Never invent regulatory citations.** Only the templates' §-references (GAMP 5 Table 4.1 / §D5 / §8.5.4 / §M7, 21 CFR Part 11, EU Annex 11 §9).
6. **Honor `language`.**
7. **Read, do not write, the templates** `templates/csv/IQ.md`, `OQ.md`, `PQ.md`.

## Status semantics

Each protocol is written at `status: draft`. Instance frontmatter per each template's `instance_frontmatter_spec`:

```yaml
---
title: "<IQ|OQ|PQ> — <…> for {{system_name}}"
type: instance
based_on_template: "<IQ|OQ|PQ>"
based_on_template_version: "0.1.0"
project_id: "{{project_id}}"
system_id: "{{system_id}}"
traces_to: "<source spec(s) + version + status>"
gamp_category: {{3|4|5}}
status: draft
version: "0.1"
created: "{{today}}"
updated: "{{today}}"
language: "{{language from .gxp-dev.yaml}}"
# cross-refs: ra_ref (all); iq_ref (OQ); oq_ref (PQ)
---
```

- **IQ** `traces_to`: CS (Cat 4) / DS (Cat 5) + FS. **OQ** `traces_to`: FS. **PQ** `traces_to`: URS.
- `executed_by` / `reviewed_by` / `execution_date` fields are set at execution time.

> **Status-enum gap (known issue TF1).** The IQ/OQ/PQ templates define `status: {draft, in-execution, executed, approved, superseded}`, but the current `validate-frontmatter.py` only accepts `{draft, in-review, approved, superseded}`. Author protocols at `status: draft` (validates cleanly). The `in-execution` / `executed` states are set at execution time and currently **do not pass** `validate-frontmatter` — flagged for a script fix; do not work around it by inventing a different status.

**Never** set `status: in-review`, `status: approved`, `status: in-execution`, or `status: executed` at authoring time.

## Output shape (reference)

Mirror the canonical templates. Three output files:

- `specs/IQ.md` — installation/configuration verification cases, each `IQ-TC-NNN` citing a CS/FS-ID.
- `specs/OQ.md` — functional test cases, each `OQ-TC-NNN` citing a FS-ID + RA-INIT-NNN; §6 coverage table; special test types per URS presets.
- `specs/PQ.md` — end-to-end business scenarios, each `PQ-SCEN-NNN` citing URS-IDs + RA-INIT-NNN; §8 statement of fitness (§M7, left unmarked).

Worked examples: `examples/temp-logger-gmp-chamber/specs/{IQ,OQ,PQ}.md` (IQ 15 IQ-TC, OQ 14 OQ-TC with 4 high-RPN functions pos+neg, PQ 4 PQ-SCEN + §M7 fitness statement). See `skills/tests-from-ra/output-template.md` for the exact section shapes.

## Post-flight — call the shared Python core

From the consumer project root (substitute `<gdd-path>` with your `gxp-driven-dev` install):

```bash
python <gdd-path>/skills/_scripts/validate-frontmatter.py specs/IQ.md
python <gdd-path>/skills/_scripts/validate-frontmatter.py specs/OQ.md
python <gdd-path>/skills/_scripts/validate-frontmatter.py specs/PQ.md
python <gdd-path>/skills/_scripts/check-clarification-markers.py specs/IQ.md specs/OQ.md specs/PQ.md --draft
python <gdd-path>/skills/_scripts/generate-rtm.py --specs-dir specs
```

If `validate-frontmatter.py` fails on any file, report the errors and do **not** claim success. Then run coverage checks and print summary:

**Coverage gates (run before claiming complete):**
- **OQ**: every GxP FS-ID with Risk Priority=H (RA-DET RPN ≥ 12) has **both** a positive and a negative OQ-TC (cross-check §6 vs OQ-TC rows).
- **PQ**: every URS-ID with prio=H is covered by ≥1 PQ-SCEN (or risk-accepted with rationale).
- **IQ**: every CS/FS install item has ≥1 IQ-TC.
- **Traceability**: each test ID cites its source spec ID (IQ-TC→CS/FS; OQ-TC→FS+RA-INIT; PQ-SCEN→URS+RA-INIT).

**Print summary**: IQ-TC count / OQ-TC count / PQ-SCEN count, the high-RPN functions and their pos+neg tests, risk-accepted functions, clarification marker count.

**Suggest next**: `/gdd-trace-validate` to verify traceability, then `/gdd-next` for the next cascade step (Validation Report — `/gdd-vr-from-tests` consumes the protocol summaries + the PQ statement of fitness, GAMP 5 §M7, to close the V-Model).

## When to refuse

- `.gxp-dev.yaml` missing → redirect to `/gdd-init`.
- `specs/FS.md` or `specs/RA-DET.md` missing → STOP and name the missing file; redirect to the skill that produces it (`/gdd-fs-from-urs`, `/gdd-ra-detail-from-urs-fs`).
- User asks to fill in "Actual result" / pass columns without real execution → refuse; that is fabricating evidence.
- User asks to claim total OQ coverage when low-risk functions were not tested → refuse; document risk-acceptance per GAMP 5 §D5 instead.
- User asks to have IT execute the PQ → flag; the PQ is executed by end users (if the user insists, insert `[NEEDS CLARIFICATION: PQ executor role — must be end user, not IT]`).
- "Just make up the test results" → refuse; cite anti-hallucination policy.
