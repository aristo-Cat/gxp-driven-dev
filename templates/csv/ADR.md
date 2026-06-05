---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "ADR — Architecture Decision Record (canonical template)"
type: template
template_class: csv
template_id: "ADR"
template_version: "0.1.0"
v_model_phase: design-specification
gamp_categories_applicable: [4, 5]
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# ADR captures design decisions that shape the FS and DS. It is not a root
# document: it references URS requirements and/or FS entries it affects.
inputs:
  - template_id: "FS"
    required: false
    description: "Functional Specification — the ADR may resolve an open design question raised during FS authoring, or constrain how an FS requirement is realized."
  - template_id: "URS"
    required: false
    description: "User Requirements Specification — ADRs that affect GxP requirements must cite the impacted URS-<CATEGORY>-NNN so the decision is traceable to the requirement."
outputs:
  - artifact: "ADR instance (Markdown)"
    consumed_by:
      - "DS"        # Design Specification — accepted ADRs constrain DS choices
      - "FS"        # Functional Specification — ADRs may close FS open questions
      - "RTM"       # Requirements Traceability Matrix — accepted ADRs link to URS/FS IDs
applicable_regulations:
  - "gamp-5"        # §D3 (Design Specification) — design decisions must be documented and traceable; §M8 (Change Control) — superseded ADRs constitute the change record for design reversals
based_on:
  - "GAMP 5 §D3 (Design Specification — documenting and justifying design choices)"
  - "GAMP 5 §M8 (Change Control — rationale for design reversals must be retained)"
  - "Michael Nygard's Architecture Decision Records (ADR) format — context/decision/consequences pattern"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
    description: "Human-readable name of the system this ADR applies to (must match the source URS/FS if they exist)"
    example: "QC LIMS at site A"
  system_id:
    type: string
    required: true
    description: "Unique system identifier (same as the source URS/FS)"
  adr_id:
    type: string
    required: true
    description: "Unique identifier of this ADR following the pattern ADR-<CATEGORY>-NNN (e.g. ADR-ARCH-001, ADR-SEC-002)"
    example: "ADR-ARCH-001"
  adr_title:
    type: string
    required: true
    description: "Short descriptive title of the decision (≤80 characters)"
    example: "Use append-only audit-trail table instead of application-level logging"
  adr_author_name:
    type: string
    required: true
  adr_author_dept:
    type: string
    required: true
  decision_date:
    type: string
    required: false
    description: "ISO date when the decision was formally accepted (YYYY-MM-DD). Null while status is proposed."
  traces_to_urs:
    type: string
    required: false
    description: "Comma-separated list of URS-<CATEGORY>-NNN IDs whose realization is constrained by this decision"
    example: "URS-EREC-005, URS-SEC-001"
  traces_to_fs:
    type: string
    required: false
    description: "Comma-separated list of FS-<CATEGORY>-NNN IDs whose design is constrained by this decision"
    example: "FS-EREC-005, FS-DATA-003"
  org_csv_policy_ref:
    type: string
    required: false
  custom_ref:
    type: string
    required: false

# ─── ADR Status lifecycle ─────────────────────────────────────────────────────
# Each individual ADR block inside a document instance carries its own status.
# Allowed values: proposed | accepted | superseded
# An ADR instance file may contain multiple ADR-<CATEGORY>-NNN blocks at
# different statuses (e.g. ADR-ARCH-001 accepted, ADR-ARCH-002 proposed).
adr_status_values:
  proposed:
    meaning: "Decision is under evaluation — options are being weighed. No implementation may proceed on this ADR's scope."
    gate: "Author + at least one reviewer agree the context and options are complete."
  accepted:
    meaning: "Decision is final. Implementation may proceed. Cited URS/FS IDs are now constrained by this decision."
    gate: "Approver (System Owner or Quality Unit for GxP-impacting decisions) signs off."
  superseded:
    meaning: "A later ADR reversed or replaced this decision. The text is retained for audit continuity; a `superseded_by: ADR-<CAT>-NNN` field must be added."
    gate: "New ADR accepted; change-control note added to the superseded block."

# ─── INSTANCE frontmatter spec (not the template's) ─────────────────────────
instance_frontmatter_spec:
  required_fields:
    - title
    - type: "instance"
    - based_on_template: "ADR"
    - based_on_template_version
    - system_id
    - status              # draft | in-review | approved | superseded (document-level status)
    - version             # instance's own semver
    - created
    - updated
    - language
  conditional_fields:
    - traces_to: "URS and/or FS instance IDs + versions this ADR constrains — OPTIONAL: omit if the ADR is purely architectural with no direct URS/FS trace (see §0). Required for any ADR that constrains a GxP requirement (URS-<CAT>-NNN with GxP=Y)."
    - approved_by: "required if status == approved"
    - supersedes: "version of the previous ADR document if this is a new revision of the whole file"
    - decision_date: "required for any ADR block with status: accepted"
    - superseded_by: "required for any ADR block with status: superseded — cite the ADR-<CAT>-NNN that replaces it"

# ─── Validation rules ────────────────────────────────────────────────────────
validation_rules:
  - "Each ADR-<CATEGORY>-NNN block must have a Status, Context, Decision, and Consequences section"
  - "An ADR block with status: accepted must have a non-null decision_date"
  - "An ADR block with status: superseded must have a superseded_by field citing the replacing ADR-<CATEGORY>-NNN"
  - "Any ADR that constrains a GxP requirement (URS-<CATEGORY>-NNN with GxP=Y) must cite that ID in the 'Relates to' field"
  - "Options considered must include at least two alternatives plus a 'do nothing' / status-quo option where meaningful"
  - "The Decision Outcome must state the chosen option unambiguously — not 'we will consider' or 'it depends'"
  - "Consequences must list at least one Positive and at least one Negative/Risk entry"
  - "No ADR block may be deleted: superseded blocks are retained in full with status: superseded"
  - "Signature block must include an identified author; for GxP-impacting decisions, an approver from the Quality Unit or System Owner"

tags:
  - template
  - csv
  - adr
  - architecture-decision-record
  - design-specification
  - v-model
  - canonical
---

# ADR — Architecture Decision Record

> [!note] Canonical template
> **Canonical** template for producing **Architecture Decision Records (ADRs)** within the gxp-driven-dev toolkit. An ADR captures a significant architecture or design decision: its context, the options weighed, the decision taken, and its consequences — so the rationale survives for developers, reviewers, and (in regulated contexts) auditors. Aligned with GAMP 5 §D3 (Design Specification) and §M8 (Change Control). The toolkit itself dogfoods ADRs in `docs/decisions/` — this template is the consumer-facing, instantiable version.

> [!tip] Embedded usage rules
> 1. **One file, multiple ADRs** — a single ADR instance file may contain several `ADR-<CATEGORY>-NNN` blocks, each with its own status. Grouping related decisions (e.g. all security-architecture decisions under `ADR-SEC-NNN`) keeps context together without creating an unmanageable file explosion.
> 2. **Proposed before accepted** — no implementation may proceed on an ADR's scope until it reaches status: accepted. This mirrors the GAMP 5 principle that design decisions must be documented before implementation begins (§D3).
> 3. **No-deletion rule** — a superseded ADR block is **never deleted**. Mark it `status: superseded` + add `superseded_by: ADR-<CAT>-NNN`. Deletion breaks the design rationale audit trail.
> 4. **GxP-impact traceability** — any ADR that constrains the realization of a URS or FS requirement with GxP=Y must cite the affected IDs in the "Relates to" field. This makes the ADR visible in the RTM.
> 5. **Decision ≠ option description** — the Decision Outcome must name the chosen option clearly and state why it was chosen over the alternatives. Vague outcomes ("we will evaluate X going forward") are not valid.
> 6. **Consequences are mandatory** — positive outcomes, negative trade-offs, and residual risks must all be named. An ADR with only upsides is incompletely reasoned.
> 7. **Instantiation scope** — ADRs are Mode-B (develop) artifacts. They apply to Cat 4 and Cat 5 systems where design choices are non-trivial. For Cat 3 (standard products with minimal configuration), ADRs are optional unless a GxP-relevant configuration choice is made.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **URS impacted** | `{{traces_to_urs}}` *(leave blank if ADR is purely architectural with no direct URS trace)* |
| **FS entries impacted** | `{{traces_to_fs}}` *(leave blank if FS not yet authored)* |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Author | `{{adr_author_name}}` | `{{adr_author_dept}}` |  |  |
| Reviewer 1 (System Owner / Lead Developer) |  |  |  |  |
| Reviewer 2 (SME / Architect) |  |  |  |  |
| Approver (Quality Unit) *(required for GxP-impacting decisions)* |  |  |  |  |

> [!note] Who authors the ADR
> Typically the **lead developer**, **solution architect**, or **CSV Manager / Validation Coordinator** responsible for the design area in question. For GxP-impacting decisions (those that constrain a URS requirement with GxP=Y), a Quality Unit approver is required before the ADR may be accepted.

---

## 1. Introduction

This document records **Architecture Decision Records (ADRs)** for the system **`{{system_name}}`** (`{{system_id}}`). Each ADR captures one significant design decision with its context, the options weighed, the outcome chosen, and its consequences — so the rationale is preserved and auditable over the full lifecycle of the system.

According to GAMP 5 §D3, design decisions for computerized systems must be documented and traceable to the requirements they realize. ADRs complement the [Functional Specification](FS.md) and [Design Specification](DS.md) by capturing the **why** behind the **how**.

> [!note] Relationship to other specifications
> - **URS** defines the **what** (user requirements). ADRs do not repeat the what.
> - **FS** defines the **how** (functional realization). ADRs explain why a particular how was chosen over alternatives.
> - **DS** defines the technical detail. Accepted ADRs constrain the DS and must be cited in the DS where they apply.
> - **RTM** — ADRs affecting GxP requirements are referenced in the traceability matrix alongside the URS/FS IDs they constrain.

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| ADR | Architecture Decision Record — a record of a significant design decision with context, options, outcome, and consequences |
| ADR-<CATEGORY>-NNN | Unique identifier for an individual decision: category code + 3-digit sequence (e.g. ADR-ARCH-001) |
| Context | The forces, constraints, and circumstances that make a decision necessary |
| Decision drivers | The criteria — technical, regulatory, organizational — used to evaluate options |
| Proposed | ADR under evaluation — no implementation may proceed |
| Accepted | Decision finalized — implementation may proceed |
| Superseded | A later ADR has reversed or replaced this decision; retained for audit continuity |
| GAMP 5 | Good Automated Manufacturing Practice 5, ISPE 2022 |
| DS | Design Specification — detailed hw/sw design (GAMP 5 §D3) |
| FS | Functional Specification — the technical "how" that realizes the URS |
| RTM | Requirements Traceability Matrix |

---

## 3. ADR category codes

ADR IDs follow the pattern `ADR-<CATEGORY>-NNN`. The category mirrors the 22 canonical acronyms used across the toolkit (see `docs/requirement-id-scheme.md`), scoped to the design area the decision affects. Common categories for ADRs:

| Category code | Design area | Example |
|---|---|---|
| `ARCH` | Overall architecture / topology | Database engine, deployment model, layered vs micro |
| `DATA` | Data model / persistence | Schema design, ORM choice, data partitioning |
| `SEC` | Security architecture | Auth mechanism, encryption approach, secrets management |
| `API` | Interface design | REST vs GraphQL, versioning strategy, contract testing |
| `EREC` | Electronic records implementation | Audit trail mechanism, immutability strategy |
| `ESIG` | Electronic signature implementation | Signing flow, tamper-evidence mechanism |
| `PERF` | Performance architecture | Caching, pooling, async processing |
| `OPS` | Operational / infrastructure | Cloud vs on-prem, containerization, disaster recovery |
| `MIGR` | Data migration strategy | Tooling, verification, rollback |
| `TEST` | Testing strategy | Test framework, coverage targets, test environment |
| `DOCS` | Documentation architecture | Doc-as-code tooling, versioning |
| `UI` | UI architecture | SPA vs MPA, component library, accessibility approach |
| `DEVENV` | Development environment | Language runtime, build tooling, CI/CD pipeline |

Use the category that best fits the design area. If a decision spans multiple areas, pick the primary area and note the secondary in the "Relates to" field.

---

## 4. ADR log (index)

> [!tip] Maintain this table as the master index of all ADRs in this document
> Each accepted ADR constrains the implementation. A `validate-traceability` skill may use this table to verify that accepted ADRs are cited in the DS/FS where they apply.

| ADR-ID | Title (summary) | Status | Decision date | Relates to (URS/FS-IDs) |
|---|---|---|---|---|
| `ADR-ARCH-001` | *(title)* | proposed / accepted / superseded | YYYY-MM-DD |  |
|  |  |  |  |  |

---

## 5. Architecture Decision Records

> [!note] Per-ADR block structure
> Each ADR block below follows the same structure. Copy the block for each new decision. Do not delete superseded blocks.

---

### ADR-`{{adr_id}}` — `{{adr_title}}`

**Status:** `proposed` *(change to `accepted` or `superseded` when appropriate)*
**Decision date:** *(null while proposed; fill with YYYY-MM-DD when accepted)*
**Relates to:** `{{traces_to_urs}}` · `{{traces_to_fs}}`

> [!warning] Status: proposed — no implementation may proceed
> This ADR is under evaluation. The decision has not been accepted. No code, configuration, or documentation that depends on this decision may be considered final until the status changes to `accepted`.

*(Replace the above callout with the appropriate status callout when status changes — see Status callouts below.)*

#### 5.x.1 Context

> Describe the situation that makes this decision necessary: the technical or regulatory constraints, the quality attributes at stake, and the forces that pull in different directions. Write as if explaining to a senior engineer who is unfamiliar with this system.

`[NEEDS CLARIFICATION: Describe the context, constraints, and driving forces here.]`

#### 5.x.2 Decision drivers

| Driver | Type | Weight (H/M/L) |
|---|---|---|
| *(e.g. Audit trail integrity — mandatory for GxP systems)* | Regulatory | H |
| *(e.g. Minimal operational overhead)* | Operational | M |
| *(e.g. Team familiarity with technology)* | Organizational | L |
|  |  |  |

#### 5.x.3 Considered options

> [!note] Always include at least two substantive alternatives plus a "do nothing" / status-quo option where meaningful

##### Option A — *(name)*

*(Description: what this option entails in concrete terms.)*

| Pros | Cons |
|---|---|
| *(pro)* | *(con)* |
| *(pro)* | *(con)* |

##### Option B — *(name)* *(recommended)*

*(Description: what this option entails in concrete terms.)*

| Pros | Cons |
|---|---|
| *(pro)* | *(con)* |
| *(pro)* | *(con)* |

##### Option C — *(name)* *(rejected)*

*(Description: what this option entails in concrete terms.)*

| Pros | Cons |
|---|---|
| *(pro)* | *(con)* |
| *(pro)* | *(con)* |

#### Comparison matrix

| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| *(Decision driver 1)* | Low | High | Medium |
| *(Decision driver 2)* | High | Medium | Low |
| *(Regulatory fit)* | Medium | High | Low |
| **Overall fit** | **Low** | **High** | **Low** |

#### 5.x.4 Decision outcome

> [!tip] State the chosen option unambiguously
> Name the option chosen, the primary reason it was selected, and any conditions or constraints that apply to the implementation.

**Chosen option: Option `[X]` — *(name).***

*(Explanation: why this option was chosen over the others. Cite the dominant decision drivers. Be specific — "it best satisfies the regulatory requirements for audit-trail immutability while keeping operational overhead manageable" is better than "it is the best balance.")*

#### 5.x.5 Consequences

##### Positive

- *(What becomes better, easier, or more compliant as a result of this decision.)*
- *(e.g. Full audit trail immutability at the DB level satisfies URS-EREC-005 without relying on application-layer controls.)*

##### Negative / trade-offs

- *(What becomes harder, more expensive, or more constrained as a result of this decision.)*
- *(e.g. The append-only schema requires a separate compaction/archival process for long-running systems.)*

##### Risks

| Risk | Likelihood (H/M/L) | Impact (H/M/L) | Mitigation |
|---|---|---|---|
| *(e.g. Schema changes to the audit table require migration scripts and re-validation)* | L | H | *(Change-control process + test coverage for migration)* |
|  |  |  |  |

#### 5.x.6 Relates to

| Reference type | ID | Description |
|---|---|---|
| URS requirement constrained | `URS-...-NNN` | *(one-line summary of the requirement)* |
| FS entry constrained | `FS-...-NNN` | *(one-line summary of the realization)* |
| Related ADR | `ADR-...-NNN` | *(related decision — cite if this ADR depends on or is superseded by another)* |
|  |  |  |

---

### Status callouts (copy-paste the appropriate one)

> [!note] Status: PROPOSED — decision under evaluation; no implementation may proceed until accepted.

> [!tip] Status: ACCEPTED — decision is final; implementation may proceed. Implementation must comply with the Decision Outcome and Consequences above.

> [!warning] Status: SUPERSEDED by `ADR-<CATEGORY>-NNN` — this decision has been reversed or replaced. The text is retained for audit continuity. Do not implement based on this block.

---

## 6. Related documents

| Document | Reference |
|---|---|
| Functional Specification | [FS](FS.md) — `{{traces_to_fs}}` |
| User Requirements Specification | [URS](URS.md) — `{{traces_to_urs}}` |
| Design Specification | [DS](DS.md) *(accepted ADRs must be cited in the DS where they constrain design)* |
| Requirements Traceability Matrix | [RTM](RTM.md) |
| Organization's CSV Policy | `{{org_csv_policy_ref}}` |
| `{{custom_ref}}` |  |

---

## 7. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{adr_author_name}}`, `{{adr_author_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] ADRs are the design rationale layer of the V-Model
> The V-Model traces requirements from URS → FS → DS/CS → Test specs. ADRs sit orthogonal to this chain: they document **why** the FS and DS were designed as they are. Each accepted ADR should be cited in the DS or FS section it constrains, so a reviewer can navigate from a design decision back to its rationale and forward to its test evidence.

> [!note] GAMP 5 regulatory anchoring
> GAMP 5 §D3 requires that design decisions for computerized systems are documented, justified, and traceable. ADRs are the lightest-weight artifact that satisfies this requirement. For GxP-impacting decisions (those constraining a URS requirement with GxP=Y), the ADR must be approved by the Quality Unit before implementation begins — this is the Design Review gate described in §D3. §M8 (Change Control) applies when an accepted ADR is superseded: the reversal must be documented, and the prior decision retained for audit continuity.

> [!note] The toolkit dogfoods its own ADRs
> The toolkit itself records architectural decisions in `docs/decisions/ADR-NNN-*.md` (instance format, not this template). When the toolkit evolves a convention that consumers depend on (e.g., changing the ID scheme, adding a new template phase), an ADR is filed. This template is the consumer-facing, audit-grade version of the same practice.

> [!tip] Natural outputs of an accepted ADR
> - A cited constraint in the relevant DS/FS section: "This design follows ADR-ARCH-001 (accepted YYYY-MM-DD)."
> - A row in the RTM linking the URS/FS IDs to the decision for full traceability.
> - A supersession note in the old ADR block if a prior decision is reversed (GAMP 5 §M8 change record).

## Related

- [FS](FS.md) · [DS](DS.md) · [URS](URS.md) · [RTM](RTM.md)
- GAMP 5
- V-Model · design specification · specification traceability

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.adr.from-design-question` skill.

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer project. If it does not exist → redirect to `/gdd.init`.
2. **Confirm mode: develop** — ADRs are a Mode-B (develop) artifact. If mode is `validate`, ADRs are optional; note this to the user.
3. **Locate the FS instance** (`specs/FS.md`) and URS instance (`specs/URS.md`) if they exist. Read them to understand which URS/FS IDs may be constrained by the incoming decision.
4. **Read `templates/csv/ADR.md`** from the toolkit as the source template (this file).
5. **Identify the GAMP category** from `.gxp-dev.yaml`. For Cat 3, prompt the user whether an ADR is warranted; for Cat 4/5, proceed directly.

### Generation flow

1. **Elicit the design question** — ask the user (or parse the prompt) for:
   - The design area / category (ARCH, DATA, SEC, API, EREC, …).
   - A short title for the decision (≤80 chars).
   - Whether any URS or FS IDs are directly constrained.
2. **Determine the target file**:
   - If `specs/ADR.md` already exists → append a new ADR block to it. Update the ADR log (section 4).
   - If it does not exist → create `specs/ADR.md` from this template, filling identity + signatures.
3. **Assign the ADR-ID**: `ADR-<CATEGORY>-NNN` where NNN is the next sequential number within that category in the document.
4. **Draft the ADR block**:
   - **Context**: summarize the forces, constraints, and technical landscape. Insert `[NEEDS CLARIFICATION: …]` for any information the agent cannot determine from the available specs.
   - **Decision drivers**: identify 2–4 drivers weighted H/M/L; for GxP-impacting decisions, always include a regulatory driver.
   - **Considered options**: generate at least 2 substantive alternatives + a "do nothing" option. Evaluate each against the decision drivers.
   - **Comparison matrix**: fill the table with the options vs. criteria.
   - **Decision outcome**: state the recommended option. If the user has already indicated a preference, record it as `accepted`; otherwise set `proposed` and ask the user to confirm.
   - **Consequences**: list positive outcomes, negative trade-offs, and at least one risk row.
   - **Relates to**: populate URS/FS IDs if they exist.
5. **Anti-hallucination**: never invent regulatory §-citations beyond GAMP 5 §D3 and §M8. Do not invent technical mechanisms or vendor features. Insert `[NEEDS CLARIFICATION: …]` for unknowns.
6. **Output**: write/update `specs/ADR.md` (status of the new block: `proposed` by default); print summary of ADR-ID, title, category, and the URS/FS IDs it relates to.
7. **Post-flight**: run `validate-frontmatter.py` + `check-clarification-markers.py`.

### Stop criteria ("complete" ADR block)

- [ ] Status field is one of: proposed | accepted | superseded
- [ ] Context explains the forces and constraints clearly (no generic placeholder text)
- [ ] At least two substantive options considered (+ do-nothing where applicable)
- [ ] Decision Outcome names the chosen option unambiguously
- [ ] At least one Positive and one Negative/Risk consequence listed
- [ ] Any GxP-impacting decision cites the affected URS-<CATEGORY>-NNN in "Relates to"
- [ ] ADR-ID added to the ADR log (section 4)
- [ ] If accepted: decision_date is set and approver signature row is present
- [ ] If superseded: superseded_by field names the replacing ADR-<CATEGORY>-NNN

### `status` transitions (per ADR block)

```
proposed ──[context + options complete; reviewer confirms]──> accepted
accepted ──[new design decision reverses this one]──> superseded (new ADR-<CAT>-NNN accepted)
```

### Downstream mapping — how ADRs trace to DS/FS/RTM

| Origin (ADR) | Destination | Cardinality | Rule |
|---|---|---|---|
| `ADR-<CATEGORY>-NNN` (accepted) | Cited in `DS.md` or `FS.md` section | 1:N | Every DS/FS section whose design is constrained by the ADR must cite it |
| `ADR-<CATEGORY>-NNN` (GxP-impacting) | Row in `RTM.md` | 1:1 | The RTM links the constrained URS/FS IDs to the accepted ADR |
| `ADR-<CATEGORY>-NNN` (superseded) | Retained in the ADR file | — | GAMP 5 §M8: design reversals must be auditable; do not delete |
