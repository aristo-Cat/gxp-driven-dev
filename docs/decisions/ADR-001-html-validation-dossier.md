---
id: ADR-001
title: Self-contained HTML "validation dossier" output mode
status: accepted
decision_date: 2026-05-31
proposed_date: 2026-05-29
deciders:
  - project-owner
relates_to:
  - docs/inspirations.md  # Framework 5 (bm-prd-creator), Cat C row
tags:
  - adr
  - output-format
  - roadmap
---

# ADR-001 — Self-contained HTML "validation dossier" output mode

> **Status: ACCEPTED (2026-05-31).** Decision: **Option B**, scoped as **roadmap (Cat C, target after `v0.5.0`)** — not blocking for `v0.1.0`/`v0.5.0`. See the **Decision** section below.

## Context

`bm-prd-creator` (see `docs/inspirations.md` → Framework 5) emits its PRD as a single self-contained `prd.html`: Tailwind via CDN + Lucide icons + Google Fonts, a light/dark toggle, print-friendly `@media print` rules, no build step and no external files. For a **non-technical reviewer**, a scannable visual page is far easier to review and share than raw markdown.

`gxp-driven-dev` produces audit-grade artifacts (URS, RA-INIT/RA-DET, RTM, VR) as markdown with typed frontmatter. Our **primary** consumers (pharma-IT consultants) read markdown fine. But two **secondary** audiences — auditors, QA reviewers, regulators, founders — often do **not**, and a printable, self-contained dossier is exactly the artifact they expect to receive and file.

## Question

Should the toolkit offer an **optional output mode** that renders one or more locked specs into a single self-contained, print-friendly HTML "validation dossier", as a presentation layer over the already-locked markdown — and if so, at what scope and when?

## Options considered

### Option A — Do nothing (markdown + existing compliance-bundle only)

- **Description:** Keep markdown as the only spec format. The planned `compliance-bundle/` (Cat D) already assembles a static, inspector-friendly directory.
- **Pros:** Zero new surface. No HTML-generation logic to maintain. Markdown renders fine in most modern review tools.
- **Cons:** Misses the non-technical-reviewer audience that `bm-prd-creator` targets directly. A directory of markdown files is not a *document* an auditor can print and sign.
- **Regulatory fit:** Neutral — markdown is acceptable evidence, but less "dossier-shaped" than QA expects.

### Option B — Single-file HTML dossier as an optional output mode (recommended)

- **Description:** A `gdd.dossier.render` skill that takes locked specs (URS + RA + RTM + VR, configurable) and emits one self-contained `dossier.html`. Pure presentation over locked markdown — **never a different scope, never new content** (same hard rule `bm-prd-creator` enforces on its HTML). Print CSS produces a clean PDF via browser print.
- **Pros:** Serves auditors/QA/founders directly. Self-contained = trivially shareable and archivable. The "locked content, different presentation" rule keeps it from drifting into a second source of truth.
- **Cons:** Generation logic to maintain; CDN dependencies (mitigable by inlining for true offline use); must guarantee byte-for-byte content parity with the markdown it renders.
- **Regulatory fit:** Strong — a single, print-stable, frozen-at-render dossier matches how validation packages are filed and signed. Pairs naturally with the `compliance-bundle/`.

### Option C — Full HTML *editing* surface (rejected outright)

- **Description:** An interactive HTML app to author/edit specs.
- **Pros:** Rich UX.
- **Cons:** Massively out of scope; reintroduces an eQMS we explicitly are not building; creates a second mutable source of truth. **Violates the "markdown is the contract" principle.**
- **Regulatory fit:** Poor — two sources of truth is an audit liability.

## Comparison matrix

| Criterion | A (markdown only) | B (HTML dossier) | C (HTML editor) |
|---|---|---|---|
| Non-technical reviewability | Low | High | High |
| Maintenance cost | None | Low–Medium | High |
| Risk of second source of truth | None | Low (render-only) | High |
| Audit/file-and-sign fit | Medium | High | Low |
| Scope alignment | High | High | Violates anti-goals |

## Recommendation (for the owner to accept/reject)

**Option B**, scoped as **roadmap (Cat C, target after `v0.5.0`)** — not blocking for `v0.1.0`. Implement as a `gdd.dossier.render` skill with one inviolable rule borrowed from `bm-prd-creator`: *the HTML is a presentation of the locked markdown, never a different plan.* Add a content-parity check so the dossier cannot silently diverge from its source specs.

## Decision (2026-05-31)

**ACCEPTED — Option B, as Cat C roadmap (post-`v0.5.0`), non-blocking.**

The toolkit will eventually ship a `gdd.dossier.render` skill that renders locked specs (default scope: URS + RA + RTM + VR, configurable) into a single self-contained, print-friendly `dossier.html`, governed by the inviolable rule that **the HTML is a presentation of the already-locked markdown, never a different scope and never new content**.

Binding constraints for the future implementation:
- **Content parity is mandatory.** The render step must include a guard that fails if the dossier diverges from its source markdown (no second source of truth).
- **Offline option required.** An `--inline` flag must embed CSS/fonts/icons so air-gapped/validated sites are not forced to depend on CDNs.
- **Pairs with `compliance-bundle/`** (Cat D), not a replacement for it.

**Not started now.** No work proceeds in `v0.1.0`/`v0.5.0`; this ADR fixes the direction so the design is stable when the roadmap reaches it. The open questions below are carried into the implementation issue.

## Consequences

### Positive
- A demo-able, shareable artifact that lands with the audiences who don't read markdown.
- Differentiates from a bare directory bundle without adding a mutable surface.

### Negative / risks
- Content-parity drift if the render step is not guarded.
- CDN dependency for offline/air-gapped sites (mitigation: an `--inline` flag that embeds CSS/fonts/icons).

### Things that become possible
- A one-command "hand this to the auditor" deliverable.
- A future styled theme per `profile:` (pharma / medical-device / finance).

## Open questions left for later

- Which spec set is the default dossier scope (URS-only vs full URS+RA+RTM+VR)?
- Inline-everything for air-gapped environments, or accept CDN for v1?
- Does the dossier carry the `compliance-bundle/` hash manifest for tamper-evidence?
