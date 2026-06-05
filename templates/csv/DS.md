---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "DS — Design Specification (canonical CSV template)"
type: template
template_class: csv
template_id: "DS"
template_version: "0.1.0"
v_model_phase: design-specification
gamp_categories_applicable: [5]
language: en
status: canonical-draft
created: 2026-05-28
updated: 2026-05-29
# Round 2 (2026-05-29): translated to English canonical (was language: es). §-citations + IDs preserved verbatim.

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# DS is the detailed hw/sw design of a custom Cat 5 application
# (GAMP 5 §D3.3.1.2). It hangs from the FS (realises the functional "how" into
# technical hw/sw design) and is verified in IQ (installation) + OQ (functional). Paired with IQ.
inputs:
  - template_id: "FS"
    required: true
    description: "Functional Specification — the FS defines the functional what; the DS realises it in detailed technical hw/sw design"
  - template_id: "RA-INIT"
    required: false
    description: "Risk Assessment — scales the design detail for critical modules"
outputs:
  - artifact: "DS instance (Markdown) — detailed hw/sw design"
    consumed_by:
      - "IQ"        # IQ verifies that the deployed build matches the DS
      - "OQ"        # OQ verifies the behaviour of the designed modules
      - "RTM"       # traceability DS↔FS↔test
applicable_regulations:
  - "gamp-5"          # §D3.3.1.2 p.199 (Design Specification) + §D4 (software dev/review) + §6.2.7
  - "eu-annex-11"     # §4.4 Specifications
based_on:
  - "GAMP 5 §D3.3.1.2 p.199 (Design Specification — hw design + sw design: modules, interfaces, data hierarchy, error handling) + §D4 (SBOM, coding standards, source-code review)"
  - "Structure: detailed Cat 5 design that makes the implementation maintainable; traceable bottom-up to FS/URS; basis for design review + source-code review + unit/integration testing"

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
    description: "Approved FS whose technical design this DS details"
  architecture_overview:
    type: string
    required: true
    description: "High-level architecture (modules, layers, main interfaces)"
  tech_stack:
    type: string
    required: true
    description: "Languages, frameworks, runtime, database"
  has_hardware:
    type: boolean
    required: false
    description: "true if the Cat 5 system includes custom hardware"
  ds_author_name:
    type: string
    required: true
  ds_author_dept:
    type: string
    required: true
  custom_ref:
    type: string
    required: false

# ─── Instance frontmatter spec ──────────────────────────────────────────────
instance_frontmatter_spec:
  required_fields:
    - title
    - type: "instance"
    - based_on_template: "DS"
    - based_on_template_version
    - system_id
    - traces_to            # FS instance
    - status               # draft | in-review | approved | superseded
    - version
    - created
    - updated
    - language
  conditional_fields:
    - approved_by: "required if status == approved"
    - supersedes
    - sbom_ref: "reference to the Software Bill of Materials (GAMP 5 §D4)"

# ─── Validation rules (Round 1 subset) ──────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "traces_to must point to an approved FS"
  - "Each DS-<CATEGORY>-NNN must cite the FS-ID it designs (bottom-up traceability)"
  - "The DS must be sufficient for a developer who is not the author to maintain the code"
  - "The DS must be kept in sync with the code (avoid spec-code drift)"
  - "Cat 5 only — do not require a DS for Cat 3/4 (Cat 4 uses CS)"
  - "Software Bill of Materials (SBOM) referenced for components/dependencies (GAMP 5 §D4)"

tags:
  - template
  - csv
  - design-specification
  - ds
  - gamp-d3
  - cat5
  - canonical
---

# DS — Design Specification

> [!note] Canonical CSV template — Cat 5
> **Canonical** template for the **Design Specification (DS)** — the **detailed hardware/software design** of a custom application (Cat 5): high-level architecture + low-level module design (GAMP 5 §D3.3.1.2 p.199). It hangs from the [FS](FS.md) (realises the functional "how" into technical design) and is the basis for the design review, source-code review and unit/integration testing. Verified in [IQ](IQ.md) (installation).

> [!tip] Embedded usage rules
> 1. **Cat 5 only** — the DS is essential for custom software. Cat 4 uses [CS](CS.md); Cat 3 does not require one.
> 2. **Makes the code maintainable** — the DS must allow a developer who is not the author to maintain the code. An overly brief DS = difficult maintenance.
> 3. **Bottom-up traceability** — each `DS-<CATEGORY>-NNN` traces to FS/URS. Drives unit + integration test design.
> 4. **Anti-drift** — the DS is kept in sync with the code; spec-code drift is a gap.
> 5. **SBOM** (GAMP 5 §D4) — reference the Software Bill of Materials for components/dependencies + OSS hygiene.
> 6. **HW + SW** — includes Hardware Design Spec (if custom hw is present) + Software Design Spec.

---

## 0. Identification and signatures

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **FS being designed** | `{{fs_ref}}` ([FS](FS.md)) |
| **Technology stack** | `{{tech_stack}}` |
| **Includes custom hardware?** | `{{has_hardware}}` |

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Author (developer / architect) | `{{ds_author_name}}` | `{{ds_author_dept}}` |  |  |
| Reviewer (SME / design review) |  |  |  |  |
| Approver (System Owner) |  |  |  |  |
| Approver (Quality Unit) |  |  |  |  |

---

## 1. Objective

Specify the detailed hardware/software design of the custom system **`{{system_name}}`**, sufficient to implement, review (design review + source-code review) and maintain the code, technically realising the requirements of the [FS](FS.md) (`{{fs_ref}}`).

---

## 2. High-level architecture

`{{architecture_overview}}`

> Attach architecture diagram: modules, layers, main interfaces, data flows.

---

## 3. Software Design Specification — `DS-<CATEGORY>-NNN`

### 3.1 Modules — `DS-FUNC-NNN`

> Per module: operation, interfaces, error handling, data mapping.

| DS-ID | Designs (FS-ID) | Module | Operation / responsibility | Interfaces | Error handling |
|---|---|---|---|---|---|
| `DS-FUNC-001` | `FS-FUNC-001` |  |  |  |  |
|  |  |  |  |  |  |

### 3.2 Data hierarchy — `DS-DATA-NNN`

| DS-ID | Designs (FS-ID) | Entity / table | Type / format / precision | Relationships |
|---|---|---|---|---|
| `DS-DATA-001` | `FS-DATA-001` |  |  |  |
|  |  |  |  |  |

### 3.3 Interfaces / API — `DS-API-NNN`

| DS-ID | Designs (FS-ID) | Contract (endpoint / protocol) | Request / response | Errors |
|---|---|---|---|---|
| `DS-API-001` | `FS-API-001` |  |  |  |
|  |  |  |  |  |

### 3.4 Security / records / signatures — `DS-SEC-NNN` / `DS-EREC-NNN` / `DS-ESIG-NNN`

| DS-ID | Designs (FS-ID) | Design mechanism | Detail |
|---|---|---|---|
| `DS-SEC-001` | `FS-SEC-001` |  |  |
| `DS-EREC-001` | `FS-EREC-005` | *e.g.: append-only audit trail table + triggers* |  |
|  |  |  |  |

### 3.5 Sub-programs / components

| DS-ID | Designs (FS-ID) | Sub-program | Parameters | Side-effects | Screens/reports |
|---|---|---|---|---|---|
| `DS-FUNC-00X` |  |  |  |  |  |
|  |  |  |  |  |  |

---

## 4. Hardware Design Specification (if `has_hardware == true`) — `DS-HW-NNN`

| DS-ID | Designs (FS/URS-ID) | HW component | Architecture / storage / I/O | Environment / electrical |
|---|---|---|---|---|
| `DS-HW-001` | `FS-HW-001` |  |  |  |
|  |  |  |  |  |

---

## 5. Software Bill of Materials (SBOM)

> GAMP 5 §D4 — components and dependencies + OSS hygiene.

| Component / library | Version | License | OSS hygiene (✓) |
|---|---|---|---|
|  |  |  |  |

---

## 6. Coding and development standards

> GAMP 5 §D4 — coding standards, naming conventions, repository, dead-code removal, source-code review (≥1 independent reviewer).

| Aspect | Definition |
|---|---|
| Coding standards | |
| Naming conventions | |
| Repository / branching | |
| Source-code review | ≥1 independent reviewer |

---

## 7. Related documents

| Document | Reference |
|---|---|
| FS being designed | `{{fs_ref}}` ([FS](FS.md)) |
| Installation Qualification | [IQ](IQ.md) |
| Operational Qualification | [OQ](OQ.md) |
| Configuration Spec (if Cat 4 components) | [CS](CS.md) |
| `{{custom_ref}}` |  |

---

## 8. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{ds_author_name}}`, `{{ds_author_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] DS is for Cat 5
> Custom → DS. Configured → CS. Standard → none. The DS makes the code maintainable and is the basis for the design review + source-code review (GAMP 5 §D4).

> [!note] Bottom-up traceability
> Each design element traces to the FS/URS it realises. This enables impact analysis and drives the design of unit/integration tests.

> [!tip] Anti spec-code drift
> The DS is not a dead document after implementation: it is kept in sync with the code. An outdated DS is worse than having none at all (it misleads the maintainer).

## Related

- [FS](FS.md) · [CS](CS.md) · [IQ](IQ.md) · [OQ](OQ.md) · [RTM](RTM.md)
- GAMP 5 · EU Annex 11
- design specification · specification traceability · gamp category 5 custom application

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. Guidance for the `gdd.ds.from-fs` skill.

### Pre-flight
1. Read `.gxp-dev.yaml` + confirm `gamp_category == 5`. If Cat 4 → use CS. If Cat 3 → not applicable.
2. Locate the approved FS (`specs/FS.md`).
3. Read `templates/csv/DS.md` from the toolkit.

### Flow
1. Parse the custom FS-IDs that require design.
2. For each one, design the module/data/API/security, citing the FS-ID.
3. SBOM + coding standards (§5-§6).
4. HW design if `has_hardware`.
5. Anti-hallucination: `[NEEDS CLARIFICATION: ...]`; never invent technical design or dependencies.
6. Output: `specs/DS.md` (status: draft).
7. Post-flight: `validate-frontmatter.py` + `check-clarification-markers.py`.

### Mapping
| Origin (DS) | Destination | Rule |
|---|---|---|
| `DS-<CATEGORY>-NNN` | IQ | IQ verifies the deployed build against the DS |
| Designed modules | OQ + unit/integration tests | Drives test design |
| Design | RTM | Traceability DS↔FS↔test |
