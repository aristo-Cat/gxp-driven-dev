---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "RN — Release Notes (canonical CSV template)"
type: template
template_class: csv
template_id: "RN"
template_version: "0.1.0"
v_model_phase: reporting
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# RN is the RELEASE RECORD (GAMP 5 §M8 change/config + §M9 documentation).
# It summarizes what a release contains — version, changes, fixes, known
# issues, and the validation status covering the release. The human-readable
# record of what went live; mandatory input for operation and audit.
inputs:
  - template_id: "VR"
    required: true
    description: "Validation Report — the VR provides the fitness-for-intended-use statement and approved protocol references that the RN must cite"
  - template_id: "CC"
    required: false
    description: "Change Control Record(s) — change records whose implementation is included in this release (may be one-to-many)"
outputs:
  - artifact: "RN instance (Markdown) — Release Notes with validation status"
    consumed_by:
      - "operation"   # confirms what is running in production and under what validation coverage
      - "audit"       # human-readable record of release contents and approval chain

applicable_regulations:
  - "gamp-5"       # §M8 (Change and Configuration Management) — every release is a controlled change event; §M9 (Documentation) — the release record is a required deliverable
  - "eu-annex-11"  # §10 Change and Configuration Management (configuration register, change verification); §4.8 Documentation (complete audit trail of changes)

based_on:
  - "GAMP 5 §M8 (Change and Configuration Management) — release as a controlled change event; requires link to the change records, verification of validation coverage, and a rollback procedure"
  - "GAMP 5 §M9 (Documentation) — the release record is a required documentation deliverable; must identify the system, version, date, and approving signatures"
  - "EU Annex 11 §10 (Change and Configuration Management) — changes must be documented, verified, and traceable to validation evidence before going live"
  - "EU Annex 11 §4.8 (Documentation) — an audit trail entry is required for each configuration change; the RN serves as the human-readable audit record"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
  system_id:
    type: string
    required: true
  release_version:
    type: string
    required: true
    description: "Semantic version of the release (e.g. 1.2.0)"
  release_date:
    type: string
    required: true
    description: "Date the release was deployed to production (DD.MM.YYYY)"
  vr_ref:
    type: string
    required: true
    description: "Reference to the approved Validation Report that covers this release"
  validation_status:
    type: enum
    required: true
    values: ["fully-validated", "validated-with-conditions", "pending-validation-close"]
    description: "Overall validation coverage status at the time of release"
  rn_author_name:
    type: string
    required: true
  rn_author_dept:
    type: string
    required: true
  rollback_procedure_ref:
    type: string
    required: true
    description: "Reference to the rollback / restoration procedure (SOP, DEPLOY-RUN section, or equivalent)"
  known_issues_summary:
    type: string
    required: false
    description: "High-level summary of known issues / limitations in this release (details go in the table in §6)"
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
    - based_on_template: "RN"
    - based_on_template_version
    - system_id
    - traces_to          # VR instance (required)
    - status             # draft | in-review | approved | superseded
    - version            # release version this RN documents
    - created
    - updated
    - language
  conditional_fields:
    - approved_by: "required if status == approved (Author + System Owner release approval)"
    - supersedes: "if this RN supersedes a prior version of the same release's RN"
    - validation_conditions: "required if validation_status == validated-with-conditions"

# ─── Validation rules ────────────────────────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "traces_to must point to an approved VR"
  - "Every row in the changes table (§4) must cite at least one CC-YYYY-NNN or URS/FS requirement ID"
  - "Validation status table (§7) must reference approved IQ/OQ/PQ/VR by document ID and date before a production release is authorized"
  - "Known issues must declare a severity (critical / major / minor) and a mitigation or target resolution version"
  - "Rollback note must reference an existing, approved rollback procedure — no blank field"
  - "Approved by Author + System Owner (System Owner authorizes deployment; GAMP 5 §M8)"
  - "If validation_status == validated-with-conditions → document conditions in instance frontmatter (validation_conditions)"

tags:
  - template
  - csv
  - release-notes
  - rn
  - reporting
  - gamp-m8
  - gamp-m9
  - change-control
  - canonical
---

# RN — Release Notes

> [!note] Canonical CSV template — RELEASE RECORD
> **Canonical** template for the **Release Notes (RN)** — the human-readable record of what a release contains, which changes were implemented, what validation protocols cover the release, and whether it is safe to operate. It links back to the [Validation Report](VR.md) and to the [Change Control Records](CC.md) whose implementations are bundled in the release. Required by GAMP 5 §M8 (change/config management) and §M9 (documentation), and by EU Annex 11 §10.

> [!tip] Embedded usage rules
> 1. **Every change cites its CC** — each row in the changes table (§4) must reference the `CC-YYYY-NNN` (Change Control Record) that authorized it, or the `URS/FS` requirement it implements for first-release features. No undocumented changes.
> 2. **Validation status is explicit** (§7) — cite the approved IQ/OQ/PQ/VR by document ID and approval date. A release to production is not authorized until the cited protocols are approved.
> 3. **Known issues are mandatory** (§6) — if there are none, state "None identified at release time." Do not leave the section blank.
> 4. **Rollback is non-optional** — a blank rollback note is a blocking validation gap (GAMP 5 §M8).
> 5. **Approval** — Author (CSV/SME) prepares; System Owner authorizes the deployment (GAMP 5 §M8). Quality Unit reviews if the release affects GxP processes or triggers re-qualification.
> 6. **RN ≠ VR** — the RN records *what went live*; the VR records *fitness for intended use*. Both are required. The RN is the operational record; the VR is the formal validation closure.

---

## 0. Identification and signatures

### Release identity

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **Release version** | `{{release_version}}` |
| **Release date** | `{{release_date}}` |
| **Validation Report** | `{{vr_ref}}` ([VR](VR.md)) |
| **Validation status at release** | `{{validation_status}}` |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Author (CSV/SME) | `{{rn_author_name}}` | `{{rn_author_dept}}` |  |  |
| Release approver (System Owner) |  |  |  |  |
| Quality review (Quality Unit) *(if GxP-impacting)* |  |  |  |  |

---

## 1. Introduction and scope

These **Release Notes** document the contents of release **`{{release_version}}`** of system **`{{system_name}}`** (`{{system_id}}`), deployed on `{{release_date}}`. They record all changes included in this release, their authorization source, the validation coverage in effect, and any known issues at time of release.

This document is produced in accordance with GAMP 5 §M8 (Change and Configuration Management) and §M9 (Documentation), and EU Annex 11 §10 (Change and Configuration Management).

---

## 2. Summary of release contents

> Brief human-readable summary of what this release delivers. One paragraph maximum. Expand in §4.

---

## 3. Change Control records in this release

> List the Change Control records (`CC-YYYY-NNN`) whose implementation is bundled in this release. If this is the initial release of the system, state "Initial release — no prior change control records; first-time validation under VR `{{vr_ref}}`."

| CC record | Title / description | Authorized by | Date authorized |
|---|---|---|---|
|  |  |  |  |

---

## 4. Changes included in this release

### 4.1 New features

| ID | Description | Implements (URS/FS/CC) | Verification reference |
|---|---|---|---|
|  |  |  |  |

> [!note] Traceability requirement (GAMP 5 §M8)
> Every new feature must cite the requirement ID(s) it implements (`URS-FUNC-NNN`, `FS-FUNC-NNN`, or `CC-YYYY-NNN`) and the test or protocol that verified it before release.

### 4.2 Changes to existing functionality

| ID | Description | Implements (CC) | Verification reference |
|---|---|---|---|
|  |  |  |  |

### 4.3 Fixes

| ID | Description | Root cause (brief) | CC / incident reference | Verification reference |
|---|---|---|---|---|
|  |  |  |  |  |

---

## 5. Configuration changes

> Document any configuration parameters, environment variables, or infrastructure settings that changed as part of this release. Required by EU Annex 11 §10 (configuration register).

| Configuration item | Prior value / state | New value / state | Rationale | CC reference |
|---|---|---|---|---|
|  |  |  |  |  |

> If no configuration changes: state "No configuration changes in this release."

---

## 6. Known issues and limitations

`{{known_issues_summary}}`

| ID | Description | Severity | Impact | Mitigation / workaround | Target version |
|---|---|---|---|---|---|
|  |  | critical / major / minor |  |  |  |

> [!warning] Severity definitions
> **Critical** — GxP data integrity, patient safety, or regulatory compliance is at risk; must be resolved before or at this release. **Major** — significant functional impact, workaround available. **Minor** — cosmetic or low-impact; scheduled for a future release.
>
> If no known issues: state "None identified at release time."

---

## 7. Validation status

> [!quote] Validation coverage statement (GAMP 5 §M8; EU Annex 11 §10)
> Release **`{{release_version}}`** of system **`{{system_name}}`** is authorized for production deployment under the following approved validation coverage:

| Protocol / document | Document ID | Approval date | Status | Scope |
|---|---|---|---|---|
| [Installation Qualification](IQ.md) |  |  | approved |  |
| [Operational Qualification](OQ.md) |  |  | approved |  |
| [Performance Qualification](PQ.md) |  |  | approved |  |
| [Validation Report](VR.md) | `{{vr_ref}}` |  | approved | fitness-for-intended-use |

**Overall validation status**: `{{validation_status}}`

| Status value | Meaning |
|---|---|
| **fully-validated** | All protocols approved; VR issues fit-for-intended-use without conditions |
| **validated-with-conditions** | VR approved with conditions; conditions documented in instance frontmatter (`validation_conditions`) and tracked to resolution |
| **pending-validation-close** | VR not yet approved; this release must not go to a GxP-production environment until the VR is approved |

> [!warning] Production authorization
> A release to a **GxP-production environment** requires `validation_status: fully-validated` or `validated-with-conditions` **with the VR approved**. `pending-validation-close` is only acceptable for pre-production environments (UAT, staging, IQ/OQ execution).

---

## 8. Rollback note

> [!warning] Rollback procedure (GAMP 5 §M8)
> A tested rollback or restoration procedure must exist and be referenced here. A blank rollback note is a blocking validation gap.

**Rollback procedure reference**: `{{rollback_procedure_ref}}`

| Rollback aspect | Detail |
|---|---|
| Rollback procedure | `{{rollback_procedure_ref}}` |
| Data preserved on rollback | |
| Maximum time to restore prior version | |
| Tested (✓ / ✗) | |
| Tested by / date | |

---

## 9. Related documents

| Document | Reference |
|---|---|
| Validation Report | `{{vr_ref}}` ([VR](VR.md)) |
| Change Control Records | See §3 table |
| Deployment Runbook | [DEPLOY-RUN](DEPLOY-RUN.md) |
| Requirements Traceability Matrix | [RTM](RTM.md) |
| Performance Qualification | [PQ](PQ.md) |
| Organization's CSV Policy | `{{org_csv_policy_ref}}` |
| `{{custom_ref}}` |  |

---

## 10. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{rn_author_name}}`, `{{rn_author_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] RN is the operational audit record
> GAMP 5 §M9 and EU Annex 11 §10 require a documented record of every controlled release. The RN is that record. It is the first document an operations team reaches for when asked "what exactly changed in version X?" Keep it concise, accurate, and fully cross-referenced.

> [!note] Link every change to its authorization
> A change that appears in §4 without a `CC-YYYY-NNN` or requirement ID is undocumented — a compliance gap. If a change was done informally (hotfix), raise a retrospective CC immediately and cite it here.

> [!tip] Validation status must be current at release time
> The validation status table (§7) reflects the state at the moment of release. If the VR was approved after the RN was drafted, update §7 and increment the revision history before the release goes live.

## Related

- [VR](VR.md) · [CC](CC.md) · [PQ](PQ.md) · [IQ](IQ.md) · [OQ](OQ.md) · [RTM](RTM.md) · [DEPLOY-RUN](DEPLOY-RUN.md)
- GAMP 5 · EU Annex 11
- change control · configuration management · validated state

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the orchestrating skill (`gdd.lifecycle`).

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer project.
2. **Confirm approved VR exists** — if no approved VR is found, the release cannot be authorized for a GxP-production environment. Set `validation_status: pending-validation-close` and flag with `[NEEDS CLARIFICATION: VR not yet approved — production deployment is blocked]`.
3. **Collect CC records for the release** — read each `CC-YYYY-NNN` that is scoped to this release version. If the consumer project has no CC records (initial release), note "Initial release" in §3.
4. **Read IQ/OQ/PQ approval dates** — populate the validation status table (§7) with document IDs and approval dates.
5. **Read `templates/csv/RN.md`** from the toolkit as the source template (this file).

### Generation flow

1. **Populate release identity** (§0): system, version, date, VR reference.
2. **List CC records** (§3): one row per CC in scope.
3. **Expand changes** (§4): for each CC, extract new features / changes / fixes into the appropriate sub-table. For initial releases, populate from URS/FS requirement IDs.
4. **Document configuration changes** (§5): compare `.gxp-dev.yaml` or configuration baseline between prior and current release.
5. **Populate known issues** (§6): from open CC/IR records scoped to the release; if none, write "None identified at release time."
6. **Fill validation status table** (§7): cite IQ/OQ/PQ/VR by ID and approval date; set `validation_status` enum.
7. **Populate rollback note** (§8): reference the DEPLOY-RUN rollback section or equivalent SOP.
8. **Anti-hallucination**: use `[NEEDS CLARIFICATION: ...]` when document IDs, approval dates, or rollback procedure references are unknown. Never set `validation_status: fully-validated` without confirmed approved VR evidence.
9. **Output**: write `specs/RN.md` (status: draft).
10. **Post-flight**: `validate-frontmatter.py` + `check-clarification-markers.py`.

### `status` transitions

```
draft ──[changes complete + validation status confirmed + rollback ref present]──> in-review
in-review ──[Author + System Owner sign; QU reviews if GxP-impacting]──> approved
approved ──[subsequent release supersedes this version]──> superseded
```

> [!warning] Do not authorize production without an approved VR
> Setting `validation_status: fully-validated` requires a confirmed, approved VR instance. Setting it without that evidence is a compliance falsification — use `pending-validation-close` and block the production deployment.

### Mapping

| Origin (RN) | Destination | Rule |
|---|---|---|
| `validation_status: fully-validated` | System Owner | Authorizes production deployment |
| `validation_status: validated-with-conditions` | System Owner + QU | Authorizes with documented conditions; conditions tracked to resolution |
| `validation_status: pending-validation-close` | Hold | Production deployment blocked until VR is approved |
| RN approved | Operation team | Confirms exactly what is running and under what validation coverage |
| Known issues table | CC backlog | Each known issue with a target version feeds a new CC record |
