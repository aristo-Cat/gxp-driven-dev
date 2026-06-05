---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "FS — Functional Specification (canonical CSV template)"
type: template
template_class: csv
template_id: "FS"
template_version: "0.1.0"
v_model_phase: functional-specification
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-28
updated: 2026-05-29
# Round 2 (2026-05-29): translated to English canonical (was language: es). §-citations + IDs preserved verbatim.

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# FS realizes the URS (the "how" that answers the "what"). Not a root: depends on URS.
inputs:
  - template_id: "URS"
    required: true
    description: "Approved User Requirements Specification — source of all URS-<CATEGORY>-NNN that this FS realizes. Without an approved URS there is no valid FS."
  - template_id: "RA-INIT"
    required: false
    description: "Initial Risk Assessment — scales the level of detail of the FS according to risk (GAMP 5 §M3 step 1). Recommended for Cat 4/5."
outputs:
  - artifact: "FS instance (Markdown)"
    consumed_by:
      - "CS"        # Configuration Specification — Cat 4 (1:1 from FS configurable items)
      - "DS"        # Design Specification — Cat 5 (1:N from FS toward hw/sw design)
      - "RA-DET"    # Detailed Risk Assessment — uses URS + FS (GAMP 5 §M3 step 3)
      - "OQ"        # OQ test cases — functional verification (1:N from FS-IDs)
applicable_regulations:
  - "gamp-5"          # §D1 Specifying Requirements (D2 retired, merged) + §D3.3 functional-design
  - "21-cfr-part-11"
  - "eu-annex-11"     # §4.4 Specifications + traceability
based_on:
  - "GAMP 5 §D1 (Specifying Requirements) + §D3.3 (functional-design specs for custom systems)"
  - "V-Model structure: FS mirrors the URS by realizing what→how, with bidirectional traceability FS↔URS (≥1 FS per each URS GxP)"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
    description: "Human-readable name of the system (must match the source URS)"
    example: "QC LIMS at site A"
  system_id:
    type: string
    required: true
    description: "Unique system identifier (same as the source URS)"
  urs_ref:
    type: string
    required: true
    description: "Identifier + version of the URS instance that this FS realizes"
    example: "URS-PROJ-2026-001 v1.0 (approved)"
  supplier:
    type: string
    required: true
    description: "Supplier responsible for the realization (or 'in-house' if custom)"
  version:
    type: string
    required: true
    description: "Version of the base product being specified"
  gamp_category:
    type: enum
    required: true
    values: [3, 4, 5]
    description: "GAMP 5 category (inherited from RA-INIT / URS). Cat 1/2 do not require an FS."
  fs_author_name:
    type: string
    required: true
  fs_author_dept:
    type: string
    required: true
  system_overview:
    type: string
    required: true
    description: "General overview of the realization: main processes, modules, key interfaces"
  deviations_to_urs:
    type: string
    required: false
    description: "Changes that arose between URS approval and FS creation (change-control mechanism between specification phases)"
  covers_ds:
    type: boolean
    required: false
    description: "true if this FS incorporates the Design Specification (hw/sw) instead of a separate DS document (typical for simple Cat 3/4)"
  module_descriptions:
    type: string
    required: false
    description: "For large Cat 5 projects: list of separate Module Descriptions referenced from this FS"
  org_csv_policy_ref:
    type: string
    required: false
  custom_ref:
    type: string
    required: false

# ─── Presets: NOT redefined — INHERITED via cascade from the URS ─────────────
# Unlike the URS, the FS does not declare its own presets. The regulatory
# preset requirements (URS-EREC, URS-ESIG, URS-SEC, URS-API, URS-MIGR) were
# already decided in the URS; the FS REALIZES them: each active URS-EREC-NNN
# generates ≥1 FS-EREC-NNN describing HOW the system implements that control.
presets_inheritance:
  rule: "Each preset requirement active in the URS (URS-EREC/ESIG/SEC/API/MIGR) must have ≥1 FS-<CATEGORY>-NNN that realizes it. The FS does not re-decide applicability: it inherits the decision from the URS."
  part11_records: "If URS-EREC is active → FS-EREC is mandatory (technical realization of each Part 11/Annex 11 control)"
  part11_signatures: "If URS-ESIG is active → FS-ESIG is mandatory"
  annex11_security: "If URS-SEC-001/002 are active → FS-SEC realizes encryption + MFA"
  annex11_interfaces: "If URS-API-001 is active → FS-API realizes validated interfaces"
  annex11_migration: "If URS-MIGR-001 is active → FS-MIGR realizes validated migration"

# ─── INSTANCE frontmatter spec (not the template's) ─────────────────────────
instance_frontmatter_spec:
  required_fields:
    - title
    - type: "instance"
    - based_on_template: "FS"
    - based_on_template_version
    - system_id
    - traces_to            # URS instance ID + version that this FS realizes
    - status               # draft | in-review | approved | superseded
    - version              # instance's own semver
    - created
    - updated
    - language
  conditional_fields:
    - approved_by: "required if status == approved"
    - supersedes: "version of the previous FS if this is a new revision"
    - deviations_logged: "boolean — true if section 4.2 documents deviations from the URS"

# ─── Validation rules (Round 1 subset) ──────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "traces_to must point to a URS instance with status: approved (GAMP 5: FS realizes an approved URS)"
  - "Each FS-<CATEGORY>-NNN row must cite at least one URS-<CATEGORY>-NNN in the 'Realizes' column"
  - "Minimum cardinality: each URS-<CATEGORY>-NNN with GxP=Y must be realized by ≥1 FS-<CATEGORY>-NNN (full coverage)"
  - "Each URS-<CATEGORY>-NNN with prio=H without an FS counterpart = blocking gap (prevents status: approved)"
  - "If URS-EREC is active in the source URS → section 9.2 FS-EREC cannot be empty"
  - "If URS-ESIG is active in the source URS → section 9.3 FS-ESIG cannot be empty"
  - "The 'Realization' column must describe the technical HOW, not repeat the WHAT from the URS"
  - "Signature block must include an identified Data Owner (GAMP 5 §6.2.3.1 + M10)"
  - "Section 4.2 (Deviations to URS) must be present: empty only if there were no changes since the approved URS"

tags:
  - template
  - csv
  - fs
  - functional-specification
  - v-model
  - cascade
  - canonical
---

# FS — Functional Specification

> [!note] Canonical CSV template
> **Canonical** template for producing the **Functional Specification (FS)** of a computerized system. The FS describes the **"how"** (technical realization) that answers the **"what"** defined in the [URS](URS.md). Complies with GAMP 5 §D1 (Specifying Requirements — D2 retired and merged into D1) + §D3.3 (functional-design specs), EU Annex 11 §4.4, and 21 CFR Part 11. Mirrors the **22 canonical acronyms** of the URS with bidirectional traceability FS↔URS.

> [!tip] Embedded usage rules
> 1. **WHAT vs HOW** — the URS describes the requirement (the "what"); the FS describes the **realization** (the concrete "how"). Do not repeat the URS text: explain how the system implements it.
> 2. **Mandatory traceability** — each `FS-<CATEGORY>-NNN` must cite at least one `URS-<CATEGORY>-NNN` in the "Realizes" column. This is the backbone of the traceability matrix.
> 3. **Cardinality** — **minimum one FS per each URS** with GxP=Y. One URS requirement may generate several FS entries (1:N), but no GxP=Y/prio=H requirement may be left without a realization (1:0 is prohibited for critical requirements).
> 4. **Inherited GxP/Priority** — the FS inherits the GxP (Y/N) mark and priority (H/M/L) from the URS it realizes. These are not re-evaluated here.
> 5. **No-deletion rule** — an obsolete FS entry is **not** deleted: it is struck through (`~~FS-FUNC-007: ...~~`). Deleting breaks the URS↔FS↔DS↔Test specs traceability (`IQ.md` / `OQ.md` / `PQ.md`).
> 6. **Inherited presets, not redefined** — the regulatory preset controls (EREC/ESIG/SEC/API/MIGR) were already decided in the URS; the FS **realizes** them, it does not re-decide their applicability.
> 7. **V-Model pairing** — the FS is verified in the **OQ** (functional verification, GAMP 5 Table 4.1). Each `FS-<CATEGORY>-NNN` with prio=H generates ≥1 test case in `OQ.md`.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **URS being realized** | `{{urs_ref}}` *(must be approved)* |
| **Supplier** | `{{supplier}}` |
| **Version** | `{{version}}` |
| **GAMP category** | `{{gamp_category}}` *(inherited from [Risk Analysis](RA-INIT.md) / URS)* |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Author | `{{fs_author_name}}` | `{{fs_author_dept}}` |  |  |
| Reviewer 1 (System Owner / IT) |  |  |  |  |
| Reviewer 2 (SME / Process Owner) |  |  |  |  |
| Reviewer 3 (Data Owner) *(GAMP 5 §6.2.3.1 + M10)* |  |  |  |  |
| Approver 1 (System Owner) |  |  |  |  |
| Approver 2 (Quality Unit) |  |  |  |  |

> [!note] Who authors the FS
> Typically the **Supplier** (if the vendor produces the FS) or the **CSV Manager / Validation Coordinator** (if in-house). For Cat 5 custom software, the FS is usually authored by the development team; the regulated organization reviews and approves it.

---

## 1. Introduction

This **Functional Specification (FS)** describes **how** the system **`{{system_name}}`** will realize the requirements defined in its [URS](URS.md) (`{{urs_ref}}`). It constitutes the **Functional Specification** phase of the CSV V-Model (left-hand side, below the URS) and is verified in the **OQ** (functional verification).

According to GAMP 5 §D1, the URS and the FS form a **specification continuum**. This template keeps them as separate documents (a common and accepted practice), but for **simple Cat 3** systems the FS may be integrated into the URS or into the [Validation Plan](VP.md).

**Scope of this FS**: `{{system_overview}}`

> [!note] What this FS may cover
> Depending on complexity and GAMP category, this FS may incorporate:
> - **Design Specification (DS)** for hardware and software — if `{{covers_ds}}` = true (typical for simple Cat 3/4, where no separate DS is produced).
> - **Functional Description (FD)** — high-level narrative functional description.
> - Separate **Module Descriptions** — for large Cat 5 projects: `{{module_descriptions}}`.

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| FS | Functional Specification — the technical "how" that realizes the URS |
| URS | User Requirements Specification — the "what" from the user's perspective |
| DS | Design Specification — detailed hw/sw design (GAMP 5 §D3) |
| CS | Configuration Specification — configured settings/parameters (Cat 4, GAMP 5 §D3) |
| Realization | Technical description of how the system implements a user requirement |
| GAMP 5 | Good Automated Manufacturing Practice 5, ISPE 2022 |
| 21 CFR Part 11 | FDA — Electronic Records; Electronic Signatures |
| Annex 11 | EU GMP — Computerised Systems |
|  |  |

---

## 3. Catalog of requirement category codes (canonical)

The FS uses the same **22 canonical acronyms** as the URS. Each FS requirement receives an ID `FS-<CATEGORY>-NNN` and references the `URS-<CATEGORY>-NNN` it realizes. See `docs/requirement-id-scheme.md` for the master documentation.

| Code | Category | FS section |
|---|---|---|
| `ARCH` | Archiving | 9.12 |
| `DEVENV` | Development environment | 5 |
| `MIGR` | Data migration | 9.11 |
| `DOCS` | Documentation | 9.14 |
| `DATA` | Data structure | 9.4 |
| `PERIPH` | Peripheral devices / equipment | 10 |
| `EREC` | Electronic Records (21 CFR Part 11 + Annex 11) | 9.2 |
| `ESIG` | Electronic Signatures (21 CFR Part 11 + Annex 11) | 9.3 |
| `FUNC` | Functional requirements | 9.1 |
| `FLOW` | Data flow | 9.6 |
| `UI` | User Interface | 9.9 |
| `HW` | Hardware specification | 11 |
| `API` | Interfaces with other systems | 9.10 |
| `PROC` | Organization / process | 9.8 |
| `PERF` | Performance | 8 |
| `QUAL` | Quality | 6 |
| `REPORT` | Reports and listings | 9.5 |
| `SEC` | Data security | 9.7 |
| `DELIV` | Components to be delivered | 9.15.2 |
| `OPS` | System operation and environment | 9.13 |
| `TRAIN` | Training requirements | 7 |
| `TEST` | Testing | 9.15.1 |

---

## 4. Project context

### 4.1 System Overview

General overview of the technical realization: main processes the system automates, modules/components, key interfaces, and high-level logical architecture. Attach architecture diagrams if available.

`{{system_overview}}`

### 4.2 Deviations to URS

> [!warning] Change-control mechanism between specification phases
> Record here any change that arose **between URS approval and the creation of this FS**. Examples: a URS requirement turned out to be technically infeasible and was renegotiated; a constraint of the base product forced an alternative approach; an implicit requirement was discovered. Each deviation must be traced to the affected `URS-<CATEGORY>-NNN` and, if material, must trigger a URS revision.

`{{deviations_to_urs}}`

| Affected URS-ID | Deviation | Impact | Action (revise URS / accept in FS) |
|---|---|---|---|
| `URS-...-NNN` |  |  |  |
|  |  |  |  |

---

## 4.5 URS → FS traceability matrix (cascade)

> [!tip] This is the backbone of the document
> The following table is the **traceability summary** between URS requirements and their realization in this FS. Each URS requirement with GxP=Y must appear here with ≥1 FS entry realizing it. A `validate-traceability` skill uses this table to detect gaps. The detailed per-category tables (sections 5–11) contain the full realization; this table is the master index.

| URS-ID | URS statement (summary) | FS-ID(s) realizing it | Cardinality | GxP | Prio |
|---|---|---|---|---|---|
| `URS-FUNC-001` |  | `FS-FUNC-001` | 1:1 |  |  |
| `URS-EREC-005` |  | `FS-EREC-005`, `FS-DATA-00X` | 1:N |  |  |
|  |  |  |  |  |  |

**Cardinality rules**:

| Cardinality | Meaning | When |
|---|---|---|
| **1:1** | One URS → one FS | Direct realization, simple requirement |
| **1:N** | One URS → several FS entries | The user requirement needs multiple technical realizations (e.g. a Part 11 control that touches audit trail + access control + reporting) |
| **1:0** | One URS → no FS | **Only permitted for URS with GxP=N**. A URS with GxP=Y or prio=H without an FS entry = blocking gap. |

---

## 5. Realization of development environment requirements — `FS-DEVENV-NNN`

> For Cat 3 (standard products) this section may be **N/A**. For Cat 4/5, describe how the tools, IDEs, repositories, and CI/CD pipelines requested by the URS are implemented.

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-DEVENV-001` | `URS-DEVENV-001` |  |
|  |  |  |

---

## 6. Realization of quality requirements — `FS-QUAL-NNN`

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-QUAL-001` | `URS-QUAL-001` |  |
|  |  |  |

---

## 7. Realization of training requirements — `FS-TRAIN-NNN`

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-TRAIN-001` | `URS-TRAIN-001` |  |
|  |  |  |

---

## 8. Realization of performance requirements — `FS-PERF-NNN`

> The realization must be as testable as the URS requirement. If `URS-PERF-001` requests "≤2 s for 100 concurrent users", the FS describes the architecture that achieves it (caching, connection pooling, sizing) in a way that can be verified in the OQ.

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-PERF-001` | `URS-PERF-001` | *e.g.: "Connection pool of 200; Redis cache for frequent queries; load balancer with 3 app nodes. Verifiable via load test in OQ."* |
|  |  |  |

---

## 9. Realization of functional / technical requirements

### 9.1 Realization of functional requirements — `FS-FUNC-NNN`

Describe how the system implements each function defined in `URS-FUNC`. Include startup/shutdown behavior, error handling, and business logic.

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-FUNC-001` | `URS-FUNC-001` |  |
|  |  |  |

---

### 9.2 Realization of Electronic Records — `FS-EREC-NNN`

> [!warning] Mandatory section if URS-EREC is active in the source URS
> Each active `URS-EREC-NNN` (including canonical presets URS-EREC-001 through 014) must have ≥1 `FS-EREC-NNN` that describes **technically how** the control is implemented. Do not repeat the Part 11 requirement: describe the mechanism (e.g. append-only audit trail table with DB triggers, retention in cold storage, etc.).

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-EREC-001` | `URS-EREC-001` | *e.g.: "Integrity validation via SHA-256 checksum per record; is_valid flag recalculated on each read."* |
| `FS-EREC-005` | `URS-EREC-005` | *e.g.: "Audit trail in an append-only table with DB triggers capturing user_id, role, old_value, new_value, timestamp_utc, reason. Immutable at DB permission level."* |
| `FS-EREC-013` | `URS-EREC-013` | *e.g.: "ALCOA+ implemented by: Attributable (user_id on every record), Contemporaneous (server-side NTP timestamp), Original (no overwrite, versioning), ..."* |
|  |  |  |

---

### 9.3 Realization of Electronic Signatures — `FS-ESIG-NNN`

> [!warning] Mandatory section if URS-ESIG is active in the source URS

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-ESIG-002` | `URS-ESIG-002` | *e.g.: "Signature manifestation: the signed record displays full_name, timestamp_utc and meaning (review/approval) rendered in PDF and in the web view."* |
| `FS-ESIG-017` | `URS-ESIG-017` | *e.g.: "Tamper-evidence: record hash calculated at signing; any subsequent UPDATE invalidates the hash and marks the record as 'signature broken'."* |
|  |  |  |

---

### 9.4 Realization of data structure — `FS-DATA-NNN`

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-DATA-001` | `URS-DATA-001` |  |
|  |  |  |

---

### 9.5 Realization of reports and listings — `FS-REPORT-NNN`

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-REPORT-001` | `URS-REPORT-001` |  |
|  |  |  |

---

### 9.6 Realization of data flow — `FS-FLOW-NNN`

> Include flow diagrams showing the realization. Each derived flow must also be transcribed as text.

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-FLOW-001` | `URS-FLOW-001` |  |
|  |  |  |

---

### 9.7 Realization of data security — `FS-SEC-NNN`

> [!warning] Realize the Annex 11 modernization presets if active in the URS
> If `URS-SEC-001` (encryption) and/or `URS-SEC-002` (remote MFA) are active, describe their concrete technical realization.

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-SEC-001` | `URS-SEC-001` | *e.g.: "At-rest encryption: AES-256 (TDE on DB); in-transit: TLS 1.3. Key management via HSM with annual rotation."* |
| `FS-SEC-002` | `URS-SEC-002` | *e.g.: "MFA via TOTP (RFC 6238) mandatory for access from outside the corporate network; integrated with the corporate IdP."* |
|  |  |  |

---

### 9.8 Realization of organization / process requirements — `FS-PROC-NNN`

> Explicitly identify which SOPs will cover the organizational requirements (direct link to the creation/update of operational SOPs).

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-PROC-001` | `URS-PROC-001` |  |
|  |  |  |

---

### 9.9 Realization of user interface — `FS-UI-NNN`

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-UI-001` | `URS-UI-001` |  |
|  |  |  |

---

### 9.10 Realization of interfaces — `FS-API-NNN`

> [!warning] Realize preset URS-API-001 (validated interfaces) if active
> Describe the protocol, data format, error handling, and how end-to-end integrity of each GxP interface is validated.

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-API-001` | `URS-API-001` | *e.g.: "REST interface with the ERP system: JSON payload validated against schema; idempotent retries; daily count reconciliation; log of every transfer with correlation_id."* |
|  |  |  |

---

### 9.11 Realization of data migration — `FS-MIGR-NNN`

> [!warning] Realize preset URS-MIGR-001 (validated migration) if active
> Describe the source↔target mapping, tooling, verification, and audit trail preservation.

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-MIGR-001` | `URS-MIGR-001` |  |
|  |  |  |

---

### 9.12 Realization of archiving — `FS-ARCH-NNN`

> Describe **how** to archive (the URS defined what): external systems, transfer, format, read-only access, pre-deletion checksum.

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-ARCH-001` | `URS-ARCH-001` |  |
|  |  |  |

---

### 9.13 Realization of system operation and environment — `FS-OPS-NNN`

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-OPS-001` | `URS-OPS-001` |  |
|  |  |  |

---

### 9.14 Realization of documentation — `FS-DOCS-NNN`

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-DOCS-001` | `URS-DOCS-001` |  |
|  |  |  |

---

### 9.15 Life cycle

#### 9.15.1 Realization of testing requirements — `FS-TEST-NNN`

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-TEST-001` | `URS-TEST-001` |  |
|  |  |  |

#### 9.15.2 Realization of components to be delivered — `FS-DELIV-NNN`

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-DELIV-001` | `URS-DELIV-001` |  |
|  |  |  |

---

## 10. Realization of peripheral and auxiliary equipment — `FS-PERIPH-NNN`

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-PERIPH-001` | `URS-PERIPH-001` |  |
|  |  |  |

---

## 11. Hardware design specification — `FS-HW-NNN`

> This section may absorb the Hardware Design Specification (DS) if `{{covers_ds}}` = true.

| FS ID-No. | Realizes (URS-ID) | Realization (how) |
|---|---|---|
| `FS-HW-001` | `URS-HW-001` |  |
|  |  |  |

---

## 12. Related documents

| Document | Reference |
|---|---|
| URS realized by this FS | `{{urs_ref}}` ([URS](URS.md)) |
| Organization's CSV Policy | `{{org_csv_policy_ref}}` |
| Validation Plan | [VP](VP.md) |
| Risk Analysis (initial) | [RA-INIT](RA-INIT.md) |
| Design Specification (Cat 5) | [DS](DS.md) *(if separate)* |
| Configuration Specification (Cat 4) | [CS](CS.md) *(if applicable)* |
| `{{custom_ref}}` |  |

---

## 13. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{fs_author_name}}`, `{{fs_author_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] The FS is the bridge URS → DS/CS → OQ
> Each `FS-<CATEGORY>-NNN` cites a `URS-<CATEGORY>-NNN`; the [Design Spec](DS.md) (Cat 5) and the [Config Spec](CS.md) (Cat 4) hang from the FS; the **OQ** (functional verification) tests the FS-IDs. This chain is the end-to-end traceability of the V-Model: `URS → FS → DS/CS → OQ`. *(GAMP 5 §4.2.6.4: "OQ" is file naming by CSV convention; it corresponds to functional verification.)*

> [!note] Category-awareness — FS depth by GAMP category
> - **Cat 3** (standard product): lightweight FS — describes the configuration of the standard product. May be integrated into the URS or VP.
> - **Cat 4** (configured): FS describes the configuration; the detailed settings/parameters go in the [Configuration Specification](CS.md).
> - **Cat 5** (custom): comprehensive FS; feeds the [Design Specification](DS.md). For large projects, use separate Module Descriptions.

> [!note] WHAT (URS) vs HOW (FS) — design principle
> The URS describes what the user needs (implementation-independent); the FS describes how it will be realized. If an FS entry merely repeats the URS text without adding a technical realization, it is poorly written. Section 4.2 "Deviations to URS" governs changes between both phases.

> [!tip] Natural output of this template
> A well-written FS produces the **central column** of the traceability matrix: each `URS-<CATEGORY>-NNN` → `FS-<CATEGORY>-NNN` (1:1 or 1:N) → `DS-<CATEGORY>-NNN` / `CS-<CATEGORY>-NNN` → test case in `OQ.md`. Section 4.5 is the master index of that traceability.

## Related

- [URS](URS.md) · [RA-INIT](RA-INIT.md) · [DS](DS.md) · [CS](CS.md) · [OQ](OQ.md)
- GAMP 5 · 21 CFR Part 11 · EU Annex 11
- V-Model · functional specification · specification traceability

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.fs.from-urs` skill.

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer project. If it does not exist → redirect to `/gdd.init`.
2. **Locate the approved URS instance** (`specs/URS.md`). If it does not exist or status != approved → **stop**: the FS realizes an approved URS (GAMP 5 §M3). Inform the user.
3. **Read `templates/csv/FS.md`** from the toolkit as the source template (this file).
4. **Read RA-INIT if it exists** — scales the level of detail of the FS according to risk.

### Generation flow (cascade from URS)

1. **Parse all `URS-<CATEGORY>-NNN`** from the approved URS, with their GxP (Y/N) and prio (H/M/L).
2. **For each URS-ID**, propose ≥1 `FS-<CATEGORY>-NNN` that realizes it:
   - Inherit GxP and prio from the URS.
   - Generate the "Realization" column describing the **technical how** — never repeat the URS text.
   - Cardinality: 1:1 by default; 1:N if the requirement needs multiple realizations; 1:0 **only** if GxP=N.
3. **Realize inherited presets**: for each active URS-EREC/ESIG/SEC/API/MIGR in the URS, generate the corresponding FS-<CATEGORY> entry.
4. **Populate the traceability matrix (section 4.5)** as the master index.
5. **Anti-hallucination**: insert `[NEEDS CLARIFICATION: ...]` when there is insufficient technical information to describe a realization; never invent technical mechanisms or regulatory citations.
6. **Output**: write `specs/FS.md` (status: draft); print summary + URS→FS coverage (% of URS requirements realized).
7. **Post-flight**: run `validate-frontmatter.py` + `check-clarification-markers.py` + `generate-rtm.py` (to verify coverage).

### Stop criteria ("complete" instance)

- [ ] `traces_to` points to a URS instance with status: approved
- [ ] All `URS-<CATEGORY>-NNN` with GxP=Y have ≥1 `FS-<CATEGORY>-NNN` (full coverage)
- [ ] No URS with prio=H is left without a realization (0 blocking gaps)
- [ ] Each FS-ID cites its URS-ID in the "Realizes" column
- [ ] The "Realization" column describes HOW, not the WHAT
- [ ] If URS-EREC/ESIG are active → sections 9.2/9.3 are not empty
- [ ] Section 4.2 (Deviations to URS) is present (empty only if there were no changes)
- [ ] Signature block with ≥1 author + reviewers (incl. Data Owner) + approvers

### `status` transitions

```
draft ──[full URS coverage + 0 H gaps]──> in-review
in-review ──[approver signatures applied]──> approved
approved ──[new version issued]──> superseded
```

### Downstream mapping — how the FS traces to DS/CS/OQ

| Origin (FS) | Destination | Cardinality | Rule |
|---|---|---|---|
| `FS-<CATEGORY>-NNN` (Cat 5) | `DS-<CATEGORY>-NNN` in `DS.md` | 1:N | The DS details the hw/sw design that implements the FS |
| `FS-<CATEGORY>-NNN` (Cat 4) | `CS-<CATEGORY>-NNN` in `CS.md` | 1:1 | The CS documents the configured settings/parameters |
| `FS-<CATEGORY>-NNN` with prio=H | Test case in `OQ.md` | 1:N | Functional verification of each critical realization |
| `FS-<CATEGORY>-NNN` | Row in `RA-DET.md` | 1:1 | The detailed RA evaluates the risk of each realization |
