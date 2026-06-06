---
description: "Detailed Risk Assessment / FMEA (RA-DET) from RA-INIT + URS + FS. Implements GAMP 5 §M3 step 3. Takes the high-Risk-Priority functions from RA-INIT and runs a detailed FMEA: Occurrence × Relevance × Detection → RPN (1-3 scale, range 1-27), double evaluation (before/after mitigation), target RPN ≤ 4, and the RPN→test-rigor bridge to OQ/PQ. Anti-hallucination: never invents risk ratings; uses `[NEEDS CLARIFICATION: …]` when a factor cannot be assessed. Output: `specs/RA-DET.md`."
argument-hint: "[nothing needed — the skill reads specs/RA-INIT.md, specs/URS.md, and specs/FS.md from the working directory]"
---

# gdd.ra.detail.from-urs-fs — Detailed Risk Assessment / FMEA (Codex prompt)

> **Codex invocation.** Place this file under your Codex prompts/skills directory so it is exposed as the slash command **`/gdd-ra-detail-from-urs-fs`** (Codex derives the command name from the filename). No `$ARGUMENTS` are needed — the skill reads its inputs from `specs/RA-INIT.md`, `specs/URS.md`, and `specs/FS.md` already present in the working directory.
>
> **Two-part port.** This prompt carries the *procedure*. The *always-on guardrails* (anti-hallucination, anonymization, "never set status: approved", "read manifest first") live in `../AGENTS.snippet.md`, which the consumer pastes into their project `AGENTS.md` so they hold even when this prompt is not the active turn. See `../PORTING.md`.
>
> **Shared core.** The deterministic work — frontmatter validation, RTM generation, clarification-marker scan, anti-leak guard, arithmetic check — is done by the harness-agnostic Python in `skills/_scripts/`, invoked by path. Do **not** re-implement it here. Source of truth: `skills/ra-detail-from-urs-fs/SKILL.md` + `generation-flow.md` + `output-template.md`.
>
> **No AskUserQuestion.** Codex has no `AskUserQuestion` tool. Wherever the source skill poses a discrete choice (O/R/D ratings, residual-risk acceptance, replace/append/abort), present it as an explicit enumerated prompt (e.g. "Reply 1 to replace / 2 to append / 3 to abort") and wait for the user's reply before proceeding.

You are producing a **RA-DET instance** (`specs/RA-DET.md`) — the detailed FMEA of GAMP 5 §M3 **step 3** — that deepens the high-risk functions identified in RA-INIT and **scales the testing rigor** of OQ/PQ. Follow `templates/csv/RA-DET.md`.

## Pre-flight (do this FIRST, before any generation)

1. **Locate `.gxp-dev.yaml`** by walking up from the working directory. If absent, **STOP**: *"This project has no `.gxp-dev.yaml` manifest. Run the init step first, then re-invoke `/gdd-ra-detail-from-urs-fs`."*
2. **Load the manifest**: `gamp_category` (RA-DET is for GAMP Cat 4/5; for simple Cat 3 say so and suggest closing with RA-INIT alone), `rigor_level`, `language`.
3. **Locate `specs/RA-INIT.md`** — **required**; it is the source of the high-Risk-Priority functions. If missing → **STOP**: *"Run `/gdd-ra-from-urs` first to produce the initial risk assessment, then re-invoke `/gdd-ra-detail-from-urs-fs`."* Warn if its status is not `approved` (canonically RA-DET traces to an approved RA-INIT) using: *"WARNING: specs/RA-INIT.md status is not approved — RA-DET should trace to an approved RA-INIT for a complete audit trail."*
4. **Locate `specs/URS.md`** (required) and `specs/FS.md` (recommended). If `specs/URS.md` is missing, **STOP** and redirect to `/gdd-urs-from-idea`. If `specs/FS.md` is missing, warn and proceed with URS only.
5. **Read the source template** `templates/csv/RA-DET.md` — authoritative for the FMEA scales (§3.1), the RPN→rigor table (§3.2), and the double-evaluation method. Read it; do not write it.
6. **Check if `specs/RA-DET.md` already exists.** If it does, present: *"specs/RA-DET.md already exists. Reply 1 to replace / 2 to append / 3 to abort."* Wait for the user's reply before continuing.

## Generation flow

Work **one high-risk function at a time** — the RA-INIT Priority-H set only. Lock each FMEA row before the next. After each row, echo the result (e.g. *"RA-DET-001: RPN₁ 18 → RPN₂ 3, mitigated"*).

| Step | Produces |
|---|---|
| Parse RA-INIT | the functions with **Risk Priority = H** (only these get a detailed FMEA) |
| FMEA §4 | ≥1 `RA-DET-NNN` per high-risk function: failure / cause / consequence (PS/PQ/DI) / existing controls / O₁ R₁ D₁ RPN₁ / mitigation / O₂ R₂ D₂ RPN₂ |
| Residual §5 | any RPN₂ > 4 with documented acceptance |
| Summary §6 | RPN distribution + OQ/PQ test-rigor link |

### Interaction principles

1. **Propose each rating with reasoning, then confirm.** For each O/R/D, state the *why* (cause, control, process severity) before asking. A confirmed rating is grounded; an unconfirmed number you write in is invention (anti-hallucination rule #1). Example: *"For sensor drift: O₁=2 (drift happens over time), R₁=3 (wrong release decision — critical), D₁=3 (silent between calibrations) → RPN₁=18. Agree?"*
2. **Offer discrete choices as an explicit enumerated prompt** for the 1-3 ratings (e.g. "Reply 1 / 2 / 3") and yes/no decisions (residual-risk acceptance). Free text for failure/cause/mitigation descriptions.
3. **One function (FMEA row) at a time.** Do not batch the whole register.
4. **Adapt depth to RPN.** Spend the most analysis on RPN₁ 12-27 functions; these drive negative/stress testing.

### Step 1 — Parse the high-risk functions

From `specs/RA-INIT.md`, extract every `RA-INIT-NNN` with **Risk Priority = H** and the `URS-<CAT>-NNN` it assesses. Pull the matching `FS-<CAT>-NNN` realization from `specs/FS.md` (the technical "how" enables function-level failure analysis). If RA-INIT has zero Priority-H functions and `system_impact` is not high, note that RA-DET may not be required and ask the user whether to proceed.

### Step 2 — FMEA per function (§4)

For each high-risk function, create ≥1 `RA-DET-NNN` with all columns:
- **Analyzes** — the `URS-<CAT>-NNN` / `FS-<CAT>-NNN`.
- **Details** — the `RA-INIT-NNN` it deepens.
- **Potential failure / Cause / Consequence (PS/PQ/DI)** — the failure mode.
- **Existing controls** — what the FS already provides (cite FS-IDs).
- **O₁ / R₁ / D₁ / RPN₁** — evaluation 1 (before mitigation). RPN₁ = O₁×R₁×D₁.
- **Mitigation measures** — ordered by preference: eliminate-by-design > reduce occurrence > increase detection > procedural control. Include the OQ/PQ test that will verify it.
- **O₂ / R₂ / D₂ / RPN₂** — evaluation 2 (after mitigation). **R₂ = R₁** (severity not mitigable). RPN₂ = O₂×R₂×D₂.

### FMEA scales (from `templates/csv/RA-DET.md` §3.1)

| Value | Occurrence (O) | Relevance (R) | Detection (D) |
|---|---|---|---|
| **1** | Unlikely | Minor impact on PS/PQ/DI | Easy to detect (automatic control) |
| **2** | Possible | Moderate impact | Detectable with effort (manual control) |
| **3** | Probable | Critical impact on PS/PQ/DI | Difficult to detect (no control) |

**RPN → test rigor**: 1-4 GEP / 6-9 positive / 12-27 positive + negative + stress.

### Step 3 — Residual risk (§5)

Any RPN₂ > 4 goes to §5 with: residual RPN, justification, accepted-by (Process Owner + Quality Unit), date. If acceptance is not yet assigned, use `[NEEDS CLARIFICATION: residual risk acceptance by Process Owner + QU]`. If no residual > 4, state *"No residual risks above the RPN ≤ 4 target."*

### Step 4 — Summary and test link (§6)

Fill the metrics table (total analyzed / # high RPN₁ 12-27 / # mitigated ≤4 / # residual >4) and the **OQ/PQ link**: list which functions need positive / negative / stress testing by RPN band. This is the bridge that `/gdd-tests-from-ra` consumes.

## Scope discipline (CORE)

**Analyze ONLY the functions RA-INIT flagged Risk Priority = H.** RA-DET deepens; it does not re-analyze the whole system. Re-running risk on low-priority functions is waste and dilutes the audit story.

## Anti-hallucination rules (NON-NEGOTIABLE — also enforced via AGENTS.md)

1. **Never invent risk ratings.** Each O/R/D must be reasoned (cause, control, process). When a factor cannot be assessed, insert `[NEEDS CLARIFICATION: …]`; do not guess a number.
2. **Verify the arithmetic**: RPN must equal O × R × D for both evaluations. All factors must be in the range 1-3.
3. **Never invent citations.** Only cite §-references already in the template (GAMP 5 §M3 / §5 / §11.5.4, ICH Q9, EU Annex 11 §4).
4. **Cite real IDs.** Each `RA-DET-NNN` cites the `URS-/FS-<CAT>-NNN` analyzed **and** the `RA-INIT-NNN` it details.
5. **Number `RA-DET-NNN` sequentially** from 001.
6. **Honor `language`** from the manifest; do not mix languages within the spec.
7. **Severity invariant**: Relevance (R) is process-driven and **never reduced across mitigation** — R₂ = R₁ for every row. Controls cannot lower severity; only Occurrence and Detection improve.

## Status semantics

Output `status: draft`. Instance frontmatter:

```yaml
---
title: "RA-DET — Detailed Risk Assessment (FMEA) for {{system_name}}"
type: instance
based_on_template: "RA-DET"
based_on_template_version: "0.1.0"
project_id: "{{project_id}}"
system_id: "{{system_id}}"
traces_to: "specs/RA-INIT.md ({{ver}}, {{status}}) + specs/URS.md (...) + specs/FS.md (...)"
gamp_category: {{4|5}}
status: draft
version: "0.1"
created: "{{today}}"
updated: "{{today}}"
language: "{{language from .gxp-dev.yaml}}"
residual_risk_accepted_by: "{{accepter or 'pending — see §5'}}"   # only if §5 has residual risk
profile: "{{profile}}"
mode: "{{mode}}"
---
```

**Never** set `status: in-review` or `status: approved`.

## Output shape

Mirror `templates/csv/RA-DET.md`. Sections in order:

- **§0 Identification and signatures**: system table (name, identifier, RA-INIT that triggers it, URS analyzed, FS analyzed, GAMP category, scope of analysis = the RA-INIT Priority-H functions). Signatures: Author (SME/CSV), Reviewer = Process Owner *(owner of Relevance)*, Approver 1 = System Owner, Approver 2 = Quality Unit. Unknown → `[NEEDS CLARIFICATION: assign <role>]`. If RA-INIT/URS/FS are still draft, add a `> [!warning]` cascade-order note.
- **§1 Objective**: one paragraph — detailed FMEA of the high-risk functions from RA-INIT; Step 3 of the QRM process (GAMP 5 §M3).
- **§3 FMEA methodology**: brief description — `RPN = O × R × D` (1-3 each, 1-27 range); R = process severity held constant; double evaluation; target RPN₂ ≤ 4; RPN→rigor 1-4/6-9/12-27. (Reference the template scales; do not re-paste the full tables.)
- **§4 Risk Analysis (FMEA)**: the 16-column table exactly as the template: `RA-DET-ID | Analyzes (URS/FS-ID) | Details (RA-INIT) | Potential failure | Cause | Consequence (PS/PQ/DI) | Existing controls | O₁ | R₁ | D₁ | RPN₁ | Mitigation measures | O₂ | R₂ | D₂ | RPN₂`. After the table, a one-line note reaffirming R is held constant.
- **§5 Residual risk**: table for every RPN₂ > 4; `[NEEDS CLARIFICATION: …]` if acceptance not yet assigned.
- **§6 Summary and link to testing**: metrics table + the OQ/PQ test-rigor link per function.
- **§7 Related documents**: RA-INIT, URS, FS, OQ, PQ, VR.
- **§8 Revision history**: `| 0.1 | <today> | Initial draft (RA-DET) — <author>, <dept> |`

## Post-flight — call the shared Python core

From the consumer project root (substitute `<gdd-path>` with your `gxp-driven-dev` install):

```bash
python <gdd-path>/skills/_scripts/validate-frontmatter.py specs/RA-DET.md
python <gdd-path>/skills/_scripts/check-clarification-markers.py specs/RA-DET.md --draft
python <gdd-path>/skills/_scripts/generate-rtm.py --specs-dir specs
```

Additionally, verify **FMEA arithmetic** for every row: RPN₁ = O₁×R₁×D₁ and RPN₂ = O₂×R₂×D₂; all factors in 1-3; R₂ = R₁.

If `validate-frontmatter.py` fails, report the errors and do **not** claim success. Then print a summary:
- Number of functions analyzed
- RPN₁ distribution (bands: 1-4 / 6-9 / 12-27)
- Number mitigated to RPN₂ ≤ 4
- Number of residual risks > 4
- List of functions requiring negative/stress testing (RPN ≥ 12) — this is the bridge for `/gdd-tests-from-ra`
- Next step: `/gdd-tests-from-ra` (IQ/OQ/PQ — the RPN scales the test rigor)

## When to refuse

- `.gxp-dev.yaml` missing → redirect to the init step (`/gdd-init`).
- `specs/RA-INIT.md` missing → redirect to `/gdd-ra-from-urs`.
- GAMP category is 3 or lower → note that RA-DET is typically not required; offer to produce a closing note or confirm Cat 3 justification instead.
- User asks to analyze low-priority (non-H) functions in detail → decline; RA-DET is for the RA-INIT Priority-H set only.
- User asks to reduce Relevance (R) via a control → refuse; severity is process-driven and not mitigable.
- User asks to fabricate an RPN to "pass" a target → refuse; cite anti-hallucination policy.
- User asks to set `status: approved` directly → refuse; approval requires Process Owner + Quality Unit signatures outside this skill.
