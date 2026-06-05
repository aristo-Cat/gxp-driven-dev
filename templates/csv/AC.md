---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "AC — Acceptance Criteria (canonical CSV template)"
type: template
template_class: csv
template_id: "AC"
template_version: "0.1.0"
v_model_phase: requirements-definition
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# AC bridges the specification arm (URS/FS) to the verification arm (OQ/PQ).
# Not a root: depends on URS and optionally FS.
inputs:
  - template_id: "URS"
    required: true
    description: "Approved (or draft) User Requirements Specification — primary source of requirements that the ACs verify. Each URS-<CATEGORY>-NNN with prio=H must have ≥1 AC."
  - template_id: "FS"
    required: false
    description: "Functional Specification — optional secondary source. ACs may target FS-<CATEGORY>-NNN when the requirement is expressed at the realization level rather than the user level."
outputs:
  - artifact: "AC instance (Markdown)"
    consumed_by:
      - "OQ"        # Operational Qualification — AC rows become or directly feed OQ test cases
      - "PQ"        # Performance Qualification — process-level ACs become PQ scenarios
      - "RTM"       # Requirements Traceability Matrix — AC-<CATEGORY>-NNN fills the verification column
applicable_regulations:
  - "gamp-5"          # §D1 Specifying Requirements — ACs make requirements testable; §D5 test planning
based_on:
  - "GAMP 5 §D1 (Specifying Requirements) — testable criteria as part of requirements definition"
  - "GAMP 5 §D5 (Testing) — Given/When/Then (GWT) as a structured test-intent format"
  - "V-Model: AC sits at the specification/verification inflection point — left arm close-out, right arm entry gate"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
    description: "Human-readable name of the system (must match the source URS and FS)"
    example: "QC LIMS at site A"
  system_id:
    type: string
    required: true
    description: "Unique system identifier (same as the source URS and FS)"
  urs_ref:
    type: string
    required: true
    description: "Identifier + version of the URS instance this AC set is based on"
    example: "URS-PROJ-2026-001 v1.0 (approved)"
  fs_ref:
    type: string
    required: false
    description: "Identifier + version of the FS instance (if ACs also target FS-IDs)"
    example: "FS-PROJ-2026-001 v1.0 (approved)"
  gamp_category:
    type: enum
    required: true
    values: [3, 4, 5]
    description: "GAMP 5 category (inherited from RA-INIT / URS). Cat 1/2 do not typically require structured ACs."
  ac_author_name:
    type: string
    required: true
  ac_author_dept:
    type: string
    required: true
  scope_statement:
    type: string
    required: true
    description: "Brief statement of which URS/FS scope this AC document covers (full system or specific modules/categories)"
    example: "All URS-FUNC, URS-EREC, URS-ESIG, and URS-PERF requirements for the QC LIMS."
  test_environment:
    type: string
    required: false
    description: "Test environment or context where the ACs will be executed (e.g., validated OQ environment, staging environment)"
  org_csv_policy_ref:
    type: string
    required: false
  custom_ref:
    type: string
    required: false

# ─── INSTANCE frontmatter spec (not the template's) ─────────────────────────
instance_frontmatter_spec:
  required_fields:
    - title
    - type: "instance"
    - based_on_template: "AC"
    - based_on_template_version
    - system_id
    - traces_to            # URS instance ID + version (and FS instance ID if applicable)
    - status               # draft | in-review | approved | superseded
    - version              # instance's own semver
    - created
    - updated
    - language
  conditional_fields:
    - approved_by: "required if status == approved"
    - supersedes: "version of the previous AC if this is a new revision"
    - fs_ref: "required if any AC-IDs cite FS-<CATEGORY>-NNN as upstream"

# ─── Validation rules ────────────────────────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "traces_to must point to a URS instance (status: approved recommended; status: draft acceptable for early AC drafting)"
  - "Each AC-<CATEGORY>-NNN row must cite at least one upstream URS-<CATEGORY>-NNN or FS-<CATEGORY>-NNN in the 'Verifies' column"
  - "Each AC row must have non-empty Given, When, and Then columns — partially filled rows are invalid"
  - "The 'Then' column must be binary and objectively verifiable: avoid subjective language ('correctly', 'well', 'fast') without a measurable threshold"
  - "Each URS-<CATEGORY>-NNN with prio=H must have ≥1 AC entry verifying it (prio=H without an AC = blocking gap)"
  - "The 'Test layer' column must be one of: OQ | PQ | both — no other values"
  - "An AC-<CATEGORY>-NNN that has no downstream OQ-TC-NNN or PQ-SCEN-NNN is an unexecuted criterion (tracked as gap in RTM)"
  - "Signature block must include an identified Quality Unit reviewer (GAMP 5 §D5)"
  - "No deletion of AC rows — obsolete ACs are struck through (~~AC-FUNC-003: ...~~) to preserve traceability"

tags:
  - template
  - csv
  - ac
  - acceptance-criteria
  - given-when-then
  - v-model
  - cascade
  - canonical
---

# AC — Acceptance Criteria

> [!note] Canonical CSV template
> **Canonical** template for producing the **Acceptance Criteria (AC)** of a computerized system. Each AC defines a testable, binary condition in **Given / When / Then (GWT)** form that establishes "done" for a requirement and feeds directly into [OQ](OQ.md) and [PQ](PQ.md) test cases. The AC is the **inflection point** of the V-Model: it closes the specification arm (left) and opens the verification arm (right). Complies with GAMP 5 §D1 (Specifying Requirements — testable criteria) and §D5 (Testing).

> [!tip] Embedded usage rules
> 1. **Binary outcome** — every AC must have a result that is either PASS or FAIL with no ambiguity. If the Then cannot be evaluated objectively, rewrite it with a measurable threshold.
> 2. **One AC per distinct verifiable condition** — a single URS requirement may generate multiple ACs (1:N) when it covers multiple behaviours or edge cases.
> 3. **Minimum coverage** — each `URS-<CATEGORY>-NNN` with prio=H must have ≥1 AC. Requirements with prio=M/L should have ACs; requirements with GxP=N may be omitted at the author's discretion.
> 4. **Test layer assignment** — assign each AC to the appropriate test layer: **OQ** (functional behaviour verified in a controlled environment) or **PQ** (process-level, real-world conditions) or **both** when warranted.
> 5. **No-deletion rule** — an obsolete AC is **not** deleted: it is struck through (`~~AC-FUNC-007~~`). Deleting breaks the URS↔AC↔OQ/PQ traceability chain.
> 6. **Category mirrors upstream** — the CATEGORY in `AC-<CATEGORY>-NNN` mirrors the CATEGORY of the upstream requirement (`URS-FUNC-001` → `AC-FUNC-001`). This preserves forward traceability across the V-Model.
> 7. **GWT is not a test script** — the Given/When/Then describes test intent, not step-by-step execution. Detailed test steps live in `OQ.md` and `PQ.md`.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **URS being verified** | `{{urs_ref}}` |
| **FS being verified** | `{{fs_ref}}` *(if applicable)* |
| **GAMP category** | `{{gamp_category}}` *(inherited from [Risk Analysis](RA-INIT.md) / URS)* |
| **Scope** | `{{scope_statement}}` |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Author | `{{ac_author_name}}` | `{{ac_author_dept}}` |  |  |
| Reviewer 1 (System Owner / IT) |  |  |  |  |
| Reviewer 2 (SME / Process Owner) |  |  |  |  |
| Reviewer 3 (Quality Unit) *(GAMP 5 §D5)* |  |  |  |  |
| Approver (System Owner) |  |  |  |  |

> [!note] Who authors the AC
> Typically the **CSV Manager / Validation Coordinator** in collaboration with the **Process Owner** and **SME**. For Cat 5 custom software, the development team drafts the ACs from the FS; the regulated organization reviews and approves. For Cat 3/4, the ACs may be drafted from the URS before the FS is complete.

---

## 1. Introduction

This **Acceptance Criteria (AC)** document defines the testable, binary conditions that determine when each requirement in `{{urs_ref}}` (and, if applicable, `{{fs_ref}}`) is satisfied. It constitutes the **acceptance gateway** of the CSV V-Model: the specification arm (URS → FS) is closed when all requirements have ≥1 AC; the verification arm (OQ → PQ) is opened by executing those ACs.

According to GAMP 5 §D1, requirements must be testable. The AC document makes testability explicit and traceable — each `AC-<CATEGORY>-NNN` maps to a specific `URS-<CATEGORY>-NNN` (or `FS-<CATEGORY>-NNN`) and declares the exact observable outcome that constitutes fulfillment.

**Scope of this AC set**: `{{scope_statement}}`

> [!note] Relationship between AC, OQ, and PQ
> - **AC** defines *what* counts as done (test intent, Given/When/Then).
> - **OQ** (`OQ-TC-NNN`) defines *how* to execute the verification (steps, data, expected results) in a controlled test environment. Each AC with Test layer = OQ generates ≥1 `OQ-TC-NNN`.
> - **PQ** (`PQ-SCEN-NNN`) verifies the system works under real-world process conditions. Each AC with Test layer = PQ generates ≥1 `PQ-SCEN-NNN`.
> - **RTM** tracks the full chain: `URS-ID → AC-ID → OQ-TC-NNN / PQ-SCEN-NNN → Pass/Fail`.

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| AC | Acceptance Criteria — testable, binary conditions that define when a requirement is satisfied |
| GWT | Given / When / Then — structured format for expressing a testable condition |
| URS | User Requirements Specification — the "what" from the user's perspective |
| FS | Functional Specification — the technical "how" that realizes the URS |
| OQ | Operational Qualification — functional verification in a controlled environment (GAMP 5 §D5) |
| PQ | Performance Qualification — process-level verification under real-world conditions (GAMP 5 §D5) |
| RTM | Requirements Traceability Matrix — cross-document traceability record |
| GAMP 5 | Good Automated Manufacturing Practice 5, ISPE 2022 |
| Prio=H | Priority High — requirement is critical; ≥1 AC is mandatory |
| GxP=Y | Requirement has a GxP impact; must be covered in verification |
| Binary | A test outcome that is unambiguously PASS or FAIL with no partial states |
|  |  |

---

## 3. Coverage rules

| Rule | Detail |
|---|---|
| **Mandatory coverage** | Each `URS-<CATEGORY>-NNN` with prio=H must have ≥1 AC row verifying it. A prio=H requirement without an AC is a **blocking gap** that prevents the AC from reaching status: approved. |
| **Recommended coverage** | Each `URS-<CATEGORY>-NNN` with prio=M should have ≥1 AC. |
| **Optional coverage** | Requirements with prio=L and GxP=N may be omitted at the author's discretion and documented in section 4.1. |
| **FS-level ACs** | When an FS exists, ACs may also target `FS-<CATEGORY>-NNN` (e.g., to verify a specific technical mechanism). These are recommended for prio=H realizations in Cat 4/5. |
| **Cardinality** | 1:N — one requirement may have multiple ACs covering distinct conditions (happy path, boundary, error path). |
| **No 1:0 for prio=H** | One requirement + zero ACs = blocking gap for any GxP=Y or prio=H requirement. |

---

## 4. Acceptance criteria table

> [!tip] Reading the table
> - **AC-ID**: `AC-<CATEGORY>-NNN` — mirrors the category of the upstream requirement.
> - **Verifies**: the upstream `URS-<CATEGORY>-NNN` (or `FS-<CATEGORY>-NNN`) this AC validates.
> - **Given**: the pre-condition or system state before the action.
> - **When**: the specific action or event that triggers the behaviour.
> - **Then**: the expected, observable, binary outcome. Must be objectively measurable — no subjective terms.
> - **Test layer**: `OQ` | `PQ` | `both` — which qualification protocol executes this AC.

> [!warning] Binary Then — anti-patterns to avoid
> - WRONG: "The system processes the record correctly." → Not binary; "correctly" is subjective.
> - WRONG: "The response is fast." → Not measurable; add a threshold (e.g., "≤2 seconds").
> - CORRECT: "The audit trail entry is written within 1 second, contains user_id, timestamp_utc, old_value, new_value, and reason; no entry is modifiable via the UI."

### 4.1 Functional — `AC-FUNC-NNN`

| AC-ID | Verifies (URS/FS-ID) | Given | When | Then | Test layer |
|---|---|---|---|---|---|
| `AC-FUNC-001` | `URS-FUNC-001` | *e.g.: The system is running and the operator is authenticated with role = Analyst.* | *e.g.: The operator submits a new sample registration form with all mandatory fields populated.* | *e.g.: The sample record is created with a unique system-assigned ID, status = Registered, and the submission timestamp is recorded; no error is displayed.* | OQ |
| `AC-FUNC-002` | `URS-FUNC-001` | *e.g.: A sample is in status = Registered.* | *e.g.: The operator attempts to submit the same registration form a second time (duplicate sample ID).* | *e.g.: The system rejects the submission with error code DUP-001 and the duplicate record is not created in the database.* | OQ |
|  |  |  |  |  |  |

### 4.2 Electronic Records — `AC-EREC-NNN`

> [!warning] Mandatory section if URS-EREC is active
> Each `URS-EREC-NNN` with prio=H must have ≥1 AC verifying the control. ACs here typically verify audit trail immutability, record integrity, ALCOA+ attributes, and retention.

| AC-ID | Verifies (URS/FS-ID) | Given | When | Then | Test layer |
|---|---|---|---|---|---|
| `AC-EREC-001` | `URS-EREC-001` | *e.g.: A GxP record exists in the system with a known checksum.* | *e.g.: A database administrator attempts to directly modify the record value via a DB client (bypassing the application).* | *e.g.: The integrity check flag on the record is set to invalid and the discrepancy is captured in the audit trail; the application UI displays a data integrity warning on the next read.* | OQ |
| `AC-EREC-005` | `URS-EREC-005` | *e.g.: An authenticated user with role = Analyst modifies a GxP field value.* | *e.g.: The user saves the change and provides a reason for change.* | *e.g.: An audit trail entry is written within 1 second containing: user_id, role, old_value, new_value, reason, and timestamp_utc; the entry is not editable or deletable via any application function.* | OQ |
|  |  |  |  |  |  |

### 4.3 Electronic Signatures — `AC-ESIG-NNN`

> [!warning] Mandatory section if URS-ESIG is active

| AC-ID | Verifies (URS/FS-ID) | Given | When | Then | Test layer |
|---|---|---|---|---|---|
| `AC-ESIG-002` | `URS-ESIG-002` | *e.g.: A record is pending approval and the approver is authenticated.* | *e.g.: The approver applies an electronic signature by re-entering their credentials and selecting meaning = "Approved".* | *e.g.: The signed record displays the approver's full name, timestamp_utc, and meaning = "Approved" in both the on-screen view and the PDF rendition; the signature cannot be removed without leaving an audit trail entry.* | OQ |
|  |  |  |  |  |  |

### 4.4 Data structure — `AC-DATA-NNN`

| AC-ID | Verifies (URS/FS-ID) | Given | When | Then | Test layer |
|---|---|---|---|---|---|
| `AC-DATA-001` | `URS-DATA-001` | *e.g.: The system is configured with the production data schema.* | *e.g.: A record is created via the application with all mandatory fields.* | *e.g.: All mandatory fields are stored in the database with the correct data types and constraints; no mandatory field contains a null value.* | OQ |
|  |  |  |  |  |  |

### 4.5 Data flow — `AC-FLOW-NNN`

| AC-ID | Verifies (URS/FS-ID) | Given | When | Then | Test layer |
|---|---|---|---|---|---|
| `AC-FLOW-001` | `URS-FLOW-001` | *e.g.: The integration interface to the upstream system is active.* | *e.g.: The upstream system sends a valid data payload to the integration endpoint.* | *e.g.: The payload is received, validated against the schema, stored, and a confirmation acknowledgement is returned within the agreed SLA; a transfer log entry with correlation_id is written.* | OQ |
|  |  |  |  |  |  |

### 4.6 Reports and listings — `AC-REPORT-NNN`

| AC-ID | Verifies (URS/FS-ID) | Given | When | Then | Test layer |
|---|---|---|---|---|---|
| `AC-REPORT-001` | `URS-REPORT-001` | *e.g.: At least 10 sample records in status = Released exist in the system.* | *e.g.: The user generates the standard batch release report with a date range that includes all 10 records.* | *e.g.: The report contains all 10 records with the correct data, is generated within 10 seconds, and can be exported to PDF with an intact audit footer.* | OQ |
|  |  |  |  |  |  |

### 4.7 Data security — `AC-SEC-NNN`

| AC-ID | Verifies (URS/FS-ID) | Given | When | Then | Test layer |
|---|---|---|---|---|---|
| `AC-SEC-001` | `URS-SEC-001` | *e.g.: The system is running in the production environment with at-rest and in-transit encryption configured.* | *e.g.: A network capture is performed on the communication channel between client and server.* | *e.g.: All traffic is encrypted with TLS 1.3 or higher; no plaintext GxP data is visible in the capture.* | OQ |
| `AC-SEC-002` | `URS-SEC-002` | *e.g.: A user account is registered and MFA is mandatory for remote access.* | *e.g.: The user attempts to log in from an IP address outside the corporate network perimeter without completing the MFA challenge.* | *e.g.: The login is rejected and an access-denied event is written to the security audit log; the user is not granted any session.* | OQ |
|  |  |  |  |  |  |

### 4.8 Performance — `AC-PERF-NNN`

| AC-ID | Verifies (URS/FS-ID) | Given | When | Then | Test layer |
|---|---|---|---|---|---|
| `AC-PERF-001` | `URS-PERF-001` | *e.g.: The test environment matches the production hardware sizing and 100 simulated concurrent users are active.* | *e.g.: A standard batch query is executed simultaneously by all 100 users.* | *e.g.: 95% of responses are returned in ≤2 seconds; no error response is returned; no data corruption is detected post-test.* | OQ |
|  |  |  |  |  |  |

### 4.9 Process organization — `AC-PROC-NNN`

| AC-ID | Verifies (URS/FS-ID) | Given | When | Then | Test layer |
|---|---|---|---|---|---|
| `AC-PROC-001` | `URS-PROC-001` | *e.g.: The system is operational and the required SOPs have been issued and are in force.* | *e.g.: The process is executed end-to-end under real operational conditions by trained personnel.* | *e.g.: The process is completed according to the SOP without deviation; the system records and audit trail accurately reflect each step; no manual workaround is required.* | PQ |
|  |  |  |  |  |  |

### 4.10 User Interface — `AC-UI-NNN`

| AC-ID | Verifies (URS/FS-ID) | Given | When | Then | Test layer |
|---|---|---|---|---|---|
| `AC-UI-001` | `URS-UI-001` | *e.g.: The user is authenticated and the main dashboard is loaded.* | *e.g.: The user performs any action that results in a validation error.* | *e.g.: The error message is displayed in the language of the user's locale, references the specific field in error, and does not expose internal system details (stack trace, DB query, etc.).* | OQ |
|  |  |  |  |  |  |

### 4.11 Interfaces — `AC-API-NNN`

> [!warning] Mandatory section if URS-API is active (validated interfaces preset)

| AC-ID | Verifies (URS/FS-ID) | Given | When | Then | Test layer |
|---|---|---|---|---|---|
| `AC-API-001` | `URS-API-001` | *e.g.: The integration interface is configured and active; the downstream system is available.* | *e.g.: An invalid payload (schema violation) is sent to the integration endpoint.* | *e.g.: The system rejects the payload with HTTP 422, logs the rejection with the correlation_id and error detail, and does not store any partial data.* | OQ |
|  |  |  |  |  |  |

### 4.12 Data migration — `AC-MIGR-NNN`

> [!warning] Mandatory section if URS-MIGR is active (validated migration preset)

| AC-ID | Verifies (URS/FS-ID) | Given | When | Then | Test layer |
|---|---|---|---|---|---|
| `AC-MIGR-001` | `URS-MIGR-001` | *e.g.: The migration tool has been executed against the legacy dataset in the test environment.* | *e.g.: A reconciliation count is performed between the legacy source and the target system.* | *e.g.: 100% of records migrate successfully; the record count matches exactly; all mandatory fields are populated; no data truncation or character encoding errors are detected; the migration log is complete.* | OQ |
|  |  |  |  |  |  |

### 4.13 Archiving — `AC-ARCH-NNN`

| AC-ID | Verifies (URS/FS-ID) | Given | When | Then | Test layer |
|---|---|---|---|---|---|
| `AC-ARCH-001` | `URS-ARCH-001` | *e.g.: GxP records have been archived to the designated archive system.* | *e.g.: A retrieval request is made for a specific archived record by its unique identifier.* | *e.g.: The record is retrieved within the agreed SLA, is identical (byte-for-byte) to the pre-archive checksum, and is presented in a human-readable format without specialist software.* | OQ |
|  |  |  |  |  |  |

### 4.14 System operations — `AC-OPS-NNN`

| AC-ID | Verifies (URS/FS-ID) | Given | When | Then | Test layer |
|---|---|---|---|---|---|
| `AC-OPS-001` | `URS-OPS-001` | *e.g.: A full backup has been performed and stored.* | *e.g.: A recovery drill is executed from the backup to a clean environment.* | *e.g.: The system is restored to operational state within the agreed RTO; all GxP data is intact and consistent; the backup integrity log confirms no corruption.* | PQ |
|  |  |  |  |  |  |

### 4.15 Training — `AC-TRAIN-NNN`

| AC-ID | Verifies (URS/FS-ID) | Given | When | Then | Test layer |
|---|---|---|---|---|---|
| `AC-TRAIN-001` | `URS-TRAIN-001` | *e.g.: Training material for end users is available and the training record system is active.* | *e.g.: A new user is granted system access.* | *e.g.: The system enforces that the user has a completed training record for the applicable role before the first login; access is blocked until the training record is confirmed.* | OQ |
|  |  |  |  |  |  |

### 4.16 Testing requirements — `AC-TEST-NNN`

| AC-ID | Verifies (URS/FS-ID) | Given | When | Then | Test layer |
|---|---|---|---|---|---|
| `AC-TEST-001` | `URS-TEST-001` | *e.g.: The test environment is provisioned and the validation test plan is approved.* | *e.g.: Qualification testing is executed.* | *e.g.: All test cases designated as mandatory in the Validation Plan are executed and documented; no critical defect remains open at the time of the Validation Report sign-off.* | OQ |
|  |  |  |  |  |  |

---

## 5. URS → AC traceability summary

> [!tip] Master coverage index
> This table is the **traceability summary** between requirements and their acceptance criteria. Populate it after all AC rows are authored. The `generate-rtm` skill uses this table (together with OQ/PQ) to build the full RTM chain: `URS-ID → AC-ID → OQ-TC-NNN / PQ-SCEN-NNN`.

| URS-ID (or FS-ID) | Statement (summary) | AC-ID(s) | Cardinality | GxP | Prio | Test layer | Gap? |
|---|---|---|---|---|---|---|---|
| `URS-FUNC-001` |  | `AC-FUNC-001`, `AC-FUNC-002` | 1:N | Y | H | OQ | No |
| `URS-EREC-005` |  | `AC-EREC-005` | 1:1 | Y | H | OQ | No |
|  |  |  |  |  |  |  |  |

**Gap legend**:

| Gap? | Meaning |
|---|---|
| No | ≥1 AC covers this requirement |
| **BLOCKING** | prio=H or GxP=Y with zero ACs — prevents status: approved |
| Deferred | prio=L or GxP=N, intentionally deferred (documented) |

---

## 6. Related documents

| Document | Reference |
|---|---|
| URS verified by this AC set | `{{urs_ref}}` ([URS](URS.md)) |
| FS verified by this AC set | `{{fs_ref}}` ([FS](FS.md)) *(if applicable)* |
| Organization's CSV Policy | `{{org_csv_policy_ref}}` |
| Validation Plan | [VP](VP.md) |
| Operational Qualification | [OQ](OQ.md) |
| Performance Qualification | [PQ](PQ.md) |
| Requirements Traceability Matrix | [RTM](RTM.md) |
| `{{custom_ref}}` |  |

---

## 7. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{ac_author_name}}`, `{{ac_author_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] The AC is the specification-to-verification bridge
> The AC closes the left arm of the V-Model (specification) and opens the right arm (verification). A requirement without an AC is specified but not yet verifiable — GAMP 5 §D1 considers testability a quality attribute of requirements. An AC without a downstream `OQ-TC-NNN` or `PQ-SCEN-NNN` is intent without execution — the RTM tracks this gap.

> [!note] Given/When/Then — intent, not execution steps
> GWT is a **test-intent format**, not a test script. The Given establishes the pre-condition; the When is the single triggering action; the Then is the observable, binary outcome. Detailed execution steps, test data setup, and pass/fail recording belong in `OQ.md` and `PQ.md`. Keep GWT concise and implementation-agnostic where possible.

> [!note] Category-awareness — AC depth by GAMP category
> - **Cat 3** (standard product): ACs focus on URS-level requirements. Configuration-specific behaviours (from the CS) may be covered with targeted ACs.
> - **Cat 4** (configured): ACs may additionally target `FS-<CATEGORY>-NNN` or `CS-<CATEGORY>-NNN` to verify configured parameters.
> - **Cat 5** (custom): comprehensive ACs at both URS and FS level; unit/integration test coverage (UT-PLAN, IT-PLAN) is separate and complements the OQ/PQ-level ACs.

> [!tip] Natural output of this template
> A well-authored AC set produces the **verification column** of the traceability matrix: each `URS-<CATEGORY>-NNN` → `AC-<CATEGORY>-NNN` (1:1 or 1:N) → `OQ-TC-NNN` / `PQ-SCEN-NNN` → Pass/Fail result. Section 5 is the master index of that traceability.

## Related

- [URS](URS.md) · [FS](FS.md) · [OQ](OQ.md) · [PQ](PQ.md) · [RTM](RTM.md)
- GAMP 5
- V-Model · acceptance criteria · specification traceability

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.ac.from-urs` skill.

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer project. If it does not exist → redirect to `/gdd.init`.
2. **Locate the URS instance** (`specs/URS.md`). If it does not exist → **stop**: an AC set without a URS has no requirements to verify. Inform the user.
3. **Locate the FS instance** (`specs/FS.md`) if it exists — load it to allow FS-level ACs.
4. **Read `templates/csv/AC.md`** from the toolkit as the source template (this file).

### Generation flow (cascade from URS/FS)

1. **Parse all `URS-<CATEGORY>-NNN`** from the URS, with their GxP (Y/N) and prio (H/M/L).
2. **If FS exists**, additionally parse all `FS-<CATEGORY>-NNN` with prio=H.
3. **For each requirement**, propose ≥1 `AC-<CATEGORY>-NNN` in GWT form:
   - **Given**: extract or infer the relevant system state / pre-condition from the requirement context.
   - **When**: identify the specific user action or system event that triggers the behaviour.
   - **Then**: state the expected binary outcome with measurable thresholds where the requirement provides them (e.g., response time in ms, field values, error codes). If the requirement lacks a measurable threshold → insert `[NEEDS CLARIFICATION: define measurable acceptance threshold for <URS-ID>]`.
   - **Test layer**: assign OQ (functional, controlled environment) or PQ (real-world process conditions) or both.
4. **Cardinality**: generate multiple ACs per requirement for happy path + boundary conditions + error paths when the requirement implies distinct verifiable behaviours.
5. **Populate section 5 (traceability summary)** as the master index. Flag any prio=H requirement without an AC as `BLOCKING`.
6. **Anti-hallucination**: insert `[NEEDS CLARIFICATION: ...]` when context is insufficient to write a binary Then; never invent regulatory citations or system-specific thresholds.
7. **Output**: write `specs/AC.md` (status: draft); print summary + URS→AC coverage (% of URS-prio=H requirements covered).
8. **Post-flight**: run `validate-frontmatter.py` + `check-clarification-markers.py` + `generate-rtm.py` (to verify coverage and build RTM).

### Stop criteria ("complete" instance)

- [ ] `traces_to` points to a URS instance
- [ ] All `URS-<CATEGORY>-NNN` with prio=H have ≥1 `AC-<CATEGORY>-NNN` (0 blocking gaps)
- [ ] Each AC row has non-empty Given, When, and Then columns
- [ ] Each Then is binary (objectively PASS/FAIL) with measurable thresholds or a `[NEEDS CLARIFICATION]` marker
- [ ] Each AC cites its upstream URS-ID (or FS-ID) in the "Verifies" column
- [ ] Section 5 (traceability summary) is populated
- [ ] No prio=H requirement appears as a BLOCKING gap in section 5
- [ ] Signature block with ≥1 author + reviewers (incl. Quality Unit) + approver

### `status` transitions

```
draft ──[all prio=H covered + 0 blocking gaps]──> in-review
in-review ──[approver signatures applied]──> approved
approved ──[new version issued]──> superseded
```

### Downstream mapping — how the AC traces to OQ/PQ/RTM

| Origin (AC) | Destination | Cardinality | Rule |
|---|---|---|---|
| `AC-<CATEGORY>-NNN` (Test layer = OQ) | `OQ-TC-NNN` in `OQ.md` | 1:N | Each AC generates ≥1 OQ test case with detailed execution steps |
| `AC-<CATEGORY>-NNN` (Test layer = PQ) | `PQ-SCEN-NNN` in `PQ.md` | 1:N | Each AC generates ≥1 PQ scenario executed under real-world conditions |
| `AC-<CATEGORY>-NNN` (Test layer = both) | Both `OQ-TC-NNN` and `PQ-SCEN-NNN` | 1:N | Behaviour verified at both functional and process levels |
| `AC-<CATEGORY>-NNN` | Row in `RTM.md` | 1:1 | RTM carries the full chain: URS-ID → AC-ID → OQ/PQ-ID → result |
