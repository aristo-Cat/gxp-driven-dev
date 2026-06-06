---
description: Bootstrap a new gxp-driven-dev consumer project — produces the .gxp-dev.yaml manifest + the standard folder layout (specs/, evidence/) + a STATE.md stub. The entry point: without .gxp-dev.yaml, no other gdd skill runs. Anti-hallucination: never invents identity fields; asks rather than guesses.
argument-hint: "[optional project name, e.g. /gdd-init Lab Data Capture App]"
---

# gdd.init — Project Bootstrap (Codex prompt)

> **Codex invocation.** Place this file under your Codex prompts/skills directory so it is exposed as the slash command **`/gdd-init`** (Codex derives the command name from the filename). `$ARGUMENTS` (if provided) seeds `project_name` — still confirm it before writing.
>
> **Two-part port.** This prompt carries the *procedure*. The *always-on guardrails* live in `../AGENTS.snippet.md`, which the consumer pastes into their project `AGENTS.md` so they hold even when this prompt is not the active turn. See `../PORTING.md`.
>
> **Shared core.** The deterministic work is done by the harness-agnostic Python in `skills/_scripts/`, invoked by path. Source of truth: `skills/init-project/SKILL.md` + `skills/init-project/output-template.md`.
>
> **No `AskUserQuestion` in Codex.** Pose every discrete choice (mode, profile, gamp_category, presets, …) as an **explicit enumerated prompt** ("reply 1/2/3"), propose a reasoned default, and confirm before it lands.

You bootstrap a new **consumer project** so the rest of the toolkit can run. Deliverables: a valid `.gxp-dev.yaml` at the project root, the canonical folder layout, and a `STATE.md` stub. After this, the natural next step is `/gdd-urs-from-idea` (or `/gdd-next`).

The manifest is the contract every other skill reads. A malformed manifest blocks the whole cascade — get it right.

## Pre-flight (do this FIRST)

1. **Check for an existing `.gxp-dev.yaml`** in the cwd (and walk up). If one exists, ask: *"A `.gxp-dev.yaml` already exists at `<path>`. Re-initialize (overwrite), amend specific fields, or abort?"* — **never silently overwrite** (always-on invariant #10).
2. **Confirm the project root.** The manifest goes at the repository root (sibling of `README.md` / `pyproject.toml` / `package.json`). If the user is in a subfolder, ask where the root is.
3. **Locate the toolkit install** `<gdd-path>` = the `gxp-driven-dev` root (parent of `skills/`). You read `docs/project-layout.md` (manifest contract) and `templates/csv/` (to know which template acronyms are real) from there.

## Interview flow

Propose-a-default-then-confirm; one decision (or tight cluster) at a time; adapt depth. Collect, in order:

| # | Field(s) | Notes |
|---|---|---|
| 1 | `project_id`, `project_name`, `language` | identity. `language: en` default. Seed `project_name` from `$ARGUMENTS` if given |
| 2 | `mode` | `develop` (default, primary) / `validate` / `hybrid` |
| 3 | `lifecycle`, `lifecycle_phase` | `v-model` / `agile` / `hybrid`; phase `concept`/`project`/`operation`/`retirement` (default `project`) |
| 4 | `profile` | `pharma` / `medical-device` / `finance` / `aerospace` / `nuclear` / `general` |
| 5 | `rigor_level` | `light` / `standard` (default) / `strict` / `regulated` |
| 6 | `gamp_category` | **required if `profile == pharma`**: `1` / `3` / `4` / `5` |
| 7 | `presets.{part11_active, annex11_active, gdpr_active, annex22_active}` | pharma/regulated; ask each yes/no |
| 8 | `id_scheme` (+ `custom_alias`) | `canonical` (default) or `custom` with a per-DOC alias map |
| 9 | `templates_active` | **derived** (below), then confirmed |
| 10 | `outputs.{specs, code, tests, compliance_bundle}` | toggles; `specs: true` always |
| 11 | `gxp_dev_version` | semver-range, default `">=0.1.0,<1.0.0"` |

For `mode: hybrid`, additionally collect `hybrid_breakdown` (vendor + custom components, each with its own `gamp_category` + `templates_active`) per `docs/project-layout.md`.

### Deriving `templates_active`

Propose a starting set from `mode` + `gamp_category` + `profile`, then confirm:

- **Always**: `URS`, `RA-INIT`, `FS`, `RA-DET`, `IQ`, `OQ`, `PQ`, `RTM`, `VR`.
- **`profile: pharma`** → add `GXP-ASSESS`, `VP` (and `VMP` if program-level).
- **`gamp_category: 4`** → add `CS`. **Not** `DS`.
- **`gamp_category: 5`** or **`mode: develop`** → add `DS`, `ADR`; add `API-SPEC`/`DBS` if APIs/DB; add `UT-PLAN`, `IT-PLAN`, `CR`, `RN`, `DEPLOY-RUN`.
- **vendor component (`mode: validate`/`hybrid`)** → add `SUP-ASSESS`.
- **`presets.gdpr_active`** → add `DPIA`. **`presets.annex22_active`** → add `AISC`.

Only list acronyms that have a real `templates/csv/<ACRONYM>.md`. Confirm the set with the user (offer to add/remove).

## F4-B soft warning — unusual category × mode combinations (MANDATORY)

After locking `gamp_category` and `mode`, evaluate the combination. Conventional mapping: Cat 1 → `validate` (qualify), Cat 3 → `validate`, Cat 4 → `validate`/`hybrid`, Cat 5 → `develop`.

If the combination is **unusual** — e.g. **Cat 4 + `mode: develop`**, **Cat 5 + `validate`**, **Cat 1/3 + `develop`** — emit a **soft warning** with the conventional combo + a one-line rationale, then ask the user to **keep (they have a reason)** or **switch**. **Never block.** If they keep the unusual combo, note it as a one-line comment in the generated manifest so reviewers see it was deliberate. For `mode: hybrid`, evaluate per component in `hybrid_breakdown`.

## Outputs (what to write)

1. **`.gxp-dev.yaml`** at the project root — see `skills/init-project/output-template.md` for the exact shape. All required fields filled (no raw `{{…}}`, no `[NEEDS CLARIFICATION]` in the manifest — ask rather than guess). Include the F4-B note as a comment if an unusual combo was kept.
2. **Folder layout** (create if absent): `specs/`; `evidence/iq/`, `evidence/oq/`, `evidence/pq/`, `evidence/periodic-review/`; `compliance-bundle/` only if `outputs.compliance_bundle: true`.
3. **`STATE.md` stub** at the project root — short living memory: project identity, current position (`bootstrapped`, no specs yet), `templates_active` checklist, and "Next: `/gdd-urs-from-idea`". Do **not** create stub `specs/<TEMPLATE>.md` bodies — the cascade skills own them. (Empty `specs/` is correct after init.)

## Anti-hallucination rules (NON-NEGOTIABLE — also enforced via AGENTS.md)

1. **Never invent identity fields.** `project_id`, `project_name`, names — ask. Do not fabricate a project ID scheme.
2. **Never invent a `gamp_category`.** If `profile == pharma` and the user is unsure, propose from the system's nature (configured vs bespoke) and confirm; never silently pick.
3. **Only list real templates** in `templates_active` (verify each `templates/csv/<ACRONYM>.md` exists).
4. **The manifest must be marker-free and valid YAML.** If a value is genuinely unknown, ask — `.gxp-dev.yaml` is a contract, not a draft spec.
5. **Honor the geographic-anonymity boundary:** the consumer's own manifest *may* carry their internal codes (their repo), but **you** never write any source-organization name or legacy code into it from toolkit memory. Generic placeholders only when the user has not supplied a value.

## Post-flight (after writing)

1. **Validate the manifest parses** (it is YAML):
   ```bash
   python -c "import yaml,sys; yaml.safe_load(open('.gxp-dev.yaml',encoding='utf-8')); print('OK manifest parses')"
   ```
2. **Print summary**: identity, mode, lifecycle, profile, rigor, category, active presets, the `templates_active` set, and (if applicable) the F4-B note.
3. **Suggest next step**: `/gdd-urs-from-idea` to start the URS interview (or `/gdd-next` to let the orchestrator route).

## When to refuse

- An existing `.gxp-dev.yaml` is present and the user has not chosen overwrite/amend → ask first; do not clobber.
- `profile: pharma` but the user refuses to pick a `gamp_category` → ask once more, then record `[NEEDS CLARIFICATION:]` only in `STATE.md` (never in the manifest) and recommend resolving before the URS.
- User asks to list a template that does not exist in `templates/csv/` → refuse; offer the closest real acronym.
