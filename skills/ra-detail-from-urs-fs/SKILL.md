---
name: gdd.ra.detail.from-urs-fs
description: |
  Detailed Risk Assessment / FMEA (RA-DET) from RA-INIT + URS + FS. Implements
  GAMP 5 §M3 step 3. Takes the high-Risk-Priority functions from RA-INIT and runs
  a detailed FMEA: Occurrence × Relevance × Detection → RPN (1-3 scale, range
  1-27), double evaluation (before/after mitigation), target RPN ≤ 4, and the
  RPN→test-rigor bridge to OQ/PQ. Anti-hallucination: never invents risk ratings;
  uses `[NEEDS CLARIFICATION: …]` when a factor cannot be assessed. Output:
  `specs/RA-DET.md`.
  Use this skill when:
  - An approved `specs/RA-INIT.md` exists with ≥1 function at Risk Priority = H
  - The URS (and ideally FS) are available to analyze failure at function level
  - The GAMP category is 4 or 5 (Cat 3 is usually closed with RA-INIT alone)
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# `gdd.ra.detail.from-urs-fs` — Detailed Risk Assessment (FMEA)

You produce a **RA-DET instance** (`specs/RA-DET.md`) — the detailed FMEA of GAMP 5 §M3 **step 3** — that deepens the high-risk functions identified in RA-INIT and **scales the testing rigor** of OQ/PQ. Follow `templates/csv/RA-DET.md`.

## Pre-flight (do this FIRST)

1. **Locate `.gxp-dev.yaml`**: walk up from cwd. If missing → `/gdd.init`.
2. **Load the manifest**: `gamp_category` (RA-DET is for Cat 4/5; for simple Cat 3 say so and suggest closing with RA-INIT), `rigor_level`, `language`.
3. **Locate `specs/RA-INIT.md`** — **required**; it is the source of the high-Risk-Priority functions. If missing → redirect to `/gdd.ra.from-urs`. Warn if its status is not `approved` (canonically RA-DET traces to an approved RA-INIT).
4. **Locate `specs/URS.md`** (required) and `specs/FS.md` (recommended) — the requirements and their realizations enable function-level failure analysis.
5. **Read the source template** `templates/csv/RA-DET.md` — authoritative for the FMEA scales (§3.1), the RPN→rigor table (§3.2), and the double-evaluation method.
6. **Check if `specs/RA-DET.md` already exists**: ask replace / append / abort.

## Generation flow

Follow `generation-flow.md` (this folder). Summary:

| Step | Produces |
|---|---|
| Parse RA-INIT | the functions with **Risk Priority = H** (only these get a detailed FMEA) |
| FMEA §4 | ≥1 `RA-DET-NNN` per high-risk function: failure / cause / consequence (PS/PQ/DI) / existing controls / O₁ R₁ D₁ RPN₁ / mitigation / O₂ R₂ D₂ RPN₂ |
| Residual §5 | any RPN₂ > 4 with documented acceptance |
| Summary §6 | RPN distribution + OQ/PQ test-rigor link |

## Scope discipline (CORE)

**Analyze ONLY the functions RA-INIT flagged Risk Priority = H.** RA-DET deepens; it does not re-analyze the whole system. Re-running risk on low-priority functions is waste and dilutes the audit story. If RA-INIT has zero Priority-H functions and `system_impact` is not high, RA-DET may not be required — say so.

## FMEA method (do not improvise the arithmetic)

- `RPN = Occurrence (O) × Relevance (R) × Detection (D)`, each factor **1-3**, RPN **1-27**. Use the scales in `templates/csv/RA-DET.md` §3.1.
- **Relevance (R) = process severity** — fixed by the GxP business process, **held constant across mitigation** (controls cannot lower severity; only Occurrence and Detection improve). Do not reduce R between eval 1 and eval 2.
- **Occurrence (O)** scales with the GAMP category.
- **Detection (D) is inverted**: high D = hard to detect = worse.
- **Double evaluation**: compute RPN₁ (before) and RPN₂ (after) mitigation — this evidences control effectiveness, not just control existence.
- **Target RPN₂ ≤ 4.** If a risk stays > 4, it goes to §5 (residual risk) with formal acceptance (Process Owner + Quality Unit).
- **RPN → test rigor**: 1-4 GEP / 6-9 positive / 12-27 positive + negative + stress. This is the bridge into OQ/PQ — a high-RPN function without negative testing is a coverage gap.

## Anti-hallucination rules (NON-NEGOTIABLE)

1. **Never invent risk ratings.** Each O/R/D must be reasoned (cause, control, process). When a factor cannot be assessed, insert `[NEEDS CLARIFICATION: …]`; do not guess a number.
2. **Verify the arithmetic**: RPN must equal O × R × D for both evaluations.
3. **Never invent citations.** Only the template's §-refs (GAMP 5 §M3 / §5 / §11.5.4, ICH Q9, EU Annex 11 §4).
4. **Cite real IDs.** Each `RA-DET-NNN` cites the `URS-/FS-<CAT>-NNN` analyzed **and** the `RA-INIT-NNN` it details.
5. **Number `RA-DET-NNN` sequentially** from 001.
6. **Honor `language`.**

## Status semantics

Output `status: draft`. Instance frontmatter per RA-DET's `instance_frontmatter_spec`: `title`, `type: instance`, `based_on_template: "RA-DET"`, `based_on_template_version`, `system_id`, `traces_to` (RA-INIT + URS, ideally approved), `gamp_category`, `status`, `version`, `created`, `updated`, `language`. If §5 has residual risk, set `residual_risk_accepted_by` (or mark pending with a clarification marker). Never `status: approved`.

## Post-flight (after writing `specs/RA-DET.md`)

1. `validate-frontmatter.py specs/RA-DET.md`.
2. `check-clarification-markers.py specs/RA-DET.md --draft`.
3. `generate-rtm.py --specs-dir specs` — regenerate RTM (URS + RA-INIT + FS + RA-DET).
4. **Arithmetic check** — confirm RPN₁ = O₁×R₁×D₁ and RPN₂ = O₂×R₂×D₂ for every row.
5. **Print summary**: # risks, RPN₁ distribution, # mitigated to ≤4, # residual >4, and the list of functions requiring negative/stress testing (RPN ≥ 12).
6. **Suggest next**: `/gdd.tests.from-ra` (IQ/OQ/PQ — the RPN scales the test rigor).

## Output template

See `output-template.md` (this folder) for the exact shape of `specs/RA-DET.md`.

## When to refuse

- `.gxp-dev.yaml` / `specs/RA-INIT.md` missing → redirect (`/gdd.init` / `/gdd.ra.from-urs`).
- User asks to analyze low-priority functions in detail → decline; RA-DET is for the RA-INIT Priority-H set.
- User asks to reduce Relevance via a control → refuse; severity is process-driven and not mitigable.
- User asks to fabricate an RPN to "pass" → refuse; cite anti-hallucination policy.
