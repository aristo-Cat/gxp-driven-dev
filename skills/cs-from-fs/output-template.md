# `gdd.cs.from-fs` — Output Template Reference

The exact shape of the `specs/CS.md` produced by the skill. Mirrors `templates/csv/CS.md` with placeholders substituted. A worked, validated example is `examples/temp-logger-gmp-chamber/specs/CS.md` (20 config items by area, custom-code = none).

---

## Frontmatter (instance shape)

```yaml
---
title: "CS — Configuration Specification for {{system_name}}"
type: instance
based_on_template: "CS"
based_on_template_version: "0.1.0"
project_id: "{{project_id}}"
system_id: "{{system_id}}"
traces_to: "specs/FS.md ({{ver}}, {{status}})"
status: draft
version: "0.1"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
language: "{{language from .gxp-dev.yaml}}"
lives_in_tool: {{bool}}              # true if the config lives in a tool with audit trail

# Copied from .gxp-dev.yaml for self-contained reference
gamp_category: 4
profile: "{{profile}}"
mode: "{{mode}}"
---
```

---

## Body sections (mirror the template)

### 0. Identification and signatures
Identity table (name, identifier, **FS being configured** + status, product version, config-management tool) + signatures: Author, Reviewer = SME, Approver = System Owner, Approver = Quality Unit. Unknown → `[NEEDS CLARIFICATION: assign <role>]`. If `lives_in_tool`, add a `> [!note]` explaining the tool is the source of truth and this CS is the summary record. Keep a `> [!warning]` cascade-order note if the FS is still draft.

### 1. Objective
One paragraph: document the configuration of `<product> <version>` that implements the FS; note whether custom code is involved (for a pure Cat 4: none).

### 2. Definitions
CS / config baseline / config drift / config item.

### 3. Configuration by area
One table per area that has config items (omit empty areas):
- **§3.1** `CS-FUNC-NNN` / `CS-PROC-NNN` — `CS-ID | Configures (FS-ID) | Setting / Parameter | Configured value | Justification`
- **§3.2** `CS-SEC-NNN` / `CS-ESIG-NNN` — `CS-ID | Configures (FS-ID) | Security setting | Configured value | Justification`
- **§3.3** `CS-API-NNN` — `CS-ID | Configures (FS-ID) | Integration mapping | Configured value | Justification`
- **§3.4** `CS-EREC-NNN` — `CS-ID | Configures (FS-ID) | Audit trail / records setting | Configured value | Justification`
- **§3.5** other (DATA/FLOW/REPORT/OPS/PERIPH) — `CS-ID | Configures (FS-ID) | Parameter | Value | Justification`

Each `CS-<CAT>-NNN` cites a real `FS-<CAT>-NNN`; the "Configured value" is concrete (or `[NEEDS CLARIFICATION:]`); the "Justification" cites the `RA-DET-NNN` when the item realizes a risk mitigation.

### 4. Configuration dependencies
`Config item | Depends on | Comment` — external dependencies (IdP, messaging gateway, key store).

### 5. Custom code within the platform (Cat 5 flag)
`Custom element | Reference in DS`. For a pure Cat 4: one row "None — pure configured COTS; no custom code." | n/a.

### 6. Related documents
FS, IQ, OQ, DS (if custom code).

### 7. Revision history
| 0.1 | <today> | Initial draft (CS) — <author>, <dept> |

---

## Anti-patterns in the output

Do NOT produce:
- ❌ A CS that mirrors every FS-ID (the CS is selective — only items with a real configurable setting).
- ❌ A fabricated configured value where the value is undecided (use `[NEEDS CLARIFICATION:]`).
- ❌ A `CS-<CAT>-NNN` whose "Configures" cites an FS-ID not present in `specs/FS.md`.
- ❌ Custom code/macros documented as configuration (those are Cat 5 → DS; §5 cross-reference only).
- ❌ A CS for a Cat 3 (not applicable) or a Cat 5 (use DS).
- ❌ A new category code outside the 22 canonical acronyms.
- ❌ `status: approved`, or any banned legacy category code / corporate identifier (see the anonymization rule in `CLAUDE.md`).
- ❌ A static CS that drifts from the live configuration (note `lives_in_tool` when the tool is the source of truth).
