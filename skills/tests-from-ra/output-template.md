# `gdd.tests.from-ra` — Output Template Reference

The exact shapes of the three protocols produced by the skill. Each mirrors its canonical template (`templates/csv/IQ.md`, `OQ.md`, `PQ.md`). Worked, validated examples: `examples/temp-logger-gmp-chamber/specs/{IQ,OQ,PQ}.md` (IQ 15 IQ-TC, OQ 14 OQ-TC with 4 high-RPN functions pos+neg, PQ 4 PQ-SCEN + §M7 fitness statement).

---

## Common frontmatter (all three, instance shape)

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
status: draft                  # protocol authored; NOT in-execution/executed (see TF1 note)
version: "0.1"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
language: "{{language}}"
# cross-refs as applicable: ra_ref (all), iq_ref (OQ), oq_ref (PQ)
---
```

- **IQ** `traces_to`: CS (Cat 4) / DS (Cat 5) + FS. **OQ** `traces_to`: FS. **PQ** `traces_to`: URS.
- All three: `status: draft`. The `executed_by`/`reviewed_by`/`execution_date` fields are set at execution.

---

## IQ instance (mirror `templates/csv/IQ.md`)

Sections: §0 identity + signatures (author/approvers + **Tester** + independent **Reviewer**) + overall-result checkboxes (unmarked); §1 objective; §4 risk-based strategy; §5 verification procedure — §3.2 prerequisites, §5.2 equipment, §5.3 components (`IQ-TC | Verifies (CS/FS-ID) | Risk (RA-INIT) | step | expected | actual | passed`), §5.4 config baseline against CS, §5.5 connectivity/interfaces/security, §5.6 documentation; §8 summary (counts); §10 related; §11 revision.
Each `IQ-TC-NNN` cites a real CS/FS-ID. "Actual result" / "Passed" blank. Environment/baseline unknowns → `[NEEDS CLARIFICATION:]`.

## OQ instance (mirror `templates/csv/OQ.md`)

Sections: §0 identity (FS + **IQ prerequisite** + RA) + roles/testers table + signatures + result checkboxes; §1 objective; §4 risk-based strategy + special test types; §5 **Test Cases** (positive + negative, one table per case): `OQ-TC | Verifies (FS-ID) | Risk (RA-INIT) | step | expected | actual | passed`; §6 **functional coverage** table; §8 summary; §10 related; §11 revision.
- RPN≥12 functions: a positive AND a negative test case.
- Negative/resilience test may cite **both** the function FS-ID and the mitigation FS-ID (TF2); §6 must agree.
- §6 lists low-risk functions as **risk-accepted** (not falsely covered).

## PQ instance (mirror `templates/csv/PQ.md`)

Sections: §0 identity (URS + **OQ prerequisite** + RA) + **end-user executors** table + signatures (author = Process Owner) + result checkboxes; §1 objective; §4 risk-based end-to-end strategy; §5 **scenarios** `PQ-SCEN-NNN` (each: Covers URS-IDs + Risk + executing **end-user** role + step table); §6 fitness coverage (URS prio=H → PQ-SCEN); §8 summary + **`> [!quote]` statement of fitness (§M7)** left unmarked; §10 related; §11 revision.
Scenarios are complete business processes, not isolated functions.

---

## Anti-patterns in the output (all three)

Do NOT produce:
- ❌ Filled "Actual result" / "Passed" columns or a marked pass/fail/fitness checkbox (protocols are authored, executed later — filling them is fabricating evidence).
- ❌ `status: in-execution` / `executed` at authoring time (and note: those currently fail `validate-frontmatter` — TF1).
- ❌ A Priority-H (RPN≥12) function in the OQ without **both** a positive and a negative test.
- ❌ A claim of total OQ coverage when low-risk functions were untested (document risk-acceptance per §D5).
- ❌ A `PQ-SCEN` that is an isolated function rather than an end-to-end business process; or a PQ executed by IT rather than end users.
- ❌ A test ID citing a source ID not present in its spec (IQ-TC→CS/FS, OQ-TC→FS+RA-INIT, PQ-SCEN→URS+RA-INIT).
- ❌ Invented versions/baselines/test data (use `[NEEDS CLARIFICATION:]`).
- ❌ Regulatory §-citations beyond the templates' (GAMP 5 Table 4.1/§D5/§8.5.4/§M7, 21 CFR Part 11, EU Annex 11 §9).
- ❌ `status: approved`, or any banned legacy category code / corporate identifier (see the anonymization rule in `CLAUDE.md`).
