---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "CC — Change Control (canonical CSV template)"
type: template
template_class: csv
template_id: "CC"
template_version: "0.1.0"
v_model_phase: operation
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# CC governs operational changes to an already-validated system. Operation phase.
# Triggered after handover (VR approved). Distinct from CR (project-phase change
# during development). A change may trigger partial re-validation (re-execute
# IQ/OQ/PQ subset proportional to assessed impact).
inputs:
  - template_id: "VR"
    required: true
    description: "Validation Report — the system must be validated (VR approved) before the operational CC regime applies"
  - template_id: "RA-INIT"
    required: false
    description: "Initial Risk Assessment — change impact on PS/PQ/DI may reference the original risk model"
  - template_id: "RA-DET"
    required: false
    description: "Detailed Risk Assessment (FMEA) — referenced when the change introduces new failure modes"
outputs:
  - artifact: "CC instance (Markdown) — operational change control record"
    consumed_by:
      - "PR"           # Periodic Review references closed CCs as evidence of controlled changes
      - "IQ"           # if the change affects installation / configuration baseline
      - "OQ"           # if the change affects functionality
      - "PQ"           # if the change affects the intended use / process performance
      - "VR"           # addendum documenting post-change re-validation outcome
applicable_regulations:
  - "gamp-5"       # §O6 (Operational Change & Configuration Management) + §M8 (project change, pre-handover)
  - "eu-annex-11"  # §10 Change management
based_on:
  - "GAMP 5 §O6 pp.303-310 (Operational Change: Request → Specification → Impact/Risk Assessment → Plan → Backout → Authorize → Execute → Release) + §M8 (configuration management, project phase) + change types (standard/like-for-like/sysadmin/emergency/temporary/global)"
  - "EU Annex 11 §10: change management for computerized systems — authorization, impact assessment, re-validation scope"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
  system_id:
    type: string
    required: true
  change_type:
    type: enum
    required: true
    values: ["standard-routine", "like-for-like", "sys-admin", "emergency", "temporary", "global"]
    description: "Operational change type (GAMP 5 §O6)"
  change_description:
    type: string
    required: true
  change_reason:
    type: string
    required: true
  requester_name:
    type: string
    required: true
  gxp_impact:
    type: enum
    required: true
    values: ["high", "medium", "low", "none"]
    description: "Overall impact on validated state, Patient Safety / Product Quality / Data Integrity"
  revalidation_scope:
    type: string
    required: true
    description: "Which IQ/OQ/PQ activities must be re-executed, or 'none' with justification"
  vr_reference:
    type: string
    required: true
    description: "Identifier of the Validation Report that established the validated baseline being changed"
  org_change_policy_ref:
    type: string
    required: false
    description: "Reference to the organization's change control SOP or policy (optional, consumer-specific)"
  custom_ref:
    type: string
    required: false

# ─── Instance frontmatter spec ───────────────────────────────────────────────
instance_frontmatter_spec:
  required_fields:
    - title
    - type: "instance"
    - based_on_template: "CC"
    - based_on_template_version
    - system_id
    - change_type
    - gxp_impact
    - traces_to                # VR identifier — the validated baseline being changed
    - status                   # requested | assessed | authorized | in-progress | implemented | closed | rejected
    - version
    - created
    - updated
    - language
  conditional_fields:
    - authorized_by: "required if status >= authorized"
    - backout_executed: "true / false / N/A — record outcome after implementation"
    - emergency_retrospective: "true if retrospective documentation was used (emergency path)"
    - revalidation_completed: "true when all re-validation activities in §4 are closed"

# ─── Validation rules ────────────────────────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "The impact on validated state and PS/PQ/DI assessment (§3) must be completed BEFORE Quality Unit authorization"
  - "Revalidation scope must be consistent with gxp_impact (high → significant re-validation; none → explicitly justified)"
  - "Quality Unit approval is mandatory before implementation begins (GAMP 5 §O6; EU Annex 11 §10)"
  - "Every change must have a backout plan, unless technically impossible — in that case, justify in §5"
  - "Emergency changes allow retrospective documentation, but the impact assessment is NOT skipped (GAMP 5 §O6)"
  - "The emergency-change path MUST NOT be used for routine changes (common audit finding)"
  - "Closure requires a documented verification that the change was implemented as planned and the system behaves as expected"
  - "traces_to must reference a valid, approved VR; a system without an approved VR is NOT in the CC operational regime"

tags:
  - template
  - csv
  - change-control
  - cc
  - gamp-o6
  - gamp-m8
  - operation
  - canonical
---

# CC — Change Control (Operational)

> [!note] Canonical CSV template — operation phase
> **Canonical** template for **Operational Change Control (CC)** — governs changes to a **validated** system in the Operation phase (after handover, [VR](VR.md) approved). Anchored to GAMP 5 §O6 (Operational Change & Configuration Management) and EU Annex 11 §10. Distinct from [CR](CR.md) (project-phase change during development, §M8, lighter): once a system is validated, every change passes through this record before implementation.
>
> Project-phase changes (before the system is validated / handed over) use [CR](CR.md) (Change Request, §M8) instead.

> [!tip] Embedded usage rules
> 1. **VR prerequisite** — CC applies only when a [Validation Report](VR.md) exists and is approved. Pre-handover changes use [CR](CR.md) (§M8).
> 2. **Impact assessment before authorization** — complete §3 (Impact & Risk Assessment) BEFORE Quality Unit signs off. No exceptions.
> 3. **Re-validation is proportional, not automatic** — GAMP 5 §O6: assess impact, re-test only what is affected. Do not re-execute 100% by default.
> 4. **Quality Unit authorization is a gate** — implementation cannot start until QU approves (EU Annex 11 §10).
> 5. **Backout plan always** — every change is reversible or the impossibility is justified in writing.
> 6. **Emergency ≠ bypassing the process** — emergency allows retrospective documentation; impact assessment is still mandatory. Abusing the emergency path is a recurring audit finding.
> 7. **Cloud / SaaS** — provider-forced updates are managed via supplier assessment + impact evaluation of each release (GAMP 5 §O6).

---

## 0. Identification and signatures

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **Validated baseline (VR)** | `{{vr_reference}}` |
| **Change type** | `{{change_type}}` |
| **GxP impact** | `{{gxp_impact}}` |
| **Requester** | `{{requester_name}}` |

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Requester | `{{requester_name}}` |  |  |  |
| Impact Assessor (SME) |  |  |  |  |
| System Owner (System Owner) |  |  |  |  |
| Quality Unit Approver (Quality Unit) |  |  |  |  |

---

## 1. Change description and justification

**Description**: `{{change_description}}`

**Reason / driver**: `{{change_reason}}`

**Change type** (GAMP 5 §O6):

| Type | Applies (✓) | Note |
|---|---|---|
| Standard / Routine | | Pre-agreed, low risk (e.g. scheduled AV update) |
| Like-for-Like | | Equivalent replacement with no functional difference |
| Sys Admin | | Administrative housekeeping (no functional impact) |
| Emergency | | Unplanned; retrospective documentation permitted |
| Temporary | | Time-limited; must be reverted at defined end date |
| Global | | Multi-site change |

---

## 2. Current validated baseline

> [!note] Establish what is being changed before assessing impact
> Describe the configuration item(s) affected: software version, configuration parameter, hardware component, or SOP. This section anchors the impact assessment to the approved validated state.

| Item | Current validated state | Proposed new state |
|---|---|---|
|  |  |  |

**Configuration baseline reference** (config item ID or [VR](VR.md) section): 

---

## 3. Impact and risk assessment

> [!warning] Complete before authorization
> This section MUST be completed and reviewed BEFORE Quality Unit authorization. Evaluate impact on the validated state, patient safety (PS), product quality (PQ), and data integrity (DI).

### 3.1 Impact on validated state

| Question | Answer (Yes / No / N/A) | Justification |
|---|---|---|
| Does the change affect functionality covered by OQ test cases? | | |
| Does the change affect process performance covered by PQ scenarios? | | |
| Does the change affect the installation baseline (IQ)? | | |
| Does the change affect data structures, retention, or audit trail? | | |
| Does the change affect access control or electronic signatures? | | |
| Does the change affect interfaces with other validated systems? | | |

### 3.2 GxP risk assessment

| Axis | Impact (H/M/L/None) | Justification |
|---|---|---|
| Patient Safety (PS) |  |  |
| Product Quality (PQ) |  |  |
| Data Integrity (DI) |  |  |
| **Overall GxP impact** | `{{gxp_impact}}` |  |

### 3.3 Affected documents and configuration items

| Affected document / config item | Requires update (✓) | Owner |
|---|---|---|
|  |  |  |

---

## 4. Re-validation scope

**Scope**: `{{revalidation_scope}}`

> [!note] Proportional re-validation (GAMP 5 §O6)
> Re-test only what is impacted by the change. Full re-execution of IQ/OQ/PQ is not required by default — assess impact and scope accordingly.

| Activity | Required? (Yes / No) | Justification |
|---|---|---|
| Re-execute [IQ](IQ.md) (subset or full) | | If the change affects installation / configuration baseline |
| Re-execute [OQ](OQ.md) (subset or full) | | If the change affects functional behavior |
| Re-execute [PQ](PQ.md) (subset or full) | | If the change affects the intended use / process performance |
| Update [RA-INIT](RA-INIT.md) or [RA-DET](RA-DET.md) | | If the change introduces new risks or resolves existing ones |
| Addendum to [VR](VR.md) | | Documented re-validation result; always recommended for major changes |

---

## 5. Implementation plan

| Step | Action | Responsible | Planned date |
|---|---|---|---|
| 1 |  |  |  |
|  |  |  |  |

---

## 6. Backout plan

> [!warning] Mandatory rollback plan
> Every operational change must be reversible. If rollback is technically impossible (e.g. irreversible data migration), this must be justified here, reviewed by the System Owner, and acknowledged by Quality Unit before authorization.

**Backout plan**:

| Rollback step | Action | Responsible | Trigger condition |
|---|---|---|---|
| 1 |  |  |  |
|  |  |  |  |

**Backout impossible?** (justify if applicable):

---

## 7. Authorization

> [!warning] Quality Unit gate
> Implementation MUST NOT start before Quality Unit authorization is recorded here (EU Annex 11 §10; GAMP 5 §O6).

| Decision | ✓ |
|---|---|
| Authorized to implement | |
| Authorized with conditions | |
| Rejected | |

**Conditions / justification**:

| Authorizer | Role | Date | Signature |
|---|---|---|---|
|  | System Owner |  |  |
|  | Quality Unit |  |  |

---

## 8. Implementation and verification

| Field | Value |
|---|---|
| Actual implementation date | |
| Implemented by | |
| Backout executed? | Yes / No / N/A |
| Re-validation activities completed (ref §4) | |
| Retrospective documentation (if emergency) | |
| Deviations from implementation plan | |

**Verification summary** (confirm the change was implemented as planned and the system behaves as expected post-change):

---

## 9. Closure and effectiveness check

> [!note] Close only when verified
> Close the CC record only after confirming that the change was implemented correctly, all re-validation activities are complete, and affected documents have been updated.

| Closure criterion | Met (✓) | Comment |
|---|---|---|
| Change implemented per plan (or deviations documented) | | |
| Re-validation activities completed and results acceptable | | |
| Affected documents / configuration baseline updated | | |
| No unintended impact observed | | |
| Temporary change: revert date confirmed (if applicable) | | |

| Closer | Role | Date | Signature |
|---|---|---|---|
|  | System Owner |  |  |
|  | Quality Unit |  |  |

**Final status**: implemented / closed / rejected

---

## 10. Related documents

| Document | Reference |
|---|---|
| Validated baseline | [VR](VR.md) (`{{vr_reference}}`) |
| Initial Risk Assessment | [RA-INIT](RA-INIT.md) |
| Detailed Risk Assessment | [RA-DET](RA-DET.md) |
| Re-validation protocols | [IQ](IQ.md) · [OQ](OQ.md) · [PQ](PQ.md) |
| Periodic Review | [PR](PR.md) |
| Organization's change control policy | `{{org_change_policy_ref}}` |
| `{{custom_ref}}` |  |

---

## 11. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue |
|  |  |  |

---

## Canonical notes for implementers

> [!note] CC vs CR — the handover boundary
> **CR** governs changes during the project lifecycle (pre-go-live, §M8, lighter process). **CC** governs changes after handover — once a [Validation Report](VR.md) is approved and the system is in operation (§O6, formal). The handover point is defined in the handover document referenced in the VR.

> [!note] Proportional re-validation
> GAMP 5 §O6 explicitly rejects automatic full re-validation for every change. The re-validation scope is derived from the assessed impact on the validated state — if the change does not touch a function covered by OQ, that OQ need not be re-run.

> [!tip] Emergency is not a shortcut
> The emergency-change path allows retrospective documentation (plan and impact assessment after the fact), but the impact assessment itself is non-negotiable. Documenting "emergency" to skip risk thinking is a recurring GMP audit finding and an indicator of systemic process failure.

> [!tip] Cloud / SaaS changes
> For SaaS systems where provider-forced updates are out of the organization's control: the supplier assessment covers the provider's release-management process; each release that affects the validated scope triggers an impact evaluation via this CC template (GAMP 5 §O6).

> [!warning] Traceability prerequisite
> `traces_to` in the instance frontmatter must reference a real, approved [VR](VR.md). An operational CC record without a traceable validated baseline is an orphan and will fail the anti-orphan lint check.

## Related

- [VR](VR.md) · [CR](CR.md) · [PR](PR.md) · [IR](IR.md)
- [RA-INIT](RA-INIT.md) · [RA-DET](RA-DET.md) · [IQ](IQ.md) · [OQ](OQ.md) · [PQ](PQ.md)
- GAMP 5 · EU Annex 11
- operational change management · change management · configuration management

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. Guidance for the `gdd.change` skill (future).

### Pre-flight
1. Read the consumer's `.gxp-dev.yaml`.
2. Confirm the system is in the **operational** regime: a `VR` must exist with status `approved`. If no VR exists, redirect to [CR](CR.md) (project-phase change, §M8).
3. Read `RA-INIT` and `RA-DET` if they exist — they anchor the impact assessment in §3.
4. Read `templates/csv/CC.md` from the toolkit.

### Flow
1. Capture `change_description` + `change_reason` + `change_type`.
2. Populate **§2 (Current validated baseline)** — what configuration items are being changed.
3. Complete **§3 (Impact & Risk Assessment)** BEFORE generating the authorization block in §7. If the agent cannot determine impact, emit `[NEEDS CLARIFICATION: impact on <item> not determinable from available context]`.
4. Derive `revalidation_scope` proportional to `gxp_impact` — populate **§4**.
5. Generate **§5 (Implementation plan)** + **§6 (Backout plan)**.
6. Generate the **§7 (Authorization)** block with status `assessed`, not `authorized` — a human must authorize.
7. Anti-hallucination: never mark `status: authorized` autonomously; never skip impact assessment.
8. Output: `specs/CC-<YYYY>-<NNN>.md` (status: `requested`).
9. Post-flight: `validate-frontmatter.py` + `check-clarification-markers.py`.

### `status` transitions

```
requested ──[impact assessment complete]──> assessed
assessed ──[QU + System Owner authorization]──> authorized
authorized ──[implementation started]──> in-progress
in-progress ──[executed + re-validation complete]──> implemented
implemented ──[effectiveness check + closure]──> closed
(or assessed/authorized ──> rejected)
```

### Mapping
| Origin (CC) | Destination | Rule |
|---|---|---|
| gxp_impact high | IQ/OQ/PQ re-execution (subset or full) | Proportional re-validation (GAMP 5 §O6) |
| Change implemented | VR addendum | Document re-validation outcome |
| New risks introduced | RA-INIT / RA-DET update | If the change adds failure modes not in the original RA |
| CC closed | PR evidence | Periodic Review references closed CCs as proof of controlled change history |
