# Patterns — `gxp-driven-dev`

**Patterns** are reusable, cross-cutting design recipes referenced by multiple templates and skills. Where a **template** is an instantiable deliverable (URS, FS, IQ…) and a **skill** is the executable that produces it, a **pattern** is the *methodology* distilled from them — the "why it is shaped this way", reusable across profiles.

Patterns are **inert reference content** (no runtime logic). A template's body or a skill's flow may cite a pattern instead of re-explaining the method.

---

## Format

Every pattern carries YAML frontmatter + a fixed body structure.

```yaml
---
title: "<Human-readable title>"
type: pattern
pattern_id: "<kebab-case-id>"
pattern_class: risk | lifecycle | governance | testing | data-model
language: en
status: canonical-draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
applies_to_templates: [URS, FS, …]      # templates that embody / reference it
applicable_regulations: [gamp-5, ich-q9, …]
tags: [pattern, …]
---
```

Body sections: **Intent · Context (when to use) · The pattern · Regulatory anchor · How to apply · Anti-patterns · Related**.

---

## Catalog (v0.1.0 — 6 patterns)

| Pattern | Class | Embodied in | Anchor |
|---|---|---|---|
| [FMEA](fmea.md) | risk | RA-DET (+ RA-INIT qualitative variant) | GAMP 5 §M3 step 3, ICH Q9 |
| [V-Model deliverables](v-model-deliverables.md) | lifecycle | the whole cascade | GAMP 5 Table 4.1 |
| [GAMP category applicability](gamp-category-applicability.md) | governance | RA-INIT decides; URS→PQ scaled | GAMP 5 §M4 |
| [System criticality](system-criticality.md) | governance | GXP-ASSESS, RA-INIT, VP | GAMP 5 §5.3, §M3 step 1 |
| [Constitution](constitution.md) | governance | VMP / consumer VP | GAMP 5 §M1, spec-kit Constitution |
| [Spreadsheet fixed tests](spreadsheet-fixed-tests.md) | testing | end-user-computing template (planned) | GAMP 5 §S3, EU Annex 11 |

All pattern content is 100% anonymous (see the anonymization rule in `CLAUDE.md`; enforced by `skills/_scripts/anti-leak-guard.py`).
