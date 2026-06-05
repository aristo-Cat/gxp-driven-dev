---
title: "FMEA — Failure Mode & Effect Analysis (risk scoring)"
type: pattern
pattern_id: "fmea"
pattern_class: risk
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30
applies_to_templates: [RA-DET, RA-INIT, OQ, PQ]
applicable_regulations: [gamp-5, ich-q9, eu-annex-11]
tags: [pattern, risk, fmea, qrm, rpn]
---

# FMEA — Failure Mode & Effect Analysis

## Intent

Score and prioritize the failure modes of a function so that **control and testing effort scales with risk**, not with template inertia — and so an auditor sees *why* each control and each test exists.

## Context (when to use)

Use for any GxP-critical function whose failure could harm patient safety, product quality, or data integrity — typically the high-priority functions surfaced by an initial qualitative assessment. The detailed FMEA is run in [`RA-DET`](../templates/csv/RA-DET.md); the initial qualitative H/M/L variant is run in [`RA-INIT`](../templates/csv/RA-INIT.md).

## The pattern

```
Risk Priority Number (RPN) = Occurrence (O) × Relevance/Severity (R) × Detection (D)
```

- **Each factor 1–3** (simplified pharma scale, consistent with ICH Q9 — **not** the classic 1–10). RPN range **1–27**.
- **Relevance (R) = process severity** — fixed by the GxP business process and **held constant across mitigation**. Controls cannot lower severity; only Occurrence and Detection improve. (RA-INIT uses the qualitative twin: Risk Class = Severity × Probability; Risk Priority = Risk Class × Detectability.)
- **Occurrence (O)** scales with the GAMP category (custom → higher).
- **Detection (D) is inverted**: high D = hard to detect = worse.
- **Double evaluation** — compute RPN **before** (eval 1) and **after** (eval 2) mitigation. This evidences control *effectiveness*, not mere existence.
- **Target RPN ≤ 4.** A risk that stays > 4 is **accepted residual risk** with formal sign-off (Process Owner + Quality Unit).
- **RPN → testing rigor** (the bridge to OQ/PQ): **1–4** Good Engineering Practice · **6–9** positive testing · **12–27** positive + negative + stress.

## Regulatory anchor

GAMP 5 §M3 step 3 (Functional Risk Assessment) + §5.3 (five-step QRM) + §11.5.4 (Risk Priority); [`ICH Q9`](https://www.ich.org) (severity × probability × detectability). EU Annex 11 §4 (Risk Management).

## How to apply

1. Take the Risk-Priority-H functions from the initial assessment.
2. Per function: failure mode → cause → consequence (PS/PQ/DI) → existing controls → O₁ R₁ D₁ RPN₁ → mitigation → O₂ R₂ D₂ RPN₂ (R₂ = R₁).
3. Order mitigations by preference: eliminate-by-design > reduce occurrence > increase detection > procedural control.
4. Route RPN₂ to the OQ/PQ test rigor; record residuals > 4 with acceptance.

## Anti-patterns

- ❌ Lowering Relevance/Severity through a control (severity is process-driven, not mitigable).
- ❌ Using RPN without the before/after double evaluation (hides whether controls work).
- ❌ Exhaustive or uniform testing that ignores the RPN bands (wastes effort, dilutes the audit story).
- ❌ A residual RPN > 4 left without documented acceptance.

## Related

- [`RA-DET`](../templates/csv/RA-DET.md) · [`RA-INIT`](../templates/csv/RA-INIT.md) · [`OQ`](../templates/csv/OQ.md) · [`PQ`](../templates/csv/PQ.md)
- [System criticality](system-criticality.md) · [GAMP category applicability](gamp-category-applicability.md)
