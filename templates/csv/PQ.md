---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "PQ — Performance Qualification (canonical CSV template)"
type: template
template_class: csv
template_id: "PQ"
template_version: "0.1.0"
v_model_phase: fitness-for-intended-use-verification
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-28
updated: 2026-05-29
# Round 2 (2026-05-29): translated to English canonical (was language: es). §-citations + IDs preserved verbatim.

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# PQ is the upper-right vertex of the V-Model paired with the URS
# (fitness-for-intended-use verification, GAMP 5 Table 4.1). It verifies that
# the system meets user requirements under real operating conditions.
inputs:
  - template_id: "URS"
    required: true
    description: "Approved User Requirements Specification — source of the URS-<CATEGORY>-NNN whose fitness-for-intended-use the PQ verifies"
  - template_id: "RA-INIT"
    required: true
    description: "Risk Assessment — scales PQ scenarios by Risk Priority"
  - template_id: "OQ"
    required: true
    description: "Approved Operational Qualification — prerequisite (function must be verified before testing fitness)"
outputs:
  - artifact: "PQ instance (Markdown) — executed performance qualification"
    consumed_by:
      - "RTM"       # Requirements Traceability Matrix — fitness coverage
      - "VR"        # Validation Report — statement of fitness for intended use
applicable_regulations:
  - "gamp-5"          # Table 4.1 (PQ → fitness-for-intended-use verification) + §D5 + M7 (fitness statement)
  - "21-cfr-part-11"
  - "eu-annex-11"     # §9 Qualification and Validation
based_on:
  - "GAMP 5 Table 4.1 (PQ = fitness-for-intended-use verification) + §D5 (day-in-the-life / UAT) + M7 (statement of fitness)"
  - "Structure: end-to-end test protocol executed by end users under production-like conditions; PQ-SCEN-NNN scenarios trace to URS-IDs"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
  system_id:
    type: string
    required: true
  urs_ref:
    type: string
    required: true
    description: "Identifier + version of the URS whose fitness-for-intended-use the PQ verifies"
  ra_ref:
    type: string
    required: true
  oq_ref:
    type: string
    required: true
    description: "Identifier of the approved OQ (prerequisite)"
  gamp_category:
    type: enum
    required: true
    values: [3, 4, 5]
  production_like_environment:
    type: string
    required: true
    description: "Production-like environment where the PQ is executed (as close to production as possible)"
  end_user_testers:
    type: string
    required: true
    description: "Real end users who execute the PQ (GAMP: PQ is executed by end users, not IT)"
  intended_use_statement:
    type: string
    required: true
    description: "The regulatory intended use of the system (from the URS) that the PQ confirms"
  pq_reviewer_name:
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
    - based_on_template: "PQ"
    - based_on_template_version
    - system_id
    - traces_to            # URS instance whose fitness is verified
    - gamp_category
    - status               # draft | in-execution | executed | approved | superseded
    - version
    - created
    - updated
    - language
  conditional_fields:
    - executed_by          # end users
    - reviewed_by
    - execution_date
    - partial_test_ref
    - deviations_count

# ─── Validation rules (Round 1 subset) ──────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "traces_to must point to an approved URS"
  - "oq_ref must point to an approved OQ (V-Model prerequisite)"
  - "Every URS-<CATEGORY>-NNN with prio=H must be covered by ≥1 PQ-SCEN-NNN (fitness of critical requirements)"
  - "PQ scenarios must be end-to-end (complete business processes), not isolated functions"
  - "PQ testers must be end users (GAMP 5: PQ is executed by end users, not IT)"
  - "Each PQ-SCEN-NNN must cite the URS-IDs it covers + the associated RA-INIT-NNN risk"
  - "The environment must be production-like (as close to production as possible)"
  - "The conclusion must include the statement of fitness for intended use (GAMP 5 M7)"

tags:
  - template
  - csv
  - performance-qualification
  - pq
  - fitness-for-intended-use
  - v-model
  - canonical
---

# PQ — Performance Qualification

> [!note] Canonical CSV template
> **Canonical** template for the **Performance Qualification (PQ)** — the test protocol that verifies that the system **`{{system_name}}`** is **fit for its intended use** under real operating conditions, in accordance with its [URS](URS.md). It is the upper-right vertex of the V-Model paired with the URS. Complies with GAMP 5 Table 4.1 (PQ = *fitness-for-intended-use verification*), §D5 (day-in-the-life / UAT) and §M7 (statement of fitness).

> [!warning] GAMP 5 §4.2.6.4 terminology
> The filename `PQ.md` is retained by industrial CSV convention; internally it corresponds to **fitness-for-intended-use verification** (Table 4.1). GAMP 5 2nd Ed does not prescribe the term "PQ".

> [!tip] Embedded usage rules
> 1. **Fitness, not function** — the PQ confirms that the system serves its **intended use** under real conditions. Functional verification was already performed by the [OQ](OQ.md) (prerequisite).
> 2. **End-to-end, not isolated** — PQ scenarios are **complete business processes** ("day in the life"), not individual functions.
> 3. **Executed by end users** — GAMP 5: the PQ is executed by **real end users**, not IT. It demonstrates fitness in the hands of those who will operate the system.
> 4. **Production-like conditions** — the environment and data must be as close to production as possible.
> 5. **Traceability** — each `PQ-SCEN-NNN` cites the URS-IDs it covers + the associated risk.
> 6. **Statement of fitness** (GAMP 5 §M7) — the conclusion includes the formal declaration of fitness for intended use.
> 7. **Risk-based** — scenarios prioritize URS requirements with the highest Risk Priority.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **URS whose fitness is verified** | `{{urs_ref}}` ([URS](URS.md)) |
| **RA that scales the scenarios** | `{{ra_ref}}` ([RA-INIT](RA-INIT.md)) |
| **OQ prerequisite** | `{{oq_ref}}` ([OQ](OQ.md) — must be approved) |
| **GAMP category** | `{{gamp_category}}` |
| **Production-like environment** | `{{production_like_environment}}` |
| **Intended use verified** | `{{intended_use_statement}}` |

### End user executors

> GAMP 5: the PQ is executed by real end users, not IT.

| Business role | End user (tester) | Initials |
|---|---|---|
| `{{end_user_testers}}` |  |  |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Protocol author (Process Owner / SME) |  |  |  |  |
| Approver 1 (System Owner) |  |  |  |  |
| Approver 2 (Quality Unit) |  |  |  |  |
| **Reviewer** (independent) | `{{pq_reviewer_name}}` |  |  |  |

**Overall result**: ☐ Pass (fit for intended use) ☐ Pass with non-critical deviations (see §7) ☐ Fail · **Execution No.**: `______`

---

## 1. Objective

Formally verify that the system **`{{system_name}}`** is **fit for its intended use** (`{{intended_use_statement}}`) under real operating conditions, by executing GxP end-to-end business processes with real users, data and workflows. This PQ is the **fitness-for-intended-use verification** (GAMP 5 Table 4.1) and the final verification phase of the V-Model before the Validation Report.

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| PQ | Performance Qualification — fitness-for-intended-use verification (GAMP 5 Table 4.1) |
| Scenario | Complete end-to-end business process executed as a real user would |
| Day-in-the-life | Testing that simulates a real operational day/cycle of the system |
| Production-like | Environment/data as close as possible to production |
| Fitness for intended use | Suitability of the system for the regulatory intended use declared in the URS |
| UAT | User Acceptance Testing — the PQ is the GxP form of UAT |

---

## 3. Test requirements and prerequisites

> [!warning] Execution rules
> - Execute only on an **approved copy** of the protocol.
> - **Approved OQ** is a prerequisite (function must be verified before testing fitness).
> - Testers are **end users** trained in the business process.
> - Environment and data must be **production-like**.
> - Deviations must be escalated to quality before any action.

| Base document | Reference |
|---|---|
| URS whose fitness is verified | `{{urs_ref}}` |
| Risk Assessment | `{{ra_ref}}` |
| Operational Qualification (pre-req) | `{{oq_ref}}` |
| Validation Plan | [VP](VP.md) |

---

## 4. Test strategy (risk-based, end-to-end)

> [!note] GAMP 5 §D5 — day-in-the-life testing
> The PQ favors end-to-end and unscripted testing ("day in the life") that exercises the system as it will be used in real operation. Scenarios prioritize URS requirements with the highest Risk Priority. Witnesses are not mandatory (§8.5.4).

| Risk Priority (RA-INIT) of the URS requirement | PQ scenario depth |
|---|---|
| **H** | Full scenario + boundary conditions + realistic volume + concurrency |
| **M** | Representative scenario of the normal process |
| **L** | Covered by general scenarios or risk-accepted |

---

## 5. Test scenarios — `PQ-SCEN-NNN`

> Central section. Each scenario is a complete end-to-end business process. It covers one or more URS-IDs. Executed by the end user of the corresponding role.

### Scenario 1 — `<business process name>`

**Covers (URS-ID)**: `URS-FUNC-001`, `URS-...`
**Risk (RA-INIT-NNN)**: `______`
**Executing role (end user)**: `______`
**Scenario description**: *complete business process from start to finish, as the real user would perform it.*

| Step | User action | Expected result | Actual result / evidence | Passed (✓/✗) |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
|  |  |  |  |  |

*End user / reviewer signature at scenario close:* ______ / ______

### Scenario 2 — `<name>`

**Covers (URS-ID)**: `URS-...`
**Risk**: `______` · **Executing role**: `______`

| Step | User action | Expected result | Actual result / evidence | Passed (✓/✗) |
|---|---|---|---|---|
| 1 |  |  |  |  |
|  |  |  |  |  |

### Scenario 3+ — (additional scenarios per process)

| PQ-SCEN | Covers (URS-ID) | Business process | Result | Passed |
|---|---|---|---|---|
| `PQ-SCEN-003` |  |  |  |  |
|  |  |  |  |  |

---

## 6. Fitness coverage (traceability summary)

> Confirms that every URS-ID with prio=H is covered by ≥1 PQ scenario.

| URS-ID | Prio | Risk Priority | PQ-SCEN covering it | Covered (✓) / Risk-accepted |
|---|---|---|---|---|
| `URS-FUNC-001` |  |  | `PQ-SCEN-001` |  |
|  |  |  |  |  |

---

## 7. Overall assessment / Deviations

| Scenario/Step | Expected result | Actual result | Assessment | Action | Owner | Date | Completed |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

---

## 8. Results summary and statement of fitness

| Metric | Value |
|---|---|
| Total PQ scenarios | |
| Passed / Failed | |
| Deviations (critical / non-critical) | |
| URS-IDs prio=H covered / total | |

> [!quote] Statement of fitness for intended use (GAMP 5 §M7)
> *(Formal declaration)*: Based on the results of this PQ, the system **`{{system_name}}`** ☐ **is** / ☐ **is not** fit for its intended use (`{{intended_use_statement}}`) under real operating conditions.

**Conclusion**: ☐ Fit for intended use. ☐ Fit with non-critical deviations documented. ☐ Not fit — remediation required.

---

## 9. Appendix list (evidence)

| Appendix No. | Description | No. of pages |
|---|---|---|
|  |  |  |

---

## 10. Related documents

| Document | Reference |
|---|---|
| URS whose fitness is verified | `{{urs_ref}}` ([URS](URS.md)) |
| Risk Assessment | `{{ra_ref}}` ([RA-INIT](RA-INIT.md)) |
| Operational Qualification (pre-req) | `{{oq_ref}}` ([OQ](OQ.md)) |
| Validation Report (receives the fitness statement) | [VR](VR.md) |
| `{{custom_ref}}` |  |

---

## 11. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue |
|  |  |  |

---

## Canonical notes for implementers

> [!note] PQ verifies fitness, not function
> The PQ confirms fitness for intended use under real conditions with real users. If a PQ scenario merely repeats a functional test from the OQ, it is poorly designed: the PQ exercises complete end-to-end business processes.

> [!note] Executed by end users (not IT)
> This is the defining principle of the PQ: it demonstrates that the system works **in the hands of those who will use it**, not the technical team. That is why the Process Owner (not the System Owner) leads it.

> [!tip] The PQ feeds the Validation Report
> The statement of fitness for intended use (§8) is the key input to the [Validation Report](VR.md) (GAMP 5 §M7: *"a statement of fitness for intended use of the system"*).

> [!tip] Category awareness
> - **Cat 3/4/5**: the PQ always verifies end-to-end fitness. For simple systems it may be combined with the OQ (OP), but the fitness/end-user focus is maintained.

## Related

- [URS](URS.md) · [RA-INIT](RA-INIT.md) · [OQ](OQ.md) · [VR](VR.md)
- GAMP 5 · 21 CFR Part 11 · EU Annex 11
- V-Model · performance qualification · risk based testing

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.tests.from-ra` skill.

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer project. If it does not exist → redirect to `/gdd.init`.
2. **Locate the approved URS** (`specs/URS.md`) — source of requirements whose fitness is verified.
3. **Locate the approved RA-INIT** — scales the scenarios.
4. **Confirm the approved OQ** (`specs/OQ.md`) — prerequisite. If missing → warn.
5. **Read `templates/csv/PQ.md`** from the toolkit as the source template (this file).

### Generation flow

1. **Parse the URS-<CATEGORY>-NNN with prio=H** from the URS.
2. **Group requirements into end-to-end business processes** (not isolated functions) → each group becomes a `PQ-SCEN-NNN`.
3. **For each scenario**: cite the URS-IDs it covers + risk + end-user executor role + steps of the complete process.
4. **Scale depth** by Risk Priority.
5. **Generate the statement of fitness** (§8) linked to the intended_use from the URS.
6. **Anti-hallucination**: use `[NEEDS CLARIFICATION: ...]` when process information is missing; never invent results or declare fitness without evidence.
7. **Output**: write `specs/PQ.md` (status: draft); print coverage (URS prio=H covered / total).
8. **Post-flight**: `validate-frontmatter.py` + `check-clarification-markers.py` + `generate-rtm.py`.

### `status` transitions

```
draft ──[complete scenarios + approved + OQ approved]──> in-execution
in-execution ──[executed by end users + evidence]──> executed
executed ──[reviewer signs + deviations closed + fitness statement]──> approved
approved ──[new version issued]──> superseded
```

### Mapping

| Origin (PQ) | Destination | Rule |
|---|---|---|
| `PQ-SCEN-NNN` | Row in `RTM.md` | Fitness-for-intended-use coverage |
| Statement of fitness (§8) | `VR.md` | Key input to the Validation Report (GAMP 5 §M7) |
| PQ approved | V-Model closure | Final verification before the Validation Report |
