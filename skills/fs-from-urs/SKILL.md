---
name: gdd.fs.from-urs
description: |
  Functional Specification (FS) from an approved URS. Realizes the "what" of the
  URS with the technical "how" (GAMP 5 §D1 + §D3.3). Reads `specs/URS.md` and
  `.gxp-dev.yaml` (and RA-INIT if present, to scale detail by risk), then emits
  ≥1 `FS-<CAT>-NNN` per URS requirement with GxP=Y — full coverage — describing
  the realization, not repeating the requirement. Anti-hallucination: never
  invents technical mechanisms, citations, or coverage; uses
  `[NEEDS CLARIFICATION: …]` when the realization is not yet known.
  Use this skill when:
  - A `specs/URS.md` exists (ideally approved) and no `specs/FS.md` yet
  - The user says "spec the functions", "how will we build it", or "draft the FS"
  - After RA-INIT has set the GAMP category (it scales the FS depth)
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# `gdd.fs.from-urs` — Functional Specification

You produce an **FS instance** (`specs/FS.md`) that realizes a project's URS — the technical **"how"** answering the URS **"what"** — following `templates/csv/FS.md`. The FS is verified later in the OQ; each `FS-<CAT>-NNN` with prio=H generates ≥1 OQ test case.

## Pre-flight (do this FIRST)

1. **Locate `.gxp-dev.yaml`**: walk up from cwd. If missing, **STOP** → `/gdd.init`.
2. **Load the manifest**: `mode`, `profile`, `rigor_level`, `gamp_category`, `presets.*`, `language`.
3. **Locate the URS** (`specs/URS.md`). If missing → redirect to `/gdd.urs.from-idea`. **Check its `status`**: the FS canonically realizes an **approved** URS (GAMP 5 §D1). If the URS is `draft`/`in-review`, **warn** the user — you may proceed for a draft FS, but `traces_to` should be updated and the FS re-confirmed once the URS is approved.
4. **Read RA-INIT if it exists** (`specs/RA-INIT.md`) — it sets the GAMP category and the high-risk functions; it **scales the FS depth** (focus detail on Risk Priority = H functions).
5. **Read the source template** `templates/csv/FS.md` — authoritative for structure and the cardinality/coverage rules.
6. **Check if `specs/FS.md` already exists**: ask replace / append / abort.

## Generation flow

Follow `generation-flow.md` (this folder). Summary:

| Step | Produces |
|---|---|
| Parse URS | every `URS-<CAT>-NNN` with its GxP (Y/N) and prio (H/M/L) |
| Realize | ≥1 `FS-<CAT>-NNN` per URS GxP=Y, citing the URS-ID in "Realizes", describing the technical HOW |
| Presets | realize each active URS-EREC/ESIG/SEC/API/MIGR (1:1; keep N/A rows for traceability) |
| Deviations §4.2 | any change since URS approval (empty if none) |
| Coverage §4.5 | per-category coverage summary (per-ID traces live in sections 5–11) |

## The full-coverage invariant (CORE)

**Every `URS-<CAT>-NNN` with GxP=Y must be realized by ≥1 `FS-<CAT>-NNN`.** No GxP=Y / prio=H requirement may be left without a realization (1:0 is permitted **only** for GxP=N). This is the FS's reason to exist and the backbone of the RTM. Run the coverage check (post-flight) and do not claim success while any GxP=Y URS-ID is uncovered.

## Cat-aware realization

Adapt the "Realization (how)" wording to `gamp_category`:
- **Cat 3** (standard product): lightweight — describe the product's out-of-the-box behavior + parameterization. FS may fold into URS/VP.
- **Cat 4** (configured): describe the **configured COTS feature** that realizes the requirement; the concrete settings/values go in the [CS](../../templates/csv/CS.md).
- **Cat 5** (custom): describe the software realization; feeds the [DS](../../templates/csv/DS.md); large projects use Module Descriptions.

## Anti-hallucination rules (NON-NEGOTIABLE)

1. **Describe HOW, never repeat the WHAT.** If a row merely restates the URS text, it is wrong. Add the technical realization.
2. **Never invent technical mechanisms.** If the realization (framework, protocol, product feature) is not yet decided, insert `[NEEDS CLARIFICATION: how is <X> realized?]` — do not fabricate.
3. **Never invent citations.** Only the §-refs the FS template carries (GAMP 5 §D1/§D3.3, EU Annex 11 §4.4, 21 CFR Part 11).
4. **Only cite URS-IDs that exist** in `specs/URS.md`. Each FS row's "Realizes" cites a real `URS-<CAT>-NNN`.
5. **Number `FS-<CAT>-NNN` sequentially** within each category from 001.
6. **Inherit GxP/prio from the URS** — do not re-evaluate them here.
7. **Honor the `language`** field of the manifest.

## Status semantics

Output starts at `status: draft`. Instance frontmatter must include the fields from FS's `instance_frontmatter_spec`: `title`, `type: instance`, `based_on_template: "FS"`, `based_on_template_version`, `system_id`, `traces_to` (the URS instance + version), `status`, `version`, `created`, `updated`, `language`. If §4.2 logs deviations, set `deviations_logged: true`. Never set `status: approved` (human signatures).

## Post-flight (after writing `specs/FS.md`)

1. `validate-frontmatter.py specs/FS.md` — report errors, no success-claim on failure.
2. `check-clarification-markers.py specs/FS.md --draft` — report count (markers expected in draft).
3. `generate-rtm.py --specs-dir specs` — regenerate RTM (now URS + RA-INIT + FS).
4. **Coverage check** — confirm every URS GxP=Y is cited by ≥1 FS row. Report coverage % and any uncovered GxP=Y (must be empty except documented N/A).
5. **Print summary**: FS-ID count, URS→FS coverage %, blocking H gaps (must be 0), marker count.
6. **Suggest next**: `/gdd.cs.from-fs` (Cat 4 — Configuration Spec) and/or `/gdd.ra.detail.from-urs-fs` (RA-DET on the high-risk functions) → then `/gdd.tests.from-ra` (IQ/OQ/PQ).

## Output template

See `output-template.md` (this folder) for the exact shape of `specs/FS.md`.

## When to refuse

- `.gxp-dev.yaml` missing → `/gdd.init`. `specs/URS.md` missing → `/gdd.urs.from-idea`.
- User asks to leave a GxP=Y / prio=H requirement unrealized → refuse (blocking gap).
- User asks to copy the URS text as the FS → refuse; the FS must add the technical HOW.
- User asks to fabricate a realization for an undecided mechanism → refuse; use `[NEEDS CLARIFICATION:]`.
