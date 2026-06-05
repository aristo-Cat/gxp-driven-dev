# AGENTS.md snippet — gxp-driven-dev guardrails (Codex)

> Paste this block into the **consumer project's `AGENTS.md`** (repo root). Codex merges `AGENTS.md` from the git root down to the working directory on every run, so these guardrails are *always in context* — they hold even when the `/gdd-urs-from-idea` slash prompt is not the active turn. The slash prompt carries the *procedure*; this snippet carries the *invariants*.
>
> This is the **shared guardrail snippet for the whole gxp-driven-dev skill family** — it is not specific to URS. When porting the other skills (ra-from-urs, fs-from-urs, …), **extend this one snippet**, do not fork a copy per skill.

---

## gxp-driven-dev — spec authoring invariants (always apply)

When generating or editing any `specs/*.md` in this project (URS, FS, RA-INIT, RA-DET, CS, IQ/OQ/PQ, …):

1. **Read `.gxp-dev.yaml` first.** It declares `mode`, `profile`, `rigor_level`, `gamp_category`, `id_scheme`, `presets.*`, and `language`. If it is missing or malformed, stop and ask the user to run the init step. Never proceed without the manifest.

2. **Never invent requirement IDs.** IDs are `<DOC>-<CATEGORY>-<NNN>`, sequential within each `<DOC>-<CATEGORY>` block starting at `001`. Read the highest existing N and continue from N+1. Honor `id_scheme` (`canonical` = `URS-FUNC-001`; `custom` applies the manifest's `custom_alias`).

3. **Never invent regulatory citations.** Only cite §-references that the source template in `templates/csv/` already carries. Preset requirements (e.g. the URS Part 11 EREC/ESIG presets) are **copied verbatim** — never paraphrase the legal text or edit their `GxP`/`Prio` cells.

4. **Never invent package names, architectures, or technologies.** If a framework/database/language/cloud choice is undecided, insert `[NEEDS CLARIFICATION: which X?]` instead of guessing.

5. **Use `[NEEDS CLARIFICATION: …]` markers** — always with the actual question after the colon — whenever the user cannot answer. Do not paper over gaps.

6. **Status transitions are linear and human-gated.** `draft → in-review → approved → superseded`. Author new specs at `status: draft`. **Never** set `in-review` or `approved` yourself — that requires explicit human action.

7. **Honor the `language` field** of the manifest; do not mix languages within a spec.

8. **Anonymization (if this project is derived from the toolkit's own tree).** Use only the 22 canonical category acronyms (FUNC, EREC, ESIG, QUAL, TRAIN, DEVENV, DATA, FLOW, REPORT, PROC, UI, API, MIGR, ARCH, OPS, DOCS, TEST, DELIV, PERIPH …). Never introduce a source-organization name, corporate document code, corporate ID scheme, site code, or non-English heritage term for "category code".

9. **The deterministic checks are scripts, not prose.** After writing a spec, run the harness-agnostic Python from `<gdd-path>/skills/_scripts/` (`validate-frontmatter.py`, `check-clarification-markers.py --draft`, `generate-rtm.py`). If `validate-frontmatter.py` fails, do not claim the spec is valid.
