# Methodology — Spec-Driven Development for AI Agents, with Pharma-Grade Rigor

> **Status: working draft.** Matures as the toolkit stabilizes.

This document explains the **methodology** behind `gxp-driven-dev` — the "why" of bringing pharma-grade spec rigor to general software development that is increasingly assisted by AI agents, the trade-offs, and the boundaries.

---

## Premise

AI coding agents (Claude Code, Cursor, Codex, GPT-4/5, Gemini) ship faster code than humans alone. But "vibe coding" — feeding the agent prose prompts and accepting whatever it returns — produces software that **fails at audit** (in regulated domains) and **fails at scale** (in enterprise tooling). The agent invents requirements, hallucinates package names, picks arbitrary architectures, and loses coherence across sessions.

The fix is not less AI; the fix is **better specs**. If we give the agent structured, versioned, traceable specifications as its **authoritative context**, it stops inventing and starts implementing what the spec says. This is the core insight of **spec-driven development** — and it has been a solved problem for 40+ years in the pharmaceutical industry, which produces audit-grade specifications under ISPE GAMP 5 for every computerized system that touches patient safety.

`gxp-driven-dev` borrows that pharma-grade rigor and **adapts it for any team where spec quality matters**: pharma-IT consultancies, R&D labs, indie founders in fintech / health-tech / aerospace / nuclear / automotive safety, and enterprise teams that want their AI agents grounded.

As a **side-effect**, when the consumer project happens to be in a regulated domain, the specs produced by this toolkit serve directly as compliance documentation. Zero extra effort.

---

## Why GAMP 5 as the rigor source?

ISPE **GAMP 5 Second Edition (2022)** is the global reference for validating computerized systems in regulated pharmaceutical manufacturing. It defines:

- A **4-phase lifecycle**: Concept → Project → Operation → Retirement (§3.1 p.23).
- A **V-Model** linking specifications to verifications (URS↔PQ, FS↔OQ, DS↔IQ) — §3.2 p.25 Figure 3.3. GAMP 5 also explicitly accepts iterative/Agile shapes (§3.2 Figure 3.4), so the V-Model is **one valid shape, not a mandate**.
- A **risk-based scaling** approach — work effort scales with patient-safety/product-quality/data-integrity risk, not with template inertia (§5 + Appendix M3).
- A **5-category framework** (Cat 1 infrastructure, Cat 3 standard product, Cat 4 configured, Cat 5 custom) that scopes what artifacts are required (Appendix M4).
- A **role separation** that travels across organizations: Process Owner, System Owner, Data Owner, Quality Unit, SME, Supplier, End User (§6.2.3).

The combination of "structured specs + paired verification + risk-based scaling + clear roles + audit trail" is what survives **FDA inspection** — the hardest external software audit in industry. That same rigor transfers naturally to:

- **Enterprise B2B tooling** (where customers' procurement teams want SOC 2 + ISO 27001 alignment evidence)
- **Scientific R&D platforms** (where reproducibility matters)
- **Indie startups in regulated markets** (where day-one inspection readiness avoids costly retrofits)
- **AI-assisted software construction in any domain** (where grounding the agent is the difference between shippable and demo-quality)

We are **not certified to GAMP 5**, nor do we certify anyone else. We borrow the **structural rigor** and **explicit traceability** that GAMP 5 prescribes, adapt them to be machine-readable by AI agents, and ship the toolkit under permissive open-source license.

---

## Spec-driven development — definition for AI agents

> **Spec-driven development for AI agents** is the discipline of writing **executable specifications** *before* (and continuously *alongside*) implementation, with the specifications themselves being the **canonical source of truth** — versionable, validatable, diffable, and **consumable by AI agents as authoritative context**.

In concrete terms:

1. **Structured Markdown + YAML frontmatter**: every spec is a `.md` file with declarative metadata at the top (placeholders, presets, validation rules, downstream consumers).
2. **Stable canonical IDs**: every requirement, design point and test case has an identifier of the form `<DOC-TYPE>-<CATEGORY>-<NNN>` (see `docs/requirement-id-scheme.md`) that survives the lifecycle — never reused, never deleted, only struck through if obsolete.
3. **Explicit downstream mapping**: each template's frontmatter declares which downstream artifacts consume it. `URS` feeds `FS`, `RA-INIT`, `IQ`, `PQ`. `FS` feeds `DS`, `RA-DET`, `OQ`. Etc.
4. **Skills as the agent interface**: skills (`gdd.urs.from-idea`, `gdd.fs.from-urs`, `gdd.trace.validate`, etc.) are how AI agents instantiate, validate, and cascade between specs.
5. **`[NEEDS CLARIFICATION: …]` markers** when an agent cannot answer a placeholder — a later interactive skill resolves these with the human.

The agent **does not invent requirements**; it reads `URS-FUNC-001` from the URS, drafts the matching `FS-FUNC-001` section in the FS, and the human reviews. The agent **does not invent test cases**; it reads the URS+FS, drafts `OQ-TC-NNN` test cases, and the human reviews. The agent **does not invent regulatory citations**; it reads what the template already cites and stays within those bounds.

This is what we call the **generative cascade**:

```
idea
 │
 ├──► /gdd.init                         creates `.gxp-dev.yaml` (manifest)
 │
 ├──► /gdd.urs.from-idea                interview → `specs/URS.md`
 │
 ├──► /gdd.ra.from-urs                  Initial Risk Assessment → `specs/RA-INIT.md`
 │
 ├──► /gdd.fs.from-urs                  drafts `specs/FS.md` with FS-XXX-NNN traced to URS-XXX-NNN
 │
 ├──► /gdd.ra.detail.from-urs-fs        Detailed RA / FMEA → `specs/RA-DET.md`
 │
 ├──► /gdd.tests.from-ra                drafts IQ/OQ/PQ test specs
 │
 ├──► /gdd.implement-from-specs         AI agent writes code using specs as authoritative context
 │
 ├──► /gdd.trace.validate               derives `specs/RTM.md` + reports gaps
 │
 └──► /gdd.compliance-bundle            (optional) assembles `compliance-bundle/` for regulated audits
```

Each step: AI proposes a draft; human reviews; status advances `draft → in-review → approved`. The specs are the contract; the agent uses them as authoritative context throughout, eliminating hallucination loops.

---

## Two modes: Develop and Validate (+ Hybrid)

The `.gxp-dev.yaml` manifest declares a `mode` field that scopes how the toolkit is used:

### Mode B — Develop (primary)

Consumer **builds new custom software**. AI agents consume specs as authoritative context when implementing the system. Typical templates active: `URS · FS · DS · ADR · API-SPEC · DBS · UC · AC · CR · UT-PLAN · IT-PLAN · SEC-TEST · PERF-TEST · IQ · OQ · PQ · RTM · VR · RN · DEPLOY-RUN`. Anchored in GAMP 5 D-Appendices (D1 specifying requirements, D3 configuration/design, D4 software mgmt/dev review, D5 testing, D8 Agile software dev).

### Mode A — Validate (secondary)

Consumer **validates an existing third-party software** (commercial product, SaaS) by applying the same spec rigor. Typical templates active: `URS · CS · SUP-ASSESS · IQ · OQ · PQ · RTM · VR`, plus a **SaaS bundle** (`SOC-EVIDENCE · SLA · SHARED-RESP · EXIT-PLAN`) when applicable. Anchored in GAMP 5 M2 (Supplier Assessment), D7 (Data Migration if applicable) and Ch 7 (supplier good practices).

### Mode Hybrid (most realistic)

Consumer has **both** vendor components and custom integrations. Both sets of templates active, declared via `hybrid_breakdown` in `.gxp-dev.yaml`. Example: a LIMS commercial core + custom plugins for QC data capture → LIMS goes through Validate flow, plugins go through Develop flow, RTM is unified.

---

## What this changes — and what it does not

| Changes | Stays the same |
|---|---|
| AI agents grounded on structured specs (instead of vibe-coded from prompts) | Need for human judgment on requirements appropriateness |
| Medium of specifications (Word → structured Markdown + YAML) | Regulatory contracts (GAMP 5, Part 11, Annex 11, Annex 22, GDPR, MDR, …) |
| Storage (file servers → Git, diffable, versionable) | Quality Unit accountability for approving specs |
| Traceability mechanism (Excel matrix → script-derived RTM) | Need for trained personnel reviewing AI output |
| Authoring effort (manual → AI-co-authored) | Need for human checkpoints (`draft → in-review → approved`) |
| Inspection format (PDFs → versioned Markdown + rendered bundles) | Need for periodic review and lifecycle discipline |
| Speed of bootstrapping a compliant project (months → days) | Inspection rigor and evidence requirements |

---

## Boundaries — what this methodology does NOT solve

- **Critical thinking is irreducible.** AI can draft specifications faster than a human, but it cannot replace the system owner's judgment about whether a control is appropriate for the risk. The methodology automates paperwork, not accountability.
- **AI agents are not certified.** The toolkit produces specs an AI can use as context, but the AI itself remains accountable to the consumer's review discipline. EU GMP **Annex 22 (2025 consultation)** sets the bar for AI in pharma manufacturing. We align with it but do not certify any AI runtime.
- **Validation of the validation toolkit.** A future open question: do specs produced by AI need additional review compared to specs produced by humans? Probably yes, initially. The methodology should evolve to include explicit guardrails for AI-co-authored content.
- **Vendor system constraints.** Many enterprise systems (TrackWise, Veeva, MasterControl, SAP) have their own internal templates and workflows. The toolkit complements those systems; it does not replace them.
- **Cultural change.** Adopting spec-driven development in a Word-document-driven organization requires more than tooling — it requires retraining and procedural adjustment. This is out of scope of the toolkit.

---

## Further reading (canonical inputs)

- **ISPE GAMP 5 Second Edition (2022)** — the foundational framework. Anchor for V-Model, category framework, role separation, risk-based scaling.
- **FDA 21 CFR Part 11** — Electronic Records / Electronic Signatures. Anchor for `EREC` and `ESIG` requirement categories.
- **EU GMP Annex 11 (2025 consultation)** — Computerised Systems. Anchor for many `OPS`, `SEC`, `ARCH` requirements; introduces explicit cybersecurity expectations in §17.
- **EU GMP Annex 22 (2025 consultation)** — AI/ML in pharmaceutical manufacturing. Reference for `AISC` template.
- **ICH Q9 (R1)** — Quality Risk Management. Anchor for `RA-INIT` and `RA-DET` methods.
- **PIC/S PI 041-1** — Data Integrity in GxP environments. Anchor for ALCOA+ enforcement across all spec types.
- **ISO/IEC 12207** — Software lifecycle processes. General-software anchor that maps cleanly to the V-Model.
- **OWASP ASVS** — Application Security Verification Standard. Anchor for `SEC-TEST` and `SEC` requirements.
- **ISO 25010** — Software product quality model. Anchor for `PERF` and `QUAL` requirements.

For pharma-adjacent industries with their own rigorous frameworks, the toolkit can extend via the **multi-industry anchor system** (planned in Cat D innovations — `docs/inspirations.md`):

- **IEC 62304** — Medical device software lifecycle
- **DO-178C** — Airborne software (aerospace)
- **ISO 26262** — Functional safety (automotive)
- **IEC 60880** — Nuclear instrumentation software
- **SOX + NIST CSF + PCI DSS** — Financial systems

---

## Open questions for the methodology

- How do `mode=develop` and `mode=validate` share artifacts in `hybrid` projects when components partially overlap?
- Should code generation from approved FS be deterministic (template-based) or AI-assisted (LLM with FS as context)? Probably the latter, but with hard guardrails (test coverage gate, slopcheck for hallucinated packages).
- How do we handle bilingual/multilingual instances? Canonical IDs are stable; body text translatable. A skill `translate-spec` could AI-assist with human approval.
- How do we integrate the toolkit's specs into corporate eQMS / DMS systems (TrackWise, Veeva, MasterControl) for formal approval workflows? Roadmap (Cat C).
- How do we audit AI-co-authored content beyond the human reviewer's eye? Logging of LLM contributions per spec? Diff annotations? Both, planned for `v0.5.0`+.
- How do we evolve the 22 canonical category codes if industry practice shifts? The set is intentionally frozen for `v0.x`; changes deferred to `v2.0`+ and require explicit migration tooling.

These questions are deliberately left open. They will be addressed as the toolkit matures and gathers real usage.
