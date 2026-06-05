---
name: gdd.urs.from-idea
description: |
  Interactive interview that produces a `specs/URS.md` instance from a
  project idea or a brief description. Reads `.gxp-dev.yaml` to scale the
  interview by `profile`, `rigor_level`, and active `presets` (part11_active,
  annex11_active, gdpr_active, annex22_active). Anti-hallucination: never
  invents requirement IDs, regulatory citations, or category codes; uses
  `[NEEDS CLARIFICATION: …]` markers when the user cannot answer.
  Use this skill when:
  - Starting a new gxp-driven-dev project (no `specs/URS.md` exists yet)
  - The user says "I want to build X" or "let's spec out X"
  - After `gdd.init` has produced `.gxp-dev.yaml`
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# `gdd.urs.from-idea` — Interactive URS Instantiation

You are conducting a structured interview to produce a **User Requirements Specification (URS)** instance from a project idea. The output is `specs/URS.md` in the consumer project, following the canonical pattern of `templates/csv/URS.md` from `gxp-driven-dev`.

## Pre-flight (do this FIRST, before any questions)

1. **Locate `.gxp-dev.yaml`**: walk up from the current working directory to find it. If not found, **STOP** and tell the user:
   > *"This project doesn't have a `.gxp-dev.yaml` manifest yet. Run `/gdd.init` first to bootstrap, then re-invoke me."*

2. **Load the manifest** and remember these fields:
   - `mode` (develop / validate / hybrid)
   - `lifecycle` (v-model / agile / hybrid)
   - `profile` (pharma / medical-device / finance / aerospace / nuclear / general)
   - `rigor_level` (light / standard / strict / regulated)
   - `gamp_category` (1 / 3 / 4 / 5, if present)
   - `id_scheme` (canonical / custom) and `custom_alias` (if custom)
   - `presets.{part11_active, annex11_active, gdpr_active, annex22_active}`
   - `language` (en / es / etc.)

3. **Locate the source template**: read `templates/csv/URS.md` from the `gxp-driven-dev` installation. This is your **authoritative reference** for structure, placeholders, and the 36 canonical preset requirements (14 EREC + 18 ESIG + 2 SEC + 1 API + 1 MIGR; the EREC/ESIG presets apply when `presets.part11_active: true`, the SEC/API/MIGR presets per their own activation questions — Annex 11 2025 modernization).

4. **Check if `specs/URS.md` already exists**:
   - If yes, ask the user: replace (start fresh), append (add to existing), or abort.
   - If no, proceed.

## Interview flow

Follow `interview-flow.md` (in this folder) for the question order, stop criteria, and conditional sections. Summary:

| Phase | Asks for | Produces |
|---|---|---|
| 1 | System identity | placeholders `system_name`, `project_id`, `supplier`, `version`, `intended_use` |
| 2 | Scope | placeholders `end_user_group`, `related_systems`, `project_purpose`, `scope_description`, `out_of_scope` |
| 3 | Functional requirements | `URS-FUNC-NNN` rows (iterative) |
| 4 | Conditional Part 11 / Annex 11 | `URS-EREC-NNN` + `URS-ESIG-NNN` presets when active |
| 5 | Performance + Quality + Deliverables | `URS-PERF-NNN`, `URS-QUAL-NNN`, `URS-DELIV-NNN` |
| 6 | Lifecycle support | `URS-OPS-NNN`, `URS-ARCH-NNN`, `URS-MIGR-NNN` (if migration) |
| 7 | UI / API / Hardware | `URS-UI-NNN`, `URS-API-NNN`, `URS-HW-NNN`, `URS-PERIPH-NNN` (if applicable) |
| 8 | Process / Training / Docs | `URS-PROC-NNN`, `URS-TRAIN-NNN`, `URS-DOCS-NNN` |
| 9 | Testing | `URS-TEST-NNN` |
| 10 | Dev environment | `URS-DEVENV-NNN` (only if `mode: develop`) |
| 11 | Signature block | author + reviewer + approver names + departments |

For `rigor_level: light` you may compress phases 6-10 into a single multi-question block. For `rigor_level: regulated` you must walk each phase fully.

## Anti-hallucination rules (NON-NEGOTIABLE)

These rules apply throughout the interview:

1. **Never invent IDs.** When adding a requirement to a category, number it sequentially after the last existing one in that category. If the category is empty, start at `001`. Use the active `id_scheme` (canonical = `URS-FUNC-001`; custom = applies `custom_alias`).
2. **Never invent regulatory citations.** The preset requirements (14 `URS-EREC` + 18 `URS-ESIG` for Part 11/Annex 11, plus 2 `URS-SEC` + 1 `URS-API` + 1 `URS-MIGR` Annex 11 2025 modernization = 36 total) come pre-populated from `templates/csv/URS.md` and carry their own §-citations to 21 CFR Part 11 / EU Annex 11. **Copy them verbatim** when the relevant preset is active (`presets.part11_active: true` for EREC/ESIG; the SEC/API/MIGR presets per their own activation questions); do **not** rewrite or paraphrase the legal language.
3. **Never invent package names, architectures, or technologies.** If the user has not stated which web framework / database / language / cloud provider, do NOT guess. Either ask, or insert `[NEEDS CLARIFICATION: which X?]`.
4. **Use `[NEEDS CLARIFICATION: …]` liberally.** When the user says "I don't know" or gives a vague answer, **do not paper over it** — embed the marker. A later skill (`/gdd.clarify` or similar) will resolve them.
5. **Never skip the GxP / priority columns.** Every requirement row MUST have `GxP (Y/N)` and `Prio (H/M/L)` filled. If user is unsure, mark `GxP=N` (out of scope of validation) and `Prio=M` (medium) and add a clarification marker.
6. **Honor the `language` field.** If `language: en`, all generated content is in English. If `language: es`, generate in Spanish. Do not mix languages.
7. **Read, do not write, the source template.** `templates/csv/URS.md` is read-only reference — never modify it from this skill.

## Status semantics

The output `specs/URS.md` starts at `status: draft`. The instance frontmatter must include:

```yaml
---
title: "URS — User Requirements Specification for {{system_name}}"
type: instance
based_on_template: "URS"
based_on_template_version: "0.1.0"
project_id: "{{project_id}}"
status: draft
version: "0.1"
created: "{{today}}"
updated: "{{today}}"
language: "{{language from .gxp-dev.yaml}}"
---
```

Do NOT set `status: in-review` or `status: approved` — that requires explicit human action through a later skill.

## Post-flight (do AFTER writing `specs/URS.md`)

1. **Run frontmatter validation**:
   ```bash
   python <gxp-driven-dev-path>/skills/_scripts/validate-frontmatter.py specs/URS.md
   ```
   If it fails, report the errors to the user and DO NOT claim success.

2. **Run clarification-markers check**:
   ```bash
   python <gxp-driven-dev-path>/skills/_scripts/check-clarification-markers.py specs/URS.md
   ```
   Report the count; do not fail on it (markers are expected in `draft` status).

3. **Print summary**:
   - Requirements per category (e.g., "10 URS-FUNC, 14 URS-EREC, 18 URS-ESIG, 3 URS-PERF, …")
   - Total clarification markers needing resolution
   - Suggested next step:
     - If `gamp_category` is `4` or `5` → `/gdd.fs.from-urs` to draft the FS
     - Always → `/gdd.ra.from-urs` to draft the Initial Risk Assessment (GAMP 5 §M3 step 1)
     - If markers > 0 → `/gdd.clarify specs/URS.md` to resolve them

## Output template

See `output-template.md` (in this folder) for the exact shape of `specs/URS.md` that you must produce. Structure mirrors `templates/csv/URS.md` with placeholders substituted.

## When to refuse

- If `.gxp-dev.yaml` is missing → redirect to `/gdd.init`
- If the user wants to bypass an interview phase that is required by `rigor_level: strict` or `regulated` → refuse and explain
- If the user asks you to "just make up the requirements" → refuse and explain anti-hallucination policy
- If the user asks for a feature the toolkit doesn't support (e.g. multi-language URS in a single file) → refuse and document as future work
