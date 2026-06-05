---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "API-SPEC — API Specification (canonical CSV template)"
type: template
template_class: csv
template_id: "API-SPEC"
template_version: "0.1.0"
v_model_phase: design-specification
gamp_categories_applicable: [4, 5]
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# API-SPEC realizes FS-API-NNN / URS-API-NNN requirements.
# It sits in the design-specification phase alongside DS/CS.
inputs:
  - template_id: "FS"
    required: true
    description: "Approved Functional Specification — source of all FS-API-NNN that this API-SPEC realizes. Each endpoint row must cite at least one FS-API-NNN."
  - template_id: "URS"
    required: false
    description: "Approved User Requirements Specification — source of URS-API-NNN requirements that the FS-API-NNN already traces to. Used to verify end-to-end traceability URS → FS → API-SPEC. Optional: the API-SPEC is valid on the FS-only path (the FS already carries the URS trace)."
outputs:
  - artifact: "API-SPEC instance (Markdown)"
    consumed_by:
      - "OQ"         # OQ interface test cases — each validated endpoint generates ≥1 OQ-TC
      - "RTM"        # Requirements Traceability Matrix — FS-API-NNN → API-SPEC-API-NNN → OQ-TC
applicable_regulations:
  - "gamp-5"          # §D3 Design Specifications; GAMP 5 Appendix D3 — validated interfaces
  - "eu-annex-11"     # §10 Input checks, error handling, end-to-end integrity, encryption
  - "21-cfr-part-11"  # §11.10 Controls for closed systems (records, data integrity)
based_on:
  - "GAMP 5 §D3 (Design Specifications) — validated interfaces for GxP data transfer"
  - "EU Annex 11 §10 — data entry controls; §4 Validation (interface scope); §7 Data storage (integrity)"
  - "V-Model: API-SPEC is authored in the design-specification phase (left arm), verified in OQ (right arm)"

# ─── Placeholders (declarative, for instantiation skills) ───────────────────
placeholders:
  system_name:
    type: string
    required: true
    description: "Human-readable name of the system that exposes or consumes the APIs (must match the FS and URS)"
    example: "QC LIMS at site A"
  system_id:
    type: string
    required: true
    description: "Unique system identifier (same as the source FS and URS)"
  fs_ref:
    type: string
    required: true
    description: "Identifier + version of the FS instance from which FS-API-NNN requirements are realized"
    example: "FS-PROJ-2026-001 v1.0 (approved)"
  urs_ref:
    type: string
    required: true
    description: "Identifier + version of the URS instance (for end-to-end traceability)"
    example: "URS-PROJ-2026-001 v1.0 (approved)"
  api_base_url:
    type: string
    required: true
    description: "Base URL of the API (production environment). Use a placeholder if not yet determined."
    example: "https://api.example.internal/v1"
  api_version:
    type: string
    required: true
    description: "Version string of the API being specified (semantic versioning recommended)"
    example: "1.0.0"
  api_versioning_strategy:
    type: enum
    required: true
    values: ["url-path", "header", "query-param", "content-negotiation"]
    description: "Mechanism used to communicate the API version to consumers"
  auth_mechanism:
    type: enum
    required: true
    values: ["OAuth2-client-credentials", "OAuth2-authorization-code", "API-key", "mTLS", "JWT-bearer", "SAML", "other"]
    description: "Primary authentication mechanism. Select 'other' and fill auth_mechanism_other if not listed."
  auth_mechanism_other:
    type: string
    required: false
    description: "Free-text description of the auth mechanism when auth_mechanism = 'other'"
  transport_encryption:
    type: enum
    required: true
    values: ["TLS-1.2", "TLS-1.3", "mTLS", "other"]
    description: "Transport-layer encryption protocol (EU Annex 11 §10 — encryption across untrusted perimeters)"
  spec_author_name:
    type: string
    required: true
  spec_author_dept:
    type: string
    required: true
  gamp_category:
    type: enum
    required: true
    values: [4, 5]
    description: "GAMP 5 category of the system (inherited from RA-INIT / URS / FS). Cat 1-3 do not typically require a standalone API-SPEC."
  rate_limit_policy:
    type: string
    required: false
    description: "Default rate-limit policy applied to all endpoints unless overridden in the endpoint table"
    example: "100 requests / 60 s / consumer key; burst cap 200"
  idempotency_policy:
    type: string
    required: false
    description: "Policy for idempotent operations (e.g. use of Idempotency-Key header, server-side deduplication window)"
  reconciliation_mechanism:
    type: string
    required: false
    description: "Mechanism for end-to-end GxP data-transfer integrity verification (e.g. daily record-count reconciliation, hash comparison, correlation IDs). Required when URS-API-001 is active."
  org_csv_policy_ref:
    type: string
    required: false
    description: "Reference to the organization's CSV / data integrity policy that governs this document"
  custom_ref:
    type: string
    required: false
    description: "Additional reference document (optional, free-text)"

# ─── INSTANCE frontmatter spec (not the template's) ─────────────────────────
instance_frontmatter_spec:
  required_fields:
    - title
    - type: "instance"
    - based_on_template: "API-SPEC"
    - based_on_template_version
    - system_id
    - traces_to           # FS instance ID + version (FS-API-NNN source)
    - status              # draft | in-review | approved | superseded
    - version             # instance's own semver
    - created
    - updated
    - language
  conditional_fields:
    - approved_by: "required if status == approved"
    - supersedes: "version of the previous API-SPEC if this is a new revision"
    - urs_traces_to: "recommended — URS instance ID for end-to-end traceability"

# ─── Validation rules ────────────────────────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "traces_to must point to an FS instance with status: approved"
  - "Each API-SPEC-API-NNN row in the endpoint table must cite at least one FS-API-NNN (or URS-API-NNN) in the 'Realizes' column — orphan rows are prohibited"
  - "Each FS-API-NNN from the source FS must be covered by ≥1 API-SPEC endpoint row (full interface coverage)"
  - "If URS-API-001 (validated interfaces) is active in the source URS → section 6 (Validated GxP Interface Controls) must not be empty and must describe the reconciliation mechanism"
  - "If URS-SEC-001 (encryption) is active → transport_encryption must be TLS-1.2, TLS-1.3, mTLS, or other with documented rationale"
  - "Each endpoint row must specify at least: Method, Path, Auth, expected success HTTP status, and at least one error code"
  - "Version string must follow semantic versioning (MAJOR.MINOR.PATCH)"
  - "Signature block must include an identified Data Owner (GAMP 5 §6.2.3.1 + M10)"

tags:
  - template
  - csv
  - api-spec
  - api-specification
  - interfaces
  - v-model
  - design-specification
  - gxp
  - canonical
---

# API-SPEC — API Specification

> [!note] Canonical CSV template
> **Canonical** template for producing the **API Specification (API-SPEC)** of a computerized system. The API-SPEC describes the precise contract of the APIs a system **exposes** (provider role) or **consumes** (consumer role) — endpoints, HTTP methods, authentication, request/response payloads, versioning, error handling, and the **validated-interface controls** mandated by EU Annex 11 §10 for GxP data transfer. It **realizes** `FS-API-NNN` (and upstream `URS-API-NNN`) requirements and is verified in the **OQ** (interface test cases). Complies with GAMP 5 §D3 (Design Specifications), EU Annex 11 §10, and 21 CFR Part 11.

> [!tip] Embedded usage rules
> 1. **Realizes, does not re-decide** — interface applicability was decided in the URS (URS-API-001 preset); the FS specified how (FS-API-NNN); this document specifies the **exact contract** of each interface. It does not re-open the "should we have an API?" question.
> 2. **Mandatory traceability** — each `API-SPEC-API-NNN` endpoint row must cite at least one `FS-API-NNN` in the "Realizes" column. Orphan rows (endpoints with no upstream requirement) are prohibited.
> 3. **Full interface coverage** — every `FS-API-NNN` from the approved FS must be traceable to ≥1 endpoint row in this document (1:0 is a blocking gap).
> 4. **GxP data-transfer integrity** — when URS-API-001 is active, section 6 (Validated GxP Interface Controls) is **mandatory**. It must describe input checks, error handling, end-to-end integrity verification, and encryption (EU Annex 11 §10).
> 5. **No-deletion rule** — an obsolete endpoint row is **not** deleted: it is struck through (`~~API-SPEC-API-007: ...~~`). Deleting breaks the FS-API → API-SPEC → OQ traceability chain.
> 6. **V-Model pairing** — the API-SPEC is authored in the design-specification phase (left arm of the V) and verified in the **OQ** (right arm). Each endpoint row with prio=H (inherited from the FS/URS) generates ≥1 interface test case in `OQ.md`.
> 7. **Provider vs consumer** — clearly label each endpoint as **P** (this system is the provider/server) or **C** (this system is the consumer/client). The spec covers both directions within a single system boundary.

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **FS being realized** | `{{fs_ref}}` *(must be approved)* |
| **URS (end-to-end traceability)** | `{{urs_ref}}` |
| **API base URL** | `{{api_base_url}}` |
| **API version** | `{{api_version}}` |
| **GAMP category** | `{{gamp_category}}` *(inherited from [Risk Analysis](RA-INIT.md) / URS / FS)* |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Author | `{{spec_author_name}}` | `{{spec_author_dept}}` |  |  |
| Reviewer 1 (System Owner / IT) |  |  |  |  |
| Reviewer 2 (SME / Integration Lead) |  |  |  |  |
| Reviewer 3 (Data Owner) *(GAMP 5 §6.2.3.1 + M10)* |  |  |  |  |
| Approver 1 (System Owner) |  |  |  |  |
| Approver 2 (Quality Unit) |  |  |  |  |

> [!note] Who authors the API-SPEC
> Typically the **integration engineer** or **software architect** responsible for the interface design. For Cat 5 custom systems, the development team authors this document; the regulated organization reviews and approves it. For Cat 4 configured products with integration adapters, authorship may be shared between the supplier and the in-house CSV/IT team.

---

## 1. Introduction

This **API Specification (API-SPEC)** defines the precise interface contract for the system **`{{system_name}}`** (`{{system_id}}`). It realizes the interface requirements defined in the [Functional Specification](FS.md) (`{{fs_ref}}`) and traces back to the user requirements in the [URS](URS.md) (`{{urs_ref}}`).

The API-SPEC occupies the **design-specification phase** of the CSV V-Model (left arm, at the same level as the [Design Specification](DS.md) and [Configuration Specification](CS.md)). It is verified in the **OQ** (interface test cases, right arm).

**Scope**: this document covers all interfaces that `{{system_name}}` **exposes** (provider role, **P**) or **consumes** (consumer role, **C**). Each interface endpoint is expressed as a row in the endpoint table (section 3) and linked to the `FS-API-NNN` requirement it realizes.

> [!note] Applicability — when is an API-SPEC required?
> An API-SPEC is required when the approved URS includes `URS-API-001` (validated interfaces preset) and the FS includes one or more `FS-API-NNN` entries that cannot be fully specified within the FS body alone. For simple point-to-point file-drop integrations with no runtime API, the FS-API section may be sufficient and a standalone API-SPEC may be waived with documented rationale.

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| API-SPEC | API Specification — the precise contract of all interfaces the system exposes or consumes |
| FS | Functional Specification — the technical "how" that realized the URS; source of FS-API-NNN |
| URS | User Requirements Specification — the "what" from the user's perspective; source of URS-API-NNN |
| OQ | Operational Qualification — functional verification phase; consumes API-SPEC for interface test cases |
| RTM | Requirements Traceability Matrix — cross-document traceability index |
| GxP | Good x Practice — umbrella for GMP, GLP, GCP, GEP in regulated industries |
| Validated interface | An interface for GxP data transfer that has been specified, tested, and accepted under the CSV program |
| P | Provider — this system exposes/serves the endpoint |
| C | Consumer — this system calls/consumes the endpoint from another system |
| mTLS | Mutual TLS — bidirectional certificate-based authentication at transport layer |
| GAMP 5 | Good Automated Manufacturing Practice 5, ISPE 2022 |
| EU Annex 11 | EU GMP Annex 11 — Computerised Systems |
| 21 CFR Part 11 | FDA — Electronic Records; Electronic Signatures |
|  |  |

---

## 3. Endpoint catalog — `API-SPEC-API-NNN`

> [!tip] This is the core of the document
> Every interface endpoint (REST, SOAP, message queue, file-based, etc.) is a row in this table. Use one row per logical endpoint / operation. Each row receives a unique `API-SPEC-API-NNN` identifier (sequential within this document). The "Realizes" column links back to the `FS-API-NNN` (or `URS-API-NNN`) from which the endpoint originates.

> [!warning] Orphan prevention
> Any endpoint without a "Realizes" citation is a traceability gap and will be flagged by `validate-traceability.py`. Any `FS-API-NNN` from the source FS without a corresponding row here is a coverage gap and is a blocking issue for status: approved.

| API-SPEC ID | Realizes (FS / URS-API-ID) | Role (P/C) | Method | Path / Queue / Topic | Auth | Request (schema / payload) | Response (success) | Error codes | Rate limit | GxP | Prio |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `API-SPEC-API-001` | `FS-API-001` | P | `GET` | `/records/{id}` | *see §4* | — | `200 OK` · JSON · `RecordDto` schema | `400` `401` `403` `404` `422` `500` | *see §5* | Y | H |
| `API-SPEC-API-002` | `FS-API-002` | P | `POST` | `/records` | *see §4* | JSON · `CreateRecordCmd` schema | `201 Created` · JSON · `RecordDto` | `400` `401` `403` `409` `422` `500` | *see §5* | Y | H |
| `API-SPEC-API-003` | `FS-API-003` | C | `POST` | `https://external-system/events` | *see §4* | JSON · `EventPayload` schema | `200 OK` | `400` `401` `408` `500` `503` | *see §5* | Y | M |
|  |  |  |  |  |  |  |  |  |  |  |  |

**Column definitions**

| Column | Meaning |
|---|---|
| **API-SPEC ID** | Unique identifier for this endpoint row (`API-SPEC-API-NNN`) |
| **Realizes** | `FS-API-NNN` (and/or `URS-API-NNN`) this endpoint realizes — mandatory |
| **Role** | **P** = this system is the provider (serves the request) · **C** = this system is the consumer (sends the request) |
| **Method** | HTTP method (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) or protocol type (`MQ-PUBLISH`, `MQ-SUBSCRIBE`, `FILE-SFTP`, `SOAP`, etc.) |
| **Path / Queue / Topic** | URL path, queue name, or topic identifier |
| **Auth** | Authentication mechanism applied to this endpoint (reference to §4 or endpoint-specific override) |
| **Request** | Request body schema name, content-type, and key fields; or "—" for endpoints with no body |
| **Response (success)** | Success HTTP status code + response body schema and key fields |
| **Error codes** | HTTP error codes this endpoint may return (all must be handled) |
| **Rate limit** | Endpoint-specific rate limit, or "default" to inherit §5.1 |
| **GxP** | Y / N — whether the data transferred via this endpoint is GxP-relevant |
| **Prio** | H / M / L — inherited from the source FS-API-NNN/URS-API-NNN |

---

## 4. Authentication and authorization

> [!warning] Mandatory section
> EU Annex 11 §11.6 (remote MFA) and §10 (access/data controls) require that access to computerised systems is controlled. This section documents the auth mechanisms governing API access. Link each mechanism to the `FS-SEC-NNN` / `FS-API-NNN` that mandated it.

### 4.1 Primary authentication mechanism

| Field | Value |
|---|---|
| **Mechanism** | `{{auth_mechanism}}` *(e.g. OAuth2-client-credentials, API-key, mTLS)* |
| **Token/credential endpoint** | *(e.g. `https://idp.example.internal/oauth2/token`)* |
| **Token lifetime** | *(e.g. access token: 1 h; refresh token: 24 h)* |
| **Realizes** | `FS-API-NNN` / `FS-SEC-NNN` |

> [!note] Detail when `auth_mechanism` = `other`
> `{{auth_mechanism_other}}`

### 4.2 Authorization model

Describe the authorization model (role-based, attribute-based, scope-based) and the mapping between consumer identities and allowed operations:

| Consumer identity / role | Allowed endpoints (API-SPEC IDs) | Scope / claim |
|---|---|---|
| *(e.g. service account `lims-integration`)* | `API-SPEC-API-001`, `API-SPEC-API-002` | `records:read records:write` |
| *(e.g. read-only report consumer)* | `API-SPEC-API-001` | `records:read` |
|  |  |  |

### 4.3 Transport encryption

| Field | Value |
|---|---|
| **Protocol** | `{{transport_encryption}}` |
| **Minimum TLS version enforced** | *(e.g. TLS 1.2 — weak cipher suites disabled; server certificate from internal PKI)* |
| **Certificate management** | *(e.g. annual renewal; managed by infrastructure team; CN validated against system_id)* |
| **Realizes** | `FS-SEC-NNN` *(EU Annex 11 §10 — encryption across untrusted network perimeters)* |

> [!warning] GxP data across untrusted perimeters
> EU Annex 11 §10 requires that data transmitted across untrusted network segments is protected. If any `GxP=Y` endpoint in §3 crosses an untrusted perimeter (internet, DMZ, cloud boundary), `transport_encryption` must be TLS-1.2 or stronger, and the implementation must be verified in the OQ (interface security test case).

---

## 5. Rate limiting and availability

### 5.1 Default rate-limit policy

| Field | Value |
|---|---|
| **Default limit** | `{{rate_limit_policy}}` |
| **Burst allowance** | *(e.g. up to 200 requests in any 10 s window)* |
| **Headers returned** | *(e.g. `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`)* |
| **Response when exceeded** | `429 Too Many Requests` with `Retry-After` header |

### 5.2 Idempotency

| Field | Value |
|---|---|
| **Idempotency mechanism** | `{{idempotency_policy}}` |
| **Header** | *(e.g. `Idempotency-Key: <UUID v4>` — required for `POST` / `PUT` / `PATCH` state-mutating endpoints)* |
| **Deduplication window** | *(e.g. server retains key → result mapping for 24 h)* |
| **Rationale** | Prevents duplicate GxP records in case of network retries (EU Annex 11 §10 — error handling) |

### 5.3 Availability and SLA

| Endpoint group | Target availability | Planned maintenance window |
|---|---|---|
| GxP endpoints (`GxP=Y`) | *(e.g. 99.5% monthly, excluding planned windows)* | *(e.g. Sundays 02:00–04:00 UTC)* |
| Non-GxP endpoints | *(e.g. 99.0% monthly)* |  |

---

## 6. Validated GxP interface controls

> [!warning] Mandatory section if URS-API-001 is active
> EU Annex 11 §10 requires that data entered into a computerised system is checked for correctness. For interfaces, this means: (a) input validation on the receiving side; (b) explicit error handling and logging; (c) end-to-end integrity verification for GxP data transfers; (d) encryption across untrusted perimeters. This section is **mandatory** when `URS-API-001` (validated interfaces) is active in the source URS. Document each control against its `FS-API-NNN` and `API-SPEC-API-NNN`.

### 6.1 Input validation (EU Annex 11 §10)

| API-SPEC ID | Validation applied | Schema / rule | Error response if invalid |
|---|---|---|---|
| `API-SPEC-API-001` | JSON Schema validation on request body | *(schema name / link)* | `422 Unprocessable Entity` with field-level error detail |
| `API-SPEC-API-002` | JSON Schema + domain validation (mandatory fields, referential integrity) | *(schema name / link)* | `422` with structured error body |
|  |  |  |  |

> [!tip] Input validation principle
> Validate at the API boundary, not only inside business logic. The validator must: (1) reject unknown fields (strict mode); (2) enforce field types, lengths, and enumeration constraints; (3) return a structured error response that does not leak internal stack traces (EU Annex 11 §10 — error handling).

### 6.2 Error handling and audit logging

| API-SPEC ID | Error events logged | Log fields (minimum) | Log destination |
|---|---|---|---|
| `API-SPEC-API-001` | `401` `403` `404` `422` `500` | `timestamp_utc`, `correlation_id`, `consumer_id`, `http_status`, `error_code`, `endpoint` | *(e.g. centralized audit log service; immutable append-only)* |
| `API-SPEC-API-002` | All errors + success `201` | Same + `record_id` created | *(same)* |
|  |  |  |  |

> [!note] Audit log immutability
> The audit log for GxP API calls must be append-only and tamper-evident (EU Annex 11 §10 + 21 CFR Part 11 §11.10(e)). Architecture of the log store is described in `FS-EREC-NNN` / `FS-API-NNN`; this table identifies which API events are written to it.

### 6.3 End-to-end data integrity

| Field | Value |
|---|---|
| **Reconciliation mechanism** | `{{reconciliation_mechanism}}` |
| **Correlation ID** | *(e.g. `X-Correlation-ID` header set by the initiating system, propagated through all hops, stored on every log entry)* |
| **Record-count verification** | *(e.g. daily job compares record counts between source and target; discrepancies trigger incident `IR-NNN`)* |
| **Checksum / hash** | *(e.g. SHA-256 of the request payload included in `X-Content-Hash` header; validated on receipt before persistence)* |
| **Realizes** | `FS-API-NNN` *(EU Annex 11 §10 — end-to-end integrity for GxP data transfer)* |

### 6.4 Encryption across untrusted perimeters

| Interface | Classification | Perimeter type | Encryption applied | Realizes |
|---|---|---|---|---|
| `API-SPEC-API-001` | GxP=Y | Internal network | TLS 1.3 (server cert; client cert optional) | `FS-SEC-001`, `FS-API-001` |
| `API-SPEC-API-003` | GxP=Y | Internet (outbound) | TLS 1.3 + certificate pinning for external endpoint | `FS-SEC-001`, `FS-API-003` |
|  |  |  |  |  |

---

## 7. Versioning policy

| Field | Value |
|---|---|
| **Versioning strategy** | `{{api_versioning_strategy}}` *(e.g. url-path: `/v1/`, `/v2/`)* |
| **Current version** | `{{api_version}}` |
| **Deprecation notice period** | *(e.g. minimum 6 months advance notice before breaking change; communicated via changelog and API response header `Deprecation`)* |
| **Backward compatibility** | *(e.g. additive changes — new optional fields — are non-breaking; removal or type changes require a major version bump and a new API-SPEC instance)* |
| **Breaking change process** | *(describe change-control mechanism: new API-SPEC version → FS revision → OQ re-test of affected endpoints → CC record)* |

> [!warning] Breaking changes require change control
> Any breaking API change affecting a `GxP=Y` endpoint must follow the organization's change control process (see [CC](CC.md)). A new `API-SPEC` version must be issued, the source FS updated, and the affected OQ test cases re-executed before the change is deployed to production.

---

## 8. FS-API → API-SPEC traceability matrix

> [!tip] Coverage check
> This table is the master traceability index between FS interface requirements and their API-SPEC endpoint rows. Used by `validate-traceability.py` to detect coverage gaps. A `FS-API-NNN` without a corresponding `API-SPEC-API-NNN` row is a blocking gap.

| FS-API-ID | FS statement (summary) | API-SPEC-API-NNN(s) realizing it | GxP | Prio |
|---|---|---|---|---|
| `FS-API-001` |  | `API-SPEC-API-001` | Y | H |
| `FS-API-002` |  | `API-SPEC-API-002` | Y | H |
| `FS-API-003` |  | `API-SPEC-API-003` | Y | M |
|  |  |  |  |  |

**Coverage rule**: every `FS-API-NNN` from the approved FS must appear in this table with at least one `API-SPEC-API-NNN`. Rows with no FS-API-ID citation are orphan endpoints and must be resolved before approval.

---

## 9. Related documents

| Document | Reference |
|---|---|
| Functional Specification realized by this API-SPEC | `{{fs_ref}}` ([FS](FS.md)) |
| User Requirements Specification (upstream) | `{{urs_ref}}` ([URS](URS.md)) |
| Design Specification (Cat 5, if separate) | [DS](DS.md) *(if applicable)* |
| Configuration Specification (Cat 4) | [CS](CS.md) *(if applicable)* |
| Operational Qualification (consumer of this spec) | [OQ](OQ.md) |
| Requirements Traceability Matrix | [RTM](RTM.md) |
| Organization's CSV Policy | `{{org_csv_policy_ref}}` |
| `{{custom_ref}}` |  |

---

## 10. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue — `{{spec_author_name}}`, `{{spec_author_dept}}` |
|  |  |  |

---

## Canonical notes for implementers

> [!note] API-SPEC sits at the design-specification level of the V-Model
> The [URS](URS.md) defines the interface requirement ("the system shall integrate with system X"); the [FS](FS.md) realizes it functionally ("the integration uses a REST API with OAuth2"); this **API-SPEC** specifies the exact contract. The OQ verifies each endpoint in section 3 via interface test cases (`OQ-TC-NNN`). Traceability chain: `URS-API-NNN → FS-API-NNN → API-SPEC-API-NNN → OQ-TC-NNN`. *(GAMP 5 §D3; OQ = functional verification per CSV convention.)*

> [!note] Category-awareness — depth by GAMP category
> - **Cat 4** (configured product with integration adapter): the API-SPEC focuses on the adapter configuration, its input validation rules, and the reconciliation mechanism. The supplier's API documentation serves as a supplementary reference (not a replacement for the validated specification).
> - **Cat 5** (custom-built system): comprehensive API-SPEC authored by the development team. Includes schema definitions, OpenAPI / AsyncAPI references (attach as appendix), and full error-handling matrix. Each endpoint generates ≥1 OQ interface test case.

> [!note] Provider vs consumer — full coverage in one document
> A single API-SPEC may cover both endpoints this system exposes (P) and endpoints it consumes from other systems (C). This gives the validation team a single-source-of-truth for all interface risks. Each endpoint row is labeled P or C (column "Role" in §3).

> [!tip] Natural output of this template
> A well-authored API-SPEC produces: (1) the endpoint catalog (§3) feeding OQ test case generation; (2) the traceability matrix (§8) feeding the RTM; (3) the validated-interface controls (§6) satisfying EU Annex 11 §10 for each GxP=Y endpoint. Section 8 is the master coverage check before marking status: approved.

> [!warning] OpenAPI / AsyncAPI appendix
> For REST/HTTP APIs, attach an OpenAPI 3.x specification as an appendix (or reference it by URL to the version-controlled file). For event-driven interfaces, attach an AsyncAPI specification. These machine-readable schemas are the implementation contract; section 3 of this document is the audit-grade, human-readable validation record. Both must be consistent: any discrepancy between the narrative table and the machine-readable spec must be resolved before approval.

## Related

- [URS](URS.md) · [FS](FS.md) · [DS](DS.md) · [CS](CS.md) · [OQ](OQ.md) · [RTM](RTM.md)
- GAMP 5 · 21 CFR Part 11 · EU Annex 11
- V-Model · validated interface · data integrity

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.api-spec.from-fs` skill.

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer project. If it does not exist → redirect to `/gdd.init`.
2. **Locate the approved FS instance** (`specs/FS.md`). If it does not exist or status != approved → **stop**: the API-SPEC realizes an approved FS. Inform the user.
3. **Locate the approved URS instance** (`specs/URS.md`) for end-to-end traceability context.
4. **Read `templates/csv/API-SPEC.md`** from the toolkit as the source template (this file).
5. **Check URS-API-001 activation**: if URS-API-001 is not active in the URS, confirm with the user whether an API-SPEC is still required or if the FS-API section is sufficient. Do not proceed blindly.

### Generation flow (cascade from FS)

1. **Parse all `FS-API-NNN`** from the approved FS, with their GxP (Y/N) and prio (H/M/L).
2. **For each FS-API-NNN**, generate ≥1 `API-SPEC-API-NNN` endpoint row in §3:
   - Populate Method, Path, Auth, Request schema, Response schema, Error codes from the FS realization text.
   - Inherit GxP and prio from the FS-API-NNN.
   - Mark Role as P or C based on context (ask if ambiguous).
   - Cardinality: 1:1 by default; 1:N if the FS entry covers multiple distinct endpoints; 1:0 is prohibited for FS-API with GxP=Y.
3. **Populate §6 (Validated GxP Interface Controls)** for every `GxP=Y` endpoint:
   - §6.1 Input validation rules.
   - §6.2 Error events to be logged (minimum fields).
   - §6.3 End-to-end reconciliation mechanism.
   - §6.4 Encryption classification per endpoint.
4. **Populate §8 (traceability matrix)** as the master coverage index.
5. **Anti-hallucination**: insert `[NEEDS CLARIFICATION: ...]` when there is insufficient technical information to specify an endpoint (e.g. path not yet decided, auth mechanism TBD, error codes unknown). Never invent technical details or regulatory citations.
6. **Output**: write `specs/API-SPEC.md` (status: draft); print summary + FS-API → API-SPEC coverage (% of FS-API requirements with endpoint rows).
7. **Post-flight**: run `validate-frontmatter.py` + `check-clarification-markers.py` + `generate-rtm.py` (to verify coverage and update the RTM).

### Stop criteria ("complete" instance)

- [ ] `traces_to` points to an FS instance with status: approved
- [ ] All `FS-API-NNN` from the approved FS have ≥1 `API-SPEC-API-NNN` row (full coverage)
- [ ] No `FS-API-NNN` with prio=H is left without an endpoint row (0 blocking gaps)
- [ ] Each endpoint row cites its `FS-API-NNN` in the "Realizes" column
- [ ] Section 6 (Validated GxP Interface Controls) is populated for all `GxP=Y` endpoints
- [ ] Authentication mechanism and transport encryption are documented in §4
- [ ] Versioning policy is documented in §7
- [ ] Section 8 (traceability matrix) is complete and consistent with §3
- [ ] Signature block with ≥1 author + reviewers (incl. Data Owner) + approvers

### `status` transitions

```
draft ──[full FS-API coverage + 0 H gaps + §6 populated]──> in-review
in-review ──[approver signatures applied]──> approved
approved ──[breaking change issued]──> superseded
```

### Downstream mapping — how API-SPEC traces to OQ and RTM

| Origin (API-SPEC) | Destination | Cardinality | Rule |
|---|---|---|---|
| `API-SPEC-API-NNN` with GxP=Y | `OQ-TC-NNN` (interface test case) in `OQ.md` | 1:N | Each GxP endpoint generates ≥1 OQ interface test case verifying request/response contract, auth, error handling, and (for H prio) reconciliation |
| `API-SPEC-API-NNN` | Row in `RTM.md` | 1:1 | The RTM records `URS-API-NNN → FS-API-NNN → API-SPEC-API-NNN → OQ-TC-NNN` for each endpoint |
| `API-SPEC-API-NNN` with GxP=Y | Row in `RA-DET.md` | 1:1 | The detailed RA evaluates interface failure risk (data loss, integrity breach, unauthorized access) per endpoint |
