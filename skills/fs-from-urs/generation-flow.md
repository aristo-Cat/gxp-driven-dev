# `gdd.fs.from-urs` — Generation Flow

Detailed step order, cardinality rules, the coverage gate, stop criteria, and interaction principles for the FS instantiation skill. Referenced from `SKILL.md`.

---

## Conventions

- Work **category by category** through the URS; lock each before the next.
- After each category, echo coverage ("FUNC: 5/5 URS GxP=Y realized").
- If the realization is not yet known → `[NEEDS CLARIFICATION: …]`; never fabricate a mechanism.

### Interaction principles (adopted from `bm-prd-creator` — see `docs/inspirations.md` Framework 5)

1. **Propose a realization with reasoning, then ask to confirm or change.** For each URS-ID, propose the technical HOW with the *why*, and let the user correct. A **confirmed realization is grounded**; an **unconfirmed mechanism you write into the FS is invention** (anti-hallucination rule #2). Example — *"`URS-FUNC-003` (excursion alarm): I'd realize it as an alarm rule evaluated on ingest + notification to the on-call distribution. Agree, or is there a specific alerting channel?"*
2. **Use `AskUserQuestion` for discrete choices** (cardinality 1:1 vs 1:N; `covers_ds` yes/no; whether a preset is realized or N/A). Free text for the realization wording.
3. **One category (or tight cluster) at a time.** Don't dump the whole FS in one prompt.
4. **Adapt depth to category + risk.** Use RA-INIT: spend the most detail on Risk Priority = H functions. `rigor_level: light` → concise realizations; `regulated` → full detail per GxP=Y.

---

## Flow

### 1. Parse the URS
Extract every `URS-<CATEGORY>-NNN` with its **GxP (Y/N)** and **prio (H/M/L)**. Note which presets are active (URS-EREC/ESIG/SEC/API/MIGR present and not marked N/A). Do not introduce new categories — the FS mirrors the URS's 22 canonical codes.

### 2. Realize each URS requirement
For each `URS-<CATEGORY>-NNN`:
- **GxP=Y** → produce ≥1 `FS-<CATEGORY>-NNN` (same category), citing the URS-ID in the **Realizes** column, with a **Realization (how)** describing the technical mechanism (Cat-aware: configured COTS feature for Cat 4; software/design for Cat 5).
- **GxP=N** → an FS row is optional (1:0 permitted).
- **Cardinality**: 1:1 by default; 1:N when one requirement needs several realizations (e.g. a Part 11 control touching audit trail + access control + reporting). 1:0 **only** for GxP=N.
- **Inherit** GxP and prio from the URS — never re-evaluate.

### 3. Realize inherited presets
The FS does **not** re-decide Part 11/Annex 11 applicability — it inherits the URS decision and **realizes** it:
- URS-EREC active → `FS-EREC-NNN` for each (technical mechanism per control).
- URS-ESIG active → `FS-ESIG-NNN` for each. Keep N/A preset rows (e.g. a hybrid-signature requirement marked N/A) **as a row** for traceability, with the realization "N/A — <reason>".
- URS-SEC-001/002 → `FS-SEC` (encryption + MFA). URS-API-001 → `FS-API` (validated interfaces). URS-MIGR-001 → `FS-MIGR` (validated migration) — skip only if the URS marked MIGR N/A.

### 4. Deviations to URS (§4.2)
Record any change that arose between URS approval and FS creation, traced to the affected URS-ID. Empty only if there were no changes (set `deviations_logged: false`).

### 5. Coverage summary (§4.5)
Render §4.5 as a **per-category coverage summary** (category | # URS GxP=Y | # FS entries | coverage), **not** a per-ID matrix — the per-ID traces live in the section 5–11 tables and are the RTM source. State "Blocking gaps: none" only after the coverage check passes. *(Lesson from the FS smoke test: a per-ID 4.5 matrix is unwieldy for preset-heavy systems with 30+ EREC/ESIG rows.)*

---

## Coverage gate (the core check)

Before claiming the FS complete, verify: **the set of URS-IDs with GxP=Y is a subset of the URS-IDs cited in the FS "Realizes" columns.** Any GxP=Y URS-ID not realized is a gap; any prio=H gap is **blocking**. The deterministic way: regex the URS for IDs followed by `| Y |`, regex the FS for cited URS-IDs, and diff. (A future `gdd.trace.validate` script will own this; until then, run it in post-flight.)

---

## Stop criteria ("complete enough to write")

- [ ] `traces_to` points to the URS instance (warn if not `approved`)
- [ ] Every `URS-<CAT>-NNN` with GxP=Y has ≥1 `FS-<CAT>-NNN` (full coverage)
- [ ] 0 blocking gaps (no prio=H URS without realization)
- [ ] Each FS row cites its URS-ID in "Realizes"; the Realization describes HOW, not the WHAT
- [ ] If URS-EREC/ESIG active → sections 9.2/9.3 non-empty
- [ ] §4.2 (Deviations to URS) present (empty only if no changes)
- [ ] Signature block with ≥1 author + reviewers (incl. Data Owner) + approvers — markers OK in draft

---

## What to do at the end

1. Write `specs/FS.md` (`status: draft`) per `output-template.md`.
2. Run post-flight (see `SKILL.md`): validate-frontmatter, markers `--draft`, generate-rtm, **coverage check**.
3. Print FS-ID count, coverage %, blocking H gaps (0), marker count.
4. Suggest next: `/gdd.cs.from-fs` (Cat 4) and/or `/gdd.ra.detail.from-urs-fs`, then `/gdd.tests.from-ra`.
5. Never claim the FS is "approved" — it realizes an approved URS and needs its own human signatures.
