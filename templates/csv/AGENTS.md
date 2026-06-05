# templates/csv/ — local agent rules (the 33 canonical templates)

These templates are the source every consumer instantiates and the RTM traces through —
editing one wrong breaks every downstream project. These rules ADD to the root `CLAUDE.md`;
they do not repeat it.

## Local invariants

- The requirement-ID scheme is FIXED: `<DOC-TYPE>-<CATEGORY>-<NNN>` with exactly the 22 canonical
  categories in `docs/requirement-id-scheme.md`. Never add a category or DOC-TYPE here — it breaks RTM
  traceability and risks re-introducing corporate nomenclature.
- `presets` / `presets_inheritance` is CONDITIONAL: only `URS` declares `presets`; `FS` uses
  `presets_inheritance`; every downstream spec, test protocol and operational record OMITS it.
- Required frontmatter blocks for a template: `placeholders`, `validation_rules`, `inputs/outputs`,
  `instance_frontmatter_spec`. Keep them — skills and `validate-frontmatter.py` depend on them.
- Never invent a regulatory citation, section number, or value to fill a gap — write
  `[NEEDS CLARIFICATION: …]`. Citations are load-bearing audit evidence.
- Never weaken a `validation_rule`, preset, or citation just to make `validate-frontmatter` /
  `lint-spec` pass. Fix the content, not the gate.
- Renaming, deleting, or restructuring any of the 33 templates (or their acronyms) is a root-level
  "stop and ask" — it breaks every consumer and the RTM. Confirm before touching the catalog shape.

## Known traps (open flags — do not silently "resolve")

- EU Annex 11 canonical edition = **2025-revised**. REPORT / ARCH / OPS still carry 2011 anchors flagged
  "(2011 — confirm 2025 §)" — they are UNCONFIRMED, not wrong; verify before citing as 2025.
- GAMP appendix numbers for DECOM-PLAN (§M10) and INFRA-QUAL (§M11) are UNVERIFIED — confirm before
  relying on them.
- `CR` = Change Request (project, GAMP §M8); `CC` = Change Control (operational, §O6). Do not relabel
  `CR` as "Code Review" (that collision was already fixed once).
- Forward-ref stubs still missing: `roles/data-protection-officer`, `templates/csv/AISC` (Annex 22),
  `templates/csv/RETIRE-REPORT`. Links to them are intentionally de-linked as "planned" — don't "fix"
  them by inventing the target.
