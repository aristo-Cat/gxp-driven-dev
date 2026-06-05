---
title: Requirements Traceability Matrix (derived)
type: derived
generator: skills/_scripts/generate-rtm.py
generated_at: "2026-06-05T07:07:34+00:00"
status: auto-generated
---

# Requirements Traceability Matrix (RTM)

> ⚙ This file is **derived automatically** from `specs/*.md` by `skills/_scripts/generate-rtm.py`. **Do not hand-edit** — re-run the generator instead.

**Generated at**: `2026-06-05T07:07:34+00:00`

## Summary

- Spec files scanned: **9**
- Total requirement IDs declared: **215**
- Forward-trace links: **198**
- IDs without downstream: **98**
- Dangling references: **0**

## Requirement IDs per spec file

| Spec file | DOC-TYPE | Own IDs | References others |
|---|---|---:|---:|
| `CS.md` | CS | 20 | 29 |
| `FS.md` | FS | 72 | 75 |
| `IQ.md` | IQ | 15 | 12 |
| `OQ.md` | OQ | 14 | 18 |
| `PQ.md` | PQ | 4 | 13 |
| `RA-DET.md` | RA-DET | 4 | 16 |
| `RA-INIT.md` | RA-INIT | 10 | 14 |
| `URS.md` | URS | 76 | 0 |
| `VR.md` | VR | 0 | 13 |

## Forward traceability (upstream → downstream)

| Upstream ID | Downstream IDs |
|---|---|
| `CS-API-001` | `IQ-TC-011` |
| `CS-API-002` | `IQ-TC-012` |
| `CS-DATA-001` | `IQ-TC-010` |
| `CS-FUNC-001` | `IQ-TC-007` |
| `CS-FUNC-002` | `IQ-TC-006` |
| `CS-SEC-001` | `IQ-TC-008` |
| `CS-SEC-003` | `IQ-TC-009` |
| `CS-SEC-004` | `IQ-TC-013` |
| `FS-API-002` | `CS-API-001`, `OQ-TC-013`, `OQ-TC-014` |
| `FS-API-003` | `CS-API-002` |
| `FS-DEVENV-001` | `IQ-TC-004` |
| `FS-DOCS-001` | `IQ-TC-014`, `IQ-TC-015` |
| `FS-EREC-005` | `CS-EREC-001`, `OQ-TC-009`, `RA-DET-003` |
| `FS-EREC-009` | `CS-SEC-001` |
| `FS-EREC-014` | `CS-EREC-002`, `RA-DET-003` |
| `FS-ESIG-002` | `CS-ESIG-001`, `OQ-TC-010`, `OQ-TC-011` |
| `FS-ESIG-009` | `CS-SEC-005` |
| `FS-ESIG-017` | `CS-ESIG-002`, `OQ-TC-010`, `OQ-TC-011` |
| `FS-FLOW-001` | `CS-FLOW-001`, `OQ-TC-002`, `RA-DET-002` |
| `FS-FUNC-001` | `CS-FUNC-001`, `OQ-TC-001`, `OQ-TC-002`, `RA-DET-002` |
| `FS-FUNC-002` | `CS-SEC-002`, `OQ-TC-005`, `OQ-TC-006`, `RA-DET-003` |
| `FS-FUNC-003` | `CS-FUNC-002`, `CS-FUNC-003`, `OQ-TC-003`, `OQ-TC-004`, `RA-DET-001` |
| `FS-FUNC-005` | `CS-FUNC-004` |
| `FS-OPS-001` | `CS-OPS-001`, `RA-DET-002` |
| `FS-PERF-004` | `CS-DATA-001` |
| `FS-PERIPH-001` | `CS-PERIPH-001`, `IQ-TC-005`, `OQ-TC-007`, `OQ-TC-008`, `RA-DET-004` |
| `FS-REPORT-001` | `CS-REPORT-001` |
| `FS-SEC-001` | `CS-SEC-003` |
| `FS-SEC-002` | `CS-SEC-004`, `OQ-TC-012` |
| `RA-DET-001` | `CS-API-001`, `CS-FUNC-003`, `OQ-TC-003`, `OQ-TC-004` |
| `RA-DET-002` | `CS-FLOW-001`, `OQ-TC-001`, `OQ-TC-002` |
| `RA-DET-003` | `CS-SEC-002`, `OQ-TC-005`, `OQ-TC-006` |
| `RA-DET-004` | `CS-PERIPH-001`, `OQ-TC-007`, `OQ-TC-008` |
| `RA-INIT-001` | `OQ-TC-003`, `OQ-TC-004`, `OQ-TC-013`, `OQ-TC-014`, `RA-DET-001` |
| `RA-INIT-002` | `OQ-TC-001`, `OQ-TC-002`, `RA-DET-002` |
| `RA-INIT-004` | `OQ-TC-005`, `OQ-TC-006`, `RA-DET-003` |
| `RA-INIT-009` | `IQ-TC-005`, `OQ-TC-007`, `OQ-TC-008`, `RA-DET-004` |
| `URS-API-001` | `FS-API-001` |
| `URS-API-002` | `CS-API-001`, `FS-API-002`, `PQ-SCEN-002`, `RA-INIT-006` |
| `URS-API-003` | `CS-API-002`, `FS-API-003` |
| `URS-ARCH-001` | `FS-ARCH-001` |
| `URS-ARCH-002` | `FS-ARCH-002` |
| `URS-DATA-001` | `FS-DATA-001` |
| `URS-DATA-002` | `FS-DATA-002` |
| `URS-DELIV-001` | `FS-DELIV-001` |
| `URS-DELIV-002` | `FS-DELIV-002` |
| `URS-DEVENV-001` | `FS-DEVENV-001` |
| `URS-DOCS-001` | `FS-DOCS-001` |
| `URS-EREC-001` | `FS-EREC-001` |
| `URS-EREC-002` | `FS-EREC-002` |
| `URS-EREC-003` | `FS-ARCH-001`, `FS-EREC-003`, `FS-PERF-004` |
| `URS-EREC-004` | `FS-EREC-004`, `FS-EREC-009` |
| `URS-EREC-005` | `FS-EREC-005`, `RA-INIT-003` |
| `URS-EREC-006` | `FS-EREC-006` |
| `URS-EREC-007` | `FS-EREC-007` |
| `URS-EREC-008` | `FS-EREC-008` |
| `URS-EREC-009` | `FS-EREC-009` |
| `URS-EREC-010` | `FS-DEVENV-001`, `FS-EREC-010` |
| `URS-EREC-011` | `FS-EREC-011` |
| `URS-EREC-012` | `FS-EREC-012` |
| `URS-EREC-013` | `FS-EREC-013`, `FS-FLOW-001`, `FS-PERIPH-001` |
| `URS-EREC-014` | `FS-EREC-014`, `RA-INIT-003` |
| `URS-ESIG-001` | `FS-ESIG-001`, `FS-PROC-002` |
| `URS-ESIG-002` | `FS-ESIG-002`, `PQ-SCEN-003` |
| `URS-ESIG-003` | `FS-ESIG-003` |
| `URS-ESIG-004` | `FS-ESIG-004` |
| `URS-ESIG-005` | `FS-ESIG-005` |
| `URS-ESIG-006` | `FS-ESIG-006` |
| `URS-ESIG-007` | `FS-ESIG-007` |
| `URS-ESIG-008` | `FS-ESIG-008` |
| `URS-ESIG-009` | `FS-ESIG-009` |
| `URS-ESIG-010` | `FS-ESIG-010` |
| `URS-ESIG-011` | `FS-ESIG-011` |
| `URS-ESIG-012` | `FS-ESIG-012` |
| `URS-ESIG-013` | `FS-ESIG-013` |
| `URS-ESIG-014` | `FS-ESIG-014` |
| `URS-ESIG-015` | `FS-ESIG-015` |
| `URS-ESIG-016` | `FS-ESIG-016` |
| `URS-ESIG-017` | `FS-ESIG-017`, `RA-INIT-005` |
| `URS-ESIG-018` | `FS-ESIG-018` |
| `URS-FLOW-001` | `FS-FLOW-001`, `RA-INIT-002` |
| `URS-FUNC-001` | `FS-FUNC-001`, `PQ-SCEN-001`, `RA-DET-002`, `RA-INIT-002` |
| `URS-FUNC-002` | `FS-EREC-005`, `FS-FUNC-002`, `PQ-SCEN-004`, `RA-DET-003`, `RA-INIT-004` |
| `URS-FUNC-003` | `FS-FUNC-003`, `PQ-SCEN-002`, `RA-DET-001`, `RA-INIT-001` |
| `URS-FUNC-004` | `FS-FUNC-004` |
| `URS-FUNC-005` | `FS-ESIG-002`, `FS-FUNC-005`, `PQ-SCEN-003`, `RA-INIT-005` |
| `URS-OPS-001` | `CS-OPS-001`, `FS-OPS-001`, `RA-INIT-010` |
| `URS-OPS-002` | `FS-OPS-002` |
| `URS-OPS-003` | `FS-OPS-003` |
| `URS-PERF-001` | `CS-FUNC-001`, `FS-PERF-001`, `PQ-SCEN-001` |
| `URS-PERF-002` | `FS-PERF-002`, `RA-INIT-007` |
| `URS-PERF-003` | `FS-PERF-003` |
| `URS-PERF-004` | `CS-DATA-001`, `FS-PERF-004` |
| `URS-PERIPH-001` | `FS-PERIPH-001`, `RA-DET-004`, `RA-INIT-009` |
| `URS-PERIPH-002` | `FS-FLOW-001`, `FS-PERIPH-002` |
| `URS-PROC-001` | `FS-PROC-001` |
| `URS-PROC-002` | `FS-EREC-014`, `FS-PROC-002` |
| `URS-QUAL-001` | `FS-QUAL-001` |
| `URS-QUAL-002` | `FS-QUAL-002` |
| `URS-REPORT-001` | `CS-REPORT-001`, `FS-REPORT-001` |
| `URS-REPORT-002` | `FS-REPORT-002` |
| `URS-SEC-001` | `FS-SEC-001`, `RA-INIT-008` |
| `URS-SEC-002` | `FS-SEC-002` |
| `URS-SEC-003` | `FS-SEC-003` |
| `URS-TEST-001` | `FS-TEST-001` |
| `URS-TEST-002` | `FS-TEST-002` |
| `URS-TRAIN-001` | `FS-TRAIN-001` |
| `URS-TRAIN-002` | `FS-TRAIN-002` |
| `URS-UI-002` | `FS-UI-002` |

## Gaps and orphans

### IDs with no downstream reference

These requirements are declared but never referenced by any downstream document. This is acceptable for:
- Requirements at the **last layer** of the V-Model (e.g. `PQ-*` IDs)
- Requirements marked `GxP=N` (out of scope of formal validation)

Investigate if these IDs should have downstream consumers:

- `CS-EREC-001`
- `CS-EREC-002`
- `CS-ESIG-001`
- `CS-ESIG-002`
- `CS-FLOW-001`
- `CS-FUNC-003`
- `CS-FUNC-004`
- `CS-PERIPH-001`
- `CS-REPORT-001`
- `CS-SEC-002`
- `CS-SEC-005`
- `FS-API-001`
- `FS-ARCH-001`
- `FS-ARCH-002`
- `FS-DATA-001`
- `FS-DATA-002`
- `FS-DELIV-002`
- `FS-EREC-001`
- `FS-EREC-002`
- `FS-EREC-003`
- `FS-EREC-004`
- `FS-EREC-006`
- `FS-EREC-007`
- `FS-EREC-008`
- `FS-EREC-010`
- `FS-EREC-011`
- `FS-EREC-012`
- `FS-EREC-013`
- `FS-ESIG-001`
- `FS-ESIG-003`
- `FS-ESIG-004`
- `FS-ESIG-005`
- `FS-ESIG-006`
- `FS-ESIG-007`
- `FS-ESIG-008`
- `FS-ESIG-010`
- `FS-ESIG-011`
- `FS-ESIG-012`
- `FS-ESIG-013`
- `FS-ESIG-014`
- `FS-ESIG-015`
- `FS-ESIG-016`
- `FS-ESIG-018`
- `FS-FUNC-004`
- `FS-OPS-002`
- `FS-PERF-001`
- `FS-PERF-002`
- `FS-PERF-003`
- `FS-PERIPH-002`
- `FS-PROC-002`
- … and 48 more

