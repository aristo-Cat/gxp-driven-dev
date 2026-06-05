---
title: "Spreadsheet fixed tests — validating end-user computing"
type: pattern
pattern_id: "spreadsheet-fixed-tests"
pattern_class: testing
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30
applies_to_templates: [OQ, CS]
applicable_regulations: [gamp-5, eu-annex-11, 21-cfr-part-11]
tags: [pattern, testing, spreadsheet, end-user-computing]
---

# Spreadsheet fixed tests — validating end-user computing

## Intent

Validate **end-user computing** (spreadsheets and similar configurable calculation tools) proportionate to risk: prove the **template** (formulas + structure) is correct and locked, separately from the **data** entered into it.

## Context (when to use)

For GxP spreadsheets used in calculations, trending, or record-keeping (typically Cat 3 fixed or Cat 4 configured). The validation focuses on the protected template, executed as a special test type in the [`OQ`](../templates/csv/OQ.md); the locked configuration is recorded like a [`CS`](../templates/csv/CS.md).

## The pattern

1. **Separate template from data** — validate the calculation template (formulas, layout, validations); the data instance is a record, not the thing validated.
2. **Lock and protect** — protect formula cells and structure (cell/sheet protection); only designated input cells are editable; macros, if any, are **Cat 5 → design-spec'd** separately.
3. **Fixed test set** — a predefined set of known **input → expected output** cases that exercise:
   - representative normal values,
   - **boundary / limit** values (min, max, just-outside),
   - **error / invalid** inputs (rejected or flagged).
4. **Formula verification** — verify each load-bearing formula against an independent calculation (not the spreadsheet's own result).
5. **Version + change control** — the validated template is versioned; any formula/structure change re-triggers the fixed test set under change control.
6. **Data integrity** — input validation, audit trail / locked history where the predicate rule requires it; printed/exported output carries the template version.

## Regulatory anchor

GAMP 5 §S3 (end-user spreadsheets / end-user computing) + §M4 (categorization — fixed vs configured); EU Annex 11 §5–§7 (data, accuracy checks, integrity); 21 CFR Part 11 where the spreadsheet holds electronic records.

## How to apply

1. Categorize the spreadsheet (fixed Cat 3 vs configured Cat 4); flag macros as Cat 5.
2. Record the locked configuration (protected ranges, input cells, formulas) as a CS-style baseline.
3. Author the fixed test set as OQ test cases (positive + boundary + error), scaled by [FMEA](fmea.md) risk.
4. Re-run the fixed set on every template change.

## Anti-patterns

- ❌ Validating a populated spreadsheet (the data) instead of the empty protected template.
- ❌ Unprotected formula cells — anyone can silently break the calculation.
- ❌ A test set with no boundary or error cases (only happy-path values).
- ❌ Treating embedded macros as configuration rather than custom code (Cat 5 → DS).

## Related

- [`OQ`](../templates/csv/OQ.md) · [`CS`](../templates/csv/CS.md) · [FMEA](fmea.md) · [GAMP category applicability](gamp-category-applicability.md)
