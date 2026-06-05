---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "GXP-ASSESS — GxP Assessment & System Registration (canonical CSV template)"
type: template
template_class: csv
template_id: "GXP-ASSESS"
template_version: "0.1.0"
v_model_phase: concept
gamp_categories_applicable: [1, 3, 4, 5]
language: en
# Round 2 (2026-05-29): translated to English canonical (was language: es). §-citations + IDs preserved verbatim.
status: canonical-draft
created: 2026-05-28
updated: 2026-05-29

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# GXP-ASSESS is the TRUE ROOT of the cascade. It runs in the Concept phase
# (GAMP 5 §3.1 p.24), BEFORE the project. It registers the system, determines
# whether it is GxP-relevant, and identifies applicable regulations. It feeds URS + RA-INIT.
inputs: []
outputs:
  - artifact: "GXP-ASSESS instance (Markdown) — system registration + GxP determination"
    consumed_by:
      - "URS"        # inherits system identity + GxP scope
      - "RA-INIT"    # inherits the initial GxP determination (it is Step 1 of QRM)
      - "VP"         # the Validation Plan is triggered only if the system is GxP-relevant
      - "SUP-ASSESS" # determines whether a supplier assessment is needed (Cat 4/5)
applicable_regulations:
  - "gamp-5"          # §3.1 p.24 (GxP assessment = Step 1 QRM) + §M4 (categorization) + §4 Concept phase
  - "21-cfr-part-11"  # identifies applicable electronic records/signatures
  - "eu-annex-11"     # §1 scope (every system touching GMP manufacturing)
based_on:
  - "GAMP 5 §3.1 p.24 (GxP assessment before project phase) + §5.3 Step 1 (initial risk assessment + system impact) + §M4 (categorization)"
  - "Structure: system registration + GxP determination + preliminary GAMP categorization + identification of applicable regulations"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
    description: "Human-readable name of the system (propagated to URS, RA-INIT, etc.)"
  system_id:
    type: string
    required: true
    description: "Unique identifier assigned in the register (organization's corporate scheme)"
  system_description:
    type: string
    required: true
    description: "General description of the system and its function"
  business_process:
    type: string
    required: true
    description: "Business process supported by the system"
  intended_use:
    type: string
    required: true
    description: "Regulatory intended use (1-3 sentences) — propagated to the URS"
  supplier:
    type: string
    required: false
    description: "Supplier of the base product (if COTS / configured / SaaS)"
  gxp_determination:
    type: enum
    required: true
    values: ["gxp-relevant", "non-gxp", "indirect-gxp"]
    description: "OUTPUT: is the system GxP-relevant? Decides whether it enters CSV scope."
  applicable_regulations_list:
    type: list
    required: true
    description: "Applicable regulations determined (GMP/GLP/GCP/GDP/GVP; Part 11; Annex 11; etc.)"
  gamp_category_preliminary:
    type: enum
    required: true
    values: [1, 3, 4, 5]
    description: "Preliminary GAMP category (confirmed/refined in RA-INIT)"
  records_signatures_relevant:
    type: boolean
    required: true
    description: "Does the system handle GxP electronic records / signatures? Decides URS-EREC/ESIG preset activation."
  validation_required:
    type: boolean
    required: true
    description: "OUTPUT: is CSV validation required? (triggers the Validation Plan)"
  assessor_name:
    type: string
    required: true
  assessor_dept:
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
    - based_on_template: "GXP-ASSESS"
    - based_on_template_version
    - system_id
    - gxp_determination
    - gamp_category_preliminary
    - validation_required
    - status               # draft | in-review | approved | superseded
    - version
    - created
    - updated
    - language
  conditional_fields:
    - approved_by: "required if status == approved"
    - supersedes
    - based_on_previous_assessment: "reference if based on a previous assessment of a similar system"

# ─── Validation rules (Round 1 subset) ──────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "gxp_determination must be justified (not just the enum value)"
  - "If gxp_determination == 'gxp-relevant' → validation_required should be true (justify if false)"
  - "gamp_category_preliminary must have a rationale (refined in RA-INIT)"
  - "records_signatures_relevant must be consistent with the future activation of URS-EREC/ESIG presets"
  - "GXP-ASSESS must be approved BEFORE the project begins (GAMP 5 §3.1: assessment before project phase)"
  - "If reusing a previous assessment → document based_on_previous_assessment + re-evaluation of differences"

tags:
  - template
  - csv
  - gxp-assessment
  - system-registration
  - concept-phase
  - gamp-m4
  - canonical
---

# GXP-ASSESS — GxP Assessment & System Registration

> [!note] Canonical CSV template — CASCADE ROOT
> **Canonical** template for the **GxP Assessment + system registration** — the **root document** of the entire CSV life cycle. It runs in the **Concept** phase (GAMP 5 §3.1 p.24), **before** the project begins. It determines whether system **`{{system_name}}`** is GxP-relevant, which regulations apply, and its preliminary GAMP category. Its output triggers (or does not trigger) the [Validation Plan](VP.md) and feeds the [URS](URS.md) and the [RA-INIT](RA-INIT.md).

> [!tip] Embedded usage rules
> 1. **Before the project** — the GxP assessment is performed in the Concept phase, before the project begins (GAMP 5 §3.1). Doing it late forces retrofitting of controls.
> 2. **It is Step 1 of QRM** — it coincides with Step 1 of the 5-step process (quality risk management process). The [RA-INIT](RA-INIT.md) inherits and deepens this determination.
> 3. **Decides scope** — if the system is NOT GxP-relevant, it falls outside CSV scope (the determination is documented and the assessment is closed). If it is GxP-relevant, it triggers the Validation Plan.
> 4. **Preliminary category** — the GAMP category here is preliminary; it is confirmed/refined in the RA-INIT.
> 5. **Propagated identity** — system_name, system_id, and intended_use are propagated to all downstream documents.
> 6. **Reuse permitted** — the assessment may be based on a previous assessment of a similar system, with a documented re-evaluation of differences.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **Description** | `{{system_description}}` |
| **Business process** | `{{business_process}}` |
| **Intended Use** | `{{intended_use}}` |
| **Supplier** | `{{supplier}}` |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Assessor / Author | `{{assessor_name}}` | `{{assessor_dept}}` |  |  |
| Reviewer (Process Owner) |  |  |  |  |
| Approver (Quality Unit) |  |  |  |  |

---

## 1. Objective

Determine whether system **`{{system_name}}`** is subject to GxP regulations, register it in the computerized system inventory, identify applicable regulations, and establish its preliminary GAMP category — all **before** starting the validation project. This assessment is **Step 1** of the QRM process (GAMP 5 §3.1 + §5.3) and the input that triggers (or does not trigger) the rest of the CSV life cycle.

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| GxP Assessment | Determination of whether a system is GxP-relevant + applicable regulations |
| GAMP category | Cat 1 (infrastructure) / 3 (standard) / 4 (configured) / 5 (custom) — GAMP 5 §M4 |
| Predicate rule | The underlying GxP regulation requiring registration (GMP, GLP, GCP, GDP, GVP) |
| System inventory | The organization's computerized system inventory |
| Concept phase | Pre-project phase (GAMP 5 §4) |

---

## 3. System registration

| Field | Value |
|---|---|
| Registration date | DD.MM.YYYY |
| Process Owner (Process Owner) | |
| System Owner (System Owner) | |
| Location / deployment (on-prem / cloud / SaaS) | |
| Life cycle status | Concept / Project / Operation / Retirement |

---

## 4. GxP Determination

### 4.1 Is it GxP-relevant?

**Determination**: `{{gxp_determination}}`

> Criterion: the system creates/modifies/stores/transmits records under a GxP predicate rule, or controls a process with impact on patient safety / product quality / data integrity.

| Question | Yes/No | Justification |
|---|---|---|
| Does the system support a GxP process (GMP/GLP/GCP/GDP/GVP)? |  |  |
| Does it create/store records required by a predicate rule? |  |  |
| Would its failure impact patient safety, product quality, or data integrity? |  |  |

### 4.2 Applicable regulations

**List**: `{{applicable_regulations_list}}`

| Regulation | Applicable? | Comment |
|---|---|---|
| GMP (cGMP / EU GMP) |  |  |
| GLP |  |  |
| GCP |  |  |
| GDP / GVP |  |  |
| 21 CFR Part 11 (Electronic Records/Signatures) |  |  |
| EU Annex 11 (Computerised Systems) |  |  |

### 4.3 Electronic records / signatures

**Does the system handle GxP electronic records/signatures?** `{{records_signatures_relevant}}`

> This result **anticipates** the activation decision for the `URS-EREC` / `URS-ESIG` presets in the URS (which the RA-INIT will confirm).

---

## 5. Preliminary GAMP categorization

**Preliminary category**: `{{gamp_category_preliminary}}`

> [!note] Preliminary — confirmed in RA-INIT
> This category is a first estimate for scoping the project. The [RA-INIT](RA-INIT.md) confirms or refines it with the full rationale.

| Category | Criterion (GAMP 5 §M4) | Applicable? |
|---|---|---|
| **Cat 1** | Infrastructure software (qualified, not validated) |  |
| **Cat 3** | Standard product, unconfigured |  |
| **Cat 4** | Configured product |  |
| **Cat 5** | Custom application |  |

---

## 6. Decision: is validation required?

**CSV validation required?** `{{validation_required}}`

> [!note] Cascade trigger
> If `true` → the project is initiated and the [Validation Plan](VP.md) is produced. If `false` → the determination is documented (system outside CSV scope) and the assessment is closed.

| Outcome | Action |
|---|---|
| GxP-relevant + validation required | → produce [VP](VP.md) + [RA-INIT](RA-INIT.md) + [URS](URS.md) |
| GxP-relevant + Cat 1 | → infrastructure qualification (no full validation) |
| Non-GxP | → outside CSV scope; document and close |

**Is a Supplier Assessment required?** (Cat 4/5 or external services) → [SUP-ASSESS](SUP-ASSESS.md)

---

## 7. Related documents

| Document | Reference |
|---|---|
| Validation Plan (if validation required) | [VP](VP.md) |
| Initial Risk Assessment | [RA-INIT](RA-INIT.md) |
| User Requirements Specification | [URS](URS.md) |
| Supplier Assessment (Cat 4/5) | [SUP-ASSESS](SUP-ASSESS.md) |
| Organization's CSV Policy | `{{org_csv_policy_ref}}` |
| `{{custom_ref}}` |  |

---

## 8. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{assessor_name}}`, `{{assessor_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] GXP-ASSESS is the true cascade root
> Although the URS is often considered the "first" document, the true entry point is the GxP Assessment: it decides whether a project exists, which regulations apply, and the system identity that everything else inherits.

> [!note] Coincides with RA-INIT Step 1
> The GxP assessment is Step 1 of the 5-step QRM process. In small organizations it may be integrated with the RA-INIT; in mature organizations it is a separate registration form that precedes everything else.

> [!tip] Natural output
> A well-executed GXP-ASSESS produces: (1) the go/no-go validation decision; (2) the system identity (name/id/intended_use) that is propagated downstream; (3) the preliminary category; (4) the list of regulations that will activate presets in the URS.

## Related

- [VP](VP.md) · [RA-INIT](RA-INIT.md) · [URS](URS.md) · [SUP-ASSESS](SUP-ASSESS.md)
- GAMP 5 · 21 CFR Part 11 · EU Annex 11
- gxp assessment · gamp categories · quality risk management process

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.init` / `gdd.gxp-assess` skill.

### Generation flow

1. **Collect system identity**: name, id, description, business process, intended use, supplier.
2. **GxP determination** (§4): guide through the 3 questions; capture justification.
3. **Applicable regulations** (§4.2): mark GMP/GLP/GCP/GDP/GVP + Part 11 + Annex 11.
4. **Electronic records/signatures** (§4.3): decides the advance activation of URS-EREC/ESIG presets.
5. **Preliminary GAMP category** (§5): first estimate with rationale.
6. **Validation decision** (§6): go/no-go; if go → flag production of VP/RA-INIT/URS.
7. **Anti-hallucination**: use `[NEEDS CLARIFICATION: ...]` when information is missing; never invent regulatory applicability without a basis.
8. **Output**: write `specs/GXP-ASSESS.md` (status: draft); propagate identity to URS/RA-INIT placeholders.
9. **Post-flight**: `validate-frontmatter.py` + `check-clarification-markers.py`.

### `status` transitions

```
draft ──[determination + category + decision complete]──> in-review
in-review ──[Process Owner + QU sign]──> approved
approved ──[new version]──> superseded
```

> [!warning] GXP-ASSESS approved before the project
> GAMP 5 §3.1: the assessment is completed before the project begins. It is a prerequisite for URS/RA-INIT/VP.

### Downstream mapping

| Origin (GXP-ASSESS) | Destination | Rule |
|---|---|---|
| system_name/id/intended_use | URS, RA-INIT, all | Propagated identity |
| gxp_determination + regulations | RA-INIT Step 1 | RA-INIT inherits and deepens |
| records_signatures_relevant | preset_part11_active in URS | Advances EREC/ESIG activation |
| gamp_category_preliminary | RA-INIT | Confirmed/refined |
| validation_required == true | VP | Triggers the Validation Plan |
| Cat 4/5 or external services | SUP-ASSESS | Triggers supplier assessment |
