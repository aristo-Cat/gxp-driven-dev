---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "CS — Configuration Specification (canonical CSV template)"
type: template
template_class: csv
template_id: "CS"
template_version: "0.1.0"
v_model_phase: configuration-specification
gamp_categories_applicable: [4]
language: en
status: canonical-draft
created: 2026-05-28
updated: 2026-05-29
# Round 2 (2026-05-29): translated to English canonical (was language: es). §-citations + IDs preserved verbatim.

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# CS describes the settings/parameters configured for a Cat 4 product
# (GAMP 5 §D3.3.1.1). It hangs from the FS (implements the configuration the FS defines)
# and is verified in IQ (installation/config baseline) + OQ (config works).
inputs:
  - template_id: "FS"
    required: true
    description: "Functional Specification — defines what is configured; the CS documents HOW it ends up configured (settings/parameters)"
  - template_id: "RA-INIT"
    required: false
    description: "Risk Assessment — scales the detail of critical configuration"
outputs:
  - artifact: "CS instance (Markdown) — configuration settings record"
    consumed_by:
      - "IQ"        # IQ verifies the config baseline against the CS
      - "OQ"        # OQ verifies that the configuration works
      - "RTM"       # traceability CS↔FS↔test
applicable_regulations:
  - "gamp-5"          # §D3.3.1.1 p.199 (Configuration Specification) + §6.2.7
  - "eu-annex-11"     # §4.4 Specifications
based_on:
  - "GAMP 5 §D3.3.1.1 p.199 (Configuration Specification — settings, parameters, workflows, business rules, security config, integration mappings, dependencies)"
  - "Structure: Cat 4 configuration record; may live in a tool with audit trail; traceable to FS"

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
    description: "Approved FS whose configuration this CS documents"
  product_version:
    type: string
    required: true
    description: "Version of the configured base product"
  config_management_tool:
    type: string
    required: false
    description: "Config management tool with audit trail (if the CS lives in a tool rather than a document)"
  cs_author_name:
    type: string
    required: true
  cs_author_dept:
    type: string
    required: true
  custom_ref:
    type: string
    required: false

# ─── Instance frontmatter spec ───────────────────────────────────────────────
instance_frontmatter_spec:
  required_fields:
    - title
    - type: "instance"
    - based_on_template: "CS"
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
    - lives_in_tool: "true if the config lives in a config-management tool with audit trail"

# ─── Validation rules (Round 1 subset) ──────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "traces_to must point to an approved FS"
  - "Each CS-<CATEGORY>-NNN must cite the FS-ID it configures"
  - "Custom code / macros within the Cat 4 platform must be flagged as Cat 5 (goes to DS, not CS)"
  - "If the config lives in a tool with audit trail → maintain a summary record + approval under change control"
  - "The CS must be kept in sync with the live configuration (avoid config drift)"

tags:
  - template
  - csv
  - configuration-specification
  - cs
  - gamp-d3
  - cat4
  - canonical
---

# CS — Configuration Specification

> [!note] Canonical CSV template — Cat 4
> **Canonical** template for the **Configuration Specification (CS)** — documents the **settings and parameters configured** for a configurable product (Cat 4): workflows, business rules, security config, integration mappings, dependencies (GAMP 5 §D3.3.1.1 p.199). It hangs from the [FS](FS.md) (implements the configuration the FS defines) and is verified in [IQ](IQ.md)/[OQ](OQ.md).

> [!tip] Embedded usage rules
> 1. **Cat 4 only** — the CS is the load-bearing spec for configured products. Cat 3 does not need it; Cat 5 uses [DS](DS.md).
> 2. **HOW it ends up configured** — the FS defines what is configured; the CS documents the concrete settings/parameter values.
> 3. **Custom code = Cat 5** — custom macros/scripts within a Cat 4 platform are flagged as Cat 5 and go to the DS, not the CS.
> 4. **May live in a tool** — GAMP 5 §D3 allows the CS to consist of records in a config-management tool with audit trail (rather than a document). In that case, maintain a summary + approval under change control.
> 5. **Anti-drift** — the CS must be kept in sync with the live configuration; a static CS while the configuration evolves is a configuration management gap.
> 6. **Traceability** — each `CS-<CATEGORY>-NNN` cites the FS-ID it configures.

---

## 0. Identification and signatures

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **FS being configured** | `{{fs_ref}}` ([FS](FS.md)) |
| **Product version** | `{{product_version}}` |
| **Config management tool** | `{{config_management_tool}}` |

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Author | `{{cs_author_name}}` | `{{cs_author_dept}}` |  |  |
| Reviewer (SME) |  |  |  |  |
| Approver (System Owner) |  |  |  |  |
| Approver (Quality Unit) |  |  |  |  |

---

## 1. Objective

Document the configuration of product **`{{system_name}}`** (version `{{product_version}}`): the settings, parameters, workflows, business rules, security configuration, and integration mappings that implement the requirements of the [FS](FS.md) (`{{fs_ref}}`).

---

## 2. Definitions

| Term | Definition |
|---|---|
| CS | Configuration Specification — configured settings/parameters (Cat 4) |
| Config baseline | Approved and verified configuration state |
| Config drift | Divergence between the documented CS and the live configuration |
| Config item | Configuration element under control |

---

## 3. Configuration by area — `CS-<CATEGORY>-NNN`

> Each configuration item cites the FS-ID it implements. Use the 22 canonical acronyms according to the area.

### 3.1 Workflows and business rules — `CS-PROC-NNN` / `CS-FUNC-NNN`

| CS-ID | Configures (FS-ID) | Setting / Parameter | Configured value | Justification |
|---|---|---|---|---|
| `CS-FUNC-001` | `FS-FUNC-001` |  |  |  |
|  |  |  |  |  |

### 3.2 Security and roles — `CS-SEC-NNN`

| CS-ID | Configures (FS-ID) | Security setting | Configured value | Justification |
|---|---|---|---|---|
| `CS-SEC-001` | `FS-SEC-001` | *e.g.: role-permission mapping* |  |  |
|  |  |  |  |  |

### 3.3 Integrations / interfaces — `CS-API-NNN`

| CS-ID | Configures (FS-ID) | Integration mapping | Configured value | Justification |
|---|---|---|---|---|
| `CS-API-001` | `FS-API-001` |  |  |  |
|  |  |  |  |  |

### 3.4 Audit trail / records — `CS-EREC-NNN`

| CS-ID | Configures (FS-ID) | Audit trail / records setting | Configured value | Justification |
|---|---|---|---|---|
| `CS-EREC-001` | `FS-EREC-005` | *e.g.: audit trail enabled for table X* |  |  |
|  |  |  |  |  |

### 3.5 Other parameters (DATA, FLOW, REPORT, OPS…)

| CS-ID | Configures (FS-ID) | Parameter | Value | Justification |
|---|---|---|---|---|
| `CS-DATA-001` |  |  |  |  |
|  |  |  |  |  |

---

## 4. Configuration dependencies

| Config item | Depends on | Comment |
|---|---|---|
|  |  |  |

---

## 5. Custom code within the platform (Cat 5 flag)

> [!warning] Custom code = Cat 5 → goes to DS
> Any macro, script, or custom code within the Cat 4 platform is documented in the [DS](DS.md) (Cat 5), not here. List here only as a cross-reference.

| Custom element | Reference in DS |
|---|---|
|  |  |

---

## 6. Related documents

| Document | Reference |
|---|---|
| FS being configured | `{{fs_ref}}` ([FS](FS.md)) |
| Installation Qualification | [IQ](IQ.md) |
| Operational Qualification | [OQ](OQ.md) |
| Design Spec (custom code) | [DS](DS.md) |
| `{{custom_ref}}` |  |

---

## 7. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{cs_author_name}}`, `{{cs_author_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] CS is for Cat 4
> Configured product → CS. Custom → DS. Standard → neither. Do not request a CS for a Cat 3, nor a DS for a Cat 4 without custom code.

> [!tip] Config in tool vs document
> GAMP 5 §D3 + §M9: the configuration may live in a tool with audit trail. In that case the "CS" is a summary record and the tool is the source of truth. Avoids double maintenance.

## Related

- [FS](FS.md) · [DS](DS.md) · [IQ](IQ.md) · [OQ](OQ.md) · [RTM](RTM.md)
- GAMP 5 · EU Annex 11
- configuration specification · configuration management · gamp category 4 configured product

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.cs.from-fs` skill.

### Pre-flight
1. Read `.gxp-dev.yaml` + confirm `gamp_category == 4`. If Cat 5 → use DS. If Cat 3 → not applicable.
2. Locate the approved FS (`specs/FS.md`).
3. Read `templates/csv/CS.md` from the toolkit.

### Flow
1. Parse the FS-IDs that require configuration.
2. For each one, document settings/parameters with value + justification, citing the FS-ID.
3. Flag custom code as Cat 5 → DS.
4. Anti-hallucination: `[NEEDS CLARIFICATION: ...]`; never invent configuration values.
5. Output: `specs/CS.md` (status: draft).
6. Post-flight: `validate-frontmatter.py` + `check-clarification-markers.py`.

### Mapping
| Origin (CS) | Destination | Rule |
|---|---|---|
| `CS-<CATEGORY>-NNN` | IQ config baseline | IQ verifies the configured values |
| `CS-<CATEGORY>-NNN` | OQ | OQ verifies that the configuration works |
| Config items | RTM | Traceability CS↔FS↔test |
