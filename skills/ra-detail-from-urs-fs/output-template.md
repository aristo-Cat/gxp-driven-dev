# `gdd.ra.detail.from-urs-fs` — Output Template Reference

The exact shape of the `specs/RA-DET.md` produced by the skill. Mirrors `templates/csv/RA-DET.md` with placeholders substituted. A worked, validated example is `examples/temp-logger-gmp-chamber/specs/RA-DET.md` (FMEA on 4 high-risk functions, one residual risk).

---

## Frontmatter (instance shape)

```yaml
---
title: "RA-DET — Detailed Risk Assessment (FMEA) for {{system_name}}"
type: instance
based_on_template: "RA-DET"
based_on_template_version: "0.1.0"
project_id: "{{project_id}}"
system_id: "{{system_id}}"
traces_to: "specs/RA-INIT.md ({{ver}}, {{status}}) + specs/URS.md (...) + specs/FS.md (...)"
gamp_category: {{4|5}}
status: draft
version: "0.1"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
language: "{{language from .gxp-dev.yaml}}"
residual_risk_accepted_by: "{{accepter or 'pending — see §5'}}"   # only if §5 has residual risk

# Copied from .gxp-dev.yaml for self-contained reference
profile: "{{profile}}"
mode: "{{mode}}"
---
```

---

## Body sections (mirror the template)

### 0. Identification and signatures
System table (name, identifier, **RA-INIT that triggers it**, URS analyzed, FS analyzed, GAMP category, **scope of analysis** = the RA-INIT Priority-H functions). Signatures: Author (SME/CSV), Reviewer = **Process Owner** *(owner of Relevance)*, Approver 1 = System Owner, Approver 2 = Quality Unit. Unknown → `[NEEDS CLARIFICATION: assign <role>]`. Keep a `> [!warning]` cascade-order note if RA-INIT/URS/FS are still draft.

### 1. Objective
One paragraph: detailed FMEA of the high-risk functions from RA-INIT; Step 3 of the QRM process (GAMP 5 §M3).

### 3. FMEA methodology
Brief: `RPN = O × R × D` (1-3 each, 1-27 range); R = process severity held constant; double evaluation; target RPN₂ ≤ 4; RPN→rigor 1-4/6-9/12-27. (Reference the template scales; don't re-paste the full tables.)

### 4. Risk Analysis (FMEA) — the core table
The 16-column table exactly as the template:
`RA-DET-ID | Analyzes (URS/FS-ID) | Details (RA-INIT) | Potential failure | Cause | Consequence (PS/PQ/DI) | Existing controls | O₁ | R₁ | D₁ | RPN₁ | Mitigation measures | O₂ | R₂ | D₂ | RPN₂`
- One row per RA-INIT Priority-H function (≥1 each).
- `RA-DET-NNN` sequential from 001.
- RPN₁ = O₁×R₁×D₁; RPN₂ = O₂×R₂×D₂; **R₂ = R₁**.
- After the table, a one-line note reaffirming R is held constant (severity not mitigable).

### 5. Residual risk
Table for every RPN₂ > 4: `RA-DET-ID | Residual RPN | Justification for acceptance | Accepted by | Date`. Acceptance pending → `[NEEDS CLARIFICATION: residual risk acceptance by Process Owner + QU]`. If no residual > 4, state "No residual risks above the RPN ≤ 4 target."

### 6. Summary and link to testing
Metrics table (total analyzed / # RPN₁ 12-27 / # mitigated ≤4 / # residual >4) + the **Link to OQ/PQ**: which functions need positive / negative / stress testing, named per RA-DET-ID. This feeds `gdd.tests.from-ra`.

### 7. Related documents
RA-INIT, URS, FS, OQ, PQ, VR.

### 8. Revision history
| 0.1 | <today> | Initial draft (RA-DET) — <author>, <dept> |

---

## Anti-patterns in the output

Do NOT produce:
- ❌ An RPN that does not equal O × R × D, or a factor outside 1-3.
- ❌ Relevance reduced between eval 1 and eval 2 (severity is process-driven, not mitigable).
- ❌ A detailed FMEA of low-priority functions (RA-DET is only for the RA-INIT Priority-H set).
- ❌ A residual RPN₂ > 4 not recorded in §5 with acceptance.
- ❌ A row that does not cite both the URS/FS-ID **and** the RA-INIT-NNN it details.
- ❌ Fabricated risk ratings where information is missing (use `[NEEDS CLARIFICATION:]`).
- ❌ Regulatory §-citations beyond the template's (GAMP 5 §M3/§5/§11.5.4, ICH Q9, EU Annex 11 §4).
- ❌ `status: approved`, or any banned legacy category code / corporate identifier (see the anonymization rule in `CLAUDE.md`).
