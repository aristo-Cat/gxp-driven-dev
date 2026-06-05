# `gdd.ra.from-urs` — Generation Flow

Detailed step order, the risk matrices, stop criteria, and interaction principles for the RA-INIT instantiation skill. Referenced from `SKILL.md`.

---

## Conventions

- Work through the steps **in order**; lock each before the next. The category decision (Step 1.3) gates everything downstream.
- After each step, do a 1-line **confirmation echo** ("Category locked: Cat 4 — configured COTS").
- If the user cannot supply what a rating needs → insert `[NEEDS CLARIFICATION: …]`; never fabricate an H/M/L.

### Interaction principles (adopted from `bm-prd-creator` — see `docs/inspirations.md` Framework 5)

1. **Propose a default with reasoning, then ask to confirm or change.** Never ask open-ended. For risk work this is doubly important: propose a Severity/Probability/Detectability with the *why*, and let the user correct. A **confirmed proposal is grounded**; an **unconfirmed rating you write into the register is invention** (anti-hallucination rule #2). Example — *"For 'excursion not alarmed' I'd rate Severity H (undetected bad storage → product/patient impact), Probability M (Cat 4 configured), Detectability L (a silent alarm failure is hard to notice) → Risk Priority H. Agree, or adjust?"*
2. **Use `AskUserQuestion` for discrete choices** (GAMP category 1/3/4/5; H/M/L ratings; yes/no Part 11 questions; proceed-to-RA-DET). Free text only for rationale/justification.
3. **One decision (or tight cluster) at a time, in sequence.** Don't batch the whole risk register into one prompt.
4. **Adapt depth to rigor + impact.** `rigor_level: light` / low impact → compress (assess only the clearly GxP-critical functions). `regulated` / high impact → assess every GxP=Y function.

---

## Step 1 — Initial Risk Assessment + System Impact

### 1.1 GxP determination
Propose from the URS intended use + GXP-ASSESS (if present): `gxp-relevant` / `non-gxp` / `indirect-gxp`. Confirm. Criterion: the system creates/modifies/stores/transmits records under a GxP predicate rule, or controls a process impacting PS/PQ/DI.

### 1.2 System impact (PS / PQ / DI)
For each axis (Patient Safety, Product Quality, Data Integrity), propose an H/M/L with a one-line justification **rooted in the business process**, then confirm. Derive the overall `system_impact` (high if any axis is H on a safety/quality-critical process).

### 1.3 GAMP category decision (critical output)
Propose a category from GAMP 5 §M4 + the system's nature, with rationale:
- **Cat 1** — infrastructure (OS/DB/middleware); qualified, not validated.
- **Cat 3** — standard product used out-of-the-box (no meaningful configuration).
- **Cat 4** — configured product (LIMS/SCADA/ERP/CDS/EDMS/BMS/configurable spreadsheets).
- **Cat 5** — custom/bespoke code.

Use `AskUserQuestion` to confirm/override. If the manifest already declares `gamp_category`, treat it as the proposal and confirm the rationale. Capture `gamp_category_rationale` (non-empty — validation requires it).

### 1.4 Part 11 / Annex 11 applicability (the five questions)
Ask the 5 questions from RA-INIT §5.4; each Yes activates a URS preset:

| Question | Yes → preset |
|---|---|
| GxP electronic records as primary source? | URS-EREC |
| Electronic signatures (not scanned)? | URS-ESIG |
| Cloud/SaaS or remote access? | URS-SEC (encryption + MFA) |
| Interfaces transferring GxP data? | URS-API |
| Migrate legacy data? | URS-MIGR |

Set `part11_applicable` true if either of the first two is Yes. **Cross-check against the URS**: the answers must match the presets the URS activated; flag any mismatch.

---

## Step 2 — Identify Functions with Impact

Parse `specs/URS.md` for every `URS-<CATEGORY>-NNN` with `GxP=Y`. For each, classify impact on PS / PQ / DI (H/M/L per axis) and mark GxP-critical (Yes/No). Non-GxP functions (e.g. browser compatibility) are marked No and fall outside formal risk analysis. Produce the Step 2 table. Do **not** invent requirements not in the URS.

---

## Risk register — `RA-INIT-NNN`

For each GxP-critical function (and any system-level risks), create one `RA-INIT-NNN` row:

1. **Risk** — name the potential failure (what goes wrong and its GxP consequence).
2. **Severity** — from the business process (§1.2 axes). H/M/L.
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

Apply the interaction principles: propose each row's ratings with reasoning, confirm/adjust. Mark `[NEEDS CLARIFICATION: …]` where a factor cannot be assessed.

---

## RA-DET decision

`detailed_ra_required` is typically **true** if any trigger is present:
- `system_impact == high`
- `gamp_category in [4, 5]`
- ≥1 function with Risk Priority = H

If `false`, justify explicitly (e.g. simple Cat 3, low impact, GEP + supplier evidence sufficient). Record the final decision + justification.

---

## Stop criteria ("complete enough to write")

- [ ] `gamp_category_decision` assigned with non-empty rationale
- [ ] GxP determination + system impact (PS/PQ/DI) complete
- [ ] Part 11/Annex 11 applicability decided (5 questions), cross-checked vs URS presets
- [ ] If `gxp-relevant`: Step 2 functions table has ≥1 row
- [ ] Risk register: each GxP-critical function has Risk Class + Risk Priority (or a clarification marker)
- [ ] RA-DET decision taken with justification
- [ ] Signatures: ≥1 author + Process Owner designated (owner of severity) — markers OK in draft

---

## What to do at the end

1. Write `specs/RA-INIT.md` (`status: draft`) per `output-template.md`.
2. Run the post-flight scripts (see `SKILL.md`).
3. Print the determined category, GxP-critical function count, `RA-INIT-NNN` count by priority, RA-DET decision, marker count.
4. **Propagate**: update `{{gamp_category}}` and `preset_part11_active` in `specs/URS.md` (flag discrepancies, do not silently overwrite).
5. Never claim the RA-INIT is "approved" — that requires human signatures, and it must be approved before the URS.
