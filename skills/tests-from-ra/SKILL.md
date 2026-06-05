---
name: gdd.tests.from-ra
description: |
  Test protocols (IQ / OQ / PQ) from the cascade. The risk bridge: each RA-DET
  high-RPN function gets positive + negative testing in the OQ; the IQ verifies
  installation/config against CS/FS scaled by RA-INIT priority; the PQ verifies
  fitness-for-intended-use end-to-end by end users against the URS prio=H set.
  Produces draft protocols (templates filled, "Actual result" columns left for
  execution) — NEVER fabricates test results. Anti-hallucination: uses
  `[NEEDS CLARIFICATION: …]` for environment/baseline/tester gaps.
  Output: `specs/IQ.md`, `specs/OQ.md`, `specs/PQ.md`.
  Use this skill when:
  - FS (+ CS for Cat 4 / DS for Cat 5), RA-INIT and RA-DET exist
  - The user says "draft the tests", "write the IQ/OQ/PQ", or "qualification protocols"
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# `gdd.tests.from-ra` — Test protocols (IQ / OQ / PQ)

You produce the three **qualification protocols** from the cascade, in V-Model order. Each is a *protocol* (`status: draft`) — the test steps and expected results are written; the **"Actual result" / pass columns are left blank for execution**. Follow `templates/csv/IQ.md`, `OQ.md`, `PQ.md`.

| Protocol | Verifies | Against | Owner of rigor |
|---|---|---|---|
| **IQ** (installation verification) | the system is correctly installed/configured | CS (Cat 4) / DS (Cat 5) + FS | RA-INIT Risk Priority |
| **OQ** (functional verification) | each GxP function operates per the FS | FS | **RA-DET RPN** (the bridge) |
| **PQ** (fitness-for-intended-use) | the system is fit for intended use end-to-end | URS (prio=H) | RA-INIT Risk Priority |

## Pre-flight (do this FIRST)

1. **Locate `.gxp-dev.yaml`**: walk up from cwd. If missing → `/gdd.init`. Note `gamp_category` (Cat 4 → IQ uses CS; Cat 5 → IQ uses DS), `rigor_level`, `language`.
2. **Locate the inputs** (warn if any is not `approved` — protocols verify approved specs):
   - `specs/FS.md` (required — OQ source), `specs/URS.md` (required — PQ source).
   - `specs/CS.md` (Cat 4) or `specs/DS.md` (Cat 5) — IQ source.
   - `specs/RA-INIT.md` (required — scales IQ/PQ rigor + Risk Priority) and `specs/RA-DET.md` (required — RPN scales OQ rigor).
3. **Read the three source templates** `templates/csv/IQ.md`, `OQ.md`, `PQ.md`.
4. **Check existing** `specs/{IQ,OQ,PQ}.md`: ask replace / append / abort per file.

## Generation flow

Follow `generation-flow.md` (this folder). Generate **in V-Model order** — IQ, then OQ, then PQ (each later one references the earlier as prerequisite). Summary:

| Protocol | Per item | Rigor rule |
|---|---|---|
| **IQ** | each CS/FS install/config item → ≥1 `IQ-TC-NNN` citing the CS/FS-ID (+ RA-INIT-NNN if applicable) | RA-INIT priority: H exhaustive / M sampling / L basic |
| **OQ** | each GxP `FS-<CAT>-NNN` → ≥1 `OQ-TC-NNN` citing FS-ID + RA-INIT-NNN | **RA-DET RPN: ≥12 → positive + negative; 6-9 → positive; 1-4 → GEP/risk-accepted** |
| **PQ** | each business process covering URS prio=H → one `PQ-SCEN-NNN` citing the URS-IDs + RA-INIT-NNN | end-to-end, by end users, production-like; statement of fitness §M7 |

## The RPN→rigor bridge (CORE of the OQ)

This is the reason RA-DET exists. For every function in RA-DET:
- **RPN ≥ 12** → **positive AND negative** test (and stress where the failure mode is performance/resilience). Both `OQ-TC` cite the same `RA-INIT-NNN`.
- **RPN 6-9** → positive (happy path) test.
- **RPN 1-4** → Good Engineering Practice; may be risk-accepted (document it, do not fake coverage).

> **Negative-test attribution (lesson TF2).** A function's negative/resilience test may exercise the FS-ID of the *mitigation* that protects it (e.g. a recording function's resilience is realized by a buffer/reconciliation FS-ID). In that case **cite both FS-IDs** on the `OQ-TC` "Verifies" cell, and make the §6 coverage table agree — so the "every Priority-H function has positive+negative" check passes.

## Special test types (activate per active URS presets)

| If active in URS | Add to OQ |
|---|---|
| URS-EREC | audit-trail test (old/new/reason captured; peer review) |
| URS-ESIG | e-signature test (manifestation + linking + tamper-evidence/negative) |
| URS-SEC | access/MFA test (roles, segregation, MFA enforced — negative on unauthorized) |
| URS-API | interface test (validated end-to-end + failure/retry negative) |

## Risk-based, not exhaustive (GAMP 5 §D5)

*"Not all functionalities will be challenged"* (§25.5). Low-risk GxP functions not tested in the OQ are **documented with risk-acceptance** in §6 — never falsely claim total coverage. They may instead be covered end-to-end in the PQ.

## Anti-hallucination rules (NON-NEGOTIABLE)

1. **Never fabricate test results, evidence, versions, or data.** Protocols are authored at `status: draft`; the "Actual result" / pass columns are blank until real execution.
2. **Never invent environment/baseline/tester values.** Use `[NEEDS CLARIFICATION: …]` for the test environment, installation baseline, and tester/reviewer assignments.
3. **Cite real IDs.** IQ-TC → CS/FS-ID; OQ-TC → FS-ID + RA-INIT-NNN; PQ-SCEN → URS-IDs + RA-INIT-NNN. Never reference an ID not in its source spec.
4. **Tester ≠ Reviewer** (segregation of duties); the PQ is executed by **end users**, not IT.
5. **Never invent citations.** Only the templates' §-refs (GAMP 5 Table 4.1 / §D5 / §8.5.4 / §M7, 21 CFR Part 11, EU Annex 11 §9).
6. **Honor `language`.**

## Status semantics

Each protocol is written at `status: draft`. Instance frontmatter per each template's `instance_frontmatter_spec` (IQ/OQ/PQ): `title`, `type: instance`, `based_on_template`, `based_on_template_version`, `system_id`, `traces_to`, `gamp_category`, `status`, `version`, `created`, `updated`, `language` (+ `ra_ref`/`iq_ref`/`oq_ref` cross-refs).

> [!warning] Status-enum gap (finding TF1)
> The IQ/OQ/PQ templates define `status: {draft, in-execution, executed, approved, superseded}`, but the current `validate-frontmatter.py` only accepts `{draft, in-review, approved, superseded}`. Author protocols at `status: draft` (validates cleanly). The `in-execution`/`executed` states are set at execution time and currently do **not** pass `validate-frontmatter` — flagged for a script fix; do not work around it by inventing a status.

## Post-flight (after writing the protocols)

1. `validate-frontmatter.py` on each of `specs/{IQ,OQ,PQ}.md`.
2. `check-clarification-markers.py specs/IQ.md specs/OQ.md specs/PQ.md --draft`.
3. `generate-rtm.py --specs-dir specs` — regenerate the RTM (now includes the test layers).
4. **Coverage checks**: every GxP FS-ID with Risk Priority=H has both a positive and a negative OQ-TC; every URS prio=H is covered by ≥1 PQ-SCEN; every CS/FS install item has ≥1 IQ-TC.
5. **Print summary**: # IQ-TC / OQ-TC / PQ-SCEN, the high-RPN functions and their pos+neg tests, risk-accepted functions, marker count.
6. **Suggest next**: `/gdd.vr.from-tests` (Validation Report — consumes the IQ/OQ/PQ summaries + the PQ statement of fitness, GAMP 5 §M7) to close the V-Model.

## Output template

See `output-template.md` (this folder) for the exact shape of the three protocols.

## When to refuse

- `.gxp-dev.yaml` / `specs/FS.md` / `specs/RA-DET.md` missing → redirect.
- User asks to fill in "Actual result" / pass columns without real execution → refuse; that is fabricating evidence.
- User asks to claim total OQ coverage when low-risk functions were not tested → refuse; document risk-acceptance instead.
- User asks to have IT execute the PQ → flag; the PQ is executed by end users.
