---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "DEPLOY-RUN — Deployment Runbook (canonical CSV template)"
type: template
template_class: csv
template_id: "DEPLOY-RUN"
template_version: "0.1.0"
v_model_phase: deployment
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# DEPLOY-RUN is the operational procedure that bridges qualification (IQ)
# and live production. Executed under change control; references the IQ
# installation baseline and, for Cat 4/5, the CS/DS config baseline.
inputs:
  - template_id: "IQ"
    required: true
    description: "Installation Qualification (approved) — installation baseline and post-deploy verification anchor"
  - template_id: "CS"
    required: false
    description: "Configuration Specification (Cat 4) — config baseline deployed in this release"
  - template_id: "DS"
    required: false
    description: "Design Specification (Cat 5) — design baseline for the release build being deployed"
outputs:
  - artifact: "DEPLOY-RUN instance (Markdown) — executed deployment runbook"
    consumed_by:
      - "operation"    # The deployed system enters the operational phase
      - "IQ"           # Post-deploy verification confirms IQ baseline is intact

applicable_regulations:
  - "gamp-5"          # §M8 change and configuration management; deployment under change control
  - "eu-annex-11"     # §9 Qualification and Validation; §10 change and configuration management

based_on:
  - "GAMP 5 §M8 (change and configuration management — deployment gate) + §M11 (IT infrastructure)"
  - "EU Annex 11 §9 (qualification/validation) + §10 (change control)"
  - "Structure: ordered, executable runbook with pre-checks, numbered deployment steps with rollback points, post-deploy smoke verification, and full rollback procedure"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
  system_id:
    type: string
    required: true
  release_version:
    type: string
    required: true
    description: "Version string of the release being deployed (e.g. v1.2.0)"
  target_environment:
    type: string
    required: true
    description: "Target environment (e.g. Production, Staging, Validation)"
  iq_ref:
    type: string
    required: true
    description: "Identifier + version of the approved IQ that defines the installation baseline"
  cs_ref:
    type: string
    required: false
    description: "Identifier + version of the CS (Cat 4 config baseline); omit for Cat 5"
  ds_ref:
    type: string
    required: false
    description: "Identifier + version of the DS (Cat 5 design baseline); omit for Cat 3/4"
  change_control_ref:
    type: string
    required: true
    description: "Change Control record authorizing this deployment (CC-YYYY-NNN)"
  deployer_name:
    type: string
    required: true
    description: "Name of the person who executes the deployment steps"
  verifier_name:
    type: string
    required: true
    description: "Name of the independent person who verifies the deployment (different from deployer)"
  rollback_version:
    type: string
    required: true
    description: "Version to restore if rollback is triggered (previous stable baseline)"
  rollback_deadline_hours:
    type: string
    required: false
    description: "Maximum hours from deployment start within which rollback must be decided if triggered"
  org_csv_policy_ref:
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
    - based_on_template: "DEPLOY-RUN"
    - based_on_template_version
    - system_id
    - traces_to            # IQ instance (required) + CS/DS instance (as applicable)
    - gamp_category
    - status               # draft | in-execution | executed | approved | superseded
    - version
    - created
    - updated
    - language
  conditional_fields:
    - executed_by: "deployer who executed the steps (mandatory if status >= executed)"
    - verified_by: "independent verifier (mandatory if status >= executed)"
    - execution_date: "date of deployment execution"
    - change_control_ref: "mandatory — deployment must be authorized by change control"
    - rollback_triggered: "boolean — true if rollback was executed"
    - rollback_date: "mandatory if rollback_triggered: true"
    - deviations_count: "number of deviations recorded during execution"

# ─── Validation rules ────────────────────────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled before the runbook is approved for execution"
  - "traces_to must reference an approved IQ (GAMP 5 §M8 — deployment gates on qualified installation)"
  - "change_control_ref must reference a valid, authorized change control record"
  - "Deployer and Verifier must be different persons (segregation of duties)"
  - "A rollback procedure must be present and reference a known-good rollback_version"
  - "Post-deploy verification steps must explicitly tie back to the IQ baseline (smoke-check traceability)"
  - "Result and Done columns in all checklists must remain BLANK until actual execution (never pre-filled)"
  - "DEPLOY-RUN must reach status: approved before the system transitions to operational status"

tags:
  - template
  - csv
  - deployment
  - deploy-run
  - runbook
  - change-control
  - rollback
  - v-model
  - canonical
---

# DEPLOY-RUN — Deployment Runbook

> [!note] Canonical CSV template
> **Canonical** template for the **Deployment Runbook (DEPLOY-RUN)** — the step-by-step procedure to deploy a release of **`{{system_name}}`** (`{{release_version}}`) into **`{{target_environment}}`**. Executed under change control; authorizes the transition from the qualified installation baseline (see [IQ](IQ.md)) to operational use. Complies with GAMP 5 §M8 (change and configuration management) and EU Annex 11 §9–§10.

> [!warning] GAMP 5 §M8 — deployment must be authorized and controlled
> No release may be deployed to a qualified environment without a **closed, authorized change control record** (CC-YYYY-NNN). The DEPLOY-RUN does not substitute change control; it is the **execution artifact** that records what was done under that control.

> [!tip] Embedded usage rules
> 1. **Under change control** (GAMP 5 §M8) — a CC record authorizes the deployment before this runbook is executed. The CC reference is mandatory.
> 2. **Deployer ≠ Verifier** — segregation of duties: the person who executes the steps must not also be the sole verifier.
> 3. **Rollback is mandatory** — every DEPLOY-RUN must have a documented rollback procedure and a defined rollback trigger. Absence of a rollback procedure is a critical deficiency.
> 4. **Post-deploy verification ties to IQ** — smoke checks verify that the IQ baseline is intact after the deployment; they are not a replacement for OQ/PQ.
> 5. **Blank until executed** — result and "Done" columns are left blank in the approved runbook; they are filled only during actual execution. Pre-filling results is a data-integrity violation.
> 6. **Evidence with metadata** — screenshots/printouts must contain: date+time, step ID, deployer initials, reference to this runbook, and total page count.
> 7. **Cat awareness** — Cat 3: configuration may be captured in pre-check steps; Cat 4: reference [CS](CS.md) baseline; Cat 5: reference [DS](DS.md) baseline + build artifacts.

---

## 0. Identification and signatures

### Release and environment

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **Release version** | `{{release_version}}` |
| **Target environment** | `{{target_environment}}` |
| **Rollback-to version** | `{{rollback_version}}` |
| **Change Control record** | `{{change_control_ref}}` |
| **IQ baseline reference** | `{{iq_ref}}` ([IQ](IQ.md)) |
| **Config baseline (CS / Cat 4)** | `{{cs_ref}}` ([CS](CS.md)) |
| **Design baseline (DS / Cat 5)** | `{{ds_ref}}` ([DS](DS.md)) |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Runbook author (SME / CSV) |  |  |  |  |
| Change Control approver (Quality Unit) |  |  |  |  |
| **Deployer** (executes) | `{{deployer_name}}` |  |  |  |
| **Verifier** (independent) | `{{verifier_name}}` |  |  |  |

**Overall deployment result**: ☐ Success (no deviations) ☐ Success with non-critical deviations (see §7) ☐ Failed — rollback executed ☐ Failed — rollback not executed (escalate immediately)

**Execution date / time start**: `__________`   **End**: `__________`

> [!note] Deployer prior training
> The deployer confirms by signature that the necessary training has been completed (GxP, the [Validation Plan](VP.md), and the system's operational procedure) before executing this runbook. The verifier confirms independent review of the execution record.

---

## 1. Objective and scope

### 1.1 Objective

Provide an ordered, auditable procedure to deploy **`{{system_name}}`** release **`{{release_version}}`** into **`{{target_environment}}`** in a controlled manner, confirm that the IQ installation baseline is intact after deployment, and enable a defined rollback to **`{{rollback_version}}`** if the deployment cannot be completed successfully.

### 1.2 Scope

This runbook covers:
- Pre-deployment environment and readiness checks
- Ordered deployment steps with expected outcomes and individual rollback points
- Post-deployment smoke verification (tied to IQ baseline)
- Rollback procedure (trigger conditions + ordered steps)

This runbook does **not** substitute for the [IQ](IQ.md) (installation verification), [OQ](OQ.md) (functional verification), or [PQ](PQ.md) (performance verification) — those remain as the primary qualification record. Post-deploy smoke checks here are a fast-check to confirm the baseline, not a replacement for OQ execution.

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| DEPLOY-RUN | Deployment Runbook — the executable change-control artifact for a release deployment |
| IQ | Installation Qualification — installation verification (GAMP 5 Table 4.1); defines the baseline this runbook must preserve |
| CS | Configuration Specification — the configuration baseline for Cat 4 systems |
| DS | Design Specification — the design/build baseline for Cat 5 systems |
| CC | Change Control record — authorizes the deployment before execution |
| Rollback | Controlled reversion to the previous stable baseline (`{{rollback_version}}`) |
| Rollback point | The latest step up to which the deployment can be reverted without full rollback |
| Smoke check | Fast post-deployment test confirming key installation items match the IQ baseline |
| Deviation | Unexpected result during deployment that requires evaluation before proceeding |

---

## 3. Prerequisites

> [!warning] Execution gates (GAMP 5 §M8 + data integrity)
> - This runbook is executed **only against an approved copy** of this document.
> - The change control record (`{{change_control_ref}}`) must be **authorized and closed** before deployment begins.
> - The IQ (`{{iq_ref}}`) must be **approved** — deployment into an unqualified installation is not permitted.
> - The deployer and verifier must be **different persons**.
> - Any deviation encountered during deployment is escalated to the quality function **before** proceeding past the affected step or deciding on rollback.

### 3.1 Source documents

| Document | Reference |
|---|---|
| Change Control record authorizing this deployment | `{{change_control_ref}}` |
| IQ installation baseline being maintained | `{{iq_ref}}` ([IQ](IQ.md)) |
| Configuration Specification (Cat 4) | `{{cs_ref}}` ([CS](CS.md)) |
| Design Specification (Cat 5) | `{{ds_ref}}` ([DS](DS.md)) |
| Validation Plan | [VP](VP.md) |
| Release Notes | [RN](RN.md) |

### 3.2 Pre-deployment checklist

> All items must be confirmed (✓) before proceeding to §4. Leave blank until verified at execution.

| ID-No. | Pre-check | Expected | Done (✓) |
|---|---|---|---|
| `DEPLOY-RUN-001` | Change control record `{{change_control_ref}}` is authorized and approved | CC status = Approved |  |
| `DEPLOY-RUN-002` | IQ `{{iq_ref}}` is in status: approved | IQ status = Approved |  |
| `DEPLOY-RUN-003` | Release artifact `{{release_version}}` is available and integrity-verified (checksum / hash confirmed) | Artifact present; hash matches published value |  |
| `DEPLOY-RUN-004` | Target environment `{{target_environment}}` is accessible and in expected baseline state | Environment accessible; matches IQ baseline |  |
| `DEPLOY-RUN-005` | Rollback artifact `{{rollback_version}}` is available and integrity-verified | Rollback artifact present; hash confirmed |  |
| `DEPLOY-RUN-006` | Deployer and verifier are identified and available | Two distinct persons confirmed |  |
| `DEPLOY-RUN-007` | Maintenance window is confirmed and users/stakeholders have been notified | Notification sent; window confirmed |  |
| `DEPLOY-RUN-008` | Current system state (pre-deployment) is documented / snapshotted | Snapshot or record of pre-deploy state captured |  |
|  |  |  |  |

---

## 4. Deployment steps

> [!note] Step execution rules
> - Steps are executed **in the order listed**. Do not skip steps without quality-function approval.
> - **Expected result** describes the pass criterion. Any deviation from the expected result is a **deviation** (see §7) and escalates to the quality function before proceeding.
> - **Rollback point** column marks the latest step from which rollback can safely return to `{{rollback_version}}`. After a step that is NOT marked as a rollback point, rollback from that point forward requires special assessment.
> - Leave the **Actual result** and **Done** columns BLANK until execution.

| Step | Action | Expected result | Actual result | Rollback point | Done (✓/✗) |
|---|---|---|---|---|---|
| **1** | Confirm environment is in maintenance mode / access restrictions applied | Users cannot access `{{target_environment}}` during deployment window |  | Yes |  |
| **2** | Back up the current state of `{{target_environment}}` (database, config files, installed artifacts) | Backup completed; backup reference recorded |  | Yes |  |
| **3** | Verify backup integrity (restore test or checksum validation) | Backup verified as restorable |  | Yes |  |
| **4** | Stop application services / processes in `{{target_environment}}` | All application services stopped gracefully |  | Yes |  |
| **5** | Deploy release artifact `{{release_version}}` to target location | Artifact deployed; no errors reported during deployment |  | Yes |  |
| **6** | Apply configuration changes specified in `{{cs_ref}}` (Cat 4) or `{{ds_ref}}` (Cat 5) | Configuration parameters match baseline defined in CS/DS |  | Yes |  |
| **7** | Apply database schema changes or data migrations (if applicable) | Schema/migration applied without errors; record migration log reference |  | No — assess before rollback |  |
| **8** | Restart application services / processes | All application services start without errors; no unexpected log output |  | No — confirm state before deciding |  |
| **9** | Confirm process/service health (process status, log scan for startup errors) | All expected processes running; no error-level entries at startup |  | No — proceed to smoke checks |  |
|  |  |  |  |  |  |

> [!note] Additional steps
> Insert additional system-specific steps above as needed. Maintain the sequential numbering. Each step must carry an expected result and a rollback-point designation.

---

## 5. Post-deployment verification (smoke checks)

> [!note] Purpose and scope
> Smoke checks confirm that the IQ installation baseline is intact after the deployment. They are fast, targeted checks — not a substitute for OQ or PQ. Each check ties to an IQ test case (`IQ-TC-NNN`) to make the traceability explicit.

| ID-No. | Smoke check | Ties to IQ-TC | Expected result | Actual result | Passed (✓/✗) |
|---|---|---|---|---|---|
| `DEPLOY-RUN-009` | Verify installed version string matches `{{release_version}}` | `IQ-TC-001` *(update to actual)* | Version = `{{release_version}}` |  |  |
| `DEPLOY-RUN-010` | Verify application is accessible at the expected endpoint / URL / interface | `IQ-TC-002` *(update to actual)* | Application responds at expected entry point |  |  |
| `DEPLOY-RUN-011` | Verify configuration parameters match the CS/DS baseline | `IQ-TC-003` *(update to actual)* | Key configuration values match baseline record |  |  |
| `DEPLOY-RUN-012` | Verify database connectivity and schema version | `IQ-TC-004` *(update to actual)* | DB accessible; schema version matches expected |  |  |
| `DEPLOY-RUN-013` | Verify audit trail / logging is active and writing correctly | `IQ-TC-005` *(update to actual)* | Log entries visible and correctly timestamped |  |  |
| `DEPLOY-RUN-014` | Verify key integrations / interfaces respond (if applicable) | `IQ-TC-006` *(update to actual)* | Interface health-check returns expected status |  |  |
|  |  |  |  |  |  |

**Smoke-check summary**: ☐ All passed — system confirmed in IQ-baseline-compliant state ☐ Partial failure — see deviations §7 ☐ Critical failure — rollback triggered (proceed to §6)

---

## 6. Rollback procedure

> [!warning] Rollback trigger conditions
> Rollback must be triggered if **any** of the following conditions is met:
> - A deployment step fails and cannot be resolved within the authorized maintenance window.
> - A smoke check in §5 fails and the quality function determines the system cannot be safely released.
> - The quality function or system owner decides, for any reason, that the deployment cannot be accepted.
>
> Rollback must be executed within `{{rollback_deadline_hours}}` hours of the trigger event (if specified). Exceeding this window requires escalation.

> [!note] Rollback is not failure
> Executing a controlled rollback is the correct GxP response to a failed deployment. An uncontrolled deployment in a qualified environment is far worse than a documented rollback.

### 6.1 Rollback trigger

| Field | Value |
|---|---|
| **Rollback triggered?** | ☐ Yes ☐ No |
| **Trigger event / reason** |  |
| **Step at which rollback was triggered** |  |
| **Quality function notified?** | ☐ Yes — Name / date: |
| **Rollback decision authorized by** |  |

### 6.2 Rollback steps

> Rollback is executed only when trigger conditions in §6.1 are met and quality function has been notified. Leave result column blank until executed.

| Step | Rollback action | Expected result | Actual result | Done (✓/✗) |
|---|---|---|---|---|
| **R-1** | Stop all application services in `{{target_environment}}` | Services stopped gracefully |  |  |
| **R-2** | Remove / uninstall deployed artifact `{{release_version}}` | `{{release_version}}` artifacts removed |  |  |
| **R-3** | Restore application artifacts from backup to `{{rollback_version}}` | `{{rollback_version}}` artifacts restored from backup |  |  |
| **R-4** | Restore configuration to `{{rollback_version}}` baseline | Configuration matches `{{rollback_version}}` baseline |  |  |
| **R-5** | Restore database to pre-deployment backup (if schema changes were applied in Step 7 of §4) | Database restored; schema version matches `{{rollback_version}}` |  |  |
| **R-6** | Restart application services | All application services start without errors |  |  |
| **R-7** | Execute smoke checks from §5 against `{{rollback_version}}` baseline | All smoke checks pass against `{{rollback_version}}` |  |  |
| **R-8** | Remove maintenance mode / restore user access | Environment accessible; users notified |  |  |
|  |  |  |  |  |

**Rollback result**: ☐ Rollback successful — environment restored to `{{rollback_version}}` ☐ Rollback unsuccessful — escalate immediately to quality function and system owner

---

## 7. Deviations

> Record all deviations here. Any unexpected result in §3 (pre-checks), §4 (deployment steps), §5 (smoke checks), or §6 (rollback) is a deviation. Each deviation is escalated to the quality function before defining corrective action or deciding to proceed / rollback.

| Step / ID | Expected result | Actual result | Evaluation | Action taken | Responsible | Date | Resolved (✓) |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

---

## 8. Results summary and conclusion

| Metric | Value |
|---|---|
| Deployment steps total | |
| Deployment steps completed successfully | |
| Smoke checks total | |
| Smoke checks passed | |
| Deviations recorded | |
| Rollback triggered? | ☐ Yes ☐ No |

**Conclusion**: ☐ Deployment of `{{release_version}}` to `{{target_environment}}` completed successfully. System confirmed in IQ-baseline-compliant state; ready for operational use. ☐ Deployment completed with non-critical deviations — documented and accepted by quality function. ☐ Deployment failed — rollback executed; environment restored to `{{rollback_version}}`. ☐ Critical failure — escalate; environment state requires assessment before returning to service.

---

## 9. List of appendices (evidence)

| Appendix no. | Description | No. of pages |
|---|---|---|
|  | Pre-deployment snapshot / backup record |  |
|  | Deployment execution log / terminal output |  |
|  | Post-deployment smoke check screenshots |  |
|  | Rollback evidence (if triggered) |  |
|  |  |  |

---

## 10. Related documents

| Document | Reference |
|---|---|
| Change Control record (authorizes this deployment) | `{{change_control_ref}}` |
| IQ (installation baseline) | `{{iq_ref}}` ([IQ](IQ.md)) |
| Configuration Specification (Cat 4) | `{{cs_ref}}` ([CS](CS.md)) |
| Design Specification (Cat 5) | `{{ds_ref}}` ([DS](DS.md)) |
| Validation Plan | [VP](VP.md) |
| Release Notes | [RN](RN.md) |
| Validation Report | [VR](VR.md) |
| `{{custom_ref}}` |  |

---

## 11. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue |
|  |  |  |

---

## Canonical notes for implementers

> [!note] DEPLOY-RUN is an execution artifact, not a planning artifact
> This document is drafted before deployment (status: draft) and filled in during execution (status: in-execution → executed → approved). It is **not** a design document. The design lives in DS/CS; the installation baseline lives in IQ. DEPLOY-RUN bridges them into the production environment.

> [!note] Change control is a gate, not a formality
> GAMP 5 §M8 requires that changes to qualified systems are assessed and authorized before implementation. An unauthorized deployment — even a "small fix" — is a GxP deficiency. The CC record (`{{change_control_ref}}`) must predate the execution date of this runbook.

> [!warning] Database migrations — special rollback risk
> If the deployment includes database schema changes (§4 Step 7), the rollback window may be limited. Schema migrations that destroy data cannot be reversed without a full database restore. Assess this risk during change control planning and ensure the backup (§4 Step 2–3) is complete and verified before applying migrations.

> [!tip] Category awareness
> - **Cat 3**: DEPLOY-RUN captures steps for installing a standard product + its configuration. Smoke checks reference the IQ baseline for the standard package.
> - **Cat 4**: DEPLOY-RUN references the [CS](CS.md) baseline. Configuration drift is a primary risk; post-deploy verification must confirm parameter values match CS.
> - **Cat 5**: DEPLOY-RUN references the [DS](DS.md) build baseline + release artifact. Build traceability (artifact hash → DS version) must be confirmed.

## Related

- [IQ](IQ.md) · [CS](CS.md) · [DS](DS.md) · [OQ](OQ.md) · [VR](VR.md) · [RN](RN.md)
- GAMP 5 · EU Annex 11
- change control · configuration management · V-Model

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.deploy.from-iq` skill (planned).

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer project. If it does not exist → redirect to `/gdd.init`.
2. **Locate the approved IQ** (`specs/IQ.md`) — the installation baseline this runbook must preserve.
3. **Locate the change control record** — the CC reference is mandatory; without it, generation produces a DEPLOY-RUN with a prominent `[NEEDS CLARIFICATION: change_control_ref — no CC record found]` marker.
4. **Locate CS or DS** as applicable to the GAMP category declared in `.gxp-dev.yaml`.
5. **Read `templates/csv/DEPLOY-RUN.md`** from the toolkit as the source template (this file).

### Generation flow

1. **Parse the IQ smoke-check anchors** — for each critical `IQ-TC-NNN` in the approved IQ, generate a corresponding smoke check (`DEPLOY-RUN-NNN`) in §5, filling the "Ties to IQ-TC" column.
2. **Parse the CS/DS baseline** — populate §3.2 pre-check `DEPLOY-RUN-003` with the specific artifact hash or version string; populate §4 Step 6 with the configuration items from CS/DS.
3. **Populate the rollback steps** — confirm `{{rollback_version}}` is named; flag `[NEEDS CLARIFICATION: rollback_version]` if not declared in `.gxp-dev.yaml` or the CC record.
4. **Anti-hallucination**: insert `[NEEDS CLARIFICATION: ...]` for any field that cannot be resolved from source documents; never fabricate version strings, configuration values, or test results.
5. **Output**: write `specs/DEPLOY-RUN.md` (status: draft); print a summary of smoke checks generated vs. IQ-TC anchors available.
6. **Post-flight**: run `validate-frontmatter.py` + `check-clarification-markers.py`.

### `status` transitions

```
draft ──[CC authorized + pre-checks complete]──> in-execution
in-execution ──[all steps executed + smoke checks done]──> executed
executed ──[verifier signs + deviations resolved]──> approved
approved (deployment successful) ──> system enters operational phase
approved (rollback executed) ──> rollback documented; new CC required for retry
approved ──[new version]──> superseded
```

### Mapping

| Origin (DEPLOY-RUN) | Destination | Rule |
|---|---|---|
| `DEPLOY-RUN-NNN` smoke check | Row in `RTM.md` | Post-deploy baseline verification coverage |
| DEPLOY-RUN approved (success) | System enters operational phase | Operational procedures + periodic review apply |
| DEPLOY-RUN approved (rollback) | New CC required | New change control must be opened for retry |
| DEPLOY-RUN summary | `VR.md` | Validation Report records the deployment outcome |
