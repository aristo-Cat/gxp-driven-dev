# Inspirations — what we learned from related frameworks

This document records the **explicit lessons** `gxp-driven-dev` extracted from five reference open-source frameworks during early scaffolding (2026-05-24, the 2026-05-25 reframe, and the 2026-05-29 Builder Methods study), how each lesson maps into the design of this toolkit, and the **5-tier adoption matrix** (Cat 0/A/B/C/D) that governs our roadmap.

We investigated:
- **[github/spec-kit](https://github.com/github/spec-kit)** — GitHub's official spec-driven development toolkit (~105k stars).
- **[gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)** — A multi-agent meta-prompting + spec-driven framework.
- **[bmad-code-org/bmad-method](https://github.com/bmad-code-org/bmad-method)** — A structured methodology with named agent personas.
- **[buildermethods/agent-os](https://github.com/buildermethods/agent-os)** — A lightweight standards/context router for AI agents.
- **[buildermethods/bm-skills](https://github.com/buildermethods/bm-skills) + [build-new](https://github.com/buildermethods/build-new)** — Brian Casel's spec-driven-development skill (`bm-prd-creator`) and starter boilerplate. *Same author as agent-os (Framework 4); studied separately because it is the first reference that is **non-technical-audience-first** and **visual-output-first**, and is a shipped, operative implementation of the exact front-of-funnel skill we are building.*

For each framework we document: what it is, concepts we adopt (with concrete mapping), concepts we explicitly reject (anti-patterns), and one surprise. The **adoption matrix** at the top is the authoritative source of "what's in / what's deferred / what's unique to us".

---

## Adoption matrix (5-tier)

The adoption matrix captures every lesson extracted from the four frameworks plus the unique innovations that don't come from any of them. Each item is classified by **when** it enters the toolkit.

### 🔴 Cat 0 — Core value proposition (`v0.1.0` essentials)

These are the non-negotiable foundations. Without them, the toolkit doesn't deliver its promise.

| Concept | From | How we adopt it |
|---|---|---|
| **Lightweight index router** | agent-os | `.gxp-dev.yaml` manifest = single declarative entry-point. An AI agent reads it first to know `mode`, `profile`, `templates_active`, `presets`, instead of scanning every spec file. |
| **7-state lifecycle** (constitution→specify→clarify→plan→tasks→analyze→implement) | spec-kit | We adapt to the **generative cascade**: idea → URS → RA-INIT → FS → RA-DET → tests → code → bundle. Same idea: explicit states the AI agent can advance one at a time. |
| **STATE.md living memory** | gsd-build | We **dogfood** the pattern: this toolkit's own `STATE.md` documents its development. Consumer projects keep their own `STATE.md` at root with YAML frontmatter (`active_phase`, `next_action`, `progress.percent`) parseable by tooling. |
| **Fresh-context-per-agent** | gsd-build | Each skill that spawns a sub-agent (e.g. independent code review, audit) gives it a clean context window. The orchestrator stays thin. |
| **Plan-checker loop** | gsd-build | Skills produce drafts; humans (or another agent with a different role/profile) review before commit. Max iterations bounded to prevent runaway. |
| **Slopcheck / anti-hallucination defenses** | gsd-build | Skills must never invent IDs, never invent regulatory citations, never invent package names. Verified by `skills/_scripts/check-clarification-markers.py` and CI grep guards. |
| **"What vs how" boundary as a first-class principle** | bm-prd-creator | A spec (URS/FS) is a *what* document: user-facing behavior, scope boundaries, data the system must remember, named stack + named integration providers. It is **not** a *how* document: no library choices beyond the stack, no method names, no internal logic, no timeout/retry/parsing decisions. Those belong to the agent in plan mode per cascade step. Articulated crisply by `bm-prd-creator` with worked examples; we adopt the language verbatim into `docs/methodology.md`. |

### 🟢 Cat A — Round 1 blocking (Sprint 2)

These are required before the toolkit is publicly usable.

| Concept | From | How we adopt it |
|---|---|---|
| **VMP as Constitution** | spec-kit + gsd-build | `templates/csv/VMP.md` plays the dual role of (a) Validation Master Plan in GAMP terms and (b) the consumer's "constitution" listing immutable principles (criticality classification, signature workflow, ALCOA+ enforcement, supplier qualification policy). |
| **`[NEEDS CLARIFICATION: …]` markers** | spec-kit | Canonical convention when an agent can't fill a placeholder — instead of inventing, mark for human review. A later interactive skill resolves them. |
| **Slash command namespace `gdd.*`** | spec-kit + gsd-build | All toolkit skills prefixed: `/gdd.urs.from-idea`, `/gdd.fs.from-urs`, `/gdd.trace.validate`, etc. Mirrors `github/spec-kit`'s `/speckit.*` convention. |
| **Cross-artifact analyze** | spec-kit | Implemented as the `gdd.trace.validate` skill — reads `specs/*.md`, builds RTM, reports gaps (URS-XXX-NNN without FS counterpart, FS orphans, RA coverage gaps, etc.). |
| **Propose-default interaction principles** | bm-prd-creator | Four principles baked into every interactive skill (starting with `gdd.urs.from-idea`): (1) always propose a sensible default *with reasoning* then ask to confirm/change — never ask open-ended "what do you want?"; (2) use `AskUserQuestion` for discrete choices, free text only for brain-dump; (3) one decision (or tight cluster) at a time, lock before advancing; (4) adapt interview depth to the idea (compress simple, expand complex). The user edits a proposal far better than they generate from scratch. |
| **Step-file skill decomposition** | bm-prd-creator | A skill's `SKILL.md` is a thin orchestrator that lists phases; each phase lives in its own `steps/<phase>.md` read lazily only when that phase runs. Keeps the agent's working context minimal per step. Our operative skills adopt the `SKILL.md` + per-phase-file structure. |
| **Milestone-log handoff format** | bm-prd-creator | After each cascade step / build chunk, the agent writes a log whose **top section is human-readable** ("what's new — capabilities a non-technical reviewer will now see") followed by implementation detail for the *next* agent: what was built, decisions not pre-specified in the spec, deviations and why. Aligns our per-step logs with the consumer's `STATE.md` continuity contract. |

### 🟡 Cat B — Round 2 (post-`v0.1.0`, target `v0.5.0`)

These polish the toolkit and broaden its applicability.

| Concept | From | How we adopt it |
|---|---|---|
| **Profiles with inheritance** | agent-os | `profiles/{pharma, medical-device, finance, aerospace, nuclear, general}/profile.yaml` with `inherits_from: default`. Activate via `profile:` field in `.gxp-dev.yaml`. |
| **Named agent personas mapped to GAMP §6.2.3 roles** | bmad-method | When `profile: pharma`: personas like *Quality Unit*, *Process Owner*, *Subject Matter Expert*, *System Owner* map 1:1 to the GAMP §6.2.3 roles. Generic profiles map to dev roles (architect, dev, tester, reviewer, devops, security). |
| **CSV-based help router** | bmad-method | `docs/help-router.csv` with `question, skill, prerequisites, output` columns. Auditor-friendly, diff-friendly, no embedding dependencies. |
| **Diátaxis docs structure** | bmad-method | `docs/{tutorials, how-to, reference, explanation}/` split. Serves all four learning modes simultaneously for heterogeneous audiences (devs, QA, auditors, regulators, founders). |
| **Gates canonical: Confirm / Quality / Safety / Transition** | gsd-build | Adapted to consumer-facing semantics: **Quality** = peer SME review, **Safety** = Data Integrity / 21 CFR §11.10 check, **Transition** = Process Owner sign-off, **Confirm** = Quality Unit approval (GAMP §6.2.3). |
| **Runtime adapters: Cursor, Codex, Windsurf** | spec-kit | At `v0.5.0` we add per-runtime adapters that translate the same skill across Claude Code → Cursor rules → Codex `AGENTS.md`. Markdown-first design makes this an adapter shim, not a port. |
| **Milestone breakout with granularity options** | bm-prd-creator | When sequencing a build, the skill proposes a default milestone breakout plus 2 alternatives (fewer/bigger vs more/smaller) via `AskUserQuestion`, explains the tradeoff in plain language (fewer = larger one-shot sessions, more risk; more = more checkpoints, slower), and requires each milestone to deliver visible, testable functionality and fit one self-contained agent session with explicit "Done when" criteria. Refines our cascade sequencing; **also adopted as our dogfooding discipline** for building the toolkit itself (small chunks, fresh context per chunk). |
| **Managed-instruction-block injection** | bm-design-system | The `init-project` skill injects our anti-hallucination guardrails into the consumer's `CLAUDE.md`/`AGENTS.md` between idempotent `<!-- gdd:start --> … <!-- gdd:end -->` markers, updatable non-destructively on re-run. Philosophy mirrors bm-design-system's "always check the canonical catalog first, never invent ad-hoc, propose additions to the catalog rather than one-offs" — which is literally our anti-hallucination rule (never invent IDs or regulatory citations). |
| **Plugin-marketplace packaging** | bm-skills | Distribute the toolkit as a Claude Code plugin marketplace (`.claude-plugin/marketplace.json` + per-plugin `plugin.json` + `/plugin install`). Adopt their naming discipline (name must match in folder + `plugin.json` + marketplace entry + `SKILL.md` frontmatter) and per-commit version-bump rule. Target `v0.5.0` distribution. |

### 🔵 Cat C — Roadmap (post-`v0.5.0`)

These are powerful but not blocking for early adoption.

| Concept | From | How we adopt it |
|---|---|---|
| **eQMS bridge: TasksToIssues** | spec-kit | A `/gdd.export-to-eqms` skill family targeting TrackWise, Veeva Vault QA, MasterControl. Convert approved CC/IR/PR records into upstream tickets. |
| **Wave-based parallelism** | gsd-build | For large projects, multiple skills run in parallel waves with dependency-aware scheduling. |
| **Multi-runtime auto-translation** | spec-kit | Automatic skill format conversion (write once in markdown, install everywhere). |
| **Continue-here handoff** | gsd-build | `continue-here.md` pattern for session-to-session handoff (we already use STATE.md for this, but a more granular per-skill state could help). |
| **Discuss-phase / verify-work / UI-spec / drift detection** | gsd-build | Optional sub-skills for high-rigor projects. |
| **Self-contained HTML "validation dossier" output** | bm-prd-creator | An optional output mode that renders locked specs (URS + RA + RTM + VR) into a single self-contained, print-friendly, dark-mode HTML page (Tailwind CDN + Lucide, no build step) — a presentation layer over the locked markdown, for auditors/QA who don't read raw markdown. Ports `bm-prd-creator`'s `prd.html` pattern. Decision deferred to **ADR-001** (see `docs/decisions/`). |

### 🟣 Cat D — Innovations unique to us (no precedent in studied frameworks)

These are differentiators that ship as part of the `v0.1.0`–`v1.0.0` arc.

| Innovation | Why it matters |
|---|---|
| **Multi-industry anchor system** | A single template (e.g. `URS.md`) carries anchors to multiple regulatory frameworks (GAMP 5 for pharma, IEC 62304 for medical devices, DO-178C for aerospace, ISO 26262 for automotive, SOX for finance) — the active anchors switch based on `profile:` in the manifest. |
| **Rigor levels (`light` / `standard` / `strict` / `regulated`)** | Consumer picks how much rigor to apply. Light = freelance MVP. Standard = enterprise B2B. Strict = startup in regulated market. Regulated = full FDA/EMA-grade. The same templates scale via validation_rules + presets. |
| **Spec → code traceability** | The AI agent that implements code from approved FS can annotate commits and code comments with the FS-XXX-NNN it implements. A `/gdd.trace.code` skill verifies the bidirectional link. |
| **Compliance bundles as build artifact** | `compliance-bundle/` directory assembled on demand. Static, inspector-friendly, frozen at bundle time. Lower-friction alternative to uploading specs to corporate eQMS. |
| **Cross-domain pattern library** | Patterns like FMEA, V-Model, Constitution, Criticality Assessment shared across profiles with profile-specific overlays. One canonical pattern, multiple implementations. |
| **Generative cascade** | The whole "idea → URS → FS → RA → tests → code → bundle" pipeline as a first-class concept, with each step a discrete skill and explicit human checkpoints. |

---

## Framework 1 — github/spec-kit

### What it is

GitHub's official toolkit for **spec-driven software development**. Articulates a 7-state lifecycle: *constitution → specify → clarify → plan → tasks → analyze → implement*. Templates are Markdown with `[BRACKET]` placeholders. Skills are invoked via `/speckit.*` slash commands. Supports 30+ runtimes (Claude Code, Cursor, Codex, Windsurf, Aider, etc.) through adapters. **The most viral spec-driven framework** as of mid-2026 (~105k stars).

### What we adopt

- **Constitution pattern** → `templates/csv/VMP.md` doubles as the consumer's immutable principles file (Cat A).
- **`[NEEDS CLARIFICATION: …]` markers** → canonical convention (Cat A).
- **Cross-artifact `/analyze`** → `gdd.trace.validate` skill (Cat A).
- **Slash command namespace** → `/gdd.*` convention (Cat A).
- **Runtime adapters** → planned for `v0.5.0` to reach Cursor, Codex, Windsurf (Cat B).
- **Numbered feature folders philosophy** → adapted (we use one `specs/` folder for one system, files named by acronym, not by number).

### What we reject

- **`[BRACKET]` placeholders without type information** → we use richer **typed declarative placeholders** in YAML frontmatter (`type: enum | string | …`, `required: true|false`, `description`, `pattern`, `values`).
- **No YAML frontmatter in templates** → we mandate frontmatter as machine-readable contract.
- **No consumer-level manifest** → we ship `.gxp-dev.yaml` as the declarative root.

### Surprise

spec-kit's adapter system translates the same slash command across 30+ runtimes by remapping tool names and hook events. **This is exactly the agnosticism property we want** for our skills layer. Worth studying in detail before designing our adapter layer in `v0.5.0`.

---

## Framework 2 — gsd-build/get-shit-done

### What it is

A multi-agent meta-prompting framework that solves **"context rot"** by spawning sub-agents with fresh 200K-token windows. State lives in a `.planning/` folder as **markdown files** (`STATE.md`, `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`) — inspectable, commitable, recoverable. 101 user-facing commands, 125 orchestration workflows, 34 specialized agents. Mature framework but suffering from **bloat** (some workflow files are 87 KB; CHANGELOG.md is 196 KB).

### What we adopt

- **STATE.md pattern** → core (Cat 0). Both this toolkit and consumer projects use it.
- **Fresh-context-per-agent** → core (Cat 0). Skills that spawn sub-agents give them clean context.
- **Plan-checker loop** → core (Cat 0). Drafts reviewed before commit; max iterations bounded.
- **Slopcheck / package legitimacy gate** → core (Cat 0). Skills must validate package existence and authenticity before suggesting `npm install` / `pip install`.
- **Four canonical gate types** (Confirm/Quality/Safety/Transition) → adapted to pharma semantics (Cat B).
- **`config.json` manifest principle (with "absent = enabled" → inverted to "absent = strictest")** → applied to `.gxp-dev.yaml` for audit-safe defaults.
- **Phase lifecycle with explicit states** → maps directly to V-Model phases + generative cascade states.

### What we reject

- **Bloat: 87 KB workflow files, 101 commands, 196 KB CHANGELOG.** Hard ceilings in this toolkit: ≤ 1000 lines per template, ≤ 15-20 skills total, CHANGELOG follows Keep-a-Changelog convention.
- **Contradictory documentation** (root README says "moved to redux" but repo is active). Our README is authoritative; no stub docs.
- **Two-stage hierarchical routing for command discovery** — interesting at GSD's scale (101 commands) but unnecessary at ours.

### Surprise

GSD has a `gsd-nyquist-auditor` agent and a `nyquist_validation` config flag — they borrow the **Nyquist–Shannon sampling theorem** as a metaphor for test coverage. The argument: your test suite must "sample" the system's behavior space at frequency ≥ 2× the Nyquist frequency of its failure modes. **This mathematical framing might be powerful for our `SEC-TEST` and `PERF-TEST` templates** — defending "what constitutes sufficient OQ test coverage" to an auditor with sampling-theoretic argument is more rigorous than "best judgment". Roadmap consideration.

---

## Framework 3 — bmad-code-org/bmad-method

### What it is

A structured agent collaboration methodology with **named agent personas** (e.g., *"Mary, Business Analyst"*, *"John, Project Manager"*). Each persona has a menu of skills they can perform. Lifecycle has 4 phases: *Analysis → Planning → Solutioning → Implementation*. Notable for its **CSV-based help router** (`module-help.csv` with `Q → skill_name`) — auditable, diff-friendly, no embeddings needed.

### What we adopt

- **Named agent personas** → Round 2 (Cat B). When `profile: pharma`, personas map 1:1 to GAMP §6.2.3 canonical roles (Quality Unit, Process Owner, etc.). Generic profiles get dev roles (architect, developer, tester, reviewer, devops, security).
- **CSV-based help router** → `docs/help-router.csv` (Cat B). Inspector-friendly, no LLM embeddings dependency.
- **Diátaxis docs structure** → `docs/{tutorials, how-to, reference, explanation}/` (Cat B).
- **Modular registry** → borrowed for **profile inheritance**: `profiles/<name>/profile.yaml` declares `inherits_from: default`.

### What we reject

- **Branding incoherence** ("BMAD" capitalization varies across docs). We maintain one consistent project name.
- **Mixed runtime stack (Node + Python)** — increases install friction. Our toolkit is **markdown-and-YAML-first** with optional Python 3.12+ scripts that ship separately.
- **Heavy persona ceremony for trivial actions.** We use personas only where GAMP role mapping adds clarity (review, approve, sign), not for routine instantiation.

### Surprise

The CSV-based help router is **wildly underrated**. Most teams reach for vector DBs and embeddings for "intent → tool" routing. A flat CSV with `question, skill` columns gives you: diffability, auditability, no LLM dependency, instant intelligibility for non-engineers, and zero infra. For a regulated domain where auditors want to trace exactly how the AI decided to invoke a particular skill, a CSV is **more defensible** than an embedding-based router.

---

## Framework 4 — buildermethods/agent-os

### What it is

A lightweight standards/context router for AI agents. The central artifact is `index.yml` — a small file that maps standard names to their files and metadata. Agents read the index to know **which standards exist** without reading every standard file. Deliberately minimal, designed to be **embedded into other systems** rather than used standalone.

### What we adopt

- **Lightweight index as context router** → `.gxp-dev.yaml` manifest plays this role (Cat 0). An agent reads it first to know which templates are active, which presets are on, what category applies.
- **Profiles with inheritance (`inherits_from`)** → `profiles/<name>/` structure (Cat B). Each profile inherits from `default` and overrides only what differs.
- **Designed for embedding** → philosophical influence: `gxp-driven-dev` drops into any consumer project without forcing restructure. Consumer keeps their `src/`, `tests/`, etc.; we add `specs/`, `evidence/`, `.gxp-dev.yaml`.

### What we reject

- **Standards without frontmatter** — agent-os's standard files are plain Markdown without YAML frontmatter; the index is the only structured part. We require frontmatter in every template, pattern, and skill — the alternative is fragile string parsing.

### Surprise

agent-os deliberately does **less** than every other framework we studied. It's not a methodology, not a multi-agent system, not a workflow engine — just a way to make standards discoverable. **This minimalism is enviable**. Reminds us: most of `gxp-driven-dev` should be **inert content** (templates, schemas, patterns), and the **active layer** (skills) should be as small and orthogonal as possible.

---

## Framework 5 — buildermethods/bm-skills + build-new

### What it is

Brian Casel's (Builder Methods) public toolset for "spec-driven development" aimed at **non-technical business builders**. Two pieces:

- **`build-new`** — a Rails 8 + Inertia + React 19 starter boilerplate (the author's personal stack), shipped with a complete design system and opinionated agent-governance instructions in `CLAUDE.md`.
- **`bm-skills`** — a Claude Code **plugin marketplace**. Its crown jewel is **`bm-prd-creator`**: a `user_invocable` skill that walks a non-technical user through a structured interview (brain-dump → format → core-purpose → top-features → out-of-scope → tech-stack → integrations → data-model → per-feature scoping → milestones → write-files) and emits a PRD (markdown and/or a self-contained HTML page) plus a sequence of milestone `prompt.md` trigger files for a coding agent. Companion skills: `bm-design-system`, `bm-favicon-creator`.

The thesis (from the accompanying video *"You don't need to learn to code anymore"*): the durable skill is becoming a **confident product architect** who gives AI clear direction — *"vibe coding is asking AI to pull off magic tricks; professional builders give AI clear direction so it builds the right thing the first time."* Shape: **idea → spec (PRD) → milestones → build**, plan-mode per milestone, milestone-logs as memory.

> [!tip] Why this matters most of the five
> A 20-year developer **independently arrived at our exact core thesis** (spec as authoritative *what*-context, anti-guessing, milestone decomposition, logs-as-memory) and shipped the *lite* version. This is strong external validation that our architecture is sound — and it makes our differentiator legible: everything `bm-prd-creator` lacks (typed frontmatter, RTM, regulatory anchoring, full V-Model + risk assessment, formal anti-hallucination invariants, multi-profile manifest) is precisely the audit-grade gap we fill.

### What we adopt

- **"What vs how" boundary as first-class principle** → core (Cat 0). Articulated with worked examples; language imported into `docs/methodology.md`.
- **Propose-default interaction principles** (4) → Round 1 (Cat A), applied immediately to `gdd.urs.from-idea`'s `interview-flow.md`.
- **Step-file skill decomposition** → Round 1 (Cat A). Thin `SKILL.md` orchestrator + lazy-loaded `steps/<phase>.md`.
- **Milestone-log handoff format** ("what's new" human section + implementation detail for next agent) → Round 1 (Cat A).
- **Milestone breakout with 3 granularity options + "Done when" criteria** → Round 2 (Cat B); also our **dogfooding discipline** for building the toolkit in small, fresh-context chunks.
- **Managed-instruction-block injection** (bm-design-system) → Round 2 (Cat B). Mechanism for our `init-project` skill to inject anti-hallucination guardrails into the consumer's `CLAUDE.md`.
- **Plugin-marketplace packaging + naming discipline** → Round 2 (Cat B). Our `v0.5.0` distribution path.
- **Self-contained HTML dossier output** → Roadmap (Cat C). Deferred to **ADR-001**.

### What we reject

- **Single-stack lock-in** (Rails + Inertia only). `build-new` hard-codes one stack; we are stack- and runtime-agnostic via `.gxp-dev.yaml`.
- **Prose-only specs with no machine-readable contract.** The PRD is pure markdown/HTML — zero typed frontmatter, no requirement IDs, no RTM, no validation scripts. We mandate typed frontmatter + RTM + lint scripts (this is our audit-grade differentiator, not a nice-to-have).
- **The `_build_plan/`-is-ephemeral default.** `bm-prd-creator` marks the PRD as a *temporary* scaffold to be deleted after shipping. For us the opposite holds for compliance artifacts (URS, VR = permanent audit record). This forces a design distinction we did not previously have — see **ADR-002** (durable vs ephemeral artifacts).
- **No compliance / regulatory dimension at all.** Expected for a general-audience tool; noted only to mark the boundary.

### Surprise

`bm-prd-creator` is **structurally almost identical to our `gdd.urs.from-idea`** — the skill we have built but *never run end-to-end* (our STATE.md's #1 risk). It is, in effect, a working reference implementation of our own front-of-funnel, by an author with 20 years of product experience. The cleanest possible de-risking of our smoke test is to study its phase ordering and interaction principles first — which is exactly why principles #1–#4 were merged into our `interview-flow.md` **before** running the smoke test.

A second surprise from the video: Casel deliberately designs his tools with **two interfaces — a UI for the human and an API+skill for his agents** ("the night shift"). For a toolkit whose consumers build software *with* AI agents, "is this system agent-operable?" is worth surfacing as a first-class URS prompt (candidate for `URS-API` / `URS-FUNC` interview coverage).

---

## Anti-patterns we are NOT copying (consolidated)

A consolidated list of "don'ts" gleaned from the four frameworks, applied as hard rules in our codebase:

| Anti-pattern | Source | Why we avoid it |
|---|---|---|
| Standards without frontmatter | agent-os | Fragile parsing; AI can't reliably extract structure |
| Branding incoherence | bmad-method | Confuses users; undermines documentation |
| Placeholders without type info (`[BRACKET]`) | spec-kit | AI agents cannot validate or interactively fill |
| Mixed runtime stack | bmad-method | Install friction in regulated environments |
| Bloated workflows (87 KB files) | gsd-build | Symptom of governance loss; unmaintainable |
| 101+ commands without two-stage routing | gsd-build | Cognitive overload for users |
| Contradictory documentation (README says X, repo does Y) | gsd-build | Erodes trust |
| Commercial product disguised as open-source | (industry pattern) | Violates community expectations |
| Inheriting category codes from a single corporate template catalog | (general) | Locks in confidentiality risk; we built our own 22 acronyms |
| Single-stack lock-in (boilerplate hard-codes one framework) | build-new | Limits audience to one tech choice; we stay stack-agnostic via `.gxp-dev.yaml` |
| Prose-only specs with no machine-readable contract | bm-prd-creator | No typed frontmatter / IDs / RTM → no automated traceability or audit-grade verification |

---

## How this document evolves

This file is **versioned with the toolkit**. When we adopt a new framework lesson, reject a previously-adopted one, discover a new anti-pattern, or promote/demote items in the adoption matrix, we update this file and commit it as part of the change. Future inspectors and contributors read it to understand **why** the toolkit is shaped the way it is — not just what it does.
