---
# ─── Template metadata (canonical) ──────────────────────────────────────────
title: "PERF-TEST — Performance Testing (canonical CSV template)"
type: template
template_class: csv
template_id: "PERF-TEST"
template_version: "0.1.0"
v_model_phase: performance-verification
gamp_categories_applicable: [3, 4, 5]
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30

# ─── Pipeline (V-Model neighbours) ──────────────────────────────────────────
# PERF-TEST verifies performance characteristics declared in URS-PERF and FS-PERF
# under realistic and beyond-realistic load conditions (GAMP 5 §D1/§D5, EU Annex 11 §9).
# Feeds OQ, PQ, RTM, and VR. High-RPN performance functions require stress testing.
inputs:
  - template_id: "FS"
    required: true
    description: "Approved Functional Specification — source of FS-PERF-NNN items defining performance design points"
  - template_id: "URS"
    required: true
    description: "Approved User Requirements Specification — URS-PERF-NNN items define the SLAs (pass thresholds) this protocol verifies"
  - template_id: "RA-DET"
    required: false
    description: "Detailed Risk Assessment (FMEA) — RPN values scale stress testing depth; high-RPN performance functions require stress test cases"
  - template_id: "RA-INIT"
    required: false
    description: "Initial Risk Assessment — fallback risk source: if RA-DET is absent, scale stress depth by RA-INIT Risk Priority (H/M/L); only default to load-only if neither RA-DET nor RA-INIT exists"
outputs:
  - artifact: "PERF-TEST instance (Markdown) — executed performance test protocol"
    consumed_by:
      - "OQ"    # Performance-function test cases may be referenced in OQ (§4.1 special test types)
      - "PQ"    # PQ fitness-for-use includes performance under real-world conditions
      - "RTM"   # Requirements Traceability Matrix — URS-PERF / FS-PERF coverage
      - "VR"    # Validation Report — summarises PERF-TEST results
applicable_regulations:
  - "gamp-5"       # §D1 (capacity/performance requirements) + §D5 (risk-based testing; not all functions need the same rigor) + performance under realistic load
  - "eu-annex-11"  # §9 (qualification and validation)
based_on:
  - "GAMP 5 §D1 (capacity/performance requirements) + §D5 (risk-based testing; rigor scaled by RPN) + EU Annex 11 §9 (validation)"
  - "Structure: performance test protocol; URS-PERF SLAs as pass thresholds; load + stress + soak + recovery; high-RPN → mandatory stress"

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
    description: "Identifier + version of the FS that includes FS-PERF-NNN performance design points"
  urs_ref:
    type: string
    required: true
    description: "Identifier + version of the URS that includes URS-PERF-NNN SLA thresholds used as pass criteria"
  ra_det_ref:
    type: string
    required: false
    description: "Identifier of the Detailed Risk Assessment (RA-DET); used to scale stress test depth by RPN"
  gamp_category:
    type: enum
    required: true
    values: [3, 4, 5]
  test_environment:
    type: string
    required: true
    description: "Performance test environment: server specs, OS, network topology, DB engine + version, test client count, monitoring tooling"
  load_profile_definition:
    type: string
    required: true
    description: "How concurrent users / transactions / data volumes are modelled (e.g., ramp-up strategy, steady-state duration, peak burst parameters)"
  perf_tester_name:
    type: string
    required: true
  perf_reviewer_name:
    type: string
    required: true
    description: "Independent reviewer — must be a different person from the tester"
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
    - based_on_template: "PERF-TEST"
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
    - ra_det_ref           # populate when RA-DET is available and RPN influenced test design
    - deviations_count

# ─── Validation rules ────────────────────────────────────────────────────────
validation_rules:
  - "All placeholders with required: true must be filled"
  - "traces_to must point to both an approved FS and an approved URS"
  - "Each URS-PERF-NNN SLA must appear as a pass threshold in at least one PERF-TEST-TC-NNN"
  - "Each FS-PERF-NNN performance design point must be covered by at least one PERF-TEST-TC-NNN"
  - "Performance functions with high RPN (from RA-DET) must include at least one stress test case (beyond-SLA load)"
  - "Pass thresholds must be derived verbatim from URS-PERF SLAs — never invented or estimated"
  - "Actual result and Passed columns must remain BLANK at draft stage — never fabricate results"
  - "Tester and Reviewer must be different persons (segregation of duties)"
  - "All deviations must be escalated to the quality function before any action is defined"
  - "Protocol status must be 'draft' at authoring; transitions to 'in-execution' only with approval and with the test environment confirmed"

tags:
  - template
  - csv
  - performance-testing
  - perf-test
  - performance-verification
  - v-model
  - canonical
---

# PERF-TEST — Performance Testing

> [!note] Canonical CSV template
> **Canonical** template for the **Performance Testing protocol (PERF-TEST)** — the document that formally verifies that the system **`{{system_name}}`** meets its performance requirements (load, stress, scalability, response-time, throughput, availability, and recovery) as declared in [URS](URS.md) (`URS-PERF-NNN`) and [FS](FS.md) (`FS-PERF-NNN`). Complies with GAMP 5 §D1 (capacity/performance requirements) + §D5 (risk-based testing, rigor scaled by RPN) and EU Annex 11 §9 (qualification and validation).

> [!warning] Scope boundary with OQ
> OQ (`OQ-TC-NNN`) verifies **functional** behavior — does the function operate per the FS. PERF-TEST verifies **non-functional** performance characteristics — does the system sustain SLAs under realistic and adverse load. A brief reference to performance may appear in OQ §4.1 (special test types), but the authoritative performance evidence lives here. Results feed OQ, PQ, and VR.

> [!tip] Embedded usage rules
> 1. **SLA-anchored pass thresholds** — every pass threshold must be sourced verbatim from a `URS-PERF-NNN` SLA. No invented targets.
> 2. **Four test type tiers**: load (at expected volume), stress (beyond SLA), soak/endurance (sustained duration), recovery (after failure or overload).
> 3. **Risk-based depth** (GAMP 5 §D5) — high-RPN performance functions (from RA-DET) require at minimum a load test **and** a stress test. If RA-DET is absent, scale stress depth by RA-INIT Risk Priority (H/M/L) instead; only default to load-only if neither RA-DET nor RA-INIT exists. Low-RPN / Low-priority functions may use load-only with risk-acceptance documented.
> 4. **No fabrication** — Actual and Passed columns are left BLANK at draft; filled only during execution.
> 5. **Tester/Reviewer segregation** — same rule as OQ: different persons, deviation escalation to quality.
> 6. **Traceability** — each `PERF-TEST-TC-NNN` cites the `URS-PERF-NNN` or `FS-PERF-NNN` it verifies and the RPN of the associated risk (if RA-DET is available).

---

## 0. Identification and signatures

### System

| Field | Value |
|---|---|
| **System name** | `{{system_name}}` |
| **System identifier** | `{{system_id}}` |
| **FS being verified** | `{{fs_ref}}` ([FS](FS.md)) |
| **URS SLA source** | `{{urs_ref}}` ([URS](URS.md)) |
| **RA-DET (RPN scaling)** | `{{ra_det_ref}}` ([RA-DET](RA-DET.md)) |
| **GAMP category** | `{{gamp_category}}` |
| **Test environment** | `{{test_environment}}` |
| **Load profile definition** | `{{load_profile_definition}}` |

### Signatures

| Role | Name | Department | Date | Signature |
|---|---|---|---|---|
| Protocol author (SME / CSV) |  |  |  |  |
| Approver 1 (System Owner) |  |  |  |  |
| Approver 2 (Quality Unit) |  |  |  |  |
| **Tester** | `{{perf_tester_name}}` |  |  |  |
| **Reviewer** (independent) | `{{perf_reviewer_name}}` |  |  |  |

**Overall result**: ☐ Pass ☐ Pass with non-critical deviations (see §7) ☐ Fail · **Execution no.**: `______`

---

## 1. Objective

Formally verify that the system **`{{system_name}}`** meets the performance requirements declared in [URS](URS.md) (`{{urs_ref}}`, `URS-PERF-NNN` items) and the performance design points in [FS](FS.md) (`{{fs_ref}}`, `FS-PERF-NNN` items) across all applicable test types: **load**, **stress**, **soak/endurance**, and **recovery**. Pass thresholds are sourced verbatim from `URS-PERF` SLAs. High-RPN performance functions (per [RA-DET](RA-DET.md) `{{ra_det_ref}}`) require mandatory stress testing in addition to load testing. Results constitute evidence for the [OQ](OQ.md), [PQ](PQ.md), [RTM](RTM.md), and [Validation Report](VR.md).

---

## 2. Definitions and abbreviations

| Term | Definition |
|---|---|
| PERF-TEST | Performance Testing protocol — non-functional verification of load, stress, soak, and recovery behavior |
| Load test | Executes the system at the expected (nominal) concurrent-user volume and transaction rate defined in URS-PERF SLAs |
| Stress test | Executes the system beyond the expected SLA volume to identify the failure point and verify graceful degradation |
| Soak / Endurance test | Runs at nominal load for an extended period (hours / days) to detect memory leaks, resource exhaustion, or performance drift |
| Recovery test | Verifies that the system returns to normal performance within a defined RTO after an overload or failure event |
| SLA | Service Level Agreement — the measurable commitment (response time, throughput, availability %) declared in URS-PERF |
| RPN | Risk Priority Number — from RA-DET; scales the depth of performance testing required |
| Pass threshold | The quantitative acceptance criterion derived verbatim from a URS-PERF SLA |
| Actual result | Measured outcome recorded during execution (BLANK at draft) |

---

## 3. Test requirements and prerequisites

> [!warning] Execution rules
> - Execute only on an **approved copy** of the protocol.
> - Tester must be trained (GxP + VP + URS-PERF + system architecture) before executing.
> - The test environment must match the specification in §0 — deviations from the specified environment invalidate results and must be treated as deviations.
> - Tester ≠ Reviewer. Deviations escalated to quality before any action.
> - Actual and Passed fields remain BLANK until execution; never fabricate.

| Base document | Reference |
|---|---|
| User Requirements Specification (SLA source) | `{{urs_ref}}` |
| Functional Specification (performance design points) | `{{fs_ref}}` |
| Detailed Risk Assessment (RPN scaling) | `{{ra_det_ref}}` |
| Initial Risk Assessment (fallback risk-scaling if RA-DET absent) | [RA-INIT](RA-INIT.md) |
| Validation Plan | [VP](VP.md) |

---

## 4. Test strategy (risk-based)

> [!note] GAMP 5 §D5 — risk-based performance testing
> *"Fundamental to the risk-based approach is an acceptance that not all functionalities will be challenged and consequently not all defects will be found"* (§25.5 p.218). Performance test depth is scaled by RPN from RA-DET. **If RA-DET is absent, scale depth by RA-INIT Risk Priority (H/M/L) instead — a protocol must not lose risk-scaling because the detailed FMEA was not produced. Only default to load-only when neither RA-DET nor RA-INIT exists.** High-RPN / High-priority performance functions require load **and** stress. Low-RPN / Low-priority functions may use load-only with documented risk-acceptance.

### 4.1 Test type applicability by risk

> Primary risk source is RPN from RA-DET (detailed FMEA). When RA-DET is not available, map RA-INIT Risk Priority H/M/L onto the High/Medium/Low rows below.

| RPN (RA-DET) — or RA-INIT Risk Priority fallback | Required test types |
|---|---|
| **High** | Load test **+** Stress test (mandatory). Soak and recovery recommended and activated if URS-PERF declares availability / RTO SLAs |
| **Medium** | Load test (mandatory). Stress test where URS-PERF declares a ceiling or degradation SLA |
| **Low** | Load test or supplier performance evidence / benchmark accepted. Risk-acceptance documented |

### 4.2 Test type definitions and activation criteria

| Test type | Activation criterion | Pass signal |
|---|---|---|
| **Load** | Always — for every `URS-PERF-NNN` SLA in scope | Response time / throughput meets SLA at nominal concurrency |
| **Stress** | RPN=High **or** URS-PERF declares a capacity ceiling | System degrades gracefully (no data loss, no silent failure) beyond SLA volume; error messages are informative |
| **Soak / Endurance** | URS-PERF declares availability % SLA or continuous-operation requirement | No performance drift or resource exhaustion over the specified duration |
| **Recovery** | URS-PERF declares an RTO or failover SLA | System recovers to nominal SLA within declared RTO after controlled overload or failure |

### 4.3 Test environment and load profile

**Test environment**: `{{test_environment}}`

**Load profile definition**: `{{load_profile_definition}}`

> [!warning] Environment representativeness
> Performance results are only valid for the environment described in §0. If production infrastructure differs materially from the test environment, a risk-acceptance note is required in §8, referencing the specific differences.

---

## 5. Test Cases

> Central section — one row per test case. Each `URS-PERF-NNN` SLA must be verified by at least one `PERF-TEST-TC-NNN`. High-RPN functions require at minimum one load case **and** one stress case. Actual and Passed columns remain BLANK at draft.

| PERF-TEST-TC | Verifies (URS/FS-PERF-ID) | Test type | Load profile | Pass threshold (from URS SLA) | Actual result | Passed (✓/✗) |
|---|---|---|---|---|---|---|
| `PERF-TEST-TC-001` | `URS-PERF-001` | Load | *e.g.: 50 concurrent users, steady-state 30 min* | *e.g.: p95 response time ≤ 3 s; throughput ≥ 200 tx/min* | | |
| `PERF-TEST-TC-002` | `URS-PERF-001` | Stress | *e.g.: ramp from 50 → 200 concurrent users over 10 min* | *e.g.: no data loss; graceful error at >150 users; recovery within 5 min of load reduction* | | |
| `PERF-TEST-TC-003` | `URS-PERF-002` | Soak | *e.g.: 50 concurrent users, continuous 4 h* | *e.g.: p95 response time remains ≤ 3 s throughout; no memory growth >10%* | | |
| `PERF-TEST-TC-004` | `URS-PERF-003` | Recovery | *e.g.: simulate DB overload; monitor return to nominal* | *e.g.: system returns to ≤ 3 s p95 within RTO ≤ 10 min* | | |
| `PERF-TEST-TC-005+` | | | | | | |

> [!note] High-risk functions require stress
> If RA-DET assigns RPN=High to a performance function — or, when RA-DET is absent, RA-INIT assigns Risk Priority=H — the corresponding URS-PERF-NNN must have at minimum two test cases: one Load (`PERF-TEST-TC-NNN`) and one Stress (`PERF-TEST-TC-NNN+1`). Document if this requirement is not applicable with explicit risk-acceptance.

*Tester / Reviewer signature at close of test execution:* ______ / ______

---

## 6. Performance coverage (traceability summary)

> Confirms that each `URS-PERF-NNN` and `FS-PERF-NNN` in scope has at least one `PERF-TEST-TC-NNN`. Low-RPN items not stress-tested are documented with risk-acceptance.

| URS/FS-PERF-ID | SLA (pass threshold) | RPN | Test cases verifying it | Covered (✓) / Risk-accepted |
|---|---|---|---|---|
| `URS-PERF-001` | | | `PERF-TEST-TC-001`, `PERF-TEST-TC-002` | |
| `URS-PERF-002` | | | `PERF-TEST-TC-003` | |
| `URS-PERF-003` | | | `PERF-TEST-TC-004` | |
| `FS-PERF-001` | | | | |

---

## 7. Overall evaluation / Deviations

| Test ID | Expected result | Actual result | Evaluation | Action | Owner | Date | Completed |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

---

## 8. Results summary and conclusion

| Metric | Value |
|---|---|
| Total PERF-TEST-TC | |
| Passed / Failed | |
| Deviations (critical / non-critical) | |
| URS-PERF SLAs covered / total in scope | |
| FS-PERF design points covered / total | |
| High-RPN functions with stress test / total high-RPN | |
| Risk-accepted items (load-only or not tested) | |
| Environment representativeness note | |

**Conclusion**: ☐ System meets all URS-PERF SLAs; results documented for OQ / PQ / VR. ☐ Pass with non-critical deviations. ☐ Fail.

---

## 9. Appendices list (evidence)

| Appendix no. | Description | No. of pages |
|---|---|---|
|  | *e.g.: load test tool output (JMeter / Gatling / k6 report)* | |
|  | *e.g.: monitoring screenshots (CPU, memory, response-time graphs)* | |
|  | *e.g.: soak test resource utilisation log* | |
|  | *e.g.: recovery test timeline log* | |

---

## 10. Related documents

| Document | Reference |
|---|---|
| User Requirements Specification (SLA source) | `{{urs_ref}}` ([URS](URS.md)) |
| Functional Specification (performance design points) | `{{fs_ref}}` ([FS](FS.md)) |
| Detailed Risk Assessment (RPN scaling) | `{{ra_det_ref}}` ([RA-DET](RA-DET.md)) |
| Initial Risk Assessment (fallback risk-scaling) | [RA-INIT](RA-INIT.md) |
| Operational Qualification (functional verification) | [OQ](OQ.md) |
| Performance Qualification (fitness for use) | [PQ](PQ.md) |
| Requirements Traceability Matrix | [RTM](RTM.md) |
| Validation Report | [VR](VR.md) |
| `{{custom_ref}}` | |

---

## 11. Revision history

| Version | Date | Reason for revision / Author |
|---|---|---|
| 01 | DD.MM.YYYY | Initial issue |
|  |  |  |

---

## Canonical notes for implementers

> [!note] PERF-TEST is non-functional verification — distinct from OQ
> OQ verifies that functions operate per the FS (functional behavior). PERF-TEST verifies that the system sustains its URS-PERF SLAs under load (non-functional). Both are required for regulated computerized systems. OQ §4.1 may reference PERF-TEST results, but PERF-TEST is the authoritative evidence source for performance.

> [!note] Pass thresholds are URS-PERF SLAs — never estimated
> Every pass threshold in the test case table must be sourced verbatim from a `URS-PERF-NNN` SLA declared in the URS. If a URS-PERF item does not exist for a performance characteristic under test, either add it to the URS (change control) or document the gap before executing.

> [!tip] Risk-based, not exhaustive
> GAMP 5 §D5 accepts that not all scenarios are challenged. Low-RPN performance functions may be verified by load test only (or by supplier benchmark evidence), with risk-acceptance documented in §6. Do not falsely claim stress-coverage when only load was run.

> [!tip] Category-awareness
> - **Cat 3**: PERF-TEST focuses on configured performance behaviour; supplier benchmarks may partially substitute with documented risk-acceptance.
> - **Cat 4**: PERF-TEST covers configuration-dependent performance and business-process throughput under real workflow volumes.
> - **Cat 5**: PERF-TEST covers custom code performance paths; includes profiling data and regression baselines if the system has prior releases.

> [!warning] Environment gap caveat
> If the performance test environment is materially less powerful than production (common for cost reasons), document the delta explicitly in §8 and include a risk-acceptance note. Regulatory reviewers will ask: "How do you know production meets SLAs if you only tested on a smaller environment?"

## Related

- [URS](URS.md) · [FS](FS.md) · [RA-DET](RA-DET.md) · [RA-INIT](RA-INIT.md) · [OQ](OQ.md) · [PQ](PQ.md) · [RTM](RTM.md) · [VR](VR.md)
- GAMP 5 · EU Annex 11
- V-Model · performance testing · risk based testing

---

## Instantiation flow (for AI agents)

> [!note] This section is NOT copied into the instance. It is guidance for the `gdd.perf-test.from-urs` skill.

### Pre-flight

1. **Read `.gxp-dev.yaml`** from the consumer project. If it does not exist → redirect to `/gdd.init`.
2. **Locate approved URS** (`specs/URS.md`) — source of `URS-PERF-NNN` SLAs that define pass thresholds.
3. **Locate approved FS** (`specs/FS.md`) — source of `FS-PERF-NNN` performance design points.
4. **Locate RA-DET** (`specs/RA-DET.md`) if available — extract RPN values for performance functions to scale stress test requirement. If RA-DET absent → fall back to **RA-INIT** (`specs/RA-INIT.md`) and scale by its Risk Priority (H/M/L). Only if neither exists → note and default to load-only with risk-acceptance for all items.
5. **Read `templates/csv/PERF-TEST.md`** from the toolkit as the source template (this file).

### Generation flow

1. **Parse all `URS-PERF-NNN` items** from the URS. Each SLA field becomes a pass threshold in a `PERF-TEST-TC-NNN` row.
2. **Parse all `FS-PERF-NNN` items** from the FS. Map each to the `URS-PERF-NNN` it implements; add test cases where FS-PERF items introduce additional measurable performance points.
3. **For each performance item**, generate at minimum one Load test case:
   - Populate: Test type = Load, Load profile = from `URS-PERF-NNN` concurrency/volume definition, Pass threshold = verbatim from `URS-PERF-NNN` SLA.
4. **For each high-risk item**, generate an additional Stress test case — high-risk = RPN=High from RA-DET, or (if RA-DET absent) Risk Priority=H from RA-INIT:
   - Load profile = beyond-SLA volume (e.g., 2–3× expected concurrency); Pass threshold = graceful degradation (no data loss, informative error, recovery within declared RTO).
5. **Activate Soak / Recovery cases** if `URS-PERF-NNN` declares availability % or RTO SLA fields.
6. **Document risk-acceptance** for low-RPN items verified by load-only (§6 coverage table).
7. **Anti-hallucination**: use `[NEEDS CLARIFICATION: ...]` when a pass threshold, load profile parameter, or RPN value is missing; never fabricate test results, SLA values, or RPN scores.
8. **Leave Actual result and Passed columns BLANK** — they are filled only during execution.
9. **Output**: write `specs/PERF-TEST.md` (status: draft); print coverage summary (URS-PERF SLAs covered / total).
10. **Post-flight**: `validate-frontmatter.py` + `check-clarification-markers.py` + `generate-rtm.py`.

### `status` transitions

```
draft ──[complete protocol + approved]──> in-execution
in-execution ──[executed + evidence appended]──> executed
executed ──[reviewer signs + deviations closed]──> approved
approved ──[new version issued]──> superseded
```

### Mapping

| Origin (PERF-TEST) | Destination | Rule |
|---|---|---|
| `PERF-TEST-TC-NNN` | Row in `RTM.md` | Performance verification coverage for URS-PERF and FS-PERF IDs |
| PERF-TEST approved | Referenced in `OQ.md` §4.1 and `PQ.md` | OQ and PQ reference PERF-TEST as evidence for performance characteristics |
| PERF-TEST summary | `VR.md` | Validation Report summarises PERF-TEST results alongside OQ and PQ |
