---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "VR — Validation Report (canonical CSV template)"
type: template
template_class: csv
template_id: "VR"
template_version: "0.1.0"
v_model_phase: reporting
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-28
updated: 2026-05-29
# Round 2 (2026-05-29): translated to English canonical (was language: es). §-citations + IDs preserved verbatim.

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# VR is the CLOSEOUT document (GAMP 5 §M7). It summarizes the entire
# validation project and issues the statement of fitness for intended use.
# It is often the first document an inspector requests.
inputs:
  - template_id: "VP"
    required: true
    description: "Validation Plan — the VR closes against its acceptance criteria"
  - template_id: "PQ"
    required: true
    description: "Performance Qualification — provides the statement of fitness for intended use"
  - template_id: "IQ"
    required: true
    description: "Installation Qualification — installation verification results"
  - template_id: "OQ"
    required: true
    description: "Operational Qualification — functional verification results"
  - template_id: "SUP-ASSESS"
    required: false
    description: "Supplier Assessment — summary for the VR (Cat 4/5)"
  - template_id: "RA-DET"
    required: false
    description: "Detailed Risk Assessment — residual risk to be summarized"
outputs:
  - artifact: "VR instance (Markdown) — Validation Report with fitness statement"
    consumed_by:
      - "audit"     # first document requested at inspection
      - "operation" # authorizes transition to operation

applicable_regulations:
  - "gamp-5"          # §M7 (Validation Reporting) pp.145-148 — statement of fitness for intended use
  - "21-cfr-part-11"  # §11.10.a validation evidence
  - "eu-annex-11"     # §9 Qualification and Validation
based_on:
  - "GAMP 5 §M7 (Validation Reporting) §15.4.1 content: intro/scope, scope changes, supplier assessment summary, activities summary, deliverables summary, deviations+CAPAs, statement of fitness for intended use, training/KM, maintaining compliance, glossary, appendices"
  - "Structure: closeout document that summarizes the project + issues the fitness statement; approvers Process Owner + QU (+ optionally System Owner)"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
  system_id:
    type: string
    required: true
  vp_ref:
    type: string
    required: true
    description: "Validation Plan against which this VR closes"
  intended_use_statement:
    type: string
    required: true
    description: "The intended use (from URS/GXP-ASSESS) whose fitness is declared"
  gamp_category:
    type: enum
    required: true
    values: [3, 4, 5]
  scope_changes:
    type: string
    required: false
    description: "Scope changes relative to the VP during the project"
  deviations_summary:
    type: string
    required: true
    description: "Summary of deviations + CAPAs + status (open/closed)"
  fitness_conclusion:
    type: enum
    required: true
    values: ["pending-execution", "fit-for-intended-use", "fit-with-conditions", "not-fit"]
    description: "KEY OUTPUT: declaration of fitness for intended use (GAMP 5 §M7). Use 'pending-execution' for a draft VR written before the IQ/OQ/PQ are executed — fitness cannot be declared until the PQ results support it."
  release_decision:
    type: enum
    required: true
    values: ["release-for-operation", "conditional-release", "not-released"]
  vr_author_name:
    type: string
    required: true
  vr_author_dept:
    type: string
    required: true
  org_csv_policy_ref:
    type: string
    required: false
  custom_ref:
    type: string
    required: false

# ─── INSTANCE frontmatter spec (not the template's) ─────────────────────────
instance_frontmatter_spec:
  required_fields:
    - title
    - type: "instance"
    - based_on_template: "VR"
    - based_on_template_version
    - system_id
    - traces_to            # VP instance
    - gamp_category
    - fitness_conclusion
    - release_decision
    - status               # draft | in-review | approved | superseded
    - version
    - created
    - updated
    - language
  conditional_fields:
    - approved_by: "required if status == approved (Process Owner + QU; optionally System Owner)"
    - supersedes
    - conditional_release_conditions: "if release_decision == conditional-release"

# ─── Validation rules (Round 1 subset) ──────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "traces_to must point to an approved VP"
  - "IQ, OQ must be approved; PQ approved if it was within the VP scope"
  - "fitness_conclusion must be supported by PQ results (statement of fitness)"
  - "All critical deviations must be closed before fitness-for-intended-use + release-for-operation"
  - "If release_decision == conditional-release → document the conditions + no-impact assessment on PS/PQ/DI (Annex 11 §9.8)"
  - "Approved by Process Owner + Quality Unit (GAMP 5 §M7); System Owner releases the system"
  - "The VR closes against the VP acceptance criteria (no new criteria may be introduced)"

tags:
  - template
  - csv
  - validation-report
  - vr
  - reporting
  - gamp-m7
  - fitness-for-intended-use
  - canonical
---

# VR — Validation Report

> [!note] Canonical CSV template — CLOSEOUT document
> **Canonical** template for the **Validation Report (VR)** — the document that **closes** the validation project, summarizes all activities, and issues the **statement of fitness for intended use** (GAMP 5 §M7 pp.145-148). It is often the **first document an inspector requests**. It closes against the [Validation Plan](VP.md) and receives the fitness conclusion from the [PQ](PQ.md).

> [!tip] Embedded usage rules
> 1. **Closes against the VP** — the VR evaluates whether the acceptance criteria defined in the [VP](VP.md) were met. No new criteria are introduced here.
> 2. **Statement of fitness** (GAMP 5 §M7) — the formal declaration of fitness for intended use is the heart of the VR. It is supported by PQ results.
> 3. **Deviations closed** — all critical deviations must be closed before declaring fit + release.
> 4. **Conditional release** — if the system is released with outstanding deficiencies, a documented no-impact assessment on PS/PQ/DI is required (Annex 11 §9.8).
> 5. **Approval** — Process Owner + Quality Unit (GAMP 5 §M7); the System Owner releases the system.
> 6. **Summaries, not duplicates** — the VR summarizes IQ/OQ/PQ/SUP-ASSESS/RA-DET; it does not copy their content.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **Validation Plan closed against** | `{{vp_ref}}` ([VP](VP.md)) |
| **GAMP category** | `{{gamp_category}}` |
| **Declared intended use** | `{{intended_use_statement}}` |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Author (CSV/SME) | `{{vr_author_name}}` | `{{vr_author_dept}}` |  |  |
| Approver 1 (Process Owner) |  |  |  |  |
| Approver 2 (Quality Unit) |  |  |  |  |
| Release (System Owner) *(releases the system)* |  |  |  |  |

---

## 1. Introduction and scope

This **Validation Report** summarizes the validation activities for system **`{{system_name}}`** executed in accordance with [Validation Plan](VP.md) `{{vp_ref}}`, and issues the declaration of fitness for intended use.

---

## 2. Scope changes relative to the VP

`{{scope_changes}}`

> Document any deviations from the planned scope in the VP (deliverables added/removed, strategy changes).

---

## 3. Supplier Assessment summary

> (If Cat 4/5) Summary of the [Supplier Assessment](SUP-ASSESS.md): decision, CAPAs, leverage applied.

| Aspect | Result |
|---|---|
| Assessment decision | |
| CAPAs closed | |
| Leveraged evidence | |

---

## 4. Validation activities summary

| Deliverable | Reference | Status | Result |
|---|---|---|---|
| [GxP Assessment](GXP-ASSESS.md) |  | approved | |
| [Initial Risk Assessment](RA-INIT.md) |  | approved | |
| [URS](URS.md) |  | approved | |
| [FS](FS.md) |  | approved | |
| [Detailed RA](RA-DET.md) |  |  | |
| [IQ](IQ.md) |  | approved | Pass / Pass w/dev |
| [OQ](OQ.md) |  | approved | Pass / Pass w/dev |
| [PQ](PQ.md) |  | approved | Fit / Fit w/cond |
| [RTM](RTM.md) |  |  | full coverage |

---

## 5. Deliverables and traceability summary

> Confirm full coverage via [RTM](RTM.md): 0 dangling references, critical GxP requirements traced through to test.

| Traceability metric (from RTM) | Value |
|---|---|
| URS requirements with GxP=Y | |
| Traced through to test | |
| Dangling references | 0 (required) |
| Critical requirements coverage | |

---

## 6. Deviations and CAPAs summary

`{{deviations_summary}}`

| Deviation | Severity | CAPA | Status | Impact on PS/PQ/DI |
|---|---|---|---|---|
|  |  |  |  |  |

> [!warning] Critical deviations
> All **critical** deviations must be **closed** before declaring fit-for-intended-use + release-for-operation.

---

## 7. Residual risk

> Summary of accepted residual risk from [RA-DET](RA-DET.md) (RPN > 4 accepted).

| RA-DET-ID | Residual RPN | Accepted by | Justification |
|---|---|---|---|

---

## 8. Statement of fitness for intended use

> [!quote] Formal declaration (GAMP 5 §M7 §15.4)
> Based on the results of the validation activities summarized in this report, system **`{{system_name}}`** is declared:
>
> **`{{fitness_conclusion}}`** for its intended use: *`{{intended_use_statement}}`*

| Conclusion | Meaning |
|---|---|
| **pending-execution** | Draft VR — IQ/OQ/PQ not yet executed; fitness not yet declarable |
| **fit-for-intended-use** | Fit without conditions |
| **fit-with-conditions** | Fit with non-critical deviations / documented conditions |
| **not-fit** | Not fit — remediation required |

---

## 9. Release decision

**Decision**: `{{release_decision}}`

| Decision | Condition |
|---|---|
| release-for-operation | Validation complete, no open critical deviations |
| conditional-release | Released with conditions + no-impact assessment on PS/PQ/DI (Annex 11 §9.8) |
| not-released | Not released |

**Conditions (if conditional)**: 

---

## 10. Training and knowledge management

> Confirm that end-user training + knowledge transfer (explicit + tacit) was completed before go-live.

---

## 11. Maintaining validated state

> Summary of the operational processes that maintain the validated state: change control, periodic review, backup/restore, security, incident/problem management.

| Operational process | Defined (✓) | SOP / reference |
|---|---|---|
| Change control |  |  |
| Periodic review |  |  |
| Backup / restore |  |  |
| Security management |  |  |
| Incident / problem management |  |  |

---

## 12. Related documents

| Document | Reference |
|---|---|
| Validation Plan | `{{vp_ref}}` ([VP](VP.md)) |
| Performance Qualification | [PQ](PQ.md) |
| Traceability Matrix | [RTM](RTM.md) |
| Supplier Assessment | [SUP-ASSESS](SUP-ASSESS.md) |
| Organization's CSV Policy | `{{org_csv_policy_ref}}` |
| `{{custom_ref}}` |  |

---

## 13. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{vr_author_name}}`, `{{vr_author_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] The VR is the first inspection document
> GAMP 5 §M7: the Validation Report is often the first document an inspector requests. It must be clear, self-contained (with references), and issue an unambiguous fitness statement.

> [!note] Summarize, do not duplicate
> The VR summarizes the results of IQ/OQ/PQ/SUP-ASSESS/RA-DET. It does not copy their content — it references the documents and distills conclusions.

> [!tip] Closes against the VP
> The acceptance criteria were defined in the VP. The VR evaluates whether they were met. Do not introduce new criteria in the VR — that would be moving the goalposts.

## Related

- [VP](VP.md) · [PQ](PQ.md) · [IQ](IQ.md) · [OQ](OQ.md) · [RTM](RTM.md) · [SUP-ASSESS](SUP-ASSESS.md)
- GAMP 5 · 21 CFR Part 11 · EU Annex 11
- V-Model · validation report

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the orchestrating skill (`gdd.lifecycle`).

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer.
2. **Confirm approved**: VP, IQ, OQ, PQ (if within scope). If any is missing → the VR cannot be closed.
3. **Read SUP-ASSESS + RA-DET if they exist** — summaries.
4. **Run generate-rtm.py** — confirm 0 dangling references + coverage.
5. **Read `templates/csv/VR.md`** from the toolkit as the source template (this file).

### Generation flow

1. **Summarize activities** (§4): status of each deliverable.
2. **Summarize traceability** (§5) from the RTM.
3. **Summarize deviations** (§6) — confirm critical ones are closed.
4. **Summarize residual risk** (§7) from RA-DET.
5. **Issue fitness statement** (§8) supported by PQ.
6. **Release decision** (§9).
7. **Anti-hallucination**: `[NEEDS CLARIFICATION: ...]` when information is missing; never declare fit without PQ evidence or close deviations without a CAPA.
8. **Output**: write `specs/VR.md` (status: draft).
9. **Post-flight**: `validate-frontmatter.py` + `check-clarification-markers.py`.

### `status` transitions

```
draft ──[summaries complete + fitness statement + critical deviations closed]──> in-review
in-review ──[Process Owner + QU sign; System Owner releases]──> approved
approved ──[new version / re-validation]──> superseded
```

> [!warning] Do not declare fit without PQ
> The fitness statement must be supported by actual PQ results. Declaring fit-for-intended-use without an approved PQ is a validation gap.

### Mapping

| Origin (VR) | Destination | Rule |
|---|---|---|
| fitness_conclusion | operation | Authorizes (or not) transition to production |
| release_decision | System Owner | The System Owner executes the release |
| VR approved | project closeout | End of the project phase; start of operation |
