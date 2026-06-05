---
name: gdd.init
description: |
  Bootstrap a new gxp-driven-dev consumer project. Interactive prompts produce
  the `.gxp-dev.yaml` manifest (per `docs/project-layout.md`) + the standard
  folder layout (`specs/`, `evidence/{iq,oq,pq,periodic-review}/`) + a `STATE.md`
  stub. Derives `templates_active` from profile + mode + gamp_category and
  confirms it with the user. Emits the **F4-B soft warning** for unusual
  GAMP-category × mode combinations (recommends the conventional combo but
  ALLOWS override). The entry-point skill: without `.gxp-dev.yaml`, no other
  skill runs. Anti-hallucination: never invents identity fields — uses
  `[NEEDS CLARIFICATION: …]` only where appropriate (the manifest itself should
  be marker-free; ask rather than guess).
  Use this skill when:
  - Starting a brand-new consumer project (no `.gxp-dev.yaml` yet)
  - The user says "init", "set up a new project", or "bootstrap gxp-dev"
  - Another skill redirected here because the manifest is missing
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# `gdd.init` — Project Bootstrap

You bootstrap a new **consumer project** so the rest of the toolkit can run. The deliverables are a valid `.gxp-dev.yaml` manifest at the project root, the canonical folder layout, and a `STATE.md` stub. After this, the natural next step is `/gdd.urs.from-idea` (or `/gdd.next`).

The manifest is the contract every other skill reads. Get it right — a malformed manifest blocks the whole cascade.

## Pre-flight (do this FIRST)

1. **Check for an existing `.gxp-dev.yaml`** in the cwd (and walk up). If one exists:
   > Ask: *"A `.gxp-dev.yaml` already exists at `<path>`. Re-initialize (overwrite), amend specific fields, or abort?"*
   Never silently overwrite an existing manifest.

2. **Confirm the project root.** The manifest goes at the repository root (sibling of `README.md` / `pyproject.toml` / `package.json`). Confirm the cwd is that root; if the user is in a subfolder, ask where the root is.

3. **Locate the toolkit install.** Resolve `<gdd-path>` = the `gxp-driven-dev` root (parent of `skills/`). You read `docs/project-layout.md` (manifest contract) and `templates/csv/` (to know which template acronyms are real) from there.

## Interview flow

Follow the four interaction principles (propose-a-default-then-confirm; `AskUserQuestion` for discrete choices; one decision at a time; adapt depth). Collect, in order:

| # | Field(s) | Notes |
|---|---|---|
| 1 | `project_id`, `project_name`, `language` | identity. `language: en` default |
| 2 | `mode` | `develop` (default, primary) / `validate` / `hybrid` |
| 3 | `lifecycle`, `lifecycle_phase` | `v-model` / `agile` / `hybrid`; phase `concept`/`project`/`operation`/`retirement` (default `project`) |
| 4 | `profile` | `pharma` / `medical-device` / `finance` / `aerospace` / `nuclear` / `general` |
| 5 | `rigor_level` | `light` / `standard` (default) / `strict` / `regulated` |
| 6 | `gamp_category` | **required if `profile == pharma`**: `1` / `3` / `4` / `5` |
| 7 | `presets.{part11_active, annex11_active, gdpr_active, annex22_active}` | pharma/regulated; ask each yes/no |
| 8 | `id_scheme` (+ `custom_alias`) | `canonical` (default) or `custom` with a per-DOC alias map |
| 9 | `templates_active` | **derived** (see below), then confirmed |
| 10 | `outputs.{specs, code, tests, compliance_bundle}` | toggles; `specs: true` always |
| 11 | `gxp_dev_version` | semver-range constraint, default `">=0.1.0,<1.0.0"` |

For `mode: hybrid`, additionally collect `hybrid_breakdown` (vendor + custom components, each with its own `gamp_category` + `templates_active`) per `docs/project-layout.md`.

### Deriving `templates_active`

Propose a starting set, then confirm. Base it on `mode` (see `CLAUDE.md` "Operational modes") + `gamp_category` + `profile`:

- **Always**: `URS`, `RA-INIT`, `FS`, `RA-DET`, `IQ`, `OQ`, `PQ`, `RTM`, `VR`.
- **`profile: pharma`** → add `GXP-ASSESS`, `VP` (and `VMP` if program-level).
- **`gamp_category: 4`** → add `CS` (Configuration Spec). **Not** `DS`.
- **`gamp_category: 5`** or **`mode: develop`** → add `DS`, `ADR`; add `API-SPEC`/`DBS` if APIs/DB; add `UT-PLAN`, `IT-PLAN`, `CR`, `RN`, `DEPLOY-RUN`.
- **vendor component (`mode: validate`/`hybrid`)** → add `SUP-ASSESS`.
- **`presets.gdpr_active`** → add `DPIA`. **`presets.annex22_active`** → add `AISC`.

Only list acronyms that have a real `templates/csv/<ACRONYM>.md`. Confirm the set with the user (`AskUserQuestion` to add/remove).

## F4-B soft warning — unusual category × mode combinations (MANDATORY)

After locking `gamp_category` and `mode`, evaluate the combination. The **conventional** mapping is:

| GAMP category | Conventional mode | Rationale |
|---|---|---|
| Cat 1 (infrastructure) | `validate` (qualify, not validate) | infrastructure is qualified against suitability, not custom-built |
| Cat 3 (standard product) | `validate` | used out-of-the-box; you validate the vendor's product |
| Cat 4 (configured product) | `validate` (or `hybrid`) | you configure + validate a vendor platform |
| Cat 5 (custom/bespoke) | `develop` | you are building the software yourself |

If the user's combination is **unconventional** — e.g. **Cat 4 + `mode: develop`**, or **Cat 5 + `mode: validate`**, or **Cat 1/3 + `mode: develop`** — emit a **soft warning** and let them override:

> [!warning] Unusual GAMP-category × mode combination
> You selected **Cat {{n}} + mode: {{mode}}**. The conventional combination for a Cat {{n}} system is **mode: {{conventional_mode}}** ({{one-line rationale}}). This is unusual but not forbidden — e.g. you may be developing custom extensions on a configured platform (Cat 4 + develop), or validating a bespoke system you did not build (Cat 5 + validate). **Confirm to proceed with `{{mode}}`, or switch to `{{conventional_mode}}`.**

Use `AskUserQuestion` with two options: *"Keep {{mode}} (I have a reason)"* / *"Switch to {{conventional_mode}}"*. **Never block** — record the user's confirmed choice. If they keep the unusual combo, note it as a one-line comment in the generated manifest so reviewers see it was deliberate.

For `mode: hybrid`, evaluate the warning **per component** in `hybrid_breakdown` (a Cat 5 custom component in develop is conventional; a Cat 4 vendor core in develop triggers the warning).

## Outputs (what to write)

1. **`.gxp-dev.yaml`** at the project root — see `output-template.md` (this folder) for the exact shape. All required fields filled (no raw `{{…}}`, no `[NEEDS CLARIFICATION]` in the manifest — ask rather than guess). Include the F4-B note as a comment if an unusual combo was kept.
2. **Folder layout** (create if absent):
   - `specs/`
   - `evidence/iq/`, `evidence/oq/`, `evidence/pq/`, `evidence/periodic-review/`
   - `compliance-bundle/` only if `outputs.compliance_bundle: true`
3. **`STATE.md` stub** at the project root — a short living-memory file: project identity, current lifecycle position (`bootstrapped`, no specs yet), `templates_active` checklist, and "Next: `/gdd.urs.from-idea`". Do **not** create stub `specs/<TEMPLATE>.md` files with bodies — the cascade skills own the bodies. (Empty `specs/` is correct after init; the cascade fills it.)

## Anti-hallucination rules (NON-NEGOTIABLE)

1. **Never invent identity fields.** `project_id`, `project_name`, names — ask. Do not fabricate a project ID scheme.
2. **Never invent a `gamp_category`.** If `profile == pharma` and the user is unsure, propose from the system's nature (configured vs bespoke) and confirm; do not silently pick one.
3. **Only list real templates** in `templates_active` (verify each `templates/csv/<ACRONYM>.md` exists).
4. **The manifest must be marker-free and valid YAML.** If a value is genuinely unknown, ask — `.gxp-dev.yaml` is a contract, not a draft spec.
5. **Honor the geographic-anonymity boundary:** the consumer's own manifest *may* carry their internal codes (it is their repo, not the toolkit), but **you** must never write any source-organization name or legacy code into it from toolkit memory. Use generic placeholders only when the user has not supplied a value.

## Post-flight (after writing)

1. **Validate the manifest parses** (it is YAML):
   ```bash
   python -c "import yaml,sys; yaml.safe_load(open('.gxp-dev.yaml',encoding='utf-8')); print('OK manifest parses')"
   ```
2. **Print summary**: identity, mode, lifecycle, profile, rigor, category, active presets, the `templates_active` set, and (if applicable) the F4-B note that the unusual combo was kept by user choice.
3. **Suggest next step**: `/gdd.urs.from-idea` to start the URS interview (or `/gdd.next` to let the orchestrator route).

## When to refuse

- An existing `.gxp-dev.yaml` is present and the user has not chosen overwrite/amend → ask first; do not clobber.
- User asks to set `profile: pharma` but refuses to pick a `gamp_category` → ask once more, then record `[NEEDS CLARIFICATION:]` only in `STATE.md` (never in the manifest) and recommend resolving before the URS.
- User asks to list a template that does not exist in `templates/csv/` → refuse; offer the closest real acronym.
