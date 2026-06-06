---
description: "Configuration Specification (CS) from an approved FS — GAMP 5 Cat 4 ONLY (§D3.3.1.1). Documents the concrete settings/parameters configured for a configurable product: workflows, business rules, security/roles, integration mappings, audit-trail config. Selective — only the FS items that require configuration, each with a configured value + justification. Custom code/macros are flagged Cat 5 and go to the DS, not here. Anti-hallucination: never invents configuration values; uses [NEEDS CLARIFICATION: …] when a value is unknown. Output: specs/CS.md."
argument-hint: "[nothing needed — pre-flight reads .gxp-dev.yaml and specs/FS.md automatically]"
---

# gdd.cs.from-fs — Configuration Specification (Cat 4) (Codex prompt)

> **Codex invocation.** Place this file under your Codex prompts/skills directory so it is exposed as the slash command **`/gdd-cs-from-fs`** (Codex derives the command name from the filename). No `$ARGUMENTS` seed is needed — all inputs are read from `.gxp-dev.yaml` and `specs/FS.md` during pre-flight.
>
> **Two-part port.** This prompt carries the *procedure*. The *always-on guardrails* (anti-hallucination, anonymization, linear status, "never set status: approved") live in `../AGENTS.snippet.md`, which the consumer pastes into their project `AGENTS.md` so they hold even when this prompt is not the active turn. See `../PORTING.md`.
>
> **Shared core.** The deterministic work — frontmatter validation, clarification-marker scan, RTM generation, anti-leak guard — is done by the harness-agnostic Python in `skills/_scripts/`, invoked by path. Do **not** re-implement it here. Source of truth: `skills/cs-from-fs/SKILL.md` + `generation-flow.md` + `output-template.md`.
>
> **No AskUserQuestion.** Codex has no `AskUserQuestion` tool. Wherever the source skill poses discrete choices (e.g. `lives_in_tool` yes/no, custom code present yes/no, replace/append/abort), present them as an explicit enumerated prompt: *"Reply 1 = replace / 2 = append / 3 = abort."* For configured values, propose a value with reasoning and ask the user to confirm or correct — do not silently write unconfirmed values.

You produce a **CS instance** (`specs/CS.md`) — the record of the settings/parameters configured for a **Cat 4** product (GAMP 5 §D3.3.1.1) — that implements the configuration the FS defines. The CS is verified in IQ (config baseline) + OQ (config works).

## Pre-flight (do this FIRST, before any generation)

1. **Locate `.gxp-dev.yaml`** by walking up from the working directory. If absent, **STOP**: *"This project has no `.gxp-dev.yaml` manifest. Run `/gdd-init` first, then re-invoke `/gdd-cs-from-fs`."*
2. **Load the manifest**: `mode`, `profile`, `rigor_level`, `gamp_category`, `id_scheme` + `custom_alias`, `language`.
3. **Confirm `gamp_category == 4`.** This skill is **Cat 4 only**:
   - **Cat 5** (custom) → **refuse**: *"This system has custom code. Document the design in the DS using `/gdd-fs-from-urs` (DS path); the CS is not applicable."*
   - **Cat 3** (standard, no meaningful configuration) → **refuse**: *"Cat 3 products have no meaningful configuration; a CS is not applicable."*
4. **Locate `specs/FS.md`** — **required**. If missing → redirect to `/gdd-fs-from-urs`. If present but `status != approved`, warn: *"FS is still `<status>` — the CS configures an approved FS. Proceed anyway? Reply 1 = yes / 2 = abort."*
5. **Read `specs/RA-INIT.md` / `specs/RA-DET.md` if present** — they scale the detail of critical configuration (config items that mitigate high-RPN risks deserve explicit values + justification).
6. **Read the source template** `templates/csv/CS.md` — authoritative for the by-area structure (§3.1–3.5) and the Cat 5 custom-code rule.
7. **Check if `specs/CS.md` already exists**. If it does, present: *"specs/CS.md already exists. Reply 1 = replace / 2 = append / 3 = abort."*

## Generation flow

Work **area by area** (§3.1 → §3.5). After each area, echo coverage (e.g. *"Security: 7 config items documented"*). Lock each area before moving to the next.

**Interaction principles (every config item):**
1. **Propose a configured value with reasoning, then ask to confirm or change.** A confirmed value is grounded; an unconfirmed value you write into the CS is invention (anti-hallucination rule #1). Example: *"For the alarm band I'd configure lower 2.0 °C / upper 8.0 °C (the GMP cold-storage range). Confirm, or is your range different?"*
2. **Offer discrete choices as an explicit enumerated prompt** (`lives_in_tool` yes/no, custom-code present yes/no). Free text for parameter descriptions and justifications.
3. **One area (or tight cluster) at a time.**
4. **Adapt depth to risk.** Config items that mitigate high-RPN RA-DET risks get explicit values + justification (cite the `RA-DET-NNN`); routine settings can be concise.

| Step | Produces |
|---|---|
| Parse FS | the `FS-<CAT>-NNN` items that **require configuration** (selective — not every FS-ID) |
| Document | one `CS-<CAT>-NNN` per configurable item: Setting/Parameter + **Configured value** + Justification, citing the FS-ID |
| §3.1 Workflows / business rules | `CS-FUNC-NNN` / `CS-PROC-NNN` (intervals, alarm bands, notification rules, report generation) |
| §3.2 Security, roles and signatures | `CS-SEC-NNN` / `CS-ESIG-NNN` (role-permission matrix, encryption, MFA, password policy, signature manifestation, tamper-evidence) |
| §3.3 Integrations / interfaces | `CS-API-NNN` (endpoints, payload mappings, retry) |
| §3.4 Audit trail / records | `CS-EREC-NNN` (audit-trail scope/fields, reason prompt, review workflow) |
| §3.5 Other | `CS-DATA/FLOW/REPORT/OPS/PERIPH-NNN` (retention, buffer, report template, backup schedule, recalibration interval) |
| Dependencies §4 | config items that depend on external systems (IdP, gateways, key store) |
| Custom code §5 | flag any macro/script as **Cat 5 → DS** (cross-reference only) |

### Selectivity (CORE — different from the FS)

The CS is **selective**: it documents only the FS items that have a **concrete configurable setting**. Do NOT mirror every FS-ID (that is the FS's job). A configured value with no real parameter to set adds noise. Conversely, every config item that a high-RPN RA-DET mitigation relies on **must** be documented with its value.

### Cat 4 boundary + custom code

- **Custom code = Cat 5 → DS.** Any macro, script, or custom code inside the Cat 4 platform is documented in the DS (Cat 5 path), not the CS. §5 lists it only as a cross-reference. If the system has substantial custom code, it may not be a pure Cat 4 — flag it.
- **Config may live in a tool.** GAMP 5 §D3/§M9 allows the configuration to live in a config-management tool with an audit trail. If so, set `lives_in_tool: true`; this CS is the **summary record** and the tool is the source of truth.
- **Anti-drift.** The CS must stay in sync with the live configuration; a static CS while the config evolves is a configuration-management gap.

## Anti-hallucination rules (NON-NEGOTIABLE — also enforced via AGENTS.md)

1. **Never invent a configured value.** If the concrete value (threshold, interval, key length, recalibration period) is not yet decided, insert `[NEEDS CLARIFICATION: define <X>]` — do not fabricate a number.
2. **Only cite FS-IDs that exist** in `specs/FS.md`. Each `CS-<CAT>-NNN` cites the `FS-<CAT>-NNN` it configures.
3. **Never invent citations.** Only the template's §-refs (GAMP 5 §D3.3.1.1 / §6.2.7, EU Annex 11 §4.4); regulatory anchors in justifications come from the URS/FS being configured.
4. **Number `CS-<CAT>-NNN` sequentially** within each category from 001.
5. **Cross-trace to RA-DET** where a config item realizes a risk mitigation — cite the `RA-DET-NNN` in the justification.
6. **Honor `language`.**

## Citation gate (core check before claiming complete)

Before claiming complete: **every `CS-<CAT>-NNN`'s "Configures" must cite an `FS-<CAT>-NNN` that exists in `specs/FS.md`.** A CS item with no upstream FS item is an orphan (either the FS is incomplete or the config item is invented).

## Status semantics

Output `status: draft`. Instance frontmatter:

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
created: "{{today}}"
updated: "{{today}}"
language: "{{language from .gxp-dev.yaml}}"
lives_in_tool: {{bool}}              # true if the config lives in a tool with audit trail

# Copied from .gxp-dev.yaml for self-contained reference
gamp_category: 4
profile: "{{profile}}"
mode: "{{mode}}"
---
```

**Never** set `status: in-review` or `status: approved`.

## Output shape

Mirror `templates/csv/CS.md`. Sections in order:

- **§0 Identification and signatures** — identity table (name, identifier, FS being configured + status, product version, config-management tool) + signatures: Author, Reviewer = SME, Approver = System Owner, Approver = Quality Unit. Unknown → `[NEEDS CLARIFICATION: assign <role>]`. If `lives_in_tool`, add a `> [!note]` explaining the tool is the source of truth and this CS is the summary record. If the FS is still draft, add a `> [!warning]` cascade-order note.
- **§1 Objective** — one paragraph documenting the configuration of `<product> <version>` that implements the FS; note whether custom code is involved.
- **§2 Definitions** — CS / config baseline / config drift / config item.
- **§3 Configuration by area** — one table per area that has config items (omit empty areas):
  - §3.1: `CS-ID | Configures (FS-ID) | Setting / Parameter | Configured value | Justification`
  - §3.2: `CS-ID | Configures (FS-ID) | Security setting | Configured value | Justification`
  - §3.3: `CS-ID | Configures (FS-ID) | Integration mapping | Configured value | Justification`
  - §3.4: `CS-ID | Configures (FS-ID) | Audit trail / records setting | Configured value | Justification`
  - §3.5: `CS-ID | Configures (FS-ID) | Parameter | Value | Justification`
- **§4 Configuration dependencies** — `Config item | Depends on | Comment`
- **§5 Custom code within the platform (Cat 5 flag)** — `Custom element | Reference in DS`. For a pure Cat 4: *"None — pure configured COTS; no custom code."*
- **§6 Related documents** — FS, IQ, OQ, DS (if custom code).
- **§7 Revision history** — `| 0.1 | <today> | Initial draft (CS) — <author>, <dept> |`

**Anti-patterns — do NOT produce:**
- A CS that mirrors every FS-ID (the CS is selective — only items with a real configurable setting).
- A fabricated configured value where the value is undecided (use `[NEEDS CLARIFICATION:]`).
- A `CS-<CAT>-NNN` whose "Configures" cites an FS-ID not present in `specs/FS.md`.
- Custom code/macros documented as configuration (those are Cat 5 → DS; §5 cross-reference only).
- A CS for a Cat 3 (not applicable) or Cat 5 (use DS).
- A new category code outside the 22 canonical acronyms.
- `status: approved`, or any banned legacy category code / corporate identifier.
- A static CS that drifts from the live configuration.

## Post-flight — call the shared Python core

From the consumer project root (substitute `<gdd-path>` with your `gxp-driven-dev` install):

```bash
python <gdd-path>/skills/_scripts/validate-frontmatter.py specs/CS.md
python <gdd-path>/skills/_scripts/check-clarification-markers.py specs/CS.md --draft
python <gdd-path>/skills/_scripts/generate-rtm.py --specs-dir specs
```

If `validate-frontmatter.py` fails, report the errors and do **not** claim success. Perform the **citation check** manually: verify every `CS-<CAT>-NNN`'s "Configures" cell contains an FS-ID present in `specs/FS.md`.

Then print a summary: config items by area, number of `[NEEDS CLARIFICATION]` values, custom-code flag (count flagged → DS). Suggest the next step:
- `/gdd-tests-from-ra` — IQ verifies the config baseline against the CS; OQ verifies the configuration works.
- Resolve all `[NEEDS CLARIFICATION]` markers before leaving `draft`.

## When to refuse

- `gamp_category != 4` → refuse (Cat 5 → DS; Cat 3 → not applicable).
- `.gxp-dev.yaml` missing → redirect to `/gdd-init`.
- `specs/FS.md` missing → redirect to `/gdd-fs-from-urs`.
- User asks to put custom code/macros in the CS → refuse; that is Cat 5 → DS.
- User asks to fabricate a configured value → refuse; use `[NEEDS CLARIFICATION:]`.
- `rigor_level: regulated` and the FS `status != approved` and the user wants to skip the warning → refuse and explain cascade order.
