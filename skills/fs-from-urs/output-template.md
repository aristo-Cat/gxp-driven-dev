# `gdd.fs.from-urs` — Output Template Reference

The exact shape of the `specs/FS.md` produced by the skill. Mirrors `templates/csv/FS.md` with placeholders substituted. A worked, validated example is `examples/temp-logger-gmp-chamber/specs/FS.md` (72 FS-IDs, full URS GxP=Y coverage).

---

## Frontmatter (instance shape)

```yaml
---
title: "FS — Functional Specification for {{system_name}}"
type: instance
based_on_template: "FS"
based_on_template_version: "0.1.0"
project_id: "{{project_id}}"
system_id: "{{system_id}}"
traces_to: "specs/URS.md ({{urs version}}, {{urs status}})"
gamp_category: {{3|4|5}}
status: draft
version: "0.1"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
language: "{{language from .gxp-dev.yaml}}"
deviations_logged: {{bool}}          # true if §4.2 records deviations

# Copied from .gxp-dev.yaml for self-contained reference
profile: "{{profile}}"
mode: "{{mode}}"
---
```

`approved_by` / `supersedes` appear only at the relevant status.

---

## Body sections (mirror the template)

### 0. Identification and signatures
System table (name, identifier, **URS being realized** + status, supplier, version, GAMP category) + signature table: Author (often the supplier or CSV coordinator), Reviewer 1 = System Owner/IT, Reviewer 2 = SME/Process Owner, Reviewer 3 = **Data Owner**, Approver 1 = System Owner, Approver 2 = Quality Unit. Unknown → `[NEEDS CLARIFICATION: assign <role>]`. If the URS is still draft (smoke-test / parallel work), keep a `> [!warning]` cascade-order note.

### 1. Introduction
One paragraph: this FS realizes the URS for `{{system_name}}`; it is the FS phase of the V-Model, verified in the OQ. For Cat 4, note that concrete settings/values live in the CS.

### 2. Definitions and abbreviations
FS/URS/CS/DS + project-specific terms.

### 4.1 System Overview
The realization overview: modules, key interfaces, high-level architecture. Cat-aware (configured COTS vs custom build).

### 4.2 Deviations to URS
The deviations table (affected URS-ID | deviation | impact | action). Empty + a one-line "no deviations" note if none; set `deviations_logged` accordingly.

### 4.5 URS → FS traceability coverage (summary)
**Per-category** table: `Category | URS GxP=Y | FS entries | Coverage`. End with **"Blocking gaps (GxP=Y or prio=H without FS realization): none."** Do NOT render 1 row per URS-ID — the per-ID traces are in sections 5–11 (and are what the RTM reads).

### 5–11. Realization tables (the body)
One section per category that has ≥1 realization, each a table:
`FS ID-No. | Realizes (URS-ID) | Realization (how)`
- `FS-<CAT>-NNN` sequential from 001 within the category.
- "Realizes" cites a real `URS-<CAT>-NNN`.
- "Realization (how)" = the technical mechanism, **not** the URS text.
- Sections 9.2 (FS-EREC) / 9.3 (FS-ESIG) are mandatory and non-empty if those URS presets are active. Keep N/A preset rows with "N/A — <reason>".
- For GxP=N requirements left 1:0, add a one-line note under the section ("`URS-XXX-NNN` is GxP=N → 1:0, no FS realization required").

### 12. Related documents
URS, RA-INIT, CS (Cat 4) / DS (Cat 5), RA-DET, VP.

### 13. Revision history
| 0.1 | <today> | Initial draft (FS) — <author>, <dept> |

---

## Anti-patterns in the output

Do NOT produce:
- ❌ An FS row whose "Realization" merely repeats the URS WHAT (must add the technical HOW).
- ❌ A GxP=Y / prio=H URS requirement with no FS realization (blocking coverage gap).
- ❌ `FS-<CAT>-NNN` whose "Realizes" cites a `URS-ID` not present in `specs/URS.md`.
- ❌ A new category code not in the URS / not in the 22 canonical acronyms.
- ❌ Invented technical mechanisms where the realization is undecided (use `[NEEDS CLARIFICATION:]`).
- ❌ Regulatory §-citations beyond what the template carries (GAMP 5 §D1/§D3.3, EU Annex 11 §4.4, 21 CFR Part 11).
- ❌ Deleting an obsolete FS row (strike through `~~...~~`, never delete — preserves traceability).
- ❌ `status: approved`, or any banned legacy category code / corporate identifier (see the anonymization rule in `CLAUDE.md`).
- ❌ A per-ID §4.5 matrix for a preset-heavy system (use the per-category coverage summary).
