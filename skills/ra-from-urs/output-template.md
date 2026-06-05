# `gdd.ra.from-urs` — Output Template Reference

The exact shape of the `specs/RA-INIT.md` produced by the skill. Mirrors `templates/csv/RA-INIT.md` with placeholders substituted. A worked, validated example is `examples/temp-logger-gmp-chamber/specs/RA-INIT.md`.

---

## Frontmatter (instance shape)

```yaml
---
title: "RA-INIT — Initial Risk Assessment for {{system_name}}"
type: instance
based_on_template: "RA-INIT"
based_on_template_version: "0.1.0"
project_id: "{{project_id}}"
system_id: "{{system_id}}"
traces_to: "specs/URS.md ({{urs version}}, {{urs status}})"
gamp_category: {{1|3|4|5}}          # the decided category — key output
status: draft
version: "0.1"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
language: "{{language from .gxp-dev.yaml}}"
detailed_ra_ref: "specs/RA-DET.md (planned)"   # ONLY if detailed_ra_required: true

# Copied from .gxp-dev.yaml for self-contained reference
profile: "{{profile}}"
mode: "{{mode}}"
part11_applicable: {{bool}}
---
```

`detailed_ra_ref` is conditional (present only when `detailed_ra_required: true`). `approved_by` / `supersedes` appear only at the relevant status.

---

## Body sections (mirror the template, omit none that apply)

### 0. Identification and signatures
- System table: name, identifier, **URS assessed** (with version/status), **GxP business process**, **determined GAMP category**.
- Signature table: Author, Reviewer 1 = **Process Owner** *(owner of severity)*, Reviewer 2 = SME, Approver 1 = System Owner, Approver 2 = Quality Unit. Unknown signatories → `[NEEDS CLARIFICATION: assign <role>]`.
- Keep the approval-order `> [!warning]` (RA-INIT approved before URS). If the URS was authored first (as in a smoke test), say so and state that this RA-INIT *confirms* the URS's category/presets.

### 1. Objective
One paragraph: this performs Step 1 + Step 2 of the GAMP 5 five-step QRM for `{{system_name}}`; steps 3-5 live in RA-DET + operation.

### 3. Methodology
Brief: qualitative H/M/L, `Class = Severity × Probability`, `Priority = Class × Detectability`, matrices per the template §3.1-3.2. (Do not re-paste the full matrices; reference them.)

### 4. System context and boundary
- `system_boundary` — what's inside/outside the analysis.
- `business_process` — origin of severity.

### 5. Step 1
- 5.1 GxP determination (`gxp_determination`).
- 5.2 System impact — the PS/PQ/DI table with H/M/L + justification per axis; overall `system_impact`.
- 5.3 GAMP category — `gamp_category_decision` + `gamp_category_rationale` + the §M4 criteria table with "Applies?" filled (one Yes).
- 5.4 Part 11/Annex 11 — the 5-question table with Yes/No + preset consequence; a one-line consistency note vs the URS presets.

### 6. Step 2 — functions with impact
Table: `URS-ID | Function | Impacts PS | Impacts PQ | Impacts DI | GxP-critical?`. One row per GxP=Y URS requirement (plus clearly non-GxP ones marked No for completeness). Only real URS-IDs.

### 7. Initial Risk Register — `RA-INIT-NNN`
The 10-column table exactly as the template:
`RA-ID | Assesses (URS-ID) | Risk (potential failure) | Severity | Probability | Risk Class | Detectability | Risk Priority | Initial control | Proceed to RA-DET?`
- `RA-INIT-NNN` sequential from 001.
- `Assesses` = a real `URS-<CAT>-NNN` or the literal `system-level`.
- Ratings consistent with the §3.1/§3.2 matrices.
- After the table, a bold line listing the Risk Priority = H functions that proceed to RA-DET.

### 8. RA-DET decision
`detailed_ra_required` (true/false) + the trigger table (system_impact high / Cat 4-5 / ≥1 Priority H) + final decision & justification.

### 9. Related documents
URS assessed, GXP-ASSESS, RA-DET (if required), VP.

### 10. Revision history
| 0.1 | <today> | Initial draft (RA-INIT) — <author>, <dept> |

---

## Anti-patterns in the output

Do NOT produce:
- ❌ A category with no rationale, or a category invented without §M4 justification.
- ❌ Risk ratings (`H/M/L`) that don't follow the §3.1/§3.2 matrices, or fabricated ratings where the user couldn't supply info (use `[NEEDS CLARIFICATION:]`).
- ❌ `RA-INIT-NNN` citing a `URS-ID` that does not exist in `specs/URS.md`.
- ❌ Severity inflated because the system is Cat 5 (severity comes from the process, not the category).
- ❌ `status: approved` (requires human signatures; and RA-INIT approves before the URS).
- ❌ Any banned legacy category code or corporate/site/heritage identifier (see the anonymization rule in `CLAUDE.md`).
- ❌ Regulatory §-citations beyond what the template carries (GAMP 5 §5.3/§M3/§M4, ICH Q9, EU Annex 11 §4).
- ❌ `[NEEDS CLARIFICATION:` without a question after the colon.
