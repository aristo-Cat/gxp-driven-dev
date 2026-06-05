---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "VP — Validation Plan (canonical CSV template)"
type: template
template_class: csv
template_id: "VP"
template_version: "0.1.0"
v_model_phase: planning
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-28
updated: 2026-05-29
# Round 2 (2026-05-29): translated to English canonical (was language: es). §-citations + IDs preserved verbatim.

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# VP is the per-system UMBRELLA document (GAMP 5 §M1 Validation Planning).
# It plans and authorizes all V-Model deliverables for ONE system.
# Distinct from the VMP (Validation Master Plan), which governs multiple systems.
inputs:
  - template_id: "GXP-ASSESS"
    required: true
    description: "Approved GxP Assessment — the VP is only produced if validation_required == true"
  - template_id: "RA-INIT"
    required: false
    description: "Initial Risk Assessment — contributes the GAMP category and risk-based strategy to the VP"
outputs:
  - artifact: "VP instance (Markdown) — per-system Validation Plan"
    consumed_by:
      - "URS"        # the VP authorizes and frames the URS (may absorb it for simple Cat 3)
      - "RA-INIT"    # the VP references the QRM strategy
      - "IQ"         # the VP defines the testing approach that IQ/OQ/PQ follow
      - "OQ"
      - "PQ"
      - "VR"         # the Validation Report closes against this VP
applicable_regulations:
  - "gamp-5"          # §M1 (Validation Planning) pp.85-92
  - "21-cfr-part-11"  # §11.10.a validation
  - "eu-annex-11"     # §4 (Risk Management) + §9 (Qualification and Validation)
based_on:
  - "GAMP 5 §M1 (Validation Planning) — content §9.3.3: intro/scope, system overview, org structure, QRM approach, validation strategy (incl. Agile), deliverables, acceptance criteria, change control, SOPs, supporting processes"
  - "Structure: per-system umbrella document; deliverables matrix by GAMP category; acceptance criteria; release strategy"

# ─── Relationship to the VMP ─────────────────────────────────────────────────
# VMP (Validation Master Plan, template_family: master) governs MULTIPLE
# systems and declares templates_active at program level. The VP (this) is
# PER-SYSTEM. One VMP may encompass many VPs. For a small org with a
# single system, the VP alone may be sufficient without a VMP.
relationship_to_vmp:
  vmp_scope: "program / multiple systems (Constitution)"
  vp_scope: "one specific system (this document)"
  rule: "The VP inherits policies from the VMP if one exists; otherwise declares them locally"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
  system_id:
    type: string
    required: true
  gxp_assess_ref:
    type: string
    required: true
    description: "Identifier of the approved GXP-ASSESS that triggers this VP"
  gamp_category:
    type: enum
    required: true
    values: [3, 4, 5]
    description: "GAMP category (from RA-INIT) — determines the deliverables matrix"
  project_objective:
    type: string
    required: true
  system_description:
    type: string
    required: true
  end_users:
    type: string
    required: true
  related_systems:
    type: string
    required: false
  validation_strategy:
    type: string
    required: true
    description: "Validation strategy: lifecycle (V-Model linear or iterative/Agile), risk-scaled rigor"
  acceptance_criteria:
    type: string
    required: true
    description: "Global project acceptance criteria (incl. MVP/DoD if Agile)"
  release_strategy:
    type: enum
    required: true
    values: ["final-only", "conditional-then-final"]
    description: "Release strategy: final-only, or conditional followed by final"
  roles_assigned:
    type: map
    required: true
    description: "Mapping of GAMP §6.2.3 roles to project persons/teams"
  vmp_ref:
    type: string
    required: false
    description: "Reference to the VMP that encompasses this VP (if one exists)"
  vp_author_name:
    type: string
    required: true
  vp_author_dept:
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
    - based_on_template: "VP"
    - based_on_template_version
    - system_id
    - traces_to            # GXP-ASSESS instance
    - gamp_category
    - status               # draft | in-review | approved | superseded
    - version
    - created
    - updated
    - language
  conditional_fields:
    - approved_by: "required if status == approved (Process Owner + Quality Unit, GAMP M1)"
    - supersedes
    - vmp_ref: "if the VP is under a VMP"

# ─── Validation rules (Round 1 subset) ──────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "traces_to must point to an approved GXP-ASSESS with validation_required == true"
  - "The deliverables matrix (§7) must be consistent with gamp_category"
  - "Approved by Process Owner + Quality Unit (GAMP 5 §M1 §9.3.3)"
  - "If validation_strategy is Agile/iterative → acceptance_criteria must include Definition of Done"
  - "If release_strategy == 'conditional-then-final' → must document the conditions of the conditional release"
  - "If SaaS → the VP must explicitly describe which activities the service provider executes (GAMP 5 §M1)"

tags:
  - template
  - csv
  - validation-plan
  - vp
  - planning
  - gamp-m1
  - canonical
---

# VP — Validation Plan

> [!note] Canonical CSV template — per-system umbrella document
> **Canonical** template for the **Validation Plan (VP)** — the document that plans and authorizes **all** validation activities for **one system** (GAMP 5 §M1 pp.85-92). Defines which deliverables are produced, roles, acceptance criteria, testing strategy and release strategy. Approved by Process Owner + Quality Unit.

> [!warning] VP ≠ VMP
> The **VP** (this document) is **per-system**. The [VMP](VMP.md) (Validation Master Plan, `template_family: master`) governs **multiple systems** at program level and plays the role of Constitution. One VMP may encompass many VPs. A small organization with a single system may use only the VP.

> [!tip] Embedded usage rules
> 1. **Triggered by GXP-ASSESS** — the VP is only produced if the [GxP Assessment](GXP-ASSESS.md) determined `validation_required == true`.
> 2. **Umbrella with absorption** — for simple Cat 3, the VP may absorb the URS / RA / Data Migration Plan.
> 3. **Matrix by category** — mandatory deliverables depend on the GAMP category (§7).
> 4. **Risk-based + lifecycle** — the strategy may be V-Model linear or iterative/Agile (GAMP 5 §M1 supports both; Annex 11 §6.1 endorses Agile).
> 5. **Release strategy** — final-only or conditional-then-final (with documented conditions).
> 6. **Approval** — Process Owner + Quality Unit (minimum per GAMP M1).

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **GxP Assessment that triggers it** | `{{gxp_assess_ref}}` ([GXP-ASSESS](GXP-ASSESS.md)) |
| **GAMP category** | `{{gamp_category}}` |
| **VMP that encompasses it** | `{{vmp_ref}}` ([VMP](VMP.md) — if applicable) |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Author (CSV/SME) | `{{vp_author_name}}` | `{{vp_author_dept}}` |  |  |
| Reviewer (System Owner) |  |  |  |  |
| Approver 1 (Process Owner) |  |  |  |  |
| Approver 2 (Quality Unit) |  |  |  |  |

---

## 1. Introduction

This **Validation Plan (VP)** plans and authorizes the validation activities for the system **`{{system_name}}`**, in accordance with GAMP 5 §M1. It is the umbrella document of the project: it defines the scope, deliverables, roles, acceptance criteria and release strategy.

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| VP | Validation Plan — per-system validation plan (GAMP 5 §M1) |
| VMP | Validation Master Plan — multi-system master plan (Constitution) |
| Deliverable | V-Model deliverable (URS, FS, RA, IQ, OQ, PQ, VR, etc.) |
| Conditional release | Conditional release with documented deficiencies having no impact on PS/PQ/DI |
| DoD | Definition of Done (Agile) |

---

## 3. Project overview

### 3.1 Project objective
`{{project_objective}}`

### 3.2 System description
`{{system_description}}`

### 3.3 End users
`{{end_users}}`

### 3.4 Related systems
`{{related_systems}}`

### 3.5 Validation obligation
- **GAMP category**: `{{gamp_category}}`
- **Electronic records/signatures**: (from [GXP-ASSESS](GXP-ASSESS.md))
- **GxP justification**: (reference to the GxP Assessment)

---

## 4. Roles and responsibilities

> Mapping of GAMP §6.2.3 roles to persons/teams: `{{roles_assigned}}`

| GAMP §6.2.3 Role | Person / Team | Responsibility in the project |
|---|---|---|
| Process Owner |  | Process owner; approves URS + VP + VR |
| System Owner |  | Availability/support; releases the system |
| Data Owner |  | Ownership of GxP data |
| Quality Unit |  | Approves key deliverables; owns compliance risks |
| SME |  | Leads verification |
| Supplier |  | Creates/configures; executes agreed testing |
| End User |  | Input to requirements; executes PQ |

---

## 5. Project team training

| Person | Required training | Completed (✓) |
|---|---|---|
|  | GxP + CSV + system |  |

---

## 6. Validation approach / Quality concept

### 6.1 Validation principles
Strategy: `{{validation_strategy}}` (V-Model linear or iterative/Agile; rigor scaled by risk from [RA-INIT](RA-INIT.md)).

### 6.2 Change management and deviations before go-live
> Pre-go-live deviations are managed within this VP / project deviation log. Post-go-live, operational change control and deviations apply.

### 6.3 Acceptance criteria
`{{acceptance_criteria}}`

Minimum generic criteria:
- [ ] All test scripts executed and approved
- [ ] No open critical defects
- [ ] Complete URS→FS→tests traceability ([RTM](RTM.md))
- [ ] Validation Report approved

### 6.4 Release to production / operation
Strategy: `{{release_strategy}}`

---

## 7. Validation activities (deliverables matrix by category)

> The applicable column depends on `{{gamp_category}}`. ✓ = mandatory, ○ = optional/integratable, — = not applicable.

| Deliverable | Cat 3 | Cat 4 | Cat 5 |
|---|---|---|---|
| [GxP Assessment](GXP-ASSESS.md) | ✓ | ✓ | ✓ |
| **VP** (this document) | ✓ | ✓ | ✓ |
| [Initial Risk Assessment](RA-INIT.md) | ✓ | ✓ | ✓ |
| [URS](URS.md) | ✓ | ✓ | ✓ |
| [Supplier Assessment](SUP-ASSESS.md) | ○ | ✓ | ✓ |
| [FS](FS.md) | ○ | ✓ | ✓ |
| [Configuration Spec](CS.md) | — | ✓ | ○ |
| [Design Spec](DS.md) | — | ○ | ✓ |
| [Detailed Risk Assessment](RA-DET.md) | ○ | ✓ | ✓ |
| [IQ](IQ.md) | ✓ | ✓ | ✓ |
| [OQ](OQ.md) | ✓ | ✓ | ✓ |
| [PQ](PQ.md) | ○ | ✓ | ✓ |
| [Traceability Matrix](RTM.md) | ✓ | ✓ | ✓ |
| [Validation Report](VR.md) | ✓ | ✓ | ✓ |

---

## 8. Testing activities

### 8.1 Test phases
IQ / OQ / PQ (see matrix §7). Defect classification by severity:

| Severity | Criterion |
|---|---|
| **Critical** | Impact on PS/PQ/DI; blocks release |
| **Major** | Significant functional impact without directly affecting PS/PQ/DI |
| **Minor** | Cosmetic / minor; does not block |

Defect types: Application / Functionality / Data / Tester / Documentation / Test Script / Other.

### 8.2 Test environment
(define server, OS, network, DB, clients, test data)

### 8.3 Test documentation
Each deviation is recorded and evaluated with the quality function.

---

## 9. Data migration
(if applicable — reference to [URS](URS.md) §9.11 + migration plan)

## 10. Decommissioning of predecessor systems
(if applicable)

## 11. End-user training and system SOPs
(SOPs to be created/updated for operation)

## 12. Documentation guidelines / document management
(version control, approvals)

## 13. Methods and tools
(development, design, documentation/testing tools)

## 14. Data integrity
> Data integrity is assured by defining DI/ALCOA+ requirements in the [URS](URS.md) (URS-EREC-013) and testing them in IQ/OQ/PQ — it is not a separate process.

---

## 15. Related documents

| Document | Reference |
|---|---|
| GxP Assessment | `{{gxp_assess_ref}}` ([GXP-ASSESS](GXP-ASSESS.md)) |
| VMP (if applicable) | `{{vmp_ref}}` ([VMP](VMP.md)) |
| Initial Risk Assessment | [RA-INIT](RA-INIT.md) |
| URS | [URS](URS.md) |
| Validation Report | [VR](VR.md) |
| Organization's CSV Policy | `{{org_csv_policy_ref}}` |
| `{{custom_ref}}` |  |

---

## 16. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{vp_author_name}}`, `{{vp_author_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] Per-system VP vs multi-system VMP
> The VP plans ONE system. If the organization validates many systems, the [VMP](VMP.md) governs them at program level and each system has its own VP that inherits the VMP's policies.

> [!note] Umbrella document with absorption
> For simple Cat 3, the VP may absorb the URS/RA/Data Migration Plan. The matrix in §7 marks with ○ the integratable deliverables.

> [!tip] GAMP M1 approval
> Minimum: Process Owner + Quality Unit. For SaaS, the VP must describe which activities the service provider executes.

## Related

- [GXP-ASSESS](GXP-ASSESS.md) · [VMP](VMP.md) · [RA-INIT](RA-INIT.md) · [URS](URS.md) · [VR](VR.md)
- GAMP 5 · 21 CFR Part 11 · EU Annex 11
- V-Model · validation plan deliverables · gamp categories

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.init` skill / orchestrator.

### Pre-flight

1. **Read `.gxp-dev.yaml`** + locate approved GXP-ASSESS (`specs/GXP-ASSESS.md`) with `validation_required == true`.
2. **Read RA-INIT if it exists** — contributes category + risk-based strategy.
3. **Read VMP if it exists** — inherit program-level policies.
4. **Read `templates/csv/VP.md`** from the toolkit as the source template.

### Generation flow

1. **Inherit identity** from the GXP-ASSESS (name/id/intended_use/category).
2. **Project overview** (§3): objective, description, end-users, validation obligation.
3. **Roles** (§4): map GAMP §6.2.3 to persons.
4. **Strategy** (§6): lifecycle (linear/Agile), acceptance criteria, release.
5. **Deliverables matrix** (§7): mark mandatory items per category.
6. **Anti-hallucination**: `[NEEDS CLARIFICATION: ...]` when information is missing.
7. **Output**: write `specs/VP.md` (status: draft).
8. **Post-flight**: `validate-frontmatter.py` + `check-clarification-markers.py`.

### `status` transitions

```
draft ──[overview + roles + strategy + matrix complete]──> in-review
in-review ──[Process Owner + QU sign]──> approved
approved ──[new version]──> superseded
```

### Downstream mapping

| Origin (VP) | Destination | Rule |
|---|---|---|
| Deliverables matrix | Entire project | Defines which templates are instantiated |
| Acceptance criteria | VR | The Validation Report closes against these |
| Testing strategy | IQ/OQ/PQ | Defines the approach the protocols follow |
| Roles | All deliverables | Consistent signatures across the entire project |
