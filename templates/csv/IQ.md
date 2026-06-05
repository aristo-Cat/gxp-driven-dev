---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "IQ — Installation Qualification (canonical CSV template)"
type: template
template_class: csv
template_id: "IQ"
template_version: "0.1.0"
v_model_phase: installation-verification
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-28
updated: 2026-05-29
# Round 2 (2026-05-29): translated to English canonical (was language: es). §-citations + IDs preserved verbatim.

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# IQ is the right arm of the V-Model paired with DS/HW (installation
# verification, GAMP 5 Table 4.1). Verifies that the system was installed
# in conformance with the design. Pre-requisite of OQ.
inputs:
  - template_id: "DS"
    required: false
    description: "Design Specification (Cat 5) — source of the DS-<CATEGORY>-NNN installation items to verify"
  - template_id: "FS"
    required: false
    description: "Functional Specification — for Cat 3/4 where the FS absorbs the design/installation spec"
  - template_id: "RA-INIT"
    required: true
    description: "Initial Risk Assessment — scales the IQ rigor by Risk Priority"
outputs:
  - artifact: "IQ instance (Markdown) — executed installation qualification"
    consumed_by:
      - "OQ"        # IQ must be complete before OQ (pre-requisite)
      - "RTM"       # Requirements Traceability Matrix — installation coverage
      - "VR"        # Validation Report — summary of IQ results
applicable_regulations:
  - "gamp-5"          # Table 4.1 (IQ → installation verification) + §D5 testing + §M11 infra
  - "21-cfr-part-11"  # §11.10.a validation evidence
  - "eu-annex-11"     # §9 Qualification and Validation (follows Annex 15)
based_on:
  - "GAMP 5 Table 4.1 (IQ = installation verification) + §D5 (risk-based testing) + §M11 (IT infrastructure qualification)"
  - "Structure: test protocol that verifies the installation against DS/HW; each installation item → ≥1 test step; traceability IQ-TC↔DS/HW"

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
    required: false
    description: "Identifier + version of the DS/FS that defines the installation to be verified"
  ra_ref:
    type: string
    required: true
    description: "Identifier + version of the RA-INIT that scales the rigor of this IQ"
  gamp_category:
    type: enum
    required: true
    values: [3, 4, 5]
    description: "GAMP category inherited from RA-INIT"
  test_environment:
    type: string
    required: true
    description: "Environment where the IQ is executed: server, OS, network, DB, clients"
  iq_tester_name:
    type: string
    required: true
  iq_reviewer_name:
    type: string
    required: true
    description: "Reviewer independent of the tester (GAMP segregation)"
  installation_baseline:
    type: string
    required: true
    description: "Expected configuration baseline (sw versions, parameters, builds)"
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
    - based_on_template: "IQ"
    - based_on_template_version
    - system_id
    - traces_to            # DS/FS instance that defines the installation
    - gamp_category
    - status               # draft | in-execution | executed | approved | superseded
    - version
    - created
    - updated
    - language
  conditional_fields:
    - executed_by: "tester who executed (mandatory if status >= executed)"
    - reviewed_by: "independent reviewer (mandatory if status == approved)"
    - execution_date
    - partial_test_ref: "reference number if partial execution / selective retest"
    - deviations_count: "number of deviations recorded during execution"

# ─── Validation rules (subset Round 1) ──────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "traces_to must point to an approved DS or FS (the IQ verifies a specified installation)"
  - "ra_ref must point to an approved RA-INIT (IQ rigor is scaled by Risk Priority)"
  - "Each DS/HW installation item must have ≥1 IQ-TC-NNN test step verifying it"
  - "Each IQ-TC-NNN must cite the DS/HW/FS-ID it verifies + the associated risk RA-INIT-NNN (if applicable)"
  - "Tester and Reviewer must be different persons (segregation of duties)"
  - "Every deviation must be escalated to the quality function before defining corrective action"
  - "IQ must be status: approved before OQ can reach status: approved (V-Model pre-requisite)"

tags:
  - template
  - csv
  - installation-qualification
  - iq
  - verification
  - v-model
  - canonical
---

# IQ — Installation Qualification

> [!note] Canonical CSV template
> **Canonical** template for the **Installation Qualification (IQ)** — the test protocol that verifies that the system **`{{system_name}}`** was installed in conformance with its design specification ([DS](DS.md) for Cat 5, or [FS](FS.md) for Cat 3/4). It is the right arm of the V-Model paired with the design/installation phase. Complies with GAMP 5 Table 4.1 (IQ = *installation verification*), §D5 (risk-based testing) and §M11 (qualified IT infrastructure).

> [!warning] GAMP 5 §4.2.6.4 terminology note
> GAMP 5 2nd Ed **does not use** "IQ/OQ/PQ" as life-cycle activity terminology — it uses *installation / functional / fitness verification*. The filename `IQ.md` is retained by industrial CSV convention; internally it is equivalent to **installation verification** (Table 4.1: IQ → installation verification).

> [!tip] Embedded usage rules
> 1. **Mirror of design** — the IQ has no logic of its own: each DS/HW installation item generates ≥1 test step. The IQ verifies *presence and correctness* of the installation.
> 2. **Pre-requisite of OQ** — the IQ must be completed and approved **before** the OQ (there is no point in testing functions on an unverified installation).
> 3. **Risk-based rigor** (GAMP 5 §D5) — depth is scaled by the Risk Priority from [RA-INIT](RA-INIT.md). Not every item is verified with the same intensity.
> 4. **Traceability** — each `IQ-TC-NNN` cites the DS/HW/FS-ID it verifies + the associated risk (if applicable).
> 5. **Segregation Tester/Reviewer** — the executor and the reviewer are different persons. The reviewer is independent.
> 6. **No mandatory witnessing** (GAMP 5 §8.5.4) — a witness and per-step initialing are *not* required; the audit trail and automated evidence replace unnecessary secondary evidence.
> 7. **Evidence with metadata** — screenshots/printouts must contain: date+time, Test ID, tester initials, reference to the script, and total page count.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **Design/spec being verified** | `{{ds_ref}}` ([DS](DS.md) / [FS](FS.md)) |
| **RA that scales the rigor** | `{{ra_ref}}` ([RA-INIT](RA-INIT.md)) |
| **GAMP category** | `{{gamp_category}}` |
| **Test environment** | `{{test_environment}}` |
| **Installation baseline** | `{{installation_baseline}}` |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Protocol author (SME / CSV) |  |  |  |  |
| Approver 1 (System Owner) |  |  |  |  |
| Approver 2 (Quality Unit) |  |  |  |  |
| **Tester** (executes) | `{{iq_tester_name}}` |  |  |  |
| **Reviewer** (independent) | `{{iq_reviewer_name}}` |  |  |  |

**Overall execution result**: ☐ Pass (no deviations) ☐ Pass with non-critical deviations (see §7) ☐ Fail

**Execution no. / Partial test ref**: `__________`

> [!note] Tester prior training
> The tester confirms by signature that the necessary training has been completed (GxP, the [Validation Plan](VP.md), and system operation) before executing the IQ.

---

## 1. Objective

Formally verify that the system **`{{system_name}}`** has been **correctly installed** in conformance with its design/installation specification, in the defined environment, with the expected configuration baseline. This IQ is the **installation verification** (GAMP 5 Table 4.1) and constitutes the pre-requisite of the [OQ](OQ.md) (functional verification).

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| IQ | Installation Qualification — installation verification (GAMP 5 Table 4.1) |
| DS / FS | Design / Functional Specification — defines the installation to be verified |
| Baseline | Expected configuration state (versions, parameters, builds) |
| Test step | Individual verification step with expected vs. actual result |
| Deviation | Difference between expected and actual result that requires evaluation |
| Partial test | Execution of a subset of test steps (selective retest) |

---

## 3. Test requirements and prerequisites

> [!warning] Execution rules (GAMP 5 + data integrity)
> - The IQ is only executed against an **approved copy** of the protocol.
> - The tester must be trained (GxP + VP + system) before executing.
> - Tester and reviewer must be **different persons**.
> - Deviations are escalated to the quality function **before** defining corrective action.

### 3.1 Source documents

| Document | Reference |
|---|---|
| Design/Functional Spec being verified | `{{ds_ref}}` |
| Risk Assessment (scales the rigor) | `{{ra_ref}}` |
| Validation Plan | [VP](VP.md) |

### 3.2 Prerequisites verified before starting

| ID-No. | Prerequisite | Verified (✓) |
|---|---|---|
| `IQ-TC-001` | The installation environment is available and accessible |  |
| `IQ-TC-002` | Installation components/media are available and are the correct version |  |
|  |  |  |

---

## 4. Test strategy (risk-based)

> [!note] GAMP 5 §D5 — risk-based testing
> The rigor of the IQ is scaled by the Risk Priority from RA-INIT. Installation verification is primarily about **presence/correctness** (not positive/negative as in OQ). **Unscripted testing** (exploratory) is permitted as additional coverage where it adds value; witnesses are not mandatory (§8.5.4).

| Risk Priority (from RA-INIT) | IQ verification rigor |
|---|---|
| **H** | Exhaustive verification of all items + documented evidence |
| **M** | Verification of critical items + sampling of the rest |
| **L** | Basic verification + supplier evidence / GEP |

---

## 5. Verification procedure

### 5.1 Prerequisites

(see table §3.2)

### 5.2 Measurement and test equipment

| ID-No. | Required equipment | Available (✓) |
|---|---|---|
| `IQ-TC-003` |  |  |
|  |  |  |

### 5.3 Components to install / verify

> Repeatable section per component. Each DS/HW item → ≥1 test step.

| ID-No. | Verifies (DS/HW/FS-ID) | Risk (RA-INIT-NNN) | Verification step | Expected result | Actual result | Passed (✓/✗) |
|---|---|---|---|---|---|---|
| `IQ-TC-004` | `DS-...-NNN` |  | *e.g.: verify the version of the installed software* | *e.g.: version == baseline* |  |  |
| `IQ-TC-005` | `HW-...-NNN` |  |  |  |  |  |
|  |  |  |  |  |  |  |

### 5.4 Configuration / baseline

| ID-No. | Verifies (DS/FS-ID) | Configuration parameter | Expected value (baseline) | Actual value | Passed (✓/✗) |
|---|---|---|---|---|---|
| `IQ-TC-006` |  |  | `{{installation_baseline}}` |  |  |
|  |  |  |  |  |  |

### 5.5 Connectivity / interfaces / security

| ID-No. | Verifies (DS/FS-ID) | Item (network, interface, security setting) | Expected result | Actual result | Passed (✓/✗) |
|---|---|---|---|---|---|
| `IQ-TC-007` |  |  |  |  |  |
|  |  |  |  |  |  |

### 5.6 Documentation present

| ID-No. | Expected document | Present (✓) |
|---|---|---|
| `IQ-TC-008` | User / operation manual |  |
| `IQ-TC-009` | System description (EU Annex 11 §D6) |  |
|  |  |  |

---

## 6. Additional success criteria

| ID-No. | Supplementary criterion | Expected result | Actual result | Passed (✓/✗) |
|---|---|---|---|---|
| `IQ-TC-010` |  |  |  |  |
|  |  |  |  |  |

---

## 7. Overall evaluation / Deviations

> Consolidate all deviations here. Each one is escalated to the quality function before defining action.

| Test ID | Expected result | Actual result | Evaluation | Action | Responsible | Date | Completed |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

---

## 8. Results summary and conclusion

| Metric | Value |
|---|---|
| Total test steps | |
| Passed | |
| Failed | |
| Deviations (critical / non-critical) | |
| Installation items covered / total | |

**Conclusion**: ☐ The installation was verified in conformance with the design; the system is ready for OQ. ☐ Pass with non-critical deviations documented. ☐ Fail — the installation does not conform to the design.

---

## 9. List of appendices (evidence)

| Appendix no. | Description | No. of pages |
|---|---|---|
|  |  |  |

---

## 10. Related documents

| Document | Reference |
|---|---|
| Design/Functional Spec being verified | `{{ds_ref}}` ([DS](DS.md) / [FS](FS.md)) |
| Risk Assessment | `{{ra_ref}}` ([RA-INIT](RA-INIT.md)) |
| Operational Qualification (next phase) | [OQ](OQ.md) |
| Validation Plan | [VP](VP.md) |
| `{{custom_ref}}` |  |

---

## 11. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue |
|  |  |  |

---

## Canonical notes for implementers

> [!note] IQ verifies installation, not function
> The IQ confirms that the system *is correctly installed* (versions, baseline, connectivity, docs). It does NOT test that functions *operate* — that is the [OQ](OQ.md). Conflating the two is a common mistake.

> [!note] Pre-requisite of OQ (V-Model order)
> The IQ must reach `approved` before the OQ. There is no point in verifying functions on an unconfirmed installation.

> [!tip] Category awareness
> - **Cat 3**: Lightweight IQ — verifies installation of the standard product + config. May be combined with OQ for simple systems.
> - **Cat 4**: IQ verifies installation + configuration baseline (detailed settings are specified in [CS](CS.md)).
> - **Cat 5**: IQ verifies the custom build deployed in conformance with [DS](DS.md).

## Related

- [DS](DS.md) · [FS](FS.md) · [RA-INIT](RA-INIT.md) · [OQ](OQ.md) · [VR](VR.md)
- GAMP 5 · 21 CFR Part 11 · EU Annex 11
- V-Model · installation qualification · specification traceability

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.tests.from-ra` skill.

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer project. If it does not exist → redirect to `/gdd.init`.
2. **Locate the approved DS or FS** (`specs/DS.md` or `specs/FS.md`) — defines the installation to be verified.
3. **Locate the approved RA-INIT** (`specs/RA-INIT.md`) — scales the rigor by Risk Priority.
4. **Read `templates/csv/IQ.md`** from the toolkit as the source template (this file).

### Generation flow

1. **Parse the installation items** from the DS/HW/FS (sw versions, hw, config, connectivity, security, docs).
2. **For each item**, generate ≥1 `IQ-TC-NNN` with: upstream reference (DS/HW/FS-ID), associated risk (RA-INIT-NNN if applicable), verification step, expected result.
3. **Scale the rigor** by Risk Priority (H exhaustive / M sampling / L basic).
4. **Anti-hallucination**: insert `[NEEDS CLARIFICATION: ...]` when environment/baseline information is missing; never fabricate versions, parameters, or test results.
5. **Output**: write `specs/IQ.md` (status: draft); print coverage (installation items covered / total).
6. **Post-flight**: run `validate-frontmatter.py` + `check-clarification-markers.py`.

### `status` transitions

```
draft ──[complete protocol + approved]──> in-execution
in-execution ──[executed + evidence]──> executed
executed ──[reviewer signs + deviations closed]──> approved
approved ──[new version]──> superseded
```

### Mapping

| Origin (IQ) | Destination | Rule |
|---|---|---|
| `IQ-TC-NNN` | Row in `RTM.md` | Installation verification coverage |
| IQ approved | Pre-requisite of `OQ.md` | OQ is not approved without IQ approved |
| IQ summary | `VR.md` | The Validation Report summarizes IQ results |
