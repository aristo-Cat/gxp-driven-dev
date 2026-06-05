---
name: gdd.cs.from-fs
description: |
  Configuration Specification (CS) from an approved FS — GAMP 5 Cat 4 ONLY
  (§D3.3.1.1). Documents the concrete settings/parameters configured for a
  configurable product: workflows, business rules, security/roles, integration
  mappings, audit-trail config. Selective — only the FS items that require
  configuration, each with a configured value + justification. Custom code/macros
  are flagged Cat 5 and go to the DS, not here. Anti-hallucination: never invents
  configuration values; uses `[NEEDS CLARIFICATION: …]` when a value is unknown.
  Output: `specs/CS.md`.
  Use this skill when:
  - `.gxp-dev.yaml` `gamp_category == 4` and an approved `specs/FS.md` exists
  - The user says "document the configuration" or "what settings"
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# `gdd.cs.from-fs` — Configuration Specification (Cat 4)

You produce a **CS instance** (`specs/CS.md`) — the record of the settings/parameters configured for a **Cat 4** product (GAMP 5 §D3.3.1.1) — that implements the configuration the FS defines. The CS is verified in IQ (config baseline) + OQ (config works).

## Pre-flight (do this FIRST)

1. **Locate `.gxp-dev.yaml`**: walk up from cwd. If missing → `/gdd.init`.
2. **Confirm `gamp_category == 4`.** This skill is **Cat 4 only**:
   - **Cat 5** (custom) → **refuse**; the design goes in the [DS](../../templates/csv/DS.md) (`/gdd.ds.from-fs` when available).
   - **Cat 3** (standard, no meaningful configuration) → **refuse**; a CS is not applicable.
3. **Locate the FS** (`specs/FS.md`) — **required**. If missing → `/gdd.fs.from-urs`. Warn if its status is not `approved` (the CS configures an approved FS).
4. **Read RA-INIT/RA-DET if present** — they scale the detail of critical configuration (config items that mitigate high-RPN risks deserve explicit values + justification).
5. **Read the source template** `templates/csv/CS.md` — authoritative for the by-area structure (§3.1-3.5) and the Cat 5 custom-code rule.
6. **Check if `specs/CS.md` already exists**: ask replace / append / abort.

## Generation flow

Follow `generation-flow.md` (this folder). Summary:

| Step | Produces |
|---|---|
| Parse FS | the `FS-<CAT>-NNN` items that **require configuration** (selective — not every FS-ID) |
| Document | one `CS-<CAT>-NNN` per configurable item: Setting/Parameter + **Configured value** + Justification, citing the FS-ID |
| Organize | by area: §3.1 workflows/business rules, §3.2 security/roles/signatures, §3.3 integrations, §3.4 audit trail/records, §3.5 other (DATA/FLOW/REPORT/OPS/PERIPH) |
| Dependencies §4 | config items that depend on external systems (IdP, gateways, key store) |
| Custom code §5 | flag any macro/script as **Cat 5 → DS** (cross-reference only) |

## Selectivity (CORE — different from the FS)

The CS is **selective**: it documents only the FS items that have a **concrete configurable setting**. Do NOT mirror every FS-ID (that is the FS's job). A configured value with no real parameter to set adds noise. Conversely, every config item that a high-RPN RA-DET mitigation relies on **must** be documented with its value.

## Cat 4 boundary + custom code

- **Custom code = Cat 5 → DS.** Any macro, script, or custom code inside the Cat 4 platform is documented in the [DS](../../templates/csv/DS.md) (Cat 5), not the CS. §5 lists it only as a cross-reference. If the system has substantial custom code, it may not be a pure Cat 4 — flag it.
- **Config may live in a tool.** GAMP 5 §D3/§M9 allows the configuration to live in a config-management tool with an audit trail. If so, set `lives_in_tool: true`; this CS is the **summary record** and the tool is the source of truth.
- **Anti-drift.** The CS must stay in sync with the live configuration; a static CS while the config evolves is a configuration-management gap.

## Anti-hallucination rules (NON-NEGOTIABLE)

1. **Never invent a configured value.** If the concrete value (threshold, interval, key length, recalibration period) is not yet decided, insert `[NEEDS CLARIFICATION: define <X>]` — do not fabricate a number.
2. **Only cite FS-IDs that exist** in `specs/FS.md`. Each `CS-<CAT>-NNN` cites the `FS-<CAT>-NNN` it configures.
3. **Never invent citations.** Only the template's §-refs (GAMP 5 §D3.3.1.1 / §6.2.7, EU Annex 11 §4.4); regulatory anchors in justifications come from the URS/FS being configured.
4. **Number `CS-<CAT>-NNN` sequentially** within each category from 001.
5. **Cross-trace to RA-DET** where a config item realizes a risk mitigation (good audit story) — cite the `RA-DET-NNN` in the justification.
6. **Honor `language`.**

## Status semantics

Output `status: draft`. Instance frontmatter per CS's `instance_frontmatter_spec`: `title`, `type: instance`, `based_on_template: "CS"`, `based_on_template_version`, `system_id`, `traces_to` (the FS), `status`, `version`, `created`, `updated`, `language`. Set `lives_in_tool` if the config lives in a tool. Never `status: approved`.

## Post-flight (after writing `specs/CS.md`)

1. `validate-frontmatter.py specs/CS.md`.
2. `check-clarification-markers.py specs/CS.md --draft`.
3. `generate-rtm.py --specs-dir specs` — regenerate RTM (… + CS).
4. **Citation check** — every CS-ID's "Configures" cites an FS-ID present in `specs/FS.md`.
5. **Print summary**: # config items by area, # with `[NEEDS CLARIFICATION]` values, custom-code flag (count → DS).
6. **Suggest next**: `/gdd.tests.from-ra` (IQ verifies the config baseline against the CS; OQ verifies the configuration works).

## Output template

See `output-template.md` (this folder) for the exact shape of `specs/CS.md`.

## When to refuse

- `gamp_category != 4` → refuse (Cat 5 → DS; Cat 3 → not applicable).
- `.gxp-dev.yaml` / `specs/FS.md` missing → redirect.
- User asks to put custom code/macros in the CS → refuse; that is Cat 5 → DS.
- User asks to fabricate a configured value → refuse; use `[NEEDS CLARIFICATION:]`.
