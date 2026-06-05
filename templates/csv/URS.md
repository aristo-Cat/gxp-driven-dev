---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "URS — User Requirements Specification (canonical CSV template)"
type: template
template_class: csv
template_id: "URS"
template_version: "0.1.0"
v_model_phase: requirements-definition
gamp_categories_applicable: [2, 3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-24
updated: 2026-05-29
# Round 2 (2026-05-29): translated to English canonical (was language: es).
# §-citations are language-neutral and preserved verbatim. Spanish version
# recoverable from git history; an optional URS.es.md translation may be added later.

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
inputs:
  - template_id: "GXP-ASSESS"
    required: true
    description: "System identity + GxP/GAMP/Privacy categorization"
  - template_id: "DPIA"
    required: false
    description: "Activate if the system processes personal data (GDPR/HIPAA)"
outputs:
  - artifact: "URS instance (Markdown)"
    consumed_by:
      - "FS"               # Functional Specification — 1:N mapping URS→FS
      - "RA-INIT"    # Risk Analysis — inherits URS IDs with GxP=Y
      - "IQ"     # IQ test cases — inherits URS with prio H
applicable_regulations:
  - "21-cfr-part-11"
  - "eu-annex-11"
  - "gamp-5"
based_on:
  - "Industrial CSV catalog template — EN version (V-Model structure + 22 category codes)"
  - "Industrial CSV catalog template — DE version (21 CFR Part 11 presets — canonical requirements)"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
# An agnostic skill reads this block to know what to ask the user and to
# validate that the instance is complete.
placeholders:
  system_name:
    type: string
    required: true
    description: "Human-readable name of the computerized system"
    example: "QC LIMS at site A"
  system_id:
    type: string
    required: true
    description: "Unique identifier per the organization's corporate scheme"
    example: "PROJ-2026-001"
  supplier:
    type: string
    required: true
    description: "Supplier of the base product (or 'in-house' if custom)"
  version:
    type: string
    required: true
    description: "Version of the base product being validated"
  intended_use:
    type: string
    required: true
    description: "Regulatory intended use (1-3 sentences, must be testable)"
  gamp_category:
    type: enum
    required: true
    values: [1, 3, 4, 5]
    description: "GAMP 5 category (decided in RA-INIT)"
  site_code:
    type: string
    required: false
    description: "Only if the installation is site-specific within a multi-site organization"
  end_user_group:
    type: string
    required: true
    description: "Target user groups"
  related_systems:
    type: string
    required: false
    description: "Connected systems; described from the receiver's perspective"
  project_purpose:
    type: string
    required: true
  system_description:
    type: string
    required: true
  scope_description:
    type: string
    required: true
  out_of_scope:
    type: string
    required: false
  detailed_process_description:
    type: string
    required: true
  author_name:
    type: string
    required: true
  author_dept:
    type: string
    required: true
  org_csv_policy_ref:
    type: string
    required: false
    description: "Reference to the organization's corporate CSV policy (if any)"
  org_cs_operation_ref:
    type: string
    required: false
  custom_ref:
    type: string
    required: false

# ─── Activatable presets (21 CFR Part 11 / EU Annex 11) ─────────────────────
# A skill decides preset_active based on the DPIA output and the direct
# question: "does the system generate/store GxP electronic records?"
presets:
  URS-EREC:
    description: "14 preset Electronic Records requirements (21 CFR Part 11 + Annex 11 2025: ALCOA+ + peer review audit trail)"
    activation_question: "Does the system generate or store GxP electronic records as the primary source?"
    if_inactive_action: "Mark section 9.2 as 'N/A — the system is not 21 CFR Part 11 / Annex 11 relevant' and keep the section"
  URS-ESIG:
    description: "18 preset Electronic Signatures requirements (21 CFR Part 11 + Annex 11 2025: tamper-evidence + hybrid wet-ink+hash)"
    activation_question: "Does the system implement electronic signatures (not just scanned ones)?"
    if_inactive_action: "Mark section 9.3 as 'N/A — the system does not use Part 11 electronic signatures'"
  URS-SEC-modern:
    description: "2 preset Security modernization requirements (EU Annex 11 2025: encryption + remote MFA)"
    activation_question: "Does the system process critical GxP data in cloud/SaaS or have remote access?"
    if_inactive_action: "Mark URS-SEC-001/002 as 'N/A — the system is on-premises with no remote access' and keep the section"
  URS-API-valid:
    description: "1 preset Validated interfaces requirement (EU Annex 11 2025 §10)"
    activation_question: "Does the system transfer GxP data to/from other systems via interfaces?"
    if_inactive_action: "Mark URS-API-001 as 'N/A — standalone system with no interfaces' and keep the section"
  URS-MIGR-valid:
    description: "1 preset Validated migration requirement (EU Annex 11 2025 §10 + GAMP 5 D7)"
    activation_question: "Is there legacy data to migrate from a predecessor system?"
    if_inactive_action: "Mark URS-MIGR-001 as 'N/A — no legacy data migration' and keep the section"

# ─── INSTANCE frontmatter spec (not the template's) ─────────────────────────
# When a skill instantiates this template for a real system, the resulting
# file's frontmatter must follow this shape.
instance_frontmatter_spec:
  required_fields:
    - title
    - type: "instance"
    - based_on_template: "URS"
    - based_on_template_version
    - system_id
    - status     # draft | in-review | approved | superseded
    - version    # instance's own semver, e.g. "1.0", "1.1"
    - created
    - updated
    - language   # "en" | "es" | "de" | etc.
  conditional_fields:
    - approved_by: "required if status == approved"
    - supersedes: "version of the previous URS if this is a new revision"
    - preset_part11_active: "boolean — true if URS-EREC / URS-ESIG presets are active"

# ─── Validation rules (Round 1 subset; rest in Round 2 + formal schema) ─────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "Every requirement row in a URS-<CATEGORY> table must have non-empty GxP (Y/N) and prio (H/M/L)"
  - "Section 4.1-4.4 (Project Context) must have non-empty descriptions"
  - "If gamp_category == 5: URS-DEVENV, URS-QUAL, URS-TRAIN must each have ≥3 requirements"
  - "If preset_part11_active: true → sections 9.2 URS-EREC and 9.3 URS-ESIG cannot be marked N/A"
  - "If preset_part11_active: false → 9.2 and 9.3 must carry an explicit 'N/A — reason' mark"
  - "Signature table must have ≥1 author, ≥1 reviewer, ≥1 approver designated before status: in-review"
  - "Signature block must include an identified Data Owner (GAMP 5 §6.2.3.1 + M10)"
  - "RA-INIT must be status: approved before the URS can reach status: approved (GAMP 5 §M3 step 1)"
  - "URS-EREC-013 (ALCOA+) must document how each of the 9 attributes is ensured in the design"

tags:
  - template
  - csv
  - urs
  - v-model
  - requirements
  - canonical
---

# URS — User Requirements Specification

> [!note] Canonical CSV template
> **Canonical** template (multi-organization, multi-site) for producing the **User Requirements Specification (URS)** of a computerized system in compliance with GAMP 5, EU Annex 11 and 21 CFR Part 11. It synthesizes the structure of an industrial CSV catalog (EN source for the V-Model structure + DE source for the Part 11 presets), preserving the 22 canonical **category codes** for IDs and the 36 preset requirements (ER/ES + Annex 11 2025 modernization). The `{{...}}` placeholders are the per-project/per-organization parameterization points.

> [!tip] Embedded usage rules
> 1. **Testability** — every requirement must be verifiable by a future test script. Avoid "the system shall be performant"; write "the system shall respond within ≤2 s".
> 2. **Stable IDs** — each requirement has a unique `ID-No.` formed as `URS-<CATEGORY>-NNN`. It starts at `001` and increments sequentially within each category code.
> 3. **No-deletion rule** — an obsolete requirement is **not** deleted: it is struck through (`~~URS-FUNC-007: ...~~`). Deleting breaks the URS↔FS↔DS↔Test-spec traceability (`IQ.md` / `OQ.md` / `PQ.md`). *(Note GAMP 5 §4.2.6.4: the guide does not use "IQ/OQ/PQ" as life-cycle activity terminology; the file names are kept by industrial CSV convention, but internally they correspond to installation/functional/fitness verification.)*
> 4. **Mandatory GxP relevancy** — every row must mark `Y` (GxP-relevant) or `N`. This defines the regulatory scope.
> 5. **Mandatory prioritization** — `H` (high, critical — non-implementation = critical deviation), `M` (medium), `L` (low, nice-to-have).
> 6. **Implementation independence** — the "what" goes here; the "how" goes in [FS](FS.md) and [DS](DS.md).
> 7. **Optional integration into VP** — for low-complexity projects (typically simple Cat 3), the URS may be integrated into the [Validation Plan](VP.md) without a separate URS document.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` *(per the corporate scheme defined in [GXP-ASSESS](GXP-ASSESS.md))* |
| **Supplier** | `{{supplier}}` |
| **Version** | `{{version}}` |
| **Intended Use** | `{{intended_use}}` |
| **GAMP category** | `{{gamp_category}}` *(determined in [Risk Analysis](RA-INIT.md))* |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Author | `{{author_name}}` | `{{author_dept}}` |  |  |
| Reviewer 1 (Process Owner) |  |  |  |  |
| Reviewer 2 (SME) |  |  |  |  |
| Reviewer 3 (Data Owner) *(GAMP 5 §6.2.3.1 + M10)* |  |  |  |  |
| Approver 1 (System Owner) |  |  |  |  |
| Approver 2 (Quality Unit) |  |  |  |  |

---

## 1. Introduction

This **User Requirements Specification (URS)** describes the requirements that the system **`{{system_name}}`** must meet. It defines the "what" from the regulated user's perspective and constitutes the formal input to the Requirements Definition phase of the CSV V-Model.

**Scope**: `{{scope_description}}`
**Out of scope**: `{{out_of_scope}}`

---

## 2. Definitions and abbreviations

List relevant terms in alphabetical order. The catalog category codes (section 3) are **not** repeated here.

| Term | Definition |
|---|---|
| GxP | Good "x" Practices — covers GMP, GLP, GCP, GDP, GVP |
| GAMP 5 | Good Automated Manufacturing Practice 5, ISPE 2022 |
| CSV | Computerized System Validation |
| 21 CFR Part 11 | FDA — Electronic Records; Electronic Signatures |
| Annex 11 | EU GMP — Computerised Systems |
|  |  |

---

## 3. Catalog of requirement category codes (canonical)

The **22 canonical acronyms** define the requirement categories. Each URS requirement receives an ID `URS-<CATEGORY>-NNN`. This catalog is **not modified**: adding codes breaks traceability with FS/DS, which expect the canonical set. See `docs/requirement-id-scheme.md` for the master documentation.

| Code | Category | URS section |
|---|---|---|
| `ARCH` | Archiving | 9.12 |
| `DEVENV` | Development environment | 5 |
| `MIGR` | Data migration (from predecessor systems) | 9.11 |
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
| `DELIV` | Components to be delivered (Scope of supply) | 9.15.2 |
| `OPS` | System operation and deployment environment | 9.13 |
| `TRAIN` | Training requirements | 7 |
| `TEST` | Testing | 9.15.1 |

---

## 4. Project context

### 4.1 Project objective and purpose

General description of the project: why the system is implemented or developed, and whether validation is required and approved per the computerized-system registration and assessment form ([GXP-ASSESS](GXP-ASSESS.md)).

`{{project_purpose}}`

### 4.2 System description

General description of the system, functionality, system environment, hardware and software components. Attach diagrams showing the system and its components.

`{{system_description}}`

### 4.3 End user

Define which user groups the system is designed for (e.g.: "production of generics only at site `{{site_code}}`").

`{{end_user_group}}`

### 4.4 Related systems

Describe connected or adjacent systems. If only the target system is validated but interfaces to other systems exist, make explicit what is in/out of scope.

> Interfaces are **always described from the receiving system's perspective** (canonical rule), to ensure consistency across URSs of different systems.

`{{related_systems}}`

---

## 5. Development environment requirements — `URS-DEVENV-NNN`

> For Cat 3 (standard products) this section may be **N/A**. For Cat 4 (configured) and Cat 5 (custom), describe development tools, IDE, languages, compilers, repositories.

> [!note] Category × mode interpretation
> The meaning of this section depends on the **GAMP category** combined with the manifest `mode`:
> - **Cat 5 + `mode: develop`** (custom software built from scratch): full development environment — programming languages, IDE, compilers, source control + branching, CI/CD, static analysis. This is the section's primary intent.
> - **Cat 3/4 + `mode: validate`** (configured/standard COTS being validated): typically **N/A** or limited to the supplier's own development environment (covered by supplier assessment, not by your team).
> - **Cat 3/4 + `mode: develop`** (a configured product whose *configuration* you manage as if developing): interpret DEVENV as the **configuration & version-control toolchain** (config repository, config-vs-production environment separation, change traceability), **not** from-scratch code development. This Cat × mode combination is unusual — if you are validating a vendor product rather than building, consider `mode: validate` or `hybrid` instead.

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-DEVENV-001` |  |  | `{{requirement}}` |
|  |  |  |  |

---

## 6. Quality requirements — `URS-QUAL-NNN`

Quality assurance, programming standards, test execution, configuration and version management, applicable standards.

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-QUAL-001` |  |  |  |
|  |  |  |  |

---

## 7. Training requirements for developer and end user — `URS-TRAIN-NNN`

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-TRAIN-001` |  |  |  |
|  |  |  |  |

---

## 8. Performance requirements — `URS-PERF-NNN`

Application and data availability, max. downtime, fault tolerance, data volume (daily/monthly/yearly), estimated number of concurrent users, response time, network requirements, etc.

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-PERF-001` |  |  | *e.g.: "The system shall respond to interactive transactions within ≤2 s for 100 concurrent users."* |
|  |  |  |  |

---

## 9. Functional / technical requirements

### 9.1 Functional requirements — `URS-FUNC-NNN`

#### 9.1.1 Detailed process description

Description of the business processes the system must cover. Use flow diagrams where possible. See also the system description (4.2).

`{{detailed_process_description}}`

#### 9.1.2 Partial functions

Functions of system components (startup, shutdown, generation of error messages and their handling). Before adding, verify the requirement does not belong to another section (DATA, SEC, API, etc.).

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-FUNC-001` |  |  |  |
|  |  |  |  |

---

### 9.2 Electronic Records requirements (21 CFR Part 11) — `URS-EREC-NNN`

> [!warning] Optional preset — activate only if applicable
> This section **only** applies if the system was identified as subject to 21 CFR Part 11 or EU Annex 11 (typically: a GxP system that generates electronic records as the primary source). The 14 requirements below are the canonical industrial set with exact §-citations to 21 CFR Part 11. If the section does not apply, mark "N/A — the system is not 21 CFR Part 11 relevant" and keep the section.

| ID-No. | GxP | Prio. | Requirement |
|---|---|---|---|
| `URS-EREC-001` | Y | H | It must be possible to **identify invalid or altered records** (21 CFR Part 11 §11.10.a). |
| `URS-EREC-002` | Y | H | Complete printouts of the electronic data must be producible from the system (§10.b). |
| `URS-EREC-003` | Y | H | Electronic records must remain electronically accessible throughout their retention period (§10.c). |
| `URS-EREC-004` | Y | H | System access must be limited per user; a strict user-management concept must be defined and implemented (§10.d, §10.g). |
| `URS-EREC-005` | Y | H | A **secure, computer-generated, time-stamped audit trail** that records operator create/modify/delete actions without obscuring previous information. For each change it must capture: user (with role if applicable), **old value**, **new value**, date+time (with timezone if applicable), and **reason for change** prompted to the user. Audit trail data must be recorded **at the time of events**, not at the end of the process. Specify which GxP data it is implemented for (21 CFR Part 11 §11.10.e + EU Annex 11 §12.2 p.10). |
| `URS-EREC-006` | Y | H | It must be possible to perform functional checks of the system (§10.f). |
| `URS-EREC-007` | Y | H | When performing device checks (e.g. terminals), it must be possible to determine the validity of the source of the data input or instruction (§10.h). |
| `URS-EREC-008` | Y | H | Training of users, developers and support must be documented (§10.i). |
| `URS-EREC-009` | Y | H | There must be a definition of which user groups can grant access rights and which system operations each is permitted (§10.k). |
| `URS-EREC-010` | Y | H | The system documentation must be managed under version control (§10.k). |
| `URS-EREC-011` | Y | H | It must be defined whether this is a **closed or open system** (21 CFR Part 11 §11.30). *(Note: a system accessible remotely via the Internet but only by the persons owning the data is still a closed system.)* **If open**: additional **encryption** and/or **digital signature** controls are required to ensure authenticity and confidentiality (§11.30). |
| `URS-EREC-012` | Y | H | Explicitly define which system data constitute "electronic records" in the Part 11 sense. *(Name them in detail here.)* |
| `URS-EREC-013` | Y | H | The system must implement the **ALCOA+** data-integrity principles: **A**ttributable, **L**egible, **C**ontemporaneous, **O**riginal, **A**ccurate + **C**omplete, **C**onsistent, **E**nduring, **A**vailable. Document how each of the 9 attributes is ensured in the design (EU Annex 11 §2.4 / Glossary p.17 + GAMP 5 §G2.1 p.389). |
| `URS-EREC-014` | Y | H | Audit trail reviews must be performed by personnel **not directly involved** in the activities covered by the review — **independent peer review** (EU Annex 11 §12.6 p.10). |
| `URS-EREC-NNN` |  |  | *(add additional system-specific requirements, starting at NNN=015)* |

---

### 9.3 Electronic Signatures requirements (21 CFR Part 11) — `URS-ESIG-NNN`

> [!warning] Optional preset — activate only if the system uses electronic signatures
> Same criterion as `URS-EREC`. If the system does not implement electronic signatures, mark the section "N/A".

| ID-No. | GxP | Prio. | Requirement |
|---|---|---|---|
| `URS-ESIG-001` | Y | H | An SOP must exist regulating that each person can be held accountable for actions performed under their electronic signature (§10.j). *(Check whether one already exists in the organization.)* |
| `URS-ESIG-002` | Y | H | Signed electronic records must visibly contain the signer's full legible name, the date and time of signing, and the meaning or reason for the signature — both in paper printout and in electronic display (§50). |
| `URS-ESIG-003` | Y | H | Electronic signatures must be securely linked to the record they belong to (§70). |
| `URS-ESIG-004` | Y | H | Each electronic signature must be unique to one single person; it cannot be reused or reassigned (§100.a). |
| `URS-ESIG-005` | Y | H | The holder's identity must be verified before assigning the electronic signature (§100.b). |
| `URS-ESIG-006` | Y | H | For non-biometric signatures: it must be ensured that an attempt to forge an electronic signature requires the collaboration of at least 2 persons (§200.a.3). |
| `URS-ESIG-007` | Y | H | For non-biometric signatures: it must be ensured that two persons do not obtain the same ID and password combination (§300.a). |
| `URS-ESIG-008` | Y | H | It must be ensured that the correct functioning of the credentials (ID and password) is checked periodically (§300.b). |
| `URS-ESIG-009` | Y | H | Periodic password expiry with mandatory renewal must be implemented (§300.b). |
| `URS-ESIG-010` | Y | H | The blocking or revocation of the identification must be regulated for cases of leaving the company or changing department (§300.b). |
| `URS-ESIG-011` | Y | H | It must be possible to electronically disable an access device or ID/password combination in case of loss (§300.c). |
| `URS-ESIG-012` | Y | H | For non-biometric signatures: unauthorized access attempts must be logged and the results reported periodically to management (§300.d). |
| `URS-ESIG-013` | Y | H | Describe the electronic signature mechanism (smartcard, fingerprint, etc.). If only ID/password is used: specify the minimum length of each (§200.a.1.i). |
| `URS-ESIG-014` | Y | H | Describe whether multiple consecutive signatures on screen are required. If so: the password must be re-entered for each signature (§200.a.1.ii). |
| `URS-ESIG-015` | Y | H | An organizational procedure must exist for cases of loss of access devices (smartcards, tokens): electronic disabling + strict control of any physical relocation (§300.c). |
| `URS-ESIG-016` | Y | H | When putting access devices into operation, a commissioning test must be performed, including verification against unauthorized tampering. Thereafter, periodic testing (§300.e). |
| `URS-ESIG-017` | Y | H | **Tamper-evidence**: signed records must implement controls ensuring the signed record **cannot be modified** or, alternatively, that any subsequent modification makes the record **appear as unsigned** (EU Annex 11 §13.7-13.8 p.11). |
| `URS-ESIG-018` | Y | H | **Hybrid solution** (handwritten signature on paper over an electronic record): if implemented, a high degree of certainty must be ensured that any change to the electronic record invalidates the signature — typically via a **checksum/hash** of the electronic record printed on the signature page (EU Annex 11 §13.9 p.11). *(Activate only if the organization uses hybrid signatures.)* |
| `URS-ESIG-NNN` |  |  | *(add additional system-specific requirements, starting at NNN=019)* |

---

### 9.4 Data structure requirements — `URS-DATA-NNN`

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-DATA-001` |  |  | *e.g.: "Since the system is 21 CFR Part 11 relevant, the data model must support large volumes together with the audit trail functionality."* |
|  |  |  |  |

---

### 9.5 Reports and listings requirements — `URS-REPORT-NNN`

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-REPORT-001` |  |  | *e.g.: "The system shall generate a monthly report with all temperature readings of the period, exportable to a signed PDF."* |
|  |  |  |  |

---

### 9.6 Data flow requirements — `URS-FLOW-NNN`

> Include flow diagrams where possible. Each requirement derived from a diagram must also be transcribed as text in the table.

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-FLOW-001` |  |  |  |
|  |  |  |  |

---

### 9.7 Data security requirements — `URS-SEC-NNN`

> [!warning] Annex 11 2025 modernization preset — activate for cloud/SaaS or remote-access systems
> The following requirements are **post-2011 modernization** of EU Annex 11. For cloud/SaaS, multi-tenant or remotely accessible systems from outside controlled perimeters, they are typically mandatory. If the system is on-premises with no remote access, mark as `N/A — on-premises system with no remote access`.

| ID-No. | GxP | Prio. | Requirement |
|---|---|---|---|
| `URS-SEC-001` | Y | H | **Encryption of critical GxP data** at rest (at-rest) and in transit (in-transit). Cryptographic algorithms, key management, and key rotation documented (EU Annex 11 §10 — *encryption of critical data*). |
| `URS-SEC-002` | Y | H | **Multi-Factor Authentication (MFA)** mandatory for remote authentication of critical systems from outside controlled perimeters (EU Annex 11 §11.6 p.9 — NEW vs 2011). |

**System-specific requirements:**

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-SEC-003` |  |  | *e.g.: "Continuous monitoring of unauthorized access with real-time alarms must be implemented."* |
|  |  |  |  |

---

### 9.8 Organization / process requirements — `URS-PROC-NNN`

Check whether additional SOPs are required for system operation.

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-PROC-001` |  |  | *e.g.: "An SOP for qualification of associated equipment must be created."* |
|  |  |  |  |

---

### 9.9 User interface requirements — `URS-UI-NNN`

Define interface standards and reference mockups if any exist.

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-UI-001` |  |  | *e.g.: "The UI shall be a Windows application compatible with resolutions ≥1920×1080."* |
|  |  |  |  |

---

### 9.10 Interface requirements — `URS-API-NNN`

Interfaces with other systems, internal modules, devices. Always describe **from the receiving system's perspective**.

> [!warning] Annex 11 2025 preset — activate if there are interfaces transferring GxP data
> EU Annex 11 §10 requires that interfaces transferring GxP data be **validated**. If the system is standalone with no interfaces, mark `URS-API-001` as `N/A — standalone system with no interfaces`.

| ID-No. | GxP | Prio. | Requirement |
|---|---|---|---|
| `URS-API-001` | Y | H | All interfaces that transfer GxP data must be **validated**: correct input checks, documented error handling, end-to-end verifiable flow integrity, encryption if data crosses untrusted perimeters (EU Annex 11 §10 — *validated interfaces*). |

**System-specific requirements:**

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-API-002` |  |  | *e.g.: "Data xy will be sent to the connected weighing system attached to SAP; data yz will be returned to SAP."* |
|  |  |  |  |

---

### 9.11 Data migration requirements — `URS-MIGR-NNN`

How data is loaded into the system. If it comes from a legacy system, describe format, mapping and validation. See also MIGRATION PLAN (when it exists in the cascade).

> [!warning] Annex 11 2025 + GAMP 5 D7 preset — activate if legacy data must be migrated
> If there is NO data migration (greenfield system), mark `URS-MIGR-001` as `N/A — no legacy data migration`.

| ID-No. | GxP | Prio. | Requirement |
|---|---|---|---|
| `URS-MIGR-001` | Y | H | Data migration from predecessor systems must be **validated**: approved migration plan, documented source↔target mapping, verification of each migrated record, preserved audit trail, formal post-migration sign-off. During the migration project, unrelated changes (software versions, DB schemas) must be **frozen** (EU Annex 11 §10 + GAMP 5 §D7). |

**System-specific requirements:**

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-MIGR-002` |  |  |  |
|  |  |  |  |

---

### 9.12 Archiving requirements — `URS-ARCH-NNN`

> Although archiving belongs operationally to system operation, **21 CFR Part 11** elevated it to a critical topic deserving its own section. Define what data is archived, retention period, format, media, and the migration plan across software versions.

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-ARCH-001` |  |  |  |
|  |  |  |  |

Also consider:
- Selection of the archiving solution provider / vendor
- Storage concept (e.g.: jukebox / SAN / cloud)
- Media selection (WORM, CD, S3 object-lock, etc.)
- Estimated volume (month/year)
- Interfaces with generating systems
- Room / data center requirements
- Operational responsibilities
- Conversion strategy vs. keeping the predecessor software version on upgrades

---

### 9.13 System operation and environment requirements — `URS-OPS-NNN`

The broadest requirement of the URS. Cover at minimum:

- Incident-, problem-, change-, request-, configuration-, release-management
- Backup / recovery / restore (see it service mgmt policy)
- User management and authorization concept (see `URS-EREC-004` and `URS-EREC-009`)
- System training and maintenance
- Periodic monitoring
- Periodic Review (see periodic review)
- Disaster Recovery and emergency handling
- Security and antivirus protection
- Responsibilities during operation
- Server room requirements (UPS, temperature range, humidity)

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-OPS-001` |  |  | *e.g.: "The server room shall have a UPS with ≥30 min autonomy; controlled temperature in the 18–24 °C range; relative humidity 40–60 %."* |
|  |  |  |  |

---

### 9.14 Documentation requirements — `URS-DOCS-NNN`

Define which documentation must be delivered for users, system operators, support, and administrators.

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-DOCS-001` |  |  |  |
|  |  |  |  |

---

### 9.15 Life cycle

#### 9.15.1 Testing requirements — `URS-TEST-NNN`

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-TEST-001` |  |  | *e.g.: "Specific test data sets for load scenarios; network failure simulations."* |
|  |  |  |  |

#### 9.15.2 Components to be delivered — `URS-DELIV-NNN`

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-DELIV-001` |  |  | **Documents**: define which documents the supplier will deliver (FS, OQ/PQ specs, design spec, user manual, etc.). |
| `URS-DELIV-002` |  |  | **Identification scheme**: how delivered units are uniquely identified. |
| `URS-DELIV-003` |  |  | **Distribution mode**: format and media of delivery of the components. |
|  |  |  |  |

---

## 10. Peripheral and auxiliary equipment — `URS-PERIPH-NNN`

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-PERIPH-001` |  |  | *e.g.: "Hand-held terminals with xy capability."* |
| `URS-PERIPH-002` |  |  | *e.g.: "Scanner and color printer at each workstation."* |
|  |  |  |  |

---

## 11. Hardware specification — `URS-HW-NNN`

| ID-No. | GxP (Y/N) | Prio. (H/M/L) | Requirement |
|---|---|---|---|
| `URS-HW-001` |  |  | Define hardware requirements (CPU, RAM, storage, network bandwidth, GPUs if ML, etc.). |
|  |  |  |  |

---

## 12. Related documents

| Document | Reference |
|---|---|
| Organization's CSV Policy | `{{org_csv_policy_ref}}` |
| Computerized System Operation Policy | `{{org_cs_operation_ref}}` |
| System registration and assessment | [GXP-ASSESS](GXP-ASSESS.md) |
| Validation Plan | [VP](VP.md) |
| Risk Analysis | [RA-INIT](RA-INIT.md) |
| Data Privacy Assessment | [DPIA](DPIA.md) *(if applicable)* |
| `{{custom_ref}}` |  |

---

## 13. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{author_name}}`, `{{author_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] Per-organization ID scheme
> The template uses `{{system_id}}` as a neutral placeholder. Each organization substitutes it with its corporate scheme (possible examples: `PROJ-2026-001-URS-v1.0`, a 5-digit `<year><sequential>`, `<area>-<system>-<version>`, etc.). The canonical rule is that **the identifier must be unique and persistent throughout the whole life cycle** (URS → FS → DS → Verification protocols (IQ/OQ/PQ as filenames per CSV industry convention) → Validation Report → Periodic Review → Decommissioning). *(Note GAMP 5 §4.2.6.4: "IQ/OQ/PQ" terminology is not prescriptive — it corresponds to installation / functional / fitness verification. The file names are kept by industrial convention.)*

> [!note] Template origin + modernization (Round 1.5 2026-05-27; translated to EN Round 2 2026-05-29)
> Round 1 merged two sources from the industrial CSV catalog: V-Model structure + 22 proprietary acronyms; 28 preset 21 CFR Part 11 requirements (12 EREC + 16 ESIG). Round 1.5 (2026-05-27) added **Annex 11 2025 modernization**: URS-EREC-013 (ALCOA+), URS-EREC-014 (peer review audit trail), URS-ESIG-017 (tamper-evidence), URS-ESIG-018 (hybrid wet-ink+hash), URS-SEC-001/002 (encryption + remote MFA), URS-API-001 (validated interfaces), URS-MIGR-001 (validated migration). Current preset count: **14 EREC + 18 ESIG + 2 SEC + 1 API + 1 MIGR = 36 preset canonical requirements**. Round 2 (2026-05-29) translated the template to English canonical.

> [!note] Contradiction documented in the source
> The canonical [Validation Plan](VP.md) declares a defect-severity taxonomy (Critical / Major / Minor + 7 functional types), but the test-spec templates (`IQ`, `09-test-spec-cat1`) do **not** formally apply this taxonomy. See the `> [!warning]` callout in those templates where the inconsistency is flagged so each organization decides whether to enforce it in its instantiation.

> [!tip] Natural output of this template
> A well-written URS **automatically** produces the left-hand column of the traceability matrix. Each `URS-<CATEGORY>-NNN` is referenced 1..N times as `FS-<CATEGORY>-NNN` in the Functional Specification, as `DS-<CATEGORY>-NNN` in the Design Spec (Cat 4/5), and as an entry in the test cases of the verification protocols (`IQ.md` / `OQ.md` / `PQ.md` — naming per CSV industry convention; equivalent GAMP terminology: installation / functional / fitness verification per §4.2.6.4).

## Related

- [GXP-ASSESS](GXP-ASSESS.md) · [VP](VP.md) · [RA-INIT](RA-INIT.md) · [FS](FS.md) · [DS](DS.md)
- GAMP 5 · 21 CFR Part 11 · EU Annex 11
- V-Model · user requirements specification · specification traceability

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for an agnostic AI running the `instantiate-urs` skill or equivalent.

### Order of questions to the user

A skill that instantiates this template must follow this interaction flow. Each step gathers the minimum information needed to fill the corresponding placeholders.

1. **System identity** *(placeholders: `system_name`, `system_id`, `supplier`, `version`, `intended_use`)*
   - Ask for name, ID, supplier, base-product version, and regulatory intended use (1-3 testable sentences).
   - If an instantiated `GXP-ASSESS.md` exists, the skill may inherit it instead of asking again.

2. **GAMP categorization** *(placeholder: `gamp_category`)*
   - If an instantiated `RA-INIT.md` exists, read the category from its frontmatter.
   - If not, ask: "which GAMP category applies? 1 (infrastructure), 3 (standard product), 4 (configured), 5 (custom)?" — guide the user with the canonical criteria.

3. **21 CFR Part 11 / EU Annex 11 applicability** *(activation of the `URS-EREC` preset)*
   - Ask: *"does this system generate or store GxP electronic records as the primary source?"*
   - If **Yes** → activate the URS-EREC preset (copy the 14 requirements into the document).
   - If **No** → mark section 9.2 as `N/A — the system is not 21 CFR Part 11 / Annex 11 relevant` and keep the section.

4. **Electronic signatures applicability** *(activation of the `URS-ESIG` preset)*
   - Ask: *"does the system implement electronic signatures (not just scanned ones)?"*
   - If **Yes** → activate the URS-ESIG preset.
   - If **No** → mark section 9.3 as `N/A — the system does not use Part 11 electronic signatures`.

5. **Performance constraints** *(section 8 — `URS-PERF`)*
   - Ask for concrete, testable metrics: response time, throughput, concurrent users, uptime SLA, recovery time objective, etc.

6. **Interfaces** *(section 9.10 — `URS-API`)*
   - List connected systems. Describe **always from the receiver's perspective** (canonical rule).

7. **For each applicable category code** *(sections 5–11)*
   - For each acronym (DEVENV, QUAL, TRAIN, PERF, FUNC, DATA, REPORT, FLOW, SEC, PROC, UI, API, MIGR, ARCH, OPS, DOCS, TEST, DELIV, PERIPH, HW): ask which system-specific requirements fall into that category.
   - For N/A categories: mark explicitly with a reason.
   - The italic example embedded in each section serves as a few-shot to guide the user toward well-written requirements (testable, measurable).

8. **Signatures matrix** *(section 0)*
   - Designate at least 1 author + 1 reviewer + 1 approver with name and department. Actual signatures are applied outside the document (corporate 21 CFR Part 11-compliant system).

### Stop criteria ("complete" instance)

The skill considers the URS complete only if:

- [ ] All `placeholders.required: true` are filled (no unsubstituted `{{...}}` remain)
- [ ] The 22 category-code sections each have at least `N/A — reason` or ≥1 instantiated requirement
- [ ] Section 4.1-4.4 (Project Context) has non-empty descriptions
- [ ] If `gamp_category == 5`: URS-DEVENV, URS-QUAL, URS-TRAIN each have ≥3 requirements
- [ ] If `preset_part11_active == true`: URS-EREC and URS-ESIG are copied with human case-by-case applicability verification (not a blind copy)
- [ ] If `preset_part11_active == false`: URS-EREC and URS-ESIG carry an explicit "N/A — reason" mark
- [ ] The signature table (section 0) has ≥1 author + ≥1 reviewer + ≥1 approver with name + department
- [ ] Every requirement row has non-empty `GxP (Y/N)` and `Prio (H/M/L)`

### `status` transitions

```
draft ──[meet stop criteria]──> in-review
in-review ──[approver signatures applied]──> approved
approved ──[new version issued]──> superseded
```

- Only `draft` and `in-review` allow free edits.
- In `approved`, any edit requires issuing a new version (increment the `version` semver; the previous becomes `superseded`, with `supersedes:` pointing to the prior version).
- The canonical "no deletion, only strike-through" rule applies to requirements that become obsolete within an active version.

### Downstream mapping — how requirements trace to FS / RA / IQ

| Origin (URS) | Destination | Cardinality | Rule |
|---|---|---|---|
| `URS-<CATEGORY>-NNN` with `GxP=Y` | `FS-<CATEGORY>-NNN` in `FS.md` | 1:N (one URS req may generate several FS reqs) | The FS expands the URS "what" into the concrete "how" |
| `URS-<CATEGORY>-NNN` with `GxP=Y` | Row in `RA-INIT.md` | 1:1 mandatory | Each GxP requirement must have a risk evaluation |
| `URS-<CATEGORY>-NNN` with `prio=H` | Test case in `IQ.md` / `OQ.md` / `test-script.md` | 1:N | Critical H reqs generate at least one test case |
| `URS-<CATEGORY>-NNN` with `GxP=N` | Optionally FS, optionally test | 1:0 or 1:1 | Non-GxP reqs may fall outside the formal validation scope |

A future `validate-traceability` skill reads `specs/URS.md` + `specs/FS.md` + `specs/RA-INIT.md` and emits a consistency report: URS requirements without an FS counterpart, orphan FS requirements, RA coverage gaps, etc.
