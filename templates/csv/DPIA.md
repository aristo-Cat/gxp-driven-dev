---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "DPIA — Data Privacy Impact Assessment (canonical CSV template)"
type: template
template_class: csv
template_id: "DPIA"
template_version: "0.1.0"
v_model_phase: concept
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# DPIA is a cross-cutting, CONDITIONAL document. It runs only when the system
# processes personal data. When triggered it gates the gdpr_active URS preset
# and feeds privacy-derived requirements into the URS.
inputs:
  - artifact: "GXP-ASSESS instance (optional) — system identity"
    source: "GXP-ASSESS"
  - artifact: "URS draft (optional) — preliminary data-handling scope"
    source: "URS"
outputs:
  - artifact: "DPIA instance (Markdown) — privacy risk assessment + conclusion"
    consumed_by:
      - "URS"     # gates gdpr_active preset; privacy requirements injected as URS-SEC / URS-DATA / URS-ARCH rows
      - "audit"   # required evidence when processing personal data under GDPR Art.35
applicable_regulations:
  - "eu-annex-11"   # §4 (data integrity), §7 (data storage/retention), §12 (security)
  - "gamp-5"        # general data protection principles as quality attributes

# ─── Regulation anchor ───────────────────────────────────────────────────────
# Basis: GDPR Article 35 (Data Protection Impact Assessment — mandatory when
# processing "likely to result in a high risk to the rights and freedoms of
# natural persons"). This template covers both Art.35 mandatory DPIAs and
# voluntary lightweight assessments for lower-risk personal-data processing.

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
    description: "Human-readable name of the system (inherited from GXP-ASSESS if available)"
  system_id:
    type: string
    required: true
    description: "Unique identifier of the system (propagated to URS)"
  system_description:
    type: string
    required: true
    description: "Brief functional description of the system"
  dpia_required_mandatory:
    type: boolean
    required: true
    description: "Is the DPIA mandatory under GDPR Art.35 (high-risk processing)?"
  personal_data_processed:
    type: boolean
    required: true
    description: "Does the system process any personal data? (If false, DPIA is closed without further assessment.)"
  data_controller:
    type: string
    required: true
    description: "Name / role of the Data Controller (the entity that determines purposes + means of processing)"
  data_processor:
    type: string
    required: false
    description: "Name / role of the Data Processor (if different from the controller; e.g. SaaS vendor)"
  dpo_name:
    type: string
    required: false
    description: "Data Protection Officer name (if appointed; mandatory for GDPR Art.37 organisations)"
  author_name:
    type: string
    required: true
  author_dept:
    type: string
    required: true
  lawful_basis:
    type: enum
    required: true
    values:
      - "consent (Art.6(1)(a))"
      - "contract (Art.6(1)(b))"
      - "legal obligation (Art.6(1)(c))"
      - "vital interests (Art.6(1)(d))"
      - "public task (Art.6(1)(e))"
      - "legitimate interests (Art.6(1)(f))"
    description: "GDPR Art.6 lawful basis for processing personal data"
  special_categories_present:
    type: boolean
    required: true
    description: "Does the system process special-category data (GDPR Art.9 — health, biometric, ethnic origin, etc.)?"
  retention_period:
    type: string
    required: true
    description: "Retention period for personal data; must align with URS-ARCH requirements"
  conclusion:
    type: enum
    required: true
    values:
      - "proceed"
      - "proceed-with-mitigations"
      - "consult-supervisory-authority"
    description: "DPIA conclusion: can the project proceed, or must the supervisory authority be consulted first (GDPR Art.36)?"
  gdpr_active_preset_triggered:
    type: boolean
    required: true
    description: "OUTPUT: does this DPIA trigger the gdpr_active preset in the URS? (true when personal_data_processed == true)"
  org_privacy_policy_ref:
    type: string
    required: false
    description: "Reference to the organisation's privacy policy / data protection policy"
  custom_ref:
    type: string
    required: false

# ─── Instance frontmatter spec ───────────────────────────────────────────────
instance_frontmatter_spec:
  required_fields:
    - title
    - type: "instance"
    - based_on_template: "DPIA"
    - based_on_template_version
    - system_id
    - status               # draft | in-review | approved | superseded
    - version
    - created
    - updated
    - language
  conditional_fields:
    - approved_by: "required if status == approved"
    - supersedes: "if this replaces a previous DPIA for the same system"

# ─── Validation rules ────────────────────────────────────────────────────────
validation_rules:
  - "personal_data_processed must be explicitly stated; if false, the assessment is closed at §2 with documented justification"
  - "If personal_data_processed == true → personal data inventory (§3) must be complete with at least one row"
  - "lawful_basis must be stated and justified; 'legitimate interests' requires a Legitimate Interests Assessment note"
  - "special_categories_present: if true → Art.9 lawful basis must also be stated (§3)"
  - "Risk-to-data-subjects table (§5) must contain at least one assessed risk row (DPIA-NNN identifier)"
  - "Every risk rated High or Medium must have at least one mitigation; residual risk must be re-rated"
  - "conclusion must be stated explicitly (§7); if 'consult-supervisory-authority' → GDPR Art.36 consultation record reference required"
  - "gdpr_active_preset_triggered == true whenever personal_data_processed == true"
  - "Data flows and third-country transfers (§4) must be documented; transfers outside EEA require a legal transfer mechanism citation"
  - "Retention period must be consistent with URS-ARCH requirements when URS is drafted"

tags:
  - template
  - csv
  - dpia
  - gdpr
  - privacy
  - data-protection
  - concept-phase
  - cross-cutting
  - canonical
---

# DPIA — Data Privacy Impact Assessment

> [!note] Canonical CSV template — Cross-cutting / Conditional
> **Canonical** template for the **Data Privacy Impact Assessment** — a cross-cutting document that runs **conditionally** when system **`{{system_name}}`** processes personal data. Its basis is **GDPR Article 35** (mandatory DPIA for high-risk processing) supplemented by general data-protection principles aligned with EU Annex 11 §12 (security) and GAMP 5 quality attributes. Its output gates the `gdpr_active` preset in the [URS](URS.md) and feeds privacy-derived requirements directly into the URS requirement table.

> [!tip] Embedded usage rules
> 1. **Conditional trigger** — run this template only when the system processes personal data. If it does not, document that determination at §2 and close the assessment.
> 2. **GDPR Art.35 mandatory vs. voluntary** — Art.35 makes a full DPIA mandatory for processing "likely to result in a high risk" (large-scale health data, systematic profiling, etc.). For lower-risk personal-data processing a voluntary lightweight DPIA is still best practice and is fully supported by this template.
> 3. **Run at Concept phase** — the DPIA should be initiated alongside or immediately after the [GXP-ASSESS](GXP-ASSESS.md) so that privacy requirements reach the [URS](URS.md) before the specification is frozen.
> 4. **DPO consultation** — if a Data Protection Officer is appointed, they must be consulted during the assessment (GDPR Art.35(2)).
> 5. **Conclusion gates progression** — if the conclusion is `consult-supervisory-authority`, the project may not start processing until the supervisory authority has responded (GDPR Art.36).
> 6. **Feeds URS** — privacy risks that require system-level controls become formal URS requirements (categories: SEC, DATA, ARCH, PROC). The `gdpr_active` URS preset activates the standard privacy requirement block.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **Description** | `{{system_description}}` |
| **Data Controller** | `{{data_controller}}` |
| **Data Processor** (if different) | `{{data_processor}}` |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Author | `{{author_name}}` | `{{author_dept}}` |  |  |
| Data Protection Officer (DPO) | `{{dpo_name}}` |  |  |  |
| Reviewer (Process Owner) |  |  |  |  |
| Approver (Quality Unit) |  |  |  |  |

---

## 1. Objective

Assess the privacy impact of system **`{{system_name}}`** on the rights and freedoms of the data subjects whose personal data it processes, in accordance with **GDPR Article 35**. Identify the categories of personal data processed, the lawful basis for processing, the associated risks to data subjects, and the controls required to bring residual risk to an acceptable level. The conclusion either clears the system to proceed, requires implementation of defined mitigations before proceeding, or triggers mandatory supervisory-authority consultation under **GDPR Article 36**.

---

## 2. Necessity and applicability

### 2.1 Does the system process personal data?

**Determination**: `{{personal_data_processed}}`

> Personal data means any information relating to an identified or identifiable natural person (GDPR Art.4(1)). This includes names, identifiers, location data, online identifiers, or factors specific to physical, physiological, genetic, mental, economic, cultural, or social identity.

| Question | Yes / No | Justification |
|---|---|---|
| Does the system collect, store, or transmit data about natural persons? |  |  |
| Can individuals be identified directly or indirectly from the data held? |  |  |
| Is personal data processed on behalf of the organization as controller? |  |  |

> [!warning] If personal_data_processed == false
> Document the rationale here and close the assessment. The `gdpr_active` preset in the URS is NOT activated. File this completed section as evidence that the determination was made deliberately.

### 2.2 Is a full DPIA mandatory under GDPR Art.35?

**Mandatory DPIA**: `{{dpia_required_mandatory}}`

| High-risk indicator (GDPR Art.35 + WP29/EDPB guidelines) | Present? | Notes |
|---|---|---|
| Large-scale processing of special-category data (Art.9) |  |  |
| Systematic and large-scale profiling of individuals |  |  |
| Systematic monitoring of a publicly accessible area |  |  |
| Processing that may result in denial of service to individuals |  |  |
| Processing of data concerning vulnerable subjects (patients, children) |  |  |
| Innovative use of new technologies with privacy implications |  |  |
| Processing of biometric data for unique identification |  |  |

> [!note] Voluntary DPIA
> Even if no mandatory indicator is present, completing this assessment is recommended best practice when any personal data is processed in a regulated-sector system.

> [!note] AI / automated-decision bridge → AISC
> If "systematic and large-scale profiling" or any **automated decision-making** (see §6, GDPR Art.22) is performed by an **AI/ML component**, the privacy risk assessment must be paired with an AI System Compliance assessment — see AISC (EU Annex 22, AI/ML). The DPIA covers the privacy dimension; the AISC covers AI-specific model-lifecycle, explainability and bias controls. Cross-reference both by risk ID.

---

## 3. Personal data inventory

### 3.1 Data categories and data subjects

> Complete one row per distinct data category. Add rows as needed.

| Ref | Data category | Examples | Data subjects | Volume / scale | Special category? (Art.9) | Source |
|---|---|---|---|---|---|---|
| D1 | `[e.g. user account data]` | `[name, email, department]` | `[system users / employees]` | `[e.g. < 500 per site]` | No |  |
| D2 | `[e.g. audit-trail records]` | `[user-ID, action, timestamp]` | `[system users]` | `[retained N years]` | No |  |
| D3 | `[add row as needed]` |  |  |  |  |  |

> [!note] Data-inventory rows use plain local labels
> The `D1`, `D2`, … labels are **local references within this DPIA**, not toolkit IDs. The `DPIA-NNN` ID counter belongs solely to the privacy risk register (§5), the DPIA's primary entity (see [requirement-id-scheme](../../docs/requirement-id-scheme.md)).

### 3.2 Special-category data (GDPR Art.9)

**Special categories present**: `{{special_categories_present}}`

> [!warning] If special_categories_present == true
> State the Art.9 lawful basis for processing (e.g. Art.9(2)(b) — employment obligations; Art.9(2)(h) — medical purposes). Document it below.

| Art.9 category | Present? | Art.9(2) basis if present |
|---|---|---|
| Health data |  |  |
| Biometric data (for unique identification) |  |  |
| Genetic data |  |  |
| Racial or ethnic origin |  |  |
| Political opinions |  |  |
| Religious or philosophical beliefs |  |  |
| Trade union membership |  |  |
| Sex life or sexual orientation |  |  |

---

## 4. Processing purposes, lawful basis, and data flows

### 4.1 Processing purposes and lawful basis

| Processing purpose | Lawful basis (GDPR Art.6) | Justification |
|---|---|---|
| `[e.g. user authentication and access logging]` | `{{lawful_basis}}` | `[brief justification]` |
| `[add row as needed]` |  |  |

> [!note] Legitimate Interests
> If lawful basis is "legitimate interests (Art.6(1)(f))", a Legitimate Interests Assessment (LIA) is required. Reference the LIA document here.

### 4.2 Data flows and recipients

| Data flow | Origin | Destination | Personal data transferred | Transfer mechanism |
|---|---|---|---|---|
| `[e.g. user data → backup system]` |  |  |  | `[internal / EEA / SCCs / adequacy decision]` |
| `[e.g. audit logs → log management platform]` |  |  |  |  |

> [!warning] Third-country transfers
> Any transfer of personal data outside the EEA requires a valid legal transfer mechanism: adequacy decision (GDPR Art.45), Standard Contractual Clauses (Art.46(2)(c)), or Binding Corporate Rules (Art.47). Document the mechanism in the "Transfer mechanism" column above.

### 4.3 Retention and deletion

| Data category | Retention period | Deletion / anonymisation mechanism | URS-ARCH requirement |
|---|---|---|---|
| All personal data (default) | `{{retention_period}}` |  | `[URS-ARCH-NNN when drafted]` |
| `[category with different period]` |  |  |  |

---

## 5. Privacy risk assessment (risks to data subjects)

> Rate each risk to data subjects (not to the organization). Severity and likelihood are assessed from the data subject's perspective. Residual risk is rated after mitigations are implemented.

| Risk ID | Risk to data subjects | Likelihood (H/M/L) | Severity (H/M/L) | Overall (H/M/L) | Mitigation | Residual (H/M/L) | URS req. |
|---|---|---|---|---|---|---|---|
| DPIA-001 | `[e.g. Unauthorised access to personal data — identity theft / harm]` | `M` | `H` | `H` | `[e.g. Role-based access control; encryption at rest and in transit]` | `L` | `[URS-SEC-NNN]` |
| DPIA-002 | `[e.g. Excessive retention — data held beyond purpose]` | `M` | `M` | `M` | `[e.g. Automated deletion after retention period; periodic data-minimisation review]` | `L` | `[URS-ARCH-NNN]` |
| DPIA-003 | `[e.g. Inadequate audit trail — inability to detect/prove misuse]` | `L` | `M` | `M` | `[e.g. Immutable audit trail; periodic review of access logs]` | `L` | `[URS-DATA-NNN]` |
| DPIA-004 | `[add row as needed]` |  |  |  |  |  |  |

> [!note] Risk rating scale
> **H** (High) — likely to cause significant harm to data subjects (financial loss, discrimination, reputational damage, physical harm). **M** (Medium) — possible harm with moderate probability; mitigations reduce impact. **L** (Low) — minimal or unlikely impact; standard controls sufficient. All H and M risks require at least one documented mitigation and a re-rated residual risk.

---

## 6. Data-subject rights handling

> Document how the system supports the rights granted to data subjects by GDPR Chapter III.

| Right | Applicable? | How the system supports it | Responsible role |
|---|---|---|---|
| Right of access (Art.15) |  | `[e.g. DPO / admin can export user records on request]` | |
| Right to rectification (Art.16) |  | `[e.g. User profile editable by admin]` | |
| Right to erasure / "right to be forgotten" (Art.17) |  | `[e.g. Delete-account function removes personal data; audit trail pseudonymised]` | |
| Right to restriction of processing (Art.18) |  |  | |
| Right to data portability (Art.20) |  | `[e.g. Export in machine-readable format — CSV / JSON]` | |
| Right to object (Art.21) |  |  | |
| Rights related to automated decision-making (Art.22) |  |  | |

> [!note] Automated decision-making by AI/ML → AISC
> If automated decision-making (Art.22) is implemented by an AI/ML component, pair this DPIA with an AISC (EU Annex 22) to assess AI-specific controls (explainability, human oversight, bias). The Art.22 right above is the privacy hook; the AISC carries the AI-lifecycle assessment.

---

## 7. Conclusion

**Conclusion**: `{{conclusion}}`

**gdpr_active URS preset triggered**: `{{gdpr_active_preset_triggered}}`

| Conclusion | Meaning | Next action |
|---|---|---|
| **proceed** | All risks are low or have been reduced to low by design; no outstanding H/M residual risks | Continue to URS; activate `gdpr_active` preset |
| **proceed-with-mitigations** | Medium residual risks remain; identified mitigations must be implemented as URS requirements before go-live | Inject mitigations as URS-SEC / URS-DATA / URS-ARCH requirements; confirm at IQ/OQ/PQ |
| **consult-supervisory-authority** | High residual risks remain that cannot be mitigated by technical/organisational measures alone; GDPR Art.36 applies | Do NOT start processing until supervisory authority responds (max. 8 weeks); document consultation reference below |

**Supervisory authority consultation reference** *(if applicable)*: `[NEEDS CLARIFICATION: reference to Art.36 consultation file]`

**Summary of required URS requirements generated by this DPIA**:

| URS requirement ID (placeholder) | Category | Description | Driven by risk |
|---|---|---|---|
| `[URS-SEC-NNN]` | SEC | `[e.g. Role-based access control with least-privilege principle]` | DPIA-001 |
| `[URS-ARCH-NNN]` | ARCH | `[e.g. Automated personal data deletion after retention period]` | DPIA-002 |
| `[URS-DATA-NNN]` | DATA | `[e.g. Immutable audit trail covering all personal data access events]` | DPIA-003 |

> [!note] Requirement IDs
> Assign final URS IDs (`URS-SEC-NNN`, `URS-ARCH-NNN`, etc.) when the URS is drafted. Use the placeholder column to track origin.

---

## 8. Related documents

| Document | Reference |
|---|---|
| GxP Assessment | [GXP-ASSESS](GXP-ASSESS.md) |
| User Requirements Specification | [URS](URS.md) |
| Initial Risk Assessment | [RA-INIT](RA-INIT.md) |
| Detailed Risk Assessment | [RA-DET](RA-DET.md) |
| Security Testing Records | [SEC-TEST](SEC-TEST.md) |
| Organisation's privacy / data-protection policy | `{{org_privacy_policy_ref}}` |
| `{{custom_ref}}` |  |

---

## 9. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{author_name}}`, `{{author_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] GDPR Art.35 is the statutory basis
> This template implements the GDPR Article 35 Data Protection Impact Assessment. For systems in EEA jurisdictions (or processing EEA subjects' data) this is the operative legal requirement. For non-EEA jurisdictions with equivalent legislation (e.g. UK GDPR, Swiss nDSG, Brazil LGPD) the structure is applicable with minor lawful-basis terminology adjustments.

> [!note] EU Annex 11 alignment
> EU Annex 11 §12 requires that computerised systems have controls for security, including access management and audit trails. The privacy risks assessed here (especially DPIA-001 and DPIA-003) directly map to Annex 11 security controls, creating a natural bridge between GxP and GDPR controls.

> [!tip] DPIA vs. RA-INIT — distinct scopes
> The [RA-INIT](RA-INIT.md) assesses **product / process risk** (patient safety, product quality, data integrity). The DPIA assesses **risk to natural persons** (data subjects). Both can identify the same system weakness (e.g. weak access control) but from different angles and with different escalation paths. Keep them as separate documents; cross-reference by risk ID where controls overlap.

> [!tip] Pseudonymisation and anonymisation
> GDPR does not apply to truly anonymous data. If the system can pseudonymise personal data (replace direct identifiers with a key, stored separately), the risk profile decreases substantially. Document pseudonymisation decisions in the personal data inventory (§3) and the risk table (§5).

> [!warning] DPO consultation is mandatory when a DPO is appointed
> GDPR Art.35(2): "the controller shall seek the advice of the data protection officer, where designated, when carrying out a data protection impact assessment." Failure to consult the DPO invalidates the DPIA for regulatory purposes.

## Related

- [GXP-ASSESS](GXP-ASSESS.md) · [URS](URS.md) · [RA-INIT](RA-INIT.md) · [SEC-TEST](SEC-TEST.md) · [RA-DET](RA-DET.md) · AISC
- EU Annex 11 · GAMP 5
- data integrity · audit trail · access control
- data protection officer · process owner · quality unit

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.dpia` skill.

### Generation flow

1. **Inherit system identity**: pull `system_name`, `system_id`, `system_description` from GXP-ASSESS instance (if available); otherwise collect from user.
2. **Applicability gate** (§2.1): ask whether the system processes personal data. If `personal_data_processed == false` → document determination, set `gdpr_active_preset_triggered: false`, close assessment. No further sections needed.
3. **Mandatory DPIA check** (§2.2): walk through the high-risk indicators table. Set `dpia_required_mandatory` accordingly.
4. **Consult DPO**: if DPO is appointed, flag that their consultation is required before finalising §5–§7.
5. **Personal data inventory** (§3): collect data categories, data subjects, volume, and special-category flag. Label rows with plain local references `D1`, `D2`, … (NOT toolkit IDs — the `DPIA-NNN` counter is reserved for the §5 risk register).
6. **Lawful basis** (§4.1): elicit the Art.6 basis for each processing purpose; if "legitimate interests", flag the need for a Legitimate Interests Assessment.
7. **Data flows** (§4.2): map origins, destinations, recipients, and transfer mechanisms. Flag any third-country transfers.
8. **Retention** (§4.3): capture retention period; note it will anchor URS-ARCH requirements.
9. **Risk assessment** (§5): for each identified risk assign a `DPIA-NNN` ID starting at `DPIA-001` (risks are the DPIA's primary entity), rate likelihood + severity from the data subject's perspective, propose mitigations, re-rate residual risk. Flag any H residual risks for escalation.
10. **Data-subject rights** (§6): confirm system-level support for each applicable right.
11. **Conclusion** (§7): derive `conclusion` from the residual risk table; set `gdpr_active_preset_triggered: true`; generate the list of URS requirement placeholders driven by this DPIA.
12. **Anti-hallucination**: use `[NEEDS CLARIFICATION: ...]` when regulatory applicability cannot be determined without human input; never fabricate lawful-basis justifications.
13. **Output**: write `specs/DPIA.md` (status: draft); propagate `gdpr_active_preset_triggered` and the URS requirement placeholders to the URS skill.
14. **Post-flight**: `validate-frontmatter.py` + `check-clarification-markers.py`.

### `status` transitions

```
draft ──[personal data inventory + lawful basis + risk assessment complete]──> in-review
in-review ──[DPO + Process Owner + QU sign]──> approved
approved ──[system change or new processing purpose]──> superseded
```

> [!warning] Conclusion before proceeding
> The DPIA must reach `approved` status before the system is authorised to process personal data in production. If conclusion is `consult-supervisory-authority`, `approved` status cannot be reached until the supervisory authority responds.

### Downstream mapping

| Origin (DPIA) | Destination | Rule |
|---|---|---|
| `gdpr_active_preset_triggered: true` | URS `gdpr_active` preset | Activates standard privacy requirement block in URS |
| DPIA-NNN mitigations | URS-SEC / URS-DATA / URS-ARCH rows | Privacy-derived requirements injected into URS requirement table |
| retention_period | URS-ARCH-NNN | Anchors retention requirement in URS |
| special_categories_present: true | RA-INIT | Flags elevated data-sensitivity in initial risk assessment |
| conclusion == consult-supervisory-authority | project gating | Project is blocked until Art.36 consultation is resolved |
