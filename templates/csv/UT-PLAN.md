---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "UT-PLAN — Unit Test Plan (canonical CSV template)"
type: template
template_class: csv
template_id: "UT-PLAN"
template_version: "0.1.0"
v_model_phase: unit-verification
gamp_categories_applicable: [5]
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# UT-PLAN covers developer-level unit testing of custom code (Cat 5).
# Paired with the DS on the left arm of the V-Model (design → unit test).
# Outputs feed OQ (functional integration), RTM (coverage traceability),
# and VR (validation summary).
inputs:
  - template_id: "DS"
    required: true
    description: "Approved Design Specification — source of the DS-<CATEGORY>-NNN design units that UT-PLAN verifies at code level"
  - template_id: "FS"
    required: true
    description: "Approved Functional Specification — provides functional intent for each unit under test; required for traceability to FS-IDs in OQ/RTM"
  - template_id: "RA-INIT"
    required: true
    description: "Initial Risk Assessment — scales unit-coverage target by Risk Priority (H/M/L); the body and instantiation flow rely on it to set per-module coverage depth"
outputs:
  - artifact: "UT-PLAN instance (Markdown) — executed unit test plan with records"
    consumed_by:
      - "OQ"      # Unit test evidence feeds into OQ coverage of the same FS functions
      - "RTM"     # Requirements Traceability Matrix — unit verification coverage
      - "VR"      # Validation Report — summarizes unit test results

applicable_regulations:
  - "gamp-5"   # §D4 (software development — code review + unit testing for Cat 5) + §D5 (risk-based testing; coverage target by criticality)

based_on:
  - "GAMP 5 §D4 (Cat 5 custom software: formal unit testing required; Tester ≠ Reviewer; coverage proportional to risk) + §D5 (risk-based testing; not all defects need to be found; evidence of supplier/developer testing is sufficient for low-risk units)"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
  system_id:
    type: string
    required: true
  ds_ref:
    type: string
    required: true
    description: "Identifier + version of the DS that this UT-PLAN verifies at unit level"
  fs_ref:
    type: string
    required: true
    description: "Identifier + version of the FS providing functional intent for traceability"
  gamp_category:
    type: enum
    required: true
    values: [5]
  test_framework:
    type: string
    required: true
    description: "Language/framework used for unit testing (e.g. pytest, JUnit, Jest, go test, RSpec)"
  coverage_target_percent:
    type: integer
    required: true
    description: "Minimum line/branch coverage target, scaled by risk (e.g. 80 for H-risk modules, 60 for M-risk, documented risk-acceptance for L-risk)"
  ci_integration:
    type: string
    required: true
    description: "How unit tests are executed in CI (e.g. GitHub Actions workflow name; 'none' if manual only)"
  test_environment:
    type: string
    required: true
    description: "Runtime environment where unit tests execute (OS, language runtime version, relevant dependencies)"
  ut_tester_name:
    type: string
    required: true
    description: "Developer / tester who authors and executes the unit tests"
  ut_reviewer_name:
    type: string
    required: true
    description: "Independent reviewer (must be different from ut_tester_name)"
  org_csv_policy_ref:
    type: string
    required: false
  custom_ref:
    type: string
    required: false

# ─── Instance frontmatter spec ───────────────────────────────────────────────
instance_frontmatter_spec:
  required_fields:
    - title
    - type: "instance"
    - based_on_template: "UT-PLAN"
    - based_on_template_version
    - system_id
    - traces_to            # DS instance + FS instance this UT-PLAN verifies
    - gamp_category        # must be 5
    - status               # draft | in-execution | executed | approved | superseded
    - version
    - created
    - updated
    - language
  conditional_fields:
    - executed_by
    - reviewed_by
    - execution_date
    - coverage_achieved_percent
    - deviations_count

# ─── Validation rules ────────────────────────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "traces_to must point to an approved DS and an approved FS"
  - "gamp_category must be 5 — this template is Cat 5 custom code only"
  - "Tester and Reviewer must be different persons (GAMP 5 §D4 — developer self-review is insufficient)"
  - "Each DS-<CATEGORY>-NNN unit marked as GxP-relevant or Risk Priority=H must have ≥1 UT-PLAN-TC-NNN verifying it"
  - "Each UT-PLAN-TC-NNN must cite the DS-ID (and optionally the FS-ID) it verifies"
  - "Actual result and Passed columns MUST be left blank in the authored draft — never fabricate execution results"
  - "Coverage summary must report achieved vs target; shortfall documented with risk-acceptance (GAMP 5 §D5)"
  - "All deviations must be escalated to the quality function before any corrective action is defined"
  - "CI integration field must be specified (or 'none' with documented rationale)"

tags:
  - template
  - csv
  - unit-test-plan
  - ut-plan
  - unit-verification
  - v-model
  - cat5
  - custom-code
  - canonical
---

# UT-PLAN — Unit Test Plan

> [!note] Canonical CSV template
> **Canonical** template for the **Unit Test Plan (UT-PLAN)** — the developer-level test plan that verifies each unit / module of custom code in **`{{system_name}}`** (GAMP 5 Category 5) conforms to its [DS](DS.md) design specification. It is the innermost right-hand arm of the V-Model, paired with the DS, and constitutes the **earliest formal verification checkpoint** before functional integration testing. Complies with GAMP 5 §D4 (Cat 5 software development obligations — unit testing, code review, Tester ≠ Reviewer) and §D5 (risk-based testing — coverage target scaled by criticality).

> [!warning] Cat 5 scope only
> UT-PLAN applies exclusively to **Category 5 custom-developed code**. Configured or standard software (Cat 3, Cat 4) does not have source units to test at this level — their verification is handled by the [CS](CS.md) + [OQ](OQ.md) path.

> [!tip] Embedded usage rules
> 1. **Design unit → test case** — each DS-<CATEGORY>-NNN design element that is GxP-relevant or Risk Priority=H must be covered by ≥1 `UT-PLAN-TC-NNN`.
> 2. **Tester ≠ Reviewer** — the developer who writes the unit tests cannot be the reviewer who signs off on results (GAMP 5 §D4). Peer review is the minimum acceptable segregation.
> 3. **Risk-based coverage** (GAMP 5 §D5) — coverage target is proportional to risk. Not all units require the same depth. Risk-acceptance is documented for low-risk units that fall below target.
> 4. **Blank at authoring** — the `Actual result` and `Passed` columns must be **blank** when the protocol is authored; they are filled only during execution. Fabricating results is a data integrity violation.
> 5. **CI integration is canonical** — whenever possible, unit tests run automatically in CI so evidence is machine-generated and reproducible.
> 6. **Feeds OQ** — unit test evidence reduces the depth of scripted OQ testing needed for the same functions (risk-based); reference in RTM.
> 7. **Deviations escalated** — any failing test case that cannot be immediately corrected is escalated to the quality function before any action is defined.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **DS being verified** | `{{ds_ref}}` ([DS](DS.md)) |
| **FS providing functional intent** | `{{fs_ref}}` ([FS](FS.md)) |
| **GAMP category** | `{{gamp_category}}` (Cat 5 — custom code) |
| **Test framework** | `{{test_framework}}` |
| **Coverage target** | `{{coverage_target_percent}}`% (scaled by risk per §D5) |
| **CI integration** | `{{ci_integration}}` |
| **Test environment** | `{{test_environment}}` |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Protocol author (SME / Lead developer) |  |  |  |  |
| Approver (System Owner) |  |  |  |  |
| Approver (Quality Unit) |  |  |  |  |
| **Tester** (developer executing tests) | `{{ut_tester_name}}` |  |  |  |
| **Reviewer** (independent) | `{{ut_reviewer_name}}` |  |  |  |

**Overall result**: ☐ Pass ☐ Pass with deviations (see §7) ☐ Fail · **Coverage achieved**: `______`%

---

## 1. Objective

Formally verify, at the **unit / module level**, that each design element of **`{{system_name}}`** specified in the [DS](DS.md) (`{{ds_ref}}`) behaves correctly in isolation: correct output for valid inputs, correct rejection of invalid inputs, correct boundary behavior, and correct error handling. This UT-PLAN constitutes the **unit-level verification** (GAMP 5 §D4), prerequisite evidence for the [OQ](OQ.md) functional test and the [RTM](RTM.md) traceability chain.

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| UT-PLAN | Unit Test Plan — developer-level test plan for Cat 5 custom code (GAMP 5 §D4) |
| Unit under test (UUT) | A single function, class, method, or module tested in isolation |
| Mock / stub | A controlled substitute for an external dependency, used to isolate the UUT |
| Coverage | Percentage of code lines / branches executed by the test suite |
| Risk-based coverage | Coverage target that scales with the Risk Priority of the unit (GAMP 5 §D5) |
| Positive test | Verifies the unit does what it should with valid inputs (happy path) |
| Negative test | Verifies the unit rejects invalid inputs / states correctly |
| Boundary test | Verifies behavior at the edge of valid input ranges |
| CI | Continuous Integration — automated execution of tests on each code commit |
| Risk Priority | Output of RA-INIT that scales the unit testing rigor |

---

## 3. Test requirements and prerequisites

> [!warning] Execution rules
> - Execute only on an **approved copy** of the protocol.
> - Tester must have read and understood the DS and FS before executing.
> - **Tester ≠ Reviewer** (GAMP 5 §D4) — the developer who writes/runs the tests cannot self-approve results.
> - `Actual result` and `Passed` columns are **blank at authoring**; filled only during execution. Never pre-fill.
> - Deviations (failing test cases not immediately corrected) escalated to quality before any corrective action.

| Base document | Reference |
|---|---|
| Design Specification being verified | `{{ds_ref}}` |
| Functional Specification (functional intent) | `{{fs_ref}}` |
| Initial Risk Assessment (scales rigor) | [RA-INIT](RA-INIT.md) |
| Validation Plan | [VP](VP.md) |

---

## 4. Test strategy (risk-based)

> [!note] GAMP 5 §D5 — risk-based testing at unit level
> *"Fundamental to the risk-based approach is an acceptance that not all functionalities will be challenged and consequently not all defects will be found"* (§25.5). Coverage target for unit testing is proportional to the Risk Priority of each module. Low-risk utility code may rely on CI execution + code review as sufficient evidence.

| Risk Priority (RA-INIT) | Required test types | Minimum coverage target |
|---|---|---|
| **H** | Positive + negative + boundary + error-path | `{{coverage_target_percent}}`% (H-tier target) |
| **M** | Positive + selective negative + boundary | Document M-tier target |
| **L** | Positive (happy path) + CI execution evidence | Risk-acceptance documented; lower threshold acceptable |

### 4.1 Test types activated per module

| Test type | When applicable |
|---|---|
| Positive (happy path) | All units |
| Negative (invalid input) | GxP-relevant units, Risk Priority=H/M |
| Boundary / limit | Units with numeric ranges, enumerations, or size constraints |
| Error-path / exception | Units with error handling or fallback logic |
| Mock-based isolation | Units with external dependencies (DB, API, file system, clock) |
| Security-sensitive logic | Units implementing access control, encryption, signing — cite DS-SEC-NNN |
| Data-integrity logic | Units implementing record creation, update, audit trail — cite DS-EREC/DS-DATA-NNN |

### 4.2 Framework and CI configuration

**Test framework**: `{{test_framework}}`
**CI integration**: `{{ci_integration}}`
**Test environment**: `{{test_environment}}`

> [!tip] CI as evidence source
> When tests run in CI on every commit, the CI run log (with pass/fail per test case, coverage report, timestamp, commit SHA) constitutes machine-generated execution evidence. Attach CI run artifacts as Appendix evidence.

---

## 5. Test Cases

> Central section — one block per unit / module under test. Each DS-ID marked GxP-relevant or Risk Priority ≥ M must have ≥1 `UT-PLAN-TC-NNN`. `Actual result` and `Passed` columns are **left blank** at authoring.

### Test Case 1 — `<module/unit name>` — Positive test

**Unit under test**: `<module path or function signature>`
**Objective**: verify that `<unit>` produces the correct output for valid inputs as specified in `DS-<CATEGORY>-NNN`.

| UT-PLAN-TC | Verifies (DS-ID) | FS-ID (intent) | Test step | Input / precondition | Expected result | Actual result | Passed (✓/✗) |
|---|---|---|---|---|---|---|---|
| `UT-PLAN-TC-001` | `DS-FUNC-001` | `FS-FUNC-001` | Call `<function>` with valid input `X` | `X = <value>` | Returns `<expected>` with no exception |  |  |
|  |  |  |  |  |  |  |  |

*Tester / Reviewer signature at close of Test Case 1:* ______ / ______

---

### Test Case 2 — `<module/unit name>` — Negative test

**Unit under test**: `<module path or function signature>`
**Objective**: verify that `<unit>` **rejects** invalid inputs / illegal states as specified in `DS-<CATEGORY>-NNN`.

| UT-PLAN-TC | Verifies (DS-ID) | FS-ID (intent) | Test step | Input / precondition | Expected result (rejection / error) | Actual result | Passed (✓/✗) |
|---|---|---|---|---|---|---|---|
| `UT-PLAN-TC-002` | `DS-FUNC-001` | `FS-FUNC-001` | Call `<function>` with invalid input `Y` | `Y = <invalid value>` | Raises `<ErrorType>` / returns error code `<X>` |  |  |
|  |  |  |  |  |  |  |  |

*Tester / Reviewer signature at close of Test Case 2:* ______ / ______

---

### Test Case 3 — `<module/unit name>` — Boundary test

**Unit under test**: `<module path or function signature>`
**Objective**: verify behavior at the edge of valid input ranges for `DS-<CATEGORY>-NNN`.

| UT-PLAN-TC | Verifies (DS-ID) | FS-ID (intent) | Test step | Input / precondition | Expected result | Actual result | Passed (✓/✗) |
|---|---|---|---|---|---|---|---|
| `UT-PLAN-TC-003` | `DS-FUNC-002` | `FS-FUNC-001` | Call `<function>` at lower boundary | `X = <min>` | Returns `<expected>` |  |  |
| `UT-PLAN-TC-004` | `DS-FUNC-002` | `FS-FUNC-001` | Call `<function>` at upper boundary | `X = <max>` | Returns `<expected>` |  |  |
| `UT-PLAN-TC-005` | `DS-FUNC-002` | `FS-FUNC-001` | Call `<function>` just outside lower boundary | `X = <min - 1>` | Raises `<ErrorType>` / returns error |  |  |

*Tester / Reviewer signature at close of Test Case 3:* ______ / ______

---

### Test Case 4+ — (additional per project)

| UT-PLAN-TC | Verifies (DS-ID) | FS-ID (intent) | Test step | Input / precondition | Expected result | Actual result | Passed (✓/✗) |
|---|---|---|---|---|---|---|---|
| `UT-PLAN-TC-006` |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |

---

## 6. Coverage summary (traceability)

> Confirms that each DS-ID that is GxP-relevant or Risk Priority=H/M has ≥1 `UT-PLAN-TC-NNN`. Units not covered are documented with risk-acceptance rationale (never falsely claimed as covered).

| DS-ID | GxP relevant | Risk Priority | UT-PLAN-TC verifying it | Covered (✓) / Risk-accepted |
|---|---|---|---|---|
| `DS-FUNC-001` | Y |  | `UT-PLAN-TC-001`, `UT-PLAN-TC-002` |  |
| `DS-FUNC-002` | Y |  | `UT-PLAN-TC-003`, `UT-PLAN-TC-004`, `UT-PLAN-TC-005` |  |
| `DS-DATA-001` |  |  |  |  |
|  |  |  |  |  |

**Coverage metric** (if framework reports it):

| Metric | Target | Achieved |
|---|---|---|
| Line coverage (H-risk modules) | `{{coverage_target_percent}}`% |  |
| Branch coverage (H-risk modules) | Document target |  |
| Overall project line coverage | Document target |  |

---

## 7. Deviations

| TC-ID | Expected result | Actual result | Classification | Action | Owner | Date | Resolved |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

> [!warning] Deviation escalation
> Any failing test case that cannot be immediately corrected with a code fix in the same commit **must** be escalated to the quality function. No corrective action (workaround, scope change, risk-acceptance) is defined without quality involvement.

---

## 8. Results summary and conclusion

| Metric | Value |
|---|---|
| Total UT-PLAN-TC | |
| Passed / Failed | |
| Deviations (open / closed) | |
| DS-IDs covered / total GxP-relevant | |
| Risk-accepted units (below coverage target) | |
| Coverage achieved (H-risk modules) | % |
| CI run reference (if applicable) | |

**Conclusion**: ☐ All units verified per DS; ready to feed OQ. ☐ Pass with documented deviations (see §7). ☐ Fail — retest required.

---

## 9. Appendices list (evidence)

| Appendix no. | Description | No. of pages / artifact |
|---|---|---|
| A | CI run log (pass/fail per TC, coverage report, commit SHA, timestamp) | |
| B | Code review record (CR) cross-reference | |
| C | Screenshots / logs of manual test execution (if not CI-automated) | |

---

## 10. Related documents

| Document | Reference |
|---|---|
| Design Specification being verified | `{{ds_ref}}` ([DS](DS.md)) |
| Functional Specification (functional intent) | `{{fs_ref}}` ([FS](FS.md)) |
| Initial Risk Assessment (scales rigor) | [RA-INIT](RA-INIT.md) |
| Code Review Record (Cat 5 companion) | [CR](CR.md) |
| Operational Qualification (next level) | [OQ](OQ.md) |
| Requirements Traceability Matrix | [RTM](RTM.md) |
| Validation Report (summary consumer) | [VR](VR.md) |
| `{{org_csv_policy_ref}}` | |
| `{{custom_ref}}` | |

---

## 11. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue |
|  |  |  |

---

## Canonical notes for implementers

> [!note] UT-PLAN verifies design units in isolation
> Unit tests verify individual functions, methods, or modules with mocks replacing external dependencies. They are **not** integration or functional tests. The [OQ](OQ.md) covers end-to-end functional behavior; UT-PLAN evidence reduces the scripted OQ burden for verified units.

> [!note] Blank Actual/Passed at authoring is a data integrity requirement
> Filling in `Actual result` and `Passed` before execution is a **data integrity violation** equivalent to backdating records. The protocol is authored with these columns blank; they are populated only when tests are run and evidence is captured.

> [!tip] Risk-based coverage is not an excuse to skip GxP units
> GAMP 5 §D5 permits lower coverage for low-risk units — it does not permit skipping units that implement GxP-critical logic (audit trail, e-signature, access control, record integrity). Those must be covered regardless of the general coverage target.

> [!tip] Cat 5 unit testing feeds downstream verification
> Strong unit test coverage (with CI evidence) can reduce the depth of scripted OQ test cases needed for the same functions. Document this rationale explicitly in the OQ and RTM — "unit testing at UT-PLAN-TC-NNN provides base coverage for `FS-FUNC-NNN`; OQ adds integration-level verification only."

> [!tip] Category-awareness
> - **Cat 5**: UT-PLAN is **mandatory** (GAMP 5 §D4). Custom code without unit test evidence is not compliant. The [CR](CR.md) (Code Review Record) is the companion document — both are required for Cat 5 code quality assurance.

## Related

- [DS](DS.md) · [FS](FS.md) · [CR](CR.md) · [OQ](OQ.md) · [RTM](RTM.md) · [VR](VR.md)
- GAMP 5
- V-Model · unit testing · risk based testing

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.tests.from-ds` skill (or the general instantiation skill for Cat 5 projects).

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer project. If it does not exist → redirect to `/gdd.init`.
2. **Confirm `mode: develop`** (or `hybrid`) and `gamp_category: 5` — UT-PLAN is Cat 5 only.
3. **Locate approved DS** (`specs/DS.md`) — source of design units to verify.
4. **Locate approved FS** (`specs/FS.md`) — source of functional intent for traceability.
5. **Locate RA-INIT** (`specs/RA-INIT.md`) — scales coverage target by Risk Priority.
6. **Read `templates/csv/UT-PLAN.md`** from the toolkit as the source template (this file).

### Generation flow

1. **Parse DS-<CATEGORY>-NNN items** from the DS, filtering for GxP-relevant entries and Risk Priority=H/M from RA-INIT.
2. **For each DS-ID**, generate ≥1 `UT-PLAN-TC-NNN`:
   - For Risk Priority=H → generate positive + negative + boundary tests.
   - For Risk Priority=M → generate positive + selective negative.
   - For Risk Priority=L → generate positive only + document risk-acceptance in coverage summary.
   - Cite DS-ID + FS-ID (from FS, for forward traceability) in each test case row.
3. **Activate special test types** per DS content:
   - DS-SEC-NNN → security-sensitive logic tests (access control, encryption, signing).
   - DS-EREC-NNN / DS-DATA-NNN → data-integrity logic tests (record creation, audit trail, update).
   - DS-FLOW-NNN with external I/O → mock-based isolation tests.
4. **Anti-hallucination**: use `[NEEDS CLARIFICATION: ...]` when a DS-ID is ambiguous or a placeholder cannot be filled from available context; never fabricate test results or preconditions.
5. **Leave Actual result and Passed columns blank** — always. This is a data integrity rule, not a formatting preference.
6. **Output**: write `specs/UT-PLAN.md` (status: draft); print coverage plan (DS-IDs covered / total GxP-relevant).
7. **Post-flight**: `validate-frontmatter.py` + `check-clarification-markers.py` + `generate-rtm.py`.

### `status` transitions

```
draft ──[complete protocol + approved]──> in-execution
in-execution ──[tests executed + CI evidence attached]──> executed
executed ──[reviewer signs + deviations closed or risk-accepted]──> approved
approved ──[new version issued]──> superseded
```

### Mapping

| Origin (UT-PLAN) | Destination | Rule |
|---|---|---|
| `UT-PLAN-TC-NNN` | Row in `RTM.md` | Unit verification coverage for the DS-ID |
| UT-PLAN approved | Input to `OQ.md` | OQ acknowledges unit evidence; may reduce scripted OQ depth |
| UT-PLAN summary | `VR.md` | The Validation Report summarizes unit test results alongside OQ/PQ |
| CI coverage report | Appendix A | Machine-generated evidence; attach run artifact with commit SHA |
