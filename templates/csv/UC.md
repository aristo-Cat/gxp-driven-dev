---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "UC — Use Case (canonical CSV template)"
type: template
template_class: csv
template_id: "UC"
template_version: "0.1.0"
v_model_phase: requirements-definition
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# UC elaborates URS-FUNC requirements into concrete user flows.
# Not a root: depends on URS.
inputs:
  - template_id: "URS"
    required: true
    description: "Approved (or at minimum in-review) User Requirements Specification — source of all URS-FUNC-NNN that this UC elaborates. Each use case block must cite at least one URS-FUNC-NNN."
outputs:
  - artifact: "UC instance (Markdown)"
    consumed_by:
      - "FS"          # Functional Specification — UC flows inform the functional design
      - "OQ"          # OQ test cases — each UC main-success-flow step maps to ≥1 test case
      - "PQ"          # PQ scenarios — each UC scenario can become a PQ real-world scenario
      - "RTM"         # Requirements Traceability Matrix — UC ↔ URS-FUNC ↔ OQ/PQ
applicable_regulations:
  - "gamp-5"          # §D1 (Specifying Requirements) — UC is a supplemental view of URS-FUNC

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
    description: "Human-readable name of the system (must match the source URS)"
    example: "QC LIMS at site A"
  system_id:
    type: string
    required: true
    description: "Unique system identifier (same as in the source URS)"
  urs_ref:
    type: string
    required: true
    description: "Identifier + version of the URS instance that this UC document elaborates"
    example: "URS-PROJ-2026-001 v1.0 (approved)"
  uc_author_name:
    type: string
    required: true
  uc_author_dept:
    type: string
    required: true
  scope_narrative:
    type: string
    required: true
    description: "One-paragraph description of which user goals and actors are covered by this UC document"
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
    - based_on_template: "UC"
    - based_on_template_version
    - system_id
    - traces_to            # URS instance ID + version (at minimum in-review)
    - status               # draft | in-review | approved | superseded
    - version              # instance's own semver
    - created
    - updated
    - language
  conditional_fields:
    - approved_by: "required if status == approved"
    - supersedes: "version of the previous UC document if this is a new revision"

# ─── Validation rules ────────────────────────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "Each UC block must declare exactly one UC-FUNC-NNN identifier"
  - "Each UC block must cite at least one URS-FUNC-NNN in the 'Covers' field"
  - "Each UC block must have a non-empty Actor, at least one Precondition, a Main success flow with ≥2 numbered steps, and at least one Postcondition"
  - "Main success flow steps must alternate: odd steps are Actor actions; even steps are System responses (or annotated explicitly)"
  - "At least one Alternate / exception flow per UC block must be present (even if marked N/A with rationale)"
  - "Traceability note at the end of each UC block must reference the UC-FUNC-NNN → URS-FUNC-NNN link and the downstream OQ/PQ link"
  - "Signature block must include an identified author + at least one reviewer (Process Owner or SME)"

tags:
  - template
  - csv
  - uc
  - use-case
  - requirements-definition
  - v-model
  - canonical
---

# UC — Use Case

> [!note] Canonical CSV template
> **Canonical** template for producing the **Use Case (UC)** document of a computerized system. A UC captures a **user-goal-level interaction** between an actor (end-user role) and the system: preconditions, a numbered main success flow (actor action → system response), alternate and exception flows, and postconditions. UC blocks elaborate `URS-FUNC` requirements into concrete interaction sequences and feed [OQ](OQ.md) functional test cases and [PQ](PQ.md) real-world scenarios. Complies with GAMP 5 §D1 (Specifying Requirements) as a supplemental view of the [URS](URS.md).

> [!tip] Embedded usage rules
> 1. **Relationship to URS-FUNC** — a UC *elaborates* a URS-FUNC requirement into a concrete interaction: it describes the conversation between an actor and the system, step by step. It does not replace the URS or the FS; it sits alongside them as a behavioral view.
> 2. **One UC block per user goal** — each `UC-FUNC-NNN` block describes one coherent user goal (e.g. "record a measurement result"). If a URS-FUNC requirement covers multiple distinct user goals, create one UC block per goal and reference the same URS-FUNC-NNN from each.
> 3. **Main flow format** — steps alternate: odd steps are actor actions; even steps are system responses. Number them `1.`, `2.`, `3.`, etc. This alternation makes gaps visible and maps naturally to OQ test case steps.
> 4. **Alternate / exception flows** — label them `A1`, `A2`, `E1`, `E2`. At step N where the deviation occurs, reference the label: `→ [A1]`. If genuinely no alternate or exception exists, state `N/A — single success path only` with brief rationale; do not leave the field blank.
> 5. **Postconditions = testable assertions** — postconditions are the basis for OQ pass/fail criteria. Write them as observable, testable system states (e.g. "The record is stored in the database with status = 'draft' and an audit-trail entry is created").
> 6. **Traceability** — every UC block must end with a traceability note linking `UC-FUNC-NNN → URS-FUNC-NNN` (backward) and `UC-FUNC-NNN → OQ-TC-NNN / PQ-SCEN-NNN` (forward). The forward link may be `[TBD]` until OQ/PQ are authored.
> 7. **No-deletion rule** — an obsolete UC block is **not** deleted: strike it through (`~~UC-FUNC-007 …~~`) and note the reason. Deleting breaks downstream traceability to OQ/PQ/RTM.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **URS being elaborated** | `{{urs_ref}}` |
| **Scope of this UC document** | `{{scope_narrative}}` |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Author | `{{uc_author_name}}` | `{{uc_author_dept}}` |  |  |
| Reviewer 1 (Process Owner / SME) |  |  |  |  |
| Reviewer 2 (Quality Unit) |  |  |  |  |
| Approver (System Owner) |  |  |  |  |

> [!note] Who authors the UC
> Typically a **Business Analyst**, **CSV Manager**, or **Process Owner** — someone who understands both user workflows and the system's intended behavior. The UC is reviewed by the Process Owner (or SME) and optionally by the Quality Unit. Approval level depends on the organization's CSV Policy; for GAMP Cat 4/5 the UC is usually approved together with or immediately after the URS.

---

## 1. Introduction

This **Use Case (UC)** document elaborates the functional user interactions defined in the [URS](URS.md) (`{{urs_ref}}`) for the system **`{{system_name}}`**. Each `UC-FUNC-NNN` block describes a single user goal: who initiates it (the actor), under what preconditions, the sequence of steps (main success flow), deviations (alternate/exception flows), and the observable system state after completion (postconditions).

According to GAMP 5 §D1, UCs are one recognized technique for capturing and communicating user requirements as behavioral interactions. This document is a **supplemental requirements view**, not a replacement for the URS or the FS. It feeds:

- **[OQ](OQ.md)** — each main success flow step maps to ≥1 OQ test case, ensuring functional coverage.
- **[PQ](PQ.md)** — each complete UC scenario (including realistic preconditions and actor data) maps to a PQ scenario.
- **[RTM](RTM.md)** — the UC serves as a bridge: `URS-FUNC-NNN → UC-FUNC-NNN → OQ-TC-NNN / PQ-SCEN-NNN`.

**Scope of this UC document**: `{{scope_narrative}}`

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| UC | Use Case — a goal-level description of actor–system interaction |
| Actor | An end-user role (not a named individual) interacting with the system to achieve a goal |
| Main success flow | The primary sequence of steps when everything works as expected (the "happy path") |
| Alternate flow | A valid deviation from the main flow that still achieves the user goal (e.g. choosing an optional sub-step) |
| Exception flow | A failure or error condition that prevents the user goal from being completed normally |
| Precondition | System or user state that must be true before the use case can begin |
| Postcondition | Observable, testable state of the system after the use case completes successfully |
| URS | User Requirements Specification — the "what" from the user's perspective |
| FS | Functional Specification — the technical "how" that realizes the URS |
| OQ | Operational Qualification — functional verification phase of the V-Model |
| PQ | Performance Qualification — real-world scenario verification phase of the V-Model |
| GAMP 5 | Good Automated Manufacturing Practice 5, ISPE 2022 |
|  |  |

---

## 3. UC identifier scheme

Each use case block is identified as `UC-FUNC-NNN`:

| Segment | Value |
|---|---|
| `UC` | Document type — Use Case (matches `<DOC-TYPE>` in `docs/requirement-id-scheme.md`) |
| `FUNC` | Category — use cases elaborate functional requirements; always `FUNC` unless the UC is specifically about performance interactions (`PERF`) |
| `NNN` | Sequential, 3-digit, zero-padded, per document (`001`, `002`, …) |

> [!note] Why only FUNC (and optionally PERF)?
> Use cases capture behavioral user goals, which are functional in nature. Non-functional requirements (security, performance thresholds, data retention, etc.) are better expressed as quality attributes in the URS-<CATEGORY> tables — not as actor–system interaction flows. If a use case specifically models a performance-critical interaction (e.g. "operator runs a bulk report and observes response within 2 s"), it may carry the `PERF` category. All other categories remain in the URS.

---

## 4. Use case blocks

> [!tip] One block per user goal
> Each subsection below is one use case. Copy the structure for each additional UC. The blocks are numbered sequentially: `UC-FUNC-001`, `UC-FUNC-002`, etc. Do not skip numbers; strike through obsolete blocks.

---

### UC-FUNC-001 — `[User goal in 5–8 words]`

**Covers:** `URS-FUNC-NNN` *(list all URS-FUNC IDs this UC elaborates; ≥1 required)*

**Actor:** `[End-user role — e.g. "QC Analyst", "Lab Operator", "System Administrator"]`
*(Use a role, never a named person. Roles must match those defined in the URS or in `wiki/roles/`.)*

#### Preconditions

> [!note] Preconditions are observable system / actor states that must hold before step 1 begins.

- P1. `[e.g. "The actor is authenticated and holds the 'QC Analyst' role in the system."]`
- P2. `[e.g. "The sample record referenced in the task exists in the system with status = 'pending analysis'."]`
- P3. *(add as needed)*

#### Main success flow

> [!tip] Odd steps = actor actions; even steps = system responses. Use present tense. Be specific but implementation-neutral.

| Step | Actor / System | Description |
|---|---|---|
| 1 | Actor | `[e.g. "The actor navigates to the 'Sample Analysis' module and selects the pending sample from the worklist."]` |
| 2 | System | `[e.g. "The system displays the sample details form populated with the sample metadata and an empty results entry area."]` |
| 3 | Actor | `[e.g. "The actor enters the measurement result values and selects the applicable test method."]` |
| 4 | System | `[e.g. "The system validates the entered values against the configured acceptance criteria and highlights any out-of-range fields."]` |
| 5 | Actor | `[e.g. "The actor confirms the entry and submits the record."]` |
| 6 | System | `[e.g. "The system saves the record with status = 'draft', timestamps the entry (server-side), attributes it to the actor's user ID, and creates an audit-trail entry capturing the action, old value, new value, timestamp, and actor identity."]` |
| *(add steps as needed)* | | |

#### Alternate flows

| Label | At step | Condition | Alternate path |
|---|---|---|---|
| A1 | 3 | `[e.g. "Actor enters a value outside the acceptance range but within a configurable extended range."]` | `[e.g. "System highlights the field in amber and displays an alert. Actor may proceed by entering a mandatory justification comment. Flow continues at step 5."]` |
| A2 | *(step)* | *(condition)* | *(path)* |

#### Exception flows

| Label | At step | Condition | Exception path |
|---|---|---|---|
| E1 | 5 | `[e.g. "Actor's session has expired before submission."]` | `[e.g. "System displays a session-timeout error. The partially entered data is not persisted. Actor must re-authenticate and re-enter the record. UC ends without completion."]` |
| E2 | 4 | `[e.g. "System detects a duplicate result entry for the same sample and test method."]` | `[e.g. "System blocks the submission and displays an error message identifying the existing record. Actor must review and either cancel or initiate a correction workflow. UC ends without completion at this attempt."]` |
| E3 | *(step)* | *(condition)* | *(path)* |

> [!note] If no alternate or exception flows exist, state: `N/A — single success path only. Rationale: [brief reason].` Do not leave blank.

#### Postconditions

> [!tip] Postconditions are testable assertions about the system state after the use case completes successfully. These become OQ pass/fail criteria.

- PC1. `[e.g. "A result record exists in the system linked to the sample, carrying the actor's user ID, a server-side timestamp, and status = 'draft'."]`
- PC2. `[e.g. "An audit-trail entry for the creation event is persisted and is read-only."]`
- PC3. *(add as needed)*

#### Traceability note

| Link direction | Reference |
|---|---|
| UC-FUNC-001 elaborates | `URS-FUNC-NNN` *(cite the covered IDs)* |
| UC-FUNC-001 is tested by (OQ) | `OQ-TC-NNN` *(or `[TBD — OQ not yet authored]`)* |
| UC-FUNC-001 maps to (PQ) | `PQ-SCEN-NNN` *(or `[TBD — PQ not yet authored]`)* |

---

### UC-FUNC-002 — `[User goal in 5–8 words]`

**Covers:** `URS-FUNC-NNN`

**Actor:** `[End-user role]`

#### Preconditions

- P1. `[Precondition]`
- P2. *(add as needed)*

#### Main success flow

| Step | Actor / System | Description |
|---|---|---|
| 1 | Actor | `[Actor action]` |
| 2 | System | `[System response]` |
| 3 | Actor | `[Actor action]` |
| 4 | System | `[System response]` |
| *(add steps as needed)* | | |

#### Alternate flows

| Label | At step | Condition | Alternate path |
|---|---|---|---|
| A1 | *(step)* | *(condition)* | *(path)* |

#### Exception flows

| Label | At step | Condition | Exception path |
|---|---|---|---|
| E1 | *(step)* | *(condition)* | *(path)* |

#### Postconditions

- PC1. `[Testable system state]`
- PC2. *(add as needed)*

#### Traceability note

| Link direction | Reference |
|---|---|
| UC-FUNC-002 elaborates | `URS-FUNC-NNN` |
| UC-FUNC-002 is tested by (OQ) | `[TBD — OQ not yet authored]` |
| UC-FUNC-002 maps to (PQ) | `[TBD — PQ not yet authored]` |

---

> [!note] Add one subsection per additional use case following the same structure. Increment the ID sequentially: `UC-FUNC-003`, `UC-FUNC-004`, etc.

---

## 5. UC → URS-FUNC traceability matrix

> [!tip] Master index of backward coverage
> This table is the master index of backward traceability: every `URS-FUNC-NNN` that this UC document elaborates must appear here. A `validate-traceability` skill uses this table to detect gaps (URS-FUNC requirements with no UC elaboration and no rationale for omission).

| UC-ID | User goal (summary) | URS-FUNC-ID(s) covered | Actor | GxP | Prio |
|---|---|---|---|---|---|
| `UC-FUNC-001` | `[Goal summary]` | `URS-FUNC-NNN` | `[Role]` | *(inherited from URS)* | *(inherited from URS)* |
| `UC-FUNC-002` | `[Goal summary]` | `URS-FUNC-NNN` | `[Role]` | | |
|  |  |  |  |  |  |

**Coverage note:** URS-FUNC requirements not elaborated by any UC:

| URS-FUNC-ID | Reason not covered by a UC | Acceptable? |
|---|---|---|
| `URS-FUNC-NNN` | *[e.g. "Non-interactive background process — no actor goal. Verified directly in OQ."]* | Y / N |
|  |  |  |

---

## 6. UC → OQ / PQ forward traceability

> [!tip] Forward traceability to the right side of the V-Model
> Each UC block drives at least one OQ test case (functional verification). High-priority UCs with real-world data additionally drive PQ scenarios. This table is the master forward link; it is populated iteratively as OQ/PQ are authored.

| UC-ID | OQ test case(s) | PQ scenario(s) | Notes |
|---|---|---|---|
| `UC-FUNC-001` | `OQ-TC-NNN` | `PQ-SCEN-NNN` | |
| `UC-FUNC-002` | `[TBD]` | `[TBD]` | *OQ not yet authored* |
|  |  |  |  |

---

## 7. Related documents

| Document | Reference |
|---|---|
| URS elaborated by this UC | `{{urs_ref}}` ([URS](URS.md)) |
| Functional Specification | [FS](FS.md) |
| Operational Qualification | [OQ](OQ.md) |
| Performance Qualification | [PQ](PQ.md) |
| Requirements Traceability Matrix | [RTM](RTM.md) |
| Organization's CSV Policy | `{{org_csv_policy_ref}}` |
| `{{custom_ref}}` |  |

---

## 8. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{uc_author_name}}`, `{{uc_author_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] The UC is a behavioral bridge, not a specification layer
> The UC does not add requirements that are not already in the URS. Its value is in **making the interaction concrete**: who does what, in what sequence, under what conditions. If a UC step reveals a requirement gap in the URS, the gap must be addressed in the URS (via change control) — not patched in the UC.

> [!note] Category-awareness — UC depth by GAMP category
> - **Cat 3** (standard product): UCs may be lightweight or entirely omitted if the vendor provides equivalent flow documentation. Reference supplier documentation instead.
> - **Cat 4** (configured product): UCs are useful for documenting configuration-driven workflows that differ from the standard product behavior.
> - **Cat 5** (custom software): UCs are highly recommended. Each `URS-FUNC-NNN` with GxP=Y should have a corresponding UC block to drive OQ test case design.

> [!note] UC vs Acceptance Criteria (AC)
> UCs and [Acceptance Criteria](AC.md) are complementary. A UC describes *how* the user interacts with the system (the flow). An AC describes *what the system must do* to be considered done (a verifiable condition). In Agile contexts, user stories + AC pairs can replace or augment UCs; in formal CSV contexts, UCs + OQ test cases are the standard path.

> [!tip] Natural output of this template
> A well-authored UC document produces: (a) a full behavioral inventory of the system's user goals, (b) clear OQ test case outlines (the main flow steps map directly to test steps), and (c) PQ scenario stubs (each UC with realistic precondition data becomes a PQ scenario). The [RTM](RTM.md) closes the loop: `URS-FUNC → UC-FUNC → OQ-TC / PQ-SCEN`.

## Related

- [URS](URS.md) · [FS](FS.md) · [AC](AC.md) · [OQ](OQ.md) · [PQ](PQ.md) · [RTM](RTM.md)
- GAMP 5
- V-Model · use case · specification traceability

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.uc.from-urs` skill.

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer project. If it does not exist → redirect to `/gdd.init`.
2. **Locate the URS instance** (`specs/URS.md`). Status must be `in-review` or `approved` — a UC may be drafted in parallel with the URS review, but must not precede URS creation.
3. **Read `templates/csv/UC.md`** from the toolkit as the source template (this file).
4. **Read `specs/FS.md` if it exists** — a partially authored FS provides additional context about which functional areas are most complex and may benefit from more detailed UC flows.

### Generation flow (cascade from URS-FUNC)

1. **Parse all `URS-FUNC-NNN`** from the URS, with their Actor (if stated), GxP (Y/N), and prio (H/M/L).
2. **Group by actor / user role** — URS-FUNC requirements for the same actor and related goal should be grouped into one or a small number of UC blocks.
3. **For each user goal**, draft a `UC-FUNC-NNN` block:
   - **Identify the actor** from the URS-FUNC text or from the `roles/` section of the URS. If ambiguous, insert `[NEEDS CLARIFICATION: actor role not specified in URS-FUNC-NNN]`.
   - **Derive preconditions** from the URS requirement context (authentication state, prior workflow state, data existence). Insert `[NEEDS CLARIFICATION: ...]` when not determinable.
   - **Draft the main success flow** as alternating actor/system steps, tracing the happy path described in the URS-FUNC text. Use present tense, be specific but implementation-neutral.
   - **Derive at least one alternate and one exception flow** from the URS text (error messages, validation rules, access control). If the URS does not describe exceptions, flag: `[NEEDS CLARIFICATION: exception flows for URS-FUNC-NNN not specified — please confirm or add to URS]`.
   - **Draft postconditions** as testable system states that mirror the URS-FUNC acceptance criteria (if present) or derive them from the main flow's final system response.
   - **Populate the traceability note** with the covered URS-FUNC-NNN IDs; mark OQ/PQ forward links as `[TBD]`.
4. **Populate section 5** (UC → URS-FUNC traceability matrix) as the backward coverage index.
5. **Anti-hallucination**: insert `[NEEDS CLARIFICATION: ...]` whenever there is insufficient information to describe a step, precondition, or postcondition. Never invent actor workflows or system behaviors that are not grounded in the URS or FS.
6. **Output**: write `specs/UC.md` (status: draft); print a summary listing UC blocks created, URS-FUNC IDs covered, and any NEEDS CLARIFICATION markers requiring human input.
7. **Post-flight**: run `validate-frontmatter.py` + `check-clarification-markers.py` + `generate-rtm.py` (to verify backward coverage of URS-FUNC requirements).

### Stop criteria ("complete" instance)

- [ ] `traces_to` points to a URS instance with status `in-review` or `approved`
- [ ] Every `URS-FUNC-NNN` with GxP=Y has ≥1 `UC-FUNC-NNN` that covers it, or a documented rationale for omission in section 5
- [ ] Every `UC-FUNC-NNN` block has: Actor, ≥1 Precondition, Main success flow with ≥2 steps, ≥1 Alternate or Exception flow (or `N/A` with rationale), ≥1 Postcondition, Traceability note
- [ ] Section 5 (backward traceability matrix) is populated
- [ ] 0 blank `[NEEDS CLARIFICATION: ...]` markers that are blocking (actor, main flow step, or postcondition level)
- [ ] Signature block with ≥1 author + ≥1 reviewer

### `status` transitions

```
draft ──[all GxP URS-FUNC covered + 0 blocking gaps]──> in-review
in-review ──[approver signatures applied]──> approved
approved ──[new version issued]──> superseded
```

### Downstream mapping — how the UC traces to OQ / PQ / RTM

| Origin (UC) | Destination | Cardinality | Rule |
|---|---|---|---|
| `UC-FUNC-NNN` main flow step N | Test step in `OQ-TC-NNN` | 1:N | Each actor action + system response pair maps to ≥1 OQ test step |
| `UC-FUNC-NNN` (prio=H, GxP=Y) | `PQ-SCEN-NNN` in `PQ.md` | 1:1 | High-priority UCs with real-world precondition data become PQ scenarios |
| `UC-FUNC-NNN` postconditions | OQ pass/fail criteria | 1:N | Postconditions are directly used as expected results in OQ test cases |
| `UC-FUNC-NNN` | Row in `RTM.md` | 1:1 | RTM records the URS-FUNC → UC-FUNC → OQ-TC / PQ-SCEN chain |
