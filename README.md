# gxp-driven-dev

> **Open-source toolkit for spec-driven development with pharma-grade rigor — built for AI agents to ship quality software using specs as authoritative context. Compliance docs come free.**

Inspired by **ISPE GAMP 5 Second Edition (2022)** V-Model + **21 CFR Part 11** + **EU GMP Annex 11 (2025)** + **Annex 22 (AI/ML in pharma, 2025)** + **ICH Q9 (R1)** + **PIC/S PI 041-1**. Designed for: pharma-IT consultancies developing software for regulated clients · indie hackers in regulated industries · R&D labs building internal tooling with AI assistance.

🚧 **Status: Sprint 2 (templates batch + first operative skill), pre-`v0.1.0`.** 33 canonical templates planned with acronym-only IDs; 2 in progress. Skills layer scaffolded.

---

## Table of contents

- [Why this exists](#why-this-exists)
- [What it is, in one paragraph](#what-it-is-in-one-paragraph)
- [The radical idea](#the-radical-idea)
- [Killer feature: the generative cascade](#killer-feature-the-generative-cascade)
- [What's inside the toolkit](#whats-inside-the-toolkit)
- [What this is NOT](#what-this-is-not)
- [Audiences and use cases](#audiences-and-use-cases)
- [Positioning vs github/spec-kit](#positioning-vs-githubspec-kit)
- [Architecture in 5 minutes](#architecture-in-5-minutes)
- [Requirement ID scheme](#requirement-id-scheme)
- [V-Model coverage](#v-model-coverage)
- [How a consumer project is structured](#how-a-consumer-project-is-structured)
- [The .gxp-dev.yaml manifest](#the-gxp-devyaml-manifest)
- [Status and roadmap](#status-and-roadmap)
- [Design principles](#design-principles)
- [Anti-goals](#anti-goals)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)
- [License](#license)

---

## Why this exists

AI coding agents (Claude Code, Cursor, Codex, GPT, Gemini) ship faster code than humans alone. But **"vibe coding"** — feeding the agent prose prompts and accepting whatever it returns — produces software that **fails at audit** (regulated domains) and **fails at scale** (enterprise tooling). The agent invents requirements, hallucinates package names, picks arbitrary architectures, loses coherence across sessions.

The fix is not less AI; the fix is **better specs**. Structured, versioned, traceable specifications used as the agent's **authoritative context** stop the agent from inventing and start it implementing what the spec says.

**This is a 40-year-solved problem in pharma.** ISPE GAMP 5 has produced audit-grade specifications for computerized systems since the early 1990s — the most demanding software-spec discipline in industry, designed to survive FDA inspection. `gxp-driven-dev` borrows that rigor and **adapts it for any team where spec quality matters**: pharma-IT consultancies, R&D labs, indie founders in fintech / health-tech / aerospace / nuclear / automotive safety, enterprise teams that want their AI agents grounded.

**As a side-effect**, when the consumer project happens to be in a regulated domain, the specs produced by this toolkit serve directly as compliance documentation. Zero extra effort.

---

## What it is, in one paragraph

A toolkit of **AI-callable skills** (Claude Code-first, port to Cursor / Codex in 3-6 months) that potentiate AI agents with **33 canonical Markdown templates** (URS, FS, DS, IQ, OQ, PQ, RA-INIT, RA-DET, CR, RTM, VR, PR, CC, IR, and 19 more) carrying **declarative YAML frontmatter** (typed placeholders, presets, validation rules, downstream consumers, instance frontmatter spec). Skills are **generative**: they draft cascade-down (URS → FS → RA → tests → code stubs) using approved upstream specs as authoritative context. Auxiliary Python 3.12+ scripts handle deterministic tasks (validate frontmatter, generate RTM, lint specs, slopcheck against package hallucinations). Output is **modular** per `.gxp-dev.yaml` manifest: specs + code + tests + docs + optional compliance bundle for regulated audits.

---

## The radical idea

If specifications are **structured Markdown + YAML frontmatter** with stable canonical IDs and explicit downstream mapping, then:

| Property gained | How it works |
|---|---|
| **AI-grounded** | Specs in YAML+Markdown with stable IDs become **authoritative context** for any LLM. Anti-hallucination: the agent reads `URS-FUNC-001` instead of inventing. |
| **Versionable** in Git | True diffs between revisions, full history, blame per requirement. |
| **Parseable** by scripts and AI | Frontmatter is YAML, body has predictable structure (numbered sections, ID-prefixed tables). |
| **Traceable automatically** | A grep of `URS-FUNC-001` shows every reference across URS, FS, DS, IQ, OQ, PQ. No more Excel matrix. |
| **Generable** downstream | `FS.md` can be skeletoned from `URS.md` because outputs are declared in frontmatter and IDs cascade. |
| **Validatable** across layers | A skill `gdd.trace.validate` checks coherence URS↔FS↔RA↔Tests programmatically. |
| **AI co-authorable** | LLMs read structured specs, propose requirements, draft FS sections, flag inconsistencies — humans approve. |
| **Diffable** for inspection | Auditor reads `git diff v1.0..v1.1 specs/URS.md` and sees exactly what changed and why. |

The framework **does not change the regulations**. GAMP 5, 21 CFR Part 11, EU GMP Annex 11 and Annex 22 remain the compliance contract. What changes is **how compliance is executed**: from static documents to executable specs.

---

## Killer feature: the generative cascade

One idea → URS (interview) → RA-INIT (initial risk) → FS (drafted from URS) → RA-DET (FMEA from URS+FS) → Test specs (IQ/OQ/PQ drafted from RA + FS) → Code stubs (drafted from FS + tests) → Compliance bundle (assembled from all of the above).

Each step: AI proposes a draft; human reviews; status advances `draft → in-review → approved`. The specs are the **contract**; the agent uses them as authoritative context throughout, **eliminating hallucination loops**.

This cascade is also the **anti-vibe-coding** defense: at every stage the agent is grounded in approved upstream content, citations are pre-existing in the templates (not invented), package suggestions are slopchecked, and traceability is computable instead of hand-curated.

---

## What's inside the toolkit

```
gxp-driven-dev/
├── README.md                ← This file
├── LICENSE                  ← Apache License 2.0
├── NOTICE                   ← Apache 2.0 attribution notice
├── STATE.md                 ← Living memory of toolkit development
├── MEMORY.md                ← Durable lessons (traps, fixes) — auditable, in-Git
├── AGENTS.md                ← AI-agent contract — THE single source
├── CLAUDE.md                ← one line: @AGENTS.md (Claude Code import; never edit directly)
├── .gitignore
├── docs/
│   ├── methodology.md       ← Why pharma-grade rigor for general software dev
│   ├── project-layout.md    ← Canonical layout for consumer projects + .gxp-dev.yaml schema
│   ├── inspirations.md      ← Adoption matrix Cat 0/A/B/C/D from 4 reference frameworks
│   ├── requirement-id-scheme.md ← 22 canonical category acronyms + format <DOC>-<CAT>-<NNN>
│   └── (planned) canonical-schemas.md, v-model.md, glossary.md
├── templates/csv/           ← 33 canonical templates (acronym-named)
│   ├── URS.md               ← Round 1 complete (28 Part 11 reqs embedded)
│   └── VMP.md               ← in progress (Sprint 2)
├── patterns/                ← 6+ planned cross-cutting reusable patterns
├── skills/                  ← AI-callable skills (Claude Code first)
│   ├── README.md
│   ├── _scripts/            ← Python 3.12+ auxiliary scripts
│   └── <skill-name>/SKILL.md
├── examples/                ← (planned) fully instantiated end-to-end cases
└── .github/                 ← (planned) CI workflows, issue templates
```

### Templates (33 canonical, organized by lifecycle phase)

| Family | Templates |
|---|---|
| **Master** | `VMP` |
| **Concept** | `GXP-ASSESS` |
| **Project — Planning** | `VP` · `SUP-ASSESS` · `RA-INIT` |
| **Project — Specification** | `URS` · `FS` · `CS` · `DS` · `API-SPEC` · `DBS` · `UC` · `AC` · `ADR` |
| **Project — Detailed Risk** | `RA-DET` |
| **Project — Verification** | `IQ` · `OQ` · `PQ` · `UT-PLAN` · `IT-PLAN` · `SEC-TEST` · `PERF-TEST` · `CR` · `RTM` |
| **Project — Closeout** | `VR` · `RN` · `DEPLOY-RUN` |
| **Operation** | `PR` · `CC` · `IR` · `CONFIG-BL` · `UAR` · `BRR` |
| **Retirement** | `DECOM-PLAN` · `RETIRE-REPORT` |
| **Cross-cutting (conditional)** | `DPIA` · `CYBER-RA` · `AISC` · `P11M` · `SVP` |
| **SaaS-specific bundle** | `SOC-EVIDENCE` · `SLA` · `SHARED-RESP` · `EXIT-PLAN` |

Status:
- `URS` — Round 1 complete (28 Part 11 requirements embedded as preset)
- `VMP` — Round 1 in progress (Sprint 2 — next)
- 31 templates planned for Round 1 across `v0.1.0`

### Skills (10 folders planned)

| Skill | Status | Role |
|---|---|---|
| `gdd.urs.from-idea` | Sprint 2 (operative) | Interactive interview → `specs/URS.md` |
| `gdd.fs.from-urs` | Stub | Draft `specs/FS.md` from approved URS |
| `gdd.ra.from-urs` | Stub | Initial Risk Assessment (GAMP 5 §M3 step 1) |
| `gdd.ra.detail.from-urs-fs` | Stub (Round 2) | Detailed RA / FMEA from URS+FS |
| `gdd.tests.from-ra` | Stub | Draft IQ/OQ/PQ from RA + FS |
| `gdd.cs.from-fs` | Stub | (Cat 4 only) Configuration Spec from FS |
| `gdd.trace.validate` | Stub | Derive RTM, report gaps URS↔FS↔RA↔Tests |
| `gdd.lint.spec` | Stub | Validate frontmatter + check `[NEEDS CLARIFICATION]` markers |
| `gdd.init` | Stub | Bootstrap a new consumer project from manifest |
| `gdd.next` | Stub (orchestrator) | Suggest next skill based on STATE + manifest |
| `gdd.lifecycle` | Stub (orchestrator) | Full-cascade orchestration |

Auxiliary scripts (Python 3.12+ stdlib + PyYAML in `skills/_scripts/`): `validate-frontmatter.py` · `generate-rtm.py` · `check-clarification-markers.py` · `lint-spec.py` · `lib/gdd_common.py`.

---

## What this is NOT

- ❌ **Not an eQMS or DMS.** Does not manage the runtime lifecycle (workflow execution, approval routing, retention scheduling). Use TrackWise / Veeva Vault QA / MasterControl for that.
- ❌ **Does not replace qualified electronic signatures.** Produces the content; the signature is applied by your corporate 21 CFR Part 11–compliant signing system.
- ❌ **Not vendor-specific.** Agnostic to Empower / Chromeleon / LabWare / SAP / TrackWise / Veeva.
- ❌ **Does not certify anything.** Templates are inputs to validation; regulatory accountability remains with the consumer's Quality Unit.
- ❌ **Not an automatic translator.** Templates ship in English; instantiation in other languages is human work (AI-assisted if desired).
- ❌ **Not a GAMP 5 course.** Assumes familiarity with the framework. For learning, consult ISPE GAMP 5 Second Edition (2022) directly.
- ❌ **Not a substitute for critical thinking.** AI automates paperwork, not judgment. A system owner remains accountable for whether a control is appropriate for a given risk.
- ❌ **Not a competitor to ISPE GAMP 5.** It is an *implementation companion* inspired by the framework, intended to make rigorous spec-driven development more accessible.
- ❌ **Not a clone of `github/spec-kit`.** We speak a different language — see [Positioning](#positioning-vs-githubspec-kit) below.

---

## Audiences and use cases

| Audience | How they use the toolkit | Value they obtain |
|---|---|---|
| **Pharma-IT consultant developing software for regulated clients** | Apply the toolkit per client project; AI agents draft specs and code while the consultant reviews and signs off | Sell rigor, not Word templates; faster project delivery; portable methodology |
| **Indie founder in a regulated industry** | Bootstrap an inspection-ready SDLC in days instead of months | Don't reinvent the V-Model; arrive at first audit aligned with framework expectations |
| **R&D lab building internal tooling with AI** | Instantiate templates for each tool; cascade through the lifecycle | Reproducible, traceable, low-friction tooling that survives team turnover |
| **Enterprise tooling team** | Adopt the toolkit for internal B2B tools that need to clear procurement security reviews | SOC 2 + ISO 27001 alignment evidence as side-effect of normal development |
| **CSV manager modernizing practice** | Replace Word document chains with versionable Markdown specs co-authored with AI | 60-80% less time on paperwork; automatic traceability |
| **Auditor / regulatory inspector** | Read auto-generated traceability reports; consult Git diffs between approved versions | Audit structural coherence, not manually reconstructed binders |
| **GAMP 5 educator / trainer** | Use templates + worked examples as didactic material | Modern teaching material (Markdown + Git + AI assistants) instead of legacy Word screenshots |

---

## Positioning vs github/spec-kit

`github/spec-kit` is **general-purpose spec-driven development** for app developers — broad audience, lightweight conventions, brilliant adapter system across 30+ runtimes.

`gxp-driven-dev` is **specialized for environments where spec quality matters at audit grade**: regulated industries, R&D labs, enterprise tooling consultancies. **Different audience, different vocabulary, complementary not competing.**

We borrow from spec-kit: `[NEEDS CLARIFICATION]` markers, the cross-artifact analyze concept, the slash command namespace pattern, the runtime adapter philosophy (planned for `v0.5.0`).

We add: **typed YAML frontmatter** (vs `[BRACKET]` placeholders), **V-Model lifecycle as default** (with Agile as opt-in), **GAMP-grade traceability** with RTM as a derived first-class artifact, **22 canonical category acronyms** producing stable `<DOC>-<CAT>-<NNN>` IDs across the lifecycle, **compliance bundles** as a free byproduct, **multi-industry anchors** (pharma + medical-device + finance + aerospace + nuclear + general), and **rigor levels** (light/standard/strict/regulated).

Both projects can coexist in the same ecosystem. If you don't need pharma-grade rigor, use spec-kit. If you do (or you're in any domain where audit-readiness matters), `gxp-driven-dev` is the specialized companion.

---

## Architecture in 5 minutes

The toolkit has **three layers**, deliberately separated so an AI agent can read and reason about each independently:

### Layer 1 — Templates (`templates/csv/`)

Markdown files with rich YAML frontmatter. Each template:
- **Declarative**: declares its `placeholders`, `presets`, `validation_rules`, `inputs`, `outputs`, `instance_frontmatter_spec`.
- **Self-describing**: embeds an *Instantiation flow* section at the bottom — interview order, stop criteria, status transitions, downstream mapping.
- **Versioned**: `template_version` field (semver) within the toolkit.

Example frontmatter (excerpt from `URS.md`):
```yaml
template_id: "URS"
template_version: "0.1.0"
v_model_phase: requirements-definition
gamp_categories_applicable: [2, 3, 4, 5]
inputs:
  - template_id: "GXP-ASSESS"
    required: true
outputs:
  - artifact: "URS instance (Markdown)"
    consumed_by: ["FS", "RA-INIT", "IQ-test-cases"]
placeholders:
  system_name: { type: string, required: true, … }
  gamp_category: { type: enum, values: [1, 3, 4, 5], required: true }
presets:
  URS-EREC: { description: "12 reqs of 21 CFR Part 11 Electronic Records", activation_question: "…" }
validation_rules:
  - "If gamp_category == 5: URS-DEVENV, URS-QUAL, URS-TRAIN must each have ≥3 requirements"
```

### Layer 2 — Patterns (`patterns/`) — planned

Reusable design patterns referenced from multiple templates (FMEA, V-Model deliverables, Constitution, Criticality Assessment, Spreadsheet Fixed Tests).

### Layer 3 — Skills (`skills/`)

AI-callable skills that operate on templates and produce instances or validation reports. Designed for Claude Code first; port to Cursor / Codex in `v0.5.0`. Auxiliary scripts in Python 3.12+ handle deterministic tasks.

---

## Requirement ID scheme

Every requirement is identified as `<DOC-TYPE>-<CATEGORY>-<NNN>`. Full spec in [`docs/requirement-id-scheme.md`](docs/requirement-id-scheme.md).

The **22 canonical categories**:

| Code | Meaning | Code | Meaning |
|---|---|---|---|
| `FUNC` | Functional | `OPS` | System Operations |
| `PERF` | Performance | `DOCS` | Documentation |
| `QUAL` | Quality (process) | `TEST` | Testing |
| `TRAIN` | Training | `DELIV` | Deliverables / Scope of supply |
| `DEVENV` | Development environment | `PERIPH` | Peripherals |
| `DATA` | Data structure | `HW` | Hardware |
| `FLOW` | Data flow | `EREC` | Electronic Records (21 CFR Part 11) |
| `REPORT` | Reports / Printouts | `ESIG` | Electronic Signatures (21 CFR Part 11) |
| `SEC` | Security | | |
| `PROC` | Process organization | | |
| `UI` | User Interface | | |
| `API` | Interfaces / APIs | | |
| `MIGR` | Data Migration | | |
| `ARCH` | Archiving | | |

Examples: `URS-FUNC-001` (User Requirement #1 functional), `FS-API-002` (Functional Spec #2 API), `DS-DATA-005` (Design Spec #5 data structure), `IQ-TC-042` (IQ test case #42), `RA-INIT-001` (Initial RA finding #1).

Consumers with internal naming conventions can opt out via `id_scheme: custom` + `custom_alias` in `.gxp-dev.yaml`.

---

## V-Model coverage

The toolkit covers the full V-Model lifecycle (ISPE GAMP 5 §3.2 Figure 3.3) and accommodates Agile variants (§3.2 Figure 3.4). Each template's frontmatter declares its `v_model_phase` and downstream consumers.

```
   Requirements Definition          Performance Qualification (PQ)
              ↓                                ↑
         URS (top)            ───tests───→     PQ
              ↓                                ↑
   Functional Specification     ───tests───→  OQ
         FS (middle)                           ↑
              ↓                                ↑
    Design Specification        ───tests───→  IQ
         DS (bottom, Cat 5)
   (CS for Cat 4 alternates here)
```

Cross-cutting throughout: `VMP`, `GXP-ASSESS`, `VP`, `SUP-ASSESS`, `RA-INIT`, `RA-DET`, `CR` (Cat 5), `RTM`. Cross-cutting conditional: `DPIA`, `CYBER-RA`, `AISC`, `P11M`, `SVP`. Lifecycle close: `VR`, `RN`, `DEPLOY-RUN`. Operation: `PR`, `CC`, `IR`, `CONFIG-BL`, `UAR`, `BRR`. Retirement: `DECOM-PLAN`, `RETIRE-REPORT`.

---

## How a consumer project is structured

When an organization adopts `gxp-driven-dev` for a specific system, the consumer's repo follows this layout (full detail in [`docs/project-layout.md`](docs/project-layout.md)):

```
my-project/
├── README.md
├── .gxp-dev.yaml                ← manifest
├── pyproject.toml / package.json ← stack-specific
├── src/                          ← application code
├── tests/                        ← functional tests
├── specs/                        ← ⭐ instantiated specs (acronym-named)
│   ├── URS.md   FS.md   DS.md   RA-INIT.md   RA-DET.md
│   ├── IQ.md    OQ.md   PQ.md   RTM.md       VR.md
│   └── …
├── evidence/                     ← IQ/OQ/PQ evidence captured
│   └── iq/ oq/ pq/ periodic-review/
├── compliance-bundle/            ← (optional) assembled for audit
└── .github/workflows/
    ├── gdd-lint.yml              ← CI: frontmatter, broken-link, anti-leak grep
    └── trace-check.yml           ← CI: URS↔FS↔RA↔Tests coherence
```

The **`specs/`** folder is the spec documentation of the consumer system. Instances are version-controlled in Git; amendments to approved specs emit new semver versions, mark previous as `superseded`, never overwrite history.

---

## The `.gxp-dev.yaml` manifest

Declarative file at the root of the consumer's repository. Full spec in [`docs/project-layout.md`](docs/project-layout.md).

```yaml
gxp_dev_version: ">=0.1.0,<1.0.0"
project_id: "PROJ-2026-001"
project_name: "Lab Data Capture App"
language: en

mode: develop                  # develop | validate | hybrid
lifecycle: v-model             # v-model | agile | hybrid
gamp_category: 4
lifecycle_phase: project

id_scheme: canonical           # canonical | custom
custom_alias:                  # only when id_scheme == custom
  URS: "REQ-USER-DOC"

profile: pharma                # pharma | medical-device | finance | aerospace | nuclear | general
rigor_level: standard          # light | standard | strict | regulated

presets:
  part11_active: true
  annex11_active: true
  gdpr_active: false
  annex22_active: false

templates_active:
  - VMP
  - GXP-ASSESS
  - VP
  - URS
  - FS
  - DS
  - ADR
  - RA-INIT
  - RA-DET
  - IQ
  - OQ
  - PQ
  - RTM
  - VR

outputs:
  specs: true
  code: true                   # AI agent generates from approved specs
  tests: true
  compliance_bundle: true
```

---

## Status and roadmap

### Current sprint

- **Sprint 2 — Template Design** (in progress, pre-`v0.1.0`).
- `URS.md` Round 1 complete (frontmatter declarative, 28 Part 11 requirements embedded, Instantiation flow documented).
- `VMP.md` next in line as Sprint 2's second template.
- Skills layer scaffolded with `gdd.urs.from-idea` as first operative skill + 9 stubs.

### Targets

| Milestone | Scope |
|---|---|
| **`v0.1.0`** | 33 templates Round 1 + 6 patterns + 5 skills + 1 worked example + CI lint |
| **`v0.5.0`** | All templates Round 2 (formal schemas, output schemas, agnostic markdown links) + 10-15 skills + Cursor/Codex adapters + 2 examples |
| **`v1.0.0`** | Feature-complete, externally documented, community-ready, public release (license applied: Apache 2.0) |
| **`v2.0.0`** | Community contributions integrated; coverage of additional regulatory regimes (medical devices ISO 13485 / IEC 62304, aerospace DO-178C, automotive ISO 26262) |

### Roadmap themes

- **Integration with corporate eQMS** (TrackWise / Veeva / MasterControl) via export adapters and `/gdd.export-to-eqms` skill.
- **Automated test scaffolding** — generate `pytest` / `Playwright` / `Vitest` stubs from approved OQ/PQ test cases.
- **Multilingual instances** — same canonical IDs, body translatable; AI-assisted with human approval.
- **Inspector mode** — read-only view optimized for FDA / EMA / regional inspectors with auto-generated traceability narrative.
- **Continuous compliance** — CI checks for drift between approved specs and running application behavior.

---

## Design principles

1. **Specifications as executable contracts**, not narrative documents.
2. **Machine-readable frontmatter** declares structure; body provides human-readable content.
3. **Stable canonical IDs** survive the full lifecycle — never reused, never deleted, only struck through if obsolete.
4. **Anti-leak hygiene**: nothing in this toolkit references any specific corporate identity, document code, site code or proprietary scheme.
5. **AI-agnostic by construction**: any sufficiently capable LLM consumes the templates and skills; no Claude-only or GPT-only features.
6. **Regulations are the contract; the toolkit is the implementation**. We never claim to override GAMP 5, Part 11, Annex 11 or Annex 22.
7. **Critical thinking is irreducible**. The toolkit automates paperwork; humans remain accountable for judgment.
8. **Versionable in Git**. Diffs between revisions are first-class; history is never overwritten.
9. **Composable downstream**. Each template's output is structured so the next layer auto-drafts from approved upstream.
10. **Optimize for inspection-readiness**. The chain must be auditor-friendly out of the box.

---

## Anti-goals

- ❌ A toolkit that only works with one AI assistant. Agnosticism is non-negotiable.
- ❌ A "dead" repo of static templates that don't evolve with regulatory updates.
- ❌ A commercial product disguised as open-source (free today, paywall tomorrow).
- ❌ A toolkit dependent on any single person. Must survive maintainer changes.
- ❌ A replacement for critical thinking about the software under development.
- ❌ A clone of `github/spec-kit` with a regulatory sticker. We are independent and audit-grade-native.

---

## Contributing

Currently in **solo authoring phase** (pre-`v0.5.0`). External contributions will open as the toolkit stabilizes.

If you are a pharma-IT consultant, developer, auditor or open-source enthusiast and you want to follow or eventually contribute:

- Open an issue with your use case, the pain point you want addressed, or a regulatory clarification you need.
- Star and watch the repo (once it is public).
- Share with peers in your organization who deal with regulated software daily.

When external contributions open (planned around `v0.5.0` → `v1.0.0`), we will provide a `CONTRIBUTING.md` with templates for issues, PRs, new templates, new patterns and new skills.

---

## Acknowledgments

This project would not exist without the work of the broader open-source software and regulated-industries communities. Explicit inspirations (full details in [`docs/inspirations.md`](docs/inspirations.md)):

- **[github/spec-kit](https://github.com/github/spec-kit)** — the Constitution pattern, `[NEEDS CLARIFICATION]` markers, cross-artifact analyze concept, slash command namespace, runtime adapter philosophy.
- **[gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)** — STATE.md living-memory pattern, four canonical gate types (Confirm / Quality / Safety / Transition), fresh-context-per-agent spawn pattern, slopcheck against package hallucinations.
- **[bmad-code-org/bmad-method](https://github.com/bmad-code-org/bmad-method)** — named-agent personas concept, CSV-based help router for skill discovery, Diátaxis docs structure.
- **[buildermethods/agent-os](https://github.com/buildermethods/agent-os)** — lightweight index-as-router pattern, profiles-with-inheritance approach.

On the regulatory and methodological side:

- **ISPE GAMP 5 Second Edition (2022)** — the foundational framework.
- **FDA 21 CFR Part 11** — Electronic Records / Electronic Signatures.
- **EU GMP Annex 11 (2025 consultation)** and **Annex 22 (2025 consultation)**.
- **ICH Q9 (R1)** — Quality Risk Management.
- **PIC/S PI 041-1** — Data Integrity.
- **ISO/IEC 12207** — Software lifecycle processes.
- **OWASP ASVS** — Application Security Verification Standard.
- **ISO 25010** — Software product quality model.

---

## License

Licensed under the **Apache License 2.0** — see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).

Apache 2.0 was chosen (over MIT, CC0 and a dual Apache+CC-BY-SA arrangement) for three reasons specific to this toolkit: (1) a single permissive license lets the templates be **instantiated inside consumer projects — including proprietary, regulated ones — without contaminating them** (a share-alike clause on the templates would have been disqualifying for the primary use case); (2) the **explicit patent grant** matters to the enterprise/pharma legal teams who are the primary audience; (3) the NOTICE-file attribution preserves credit. The full rationale is recorded in the project memory and `STATE.md`.

---

*Authored as a personal initiative to bring spec-driven development methodology to AI-assisted software construction, anchored on published international standards (GAMP 5 / EU GMP / FDA 21 CFR Part 11), and to give the open-source community a foundation upon which to build the next generation of compliant, AI-native software tools.*
