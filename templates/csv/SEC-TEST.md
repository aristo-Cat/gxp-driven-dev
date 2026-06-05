---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "SEC-TEST — Security Testing (canonical CSV template)"
type: template
template_class: csv
template_id: "SEC-TEST"
template_version: "0.1.0"
v_model_phase: security-verification
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# SEC-TEST is a targeted security verification protocol that runs in parallel
# with or as a sub-set of OQ. Verifies that all URS-SEC / URS-EREC / URS-ESIG
# controls are implemented and enforced (access control, MFA, encryption,
# audit-trail protection, vulnerability assessment / pen test). Feeds OQ, RTM
# and VR. GAMP 5 §D5 (risk-based testing) + EU Annex 11 §11-§12 (access
# control / security) + 21 CFR Part 11 §11.10(d) / §11.300 (electronic
# records / signatures security controls).
inputs:
  - template_id: "FS"
    required: true
    description: "Approved Functional Specification — source of FS-SEC / FS-EREC / FS-ESIG items that SEC-TEST verifies"
  - template_id: "URS"
    required: true
    description: "Approved User Requirements Specification — source of URS-SEC / URS-EREC / URS-ESIG items that define the security posture"
  - template_id: "RA-INIT"
    required: false
    description: "Initial Risk Assessment — scales rigor; High-risk security controls require positive + negative tests"
  - template_id: "OQ"
    required: false
    description: "OQ may delegate security test cases to this protocol or consume the executed SEC-TEST results as supporting evidence"
outputs:
  - artifact: "SEC-TEST instance (Markdown) — executed security testing protocol"
    consumed_by:
      - "OQ"       # Security test cases referenced or embedded in the OQ package
      - "RTM"      # Requirements Traceability Matrix — security coverage
      - "VR"       # Validation Report — security section / summary

applicable_regulations:
  - "gamp-5"          # §D5 (risk-based testing) + §D5 §25.5 (not all functions challenged)
  - "eu-annex-11"     # §11 (physical and logical security) + §12 (security requirements)
  - "21-cfr-part-11"  # §11.10(d) limiting system access; §11.10(g) authority checks; §11.300 electronic signatures controls
based_on:
  - "GAMP 5 §D5 (risk-based testing; negative tests for high-risk controls)"
  - "EU Annex 11 §11 (physical security) + §12 (security management)"
  - "21 CFR Part 11 §11.10(d) access control / §11.10(g) authority / §11.300 signature controls"
  - "OWASP Application Security Verification Standard (ASVS) — security verification framework"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
  system_id:
    type: string
    required: true
  fs_ref:
    type: string
    required: true
    description: "Identifier + version of the FS whose FS-SEC/EREC/ESIG items this protocol verifies"
  urs_ref:
    type: string
    required: true
    description: "Identifier + version of the URS that defines the security requirements (URS-SEC/EREC/ESIG)"
  ra_ref:
    type: string
    required: false
    description: "Identifier of the RA-INIT (risk-scaling) — optional; if absent, all security controls default to Risk Priority H"
  gamp_category:
    type: enum
    required: true
    values: [3, 4, 5]
  test_environment:
    type: string
    required: true
    description: "Security test environment — server, OS, network, DB, clients, test accounts, isolation level"
  test_data_strategy:
    type: string
    required: true
    description: "How test accounts, roles and datasets are managed; credential handling during testing; anonymization"
  sec_test_tester_name:
    type: string
    required: true
    description: "Person executing the security tests — must differ from Reviewer"
  sec_test_reviewer_name:
    type: string
    required: true
    description: "Independent reviewer of execution evidence — must differ from Tester"
  asvs_level:
    type: enum
    required: false
    values: [L1, L2, L3]
    description: "OWASP ASVS level adopted as the security verification framework baseline (L1 = basic; L2 = standard; L3 = high-assurance). Defaults to L2 for GAMP Cat 4/5."
  pen_test_scope:
    type: string
    required: false
    description: "Scope + boundaries of any penetration test (IP ranges, authentication tested, out-of-scope items). Leave blank if no pen test planned; document risk-acceptance."
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
    - based_on_template: "SEC-TEST"
    - based_on_template_version
    - system_id
    - traces_to            # list: FS instance + URS instance being verified
    - gamp_category
    - status               # draft | in-execution | executed | approved | superseded
    - version
    - created
    - updated
    - language
  conditional_fields:
    - executed_by
    - reviewed_by
    - execution_date
    - asvs_level
    - pen_test_scope
    - deviations_count
    - vulnerability_scan_tool
    - pen_test_provider

# ─── Validation rules ────────────────────────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "traces_to must point to an approved FS AND an approved URS"
  - "Tester and Reviewer must be different persons"
  - "Each URS-SEC / URS-EREC / URS-ESIG item with GxP=Y must have ≥1 SEC-TEST-TC-NNN that verifies it"
  - "Each FS-SEC / FS-EREC / FS-ESIG item with GxP=Y must have ≥1 SEC-TEST-TC-NNN that verifies it"
  - "All High-risk security controls (Risk Priority=H) require both a positive AND a negative test case"
  - "Negative tests must verify that unauthorized access is DENIED and LOGGED (audit trail)"
  - "Actual result and Passed columns must be BLANK in the draft; never pre-filled or fabricated"
  - "All deviations must be escalated to the quality function before any corrective action is defined"
  - "If no penetration test is planned, risk-acceptance must be explicitly documented"
  - "OWASP ASVS level adopted must match the system's risk profile (L2 minimum for GAMP Cat 4/5 systems under Part 11 / Annex 11)"

tags:
  - template
  - csv
  - security-testing
  - sec-test
  - security-verification
  - access-control
  - part-11
  - annex-11
  - owasp-asvs
  - v-model
  - canonical
---

# SEC-TEST — Security Testing

> [!note] Canonical CSV template
> **Canonical** template for the **Security Testing Protocol (SEC-TEST)** — the targeted verification protocol that confirms the system **`{{system_name}}`** enforces all security controls specified in its [URS](URS.md) (`URS-SEC` / `URS-EREC` / `URS-ESIG`) and implemented in its [FS](FS.md) (`FS-SEC` / `FS-EREC` / `FS-ESIG`). Covers access control, segregation of duties, authentication + MFA, encryption at rest and in transit, audit-trail tamper protection, session and password policy, vulnerability scanning, and penetration testing. Complies with GAMP 5 §D5, EU Annex 11 §11-§12 and 21 CFR Part 11 §11.10(d) / §11.10(g) / §11.300, using **OWASP ASVS** as the security verification framework.

> [!warning] Relationship to OQ
> SEC-TEST is a **companion protocol** to the [OQ](OQ.md), not a replacement. Security test cases may be (a) executed in this dedicated protocol and referenced from the OQ package, or (b) embedded directly in the OQ. Both approaches are accepted; the choice must be declared in the [VP](VP.md). Either way, the OQ package is incomplete without evidence of security verification.

> [!tip] Embedded usage rules
> 1. **Negative tests are mandatory** for every High-risk security control — unauthorized access must be **denied AND logged**. Logging the attempt is a regulatory control, not optional.
> 2. **Tester ≠ Reviewer** — segregation of duties applies to the security protocol itself.
> 3. **Actual result and Passed columns are BLANK in the draft** — never pre-fill; doing so is a GxP data integrity violation.
> 4. **Risk-based depth** (GAMP 5 §D5) — rigor scales with Risk Priority from RA-INIT. Low-risk controls may use supplier evidence + risk-acceptance instead of full scripted tests.
> 5. **OWASP ASVS** is the security verification framework baseline; the applicable level (`{{asvs_level}}`) is declared in §2 and drives which verification categories are in scope.
> 6. **Penetration testing scope** must be declared in §3 even if no pen test is planned — absence requires explicit risk-acceptance.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **FS being verified** | `{{fs_ref}}` ([FS](FS.md)) |
| **URS being verified** | `{{urs_ref}}` ([URS](URS.md)) |
| **RA scaling rigor** | `{{ra_ref}}` ([RA-INIT](RA-INIT.md)) |
| **GAMP category** | `{{gamp_category}}` |
| **OWASP ASVS level** | `{{asvs_level}}` |
| **Test environment** | `{{test_environment}}` |

### Test accounts and roles

> List every system role used during testing, with the test username and the person who exercised it. Credentials must be revoked or reset after protocol execution.

| System role | Test username | Tester / executor | Notes |
|---|---|---|---|
| *Privileged user (admin)* |  |  |  |
| *Standard user* |  |  |  |
| *Read-only / view-only* |  |  |  |
| *Unauthorized / no-access account* |  |  | Used for negative tests only |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Protocol author (SME / CSV / Security) |  |  |  |  |
| Approver 1 (System Owner) |  |  |  |  |
| Approver 2 (Quality Unit) |  |  |  |  |
| **Tester** | `{{sec_test_tester_name}}` |  |  |  |
| **Reviewer** (independent) | `{{sec_test_reviewer_name}}` |  |  |  |

**Overall result**: ☐ Pass ☐ Pass with non-critical deviations (see §8) ☐ Fail · **Execution no.**: `______`

---

## 1. Objective

Formally verify that the system **`{{system_name}}`** enforces all security controls specified in `{{urs_ref}}` (URS-SEC / URS-EREC / URS-ESIG items) and implemented in `{{fs_ref}}` (FS-SEC / FS-EREC / FS-ESIG items). Verification confirms:

- Access control and segregation of duties are enforced as specified.
- Authentication mechanisms (including MFA where required) reject unauthorized access.
- Data is protected by encryption at rest and in transit as specified.
- The audit trail cannot be modified, deleted, or bypassed by any system role.
- Session and password policies are enforced.
- No known exploitable vulnerabilities exist within the declared scope.

This protocol constitutes the **security verification** required by GAMP 5 §D5, EU Annex 11 §11-§12, and 21 CFR Part 11 §11.10(d) / §11.10(g) / §11.300. Results feed the [OQ](OQ.md) package and the [Validation Report](VR.md).

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| SEC-TEST | Security Testing — this protocol |
| Positive test | Verifies that an authorized user or action is permitted (happy path) |
| Negative test | Verifies that an unauthorized user or action is **rejected and the attempt is logged** |
| Access control | Mechanism limiting system access to authorized identities and roles (EU Annex 11 §12; 21 CFR Part 11 §11.10(d)) |
| Segregation of duties | No single user can both perform and approve a critical GxP action |
| MFA | Multi-Factor Authentication — requires ≥2 distinct authentication factors |
| Encryption at rest | Data stored on disk / database is encrypted using approved algorithms |
| Encryption in transit | Data traversing the network is protected (e.g., TLS 1.2+) |
| Audit trail | Immutable, time-stamped record of GxP-relevant actions; tamper-protection is a regulatory requirement |
| OWASP ASVS | Application Security Verification Standard — the security verification framework used to scope and classify test cases |
| Vulnerability scan | Automated scan for known CVEs and misconfigurations |
| Penetration test | Authorized simulated attack to discover exploitable vulnerabilities within the declared scope |
| Risk Priority | H / M / L — output of RA-INIT used to scale testing rigor per GAMP 5 §D5 |

---

## 3. Test requirements and prerequisites

> [!warning] Execution rules
> - Execute only on an **approved copy** of the protocol.
> - Tester must be trained (GxP + VP + FS + system + security methodology) before executing.
> - **Actual result and Passed columns must be left BLANK** until execution; pre-filling is a data integrity violation.
> - Tester ≠ Reviewer. Deviations escalated to quality before any corrective action is defined.
> - Test credentials must be revoked or reset immediately after protocol completion.

| Base document | Reference |
|---|---|
| Functional Spec being verified (security items) | `{{fs_ref}}` |
| User Requirements Spec (security items) | `{{urs_ref}}` |
| Risk Assessment (risk-scaling) | `{{ra_ref}}` |
| Validation Plan | [VP](VP.md) |
| Organization CSV policy | `{{org_csv_policy_ref}}` |

### Penetration test scope

| Field | Value |
|---|---|
| **Pen test planned?** | ☐ Yes ☐ No (document risk-acceptance below) |
| **Scope / IP ranges** | `{{pen_test_scope}}` |
| **Out-of-scope items** | |
| **Provider / executor** | |
| **Risk-acceptance if no pen test** | *[NEEDS CLARIFICATION: document explicit risk-acceptance if pen test is not planned — reference RA-INIT finding that supports the decision]* |

---

## 4. Test strategy (risk-based)

> [!note] GAMP 5 §D5 — risk-based security testing
> *"Fundamental to the risk-based approach is an acceptance that not all functionalities will be challenged and consequently not all defects will be found"* (§D5 §25.5). Security controls with Risk Priority=H require positive + negative tests. Lower-risk controls may rely on supplier evidence + risk-acceptance. OWASP ASVS `{{asvs_level}}` defines the verification categories in scope.

| Risk Priority (RA-INIT) | Required testing type |
|---|---|
| **H** | Positive + **negative** + boundary / limit where applicable. Both tests mandatory. |
| **M** | Positive (access permitted) + selective negative (at least one rejection case) |
| **L** | Basic positive verification + supplier evidence / configuration review (risk-acceptance documented) |

### 4.1 Security test types in scope

| Test type | Regulatory anchor | Risk Priority threshold | Applicable (✓/✗/NA) |
|---|---|---|---|
| Access control — positive (authorized access permitted) | EU Annex 11 §12; 21 CFR §11.10(d) | M+ | |
| Access control — negative (unauthorized access denied + logged) | EU Annex 11 §12; 21 CFR §11.10(d) | H (mandatory) | |
| Segregation of duties — negative (single user cannot perform + approve) | GAMP 5 §6.2.3; EU Annex 11 §12 | H | |
| Authentication + MFA — positive (valid credentials admitted) | 21 CFR §11.10(d); EU Annex 11 §12 | M+ | |
| Authentication — negative (invalid credentials / expired MFA rejected) | 21 CFR §11.10(d) | H | |
| Encryption at rest (data unreadable without decryption key) | EU Annex 11 §12; OWASP ASVS | M+ | |
| Encryption in transit (TLS enforcement; no plaintext channel) | EU Annex 11 §12; OWASP ASVS | M+ | |
| Audit-trail tamper protection (no edit / delete path for any role) | EU Annex 11 §11; 21 CFR §11.10(e) | H (mandatory) | |
| Session policy (timeout, re-authentication after idle) | 21 CFR §11.10(d); OWASP ASVS | M+ | |
| Password policy (complexity, expiry, history, lockout) | 21 CFR §11.300; OWASP ASVS | M+ | |
| Vulnerability scan (automated, within test environment) | OWASP ASVS | M+ | |
| Penetration test (authorized simulated attack, declared scope) | OWASP ASVS L2/L3; EU Annex 11 §12 | H or as declared | |

### 4.2 OWASP ASVS level mapping

| ASVS Level | When applicable | Verification categories |
|---|---|---|
| **L1** | Low-risk systems (GAMP Cat 3 / non-GxP critical) | Basic authentication, input validation, minimal access control |
| **L2** | Standard GxP systems (GAMP Cat 4 / Part 11 / Annex 11 systems) | All L1 + session management, encryption, audit trail, detailed access control |
| **L3** | High-assurance systems (safety-critical, Cat 5 with sensitive PII / IP) | All L2 + penetration test + advanced cryptography + supply-chain verification |

### 4.3 Test environment and data

**Environment**: `{{test_environment}}`
**Test data strategy**: `{{test_data_strategy}}`

> [!warning] Test credential hygiene
> Test accounts used for negative tests (no-access / unauthorized roles) must not exist in the production environment. All test credentials must be revoked or reset immediately after protocol completion. Document the revocation as an appendix entry.

---

## 5. Test cases

> Central section. Each URS-SEC / URS-EREC / URS-ESIG item AND each FS-SEC / FS-EREC / FS-ESIG item with GxP=Y requires ≥1 SEC-TEST-TC-NNN. Actual result and Passed columns are BLANK in the draft. Negative tests must verify that rejection is both **enforced** and **logged**.

### Test Case 1 — Access control (positive): authorized user granted access

**Objective**: Verify that a user with the correct role can access the authorized system function.

| SEC-TEST-TC | Verifies (URS/FS ID) | Risk (RA-INIT-NNN) | Test step | Expected result | Actual result / evidence / deviation no. | Passed (✓/✗) |
|---|---|---|---|---|---|---|
| `SEC-TEST-TC-001` | `FS-SEC-001` / `URS-SEC-001` | | Log in with a valid account assigned to the authorized role. Navigate to the protected function. | Access granted. Function is available as specified in `FS-SEC-001`. | | |
| | | | | | | |

*Tester / Reviewer signature at close of Test Case 1:* ______ / ______

---

### Test Case 2 — Access control (negative): unauthorized user denied + attempt logged

**Objective**: Verify that a user WITHOUT the required role is **denied** access and the attempt is **recorded in the audit trail**.

> [!warning] Negative test — mandatory for Risk Priority=H
> The unauthorized attempt must be (a) rejected at the system boundary and (b) logged with timestamp, user identity, and action attempted. A rejection without logging is an audit-trail gap — mark as deviation.

| SEC-TEST-TC | Verifies (URS/FS ID) | Risk (RA-INIT-NNN) | Test step | Expected result (denial + audit trail) | Actual result / evidence / deviation no. | Passed (✓/✗) |
|---|---|---|---|---|---|---|
| `SEC-TEST-TC-002` | `FS-SEC-001` / `URS-SEC-001` | | Log in with a valid account that does NOT hold the required role. Attempt to access the protected function. | Access denied. Error message does not disclose system internals. Attempt recorded in the audit trail (timestamp + user identity + action). | | |
| | | | | | | |

*Tester / Reviewer signature at close of Test Case 2:* ______ / ______

---

### Test Case 3 — Segregation of duties (negative): single user cannot perform + approve

**Objective**: Verify that the same user account cannot both execute and approve a GxP-critical action in the same workflow.

| SEC-TEST-TC | Verifies (URS/FS ID) | Risk (RA-INIT-NNN) | Test step | Expected result (denial + audit trail) | Actual result / evidence / deviation no. | Passed (✓/✗) |
|---|---|---|---|---|---|---|
| `SEC-TEST-TC-003` | `FS-SEC-002` / `URS-SEC-002` | | Complete a GxP-critical action as User A. Attempt to also approve that same action as User A (without switching to a second account). | Approval step requires a different user. System prevents self-approval. Attempt (if possible) is logged. | | |
| | | | | | | |

*Tester / Reviewer signature at close of Test Case 3:* ______ / ______

---

### Test Case 4 — Authentication + MFA (positive): valid credentials admitted

**Objective**: Verify that a valid user with enrolled MFA can authenticate successfully.

| SEC-TEST-TC | Verifies (URS/FS ID) | Risk (RA-INIT-NNN) | Test step | Expected result | Actual result / evidence / deviation no. | Passed (✓/✗) |
|---|---|---|---|---|---|---|
| `SEC-TEST-TC-004` | `FS-SEC-003` / `URS-SEC-003` | | Authenticate with valid username + password + valid MFA token. | User authenticated and session established. Successful login recorded in audit trail. | | |
| | | | | | | |

*Tester / Reviewer signature at close of Test Case 4:* ______ / ______

---

### Test Case 5 — Authentication (negative): invalid credentials / failed MFA rejected

**Objective**: Verify that invalid credentials are rejected, MFA failure blocks access, and account lockout engages after repeated failures.

| SEC-TEST-TC | Verifies (URS/FS ID) | Risk (RA-INIT-NNN) | Test step | Expected result (denial + audit trail) | Actual result / evidence / deviation no. | Passed (✓/✗) |
|---|---|---|---|---|---|---|
| `SEC-TEST-TC-005a` | `FS-SEC-003` / `URS-SEC-003` | | Attempt login with valid username and invalid password. | Access denied. Failed attempt logged. | | |
| `SEC-TEST-TC-005b` | `FS-SEC-003` / `URS-SEC-003` | | Attempt login with valid credentials but invalid MFA token. | Access denied at MFA step. Failed attempt logged. | | |
| `SEC-TEST-TC-005c` | `FS-SEC-003` / `URS-SEC-003` | | Repeat failed login N times (per password policy threshold). | Account locked. Lockout event logged. Administrator notification triggered (if specified). | | |
| | | | | | | |

*Tester / Reviewer signature at close of Test Case 5:* ______ / ______

---

### Test Case 6 — Audit-trail tamper protection: no edit / delete path for any role

**Objective**: Verify that no system role — including administrators — can edit or delete an existing audit-trail record.

> [!warning] Audit-trail integrity — EU Annex 11 §11 + 21 CFR §11.10(e)
> The inability to modify the audit trail is not optional. A system where any role can alter or delete audit records is non-compliant regardless of other controls. This test must be executed and must pass before OQ can be approved.

| SEC-TEST-TC | Verifies (URS/FS ID) | Risk (RA-INIT-NNN) | Test step | Expected result (tamper rejected) | Actual result / evidence / deviation no. | Passed (✓/✗) |
|---|---|---|---|---|---|---|
| `SEC-TEST-TC-006a` | `FS-EREC-001` / `URS-EREC-001` | | As a standard user: locate an audit-trail record and attempt to edit its content via the UI. | No edit capability exposed. Any attempt rejected by the system. | | |
| `SEC-TEST-TC-006b` | `FS-EREC-001` / `URS-EREC-001` | | As an administrator: attempt to delete or modify an audit-trail record via any available interface (UI, API, admin console). | Modification / deletion rejected or not possible. If an admin path exists, escalate immediately as Critical deviation. | | |
| `SEC-TEST-TC-006c` | `FS-EREC-001` / `URS-EREC-001` | | Verify that audit-trail entries include: timestamp, user identity, action taken, previous value, new value, and reason (where required). | All mandatory fields present and populated correctly in a sample of ≥10 records. | | |
| | | | | | | |

*Tester / Reviewer signature at close of Test Case 6:* ______ / ______

---

### Test Case 7 — Encryption at rest and in transit

**Objective**: Verify that data is encrypted at rest (storage) and in transit (network transport layer).

| SEC-TEST-TC | Verifies (URS/FS ID) | Risk (RA-INIT-NNN) | Test step | Expected result | Actual result / evidence / deviation no. | Passed (✓/✗) |
|---|---|---|---|---|---|---|
| `SEC-TEST-TC-007a` | `FS-SEC-004` / `URS-SEC-004` | | Review database / storage configuration documentation or configuration export to confirm encryption at rest is enabled (algorithm, key management). | Encryption at rest enabled using an approved algorithm. Key management documented. Configuration evidence attached as appendix. | | |
| `SEC-TEST-TC-007b` | `FS-SEC-004` / `URS-SEC-004` | | Use a network traffic capture tool in the test environment. Initiate a session and attempt to observe data in transit. | All traffic encrypted (TLS 1.2 or higher). No sensitive data visible in plaintext. Certificate valid and not expired. | | |
| | | | | | | |

*Tester / Reviewer signature at close of Test Case 7:* ______ / ______

---

### Test Case 8 — Session and password policy

**Objective**: Verify that session timeout, re-authentication, password complexity, expiry, history, and lockout policies are enforced as specified.

| SEC-TEST-TC | Verifies (URS/FS ID) | Risk (RA-INIT-NNN) | Test step | Expected result | Actual result / evidence / deviation no. | Passed (✓/✗) |
|---|---|---|---|---|---|---|
| `SEC-TEST-TC-008a` | `FS-SEC-005` / `URS-SEC-005` | | Establish a session. Leave it idle past the configured timeout period. Attempt to interact with the system. | Session terminated. User prompted to re-authenticate. Timeout event logged. | | |
| `SEC-TEST-TC-008b` | `FS-SEC-005` / `URS-SEC-005` | | Attempt to set a password that does not meet complexity requirements (e.g., too short, no special character). | Password rejected. Clear error message returned. No sensitive system detail leaked in the error. | | |
| `SEC-TEST-TC-008c` | `FS-SEC-005` / `URS-SEC-005` | | Attempt to reuse a recently used password (within history window). | Password change rejected. History policy enforced. | | |
| | | | | | | |

*Tester / Reviewer signature at close of Test Case 8:* ______ / ______

---

### Test Case 9 — Vulnerability scan

**Objective**: Execute an automated vulnerability scan within the declared scope and confirm no Critical or High findings remain open.

| SEC-TEST-TC | Verifies (URS/FS ID) | Risk (RA-INIT-NNN) | Test step | Expected result | Actual result / evidence / deviation no. | Passed (✓/✗) |
|---|---|---|---|---|---|---|
| `SEC-TEST-TC-009` | `FS-SEC-006` / `URS-SEC-006` | | Run the agreed vulnerability scanning tool against the test environment (within declared scope). Export findings report. | No Critical or High severity findings open. Medium / Low findings reviewed, risk-accepted or remediated. Scan report attached as appendix. | | |
| | | | | | | |

*Tester / Reviewer signature at close of Test Case 9:* ______ / ______

---

### Test Case 10 — Penetration test (if in scope)

**Objective**: Confirm that an authorized penetration test was conducted within the declared scope and no exploitable Critical vulnerabilities remain.

> [!note] Pen test — skip if not in scope
> If `{{pen_test_scope}}` is blank, this test case is N/A. Risk-acceptance must be documented in §3 referencing the RA-INIT finding. Do not leave this section blank without a documented risk-acceptance statement.

| SEC-TEST-TC | Verifies (URS/FS ID) | Risk (RA-INIT-NNN) | Test step | Expected result | Actual result / evidence / deviation no. | Passed (✓/✗) |
|---|---|---|---|---|---|---|
| `SEC-TEST-TC-010` | `FS-SEC-007` / `URS-SEC-007` | | Confirm pen test was executed per declared scope by the named provider. Review findings report. Verify that all Critical and High findings have been remediated and retested (or risk-accepted with QA approval). | Pen test report available. No unmitigated Critical findings. Remediation evidence or risk-acceptance attached as appendix. | | |
| | | | | | | |

*Tester / Reviewer signature at close of Test Case 10:* ______ / ______

---

### Test Case 11+ — (additional per project)

> Add further SEC-TEST-TC-NNN entries here as required by the FS-SEC / URS-SEC / URS-EREC / URS-ESIG gap analysis. Number sequentially. Do not renumber existing entries.

| SEC-TEST-TC | Verifies (URS/FS ID) | Risk (RA-INIT-NNN) | Test step | Expected result | Actual result / evidence / deviation no. | Passed (✓/✗) |
|---|---|---|---|---|---|---|
| `SEC-TEST-TC-011` | | | | | | |
| | | | | | | |

---

## 6. Security coverage (traceability summary)

> Confirms that each URS-SEC / URS-EREC / URS-ESIG AND FS-SEC / FS-EREC / FS-ESIG item with GxP=Y has ≥1 SEC-TEST-TC verifying it. Controls not tested are documented with risk-acceptance.

| Requirement ID | Source (URS / FS) | GxP | Risk Priority | SEC-TEST-TC verifying it | Covered (✓) / Risk-accepted |
|---|---|---|---|---|---|
| `URS-SEC-001` | URS | Y | H | `SEC-TEST-TC-001`, `SEC-TEST-TC-002` | |
| `URS-EREC-001` | URS | Y | H | `SEC-TEST-TC-006a`, `SEC-TEST-TC-006b`, `SEC-TEST-TC-006c` | |
| `URS-ESIG-001` | URS | Y | | | |
| `FS-SEC-001` | FS | Y | H | `SEC-TEST-TC-001`, `SEC-TEST-TC-002` | |
| `FS-EREC-001` | FS | Y | H | `SEC-TEST-TC-006a`, `SEC-TEST-TC-006b`, `SEC-TEST-TC-006c` | |
| | | | | | |

---

## 7. Deviations

| SEC-TEST-TC | Expected result | Actual result | Deviation classification | Proposed action | Owner | Date | Closed |
|---|---|---|---|---|---|---|---|
| | | | ☐ Critical ☐ Major ☐ Minor | | | | |

> [!warning] Deviation escalation
> All deviations must be reported to the quality function before any corrective action is defined. Critical deviations (e.g., audit trail editable by admin; no MFA enforcement despite URS requirement) block protocol approval until resolved and retested.

---

## 8. Results summary and conclusion

| Metric | Value |
|---|---|
| Total SEC-TEST-TC | |
| Passed / Failed | |
| Not applicable (N/A, documented) | |
| Deviations — Critical / Major / Minor | |
| URS-SEC / URS-EREC / URS-ESIG items covered / total GxP=Y | |
| FS-SEC / FS-EREC / FS-ESIG items covered / total GxP=Y | |
| Risk-accepted controls (not tested) | |
| Vulnerability scan: open Critical / High findings | |
| Pen test: open Critical findings | |

**Conclusion**: ☐ All security controls verified — ready to feed OQ package. ☐ Pass with non-critical deviations (see §7). ☐ Fail — security issues block OQ approval.

---

## 9. Appendices list (evidence)

| Appendix no. | Description | No. of pages |
|---|---|---|
| A | Vulnerability scan report (tool name, date, scope, findings summary) | |
| B | Penetration test report or risk-acceptance statement | |
| C | Encryption configuration evidence (at rest + in transit) | |
| D | Test credential revocation / reset confirmation | |
| E | Additional evidence / screenshots | |

---

## 10. Related documents

| Document | Reference |
|---|---|
| Functional Spec (security items verified) | `{{fs_ref}}` ([FS](FS.md)) |
| User Requirements Spec (security requirements) | `{{urs_ref}}` ([URS](URS.md)) |
| Risk Assessment | `{{ra_ref}}` ([RA-INIT](RA-INIT.md)) |
| Operational Qualification (consumer of SEC-TEST results) | [OQ](OQ.md) |
| Requirements Traceability Matrix | [RTM](RTM.md) |
| Validation Report | [VR](VR.md) |
| Organization CSV policy | `{{org_csv_policy_ref}}` |
| `{{custom_ref}}` | |

---

## 11. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue |
| | | |

---

## Canonical notes for implementers

> [!note] SEC-TEST is security-first, not security-only
> This protocol covers the security controls declared in URS-SEC / URS-EREC / URS-ESIG. It does NOT replace a full information security management program (ISO 27001, SOC 2). It verifies that the specific controls required by the system's URS and FS are implemented and enforceable.

> [!note] Negative tests are the regulatory heartbeat of this protocol
> EU Annex 11 §12 and 21 CFR §11.10(d) require that access be *limited* to authorized individuals. A system that "allows the right people in" but does not *explicitly block and log* the wrong people is not compliant. Every High-risk access control must have a passing negative test case before the system can be considered verified.

> [!tip] OWASP ASVS as the structuring framework
> OWASP ASVS (Application Security Verification Standard) provides a numbered, public catalog of security verification requirements. Referencing it allows the protocol to remain technology-neutral while anchoring verification to a recognized standard. L1 covers basic controls; L2 is the minimum for Part 11 / Annex 11 systems; L3 is for high-assurance or safety-critical deployments. The ASVS level adopted is declared in §0 and §4.2 and drives which test types in §4.1 are mandatory vs. optional.

> [!tip] Category-awareness
> - **Cat 3**: SEC-TEST verifies the configured security settings of the vendor product (role assignments, session policy, encryption settings). Pen test may not be required; risk-acceptance with supplier evidence is accepted.
> - **Cat 4**: SEC-TEST verifies configuration + business-process-level security (role assignment workflow, approval chains, audit trail per process). L2 ASVS minimum.
> - **Cat 5**: SEC-TEST extends to custom code security (SAST / DAST output reviewed, pen test typically required, code review of security-critical modules). L2-L3 ASVS.

> [!warning] Audit-trail tamper protection is always Risk Priority=H
> Regardless of overall system risk classification, the audit-trail tamper test (SEC-TEST-TC-006) is always treated as Risk Priority=H. There is no regulatory justification for risk-accepting the absence of audit-trail integrity. Any finding here is a Critical deviation.

## Related

- [URS](URS.md) · [FS](FS.md) · [RA-INIT](RA-INIT.md) · [OQ](OQ.md) · [RTM](RTM.md) · [VR](VR.md)
- GAMP 5 · EU Annex 11 · 21 CFR Part 11
- access control · audit trail · electronic signatures · segregation of duties

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.sec-test.from-fs` skill (or the `gdd.tests.from-ra` skill when invoked with the security scope flag).

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer project. If it does not exist → redirect to `/gdd.init`.
2. **Locate approved FS** (`specs/FS.md`) — extract all FS-SEC, FS-EREC and FS-ESIG items with GxP=Y.
3. **Locate approved URS** (`specs/URS.md`) — extract all URS-SEC, URS-EREC and URS-ESIG items with GxP=Y.
4. **Locate RA-INIT** (`specs/RA-INIT.md`) if present — inherit Risk Priority for each security control. If absent, default all security controls to Risk Priority=H.
5. **Read `templates/csv/SEC-TEST.md`** from the toolkit as the source template (this file).
6. **Determine OWASP ASVS level** from `.gxp-dev.yaml` (`asvs_level` field) or infer from GAMP category (Cat 3 → L1; Cat 4 → L2; Cat 5 → L2 or L3).

### Generation flow

1. **Parse the URS-SEC / URS-EREC / URS-ESIG + FS-SEC / FS-EREC / FS-ESIG items** from both documents.
2. **For each security control item**, generate ≥1 `SEC-TEST-TC-NNN`:
   - Inherit Risk Priority from RA-INIT (or default to H).
   - If Risk Priority=H → generate **both** positive and negative test case.
   - Negative test must explicitly assert: (a) access/action denied, (b) attempt logged in audit trail.
   - Cite URS-ID + FS-ID for full forward and backward traceability.
3. **Activate test types** per §4.1 based on ASVS level + RA-INIT Risk Priority:
   - Always include: access control positive + negative, audit-trail tamper (mandatory, always H).
   - Include if URS-EREC active: all audit-trail tests (TC-006a/b/c pattern).
   - Include if URS-ESIG active: electronic signature binding + non-repudiation tests (add TC-NNN per ESIG item).
   - Include if MFA specified in URS-SEC: authentication positive + negative (TC-004, TC-005 pattern).
   - Include vulnerability scan: always (scope to test environment).
   - Include pen test: if Risk Priority=H OR ASVS L2/L3 declared OR explicitly required in URS-SEC.
4. **Leave Actual result and Passed columns BLANK** — these are completed at execution time only.
5. **Document risk-acceptance** for any security control not tested with a scripted test case (reference RA-INIT finding).
6. **Anti-hallucination**: use `[NEEDS CLARIFICATION: ...]` when information is missing (e.g., pen test provider unknown, encryption algorithm unspecified in FS); never fabricate test results, credential details, or scan findings.
7. **Output**: write `specs/SEC-TEST.md` (status: draft); print security coverage summary (URS-SEC/EREC/ESIG items covered / total GxP=Y).
8. **Post-flight**: `validate-frontmatter.py` + `check-clarification-markers.py` + `generate-rtm.py`.

### `status` transitions

```
draft ──[complete protocol + URS/FS approved]──> in-execution
in-execution ──[executed + evidence attached]──> executed
executed ──[reviewer signs + deviations closed]──> approved
approved ──[new version issued]──> superseded
```

### Mapping

| Origin (SEC-TEST) | Destination | Rule |
|---|---|---|
| `SEC-TEST-TC-NNN` | Row in `RTM.md` | Security verification coverage (URS-SEC/EREC/ESIG + FS-SEC/EREC/ESIG) |
| SEC-TEST approved | Referenced in `OQ.md` | OQ package includes security verification evidence |
| SEC-TEST summary | `VR.md` | Validation Report includes security verification section |
| Open Critical deviation | Blocks OQ approval | Critical security deviations must be closed before OQ can be approved |
