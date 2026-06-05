# gxp-driven-dev — AI Agent Contract (AGENTS.md)

`AGENTS.md` is the single source; `CLAUDE.md` imports it via `@AGENTS.md`. This file is the agent's
**work contract**, not the project's encyclopedia — that is `README.md`.

## What this is

Open-source, vendor-agnostic **spec-driven development toolkit**: pharma-grade specs
(Markdown + YAML frontmatter) become authoritative context so any LLM builds & verifies
software with anti-hallucination grounding. Compliance documentation is a **side-effect**,
not the goal.

**Objective:** turn an idea into audit-grade specs + verified software through one
traceable cascade — URS → FS → DS → tests → IQ/OQ/PQ → RTM.

**Priorities (in order):**
1. **Anonymity** — never leak source-org identity (Anonymization rule below; CI-enforced)
2. **Traceability & verifiability** — every requirement carries an ID and a test
3. **Vendor-agnostic clarity** — Claude / GPT / Gemini / Llama read the same specs
4. **Polish**

**How it runs:** skills in `skills/<name>/SKILL.md` drive the cascade; consumer config
in `.gxp-dev.yaml`. Full project map, audiences, and "what this is NOT" → `README.md`.
Repo layout detail → `docs/project-layout.md`.

## How to work

Behavior, not knowledge — these turn typical agent failures into rules. Test: given a vague task, a
compliant agent asks instead of charging ahead.

- Restate the objective in one line before editing; if it is ambiguous, **ask** — don't pick a reading and run.
- Make the **smallest change** that fulfills the task; don't refactor or "improve" nearby templates, skills, or docs unless asked.
- **Never invent — mark.** When you can't answer (an ID, a regulatory citation, a category, a value), write `[NEEDS CLARIFICATION: …]` instead of guessing; surface doubts rather than choosing in silence.
- **Read the canonical source before editing anything derived from it** — the template before the skill that instantiates it; `docs/requirement-id-scheme.md` before touching IDs.
- No new template / skill / pattern / script / dependency unless it is used in 3+ places, or you were asked.
- **Durable lessons live in `MEMORY.md`.** Read it before non-trivial work; when a lesson emerges that will matter again in ~30 days, propose an entry there (no secrets, no org data). It is auditable, in-Git memory — not state.

## Long work

For complex or multi-file work (a cascade refactor, changing the ID scheme or the 22 categories, editing
many templates at once): write a short **phased plan first** — one verifiable objective per phase, each
phase reversible — and **wait for approval before implementing**. Don't write a big objective as a single
plan; split it into phases and review each before releasing. Track the active plan in `STATE.md` and keep
it updated as you go.

## Configuration layers (keep them separate)

Three concerns, three homes — never mix them in this file:

| Layer | Lives in | Examples |
|---|---|---|
| Personal style | global, per-developer (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`) — never in this repo | "be brief", "show diffs first", identity / voice |
| Team conventions | this file (`CLAUDE.md` / `AGENTS.md`) + `docs/` | the anonymization rule, ID scheme, the cascade, "stop and ask" |
| Machine permissions | `.githooks/` (git enforcement) + harness config — examples in `adapters/machine-permissions.md` | the git-push lock, allow the `_scripts/` gates, forbid `rm -rf` |

Personal preferences are global so they apply across *all* your projects; this repo file carries only the
conventions every contributor must follow. Machine permissions are enforced, not asked — see
`.githooks/README.md` for the four-layer map.

## Relationship to the source knowledge base

This folder is the **canonical product distilled from a personal knowledge base** of regulations,
concepts, SOP summaries and GAMP 5 patterns — generalized for any software context.
**Everything here must be 100% anonymous** — see below.

### Anonymization rule (NON-NEGOTIABLE)

This is an open-source toolkit: it must never carry the identity of any organization a contributor
distilled it from. Banned categories:

| Banned | Reason | Replacement |
|---|---|---|
| Any source-organization name | Confidentiality | "the organization", "the regulated company", or remove |
| An organization's internal document codes (letter-prefixed IDs) | Org-specific document identifiers | Remove, or use a placeholder like `{{org_csv_policy_ref}}` |
| An organization's internal system / ID scheme | Org-specific ID schema | Generic placeholder `{{system_id}}` |
| An organization's physical site codes / abbreviations | Org-specific site identifiers | Use `{{site_code}}` |
| Non-English heritage terms inherited from a source template | Implies a specific non-English origin | English equivalent |
| Legacy category codes inherited from a source organization | Inherited corporate nomenclature | Use the 22 canonical acronyms in `docs/requirement-id-scheme.md` (FUNC, EREC, ESIG, …) |
| Wikilinks to a contributor's private/internal source documents | Cross-links to private content | Remove |

A **CI anti-leak guard** (`skills/_scripts/anti-leak-guard.py`, run by `.github/workflows/lint.yml`)
blocks these automatically. It ships as a **generic engine**; organization-specific terms are supplied
locally via a git-ignored overlay (`skills/_scripts/.leak-overlay.txt`) or the `LEAK_OVERLAY` env var,
so the public repo never names anyone. Local git hooks in `.githooks/` wrap the same guard: `pre-commit`
runs it (plus the `CLAUDE.md`-is-`@AGENTS.md`-stub check and staged-frontmatter validation) and `pre-push`
hard-blocks publishing until the git history is verified clean. Activate per clone with
`sh .githooks/install.sh` (sets `core.hooksPath`). See `.githooks/README.md`.

## Languages

- **Primary product language: English** — for international reach in the dev/pharma-IT community.
- **Spanish secondary translations welcome** but optional.
- Internal AI-assist conversations and commit messages may be in Spanish; user-facing files
  (templates, README, docs, skills) in English.

## Operational modes

The consumer's `.gxp-dev.yaml` declares a `mode` that scopes which templates are active:

| Mode | When | Typical templates |
|---|---|---|
| `develop` | **Primary**. Consumer builds new custom software; agents read specs as authoritative context | URS · FS · DS · ADR · API-SPEC · DBS · UC · AC · CR · UT-PLAN · IT-PLAN · SEC-TEST · PERF-TEST · IQ · OQ · PQ · RTM · VR · RN · DEPLOY-RUN |
| `validate` | Secondary. Consumer validates existing third-party software (vendor product, SaaS) | URS · CS · SUP-ASSESS · IQ · OQ · PQ · RTM · VR · plus SaaS bundle when applicable |
| `hybrid` | Most realistic. Consumer has vendor components + custom integrations | Both sets, declared via `hybrid_breakdown` |

## Requirement ID scheme

Every requirement is `<DOC-TYPE>-<CATEGORY>-<NNN>` — e.g. `URS-FUNC-001` → `FS-FUNC-001` →
`DS-FUNC-005` (1:M) → `OQ-TC-042`. The 22 canonical categories and the full format spec live in
`docs/requirement-id-scheme.md`. Consumers with internal conventions opt out via
`id_scheme: custom` + `custom_alias` in `.gxp-dev.yaml`.

## Workflow conventions

- **Templates** under `templates/csv/` use canonical frontmatter declared by their `template_id`
  (acronym, e.g. `URS`, `VMP`, `FS`). Required blocks: `placeholders`, `validation_rules`,
  `inputs/outputs`, `instance_frontmatter_spec`. The `presets` / `presets_inheritance` block is
  **conditional** — only the root specs that decide or inherit regulatory preset applicability carry
  it (`URS` declares `presets`; `FS` uses `presets_inheritance`); downstream specs, test protocols
  and operational records omit it.
- **Placeholders** use Mustache-like `{{variable_name}}` — substituted by skills at instantiation.
- **Requirement IDs** follow the scheme above (`docs/requirement-id-scheme.md`).
- **Skills** live in `skills/<skill-name>/SKILL.md` with Claude Code frontmatter (`name`,
  `description`). Auxiliary scripts in `skills/_scripts/*.py` (Python 3.12+ + PyYAML).
- **Wikilinks** — during development against the source vault, internal references may use Obsidian
  wikilink syntax; files destined for public release must convert these to relative Markdown links
  (in-repo targets) or plain text / absolute URLs (vault-only pages) before publishing.
- **`[NEEDS CLARIFICATION: …]` markers** are the canonical pattern (from `github/spec-kit`) when an
  agent cannot answer a placeholder and needs human input later.

## Out of scope for this folder

- Citing corporate SOPs verbatim, or anything tied to a specific source organization's workflows,
  sites, codes, or internal procedures → parent wiki only, never here.
- Operational eQMS features (workflow runtime, approval routing, retention scheduling) → out of scope
  entirely; use TrackWise/Veeva/MasterControl for that.

## Do NOT introduce unless asked

A "no" list is not a whim — it is a compressed registry of decisions. The **Reason** says why the
rule exists; the **Revisit** says when it is fair to reconsider it.

| Do NOT introduce | Reason | Revisit |
|---|---|---|
| Python dependencies beyond PyYAML (`skills/_scripts/`) | scripts must run on any clean Python 3.12+ and in the consumer's CI; `requirements.txt` is `PyYAML>=6.0` only — minimal supply-chain surface | only if a capability is genuinely impossible with stdlib + PyYAML — propose it first |
| A new requirement-ID category (beyond the 22 canonical) | the 22 acronyms are the fixed anonymized set that replaced corporate codes; new ones break RTM traceability and risk re-introducing corporate nomenclature | only via a discussed update to `docs/requirement-id-scheme.md` |
| A new template (beyond the 33 canonical) | the catalog is curated and V-model-mapped; ad-hoc templates fragment the cascade | only when a real lifecycle gap is identified and agreed |
| A second manifest format or placeholder/templating engine | one `.gxp-dev.yaml` + Mustache-like `{{ }}` keeps skills portable and AI-agnostic | only if multi-format consumer support is prioritized |
| Single-vendor (e.g. Claude-only) features in core templates/skills | AI-agnosticism is non-negotiable (Anti-goal #1) | never in core — vendor specifics live only in `adapters/` |
| Build tooling / heavy frameworks (Node build, committed lockfiles, docs-site generator) | the toolkit is plain Markdown + small scripts; build tooling adds maintenance + supply-chain surface | only at public-release polish, if a concrete need appears |

## Stop and ask before

"Stop and ask" is not a prohibition — it says: **this decision is not only yours.**

- Renaming, deleting, or restructuring any of the 33 canonical templates (or their acronyms) — it breaks every consumer project and the RTM.
- Changing the requirement-ID scheme or the 22 canonical categories.
- Weakening a template's `validation_rules`, a preset, or a regulatory citation **just to make `lint-spec` / `validate-frontmatter` pass** — never edit the gate to go green.
- A sweep touching many templates/skills at once, or a single diff larger than ~400 lines.
- `git push` or making the repo public — no remote exists yet; the first publish is irreversible anonymization exposure, and the anti-leak guard must be green first.
- Deleting or overwriting anything outside this repository — the toolkit is distilled from a separate private knowledge base whose paths sit above the repo root and have no version control of their own, so a mistake there is effectively irreversible.
- Changing `LICENSE` / `NOTICE`, the anti-goals, or the anonymization rule.

## What "done" means

A change to this toolkit is done only when the deterministic gates in `.github/workflows/lint.yml`
pass locally — never claim completion on the model's say-so alone. Run what applies to what you touched:

1. `python skills/_scripts/anti-leak-guard.py` — always (BLOCKING; expect `0 leaks`).
2. Templates changed → `python skills/_scripts/validate-frontmatter.py --dry-run templates/csv/<X>.md`.
3. Example specs changed → `validate-frontmatter.py <file>`, then
   `generate-rtm.py --specs-dir <example>/specs` (must report 0 dangling refs), then
   `check-clarification-markers.py --all --draft --specs-dir <example>/specs`.

Report results in this **final-response format**: (1) files changed; (2) what changed and why;
(3) verification run — with results; (4) verification NOT run — with the reason; (5) risks or open
items that remain. This echoes the toolkit's own Verification Report (`VR`) artifact.

## Context — read when applicable

This file is an index, not a library — deeper detail lives in `docs/` and loads on demand. Read only when relevant:

- Methodology (why pharma rigor for general dev) → `docs/methodology.md`
- Consumer project layout + `.gxp-dev.yaml` manifest → `docs/project-layout.md`
- Requirement-ID scheme (22 categories, full format) → `docs/requirement-id-scheme.md`
- Template ↔ V-Model phase mapping → `docs/v-model.md` · data schemas → `docs/canonical-schemas.md`
- Glossary → `docs/glossary.md` · reference frameworks / adoption matrix → `docs/inspirations.md`
- Living memory (decisions, current state) → `STATE.md` · durable lessons (traps, fixes) → `MEMORY.md` · private working journal → `PROGRESS.md`
- Project map, audiences, status & roadmap, contribution, license → `README.md` (+ `LICENSE` / `NOTICE`)

## Evolution

This contract evolves with the project. When something doesn't fit — a missing convention, a brittle
structure, a workflow that breaks — flag it, discuss, and update `AGENTS.md` (`CLAUDE.md` just imports it via `@AGENTS.md`).
