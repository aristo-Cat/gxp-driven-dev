---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "RA-INIT — Initial Risk Assessment (canonical CSV template)"
type: template
template_class: csv
template_id: "RA-INIT"
template_version: "0.1.0"
v_model_phase: risk-assessment-initial
gamp_categories_applicable: [1, 3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-28
updated: 2026-05-29
# Round 2 (2026-05-29): translated to English canonical (was language: es). §-citations + IDs preserved verbatim.

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# RA-INIT implements GAMP 5 §M3 steps 1-2 (Initial Risk Assessment + System
# Impact, and Identify Functions with Impact). Its output decides the gamp_category
# that feeds URS + FS. This is NOT the detailed RA (FMEA/RPN) — that is RA-DET (Round 2).
inputs:
  - template_id: "URS"
    required: true
    description: "User Requirements Specification — source of the functions/requirements to be evaluated for GxP impact. RA-INIT may run in parallel with a draft URS (GAMP 5 §M3: 'before or during requirements development')."
  - template_id: "GXP-ASSESS"
    required: false
    description: "GxP Assessment of the system — if it exists, it contributes the initial GxP determination and regulatory context."
outputs:
  - artifact: "RA-INIT instance (Markdown)"
    consumed_by:
      - "URS"        # decides gamp_category → fills placeholder {{gamp_category}}
      - "FS"         # scales the level of detail of the FS according to risk priority
      - "RA-DET"     # Detailed RA (Round 2) takes the high-risk functions from here
      - "VP"         # Validation Plan takes the risk-based strategy from here
applicable_regulations:
  - "gamp-5"          # §5.3 pp.51-54 (5-step QRM) + §M3 steps 1-2 + §M4 categorization
  - "ich-q9"          # QRM principles (severity/probability/detectability)
  - "eu-annex-11"     # §4 Risk Management (2025 draft)
based_on:
  - "GAMP 5 §5.3 (Five-step QRM process, steps 1-2) + §M3 §11.5.4 (Risk Priority method) + §M4 (categorization)"
  - "ICH Q9 (R1) Quality Risk Management — severity × probability × detectability"
  - "Structure: Initial RA decides GxP scope + system impact + GAMP category + functions with PS/PQ/DI impact; RA-INIT↔URS traceability"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
    description: "Human-readable name of the system (matches the source URS)"
  system_id:
    type: string
    required: true
  urs_ref:
    type: string
    required: false
    description: "Identifier + version of the URS being assessed (may be draft — RA-INIT may run before URS approved)"
  system_boundary:
    type: string
    required: true
    description: "Boundary of the system under analysis: what is inside/outside the scope of the assessment"
  business_process:
    type: string
    required: true
    description: "GxP business process the system supports (severity derives from the process, not from the system)"
  gxp_determination:
    type: enum
    required: true
    values: ["gxp-relevant", "non-gxp", "indirect-gxp"]
    description: "Outcome of Step 1: is the system GxP-relevant?"
  system_impact:
    type: enum
    required: true
    values: ["high", "medium", "low"]
    description: "Overall impact of the system on patient safety / product quality / data integrity"
  gamp_category_decision:
    type: enum
    required: true
    values: [1, 3, 4, 5]
    description: "CRITICAL OUTPUT: determined GAMP category. Feeds the {{gamp_category}} placeholder in URS and FS."
  gamp_category_rationale:
    type: string
    required: true
    description: "Justification for the assigned category (GAMP 5 §M4 criteria)"
  part11_applicable:
    type: boolean
    required: true
    description: "Does the system generate/store GxP electronic records or use GxP e-signatures? Decides activation of URS-EREC/ESIG presets."
  detailed_ra_required:
    type: boolean
    required: true
    description: "Is a Detailed RA (RA-DET, FMEA/RPN) required? Typically true for Cat 4/5 or high system_impact."
  ra_author_name:
    type: string
    required: true
  ra_author_dept:
    type: string
    required: true
  org_qrm_policy_ref:
    type: string
    required: false
    description: "Reference to the organization's corporate QRM policy (if any)"
  custom_ref:
    type: string
    required: false

# ─── Risk method (GAMP 5 §M3 §11.5.4 — qualitative H/M/L) ───────────────────
# RA-INIT uses the qualitative H/M/L method from GAMP 5 (NOT the FMEA O×R×D 1-3,
# which belongs to the detailed RA-DET). Risk Class = Severity × Probability;
# Risk Priority = Risk Class × Detectability.
risk_method:
  formula: "Risk Class = Severity × Probability ; Risk Priority = Risk Class × Detectability"
  scale: "H / M / L (qualitative, GAMP 5 §11.5.4 p.116)"
  severity_owner: "The business process (independent of the GAMP category)"
  probability_note: "Tends to scale with the GAMP category (Cat 1 → 5)"
  detectability_note: "Considers both automatic and manual detection mechanisms"
  risk_class_matrix:
    description: "Severity (rows H/M/L) × Probability (columns H/M/L) → Risk Class H/M/L"
  risk_priority_matrix:
    description: "Risk Class × Detectability → Risk Priority. Low detectability raises the priority."

# ─── Instance frontmatter spec ────────────────────────────────────────────────
instance_frontmatter_spec:
  required_fields:
    - title
    - type: "instance"
    - based_on_template: "RA-INIT"
    - based_on_template_version
    - system_id
    - traces_to            # URS instance (may be draft)
    - gamp_category        # the decided category — key output
    - status               # draft | in-review | approved | superseded
    - version
    - created
    - updated
    - language
  conditional_fields:
    - approved_by: "required if status == approved"
    - supersedes: "version of the previous RA-INIT if this is a revision"
    - detailed_ra_ref: "reference to RA-DET if detailed_ra_required == true"

# ─── Validation rules (Round 1 subset) ──────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "gamp_category_decision must be one of [1, 3, 4, 5] with non-empty rationale"
  - "If gxp_determination == 'gxp-relevant' → the functions table (Step 2) cannot be empty"
  - "Each RA-INIT-NNN row must cite at least one URS-<CATEGORY>-NNN (or mark 'system-level' if it is a system-level risk)"
  - "Severity must be justified from the business_process, not from the GAMP category"
  - "If system_impact == 'high' or gamp_category in [4,5] → detailed_ra_required should be true (justify if false)"
  - "part11_applicable must be consistent with the activation of URS-EREC/ESIG presets in the URS"
  - "RA-INIT must reach status: approved before the URS (the URS inherits the gamp_category from here — GAMP 5 §M3 step 1)"
  - "Process Owner must sign (they are the owner of severity)"

tags:
  - template
  - csv
  - risk-assessment
  - ra-init
  - qrm
  - gamp-m3
  - v-model
  - canonical
---

# RA-INIT — Initial Risk Assessment

> [!note] Canonical CSV template
> **Canonical** template for the **Initial Risk Assessment (RA-INIT)** of a computerized system. It implements **steps 1-2 of the 5-step QRM process** of GAMP 5 (§5.3 pp.51-54 + §M3): *Initial Risk Assessment + System Impact* and *Identify Functions with Impact*. Its **critical output is the determination of the GAMP category**, which feeds the `{{gamp_category}}` placeholder in the [URS](URS.md) and the [FS](FS.md). Aligned with ICH Q9 and EU Annex 11 §4.

> [!warning] RA-INIT ≠ RA-DET
> This is the **initial** RA (qualitative, H/M/L, decides category + high-risk functions). The **detailed** RA (FMEA with O×R×D → RPN, controls per function) is a separate template [RA-DET](RA-DET.md) (GAMP 5 §M3 step 3, typically Round 2). The RA-INIT decides *whether* a RA-DET is needed.

> [!tip] Embedded usage rules
> 1. **GAMP 5 §M3 step 1 timing** — the RA-INIT may (and should) run *"before or during requirements development"*. It may run in parallel with a draft URS; it must reach `approved` **before** the URS, because the URS inherits the category from here.
> 2. **Severity derives from the process** — the severity of the impact is defined by the GxP business process, NOT by the GAMP category. Do not inflate severity simply because it is Cat 5.
> 3. **Probability scales with category** — the probability of failure tends to increase Cat 1 → 5.
> 4. **Detectability matters** — a risk with low detectability raises the priority even when severity/probability are moderate.
> 5. **Traceability** — each `RA-INIT-NNN` cites the `URS-<CATEGORY>-NNN` being assessed (or `system-level` if it is a system-level risk).
> 6. **The output drives the cascade** — the category determined here scales the entire rest of the V-Model: depth of the FS, need for CS/DS, rigor of testing in OQ/PQ.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **URS assessed** | `{{urs_ref}}` *(may be draft)* |
| **GxP business process** | `{{business_process}}` |
| **Determined GAMP category** | `{{gamp_category_decision}}` *(key output of this document)* |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Author | `{{ra_author_name}}` | `{{ra_author_dept}}` |  |  |
| Reviewer 1 (Process Owner) *(owner of severity)* |  |  |  |  |
| Reviewer 2 (SME) |  |  |  |  |
| Approver 1 (System Owner) |  |  |  |  |
| Approver 2 (Quality Unit) |  |  |  |  |

> [!note] Roles — GAMP 5 §M3 Table 11.1
> Process Owner / System Owner establish the team and approve; the SME + key-users identify and analyse risks; the Quality Unit owns the compliance-related risks. The **Process Owner signs** because they are the owner of severity.

---

## 1. Objective

This document performs the **Initial Risk Assessment** of the system **`{{system_name}}`** in accordance with the five-step QRM process of GAMP 5 (§5.3 + §M3), covering:

- **Step 1** — Initial Risk Assessment + System Impact: GxP determination, system impact, **GAMP category**, and applicability of 21 CFR Part 11 / EU Annex 11.
- **Step 2** — Identify Functions with Impact: identification of the functions/requirements that impact patient safety, product quality, or data integrity.

Steps 3-5 (detailed Functional Risk Assessment, implementation/verification of controls, and periodic review) are executed in [RA-DET](RA-DET.md) and during operation.

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| RA-INIT | Initial Risk Assessment (this document) |
| RA-DET | Detailed Risk Assessment (FMEA/RPN, GAMP 5 §M3 step 3) |
| QRM | Quality Risk Management (ICH Q9) |
| PS / PQ / DI | Patient Safety / Product Quality / Data Integrity (the three impact axes) |
| Severity | Severity of the impact on PS/PQ/DI (defined by the business process) |
| Probability | Probability that the failure occurs (scales with the GAMP category) |
| Detectability | Probability of detecting the failure before it causes harm |
| Risk Class | Severity × Probability |
| Risk Priority | Risk Class × Detectability |
| GAMP category | Cat 1 (infrastructure) / 3 (standard) / 4 (configured) / 5 (custom) — GAMP 5 §M4 |

---

## 3. Methodology

This RA-INIT applies the qualitative method of GAMP 5 §M3 §11.5.4 (p.116):

```
Risk Class    = Severity × Probability
Risk Priority = Risk Class × Detectability
```

Each factor is rated **H / M / L** (high / medium / low).

### 3.1 Risk Class matrix (Severity × Probability)

| Severity ↓ \ Probability → | L | M | H |
|---|---|---|---|
| **H** | M | H | H |
| **M** | L | M | H |
| **L** | L | L | M |

### 3.2 Risk Priority matrix (Risk Class × Detectability)

> Low detectability (L) **raises** the priority: a failure that is hard to detect is more dangerous.

| Risk Class ↓ \ Detectability → | H (easy to detect) | M | L (hard to detect) |
|---|---|---|---|
| **H** | M | H | H |
| **M** | L | M | H |
| **L** | L | L | M |

### 3.3 Risk Priority interpretation → strategy

| Risk Priority | Control + verification strategy |
|---|---|
| **H** | Eliminate by design (preferred) or robust controls + exhaustive testing (positive + negative + stress) in OQ/PQ. Requires RA-DET. |
| **M** | Controls + positive testing (happy path) in OQ. Consider RA-DET. |
| **L** | Good Engineering Practice + supplier evidence is typically sufficient. |

---

## 4. System context and boundary

**System boundary under analysis** (what is inside/outside the scope):

`{{system_boundary}}`

**Supported GxP business process** (origin of severity):

`{{business_process}}`

---

## 5. Step 1 — Initial Risk Assessment + System Impact

### 5.1 GxP determination

Is the system GxP-relevant? `{{gxp_determination}}`

> Criterion: the system creates/modifies/stores/transmits records under a GxP predicate rule (GMP, GLP, GCP, GDP, GVP), or controls a process with impact on PS/PQ/DI.

### 5.2 System impact

Overall impact on patient safety / product quality / data integrity: `{{system_impact}}`

| Axis | Impact (H/M/L) | Justification |
|---|---|---|
| Patient Safety (PS) |  |  |
| Product Quality (PQ) |  |  |
| Data Integrity (DI) |  |  |

### 5.3 Determination of the GAMP category (critical output)

**Assigned category**: `{{gamp_category_decision}}`

**Rationale**: `{{gamp_category_rationale}}`

| Category | Criterion (GAMP 5 §M4) | Applies? |
|---|---|---|
| **Cat 1** | Infrastructure software (OS, DB engine, middleware). *Qualified*, not validated. |  |
| **Cat 3** | Standard non-configured product (COTS parameterizable, used out-of-the-box). |  |
| **Cat 4** | Configured product (LIMS, SCADA, ERP, CDS, EDMS, BMS, configurable spreadsheets). |  |
| **Cat 5** | Custom / bespoke application (developed to specification; higher inherent risk). |  |

> [!warning] This decision scales the entire cascade
> The category determined here fills the `{{gamp_category}}` of the [URS](URS.md) and the [FS](FS.md), and defines the depth of the rest of the V-Model: Cat 3 → light FS; Cat 4 → FS + CS; Cat 5 → FS + DS + module descriptions. Continuum, not rigid boxes (§M4 §12.1).

### 5.4 Applicability of 21 CFR Part 11 / EU Annex 11

Does the system generate/store GxP electronic records or use electronic signatures? `{{part11_applicable}}`

> This result decides the **activation of the presets** `URS-EREC` / `URS-ESIG` in the URS. If `true`, the URS must activate sections 9.2/9.3.

| Question | Yes/No | Consequence |
|---|---|---|
| Does it generate/store GxP electronic records as the primary source? |  | → activate preset URS-EREC |
| Does it implement electronic signatures (not scanned ones)? |  | → activate preset URS-ESIG |
| Does it process GxP data in cloud/SaaS or with remote access? |  | → activate preset URS-SEC (encryption + MFA) |
| Does it have interfaces that transfer GxP data? |  | → activate preset URS-API |
| Does it migrate legacy data from a predecessor system? |  | → activate preset URS-MIGR |

---

## 6. Step 2 — Identify Functions with Impact

Identify the functions/requirements from the URS that impact PS/PQ/DI. Only these functions require risk analysis (functions without GxP impact fall outside the scope of formal validation).

| URS-ID | Function / Requirement | Impacts PS | Impacts PQ | Impacts DI | GxP-critical? |
|---|---|---|---|---|---|
| `URS-FUNC-001` |  |  |  |  |  |
|  |  |  |  |  |  |

---

## 7. Initial Risk Register — `RA-INIT-NNN`

> For each function with GxP impact (Step 2), assess Risk Class and Risk Priority at the **initial** level (qualitative). Functions with Risk Priority = H proceed to RA-DET for detailed FMEA analysis.

| RA-ID | Assesses (URS-ID) | Risk (potential failure) | Severity | Probability | Risk Class | Detectability | Risk Priority | Initial control | Proceed to RA-DET? |
|---|---|---|---|---|---|---|---|---|---|
| `RA-INIT-001` | `URS-FUNC-001` |  |  |  |  |  |  |  |  |
| `RA-INIT-002` | `system-level` |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |

---

## 8. Decision: is a Detailed RA (RA-DET) required?

**Is RA-DET required?** `{{detailed_ra_required}}`

> [!note] Criterion
> Typically `true` if: `system_impact == high`, or `gamp_category in [4, 5]`, or there is ≥1 function with Risk Priority = H. If `false`, justify (e.g. standard Cat 3 with low impact where Good Engineering Practice + supplier evidence is sufficient).

| Trigger | Present? | → RA-DET |
|---|---|---|
| system_impact == high |  |  |
| gamp_category 4 or 5 |  |  |
| ≥1 function with Risk Priority = H |  |  |

**Final decision + justification**:

---

## 9. Related documents

| Document | Reference |
|---|---|
| URS assessed | `{{urs_ref}}` ([URS](URS.md)) |
| GxP Assessment | [GXP-ASSESS](GXP-ASSESS.md) |
| Organization's QRM policy | `{{org_qrm_policy_ref}}` |
| Detailed Risk Assessment (if applicable) | [RA-DET](RA-DET.md) |
| Validation Plan | [VP](VP.md) |
| `{{custom_ref}}` |  |

---

## 10. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{ra_author_name}}`, `{{ra_author_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] RA-INIT is the node that scales the cascade
> The GAMP category determined here (§5.3) is the parameter that controls the depth of the entire downstream V-Model. It is the first "step" of the 5-step QRM process; steps 3-5 live in [RA-DET](RA-DET.md) and in operation (periodic review).

> [!note] Why RA hangs from URS and not from FS
> GAMP 5 §M3 step 1 places the Initial RA *"before or during requirements development"*. The RA-INIT may run in parallel with the draft URS, but its output (category + functions with impact) **precedes** and conditions the approved URS and the FS. The detailed RA (RA-DET, step 3) does use approved URS + FS.

> [!note] Severity vs Category — common error
> Severity is defined by the **business process** (what happens if the function fails in terms of PS/PQ/DI), NOT by the GAMP category. A simple Cat 3 system can have severity H if it controls a critical process. The category affects **probability**, not severity.

> [!tip] Natural output of this template
> A well-written RA-INIT produces: (1) the GAMP category that fills URS+FS; (2) the list of GxP-critical functions that focuses the validation effort; (3) the initial risk register that feeds RA-DET; (4) the decision on activation of Part 11/Annex 11 presets in the URS.

## Related

- [URS](URS.md) · [FS](FS.md) · [RA-DET](RA-DET.md) · [VP](VP.md) · [GXP-ASSESS](GXP-ASSESS.md)
- GAMP 5 · ich q9 · EU Annex 11
- quality risk management process · risk priority · quality risk management · risk register

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.ra.from-urs` skill.

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer. If it does not exist → redirect to `/gdd.init`.
2. **Locate the URS** (`specs/URS.md`) — may be draft (RA-INIT may run before URS approved, GAMP 5 §M3 step 1).
3. **Read GXP-ASSESS if it exists** — it contributes the initial GxP determination.
4. **Read `templates/csv/RA-INIT.md`** from the toolkit as the source template (this file).

### Generation flow

1. **Step 1** — guide the user through: GxP determination, system impact (PS/PQ/DI), and especially the **GAMP category determination** (present the §M4 criteria). Capture the rationale.
2. **Part 11/Annex 11 applicability** — the 5 questions in §5.4 decide which presets to activate in the URS. Propagate the result to the `preset_part11_active` placeholder in the URS.
3. **Step 2** — parse the functions from the URS; for each `URS-<CATEGORY>-NNN`, ask whether it impacts PS/PQ/DI.
4. **Initial risk register** — for each GxP-critical function, assess Severity (from the process) × Probability (from the category) → Risk Class; × Detectability → Risk Priority (use the matrices in §3.1-3.2).
5. **RA-DET decision** — apply the criteria from §8.
6. **Anti-hallucination**: insert `[NEEDS CLARIFICATION: ...]` when information is missing to assess a risk; never invent risk ratings or categories without rationale.
7. **Output**: write `specs/RA-INIT.md` (status: draft); print the determined category + list of high-risk functions + RA-DET decision.
8. **Propagation**: notify that the `gamp_category` must be propagated to `specs/URS.md` and `specs/FS.md`.
9. **Post-flight**: run `validate-frontmatter.py` + `check-clarification-markers.py`.

### Stop criteria ("complete" instance)

- [ ] `gamp_category_decision` assigned with non-empty rationale
- [ ] GxP determination + system impact (PS/PQ/DI) complete
- [ ] Part 11/Annex 11 applicability decided (5 questions §5.4)
- [ ] If gxp-relevant → functions table (Step 2) with ≥1 row
- [ ] Risk register: each GxP-critical function has Risk Class + Risk Priority
- [ ] RA-DET decision taken with justification
- [ ] Process Owner designated in signatures (owner of severity)

### `status` transitions

```
draft ──[category + functions + RA-DET decision complete]──> in-review
in-review ──[approver signatures applied]──> approved
approved ──[new version issued]──> superseded
```

> [!warning] Approval order
> RA-INIT must reach `approved` **before** the URS, because the URS inherits the `gamp_category` from here (GAMP 5 §M3 step 1).

### Downstream mapping

| Origin (RA-INIT) | Destination | Rule |
|---|---|---|
| `gamp_category_decision` | `{{gamp_category}}` in URS + FS | The category scales the depth of the cascade |
| Part 11 applicability (§5.4) | `preset_part11_active` in URS | Decides activation of URS-EREC/ESIG/SEC/API/MIGR |
| Functions with Risk Priority = H | Rows in `RA-DET.md` | The detailed RA performs FMEA on the high-risk functions |
| Risk Priority per function | Test rigor in `OQ.md` / `PQ.md` | H → negative/stress testing; M → positive; L → GEP |
| Risk-based strategy | `VP.md` | The Validation Plan takes the strategy from here |
