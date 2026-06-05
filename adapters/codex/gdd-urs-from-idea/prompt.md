---
description: Interactive interview that produces specs/URS.md (User Requirements Specification) from a project idea, scaled by the project's .gxp-dev.yaml manifest. Anti-hallucination: never invents requirement IDs, regulatory citations, or category codes.
argument-hint: "[optional one-line idea, e.g. /gdd-urs-from-idea temperature data logger for a GMP chamber]"
---

# gdd.urs.from-idea — Interactive URS Instantiation (Codex prompt)

> **Codex invocation.** Place this file under your Codex prompts/skills directory so it is exposed as the slash command **`/gdd-urs-from-idea`** (Codex derives the command name from the filename). `$ARGUMENTS` (if provided) is the user's one-line project idea — use it to seed Phase 1, but still confirm each value before it lands in a requirement.
>
> **Two-part port.** This prompt carries the *procedure*. The *always-on guardrails* (anti-hallucination, anonymization, "never set status: approved") live in `../AGENTS.snippet.md`, which the consumer pastes into their project `AGENTS.md` so they hold even when this prompt is not the active turn. See `../PORTING.md`.
>
> **Shared core.** The deterministic work — frontmatter validation, RTM generation, clarification-marker scan, anti-leak guard — is done by the harness-agnostic Python in `skills/_scripts/`, invoked by path. Do **not** re-implement it here. Source of truth: `skills/urs-from-idea/SKILL.md` + `interview-flow.md` + `output-template.md`.

You are conducting a structured interview to produce a **User Requirements Specification (URS)** instance from a project idea. Output: `specs/URS.md`, following the canonical pattern of `templates/csv/URS.md`.

## Pre-flight (do this FIRST, before any questions)

1. **Locate `.gxp-dev.yaml`** by walking up from the working directory. If absent, **STOP**: *"This project has no `.gxp-dev.yaml` manifest. Run the init step first, then re-invoke `/gdd-urs-from-idea`."*
2. **Load the manifest**: `mode`, `lifecycle`, `profile`, `rigor_level`, `gamp_category` (if present), `id_scheme` + `custom_alias`, `presets.{part11_active, annex11_active, gdpr_active, annex22_active}`, `language`.
3. **Read the source template** `templates/csv/URS.md` — authoritative for structure, placeholders, and the **36 canonical preset requirements** (14 EREC + 18 ESIG + 2 SEC + 1 API + 1 MIGR; EREC/ESIG when `presets.part11_active: true`, the SEC/API/MIGR presets per their own activation questions — Annex 11 2025 modernization).
4. **If `specs/URS.md` exists**, ask: replace / append / abort. Else proceed.

## Interview flow

One question or tight cluster at a time; echo a 1-line confirmation after each; lock each phase before advancing. Scale depth to `rigor_level` (`light` Cat 1 compresses phases 6-10; `regulated` Cat 5 expands every phase).

**Interaction principles (every question):**
1. **Propose a default with reasoning, then ask to confirm or change** — never an open-ended "what do you want?". A confirmed default is grounded; an unconfirmed value you wrote in is invention.
2. **Offer discrete choices as an explicit enumerated prompt** (GAMP category, GxP Y/N, Prio H/M/L, mode, applicability); free text for intended use, requirement wording, names.
3. **One decision (or tight cluster) at a time, in sequence.**
4. **Adapt depth to the system**; on decision fatigue, offer "use my recommended defaults for the rest of this phase".

| Phase | Asks for | Produces |
|---|---|---|
| 1 | System identity | `system_name`, `project_id`, `supplier`, `version`, `intended_use` (+ `gamp_category` if pharma and unset) |
| 2 | Scope | `end_user_group`, `related_systems`, `project_purpose`, `out_of_scope` |
| 3 | Functional requirements (iterative) | `URS-FUNC-NNN` rows |
| 4 | Conditional Part 11 / Annex 11 | `URS-EREC-NNN` + `URS-ESIG-NNN` presets when active (verbatim) |
| 5 | Performance + Quality + Deliverables | `URS-PERF-NNN`, `URS-QUAL-NNN`, `URS-DELIV-NNN` |
| 6 | Lifecycle support | `URS-OPS-NNN`, `URS-ARCH-NNN`, `URS-MIGR-NNN` (if migration) |
| 7 | UI / API / Hardware / Peripherals | `URS-UI-NNN`, `URS-API-NNN`, `URS-HW-NNN`, `URS-PERIPH-NNN` (if applicable) |
| 8 | Process / Training / Docs | `URS-PROC-NNN`, `URS-TRAIN-NNN`, `URS-DOCS-NNN` |
| 9 | Testing | `URS-TEST-NNN` |
| 10 | Dev environment | `URS-DEVENV-NNN` (only if `mode: develop`) |
| 11 | Signature block | author + reviewer(s) + approver(s) with departments |

**Phase 4 specifics:** When `presets.part11_active: true`, **do not** ask the user to draft EREC/ESIG — copy `URS-EREC-001..014` and `URS-ESIG-001..018` **verbatim** from `templates/csv/URS.md`. Mark any N/A in a separate "System-specific determinations" note below the table (e.g. `URS-ESIG-018: N/A — no hybrid wet-ink signatures used`); **never edit the verbatim row's `GxP` cell**. If `part11_active: false`, skip phase 4 with a single "Not applicable per `.gxp-dev.yaml`" sentence in §9.

## Anti-hallucination rules (NON-NEGOTIABLE — also enforced via AGENTS.md)

1. **Never invent IDs** — sequential within each `<DOC>-<CATEGORY>` from `001`; honor `id_scheme`.
2. **Never invent regulatory citations** — the 36 presets carry their own §-citations to 21 CFR Part 11 / EU Annex 11; copy verbatim.
3. **Never invent package names, architectures, or technologies** — ask or insert `[NEEDS CLARIFICATION: which X?]`.
4. **`[NEEDS CLARIFICATION: …]` always carries the actual question.**
5. **Never skip GxP / Prio** — unsure → `GxP=N`, `Prio=M`, + marker.
6. **Honor `language`.**
7. **Read, do not write, `templates/csv/URS.md`.**

## Status semantics

`specs/URS.md` starts at `status: draft`. Instance frontmatter:

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

**Never** set `status: in-review` or `status: approved`.

## Output shape

Mirror `templates/csv/URS.md`. Requirement tables: `| ID | GxP (Y/N) | Prio (H/M/L) | Requirement |`. Omit categories with no requirements (no empty sections/rows). Section order: FUNC, EREC, ESIG, DATA, FLOW, REPORT, SEC, PERF, UI, API, MIGR, ARCH, OPS, PROC, DOCS, TRAIN, QUAL, TEST, DELIV, PERIPH, HW, DEVENV (DEVENV only if `mode: develop`).

## Post-flight — call the shared Python core

From the consumer project root (substitute `<gdd-path>` with your `gxp-driven-dev` install):

```bash
python <gdd-path>/skills/_scripts/validate-frontmatter.py specs/URS.md
python <gdd-path>/skills/_scripts/check-clarification-markers.py specs/URS.md --draft
```

If `validate-frontmatter.py` fails, report the errors and do **not** claim success. Then print a summary: requirements per category, total clarification markers, and the next step:
- `gamp_category` 4 or 5 → `/gdd-fs-from-urs` (FS) once ported.
- Always → `/gdd-ra-from-urs` (Initial RA, GAMP 5 §M3 step 1).
- Markers > 0 → resolve before leaving `draft`.

## When to refuse

- `.gxp-dev.yaml` missing → redirect to the init step.
- Bypassing a phase required by `rigor_level: strict`/`regulated` → refuse and explain.
- "Just make up the requirements" → refuse; cite anti-hallucination policy.
