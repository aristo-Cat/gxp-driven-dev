# `gdd.urs.from-idea` — Output Template Reference

This file documents the **exact shape** of the `specs/URS.md` produced by the skill. It mirrors `templates/csv/URS.md` from the toolkit, with placeholders substituted by interview answers.

---

## Frontmatter (instance shape)

```yaml
---
title: "URS — User Requirements Specification for {{system_name}}"
type: instance
based_on_template: "URS"
based_on_template_version: "0.1.0"
project_id: "{{project_id}}"
status: draft
version: "0.1"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
language: "{{language from .gxp-dev.yaml}}"

# Copied from .gxp-dev.yaml for self-contained reference
gamp_category: {{1|3|4|5 or null}}
profile: "{{profile}}"
mode: "{{mode}}"
presets:
  part11_active: {{bool}}
  annex11_active: {{bool}}
  gdpr_active: {{bool}}
  annex22_active: {{bool}}
---
```

---

## Body sections

### 0. Identification

| Field | Value |
|---|---|
| System Name | <from interview> |
| Project ID | <from manifest> |
| Supplier | <from interview> |
| Version | <from interview> |
| Intended Use | <from interview> |
| GAMP Category | <from manifest or interview> |

**Signature block**: table with Author, Reviewer 1 (Process Owner), Reviewer 2 (SME), Approver 1 (System Owner), Approver 2 (Quality Unit).

### 1. Project context

- 1.1 Objective and purpose
- 1.2 System description
- 1.3 End users
- 1.4 Related systems

### 2. Definitions and abbreviations

Inherited from template + project-specific.

### 3. Category code catalog

Reference to `docs/requirement-id-scheme.md` of the toolkit — do not duplicate. Single line: *"This URS uses the 22 canonical category codes (FUNC, PERF, QUAL, …, EREC, ESIG). See `gxp-driven-dev/docs/requirement-id-scheme.md` for definitions."*

### 4. Requirements by category

For each category that has at least one requirement, emit a section:

```markdown
### 4.<n>. URS-<CATEGORY> — <Category description>

| ID | GxP (Y/N) | Prio (H/M/L) | Requirement |
|---|---|---|---|
| URS-<CATEGORY>-001 | Y | H | <requirement text> |
| URS-<CATEGORY>-002 | Y | M | <requirement text> |
| ... | | | |
```

**Section ordering** (when present):

1. `URS-FUNC` (always)
2. `URS-EREC` (if `presets.part11_active`)
3. `URS-ESIG` (if `presets.part11_active`)
4. `URS-DATA`
5. `URS-FLOW`
6. `URS-REPORT`
7. `URS-SEC`
8. `URS-PERF`
9. `URS-UI` (if applicable)
10. `URS-API` (if applicable)
11. `URS-MIGR` (if applicable)
12. `URS-ARCH`
13. `URS-OPS`
14. `URS-PROC`
15. `URS-DOCS`
16. `URS-TRAIN`
17. `URS-QUAL`
18. `URS-TEST`
19. `URS-DELIV`
20. `URS-PERIPH` (if applicable)
21. `URS-HW` (if applicable)
22. `URS-DEVENV` (only if `mode: develop`)

Categories with no requirements are **omitted** from the output (don't write empty sections).

### 5. Related documents

Hardcoded list:
- `.gxp-dev.yaml` (project manifest)
- `specs/VMP.md` (if active)
- `specs/GXP-ASSESS.md` (if active)
- `specs/VP.md` (if active)
- Downstream: `specs/FS.md`, `specs/RA-INIT.md`, `specs/IQ.md`, `specs/PQ.md`

### 6. Revision history

| Version | Date | Reason | Author |
|---|---|---|---|
| 0.1 | <today> | Initial draft from `gdd.urs.from-idea` | <author name>, <author dept> |

---

## Anti-patterns in the output

Do NOT produce:

- ❌ Empty requirement tables (`| URS-FUNC-001 | | | |`). Either fill all 4 columns or omit the row.
- ❌ Numbered prefixes (`03-urs`, `04-fs`). Always use acronyms (`URS`, `FS`).
- ❌ The legacy `US-` requirement-ID prefix (use `URS-` instead).
- ❌ Any banned legacy category code — use only the 22 canonical acronyms (FUNC/EREC/ESIG/QUAL/TRAIN/DEVENV/DATA/FLOW/REPORT/PROC/UI/API/MIGR/ARCH/OPS/DOCS/TEST/DELIV/PERIPH). See the anonymization rule in `CLAUDE.md` for the full banned list.
- ❌ Any non-English heritage term for "category code".
- ❌ References to any specific corporate organization, document code, or site code.
- ❌ Invented regulatory citations. Only use the §-refs that the source template `templates/csv/URS.md` already contains (mostly 21 CFR Part 11 §10, §50, §70, §100, §200, §300).
- ❌ `[NEEDS CLARIFICATION:` markers WITHOUT a question after the colon. Always include the actual question.
