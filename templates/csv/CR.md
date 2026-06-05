---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "CR — Change Request (project-phase, canonical CSV template)"
type: template
template_class: csv
template_id: "CR"
template_version: "0.1.0"
v_model_phase: project
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-28
updated: 2026-05-29
# Round 2 (2026-05-29): translated to English canonical (was language: es). Section-citations + IDs preserved verbatim.

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# CR = Change Request: a change raised DURING the validation project (project-
# phase, GAMP 5 §M8, lighter process). Operational-phase changes to a validated
# system use CC (Change Control, §O6) — see templates/csv/CC.md.
# A project-phase change may trigger partial re-validation (re-execute IQ/OQ/PQ).
inputs:
  - template_id: "RA-INIT"
    required: false
    description: "Risk Assessment — change impact is evaluated using PS/PQ/DI risk criteria"
outputs:
  - artifact: "CR instance (Markdown) — change control record"
    consumed_by:
      - "IQ"        # changes may require re-executing installation verification
      - "OQ"        # functional re-test of the change impact
      - "PQ"        # fitness re-test if the change affects the intended use
      - "VR"        # documented re-validation / addendum to the VR
applicable_regulations:
  - "gamp-5"          # §M8 (Project Change & Configuration Management) — project-phase change
  - "eu-annex-11"     # §10 Change management
  - "21-cfr-part-11"  # change control for records/system
based_on:
  - "GAMP 5 §M8 (Project Change & Configuration Management): project-phase change request — Request → Impact/Risk Assessment → Plan → Backout → Authorize → Execute → Release, lighter than the operational §O6 regime"
  - "Structure: change request record with risk-based impact assessment; determines re-validation scope; backout plan; change types"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
  system_id:
    type: string
    required: true
  change_phase:
    type: enum
    required: true
    values: ["project"]
    description: "project (GAMP 5 §M8, pre-go-live, lighter). Operational-phase changes to a validated system use CC (Change Control, §O6)."
  change_type:
    type: enum
    required: true
    values: ["standard-routine", "like-for-like", "sys-admin", "emergency", "temporary", "global"]
    description: "Change type (GAMP 5 §O6)"
  change_description:
    type: string
    required: true
  change_reason:
    type: string
    required: true
  requestor_name:
    type: string
    required: true
  gxp_impact:
    type: enum
    required: true
    values: ["high", "medium", "low", "none"]
    description: "Change impact on PS/PQ/DI"
  revalidation_scope:
    type: string
    required: true
    description: "Required re-validation scope (which IQ/OQ/PQ to re-execute, or none)"
  org_change_policy_ref:
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
    - based_on_template: "CR"
    - based_on_template_version
    - system_id
    - change_phase
    - change_type
    - gxp_impact
    - status               # requested | assessed | authorized | in-progress | implemented | closed | rejected
    - version
    - created
    - updated
    - language
  conditional_fields:
    - authorized_by: "required if status >= authorized"
    - backout_executed: "true if the backout plan was executed"
    - emergency_retrospective: "true if it was an emergency change with retrospective documentation"

# ─── Validation rules (Round 1 subset) ──────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "The impact/risk assessment must be completed BEFORE authorizing the change"
  - "Every change must have a backout plan (except where technically impossible — justify)"
  - "revalidation_scope must be consistent with gxp_impact (high → significant re-validation)"
  - "Emergency changes allow retrospective documentation, but the impact assessment is NOT skipped"
  - "change_phase is always project → GAMP §M8 (pre-go-live). Operational-phase changes to a validated system use CC (Change Control, §O6)"
  - "Provider-forced SaaS changes: supplier assessment + impact evaluation of the release"
  - "The emergency-change path MUST NOT be used for routine changes (anti-abuse)"

tags:
  - template
  - csv
  - change-request
  - cr
  - gamp-m8
  - project
  - canonical
---

# CR — Change Request (project-phase)

> [!note] Canonical CSV template — project phase
> **Canonical** template for the **Change Request (CR)** — a change raised **during the validation project** (project-phase, GAMP 5 §M8, lighter process). A project-phase change may trigger **partial re-validation** (re-execute IQ/OQ/PQ based on impact). Aligned with EU Annex 11 §10.
>
> Operational-phase changes to a validated system (after handover, VR approved) use [CC](CC.md) (Change Control, §O6) instead.

> [!tip] Embedded usage rules
> 1. **Impact assessment before authorizing** — no change is authorized without evaluating its impact on PS/PQ/DI.
> 2. **Backout plan always** — every change has a rollback plan (except where technically impossible and justified).
> 3. **Re-validation proportional to impact** — gxp_impact high → significant re-validation; low/none → minimal or none. Do not re-validate 100% by default (GAMP 5 §D5: assess impact).
> 4. **Emergency ≠ bypassing the process** — emergency allows retrospective documentation, but the impact assessment remains mandatory. Do not abuse the emergency path for routine changes.
> 5. **Project-phase only** — CR covers pre-go-live change (§M8, lighter). Once the system is validated and handed over, changes go through [CC](CC.md) (Change Control, §O6, formal). The handover point is defined in the handover document.
> 6. **Forced SaaS updates** — provider-forced updates are managed via supplier assessment + impact evaluation of each release.

---

## 0. Identification and signatures

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **Change phase** | `{{change_phase}}` (project §M8 — operational changes use [CC](CC.md)) |
| **Change type** | `{{change_type}}` |
| **GxP impact** | `{{gxp_impact}}` |
| **Requestor** | `{{requestor_name}}` |

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Requestor | `{{requestor_name}}` |  |  |  |
| Impact assessor (SME) |  |  |  |  |
| Authorizer (System Owner) |  |  |  |  |
| Quality approver (Quality Unit) |  |  |  |  |

---

## 1. Change description and justification

**Description**: `{{change_description}}`

**Reason / driver**: `{{change_reason}}`

**Change type** (GAMP 5 §O6):

| Type | Applies (✓) | Note |
|---|---|---|
| Standard / Routine | | Pre-agreed, low risk (e.g. AV update) |
| Like-for-Like / Kind | | Equivalent replacement |
| Sys Admin | | Administrative housekeeping |
| Emergency | | Retrospective documentation permitted |
| Temporary | | Must be reverted |
| Global | | Multi-site |

---

## 2. Impact / Risk Assessment

> [!warning] Before authorizing
> Complete this assessment BEFORE authorizing the change. Evaluate impact on patient safety / product quality / data integrity.

| Axis | Impact (H/M/L/None) | Justification |
|---|---|---|
| Patient Safety (PS) |  |  |
| Product Quality (PQ) |  |  |
| Data Integrity (DI) |  |  |
| **Overall GxP impact** | `{{gxp_impact}}` |  |

**Affected systems / documents**: (URS/FS/CS/DS/config items impacted)

| Affected document / item | Requires update (✓) |
|---|---|
|  |  |

---

## 3. Re-validation scope

**Scope**: `{{revalidation_scope}}`

> Proportional to impact (GAMP 5 §D5: assess impact, do not re-test 100% by default).

| Activity | Required? | Justification |
|---|---|---|
| Re-execute [IQ](IQ.md) | | If the change affects installation/baseline |
| Re-execute [OQ](OQ.md) | | If the change affects functionality |
| Re-execute [PQ](PQ.md) | | If the change affects the intended use |
| Update [RA](RA-INIT.md) | | If the change introduces new risks |
| Addendum to [VR](VR.md) | | Documented re-validation |

---

## 4. Implementation plan

| Step | Action | Responsible | Planned date |
|---|---|---|---|
| 1 |  |  |  |
|  |  |  |  |

---

## 5. Backout plan

> [!warning] Mandatory rollback plan
> Every change must be reversible (except where technically impossible and justified).

**Backout plan**: 

| Rollback step | Action | Responsible |
|---|---|---|
| 1 |  |  |
|  |  |  |

---

## 6. Authorization

| Decision | ✓ |
|---|---|
| Authorized to implement | |
| Authorized with conditions | |
| Rejected | |

**Conditions / justification**: 

---

## 7. Execution and closure

| Field | Value |
|---|---|
| Implementation date | |
| Backout executed? | |
| Re-validation completed | |
| Retrospective documentation (if emergency) | |
| Final status | implemented / closed / rejected |

---

## 8. Related documents

| Document | Reference |
|---|---|
| Validation Report | [VR](VR.md) |
| Risk Assessment | [RA-INIT](RA-INIT.md) |
| Re-validation protocols | [IQ](IQ.md) · [OQ](OQ.md) · [PQ](PQ.md) |
| Organization's change control policy | `{{org_change_policy_ref}}` |
| `{{custom_ref}}` |  |

---

## 9. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue |
|  |  |  |

---

## Canonical notes for implementers

> [!note] Project change (CR) vs operational change (CC)
> Pre-go-live (project, §M8) is progressive and lightweight — that is what this CR template owns. Post-handover (operational, §O6, formal) changes to a validated system use [CC](CC.md) (Change Control). The handover point is defined in the handover document (GAMP 5 §M8).

> [!note] Proportional re-validation
> GAMP 5 §D5 rejects 100% re-testing on environment changes. The re-validation scope scales with the evaluated impact, not by default.

> [!tip] Emergency is not a shortcut
> The emergency-change path allows retrospective documentation, but the impact assessment is non-negotiable. Abusing the emergency path for routine changes is a common audit finding.

> [!tip] Cloud / SaaS
> Provider-forced updates (GAMP 5 §O6 cloud): supplier assessment covers the provider's release process; each relevant release triggers an impact evaluation.

## Related

- [VR](VR.md) · [RA-INIT](RA-INIT.md) · [IQ](IQ.md) · [OQ](OQ.md) · [PQ](PQ.md)
- GAMP 5 · EU Annex 11 · 21 CFR Part 11
- operational change management · project change control · change management

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. Guidance for the `gdd.change` skill (future).

### Pre-flight
1. Read the consumer's `.gxp-dev.yaml`.
2. Confirm the change is **project-phase** (pre-go-live, no approved VR yet). If an approved VR exists, the system is operational — redirect to [CC](CC.md) (§O6) instead.
3. Read RA-INIT if it exists — impact assessment criteria.
4. Read `templates/csv/CR.md` from the toolkit.

### Flow
1. Capture description + reason + change type.
2. **Impact assessment** (§2) BEFORE authorizing — PS/PQ/DI.
3. Determine `revalidation_scope` proportional to the impact.
4. Implementation plan + backout plan.
5. Authorization.
6. Anti-hallucination: `[NEEDS CLARIFICATION: ...]`; never authorize without an impact assessment.
7. Output: `specs/CR-<NNN>.md` (status: requested).
8. Post-flight: `validate-frontmatter.py` + `check-clarification-markers.py`.

### `status` transitions

```
requested ──[impact assessment complete]──> assessed
assessed ──[authorization]──> authorized
authorized ──[implementation]──> in-progress
in-progress ──[executed + re-validation]──> implemented
implemented ──[verified + closed]──> closed
(or assessed/authorized ──> rejected)
```

### Mapping
| Origin (CR) | Destination | Rule |
|---|---|---|
| gxp_impact high | IQ/OQ/PQ re-execution | Proportional re-validation |
| Change implemented | VR addendum | Documented re-validation |
| New risks | RA-INIT update | If the change introduces new risks |
