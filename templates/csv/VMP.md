---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "VMP — Validation Master Plan (canonical template)"
type: template
template_class: csv
template_id: "VMP"
template_version: "0.1.0"
template_family: master
v_model_phase: planning
lifecycle_phase: project
gamp_categories_applicable: [3, 4, 5]   # for profile: pharma; applies to all when profile != pharma
language: en
status: canonical-draft
created: 2026-05-26
updated: 2026-05-26

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# VMP is the root: nothing comes before it; everything else is declared by it.
inputs: []
outputs:
  - artifact: "VMP instance (Markdown) — Validation Master Plan"
    consumed_by:
      - "ALL active templates declared in templates_active"
applicable_regulations:
  - "gamp-5"     # ISPE GAMP 5 2nd Ed (2022), Appendix M1 pp.85-92
  - "eu-annex-11"  # EU GMP Annex 11 §4 validation
  - "ich-q9"     # ICH Q9 (R1) Quality Risk Management
based_on:
  - "ISPE GAMP 5 §M1 (Validation Planning)"
  - "EU GMP Annex 11 §4 (Validation requirements)"
  - "ICH Q9 (R1) (QRM principles)"

# ─── Placeholders (declarative for instantiation skills) ────────────────────
placeholders:
  project_id:
    type: string
    required: true
    description: "Internal project identifier (matches .gxp-dev.yaml `project_id`)"
  project_name:
    type: string
    required: true
  scope:
    type: string
    required: true
    description: "What this VMP covers (system, program, or set of related systems)"
  in_scope_systems:
    type: list
    required: true
    description: "Explicit list of systems in scope"
  out_of_scope_systems:
    type: list
    required: false
    description: "Systems intentionally excluded (with rationale)"
  criticality_policy:
    type: string
    required: true
    description: "How the organization classifies system/data criticality (link to local SOP or inline definition)"
  signature_policy:
    type: string
    required: true
    description: "Electronic / wet-ink signature requirements for approval gates"
  alcoa_plus_enforcement:
    type: string
    required: true
    description: "How ALCOA+ data integrity principles are enforced (PIC/S PI 041-1 anchor)"
  supplier_qualification_policy:
    type: string
    required: false
    description: "How suppliers / vendors are qualified (required if any vendor systems in scope)"
  templates_active:
    type: list
    required: true
    description: "Subset of the 33 canonical templates this project will instantiate. Must match `.gxp-dev.yaml` `templates_active` field."
  roles_assigned:
    type: map
    required: true
    description: "Mapping of GAMP §6.2.3 roles to named individuals or teams"
  validation_strategy:
    type: string
    required: true
    description: "Risk-based approach, lifecycle model (v-model/agile/hybrid), supplier leveraging, traceability strategy"
  acceptance_criteria_for_release:
    type: string
    required: true
    description: "Conditions under which the system can be promoted from in-development to validated"
  author_name:
    type: string
    required: true
  author_role:
    type: string
    required: true

# ─── Validation rules (subset Round 1) ──────────────────────────────────────
validation_rules:
  - "Required placeholders must all be filled (no `{{...}}` remaining)"
  - "`templates_active` in this VMP must match `.gxp-dev.yaml` `templates_active`"
  - "Every role in `roles_assigned` must reference one of the canonical GAMP §6.2.3 roles or a documented project-specific role"
  - "If profile == pharma: `alcoa_plus_enforcement` is mandatory (PIC/S PI 041-1)"
  - "If any vendor system in scope: `supplier_qualification_policy` is mandatory (GAMP 5 M2 + Ch 7)"
  - "Signatures table must have ≥1 author + ≥1 reviewer + ≥1 approver before status: approved"
  - "VMP status transitions: draft → in-review → approved → superseded (no skipping)"

# ─── Instance frontmatter spec (when this template is instantiated) ─────────
instance_frontmatter_spec:
  required_fields:
    - title
    - type: "instance"
    - based_on_template: "VMP"
    - based_on_template_version
    - project_id
    - status     # draft | in-review | approved | superseded
    - version    # semver of the instance
    - created
    - updated
    - language
  conditional_fields:
    - approved_by: "required if status == approved"
    - supersedes: "version of previous VMP if this is a revision"

tags:
  - template
  - csv
  - vmp
  - master
  - validation-planning
  - canonical
---

# VMP — Validation Master Plan

> [!note] Template canonical — Master family
> Plantilla canonical para producir el **Validation Master Plan (VMP)** de un proyecto / programa de validación. El VMP es el documento **root** del lifecycle: declara qué templates están activos, qué roles se asignan, qué política de criticidad / firmas / ALCOA+ / supplier qualification aplica, y cuál es la estrategia de validación. Cada `.gxp-dev.yaml` consumer manifest debe respaldar las decisiones del VMP.
>
> Anchored in **ISPE GAMP 5 §M1 (Validation Planning, pp.85-92)** and **EU GMP Annex 11 §4 (Validation)**. Optional in light-rigor projects; mandatory in `profile: pharma` + `rigor_level: regulated`.

> [!tip] Embedded usage rules
> 1. **VMP is the constitution of the project.** Every downstream artifact (URS, FS, RA, IQ, OQ, PQ, …) operates within the boundaries this VMP sets.
> 2. **`templates_active` declared here is authoritative.** Any spec file in `specs/` that is not in `templates_active` should be deleted or `templates_active` should be updated.
> 3. **Approval is multi-role.** GAMP §6.2.3 requires explicit accountability — Process Owner approves business intent, System Owner approves technical scope, Quality Unit approves the validation approach.
> 4. **Risk-based scaling is the default.** Don't validate what doesn't matter; do validate what could harm patient safety, product quality, or data integrity (ICH Q9 (R1)).
> 5. **One VMP per project**, even for hybrid projects with vendor + custom components. Use `hybrid_breakdown` in `.gxp-dev.yaml` to split component-level work, but the VMP umbrella is single.

---

## 0. Identity and signatures

### Project identity

| Field | Value |
|---|---|
| **Project ID** | `{{project_id}}` |
| **Project name** | `{{project_name}}` |
| **VMP version** | `0.1` (initial draft) |
| **Author** | `{{author_name}}`, `{{author_role}}` |
| **Date drafted** | `{{date}}` |
| **Status** | `draft` |

### Approval matrix

| Role (GAMP §6.2.3) | Name | Department / Org | Date | Signature |
|---|---|---|---|---|
| Process Owner | `{{process_owner_name}}` | `{{process_owner_dept}}` |  |  |
| System Owner | `{{system_owner_name}}` | `{{system_owner_dept}}` |  |  |
| Quality Unit | `{{quality_unit_name}}` | `{{quality_unit_dept}}` |  |  |
| (optional) Data Owner | `{{data_owner_name}}` | `{{data_owner_dept}}` |  |  |
| (optional) Subject Matter Expert | `{{sme_name}}` | `{{sme_dept}}` |  |  |
| (optional) Supplier representative | `{{supplier_name}}` | `{{supplier_org}}` |  |  |

---

## 1. Scope

### 1.1 In scope

`{{scope}}`

**Systems covered by this VMP:**

`{{in_scope_systems}}`

### 1.2 Out of scope

`{{out_of_scope_systems}}`

Rationale for exclusions:

`{{out_of_scope_rationale}}`

---

## 2. Validation approach

### 2.1 Lifecycle model

The project follows the lifecycle declared in `.gxp-dev.yaml`:

- `lifecycle: v-model` — paired specification / verification (URS↔PQ, FS↔OQ, DS↔IQ; ISPE GAMP 5 §3.2 Figure 3.3)
- `lifecycle: agile` — iterative with each sprint producing specification + verification artifacts (ISPE GAMP 5 §3.2 Figure 3.4 + Appendix D8)
- `lifecycle: hybrid` — vendor components follow Validate flow, custom components follow Develop flow, RTM is unified

Concrete strategy for this project:

`{{validation_strategy}}`

### 2.2 Risk-based scaling

Per ICH Q9 (R1) and GAMP 5 §M3, effort and formality scale with risk:

- **Severity** linked to patient safety / product quality / data integrity impact
- **Probability** influenced by GAMP category (Cat 1 < Cat 3 < Cat 4 < Cat 5)
- **Detectability** considers both automated and manual detection

Initial categorization is documented in `specs/GXP-ASSESS.md` (if `profile: pharma`) and `specs/RA-INIT.md`. The detailed FMEA happens after URS+FS approval in `specs/RA-DET.md`.

### 2.3 Active templates

The following canonical templates are instantiated by this project (consistent with `.gxp-dev.yaml` `templates_active`):

`{{templates_active}}`

---

## 3. Roles and responsibilities

Per GAMP 5 §6.2.3.

`{{roles_assigned}}`

Minimum required:

- **Process Owner**: accountable for business intent and data ownership
- **System Owner**: accountable for technical operation
- **Quality Unit**: accountable for validation approach and compliance posture

Recommended (depending on system complexity):

- Subject Matter Expert (SME)
- Data Owner (if distinct from Process Owner)
- Supplier representative (if vendor components in scope)
- End User representative
- IT Quality Function (for IT infrastructure aspects)
- System Administrator (operational role)

---

## 4. Compliance posture

### 4.1 Regulatory frameworks anchored

The active frameworks for this project (set via `.gxp-dev.yaml` `profile:` and `presets:`):

- **ISPE GAMP 5 Second Edition (2022)** — foundational
- **EU GMP Annex 11 (2025 consultation)** — when `presets.annex11_active: true`
- **21 CFR Part 11** — when `presets.part11_active: true`
- **EU GMP Annex 22 (AI/ML)** — when `presets.annex22_active: true`
- **ICH Q9 (R1)** — Quality Risk Management (always)
- **PIC/S PI 041-1** — Data Integrity (always when `profile: pharma`)
- Other (e.g. GDPR if `presets.gdpr_active: true`, IEC 62304 if `profile: medical-device`, etc.)

### 4.2 Criticality policy

`{{criticality_policy}}`

### 4.3 Signature policy

`{{signature_policy}}`

For systems claiming 21 CFR Part 11 compliance, electronic signatures must satisfy §11.100, §11.200, §11.300. For systems under EU GMP Annex 11, see §14.

### 4.4 ALCOA+ enforcement

`{{alcoa_plus_enforcement}}`

ALCOA+ principles (Attributable, Legible, Contemporaneous, Original, Accurate, plus Complete, Consistent, Enduring, Available) apply to every data lifecycle stage from generation to archival. See PIC/S PI 041-1 for guidance.

### 4.5 Supplier qualification policy

(Required if any vendor systems in scope.)

`{{supplier_qualification_policy}}`

Per GAMP 5 M2 + Chapter 7, supplier assessment is documented in `specs/SUP-ASSESS.md`.

---

## 5. Acceptance criteria for system release

`{{acceptance_criteria_for_release}}`

Standard expectations:

- All `templates_active` instances reach `status: approved`
- `specs/RTM.md` shows complete forward and backward traceability with zero orphan requirements
- IQ, OQ, and (if applicable) PQ pass with no critical deviations or with documented deviation reports + CAPA
- `specs/VR.md` (Validation Report) is approved by the Quality Unit
- Operational handover signed (per GAMP 5 O1)

---

## 6. Revision history

| Version | Date | Reason of revision | Author |
|---|---|---|---|
| 0.1 | `{{date}}` | Initial draft | `{{author_name}}`, `{{author_role}}` |
|  |  |  |  |

---

## Notes for implementers

> [!note] Validation Master Plan vs Validation Plan
> The **VMP** (this template) is the **program-level umbrella**. It declares which templates / systems / risks / roles apply to the project. A separate **VP (Validation Plan)** template exists for per-system planning detail. For simple projects, VMP + VP may be merged in a single document — declare the choice in `.gxp-dev.yaml` `templates_active`.

> [!note] Relationship to the consumer manifest `.gxp-dev.yaml`
> The VMP is the **human-readable narrative** of the validation strategy. The manifest is the **machine-readable contract**. They MUST be consistent: `templates_active` in VMP matches `.gxp-dev.yaml`; `roles_assigned` in VMP matches the personas defined by the active profile; `criticality_policy` is the prose form of what the manifest's `rigor_level` enforces programmatically.

> [!tip] When VMP may be omitted
> For low-rigor projects (`rigor_level: light`) or single-system simple Cat 3 commodity software, the VMP may be folded into a longer `VP`. The toolkit accepts this: just exclude `VMP` from `templates_active` and have `VP` carry the program-level fields. Document this choice explicitly in `VP.md`.

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. Guide for an AI agent that executes the skill `gdd.vmp.from-init` (planned for `v0.5.0`) or equivalent.

### Question order

1. **Project identity** (placeholders: `project_id`, `project_name`, `author_name`, `author_role`)
2. **Scope** (`scope`, `in_scope_systems`, `out_of_scope_systems`, `out_of_scope_rationale`) — interactive list-building if multiple systems
3. **Lifecycle decision** — read from `.gxp-dev.yaml` `lifecycle:`; confirm
4. **Active templates** — read from `.gxp-dev.yaml` `templates_active:`; confirm matches intended scope
5. **Roles assignment** (`roles_assigned`) — for each canonical GAMP §6.2.3 role + any profile-specific personas, ask for name + department
6. **Compliance policies** (`criticality_policy`, `signature_policy`, `alcoa_plus_enforcement`, `supplier_qualification_policy` if vendor systems)
7. **Validation strategy** (`validation_strategy`) — narrative paragraph
8. **Acceptance criteria** (`acceptance_criteria_for_release`)

### Stop criteria (instance considered "complete")

- [ ] All `placeholders.required: true` filled (no `{{...}}` remaining)
- [ ] `templates_active` matches `.gxp-dev.yaml`
- [ ] Approval matrix has ≥1 Process Owner + ≥1 System Owner + ≥1 Quality Unit designated
- [ ] Lifecycle choice (v-model / agile / hybrid) coherent with `.gxp-dev.yaml`
- [ ] If `profile: pharma`: `alcoa_plus_enforcement` filled
- [ ] If any vendor systems in scope: `supplier_qualification_policy` filled
- [ ] No `[NEEDS CLARIFICATION: …]` markers in required fields

### Status transitions

```
draft → in-review → approved → superseded
```

- `draft`: free editing
- `in-review`: editing requires reviewer comments
- `approved`: any change requires bumping version + marking previous as `superseded`
- `superseded`: read-only historical record

### Downstream mapping

The VMP does NOT have a `<CATEGORY>` axis — it is the master document. Its content propagates to **all** active templates as constraints / context. Specifically:

| VMP section | Used by |
|---|---|
| Scope (in/out) | URS, GXP-ASSESS, SUP-ASSESS, RA-INIT |
| Roles assigned | All templates — signature blocks |
| Criticality policy | RA-INIT, RA-DET, GXP-ASSESS |
| Signature policy | All approvable docs |
| ALCOA+ enforcement | URS-EREC, URS-ESIG, OPS, ARCH, P11M |
| Supplier qualification policy | SUP-ASSESS |
| Validation strategy | VP, RTM |
| Acceptance criteria | VR |
| Active templates | `.gxp-dev.yaml` cross-check; trace-validate skill |

A future skill `gdd.vmp.propagate` (Roadmap Cat C) could automatically inject VMP-derived defaults into downstream template instances at creation time.

---

## Related

- `templates/csv/URS.md` — pattern reference for Round 1 frontmatter (validated)
- `templates/csv/GXP-ASSESS.md` — Concept-phase template (depends on VMP scope decisions)
- `templates/csv/VP.md` — per-system validation plan (sibling to VMP at project level)
- `docs/methodology.md` — Why VMP plays the Constitution role
- `docs/project-layout.md` — `.gxp-dev.yaml` manifest spec
- `docs/requirement-id-scheme.md` — for downstream artifact ID conventions
