---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "SUP-ASSESS — Supplier Assessment (canonical CSV template)"
type: template
template_class: csv
template_id: "SUP-ASSESS"
template_version: "0.1.0"
v_model_phase: planning
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-28
updated: 2026-05-29
# Round 2 (2026-05-29): translated to English canonical (was language: es). §-citations + IDs preserved verbatim.

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# SUP-ASSESS implements GAMP 5 §M2 (Supplier Assessment). Must be completed
# BEFORE finalizing the contract with the supplier. Enables leverage of
# supplier evidence (testing, config, controls) in the validation.
inputs:
  - template_id: "GXP-ASSESS"
    required: true
    description: "GxP Assessment — identifies whether an external supplier (Cat 4/5 or services) requires assessment"
  - template_id: "RA-INIT"
    required: false
    description: "Initial Risk Assessment — risk + category determine the assessment route (basic/postal/on-site)"
outputs:
  - artifact: "SUP-ASSESS instance (Markdown) — supplier assessment report"
    consumed_by:
      - "VP"         # the VP references the result to decide what supplier leverage is permitted
      - "IQ"         # supplier evidence may be leveraged in installation verification
      - "OQ"         # supplier testing may count as coverage (with assessment OK)
      - "VR"         # the Validation Report summarizes the supplier assessment (GAMP M7)
applicable_regulations:
  - "gamp-5"          # §M2 pp.93-106 (Supplier Assessment) + §6.2.5.3 + §8.3 (leverage)
  - "eu-annex-11"     # §7 Supplier and Service Management (2025) — reliance never transfers responsibility
  - "iso-27001"       # leverage for cloud security
based_on:
  - "GAMP 5 §M2 (Supplier Assessment) — 3 routes (basic / postal / on-site or virtual); complete before contract; ISO 9001/27001/SOC2 leverage"
  - "EU Annex 11 2025 §7 (reliance never transfers responsibility; exit strategy; pre-release version test)"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
  supplier_name:
    type: string
    required: true
    description: "Supplier being assessed (may be anonymized in the instance if confidential)"
  product_service:
    type: string
    required: true
    description: "Product or service supplied by the supplier"
  gamp_category:
    type: enum
    required: true
    values: [3, 4, 5]
  assessment_route:
    type: enum
    required: true
    values: ["basic", "postal-email-audit", "on-site-or-virtual-audit"]
    description: "Assessment route (GAMP M2 §10.3) — chosen by risk/category/novelty/leverage intent"
  is_cloud_saas:
    type: boolean
    required: true
    description: "Is the supplier cloud/SaaS? Activates exit strategy + pre-release test requirements (Annex 11 §7.5)"
  leverage_intent:
    type: string
    required: true
    description: "What is intended to be leveraged from the supplier (testing, config evidence, operational controls)"
  certifications_leveraged:
    type: list
    required: false
    description: "Leveraged certifications (ISO 9001, ISO 27001/27017, SOC 2, ISO 20000-1, HITRUST)"
  assessment_decision:
    type: enum
    required: true
    values: ["use-unconditionally", "use-for-certain-products", "use-subject-to-capas", "use-with-additional-oversight", "prohibit-use"]
    description: "Resulting decision from the assessment"
  reassessment_schedule:
    type: string
    required: true
    description: "Schedule for periodic re-evaluation of the supplier"
  assessor_name:
    type: string
    required: true
  assessor_dept:
    type: string
    required: true
  org_vendor_policy_ref:
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
    - based_on_template: "SUP-ASSESS"
    - based_on_template_version
    - system_id
    - assessment_route
    - assessment_decision
    - status               # draft | in-progress | completed | approved | superseded
    - version
    - created
    - updated
    - language
  conditional_fields:
    - approved_by: "required if status == approved"
    - capas_ref: "reference to agreed CAPAs if assessment_decision == use-subject-to-capas"
    - audit_report_ref: "reference to the audit report (quality record) if on-site/postal"
    - supersedes

# ─── Validation rules (Round 1 subset) ──────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "assessment_route must be justified from risk + category + novelty + leverage intent"
  - "The assessment must be completed BEFORE finalizing the contract (GAMP 5 §M2 §10.4)"
  - "If assessment_decision == 'use-subject-to-capas' → CAPAs + evidence of completion must be documented (supplier letter alone is insufficient)"
  - "If is_cloud_saas == true → the contract must cover exit strategy + pre-release version test (Annex 11 §7.5 viii-ix)"
  - "The audit report is retained as a quality record (system documentation)"
  - "If no assessment is performed for a GxP supplier → document justification (GAMP 5 §M2 §10.1)"
  - "reliance on the supplier does NOT transfer regulatory responsibility (Annex 11 §7.1)"

tags:
  - template
  - csv
  - supplier-assessment
  - sup-assess
  - gamp-m2
  - planning
  - canonical
---

# SUP-ASSESS — Supplier Assessment

> [!note] Canonical CSV template
> **Canonical** template for the **Supplier Assessment** — the formal evaluation of the supplier (QMS, technical capability, good practices) before contracting them for a GxP system or service. Implements GAMP 5 §M2 (pp.93-106) and EU Annex 11 §7. Enables **leverage** of supplier evidence (testing, config, controls) in the validation.

> [!warning] Reliance does not transfer responsibility (Annex 11 §7.1)
> Relying on the qualification of the supplier, a service provider, or internal IT **does not change** the requirements: the regulated organization remains **fully responsible** before the regulator. The supplier assessment is the documented basis that enables leverage — not the delegation of responsibility.

> [!tip] Embedded usage rules
> 1. **Before the contract** (GAMP 5 §M2 §10.4) — the assessment is completed **before** finalizing the contract and beginning the service.
> 2. **3 routes** — basic / postal-email audit / on-site-or-virtual audit. The route is chosen by risk, category, novelty/complexity, and leverage intent.
> 3. **Conditional leverage** — supplier evidence (testing, config) can only be leveraged if the assessment supports it.
> 4. **Cloud/SaaS** — activates **exit strategy** + **pre-release version test** requirements (Annex 11 §7.5 viii-ix). ISO 27001/SOC 2 may be leveraged.
> 5. **CAPAs with evidence** — if the decision is "use subject to CAPAs", evidence of completion is required (a supplier letter alone is insufficient).
> 6. **Audit report = quality record** — retained as system documentation.
> 7. **Periodic re-evaluation** — especially after changes in supplier ownership/management/licensing.

---

## 0. Identification and signatures

### System and supplier

| Field | Value |
|---|---|
| **System** | `{{system_name}}` |
| **Supplier assessed** | `{{supplier_name}}` |
| **Product / service** | `{{product_service}}` |
| **GAMP category** | `{{gamp_category}}` |
| **Assessment route** | `{{assessment_route}}` |
| **Cloud/SaaS?** | `{{is_cloud_saas}}` |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Assessor / Author | `{{assessor_name}}` | `{{assessor_dept}}` |  |  |
| Reviewer (SME) |  |  |  |  |
| Approver (Quality Unit) |  |  |  |  |

---

## 1. Objective

Formally evaluate supplier **`{{supplier_name}}`** of product/service **`{{product_service}}`** for system **`{{system_name}}`**, in accordance with GAMP 5 §M2, **before** finalizing the contract, in order to enable leverage of supplier evidence in the validation without transferring regulatory responsibility.

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| Supplier Assessment | Formal evaluation of the supplier (QMS, technical, good practices) |
| Leverage | Using supplier evidence (testing, config, controls) in the validation |
| Basic assessment | Evaluation via public information / reputation / prior experience |
| Postal/email audit | Questionnaire + documentary evidence |
| On-site/virtual audit | Audit with opening → "show me" → closing → audit report |
| CAPA | Corrective and Preventive Action |

---

## 3. Assessment route selection

**Route selected**: `{{assessment_route}}`

> GAMP 5 §M2 §10.3 — the route is chosen by: initial risk, novelty/complexity, GAMP category, and leverage intent.

| Route | When | Method |
|---|---|---|
| **Basic** | Low-impact commodity components | Public information, market reputation, prior experience, peer feedback |
| **Postal/email audit** | Standard/configurable products, remote supplier | Questionnaire + supporting evidence |
| **On-site/virtual audit** | High impact, complex, novel; cloud supplier that declines postal audit | Opening → "show me" review → closing → audit report |

**Route justification**: (risk + category + novelty + leverage intent)

---

## 4. Leverage intent

**What is intended to be leveraged**: `{{leverage_intent}}`

| Supplier evidence | Leverage intended? | Condition |
|---|---|---|
| Supplier testing (counts as coverage) |  | Assessment OK + access to results |
| Configuration evidence |  |  |
| Operational controls (cloud) |  |  |
| Design/development documentation |  |  |

---

## 5. Leveraged certifications

**Certifications**: `{{certifications_leveraged}}`

| Certification | Current? | Scope/boundary evaluated |
|---|---|---|
| ISO 27001 (ISMS) |  |  |
| ISO 27017 (cloud security) |  |  |
| SOC 2 (Type 1/2) |  |  |
| ISO 9001 (QMS) |  |  |
| ISO 20000-1 / HITRUST |  |  |

> [!note] Certificate boundary
> Verify that the scope/boundary of the certification actually covers the contracted service (a SOC 2 may exclude the relevant component).

---

## 6. Evaluation (by route)

### 6.1 Supplier QMS
(Is there a defined QMS? lifecycle approach, Agile acceptable, continuous improvement)

### 6.2 Technical capability and good practices
(GAMP §7 Table 7.1 — 12 supplier good practices: requirements, quality planning, specs, design review, testing, release, support, etc.)

### 6.3 Sub-suppliers
(Does the supplier evaluate its own sub-suppliers? Especially relevant in cloud)

### 6.4 Audit findings

| Finding | Severity | Agreed CAPA | Evidence of completion | Closed (✓) |
|---|---|---|---|---|
|  |  |  |  |  |

---

## 7. Cloud/SaaS requirements (if applicable)

> [!warning] Only if `is_cloud_saas == true` — Annex 11 §7.5
> The contract with a cloud/SaaS supplier must cover (among 9 other items):

| Annex 11 §7.5 requirement | Covered in contract? |
|---|---|
| **Exit strategy** (viii) — retain control of data upon exit |  |
| **Pre-release version test** (ix) — ability to test new versions before their release |  |
| SLA / KPIs |  |
| Notification of provider changes/releases |  |
| Data location / data residency |  |

---

## 8. Decision

**Assessment decision**: `{{assessment_decision}}`

| Possible decision | Meaning |
|---|---|
| Use unconditionally | Use without conditions |
| Use for certain products/versions | Use only for certain products/versions |
| Use subject to CAPAs | Use subject to CAPAs with evidence of completion |
| Use with additional oversight/testing | Use with additional supervision/testing |
| Prohibit use | Prohibit use |

**Reassessment schedule**: `{{reassessment_schedule}}`

---

## 9. Related documents

| Document | Reference |
|---|---|
| GxP Assessment | [GXP-ASSESS](GXP-ASSESS.md) |
| Validation Plan | [VP](VP.md) |
| Initial Risk Assessment | [RA-INIT](RA-INIT.md) |
| Audit report (quality record) | (internal reference) |
| Organization's vendor/supplier policy | `{{org_vendor_policy_ref}}` |
| `{{custom_ref}}` |  |

---

## 10. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{assessor_name}}`, `{{assessor_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] Before the contract — not after
> The most common mistake is to contract first and evaluate later. GAMP 5 §M2 §10.4 is explicit: the assessment is completed before finalizing the contract.

> [!note] Leverage ≠ delegation of responsibility
> The assessment enables leveraging supplier evidence, but regulatory responsibility is non-delegable (Annex 11 §7.1). Supplier testing counts as coverage only if the assessment supports it.

> [!tip] Assessment reuse
> Joint audits, shared audit reports, and corporate audit repositories reduce duplication. Cross-company reuse is permitted with a sharing agreement + documented justification.

## Related

- [GXP-ASSESS](GXP-ASSESS.md) · [VP](VP.md) · [RA-INIT](RA-INIT.md) · [VR](VR.md)
- GAMP 5 · EU Annex 11 · iso 27001
- supplier assessment · leveraging supplier involvement · supplier good practices

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.supplier-assess` skill.

### Pre-flight

1. **Read `.gxp-dev.yaml`** + locate approved GXP-ASSESS.
2. **Confirm there is an external supplier** (Cat 4/5 or services). If purely in-house custom with no supplier → may not apply (document).
3. **Read RA-INIT if it exists** — risk + category determine the route.
4. **Read `templates/csv/SUP-ASSESS.md`** from the toolkit as the source template.

### Generation flow

1. **Identify supplier + product/service + cloud/SaaS**.
2. **Select route** (§3) by risk/category/novelty/leverage.
3. **Leverage intent** (§4) + certifications (§5).
4. **Evaluation** (§6) per route; CAPAs with evidence.
5. **Cloud requirements** (§7) if SaaS — exit strategy + pre-release test.
6. **Decision** (§8) + reassessment schedule.
7. **Anti-hallucination**: `[NEEDS CLARIFICATION: ...]`; never invent certifications or audit findings.
8. **Output**: write `specs/SUP-ASSESS.md` (status: draft).
9. **Post-flight**: `validate-frontmatter.py` + `check-clarification-markers.py`.

### `status` transitions

```
draft ──[route + evaluation + decision complete]──> in-progress
in-progress ──[audit executed + CAPAs agreed]──> completed
completed ──[QU approves + CAPA evidence]──> approved
approved ──[re-evaluation / supplier change]──> superseded
```

> [!warning] Complete before the contract
> GAMP 5 §M2 §10.4: the assessment reaches approved before finalizing the contract.

### Downstream mapping

| Origin (SUP-ASSESS) | Destination | Rule |
|---|---|---|
| assessment_decision | VP | Determines what supplier leverage is permitted |
| Leverageable supplier testing | OQ | Counts as coverage if assessment OK |
| Certifications (cloud) | IQ/infrastructure | Leverage of operational controls |
| Audit report | VR | The Validation Report summarizes the supplier assessment (GAMP M7) |
