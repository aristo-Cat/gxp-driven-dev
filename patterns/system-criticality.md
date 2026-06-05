---
title: "System criticality — GxP impact classification"
type: pattern
pattern_id: "system-criticality"
pattern_class: governance
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30
applies_to_templates: [GXP-ASSESS, RA-INIT, VP, VR]
applicable_regulations: [gamp-5, ich-q9, eu-annex-11]
tags: [pattern, governance, criticality, gxp]
---

# System criticality — GxP impact classification

## Intent

Classify a system's **GxP criticality up front** — from its impact on patient safety, product quality, and data integrity — so the classification *gates* whether validation is required and *scales* how much. Criticality is decided before requirements, so effort is right-sized from the start.

## Context (when to use)

In the Concept phase, before the URS — in [`GXP-ASSESS`](../templates/csv/GXP-ASSESS.md) (initial GxP determination) and refined in [`RA-INIT`](../templates/csv/RA-INIT.md) §5.2. The result gates the [`VP`](../templates/csv/VP.md).

## The pattern

1. **Determine GxP relevance** — does the system create/modify/store/transmit records under a GxP predicate rule, or control a process impacting PS/PQ/DI? → `gxp-relevant` / `indirect-gxp` / `non-gxp`.
2. **Score the three impact axes** (Patient Safety, Product Quality, Data Integrity) — each High/Medium/Low, **derived from the business process** (not the technology).
3. **Roll up to a criticality level** — High if any axis is High on a safety/quality-critical process; this becomes the system's `system_impact`.
4. **Gate + scale**: non-GxP → no formal validation; GxP-relevant → validation required, with rigor scaled by criticality (and by [GAMP category](gamp-category-applicability.md) for *how* it is built).

Severity in downstream [FMEA](fmea.md) inherits from this process-derived criticality and is held constant — controls reduce occurrence/detection, never the criticality of the impact.

## Regulatory anchor

GAMP 5 §5.3 (science-based QRM) + §M3 step 1 (Initial RA + System Impact); ICH Q9 (risk to patient as the primary lens); EU Annex 11 §1 (risk management throughout the lifecycle).

## How to apply

1. In GXP-ASSESS, record GxP relevance + the PS/PQ/DI table + the rolled-up criticality, with the business-process justification.
2. Let the criticality gate the VP (no VP needed for non-GxP) and seed RA-INIT's system impact.
3. Re-confirm in RA-INIT; carry the residual-risk picture into the VR.

## Anti-patterns

- ❌ Deriving criticality from the GAMP category instead of the business process (a simple Cat 3 can be highly critical).
- ❌ Validating a non-GxP system to full GxP rigor (or skipping a critical one because it "looks simple").
- ❌ Letting a control lower the assessed criticality (criticality is the impact, not the residual).

## Related

- [`GXP-ASSESS`](../templates/csv/GXP-ASSESS.md) · [`RA-INIT`](../templates/csv/RA-INIT.md) · [FMEA](fmea.md) · [GAMP category applicability](gamp-category-applicability.md)
