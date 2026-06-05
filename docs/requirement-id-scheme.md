# Requirement ID Scheme — `gxp-driven-dev`

This document defines the **canonical naming scheme** used throughout `gxp-driven-dev` for identifying requirements, specs, qualifications, tests, change controls, incidents and any other auditable artifact produced by the toolkit.

The scheme is **format-stable**, **machine-parseable**, **diff-friendly in Git**, and **traceable across the entire V-Model lifecycle**.

---

## Format

```
<DOC-TYPE>-<CATEGORY>-<NNN>
```

Three segments, separated by hyphens, joined together for a single stable identifier.

| Segment | What it is | Example |
|---|---|---|
| `<DOC-TYPE>` | The document family that owns this identifier (also the file prefix where the instance lives) | `URS`, `FS`, `DS`, `IQ`, `OQ`, `PQ`, `RA-INIT`, `RA-DET`, `PR`, `CC`, `IR`, `TC`, `SCEN` |
| `<CATEGORY>` | One of the 22 canonical categories (see table below). Mandatory in URS/FS/DS; optional in test cases | `FUNC`, `PERF`, `EREC`, `ESIG`, `SEC`, `API`, … |
| `<NNN>` | Sequential, 3 digits zero-padded, starting at `001`. Each `<DOC-TYPE>-<CATEGORY>` combination has its own counter. | `001`, `042`, `127` |

### Examples

| Identifier | Meaning |
|---|---|
| `URS-FUNC-001` | Functional requirement #1 of the User Requirements Spec |
| `URS-EREC-007` | Electronic Records requirement #7 of the URS (21 CFR Part 11 anchor) |
| `FS-API-002` | API/Interface design point #2 of the Functional Specification, implementing one or more URS-API requirements |
| `DS-DATA-005` | Data structure design point #5 of the Design Specification |
| `IQ-TC-042` | Installation Qualification test case #42 |
| `OQ-TC-021` | Operational Qualification test case #21 |
| `PQ-SCEN-007` | Performance Qualification scenario #7 |
| `RA-INIT-001` | Initial Risk Assessment finding #1 |
| `RA-DET-014` | Detailed Risk Assessment FMEA row #14 |
| `CC-2026-038` | Change Control record #38 of year 2026 (variant: includes year) |
| `IR-2026-012` | Incident Record #12 of 2026 |

---

## The 22 canonical categories

These are the **canonical building blocks** of requirement classification. Each describes one cohesive area of requirements that a regulated computerized system must address. The 22-category set is intentionally fixed at this version — adding new categories breaks downstream traceability with documents that already exist.

| Category | Acronym | Meaning | Typical anchor |
|---|---|---|---|
| Functional | **FUNC** | Core business functions the system performs | GAMP 5 D1 §3.4 |
| Performance | **PERF** | Response time, throughput, capacity, concurrent users | GAMP 5 D1 §3.4 |
| Quality | **QUAL** | Quality assurance, programming standards, configuration mgmt | GAMP 5 M1 |
| Training | **TRAIN** | Training requirements for developers, end-users, support | GAMP 5 M1 |
| Development environment | **DEVENV** | Dev tools, IDE, language, compilers, repos (Cat 5 only) | GAMP 5 D4 |
| Data structure | **DATA** | Data model, schemas, retention, integrity | EU Annex 11 §10 (2025) + §2.4 (ALCOA+), 21 CFR §11.10(c) |
| Data flow | **FLOW** | How data moves between components, with whom, via what protocol | EU Annex 11 §10 (2025 — validated interfaces) |
| Reports / Printouts | **REPORT** | What reports the system produces, format, audience | EU Annex 11 §8 (2011 — confirm 2025 §) |
| Security | **SEC** | Access control, authorization, encryption, attack surface | EU Annex 11 §10 (encryption) + §11.6 (remote MFA, 2025), 21 CFR §11.10(d) |
| Process organization | **PROC** | SOPs needed, roles, responsibilities, organizational impact | GAMP 5 §6.2.3 |
| User Interface | **UI** | UI standards, accessibility, layout, error messages | GAMP 5 D1 |
| Interfaces / APIs | **API** | Integrations with other systems (from receiver's perspective) | GAMP 5 D1 |
| Data Migration | **MIGR** | How data comes from legacy systems, format, validation | GAMP 5 D7 |
| Archiving | **ARCH** | Retention, media, retrieval, conversion across software versions | EU Annex 11 §17 (2011 — confirm 2025 §) |
| System Operations | **OPS** | Incident, change, request, backup, monitoring, periodic review | GAMP 5 O1-O13; Annex 11 §10-16 (2011 — confirm 2025 §) |
| Documentation | **DOCS** | Required deliverables (user manuals, SOPs, runbooks) | GAMP 5 M9 |
| Testing | **TEST** | Specific test requirements, test data, load tests, simulation | GAMP 5 D5 |
| Deliverables (scope of supply) | **DELIV** | What the supplier delivers, format, ID scheme | GAMP 5 M2 |
| Peripherals / Ancillary equipment | **PERIPH** | Terminals, scanners, printers connected to the system | — |
| Hardware Design Spec | **HW** | Hardware requirements (CPU, RAM, storage, network) | — |
| Electronic Records | **EREC** | Requirements for electronic records (Part 11 §10) | 21 CFR Part 11 §10; EU Annex 11 §12.6 (audit-trail review, 2025) |
| Electronic Signatures | **ESIG** | Requirements for electronic signatures (Part 11 §100-§300) | 21 CFR Part 11 §100, §200, §300; EU Annex 11 §13.7–13.9 (tamper-evidence, 2025) |

> [!note] EU Annex 11 edition — **2025-revised** is canonical
> Annex 11 anchors in this scheme follow the **2025-revised** EU Annex 11 numbering, consistent with the e2e-validated gold-standard `templates/csv/URS.md` / `FS.md`. Ground-truth 2025 anchors those templates use: ALCOA+ **§2.4**; encryption / validated interfaces / validated migration **§10**; remote MFA **§11.6** (NEW vs 2011); audit-trail independent peer review **§12.6**; e-signature tamper-evidence **§13.7–13.9**. Anchors tagged "(2011 — confirm 2025 §)" above (REPORT §8, ARCH §17, OPS §10-16) are **pending reconciliation** to the 2025 numbering — flagged for the owner, since their 2025 equivalents are not yet pinned in the gold-standard set.

### Why 22 (not 30, not 10)

- **Fewer than 22** misses regulatory anchors that auditors will ask about (especially EREC/ESIG/SEC/ARCH for Part 11 / Annex 11 systems).
- **More than 22** creates category sprawl: hard to remember which category a requirement belongs to, harder to enforce consistency across documents.
- The set is **inspired by industrial CSV practice** but **renamed in full** to remove any single-organization heritage. Each acronym is plain English (or English+CSV vocabulary), no German technical terms, no internal corporate codes.

---

## `<DOC-TYPE>` reference

| Prefix | Document | Lifecycle phase |
|---|---|---|
| `VMP` | Validation Master Plan | Master / program-level |
| `GXP-ASSESS` | GxP Assessment | Concept |
| `VP` | Validation Plan (per project) | Project — planning |
| `SUP-ASSESS` | Supplier Assessment | Project — planning |
| `RA-INIT` | Initial Risk Assessment | Project — planning (paralelo a URS) |
| `URS` | User Requirements Specification | Project — specification (top of V-Model left arm) |
| `FS` | Functional Specification | Project — specification |
| `CS` | Configuration Specification | Project — specification (Cat 4) |
| `DS` | Design Specification | Project — specification (Cat 5) |
| `API-SPEC` | API Specification | Project — specification (Mode B) |
| `DBS` | Database Schema Specification | Project — specification (Mode B) |
| `UC` | Use Cases / User Stories | Project — specification (Agile) |
| `AC` | Acceptance Criteria | Project — specification (Agile) |
| `ADR` | Architecture Decision Records | Project — specification (Mode B) |
| `RA-DET` | Detailed Risk Assessment (Functional RA / FMEA) | Project — post-spec |
| `IQ` | Installation Qualification | Project — verification |
| `OQ` | Operational Qualification | Project — verification |
| `PQ` | Performance Qualification | Project — verification |
| `UT-PLAN` | Unit Test Plan + Records | Project — verification (Mode B) |
| `IT-PLAN` | Integration Test Plan + Records | Project — verification (Mode B) |
| `SEC-TEST` | Security Testing Records | Project — verification |
| `PERF-TEST` | Performance Testing Records | Project — verification |
| `CR` | Change Request (project-phase change control) | Project — change management (GAMP §M8) |
| `RTM` | Requirements Traceability Matrix | Project — cross-cutting |
| `VR` | Validation Report | Project — closeout |
| `RN` | Release Notes | Project — closeout |
| `DEPLOY-RUN` | Deployment Runbook | Project — closeout |
| `PR` | Periodic Review | Operation |
| `CC` | Change Control Record (operational-phase change to the validated system) | Operation (GAMP §O6) |
| `IR` | Incident / Problem Record | Operation |
| `CONFIG-BL` | Configuration Baseline | Operation |
| `UAR` | User Access Review | Operation |
| `BRR` | Backup / Recovery Record | Operation |
| `DECOM-PLAN` | Decommissioning Plan | Retirement |
| `RETIRE-REPORT` | Retirement Report | Retirement |
| `DPIA` | Data Privacy Impact Assessment | Cross-cutting (GDPR/HIPAA) |
| `CYBER-RA` | Cybersecurity Risk Assessment | Cross-cutting (Annex 11 §17) |
| `AISC` | AI/ML System Card | Cross-cutting (Annex 22) |
| `P11M` | 21 CFR Part 11 Compliance Matrix | Cross-cutting (when applicable) |
| `SVP` | Spreadsheet Validation Protocol | Cross-cutting |
| `SOC-EVIDENCE`, `SLA`, `SHARED-RESP`, `EXIT-PLAN` | SaaS-specific bundle | Cross-cutting (SaaS deployments) |

> [!note] `CR` vs `CC` vs Code Review — disambiguated (2026-05-31)
> The change-management prefixes are partitioned by **lifecycle phase**, not by activity:
> - **`CR` = Change Request** — a change raised **during the validation project** (project-phase, GAMP §M8). Owned by `templates/csv/CR.md`.
> - **`CC` = Change Control Record** — a change to the **already-validated / production system** (operational-phase, GAMP §O6). Owned by `templates/csv/CC.md`.
> - **Code Review** is a *verification activity*, not a change record. If a Code-Review template is added later it takes the prefix **`CRR`** (Code Review Record); `CR` stays reserved for Change Request. (Earlier drafts of this table mislabeled `CR` as "Code Review Record" — corrected here.)

### Test case & record sub-prefixes

Within qualification / test documents, individual test cases carry a sub-prefix between the `<DOC-TYPE>` and the counter:

| Prefix | Use |
|---|---|
| `TC` | Test Case (structured test in IQ / OQ / UT-PLAN / IT-PLAN / SEC-TEST / INFRA-QUAL, and retrieval tests in DECOM-PLAN) |
| `SCEN` | Scenario (PQ — real-world process scenarios) |

So `IQ-TC-042` reads as "Installation Qualification, Test Case #42", and `DECOM-PLAN-TC-003` is "Decommissioning Plan, Test Case #3" — keeping the test namespace separate from the plan's step counter.

### Two-segment IDs for assessment & operational-record documents

Documents whose **primary entity is a finding / risk / step / record** (not a categorized requirement) use a **two-segment** ID — `<DOC-TYPE>-<NNN>`, with no category segment — because the document itself *is* the category:

| Pattern | Example | Used by |
|---|---|---|
| `<DOC>-<NNN>` | `RA-INIT-001`, `RA-DET-014`, `DPIA-007` | Risk / assessment registers (RA-INIT, RA-DET, **DPIA risk rows**), decommissioning steps (DECOM-PLAN) |
| `<DOC>-<YYYY>-<NNN>` | `CC-2026-038`, `IR-2026-012` | Operational records with a year variant (CC, IR, BRR, UAR) |

Non-requirement table rows that are **not** themselves the primary entity (e.g. a DPIA's data-inventory rows) take a plain local label (`D1`, `D2`, …) rather than an ID, to avoid colliding with the document's `<DOC>-<NNN>` finding counter. The parser in `skills/_scripts/lib/gdd_common.py` treats `INIT`, `DET`, `TC`, `SCEN` as non-category middles, so compound DOC-TYPEs (`RA-INIT`, `RA-DET`, `DECOM-PLAN`, `UT-PLAN`) do not report phantom categories.

---

## Forward traceability

The naming scheme encodes **forward traceability** by carrying the category across documents:

```
URS-FUNC-001  (User Requirements — what the user needs)
    │
    ├──► FS-FUNC-001    (Functional Spec — how the system responds to URS-FUNC-001)
    │       │
    │       ├──► DS-FUNC-005    (Design Spec — internal design that implements FS-FUNC-001)
    │       │
    │       └──► OQ-TC-042      (OQ test case — verifies FS-FUNC-001 behaviorally)
    │
    └──► PQ-SCEN-007     (PQ scenario — verifies URS-FUNC-001 in real-world conditions)
```

- **1:1, 1:N, 1:0** cardinality is allowed. `URS-FUNC-001` may expand into several `FS-FUNC-NNN` entries (decomposition) or stay 1:1.
- The category travels with the requirement to the right side of the V (verification). Test cases of FUNC requirements get `OQ-TC-NNN` IDs — the `TC` prefix indicates they are test cases, and the **category being tested** is recorded inside the test case's frontmatter or content, not in the ID.

---

## Backward references (anti-orphan)

Every spec ID **must** be traceable both forward (to its consumers) and backward (to its sources):

- A `FS-XXX-NNN` row **must** name the `URS-XXX-NNN` it implements (otherwise it's orphan).
- An `OQ-TC-NNN` test case **must** name the `FS-XXX-NNN` (or `URS-XXX-NNN`) it verifies.
- A `RA-DET-NNN` row **must** name the `URS-XXX-NNN` and/or `FS-XXX-NNN` it analyzes risk for.

The `generate-rtm` skill produces a derived `specs/RTM.md` (or `specs/traceability.yaml`) by walking all spec files and following these references.

---

## Consumer-side override (`id_scheme: custom`)

Organizations with pre-existing internal naming conventions can override the canonical scheme via `.gxp-dev.yaml`:

```yaml
id_scheme: custom
custom_alias:
  URS: "REQ-USER"
  FS:  "SPEC-FUNC"
  IQ:  "TEST-IQ"
  # ... map only the prefixes you want to alias
```

Skills consuming the manifest translate `URS-FUNC-001` → `REQ-USER-FUNC-001` at instantiation. Categories themselves (the 22 acronyms) are intentionally **not** aliasable — they are the spine of traceability and changing them per-organization would defeat the purpose of a shared canonical scheme.

---

## Anti-patterns (do not use)

The following naming patterns are **explicitly forbidden** in any file under `gxp-driven-dev/`:

| Banned | Why |
|---|---|
| Legacy `US-` requirement-ID prefix | Ambiguous and inherited from a prior template catalog; use `URS-` |
| Any legacy 3-letter category code inherited from a prior corporate catalog | Confidentiality + consistency; use only the 22 canonical acronyms above. The enforcement set lives in `skills/_scripts/lib/gdd_common.py`. |
| Corporate-specific instance-ID schemes (fixed-format site/sequence codes) | Corporate IP; use a generic `{{system_id}}` placeholder |
| Non-English heritage terms for domain concepts | English-only product surface |

The CI anti-leak guard (`skills/_scripts/anti-leak-guard.py`) detects and blocks the banned identifiers automatically.

---

## See also

- `templates/csv/URS.md` — first canonical template using this scheme
- `templates/csv/VMP.md` — Master template that declares which `<DOC-TYPE>` prefixes are active per project
- `docs/project-layout.md` — the `.gxp-dev.yaml` manifest and how `id_scheme` + `custom_alias` work
- `skills/_scripts/generate-rtm.py` — derives the RTM from spec files using this scheme
