---
description: |
  Initial Risk Assessment (RA-INIT) from a URS. Implements GAMP 5 §M3 steps 1-2
  (Initial RA + System Impact, and Identify Functions with Impact). Reads
  `specs/URS.md` (may be draft) and `.gxp-dev.yaml`, then determines the GAMP
  category, Part 11/Annex 11 applicability, the GxP-critical functions, and a
  qualitative H/M/L risk register — deciding whether a Detailed RA (RA-DET) is
  required. Anti-hallucination: never invents categories, risk ratings, or
  citations; uses `[NEEDS CLARIFICATION: …]` when it cannot assess a risk.
argument-hint: "[nothing needed — reads specs/URS.md and .gxp-dev.yaml automatically]"
---

# gdd.ra.from-urs — Initial Risk Assessment (Codex prompt)

> **Codex invocation.** Place this file under your Codex prompts/skills directory so it is exposed as the slash command **`/gdd-ra-from-urs`** (Codex derives the command name from the filename). This skill takes no seed argument — it reads `specs/URS.md` and `.gxp-dev.yaml` automatically on pre-flight.
>
> **Two-part port.** This prompt carries the *procedure*. The *always-on guardrails* (anti-hallucination, anonymization, linear status, never set status: approved) live in `../AGENTS.snippet.md`, which the consumer pastes into their project `AGENTS.md` so they hold even when this prompt is not the active turn. See `../PORTING.md`.
>
> **Shared core.** The deterministic work — frontmatter validation, RTM generation, clarification-marker scan — is done by the harness-agnostic Python in `skills/_scripts/`, invoked by path. Do **not** re-implement it here. Source of truth: `skills/ra-from-urs/SKILL.md` + `generation-flow.md` + `output-template.md`.
>
> **No AskUserQuestion.** Codex has no `AskUserQuestion` tool. Wherever the skill poses discrete choices (GAMP category, H/M/L ratings, Yes/No Part 11 questions, proceed-to-RA-DET), present them as an explicit enumerated prompt and wait for a reply (e.g. "Reply 1=Cat 3 / 2=Cat 4 / 3=Cat 5 / 4=needs more context").

You produce a **RA-INIT instance** (`specs/RA-INIT.md`) from a project's URS, implementing **GAMP 5 §M3 steps 1-2** of the five-step QRM process. The output's headline deliverable is the **determined GAMP category**, which scales the rest of the V-Model. Follow the canonical pattern of `templates/csv/RA-INIT.md`.

## Pre-flight (do this FIRST, before any questions)

1. **Locate `.gxp-dev.yaml`**: walk up from the cwd. If not found, **STOP**:
   *"This project has no `.gxp-dev.yaml` manifest. Run `/gdd-init` first, then re-invoke `/gdd-ra-from-urs`."*

2. **Load the manifest** and remember: `mode`, `profile`, `rigor_level`, `gamp_category` (may already be declared — treat as a *proposal* to confirm, not a fact), `presets.*`, `language`.

3. **Locate the URS**: read `specs/URS.md`. If missing, **STOP** and redirect:
   *"No `specs/URS.md` found. Run `/gdd-urs-from-idea` first, then re-invoke `/gdd-ra-from-urs`."*
   The URS may be `draft` — RA-INIT may run before the URS is approved (GAMP 5 §M3 step 1: *"before or during requirements development"*).

4. **Read `GXP-ASSESS.md` if it exists** — it contributes the initial GxP determination and regulatory context; inherit rather than re-ask.

5. **Read the source template** `templates/csv/RA-INIT.md` — authoritative reference for structure, the H/M/L matrices (§3.1-3.2), and the §M4 category criteria.

6. **Check if `specs/RA-INIT.md` already exists**: if yes, present:
   ```
   specs/RA-INIT.md already exists. Reply:
   1 — Replace (overwrite)
   2 — Append
   3 — Abort
   ```
   Wait for the reply before continuing.

## Generation flow

Work through the steps **in order**; lock each step before advancing. The category decision (Step 1.3) gates everything downstream. After each step, output a 1-line **confirmation echo** ("Category locked: Cat 4 — configured COTS").

**Interaction principles (every question):**
1. **Propose a default with reasoning, then ask to confirm or change.** Never ask open-ended. For risk work: propose a Severity/Probability/Detectability with the *why*, and let the user correct. A confirmed proposal is grounded; an unconfirmed rating you write into the register is invention (anti-hallucination rule #2). Example: *"For 'excursion not alarmed' I'd rate Severity H (undetected bad storage → product/patient impact), Probability M (Cat 4 configured), Detectability L (silent alarm failure is hard to notice) → Risk Priority H. Agree, or adjust?"*
2. **Offer discrete choices as an explicit enumerated prompt** (GAMP category 1/3/4/5; H/M/L ratings; Yes/No Part 11 questions; proceed-to-RA-DET). Free text only for rationale/justification.
3. **One decision (or tight cluster) at a time, in sequence.**
4. **Adapt depth to rigor + impact.** `rigor_level: light` / low impact → compress (assess only the clearly GxP-critical functions). `regulated` / high impact → assess every GxP=Y function.

| Phase | GAMP §M3 | Produces |
|---|---|---|
| Step 1 | Initial RA + System Impact | `gxp_determination`, `system_impact` (PS/PQ/DI), **`gamp_category_decision` + rationale**, `part11_applicable` (§5.4 five questions) |
| Step 2 | Identify Functions with Impact | functions-with-impact table (parse `URS-<CAT>-NNN` with `GxP=Y`) |
| Risk register | §11.5.4 | `RA-INIT-NNN` rows: Severity × Probability → Class; × Detectability → Priority |
| RA-DET decision | §8 triggers | `detailed_ra_required` (bool) + justification |

### Step 1 — Initial Risk Assessment + System Impact

**1.1 GxP determination.** Propose from the URS intended use + GXP-ASSESS (if present): `gxp-relevant` / `non-gxp` / `indirect-gxp`. Confirm. Criterion: the system creates/modifies/stores/transmits records under a GxP predicate rule, or controls a process impacting PS/PQ/DI.

**1.2 System impact (PS / PQ / DI).** For each axis (Patient Safety, Product Quality, Data Integrity), propose an H/M/L with a one-line justification **rooted in the business process**, then confirm. Derive the overall `system_impact` (high if any axis is H on a safety/quality-critical process). Present as:
```
Proposed system impact (reply to confirm or adjust each):
PS (Patient Safety): [H/M/L] — [reason]
PQ (Product Quality): [H/M/L] — [reason]
DI (Data Integrity):  [H/M/L] — [reason]
Overall system_impact: [high/medium/low]
Reply with any corrections, or "confirm all".
```

**1.3 GAMP category decision (critical output).** Propose a category from GAMP 5 §M4 + the system's nature, with rationale:
- **Cat 1** — infrastructure (OS/DB/middleware); qualified, not validated.
- **Cat 3** — standard product used out-of-the-box (no meaningful configuration).
- **Cat 4** — configured product (LIMS/SCADA/ERP/CDS/EDMS/BMS/configurable spreadsheets).
- **Cat 5** — custom/bespoke code.

If the manifest already declares `gamp_category`, treat it as the proposal and confirm the rationale. Present:
```
Proposed GAMP category: Cat [N] — [rationale]
Reply:
1 — Confirm Cat [N]
2 — Override to Cat 1
3 — Override to Cat 3
4 — Override to Cat 4
5 — Override to Cat 5
6 — Needs more context ([question])
```
Capture `gamp_category_rationale` (non-empty — validation requires it).

**1.4 Part 11 / Annex 11 applicability (the five questions).** Ask each question sequentially; each "Yes" activates a URS preset:

| Question | Yes → preset |
|---|---|
| GxP electronic records as primary source? | URS-EREC |
| Electronic signatures (not scanned)? | URS-ESIG |
| Cloud/SaaS or remote access? | URS-SEC (encryption + MFA) |
| Interfaces transferring GxP data? | URS-API |
| Migrate legacy data? | URS-MIGR |

Set `part11_applicable` true if either of the first two is Yes. **Cross-check against the URS**: the answers must match the presets the URS activated; flag any mismatch.

### Step 2 — Identify Functions with Impact

Parse `specs/URS.md` for every `URS-<CATEGORY>-NNN` with `GxP=Y`. For each, classify impact on PS / PQ / DI (H/M/L per axis) and mark GxP-critical (Yes/No). Non-GxP functions (e.g. browser compatibility) are marked No and fall outside formal risk analysis. Produce the Step 2 table. Do **not** invent requirements not in the URS.

### Risk register — `RA-INIT-NNN`

For each GxP-critical function (and any system-level risks), create one `RA-INIT-NNN` row. Propose each row's ratings with reasoning and confirm/adjust before writing; mark `[NEEDS CLARIFICATION: …]` where a factor cannot be assessed.

Row columns: `RA-ID | Assesses (URS-ID) | Risk (potential failure) | Severity | Probability | Risk Class | Detectability | Risk Priority | Initial control | Proceed to RA-DET?`

1. **Risk** — name the potential failure (what goes wrong and its GxP consequence).
2. **Severity** — from the business process (§1.2 axes). H/M/L. **Not inflated by GAMP category.**
3. **Probability** — scales with the GAMP category. H/M/L.
4. **Risk Class** = Severity × Probability — use the matrix in `templates/csv/RA-INIT.md` §3.1 (do not improvise):

   | Sev ↓ \ Prob → | L | M | H |
   |---|---|---|---|
   | **H** | M | H | H |
   | **M** | L | M | H |
   | **L** | L | L | M |

5. **Detectability** — H (easy to detect) / M / L (hard to detect).
6. **Risk Priority** = Risk Class × Detectability — use §3.2 (low detectability raises priority):

   | Class ↓ \ Detect → | H | M | L |
   |---|---|---|---|
   | **H** | M | H | H |
   | **M** | L | M | H |
   | **L** | L | L | M |

7. **Initial control** — the existing/planned control (often a URS requirement; cite its ID).
8. **Proceed to RA-DET?** — Yes if Risk Priority = H.

### RA-DET decision

`detailed_ra_required` is typically **true** if any trigger is present:
- `system_impact == high`
- `gamp_category in [4, 5]`
- ≥1 function with Risk Priority = H

If `false`, justify explicitly (e.g. simple Cat 3, low impact, GEP + supplier evidence sufficient). Record the final decision + justification.

**Stop criteria — complete enough to write:**
- [ ] `gamp_category_decision` assigned with non-empty rationale
- [ ] GxP determination + system impact (PS/PQ/DI) complete
- [ ] Part 11/Annex 11 applicability decided (5 questions), cross-checked vs URS presets
- [ ] If `gxp-relevant`: Step 2 functions table has ≥1 row
- [ ] Risk register: each GxP-critical function has Risk Class + Risk Priority (or a clarification marker)
- [ ] RA-DET decision taken with justification
- [ ] Signatures: ≥1 author + Process Owner designated (owner of severity) — markers OK in draft

## Anti-hallucination rules (NON-NEGOTIABLE — also enforced via AGENTS.md)

1. **Never invent a GAMP category.** Propose one from the §M4 criteria + the system's nature, state the rationale, and have the user confirm. If genuinely unclear, insert `[NEEDS CLARIFICATION: Cat 3, 4 or 5? — depends on whether the product is configured or bespoke]`.
2. **Never invent risk ratings.** Severity, Probability, Detectability must each be reasoned, not guessed. When the user cannot supply the information needed to rate a factor, insert `[NEEDS CLARIFICATION: …]` — do not fabricate an H/M/L.
3. **Never invent regulatory citations.** Use only the citations the source template carries (GAMP 5 §5.3 / §M3 / §M4, ICH Q9, EU Annex 11 §4). Do not attach new §-numbers.
4. **Only cite URS-IDs that exist.** Each `RA-INIT-NNN` cites a real `URS-<CAT>-NNN` from `specs/URS.md`, or the literal `system-level` for system-level risks. Never reference a URS-ID that is not in the URS.
5. **Number `RA-INIT-NNN` sequentially** from `001`; never reuse or skip.
6. **Severity derives from the business process, NOT the GAMP category.** A Cat 3 system controlling a critical process can have Severity H. Do not inflate severity because it is Cat 5 (GAMP 5 §M3).
7. **Probability scales with the GAMP category** (Cat 1 → 5). This is the axis the category affects.
8. **`[NEEDS CLARIFICATION: …]` always carries the actual question after the colon.**
9. **Honor the `language` field** of the manifest.

## Status semantics

Output starts at `status: draft`. Instance frontmatter:

```yaml
---
title: "RA-INIT — Initial Risk Assessment for {{system_name}}"
type: instance
based_on_template: "RA-INIT"
based_on_template_version: "0.1.0"
project_id: "{{project_id}}"
system_id: "{{system_id}}"
traces_to: "specs/URS.md ({{urs_version}}, {{urs_status}})"
gamp_category: {{1|3|4|5}}
status: draft
version: "0.1"
created: "{{today}}"
updated: "{{today}}"
language: "{{language from .gxp-dev.yaml}}"
detailed_ra_ref: "specs/RA-DET.md (planned)"   # ONLY if detailed_ra_required: true
profile: "{{profile}}"
mode: "{{mode}}"
part11_applicable: {{bool}}
---
```

`detailed_ra_ref` is conditional: include only when `detailed_ra_required: true`. **Never** set `status: in-review` or `status: approved`.

> **Approval order:** RA-INIT must reach `approved` **before** the URS, because the URS inherits `gamp_category` from here. Never set `status: approved` yourself — that requires human signatures (Process Owner = owner of severity).

## Output shape

Mirror `templates/csv/RA-INIT.md` body section order:

- **§0. Identification and signatures** — system table (name, identifier, URS assessed with version/status, GxP business process, determined GAMP category); signature table (Author, Reviewer 1 = Process Owner (owner of severity), Reviewer 2 = SME, Approver 1 = System Owner, Approver 2 = Quality Unit). Unknown signatories → `[NEEDS CLARIFICATION: assign <role>]`. Keep the approval-order warning (RA-INIT approved before URS).
- **§1. Objective** — one paragraph: performs Step 1 + Step 2 of the GAMP 5 five-step QRM; steps 3-5 live in RA-DET + operation.
- **§3. Methodology** — brief: qualitative H/M/L, Class = Severity × Probability, Priority = Class × Detectability, matrices per the template §3.1-3.2 (reference, do not re-paste).
- **§4. System context and boundary** — `system_boundary` (what's inside/outside) + `business_process` (origin of severity).
- **§5. Step 1** — 5.1 GxP determination; 5.2 PS/PQ/DI table with H/M/L + justification per axis + overall `system_impact`; 5.3 GAMP category decision + rationale + §M4 criteria table; 5.4 five-question Part 11/Annex 11 table with preset consequences + consistency note vs URS.
- **§6. Step 2 — functions with impact** — table: `URS-ID | Function | Impacts PS | Impacts PQ | Impacts DI | GxP-critical?`. One row per GxP=Y URS requirement (plus clearly non-GxP ones marked No). Only real URS-IDs.
- **§7. Initial Risk Register** — the 10-column table; `RA-INIT-NNN` sequential from 001; `Assesses` = real `URS-<CAT>-NNN` or `system-level`; ratings consistent with §3.1/§3.2 matrices; bold line listing Priority = H functions that proceed to RA-DET.
- **§8. RA-DET decision** — `detailed_ra_required` (true/false) + trigger table + final decision & justification.
- **§9. Related documents** — URS assessed, GXP-ASSESS, RA-DET (if required), VP.
- **§10. Revision history** — `| 0.1 | <today> | Initial draft (RA-INIT) — <author>, <dept> |`

## Propagation (after writing)

The category and Part 11 applicability decided here are inputs to other specs:
- Propagate `gamp_category_decision` → the `{{gamp_category}}` of `specs/URS.md` and (later) `specs/FS.md`. If the URS already declares a different category, **flag the discrepancy** to the user; do not silently overwrite.
- Propagate the §5.4 applicability → the URS `preset_part11_active` and the EREC/ESIG/SEC/API/MIGR preset activation. Flag any inconsistency with the URS.

## Post-flight — call the shared Python core

From the consumer project root (substitute `<gdd-path>` with your `gxp-driven-dev` install):

```bash
python <gdd-path>/skills/_scripts/validate-frontmatter.py specs/RA-INIT.md
python <gdd-path>/skills/_scripts/check-clarification-markers.py specs/RA-INIT.md --draft
python <gdd-path>/skills/_scripts/generate-rtm.py --specs-dir specs
```

If `validate-frontmatter.py` fails, report the errors and do **not** claim success. Then print a summary:
- Determined GAMP category + rationale
- Count of GxP-critical functions (Step 2)
- Count of `RA-INIT-NNN` by Risk Priority (H/M/L)
- RA-DET decision (true/false) + triggers
- Count of clarification markers

Suggest next step:
- `detailed_ra_required: true` → `/gdd-ra-detail-from-urs-fs` (after the FS is drafted) for the high-priority functions.
- Always → `/gdd-fs-from-urs` to draft the FS (the category now scales its depth).
- Markers > 0 → resolve before promoting RA-INIT to `in-review`.

## When to refuse

- `.gxp-dev.yaml` missing → redirect to `/gdd-init`.
- `specs/URS.md` missing → redirect to `/gdd-urs-from-idea`.
- User asks to "just assign a category" without rationale → refuse; the category requires §M4 justification.
- User asks to fabricate risk ratings to "pass" → refuse; cite anti-hallucination policy.
- Bypassing a phase required by `rigor_level: strict`/`regulated` → refuse and explain.
