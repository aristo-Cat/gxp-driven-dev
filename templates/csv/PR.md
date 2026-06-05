---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "PR — Periodic Review (canonical CSV template)"
type: template
template_class: csv
template_id: "PR"
template_version: "0.1.0"
v_model_phase: operation
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# PR is the OPERATION document that confirms a validated system remains in a
# validated state (GAMP 5 §O8 Periodic Review). It reviews changes, deviations,
# CAPA status, audit trail, access, backups, training, and supplier standing
# since the last review period, then issues a conclusion.
inputs:
  - template_id: "VR"
    required: true
    description: "Validation Report — proof that the system was initially validated"
  - template_id: "CC"
    required: false
    description: "Change Control Records since the last review (if any changes occurred)"
  - template_id: "IR"
    required: false
    description: "Incident / Problem Records since the last review (if any incidents occurred)"
outputs:
  - artifact: "PR instance (Markdown) — Periodic Review with validation-status conclusion"
    consumed_by:
      - "operation"  # drives next review cycle or revalidation
      - "audit"      # regulators may request periodic review evidence

applicable_regulations:
  - "gamp-5"      # §O8 (Periodic Review) — assessing ongoing fitness for intended use
  - "eu-annex-11" # §11 (Periodic Evaluation) — regularity of evaluation for continued compliance

based_on:
  - "GAMP 5 §O8 Periodic Review: purpose, frequency, review areas (changes, deviations, audit trail, access, backup, training, supplier), conclusion and escalation"
  - "EU Annex 11 §11 Periodic Evaluation: GxP-critical computerized systems shall be evaluated periodically; include assessments of changes, deviations, incidents, access controls, and audit trails"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
  system_id:
    type: string
    required: true
  vr_ref:
    type: string
    required: true
    description: "Reference to the Validation Report that authorized this system for operation"
  review_period_start:
    type: string
    required: true
    description: "Start of the review period (ISO 8601 date, YYYY-MM-DD)"
  review_period_end:
    type: string
    required: true
    description: "End of the review period (ISO 8601 date, YYYY-MM-DD)"
  review_frequency:
    type: enum
    required: true
    values: ["annual", "biennial", "triennial", "risk-based"]
    description: "Frequency of periodic review as defined in the Validation Plan or SOPs"
  gamp_category:
    type: enum
    required: true
    values: [3, 4, 5]
  pr_author_name:
    type: string
    required: true
  pr_author_dept:
    type: string
    required: true
  previous_pr_ref:
    type: string
    required: false
    description: "Reference to the previous Periodic Review (if this is not the first)"
  review_conclusion:
    type: enum
    required: true
    values:
      - "validation-still-valid"
      - "actions-required"
      - "revalidation-triggered"
    description: "KEY OUTPUT: overall conclusion on the current validated state"
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
    - based_on_template: "PR"
    - based_on_template_version
    - system_id
    - traces_to   # VR instance
    - status      # draft | in-review | approved | superseded
    - version
    - created
    - updated
    - language
  conditional_fields:
    - approved_by: "required if status == approved (System Owner + Quality Unit)"
    - supersedes: "reference to the previous PR if this is a subsequent review"
    - revalidation_plan_ref: "required if review_conclusion == revalidation-triggered"
    - actions_list: "required if review_conclusion == actions-required"

# ─── Validation rules (Round 1 subset) ──────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "traces_to must point to an approved VR"
  - "All seven review areas (changes / deviations+CAPA / audit trail / access / backup-restore / training / supplier status) must be marked reviewed (✓) with findings documented"
  - "review_conclusion must be one of: validation-still-valid / actions-required / revalidation-triggered"
  - "Any critical finding must have an assigned owner, target date, and CAPA reference"
  - "If review_conclusion == revalidation-triggered → revalidation_plan_ref must be populated or a [NEEDS CLARIFICATION] marker placed"
  - "Approved by System Owner + Quality Unit (GAMP 5 §O8)"
  - "Review period must not exceed the frequency defined in the Validation Plan or organizational CSV policy"

tags:
  - template
  - csv
  - periodic-review
  - pr
  - operation
  - gamp-o8
  - eu-annex-11-11
  - validated-state
  - canonical
---

# PR — Periodic Review

> [!note] Canonical CSV template — OPERATION document
> **Canonical** template for the **Periodic Review (PR)** — the operational document that confirms a validated computerized system **remains in a validated state** (GAMP 5 §O8). Scheduled at a defined frequency (typically annual for GxP-critical systems), it reviews all relevant changes, deviations, incidents, audit trails, access rights, backup/restore, training records, and supplier standing since the last review period. The review concludes with one of three outcomes: validation still valid · actions required · revalidation triggered (EU Annex 11 §11).

> [!tip] Embedded usage rules
> 1. **GAMP 5 §O8 scope** — the review covers all significant changes, deviations/incidents and CAPA status, audit-trail integrity, user access, backup/restore verification, training currency, and supplier/support standing.
> 2. **EU Annex 11 §11** — GxP-critical computerized systems shall be periodically evaluated to confirm they remain in a valid state and that GxP, data integrity, and security controls are still effective.
> 3. **Conclusion is mandatory** — every PR must close with one of the three enumerated conclusions. An inconclusive or silent PR is not compliant.
> 4. **Critical findings escalate** — any critical finding must trigger a CAPA with an owner and target date before the review can be approved.
> 5. **Revalidation trigger** — if revalidation is triggered, a plan or reference must be documented in the same instance.
> 6. **Approval** — System Owner + Quality Unit (GAMP 5 §O8). The System Owner owns the operational state; the Quality Unit ensures regulatory adequacy.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **Validation Report (initial)** | `{{vr_ref}}` ([VR](VR.md)) |
| **GAMP category** | `{{gamp_category}}` |
| **Review period** | `{{review_period_start}}` to `{{review_period_end}}` |
| **Review frequency** | `{{review_frequency}}` |
| **Previous Periodic Review** | `{{previous_pr_ref}}` *(omit if first review)* |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Author (CSV/SME) | `{{pr_author_name}}` | `{{pr_author_dept}}` |  |  |
| Approver 1 (System Owner) |  |  |  |  |
| Approver 2 (Quality Unit) |  |  |  |  |

---

## 1. Purpose and regulatory basis

This **Periodic Review** evaluates whether system **`{{system_name}}`** continues to operate in a validated state following the review period **`{{review_period_start}}`** to **`{{review_period_end}}`**.

Regulatory basis:

- **GAMP 5 §O8** — Periodic Review: organizations shall establish a process to periodically assess the continued suitability and fitness for intended use of validated computerized systems, reviewing changes, incidents, deviations, audit trails, access controls, backup/restore, and supplier status.
- **EU Annex 11 §11** — Periodic Evaluation: computerized systems should be periodically evaluated to confirm that they remain in a valid state and comply with GxP requirements; the evaluation shall cover the system functionality, deviations, incidents, problems, change history, and upgrade/update procedures.

---

## 2. Scope of this review

> Describe the boundaries of this review: which modules, interfaces, or sub-systems are in scope; any explicit exclusions with justification.

| In scope | Out of scope / justification |
|---|---|
|  |  |

---

## 3. Review areas

> For each area: mark **Reviewed ✓** once evidence has been examined; record findings; assign actions where required.

### 3.1 Changes since last review

> Review all [Change Control Records](CC.md) executed since the last review. Confirm each change was properly controlled and re-qualified if required.

| Finding | Reviewed ✓ |
|---|---|
| Number of CC records in period | |
| All changes processed under change control | |
| Re-qualification performed where required | |

| CC reference | Summary | Impact on validated state | Actions |
|---|---|---|---|
|  |  |  |  |

> [!warning] Uncontrolled changes
> Any change applied to the system outside of a documented change control process is a critical finding and must trigger a CAPA before this review can be approved.

---

### 3.2 Deviations, incidents, and CAPA status

> Review all [Incident / Problem Records](IR.md) and deviations raised since the last review. Confirm CAPA closure.

| Finding | Reviewed ✓ |
|---|---|
| Number of IR records in period | |
| Number of open CAPAs from previous review | |
| Open CAPAs closed in this period | |
| Remaining open CAPAs | |

| IR / CAPA reference | Severity | Description | Status | Target date |
|---|---|---|---|---|
|  |  |  |  |  |

> [!warning] Open critical CAPAs
> Any **critical** open CAPA must be resolved or a justified risk-acceptance documented before the review can conclude **validation-still-valid**.

---

### 3.3 Audit trail review

> Confirm the audit trail is intact, has not been modified, and is complete for the review period (EU Annex 11 §11; GAMP 5 §O8).

| Finding | Reviewed ✓ |
|---|---|
| Audit trail enabled continuously through the period | |
| No evidence of gaps, deletions, or unauthorized modifications | |
| Audit trail retention meets regulatory requirements | |
| Sample of records reviewed for completeness and attributability | |

**Observations:**

> *(Document any anomalies, gaps, or concerns found during the audit-trail review. If none, state "No anomalies found.")*

---

### 3.4 Access review

> Review current user access rights: confirm that all active accounts are authorized, that roles are appropriate, and that leavers have been de-provisioned (EU Annex 11 §12; GAMP 5 §O8).

| Finding | Reviewed ✓ |
|---|---|
| Active accounts reviewed against current staff list | |
| Departed users de-provisioned | |
| Role assignments remain appropriate | |
| Shared / generic accounts justified and controlled | |
| Administrative access restricted to authorized personnel | |

**Observations:**

> *(Document any unauthorized accounts, orphaned accounts, or role mismatches. If none, state "No issues found.")*

---

### 3.5 Backup and restore verification

> Confirm that scheduled backups completed successfully and that restore capability was tested at least once in the review period (GAMP 5 §O8; EU Annex 11 §10).

| Finding | Reviewed ✓ |
|---|---|
| Scheduled backups completed without critical failure | |
| Restore test performed within the review period | |
| Recovery Time Objective (RTO) / Recovery Point Objective (RPO) verified | |
| Backup media / storage integrity confirmed | |

**Observations:**

---

### 3.6 Training records

> Confirm that all personnel operating or maintaining the system have current, documented training (GAMP 5 §O8; EU Annex 11 §2).

| Finding | Reviewed ✓ |
|---|---|
| Training records up to date for all active users | |
| New personnel trained before access granted | |
| Re-training completed following significant changes | |

**Observations:**

---

### 3.7 Supplier and support status

> Review the supplier's support status, SLA adherence, security disclosures, and any patches or updates issued in the period (GAMP 5 §O8; EU Annex 11 §3).

| Finding | Reviewed ✓ |
|---|---|
| Supplier still providing active support (no end-of-life announcement) | |
| Patches / updates reviewed and assessed for impact | |
| Security advisories reviewed; critical patches applied or risk-accepted | |
| SLA or support contract current | |

**Observations:**

---

## 4. Summary of findings and actions

> Consolidate all open findings and required actions from §3. Each action must have an owner, target date, and severity.

| Action ID | Review area | Finding description | Severity | Owner | Target date | CAPA ref |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

> [!note] Severity definitions
> **Critical** — potential direct impact on data integrity, patient safety, or regulatory compliance. Must be resolved before approving **validation-still-valid**.
> **Major** — significant process or control gap without immediate safety impact. Must have a CAPA with a committed date.
> **Minor** — low-risk observation; corrective action recommended but does not block approval.

---

## 5. Conclusion

> [!quote] Formal conclusion (GAMP 5 §O8 / EU Annex 11 §11)
> Based on the review activities summarized in this report, the validated state of system **`{{system_name}}`** for the period **`{{review_period_start}}`** to **`{{review_period_end}}`** is concluded as:
>
> **`{{review_conclusion}}`**

| Conclusion | Meaning |
|---|---|
| **validation-still-valid** | All review areas satisfactory; no critical open findings; system continues to operate in its validated state |
| **actions-required** | One or more major findings identified; system remains in use but CAPAs must be closed by the dates in §4 |
| **revalidation-triggered** | Scope, function, technology, or risk profile has changed sufficiently that a new validation cycle (partial or full) is required |

**Narrative justification:**

> *(Provide 2–5 sentences supporting the conclusion above. Reference the key findings or the absence of findings.)*

**Next review due:** *(date, calculated from review_period_end + review_frequency)*

---

## 6. Revalidation plan (if triggered)

> Complete this section **only** if `review_conclusion == revalidation-triggered`. Otherwise mark "N/A".

| Field | Value |
|---|---|
| Revalidation scope | |
| Revalidation plan reference | `[NEEDS CLARIFICATION: insert revalidation plan ref]` |
| Target completion date | |
| Responsible owner | |

---

## 7. Related documents

| Document | Reference |
|---|---|
| Validation Report | `{{vr_ref}}` ([VR](VR.md)) |
| Previous Periodic Review | `{{previous_pr_ref}}` *(if applicable)* |
| Change Control Records | [CC](CC.md) |
| Incident / Problem Records | [IR](IR.md) |
| User Access Review | UAR |
| Backup / Recovery Record | BRR |
| Organization's CSV Policy | `{{org_csv_policy_ref}}` |
| `{{custom_ref}}` |  |

---

## 8. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{pr_author_name}}`, `{{pr_author_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] Frequency is risk-based
> GAMP 5 §O8 does not mandate a fixed interval — it requires a frequency appropriate to the risk profile of the system and its GxP impact. Annual review is conventional for GxP-critical systems (Category 4/5); lower-risk systems (Category 3) may use biennial or triennial cycles with documented justification.

> [!note] The review is documentary evidence, not a re-qualification
> The Periodic Review is a structured document review, not a re-execution of IQ/OQ/PQ test cases. It confirms that the controls established at initial validation are still in place and effective. If those controls have changed materially, revalidation may be required.

> [!tip] Audit trail review scope
> A full audit trail review of every transaction is rarely practical. A **risk-based sample** (e.g., date-range or event-type filter) is acceptable provided the sampling rationale is documented. Focus on GxP-critical transactions: data creation, modification, deletion, and system configuration changes.

> [!warning] Silence is a finding
> A Periodic Review that finds nothing across all seven areas for a complex production system is itself a red flag at inspection. Document what was examined (evidence source, sample size, date range) so the reviewer's work is visible and traceable.

## Related

- [VR](VR.md) · [CC](CC.md) · [IR](IR.md) · UAR · BRR
- GAMP 5 · EU Annex 11
- periodic review · validated state · change control

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the orchestrating skill (`gdd.lifecycle`).

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer.
2. **Confirm approved VR exists** for the system. If no VR → the system is not in a validated state and a PR cannot be issued; escalate.
3. **Collect CC records** since the last review period end date (or since VR approval date if this is the first review).
4. **Collect IR records** for the same period.
5. **Determine review_frequency** from the VR or VP (default: annual for Cat 4/5; biennial for Cat 3 if risk-justified).
6. **Read `templates/csv/PR.md`** from the toolkit as the source template (this file).

### Generation flow

1. **Populate identification** (§0): system identity, review period, previous PR ref.
2. **Review area §3.1 — Changes**: read all CC records; populate table; flag uncontrolled changes.
3. **Review area §3.2 — Deviations/CAPA**: read all IR records; confirm CAPA status.
4. **Review area §3.3 — Audit trail**: confirm audit trail continuity; sample review; document observations.
5. **Review area §3.4 — Access**: compare current user list to staff roster; flag orphaned or unauthorized accounts.
6. **Review area §3.5 — Backup/restore**: check backup logs; confirm restore test was performed.
7. **Review area §3.6 — Training**: check training records for all active users.
8. **Review area §3.7 — Supplier status**: check supplier SLA, patch status, end-of-life advisories.
9. **Summarize findings** (§4): consolidate all findings with severity + owner + target date.
10. **Issue conclusion** (§5) supported by §3 findings: validation-still-valid / actions-required / revalidation-triggered.
11. **Anti-hallucination**: use `[NEEDS CLARIFICATION: ...]` for missing evidence; never conclude **validation-still-valid** without reviewing all seven areas; never leave critical findings without a CAPA.
12. **Output**: write `specs/PR-YYYY-MM-DD.md` (status: draft, where date = review_period_end).
13. **Post-flight**: `validate-frontmatter.py` + `check-clarification-markers.py`.

### `status` transitions

```
draft ──[all review areas completed + conclusion issued]──> in-review
in-review ──[System Owner + QU sign]──> approved
approved ──[next review cycle]──> superseded
```

> [!warning] Do not conclude without reviewing all seven areas
> A conclusion of validation-still-valid issued without evidence from all seven review areas is a regulatory finding. Each area must be marked Reviewed ✓ with documented observations before the conclusion section can be completed.

### Mapping

| Origin (PR) | Destination | Rule |
|---|---|---|
| review_conclusion = validation-still-valid | operation | Confirms continued authorized use; schedules next review |
| review_conclusion = actions-required | CAPA tracker | Opens formal CAPAs with owners + dates; system continues in use |
| review_conclusion = revalidation-triggered | VP (new) | Initiates a new validation project; scope defined by the findings |
| PR approved | audit trail | Evidence of periodic evaluation per EU Annex 11 §11 |
