---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "RA-DET — Detailed Risk Assessment / FMEA (canonical CSV template)"
type: template
template_class: csv
template_id: "RA-DET"
template_version: "0.1.0"
v_model_phase: risk-assessment-detailed
gamp_categories_applicable: [4, 5]
language: en
status: canonical-draft
created: 2026-05-28
updated: 2026-05-29
# Round 2 (2026-05-29): translated to English canonical (was language: es). §-citations + IDs preserved verbatim.

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# RA-DET implements GAMP 5 §M3 step 3 (Functional Risk Assessment). It is the
# detailed FMEA that deepens the high-risk functions identified in RA-INIT,
# using URS + FS. Calculates RPN, defines controls, and scales testing rigor.
inputs:
  - template_id: "RA-INIT"
    required: true
    description: "Initial Risk Assessment — provides the high-Risk Priority functions that require detailed FMEA analysis"
  - template_id: "URS"
    required: true
    description: "User Requirements — the GxP requirements whose risk is analyzed in detail"
  - template_id: "FS"
    required: false
    description: "Functional Specification — the technical realization enables failure analysis at function level"
outputs:
  - artifact: "RA-DET instance (Markdown) — FMEA-based detailed risk assessment"
    consumed_by:
      - "OQ"        # RPN determines testing rigor (positive/negative/stress)
      - "PQ"        # PQ scenarios prioritize high-RPN functions
      - "VR"        # Validation Report summarizes residual risk
applicable_regulations:
  - "gamp-5"          # §M3 step 3 (Functional Risk Assessment) + §11.5.4 (Risk Priority) + §5 (QRM)
  - "ich-q9"          # QRM + FMEA methodology
  - "eu-annex-11"     # §4 Risk Management
based_on:
  - "GAMP 5 §M3 step 3 (Functional Risk Assessment) + ICH Q9 FMEA — Occurrence × Relevance × Detection → RPN; double evaluation (before/after mitigation); target RPN ≤ 4"
  - "Structure: FMEA with 1-3 scale, RPN, double evaluation, RPN→test rigor; traceability RA-DET↔URS/FS↔RA-INIT"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
  system_id:
    type: string
    required: true
  ra_init_ref:
    type: string
    required: true
    description: "Identifier of the approved RA-INIT that triggers this detailed analysis"
  urs_ref:
    type: string
    required: true
  fs_ref:
    type: string
    required: false
  gamp_category:
    type: enum
    required: true
    values: [4, 5]
    description: "RA-DET typically for Cat 4/5; simple Cat 3 usually suffices with RA-INIT"
  scope_of_analysis:
    type: string
    required: true
    description: "Which functions/requirements this detailed analysis covers (the high-risk ones from RA-INIT)"
  ra_author_name:
    type: string
    required: true
  ra_author_dept:
    type: string
    required: true
  org_qrm_policy_ref:
    type: string
    required: false
  custom_ref:
    type: string
    required: false

# ─── FMEA method (GAMP 5 §M3 + ICH Q9 — 1-3 scale) ─────────────────────────
fmea_method:
  formula: "RPN = Occurrence (O) × Relevance/Severity (R) × Detection (D)"
  scale: "Each factor 1-3 (simplified pharma scale, consistent with ICH Q9 and GAMP 5; NOT the classic FMEA 1-10 scale)"
  rpn_range: "1-27"
  occurrence: "O — probability that the failure occurs (1=low, 3=high; scales with GAMP category)"
  relevance: "R — severity of impact on PS/PQ/DI (1=low, 3=high; defined by the business process)"
  detection: "D — probability of NOT detecting the failure in time (1=easy to detect, 3=difficult to detect)"
  double_evaluation: "RPN is calculated before (evaluation 1) and after (evaluation 2) mitigation measures"
  mitigation_target: "Final RPN ≤ 4"
  rpn_to_test_rigor:
    "1-4": "Testing per Good Engineering Practice (GEP) — optional"
    "6-9": "Positive testing (happy path)"
    "12-27": "Positive + negative + stress/performance testing"

# ─── INSTANCE frontmatter spec (not the template's) ─────────────────────────
instance_frontmatter_spec:
  required_fields:
    - title
    - type: "instance"
    - based_on_template: "RA-DET"
    - based_on_template_version
    - system_id
    - traces_to            # RA-INIT instance + URS instance
    - gamp_category
    - status               # draft | in-review | approved | superseded
    - version
    - created
    - updated
    - language
  conditional_fields:
    - approved_by: "required if status == approved"
    - supersedes
    - residual_risk_accepted_by: "who accepts the residual risk (typically Process Owner + QU)"

# ─── Validation rules (Round 1 subset) ──────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "traces_to must point to an approved RA-INIT + an approved URS"
  - "Each RA-DET-NNN row must cite the URS/FS-ID analyzed + the RA-INIT-NNN it details"
  - "RPN = O × R × D, each factor on a 1-3 scale (RPN range 1-27)"
  - "Each risk must have a double evaluation (RPN before and after mitigation)"
  - "The mitigation target is RPN ≤ 4; if a risk remains with RPN > 4, residual risk acceptance must be documented"
  - "Relevance (severity) is justified from the process, not from the GAMP category"
  - "The final RPN determines the testing rigor required in OQ/PQ (1-4 GEP / 6-9 positive / 12-27 positive+negative+stress)"

tags:
  - template
  - csv
  - risk-assessment
  - ra-det
  - fmea
  - qrm
  - gamp-m3
  - canonical
---

# RA-DET — Detailed Risk Assessment (FMEA)

> [!note] Canonical CSV template
> **Canonical** template for the **Detailed Risk Assessment** based on **FMEA** (Failure Mode & Effect Analysis) methodology. Implements **Step 3** of the QRM process of GAMP 5 (§M3 — Functional Risk Assessment). It deepens the high-risk functions identified in [RA-INIT](RA-INIT.md), calculates the RPN, defines mitigation controls, and **scales the testing rigor** of [OQ](OQ.md)/[PQ](PQ.md). Aligned with ICH Q9.

> [!warning] RA-DET ≠ RA-INIT
> The [RA-INIT](RA-INIT.md) is the **initial** assessment (qualitative H/M/L, steps 1-2, decides category). The **RA-DET** (this document) is the **detailed** one (quantitative FMEA O×R×D→RPN, step 3, per function). The RA-DET takes the functions with Risk Priority=H from RA-INIT and analyzes them in depth.

> [!tip] Embedded usage rules
> 1. **FMEA 1-3 scale** — Occurrence × Relevance × Detection, each factor 1-3 → RPN (1-27). Pharma simplification consistent with ICH Q9 (not the classic 1-10 scale).
> 2. **Relevance = process severity** — defined by the business process, NOT the GAMP category. Occurrence does scale with the category.
> 3. **Detection is inverted** — high D = difficult to detect = worse. An invisible failure is more dangerous.
> 4. **Double evaluation** — RPN before and after mitigation; demonstrates the effectiveness of controls.
> 5. **Target RPN ≤ 4** — if a risk remains > 4 after mitigation, residual risk acceptance is documented.
> 6. **RPN → testing rigor** — 1-4 GEP / 6-9 positive / 12-27 positive+negative+stress. This is the bridge RA→OQ/PQ.
> 7. **Traceability** — each `RA-DET-NNN` cites the URS/FS-ID + the RA-INIT-NNN it details.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **RA-INIT that triggers it** | `{{ra_init_ref}}` ([RA-INIT](RA-INIT.md)) |
| **URS analyzed** | `{{urs_ref}}` ([URS](URS.md)) |
| **FS analyzed** | `{{fs_ref}}` ([FS](FS.md)) |
| **GAMP category** | `{{gamp_category}}` |
| **Scope of analysis** | `{{scope_of_analysis}}` |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Author (SME / CSV) | `{{ra_author_name}}` | `{{ra_author_dept}}` |  |  |
| Reviewer (Process Owner) *(owner of Relevance)* |  |  |  |  |
| Approver 1 (System Owner) |  |  |  |  |
| Approver 2 (Quality Unit) |  |  |  |  |

---

## 1. Objective

Analyze in detail, via FMEA, the risks of the high-risk functions of system **`{{system_name}}`** (identified in [RA-INIT](RA-INIT.md)), calculate their RPN, define mitigation measures, and determine the testing rigor required in OQ/PQ. This is **Step 3** of the QRM process (GAMP 5 §M3).

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| FMEA | Failure Mode & Effect Analysis |
| RPN | Risk Priority Number = O × R × D (range 1-27) |
| Occurrence (O) | Probability of failure occurrence (1-3) |
| Relevance (R) | Severity of impact on PS/PQ/DI (1-3) — defined by the process |
| Detection (D) | Difficulty of detecting the failure in time (1=easy, 3=difficult) |
| Residual risk | RPN after applying mitigation measures |

---

## 3. FMEA methodology

```
RPN = Occurrence (O) × Relevance (R) × Detection (D)
```

Each factor on a **1-3** scale → RPN in the range **1-27**.

### 3.1 Rating scales

| Value | Occurrence (O) | Relevance (R) | Detection (D) |
|---|---|---|---|
| **1** | Unlikely | Minor impact on PS/PQ/DI | Easy to detect (automatic control) |
| **2** | Possible | Moderate impact | Detectable with effort (manual control) |
| **3** | Probable | Critical impact on PS/PQ/DI | Difficult to detect (no control) |

### 3.2 RPN categories → testing rigor

| RPN | Testing strategy |
|---|---|
| **1-4** | Good Engineering Practice (GEP) — testing optional |
| **6-9** | Positive testing (happy path) in OQ |
| **12-27** | Positive + negative + stress/performance testing in OQ/PQ |

### 3.3 Mitigation target

Reduce the RPN to **≤ 4** through mitigation measures. If not achievable, document **residual risk acceptance** (Process Owner + QU).

---

## 4. Risk Analysis (FMEA)

> For each high-risk function from RA-INIT, one row. Double evaluation: RPN before (eval 1) and after (eval 2) the measures.

| RA-DET-ID | Analyzes (URS/FS-ID) | Details (RA-INIT-NNN) | Potential failure | Cause | Consequence (PS/PQ/DI) | Existing controls | O₁ | R₁ | D₁ | RPN₁ | Mitigation measures | O₂ | R₂ | D₂ | RPN₂ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `RA-DET-001` | `URS-FUNC-001` | `RA-INIT-001` |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 5. Residual risk

> Risks that remain with RPN > 4 after mitigation. Require formal acceptance.

| RA-DET-ID | Residual RPN | Justification for acceptance | Accepted by | Date |
|---|---|---|---|---|
|  |  |  |  |  |

---

## 6. Summary and link to testing

| Metric | Value |
|---|---|
| Total risks analyzed | |
| Risks with high RPN₁ (12-27) | |
| Risks mitigated to RPN₂ ≤ 4 | |
| Residual risks accepted (> 4) | |

**Link to OQ/PQ**: functions with RPN ≥ 12 require negative/stress testing; RPN 6-9 requires positive testing. This prioritization feeds the strategy of [OQ](OQ.md) and [PQ](PQ.md).

---

## 7. Related documents

| Document | Reference |
|---|---|
| Initial Risk Assessment | `{{ra_init_ref}}` ([RA-INIT](RA-INIT.md)) |
| URS analyzed | `{{urs_ref}}` ([URS](URS.md)) |
| FS analyzed | `{{fs_ref}}` ([FS](FS.md)) |
| Operational Qualification | [OQ](OQ.md) |
| Validation Report | [VR](VR.md) |
| Organization's QRM policy | `{{org_qrm_policy_ref}}` |
| `{{custom_ref}}` |  |

---

## 8. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{ra_author_name}}`, `{{ra_author_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] RA-DET deepens, RA-INIT decides
> The RA-INIT decides the category and which functions are high-risk. The RA-DET performs the detailed FMEA only on those high-risk functions — it does not re-analyze everything. Simple Cat 3 is typically closed with RA-INIT; Cat 4/5 requires RA-DET.

> [!note] Double evaluation = evidence of control
> Capturing the RPN before and after mitigation demonstrates to the auditor that controls are effective (not merely that they exist).

> [!tip] RPN is the bridge RA→test
> The RPN→rigor categorization is the direct connection between the risk analysis and the OQ/PQ scripts. A requirement with RPN 12-27 without negative testing is a coverage gap.

## Related

- [RA-INIT](RA-INIT.md) · [URS](URS.md) · [FS](FS.md) · [OQ](OQ.md) · [PQ](PQ.md) · [VR](VR.md)
- GAMP 5 · ich q9 · EU Annex 11
- quality risk management process · risk priority · residual risk

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the skill `gdd.ra.detail-from-urs-fs`.

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer. If it does not exist → redirect to `/gdd.init`.
2. **Locate the approved RA-INIT** (`specs/RA-INIT.md`) — source of the high-risk functions.
3. **Locate the approved URS** + FS if it exists — the requirements/realizations to analyze.
4. **Read `templates/csv/RA-DET.md`** from the toolkit as the source template (this file).

### Generation flow

1. **Parse functions with Risk Priority=H** from RA-INIT.
2. **For each one**, generate ≥1 `RA-DET-NNN` with: URS/FS-ID analyzed, RA-INIT-NNN it details, potential failure, cause, consequence (PS/PQ/DI), existing controls, O₁/R₁/D₁/RPN₁, mitigation measures, O₂/R₂/D₂/RPN₂.
3. **Calculate RPN** = O × R × D (1-3 scale). Relevance from the process, Occurrence from the category.
4. **Residual risks** > 4 → table §5 with acceptance.
5. **Anti-hallucination**: `[NEEDS CLARIFICATION: ...]` when information is missing; never invent risk ratings.
6. **Output**: write `specs/RA-DET.md` (status: draft); print RPN distribution + risks requiring negative testing.
7. **Post-flight**: `validate-frontmatter.py` + `check-clarification-markers.py`.

### `status` transitions

```
draft ──[complete FMEA + RPN calculated + residuals accepted]──> in-review
in-review ──[Process Owner + QU sign]──> approved
approved ──[new version]──> superseded
```

### Downstream mapping

| Origin (RA-DET) | Destination | Rule |
|---|---|---|
| RPN ≥ 12 | OQ negative/stress test | Testing rigor scaled by RPN |
| RPN 6-9 | OQ positive test | |
| High-RPN functions | PQ priority scenarios | |
| Residual risk | VR | Validation Report summarizes accepted residual risk |
