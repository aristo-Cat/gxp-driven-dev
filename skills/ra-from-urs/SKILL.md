---
name: gdd.ra.from-urs
description: |
  Initial Risk Assessment (RA-INIT) from a URS. Implements GAMP 5 §M3 steps 1-2
  (Initial RA + System Impact, and Identify Functions with Impact). Reads
  `specs/URS.md` (may be draft) and `.gxp-dev.yaml`, then determines the GAMP
  category, Part 11/Annex 11 applicability, the GxP-critical functions, and a
  qualitative H/M/L risk register — deciding whether a Detailed RA (RA-DET) is
  required. Anti-hallucination: never invents categories, risk ratings, or
  citations; uses `[NEEDS CLARIFICATION: …]` when it cannot assess a risk.
  Use this skill when:
  - A `specs/URS.md` exists (draft or approved) and no `specs/RA-INIT.md` yet
  - The user says "assess risk", "what GAMP category", or "do the initial RA"
  - Before approving the URS (the URS inherits `gamp_category` from RA-INIT)
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# `gdd.ra.from-urs` — Initial Risk Assessment

You produce a **RA-INIT instance** (`specs/RA-INIT.md`) from a project's URS, implementing **GAMP 5 §M3 steps 1-2** of the five-step QRM process. The output's headline deliverable is the **determined GAMP category**, which scales the rest of the V-Model. Follow the canonical pattern of `templates/csv/RA-INIT.md`.

## Pre-flight (do this FIRST, before any questions)

1. **Locate `.gxp-dev.yaml`**: walk up from the cwd. If not found, **STOP**:
   > *"This project has no `.gxp-dev.yaml` manifest. Run `/gdd.init` first, then re-invoke me."*

2. **Load the manifest** and remember: `mode`, `profile`, `rigor_level`, `gamp_category` (may already be declared — treat as a *proposal* to confirm, not a fact), `presets.*`, `language`.

3. **Locate the URS**: read `specs/URS.md`. If missing, **STOP** and redirect to `/gdd.urs.from-idea`. The URS may be `draft` — RA-INIT may run before the URS is approved (GAMP 5 §M3 step 1: *"before or during requirements development"*).

4. **Read `GXP-ASSESS.md` if it exists** — it contributes the initial GxP determination and regulatory context; inherit rather than re-ask.

5. **Read the source template** `templates/csv/RA-INIT.md` — authoritative reference for structure, the H/M/L matrices (§3.1-3.2), and the §M4 category criteria.

6. **Check if `specs/RA-INIT.md` already exists**: if yes, ask replace / append / abort.

## Generation flow

Follow `generation-flow.md` (this folder) for the detailed step order, the risk matrices, and the four interaction principles. Summary:

| Phase | GAMP §M3 | Produces |
|---|---|---|
| Step 1 | Initial RA + System Impact | `gxp_determination`, `system_impact` (PS/PQ/DI), **`gamp_category_decision` + rationale**, `part11_applicable` (§5.4 five questions) |
| Step 2 | Identify Functions with Impact | functions-with-impact table (parse `URS-<CAT>-NNN` with `GxP=Y`) |
| Risk register | §11.5.4 | `RA-INIT-NNN` rows: Severity × Probability → Class; × Detectability → Priority |
| RA-DET decision | §8 triggers | `detailed_ra_required` (bool) + justification |

## Anti-hallucination rules (NON-NEGOTIABLE)

1. **Never invent a GAMP category.** Propose one from the §M4 criteria + the configured/custom nature of the system, state the rationale, and have the user confirm. If genuinely unclear, insert `[NEEDS CLARIFICATION: Cat 3, 4 or 5? — depends on whether the product is configured or bespoke]`.
2. **Never invent risk ratings.** Severity, Probability, Detectability must each be reasoned, not guessed. When the user cannot supply the information needed to rate a factor, insert `[NEEDS CLARIFICATION: …]` and do not fabricate an H/M/L.
3. **Never invent regulatory citations.** Use only the citations the source template carries (GAMP 5 §5.3 / §M3 / §M4, ICH Q9, EU Annex 11 §4). Do not attach new §-numbers.
4. **Only cite URS-IDs that exist.** Each `RA-INIT-NNN` cites a real `URS-<CAT>-NNN` from `specs/URS.md`, or the literal `system-level` for system-level risks. Never reference a URS-ID that is not in the URS.
5. **Number `RA-INIT-NNN` sequentially** from `001`; never reuse or skip.
6. **Honor the `language` field** of the manifest.

## Key methodology rules (easy to get wrong)

- **Severity derives from the business process, NOT the GAMP category.** A Cat 3 system controlling a critical process can have severity H. Do not inflate severity because it is Cat 5. (GAMP 5 §M3.)
- **Probability scales with the GAMP category** (Cat 1 → 5). This is the axis the category affects — not severity.
- **Low detectability raises priority.** Use the matrices in `templates/csv/RA-INIT.md` §3.1 (Class = Severity × Probability) and §3.2 (Priority = Class × Detectability) — do not improvise the arithmetic.

## Status semantics

Output starts at `status: draft`. Instance frontmatter must include the fields from RA-INIT's `instance_frontmatter_spec`: `title`, `type: instance`, `based_on_template: "RA-INIT"`, `based_on_template_version`, `system_id`, `traces_to` (the URS), `gamp_category` (the decided value), `status`, `version`, `created`, `updated`, `language`. If `detailed_ra_required: true`, add `detailed_ra_ref`.

> [!warning] Approval order
> RA-INIT must reach `approved` **before** the URS, because the URS inherits `gamp_category` from here. Never set `status: approved` yourself — that needs human signatures (Process Owner = owner of severity).

## Propagation (after writing)

The category and Part 11 applicability decided here are inputs to other specs:
- Propagate `gamp_category_decision` → the `{{gamp_category}}` of `specs/URS.md` and (later) `specs/FS.md`. If the URS already declares a different category, **flag the discrepancy** to the user; do not silently overwrite.
- Propagate the §5.4 applicability → the URS `preset_part11_active` and the EREC/ESIG/SEC/API/MIGR preset activation. Flag any inconsistency with the URS.

## Post-flight (after writing `specs/RA-INIT.md`)

1. `python <gdd-path>/skills/_scripts/validate-frontmatter.py specs/RA-INIT.md` — report errors, do not claim success on failure.
2. `python <gdd-path>/skills/_scripts/check-clarification-markers.py specs/RA-INIT.md --draft` — report the count (markers are expected in draft; `--draft` exits 0).
3. `python <gdd-path>/skills/_scripts/generate-rtm.py --specs-dir specs` — regenerate the RTM now covering URS + RA-INIT.
4. **Print summary**: determined category + rationale, count of GxP-critical functions, count of `RA-INIT-NNN` by Risk Priority (H/M/L), the RA-DET decision, and any clarification markers.
5. **Suggest next step**:
   - `detailed_ra_required: true` → `/gdd.ra.detail.from-urs-fs` (after FS) for the high-priority functions.
   - Always → `/gdd.fs.from-urs` to draft the FS (the category now scales its depth).
   - Markers > 0 → resolve before promoting RA-INIT to `in-review`.

## Output template

See `output-template.md` (this folder) for the exact shape of `specs/RA-INIT.md`.

## When to refuse

- `.gxp-dev.yaml` missing → redirect to `/gdd.init`.
- `specs/URS.md` missing → redirect to `/gdd.urs.from-idea`.
- User asks to "just assign a category" without rationale → refuse; the category needs §M4 justification.
- User asks to fabricate risk ratings to "pass" → refuse; cite anti-hallucination policy.
