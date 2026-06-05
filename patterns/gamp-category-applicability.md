---
title: "GAMP category applicability — deliverable set by category"
type: pattern
pattern_id: "gamp-category-applicability"
pattern_class: governance
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30
applies_to_templates: [RA-INIT, URS, FS, CS, DS, IQ, OQ, PQ]
applicable_regulations: [gamp-5]
tags: [pattern, governance, gamp-category, scaling]
---

# GAMP category applicability — deliverable set by category

## Intent

Scale the **deliverable set and validation rigor to the software category** so a project neither over-validates a standard product nor under-validates custom code. The category (decided in [`RA-INIT`](../templates/csv/RA-INIT.md)) is the parameter that scales the depth of the entire downstream cascade.

## Context (when to use)

Once the GAMP category is determined (RA-INIT §5.3), use this pattern to decide which templates are active and how deep each goes.

## The pattern

| Category | What it is | Deliverable depth | Verification |
|---|---|---|---|
| **Cat 1** | Infrastructure (OS, DB engine, middleware) | **Qualified**, not validated; covered by IT infrastructure qualification (§M11) | infrastructure qualification |
| **Cat 3** | Standard product used out-of-the-box | Lightweight FS (may fold into URS / VP); no CS, no DS | IQ + OQ (often combined for simple systems) |
| **Cat 4** | Configured product (LIMS/SCADA/ERP/CDS/EDMS/BMS, configurable spreadsheets) | URS → FS → **CS** (configured settings/parameters). No DS unless custom code | IQ verifies install + config baseline (against CS); OQ verifies configured function; PQ fitness |
| **Cat 5** | Custom / bespoke software | URS → FS → **DS** (+ Module Descriptions for large projects). Higher inherent risk | full IQ/OQ/PQ + integration + regression of custom code |

**Continuum, not rigid boxes** (§M4 §12.1): a Cat 4 product may contain Cat 5 custom macros/scripts — those are documented in the [`DS`](../templates/csv/DS.md), not the [`CS`](../templates/csv/CS.md). Categories scale **Occurrence** in [FMEA](fmea.md), never **Severity**.

## Regulatory anchor

GAMP 5 §M4 (software categories) + §12.1 (categories as a continuum) + §M11 (IT infrastructure qualification for Cat 1).

## How to apply

1. Read `gamp_category` from `RA-INIT` (or the manifest).
2. Activate the deliverable set for that category; mark the rest N/A with a reason.
3. For Cat 4, route configured settings to the CS; for Cat 5, route design to the DS; flag any custom code inside a Cat 4 platform as Cat 5 → DS.

## Anti-patterns

- ❌ A DS for a Cat 4 with no custom code, or a CS for a Cat 3 (deliverable that doesn't apply).
- ❌ Treating categories as rigid boxes — missing the Cat 5 custom code hiding inside a Cat 4 platform.
- ❌ Inflating severity because the system is Cat 5 (severity comes from the process, not the category).

## Related

- [`RA-INIT`](../templates/csv/RA-INIT.md) · [V-Model deliverables](v-model-deliverables.md) · [System criticality](system-criticality.md)
