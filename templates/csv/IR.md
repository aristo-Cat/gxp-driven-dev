---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "IR — Incident Report (canonical CSV template)"
type: template
template_class: csv
template_id: "IR"
template_version: "0.1.0"
v_model_phase: operation
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# IR is an OPERATION-phase document (GAMP 5 §O4 Incident/Problem Management).
# It records a GxP incident or deviation affecting the computerized system,
# assesses impact on patient safety / product quality / data integrity,
# captures containment actions, root-cause analysis, and CAPA.
# It feeds the Periodic Review and may raise a Change Control for
# corrective modifications to the system.
inputs:
  - artifact: "Operating computerized system (the system that experienced the incident)"
    required: true
    description: "The validated, running system that is the subject of the incident"
outputs:
  - artifact: "IR instance (Markdown) — closed Incident Report"
    consumed_by:
      - template_id: "PR"
        description: "Periodic Review — aggregates all IRs in the review period"
      - "audit"                # GxP inspectors will request open + closed IRs
  - artifact: "CC trigger (optional)"
    consumed_by:
      - template_id: "CC"
        description: "Change Control — raised when CAPA requires a modification to the system"

applicable_regulations:
  - "gamp-5"          # §O4 Incident/Problem Management — detection, classification, investigation, CAPA
  - "eu-annex-11"     # §13 Incident Management — reporting, investigation, corrective actions
  - "21-cfr-part-11"  # §11.10(k) audit trails — supports investigation of record-affecting incidents

based_on:
  - "GAMP 5 §O4 (Incident/Problem Management): detection, classification, containment, root-cause analysis, CAPA, closure, trending"
  - "EU Annex 11 §13 (Incident Management): all incidents reported and investigated; corrective and preventive actions taken; deviations from normal operation must not be ignored"
  - "Structure: incident lifecycle document — Reporter + System Owner + QU; impact table (PS/PQ/DI); root-cause analysis; CAPA with owner/due date/status; data-integrity assessment; closure"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
  system_id:
    type: string
    required: true
  incident_id:
    type: string
    required: true
    description: "IR identifier following the scheme IR-YYYY-NNN (e.g. IR-2026-001)"
  incident_date:
    type: string
    required: true
    description: "Date and time the incident occurred (DD.MM.YYYY HH:MM)"
  detection_date:
    type: string
    required: true
    description: "Date and time the incident was detected (DD.MM.YYYY HH:MM)"
  detected_by:
    type: string
    required: true
    description: "Name and role of the person who detected the incident"
  incident_description:
    type: string
    required: true
    description: "Factual description of what happened — what was observed, what failed"
  incident_severity:
    type: enum
    required: true
    values: ["critical", "major", "minor"]
    description: "Severity classification. Critical = potential impact on PS; Major = potential impact on PQ/DI; Minor = no direct GxP impact"
  ps_impact:
    type: enum
    required: true
    values: ["H", "M", "L", "N/A"]
    description: "Impact on Patient Safety"
  pq_impact:
    type: enum
    required: true
    values: ["H", "M", "L", "N/A"]
    description: "Impact on Product Quality"
  di_impact:
    type: enum
    required: true
    values: ["H", "M", "L", "N/A"]
    description: "Impact on Data Integrity"
  impact_justification:
    type: string
    required: true
    description: "Narrative justification for the PS/PQ/DI ratings above"
  containment_actions:
    type: string
    required: true
    description: "Immediate actions taken to contain the incident and limit further impact"
  root_cause:
    type: string
    required: true
    description: "Root cause(s) identified through investigation (required for critical/major; documented as N/A for minor with justification)"
  capa_summary:
    type: string
    required: true
    description: "Summary of corrective and preventive actions — individual CAPA rows in body §7"
  di_assessment:
    type: enum
    required: true
    values: ["records-unaffected", "records-affected-remediated", "records-affected-under-investigation", "N/A"]
    description: "Overall data-integrity impact conclusion"
  reporter_name:
    type: string
    required: true
  reporter_dept:
    type: string
    required: true
  cc_raised:
    type: boolean
    required: true
    description: "Was a Change Control raised as a result of CAPA?"
  cc_ref:
    type: string
    required: false
    description: "CC identifier if cc_raised == true (e.g. CC-2026-007)"
  org_csv_policy_ref:
    type: string
    required: false
    description: "Reference to the organization's CSV / GxP incident management SOP"
  custom_ref:
    type: string
    required: false

# ─── INSTANCE frontmatter spec (not the template's) ─────────────────────────
instance_frontmatter_spec:
  required_fields:
    - title
    - type: "instance"
    - based_on_template: "IR"
    - based_on_template_version
    - system_id
    - incident_id
    - incident_severity
    - di_assessment
    - status               # open | under-investigation | capa-in-progress | closed | cancelled
    - version
    - created
    - updated
    - language
  optional_fields:
    - traces_to            # the system (system_id or wikilink to system spec)
    - cc_ref               # if a CC was raised

# ─── Validation rules ────────────────────────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "Impact on PS, PQ, and DI must each be assessed with a written justification"
  - "Root cause must be documented for critical and major incidents; minor incidents require justification for 'N/A'"
  - "At least one CAPA must be present for critical and major incidents"
  - "Each CAPA row must have an owner, a due date, and a status"
  - "Data-integrity assessment must be completed — any affected records require remediation or documented investigation"
  - "If cc_raised == true, cc_ref must be populated and the CC document must exist"
  - "Signed by Reporter, System Owner, and Quality Unit before closure"
  - "status == closed requires all CAPAs to be completed or formally accepted with documented risk"

tags:
  - template
  - csv
  - incident-report
  - ir
  - operation
  - gamp-o4
  - incident-management
  - capa
  - data-integrity
  - canonical
---

# IR — Incident Report

> [!note] Canonical CSV template — OPERATION-phase document
> **Canonical** template for the **Incident Report (IR)** — the document that records a GxP incident or deviation affecting the computerized system, assesses its impact on patient safety, product quality, and data integrity, captures containment actions and root-cause analysis, and drives CAPA to closure (GAMP 5 §O4; EU Annex 11 §13). Closed IRs feed the [Periodic Review](PR.md) and may trigger a [Change Control](CC.md) for corrective system modifications.

> [!tip] Embedded usage rules
> 1. **Detection is mandatory** — EU Annex 11 §13: all incidents must be reported and investigated. Deviations from normal operation must not be ignored.
> 2. **Impact trinity** — every IR must assess impact on Patient Safety (PS), Product Quality (PQ), and Data Integrity (DI), each independently rated H / M / L / N/A with written justification.
> 3. **Root cause required** for critical and major incidents. For minor incidents, document rationale for waiving root-cause analysis.
> 4. **CAPA completeness** — every CAPA row needs an owner, a due date, and a tracked status. Critical/major incidents must have at least one CAPA.
> 5. **Data integrity check** — if any electronic records were affected, those records must be remediated or the investigation explicitly documented; the conclusion is mandatory.
> 6. **CC linkage** — if a CAPA requires a modification to the validated system (configuration, code, infrastructure), raise a [Change Control](CC.md) and record the reference here.
> 7. **Approval chain** — Reporter → System Owner → Quality Unit. All three signatures required before closure.

---

## 0. Identification and signatures

### Incident and system

| Field | Value |
|---|---|
| **Incident identifier** | `{{incident_id}}` |
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **Date / time of incident** | `{{incident_date}}` |
| **Date / time detected** | `{{detection_date}}` |
| **Detected by** | `{{detected_by}}` |
| **Severity** | `{{incident_severity}}` |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Reporter (SME/Reporter) | `{{reporter_name}}` | `{{reporter_dept}}` |  |  |
| Reviewer (System Owner) |  |  |  |  |
| Approver (Quality Unit) |  |  |  |  |

---

## 1. Incident description

`{{incident_description}}`

> Describe factually what was observed — what failed, what behaved unexpectedly, what was not as intended. Include system state, user actions, error messages, log references, and time sequence. Avoid conclusions here; this is the factual account.

---

## 2. Impact assessment

> [!note] EU Annex 11 §13 / GAMP 5 §O4
> Each dimension must be assessed independently. **H** = High (direct or likely impact), **M** = Medium (potential impact, mitigated by controls), **L** = Low (minimal or negligible impact), **N/A** = Not applicable (with documented rationale).

| Dimension | Rating | Justification |
|---|---|---|
| **Patient Safety (PS)** | `{{ps_impact}}` | `{{impact_justification}}` |
| **Product Quality (PQ)** | `{{pq_impact}}` | |
| **Data Integrity (DI)** | `{{di_impact}}` | |

> [!warning] High PS or PQ rating
> Any **H** rating on PS or PQ escalates this incident to **critical** severity and may require immediate escalation to senior management and the Quality Unit. Regulatory reporting obligations may apply (e.g., deviation to competent authorities).

---

## 3. Immediate containment actions

`{{containment_actions}}`

| Action | Owner | Completed (date) |
|---|---|---|
|  |  |  |
|  |  |  |

> Document every action taken immediately to stop the incident, limit further damage, protect affected records, or restore the system to a safe state. Include system lockout, user notification, data quarantine, or interim process substitution if applicable.

---

## 4. Root-cause analysis

`{{root_cause}}`

> [!note] GAMP 5 §O4 — Investigation
> For **critical** and **major** incidents, a structured root-cause analysis is mandatory. Use a recognized technique (e.g., 5-Why, Ishikawa/fishbone, fault-tree). For **minor** incidents, document the rationale for limiting investigation scope.

### Root cause category

| Category | Applicable? | Notes |
|---|---|---|
| Software defect |  |  |
| Configuration error |  |  |
| Infrastructure / environment failure |  |  |
| Procedural / human error |  |  |
| Training gap |  |  |
| Supplier / vendor issue |  |  |
| Specification gap |  |  |
| Other |  |  |

---

## 5. Data-integrity assessment

> [!note] 21 CFR Part 11 §11.10(k) / EU Annex 11 §13
> If any electronic records were created, modified, or deleted abnormally during the incident, each affected record type must be assessed. Identify whether the record can be trusted, reconstructed from audit trail, or must be invalidated.

**Overall DI conclusion:** `{{di_assessment}}`

| Record type / ID | Affected? | Audit trail intact? | Remediation action | Status |
|---|---|---|---|---|
|  |  |  |  |  |
|  |  |  |  |  |

> [!warning] Affected records
> Any electronic records with `di_assessment` = **records-affected-remediated** or **records-affected-under-investigation** must be traceable to a documented remediation or formal risk acceptance. Closure of the IR is blocked until this is resolved.

---

## 6. Timeline

| Date / Time | Event |
|---|---|
| `{{incident_date}}` | Incident occurs |
| `{{detection_date}}` | Incident detected by `{{detected_by}}` |
|  | Containment action initiated |
|  | Root-cause investigation opened |
|  | Root cause confirmed |
|  | CAPA defined |
|  | IR closed |

---

## 7. Corrective and Preventive Actions (CAPA)

`{{capa_summary}}`

> [!note] GAMP 5 §O4 — CAPA
> Each CAPA row must have a unique reference, a clear action description, a responsible owner, a due date, and a tracked status. For **critical** and **major** incidents, at least one CAPA is required. If a CAPA requires a system modification, raise a [Change Control](CC.md).

| CAPA-ID | Type | Description | Owner | Due date | Status | CC ref (if applicable) |
|---|---|---|---|---|---|---|
| IR-`{{incident_id}}`-CAPA-001 | Corrective |  |  | DD.MM.YYYY | open |  |
| IR-`{{incident_id}}`-CAPA-002 | Preventive |  |  | DD.MM.YYYY | open |  |

**Change Control raised:** `{{cc_raised}}` — Reference: `{{cc_ref}}`

---

## 8. Recurrence and trending

> [!note] GAMP 5 §O4 — Trending
> Check whether a similar incident has been recorded previously for this system. The [Periodic Review](PR.md) aggregates incident trends across the review period. Flag recurring incidents for enhanced root-cause analysis.

| Question | Response |
|---|---|
| Previous incident of same type on this system? | |
| Incident-ID of prior occurrence(s) | |
| Trend identified? (escalate to PR) | |

---

## 9. Related documents

| Document | Reference |
|---|---|
| System specification | `{{system_id}}` |
| Change Control (if raised) | `{{cc_ref}}` ([CC](CC.md)) |
| Periodic Review | [PR](PR.md) |
| Organization's GxP incident management SOP | `{{org_csv_policy_ref}}` |
| `{{custom_ref}}` |  |

---

## 10. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{reporter_name}}`, `{{reporter_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] Every incident is an opportunity
> GAMP 5 §O4: incident management is not bureaucratic overhead — it is the primary feedback mechanism for maintaining the validated state. A well-investigated IR prevents recurrence and strengthens the system's compliance posture.

> [!note] Severity classification drives response time
> Define classification criteria in the organization's GxP incident management SOP:
> - **Critical** — immediate response; Quality Unit notified within hours; potential regulatory notification.
> - **Major** — response within 1–3 business days; Quality Unit notified.
> - **Minor** — response within the normal change/review cycle.

> [!tip] Impact on PS vs. PQ vs. DI are independent
> An incident can have low PS impact but high DI impact (e.g., audit trail gap with no batch impact). Assess all three dimensions separately.

> [!warning] Do not close without CAPA verification
> Closing an IR with open CAPAs is a finding risk. If a CAPA cannot be completed by the due date, document the extension rationale and obtain Quality Unit acceptance before proceeding.

## Related

- [PR](PR.md) · [CC](CC.md) · [VR](VR.md)
- GAMP 5 · EU Annex 11 · 21 CFR Part 11
- data integrity · capa · audit trail

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the orchestrating skill (`gdd.lifecycle`).

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer project.
2. **Identify the affected system** — locate the system's `system_id` and confirm the system has an approved VR (validated state established).
3. **Determine severity** — apply the classification criteria from the organization's SOP or default to: Critical (PS impact H), Major (PQ/DI impact H), Minor (no direct GxP impact).
4. **Read `templates/csv/IR.md`** from the toolkit as the source template (this file).

### Generation flow

1. **Populate §0** — incident ID (follow IR-YYYY-NNN scheme from `docs/requirement-id-scheme.md`), system fields, reporter.
2. **Capture incident description** (§1) — factual, time-ordered, no conclusions.
3. **Complete impact table** (§2) — all three dimensions (PS / PQ / DI) with written justification; never leave impact cells blank.
4. **Document containment** (§3) — list every immediate action with owner + completion date.
5. **Root-cause analysis** (§4) — for critical/major: structured investigation + category table; for minor: brief justification.
6. **Data-integrity assessment** (§5) — for every affected record type: audit trail check + remediation action; set overall `di_assessment` conclusion.
7. **Timeline** (§6) — fill in all known dates.
8. **CAPA table** (§7) — at least one row for critical/major; set `cc_raised` and `cc_ref` if a system modification is needed.
9. **Trending** (§8) — check prior IRs for the same system and flag recurrence.
10. **Anti-hallucination**: use `[NEEDS CLARIFICATION: ...]` when information is genuinely missing; never assess DI as "records-unaffected" without audit-trail evidence.
11. **Output**: write `specs/IR-YYYY-NNN.md` (status: open).
12. **Post-flight**: `validate-frontmatter.py` + `check-clarification-markers.py`.

### `status` transitions

```
open ──[investigation started]──> under-investigation
under-investigation ──[root cause confirmed + CAPA defined]──> capa-in-progress
capa-in-progress ──[all CAPAs completed + DI resolved + signatures obtained]──> closed
open | under-investigation | capa-in-progress ──[duplicate / erroneous report]──> cancelled
```

> [!warning] Closure gate
> An IR cannot transition to **closed** unless: (1) impact on PS/PQ/DI is assessed, (2) root cause is documented (critical/major), (3) all CAPAs are complete or formally accepted, (4) data-integrity findings are resolved, and (5) all three signatures are obtained.

### Mapping

| Origin (IR) | Destination | Rule |
|---|---|---|
| `cc_raised == true` | CC | Raise a new CC instance; link via `cc_ref` |
| IR closed | PR | All closed IRs in the review period appear in the [PR](PR.md) summary table |
| High PS impact | Regulatory / management | Escalation may be required per applicable SOP |
| Recurring incidents | PR trending | Flag in the Periodic Review for pattern analysis |
