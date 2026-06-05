---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "OQ — Operational Qualification (canonical CSV template)"
type: template
template_class: csv
template_id: "OQ"
template_version: "0.1.0"
v_model_phase: functional-verification
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-28
updated: 2026-05-29
# Round 2 (2026-05-29): translated to English canonical (was language: es). §-citations + IDs preserved verbatim.

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# OQ is the right-hand arm of the V-Model paired with the FS (functional
# verification, GAMP 5 Table 4.1). Verifies that the system WORKS per the FS.
# Requires IQ approved. Constitutes the bulk of testing.
inputs:
  - template_id: "FS"
    required: true
    description: "Approved Functional Specification — source of the FS-<CATEGORY>-NNN items that OQ verifies functionally"
  - template_id: "RA-INIT"
    required: true
    description: "Risk Assessment — each function with high Risk Priority requires positive + negative testing"
  - template_id: "IQ"
    required: true
    description: "Approved Installation Qualification — prerequisite (functions are not tested on an unverified installation)"
outputs:
  - artifact: "OQ instance (Markdown) — executed operational qualification"
    consumed_by:
      - "PQ"        # PQ typically follows OQ (fitness under real conditions)
      - "RTM"       # Requirements Traceability Matrix — functional coverage
      - "VR"        # Validation Report — summary of OQ results
applicable_regulations:
  - "gamp-5"          # Table 4.1 (OQ → functional verification) + §D5 (testing) + §8 (efficiency)
  - "21-cfr-part-11"  # §11.10 controls verified functionally
  - "eu-annex-11"     # §9 Qualification and Validation
based_on:
  - "GAMP 5 Table 4.1 (OQ = functional verification) + §D5 (risk-based testing, unscripted encouraged) + §8.5.4 (witnesses unnecessary)"
  - "Structure: functional test protocol; each FS-ID GxP → ≥1 test case; positive + negative tests; rigor scaled by Risk Priority"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
  system_id:
    type: string
    required: true
  fs_ref:
    type: string
    required: true
    description: "Identifier + version of the FS that this OQ verifies functionally"
  ra_ref:
    type: string
    required: true
  iq_ref:
    type: string
    required: true
    description: "Identifier of the approved IQ (prerequisite)"
  gamp_category:
    type: enum
    required: true
    values: [3, 4, 5]
  test_environment:
    type: string
    required: true
    description: "Functional test environment: server, OS, network, DB, clients, test data"
  test_data_strategy:
    type: string
    required: true
    description: "How test data is generated/managed (datasets, test accounts, roles)"
  oq_tester_name:
    type: string
    required: true
  oq_reviewer_name:
    type: string
    required: true
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
    - based_on_template: "OQ"
    - based_on_template_version
    - system_id
    - traces_to            # FS instance being verified
    - gamp_category
    - status               # draft | in-execution | executed | approved | superseded
    - version
    - created
    - updated
    - language
  conditional_fields:
    - executed_by
    - reviewed_by
    - execution_date
    - partial_test_ref
    - deviations_count

# ─── Validation rules (Round 1 subset) ──────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "traces_to must point to an approved FS"
  - "iq_ref must point to an approved IQ (V-Model prerequisite)"
  - "Each FS-<CATEGORY>-NNN with GxP=Y must have ≥1 OQ-TC-NNN that verifies it (functional coverage)"
  - "Each function with Risk Priority=H (from RA-INIT) must have both positive and negative tests"
  - "Each OQ-TC-NNN must cite the FS-ID it verifies + the associated RA-INIT-NNN risk"
  - "Tester and Reviewer must be different persons"
  - "All deviations must be escalated to the quality function before any action is defined"
  - "Not all functions require the same rigor — risk-acceptance documented for low-risk functions (GAMP 5 §D5)"

tags:
  - template
  - csv
  - operational-qualification
  - oq
  - functional-verification
  - v-model
  - canonical
---

# OQ — Operational Qualification

> [!note] Canonical CSV template
> **Canonical** template for the **Operational Qualification (OQ)** — the test protocol that verifies that the system **`{{system_name}}`** **operates** in conformance with its [FS](FS.md). It is the right-hand arm of the V-Model paired with the FS, and the **bulk of functional testing**. Complies with GAMP 5 Table 4.1 (OQ = *functional verification*), §D5 (risk-based testing) and §8 (efficiency: unscripted testing permitted, witnesses unnecessary).

> [!warning] GAMP 5 §4.2.6.4 terminology
> The filename `OQ.md` is retained by industrial CSV convention; internally it corresponds to **functional verification** (Table 4.1: OQ → functional verification). GAMP 5 2nd Ed does not prescribe the term "OQ".

> [!tip] Embedded usage rules
> 1. **Verifies function, not installation** — OQ tests that functions *operate* per the FS. Installation was already verified by the [IQ](IQ.md) (prerequisite).
> 2. **Positive + negative** — each critical function is tested both in its correct behavior (positive) AND in the rejection of forbidden inputs/access (negative). Risk Priority=H requires both.
> 3. **Risk-based depth** (GAMP 5 §D5) — not all functions are challenged equally. Risk-acceptance documented for low risk. *"Not all functionalities will be challenged"* (§D5 §25.5).
> 4. **Unscripted encouraged** — exploratory testing / error-guessing / day-in-the-life counts as coverage (§D5). Not scripted-only.
> 5. **No mandatory witnessing** (§8.5.4) — a witness is not required, nor is initialing every step.
> 6. **Traceability** — each `OQ-TC-NNN` cites the FS-ID it verifies + the associated RA-INIT-NNN risk.
> 7. **Tester/Reviewer segregation** + deviation escalation to quality.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **FS being verified** | `{{fs_ref}}` ([FS](FS.md)) |
| **RA scaling rigor** | `{{ra_ref}}` ([RA-INIT](RA-INIT.md)) |
| **IQ prerequisite** | `{{iq_ref}}` ([IQ](IQ.md) — must be approved) |
| **GAMP category** | `{{gamp_category}}` |
| **Test environment** | `{{test_environment}}` |

### Roles / testers table

> List the system roles used during testing, with the test username and the person who executed it (access traceability).

| System role | Test username | Tester | Initials |
|---|---|---|---|
|  |  |  |  |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Protocol author (SME / CSV) |  |  |  |  |
| Approver 1 (System Owner) |  |  |  |  |
| Approver 2 (Quality Unit) |  |  |  |  |
| **Tester** | `{{oq_tester_name}}` |  |  |  |
| **Reviewer** (independent) | `{{oq_reviewer_name}}` |  |  |  |

**Overall result**: ☐ Pass ☐ Pass with non-critical deviations (see §7) ☐ Fail · **Execution no. / Partial test**: `______`

---

## 1. Objective

Formally verify that the system **`{{system_name}}`** **operates in conformance with its [FS](FS.md)** (`{{fs_ref}}`): each GxP function behaves as specified, rejects forbidden inputs/access, and the regulatory controls (audit trail, electronic signatures, access control) are functional. This OQ constitutes the **functional verification** (GAMP 5 Table 4.1), prerequisite to the [PQ](PQ.md).

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| OQ | Operational Qualification — functional verification (GAMP 5 Table 4.1) |
| Positive test | Verifies that the system does what it should (happy path) |
| Negative test | Verifies that the system rejects what it should not (invalid inputs, unauthorized access) |
| Unscripted test | Exploratory / error-guessing testing without a prior script (counts as coverage, §D5) |
| Test case | Set of test steps sharing a common objective |
| Risk Priority | Output of RA-INIT that scales the testing rigor |

---

## 3. Test requirements and prerequisites

> [!warning] Execution rules
> - Execute only on an **approved copy** of the protocol.
> - Tester must be trained (GxP + VP + FS + system) before executing.
> - **Approved IQ** is a prerequisite (functions are not tested on an unverified installation).
> - Tester ≠ Reviewer. Deviations escalated to quality before any action.

| Base document | Reference |
|---|---|
| Functional Spec being verified | `{{fs_ref}}` |
| Risk Assessment | `{{ra_ref}}` |
| Installation Qualification (pre-req) | `{{iq_ref}}` |
| Validation Plan | [VP](VP.md) |

---

## 4. Test strategy (risk-based)

> [!note] GAMP 5 §D5 — risk-based testing
> *"Fundamental to the risk-based approach is an acceptance that not all functionalities will be challenged and consequently not all defects will be found"* (§25.5 p.218). Coverage = supplier testing + scripted + unscripted + UAT. Rigor is scaled by Risk Priority.

| Risk Priority (RA-INIT) | Required testing type |
|---|---|
| **H** | Positive **+ negative** + boundary/limit + stress/performance where applicable |
| **M** | Positive (happy path) + selective negative |
| **L** | Basic verification + supplier evidence / GEP (risk-acceptance documented) |

### 4.1 Special test types (activate per RA)

| Type | When applicable |
|---|---|
| Access Rights / Security | If URS-SEC/EREC active — verify roles, segregation of duties, MFA |
| Audit trail | If URS-EREC active — verify old/new/reason capture + peer review |
| Electronic signatures | If URS-ESIG active — verify manifestation + linking + tamper-evidence |
| Backup / Restore | If critical — verify restore test (Annex 11 §16.6) |
| Interface | If URS-API active — verify validated interfaces end-to-end |
| Limit Value / Boundary | For functions with ranges / limits |
| Stress / Performance | If URS-PERF with high Risk Priority |

### 4.2 Test environment and data

**Environment**: `{{test_environment}}`
**Test data strategy**: `{{test_data_strategy}}`

---

## 5. Test Cases

> Central section, repeatable per test case. Each FS-ID GxP → ≥1 test case. Each test step cites its FS-ID + risk.

### Test Case 1 — `<name>` — Positive test

**Objective**: verify the expected behavior of `<function>`.

| OQ-TC | Verifies (FS-ID) | Risk (RA-INIT-NNN) | Test step | Expected result | Actual result / evidence / deviation no. | Passed (✓/✗) |
|---|---|---|---|---|---|---|
| `OQ-TC-001` | `FS-FUNC-001` |  |  |  |  |  |
|  |  |  |  |  |  |  |

*Tester / Reviewer signature at close of Test Case 1:* ______ / ______

### Test Case 2 — `<name>` — Negative test

**Objective**: verify that the system **rejects** invalid inputs / unauthorized access.

| OQ-TC | Verifies (FS-ID) | Risk (RA-INIT-NNN) | Test step | Expected result (rejection) | Actual result / evidence | Passed (✓/✗) |
|---|---|---|---|---|---|---|
| `OQ-TC-002` | `FS-SEC-001` |  | *e.g.: attempt access with invalid credentials* | *e.g.: access denied + attempt logged* |  |  |
|  |  |  |  |  |  |  |

*Tester / Reviewer signature at close of Test Case 2:* ______ / ______

### Test Case 3+ — (additional per project)

| OQ-TC | Verifies (FS-ID) | Risk | Test step | Expected result | Actual result | Passed |
|---|---|---|---|---|---|---|
| `OQ-TC-003` |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

---

## 6. Functional coverage (traceability summary)

> Confirms that each FS-ID GxP has ≥1 OQ-TC. Low-risk functions not tested are documented with risk-acceptance.

| FS-ID | GxP | Risk Priority | OQ-TC verifying it | Covered (✓) / Risk-accepted |
|---|---|---|---|---|
| `FS-FUNC-001` |  |  | `OQ-TC-001` |  |
|  |  |  |  |  |

---

## 7. Overall evaluation / Deviations

| Test ID | Expected result | Actual result | Evaluation | Action | Owner | Date | Completed |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

---

## 8. Results summary and conclusion

| Metric | Value |
|---|---|
| Total OQ-TC | |
| Passed / Failed | |
| Deviations (critical / non-critical) | |
| GxP FS-IDs covered / total | |
| Risk-accepted functions (not tested) | |

**Conclusion**: ☐ System operates per the FS; ready for PQ. ☐ Pass with non-critical deviations. ☐ Fail.

---

## 9. Appendices list (evidence)

| Appendix no. | Description | No. of pages |
|---|---|---|
|  |  |  |

---

## 10. Related documents

| Document | Reference |
|---|---|
| Functional Spec being verified | `{{fs_ref}}` ([FS](FS.md)) |
| Risk Assessment | `{{ra_ref}}` ([RA-INIT](RA-INIT.md)) |
| Installation Qualification (pre-req) | `{{iq_ref}}` ([IQ](IQ.md)) |
| Performance Qualification (next phase) | [PQ](PQ.md) |
| `{{custom_ref}}` |  |

---

## 11. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue |
|  |  |  |

---

## Canonical notes for implementers

> [!note] OQ verifies function in the test environment
> OQ tests that functions operate per the FS, typically in a test environment (not production). Fitness for intended use under real conditions with real users is the scope of the [PQ](PQ.md).

> [!note] Positive + negative is canonical
> GAMP 5 + CSV practice: critical functions are tested in both directions. An access control must be verified both by allowing the authorized user (positive) and by rejecting the unauthorized user (negative).

> [!tip] Risk-based, not exhaustive
> GAMP 5 §D5 explicitly accepts that not all functions are challenged. Low-risk untested functions are documented with risk-acceptance — coverage is NOT falsely claimed as total.

> [!tip] Category-awareness
> - **Cat 3**: OQ verifies the standard configured functionality that is used. May be combined with IQ/PQ for simple systems.
> - **Cat 4**: OQ verifies the configuration + business-process functional testing.
> - **Cat 5**: OQ covers the full chain (includes integration verification + regression of custom code).

## Related

- [FS](FS.md) · [RA-INIT](RA-INIT.md) · [IQ](IQ.md) · [PQ](PQ.md) · [VR](VR.md)
- GAMP 5 · 21 CFR Part 11 · EU Annex 11
- V-Model · operational qualification · risk based testing

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.tests.from-ra` skill.

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer project. If it does not exist → redirect to `/gdd.init`.
2. **Locate approved FS** (`specs/FS.md`) — source of functions to verify.
3. **Locate approved RA-INIT** (`specs/RA-INIT.md`) — scales rigor + defines positive/negative.
4. **Confirm approved IQ** (`specs/IQ.md`) — prerequisite. If absent → warn.
5. **Read `templates/csv/OQ.md`** from the toolkit as the source template (this file).

### Generation flow

1. **Parse the FS-<CATEGORY>-NNN items with GxP=Y** from the FS.
2. **For each FS-ID**, generate ≥1 `OQ-TC-NNN`:
   - Inherit Risk Priority from RA-INIT.
   - If Risk Priority=H → generate both positive **and** negative test.
   - Cite FS-ID + risk RA-INIT-NNN.
3. **Activate special test types** per URS presets (audit trail if EREC, e-sig if ESIG, access/MFA if SEC, interfaces if API).
4. **Document risk-acceptance** for low-risk functions not tested (do not falsely claim total coverage).
5. **Anti-hallucination**: use `[NEEDS CLARIFICATION: ...]` when information is missing; never fabricate test results or data.
6. **Output**: write `specs/OQ.md` (status: draft); print functional coverage (GxP FS-IDs covered / total).
7. **Post-flight**: `validate-frontmatter.py` + `check-clarification-markers.py` + `generate-rtm.py`.

### `status` transitions

```
draft ──[complete protocol + approved + IQ approved]──> in-execution
in-execution ──[executed + evidence]──> executed
executed ──[reviewer signs + deviations closed]──> approved
approved ──[new version issued]──> superseded
```

### Mapping

| Origin (OQ) | Destination | Rule |
|---|---|---|
| `OQ-TC-NNN` | Row in `RTM.md` | Functional verification coverage |
| OQ approved | Typically precedes `PQ.md` | Fitness under real conditions after function verified |
| OQ summary | `VR.md` | The Validation Report summarizes OQ results |
