---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "IT-PLAN — Integration Test Plan (canonical CSV template)"
type: template
template_class: csv
template_id: "IT-PLAN"
template_version: "0.1.0"
v_model_phase: integration-verification
gamp_categories_applicable: [4, 5]
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# IT-PLAN sits on the right-hand arm of the V-Model, between the FS/API-SPEC
# (left-arm specs) and the OQ (functional verification). It verifies that
# modules and interfaces between systems work together end-to-end — data flows
# correctly across boundaries and validated interfaces meet GAMP 5 §D5 and
# EU Annex 11 §10 requirements. An approved IT-PLAN feeds the OQ, RTM, and VR.
inputs:
  - template_id: "FS"
    required: true
    description: "Approved Functional Specification — source of FS-API-NNN and FS-FLOW-NNN items that define integration points to verify"
  - template_id: "API-SPEC"
    required: false
    description: "API Specification — defines interface contracts (endpoints, data schemas, protocols) tested by this plan"
  - template_id: "RA-INIT"
    required: false
    description: "Initial Risk Assessment — scales integration testing rigor; High-risk interfaces require positive + failure/retry testing"
outputs:
  - artifact: "IT-PLAN instance (Markdown) — executed integration test plan with results"
    consumed_by:
      - "OQ"    # OQ functional verification builds on verified interfaces
      - "RTM"   # Requirements Traceability Matrix — integration coverage
      - "VR"    # Validation Report — summary of integration test results
applicable_regulations:
  - "gamp-5"       # §D5 (risk-based testing approach) + integration-testing activity within functional verification (Table 4.1)
  - "eu-annex-11"  # §10 (validated interfaces — data integrity across system boundaries)
based_on:
  - "GAMP 5 §D5 (risk-based testing; not all interfaces challenged equally) + the integration-testing activity within functional verification (Table 4.1)"
  - "EU Annex 11 §10 (validated interfaces: data integrity, error handling, and audit across system boundaries)"
  - "Structure: integration test protocol; each FS-API/FS-FLOW/API-SPEC-ID → ≥1 IT-PLAN-TC; positive + failure/retry for GxP interfaces; rigor scaled by Risk Priority"

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
    description: "Identifier + version of the FS that defines the integration points this plan verifies"
  api_spec_ref:
    type: string
    required: false
    description: "Identifier + version of the API Specification (if applicable)"
  ra_ref:
    type: string
    required: false
    description: "Identifier of the Risk Assessment that scales integration testing rigor"
  gamp_category:
    type: enum
    required: true
    values: [4, 5]
  test_environment:
    type: string
    required: true
    description: "Integration test environment: systems under test, network topology, test data stores, protocol versions"
  test_data_strategy:
    type: string
    required: true
    description: "How integration test data is generated/managed (synthetic datasets, mock endpoints, test accounts)"
  it_tester_name:
    type: string
    required: true
  it_reviewer_name:
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
    - based_on_template: "IT-PLAN"
    - based_on_template_version
    - system_id
    - traces_to            # FS instance defining the integration points
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
    - api_spec_ref
    - deviations_count

# ─── Validation rules ────────────────────────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "traces_to must point to an approved FS"
  - "Each FS-API-NNN and FS-FLOW-NNN with GxP=Y must have ≥1 IT-PLAN-TC-NNN that verifies the integration point"
  - "Each API-SPEC-ID referenced in an IT-PLAN-TC must be traceable to a FS-API-NNN or FS-FLOW-NNN"
  - "Each interface with Risk Priority=H (from RA-INIT) must have both a positive test AND a failure/retry test"
  - "Each IT-PLAN-TC-NNN must cite the FS-ID (or API-SPEC-ID) it verifies"
  - "Tester and Reviewer must be different persons"
  - "All deviations must be escalated to the quality function before any corrective action is defined"
  - "Data-integrity assertions must be explicit: the test step states the expected payload/field values at the receiving boundary"
  - "Actual result and Passed columns must be blank at status: draft — never fabricate results"

tags:
  - template
  - csv
  - integration-test
  - it-plan
  - integration-verification
  - v-model
  - canonical
---

# IT-PLAN — Integration Test Plan

> [!note] Canonical CSV template
> **Canonical** template for the **Integration Test Plan (IT-PLAN)** — the test protocol that verifies that **modules and interfaces between systems** in **`{{system_name}}`** work together **end-to-end**: data flows correctly across boundaries, interface contracts are met, and error/retry conditions are handled correctly. Realizes [FS](FS.md) items of type `FS-API` and `FS-FLOW`, as well as [API-SPEC](API-SPEC.md) interface contracts. Feeds [OQ](OQ.md), [RTM](RTM.md), and [VR](VR.md). Complies with GAMP 5 §D5 (risk-based testing) and EU Annex 11 §10 (validated interfaces).

> [!warning] Scope boundary
> IT-PLAN verifies **interface contracts and data-flow integrity across system boundaries**. It does NOT verify individual functional behaviors within a single system boundary — that is the scope of the [OQ](OQ.md). An approved IT-PLAN is typically a prerequisite evidence package for the OQ, not a replacement.

> [!tip] Embedded usage rules
> 1. **Integration points as the unit of testing** — each `IT-PLAN-TC-NNN` targets one interface boundary or data-flow path. The test step explicitly states what enters the boundary and what must exit on the other side.
> 2. **Positive + failure/retry** (GAMP 5 §D5 + EU Annex 11 §10) — GxP interfaces require both a positive flow test AND a failure/retry test (e.g., network interruption, malformed payload, retry idempotency).
> 3. **Data-integrity assertions are mandatory** — the expected result must state the exact field values, record counts, or checksums expected at the receiving system. Vague "data arrives" is not a valid expected result.
> 4. **Risk-based depth** — not all interfaces are challenged equally. Low-risk interfaces may use supplier evidence or reduced testing with documented risk-acceptance (GAMP 5 §D5 §25.5).
> 5. **EU Annex 11 §10 anchor** — validated interfaces must demonstrate that data is not altered, that errors are detected and reported, and that audit-trail events are generated on both sides of the boundary where applicable.
> 6. **Tester/Reviewer segregation** + deviation escalation to quality before any action.
> 7. **Actual/Passed blank at draft** — never populate results in the template or at status: draft.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **FS defining integration points** | `{{fs_ref}}` ([FS](FS.md)) |
| **API Specification** | `{{api_spec_ref}}` ([API-SPEC](API-SPEC.md)) — if applicable |
| **RA scaling rigor** | `{{ra_ref}}` ([RA-INIT](RA-INIT.md)) — if available |
| **GAMP category** | `{{gamp_category}}` |
| **Test environment** | `{{test_environment}}` |

### Integration interfaces table

> List every interface boundary in scope. Rows added or removed per project.

| Interface ID | Source system | Target system | Protocol / method | In scope (Y/N) | Notes |
|---|---|---|---|---|---|
| `IF-001` |  |  |  |  |  |
| `IF-002` |  |  |  |  |  |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Protocol author (SME / CSV) |  |  |  |  |
| Approver 1 (System Owner) |  |  |  |  |
| Approver 2 (Quality Unit) |  |  |  |  |
| **Tester** | `{{it_tester_name}}` |  |  |  |
| **Reviewer** (independent) | `{{it_reviewer_name}}` |  |  |  |

**Overall result**: ☐ Pass ☐ Pass with non-critical deviations (see §7) ☐ Fail · **Execution no. / Partial test**: `______`

---

## 1. Objective

Formally verify that the interfaces and data flows within **`{{system_name}}`** (`{{system_id}}`) operate in conformance with the integration points defined in the [FS](FS.md) (`{{fs_ref}}`): data transits boundaries without alteration, error conditions are detected and handled correctly, retry/recovery logic operates as designed, and interface audit events are generated where required by EU Annex 11 §10. This IT-PLAN constitutes the **integration verification** evidence for the V-Model, prerequisite to the [OQ](OQ.md).

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| IT-PLAN | Integration Test Plan — protocol for verifying interfaces and data flows across system boundaries |
| Integration point | A defined boundary where two or more systems exchange data (API call, message queue, file transfer, database link, etc.) |
| Positive integration test | Verifies that a valid payload is transmitted, received, and processed correctly across the boundary |
| Failure/retry test | Verifies that an error condition (network fault, malformed payload, timeout, duplicate message) is detected, reported, and handled correctly; retry logic is idempotent |
| Data-integrity assertion | An explicit expected-result statement specifying field values, record counts, or checksums at the receiving boundary |
| Validated interface | An interface for which documented evidence exists that data integrity, error detection, and appropriate audit events are assured (EU Annex 11 §10) |
| Risk Priority | Output of RA-INIT that scales the integration testing rigor (H / M / L) |

---

## 3. Test requirements and prerequisites

> [!warning] Execution rules
> - Execute only on an **approved copy** of this protocol.
> - Tester must be trained (GxP + VP + FS + API-SPEC + system) before executing.
> - All referenced systems must be at the correct version/configuration before integration tests begin.
> - Tester ≠ Reviewer. Deviations escalated to quality before any corrective action.
> - Test environment must be representative of the production interface topology (protocols, authentication, data encoding).

| Base document | Reference |
|---|---|
| Functional Spec (integration points) | `{{fs_ref}}` |
| API Specification | `{{api_spec_ref}}` — if applicable |
| Risk Assessment | `{{ra_ref}}` — if available |
| Validation Plan | [VP](VP.md) |

---

## 4. Test strategy

> [!note] GAMP 5 §D5 + EU Annex 11 §10 — risk-based integration testing
> *"Fundamental to the risk-based approach is an acceptance that not all functionalities will be challenged"* (GAMP 5 §D5 §25.5 p.218). Coverage across integration points is scaled by Risk Priority. EU Annex 11 §10 requires that validated interfaces demonstrate data integrity, error detection, and — where applicable — audit-trail generation at the boundary.

### 4.1 Integration points in scope

> Document every interface boundary that has a corresponding `FS-API-NNN`, `FS-FLOW-NNN`, or `API-SPEC-ID`. Low-risk interfaces may be covered by supplier evidence with documented risk-acceptance rather than scripted tests.

| FS-ID / API-SPEC-ID | Description | Risk Priority | Test approach |
|---|---|---|---|
| `FS-API-001` | *e.g. inbound order message from upstream system* |  |  |
| `FS-FLOW-001` | *e.g. outbound audit event to central log aggregator* |  |  |

### 4.2 Data-flow integrity

Each IT-PLAN-TC must assert data integrity across the boundary:
- **Payload completeness**: all required fields present at the receiver
- **Field-value fidelity**: numeric, date, and string values unchanged in transit
- **Record count**: no records dropped or duplicated
- **Encoding/transformation**: character encoding, unit conversion, or schema mapping applied correctly

### 4.3 Interface validation per EU Annex 11 §10

For GxP-critical interfaces, each IT-PLAN-TC verifies:
- Data is not altered in transit (integrity check or checksum)
- Errors are detected and reported with sufficient detail for investigation
- Audit-trail events are generated on the relevant system(s) at the boundary where required

### 4.4 Error, failure, and retry paths

For each GxP interface with Risk Priority=H, a failure/retry test case is required:
- **Error injection**: simulate a network fault, timeout, or malformed payload
- **Detection**: system detects the error within the defined window
- **Reporting**: error is logged with sufficient context (source, target, timestamp, error code)
- **Recovery / retry**: retry logic (if defined) is idempotent — no duplicate records, no data loss

### 4.5 Risk-based depth

| Risk Priority (RA-INIT) | Required testing |
|---|---|
| **H** | Positive flow + failure/retry + data-integrity assertion + audit event check (where applicable) |
| **M** | Positive flow + selective error-path test |
| **L** | Basic connectivity/smoke + supplier evidence or risk-acceptance documented |

### 4.6 Test environment and data

**Environment**: `{{test_environment}}`
**Test data strategy**: `{{test_data_strategy}}`

---

## 5. Test Cases

> Central section, repeatable per test case. Each `FS-API-NNN`, `FS-FLOW-NNN`, or `API-SPEC-ID` with GxP=Y → ≥1 IT-PLAN-TC. Each test step must include a data-integrity assertion.

### Test Case 1 — `<name>` — Positive integration test

**Objective**: verify that a valid payload traverses `<integration point>` end-to-end without alteration.

| IT-PLAN-TC | Verifies (FS-API / FS-FLOW / API-SPEC-ID) | Integration point | Test step | Expected result | Actual result / evidence / deviation no. | Passed (✓/✗) |
|---|---|---|---|---|---|---|
| `IT-PLAN-TC-001` | `FS-API-001` | *e.g. System A → System B via REST POST /records* | *e.g. Submit a valid record payload with all required fields populated* | *e.g. HTTP 201 returned; record appears in System B with all field values identical to submitted payload; no error logged* |  |  |
|  |  |  |  |  |  |  |

*Tester / Reviewer signature at close of Test Case 1:* ______ / ______

### Test Case 2 — `<name>` — Failure / retry test (GxP interface)

**Objective**: verify that `<integration point>` detects, reports, and recovers from a failure condition; retry is idempotent.

| IT-PLAN-TC | Verifies (FS-API / FS-FLOW / API-SPEC-ID) | Integration point | Test step | Expected result | Actual result / evidence / deviation no. | Passed (✓/✗) |
|---|---|---|---|---|---|---|
| `IT-PLAN-TC-002` | `FS-API-001` | *e.g. System A → System B via REST POST /records* | *e.g. Simulate network interruption mid-transmission; after recovery, resubmit the same payload* | *e.g. Error logged with source, target, timestamp, and error code; on retry, exactly one record created in System B — no duplicate; audit event generated* |  |  |
|  |  |  |  |  |  |  |

*Tester / Reviewer signature at close of Test Case 2:* ______ / ______

### Test Case 3+ — (additional per project)

| IT-PLAN-TC | Verifies (FS-API / FS-FLOW / API-SPEC-ID) | Integration point | Test step | Expected result | Actual result / deviation no. | Passed |
|---|---|---|---|---|---|---|
| `IT-PLAN-TC-003` |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

---

## 6. Integration coverage (traceability summary)

> Confirms that each `FS-API-NNN` / `FS-FLOW-NNN` / `API-SPEC-ID` with GxP=Y has ≥1 IT-PLAN-TC. Low-risk interfaces not scripted are documented with risk-acceptance (GAMP 5 §D5).

| FS-ID / API-SPEC-ID | GxP | Risk Priority | IT-PLAN-TC verifying it | Covered (✓) / Risk-accepted |
|---|---|---|---|---|
| `FS-API-001` |  |  | `IT-PLAN-TC-001`, `IT-PLAN-TC-002` |  |
| `FS-FLOW-001` |  |  |  |  |
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
| Total IT-PLAN-TC | |
| Passed / Failed | |
| Deviations (critical / non-critical) | |
| GxP integration points covered / total | |
| Risk-accepted interfaces (not scripted) | |

**Conclusion**: ☐ All GxP interfaces verified; integration evidence ready for OQ. ☐ Pass with non-critical deviations. ☐ Fail.

---

## 9. Appendices list (evidence)

| Appendix no. | Description | No. of pages |
|---|---|---|
|  |  |  |

---

## 10. Related documents

| Document | Reference |
|---|---|
| Functional Spec (integration points) | `{{fs_ref}}` ([FS](FS.md)) |
| API Specification | `{{api_spec_ref}}` ([API-SPEC](API-SPEC.md)) |
| Risk Assessment | `{{ra_ref}}` ([RA-INIT](RA-INIT.md)) |
| Operational Qualification (next phase) | [OQ](OQ.md) |
| Requirements Traceability Matrix | [RTM](RTM.md) |
| Validation Report | [VR](VR.md) |
| `{{org_csv_policy_ref}}` |  |
| `{{custom_ref}}` |  |

---

## 11. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue |
|  |  |  |

---

## Canonical notes for implementers

> [!note] IT-PLAN verifies interfaces, not functions
> IT-PLAN tests that data flows correctly across system boundaries and that interface contracts are fulfilled. It does NOT verify that individual functions within a system operate correctly — that is the scope of the [OQ](OQ.md). The two protocols are complementary: IT-PLAN verifies the integration layer; OQ verifies the functional layer.

> [!note] EU Annex 11 §10 — validated interfaces
> EU Annex 11 §10 requires that interfaces between systems are validated. This means: (a) data integrity is assured across the boundary (no silent alteration or loss), (b) errors are detected and reported, and (c) audit-trail events are generated on the relevant systems at the boundary where required by GxP. IT-PLAN is the primary vehicle for satisfying this requirement.

> [!tip] Data-integrity assertions are non-negotiable for GxP interfaces
> A test step that only verifies "data arrived" without asserting specific field values, record counts, or checksums is insufficient for a GxP interface. The expected result must be specific enough that a different actual result would be unambiguously detectable.

> [!tip] Failure/retry testing is distinct from negative testing
> Negative testing (OQ scope) verifies that the system rejects unauthorized inputs or access. Failure/retry testing (IT-PLAN scope) verifies that the integration layer survives infrastructure failures, retries idempotently, and does not corrupt or duplicate GxP records in the process. Both are required for GxP interfaces; they belong in different protocols.

> [!tip] Category-awareness
> - **Cat 4**: IT-PLAN verifies interfaces between the configured product and external systems (e.g., data exports to reporting tools, inbound reference data feeds). Focus on configuration-driven integration points.
> - **Cat 5**: IT-PLAN additionally covers custom-code integration layers (adapters, middleware, ETL pipelines). Includes regression testing of integration code after each change.

## Related

- [FS](FS.md) · [API-SPEC](API-SPEC.md) · [RA-INIT](RA-INIT.md) · [OQ](OQ.md) · [RTM](RTM.md) · [VR](VR.md)
- GAMP 5 · EU Annex 11
- V-Model · integration testing · data integrity

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.it-plan.from-fs` skill.

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer project. If it does not exist → redirect to `/gdd.init`.
2. **Locate approved FS** (`specs/FS.md`) — source of `FS-API-NNN` and `FS-FLOW-NNN` items that define integration points.
3. **Locate API-SPEC** (`specs/API-SPEC.md`) if present — interface contracts to verify.
4. **Locate RA-INIT** (`specs/RA-INIT.md`) if present — scales rigor + determines positive/failure-retry requirement.
5. **Read `templates/csv/IT-PLAN.md`** from the toolkit as the source template (this file).

### Generation flow

1. **Parse `FS-API-NNN` and `FS-FLOW-NNN` items with GxP=Y** from the FS; also parse all `API-SPEC-ID` entries from the API-SPEC if present.
2. **For each integration point**, generate ≥1 `IT-PLAN-TC-NNN`:
   - Populate "Integration point" column with source → target + protocol.
   - Include a data-integrity assertion in "Expected result" (specific field values, record counts, or checksums).
   - Inherit Risk Priority from RA-INIT if available.
   - If Risk Priority=H (or no RA available and GxP=Y) → generate both a positive test **and** a failure/retry test.
   - Cite the FS-ID or API-SPEC-ID in "Verifies" column.
3. **Activate audit-event checks** for interfaces where EU Annex 11 §10 applies (data alteration prevention + error detection + audit trail).
4. **Document risk-acceptance** for low-risk interfaces not scripted (do not falsely claim total coverage).
5. **Anti-hallucination**: use `[NEEDS CLARIFICATION: ...]` when interface details are missing; never fabricate test results, field values, or endpoint URLs.
6. **Output**: write `specs/IT-PLAN.md` (status: draft); print integration coverage (GxP integration points covered / total).
7. **Post-flight**: `validate-frontmatter.py` + `check-clarification-markers.py` + `generate-rtm.py`.

### `status` transitions

```
draft ──[complete protocol + approved]──> in-execution
in-execution ──[executed + evidence captured]──> executed
executed ──[reviewer signs + deviations closed]──> approved
approved ──[new version issued]──> superseded
```

### Mapping

| Origin (IT-PLAN) | Destination | Rule |
|---|---|---|
| `IT-PLAN-TC-NNN` | Row in `RTM.md` | Integration coverage evidence |
| IT-PLAN approved | Feeds `OQ.md` | OQ functional verification builds on verified interfaces |
| IT-PLAN summary | `VR.md` | Validation Report summarizes IT-PLAN results |
| `FS-API-NNN` / `FS-FLOW-NNN` / `API-SPEC-ID` → IT-PLAN-TC coverage | `RTM.md` | Forward traceability per requirement-id-scheme |
