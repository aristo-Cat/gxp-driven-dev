# Smoke-test report — `gdd.urs.from-idea`

**Date:** 2026-05-29
**Skill under test:** `skills/urs-from-idea/` (SKILL.md + interview-flow.md + output-template.md)
**Dummy system:** Temperature Data Logger for GMP Storage Chamber (Cat 4, Part 11 + Annex 11 active, `mode: develop`, `rigor_level: regulated`, `language: es`)
**Method:** The agent acted as the skill, following SKILL.md pre-flight → interview-flow phases 1–11 → output-template → post-flight, with canned interview answers for the dummy. First end-to-end run of the instantiation flow (the project's #1 risk per STATE.md).

---

## Verdict: ✅ PASS

The flow is **executable end-to-end** and produces a valid, anti-hallucination-clean URS instance. The core risk ("16 templates exist but the instantiation flow has never been run e2e") is **retired**. 7 findings recorded (1 medium, 6 low/informational) — none blocking.

## Verification gates

| Gate | Result |
|---|---|
| `validate-frontmatter.py specs/URS.md` | **OK** (exit 0) — valid instance frontmatter |
| `check-clarification-markers.py specs/URS.md` | 7 markers (exit 1) — **expected** in `draft`; informative, non-blocking per SKILL post-flight |
| `generate-rtm.py --specs-dir specs` | **OK** (exit 0) — 76 IDs, 0 dangling references; `specs/RTM.md` generated |
| Anti-corporate-leak grep | **0 hits** (clean) |
| Banned (legacy) categories used | **NONE** |
| Non-canonical categories used | **NONE** |
| Legacy `US-` IDs | **NONE** |
| Heritage-term occurrences | **NONE** |
| Canonical categories exercised | **22 / 22** |
| Presets copied verbatim (EREC/ESIG/SEC/API/MIGR) | Yes — legal text unchanged; system-specific determinations added as separate notes |
| `[NEEDS CLARIFICATION]` used for unknowns | Yes — 5 signatures + ESIG-013 min length + ARCH retention |

## What worked (load-bearing positives)

- The SKILL pre-flight → interview → output-template → post-flight pipeline is coherent and runnable as written.
- All anti-hallucination invariants held: no invented IDs, no invented citations, presets verbatim, markers for unknowns.
- A single URS instance naturally exercised all 22 canonical categories.
- The RTM generator consumed the instance with 0 dangling refs and produced the upstream column for free.

---

## Findings

### F1 — Language tension en/es (MEDIUM)
The toolkit's stated product language is English (child `CLAUDE.md`: "user-facing files in English"), but `templates/csv/URS.md` is `language: es` and its 36 presets (EREC/ESIG/SEC/API/MIGR) exist **only in Spanish**. SKILL rule #6 ("if `language: en` generate in English") **conflicts** with rule #2 ("copy presets verbatim") whenever a consumer sets `language: en` — the agent cannot both translate and copy-verbatim. For this run we set `language: es` to keep the run clean.
**Recommendation:** decide the canonical language strategy — (a) translate the URS template + presets to English as the canonical, Spanish as optional translation; or (b) ship bilingual presets keyed by `language`; or (c) document es-only for now and have the skill refuse `language: en` until presets are translated. Until resolved, `gdd.urs.from-idea` should warn (or refuse) when `language: en` because no English presets exist.

### F2 — Preset count drift in SKILL.md (LOW)
SKILL.md says "28 canonical Part 11 (12 EREC + 16 ESIG)" and the post-flight summary example reads "12 URS-EREC, 16 URS-ESIG". The template's Round 1.5 (2026-05-27) actually has **14 EREC + 18 ESIG + 2 SEC + 1 API + 1 MIGR = 36 presets**. The SKILL numbers are stale.
**Recommendation:** update SKILL.md preset counts to match the template (14/18 + 4 modernization).

### F3 — N/A marking vs verbatim-copy tension (LOW)
`interview-flow.md` Phase 4 says for non-applicable preset rows: "keep the row but change GxP to `N` + add a comment". Editing the GxP cell mutates the verbatim row, conflicting with anti-hallucination rule #2 (copy verbatim). Resolved here by keeping rows verbatim and recording applicability in a separate "Determinaciones específicas del sistema" note (e.g. ESIG-018 = N/A hybrid; MIGR-001 = N/A greenfield).
**Recommendation:** make the canonical N/A convention explicit and consistent (separate determinations note vs in-row edit). Prefer the separate-note approach to preserve verbatim presets.

### F4 — Cat 4 + `mode: develop` semantic tension (LOW / by-design from STATE plan)
A configured COTS (Cat 4) with `mode: develop` is slightly inconsistent (`develop` usually implies Cat 5 custom build). The `URS-DEVENV` section had to be reinterpreted as "configuration environment" rather than "code-development environment".
**Recommendation:** either a guidance note in DEVENV for Cat 3/4 + develop, or a soft manifest-validation warning on the Cat × mode combination.

### F5 — `check-clarification-markers` exit code in draft (LOW / informational)
The script exits 1 whenever markers exist. SKILL post-flight correctly says "report the count; do not fail on it" for `draft`. A naive CI gate keyed on exit code would block a legitimate draft.
**Recommendation:** add a `--draft` (or `--allow-markers`) flag that exits 0 while still reporting, so CI can distinguish "draft with expected markers" from "promotion-blocking markers".

### F6 — `validate-frontmatter` doesn't enforce `instance_frontmatter_spec` (LOW)
The docstring (check #7) claims it validates required fields per the source template's `instance_frontmatter_spec`, but the code only checks `type` / `based_on_template` / `status` / `version` / `approved_by`. A minimal frontmatter missing `system_id`, `created`, etc. would still pass. (Moot for this run — full frontmatter was written.)
**Recommendation:** either implement the spec-driven required-field check or correct the docstring.

### F7 — Tooling: `_scripts/` not matched by `**` Glob (INFORMATIONAL, not a skill defect)
The Claude Glob tool did not traverse the underscore-prefixed `skills/_scripts/` directory; `find` did. No action on the toolkit — noted for agent tooling.

---

## Artifacts produced

- `.gxp-dev.yaml` — consumer manifest
- `IDEA.md` — 1-paragraph idea brief (skill input)
- `specs/URS.md` — instantiated URS (status: draft, 76 requirements, 7 clarification markers)
- `specs/RTM.md` — auto-generated traceability matrix
- this report

## Resolution log (2026-05-29, owner-reviewed finding-by-finding)

All 7 findings closed the same day:

- **F1 — DONE.** `templates/csv/URS.md` translated to **English canonical** (was `es`); §-citations + 36 presets preserved verbatim; 0 residual Spanish. This example **regenerated in English** (re-validated clean). Catalog-wide translation of the remaining 15 templates **scheduled** in STATE (Round 2).
- **F2 — DONE.** Preset counts corrected in 6 places (SKILL.md ×3 + interview-flow.md ×3): `28 (12+16)` → `36 (14 EREC + 18 ESIG + 2 SEC + 1 API + 1 MIGR)`.
- **F3 — DONE.** `interview-flow.md` Phase 4 rewritten: presets stay verbatim, N/A and system-specific answers recorded in a separate "System-specific determinations" note (never edit the GxP cell).
- **F4 — DONE.** Guidance note added to the template's DEVENV section explaining Category × mode interpretation. Manifest Cat×mode warning **scheduled** for `gdd.init` (Round 2).
- **F5 — DONE.** `check-clarification-markers.py` gained `--draft` / `--allow-markers` (reports markers, exits 0) for CI on drafts.
- **F6 — DONE.** `validate-frontmatter.py` now reads the source template's `instance_frontmatter_spec.required_fields` and enforces them (tested: full example OK; a minimal instance now fails listing the missing fields).
- **F7 — no action** (agent-tooling Glob behavior, not a toolkit defect).

## Suggested next steps (per SKILL post-flight + cascade)

Continue the cascade on this dummy as the first full example: `/gdd.ra.from-urs` (RA-INIT, GAMP §M3 step 1) → `/gdd.fs.from-urs` (Cat 4) → resolve markers via `/gdd.clarify`. Alternatively, tackle the scheduled Round 2 catalog translation.
