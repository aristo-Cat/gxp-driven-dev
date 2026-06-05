# `gdd.ra.detail.from-urs-fs` — Generation Flow

Detailed step order, the FMEA scales, the arithmetic/residual gates, stop criteria, and interaction principles for the RA-DET instantiation skill. Referenced from `SKILL.md`.

---

## Conventions

- Work **one high-risk function at a time** (the RA-INIT Priority-H set); lock each FMEA row before the next.
- After each row, echo the result ("RA-DET-001: RPN₁ 18 → RPN₂ 3, mitigated").
- If a factor cannot be assessed → `[NEEDS CLARIFICATION: …]`; never guess a number.

### Interaction principles (adopted from `bm-prd-creator` — see `docs/inspirations.md` Framework 5)

1. **Propose each rating with reasoning, then confirm.** For each O/R/D, state the *why* (cause, control, process severity) and let the user adjust. A **confirmed rating is grounded**; an **unconfirmed number you write into the FMEA is invention** (anti-hallucination rule #1). Example — *"For sensor drift: O₁=2 (drift happens over time), R₁=3 (wrong release decision — critical), D₁=3 (silent between calibrations) → RPN₁=18. Agree?"*
2. **Use `AskUserQuestion` for the 1-3 ratings** and yes/no decisions (residual-risk acceptance). Free text for failure/cause/mitigation descriptions.
3. **One function (FMEA row) at a time.** Don't batch the whole register.
4. **Adapt depth to RPN.** Spend the most analysis on RPN₁ 12-27 functions; these drive negative/stress testing.

---

## Flow

### 1. Parse the high-risk functions
From `specs/RA-INIT.md`, extract every `RA-INIT-NNN` with **Risk Priority = H** and the `URS-<CAT>-NNN` it assesses. Pull the matching `FS-<CAT>-NNN` realization from `specs/FS.md` (the technical "how" enables function-level failure analysis). Only these functions get a detailed FMEA.

### 2. FMEA per function (§4)
For each high-risk function, create ≥1 `RA-DET-NNN` with all columns:
- **Analyzes** — the `URS-<CAT>-NNN` / `FS-<CAT>-NNN`.
- **Details** — the `RA-INIT-NNN` it deepens.
- **Potential failure / Cause / Consequence (PS/PQ/DI)** — the failure mode.
- **Existing controls** — what the FS already provides (cite FS-IDs).
- **O₁ / R₁ / D₁ / RPN₁** — evaluation 1 (before mitigation). RPN₁ = O₁×R₁×D₁.
- **Mitigation measures** — ordered by preference: eliminate-by-design > reduce occurrence > increase detection > procedural control. Include the OQ/PQ test that will verify it.
- **O₂ / R₂ / D₂ / RPN₂** — evaluation 2 (after mitigation). **R₂ = R₁** (severity not mitigable). RPN₂ = O₂×R₂×D₂.

### 3. FMEA scales (from `templates/csv/RA-DET.md` §3.1)

| Value | Occurrence (O) | Relevance (R) | Detection (D) |
|---|---|---|---|
| **1** | Unlikely | Minor impact on PS/PQ/DI | Easy to detect (automatic control) |
| **2** | Possible | Moderate impact | Detectable with effort (manual control) |
| **3** | Probable | Critical impact on PS/PQ/DI | Difficult to detect (no control) |

### 4. Residual risk (§5)
Any RPN₂ > 4 goes to §5 with: residual RPN, justification, accepted-by (Process Owner + Quality Unit), date. If acceptance is not yet assigned, use `[NEEDS CLARIFICATION: residual risk acceptance by Process Owner + QU]`.

### 5. Summary + test link (§6)
Fill the metrics table (total analyzed, # high RPN₁ 12-27, # mitigated ≤4, # residual >4) and the **OQ/PQ link**: list which functions need positive / negative / stress testing by RPN band. This is the bridge that `gdd.tests.from-ra` consumes.

---

## Gates (run before claiming complete)

- **Arithmetic**: for every row, RPN₁ = O₁×R₁×D₁ and RPN₂ = O₂×R₂×D₂; all factors in 1-3.
- **Severity invariant**: R₂ = R₁ for every row (controls never lower severity).
- **Residual**: every RPN₂ > 4 appears in §5.
- **Traceability**: every row cites a real URS/FS-ID + RA-INIT-NNN.

---

## Stop criteria ("complete enough to write")

- [ ] Every RA-INIT Priority-H function has ≥1 `RA-DET-NNN`
- [ ] Each row has a complete double evaluation with correct RPN arithmetic
- [ ] R held constant across mitigation (R₂ = R₁)
- [ ] Residuals (RPN₂ > 4) documented in §5 with acceptance (or a clarification marker)
- [ ] §6 summary + OQ/PQ test-rigor link complete
- [ ] Author (SME/CSV) + Process Owner designated in signatures — markers OK in draft

---

## What to do at the end

1. Write `specs/RA-DET.md` (`status: draft`) per `output-template.md`.
2. Run post-flight (see `SKILL.md`): validate-frontmatter, markers `--draft`, generate-rtm, **arithmetic check**.
3. Print the RPN distribution + the negative/stress-testing list (RPN ≥ 12).
4. Suggest `/gdd.tests.from-ra` (IQ/OQ/PQ).
5. Never claim the RA-DET is "approved" — it needs Process Owner + QU signatures, and traces to an approved RA-INIT/URS.
