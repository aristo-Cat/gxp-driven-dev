---
title: "Constitution — immutable project-wide principles"
type: pattern
pattern_id: "constitution"
pattern_class: governance
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30
applies_to_templates: [VMP, VP]
applicable_regulations: [gamp-5]
tags: [pattern, governance, constitution, anti-drift]
---

# Constitution — immutable project-wide principles

## Intent

Declare the **non-negotiable, project-wide principles once**, in a single authoritative document, so that every downstream artifact **inherits** them and **no spec may contradict** them. Prevents principle-drift across a large deliverable set.

## Context (when to use)

At project start, in the [`VMP`](../templates/csv/VMP.md) (or the consumer's [`VP`](../templates/csv/VP.md) for a single system). Borrowed from `github/spec-kit`'s **Constitution** pattern, adapted to GAMP validation governance.

## The pattern

A single "constitution" document declares the immutable principles that bind the whole project, for example:

- **Criticality classification policy** — how GxP impact is assessed ([System criticality](system-criticality.md)).
- **Signature workflow** — who reviews/approves/releases (roles per GAMP §6.2.3), and the 21 CFR Part 11 / Annex 11 e-signature requirements.
- **Data integrity policy** — ALCOA+ enforcement, audit-trail + peer-review expectations.
- **Supplier qualification policy** — when and how suppliers are assessed.
- **Change-control policy** — how the validated state is maintained.

Every downstream spec **references** the constitution and must remain consistent with it; the constitution is **versioned and rarely changed** (a change ripples through the project). Downstream skills inject the constitution's anti-hallucination/quality guardrails into the consumer's agent instructions rather than re-deciding them per artifact.

## Regulatory anchor

GAMP 5 §M1 (Validation Planning — the VMP/VP as the governing plan); §6 (governance, roles & responsibilities). Conceptual lineage: spec-kit Constitution pattern.

## How to apply

1. Author the constitution in the VMP (multi-system) or VP (single system) at project start.
2. State each principle once, with its regulatory basis; mark them immutable for the project version.
3. Have every downstream template reference it; never re-decide a constitutional principle inside a child spec.
4. Version the constitution; a change to it triggers an impact review of dependent specs.

## Anti-patterns

- ❌ Re-deciding signature workflow / criticality / ALCOA+ policy independently in each spec (drift + contradiction).
- ❌ A constitution that silently diverges from actual practice (governance-on-paper).
- ❌ Burying immutable principles inside a low-level spec where they can't be found or enforced.

## Related

- [`VMP`](../templates/csv/VMP.md) · [`VP`](../templates/csv/VP.md) · [System criticality](system-criticality.md) · [V-Model deliverables](v-model-deliverables.md)
