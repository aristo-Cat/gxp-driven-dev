# Glossary — `gxp-driven-dev`

Concise definitions of the terms used across the toolkit, grouped by theme and alphabetical within each group. For deeper treatment see the companion docs: [`methodology.md`](methodology.md), [`v-model.md`](v-model.md), [`canonical-schemas.md`](canonical-schemas.md), [`requirement-id-scheme.md`](requirement-id-scheme.md).

---

## Frameworks, standards & regulations

**21 CFR Part 11** — US FDA regulation on Electronic Records and Electronic Signatures. Anchor for the `EREC` (§11.10 records, §11.30 closed/open systems) and `ESIG` (§11.100/§200/§300 signatures) requirement categories. Activated by `presets.part11_active`.

**ALCOA+** — The nine data-integrity attributes every GxP record must satisfy: **A**ttributable, **L**egible, **C**ontemporaneous, **O**riginal, **A**ccurate, plus **C**omplete, **C**onsistent, **E**nduring, **A**vailable. Anchored in EU Annex 11 §2.4 and PIC/S PI 041-1; enforced project-wide via the VMP's `alcoa_plus_enforcement` policy.

**CSV** — Computerized System Validation: the pharma discipline of proving (with documented evidence) that a computerized system does what it is intended to do and nothing else. The historical origin of the `templates/csv/` template family. (Not to be confused with comma-separated-values files.)

**EU Annex 11** — EU GMP Annex 11, "Computerised Systems." Anchor for many `OPS`, `SEC`, `ARCH`, `DATA`, `FLOW` requirements. The toolkit pins citations to the **2025-revised** edition, which adds explicit modernization vs the 2011 text: ALCOA+ §2.4, encryption / validated interfaces / validated migration §10, remote MFA §11.6 (new), independent audit-trail peer review §12.6, e-signature tamper-evidence §13.7–13.9.

**GAMP 5** — ISPE *Good Automated Manufacturing Practice 5, Second Edition (2022)* — the global reference for validating computerized systems in regulated pharma. The toolkit borrows its V-Model, 5-category framework, risk-based scaling (§M3), and role separation (§6.2.3) as the rigor source. The toolkit is **not certified to GAMP 5**; it adapts the structural rigor for AI-readable specs.

**GAMP category 1** — Infrastructure software (OS, network, DB platform, middleware). Qualified via `INFRA-QUAL`, not full URS→PQ validation.

**GAMP category 3** — Non-configured / standard products used as supplied ("off-the-shelf"). Lightweight specs; FS may fold into URS or VP.

**GAMP category 4** — Configured products. Configuration captured in a `CS` (Configuration Specification).

**GAMP category 5** — Custom / bespoke software built for the purpose. Full design layer (`DS`, plus develop-mode `ADR`/`API-SPEC`/`DBS`); highest rigor.

**GxP** — Umbrella for the "Good *x* Practices": GMP, GLP, GCP, GDP, GVP. A requirement marked `GxP=Y` is in regulatory scope and must be risk-assessed and (if critical) verified.

---

## V-Model & specification artifacts

**V-Model** — The lifecycle shape pairing each specification with the verification that proves it: URS↔PQ, FS↔OQ, DS/CS↔IQ (GAMP 5 §3.2 Fig 3.3). One valid shape, not a mandate — Agile is equally accepted (Fig 3.4). See [`v-model.md`](v-model.md).

**URS** — User Requirements Specification. The "what" from the regulated user's perspective; top of the left arm. Verified by the **PQ**. The only template (with FS) that carries regulatory `presets`.

**FS** — Functional Specification. The "how" that realizes the URS. Verified by the **OQ**. Inherits presets from the URS via `presets_inheritance`.

**CS** — Configuration Specification. Documents configured settings/parameters for a GAMP Cat 4 product. Verified at installation by the **IQ**.

**DS** — Design Specification. Detailed hardware/software design for GAMP Cat 5 custom software. Verified at installation by the **IQ**.

**IQ** — Installation Qualification (*installation verification*, GAMP Table 4.1). Confirms the system was installed in conformance with its DS/CS. Prerequisite of the OQ.

**OQ** — Operational Qualification (*functional verification*). Confirms the system functions as the FS specifies.

**PQ** — Performance Qualification (*fitness verification*). Confirms the system meets the URS in real-world conditions, using `PQ-SCEN-NNN` scenarios.

**RTM** — Requirements Traceability Matrix. **Derived** (never hand-edited) by `gdd.trace.validate`, which walks URS↔FS↔RA↔Tests references and reports orphans and coverage gaps.

**VR** — Validation Report. Closeout document summarizing IQ/OQ/PQ results; approved by the Quality Unit to declare the system validated.

---

## Risk & quality

**RA-INIT** — Initial Risk Assessment. Runs parallel to the URS; fixes the GAMP category and scales downstream rigor (GAMP 5 §M3 step 1; ICH Q9 R1). Uses two-segment IDs (`RA-INIT-NNN`).

**RA-DET** — Detailed Risk Assessment (Functional RA / FMEA). Performed after URS+FS approval; evaluates risk per realization and sets OQ verification intensity (`RA-DET-NNN`).

---

## Modes, profiles & rigor (manifest concepts)

**mode: develop** — Primary mode. The consumer builds new custom software; AI agents consume the specs as authoritative context when implementing. Activates the full design + test template set.

**mode: validate** — The consumer validates existing third-party software (vendor product, SaaS) by applying the same spec rigor. Activates a lean set plus the SaaS bundle when relevant.

**mode: hybrid** — The most realistic case: vendor components + custom integrations, declared via `hybrid_breakdown`. Vendor parts run the Validate flow, custom parts the Develop flow; the RTM is unified.

**profile** — Domain selector in `.gxp-dev.yaml` (`pharma`, `medical-device`, `finance`, `aerospace`, `nuclear`, `general`). Drives which regulatory anchors a template surfaces (the multi-industry anchor system) and which agent personas/roles apply. Profiles support inheritance (`inherits_from: default`).

**rigor_level** — How much validation rigor to apply, independent of profile:
- **light** — freelance MVP; minimal ceremony.
- **standard** — enterprise B2B tooling.
- **strict** — startup in a regulated market; day-one inspection readiness.
- **regulated** — full FDA / EMA-grade validation.

---

## Toolkit conventions

**anti-leak guard** — `skills/_scripts/anti-leak-guard.py`, run by CI. Enforces the geographic anonymization rule: greps the toolkit tree for source-organization names, corporate document codes, corporate ID schemes, site codes, and non-English heritage terms, and **fails the build** if any appear outside a small allowlist of governance files. Keeps the public product 100% anonymous.

**generative cascade** — The toolkit's first-class pipeline: `idea → URS → RA-INIT → FS → RA-DET → tests → code → bundle`. Each step is a discrete skill that proposes a draft; a human reviews and advances status (`draft → in-review → approved`). The agent never invents requirements, IDs, or regulatory citations — it reads upstream specs and drafts the matching downstream artifact.

**`[NEEDS CLARIFICATION: …]` marker** — The canonical convention (borrowed from spec-kit) used when an AI agent cannot fill a placeholder. Instead of inventing a value, the agent inserts the marker for a human to resolve later via an interactive skill. Detected by `skills/_scripts/check-clarification-markers.py`.

**presets / presets_inheritance** — Conditional template-frontmatter blocks for regulatory control sets. Only the **URS** declares `presets` (it decides applicability); only the **FS** carries `presets_inheritance` (it realizes each active preset). All other templates omit them. See [`canonical-schemas.md`](canonical-schemas.md).

---

## The 22 canonical category acronyms

The fixed building blocks of requirement classification (`<DOC>-<CAT>-<NNN>`). The set is intentionally frozen — adding categories breaks downstream traceability. Full anchors in [`requirement-id-scheme.md`](requirement-id-scheme.md).

| Acronym | Category (brief) |
|---|---|
| `FUNC` | Functional — core business functions |
| `PERF` | Performance — response time, throughput, capacity |
| `QUAL` | Quality — QA, programming standards, config mgmt |
| `TRAIN` | Training — for developers, end-users, support |
| `DEVENV` | Development environment — tools, IDE, repos (Cat 5) |
| `DATA` | Data structure — model, schemas, retention, integrity |
| `FLOW` | Data flow — movement between components |
| `REPORT` | Reports / printouts — format, audience |
| `SEC` | Security — access control, encryption, attack surface |
| `PROC` | Process organization — SOPs, roles, org impact |
| `UI` | User Interface — standards, accessibility, errors |
| `API` | Interfaces / APIs — integrations (receiver's view) |
| `MIGR` | Data migration — from legacy systems |
| `ARCH` | Archiving — retention, media, retrieval |
| `OPS` | System operations — incident, change, backup, monitoring |
| `DOCS` | Documentation — manuals, SOPs, runbooks |
| `TEST` | Testing — test data, load tests, simulation |
| `DELIV` | Deliverables — supplier scope of supply |
| `PERIPH` | Peripherals — terminals, scanners, printers |
| `HW` | Hardware design — CPU, RAM, storage, network |
| `EREC` | Electronic Records — 21 CFR Part 11 §10 |
| `ESIG` | Electronic Signatures — 21 CFR Part 11 §100–§300 |

---

## Related

- [`v-model.md`](v-model.md) · [`canonical-schemas.md`](canonical-schemas.md) · [`requirement-id-scheme.md`](requirement-id-scheme.md)
- [`methodology.md`](methodology.md) · [`project-layout.md`](project-layout.md) · [`inspirations.md`](inspirations.md)
