---
description: |
  Functional Specification (FS) from an approved URS. Realizes the "what" of the
  URS with the technical "how" (GAMP 5 §D1 + §D3.3). Reads specs/URS.md and
  .gxp-dev.yaml (and RA-INIT if present, to scale detail by risk), then emits
  ≥1 FS-<CAT>-NNN per URS requirement with GxP=Y — full coverage — describing
  the realization, not repeating the requirement. Anti-hallucination: never
  invents technical mechanisms, citations, or coverage; uses
  [NEEDS CLARIFICATION: …] when the realization is not yet known.
argument-hint: "[optional context, e.g. /gdd-fs-from-urs Cat 4 COTS with Part 11 active]"
---

# gdd.fs.from-urs — Functional Specification Instantiation (Codex prompt)

> **Codex invocation.** Place this file under your Codex prompts/skills directory so it is exposed as the slash command **`/gdd-fs-from-urs`** (Codex derives the command name from the filename). `$ARGUMENTS` (if provided) is optional context about the system or category — use it to seed the realization approach, but still confirm each value before it lands in an FS row.
>
> **Two-part port.** This prompt carries the *procedure*. The *always-on guardrails* (anti-hallucination, anonymization, "never set status: approved", full-coverage invariant) live in `../AGENTS.snippet.md`, which the consumer pastes into their project `AGENTS.md` so they hold even when this prompt is not the active turn. See `../PORTING.md`.
>
> **Shared core.** The deterministic work — frontmatter validation, RTM generation, clarification-marker scan — is done by the harness-agnostic Python in `skills/_scripts/`, invoked by path. Do **not** re-implement it here. Source of truth: `skills/fs-from-urs/SKILL.md` + `generation-flow.md` + `output-template.md`.
>
> **No AskUserQuestion.** Codex has no `AskUserQuestion` tool. Wherever the source skill poses discrete choices (cardinality 1:1 vs 1:N, `covers_ds` yes/no, preset N/A confirmation), present them as an explicit enumerated prompt — e.g. "Reply 1 to confirm, 2 to change, 3 to mark N/A" — and wait for the user's reply before writing the row.

You produce a **Functional Specification (FS) instance** (`specs/FS.md`) that realizes a project's URS — the technical **"how"** answering the URS **"what"** — following `templates/csv/FS.md`. The FS is verified later in the OQ; each `FS-<CAT>-NNN` with prio=H generates ≥1 OQ test case.

## Pre-flight (do this FIRST, before generating any FS rows)

1. **Locate `.gxp-dev.yaml`** by walking up from the working directory. If absent, **STOP**: *"This project has no `.gxp-dev.yaml` manifest. Run `/gdd-init` first, then re-invoke `/gdd-fs-from-urs`."*
2. **Load the manifest**: `mode`, `profile`, `rigor_level`, `gamp_category`, `presets.*`, `language`.
3. **Locate `specs/URS.md`**. If missing → **STOP**: *"No URS found. Run `/gdd-urs-from-idea` to create one first."* **Check its `status`**: the FS canonically realizes an **approved** URS (GAMP 5 §D1). If the URS is `draft` or `in-review`, **warn** the user:
   > "The URS is not yet approved — you may proceed for a draft FS, but `traces_to` should be updated and the FS re-confirmed once the URS is approved."
   > Reply 1 to proceed anyway, 2 to abort.
4. **Read `specs/RA-INIT.md` if it exists** — it sets `gamp_category` and the high-risk functions; it **scales the FS depth** (focus detail on Risk Priority = H functions). If absent, proceed; RA-INIT is recommended but not blocking.
5. **Read the source template** `templates/csv/FS.md` — authoritative for structure, cardinality rules, and the `instance_frontmatter_spec`.
6. **Check if `specs/FS.md` already exists**. If yes, ask:
   > "specs/FS.md already exists. Reply 1 to replace, 2 to append, 3 to abort."

## Generation flow

Work **category by category** through the URS; lock each before the next. After each category, echo coverage (e.g. "FUNC: 5/5 URS GxP=Y realized"). Source of detail: `skills/fs-from-urs/generation-flow.md`.

### Interaction principles (every realization)

1. **Propose a realization with reasoning, then ask to confirm or change.** For each URS-ID, propose the technical HOW with the *why*, and let the user correct. A confirmed realization is grounded; an unconfirmed mechanism you write into the FS is invention (anti-hallucination rule). Example: *"`URS-FUNC-003` (excursion alarm): I'd realize it as an alarm rule evaluated on ingest + notification to the on-call distribution. Reply 1 to confirm, 2 to change, 3 to add [NEEDS CLARIFICATION]."*
2. **Present discrete choices as an explicit enumerated prompt** (cardinality 1:1 vs 1:N, `covers_ds` yes/no, preset N/A confirmation); free text for the realization wording.
3. **One category (or tight cluster) at a time.**
4. **Adapt depth to category + risk.** Use RA-INIT: spend the most detail on Risk Priority = H functions. `rigor_level: light` → concise realizations; `regulated` → full detail per GxP=Y.

### Generation step table

| Step | Produces |
|---|---|
| 1. Parse URS | every `URS-<CAT>-NNN` with its GxP (Y/N) and prio (H/M/L); note active presets (EREC/ESIG/SEC/API/MIGR) |
| 2. Realize GxP=Y requirements | ≥1 `FS-<CAT>-NNN` per URS GxP=Y row, citing the URS-ID in "Realizes", describing the technical HOW (Cat-aware) |
| 3. GxP=N requirements | FS row optional (1:0 permitted); add a one-line note under the section |
| 4. Realize inherited presets | FS-EREC / FS-ESIG / FS-SEC / FS-API / FS-MIGR per active URS presets; keep N/A rows for traceability |
| 5. Deviations §4.2 | any change since URS approval (empty if none; set `deviations_logged: false` if empty) |
| 6. Coverage §4.5 | per-category coverage summary table — NOT a per-ID matrix |

### Cardinality rules

- **1:1 by default.** One URS GxP=Y → one FS row.
- **1:N** when one requirement needs several realizations (e.g. a Part 11 control touching audit trail + access control + reporting). Propose cardinality with reasoning before writing N rows:
  > "I propose to realize URS-FUNC-007 with 2 FS rows (one for the storage layer, one for the retrieval API). Reply 1 to confirm 1:2, 2 to keep 1:1."
- **1:0** only for GxP=N — state it explicitly.

### Cat-aware realization

Adapt the "Realization (how)" wording to `gamp_category`:
- **Cat 3** (standard product): lightweight — describe the product's out-of-the-box behavior + parameterization. FS may fold into URS/VP.
- **Cat 4** (configured): describe the **configured COTS feature** that realizes the requirement; the concrete settings/values go in the `/gdd-cs-from-fs` Configuration Spec.
- **Cat 5** (custom): describe the software realization; feeds the `/gdd-ra-detail-from-urs-fs` RA-DET and the DS; large projects use Module Descriptions.

### Preset realization

The FS does **not** re-decide Part 11/Annex 11 applicability — it **inherits** the URS decision and realizes it:
- URS-EREC active → `FS-EREC-NNN` for each (technical mechanism per control).
- URS-ESIG active → `FS-ESIG-NNN` for each. Keep N/A preset rows (e.g. a hybrid-signature requirement marked N/A) **as a row** with realization "N/A — <reason>".
- URS-SEC-001/002 → `FS-SEC` (encryption + MFA). URS-API-001 → `FS-API` (validated interfaces). URS-MIGR-001 → `FS-MIGR` (validated migration) — skip only if the URS marked that preset N/A.

## The full-coverage invariant (CORE)

**Every `URS-<CAT>-NNN` with GxP=Y must be realized by ≥1 `FS-<CAT>-NNN`.** No GxP=Y / prio=H requirement may be left without a realization (1:0 is permitted **only** for GxP=N). This is the FS's reason to exist and the backbone of the RTM. Run the coverage check in post-flight and do not claim success while any GxP=Y URS-ID is uncovered.

## Anti-hallucination rules (NON-NEGOTIABLE — also enforced via AGENTS.md)

1. **Describe HOW, never repeat the WHAT.** If a row merely restates the URS text, it is wrong. Add the technical realization.
2. **Never invent technical mechanisms.** If the realization (framework, protocol, product feature) is not yet decided, insert `[NEEDS CLARIFICATION: how is <X> realized?]` — do not fabricate.
3. **Never invent citations.** Only §-refs the FS template already carries (GAMP 5 §D1/§D3.3, EU Annex 11 §4.4, 21 CFR Part 11).
4. **Only cite URS-IDs that exist** in `specs/URS.md`. Each FS row's "Realizes" column must reference a real `URS-<CAT>-NNN`.
5. **Number `FS-<CAT>-NNN` sequentially** within each category from 001.
6. **Inherit GxP/prio from the URS** — do not re-evaluate them in the FS.
7. **Honor the `language`** field of the manifest; do not mix languages within the FS.
8. **Read, do not write, `templates/csv/FS.md`.**

## Status semantics

`specs/FS.md` starts at `status: draft`. Instance frontmatter:

```yaml
---
title: "FS — Functional Specification for {{system_name}}"
type: instance
based_on_template: "FS"
based_on_template_version: "0.1.0"
project_id: "{{project_id}}"
system_id: "{{system_id}}"
traces_to: "specs/URS.md ({{urs_version}}, {{urs_status}})"
gamp_category: {{3|4|5}}
status: draft
version: "0.1"
created: "{{today}}"
updated: "{{today}}"
language: "{{language from .gxp-dev.yaml}}"
deviations_logged: {{bool}}
profile: "{{profile}}"
mode: "{{mode}}"
---
```

**Never** set `status: in-review` or `status: approved`.

## Output shape

Mirror `templates/csv/FS.md` and `skills/fs-from-urs/output-template.md`. Key sections:

- **§0 Identification and signatures** — system table (name, identifier, URS being realized + status, supplier, version, GAMP category) + signature table: Author, Reviewer 1 (System Owner/IT), Reviewer 2 (SME/Process Owner), Reviewer 3 (Data Owner), Approver 1 (System Owner), Approver 2 (Quality Unit). Unknown → `[NEEDS CLARIFICATION: assign <role>]`.
- **§1 Introduction** — one paragraph: this FS realizes the URS for `{{system_name}}`; V-Model phase; verified in OQ. For Cat 4, note that concrete settings/values live in the CS.
- **§2 Definitions and abbreviations** — FS/URS/CS/DS + project-specific terms.
- **§4.1 System Overview** — realization overview: modules, key interfaces, high-level architecture (Cat-aware).
- **§4.2 Deviations to URS** — table (affected URS-ID | deviation | impact | action); or "No deviations" note with `deviations_logged: false`.
- **§4.5 URS→FS traceability coverage (summary)** — per-category table: `Category | URS GxP=Y | FS entries | Coverage`. End: "Blocking gaps (GxP=Y or prio=H without FS realization): none." Do NOT render one row per URS-ID.
- **§5–11 Realization tables** — one section per category with ≥1 realization, table: `FS ID-No. | Realizes (URS-ID) | Realization (how)`. Sections 9.2 (FS-EREC) and 9.3 (FS-ESIG) are mandatory and non-empty if those URS presets are active.
- **§12 Related documents** — URS, RA-INIT, CS (Cat 4) / DS (Cat 5), RA-DET, VP.
- **§13 Revision history** — `| 0.1 | <today> | Initial draft (FS) — <author>, <dept> |`

Anti-patterns to avoid in the output:
- An FS row whose "Realization" merely repeats the URS WHAT.
- A GxP=Y / prio=H URS requirement with no FS realization.
- `FS-<CAT>-NNN` whose "Realizes" cites a URS-ID not in `specs/URS.md`.
- A new category code not in the URS or not in the 22 canonical acronyms.
- Invented technical mechanisms (use `[NEEDS CLARIFICATION:]` instead).
- Regulatory §-citations beyond what the template carries.
- Deleting an obsolete FS row (strike through `~~...~~`; never delete — preserves traceability).
- `status: approved`, or any banned legacy category code / corporate identifier.
- A per-ID §4.5 matrix for a preset-heavy system (use the per-category coverage summary).

## Post-flight — call the shared Python core

From the consumer project root (substitute `<gdd-path>` with your `gxp-driven-dev` install):

```bash
python <gdd-path>/skills/_scripts/validate-frontmatter.py specs/FS.md
python <gdd-path>/skills/_scripts/check-clarification-markers.py specs/FS.md --draft
python <gdd-path>/skills/_scripts/generate-rtm.py --specs-dir specs
```

If `validate-frontmatter.py` fails, report the errors and do **not** claim success. After the RTM is regenerated, run the **coverage check**: confirm every URS GxP=Y is cited by ≥1 FS row. Then print the summary:
- FS-ID count (per category and total)
- URS→FS coverage % (GxP=Y rows covered)
- Blocking H gaps (must be 0)
- Clarification marker count

Suggest next steps:
- Cat 4 → `/gdd-cs-from-fs` (Configuration Spec)
- Any category → `/gdd-ra-detail-from-urs-fs` (RA-DET on the high-risk functions)
- After RA-DET → `/gdd-tests-from-ra` (IQ/OQ/PQ test protocols)

## When to refuse

- `.gxp-dev.yaml` missing → redirect to `/gdd-init`.
- `specs/URS.md` missing → redirect to `/gdd-urs-from-idea`.
- User asks to leave a GxP=Y / prio=H requirement unrealized → refuse (blocking coverage gap); explain why the full-coverage invariant exists.
- User asks to copy the URS text as the FS realization → refuse; the FS must add the technical HOW, not repeat the WHAT.
- User asks to fabricate a realization for an undecided mechanism → refuse; insert `[NEEDS CLARIFICATION: how is <X> realized?]` instead.
- User asks to skip the post-flight coverage check → refuse; the check is the proof-of-completeness gate.
