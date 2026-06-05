---
title: "V-Model deliverables — spec ↔ verification pairing"
type: pattern
pattern_id: "v-model-deliverables"
pattern_class: lifecycle
language: en
status: canonical-draft
created: 2026-05-30
updated: 2026-05-30
applies_to_templates: [URS, FS, DS, CS, IQ, OQ, PQ, RTM, VR]
applicable_regulations: [gamp-5, eu-annex-11, 21-cfr-part-11]
tags: [pattern, lifecycle, v-model, traceability]
---

# V-Model deliverables — spec ↔ verification pairing

## Intent

Guarantee that **every specification is verified and every verification traces to a specification** — nothing built unspecified, nothing shipped unverified — by pairing each left-arm spec with a right-arm verification.

## Context (when to use)

Always, for the structure of a validation/qualification project. The pattern is the backbone of the whole generative cascade and of the [`RTM`](../templates/csv/RTM.md).

## The pattern

The left arm decomposes intent into ever-more-concrete specs; the right arm verifies bottom-up. Each layer is verified by its **opposite**:

| Left arm (specify) | Verified by (right arm) | GAMP 5 Table 4.1 |
|---|---|---|
| [`URS`](../templates/csv/URS.md) — what the user needs | [`PQ`](../templates/csv/PQ.md) | fitness-for-intended-use verification |
| [`FS`](../templates/csv/FS.md) — how it operates | [`OQ`](../templates/csv/OQ.md) | functional verification |
| [`DS`](../templates/csv/DS.md) (Cat 5) / [`CS`](../templates/csv/CS.md) (Cat 4) — design/config detail | [`IQ`](../templates/csv/IQ.md) | installation verification |

**Traceability backbone**: `URS-<CAT>-NNN → FS-<CAT>-NNN → DS/CS-<CAT>-NNN → test case`. Each downstream ID cites its upstream ID on the same row; the [`RTM`](../templates/csv/RTM.md) is derived from those citations and must show **0 dangling references**. The [`VR`](../templates/csv/VR.md) closes the V by summarizing the right arm and issuing the fitness statement.

**Order**: IQ approved → OQ approved → PQ approved (you do not test function on an unverified installation, nor fitness before function).

## Regulatory anchor

GAMP 5 Table 4.1 (IQ/OQ/PQ ≡ installation / functional / fitness verification). **§4.2.6.4 terminology note**: GAMP 5 2nd Ed does not prescribe "IQ/OQ/PQ" as life-cycle terms — the filenames are kept by industrial CSV convention but mean installation/functional/fitness verification. EU Annex 11 §4.4 (specifications + traceability); 21 CFR Part 11 §11.10.a (validation evidence).

## How to apply

1. For each spec layer present (scaled by [GAMP category](gamp-category-applicability.md)), produce the paired verification.
2. Cite the upstream ID in every downstream row (realizes / verifies / covers column).
3. Regenerate the RTM and require 0 dangling; scale test rigor by [FMEA](fmea.md) RPN.
4. Close with the VR fitness statement.

## Anti-patterns

- ❌ A test with no upstream spec (orphan verification) or a GxP spec with no verification (untested requirement).
- ❌ Conflating IQ/OQ/PQ (installation ≠ function ≠ fitness).
- ❌ A spec layer that doesn't trace its IDs row-by-row → a meaningless RTM.

## Related

- [GAMP category applicability](gamp-category-applicability.md) · [FMEA](fmea.md) · [Constitution](constitution.md)
- [`RTM`](../templates/csv/RTM.md) · [`VR`](../templates/csv/VR.md)
