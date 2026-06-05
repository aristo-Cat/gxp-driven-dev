# Canonical schemas — the data contracts the toolkit relies on

`gxp-driven-dev` is **markdown-and-YAML-first**: the structure that makes specs machine-readable lives in four data contracts. This document is the precise reference for all four.

1. **Template frontmatter schema** — the YAML at the top of every `templates/csv/<ID>.md`.
2. **Instance frontmatter schema** — the YAML at the top of an instantiated spec in a consumer's `specs/<ID>.md`, declared by each template's `instance_frontmatter_spec` block.
3. **`.gxp-dev.yaml` manifest schema** — the consumer-repo root manifest skills read first.
4. **Requirement-ID grammar** — the identifier syntax that carries traceability across the V-Model.

Companion docs: phase mapping → [`v-model.md`](v-model.md); ID rationale → [`requirement-id-scheme.md`](requirement-id-scheme.md); consumer repo layout → [`project-layout.md`](project-layout.md); term definitions → [`glossary.md`](glossary.md).

> [!note] Why typed frontmatter (vs `[BRACKET]` placeholders)
> A bare `[BRACKET]` placeholder cannot be validated or interactively filled. The toolkit mandates **typed declarative placeholders** so an agnostic skill can know what to ask, validate completeness, and flag gaps. This is the audit-grade differentiator over prose-only spec tools (see [`inspirations.md`](inspirations.md)).

---

## 1. Template frontmatter schema

Every canonical template carries this frontmatter. Blocks are **required** unless marked conditional. Reference instances: [`URS.md`](../templates/csv/URS.md), [`FS.md`](../templates/csv/FS.md), [`IQ.md`](../templates/csv/IQ.md), [`VMP.md`](../templates/csv/VMP.md).

### 1.1 Metadata block (required)

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | string | ✅ | Human-readable template title |
| `type` | const `template` | ✅ | Distinguishes a template from an instance (`instance`) |
| `template_class` | enum (`csv`, …) | ✅ | Template family directory (`csv` during Sprint 2) |
| `template_id` | string (acronym) | ✅ | The DOC-TYPE prefix this template owns (`URS`, `FS`, `IQ`, …) |
| `template_version` | semver | ✅ | Version of the template itself (e.g. `0.1.0`) |
| `v_model_phase` | string | ✅ | V-Model position (`requirements-definition`, `functional-specification`, `installation-verification`, `planning`, …) |
| `lifecycle_phase` | enum(concept/project/operation/retirement) | ⚠️ optional | Present on master/governance templates (e.g. VMP); see [`v-model.md`](v-model.md) |
| `template_family` | string | ⚠️ optional | Grouping label (e.g. `master` for VMP) |
| `gamp_categories_applicable` | list(int) | ✅ | Which GAMP categories this template applies to (e.g. `[3, 4, 5]`) |
| `language` | enum(en/es/de/…) | ✅ | Language of the template body (canonical = `en`) |
| `status` | enum | ✅ | Template lifecycle (`canonical-draft`, `canonical`, …) |
| `created` | date (YYYY-MM-DD) | ✅ | Creation date |
| `updated` | date (YYYY-MM-DD) | ✅ | Last-modified date |
| `tags` | list(string) | ✅ | Discovery tags |

### 1.2 Pipeline block — V-Model neighbours (required)

Declares the template's place in the generative cascade.

| Field | Type | Required | Description |
|---|---|---|---|
| `inputs` | list(object) | ✅ (may be `[]`) | Upstream templates this one consumes |
| `inputs[].template_id` | string | ✅ | Upstream DOC-TYPE |
| `inputs[].required` | bool | ✅ | Whether the input is mandatory |
| `inputs[].description` | string | ✅ | What the input provides |
| `outputs` | list(object) | ✅ | What this template produces and who consumes it |
| `outputs[].artifact` | string | ✅ | Name of the produced artifact |
| `outputs[].consumed_by` | list(string) | ✅ | Downstream DOC-TYPEs |
| `applicable_regulations` | list(string) | ✅ | Regulation slugs (`gamp-5`, `21-cfr-part-11`, `eu-annex-11`, `ich-q9`, …) |
| `based_on` | list(string) | ✅ | Provenance notes (anonymized) |

### 1.3 Placeholders block (required)

A map of `{{variable}}` substitution points. Each entry is a typed declarative descriptor:

| Sub-field | Type | Required | Description |
|---|---|---|---|
| `type` | enum(string/enum/boolean/int/list/map) | ✅ | Placeholder value type |
| `required` | bool | ✅ | Whether a skill must fill it before the instance is complete |
| `description` | string | ⚠️ recommended | What to ask the user |
| `values` | list | conditional | Allowed values — required when `type: enum` |
| `example` | string | optional | Few-shot hint for the instantiation skill |
| `pattern` | regex | optional | Validation pattern for free-text fields |

### 1.4 Presets / presets_inheritance block (**CONDITIONAL**)

> [!warning] This block is conditional — most templates omit it
> Only the **root specs that decide or inherit regulatory preset applicability** carry a preset block. **`URS` declares `presets`** (it *decides* which Part 11 / Annex 11 control sets apply). **`FS` carries `presets_inheritance`** (it *inherits* the URS decision and realizes each active preset). **All other templates** — design specs, test protocols, operational records, governance — **omit the block entirely**; they neither decide nor inherit presets.

`presets` (URS only) — a map of activatable control sets:

| Sub-field | Type | Description |
|---|---|---|
| `<preset-name>` | object | e.g. `URS-EREC`, `URS-ESIG`, `URS-SEC-modern`, `URS-API-valid`, `URS-MIGR-valid` |
| `<preset>.description` | string | What the preset bundles (with citation count) |
| `<preset>.activation_question` | string | The yes/no question a skill asks to decide activation |
| `<preset>.if_inactive_action` | string | What to write when the preset is N/A (keep section, mark reason) |

`presets_inheritance` (FS only) — declares that each active URS preset must be realized:

| Sub-field | Type | Description |
|---|---|---|
| `rule` | string | The inheritance rule (each active `URS-<X>` → ≥1 `FS-<X>` realization) |
| `part11_records` / `part11_signatures` / `annex11_security` / `annex11_interfaces` / `annex11_migration` | string | Per-preset realization obligation |

### 1.5 instance_frontmatter_spec block (required)

Declares the shape the **instance** must take when this template is instantiated. See §2.

### 1.6 validation_rules block (required)

A list of plain-English assertions a linter / skill checks before the instance can advance status (e.g. *"traces_to must point to an approved URS"*). Round 1 ships a subset; a formal schema lands later.

---

## 2. Instance frontmatter schema

When a skill instantiates a template, the resulting `specs/<ID>.md` file's frontmatter must follow that template's `instance_frontmatter_spec`. The pattern is consistent across templates; specific required/conditional fields vary.

### 2.1 Common required fields

Present in essentially every instance (drawn from URS/FS/IQ/VMP):

| Field | Type | Description |
|---|---|---|
| `title` | string | Instance title (names the real system) |
| `type` | const `instance` | Marks this as an instance, not a template |
| `based_on_template` | string | DOC-TYPE of the source template (`URS`, `FS`, …) |
| `based_on_template_version` | semver | Template version this instance was generated from |
| `system_id` / `project_id` | string | Identifier of the system or project |
| `status` | enum | Instance lifecycle — see §2.3 |
| `version` | semver | The instance's **own** version (e.g. `1.0`, `1.1`) |
| `created` | date | Creation date |
| `updated` | date | Last-modified date |
| `language` | enum(en/es/de/…) | Language of the instance body |

### 2.2 Per-template required + conditional fields

| Template | Adds to required | Conditional fields |
|---|---|---|
| `VMP` | `project_id` | `approved_by` (if `approved`); `supersedes` (if a revision) |
| `URS` | `system_id` | `approved_by`; `supersedes`; `preset_part11_active` (bool — true if URS-EREC/ESIG active) |
| `FS` | `system_id`, `traces_to` (URS instance + version) | `approved_by`; `supersedes`; `deviations_logged` (bool) |
| `IQ` | `system_id`, `traces_to` (DS/FS), `gamp_category` | `executed_by`; `reviewed_by`; `execution_date`; `partial_test_ref`; `deviations_count` |

> [!tip] `traces_to` is the backward-reference spine
> Any spec below the root declares `traces_to` pointing at the approved upstream instance it realizes/verifies. This is what makes the derived **RTM** possible and what the anti-orphan rule enforces (every spec traceable forward *and* backward — see [`requirement-id-scheme.md`](requirement-id-scheme.md)).

### 2.3 Status lifecycle

Specification instances:

```
draft → in-review → approved → superseded
```

Verification (qualification) instances add execution states:

```
draft → in-execution → executed → approved → superseded
```

- `draft` / `in-review`: free editing.
- `approved`: any change requires bumping `version` and marking the prior as `superseded` (with `supersedes:` pointing back). The "no deletion, only strike-through" rule applies to obsolete rows within an active version.

---

## 3. `.gxp-dev.yaml` manifest schema

The declarative root file in the **consumer** repository. `gdd.init` writes it; `gdd.trace.validate` and CI gates read it. Full worked example in [`project-layout.md`](project-layout.md).

| Field | Type | Required | Description |
|---|---|---|---|
| `gxp_dev_version` | semver-range | ✅ | Toolkit version constraint the consumer expects |
| `project_id` | string | ✅ | Internal project identifier |
| `project_name` | string | ✅ | Human-readable project name |
| `language` | enum(en/es/de/…) | ✅ | Language of instantiated specs |
| `mode` | enum(`develop`/`validate`/`hybrid`) | ✅ | How the toolkit is used (see §3.1) |
| `lifecycle` | enum(`v-model`/`agile`/`hybrid`) | ✅ | Shape of the SDLC |
| `gamp_category` | enum(`1`/`3`/`4`/`5`) | if `profile == pharma` | GAMP 5 §M4 categorization |
| `lifecycle_phase` | enum(concept/project/operation/retirement) | ✅ | Current GAMP 5 §3.1 phase |
| `profile` | enum(pharma/medical-device/finance/aerospace/nuclear/general) | ✅ | Domain profile — drives which regulatory anchors are active |
| `rigor_level` | enum(`light`/`standard`/`strict`/`regulated`) | ✅ | Severity of validation checks (see §3.2) |
| `id_scheme` | enum(`canonical`/`custom`) | ✅ | Requirement-ID naming strategy |
| `custom_alias` | map(DOC-TYPE → string) | if `id_scheme == custom` | Per-DOC-TYPE prefix override (categories are **not** aliasable) |
| `presets` | map(string → bool) | optional | Activate canonical preset blocks: `part11_active`, `annex11_active`, `gdpr_active`, `annex22_active`, … |
| `templates_active` | list(acronym) | ✅ | Subset of the 33 canonical templates to instantiate |
| `outputs` | map(string → bool) | ✅ | Which bundles to produce: `specs`, `code`, `tests`, `compliance_bundle` |
| `hybrid_breakdown` | object | if `mode == hybrid` | Vendor + custom component split, each with its own `gamp_category` + `templates_active` |

### 3.1 `mode`

| Value | Meaning | Typical `templates_active` |
|---|---|---|
| `develop` | Build new custom software; AI agents read specs as authoritative context | URS · FS · DS · ADR · API-SPEC · DBS · UC · AC · CR · UT-PLAN · IT-PLAN · SEC-TEST · PERF-TEST · IQ · OQ · PQ · RTM · VR · RN · DEPLOY-RUN |
| `validate` | Validate existing third-party software with the same rigor | URS · CS · SUP-ASSESS · IQ · OQ · PQ · RTM · VR · (+ SaaS bundle) |
| `hybrid` | Vendor components + custom integrations | both sets, split via `hybrid_breakdown` |

### 3.2 `rigor_level`

| Value | Intended use |
|---|---|
| `light` | Freelance MVP — minimal ceremony |
| `standard` | Enterprise B2B tooling |
| `strict` | Startup in a regulated market — day-one inspection readiness |
| `regulated` | Full FDA / EMA-grade validation |

> [!note] Audit-safe default — "absent = strictest"
> The manifest inverts the common "absent = enabled" convention: when a rigor-affecting field is absent, skills assume the **strictest** interpretation, never the most permissive. This prevents an omission from silently downgrading validation rigor.

### 3.3 `hybrid_breakdown` (only when `mode: hybrid`)

| Field | Type | Description |
|---|---|---|
| `vendor_components` | list(object) | Each vendor component: `name`, `gamp_category`, `templates_active` (Validate flow) |
| `custom_components` | list(object) | Each custom component: `name`, `gamp_category`, `templates_active` (Develop flow) |

The RTM is unified across both sets.

---

## 4. Requirement-ID grammar

Stable, machine-parseable, diff-friendly identifiers carry traceability across the lifecycle. Four forms exist; full rationale in [`requirement-id-scheme.md`](requirement-id-scheme.md).

| Form | Grammar | Used by | Example |
|---|---|---|---|
| **Three-segment** (categorized requirement) | `<DOC>-<CAT>-<NNN>` | URS, FS, CS, DS, API-SPEC, DBS rows | `URS-FUNC-001`, `FS-API-002`, `DS-DATA-005` |
| **Two-segment** (finding / step / register row) | `<DOC>-<NNN>` | RA-INIT, RA-DET, DPIA findings, DECOM-PLAN steps | `RA-INIT-001`, `RA-DET-014`, `DPIA-007` |
| **Test sub-prefix** | `<DOC>-TC-<NNN>` / `<DOC>-SCEN-<NNN>` | IQ/OQ/UT-PLAN/IT-PLAN/SEC-TEST/INFRA-QUAL (`TC`); PQ scenarios (`SCEN`) | `IQ-TC-042`, `OQ-TC-021`, `PQ-SCEN-007`, `DECOM-PLAN-TC-003` |
| **Year-variant** (operational record) | `<DOC>-<YYYY>-<NNN>` | CC, IR, BRR, UAR | `CC-2026-038`, `IR-2026-012` |

**Segment definitions:**

| Segment | Rule |
|---|---|
| `<DOC>` | The DOC-TYPE prefix that owns the ID (also the file prefix). May be compound (`RA-INIT`, `RA-DET`, `DECOM-PLAN`, `UT-PLAN`). |
| `<CAT>` | One of the **22 canonical categories** (`FUNC`, `PERF`, `EREC`, `ESIG`, `SEC`, `API`, …). Mandatory in URS/FS/DS; recorded inside test-case content, not in the test ID. |
| `<NNN>` | Sequential, 3-digit zero-padded, starting at `001`. Each `<DOC>-<CAT>` (or `<DOC>` for two-segment) has its own counter. |
| `<YYYY>` | 4-digit year, for operational records only. |

> [!note] Parser awareness
> The parser in `skills/_scripts/lib/gdd_common.py` treats `INIT`, `DET`, `TC`, `SCEN` as **non-category** middles so compound DOC-TYPEs do not report phantom categories. Non-requirement table rows that are not the document's primary entity take a plain local label (`D1`, `D2`, …) to avoid colliding with the `<DOC>-<NNN>` finding counter.

### 4.1 Forward + backward traceability

- The category travels with the requirement to the right side of the V: `URS-FUNC-001` → `FS-FUNC-001` → `DS-FUNC-005` → verified by an `OQ-TC-NNN` (which names the FS-ID in its content).
- Cardinality `1:1`, `1:N`, `1:0` is allowed; `1:0` only for `GxP=N` requirements (a `GxP=Y` / `prio=H` requirement with no downstream realization is a **blocking orphan**).
- Every spec ID must be traceable **forward** (to consumers) and **backward** (to sources). `generate-rtm` walks these references to derive `specs/RTM.md`.

### 4.2 Consumer override (`id_scheme: custom`)

Consumers with pre-existing naming conventions alias **DOC-TYPE prefixes** (not categories) via `custom_alias` in `.gxp-dev.yaml`. Skills translate `URS-FUNC-001` → `REQ-USER-FUNC-001` at instantiation. The 22 categories are intentionally **not** aliasable — they are the shared spine of traceability.

---

## Related

- [`requirement-id-scheme.md`](requirement-id-scheme.md) · [`v-model.md`](v-model.md) · [`glossary.md`](glossary.md)
- [`project-layout.md`](project-layout.md) · [`methodology.md`](methodology.md) · [`inspirations.md`](inspirations.md)
