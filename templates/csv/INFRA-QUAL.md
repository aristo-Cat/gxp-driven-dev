---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "INFRA-QUAL — IT Infrastructure Qualification (canonical GAMP Category 1 template)"
type: template
template_class: csv
template_id: "INFRA-QUAL"
template_version: "0.1.0"
v_model_phase: installation-verification
gamp_categories_applicable: [1]
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# INFRA-QUAL is the qualification protocol for GAMP Category 1 IT
# infrastructure components (servers, OS, DB platforms, virtualization,
# network, storage, backup). Category 1 components are QUALIFIED, not
# validated (GAMP 5 §M4). Qualified infrastructure is a prerequisite for
# application-level IQ/OQ: an application cannot be installed on
# unqualified infrastructure (GAMP 5 §M11 — confirm the §M-appendix
# number against the GAMP 5 2nd-edition index).
inputs:
  - template_id: "INFRA-SPEC"
    required: false
    description: "Infrastructure Design / Configuration Specification — defines the baseline to be qualified. May be a network diagram, server build specification, or configuration management record."
  - template_id: "RA-INIT"
    required: false
    description: "Initial Risk Assessment — optional; used to scale qualification rigor when the infrastructure supports high-risk regulated applications."
outputs:
  - artifact: "INFRA-QUAL instance (Markdown) — executed infrastructure qualification record"
    consumed_by:
      - "IQ"        # Application IQ pre-requisite: relies on qualified infrastructure
      - "RTM"       # Requirements Traceability Matrix — infrastructure qualification coverage
      - "VR"        # Validation Report — references qualified infrastructure as a precondition
applicable_regulations:
  - "gamp-5"          # §M4 (Category 1 — qualified, not validated) + §M11 (IT Infrastructure; confirm §M-appendix number against the GAMP 5 2nd-edition index) + Table 4.1 (installation verification for Cat 1)
  - "eu-annex-11"     # §3.2 (IT infrastructure should be qualified) + §4 (Validation — infrastructure as part of the computerized system environment)
based_on:
  - "GAMP 5 §M4 (Category 1 components: qualified not validated) + §M11 (IT Infrastructure Qualification; confirm §M-appendix number against the GAMP 5 2nd-edition index) + Table 4.1 (installation verification, Cat 1 row)"
  - "Structure: test protocol that verifies the infrastructure is installed, configured, secured, and monitored as specified; each infrastructure item → ≥1 qualification test step"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  infra_name:
    type: string
    required: true
    description: "Human-readable name for the infrastructure scope (e.g., 'Production Application Server Environment')"
  system_id:
    type: string
    required: true
    description: "Unique identifier for the infrastructure system or platform (generic, no corporate coding)"
  infra_spec_ref:
    type: string
    required: false
    description: "Identifier + version of the infrastructure specification or build standard being qualified"
  ra_ref:
    type: string
    required: false
    description: "Identifier + version of the RA-INIT that scales the rigor of this qualification (if applicable)"
  gamp_category:
    type: enum
    required: true
    values: [1]
    description: "GAMP Category — always 1 for IT infrastructure components"
  test_environment:
    type: string
    required: true
    description: "Description of the environment being qualified (data center, cloud tenant, virtual cluster, etc.)"
  infra_tester_name:
    type: string
    required: true
    description: "Name of the person executing the qualification protocol"
  infra_reviewer_name:
    type: string
    required: true
    description: "Name of the independent reviewer (must be different from the tester — GAMP segregation)"
  configuration_baseline_ref:
    type: string
    required: true
    description: "Reference to the approved configuration baseline document or record (e.g., CMDB record, build spec version)"
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
    - based_on_template: "INFRA-QUAL"
    - based_on_template_version
    - system_id
    - gamp_category        # must be 1
    - status               # draft | in-execution | executed | approved | superseded
    - version
    - created
    - updated
    - language
  conditional_fields:
    - executed_by: "tester who executed (mandatory if status >= executed)"
    - reviewed_by: "independent reviewer (mandatory if status == approved)"
    - execution_date
    - infra_spec_ref: "reference to the infrastructure specification or build standard qualified"
    - ra_ref: "RA-INIT reference when a formal risk assessment was performed"
    - deviations_count: "number of deviations recorded during execution"

# ─── Validation rules ────────────────────────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "gamp_category must be 1 — this template is exclusively for GAMP Category 1 infrastructure"
  - "Tester and Reviewer must be different persons (segregation of duties)"
  - "Time synchronization (NTP) must be verified — audit-trail timestamp integrity depends on it (EU Annex 11 §4)"
  - "Backup infrastructure must be verified and restore tested before the qualification is closed"
  - "Actual results and Passed fields are BLANK in the draft; never fabricate results before execution"
  - "Every deviation must be evaluated by the quality function before corrective action is defined"
  - "INFRA-QUAL must reach status: approved before the application IQ that depends on it reaches status: approved"
  - "Configuration baseline must be referenced by an approved document or CMDB record — not a floating verbal description"

tags:
  - template
  - csv
  - infrastructure-qualification
  - infra-qual
  - gamp-category-1
  - installation-verification
  - v-model
  - canonical
---

# INFRA-QUAL — IT Infrastructure Qualification

> [!note] Canonical CSV template — GAMP Category 1
> **Canonical** template for the **IT Infrastructure Qualification (INFRA-QUAL)** — the qualification protocol that verifies that the infrastructure environment **`{{infra_name}}`** is correctly installed, configured, secured, and monitored in conformance with its specification. Applies exclusively to **GAMP Category 1** components (servers, operating systems, database platforms, virtualization, network, storage, backup). Complies with GAMP 5 §M4 (*Category 1 — qualified, not validated*), §M11 (*IT Infrastructure Qualification* — confirm the §M-appendix number against the GAMP 5 2nd-edition index), and EU Annex 11 §3.2 (*IT infrastructure should be qualified*) + §4 (*Validation scope — infrastructure environment*).

> [!warning] GAMP 5 §M4 — qualified, not validated
> GAMP 5 **Category 1** components (OS, firmware, hypervisors, network switches, standard database engines used as platform) are **qualified, not validated**. This means the qualification demonstrates that the component is fit-for-purpose as a platform, not that a specific application function is verified. The functional and performance verification of applications running *on* this infrastructure is performed by the application-level [IQ](IQ.md), [OQ](OQ.md), and [PQ](PQ.md).

> [!tip] Embedded usage rules
> 1. **Pre-requisite of application IQ** — the INFRA-QUAL must be completed and approved **before** the application [IQ](IQ.md) is approved. There is no point in verifying an application installation on unqualified infrastructure.
> 2. **Scope is infrastructure, not application** — do NOT include application-level test steps here. Component inventory, OS version, network, NTP, backup, monitoring, and security hardening are in scope. Application configuration is in scope of [IQ](IQ.md) / [CS](CS.md).
> 3. **Time synchronization is a GxP-critical item** — NTP configuration and drift must be verified. Audit-trail timestamp integrity (EU Annex 11 §4 + ALCOA+ Contemporaneous principle) depends on accurate server time.
> 4. **Backup infrastructure verification is mandatory** — verifying that backups *run* is not enough; a restore test must demonstrate that data is recoverable within the defined RTO.
> 5. **Change-management baseline** — after qualification, the infrastructure is placed under change control. Any change to a qualified item requires a [Change Control Record (CC)](CC.md) and may trigger re-qualification of the affected components.
> 6. **Segregation Tester/Reviewer** — the executor and the reviewer are different persons. The reviewer is independent of the qualification execution.
> 7. **Evidence with metadata** — screenshots, configuration exports, and printouts must contain: date+time, Test ID, tester initials, and reference to this qualification protocol.

---

## 0. Identification and signatures

### Infrastructure scope

| Field | Value |
|---|---|
| **Infrastructure name** | `{{infra_name}}` |
| **System identifier** | `{{system_id}}` |
| **Infrastructure specification / build baseline** | `{{infra_spec_ref}}` |
| **Risk Assessment (scales rigor, if applicable)** | `{{ra_ref}}` ([RA-INIT](RA-INIT.md)) |
| **GAMP category** | `{{gamp_category}}` (Category 1 — qualified, not validated) |
| **Environment** | `{{test_environment}}` |
| **Configuration baseline reference** | `{{configuration_baseline_ref}}` |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Protocol author (SME / CSV) |  |  |  |  |
| Approver 1 (System Owner) |  |  |  |  |
| Approver 2 (Quality Unit) |  |  |  |  |
| **Tester** (executes) | `{{infra_tester_name}}` |  |  |  |
| **Reviewer** (independent) | `{{infra_reviewer_name}}` |  |  |  |

**Overall qualification result**: ☐ Pass (no deviations) ☐ Pass with non-critical deviations (see §7) ☐ Fail

**Execution no. / Partial qualification ref**: `__________`

> [!note] Tester prior training
> The tester confirms by signature that the necessary training has been completed (GxP fundamentals, the [Validation Plan](VP.md), and infrastructure operation procedures) before executing the INFRA-QUAL.

---

## 1. Objective

Formally verify that the IT infrastructure **`{{infra_name}}`** has been **correctly installed and configured** in conformance with its specification and organizational build standards, in the defined environment, with the approved configuration baseline. This qualification is the **installation verification** for GAMP Category 1 components (GAMP 5 §M4, §M11 — confirm the §M-appendix number against the 2nd-edition index — and Table 4.1) and constitutes the **pre-requisite** for the application-level [IQ](IQ.md) that depends on this infrastructure.

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| INFRA-QUAL | Infrastructure Qualification — installation and configuration verification for GAMP Category 1 components |
| GAMP Category 1 | Infrastructure software (OS, firmware, hypervisor, standard DB engine as platform) — qualified, not validated (GAMP 5 §M4) |
| Configuration baseline | Approved, documented state of all infrastructure components (versions, parameters, patches) |
| NTP | Network Time Protocol — time synchronization service critical for audit-trail timestamp accuracy |
| RTO | Recovery Time Objective — maximum acceptable time to restore infrastructure after failure |
| Deviation | Difference between expected and actual result that requires quality evaluation before closure |
| Change control | Formal process to evaluate, approve, and document changes to qualified infrastructure components |
| CMDB | Configuration Management Database — authoritative record of infrastructure component inventory and state |

---

## 3. Qualification requirements and prerequisites

> [!warning] Execution rules (GAMP 5 §M11 — confirm §M-appendix number against the 2nd-edition index — + data integrity)
> - The INFRA-QUAL is only executed against an **approved copy** of the protocol.
> - The tester must be trained (GxP fundamentals + VP + infrastructure operations) before executing.
> - Tester and reviewer must be **different persons** (segregation of duties).
> - Deviations are escalated to the quality function **before** defining corrective action.
> - Actual results and Passed fields are left **blank** in the draft — results are filled in during execution only.

### 3.1 Source documents

| Document | Reference |
|---|---|
| Infrastructure specification / build standard being qualified | `{{infra_spec_ref}}` |
| Risk Assessment (scales the rigor, if applicable) | `{{ra_ref}}` |
| Configuration baseline | `{{configuration_baseline_ref}}` |
| Validation Plan | [VP](VP.md) |

### 3.2 Prerequisites verified before starting

| ID-No. | Prerequisite | Verified (✓) |
|---|---|---|
| `INFRA-QUAL-TC-001` | Infrastructure environment is accessible and in the expected state for qualification |  |
| `INFRA-QUAL-TC-002` | Approved protocol is available and in use (no draft protocols executed) |  |
| `INFRA-QUAL-TC-003` | Configuration baseline document / CMDB record is approved and available |  |
| `INFRA-QUAL-TC-004` | Tester training records (GxP + VP + infrastructure ops) are complete and current |  |
|  |  |  |

---

## 4. Qualification strategy (risk-based)

> [!note] GAMP 5 §M11 — infrastructure qualification rigor
> *(Confirm the §M-appendix number against the GAMP 5 2nd-edition index.)* The depth of infrastructure qualification is scaled by the criticality of the applications hosted on this infrastructure and by the Risk Priority from RA-INIT (when applicable). Category 1 qualification focuses on **presence, version, configuration, and operational readiness** — not on business-function behavior. The evidence may include configuration exports, CMDB records, and supplier documentation in addition to manual verification steps.

| Risk context of hosted applications | INFRA-QUAL rigor |
|---|---|
| **High** (regulated GxP applications, audit-trail-bearing) | Full component inventory + NTP + backup restore test + security hardening + monitoring. All steps documented with timestamped evidence. |
| **Medium** (mixed regulated / non-regulated) | Key infrastructure items + NTP + backup verification + security spot-checks |
| **Low** (non-regulated applications only) | Basic inventory + supplier documentation + GEP |

---

## 5. Qualification test cases

> [!note] Test case ID format
> Each test case is identified as `INFRA-QUAL-TC-NNN` following the toolkit ID scheme (see [requirement-id-scheme](../../docs/requirement-id-scheme.md)). Actual results and Passed fields are completed during execution — **never pre-filled**.

### 5.1 Component inventory and versions

> Verify that all infrastructure components are present, of the correct type, and at the approved version / patch level per the configuration baseline.

| ID-No. | Component | Verification step | Expected result | Actual result | Passed (✓/✗) |
|---|---|---|---|---|---|
| `INFRA-QUAL-TC-005` | Server / host inventory | Enumerate all hosts and verify against the approved inventory | Inventory matches configuration baseline: correct hostname, role, count |  |  |
| `INFRA-QUAL-TC-006` | Operating system version and patch level | Check OS version and applied security patches on each host | OS version and patch level match the approved baseline |  |  |
| `INFRA-QUAL-TC-007` | Virtualization platform (if applicable) | Verify hypervisor version and configuration on each host | Hypervisor version and configuration match the approved baseline |  |  |
| `INFRA-QUAL-TC-008` | Database platform version (if applicable) | Check installed DB engine version and applied patches | DB engine version matches the approved baseline; no unauthorized patch delta |  |  |
| `INFRA-QUAL-TC-009` | Storage system inventory | Verify storage arrays, volumes, and mount points | Storage inventory matches the configuration baseline |  |  |
|  |  |  |  |  |  |

### 5.2 Configuration baseline verification

> Verify that each infrastructure component is configured in conformance with the approved baseline (settings, parameters, security policies).

| ID-No. | Component | Configuration parameter | Expected value (baseline) | Actual value | Passed (✓/✗) |
|---|---|---|---|---|---|
| `INFRA-QUAL-TC-010` | OS — each host | Key OS configuration parameters (hostname, domain, locale) | As per `{{configuration_baseline_ref}}` |  |  |
| `INFRA-QUAL-TC-011` | DB platform | Critical DB engine parameters (character set, memory limits, audit settings) | As per `{{configuration_baseline_ref}}` |  |  |
| `INFRA-QUAL-TC-012` | Firewall / security groups | Permitted port rules (inbound / outbound) per host role | Only approved ports open; all others denied |  |  |
|  |  |  |  |  |  |

### 5.3 Network and connectivity

> Verify that network topology, DNS resolution, and host connectivity are as specified.

| ID-No. | Component | Verification step | Expected result | Actual result | Passed (✓/✗) |
|---|---|---|---|---|---|
| `INFRA-QUAL-TC-013` | Network topology | Verify VLAN assignments and host IP addresses match the network design | IP addresses and VLAN assignments conform to the approved network design |  |  |
| `INFRA-QUAL-TC-014` | DNS resolution | Resolve all qualified hostnames from within each relevant network segment | All hostnames resolve to the correct IP; no rogue DNS entries |  |  |
| `INFRA-QUAL-TC-015` | Host-to-host connectivity | Verify required connections between application tier and DB tier, and to backup infrastructure | Required connections succeed; unrequired connections are blocked |  |  |
|  |  |  |  |  |  |

### 5.4 Time synchronization (NTP) — GxP-critical

> [!warning] NTP is GxP-critical — audit-trail integrity depends on it
> EU Annex 11 §4 and the ALCOA+ *Contemporaneous* principle require that electronic records carry accurate, trustworthy timestamps. Clock drift across servers creates timestamp inconsistencies that can invalidate audit trails. NTP configuration and synchronization status must be verified for **every host** in the qualified environment.

| ID-No. | Component | Verification step | Expected result | Actual result | Passed (✓/✗) |
|---|---|---|---|---|---|
| `INFRA-QUAL-TC-016` | NTP client — each host | Verify NTP client is configured and pointing to the approved time server(s) | NTP client active; correct server(s) configured |  |  |
| `INFRA-QUAL-TC-017` | Time synchronization status | Check current synchronization status and clock offset on each host | Offset within the approved threshold (typically ≤ 1 second); host synchronized |  |  |
| `INFRA-QUAL-TC-018` | UTC / timezone configuration | Verify server timezone setting and UTC offset are consistent across all hosts | Consistent timezone / UTC configuration per the approved baseline |  |  |
|  |  |  |  |  |  |

### 5.5 Backup infrastructure

> [!warning] Backup verification is mandatory — restore test is required
> Verifying that backup jobs are scheduled is insufficient. A restore test must demonstrate that data is recoverable from backup media within the defined RTO.

| ID-No. | Component | Verification step | Expected result | Actual result | Passed (✓/✗) |
|---|---|---|---|---|---|
| `INFRA-QUAL-TC-019` | Backup agent / service | Verify backup agent is installed, configured, and running on each host | Backup service active; pointing to the approved backup target |  |  |
| `INFRA-QUAL-TC-020` | Backup schedule and retention | Inspect backup schedule and verify retention periods match policy | Schedule and retention match the approved backup policy |  |  |
| `INFRA-QUAL-TC-021` | Backup media integrity | Verify backup media / repository is accessible and last backup completed without errors | Most recent backup: status = successful; no errors |  |  |
| `INFRA-QUAL-TC-022` | Restore test | Perform a test restore of a representative data set to the designated restore target | Data restored within defined RTO; integrity of restored data verified |  |  |
|  |  |  |  |  |  |

### 5.6 Monitoring and alerting

> Verify that the infrastructure monitoring system is operational and configured to alert on critical conditions relevant to GxP application availability.

| ID-No. | Component | Verification step | Expected result | Actual result | Passed (✓/✗) |
|---|---|---|---|---|---|
| `INFRA-QUAL-TC-023` | Monitoring agent / service | Verify monitoring agent is installed and reporting metrics from each host | Monitoring agent active; host metrics visible in the monitoring console |  |  |
| `INFRA-QUAL-TC-024` | Alerting configuration | Verify alert thresholds and notification channels for critical conditions (CPU, disk, memory, service down) | Alert rules configured per the approved monitoring specification; notification reaches the designated contact |  |  |
| `INFRA-QUAL-TC-025` | Log aggregation | Verify that system and security logs are forwarded to the designated log management system | Logs from each host appearing in the central log system within the expected interval |  |  |
|  |  |  |  |  |  |

### 5.7 Security hardening

> Verify that the infrastructure components have been hardened in conformance with the approved security baseline.

| ID-No. | Component | Verification step | Expected result | Actual result | Passed (✓/✗) |
|---|---|---|---|---|---|
| `INFRA-QUAL-TC-026` | Default credentials | Verify that factory / vendor default credentials are not in use on any component | No default credentials active on any host, OS, or DB platform |  |  |
| `INFRA-QUAL-TC-027` | Unnecessary services | Verify that unneeded OS services and network listeners are disabled | Only approved services running; no unauthorized listeners |  |  |
| `INFRA-QUAL-TC-028` | Administrative access | Verify that administrative access is restricted to approved accounts and sourced from approved networks | Admin access limited to approved accounts and source IP ranges |  |  |
| `INFRA-QUAL-TC-029` | Security patch compliance | Verify that critical and high-severity security patches are applied per the approved patching schedule | No overdue critical/high patches; patch compliance matches baseline |  |  |
|  |  |  |  |  |  |

### 5.8 Change management integration

> Verify that the infrastructure is registered in the change management process and that the post-qualification change control procedure is in place.

| ID-No. | Component | Verification step | Expected result | Actual result | Passed (✓/✗) |
|---|---|---|---|---|---|
| `INFRA-QUAL-TC-030` | CMDB registration | Verify that all qualified infrastructure components are registered in the CMDB | All components present in CMDB with correct attributes |  |  |
| `INFRA-QUAL-TC-031` | Change control procedure | Verify that a [Change Control (CC)](CC.md) process is in place and that responsible personnel are aware of the obligation to raise a CC before changing any qualified item | Change control process documented and communicated to infrastructure team |  |  |
|  |  |  |  |  |  |

---

## 6. Additional success criteria

| ID-No. | Supplementary criterion | Expected result | Actual result | Passed (✓/✗) |
|---|---|---|---|---|
| `INFRA-QUAL-TC-032` | Infrastructure documentation available | System description, network diagrams, and build runbooks are available and version-controlled | Required documentation present and current |  |  |
|  |  |  |  |  |  |

---

## 7. Overall evaluation / Deviations

> Consolidate all deviations here. Each deviation is escalated to the quality function before defining corrective action.

| Test ID | Expected result | Actual result | Evaluation | Action | Responsible | Date | Completed |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

---

## 8. Results summary and conclusion

> [!note] Reliance statement — application IQ dependency
> The application-level [IQ](IQ.md) for systems hosted on this infrastructure **relies** on the qualified state recorded here. The INFRA-QUAL must reach `status: approved` before the dependent application IQ is approved. If the infrastructure qualification is subsequently re-opened (e.g., deviation found, change control applied), the impact on dependent application qualifications must be assessed.

| Metric | Value |
|---|---|
| Total qualification test steps | |
| Passed | |
| Failed | |
| Deviations (critical / non-critical) | |
| Infrastructure components qualified / total in scope | |
| NTP verified on all hosts | Yes / No / Partial |
| Backup restore test completed | Yes / No |

**Conclusion**: ☐ Infrastructure qualified in conformance with the approved baseline; ready to host application-level IQ. ☐ Qualified with non-critical deviations documented and accepted. ☐ Fail — infrastructure does not conform to the approved baseline; application IQ may not proceed.

---

## 9. List of appendices (evidence)

| Appendix no. | Description | No. of pages |
|---|---|---|
|  | Configuration export / CMDB snapshot |  |
|  | NTP synchronization status output |  |
|  | Backup restore test record |  |
|  | Security scan output (if applicable) |  |

---

## 10. Related documents

| Document | Reference |
|---|---|
| Infrastructure specification / build standard | `{{infra_spec_ref}}` |
| Risk Assessment (if applicable) | `{{ra_ref}}` ([RA-INIT](RA-INIT.md)) |
| Configuration baseline | `{{configuration_baseline_ref}}` |
| Application Installation Qualification (depends on this) | [IQ](IQ.md) |
| Validation Plan | [VP](VP.md) |
| Change Control (post-qualification changes) | [CC](CC.md) |
| `{{custom_ref}}` |  |

---

## 11. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue |
|  |  |  |

---

## Canonical notes for implementers

> [!note] GAMP Category 1 — qualified, not validated
> The INFRA-QUAL is NOT a validation protocol. It is a qualification record demonstrating that Category 1 infrastructure components (OS, hypervisor, standard DB engine, network devices) are fit-for-purpose as a platform. The behavioral verification of the applications running on this infrastructure belongs to the [IQ](IQ.md), [OQ](OQ.md), and [PQ](PQ.md).

> [!note] NTP is always GxP-critical — do not skip
> Time synchronization verification is mandatory for any infrastructure supporting GxP applications. Audit-trail entries that cannot be trusted for their timestamp are a data-integrity finding. NTP must be verified for every qualified host regardless of application risk level.

> [!note] Backup restore test — not optional
> Verifying that a backup schedule is configured is not sufficient for a qualification. A restore test is the only way to confirm that the backup infrastructure actually works. The restore test result must be documented as evidence.

> [!tip] Post-qualification change control
> Once INFRA-QUAL reaches `status: approved`, the infrastructure is a qualified state. Any subsequent change to a qualified component (OS patch, network reconfiguration, storage expansion, hypervisor upgrade) must go through a [Change Control (CC)](CC.md) and, depending on the impact assessment, may trigger a partial or full re-qualification.

> [!tip] Scope boundary — infrastructure vs. application
> | In scope for INFRA-QUAL | Out of scope (belongs to IQ / OQ / CS) |
> |---|---|
> | OS version and patch level | Application installation verification |
> | DB engine version (as platform) | Application database schema and configuration |
> | Hypervisor, network, storage | Application network ports and interfaces |
> | NTP, backup infrastructure, monitoring | Application backup and DR procedures |
> | Security hardening of the OS layer | Application-level access control and user management |

## Related

- [IQ](IQ.md) · [OQ](OQ.md) · [VP](VP.md) · [VR](VR.md) · [CC](CC.md) · [RA-INIT](RA-INIT.md)
- GAMP 5 · EU Annex 11
- V-Model · installation qualification · data integrity

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.infra.from-spec` skill (or a general instantiation skill targeting INFRA-QUAL).

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer project. If it does not exist → redirect to `/gdd.init`.
2. **Locate the infrastructure specification or build baseline** (`specs/INFRA-SPEC.md`, a CMDB export, or a network/server build document) — defines the component inventory and configuration to be qualified.
3. **Locate the RA-INIT** (`specs/RA-INIT.md`) if one exists — used to scale qualification rigor. If not present, default to Medium rigor.
4. **Read `templates/csv/INFRA-QUAL.md`** from the toolkit as the source template (this file).

### Generation flow

1. **Parse the infrastructure inventory** from the spec (hosts, OS, DB platform, network, storage, backup, monitoring).
2. **For each component**, confirm ≥1 `INFRA-QUAL-TC-NNN` covers it. Add component-specific rows to the relevant sections (5.1–5.8) as needed; preserve the existing canonical rows.
3. **NTP mandatory**: always include §5.4 in full regardless of application risk level.
4. **Backup restore test mandatory**: always include `INFRA-QUAL-TC-022` regardless of rigor level.
5. **Scale the depth** by risk context (High: all sections full; Medium: all sections, sampling in 5.7; Low: 5.1 + 5.4 + 5.5 + supplier docs).
6. **Anti-hallucination**: insert `[NEEDS CLARIFICATION: ...]` when component details, version numbers, IP addresses, or configuration parameters are unknown; never fabricate specific values.
7. **Output**: write `specs/INFRA-QUAL.md` (status: draft); print coverage (components qualified / total in scope).
8. **Post-flight**: run `validate-frontmatter.py` + `check-clarification-markers.py`.

### `status` transitions

```
draft ──[complete protocol + approved]──> in-execution
in-execution ──[executed + evidence collected]──> executed
executed ──[reviewer signs + deviations closed]──> approved
approved ──[change control applied or re-qualification triggered]──> superseded
```

### Mapping

| Origin (INFRA-QUAL) | Destination | Rule |
|---|---|---|
| `INFRA-QUAL-TC-NNN` | Row in `RTM.md` | Infrastructure qualification coverage |
| INFRA-QUAL approved | Pre-requisite of `IQ.md` | Application IQ is not approved without INFRA-QUAL approved |
| INFRA-QUAL summary | `VR.md` | Validation Report references qualified infrastructure as an environmental precondition |
| Change to qualified item | `CC.md` | Post-qualification change control mandatory for any modification to a qualified component |
